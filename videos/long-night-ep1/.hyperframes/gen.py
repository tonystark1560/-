"""The Dimmers · Part 1 — builds compositions/frames from longnight_eps.EPS[1]."""
import os, sys
sys.path.insert(0, "/home/user/-/videos/_tools")
from hf import Project
from longnight import Ep
from longnight_eps import EPS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
counters, frames = EPS[1]
P = Project(ROOT)
ep = Ep(P, counters)
for i, f in enumerate(frames, 1):
    ep.build(i, f)
print("ok", len(frames))
