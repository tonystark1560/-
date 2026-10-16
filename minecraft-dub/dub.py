#!/usr/bin/env python3
"""Автоматическая русская переозвучка коротких видео (Shorts / TikTok / Reels).

Шаги: скачать видео -> распознать речь (Whisper) -> перевести -> озвучить (edge-tts)
-> приглушить оригинал и наложить русскую дорожку -> вшить русские субтитры.

Примеры:
    python dub.py "https://www.youtube.com/shorts/XXXX"
    python dub.py video.mp4 --voice ru-RU-SvetlanaNeural
    python dub.py video.mp4 --ru-srt my_translation.srt   # своя (ручная) правка перевода
"""
import argparse
import asyncio
import json
import os
import re
import ssl
import subprocess
import sys
import time
from pathlib import Path

VOICES = {
    "dmitry": "ru-RU-DmitryNeural",
    "svetlana": "ru-RU-SvetlanaNeural",
}


def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    ).stdout
    return float(json.loads(out)["format"]["duration"])


# ---------- 1. Видео ----------

def get_video(src, work, cookies=None):
    if Path(src).exists():
        return Path(src)
    import yt_dlp

    opts = {
        "outtmpl": str(work / "source.%(ext)s"),
        "format": "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b",
        "merge_output_format": "mp4",
        "quiet": True,
    }
    if cookies:
        opts["cookiefile"] = cookies
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([src])
    return next(work.glob("source.*"))


# ---------- 2. Распознавание ----------

def transcribe(video, work, model_size):
    from faster_whisper import WhisperModel

    import numpy as np

    # декодируем сами через ffmpeg (не зависим от версии PyAV)
    raw = subprocess.run(
        ["ffmpeg", "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
        check=True, capture_output=True,
    ).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio, vad_filter=True)
    segs = [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segments if s.text.strip()]
    print(f"  язык оригинала: {info.language}, фраз: {len(segs)}")
    return segs, info.language


# ---------- 3. Перевод ----------

def translate(texts, src_lang):
    from deep_translator import GoogleTranslator, MyMemoryTranslator

    for attempt in range(4):
        try:
            return GoogleTranslator(source="auto", target="ru").translate_batch(texts)
        except Exception as e:  # лимиты бесплатного API
            print(f"  Google Translate: {type(e).__name__}, повтор через {2 ** (attempt + 1)} с")
            time.sleep(2 ** (attempt + 1))
    print("  переключаюсь на MyMemory")
    lang = {"en": "en-GB"}.get(src_lang, src_lang)
    return [MyMemoryTranslator(source=lang, target="ru-RU").translate(t) for t in texts]


# ---------- SRT ----------

def ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def write_srt(segs, path, key="text"):
    with open(path, "w", encoding="utf-8") as f:
        for i, s in enumerate(segs, 1):
            f.write(f"{i}\n{ts(s['start'])} --> {ts(s['end'])}\n{s[key]}\n\n")


def read_srt(path):
    def sec(x):
        h, m, rest = x.split(":")
        s, ms = rest.split(",")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

    segs = []
    for block in re.split(r"\n\s*\n", Path(path).read_text(encoding="utf-8").strip()):
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        a, b = [x.strip() for x in lines[1].split("-->")]
        segs.append({"start": sec(a), "end": sec(b), "ru": " ".join(lines[2:]).strip()})
    return segs


# ---------- 4. Озвучка ----------

def _ssl_fix():
    """edge-tts использует certifi; за корпоративным/облачным прокси нужен свой CA."""
    import edge_tts.communicate as c

    ca = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if ca and Path(ca).exists():
        c._SSL_CTX = ssl.create_default_context(cafile=ca)


async def _tts(text, voice, rate, out):
    import edge_tts

    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    await edge_tts.Communicate(text, voice, rate=f"{rate:+d}%", proxy=proxy).save(str(out))


def synthesize(segs, work, voice, video_len, max_rate):
    _ssl_fix()
    clips = []
    for i, s in enumerate(segs):
        nxt = segs[i + 1]["start"] if i + 1 < len(segs) else video_len
        slot = max(nxt - s["start"], 0.3)  # сколько времени есть до следующей фразы
        out = work / f"tts_{i:03}.mp3"
        rate = 0
        asyncio.run(_tts(s["ru"], voice, rate, out))
        d = duration(out)
        if d > slot:  # не влезает — говорим быстрее
            rate = min(int((d / slot - 1) * 100) + 5, max_rate)
            asyncio.run(_tts(s["ru"], voice, rate, out))
            d = duration(out)
        clip = out
        if d > slot:  # всё ещё не влезает — дожимаем через atempo
            tempo = min(d / slot, 2.0)
            clip = work / f"tts_{i:03}_fit.wav"
            run(["ffmpeg", "-y", "-i", str(out), "-filter:a", f"atempo={tempo:.3f}", str(clip)])
        clips.append((s["start"], clip))
        print(f"  [{i + 1}/{len(segs)}] {s['ru'][:60]}")
    return clips


# ---------- 5. Сведение ----------

def separate_background(video, work):
    """Опционально: убрать голос из оригинала через Demucs (pip install demucs)."""
    wav = work / "orig.wav"
    run(["ffmpeg", "-y", "-i", str(video), "-vn", "-ac", "2", "-ar", "44100", str(wav)])
    run([sys.executable, "-m", "demucs", "--two-stems=vocals", "-n", "htdemucs", "-o", str(work / "demucs"), str(wav)])
    return next((work / "demucs").rglob("no_vocals.wav"))


def mix_and_render(video, clips, srt, out, bg_volume, background=None, burn=True):
    inputs = ["-i", str(video)]
    bg_idx = 0
    if background:
        inputs += ["-i", str(background)]
        bg_idx = 1
    first = bg_idx + 1
    for _, c in clips:
        inputs += ["-i", str(c)]

    parts = [f"[{bg_idx}:a]volume={bg_volume}[bg]"]
    labels = ["[bg]"]
    for n, (start, _) in enumerate(clips):
        ms = int(start * 1000)
        parts.append(f"[{first + n}:a]aresample=44100,adelay={ms}|{ms},volume=1.6[v{n}]")
        labels.append(f"[v{n}]")
    parts.append(f"{''.join(labels)}amix=inputs={len(labels)}:duration=first:normalize=0[aout]")

    vmap = "0:v"
    if burn:
        style = ("FontName=DejaVu Sans,FontSize=13,Bold=1,PrimaryColour=&H00FFFFFF,"
                 "OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=60")
        esc = str(srt).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        parts.append(f"[0:v]subtitles='{esc}':force_style='{style}'[vout]")
        vmap = "[vout]"

    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(parts),
           "-map", vmap, "-map", "[aout]"]
    cmd += ["-c:v", "libx264", "-crf", "20", "-preset", "medium"] if burn else ["-c:v", "copy"]
    cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest", str(out)]
    run(cmd)


# ---------- main ----------

def main():
    p = argparse.ArgumentParser(description="Русская переозвучка шортсов")
    p.add_argument("source", help="ссылка на видео или путь к файлу")
    p.add_argument("-o", "--out-dir", default="out")
    p.add_argument("--voice", default="dmitry", help="dmitry | svetlana | любой голос edge-tts")
    p.add_argument("--model", default="small", help="модель Whisper: tiny/base/small/medium/large-v3")
    p.add_argument("--ru-srt", help="готовый русский .srt вместо автоперевода")
    p.add_argument("--bg-volume", type=float, default=0.15, help="громкость оригинала (0..1)")
    p.add_argument("--max-rate", type=int, default=50, help="макс. ускорение речи, %%")
    p.add_argument("--separate", action="store_true", help="вырезать голос оригинала через Demucs")
    p.add_argument("--no-burn", action="store_true", help="не вшивать субтитры в видео")
    p.add_argument("--cookies", help="cookies.txt для yt-dlp (если YouTube просит войти)")
    p.add_argument("--transcribe-only", action="store_true", help="только сделать en.srt и ru.srt для правки")
    a = p.parse_args()

    name = re.sub(r"[^\w-]+", "_", Path(a.source).stem if Path(a.source).exists() else a.source.rstrip("/").split("/")[-1].split("?")[0])[:60]
    work = Path(a.out_dir) / name
    work.mkdir(parents=True, exist_ok=True)

    print("1) Видео…")
    video = get_video(a.source, work, a.cookies)
    vlen = duration(video)

    if a.ru_srt:
        segs = read_srt(a.ru_srt)
    else:
        print("2) Распознаю речь…")
        segs, lang = transcribe(video, work, a.model)
        if not segs:
            sys.exit("В видео не найдено речи.")
        write_srt(segs, work / "original.srt")
        print("3) Перевожу…")
        for s, t in zip(segs, translate([s["text"] for s in segs], lang)):
            s["ru"] = t or s["text"]
    ru_srt = work / "ru.srt"
    write_srt(segs, ru_srt, key="ru")
    if a.transcribe_only:
        print(f"Готово: {work / 'original.srt'} и {ru_srt}. Поправьте ru.srt и запустите с --ru-srt.")
        return

    print("4) Озвучиваю…")
    clips = synthesize(segs, work, VOICES.get(a.voice, a.voice), vlen, a.max_rate)

    background = None
    if a.separate:
        print("   отделяю голос оригинала (Demucs)…")
        background = separate_background(video, work)

    print("5) Свожу и рендерю…")
    out = work / f"{name}_ru.mp4"
    mix_and_render(video, clips, ru_srt, out, 1.0 if background else a.bg_volume, background, not a.no_burn)
    print(f"\nГотово: {out}\nСубтитры: {ru_srt}")


if __name__ == "__main__":
    main()
