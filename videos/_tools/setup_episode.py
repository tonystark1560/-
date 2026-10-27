"""Write BRIEF.md, STORYBOARD.md, SCRIPT.md and the synthetic capture package for one episode.

usage: setup_episode.py <project_dir> <channel_script.md> <slugs_csv> <title> <message> <voice> <speed>
"""
import os, re, sys, json

prj, src, slugs_csv, title, message, voice, speed = sys.argv[1:8]
fmt = sys.argv[8] if len(sys.argv) > 8 else "1920x1080"
text = open(src).read()
body = text[text.index("## Сценарий"):]
body = body[:body.index("\n---\n")] if "\n---\n" in body else body
paras = [l.strip() for l in body.splitlines() if l.strip() and not l.startswith("[") and not l.startswith("#")]
slugs = slugs_csv.split(",")
assert len(slugs) == len(paras), (len(slugs), len(paras))

os.makedirs(os.path.join(prj, "capture", "extracted"), exist_ok=True)
open(os.path.join(prj, "capture", "extracted", "visible-text.txt"), "w").write("\n\n".join(paras))
json.dump({"title": title, "description": message, "colors": [], "fonts": ["Inter"]},
          open(os.path.join(prj, "capture", "extracted", "tokens.json"), "w"))
open(os.path.join(prj, "BRIEF.md"), "w").write(f"""---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "{message}"
destination: {"shorts" if fmt == "1080x1920" else "youtube"}
aspect: {fmt}
language: en
length: 75s
angle: narrative
---

## Intent

Full long-form episode "{title}" from {src}. The user asked for the whole video in one go ("делай ролик целиком"), autonomous run, narration a little faster than default.

## Notes

- Voiceover verbatim from the channel script (VO_MODE: verbatim), English, Kokoro {voice} at speed {speed}.
- No company logos; names as plain text only.
""")
sb = [f"""---
format: {fmt}
duration: 75s
message: "{message}"
mode: autonomous
music: none
---
"""]
sc = [f"# SCRIPT — {os.path.basename(prj)}", "", f"**Voice:** {voice} (Kokoro), speed {speed}", "", "---", ""]
for i, (sl, vo) in enumerate(zip(slugs, paras), 1):
    sb.append(f"""## Frame {i} — {sl.replace('-', ' ').title()}

- scene: see .hyperframes/gen.py
- duration: 10s
- transition_in: {"cut" if i == 1 else "crossfade"}
- status: animated
- voiceover: "{vo.replace('"', "'")}"
- src: compositions/frames/{i:02d}-{sl}.html
""")
    sc += [f"## Line {i} — {sl} (Frame {i})", "", f"    {vo}", ""]
open(os.path.join(prj, "STORYBOARD.md"), "w").write("\n".join(sb))
open(os.path.join(prj, "SCRIPT.md"), "w").write("\n".join(sc))
print("frames:", len(paras), "words:", sum(len(p.split()) for p in paras))
