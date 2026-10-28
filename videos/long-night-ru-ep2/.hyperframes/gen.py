"""Гасители · Часть 2 — builds compositions/frames from the Russian variant of longnight_eps.EPS[2]."""
import os, sys
sys.path.insert(0, "/home/user/-/videos/_tools")
from longnight_ru import build

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("ok", build(ROOT, 2))
