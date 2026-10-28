#!/bin/bash
# Russian Dimmers: voice → build → render for the given parts (skips finished steps)
cd /home/user/-/videos
for n in "$@"; do
  d=long-night-ru-ep$n
  grep -q VOICE_DONE $d/voice.log 2>/dev/null || python3 _tools/voice_ru.py $d 0.85 > $d/voice.log 2>&1
  [ -f $d/renders/the-dimmers-part-$n-ru.mp4 ] && continue
  bash _tools/build.sh $d > $d/build.log 2>&1
  (cd $d && npx hyperframes render --skill=faceless-explainer --quality high --output renders/the-dimmers-part-$n-ru.mp4 > render.log 2>&1)
  echo "RU PART $n DONE" >> long-night-ru-pipeline.log
done
