"""The Binance Heist · Part 3: Who Pays for a $40 Million Robbery? — builds compositions/frames via heist_build."""
import os, sys
sys.path.insert(0, "/home/user/-/videos/_tools")
from heist_build import build

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("ok", build(ROOT, 3, "en"))
