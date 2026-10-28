#!/bin/bash
cd /home/user/-/videos
for n in "$@"; do grep -q VOICE_DONE long-night-ep$n/voice.log 2>/dev/null || ./_tools/voice.sh long-night-ep$n am_onyx 1.05 > long-night-ep$n/voice.log 2>&1; done
