#!/usr/bin/env python3
"""Готовый YouTube Short из сырой записи CS2.

    python3 make_short.py spec.json

spec.json:
{
  "out": "out/01.mp4",
  "layout": "crop",                  # crop — центр кадра на весь экран; blur — кадр целиком на размытом фоне
  "clips": [                         # куски сырой записи, по порядку (секунды)
    {"file": "raw/mirage.mp4", "start": 12.0, "end": 14.0},
    {"file": "raw/mirage.mp4", "start": 40.5, "end": 58.0, "zoom": 1.4}
  ],
  "hook": "1 КЛИК — И ОКНО ЗАКРЫТО", # крупный текст сверху в первые 2 секунды
  "hook_seconds": 2.0,
  "captions": [                      # субтитры: время от начала готового ролика
    {"t": 2.0, "d": 3.0, "text": "Этот смок кидается без прыжка"}
  ],
  "loop": true                       # в конце 0.4 с первого кадра — переход в автоповтор без шва
}

Нужен только ffmpeg с libass. Шрифт — Inter (кириллица).
"""
import json, os, subprocess, sys, tempfile

W, H, FPS = 1080, 1920, 60
FONT = "Inter"


def ts(sec):
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def ass(spec, path):
    hook_s = spec.get("hook_seconds", 2.0)
    lines = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Alignment, "
        "MarginL, MarginR, MarginV, BorderStyle, Outline, Shadow",
        # хук: сверху, жёлтый, толстая обводка; субтитры: ниже центра, белые — вне нижней зоны кнопок YouTube
        f"Style: Hook,{FONT},96,&H0000E5FF,&H00000000,&H00000000,-1,8,60,60,260,1,8,0",
        f"Style: Cap,{FONT},84,&H00FFFFFF,&H00000000,&H00000000,-1,2,80,80,620,1,6,0",
        "", "[Events]", "Format: Layer, Start, End, Style, Text",
    ]
    if spec.get("hook"):
        lines.append(f"Dialogue: 1,{ts(0)},{ts(hook_s)},Hook,{spec['hook']}")
    for c in spec.get("captions", []):
        lines.append(f"Dialogue: 0,{ts(c['t'])},{ts(c['t'] + c['d'])},Cap,{c['text']}")
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")


def vertical(layout, zoom):
    z = max(zoom, 1.0)
    if layout == "blur":
        return (f"split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:2[bg];"
                f"[b]scale={int(W * z)}:-2,crop={W}:ih[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2")
    return f"scale=-2:{int(H * z)},crop={W}:{H}"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])


def main():
    spec_path = sys.argv[1]
    base = os.path.dirname(os.path.abspath(spec_path))
    spec = json.load(open(spec_path, encoding="utf-8"))
    out = os.path.join(base, spec["out"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        parts = []
        for i, c in enumerate(spec["clips"]):
            p = os.path.join(tmp, f"{i}.mp4")
            run(["ffmpeg", "-y", "-ss", str(c["start"]), "-to", str(c["end"]), "-i", os.path.join(base, c["file"]),
                 "-vf", vertical(spec.get("layout", "crop"), c.get("zoom", 1.0)) + f",fps={FPS},setsar=1",
                 "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", p])
            parts.append(p)
        if spec.get("loop"):
            p = os.path.join(tmp, "loop.mp4")
            run(["ffmpeg", "-y", "-i", parts[0], "-t", "0.4", "-c", "copy", p])
            parts.append(p)
        lst = os.path.join(tmp, "list.txt")
        open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
        joined = os.path.join(tmp, "joined.mp4")
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])
        sub = os.path.join(tmp, "subs.ass")
        ass(spec, sub)
        run(["ffmpeg", "-y", "-i", joined, "-vf", f"ass={sub}", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", out])
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out],
                         capture_output=True, text=True).stdout.strip()
    print(f"{out}  {float(dur):.1f} с  {W}x{H}")


if __name__ == "__main__":
    main()
