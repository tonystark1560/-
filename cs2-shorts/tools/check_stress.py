#!/usr/bin/env python3
"""Показать, где модель поставит ударения (+ перед ударной гласной) во всех фразах роликов.

    python3 check_stress.py ../shorts/*.json
"""
import json, os, sys, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import torch
from make_news_short import MODEL, stressed

acc = torch.package.PackageImporter(MODEL).load_pickle("tts_models", "model").packages[0].accentor
for f in sys.argv[1:]:
    print("==", os.path.basename(f))
    for ln in json.load(open(f, encoding="utf-8"))["lines"]:
        print("  ", acc(stressed(ln.get("say", ln["text"]))))
