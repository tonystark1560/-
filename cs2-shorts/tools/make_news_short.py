#!/usr/bin/env python3
"""Новостной Short про CS2 без своей записи игры.

Фон — официальные видео Valve, нейроозвучка Silero, субтитры по словам с подсветкой,
переходы между фразами (вспышка, зум, сдвиг) со звуком, звуки CS на ключевых фразах.

    python3 make_news_short.py shorts/01-silent-reload.json

spec.json:
{
  "out": "../out/01-silent-reload.mp4",
  "bg": ["../raw/valve/impacts.mp4"],       # фоновые видео, нарезаются по фразам
  "headline": "ТИХАЯ ПЕРЕЗАРЯДКА",
  "source": "Источник: обновление CS2 · Valve, 22.09.2026",
  "voice": "aidar",                          # aidar, eugene (м), baya, kseniya, xenia (ж)
  "lines": [
    {"text": "В CS2 теперь можно перезаряжаться бесшумно.",   # субтитр
     "say":  "В кс два теперь можно перезаряжаться бесшумно.", # как читать (только кириллица и числа словами)
     "sfx":  "go-go-go"}                                       # звук из raw/sfx в начале фразы
  ]
}

Нужно: ffmpeg с libass, torch (CPU) и модель raw/models/v5_6_ru.pt (https://models.silero.ai/models/tts/ru/v5_6_ru.pt).
Ударения для сленга — tools/stress.json; проверить, как модель прочитает фразы: tools/check_stress.py.
"""
import json, os, re, subprocess, sys, tempfile

W, H, FPS = 1080, 1920, 30
FONT = "Inter"
XF = 0.3              # длина перехода, с
PAD = 0.12            # пауза после фразы, с
SPEED = 1.08          # ускорение голоса
# обработка голоса: срез гула, меньше «бубнения», больше разборчивости, компрессор, де-эссер, лёгкая комната
VOICE_FX = ("highpass=f=75,equalizer=f=250:t=q:w=1:g=-2.5,equalizer=f=3500:t=q:w=1.2:g=2.5,"
            "equalizer=f=9000:t=q:w=1:g=1.5,acompressor=threshold=-20dB:ratio=3:attack=5:release=90:makeup=2,"
            "deesser=i=0.35,aecho=0.9:0.7:22|37:0.10|0.06")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SFX = os.path.join(ROOT, "raw", "sfx")
MODEL = os.path.join(ROOT, "raw", "models", "v5_6_ru.pt")
STRESS = json.load(open(os.path.join(HERE, "stress.json"), encoding="utf-8"))
TRANSITIONS = ["fadewhite", "zoomin", "slideleft", "circleopen", "pixelize", "slideup", "radial", "smoothleft"]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(" ".join(cmd[:4]) + "\n" + r.stderr[-2500:])
    return r.stdout


def duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).strip())


def ts(sec):
    m, s = divmod(max(sec, 0), 60)
    return f"0:{int(m):02d}:{s:05.2f}"


def load_tts():
    import torch
    m = torch.package.PackageImporter(MODEL).load_pickle("tts_models", "model")
    m.to("cpu")
    return m


def stressed(text):
    """Подставить ударения из stress.json для сленга и названий, которые модель читает неверно."""
    def fix(m):
        w = m.group(0)
        return STRESS.get(w.lower(), w)
    return re.sub(r"[A-Za-zА-Яа-яЁё0-9]+", fix, text)


def say(model, text, voice, path):
    raw = path + ".raw.wav"
    model.save_wav(text=stressed(text), speaker=voice, sample_rate=48000, audio_path=raw)
    run(["ffmpeg", "-y", "-i", raw, "-af", f"{VOICE_FX},atempo={SPEED},apad=pad_dur={PAD}", "-ar", "48000", "-ac", "2", path])


def word_events(start, dur, text):
    """Субтитр по словам: куски до 3 слов, текущее слово жёлтое и «подпрыгивает»."""
    words = text.upper().split()
    speak = max(dur - PAD, 0.3)
    weights = [len(re.sub(r"\W", "", w)) + 2 for w in words]
    total = sum(weights)
    times, t = [], start
    for wgt in weights:
        times.append((t, t + speak * wgt / total))
        t += speak * wgt / total
    out = []
    for c0 in range(0, len(words), 3):
        chunk = list(range(c0, min(c0 + 3, len(words))))
        for i in chunk:
            parts = []
            for j in chunk:
                if j == i:
                    parts.append(r"{\c&H0000E5FF&\fscx118\fscy118\t(0,90,\fscx100\fscy100)}" + words[j] + r"{\c&H00FFFFFF&}")
                else:
                    parts.append(words[j])
            a, b = times[i]
            if i == chunk[-1] and c0 + 3 >= len(words):
                b = start + dur
            out.append(f"Dialogue: 0,{ts(a)},{ts(b)},Cap,{' '.join(parts)}")
    return out


def main():
    spec_path = sys.argv[1]
    base = os.path.dirname(os.path.abspath(spec_path))
    spec = json.load(open(spec_path, encoding="utf-8"))
    out = os.path.normpath(os.path.join(base, spec["out"]))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    lines = spec["lines"]
    model = load_tts()
    with tempfile.TemporaryDirectory() as tmp:
        # 1. голос по фразам
        wavs, durs = [], []
        for i, ln in enumerate(lines):
            p = os.path.join(tmp, f"v{i}.wav")
            say(model, ln.get("say", ln["text"]), spec.get("voice", "aidar"), p)
            wavs.append(p)
            durs.append(duration(p))
        starts = [sum(durs[:i]) for i in range(len(durs))]
        total = sum(durs) + XF

        # 2. фон: на каждую фразу свой кусок видео, вертикаль с размытым фоном и медленным наездом
        bgs = [os.path.normpath(os.path.join(base, b)) for b in spec["bg"]]
        bg_len = {b: duration(b) for b in bgs}
        segs, cursor = [], {b: 0.0 for b in bgs}
        for i, d in enumerate(durs):
            b = bgs[i % len(bgs)]
            seg_len = d + XF
            st = cursor[b] if cursor[b] + seg_len <= bg_len[b] else 0.0
            cursor[b] = st + seg_len
            p = os.path.join(tmp, f"s{i}.mp4")
            vf = (f"fps={FPS},split[a][b];"
                  f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=25:2,eq=brightness=-0.18[bg];"
                  f"[b]scale={W}:-2,zoompan=z='1+0.07*on/({seg_len:.2f}*{FPS})':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':"
                  f"d=1:s={W}x{W * 9 // 16}:fps={FPS}[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-60,setsar=1")
            loop = ["-stream_loop", "-1"] if seg_len > bg_len[b] else []
            run(["ffmpeg", "-y", *loop, "-ss", f"{st:.2f}", "-i", b, "-t", f"{seg_len:.2f}", "-filter_complex", vf,
                 "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", p])
            segs.append(p)

        # 3. субтитры
        ass = os.path.join(tmp, "s.ass")
        rows = [
            "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0", "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Alignment, "
            "MarginL, MarginR, MarginV, BorderStyle, Outline, Shadow",
            f"Style: Head,{FONT},100,&H00FFFFFF,&H00000000,&H96000000,-1,8,60,60,240,1,9,4",
            f"Style: Cap,{FONT},98,&H00FFFFFF,&H00000000,&H96000000,-1,8,70,70,1200,1,10,5",
            f"Style: Src,{FONT},34,&H00CCCCCC,&H00000000,&H00000000,0,8,60,60,500,1,3,0",
            "", "[Events]", "Format: Layer, Start, End, Style, Text",
            f"Dialogue: 2,{ts(0)},{ts(total)},Head,"
            r"{\fscx60\fscy60\t(0,180,\fscx108\fscy108)\t(180,300,\fscx100\fscy100)\c&H0000E5FF&}" + spec["headline"],
        ]
        if spec.get("source"):
            rows.append(f"Dialogue: 1,{ts(0)},{ts(total)},Src,{spec['source']}")
        for i, ln in enumerate(lines):
            rows += word_events(starts[i], durs[i], ln["text"])
        open(ass, "w", encoding="utf-8").write("\n".join(rows) + "\n")

        # 4. склейка: переходы между фразами + субтитры
        inputs, fc, prev = [], [], "0:v"
        for p in segs:
            inputs += ["-i", p]
        for i in range(1, len(segs)):
            tr = TRANSITIONS[(i - 1) % len(TRANSITIONS)]
            fc.append(f"[{prev}][{i}:v]xfade=transition={tr}:duration={XF}:offset={starts[i]:.3f}[x{i}]")
            prev = f"x{i}"
        fc.append(f"[{prev}]ass={ass}[v]")
        video = os.path.join(tmp, "video.mp4")
        run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[v]", "-c:v", "libx264",
             "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", video])

        # 5. звук: голос + свист на каждом переходе + звуки CS на фразах
        lst = os.path.join(tmp, "a.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in wavs))
        voice = os.path.join(tmp, "voice.wav")
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-af", "loudnorm=I=-14:TP=-1:LRA=7",
             "-ar", "48000", voice])
        fx = [(max(starts[i] - 0.15, 0), "whoosh.wav", 0.5) for i in range(1, len(lines))]
        fx += [(starts[i], ln["sfx"] + ".mp3", 0.45) for i, ln in enumerate(lines) if ln.get("sfx")]
        ain, amix = ["-i", voice], ["[0:a]volume=1.0[a0]"]
        for k, (t0, name, vol) in enumerate(fx, 1):
            ain += ["-i", os.path.join(SFX, name)]
            amix.append(f"[{k}:a]atrim=0:1.8,afade=t=out:st=1.5:d=0.3,volume={vol},"
                        f"aresample=48000,adelay={int(t0 * 1000)}:all=1[a{k}]")
        amix.append("".join(f"[a{k}]" for k in range(len(fx) + 1)) +
                    f"amix=inputs={len(fx) + 1}:normalize=0:duration=first,alimiter=limit=0.95[a]")
        audio = os.path.join(tmp, "audio.m4a")
        run(["ffmpeg", "-y", *ain, "-filter_complex", ";".join(amix), "-map", "[a]", "-c:a", "aac", "-b:a", "192k", audio])

        run(["ffmpeg", "-y", "-i", video, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy",
             "-shortest", "-movflags", "+faststart", out])
    print(f"{out}  {total:.1f} с")


if __name__ == "__main__":
    main()
