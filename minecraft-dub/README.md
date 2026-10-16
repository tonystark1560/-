# Русская переозвучка шортсов

Бесплатный конвейер: ссылка → распознавание речи (Whisper) → перевод → русский голос (edge-tts) → сведение со звуком оригинала → вшитые русские субтитры.

## Установка
Нужны Python 3.10+ и ffmpeg.
```
pip install -r requirements.txt
```

## Использование
```
python dub.py "https://www.youtube.com/shorts/XXXX"
python dub.py video.mp4 --voice svetlana
```
Результат: `out/<имя>/<имя>_ru.mp4`, а также `ru.srt` и `original.srt`.

### Ручная правка перевода (лучшее качество)
```
python dub.py video.mp4 --transcribe-only      # сделает out/<имя>/ru.srt
# поправьте ru.srt
python dub.py video.mp4 --ru-srt out/<имя>/ru.srt
```

### Полезные опции
| Опция | Что делает |
|---|---|
| `--voice dmitry\|svetlana` | мужской или женский голос |
| `--bg-volume 0.15` | громкость оригинала под озвучкой |
| `--separate` | вырезать голос оригинала, оставив музыку и звуки (нужен `pip install demucs`) |
| `--no-burn` | не вшивать субтитры, только файл .srt |
| `--model medium` | точнее распознавание, но медленнее |
| `--cookies cookies.txt` | если YouTube пишет «Sign in to confirm you're not a bot» |
