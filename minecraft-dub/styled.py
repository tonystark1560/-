#!/usr/bin/env python3
"""Закадровая озвучка в стиле «мем-шортс»: свой текст поверх ролика,
субтитры по одному слову (жёлтые, заглавные, с обводкой), размытые поля сверху/снизу.

    python styled.py video.mp4 scripts/sulfur_cube.json -o out/sulfur_cube_ru.mp4

Формат JSON-сценария:
    {"voice": "ru-RU-DmitryNeural", "rate": 10, "pitch": 0,
     "lines": [{"t": 0.0, "text": "Первая фраза"}, {"t": 2.6, "text": "Вторая"}]}
"t" — секунда, с которой начинается фраза. Фраза должна закончиться до следующей,
иначе речь автоматически ускоряется.
"""
import argparse
import asyncio
import json
import os
import re
import ssl
import subprocess
from pathlib import Path

W, H = 1080, 1920
BAND = 1210  # высота резкой полосы по центру, остальное — размытый фон


def run(cmd):
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-2000:])


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "json", str(path)], check=True, capture_output=True, text=True).stdout
    return float(json.loads(out)["format"]["duration"])


def _ssl_fix():
    import edge_tts.communicate as c

    ca = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if ca and Path(ca).exists():
        c._SSL_CTX = ssl.create_default_context(cafile=ca)


async def _tts(text, voice, rate, pitch, out):
    """Озвучивает фразу и возвращает тайминги слов [(старт, конец, слово)] в секундах."""
    import edge_tts

    com = edge_tts.Communicate(text, voice, rate=f"{rate:+d}%", pitch=f"{pitch:+d}Hz",
                               boundary="WordBoundary",
                               proxy=os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy"))
    words = []
    with open(out, "wb") as f:
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                s = chunk["offset"] / 1e7
                words.append((s, s + chunk["duration"] / 1e7, chunk["text"]))
    return words


def voice_lines(lines, work, voice, base_rate, pitch, video_len, max_rate=60):
    _ssl_fix()
    clips = []
    for i, ln in enumerate(lines):
        slot = (lines[i + 1]["t"] if i + 1 < len(lines) else video_len) - ln["t"] - 0.1
        mp3 = work / f"line_{i:02}.mp3"
        rate = base_rate
        words = asyncio.run(_tts(ln["text"], voice, rate, pitch, mp3))
        d = duration(mp3)
        if d > slot:
            rate = min(int((1 + base_rate / 100) * d / slot * 100 - 100) + 3, max_rate)
            words = asyncio.run(_tts(ln["text"], voice, rate, pitch, mp3))
            d = duration(mp3)
        clip, k = mp3, 1.0
        if d > slot:  # дожимаем, если даже на максимальной скорости не влезло
            k = min(d / slot, 1.5)
            clip = work / f"line_{i:02}_fit.wav"
            run(["ffmpeg", "-y", "-i", str(mp3), "-filter:a", f"atempo={k:.3f}", str(clip)])
            words = [(a / k, b / k, w) for a, b, w in words]
            d /= k
        print(f"  {ln['t']:5.1f}s  [{d:.1f}/{slot:.1f}s, rate {rate:+d}%]  {ln['text']}")
        clips.append({"t": ln["t"], "path": clip, "dur": d,
                      "words": [(ln["t"] + a, ln["t"] + b, w) for a, b, w in words]})
    return clips


def ass_time(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}"


def write_ass(clips, path, font):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Word,{font},100,&H0000D2FF,&H0000D2FF,&H00000000,&H64000000,1,0,0,0,100,100,1,0,1,7,3,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    for c in clips:
        words = [(a, b, re.sub(r"[^\w\-]", "", w).upper()) for a, b, w in c["words"]]
        words = [x for x in words if x[2]]
        line_end = c["t"] + c["dur"]
        for j, (a, b, w) in enumerate(words):
            end = words[j + 1][0] if j + 1 < len(words) else max(b, line_end) + 0.15
            pop = r"{\pos(%d,%d)\fscx75\fscy75\t(0,90,\fscx105\fscy105)\t(90,150,\fscx100\fscy100)}" % (W // 2, int(H * 0.6))
            ev.append(f"Dialogue: 0,{ass_time(a)},{ass_time(end)},Word,,0,0,0,,{pop}{w}")
    Path(path).write_text(head + "\n".join(ev) + "\n", encoding="utf-8")


def content_crop(video):
    """Находит чёрные полосы в исходнике (cropdetect) и возвращает фильтр crop."""
    r = subprocess.run(["ffmpeg", "-i", str(video), "-vf", "cropdetect=limit=24:round=2", "-t", "5",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    found = re.findall(r"crop=(\d+:\d+:\d+:\d+)", r)
    return f"crop={found[-1]}," if found else ""


def render(video, clips, ass, out, music_volume, zoom):
    inputs = ["-i", str(video)]
    for c in clips:
        inputs += ["-i", str(c["path"])]
    y = (H - BAND) // 2
    esc = str(ass).replace("\\", "/").replace(":", "\\:")
    zw = int(W * zoom) // 2 * 2
    f = [
        f"[0:v]{content_crop(video)}split[c1][c2]",
        f"[c1]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=20:2,eq=brightness=-0.04[bg]",
        f"[c2]scale={zw}:-2,crop={W}:{BAND}[fg]",
        f"[bg][fg]overlay=0:{y},ass='{esc}'[v]",
        f"[0:a]volume={music_volume}[m]",
    ]
    mix = ["[m]"]
    for n, c in enumerate(clips, 1):
        ms = int(c["t"] * 1000)
        f.append(f"[{n}:a]aresample=48000,adelay={ms}|{ms},volume=1.5[s{n}]")
        mix.append(f"[s{n}]")
    f.append(f"{''.join(mix)}amix=inputs={len(mix)}:duration=first:normalize=0,alimiter=limit=0.95[a]")
    run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(f), "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("script", help="JSON со сценарием")
    p.add_argument("-o", "--out", required=True)
    p.add_argument("--music-volume", type=float, default=0.3, help="громкость звука оригинала")
    p.add_argument("--font", default="Montserrat Black")
    p.add_argument("--zoom", type=float, default=1.3, help="увеличение центральной полосы (обрезает края)")
    a = p.parse_args()

    sc = json.loads(Path(a.script).read_text(encoding="utf-8"))
    out = Path(a.out)
    work = out.parent / (out.stem + "_work")
    work.mkdir(parents=True, exist_ok=True)

    print("Озвучка:")
    clips = voice_lines(sc["lines"], work, sc.get("voice", "ru-RU-DmitryNeural"),
                        sc.get("rate", 10), sc.get("pitch", 0), duration(a.video))
    ass = work / "words.ass"
    write_ass(clips, ass, a.font)
    print("Рендер…")
    render(a.video, clips, ass, out, a.music_volume, a.zoom)
    print(f"Готово: {out}")


if __name__ == "__main__":
    main()
