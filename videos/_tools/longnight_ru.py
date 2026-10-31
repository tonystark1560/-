"""Russian variant of 'The Dimmers': translated display strings + cue timing mapped onto Russian narration."""
import copy, json, os, re
from hf import Project
from longnight_eps import EPS
import longnight

LABELS = dict(MATCHES="СПИЧКИ", OIL="МАСЛО", FLARES="ФАЕРЫ", BATTERY="БАТАРЕЙКИ", CANDLES="СВЕЧИ", FUEL="ТОПЛИВО")
WORDS = dict(FUEL="ТОПЛИВО", JAN="ЯНВ")

TR = {
"4L": "4Л", "3L": "3Л", "6H": "6Ч", "20 MIN": "20 МИН",
"Rule 1": "Правило 1", "Rule 2": "Правило 2", "Rule 3": "Правило 3", "Rule 4": "Правило 4", "Rule 5": "Правило 5", "Rule 6": "Правило 6",
"No wind": "Ветра нет",
"Brooks Range, Alaska · Nov 18": "Хребет Брукса, Аляска · 18 ноя",
"Sunset 1:42 PM": "Закат в 13:42",
"64 days of dark": "64 дня тьмы",
"Cabin · Polar night": "Хижина · Полярная ночь",
"11 polar nights": "11 полярных ночей",
"Bear: afraid of nothing": "Бэр не боится ничего",
"Kettle Creek: blackout": "Кеттл-Крик: нет света",
"Another town: blackout": "Ещё город: нет света",
"Signal lost": "Связь потеряна",
"Grrrr…": "Рррр…",
"Flame bends to the dark": "Пламя тянется во тьму",
"Too thick": "Слишком густые",
"Woof!": "Гав!",
"Yard · Morning (still dark)": "Двор · Утро (всё ещё темно)",
"Tracks stop at the light": "Следы обрываются у света",
"Part 2 →": "Часть 2 →",
"Rule 1:<br><em>They can't cross the light</em>": "Правило 1:<br><em>Они не могут войти в свет</em>",
"Light = ammo": "Свет = патроны",
"Inventory": "Запасы",
"Matches · 23": "Спички · 23", "Lamp oil · 4L": "Масло · 4Л", "Flares · 4": "Фаеры · 4", "Batteries · 2": "Батарейки · 2",
"Ruth's cabin · 3 miles": "Хижина Рут · 5 км",
"Ruth · retired nurse": "Рут · медсестра на пенсии",
"No smoke · 2 days": "Нет дыма · 2 дня",
"Bear goes first": "Бэр идёт первым",
"Batteries: new": "Батарейки новые",
"Rule 2:<br><em>They drink light.</em><br><i>Electric goes first</i>": "Правило 2:<br><em>Они пьют свет.</em><br><i>Электрический гаснет первым</i>",
"Don't let them go out": "Не дай им погаснуть",
"3 days…": "3 дня…",
"Candles left": "Осталось свечей",
"Each one half gone": "Каждая наполовину",
"*whine*": "*скулит*",
"*SHRIEK*": "*ВИЗГ*",
"Rule 3:<br><em>They hate fire.</em><br><i>Not batteries</i>": "Правило 3:<br><em>Они ненавидят огонь.</em><br><i>Не батарейки</i>",
"Ruth's cabin": "Хижина Рут",
"Generator?": "Генератор?",
"Now.": "Сейчас.",
"4 flares left": "Осталось 4 фаера",
"A wall of dark": "Стена тьмы",
"Fuel leak": "Утечка топлива",
"Ha!": "Ха!",
"Generator": "Генератор",
"6 hours of power": "6 часов света",
"Kettle Creek airstrip": "Аэродром Кеттл-Крик",
"Floodlights + fuel": "Прожекторы + топливо",
"Come south": "Идите на юг",
"Route · 40 miles south": "Маршрут · 65 км на юг",
"40 miles": "65 км",
"1 headlight": "1 фара",
"Loading up": "Сборы",
"Candles · 3": "Свечи · 3", "Flares · 3": "Фаеры · 3", "Bear · in the sled": "Бэр · в санях",
"Rule 4:<br><em>Never travel in the dark.</em><br><i>Unless it's coming anyway</i>": "Правило 4:<br><em>Не иди в темноту.</em><br><i>Если она и так идёт за тобой</i>",
"Mile 10": "16-й км", "Mile 18": "29-й км", "Mile 21": "34-й км",
"Mile 21 · No light": "34-й км · Нет света",
"Mile 21 · Off trail": "34-й км · Вне тропы",
"Something is running with us": "Рядом кто-то бежит",
"COLE!": "КОУЛ!",
"Bear?": "Бэр?",
"Gone into the dark": "Ушёл в темноту",
"Never chase your dog<br><i>into the dark</i>": "Не беги за собакой<br><i>в темноту</i>",
"20 yards of safety": "20 метров безопасности",
"That's not the way!": "Нам не туда!",
"Frozen river": "Замёрзшая река",
"Frozen river · Moonlight": "Замёрзшая река · Луна",
"Rule 5: they won't cross moonlit ice": "Правило 5: лунный лёд",
"Good boy": "Хороший пёс",
"Sky · 4:00 AM": "Небо · 04:00",
"Aurora": "Северное сияние",
"Under the aurora": "Под сиянием",
"Safe · 1 hour": "Безопасно · 1 час",
"Kettle Creek · ahead": "Кеттл-Крик · впереди",
"The town is going dark": "Город гаснет",
"Run <em>toward</em><br>the last light": "Беги <em>к</em><br>последнему свету",
"12 survivors": "12 выживших",
"Fuel: 20 min": "Топливо: 20 мин",
"The math": "Расчёт",
"Fuel · 20 min": "Топливо · 20 мин", "Flares · 2": "Фаеры · 2", "Snowmachine · full tank": "Снегоход · полный бак",
"30 feet of fire": "10 метров огня",
"10 min": "10 мин", "5 min": "5 мин",
"Not one step back": "Ни шагу назад",
"Woof! Woof!": "Гав! Гав!",
"End of the long night": "Конец долгой ночи",
"First sunrise in 64 days": "Первый рассвет за 64 дня",
"Kettle Creek · Sunrise": "Кеттл-Крик · Рассвет",
"They burn": "Они горят",
"Final rule": "Последнее правило",
"Next winter: 300 days": "До зимы: 300 дней",
"Follow for more rules": "Подпишись на новые правила",
"Light is ammo.<br><em>Never waste it.</em>": "Свет — это патроны.<br><em>Не трать зря.</em>",
}
PLACES = {"Cabin": "Хижина", "Porch": "Крыльцо", "Creek trail": "Тропа у ручья", "Ruth's cabin": "Хижина Рут", "Cole's cabin": "Хижина Коула",
          "Radio": "Рация", "River south": "Река на юг", "Kettle Creek airstrip": "Аэродром Кеттл-Крик", "Runway": "Полоса", "Horizon": "Горизонт"}


def t24(m):
    h, mi, ap = int(m.group(1)), m.group(2), m.group(3)
    h = h % 12 + (12 if ap == "PM" else 0)
    return f"{h:02d}:{mi}"


def tr(s):
    if s in TR:
        return TR[s]
    m = re.fullmatch(r"(.+) · (\d+:\d\d (?:AM|PM))", s)
    if m and m.group(1) in PLACES:
        return PLACES[m.group(1)] + " · " + re.sub(r"(\d+):(\d\d) (AM|PM)", t24, m.group(2))
    return s


def walk(x):
    if isinstance(x, str):
        return tr(x)
    if isinstance(x, list):
        return [walk(v) for v in x]
    if isinstance(x, tuple):
        return tuple(walk(v) for v in x)
    if isinstance(x, dict):
        return {k: walk(v) for k, v in x.items()}
    return x


def eps(n):
    c, fr = copy.deepcopy(EPS[n])
    return walk(c), walk(fr)


def paras(path):
    t = open(path).read()
    b = t[t.index("## Сценарий"):].split("\n---")[0]
    return [l.strip() for l in b.splitlines() if l.strip() and not l.startswith("#")]


class RuProject(Project):
    """cue(): English cue word → its relative position in the English line → Russian word at the same position."""
    def __init__(self, root, n, en_path=None):
        super().__init__(root)
        self.en = paras(en_path or f"/home/user/-/channels/long-night/ep{n}.md")
        self.over = {}

    def cue(self, n, word, nth=1, frac=0.5):
        if (n, word) in self.over:
            return self.over[(n, word)]
        norm = lambda w: re.sub(r"[^a-z0-9$%]", "", w.lower())
        toks = self.en[n - 1].split()
        k, idx = 0, None
        for i, w in enumerate(toks):
            if norm(w).startswith(norm(word)):
                k += 1
                if k == nth:
                    idx = i
                    break
        ws = self.words.get(n, [])
        if idx is None or not ws:
            return round(frac * self.dur(n), 2)
        j = min(len(ws) - 1, round(idx / max(1, len(toks) - 1) * (len(ws) - 1)))
        return round(ws[j]["start"], 2)


def build(root, n):
    longnight.LABELS.update(LABELS)
    longnight.WORDS.update(WORDS)
    P = RuProject(root, n)
    c, fr = eps(n)
    ep = longnight.Ep(P, c)
    for i, f in enumerate(fr, 1):
        ep.build(i, f)
    return len(fr)
