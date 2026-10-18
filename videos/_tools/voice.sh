#!/bin/bash
# usage: voice.sh <project_dir> <voice> <speed> — TTS + word timings, retrying empty transcripts one by one
set -e
cd "$1"
S=/home/user/-/.claude/skills/faceless-explainer/scripts
node $S/audio.mjs --script ./SCRIPT.md --storyboard ./STORYBOARD.md --hyperframes . --out ./audio_meta.json --voice "$2" --speed "$3"
python3 - <<'PY'
import json, subprocess, os, tempfile
m = json.load(open('audio_meta.json'))
for v in m['voices']:
    if v['words']:
        continue
    d = tempfile.mkdtemp()
    subprocess.run(['npx', 'hyperframes', 'transcribe', v['path'], '--model', 'small.en', '--dir', d], capture_output=True, timeout=900)
    p = os.path.join(d, 'transcript.json')
    if os.path.exists(p):
        v['words'] = [{k: w[k] for k in ('id', 'text', 'start', 'end')} for w in json.load(open(p))]
    print('retry', v['frame'], len(v['words']))
json.dump(m, open('audio_meta.json', 'w'), indent=1)
print('empty:', sum(1 for v in m['voices'] if not v['words']))
PY
node $S/audio.mjs sync-durations --audio-meta ./audio_meta.json --storyboard ./STORYBOARD.md
python3 - <<'PY'
import re
s = open('STORYBOARD.md').read()
s = re.sub(r'- duration: ([\d.]+)s', lambda m: f'- duration: {float(m.group(1)) + 0.45:.3f}s', s)
open('STORYBOARD.md', 'w').write(s)
PY
echo VOICE_DONE
