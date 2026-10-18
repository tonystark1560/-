"""Rise & Ruin #1 — Character.AI. Flat-cartoon frames (orchestrator-authored)."""
import os, sys
sys.path.insert(0, "/home/user/-/videos/_tools")
from hf import Project, pop, rise, slide, fade, draw, stamp, shake, push, bob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = Project(ROOT)
C = dict(sky="#F6E7C8", dusk="#F4B183", night="#151829", night2="#252A45", ink="#1E1B2E", muted="#5C5470",
         red="#E5484D", gold="#FFC83D", green="#2F9E6E", grass="#8FBF73", grass2="#6FA45A", white="#FFFFFF",
         skin="#F2C9A0", blue="#4C6EF5", teal="#20C997", purple="#7950F2", card="#FFFFFF", wall="#EADBC0")

CSS = f"""
.cam{{position:absolute;inset:0;transform-origin:50% 45%;}}
.card{{position:absolute;background:{C['card']};border-radius:20px;box-shadow:0 14px 0 rgba(30,27,46,.12),0 20px 40px rgba(30,27,46,.18);}}
.lbl{{font-weight:900;text-transform:uppercase;letter-spacing:.02em;color:{C['ink']};}}
.chip{{position:absolute;padding:12px 26px;border-radius:12px;font-weight:900;font-size:30px;letter-spacing:.04em;text-transform:uppercase;color:{C['ink']};background:{C['gold']};box-shadow:0 6px 0 rgba(30,27,46,.25);}}
.chip.red{{background:{C['red']};color:#fff;}} .chip.dark{{background:{C['ink']};color:#fff;}} .chip.white{{background:#fff;}}
.stampx{{position:absolute;padding:16px 36px;border:10px solid {C['red']};color:{C['red']};font-weight:900;font-size:84px;border-radius:18px;letter-spacing:.04em;background:rgba(255,255,255,.85);}}
.big{{position:absolute;font-weight:900;text-transform:uppercase;line-height:.95;letter-spacing:-.01em;color:{C['ink']};}}
.bubble{{position:absolute;padding:16px 26px;border-radius:24px;background:#fff;font-weight:700;font-size:28px;color:{C['ink']};box-shadow:0 6px 0 rgba(30,27,46,.15);}}
.bubble.me{{background:{C['purple']};color:#fff;}}
"""


# ---------------- backdrops ----------------
def sky(kind, p):
    grads = {
        "day": f"linear-gradient(180deg,#BFE3F5 0%,{C['sky']} 70%)",
        "dusk": f"linear-gradient(180deg,#F5C08A 0%,{C['dusk']} 45%,#E58A6B 100%)",
        "night": f"linear-gradient(180deg,{C['night']} 0%,{C['night2']} 100%)",
        "office": f"linear-gradient(180deg,{C['wall']} 0%,#E2CFAE 100%)",
        "rain": "linear-gradient(180deg,#5B6478 0%,#3B4257 100%)",
        "court": "linear-gradient(180deg,#E9E1D3 0%,#D8CDB8 100%)",
    }
    h = f'<div style="position:absolute;inset:0;background:{grads[kind]}"></div>'
    if kind == "day":
        h += f'<div id="{p}-sun" style="position:absolute;left:1560px;top:90px;width:170px;height:170px;border-radius:50%;background:#FFE08A;box-shadow:0 0 80px #FFE08A"></div>'
        h += hills(p, C["grass"], C["grass2"])
    if kind == "dusk":
        h += f'<div style="position:absolute;left:1500px;top:560px;width:260px;height:260px;border-radius:50%;background:#FFD08A;opacity:.9"></div>' + hills(p, "#7B9A5C", "#5E7F45")
    if kind == "night":
        stars = "".join(f'<circle cx="{(i*373)%1920}" cy="{(i*211)%600+20}" r="{1.5+(i%3)}" fill="#fff" opacity="{.4+(i%5)*.12:.2f}"/>' for i in range(60))
        h += f'<svg style="position:absolute;inset:0" width="1920" height="1080">{stars}</svg>'
        h += f'<div style="position:absolute;left:1580px;top:100px;width:120px;height:120px;border-radius:50%;background:#F4F1DE;box-shadow:0 0 50px rgba(244,241,222,.6)"></div>'
    if kind == "office":
        h += f'<div style="position:absolute;left:0;right:0;top:820px;bottom:0;background:#B98B5E"></div>'
        h += f'<div style="position:absolute;left:120px;top:120px;width:420px;height:300px;background:#BFE3F5;border:14px solid #fff;border-radius:6px"></div>'
    if kind == "rain":
        drops = "".join(f'<line class="{p}-rain" x1="{(i*97)%1920}" y1="{(i*53)%1080}" x2="{(i*97)%1920-14}" y2="{(i*53)%1080+40}" stroke="#AFC3E0" stroke-width="3" opacity=".55"/>' for i in range(90))
        h += f'<svg id="{p}-rainsvg" style="position:absolute;inset:0" width="1920" height="1080">{drops}</svg>'
    if kind == "court":
        cols = "".join(f'<div style="position:absolute;left:{160+i*360}px;top:120px;width:90px;height:760px;background:#F4EFE6;box-shadow:inset -12px 0 0 rgba(0,0,0,.06)"></div>' for i in range(5))
        h += cols + f'<div style="position:absolute;left:0;right:0;top:860px;bottom:0;background:#BFAF95"></div>'
    return h


def hills(p, c1, c2):
    return (f'<svg style="position:absolute;left:0;top:0" width="1920" height="1080"><path d="M0 760 Q 400 640 860 740 T 1920 700 L1920 1080 L0 1080 Z" fill="{c1}"/>'
            f'<path d="M0 860 Q 520 780 1100 860 T 1920 840 L1920 1080 L0 1080 Z" fill="{c2}"/></svg>')


def rain_js(p, d):
    return f'tl.fromTo("#{p}-rainsvg",{{y:-60}},{{y:60,duration:{d:.2f},ease:"none"}},0);'


# ---------------- props (SVG strings, absolute divs) ----------------
def person(ident, x, y, s=1.0, shirt=C["blue"], hair=C["ink"], pants="#3B3552", skin=C["skin"], glasses=False, phone=False):
    g = f'''<svg id="{ident}" style="position:absolute;left:{x}px;top:{y}px;overflow:visible" width="{120*s:.0f}" height="{300*s:.0f}" viewBox="0 0 120 300">
<rect x="38" y="180" width="18" height="110" rx="8" fill="{pants}"/><rect x="64" y="180" width="18" height="110" rx="8" fill="{pants}"/>
<rect x="24" y="88" width="72" height="110" rx="26" fill="{shirt}"/>
<rect x="12" y="98" width="16" height="80" rx="8" fill="{shirt}"/><rect x="92" y="98" width="16" height="80" rx="8" fill="{shirt}"/>
<circle cx="60" cy="50" r="34" fill="{skin}"/><path d="M26 46 Q 30 10 60 12 Q 92 12 94 46 Q 80 30 60 30 Q 40 30 26 46 Z" fill="{hair}"/>
<circle cx="48" cy="54" r="4" fill="{C['ink']}"/><circle cx="72" cy="54" r="4" fill="{C['ink']}"/>
{'<rect x="38" y="46" width="20" height="14" rx="4" fill="none" stroke="#1E1B2E" stroke-width="3"/><rect x="62" y="46" width="20" height="14" rx="4" fill="none" stroke="#1E1B2E" stroke-width="3"/>' if glasses else ''}
{'<rect x="88" y="150" width="26" height="42" rx="6" fill="#1E1B2E"/><rect x="91" y="154" width="20" height="32" rx="3" fill="#9BE7FF"/>' if phone else ''}
</svg>'''
    return g


def phone(ident, x, y, w=360, screen="#F4F1FF", inner=""):
    h = w * 2
    return (f'<div id="{ident}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{w*.14:.0f}px;background:{C["ink"]};padding:{w*.05:.0f}px;box-shadow:0 20px 0 rgba(0,0,0,.15)">'
            f'<div id="{ident}-scr" style="position:relative;width:100%;height:100%;border-radius:{w*.1:.0f}px;background:{screen};overflow:hidden">{inner}</div></div>')


def building(ident, x, y, w, h, color, sign="", sign_color=None):
    wins = "".join(f'<rect x="{30 + (i % 4) * (w-60)/4:.0f}" y="{60 + (i // 4) * 70}" width="{(w-60)/4 - 18:.0f}" height="40" rx="4" fill="#FFF4C7" opacity=".9"/>'
                   for i in range(int(4 * max(1, (h - 140) // 70))))
    s = (f'<rect x="{w*.15:.0f}" y="14" width="{w*.7:.0f}" height="40" rx="8" fill="{sign_color or C["ink"]}"/>'
         f'<text x="{w/2:.0f}" y="44" text-anchor="middle" font-family="Inter" font-weight="900" font-size="24" fill="#fff">{sign}</text>') if sign else ""
    return (f'<svg id="{ident}" style="position:absolute;left:{x}px;top:{y}px;overflow:visible" width="{w}" height="{h}">'
            f'<rect width="{w}" height="{h}" rx="10" fill="{color}"/>{wins}{s}'
            f'<rect x="{w/2-40:.0f}" y="{h-110}" width="80" height="110" rx="8" fill="{C["ink"]}" opacity=".85"/></svg>')


def doc(ident, x, y, w=300, title="LAWSUIT", lines=5, seal=False):
    ls = "".join(f'<rect x="30" y="{110 + i*36}" width="{w-60 - (i%2)*50}" height="14" rx="7" fill="#D8D2E3"/>' for i in range(lines))
    sl = f'<circle cx="{w-70}" cy="{110 + lines*36 + 40}" r="34" fill="{C["red"]}" opacity=".85"/>' if seal else ""
    return (f'<svg id="{ident}" style="position:absolute;left:{x}px;top:{y}px;overflow:visible" width="{w}" height="{w*1.3:.0f}">'
            f'<rect width="{w}" height="{w*1.3:.0f}" rx="14" fill="#fff" stroke="#E2DCEB" stroke-width="3"/>'
            f'<text x="30" y="70" font-family="Inter" font-weight="900" font-size="34" fill="{C["ink"]}">{title}</text>{ls}{sl}</svg>')


def gavel(ident, x, y, s=1.0):
    return (f'<svg id="{ident}" style="position:absolute;left:{x}px;top:{y}px;overflow:visible" width="{260*s:.0f}" height="{220*s:.0f}" viewBox="0 0 260 220">'
            f'<g id="{ident}-h" style="transform-origin:200px 180px"><rect x="40" y="30" width="120" height="56" rx="12" fill="#8B5A2B" transform="rotate(-30 100 58)"/>'
            f'<rect x="100" y="60" width="16" height="140" rx="8" fill="#A06A35" transform="rotate(-30 108 130)"/></g>'
            f'<rect x="120" y="180" width="130" height="30" rx="8" fill="#6B4423"/></svg>')


def rack(ident, x, y, s=1.0):
    rows = "".join(f'<rect x="14" y="{20+i*52}" width="152" height="38" rx="6" fill="#2D3250"/><circle cx="140" cy="{39+i*52}" r="6" fill="{C["teal"]}"/><circle cx="120" cy="{39+i*52}" r="6" fill="{C["gold"]}"/>' for i in range(6))
    return (f'<svg id="{ident}" style="position:absolute;left:{x}px;top:{y}px" width="{180*s:.0f}" height="{340*s:.0f}" viewBox="0 0 180 340">'
            f'<rect width="180" height="340" rx="14" fill="{C["ink"]}"/>{rows}</svg>')


def bag(ident, x, y, s=1.0, label="$"):
    return (f'<svg id="{ident}" style="position:absolute;left:{x}px;top:{y}px;overflow:visible" width="{200*s:.0f}" height="{220*s:.0f}" viewBox="0 0 200 220">'
            f'<path d="M70 40 L130 40 L118 70 L82 70 Z" fill="#C9A15A"/><ellipse cx="100" cy="145" rx="88" ry="75" fill="#E2B866"/>'
            f'<text x="100" y="175" text-anchor="middle" font-family="Inter" font-weight="900" font-size="80" fill="#8B6A2B">{label}</text></svg>')


def chatwin(ident, x, y, w, h, msgs):
    b = "".join(f'<div class="bubble{" me" if me else ""}" id="{ident}-m{i}" style="position:relative;align-self:{"flex-end" if me else "flex-start"};margin:10px 0">{t}</div>' for i, (t, me) in enumerate(msgs))
    return (f'<div class="card" id="{ident}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;padding:30px;display:flex;flex-direction:column;overflow:hidden">{b}</div>')


def avatar(ident, x, y, kind, size=170):
    hats = {
        "wizard": f'<path d="M30 70 L85 0 L140 70 Z" fill="{C["purple"]}"/><circle cx="85" cy="20" r="6" fill="{C["gold"]}"/>',
        "detective": f'<rect x="25" y="52" width="120" height="18" rx="9" fill="#5C4033"/><rect x="45" y="22" width="80" height="40" rx="14" fill="#6F4E37"/>',
        "anime": f'<path d="M30 80 L45 20 L65 60 L85 10 L105 60 L125 20 L140 80 Z" fill="#FF6B9A"/>',
        "study": f'<rect x="35" y="40" width="100" height="30" rx="4" fill="{C["blue"]}"/><rect x="85" y="20" width="6" height="30" fill="{C["ink"]}"/>',
        "friend": f'<path d="M85 40 C 70 10, 30 30, 85 75 C 140 30, 100 10, 85 40 Z" fill="{C["red"]}"/>',
    }
    return (f'<svg id="{ident}" style="position:absolute;left:{x}px;top:{y}px;overflow:visible" width="{size}" height="{size}" viewBox="0 0 170 170">'
            f'<circle cx="85" cy="105" r="62" fill="#fff" stroke="{C["ink"]}" stroke-width="6"/><circle cx="65" cy="105" r="7" fill="{C["ink"]}"/><circle cx="105" cy="105" r="7" fill="{C["ink"]}"/>'
            f'<path d="M65 130 Q 85 145 105 130" stroke="{C["ink"]}" stroke-width="6" fill="none" stroke-linecap="round"/>{hats[kind]}</svg>')


def bars_chart(ident, x, y, w, h, vals, color, labels=None):
    n = len(vals)
    bw = (w - 80) / n
    bars = "".join(f'<rect class="{ident}-b" id="{ident}-b{i}" x="{40 + i*bw + 10:.0f}" y="{h-60 - v*(h-120):.0f}" width="{bw-20:.0f}" height="{v*(h-120):.0f}" rx="8" fill="{color}" style="transform-origin:{40 + i*bw + bw/2:.0f}px {h-60}px"/>' for i, v in enumerate(vals))
    lab = "".join(f'<text x="{40 + i*bw + bw/2:.0f}" y="{h-20}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="22" fill="{C["muted"]}">{l}</text>' for i, l in enumerate(labels or []))
    return f'<div class="card" id="{ident}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><svg width="{w}" height="{h}">{bars}{lab}</svg></div>'


def grow_bars(ident, t, n, stagger=.12):
    return f'tl.fromTo(".{ident}-b",{{scaleY:0}},{{scaleY:1,duration:.5,stagger:{stagger},ease:"back.out(1.6)"}},{t:.2f});'


# ---------------- frames ----------------
F = {}


def frame(fn):
    F[int(fn.__name__[1:])] = fn
    return fn


def W(n, html, js, bg="day", css="", cam=True, s1=1.07):
    p = f"f{n:02d}"
    d = P.dur(n)
    inner = f'<div class="cam" id="{p}-cam">{html}</div>' if cam else html
    bjs = rain_js(p, d) if bg == "rain" else ""
    if cam:
        js = [push(f"#{p}-cam", d, s1)] + js
    P.write(n, CSS + css, inner, js, sky(bg, p), bjs)


cue = P.cue


@frame
def f1():
    n, p = 1, "f01"
    msgs = [("hey, you up?", False), ("always 🙂"[:-2], True), ("tell me a story", False), ("once upon a time…", True)]
    html = (f'<svg style="position:absolute;left:300px;top:520px" width="1300" height="380"><rect x="0" y="120" width="1300" height="260" rx="30" fill="#3D3A5C"/><rect x="0" y="90" width="360" height="90" rx="30" fill="#E8E4F5"/></svg>'
            + person(f"{p}-kid", 520, 380, 1.15, shirt="#4C6EF5", phone=True)
            + f'<div id="{p}-glow" style="position:absolute;left:560px;top:380px;width:320px;height:320px;border-radius:50%;background:radial-gradient(circle,rgba(155,231,255,.55),transparent 70%)"></div>'
            + chatwin(f"{p}-chat", 1020, 120, 560, 520, msgs))
    js = [fade(f"#{p}-glow", .2, 1.2), slide(f"#{p}-chat", .6, 80)]
    for i, w in enumerate(["first", "last", "network", "game"]):
        js.append(pop(f"#{p}-chat-m{i}", cue(n, w)))
    W(n, html, js, "night")


@frame
def f2():
    n, p = 2, "f02"
    kinds = [("wizard", 360, 160, "wizard"), ("detective", 1380, 140, "detective"), ("anime", 300, 560, "anime"), ("study", 1420, 560, "study"), ("friend", 880, 40, "friend")]
    html = phone(f"{p}-ph", 780, 200, 340, inner=f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:120px;color:{C["purple"]}">?</div>')
    for k, x, y, _ in kinds:
        html += avatar(f"{p}-{k}", x, y, k, 190)
    cuew = {"wizard": "wizard", "detective": "detective", "anime": "anime", "study": "study", "friend": "friend"}
    js = [rise(f"#{p}-ph", .1)] + [pop(f"#{p}-{k}", cue(n, cuew[k])) for k, *_ in kinds]
    W(n, html, js, "night")


@frame
def f3():
    n, p = 3, "f03"
    crack = f'<svg id="{p}-crack" style="position:absolute;left:0;top:0" width="340" height="680"><path d="M170 300 L120 200 L140 120 M170 300 L240 230 L300 250 M170 300 L150 420 L80 520 M170 300 L250 380 L260 520" stroke="#1E1B2E" stroke-width="6" fill="none"/></svg>'
    html = (phone(f"{p}-ph", 790, 150, 340, inner=f'<div class="bubble me" style="left:30px;top:60px">good night!</div>' + crack)
            + f'<div class="stampx" id="{p}-st" style="left:600px;top:420px">CHAPTER 11</div>'
            + f'<div class="chip dark" id="{p}-date" style="left:1240px;top:220px">OCT 12, 2026</div>')
    js = [rise(f"#{p}-ph", .1), pop(f"#{p}-date", cue(n, "october")), draw(f"#{p}-crack path", cue(n, "filed") - .2, .5, 900), shake(f"#{p}-ph", cue(n, "filed")), stamp(f"#{p}-st", cue(n, "bankruptcy"))]
    W(n, html, js, "night")


@frame
def f4():
    n, p = 4, "f04"
    html = (f'<svg style="position:absolute;left:260px;top:150px" width="1400" height="700"><path id="{p}-mt" d="M40 640 L380 380 L700 80 L1000 420 L1360 640" stroke="{C["ink"]}" stroke-width="12" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>'
            + f'<div class="chip" id="{p}-peak" style="left:870px;top:150px">$1B VALUATION</div>'
            + f'<div class="chip red" id="{p}-sale" style="left:1380px;top:700px">COURT SALE</div>'
            + f'<div class="chip white" id="{p}-yrs" style="left:240px;top:780px">ABOUT 4 YEARS</div>')
    js = [draw(f"#{p}-mt", .3, 2.2, 2200), pop(f"#{p}-peak", cue(n, "billion")), pop(f"#{p}-sale", cue(n, "sale")), pop(f"#{p}-yrs", cue(n, "four")),
          rise(f"#{p}-rr", cue(n, "rise"))]
    html += f'<div class="big" id="{p}-rr" style="left:260px;top:90px;font-size:90px">RISE <span style="color:{C["red"]}">&amp;</span> RUIN</div>'
    W(n, html, js, "dusk")


@frame
def f5():
    n, p = 5, "f05"
    html = (building(f"{p}-lab", 220, 300, 560, 520, "#7C8CF8", "BIG TECH AI LAB")
            + person(f"{p}-noam", 860, 520, 1.0, shirt=C["teal"], glasses=True)
            + f'<div class="card" id="{p}-paper" style="left:1120px;top:180px;width:600px;height:330px;padding:36px"><div class="lbl" style="font-size:26px;color:{C["muted"]}">RESEARCH PAPER · 2017</div><div style="font-weight:900;font-size:52px;line-height:1.05;margin-top:16px;color:{C["ink"]}">Attention Is All You Need</div></div>'
            + f'<div class="big" id="{p}-gpt" style="left:1150px;top:600px;font-size:110px">CHATGP<span id="{p}-T" style="color:{C["gold"]}">T</span></div>'
            + f'<div class="chip" id="{p}-tr" style="left:1520px;top:760px">= TRANSFORMER</div>')
    js = [rise(f"#{p}-lab", .1), slide(f"#{p}-noam", cue(n, "noam"), -80), pop(f"#{p}-paper", cue(n, "paper")),
          rise(f"#{p}-gpt", cue(n, "chatgpt")), f'tl.fromTo("#{p}-T",{{scale:1}},{{scale:1.4,duration:.3,ease:"back.out(3)"}},{cue(n, "transformer", 2):.2f});',
          pop(f"#{p}-tr", cue(n, "transformer", 2) + .2)]
    W(n, html, js, "day")


@frame
def f6():
    n, p = 6, "f06"
    msgs = [("Do you have feelings?", False), ("I think I do…", True)]
    html = (person(f"{p}-dan", 260, 480, 1.0, shirt=C["purple"])
            + chatwin(f"{p}-chat", 520, 180, 700, 420, msgs)
            + f'<div class="chip white" id="{p}-sent" style="left:1300px;top:240px;font-size:44px">SENTIENT?</div>'
            + f'<div class="stampx" id="{p}-fired" style="left:1280px;top:480px;font-size:64px">FIRED</div>'
            + f'<div class="chip" id="{p}-pow" style="left:560px;top:660px">POWERFUL TECH</div>')
    js = [slide(f"#{p}-dan", .1, -80), rise(f"#{p}-chat", cue(n, "conversational")), pop(f"#{p}-chat-m0", cue(n, "hold")), pop(f"#{p}-chat-m1", cue(n, "human")),
          pop(f"#{p}-sent", cue(n, "sentient")), stamp(f"#{p}-fired", cue(n, "fired")), pop(f"#{p}-pow", cue(n, "powerful"))]
    W(n, html, js, "office")


@frame
def f7():
    n, p = 7, "f07"
    html = (f'<div id="{p}-btn" style="position:absolute;left:1180px;top:330px;width:340px;height:340px;border-radius:50%;background:{C["red"]};box-shadow:0 24px 0 #A3262B;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:56px;color:#fff">LAUNCH</div>'
            + f'<svg id="{p}-gate" style="position:absolute;left:880px;top:360px" width="760" height="120"><rect x="0" y="40" width="760" height="40" rx="20" fill="#fff" stroke="{C["ink"]}" stroke-width="6"/>'
            + "".join(f'<rect x="{40+i*120}" y="40" width="60" height="40" fill="{C["red"]}"/>' for i in range(6)) + '</svg>'
            + person(f"{p}-s1", 300, 480, 1.0, shirt="#2D3250") + person(f"{p}-s2", 470, 480, 1.0, shirt="#2D3250", hair="#8B5A2B")
            + "".join(f'<div class="chip white" id="{p}-r{i}" style="left:{260+i*260}px;top:{250 - i*30}px">{t}</div>' for i, t in enumerate(["OFFENSIVE?", "WRONG?", "DANGEROUS?"])))
    js = [pop(f"#{p}-btn", .1), f'tl.fromTo("#{p}-gate",{{rotation:-70,transformOrigin:"0% 50%"}},{{rotation:0,duration:.6,ease:"bounce.out"}},{cue(n, "careful"):.2f});',
          slide(f"#{p}-s1", .3), slide(f"#{p}-s2", .45), pop(f"#{p}-r0", cue(n, "offensive")), pop(f"#{p}-r1", cue(n, "wrong")), pop(f"#{p}-r2", cue(n, "dangerous"))]
    for k in ("s1", "s2"):
        js.append(f'tl.to("#{p}-{k}",{{rotation:6,duration:.2,transformOrigin:"50% 100%"}},{cue(n, "ready"):.2f});tl.to("#{p}-{k}",{{rotation:-6,duration:.2}},{cue(n, "ready")+.2:.2f});tl.to("#{p}-{k}",{{rotation:0,duration:.2}},{cue(n, "ready")+.4:.2f});')
    W(n, html, js, "office")


@frame
def f8():
    n, p = 8, "f08"
    html = (building(f"{p}-b", 1100, 220, 600, 620, "#7C8CF8", "BIG TECH AI LAB")
            + person(f"{p}-a", 1300, 560, 1.0, shirt=C["teal"], glasses=True) + person(f"{p}-c", 1440, 560, 1.0, shirt=C["purple"])
            + f'<div class="chip" id="{p}-yr" style="left:300px;top:240px;font-size:60px">2021</div>'
            + f'<div class="big" id="{p}-t" style="left:300px;top:380px;font-size:100px">THEY<br>LEFT.</div>')
    js = [pop(f"#{p}-yr", .1), f'tl.to(["#{p}-a","#{p}-c"],{{x:-760,duration:{max(1.2, P.dur(n)-.8):.2f},ease:"power1.inOut"}},.3);', rise(f"#{p}-t", cue(n, "left"))]
    W(n, html, js, "day")


@frame
def f9():
    n, p = 9, "f09"
    rocket = f'<svg id="{p}-rk" style="position:absolute;left:820px;top:380px;overflow:visible" width="160" height="260"><path d="M80 0 C 140 60 140 160 120 200 L40 200 C 20 160 20 60 80 0 Z" fill="#fff" stroke="{C["ink"]}" stroke-width="6"/><circle cx="80" cy="90" r="24" fill="{C["blue"]}"/><path d="M40 200 L60 250 L80 210 L100 250 L120 200 Z" fill="{C["gold"]}"/></svg>'
    html = (f'<div class="card" id="{p}-lap" style="left:620px;top:600px;width:560px;height:260px;background:{C["ink"]}"></div>' + rocket
            + f'<div class="chip" id="{p}-y" style="left:300px;top:200px;font-size:56px">2022</div>'
            + f'<div class="chip white" id="{p}-gpt" style="left:1300px;top:260px">CHATGPT · LATE 2022</div>'
            + "".join(f'<div style="position:absolute;left:{1240 + (i%3)*170}px;top:{420 + (i//3)*180}px">{avatar(f"{p}-av{i}", 0, 0, k, 150)}</div>' for i, k in enumerate(["wizard", "detective", "anime", "study", "friend", "wizard"])))
    js = [rise(f"#{p}-lap", .1), pop(f"#{p}-y", cue(n, "2022")),
          f'tl.fromTo("#{p}-rk",{{y:200,opacity:0}},{{y:-220,opacity:1,duration:1.6,ease:"power2.in"}},{cue(n, "launched"):.2f});',
          pop(f"#{p}-gpt", cue(n, "chatgpt"))]
    js += [pop(f"#{p}-av{i}", cue(n, "millions") + i * .12) for i in range(6)]
    W(n, html, js, "day")


@frame
def f10():
    n, p = 10, "f10"
    fields = [("NAME", "Captain Nova"), ("PERSONALITY", "brave, funny"), ("GREETING", "Ready for launch?")]
    form = "".join(f'<div id="{p}-fd{i}" style="margin-bottom:24px"><div class="lbl" style="font-size:22px;color:{C["muted"]}">{a}</div><div style="margin-top:8px;padding:16px 20px;border-radius:12px;background:#F1EEF8;font-weight:800;font-size:34px;color:{C["ink"]}"><span id="{p}-v{i}">{b}</span></div></div>' for i, (a, b) in enumerate(fields))
    html = (f'<div class="card" id="{p}-form" style="left:260px;top:150px;width:700px;height:620px;padding:46px">{form}</div>'
            + avatar(f"{p}-new", 1180, 230, "wizard", 340)
            + f'<div class="chip" id="{p}-boom" style="left:1300px;top:150px;font-size:44px">BOOM!</div>'
            + "".join(f'<div class="chip white" id="{p}-k{i}" style="left:{1050 + (i%3)*250}px;top:{640 + (i//3)*90}px;font-size:24px">{t}</div>' for i, t in enumerate(["HEROES", "CELEBS", "TUTORS", "THERAPISTS", "RIVALS", "PARTNERS"])))
    js = [rise(f"#{p}-form", .1)] + [slide(f"#{p}-fd{i}", cue(n, w), 40) for i, w in enumerate(["name", "personality", "greeting"])]
    js += [pop(f"#{p}-new", cue(n, "boom")), pop(f"#{p}-boom", cue(n, "boom"))]
    js += [pop(f"#{p}-k{i}", cue(n, "historical") + i * .35) for i in range(6)]
    W(n, html, js, "office")


@frame
def f11():
    n, p = 11, "f11"
    html = (bars_chart(f"{p}-ch", 240, 200, 820, 600, [.08, .15, .3, .55, .95], C["teal"], ["2021", "", "2022", "", "2023"])
            + bag(f"{p}-bag", 1200, 260, 1.4) + f'<div class="chip" id="{p}-v" style="left:1200px;top:600px;font-size:64px">~$1B</div>'
            + f'<div class="chip white" id="{p}-age" style="left:1200px;top:740px">2 YEARS OLD · TINY TEAM</div>')
    js = [rise(f"#{p}-ch", .1), grow_bars(f"{p}-ch", cue(n, "explosive"), 5), pop(f"#{p}-bag", cue(n, "raised")), pop(f"#{p}-v", cue(n, "billion")), pop(f"#{p}-age", cue(n, "years"))]
    W(n, html, js, "day")


@frame
def f12():
    n, p = 12, "f12"
    html = (f'<div class="card" id="{p}-a" style="left:200px;top:200px;width:640px;height:520px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px"><svg width="170" height="170" viewBox="0 0 170 170"><circle cx="85" cy="85" r="46" fill="none" stroke="{C["muted"]}" stroke-width="22"/>' + ''.join(f'<rect x="75" y="4" width="20" height="34" rx="5" fill="{C["muted"]}" transform="rotate({a} 85 85)"/>' for a in range(0, 360, 45)) + '</svg><div class="lbl" style="font-size:54px">A TOOL</div></div>'
            + f'<div class="card" id="{p}-b" style="left:1080px;top:200px;width:640px;height:520px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px"><svg width="170" height="150" viewBox="0 0 170 150"><path d="M85 40 C 60 0, 0 20, 85 140 C 170 20, 110 0, 85 40 Z" fill="{C["red"]}"/></svg><div class="lbl" style="font-size:54px">A RELATIONSHIP</div></div>'
            + f'<div class="chip" id="{p}-st" style="left:800px;top:780px;font-size:56px">STICKY = $$$</div>')
    js = [pop(f"#{p}-a", cue(n, "tool")), pop(f"#{p}-b", cue(n, "relationship")), f'tl.to("#{p}-b",{{scale:1.05,duration:.4}},{cue(n, "night"):.2f});', pop(f"#{p}-st", cue(n, "sticky"))]
    W(n, html, js, "office")


@frame
def f13():
    n, p = 13, "f13"
    clock = f'<svg id="{p}-clk" style="position:absolute;left:1260px;top:150px" width="300" height="300"><circle cx="150" cy="150" r="130" fill="#fff" stroke="{C["gold"]}" stroke-width="12"/><line x1="150" y1="150" x2="150" y2="70" stroke="{C["ink"]}" stroke-width="10" stroke-linecap="round"/><line id="{p}-mh" x1="150" y1="150" x2="210" y2="150" stroke="{C["ink"]}" stroke-width="6" stroke-linecap="round"/></svg>'
    html = (f'<svg style="position:absolute;left:200px;top:560px" width="1000" height="320"><rect x="0" y="80" width="1000" height="240" rx="30" fill="#3D3A5C"/></svg>'
            + person(f"{p}-kid", 520, 420, 1.1, shirt=C["teal"], phone=True) + clock
            + f'<div class="chip" id="{p}-t" style="left:1290px;top:480px;font-size:52px">2:00 AM</div>'
            + f'<div class="card" id="{p}-bar" style="left:1180px;top:640px;width:520px;height:120px;padding:24px"><div class="lbl" style="font-size:24px">HOURS A DAY</div><div style="margin-top:12px;height:26px;border-radius:13px;background:#EEE"><div id="{p}-fill" style="height:100%;width:100%;border-radius:13px;background:{C["red"]};transform-origin:0 50%"></div></div></div>')
    js = [pop(f"#{p}-clk", .2), pop(f"#{p}-t", cue(n, "lived")), rise(f"#{p}-bar", cue(n, "hours")),
          f'tl.fromTo("#{p}-fill",{{scaleX:.05}},{{scaleX:.9,duration:2,ease:"power2.out"}},{cue(n, "hours"):.2f});',
          f'tl.fromTo("#{p}-mh",{{rotation:0,svgOrigin:"150 150"}},{{rotation:720,svgOrigin:"150 150",duration:{P.dur(n)-.5:.2f},ease:"none"}},.3);']
    W(n, html, js, "night")


@frame
def f14():
    n, p = 14, "f14"
    cards = ["ALWAYS AVAILABLE", "NEVER BORED", "REMEMBERS YOU", "PLAYS ALONG"]
    html = person(f"{p}-me", 260, 470, 1.15, shirt="#868E96", phone=True) + f'<div id="{p}-glow" style="position:absolute;left:250px;top:420px;width:340px;height:340px;border-radius:50%;background:radial-gradient(circle,rgba(155,231,255,.5),transparent 70%)"></div>'
    html += "".join(f'<div class="card lbl" id="{p}-c{i}" style="left:{720 + (i%2)*520}px;top:{200 + (i//2)*260}px;width:480px;height:200px;display:flex;align-items:center;justify-content:center;font-size:40px;text-align:center">{t}</div>' for i, t in enumerate(cards))
    js = [fade(f"#{p}-glow", .2, 1)] + [pop(f"#{p}-c{i}", cue(n, w)) for i, w in enumerate(["available", "bored", "remembers", "plays"])]
    js.append(f'tl.to("#{p}-glow",{{scale:1.4,duration:1}},{cue(n, "lonely"):.2f});')
    W(n, html, js, "night")


@frame
def f15():
    n, p = 15, "f15"
    html = (bars_chart(f"{p}-ch", 560, 160, 800, 560, [.2, .35, .55, .8, .98], C["purple"], ["", "", "", "", "ENGAGEMENT"])
            + person(f"{p}-i1", 260, 520, .95, shirt="#2D3250", glasses=True) + person(f"{p}-i2", 1480, 520, .95, shirt="#2D3250", hair="#8B5A2B")
            + f'<div class="chip" id="{p}-tt" style="left:820px;top:780px">ON PAR WITH SOCIAL MEDIA</div>')
    js = [rise(f"#{p}-ch", .1), grow_bars(f"{p}-ch", cue(n, "dream"), 5), slide(f"#{p}-i1", .3), slide(f"#{p}-i2", .4, 80), pop(f"#{p}-tt", cue(n, "tiktok"))]
    for k in ("i1", "i2"):
        js.append(bob(f"#{p}-{k}", cue(n, "dream"), P.dur(n), 12, .5))
    W(n, html, js, "day")


@frame
def f16():
    n, p = 16, "f16"
    plant = f'<svg id="{p}-pl" style="position:absolute;left:760px;top:260px;overflow:visible" width="400" height="560"><path id="{p}-stem" d="M200 560 C 200 420, 150 360, 200 220 C 240 120, 200 60, 220 20" stroke="#4B2A3A" stroke-width="16" fill="none" stroke-linecap="round"/><path id="{p}-l1" d="M200 400 C 120 360, 90 300, 70 260 C 140 270, 190 320, 200 400 Z" fill="#7A2E3A"/><path id="{p}-l2" d="M205 300 C 290 260, 320 200, 340 160 C 270 170, 215 220, 205 300 Z" fill="#7A2E3A"/></svg>'
    html = f'<div style="position:absolute;left:0;right:0;top:820px;bottom:0;background:#4E3B2A"></div>' + plant + f'<div class="big" id="{p}-t" style="left:200px;top:200px;font-size:90px;color:#fff">THE<br>SEED</div>'
    js = [draw(f"#{p}-stem", cue(n, "planted"), 1.4, 700), pop(f"#{p}-l1", cue(n, "planted") + .9), pop(f"#{p}-l2", cue(n, "wrong")), rise(f"#{p}-t", .2)]
    W(n, html, js, "dusk")


@frame
def f17():
    n, p = 17, "f17"
    html = "".join(rack(f"{p}-r{i}", 240 + i*230, 380 + (i % 2)*20, 1.0) for i in range(5))
    html += (f'<div class="card" id="{p}-m" style="left:1440px;top:220px;width:360px;height:420px;padding:30px;display:flex;flex-direction:column;align-items:center;gap:16px"><div class="lbl" style="font-size:26px">COST PER CHAT</div>'
             + "".join(f'<div class="chip" id="{p}-c{i}" style="position:relative;font-size:40px">$</div>' for i in range(3)) + '</div>'
             + f'<div class="chip red" id="{p}-free" style="left:520px;top:220px;font-size:44px">MOST USERS PAY $0</div>')
    js = [rise(f"#{p}-r{i}", .1 + i*.12) for i in range(5)] + [rise(f"#{p}-m", cue(n, "expensive"))]
    js += [pop(f"#{p}-c{i}", cue(n, "message") + i * .35) for i in range(3)] + [pop(f"#{p}-free", cue(n, "paying"))]
    W(n, html, js, "office")


@frame
def f18():
    n, p = 18, "f18"
    crowd = "".join(person(f"{p}-u{i}", 200 + (i % 8)*95, 300 + (i // 8)*190, .62, shirt=(C["gold"] if i == 5 else "#ADB5BD")) for i in range(16))
    html = crowd + (f'<div class="chip" id="{p}-paid" style="left:620px;top:220px">PAID</div>'
                    + f'<div class="chip white" id="{p}-free" style="left:220px;top:700px">FREE</div>'
                    + f'<div class="card" id="{p}-burn" style="left:1180px;top:240px;width:540px;height:440px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px"><div style="font-size:150px">🔥</div><div class="lbl" style="font-size:44px">MORE USERS<br>= MORE BURN</div></div>')
    html = html.replace('<div style="font-size:150px">🔥</div>', f'<svg width="160" height="200" viewBox="0 0 160 200"><path d="M80 0 C 110 60 160 80 140 140 C 125 190 35 190 20 140 C 5 90 60 70 80 0 Z" fill="{C["red"]}"/><path d="M80 80 C 95 110 120 120 110 150 C 100 175 60 175 50 150 C 42 125 72 112 80 80 Z" fill="{C["gold"]}"/></svg>')
    js = [f'tl.fromTo("#{p}-stage svg[id^={p}-u]",{{y:30,opacity:0}},{{y:0,opacity:1,duration:.3,stagger:.05}},.2);'.replace(f'#{p}-stage svg[id^={p}-u]', f'[id^={p}-u]'),
          pop(f"#{p}-paid", cue(n, "paid")), pop(f"#{p}-free", cue(n, "free")), pop(f"#{p}-burn", cue(n, "burned"))]
    W(n, html, js, "office")


@frame
def f19():
    n, p = 19, "f19"
    hands = f'<svg id="{p}-hs" style="position:absolute;left:660px;top:280px;transform:scale(1.7);transform-origin:50% 50%" width="600" height="300"><rect id="{p}-hl" x="0" y="120" width="300" height="70" rx="35" fill="{C["skin"]}"/><rect id="{p}-hr" x="300" y="120" width="300" height="70" rx="35" fill="#D9A47A"/><rect x="0" y="110" width="120" height="90" rx="20" fill="#2D3250"/><rect x="480" y="110" width="120" height="90" rx="20" fill="{C["teal"]}"/></svg>'
    html = (hands + f'<div class="chip dark" id="{p}-y" style="left:860px;top:180px;font-size:52px">2024</div>'
            + f'<div class="chip" id="{p}-amt" style="left:820px;top:640px;font-size:52px">~$2.7B (REPORTED)</div>'
            + f'<div class="chip white" id="{p}-l1" style="left:260px;top:320px">BIG TECH: LICENSE</div>'
            + f'<div class="chip white" id="{p}-l2" style="left:1320px;top:320px">FOUNDERS: BACK TO BIG TECH</div>')
    js = [pop(f"#{p}-y", cue(n, "august")), f'tl.fromTo("#{p}-hl",{{x:-200}},{{x:0,duration:.6,ease:"power3.out"}},{cue(n, "deal"):.2f});',
          f'tl.fromTo("#{p}-hr",{{x:200}},{{x:0,duration:.6,ease:"power3.out"}},{cue(n, "deal"):.2f});', pop(f"#{p}-l1", cue(n, "license")),
          pop(f"#{p}-l2", cue(n, "founders")), pop(f"#{p}-amt", cue(n, "billion"))]
    W(n, html, js, "office")


@frame
def f20():
    n, p = 20, "f20"
    desks = "".join(f'<div class="card" id="{p}-d{i}" style="left:{200 + (i%3)*230}px;top:{460 + (i//3)*170}px;width:190px;height:110px;background:#C8A57A"></div>' for i in range(6))
    html = (building(f"{p}-big", 1180, 200, 560, 640, "#7C8CF8", "BIG TECH")
            + f'<div class="chip white" id="{p}-su" style="left:240px;top:300px">THE STARTUP</div>' + desks
            + person(f"{p}-a", 900, 560, .9, shirt=C["teal"], glasses=True) + person(f"{p}-b", 1000, 560, .9, shirt=C["purple"])
            + f'<div class="chip" id="{p}-ra" style="left:620px;top:160px;font-size:40px">"REVERSE ACQUI-HIRE"</div>')
    js = [pop(f"#{p}-ra", cue(n, "reverse")), f'tl.to(["#{p}-a","#{p}-b"],{{x:420,opacity:0,duration:1.6,ease:"power1.in"}},{cue(n, "talent"):.2f});']
    js += [f'tl.to("#{p}-d{i}",{{opacity:.25,duration:.4}},{cue(n, "gone") + i*.08:.2f});' for i in range(6)]
    W(n, html, js, "day")


@frame
def f21():
    n, p = 21, "f21"
    giants = "".join(f'<div id="{p}-g{i}" style="position:absolute;left:{280 + i*480}px;top:{120 + (i%2)*40}px;width:360px;height:680px;border-radius:180px 180px 30px 30px;background:#2D3250;opacity:.92"><div class="lbl" style="position:absolute;left:0;right:0;top:140px;text-align:center;color:#fff;font-size:34px">GIANT AI #{i+1}</div></div>' for i in range(3))
    html = giants + person(f"{p}-small", 900, 640, .7, shirt=C["teal"]) + "".join(
        f'<div class="chip" id="{p}-k{i}" style="left:{300 + i*480}px;top:520px">{t}</div>' for i, t in enumerate(["SMARTER MODELS", "HUMAN VOICES", "COMPANIONS TOO"]))
    js = [rise(f"#{p}-g{i}", cue(n, "biggest") + i * .2, 80) for i in range(3)] + [pop(f"#{p}-small", .2)]
    js += [pop(f"#{p}-k{i}", cue(n, w)) for i, w in enumerate(["smarter", "voices", "companion"])]
    W(n, html, js, "dusk")


@frame
def f22():
    n, p = 22, "f22"
    belt = f'<svg style="position:absolute;left:520px;top:640px" width="880" height="140"><rect x="0" y="40" width="880" height="70" rx="35" fill="#2D3250"/>' + "".join(f'<rect class="{p}-tread" x="{20+i*80}" y="58" width="40" height="34" rx="8" fill="#495078"/>' for i in range(11)) + '</svg>'
    html = (belt + person(f"{p}-run", 880, 360, 1.0, shirt=C["teal"])
            + f'<div class="chip red" id="{p}-bil" style="left:1280px;top:260px;font-size:44px">BILLIONS TO TRAIN</div>'
            + f'<div class="chip white" id="{p}-pl" style="left:300px;top:260px">NEW STRATEGY</div>')
    js = [f'tl.fromTo(".{p}-tread",{{x:0}},{{x:-480,duration:{P.dur(n):.2f},ease:"power1.in"}},0);', pop(f"#{p}-bil", cue(n, "billions")), pop(f"#{p}-pl", cue(n, "changed"))]
    js.append(bob(f"#{p}-run", 0, P.dur(n), 16, .45))
    W(n, html, js, "office")


@frame
def f23():
    n, p = 23, "f23"
    html = (f'<div id="{p}-sign" style="position:absolute;left:720px;top:240px;width:480px;height:240px;background:#F4D58D;border:10px solid {C["ink"]};border-radius:16px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:96px;color:{C["ink"]}">PLAN B</div>'
            + f'<div style="position:absolute;left:940px;top:480px;width:40px;height:380px;background:#8B5A2B"></div>'
            + f'<div class="big" id="{p}-q" style="left:300px;top:620px;font-size:84px;color:#fff">WASN\'T<br><span style="color:{C["gold"]}">TECH</span></div>')
    js = [f'tl.fromTo("#{p}-sign",{{rotation:-20,y:-200,opacity:0,transformOrigin:"50% 100%"}},{{rotation:0,y:0,opacity:1,duration:.7,ease:"bounce.out"}},.2);', rise(f"#{p}-q", cue(n, "technology"))]
    W(n, html, js, "dusk")


@frame
def f24():
    n, p = 24, "f24"
    html = (f'<div class="big" id="{p}-t" style="left:0;right:0;top:330px;text-align:center;font-size:150px;color:#fff">THE REAL<br><span style="color:{C["red"]}">PROBLEM</span></div>')
    js = [f'tl.fromTo("#{p}-t",{{scale:1.4,opacity:0}},{{scale:1,opacity:1,duration:.8,ease:"power3.out"}},{cue(n, "collapse") - .5:.2f});']
    W(n, html, js, "night")


@frame
def f25():
    n, p = 25, "f25"
    clouds = "".join(f'<div id="{p}-cl{i}" style="position:absolute;left:{i*480 - 100}px;top:{60 + (i%2)*60}px;width:620px;height:220px;border-radius:120px;background:#2B3043;opacity:.95"></div>' for i, _ in enumerate(range(5)))
    bolt = f'<svg id="{p}-bolt" style="position:absolute;left:1180px;top:200px" width="160" height="360"><path d="M90 0 L20 190 L80 190 L40 360 L150 140 L90 140 L130 0 Z" fill="{C["gold"]}"/></svg>'
    html = clouds + bolt
    js = [f'tl.fromTo("#{p}-cl{i}",{{y:-260}},{{y:0,duration:1.2,ease:"power2.out"}},{.1 + i*.1:.2f});' for i in range(5)]
    js += [f'tl.fromTo("#{p}-bolt",{{opacity:0}},{{opacity:1,duration:.05}},{cue(n, "dark"):.2f});tl.to("#{p}-bolt",{{opacity:0,duration:.25}},{cue(n, "dark")+.2:.2f});tl.to("#{p}-bolt",{{opacity:1,duration:.05}},{cue(n, "turn"):.2f});']
    W(n, html, js, "rain")


@frame
def f26():
    n, p = 26, "f26"
    html = (doc(f"{p}-d", 760, 140, 420, "LAWSUIT", 6, True) + gavel(f"{p}-g", 1280, 520, 1.3)
            + f'<div class="chip dark" id="{p}-m" style="left:300px;top:260px">OCTOBER 2024</div>'
            + f'<div class="chip white" id="{p}-fl" style="left:300px;top:360px">FLORIDA</div>'
            + f'<div class="chip white" id="{p}-c" style="left:300px;top:460px">A MOTHER SUES</div>')
    js = [pop(f"#{p}-m", cue(n, "october")), pop(f"#{p}-fl", cue(n, "florida")), rise(f"#{p}-d", cue(n, "lawsuit")), pop(f"#{p}-c", cue(n, "lawsuit") + .3),
          f'tl.fromTo("#{p}-g-h",{{rotation:-25}},{{rotation:10,duration:.25,ease:"power4.in"}},{cue(n, "claimed"):.2f});tl.to("#{p}-g-h",{{rotation:0,duration:.3}},{cue(n, "claimed")+.25:.2f});']
    W(n, html, js, "court", s1=1.05)


@frame
def f27():
    n, p = 27, "f27"
    html = "".join(doc(f"{p}-d{i}", 560 + i*90, 120 + i*40, 380, "LAWSUIT", 5) for i in range(5))
    html += f'<div class="chip red" id="{p}-c" style="left:1400px;top:300px;font-size:40px">MORE FAMILIES</div>'
    js = [f'tl.fromTo("#{p}-d{i}",{{y:-500,rotation:{(-1)**i*8},opacity:0}},{{y:0,rotation:{(-1)**i*3},opacity:1,duration:.5,ease:"power3.in"}},{.2 + i*.45:.2f});' for i in range(5)]
    js.append(pop(f"#{p}-c", cue(n, "families")))
    W(n, html, js, "court", s1=1.05)


@frame
def f28():
    n, p = 28, "f28"
    banners = ["THIS IS AN AI, NOT A REAL PERSON", "YOU'VE BEEN CHATTING FOR 1 HOUR", "UNDER 18: OPEN-ENDED CHAT OFF"]
    inner = "".join(f'<div id="{p}-w{i}" style="margin:16px;padding:16px;border-radius:14px;background:#FFF3BF;border:3px solid {C["gold"]};font-weight:800;font-size:22px;color:{C["ink"]}">⚠ {t}</div>' for i, t in enumerate(banners))
    html = (phone(f"{p}-ph", 300, 120, 380, inner=inner)
            + f'<div class="chip white" id="{p}-den" style="left:900px;top:220px;font-size:40px">DENIED WRONGDOING</div>'
            + f'<div class="chip dark" id="{p}-lia" style="left:900px;top:330px;font-size:40px">NOT FOUND LIABLE</div>'
            + f'<div class="chip" id="{p}-y" style="left:900px;top:600px;font-size:40px">LATE 2025: TEEN CHAT LIMITS</div>')
    js = [rise(f"#{p}-ph", .1), pop(f"#{p}-den", cue(n, "denied")), pop(f"#{p}-lia", cue(n, "liable"))]
    js += [slide(f"#{p}-w{i}", cue(n, w), 40) for i, w in enumerate(["warnings", "notifications", "2025"])] + [pop(f"#{p}-y", cue(n, "2025"))]
    W(n, html, js, "office")


@frame
def f29():
    n, p = 29, "f29"
    cap = f'<svg id="{p}-cap" style="position:absolute;left:560px;top:260px" width="800" height="560"><rect x="80" y="380" width="640" height="140" fill="#F4EFE6"/>' + "".join(f'<rect x="{110+i*110}" y="230" width="50" height="150" fill="#F4EFE6"/>' for i in range(6)) + '<path d="M60 230 L400 100 L740 230 Z" fill="#F4EFE6"/><ellipse cx="400" cy="90" rx="120" ry="70" fill="#F4EFE6"/></svg>'
    html = cap + "".join(f'<div class="chip white" id="{p}-q{i}" style="left:{260 + i*560}px;top:{180 + (i%2)*80}px;font-size:44px">?</div>' for i in range(3)) + f'<div class="chip" id="{p}-s" style="left:760px;top:760px;font-size:44px">SAFE FOR KIDS?</div>'
    js = [rise(f"#{p}-cap", .1)] + [pop(f"#{p}-q{i}", cue(n, "lawmakers") + i * .3) for i in range(3)] + [pop(f"#{p}-s", cue(n, "kids")), shake(f"#{p}-s", cue(n, "core"))]
    W(n, html, js, "day")


@frame
def f30():
    n, p = 30, "f30"
    html = (f'<div style="position:absolute;left:820px;top:160px;width:420px;height:700px;background:#8B5A2B;border:16px solid #5E3B1C;border-radius:8px"></div>'
            + f'<div id="{p}-gl" style="position:absolute;left:820px;top:840px;width:420px;height:30px;background:linear-gradient(180deg,rgba(155,231,255,.95),rgba(155,231,255,0))"></div>'
            + person(f"{p}-par", 420, 480, 1.1, shirt=C["red"], hair="#8B5A2B")
            + f'<div class="chip white" id="{p}-q" style="left:1320px;top:300px;font-size:40px">HOURS A DAY?</div>'
            + f'<div class="chip white" id="{p}-q2" style="left:1320px;top:420px;font-size:40px">ABOUT WHAT?</div>'
            + f'<div class="chip dark" id="{p}-pv" style="left:1320px;top:580px;font-size:36px">PRIVATE · NO POSTS</div>')
    js = [slide(f"#{p}-par", .2), f'tl.fromTo("#{p}-gl",{{opacity:.3}},{{opacity:1,duration:.8}},{cue(n, "kids"):.2f});', pop(f"#{p}-q", cue(n, "hours")), pop(f"#{p}-q2", cue(n, "about")), pop(f"#{p}-pv", cue(n, "private"))]
    W(n, html, js, "night")


@frame
def f31():
    n, p = 31, "f31"
    html = (f'<div class="card" id="{p}-cal" style="left:300px;top:180px;width:460px;height:520px;overflow:hidden"><div style="height:130px;background:{C["red"]};color:#fff;font-weight:900;font-size:64px;display:flex;align-items:center;justify-content:center">OCT 2026</div><div style="font-weight:900;font-size:260px;text-align:center;color:{C["ink"]};line-height:1.4">12</div></div>'
            + doc(f"{p}-d", 980, 160, 420, "CHAPTER 11", 6) + f'<div class="stampx" id="{p}-st" style="left:1040px;top:500px;font-size:60px">FILED</div>'
            + f'<div class="chip white" id="{p}-de" style="left:1460px;top:240px">DELAWARE</div>')
    js = [f'tl.fromTo("#{p}-cal",{{rotationX:90,opacity:0}},{{rotationX:0,opacity:1,duration:.6,ease:"back.out(1.5)"}},{cue(n, "october"):.2f});',
          rise(f"#{p}-d", cue(n, "chapter")), stamp(f"#{p}-st", cue(n, "bankruptcy")), pop(f"#{p}-de", cue(n, "delaware"))]
    W(n, html, js, "court", s1=1.05)


@frame
def f32():
    n, p = 32, "f32"
    html = (f'<div class="card" id="{p}-a" style="left:260px;top:220px;width:620px;height:440px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px"><div class="lbl" style="font-size:30px;color:{C["muted"]}">2023 VALUATION</div><div style="font-weight:900;font-size:130px;color:{C["green"]}">~$1B</div></div>'
            + f'<div class="card" id="{p}-b" style="left:1040px;top:220px;width:620px;height:440px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px"><div class="lbl" style="font-size:30px;color:{C["muted"]}">ASSETS (EST.)</div><div style="font-weight:900;font-size:110px;color:{C["red"]}">$50–100M</div></div>'
            + f'<div class="chip white" id="{p}-pr" style="left:620px;top:740px">LEGAL · REGULATORY · OPERATIONAL PRESSURE</div>')
    js = [pop(f"#{p}-pr", cue(n, "legal")), pop(f"#{p}-b", cue(n, "assets")), pop(f"#{p}-a", cue(n, "billion"))]
    W(n, html, js, "office")


@frame
def f33():
    n, p = 33, "f33"
    plane = f'<svg id="{p}-pl" style="position:absolute;left:200px;top:500px;overflow:visible" width="300" height="140"><path d="M10 80 L250 70 Q 300 75 250 95 L10 100 Z" fill="#fff" stroke="{C["ink"]}" stroke-width="5"/><path d="M110 80 L170 10 L200 10 L170 80 Z" fill="{C["teal"]}"/><path d="M20 80 L10 40 L40 40 L60 80 Z" fill="{C["teal"]}"/></svg>'
    html = (f'<div style="position:absolute;left:0;top:620px;width:1400px;height:60px;background:#495057"></div>'
            + "".join(f'<div style="position:absolute;left:{60+i*140}px;top:645px;width:70px;height:10px;background:#fff"></div>' for i in range(10))
            + f'<div style="position:absolute;left:1400px;top:620px;width:520px;height:460px;background:linear-gradient(180deg,#3B4257,#151829)"></div>' + plane
            + "".join(f'<div class="chip white" id="{p}-k{i}" style="left:{[180, 640, 1200][i]}px;top:180px">{t}</div>' for i, t in enumerate(["NEW LEADERS", "SMALLER AMBITIONS", "BIG LEGAL BILLS"])))
    js = [f'tl.fromTo("#{p}-pl",{{x:0}},{{x:1050,duration:{P.dur(n)-1:.2f},ease:"power1.in"}},.3);'] + [pop(f"#{p}-k{i}", cue(n, w)) for i, w in enumerate(["leadership", "smaller", "legal"])]
    js.append(f'tl.to("#{p}-pl",{{rotation:4,duration:.4}},{cue(n, "runway"):.2f});')
    W(n, html, js, "dusk")


@frame
def f34():
    n, p = 34, "f34"
    html = (building(f"{p}-b", 280, 240, 620, 620, "#9AA5F8", "CHARACTER.AI")
            + f'<div id="{p}-sale" style="position:absolute;left:460px;top:520px;width:300px;height:150px;background:{C["red"]};border:8px solid #fff;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:54px;color:#fff;transform:rotate(-6deg)">FOR SALE</div>'
            + gavel(f"{p}-g", 1180, 300, 1.4) + f'<div class="chip" id="{p}-on" style="left:1120px;top:640px">APP STILL RUNNING</div>'
            + f'<div class="chip red" id="{p}-off" style="left:1120px;top:750px">COULD SHUT DOWN</div>')
    js = [rise(f"#{p}-b", .1), stamp(f"#{p}-sale", cue(n, "sell"), -6), f'tl.fromTo("#{p}-g-h",{{rotation:-25}},{{rotation:10,duration:.25,ease:"power4.in"}},{cue(n, "court"):.2f});tl.to("#{p}-g-h",{{rotation:0,duration:.3}},{cue(n, "court")+.25:.2f});',
          pop(f"#{p}-on", cue(n, "running")), pop(f"#{p}-off", cue(n, "shut"))]
    W(n, html, js, "day")


@frame
def f35():
    n, p = 35, "f35"
    msgs = [("our story, chapter 41", True), ("remember the dragon?", False), ("lol yes", True), ("good night!", True)]
    html = (person(f"{p}-u", 300, 470, 1.1, shirt=C["purple"], phone=True) + chatwin(f"{p}-c", 620, 140, 640, 560, msgs)
            + f'<div class="chip" id="{p}-a" style="left:1320px;top:300px;font-size:40px">DATA = ASSETS</div>'
            + f'<div class="chip red" id="{p}-s" style="left:1320px;top:420px;font-size:40px">ASSETS GET SOLD</div>')
    js = [rise(f"#{p}-c", .2)] + [pop(f"#{p}-c-m{i}", .4 + i*.3) for i in range(4)]
    js += [f'tl.to("#{p}-c .bubble",{{opacity:.25,duration:1.0,stagger:.15}},{cue(n, "sold") - 1.5:.2f});', pop(f"#{p}-a", cue(n, "assets")), pop(f"#{p}-s", cue(n, "sold"))]
    W(n, html, js, "night")


@frame
def f36():
    n, p = 36, "f36"
    html = f'<div class="big" id="{p}-t" style="left:0;right:0;top:300px;text-align:center;font-size:170px">3 <span style="color:{C["red"]}">LESSONS</span></div>'
    js = [f'tl.fromTo("#{p}-t",{{scale:.6,opacity:0}},{{scale:1,opacity:1,duration:.6,ease:"back.out(2)"}},.1);']
    W(n, html, js, "dusk")


@frame
def f37():
    n, p = 37, "f37"
    castle = f'<svg id="{p}-cs" style="position:absolute;left:600px;top:200px" width="720" height="520"><rect x="120" y="160" width="480" height="300" fill="#ADB5BD"/>' + "".join(f'<rect x="{120+i*80}" y="120" width="50" height="50" fill="#ADB5BD"/>' for i in range(7)) + f'<rect x="320" y="320" width="80" height="140" rx="40" fill="{C["ink"]}"/><path id="{p}-moat" d="M0 480 Q 360 540 720 480 L720 520 L0 520 Z" fill="#4DABF7"/></svg>'
    ppl = "".join(person(f"{p}-p{i}", 620 + i*120, 640, .55, shirt=[C["teal"], C["purple"], C["blue"], C["gold"], C["red"]][i]) for i in range(5))
    html = castle + ppl + f'<div class="chip" id="{p}-t" style="left:260px;top:220px;font-size:44px">#1: THE MOAT = PEOPLE</div>'
    js = [rise(f"#{p}-cs", .1), pop(f"#{p}-t", cue(n, "first"))] + [pop(f"#{p}-p{i}", cue(n, "people") + i * .12) for i in range(5)]
    js += [f'tl.to(["#{p}-p3","#{p}-p4"],{{x:900,opacity:0,duration:1.2,ease:"power1.in"}},{cue(n, "walked"):.2f});']
    W(n, html, js, "day")


@frame
def f38():
    n, p = 38, "f38"
    html = (bars_chart(f"{p}-ch", 560, 180, 800, 560, [.3, .5, .75, .98], C["red"], ["", "", "", "HOURS USED"])
            + f'<div class="chip" id="{p}-t" style="left:260px;top:220px;font-size:44px">#2: ENGAGEMENT ≠ VALUE</div>'
            + f'<div class="chip white" id="{p}-q" style="left:1400px;top:420px;font-size:40px">WHY CAN\'T<br>THEY STOP?</div>')
    js = [pop(f"#{p}-t", cue(n, "second")), rise(f"#{p}-ch", .2), grow_bars(f"{p}-ch", cue(n, "stop"), 4), pop(f"#{p}-q", cue(n, "asking"))]
    W(n, html, js, "office")


@frame
def f39():
    n, p = 39, "f39"
    scale = f'<svg id="{p}-sc" style="position:absolute;left:560px;top:260px;overflow:visible" width="800" height="520"><rect x="390" y="80" width="20" height="400" fill="{C["ink"]}"/><rect x="300" y="470" width="200" height="30" rx="10" fill="{C["ink"]}"/><g id="{p}-beam"><rect x="40" y="70" width="720" height="18" rx="9" fill="{C["ink"]}"/><rect x="40" y="88" width="200" height="80" rx="12" fill="{C["gold"]}"/><rect x="560" y="88" width="200" height="80" rx="12" fill="{C["teal"]}"/><text x="140" y="140" text-anchor="middle" font-family="Inter" font-weight="900" font-size="28" fill="#1E1B2E">GROWTH</text><text x="660" y="140" text-anchor="middle" font-family="Inter" font-weight="900" font-size="28" fill="#fff">SAFETY</text></g></svg>'
    html = scale + f'<div class="chip" id="{p}-t" style="left:260px;top:180px;font-size:44px">#3: SAFETY IS THE BUSINESS</div>'
    js = [pop(f"#{p}-t", cue(n, "third")), rise(f"#{p}-sc", .2),
          f'tl.fromTo("#{p}-beam",{{rotation:-12,svgOrigin:"400 80"}},{{rotation:12,svgOrigin:"400 80",duration:1.0,ease:"elastic.out(1,.5)"}},{cue(n, "safety"):.2f});']
    W(n, html, js, "day")


@frame
def f40():
    n, p = 40, "f40"
    html = "".join(building(f"{p}-b{i}", 260 + i*480, 260 - i*20, 380, 600 + i*20, ["#5C7CFA", "#845EF7", "#20C997"][i], f"BIG CO #{i+1}") for i in range(3))
    html += "".join(avatar(f"{p}-a{i}", 360 + i*480, 120, k, 170) for i, k in enumerate(["friend", "anime", "wizard"]))
    html += f'<div class="chip red" id="{p}-q" style="left:700px;top:30px;font-size:48px">WHO\'S RESPONSIBLE?</div>'
    js = [rise(f"#{p}-b{i}", cue(n, "bigger") + i * .2) for i in range(3)] + [pop(f"#{p}-a{i}", cue(n, "building") + i * .2) for i in range(3)] + [pop(f"#{p}-q", cue(n, "responsible"))]
    W(n, html, js, "dusk")


@frame
def f41():
    n, p = 41, "f41"
    d = P.dur(n)
    blink = "".join(f'tl.to("#{p}-cur",{{opacity:{0 if k%2==0 else 1},duration:.01}},{.5 + k*.5:.2f});' for k in range(int((d-.6)/.5)))
    html = (f'<div class="card" id="{p}-w" style="left:460px;top:170px;width:1000px;height:600px;padding:50px"><div class="lbl" style="font-size:28px;color:{C["muted"]}">NEW CHAT</div>'
            f'<div style="position:absolute;left:50px;right:50px;bottom:50px;height:90px;border-radius:20px;background:#F1EEF8;display:flex;align-items:center;padding-left:30px"><div id="{p}-cur" style="width:6px;height:50px;background:{C["ink"]}"></div></div></div>'
            + f'<div class="chip" id="{p}-b" style="left:760px;top:830px;font-size:40px">WAITING FOR A BUYER</div>')
    js = [rise(f"#{p}-w", .1), pop(f"#{p}-b", cue(n, "buy")), blink]
    W(n, html, js, "night", s1=1.04)


@frame
def f42():
    n, p = 42, "f42"
    html = (f'<svg style="position:absolute;left:560px;top:120px" width="800" height="420"><path id="{p}-ln" d="M20 380 L200 300 L360 240 L540 60 L620 380" stroke="#fff" stroke-width="16" fill="none" stroke-linejoin="round" stroke-linecap="round"/></svg>'
            + f'<div class="big" id="{p}-logo" style="left:0;right:0;top:560px;text-align:center;font-size:120px;color:#fff">RISE<span style="color:{C["red"]}">&amp;</span>RUIN</div>'
            + f'<div id="{p}-row" style="position:absolute;left:0;right:0;top:720px;display:flex;justify-content:center;gap:26px"><div class="chip white" style="position:relative">FOLLOW FOR THE NEXT FALL</div><div class="chip red" id="{p}-sub" style="position:relative">SUBSCRIBE</div></div>')
    js = [draw(f"#{p}-ln", .1, 1.6, 1400), rise(f"#{p}-logo", .8), rise(f"#{p}-row", cue(n, "subscribe")),
          f'tl.to("#{p}-sub",{{scale:1.12,duration:.2}},{cue(n, "subscribe")+.6:.2f});tl.to("#{p}-sub",{{scale:1,duration:.2}},{cue(n, "subscribe")+.8:.2f});']
    W(n, html, js, "night", s1=1.03)


if __name__ == "__main__":
    for k in sorted(F):
        F[k]()
    print("ok", len(F))
