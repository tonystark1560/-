#!/bin/bash
# Build + render parts 1..6 sequentially, waiting for each part's narration.
cd /home/user/-/videos
for n in 1 2 3 4 5 6; do
  d=long-night-ep$n
  until grep -q VOICE_DONE $d/voice.log 2>/dev/null; do sleep 15; done
  _tools/build.sh $d > $d/build.log 2>&1
  (cd $d && npx hyperframes render --skill=faceless-explainer --quality high --output renders/the-dimmers-part-$n.mp4 > render.log 2>&1)
  echo "PART $n DONE" >> /home/user/-/videos/long-night-pipeline.log
done
echo ALL_DONE >> /home/user/-/videos/long-night-pipeline.log
