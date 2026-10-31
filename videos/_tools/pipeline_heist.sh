#!/bin/bash
# Binance Heist: voice → build → render. usage: pipeline_heist.sh en|ru parts...
cd /home/user/-/videos
L=$1; shift
for n in "$@"; do
  if [ $L = en ]; then d=binance-heist-ep$n; out=binance-heist-part-$n.mp4; else d=binance-heist-ru-ep$n; out=binance-heist-part-$n-ru.mp4; fi
  [ -f $d/renders/$out ] && continue
  lines=$(grep -c "^## Line" $d/SCRIPT.md)
  for try in 1 2 3; do
    [ "$(ls $d/assets/voice/*.wav 2>/dev/null | wc -l)" -ge $lines ] && grep -q VOICE_DONE $d/voice.log 2>/dev/null && break
    if [ $L = en ]; then bash _tools/voice.sh $d am_onyx 1.05 > $d/voice.log 2>&1; else python3 _tools/voice_ru.py $d 0.85 > $d/voice.log 2>&1; fi
  done
  bash _tools/build.sh $d > $d/build.log 2>&1
  (cd $d && npx hyperframes render --skill=faceless-explainer --quality high --output renders/$out > render.log 2>&1)
  echo "$L PART $n DONE" >> heist-pipeline.log
done
