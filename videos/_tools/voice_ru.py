"""Russian narration: Piper TTS per line + whisper (ru) timings aligned onto the script words.

usage: voice_ru.py <project_dir> [length_scale]
"""
import difflib, json, os, re, subprocess, sys, tempfile, wave

prj = os.path.abspath(sys.argv[1])
ls = sys.argv[2] if len(sys.argv) > 2 else "0.85"
MODEL = "/home/user/-/videos/_tools/piper/ru_RU-dmitri-medium.onnx"
S = "/home/user/-/.claude/skills/faceless-explainer/scripts"
os.chdir(prj)
lines = re.findall(r"## Line (\d+) .*?\n\n    (.+)", open("SCRIPT.md").read())
norm = lambda w: re.sub(r"[^а-яёa-z0-9]", "", w.lower()).replace("ё", "е")
voices = []
for n, text in lines:
    n = int(n)
    path = f"assets/voice/{n:02d}.wav"
    say = text
    for a, b in (json.load(open("tts_map.json")).items() if os.path.exists("tts_map.json") else []):
        say = re.sub(rf"(?<![\w-]){re.escape(a)}(?![\w-])", b, say)
    subprocess.run(["python3", "-m", "piper", "-m", MODEL, "-f", path, "--length-scale", ls, "--sentence-silence", "0.2"],
                   input=say.encode(), check=True, capture_output=True)
    with wave.open(path) as w:
        dur = w.getnframes() / w.getframerate()
    d = tempfile.mkdtemp()
    subprocess.run(["npx", "hyperframes", "transcribe", path, "--model", "small", "--language", "ru", "--dir", d], capture_output=True, timeout=900)
    tw = json.load(open(os.path.join(d, "transcript.json"))) if os.path.exists(os.path.join(d, "transcript.json")) else []
    sw = text.split()
    a, b = [norm(w) for w in sw], [norm(w["text"]) for w in tw]
    st = [None] * len(sw)
    en = [None] * len(sw)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            st[blk.a + k], en[blk.a + k] = tw[blk.b + k]["start"], tw[blk.b + k]["end"]
    # interpolate unmatched words between their matched neighbours (by character length)
    i = 0
    while i < len(sw):
        if st[i] is not None:
            i += 1
            continue
        j = i
        while j < len(sw) and st[j] is None:
            j += 1
        t0 = en[i - 1] if i > 0 else (tw[0]["start"] if tw else 0.05)
        t1 = st[j] if j < len(sw) else (tw[-1]["end"] if tw else dur - 0.1)
        if t1 <= t0:
            t1 = t0 + 0.25 * (j - i)
        tot = sum(len(sw[k]) for k in range(i, j))
        c = t0
        for k in range(i, j):
            st[k] = c
            c += (t1 - t0) * len(sw[k]) / tot
            en[k] = c
        i = j
    words = [{"id": f"w{k}", "text": sw[k], "start": round(st[k], 3), "end": round(max(en[k], st[k] + .05), 3)} for k in range(len(sw))]
    voices.append({"frame": n, "path": path, "duration_s": round(dur, 3), "words": words})
    print(n, f"{dur:.2f}s", f"matched {sum(1 for x in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks() for _ in range(x.size))}/{len(sw)}", flush=True)
json.dump({"bgm": None, "bgm_pending": False, "voices": voices, "sfx": []}, open("audio_meta.json", "w"), indent=1, ensure_ascii=False)
subprocess.run(["node", f"{S}/audio.mjs", "sync-durations", "--audio-meta", "./audio_meta.json", "--storyboard", "./STORYBOARD.md"], check=True)
s = open("STORYBOARD.md").read()
s = re.sub(r"- duration: ([\d.]+)s", lambda m: f"- duration: {float(m.group(1)) + 0.45:.3f}s", s)
open("STORYBOARD.md", "w").write(s)
print("VOICE_DONE", sum(v["duration_s"] for v in voices))
