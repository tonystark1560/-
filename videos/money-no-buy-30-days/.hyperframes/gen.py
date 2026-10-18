"""Money Unlocked #1 — What Happens If You Stop Buying for 30 Days (orchestrator-authored frames)."""
import os, sys
sys.path.insert(0, "/home/user/-/videos/_tools")
from hf import Project, pop, rise, slide, fade, draw, stamp, shake, bob, pixel

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = Project(ROOT)
cue = P.cue
C = dict(bg="#F1FBF5", primary="#0E9F6E", text="#14213D", muted="#4B5B73", light="#94A3B8", red="#E24040",
         coin="#FBBF24", coin2="#FDE68A", mint="#C9F2DC", lemon="#FFF3C4", peach="#FFE1EC", blue="#4C6EF5")

COIN = ["...yyyy...", "..yyyyyy..", ".yyooyyyy.", ".ywwyywwy.", ".ywkyywky.", ".yyyyyyyy.", ".yyymmyyy.", "..yyyyyy..",
        "...yyyy...", "...k..k...", "..kk..kk.."]
CPAL = {"y": C["coin"], "o": C["coin2"], "w": "#fff", "k": C["text"], "m": "#B45309"}
ICONS = {
    "cart": ["k.......", "kkkkkkkk", ".kggggk.", ".kggggk.", "..kkkkk.", "..k...k."],
    "bag": ["..kkkk..", ".k....k.", "gggggggg", "gggggggg", "gggggggg", "gggggggg"],
    "phone": ["kkkkk", "kbbbk", "kbbbk", "kbbbk", "kbbbk", "kkkkk"],
    "coffee": [".w.w.", "kkkkk.", "kooookk", "koooo.k", "kookk", ".kkk."],
    "house": ["....g....", "...ggg...", "..ggggg..", ".ggggggg.", ".wwwwwww.", ".wbbwkkw.", ".wbbwkkw."],
    "heart": [".rr.rr.", "rrrrrrr", "rrrrrrr", ".rrrrr.", "..rrr..", "...r..."],
    "gift": ["..r.r..", "...r...", "ggggggg", "gggrggg", "gggrggg", "gggrggg"],
    "brain": [".pppp.", "pppppp", "pp.ppp", "pppppp", ".pppp.", "..pp.."],
    "shield": ["ggggg", "gwwwg", "gwgwg", "gwwwg", ".ggg.", "..g.."],
    "cal": ["rrrrrrr", "wwwwwww", "wkwkwkw", "wwwwwww", "wkwkwkw", "wwwwwww"],
    "check": ["......g", ".....gg", "g...gg.", "gg.gg..", ".ggg...", "..g...."],
    "cross": ["r....r", ".r..r.", "..rr..", "..rr..", ".r..r.", "r....r"],
    "pause": ["kk.kk", "kk.kk", "kk.kk", "kk.kk", "kk.kk"],
    "bill": ["gggggggg", "gwwggwwg", "gwgyygwg", "gwwggwwg", "gggggggg"],
    "egg": [".ww.", "wwww", "wwww", ".ww."],
    "piggy": [".pppppp.", "pppppppp", "ppkppppp", "pppppppp", ".pppppp.", ".p.pp.p."],
}
IPAL = {"k": C["text"], "g": C["primary"], "w": "#fff", "b": "#9BE7FF", "o": "#A16207", "r": C["red"], "p": "#FF8FB1", "y": C["coin"]}


def icon(name, size=110, ident=""):
    return pixel(ICONS[name], IPAL, size, ident=ident)


def coin_mascot(ident, size=220):
    return pixel(COIN, CPAL, size, ident=ident)


CSS = f"""
.blob{{position:absolute;border-radius:50%;filter:blur(110px);opacity:.9;}}
.card{{position:absolute;background:rgba(255,255,255,.92);border-radius:22px;box-shadow:0 18px 50px rgba(14,159,110,.14),0 2px 6px rgba(20,33,61,.06);}}
.pill{{position:absolute;display:inline-flex;align-items:center;gap:10px;padding:12px 26px;border-radius:999px;font-weight:800;font-size:26px;letter-spacing:.08em;text-transform:uppercase;background:{C['primary']};color:#fff;}}
.chip{{position:absolute;padding:12px 24px;border-radius:999px;font-weight:800;font-size:28px;color:#fff;background:{C['primary']};}}
.chip.red{{background:{C['red']};}} .chip.dark{{background:{C['text']};}} .chip.white{{background:#fff;color:{C['text']};box-shadow:0 10px 30px rgba(14,159,110,.15);}}
.h{{position:absolute;font-weight:900;letter-spacing:-.02em;line-height:1;color:{C['text']};}}
.h span{{color:{C['primary']};}} .h .r{{color:{C['red']};}}
.lbl{{font-weight:800;font-size:32px;color:{C['text']};}}
.sub{{font-weight:600;font-size:22px;color:{C['muted']};}}
.tile{{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;text-align:center;}}
.mascot{{position:absolute;filter:drop-shadow(0 14px 22px rgba(180,120,0,.35));}}
.win-bar{{height:60px;background:rgba(241,251,245,.95);display:flex;align-items:center;padding:0 22px;gap:12px;border-bottom:1.5px solid rgba(14,159,110,.15);}}
.dot{{width:15px;height:15px;border-radius:50%;}}
"""


def bg(p, d):
    h = (f'<div style="position:absolute;inset:0;background:{C["bg"]}"></div>'
         f'<div class="blob" id="{p}-b1" style="width:900px;height:900px;left:-220px;top:-260px;background:{C["mint"]}"></div>'
         f'<div class="blob" id="{p}-b2" style="width:800px;height:800px;right:-160px;top:140px;background:{C["lemon"]}"></div>'
         f'<div class="blob" id="{p}-b3" style="width:700px;height:700px;left:540px;bottom:-420px;background:{C["peach"]}"></div>')
    js = (f'tl.fromTo("#{p}-b1",{{x:0,y:0}},{{x:140,y:60,duration:{d:.2f},ease:"none"}},0);'
          f'tl.fromTo("#{p}-b2",{{x:0,y:0}},{{x:-120,y:-50,duration:{d:.2f},ease:"none"}},0);'
          f'tl.fromTo("#{p}-b3",{{x:0,y:0}},{{x:-90,y:-40,duration:{d:.2f},ease:"none"}},0);')
    return h, js


def W(n, html, js, css=""):
    p = f"f{n:02d}"
    h, bj = bg(p, P.dur(n))
    P.write(n, CSS + css, html, js, h, bj)


def mascot(p, n, x, y, size=220, t=.2):
    html = f'<div class="mascot" id="{p}-m" style="left:{x}px;top:{y}px">{coin_mascot(p+"-ms", size)}</div>'
    d = P.dur(n)
    js = [f'tl.fromTo("#{p}-m",{{y:80,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"back.out(1.6)"}},{t});', bob(f"#{p}-m", t + .6, d, 9, 1.6)]
    return html, js


def eyebrow(p, text, t=.1):
    return f'<div class="pill" id="{p}-eb" style="left:110px;top:100px">{text}</div>', rise(f"#{p}-eb", t)


def window(ident, x, y, w, h, title, body):
    return (f'<div class="card" id="{ident}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:hidden">'
            f'<div class="win-bar"><div class="dot" style="background:#FF5F57"></div><div class="dot" style="background:#FEBC2E"></div><div class="dot" style="background:#28C840"></div>'
            f'<div class="sub" style="margin-left:14px">{title}</div></div><div style="padding:34px 50px">{body}</div></div>')


def tiles(p, items, x0, y0, w, h, gap, cols, prefix="t"):
    out = []
    for i, (ic, label, sub) in enumerate(items):
        x, y = x0 + (i % cols) * (w + gap), y0 + (i // cols) * (h + gap)
        out.append(f'<div class="card tile" id="{p}-{prefix}{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
                   f'{icon(ic, 100) if ic else ""}<div class="lbl">{label}</div>{f"<div class=sub>{sub}</div>" if sub else ""}</div>')
    return "".join(out)


def checklist(p, x, y, w, h, title, items):
    rows = "".join(f'<div id="{p}-r{i}" style="display:flex;align-items:center;gap:24px;height:96px"><div id="{p}-bx{i}" style="width:56px;height:56px;border-radius:14px;border:3px solid rgba(14,159,110,.35);display:flex;align-items:center;justify-content:center">{icon("check", 34, f"{p}-ck{i}")}</div><div class="lbl" style="font-size:40px">{t}</div></div>' for i, t in enumerate(items))
    return window(f"{p}-win", x, y, w, h, title, rows)


def check_js(p, i, t):
    return (f'gsap.set("#{p}-ck{i}",{{opacity:0}});' + slide(f"#{p}-r{i}", t - .2, -40)
            + f'tl.to("#{p}-bx{i}",{{background:"#E7F8F1",borderColor:"{C["primary"]}",duration:.2}},{t+.5:.2f});tl.to("#{p}-ck{i}",{{opacity:1,duration:.2}},{t+.5:.2f});')


F = {}


def frame(fn):
    F[int(fn.__name__[1:])] = fn
    return fn


@frame
def f1():
    n, p = 1, "f01"
    m, mj = mascot(p, n, 260, 420, 260)
    cart = f'<div class="card tile" id="{p}-cart" style="left:860px;top:200px;width:560px;height:520px">{icon("cart", 300)}</div>'
    x = f'<svg id="{p}-x" style="position:absolute;left:860px;top:200px" width="560" height="520"><path id="{p}-x1" d="M90 90 L470 430" stroke="{C["red"]}" stroke-width="30" stroke-linecap="round"/><path id="{p}-x2" d="M470 90 L90 430" stroke="{C["red"]}" stroke-width="30" stroke-linecap="round"/></svg>'
    html = m + cart + x + f'<div class="chip dark" id="{p}-d" style="left:1460px;top:300px;font-size:56px">30 DAYS</div>'
    js = mj + [pop(f"#{p}-cart", .3), pop(f"#{p}-d", cue(n, "30")), draw(f"#{p}-x1", cue(n, "takeout"), .3, 600), draw(f"#{p}-x2", cue(n, "clothes"), .3, 600)]
    W(n, html, js)


@frame
def f2():
    n, p = 2, "f02"
    e, ej = eyebrow(p, "Trending in 2026")
    card = f'<div class="card tile" id="{p}-c" style="left:560px;top:230px;width:800px;height:420px"><div class="h" style="position:relative;font-size:120px">No <span>Buy</span></div><div class="sub" style="font-size:30px">the 2026 money challenge</div></div>'
    hearts = "".join(f'<div id="{p}-h{i}" style="position:absolute;left:{1300 + (i%3)*130}px;top:{260 + (i//3)*170}px">{icon("heart", 90)}</div>' for i in range(6))
    html = e + card + hearts
    js = [ej, pop(f"#{p}-c", cue(n, "challenge"))] + [f'tl.fromTo("#{p}-h{i}",{{y:60,opacity:0}},{{y:0,opacity:1,duration:.4,ease:"back.out(2)"}},{cue(n, "post") + i*.18:.2f});' for i in range(6)]
    W(n, html, js)


@frame
def f3():
    n, p = 3, "f03"
    m, mj = mascot(p, n, 800, 300, 300)
    html = m + f'<div class="chip white" id="{p}-q1" style="left:420px;top:300px;font-size:36px">What happens?</div><div class="chip white" id="{p}-q2" style="left:1200px;top:420px;font-size:36px">What do you learn?</div><div class="chip" id="{p}-u" style="left:820px;top:760px;font-size:36px">Let\'s unlock it</div>'
    js = mj + [pop(f"#{p}-q1", cue(n, "happens")), pop(f"#{p}-q2", cue(n, "learn")), pop(f"#{p}-u", cue(n, "unlock"))]
    W(n, html, js)


@frame
def f4():
    n, p = 4, "f04"
    e, ej = eyebrow(p, "Why now?")
    items = [("cart", "Cost of living", ""), ("shield", "Uncertainty", ""), ("phone", "Shopping burnout", "")]
    html = e + tiles(p, items, 260, 260, 420, 440, 60, 3)
    js = [ej] + [pop(f"#{p}-t{i}", .4 + i*.25) for i in range(3)]
    W(n, html, js)


@frame
def f5():
    n, p = 5, "f05"
    e, ej = eyebrow(p, "1 · Cost of living")
    items = ["Groceries", "Rent", "Insurance", "Eating out"]
    bars = "".join(f'<div style="position:absolute;left:{640 + i*260}px;bottom:300px;width:150px;height:440px;border-radius:20px 20px 6px 6px;background:{C["red"] if i % 2 else C["primary"]};transform-origin:50% 100%" id="{p}-b{i}x"></div><div class="lbl" style="position:absolute;left:{610 + i*260}px;top:810px;width:210px;text-align:center;font-size:26px">{t}</div>' for i, t in enumerate(items))
    html = e + bars + f'<div class="h" id="{p}-h" style="left:110px;top:260px;font-size:84px">Prices<br><span class="r">up</span></div>'
    js = [ej, slide(f"#{p}-h", cue(n, "prices"))] + [f'tl.fromTo("#{p}-b{i}x",{{scaleY:.3}},{{scaleY:{.65 + i*.08:.2f},duration:.8,ease:"back.out(1.4)"}},{cue(n, "gone") + i*.15:.2f});' for i in range(4)]
    W(n, html, js)


@frame
def f6():
    n, p = 6, "f06"
    e, ej = eyebrow(p, "2 · Uncertainty")
    gauge = f'<svg id="{p}-g" style="position:absolute;left:560px;top:200px" width="800" height="480"><path d="M100 420 A 300 300 0 0 1 700 420" stroke="#E3EAF2" stroke-width="50" fill="none"/><path d="M100 420 A 300 300 0 0 1 400 120" stroke="{C["primary"]}" stroke-width="50" fill="none"/><path d="M400 120 A 300 300 0 0 1 700 420" stroke="{C["red"]}" stroke-width="50" fill="none"/><g id="{p}-n"><rect x="394" y="150" width="12" height="270" rx="6" fill="{C["text"]}"/></g><circle cx="400" cy="420" r="24" fill="{C["text"]}"/></svg>'
    html = e + gauge + f'<div class="chip red" id="{p}-pes" style="left:820px;top:720px">PESSIMISTIC</div><div class="chip dark" id="{p}-ctl" style="left:760px;top:820px">YOU CONTROL SPENDING</div>'
    js = [ej, pop(f"#{p}-g", .2), f'tl.fromTo("#{p}-n",{{rotation:-60,svgOrigin:"400 420"}},{{rotation:55,svgOrigin:"400 420",duration:1.2,ease:"elastic.out(1,.5)"}},{cue(n, "pessimistic"):.2f});',
          pop(f"#{p}-pes", cue(n, "pessimistic")), pop(f"#{p}-ctl", cue(n, "control"))]
    W(n, html, js)


@frame
def f7():
    n, p = 7, "f07"
    e, ej = eyebrow(p, "3 · Shopping burnout")
    btns = ["BUY NOW", "1-CLICK", "SALE -40%", "PAY IN 4", "ADD TO CART", "LIMITED!"]
    html = e + "".join(f'<div class="chip {"red" if i % 2 else ""}" id="{p}-k{i}" style="left:{480 + (i%3)*400}px;top:{280 + (i//3)*220}px;font-size:40px">{t}</div>' for i, t in enumerate(btns))
    html += f'<div class="chip dark" id="{p}-ps" style="left:880px;top:760px;font-size:40px">PAUSE</div>'
    js = [ej] + [pop(f"#{p}-k{i}", cue(n, "checkout") + i * .25) for i in range(6)] + [f'tl.to("[id^={p}-k]",{{opacity:.25,duration:.4}},{cue(n, "pause"):.2f});', pop(f"#{p}-ps", cue(n, "pause"))]
    W(n, html, js)


@frame
def f8():
    n, p = 8, "f08"
    book = f'<div class="card tile" id="{p}-bk" style="left:660px;top:220px;width:600px;height:500px"><div class="h" style="position:relative;font-size:72px">The<br><span>rules</span></div><div class="sub" style="font-size:28px">(unofficial)</div></div>'
    html = book
    m, mj = mascot(p, n, 1340, 460, 220)
    js = [pop(f"#{p}-bk", .2)] + mj
    W(n, html + m, js)


@frame
def f9():
    n, p = 9, "f09"
    e, ej = eyebrow(p, "Allowed ✓")
    items = [("house", "Rent", ""), ("bill", "Bills", ""), ("cart", "Groceries", ""), ("shield", "Medicine", "")]
    html = e + tiles(p, items, 200, 280, 360, 400, 40, 4)
    js = [ej] + [pop(f"#{p}-t{i}", cue(n, w)) for i, w in enumerate(["rent", "utilities", "groceries", "medicine"])]
    W(n, html, js)


@frame
def f10():
    n, p = 10, "f10"
    e, ej = eyebrow(p, "Paused ⏸")
    items = [("coffee", "Takeout", ""), ("bag", "New clothes", ""), ("phone", "Gadgets", ""), ("gift", "Random orders", "")]
    html = e.replace(">Paused ⏸<", ">Paused<") + tiles(p, items, 200, 280, 360, 400, 40, 4)
    js = [ej] + [pop(f"#{p}-t{i}", cue(n, w)) for i, w in enumerate(["takeout", "clothes", "gadgets", "random"])]
    js += [f'tl.to("#{p}-t{i}",{{opacity:.45,scale:.95,duration:.3}},{cue(n, "random")+.8 + i*.1:.2f});' for i in range(4)]
    W(n, html, js)


@frame
def f11():
    n, p = 11, "f11"
    e, ej = eyebrow(p, "Replace, don't add")
    html = (e + f'<div class="card tile" id="{p}-a" style="left:360px;top:260px;width:460px;height:460px"><div class="lbl">Shampoo runs out</div><div class="h" style="position:relative;font-size:90px;color:{C["primary"]}">✓</div><div class="sub">buy one</div></div>'
            + f'<div class="card tile" id="{p}-b" style="left:1100px;top:260px;width:460px;height:460px"><div class="lbl">Fancier one on sale</div>{icon("cross", 120)}<div class="sub">skip it</div></div>')
    js = [ej, pop(f"#{p}-a", cue(n, "shampoo")), pop(f"#{p}-b", cue(n, "fancier"))]
    W(n, html, js)


@frame
def f12():
    n, p = 12, "f12"
    note = window(f"{p}-n", 520, 180, 880, 600, "my-rules.md", f'<div class="h" id="{p}-t" style="position:relative;font-size:60px">Essential =</div><div class="lbl" id="{p}-l1" style="margin-top:40px;font-size:40px">rent · food · bills · meds</div><div class="lbl" id="{p}-l2" style="margin-top:30px;font-size:40px;color:{C["red"]}">NOT: "it\'s on sale"</div>')
    js = [rise(f"#{p}-n", .1), rise(f"#{p}-t", cue(n, "write")), rise(f"#{p}-l1", cue(n, "essential")), rise(f"#{p}-l2", cue(n, "magically"))]
    W(n, note, js)


@frame
def f13():
    n, p = 13, "f13"
    e, ej = eyebrow(p, "Smart prep")
    html = e + checklist(p, 460, 200, 1000, 560, "prep.md", ["Unsubscribe from store emails", "Delete shopping apps", "Remove saved cards"])
    js = [ej, rise(f"#{p}-win", .2)] + [check_js(p, i, cue(n, w)) for i, w in enumerate(["unsubscribe", "delete", "saved"])]
    W(n, html, js)


@frame
def f14():
    n, p = 14, "f14"
    e, ej = eyebrow(p, "Quick math")
    steps = [("$15", "a day"), ("$450", "a month"), ("$5,400", "a year")]
    html = e + "".join(f'<div class="card tile" id="{p}-s{i}" style="left:{200 + i*560}px;top:300px;width:480px;height:360px"><div class="h" style="position:relative;font-size:{110 if i < 2 else 96}px;color:{C["primary"] if i < 2 else C["red"]}">{a}</div><div class="lbl">{b}</div></div>' for i, (a, b) in enumerate(steps))
    html += "".join(f'<div class="h" id="{p}-a{i}" style="left:{690 + i*560}px;top:430px;font-size:80px;color:{C["muted"]}">→</div>' for i in range(2))
    js = [ej, pop(f"#{p}-s0", cue(n, "15")), pop(f"#{p}-a0", cue(n, "month") - .3), pop(f"#{p}-s1", cue(n, "450")), pop(f"#{p}-a1", cue(n, "year") - .3), pop(f"#{p}-s2", cue(n, "5000", frac=.65))]
    W(n, html, js)


@frame
def f15():
    n, p = 15, "f15"
    m, mj = mascot(p, n, 300, 400, 260)
    coins = "".join(f'<div id="{p}-c{i}" style="position:absolute;left:400px;top:420px">{icon("bill", 90)}</div>' for i in range(6))
    html = m + coins + f'<div class="chip dark" id="{p}-ap" style="left:900px;top:300px;font-size:56px">AUTOPILOT</div>'
    js = mj + [f'tl.fromTo("#{p}-c{i}",{{x:0,y:0,opacity:0}},{{x:{600 + i*120},y:{-200 + (i%3)*140},opacity:1,duration:1.4,ease:"power2.out"}},{cue(n, "autopilot") - 1 + i*.3:.2f});' for i in range(6)]
    js.append(pop(f"#{p}-ap", cue(n, "autopilot")))
    W(n, html, js)


@frame
def f16():
    n, p = 16, "f16"
    rows = [("StreamMax", "$15.99"), ("FitApp Pro", "$9.99"), ("PhotoCloud", "$4.99"), ("MusicPlus", "$11.99")]
    body = "".join(f'<div id="{p}-r{i}" style="display:flex;justify-content:space-between;align-items:center;height:92px;border-bottom:1.5px solid #E6EEF2"><div class="lbl" style="font-size:38px">{a}</div><div class="lbl" style="font-size:38px;color:{C["red"]}">{b}/mo</div></div>' for i, (a, b) in enumerate(rows))
    html = window(f"{p}-w", 460, 170, 1000, 560, "subscriptions", body) + f'<div class="chip red" id="{p}-f" style="left:820px;top:780px;font-size:36px">FORGOT ABOUT THESE?</div>'
    js = [rise(f"#{p}-w", .1)] + [slide(f"#{p}-r{i}", cue(n, "subscriptions") + i*.6, -40) for i in range(4)] + [pop(f"#{p}-f", cue(n, "2023"))]
    W(n, html, js)


@frame
def f17():
    n, p = 17, "f17"
    lines = ["Coffee $5.50", "Snack $3.20", "Just $12", "Just $12", "Just $12", "Just $12", "Just $12", "Just $12"]
    body = "".join(f'<div class="lbl" id="{p}-l{i}" style="font-size:32px;padding:8px 0;border-bottom:2px dashed #E6EEF2">{t}</div>' for i, t in enumerate(lines))
    html = (f'<div class="card" id="{p}-rc" style="left:300px;top:110px;width:560px;height:760px;padding:40px;overflow:hidden">{body}</div>'
            + f'<div class="card tile" id="{p}-tot" style="left:1060px;top:300px;width:600px;height:340px"><div class="sub" style="font-size:30px">ADDED UP</div><div class="h" style="position:relative;font-size:120px;color:{C["red"]}">$100s</div></div>')
    js = [rise(f"#{p}-rc", .1)] + [slide(f"#{p}-l{i}", cue(n, "coffee") + i*.45, -30) for i in range(8)] + [pop(f"#{p}-tot", cue(n, "hundreds"))]
    W(n, html, js)


@frame
def f18():
    n, p = 18, "f18"
    loop = f'''<svg id="{p}-lp" style="position:absolute;left:760px;top:170px" width="800" height="640"><circle cx="400" cy="320" r="240" fill="none" stroke="rgba(14,159,110,.25)" stroke-width="18"/><circle id="{p}-dot" cx="400" cy="80" r="26" fill="{C["coin"]}"/></svg>'''
    labels = [("BROWSE", 1080, 170), ("ADD TO CART", 1420, 470), ("WAIT FOR BOX", 1080, 780), ("REWARD!", 700, 470)]
    html = loop + "".join(f'<div class="chip white" id="{p}-k{i}" style="left:{x-120}px;top:{y-28}px">{t}</div>' for i, (t, x, y) in enumerate(labels))
    html += f'<div class="card tile" id="{p}-br" style="left:160px;top:300px;width:420px;height:420px">{icon("brain", 200)}<div class="lbl">Reward hit</div></div>'
    js = [pop(f"#{p}-br", cue(n, "brain"))] + [pop(f"#{p}-k{i}", cue(n, w)) for i, w in enumerate(["browsing", "adding", "waiting", "good"])]
    js.append(f'tl.fromTo("#{p}-dot",{{rotation:0,svgOrigin:"400 320"}},{{rotation:1080,svgOrigin:"400 320",duration:{P.dur(n) - cue(n, "loop") + 3:.2f},ease:"power1.inOut"}},{max(.3, cue(n, "loop") - 3):.2f});')
    js.append(f'tl.to("#{p}-lp circle:first-child",{{stroke:"{C["red"]}",duration:.4}},{cue(n, "breaking"):.2f});')
    W(n, html, js)


@frame
def f19():
    n, p = 19, "f19"
    m, mj = mascot(p, n, 360, 420, 240)
    ph = f'<div class="card" id="{p}-ph" style="left:860px;top:150px;width:360px;height:680px;background:{C["text"]};padding:18px"><div style="width:100%;height:100%;border-radius:20px;background:#fff;display:flex;flex-direction:column;gap:18px;padding:24px"><div class="chip" style="position:relative">SHOP</div><div class="chip red" style="position:relative">SALE</div><div class="chip dark" style="position:relative">NEW!</div></div></div>'
    html = m + ph + f'<div class="chip white" id="{p}-bo" style="left:1320px;top:380px;font-size:40px">Bored, not in need</div>'
    js = mj + [rise(f"#{p}-ph", cue(n, "phone")), pop(f"#{p}-bo", cue(n, "boredom"))]
    W(n, html, js)


@frame
def f20():
    n, p = 20, "f20"
    rows = [("Sneakers", "bored"), ("Candle", "stressed"), ("Headphones", "tired")]
    body = "".join(f'<div id="{p}-r{i}" style="display:flex;justify-content:space-between;align-items:center;height:96px;border-bottom:1.5px solid #E6EEF2"><div class="lbl" style="font-size:38px">{a}</div><div class="chip white" style="position:relative;font-size:28px">{b}</div></div>' for i, (a, b) in enumerate(rows))
    html = window(f"{p}-w", 460, 170, 1000, 520, "urge-journal.md", body) + f'<div class="chip" id="{p}-pt" style="left:860px;top:740px;font-size:36px">PATTERNS!</div>'
    js = [rise(f"#{p}-w", .1)] + [slide(f"#{p}-r{i}", cue(n, w), -40) for i, w in enumerate(["write", "bored", "tired"])] + [pop(f"#{p}-pt", cue(n, "patterns"))]
    W(n, html, js)


@frame
def f21():
    n, p = 21, "f21"
    cal = "".join(f'<div id="{p}-d{i}" style="width:120px;height:110px;border-radius:16px;background:{C["primary"] if i < 7 else ("#FFE4E4" if i < 14 else "#EEF3F6")};display:flex;align-items:center;justify-content:center;font-weight:900;font-size:36px;color:{"#fff" if i < 7 else C["text"]}">{i+1}</div>' for i in range(21))
    html = f'<div class="card" id="{p}-c" style="left:420px;top:150px;width:1080px;height:600px;padding:40px;display:grid;grid-template-columns:repeat(7,120px);gap:20px">{cal}</div><div class="chip red" id="{p}-w" style="left:860px;top:800px;font-size:40px">WEEK 2 = HARDEST</div>'
    js = [rise(f"#{p}-c", .1), f'tl.fromTo("[id^={p}-d]",{{scale:.6,opacity:0}},{{scale:1,opacity:1,duration:.25,stagger:.04}},.3);', pop(f"#{p}-w", cue(n, "hardest"))]
    js.append(f'tl.to(["#{p}-d7","#{p}-d8","#{p}-d9","#{p}-d10","#{p}-d11","#{p}-d12","#{p}-d13"],{{scale:1.08,duration:.3,stagger:.05}},{cue(n, "urges"):.2f});')
    W(n, html, js)


@frame
def f22():
    n, p = 22, "f22"
    items = [("bag", "Sale on your wishlist", ""), ("coffee", "Fancy dinner invite", ""), ("heart", "Bad day, treat yourself", "")]
    html = tiles(p, items, 220, 250, 460, 440, 40, 3)
    js = [pop(f"#{p}-t{i}", cue(n, w)) for i, w in enumerate(["sale", "dinner", "terrible"])]
    W(n, html, js)


@frame
def f23():
    n, p = 23, "f23"
    rows = [("Air fryer", "Oct 3"), ("Jacket", "Oct 5"), ("Game", "Oct 9")]
    body = "".join(f'<div id="{p}-r{i}" style="display:flex;justify-content:space-between;align-items:center;height:96px;border-bottom:1.5px solid #E6EEF2"><div class="lbl" style="font-size:38px">{a}</div><div class="sub" style="font-size:28px">{b}</div></div>' for i, (a, b) in enumerate(rows))
    html = window(f"{p}-w", 460, 170, 1000, 520, "48-hour-list.md", body) + f'<div class="chip dark" id="{p}-tm" style="left:1420px;top:120px;font-size:44px">48:00</div>' + f'<div class="chip" id="{p}-fg" style="left:800px;top:740px;font-size:36px">MOST GET FORGOTTEN</div>'
    js = [rise(f"#{p}-w", .1), pop(f"#{p}-tm", cue(n, "48"))] + [slide(f"#{p}-r{i}", cue(n, "list") + i*.4, -40) for i in range(3)]
    js += [f'tl.to("#{p}-r{i}",{{opacity:.3,duration:.4}},{cue(n, "forgotten") + i*.15:.2f});' for i in range(3)] + [pop(f"#{p}-fg", cue(n, "forgotten"))]
    W(n, html, js)


@frame
def f24():
    n, p = 24, "f24"
    items = [("shield", "Walk", "not a shopping trip"), ("brain", "Library", "not a new book"), ("coffee", "Cook", "not delivery"), ("heart", "Host friends", "not going out")]
    html = tiles(p, items, 180, 260, 370, 420, 40, 4)
    js = [pop(f"#{p}-t{i}", cue(n, w)) for i, w in enumerate(["walk", "library", "cooking", "inviting"])]
    W(n, html, js)


@frame
def f25():
    n, p = 25, "f25"
    m, mj = mascot(p, n, 820, 330, 260)
    html = m + f'<div class="chip white" id="{p}-s" style="left:400px;top:300px;font-size:40px">Slipped?</div><div class="chip" id="{p}-k" style="left:1240px;top:340px;font-size:40px">Keep going</div><div class="chip dark" id="{p}-c" style="left:760px;top:780px;font-size:40px">1 slip ≠ 20 good days</div>'
    js = mj + [pop(f"#{p}-s", cue(n, "slip")), f'tl.to("#{p}-m",{{rotation:-20,duration:.25}},{cue(n, "slip"):.2f});tl.to("#{p}-m",{{rotation:0,duration:.4,ease:"back.out(2)"}},{cue(n, "quit"):.2f});',
                pop(f"#{p}-k", cue(n, "going")), pop(f"#{p}-c", cue(n, "erase"))]
    W(n, html, js)


@frame
def f26():
    n, p = 26, "f26"
    ev = [("Friend's birthday", "Oct 8"), ("Wedding", "Oct 19"), ("Team dinner", "Oct 24")]
    body = "".join(f'<div id="{p}-r{i}" style="display:flex;justify-content:space-between;align-items:center;height:96px;border-bottom:1.5px solid #E6EEF2"><div class="lbl" style="font-size:38px">{a}</div><div class="sub" style="font-size:28px">{b}</div></div>' for i, (a, b) in enumerate(ev))
    html = window(f"{p}-w", 260, 180, 860, 500, "calendar", body) + f'<div class="card tile" id="{p}-g" style="left:1240px;top:220px;width:420px;height:420px">{icon("gift", 160)}<div class="lbl">Gift fund</div><div class="sub">set aside upfront</div></div>'
    html += f'<div class="chip" id="{p}-sh" style="left:620px;top:760px;font-size:36px">SHOWING UP > SPENDING</div>'
    js = [rise(f"#{p}-w", .1)] + [slide(f"#{p}-r{i}", cue(n, w), -40) for i, w in enumerate(["birthdays", "weddings", "nights"])] + [pop(f"#{p}-g", cue(n, "aside")), pop(f"#{p}-sh", cue(n, "showing"))]
    W(n, html, js)


@frame
def f27():
    n, p = 27, "f27"
    m, mj = mascot(p, n, 820, 360, 260)
    stores = "".join(f'<div class="card tile" id="{p}-s{i}" style="left:{200 + i*1180}px;top:300px;width:340px;height:380px"><div class="lbl" style="font-size:40px">SALE</div>{icon("bag", 120)}</div>' for i in range(2))
    html = stores + m + f'<div class="chip" id="{p}-q" style="left:780px;top:220px;font-size:40px">Urge: quieter</div>'
    js = mj + [pop(f"#{p}-s0", .3), pop(f"#{p}-s1", .5), f'tl.to(["#{p}-s0","#{p}-s1"],{{opacity:.3,scale:.92,duration:.8}},{cue(n, "quieter"):.2f});', pop(f"#{p}-q", cue(n, "quieter"))]
    W(n, html, js)


@frame
def f28():
    n, p = 28, "f28"
    items = [("bag", "Clothes with tags", ""), ("cart", "Forgotten pantry food", ""), ("brain", "Unread books", "")]
    html = tiles(p, items, 220, 260, 460, 420, 40, 3)
    js = [pop(f"#{p}-t{i}", cue(n, w)) for i, w in enumerate(["clothes", "pantry", "books"])]
    W(n, html, js)


@frame
def f29():
    n, p = 29, "f29"
    pig = f'<div class="card tile" id="{p}-pg" style="left:660px;top:200px;width:600px;height:520px">{icon("piggy", 300)}<div class="lbl" style="font-size:44px">Saved</div></div>'
    coins = "".join(f'<div id="{p}-c{i}" style="position:absolute;left:{800 + i*70}px;top:-120px">{coin_mascot(f"{p}-cc{i}", 80)}</div>' for i, _ in enumerate(range(5)))
    html = pig + coins
    js = [pop(f"#{p}-pg", .2)] + [f'tl.fromTo("#{p}-c{i}",{{y:0,opacity:0}},{{y:420,opacity:1,duration:.6,ease:"bounce.out"}},{cue(n, "money") + i*.25:.2f});' for i in range(5)]
    W(n, html, js)


@frame
def f30():
    n, p = 30, "f30"
    m, mj = mascot(p, n, 820, 330, 280)
    html = m + f'<div class="h" id="{p}-c" style="left:0;right:0;top:160px;text-align:center;font-size:110px">In <span>control</span></div>' + f'<div class="chip white" id="{p}-a" style="left:360px;top:520px;font-size:36px">not the ads</div><div class="chip white" id="{p}-b" style="left:1260px;top:520px;font-size:36px">not the apps</div>'
    js = mj + [rise(f"#{p}-c", cue(n, "control")), pop(f"#{p}-a", cue(n, "ads")), pop(f"#{p}-b", cue(n, "apps"))]
    W(n, html, js)


@frame
def f31():
    n, p = 31, "f31"
    head = ["Day", "Wanted", "Why", "Saved"]
    rows = [("3", "Sneakers", "bored", "$90"), ("7", "Takeout", "tired", "$28"), ("12", "Candle", "stress", "$22")]
    hd = "".join(f'<div class="sub" style="font-size:26px;font-weight:800">{h}</div>' for h in head)
    body = f'<div style="display:grid;grid-template-columns:120px 1fr 1fr 140px;gap:18px 20px">{hd}' + "".join("".join(f'<div class="lbl {p}-row{i}" style="font-size:34px;{"color:" + C["primary"] if j == 3 else ""}">{c}</div>' for j, c in enumerate(r)) for i, r in enumerate(rows)) + '</div>'
    html = window(f"{p}-w", 420, 180, 1080, 520, "tracker", body) + f'<div class="chip" id="{p}-mp" style="left:780px;top:760px;font-size:36px">A MAP OF YOUR TRIGGERS</div>'
    js = [rise(f"#{p}-w", cue(n, "tracker"))] + [f'tl.fromTo(".{p}-row{i}",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:.3,stagger:.05}},{cue(n, w):.2f});' for i, w in enumerate(["day", "why", "spend"])] + [pop(f"#{p}-mp", cue(n, "map"))]
    W(n, html, js)


@frame
def f32():
    n, p = 32, "f32"
    m, mj = mascot(p, n, 300, 420, 240)
    door = f'<div class="card tile" id="{p}-door" style="left:820px;top:170px;width:420px;height:640px;background:{C["primary"]}"><div class="h" style="position:relative;font-size:90px;color:#fff">DAY<br>31</div></div>'
    cart = f'<div id="{p}-sp" style="position:absolute;left:1320px;top:360px">{icon("cart", 240)}</div><div class="chip red" id="{p}-x" style="left:1320px;top:640px;font-size:36px">SHOPPING SPREE ✗</div>'
    html = m + door + cart
    js = mj + [pop(f"#{p}-door", cue(n, "31")), pop(f"#{p}-sp", cue(n, "spree")), pop(f"#{p}-x", cue(n, "undo"))]
    W(n, html, js)


@frame
def f33():
    n, p = 33, "f33"
    items = [("piggy", "Savings account", ""), ("bill", "Pay down debt", ""), ("shield", "Emergency fund", "")]
    html = tiles(p, items, 220, 260, 460, 420, 40, 3) + f'<div class="chip dark" id="{p}-d" style="left:780px;top:760px;font-size:36px">DECIDE IN ADVANCE</div>'
    js = [pop(f"#{p}-d", cue(n, "decide"))] + [pop(f"#{p}-t{i}", cue(n, w)) for i, w in enumerate(["savings", "debt", "emergency"])]
    W(n, html, js)


@frame
def f34():
    n, p = 34, "f34"
    html = checklist(p, 460, 200, 1000, 520, "48-hour-list.md", ["Air fryer — still want it", "Jacket — meh", "Game — forgot it"])
    js = [rise(f"#{p}-win", .1)] + [check_js(p, i, cue(n, "want") + i*.6) for i in range(3)]
    js += [f'tl.to("#{p}-r1, #{p}-r2",{{opacity:.35,duration:.4}},{cue(n, "afford"):.2f});']
    W(n, html, js)


@frame
def f35():
    n, p = 35, "f35"
    html = checklist(p, 460, 200, 1000, 560, "keep-the-wins.md", ["Cancelled subs stay cancelled", "Shopping apps stay deleted", "One No Buy month per season"])
    js = [rise(f"#{p}-win", .1)] + [check_js(p, i, cue(n, w)) for i, w in enumerate(["subscriptions", "apps", "season"])]
    W(n, html, js)


@frame
def f36():
    n, p = 36, "f36"
    steps = [("shield", "1. Emergency fund", "a few hundred $"), ("bill", "2. High-interest debt", "20%+ cards first"), ("heart", "3. A goal you love", "trip · laptop · invest")]
    html = tiles(p, steps, 200, 260, 480, 440, 40, 3)
    js = [pop(f"#{p}-t{i}", cue(n, w)) for i, w in enumerate(["emergency", "debt", "goal"])]
    js.append(f'tl.to("[id^={p}-t]",{{y:-14,duration:.3,stagger:.08}},{cue(n, "job"):.2f});')
    W(n, html, js)


@frame
def f37():
    n, p = 37, "f37"
    m, mj = mascot(p, n, 820, 330, 280)
    html = m + f'<div class="h" id="{p}-t" style="left:0;right:0;top:150px;text-align:center;font-size:96px">Gentler <span>versions</span></div>'
    js = mj + [rise(f"#{p}-t", cue(n, "gentler"))]
    W(n, html, js)


@frame
def f38():
    n, p = 38, "f38"
    bar = f'<div class="card" id="{p}-c" style="left:460px;top:250px;width:1000px;height:420px;padding:60px"><div class="h" style="position:relative;font-size:84px">Low <span>Buy</span></div><div class="sub" style="font-size:30px;margin-top:20px">small fun budget</div><div style="margin-top:40px;height:36px;border-radius:18px;background:#E6EEF2"><div id="{p}-f" style="height:100%;width:100%;border-radius:18px;background:{C["primary"]};transform-origin:0 50%"></div></div></div>'
    js = [rise(f"#{p}-c", .1), f'tl.fromTo("#{p}-f",{{scaleX:0}},{{scaleX:.35,duration:1,ease:"power2.out"}},{cue(n, "budget"):.2f});']
    W(n, bar, js)


@frame
def f39():
    n, p = 39, "f39"
    items = [("bag", "Clothes", ""), ("coffee", "Takeout", ""), ("phone", "Online", "")]
    html = f'<div class="h" id="{p}-h" style="left:110px;top:120px;font-size:72px">Category <span>No Buy</span></div>' + tiles(p, items, 220, 320, 460, 400, 40, 3)
    js = [rise(f"#{p}-h", .1)] + [pop(f"#{p}-t{i}", cue(n, w)) for i, w in enumerate(["clothes", "takeout", "online"])]
    js += [f'tl.to("#{p}-t1, #{p}-t2",{{opacity:.35,duration:.4}},{cue(n, "else"):.2f});']
    W(n, html, js)


@frame
def f40():
    n, p = 40, "f40"
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    cells = "".join(f'<div id="{p}-d{i}" style="width:180px;height:200px;border-radius:20px;background:{"#E7F8F1" if i >= 5 else "#F3F6F8"};border:4px solid {C["primary"] if i >= 5 else "transparent"};display:flex;align-items:center;justify-content:center;font-weight:900;font-size:36px;color:{C["text"]}">{d}</div>' for i, d in enumerate(days))
    html = f'<div class="h" id="{p}-h" style="left:110px;top:120px;font-size:72px">No Spend <span>Weekends</span></div><div class="card" id="{p}-c" style="left:160px;top:330px;width:1600px;height:320px;padding:60px;display:flex;gap:30px">{cells}</div>'
    js = [rise(f"#{p}-h", .1), rise(f"#{p}-c", .3), f'tl.to(["#{p}-d5","#{p}-d6"],{{scale:1.1,duration:.4,ease:"back.out(3)"}},{cue(n, "two"):.2f});']
    W(n, html, js)


@frame
def f41():
    n, p = 41, "f41"
    html = checklist(p, 400, 130, 1120, 700, "recap.md", ["Write rules first", "Week 1: autopilot", "Week 2: hardest", "48-hour list", "Day 31: give money a job"])
    js = [rise(f"#{p}-win", .1)] + [check_js(p, i, cue(n, w)) for i, w in enumerate(["rules", "week", "two", "48", "31"])]
    W(n, html, js, css=f"#{p}-win .lbl{{font-size:34px !important;}}")


@frame
def f42():
    n, p = 42, "f42"
    cal = "".join(f'<div id="{p}-d{i}" style="width:150px;height:150px;border-radius:20px;background:#F3F6F8;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:44px;color:{C["text"]}">{i+1}</div>' for i in range(7))
    html = f'<div class="h" id="{p}-h" style="left:110px;top:140px;font-size:80px">Start with <span>1 week</span></div><div class="card" id="{p}-c" style="left:260px;top:380px;width:1400px;height:280px;padding:60px;display:flex;gap:40px">{cal}</div>'
    js = [rise(f"#{p}-h", .1), rise(f"#{p}-c", .3)] + [f'tl.to("#{p}-d{i}",{{background:"{C["primary"]}",color:"#fff",duration:.2}},{cue(n, "week") + .4 + i*.35:.2f});' for i in range(7)]
    W(n, html, js)


@frame
def f43():
    n, p = 43, "f43"
    m, mj = mascot(p, n, 820, 380, 260)
    html = m + f'<div class="h" id="{p}-a" style="left:0;right:0;top:130px;text-align:center;font-size:80px"><span class="r">Not</span> never spending</div><div class="h" id="{p}-b" style="left:0;right:0;top:240px;text-align:center;font-size:100px">Spending <span>on purpose</span></div>'
    js = mj + [rise(f"#{p}-a", cue(n, "never")), rise(f"#{p}-b", cue(n, "purpose"))]
    W(n, html, js)


@frame
def f44():
    n, p = 44, "f44"
    m, mj = mascot(p, n, 1560, 60, 200)
    html = (m + f'<div class="h" id="{p}-logo" style="left:0;right:0;top:280px;text-align:center;font-size:120px">Money <span>Unlocked</span></div>'
            + f'<div id="{p}-row" style="position:absolute;left:0;right:0;top:470px;display:flex;justify-content:center;gap:26px"><div class="chip white" style="position:relative;font-size:34px">Unlock more ✓</div><div class="chip dark" id="{p}-sub" style="position:relative;font-size:38px">Subscribe</div></div>'
            + f'<div class="chip white" id="{p}-q" style="left:640px;top:640px;font-size:32px">Hardest thing to give up? 💬</div>'.replace(" 💬", ""))
    js = mj + [rise(f"#{p}-logo", .1), pop(f"#{p}-q", cue(n, "hardest")), rise(f"#{p}-row", cue(n, "subscribe")),
               f'tl.to("#{p}-sub",{{scale:.92,duration:.1}},{cue(n, "subscribe")+.7:.2f});tl.to("#{p}-sub",{{scale:1,background:"{C["primary"]}",duration:.25}},{cue(n, "subscribe")+.8:.2f});']
    W(n, html, js)


if __name__ == "__main__":
    for k in sorted(F):
        F[k]()
    print("ok", len(F))
