"""Ограбление Binance · Часть 1: 7000 биткоинов одной транзакцией — builds compositions/frames via heist_build."""
import os, sys
sys.path.insert(0, "/home/user/-/videos/_tools")
from heist_build import build

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("ok", build(ROOT, 1, "ru"))
