#!/bin/bash
# usage: build.sh <project_dir> — frames, captions, index, transitions, lint
set -e
cd "$1"
S=/home/user/-/.claude/skills/faceless-explainer/scripts
python3 .hyperframes/gen.py
node $S/captions.mjs build --storyboard ./STORYBOARD.md --audio-meta ./audio_meta.json --hyperframes . --out ./caption_groups.json | tail -1
node $S/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes . | grep -E "total"
node $S/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes . > /dev/null
L=$(grep -n 'id="el-captions"' index.html | cut -d: -f1)
sed -i "${L}s/id=\"el-captions\"/id=\"el-captions\" data-track-kind=\"captions\"/" index.html
npx hyperframes lint 2>&1 | grep -E "✗|error\(s\)" | head -12
