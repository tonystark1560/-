"""Ограбление Binance · Часть 3: Кто платит за ограбление на 40 миллионов? — builds compositions/frames via heist_build."""
import os, sys
sys.path.insert(0, "/home/user/-/videos/_tools")
from heist_build import build

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("ok", build(ROOT, 3, "ru"))
