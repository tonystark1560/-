#!/usr/bin/env python3
"""Новостной Short про CS2 без своей записи: фон из официальных видео Valve + озвучка + текст.

    python3 make_news_short.py shorts/02-silent-reload.json

spec.json:
{
  "out": "../out/02-silent-reload.mp4",
  "bg": ["../raw/valve/impacts.mp4"],     # фоновые видео, идут по кругу
  "headline": "ТИХАЯ ПЕРЕЗАРЯДКА",        # заголовок сверху на всё видео
  "source": "Источник: обновление CS2 от 22.09.2026",
  "lines": [                              # каждая строка озвучивается и показывается субтитром
    {"say": "В CS2 теперь можно перезаряжаться бесшумно."},
    {"say": "...", "text": "своя подпись, если отличается от озвучки"}
  ],
  "speed": 1.2                            # ускорение озвучки
}

Озвучка — Google TTS (gTTS). Нужны ffmpeg с libass и `pip install gTTS`.
"""
import json, os, subprocess, sys, tempfile

W, H, FPS = 1080, 1920, 30
FONT = "Inter"
GAP = 0.15


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(" ".join(cmd[:3]) + "\n" + r.stderr[-2000:])
    return r.stdout


def duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).strip())


def ts(sec):
    m, s = divmod(sec, 60)
    return f"0:{int(m):02d}:{s:05.2f}"


def tts(text, path, speed):
    os.environ.setdefault("REQUESTS_CA_BUNDLE", "/root/.ccr/ca-bundle.crt") if os.path.exists("/root/.ccr/ca-bundle.crt") else None
    from gtts import gTTS
    raw = path + ".raw.mp3"
    gTTS(text, lang="ru").save(raw)
    run(["ffmpeg", "-y", "-i", raw, "-af", f"atempo={speed},apad=pad_dur={GAP}", "-ar", "44100", "-ac", "2", path])


def main():
    spec_path = sys.argv[1]
    base = os.path.dirname(os.path.abspath(spec_path))
    spec = json.load(open(spec_path, encoding="utf-8"))
    out = os.path.normpath(os.path.join(base, spec["out"]))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        # озвучка по строкам — так знаем точное время каждого субтитра
        wavs, events, t = [], [], 0.0
        for i, line in enumerate(spec["lines"]):
            p = os.path.join(tmp, f"l{i}.wav")
            tts(line["say"], p, spec.get("speed", 1.2))
            d = duration(p)
            events.append((t, t + d, line.get("text", line["say"])))
            wavs.append(p)
            t += d
        total = t
        lst = os.path.join(tmp, "a.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in wavs))
        voice = os.path.join(tmp, "voice.wav")
        # громкость под Shorts: -14 LUFS, как у большинства роликов в ленте
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-af", "loudnorm=I=-14:TP=-1:LRA=7", "-ar", "44100", voice])

        # фон: видео Valve по кругу до длины озвучки
        bl = os.path.join(tmp, "bg.txt")
        bgs = [os.path.normpath(os.path.join(base, b)) for b in spec["bg"]]
        reps = int(total // sum(duration(b) for b in bgs)) + 2
        open(bl, "w").write("".join(f"file '{b}'\n" for _ in range(reps) for b in bgs))

        ass = os.path.join(tmp, "s.ass")
        rows = [
            "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0", "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Alignment, "
            "MarginL, MarginR, MarginV, BorderStyle, Outline, Shadow",
            f"Style: Head,{FONT},104,&H0000E5FF,&H00000000,&H00000000,-1,8,60,60,250,1,9,0",
            f"Style: Cap,{FONT},72,&H00FFFFFF,&H00000000,&H00000000,-1,8,90,90,1180,1,7,0",
            f"Style: Src,{FONT},34,&H00CCCCCC,&H00000000,&H00000000,0,8,60,60,520,1,3,0",
            "", "[Events]", "Format: Layer, Start, End, Style, Text",
            f"Dialogue: 2,{ts(0)},{ts(total)},Head,{spec['headline']}",
        ]
        if spec.get("source"):
            rows.append(f"Dialogue: 1,{ts(0)},{ts(total)},Src,{spec['source']}")
        rows += [f"Dialogue: 0,{ts(a)},{ts(b)},Cap,{txt}" for a, b, txt in events]
        open(ass, "w", encoding="utf-8").write("\n".join(rows) + "\n")

        vf = (f"[0:v]fps={FPS},split[a][b];"
              f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=25:2,eq=brightness=-0.15[bg];"
              f"[b]scale={W}:-2[fg];[bg][fg]overlay=0:(H-h)/2-60,setsar=1,ass={ass}[v]")
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", bl, "-i", voice, "-filter_complex", vf,
             "-map", "[v]", "-map", "1:a", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "21",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out])
    print(f"{out}  {total:.1f} с")


if __name__ == "__main__":
    main()
