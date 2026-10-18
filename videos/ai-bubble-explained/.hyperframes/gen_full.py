"""Full-episode frames 8–38 (frames 1–7 come from gen_frames.py, rescaled to the new voice)."""
import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_frames as G
from gen_frames import C, robot, blink, bob, write, DUR

META = json.load(open(os.path.join(G.ROOT, "audio_meta.json")))
WORDS = {v["frame"]: v["words"] for v in META["voices"]}


def norm(w):
    return re.sub(r"[^a-z0-9$%]", "", w.lower())


def cue(n, word, nth=1, frac=None):
    """Start time of the nth occurrence of `word` in frame n's narration."""
    k = 0
    for w in WORDS.get(n, []):
        if norm(w["text"]).startswith(norm(word)):
            k += 1
            if k == nth:
                return round(w["start"], 2)
    return round((frac if frac is not None else 0.5) * DUR[n], 2)


# ---------- pixel icons ----------
PAL = {"k": C["text"], "c": C["cyan"], "v": C["violet"], "w": "#FFFFFF", "g": C["green"], "r": C["red"],
       "y": "#FBBF24", "o": "#D97706", "b": "#A16207", "p": "#FF5C8A", "s": "#C9A27A", "l": "#C7D2FE", "e": "#9AA0B8"}
ICONS = {
    "server": ["vvvvvvvv", "vwwwwcgv", "vvvvvvvv", "vwwwwcgv", "vvvvvvvv", "vwwwwcgv", "vvvvvvvv"],
    "chip": [".c.c.c.c.", "ckkkkkkkc", ".kvvvvvk.", "ckvwwwvkc", ".kvwwwvk.", "ckvvvvvkc", ".kkkkkkk.", "c.c.c.c.c"],
    "coin": ["..yyyy..", ".yyooyy.", "yyoyyyyy", "yyyooyyy", "yyyyyoyy", "yyooyyyy", ".yyyyyy.", "..yyyy.."],
    "bolt": ["....yy", "...yy.", "..yy..", ".yyyyy", "...yy.", "..yy..", ".yy...", "yy...."],
    "shovel": [".....ss", "....ss.", "...ss..", "..ss...", ".ee....", "eeee...", "eee....", ".e....."],
    "box": ["oooooooo", "obbwwbbo", "obbwwbbo", "obbbbbbo", "obbbbbbo", "oooooooo"],
    "chat": ["vvvvvvv", "vwwwwwv", "vwkwkwv", "vwwwwwv", "vvvvvvv", ".vv....", "v......"],
    "code": ["kkkkkkkk", "kwwwwwwk", "kwcwwgwk", "kcwwwwgk", "kwcwwgwk", "kwwwwwwk", "kkkkkkkk"],
    "head": ["..kkkk..", ".k....k.", "k......k", "kc....ck", "kc....ck", ".......k", "....kkk."],
    "brush": ["......pp", ".....pp.", "....pp..", "...ss...", "..ss....", ".vv.....", "vvv.....", "vv......"],
    "egg": [".ww.", "wwww", "wwww", ".ww."],
    "crown": ["y..y..y", "yy.y.yy", "yyyyyyy", "yrryrry", "yyyyyyy"],
    "monitor": ["kkkkkkkkk", "kccccccck", "kcwwwwwck", "kcwwwwwck", "kccccccck", "kkkkkkkkk", "....k....", "..kkkkk.."],
    "plug": [".k..k.", ".k..k.", "kkkkkk", "kwwwwk", ".kkkk.", "..kk..", "..kk..", "..kk.."],
    "dog": ["kk...kk", "kwwwwwk", ".wkwkw.", ".wwwww.", ".wwkww.", "..www..", "..ppp.."],
    "piggy": [".pppppp.", "pppppppp", "ppkpppppp"[:8], "pppppppp", ".pppppp.", ".p.pp.p."],
    "warn": ["...yy...", "..yyyy..", "..ykky..", ".yykkyy.", ".yykkyy.", "yyyyyyyy", "yyykkyyy", "yyyyyyyy"],
    "check": ["......g", ".....gg", "g...gg.", "gg.gg..", ".ggg...", "..g...."],
    "cross": ["r....r", ".r..r.", "..rr..", "..rr..", ".r..r.", "r....r"],
    "house": [".....v....", "....vvv...", "...vvvvv..", "..vvvvvvv.", ".wwwwwwww.", ".wccwwkkw.", ".wccwwkkw."],
}


def icon(name, size=120, cls=""):
    m = ICONS[name]
    h, w = len(m), max(len(r) for r in m)
    rects = "".join(f'<rect x="{x}" y="{y}" width="1.02" height="1.02" fill="{PAL[ch]}"/>'
                    for y, row in enumerate(m) for x, ch in enumerate(row) if ch in PAL)
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" width="{size}" height="{size*h/w:.0f}" '
            f'shape-rendering="crispEdges">{rects}</svg>')


# ---------- motion helpers ----------
def pop(sel, t, s0=.5):
    return f'tl.fromTo("{sel}",{{scale:{s0},opacity:0}},{{scale:1,opacity:1,duration:.45,ease:"back.out(2)"}},{t:.2f});'


def rise(sel, t, dy=40):
    return f'tl.fromTo("{sel}",{{y:{dy},opacity:0}},{{y:0,opacity:1,duration:.5,ease:"power3.out"}},{t:.2f});'


def slide(sel, t, dx=-60):
    return f'tl.fromTo("{sel}",{{x:{dx},opacity:0}},{{x:0,opacity:1,duration:.5,ease:"power3.out"}},{t:.2f});'


def draw(sel, t, dur=1.0, length=2000, ease="power2.inOut"):
    return f'tl.fromTo("{sel}",{{strokeDasharray:{length},strokeDashoffset:{length}}},{{strokeDashoffset:0,duration:{dur},ease:"{ease}"}},{t:.2f});'


def shake(sel, t):
    return "".join(f'tl.to("{sel}",{{x:{dx},duration:.05}},{t + i*0.05:.2f});' for i, dx in enumerate([10, -10, 7, -7, 0]))


GEO = {}


def SO(p, gid="g"):
    cx, cy = GEO[(p, gid)]
    return f"{cx} {cy}"

# ---------- shared CSS ----------
def css_common(p):
    return f"""
.{p}-eyebrow{{left:110px;top:100px;background:{C['primary']};color:#fff;}}
.{p}-h{{position:absolute;font-weight:900;letter-spacing:-.02em;line-height:1;}}
.{p}-h span{{color:{C['primary']};}} .{p}-h .{p}-red{{color:{C['red']};}} .{p}-h .{p}-grn{{color:{C['green']};}}
.{p}-lbl{{font-weight:800;font-size:30px;letter-spacing:.03em;}}
.{p}-sub{{font-weight:600;font-size:24px;color:{C['muted']};}}
.{p}-tile{{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:20px;text-align:center;}}
.{p}-chipx{{position:absolute;padding:12px 24px;border-radius:999px;font-weight:800;font-size:28px;color:#fff;background:{C['primary']};}}
"""


def bot_html(p, x, y, size=220, extra=""):
    return f'<div class="{p}-robotwrap" id="{p}-bot" style="left:{x}px;top:{y}px;{extra}">{robot(p, size)}</div>'


def bot_in(p, n, t=0.2):
    return (f'tl.fromTo("#{p}-bot",{{y:80,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"back.out(1.6)"}},{t});'
            + blink(p, f"#{p}-bot", min(2.2, DUR[n] * .4)) + bob(p, f"#{p}-bot", t + .6, DUR[n], amp=8))


def frame(n, slug, css, html, js):
    p = f"fd{n:02d}"
    write(f"{n:02d}-{slug}", p, DUR[n], css_common(p) + css, html, "\n".join(js))


def tiles(p, items, x0, y0, w, h, gap, cols):
    out = []
    for i, (ic, label, sub) in enumerate(items):
        x, y = x0 + (i % cols) * (w + gap), y0 + (i // cols) * (h + gap)
        out.append(f'<div class="{p}-card {p}-tile" id="{p}-t{i}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
                   f'{icon(ic, 110) if ic else ""}<div class="{p}-lbl">{label}</div>'
                   f'{f"<div class={chr(34)}{p}-sub{chr(34)}>{sub}</div>" if sub else ""}</div>')
    return "".join(out)


def gauge(p, gid, x, y, size, label):
    r = size / 2 - 20
    cx, cy = size / 2, size / 2 + 20
    GEO[(p, gid)] = (cx, cy)
    return f'''<div class="{p}-card" id="{p}-{gid}" style="left:{x}px;top:{y}px;width:{size}px;height:{size*0.78:.0f}px">
<svg width="{size}" height="{size*0.62:.0f}" viewBox="0 0 {size} {size*0.62:.0f}">
<path d="M {cx-r} {cy} A {r} {r} 0 0 1 {cx+r} {cy}" stroke="#E5E7F5" stroke-width="26" fill="none"/>
<path d="M {cx-r} {cy} A {r} {r} 0 0 1 {cx} {cy-r}" stroke="{C['green']}" stroke-width="26" fill="none"/>
<path d="M {cx} {cy-r} A {r} {r} 0 0 1 {cx+r*0.7:.0f} {cy-r*0.71:.0f}" stroke="#FBBF24" stroke-width="26" fill="none"/>
<path d="M {cx+r*0.7:.0f} {cy-r*0.71:.0f} A {r} {r} 0 0 1 {cx+r} {cy}" stroke="{C['red']}" stroke-width="26" fill="none"/>
<g id="{p}-{gid}-n"><rect x="{cx-4}" y="{cy-r+18}" width="8" height="{r-18}" rx="4" fill="{C['text']}"/></g>
<circle cx="{cx}" cy="{cy}" r="14" fill="{C['text']}"/></svg>
<div class="{p}-lbl" style="text-align:center;margin-top:6px">{label}</div></div>'''


def needle(p, gid, t, deg, dur=.8):
    cx, cy = GEO[(p, gid)]
    return f'tl.fromTo("#{p}-{gid}-n",{{rotation:-80,svgOrigin:"{cx} {cy}"}},{{rotation:{deg},svgOrigin:"{cx} {cy}",duration:{dur},ease:"elastic.out(1,.5)"}},{t:.2f});'


def linechart(p, x, y, w, h, pts, color, pid, labels_x=None):
    sx = lambda v: 80 + v * (w - 140)
    sy = lambda v: h - 70 - v * (h - 150)
    d = "M" + " L".join(f"{sx(a):.0f} {sy(b):.0f}" for a, b in pts)
    xl = "".join(f'<text x="{sx(a):.0f}" y="{h-30}" text-anchor="middle" font-family="Inter" font-weight="700" font-size="24" fill="{C["muted"]}">{t}</text>'
                 for a, t in (labels_x or []))
    return (f'<line x1="80" y1="{h-70}" x2="{w-40}" y2="{h-70}" stroke="{C["light"]}" stroke-width="3"/>{xl}'
            f'<path id="{p}-{pid}" d="{d}" fill="none" stroke="{color}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'), sx, sy


# =====================================================================
def f8():
    n, p = 8, "fd08"
    labels = ["Spending", "Revenue gap", "Circular deals", "Hype"]
    chips = "".join(f'<div class="{p}-card {p}-reason" id="{p}-r{i}" style="left:{560 + (i%2)*600}px;top:{190 + (i//2)*300}px"><div class="{p}-num">{i+1}</div><div class="{p}-lbl">{l}</div></div>' for i, l in enumerate(labels))
    css = f"""
.{p}-reason{{width:540px;height:240px;display:flex;align-items:center;gap:30px;padding:0 40px;opacity:.35;}}
.{p}-num{{width:110px;height:110px;border-radius:28px;background:rgba(124,92,255,.12);color:{C['primary']};font-weight:900;font-size:64px;display:flex;align-items:center;justify-content:center;}}
.{p}-reason .{p}-lbl{{font-size:44px;}}
"""
    html = f'<div class="{p}-pill {p}-eyebrow" id="{p}-eb">Why it looks like a bubble</div>{chips}{bot_html(p, 150, 480, 240)}'
    js = [rise(f"#{p}-eb", .1), bot_in(p, n)]
    for i in range(4):
        js.append(f'tl.fromTo("#{p}-r{i}",{{y:30,opacity:0}},{{y:0,opacity:.35,duration:.4,ease:"power3.out"}},{0.4+i*.15:.2f});')
    t = cue(n, "spending")
    js.append(f'tl.to("#{p}-r0",{{opacity:1,scale:1.06,duration:.35,ease:"back.out(2)"}},{t:.2f});')
    js.append(f'tl.to("#{p}-r0 .{p}-num",{{background:"{C["primary"]}",color:"#fff",duration:.3}},{t:.2f});')
    frame(n, "four-reasons", css, html, js)


def f9():
    n, p = 9, "fd09"
    racks = "".join(f'<div class="{p}-rack" id="{p}-k{i}" style="left:{600 + (i%6)*190}px;top:{420 + (i//6)*210}px">{icon("server", 150)}</div>' for i in range(12))
    css = f"""
.{p}-rack{{position:absolute;filter:drop-shadow(0 10px 16px rgba(124,92,255,.25));}}
.{p}-money{{position:absolute;left:600px;top:150px;width:1150px;height:200px;display:flex;align-items:center;gap:40px;padding:0 40px;}}
.{p}-coins{{display:flex;gap:10px;}}
.{p}-big{{font-weight:900;font-size:86px;color:{C['primary']};margin-left:auto;}}
.{p}-est{{position:absolute;right:46px;bottom:18px;font-weight:700;font-size:20px;color:{C['muted']};letter-spacing:.1em;}}
.{p}-icons{{position:absolute;left:110px;top:260px;display:flex;flex-direction:column;gap:40px;}}
.{p}-ic{{display:flex;align-items:center;gap:22px;}}
"""
    coins = "".join(f'<div id="{p}-c{i}">{icon("coin", 70)}</div>' for i in range(6))
    html = f'''<div class="{p}-card {p}-money" id="{p}-money"><div class="{p}-coins">{coins}</div><div class="{p}-big" id="{p}-big">$1T+</div><div class="{p}-est">ANALYST ESTIMATE</div></div>
<div class="{p}-icons"><div class="{p}-ic" id="{p}-i0">{icon("server", 90)}<div class="{p}-lbl">Data centers</div></div>
<div class="{p}-ic" id="{p}-i1">{icon("chip", 90)}<div class="{p}-lbl">Chips</div></div>
<div class="{p}-ic" id="{p}-i2">{icon("bolt", 70)}<div class="{p}-lbl">Electricity</div></div></div>{racks}'''
    js = [slide(f"#{p}-i0", cue(n, "data")), slide(f"#{p}-i1", cue(n, "chips")), slide(f"#{p}-i2", cue(n, "electricity"))]
    for i in range(12):
        js.append(pop(f"#{p}-k{i}", cue(n, "building") + i * .18))
    js.append(rise(f"#{p}-money", cue(n, "raising")))
    for i in range(6):
        js.append(f'tl.fromTo("#{p}-c{i}",{{y:-80,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"bounce.out"}},{cue(n, "raising") + .3 + i*.15:.2f});')
    t = cue(n, "trillion")
    js.append(f'tl.fromTo("#{p}-big",{{scale:.3,opacity:0}},{{scale:1,opacity:1,duration:.5,ease:"back.out(2.5)"}},{t:.2f});')
    frame(n, "spending", css, html, js)


def f10():
    n, p = 10, "fd10"
    css = f"""
.{p}-chart{{left:560px;top:130px;width:1200px;height:720px;}}
.{p}-bar{{position:absolute;bottom:120px;width:300px;border-radius:24px 24px 8px 8px;transform-origin:50% 100%;}}
.{p}-out{{left:200px;height:520px;background:linear-gradient(180deg,#FF8A8A,{C['red']});}}
.{p}-in{{left:700px;height:520px;background:linear-gradient(180deg,#5EEAD4,{C['green']});}}
.{p}-bl{{position:absolute;bottom:50px;width:300px;text-align:center;}}
.{p}-gap{{position:absolute;left:1030px;top:110px;width:120px;height:440px;border:5px dashed {C['primary']};border-left:none;border-radius:0 30px 30px 0;}}
.{p}-gapl{{position:absolute;left:1000px;top:300px;}}
"""
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eb">Reason 2 · Revenue gap</div>
<div class="{p}-card {p}-chart" id="{p}-chart"><div class="{p}-bar {p}-out" id="{p}-out"></div><div class="{p}-bar {p}-in" id="{p}-in"></div>
<div class="{p}-bl {p}-lbl" style="left:200px">MONEY OUT</div><div class="{p}-bl {p}-lbl" style="left:700px">MONEY IN</div>
<div class="{p}-gap" id="{p}-gap"></div><div class="{p}-chipx {p}-gapl" id="{p}-gapl">GAP</div></div>{bot_html(p, 160, 500, 230)}'''
    js = [rise(f"#{p}-eb", .1), rise(f"#{p}-chart", .2), bot_in(p, n, .4),
          f'tl.fromTo("#{p}-in",{{scaleY:0}},{{scaleY:.12,duration:.8,ease:"power2.out"}},{cue(n, "growing"):.2f});',
          f'tl.fromTo("#{p}-out",{{scaleY:0}},{{scaleY:1,duration:1.0,ease:"power2.out"}},{cue(n, "going", 1):.2f});',
          pop(f"#{p}-gap", cue(n, "betting")), pop(f"#{p}-gapl", cue(n, "gap")),
          f'tl.to("#{p}-in",{{scaleY:.3,duration:1.2,ease:"power1.inOut"}},{cue(n, "close"):.2f});',
          shake(f"#{p}-bot", cue(n, "nervous"))]
    frame(n, "revenue-gap", css, html, js)


def loop3(p, labels, colors):
    pos = [(960, 230), (1330, 690), (590, 690)]
    nodes = "".join(f'<div class="{p}-card {p}-node" id="{p}-n{i}" style="left:{x}px;top:{y}px;color:{colors[i]}">{l}</div>' for i, ((x, y), l) in enumerate(zip(pos, labels)))
    svg = f'''<svg style="position:absolute;left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
<defs><marker id="{p}-ah" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{C['primary']}"/></marker></defs>
<path id="{p}-e0" d="M1120 300 Q 1330 420 1330 600" stroke="{C['primary']}" stroke-width="10" fill="none" marker-end="url(#{p}-ah)"/>
<path id="{p}-e1" d="M1150 760 Q 960 850 780 760" stroke="{C['primary']}" stroke-width="10" fill="none" marker-end="url(#{p}-ah)"/>
<path id="{p}-e2" d="M590 600 Q 590 420 800 300" stroke="{C['primary']}" stroke-width="10" fill="none" marker-end="url(#{p}-ah)"/>
</svg>'''
    css = f".{p}-node{{position:absolute;width:380px;height:150px;margin-left:-190px;margin-top:-75px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:38px;}}"
    return svg + nodes, css, [(1250, 380), (1180, 720), (960, 800), (740, 720), (660, 380)]


def f11():
    n, p = 11, "fd11"
    h, c, pts = loop3(p, ["CHIP & CLOUD CO.", "AI STARTUP", "BUYS CHIPS & CLOUD"], [C["text"]] * 3)
    css = c + f".{p}-coin{{position:absolute;left:0;top:0;}}"
    html = f'<div class="{p}-pill {p}-eyebrow" id="{p}-eb">Reason 3 · Circular deals</div>{h}<div class="{p}-coin" id="{p}-coin">{icon("coin", 56)}</div>'
    js = [rise(f"#{p}-eb", .1), pop(f"#{p}-n0", cue(n, "chip")), pop(f"#{p}-n1", cue(n, "startups")),
          f'tl.fromTo("#{p}-e0",{{opacity:0,strokeDasharray:700,strokeDashoffset:700}},{{opacity:1,strokeDashoffset:0,duration:.5}},{cue(n, "investing"):.2f});',
          pop(f"#{p}-n2", cue(n, "buying")),
          f'tl.fromTo("#{p}-e1",{{opacity:0,strokeDasharray:700,strokeDashoffset:700}},{{opacity:1,strokeDashoffset:0,duration:.5}},{cue(n, "spend"):.2f});',
          f'tl.fromTo("#{p}-e2",{{opacity:0,strokeDasharray:700,strokeDashoffset:700}},{{opacity:1,strokeDashoffset:0,duration:.5}},{cue(n, "same"):.2f});']
    t = cue(n, "investing") + .3
    js.append(f'tl.fromTo("#{p}-coin",{{opacity:0,x:{pts[0][0]-28},y:{pts[0][1]-28}}},{{opacity:1,duration:.2}},{t:.2f});')
    k = 0
    while t < DUR[n] - .5:
        x, y = pts[(k + 1) % len(pts)]
        js.append(f'tl.to("#{p}-coin",{{x:{x-28},y:{y-28},duration:.6,ease:"none"}},{t:.2f});')
        t += .6; k += 1
    js.append(f'tl.to(["#{p}-n0","#{p}-n1","#{p}-n2"],{{scale:1.06,duration:.3}},{cue(n, "stronger"):.2f});')
    frame(n, "circular-deals", css, html, js)


def f12():
    n, p = 12, "fd12"
    names = ["SmartCo", "DataBox", "PixelHQ", "CloudKit", "Bloop", "Notely"]
    cards = "".join(f'<div class="{p}-card {p}-co" id="{p}-co{i}" style="left:{560 + (i%3)*400}px;top:{170 + (i//3)*330}px"><div class="{p}-lbl" id="{p}-nm{i}">{nm}<span class="{p}-ai" id="{p}-ai{i}"> AI</span></div><div class="{p}-val"><div class="{p}-valfill" id="{p}-v{i}"></div></div></div>' for i, nm in enumerate(names))
    css = f"""
.{p}-co{{width:360px;height:280px;padding:36px;display:flex;flex-direction:column;justify-content:space-between;}}
.{p}-co .{p}-lbl{{font-size:40px;}}
.{p}-ai{{color:{C['primary']};}}
.{p}-val{{height:22px;border-radius:999px;background:rgba(124,92,255,.12);overflow:hidden;}}
.{p}-valfill{{height:100%;width:100%;background:{C['primary']};transform-origin:0 50%;}}
.{p}-magic{{position:absolute;left:110px;top:300px;font-weight:900;font-size:92px;line-height:1;}}
.{p}-magic span{{color:{C['primary']};}}
"""
    html = f'<div class="{p}-pill {p}-eyebrow" id="{p}-eb">Reason 4 · Hype</div><div class="{p}-magic" id="{p}-mg">The<br><span>magic</span><br>word</div>{cards}'
    js = [rise(f"#{p}-eb", .1)]
    t0 = cue(n, "startups")
    for i in range(6):
        js.append(pop(f"#{p}-co{i}", t0 + i * .12))
        js.append(f'gsap.set("#{p}-ai{i}",{{opacity:0}});')
        js.append(f'tl.fromTo("#{p}-v{i}",{{scaleX:0}},{{scaleX:.25,duration:.4}},{t0 + .3 + i*.12:.2f});')
    t1 = cue(n, "pitch")
    for i in range(6):
        js.append(f'tl.to("#{p}-ai{i}",{{opacity:1,duration:.2}},{t1 + i*.15:.2f});')
        js.append(f'tl.to("#{p}-v{i}",{{scaleX:1,duration:.5,ease:"back.out(1.5)"}},{cue(n, "jump") + i*.08:.2f});')
    js.append(f'tl.to(".{p}-co",{{y:-12,duration:.3,stagger:.05}},{cue(n, "earnings"):.2f});tl.to(".{p}-co",{{y:0,duration:.3,stagger:.05}},{cue(n, "again"):.2f});')
    js.append(slide(f"#{p}-mg", cue(n, "magic")))
    frame(n, "hype", css, html, js)


def f13():
    n, p = 13, "fd13"
    css = f"""
.{p}-beam{{position:absolute;left:560px;top:520px;width:1140px;height:24px;border-radius:12px;background:{C['text']};transform-origin:50% 50%;}}
.{p}-tri{{position:absolute;left:1090px;top:544px;width:0;height:0;border-left:40px solid transparent;border-right:40px solid transparent;border-bottom:80px solid {C['text']};}}
.{p}-left{{position:absolute;left:600px;top:290px;width:340px;height:230px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:90px;color:{C['primary']};}}
.{p}-right{{position:absolute;left:1320px;top:330px;width:300px;height:190px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;}}
.{p}-perfect{{left:1150px;top:720px;background:{C['red']};}}
"""
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eb">What you're really buying</div>
<div class="{p}-h" id="{p}-h" style="left:110px;top:220px;font-size:80px">A slice of<br><span>future</span><br>profits</div>
<div id="{p}-scale"><div class="{p}-beam" id="{p}-beam"></div><div class="{p}-tri"></div>
<div class="{p}-card {p}-left" id="{p}-L">$100</div>
<div class="{p}-card {p}-right" id="{p}-R">{icon("coin", 80)}<div class="{p}-lbl">$1 / year</div></div></div>
<div class="{p}-chipx {p}-perfect" id="{p}-pf">PRICED FOR PERFECT</div>'''
    js = [rise(f"#{p}-eb", .1), slide(f"#{p}-h", cue(n, "slice")), rise(f"#{p}-scale", cue(n, "slice") + .4),
          pop(f"#{p}-L", cue(n, "hundred")), pop(f"#{p}-R", cue(n, "earns")),
          f'tl.to(["#{p}-beam"],{{rotation:-8,duration:.8,ease:"elastic.out(1,.5)"}},{cue(n, "betting"):.2f});',
          f'tl.to("#{p}-L",{{y:40,duration:.8,ease:"elastic.out(1,.5)"}},{cue(n, "betting"):.2f});',
          f'tl.to("#{p}-R",{{y:-60,duration:.8,ease:"elastic.out(1,.5)"}},{cue(n, "betting"):.2f});',
          f'tl.to("#{p}-R",{{y:-20,duration:.6}},{cue(n, "growth"):.2f});',
          pop(f"#{p}-pf", cue(n, "perfect"))]
    frame(n, "valuation", css, html, js)


def f14():
    n, p = 14, "fd14"
    css = f"""
.{p}-flip{{left:560px;top:250px;width:800px;height:420px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:180px;color:{C['primary']};}}
"""
    html = f'<div class="{p}-card {p}-flip" id="{p}-f">BUT…</div>{bot_html(p, 1480, 420, 260)}'
    js = [f'tl.fromTo("#{p}-f",{{rotationY:-90,opacity:0}},{{rotationY:0,opacity:1,duration:.7,ease:"back.out(1.6)"}},{cue(n, "other"):.2f});',
          bot_in(p, n, .1), f'tl.to("#{p}-f",{{scale:1.08,duration:.4,ease:"back.out(3)"}},{cue(n, "strong"):.2f});']
    frame(n, "other-side", css, html, js)


def f15():
    n, p = 15, "fd15"
    items = [("chat", "Chatbots", "100s of millions"), ("code", "Coding", "programmers"), ("head", "Support", "companies"), ("brush", "Design", "& research")]
    css = f".{p}-tile .{p}-sub{{font-size:22px;}}"
    html = f'<div class="{p}-pill {p}-eyebrow" id="{p}-eb">1 · AI is actually used</div>{tiles(p, items, 140, 260, 380, 420, 40, 4)}'
    js = [rise(f"#{p}-eb", .1), pop(f"#{p}-t0", cue(n, "hundreds")), pop(f"#{p}-t1", cue(n, "programmers")),
          pop(f"#{p}-t2", cue(n, "customer")), pop(f"#{p}-t3", cue(n, "design")),
          f'tl.to(".{p}-tile",{{y:-16,duration:.3,stagger:.06}},{cue(n, "purpose"):.2f});']
    frame(n, "ai-used", css, html, js)


def f16():
    n, p = 16, "fd16"
    css = f"""
.{p}-col{{position:absolute;top:220px;width:740px;height:600px;padding:40px;display:flex;flex-direction:column;align-items:center;gap:26px;}}
.{p}-yr{{font-weight:900;font-size:70px;}}
.{p}-stack{{display:flex;align-items:flex-end;gap:14px;height:300px;}}
.{p}-tower{{display:flex;flex-direction:column-reverse;}}
"""
    tower = lambda pref, k: "".join(f'<div class="{p}-tc {pref}" style="margin-top:-30px">{icon("coin", 70)}</div>' for _ in range(k))
    towers = "".join(f'<div class="{p}-tower">{tower(p+"-coinT", h)}</div>' for h in (4, 6, 8, 5))
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eb">2 · Who's paying</div>
<div class="{p}-card {p}-col" id="{p}-a" style="left:140px"><div class="{p}-yr">2000</div><div class="{p}-stack" id="{p}-sa">{icon("cross", 160)}</div><div class="{p}-lbl">No profits · borrowed money</div></div>
<div class="{p}-card {p}-col" id="{p}-b" style="left:1040px"><div class="{p}-yr" style="color:{C['primary']}">Today</div><div class="{p}-stack">{towers}</div><div class="{p}-lbl">Huge profits from search, cloud, software</div></div>'''
    js = [rise(f"#{p}-eb", .1), rise(f"#{p}-a", cue(n, "dot")), pop(f"#{p}-sa svg", cue(n, "profits", 2)),
          rise(f"#{p}-b", cue(n, "today")),
          f'tl.fromTo(".{p}-coinT",{{y:-60,opacity:0}},{{y:0,opacity:1,duration:.3,stagger:.06,ease:"bounce.out"}},{cue(n, "giants"):.2f});']
    frame(n, "profitable-giants", css, html, js)


def f17():
    n, p = 17, "fd17"
    W, H = 1200, 680
    up, sx, sy = linechart(p, 0, 0, W, H, [(0, .1), (.25, .25), (.5, .45), (.75, .7), (1, .95)], C["primary"], "cap", [(0, "THEN"), (1, "NOW")])
    dn_d = "M" + " L".join(f"{sx(a):.0f} {sy(b):.0f}" for a, b in [(0, .9), (.25, .65), (.5, .4), (.75, .22), (1, .1)])
    css = f".{p}-chart{{left:560px;top:150px;width:{W}px;height:{H}px;}} .{p}-k1{{left:610px;top:180px;}} .{p}-k2{{left:1360px;top:720px;background:{C['green']};}}"
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eb">3 · Better & cheaper</div>
<div class="{p}-h" style="left:110px;top:260px;font-size:84px" id="{p}-h">More<br>for<br><span>less</span></div>
<div class="{p}-card {p}-chart" id="{p}-c"><svg width="{W}" height="{H}">{up}<path id="{p}-cost" d="{dn_d}" fill="none" stroke="{C['green']}" stroke-width="10" stroke-linecap="round" stroke-dasharray="2 20"/></svg></div>
<div class="{p}-chipx {p}-k1" id="{p}-k1">WHAT AI CAN DO</div><div class="{p}-chipx {p}-k2" id="{p}-k2">COST</div>'''
    js = [rise(f"#{p}-eb", .1), rise(f"#{p}-c", .3), draw(f"#{p}-cap", cue(n, "better"), 1.4), pop(f"#{p}-k1", cue(n, "more")),
          f'tl.fromTo("#{p}-cost",{{opacity:0}},{{opacity:1,duration:.8}},{cue(n, "cheaper"):.2f});', pop(f"#{p}-k2", cue(n, "less")),
          slide(f"#{p}-h", cue(n, "opens"))]
    frame(n, "better-cheaper", css, html, js)


def f18():
    n, p = 18, "fd18"
    css = f"""
.{p}-row{{position:absolute;left:0;right:0;display:flex;justify-content:center;gap:40px;}}
.{p}-claim{{position:relative;padding:40px 60px;font-weight:900;font-size:64px;display:flex;align-items:center;gap:28px;}}
.{p}-both{{position:absolute;left:0;right:0;top:640px;text-align:center;font-weight:900;font-size:110px;color:{C['primary']};}}
"""
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eb">The key idea</div>
<div class="{p}-row" style="top:260px"><div class="{p}-card {p}-claim" id="{p}-a">{icon("check", 70)}World-changing tech</div></div>
<div class="{p}-row" style="top:440px"><div class="{p}-card {p}-claim" id="{p}-b">{icon("check", 70)}Overpriced stocks</div></div>
<div class="{p}-both" id="{p}-both">Both can be true</div>'''
    js = [rise(f"#{p}-eb", .1), pop(f"#{p}-a", cue(n, "world")), pop(f"#{p}-b", cue(n, "overpriced")),
          f'tl.fromTo("#{p}-both",{{scale:.4,opacity:0}},{{scale:1,opacity:1,duration:.5,ease:"back.out(2)"}},{cue(n, "both"):.2f});']
    frame(n, "both-true", css, html, js)


def f19():
    n, p = 19, "fd19"
    css = f"""
.{p}-mine{{position:absolute;left:560px;top:200px;width:620px;height:520px;}}
.{p}-stand{{left:1260px;top:260px;width:460px;height:460px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;}}
.{p}-sw{{position:relative;width:200px;height:200px;}}
.{p}-sw > div{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;}}
"""
    mine = f'''<svg class="{p}-mine" id="{p}-mine" viewBox="0 0 620 520"><path d="M0 520 L250 80 L330 200 L420 120 L620 520 Z" fill="#E9D5FF"/><path d="M200 520 L250 360 L300 520 Z" fill="#7C5CFF" opacity=".25"/>
<circle id="{p}-g1" cx="290" cy="300" r="22" fill="#FBBF24"/><circle id="{p}-g2" cx="380" cy="380" r="16" fill="#FBBF24"/><circle id="{p}-g3" cx="220" cy="420" r="18" fill="#FBBF24"/></svg>'''
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eb">The shovel sellers</div>{mine}
<div class="{p}-card {p}-stand" id="{p}-st"><div class="{p}-sw"><div id="{p}-sh">{icon("shovel", 170)}</div><div id="{p}-ch">{icon("chip", 170)}</div></div><div class="{p}-lbl" id="{p}-sl">SHOVELS</div></div>
{bot_html(p, 130, 470, 230)}'''
    js = [rise(f"#{p}-eb", .1), rise(f"#{p}-mine", .3), bot_in(p, n, .4), pop(f"#{p}-st", cue(n, "shovels")),
          f'gsap.set("#{p}-ch",{{opacity:0}});',
          f'tl.fromTo(["#{p}-g1","#{p}-g2","#{p}-g3"],{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:.4,stagger:.15,ease:"back.out(3)"}},{cue(n, "gold"):.2f});',
          f'tl.to("#{p}-sh",{{opacity:0,rotation:-30,duration:.3}},{cue(n, "chips"):.2f});tl.fromTo("#{p}-ch",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2.5)"}},{cue(n, "chips")+.2:.2f});',
          f'tl.to("#{p}-sl",{{opacity:0,duration:.15}},{cue(n, "chips"):.2f});',
          f'tl.to("#{p}-st",{{scale:1.08,duration:.4,ease:"back.out(2)"}},{cue(n, "explode"):.2f});']
    js = [j for j in js if "tl.call" not in j]
    html = html.replace(f'<div class="{p}-lbl" id="{p}-sl">SHOVELS</div>', f'<div class="{p}-lbl" id="{p}-sl">SHOVELS</div><div class="{p}-lbl" id="{p}-sl2" style="color:{C["primary"]};margin-top:-58px">AI CHIPS</div>')
    js.append(f'gsap.set("#{p}-sl2",{{opacity:0}});tl.to("#{p}-sl2",{{opacity:1,duration:.2}},{cue(n, "chips")+.2:.2f});')
    frame(n, "shovels", css, html, js)


def chain(p, labels, y=420, red_from=99):
    out = []
    for i, l in enumerate(labels):
        col = C["red"] if i >= red_from else C["text"]
        out.append(f'<div class="{p}-card {p}-link" id="{p}-l{i}" style="left:{140 + i*600}px;top:{y}px;color:{col}">{l}</div>')
        if i < len(labels) - 1:
            out.append(f'<div class="{p}-arr" id="{p}-a{i}" style="left:{560 + i*600}px;top:{y+60}px">→</div>')
    return "".join(out), f""".{p}-link{{position:absolute;width:420px;height:200px;display:flex;align-items:center;justify-content:center;text-align:center;font-weight:900;font-size:44px;padding:20px;}}
.{p}-arr{{position:absolute;font-weight:900;font-size:80px;color:{C['primary']};width:180px;text-align:center;}}"""


def f20():
    n, p = 20, "fd20"
    h, c = chain(p, ["AI spending ↓", "Chip sales ↓", "AI stocks ↓"], 380, 0)
    html = f'<div class="{p}-pill {p}-eyebrow" id="{p}-eb">Most sensitive to a slowdown</div>{h}{bot_html(p, 1500, 660, 200)}'
    js = [rise(f"#{p}-eb", .1), pop(f"#{p}-l0", cue(n, "spend")), pop(f"#{p}-a0", cue(n, "chip")), pop(f"#{p}-l1", cue(n, "feel")),
          pop(f"#{p}-a1", cue(n, "reason")), pop(f"#{p}-l2", cue(n, "stocks")), shake(f"#{p}-l2", cue(n, "sharply")), bot_in(p, n, .5)]
    frame(n, "sensitive", c, html, js)


def f21():
    n, p = 21, "fd21"
    css = f"""
.{p}-grid{{position:absolute;left:560px;top:200px;width:1200px;height:600px;}}
.{p}-meter{{left:1000px;top:700px;width:700px;height:60px;padding:0;overflow:hidden;border-radius:999px;}}
.{p}-mf{{position:absolute;left:8px;top:8px;bottom:8px;right:8px;border-radius:999px;background:linear-gradient(90deg,{C['green']},#FBBF24,{C['red']});transform-origin:0 50%;}}
.{p}-ml{{position:absolute;left:30px;top:15px;font-weight:900;font-size:24px;color:#fff;letter-spacing:.1em;}}
"""
    towers = "".join(f'<g transform="translate({120+i*300},120)"><path d="M60 0 L0 380 M60 0 L120 380 M20 250 L100 250 M35 150 L85 150" stroke="{C["muted"]}" stroke-width="8" fill="none"/></g>' for i in range(4))
    wires = f'<path id="{p}-w" d="M180 130 Q 330 220 480 130 Q 630 220 780 130 Q 930 220 1080 130" stroke="{C["primary"]}" stroke-width="6" fill="none"/>'
    bolts = "".join(f'<div id="{p}-bx{i}" style="position:absolute;left:{700+i*300}px;top:150px">{icon("bolt", 90)}</div>' for i in range(3))
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eb">And then there's power</div>
<svg class="{p}-grid" id="{p}-g" viewBox="0 0 1200 600">{towers}{wires}</svg>{bolts}
<div class="{p}-h" id="{p}-h" style="left:110px;top:300px;font-size:88px">The<br><span>grid</span><br>limit</div>
<div class="{p}-card {p}-meter" id="{p}-m"><div class="{p}-mf" id="{p}-mf"></div><div class="{p}-ml">GRID LOAD</div></div>'''
    js = [rise(f"#{p}-eb", .1), rise(f"#{p}-g", .2), draw(f"#{p}-w", cue(n, "electricity"), 1.2, 1400)]
    for i in range(3):
        js.append(pop(f"#{p}-bx{i}", cue(n, "enormous") + i * .2))
    js += [rise(f"#{p}-m", cue(n, "limit")), f'tl.fromTo("#{p}-mf",{{scaleX:.2}},{{scaleX:.97,duration:2,ease:"power2.in"}},{cue(n, "grid"):.2f});',
           slide(f"#{p}-h", cue(n, "grid"))]
    frame(n, "power", css, html, js)


def f22():
    n, p = 22, "fd22"
    nodes = [("BIG TECH", 960, 200), ("CHIPS", 1450, 400), ("CLOUD", 1300, 750), ("POWER", 620, 750), ("STARTUPS", 470, 400)]
    divs = "".join(f'<div class="{p}-card {p}-nd" id="{p}-n{i}" style="left:{x}px;top:{y}px">{t}</div>' for i, (t, x, y) in enumerate(nodes))
    lines = "".join(f'<line id="{p}-ln{k}" x1="{nodes[i][1]}" y1="{nodes[i][2]}" x2="{nodes[j][1]}" y2="{nodes[j][2]}" stroke="{C["primary"]}" stroke-width="5" opacity=".5"/>'
                    for k, (i, j) in enumerate([(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2), (0, 3), (1, 4)]))
    css = f".{p}-nd{{position:absolute;width:280px;height:110px;margin-left:-140px;margin-top:-55px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:34px;}}"
    html = f'<svg style="position:absolute;left:0;top:0" width="1920" height="1080">{lines}</svg>{divs}'
    js = []
    t = cue(n, "economy")
    for i in range(5):
        js.append(pop(f"#{p}-n{i}", t + i * .15))
    for k in range(8):
        js.append(f'tl.fromTo("#{p}-ln{k}",{{opacity:0}},{{opacity:.5,duration:.3}},{cue(n, "connected") + k*.08:.2f});')
    s = cue(n, "sneezes")
    js.append(shake(f"#{p}-n0", s))
    js.append(f'tl.to(["#{p}-n1","#{p}-n2","#{p}-n3","#{p}-n4"],{{color:"{C["red"]}",y:12,duration:.3,stagger:.12}},{cue(n, "cold"):.2f});')
    frame(n, "connected", css, html, js)


def f23():
    n, p = 23, "fd23"
    css = f".{p}-yr{{position:absolute;left:1180px;top:260px;font-weight:900;font-size:220px;color:{C['primary']};opacity:.9;}} .{p}-mon{{position:absolute;left:600px;top:200px;}} .{p}-right{{left:1180px;top:560px;background:{C['green']};}}"
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eb">We've been here before</div><div class="{p}-mon" id="{p}-mon">{icon("monitor", 460)}</div>
<div class="{p}-yr" id="{p}-yr">1999</div><div class="{p}-chipx {p}-right" id="{p}-ok">AND IT WAS ✓</div>'''
    js = [rise(f"#{p}-eb", .1), pop(f"#{p}-mon", cue(n, "late")), slide(f"#{p}-yr", cue(n, "1990s", frac=.3), 60),
          pop(f"#{p}-ok", cue(n, "was")), f'tl.to("#{p}-mon",{{scale:1.05,duration:.4,ease:"back.out(2)"}},{cue(n, "right"):.2f});']
    frame(n, "dotcom", css, html, js)


def chart_frame(n, slug, eyebrow, pts, xl, color, cues, notes):
    p = f"fd{n:02d}"
    W, H = 1500, 680
    svg, sx, sy = linechart(p, 0, 0, W, H, pts, color, "ln", xl)
    marks = "".join(f'<div class="{p}-chipx" id="{p}-m{i}" style="left:{210 + sx(a):.0f}px;top:{150 + sy(b) - 80:.0f}px;background:{bg}">{t}</div>' for i, (a, b, t, bg) in enumerate(notes))
    css = f".{p}-chart{{left:210px;top:150px;width:{W}px;height:{H}px;}}"
    html = f'<div class="{p}-pill {p}-eyebrow" id="{p}-eb" style="top:60px">{eyebrow}</div><div class="{p}-card {p}-chart" id="{p}-c"><svg width="{W}" height="{H}">{svg}</svg></div>{marks}'
    js = [rise(f"#{p}-eb", .1), rise(f"#{p}-c", .2), draw(f"#{p}-ln", cues[0], cues[1], 3000)]
    for i, t in enumerate(cues[2:]):
        js.append(pop(f"#{p}-m{i}", t))
    frame(n, slug, css, html, js)


def f24():
    n = 24
    chart_frame(n, "nasdaq-crash", "Nasdaq, 1995–2002", [(0, .08), (.3, .2), (.5, .4), (.62, .95), (.7, .6), (.82, .45), (1, .2)],
                [(0, "1995"), (.62, "2000"), (1, "2002")], C["primary"], [cue(n, "2000") - 1.2, 2.2, cue(n, "2000"), cue(n, "80"), cue(n, "hundreds")],
                [(.62, .95, "PEAK", C["primary"]), (1, .2, "≈ −80%", C["red"]), (.85, .42, "COMPANIES GONE", C["text"])])


def f25():
    n, p = 25, "fd25"
    css = f"""
.{p}-shop{{left:560px;top:180px;width:620px;height:560px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;}}
.{p}-stamp{{position:absolute;left:640px;top:380px;padding:20px 40px;border:10px solid {C['red']};color:{C['red']};font-weight:900;font-size:90px;border-radius:20px;transform:rotate(-12deg);}}
.{p}-tl{{position:absolute;left:1260px;top:230px;width:480px;}}
.{p}-ev{{display:flex;align-items:center;gap:20px;margin-bottom:40px;}}
.{p}-dot{{width:34px;height:34px;border-radius:50%;}}
"""
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eb">Dot-com casualty</div>
<div class="{p}-card {p}-shop" id="{p}-shop">{icon("dog", 220)}<div class="{p}-lbl" style="font-size:44px">Pets.com</div><div class="{p}-sub">online pet supplies</div></div>
<div class="{p}-tl"><div class="{p}-ev" id="{p}-e0"><div class="{p}-dot" style="background:{C['green']}"></div><div class="{p}-lbl">IPO · Feb 2000</div></div>
<div class="{p}-ev" id="{p}-e1"><div class="{p}-dot" style="background:{C['muted']}"></div><div class="{p}-lbl">9 months later…</div></div>
<div class="{p}-ev" id="{p}-e2"><div class="{p}-dot" style="background:{C['red']}"></div><div class="{p}-lbl">Shut down</div></div></div>
<div class="{p}-stamp" id="{p}-st">CLOSED</div>'''
    js = [rise(f"#{p}-eb", .1), pop(f"#{p}-shop", cue(n, "pets")), slide(f"#{p}-e0", cue(n, "public"), 60), slide(f"#{p}-e1", cue(n, "nine"), 60),
          slide(f"#{p}-e2", cue(n, "shut"), 60),
          f'tl.fromTo("#{p}-st",{{scale:2.5,opacity:0,rotation:-12}},{{scale:1,opacity:1,rotation:-12,duration:.3,ease:"power4.in"}},{cue(n, "shut"):.2f});']
    frame(n, "pets-com", css, html, js)


def f26():
    n, p = 26, "fd26"
    W, H = 1100, 560
    svg, sx, sy = linechart(p, 0, 0, W, H, [(0, .2), (.35, .55), (.5, .95), (.65, .5), (.8, .25), (1, .12)], C["primary"], "ln", [(.5, "MAR 2000"), (1, "2002")])
    css = f""".{p}-chart{{left:660px;top:250px;width:{W}px;height:{H}px;}} .{p}-crown{{position:absolute;left:{660 + sx(.5) - 60:.0f}px;top:130px;}}
.{p}-list{{position:absolute;left:110px;top:250px;display:flex;flex-direction:column;gap:26px;}}
.{p}-it{{display:flex;align-items:center;gap:18px;}}
.{p}-warn{{left:110px;top:640px;background:{C['red']};font-size:30px;width:480px;text-align:center;}}"""
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eb">Not just the weak ones</div><div class="{p}-crown" id="{p}-cr">{icon("crown", 120)}</div>
<div class="{p}-card {p}-chart" id="{p}-c"><svg width="{W}" height="{H}">{svg}</svg><div class="{p}-lbl" style="position:absolute;left:40px;top:24px">Cisco stock</div></div>
<div class="{p}-list"><div class="{p}-it" id="{p}-i0">{icon("check", 50)}<div class="{p}-lbl">Real products</div></div><div class="{p}-it" id="{p}-i1">{icon("check", 50)}<div class="{p}-lbl">Real customers</div></div><div class="{p}-it" id="{p}-i2">{icon("check", 50)}<div class="{p}-lbl">Real profits</div></div></div>
<div class="{p}-chipx {p}-warn" id="{p}-w">Great company ≠ great price</div>'''
    js = [rise(f"#{p}-eb", .1), rise(f"#{p}-c", cue(n, "cisco")), f'tl.fromTo("#{p}-ln",{{strokeDasharray:2500,strokeDashoffset:2500}},{{strokeDashoffset:1500,duration:{max(.8, cue(n, "valuable") - cue(n, "cisco")):.2f},ease:"power2.out"}},{cue(n, "cisco") + .3:.2f});',
          pop(f"#{p}-cr", cue(n, "valuable")), slide(f"#{p}-i0", cue(n, "products")), slide(f"#{p}-i1", cue(n, "customers")),
          slide(f"#{p}-i2", cue(n, "profits")),
          f'tl.to("#{p}-ln",{{strokeDashoffset:0,duration:1.6,ease:"power2.in"}},{cue(n, "lost"):.2f});',
          f'tl.to("#{p}-cr",{{y:140,rotation:40,opacity:0,duration:.8,ease:"power2.in"}},{cue(n, "lost"):.2f});',
          pop(f"#{p}-w", cue(n, "terrible"))]
    frame(n, "cisco", css, html, js)


def f27():
    n, p = 27, "fd27"
    items = [("box", "Online shopping", ""), ("chat", "Social media", ""), ("monitor", "Search", "")]
    css = f".{p}-hero{{position:absolute;left:110px;top:230px;}} .{p}-rubble{{position:absolute;left:90px;top:640px;width:400px;height:90px;border-radius:40px;background:#D6D3E8;}}"
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eb">And yet…</div><div class="{p}-rubble"></div><div class="{p}-hero" id="{p}-box">{icon("box", 330)}</div>
{tiles(p, items, 620, 250, 360, 400, 40, 3)}<div class="{p}-chipx" id="{p}-late" style="left:840px;top:720px">Just a few years later</div>'''
    js = [rise(f"#{p}-eb", .1), f'tl.fromTo("#{p}-box",{{y:200,opacity:0}},{{y:0,opacity:1,duration:.8,ease:"back.out(1.4)"}},{cue(n, "amazon"):.2f});',
          pop(f"#{p}-t2", cue(n, "google")), pop(f"#{p}-t0", cue(n, "shopping")), pop(f"#{p}-t1", cue(n, "social")),
          pop(f"#{p}-late", cue(n, "later"))]
    frame(n, "survivors", css, html, js)


def statements(n, slug, eyebrow, lines, cues, colors=None):
    p = f"fd{n:02d}"
    colors = colors or [C["text"]] * len(lines)
    rows = "".join(f'<div class="{p}-card {p}-st" id="{p}-s{i}" style="top:{220 + i*180}px;color:{colors[i]}"><div class="{p}-n">{i+1}</div>{t}</div>' for i, t in enumerate(lines))
    css = f""".{p}-st{{left:560px;width:1200px;height:140px;display:flex;align-items:center;gap:34px;padding:0 40px;font-weight:900;font-size:56px;}}
.{p}-n{{width:84px;height:84px;border-radius:22px;background:rgba(124,92,255,.12);color:{C['primary']};font-size:46px;display:flex;align-items:center;justify-content:center;}}"""
    html = f'<div class="{p}-pill {p}-eyebrow" id="{p}-eb">{eyebrow}</div>{rows}{bot_html(p, 160, 480, 220)}'
    js = [rise(f"#{p}-eb", .1), bot_in(p, n, .3)] + [slide(f"#{p}-s{i}", t, 80) for i, t in enumerate(cues)]
    frame(n, slug, css, html, js)


def f28():
    n = 28
    statements(n, "pattern", "The pattern", ["The technology wins", "Many early companies lose", "Timing is everything"],
               [cue(n, "technology"), cue(n, "early"), cue(n, "timing")], [C["green"], C["red"], C["primary"]])


def f29():
    n, p = 29, "fd29"
    html = (f'<div class="{p}-pill {p}-eyebrow" id="{p}-eb">3 gauges to watch</div>'
            + gauge(p, "g0", 160, 300, 480, "SPENDING") + gauge(p, "g1", 720, 300, 480, "CUSTOMERS") + gauge(p, "g2", 1280, 300, 480, "DEBT"))
    js = [rise(f"#{p}-eb", .1)]
    t = cue(n, "three")
    for i, d in enumerate([-30, 0, 25]):
        js.append(pop(f"#{p}-g{i}", t + i * .25))
        js.append(needle(p, f"g{i}", t + .3 + i * .25, d))
    frame(n, "gauges", "", html, js)


def f30():
    n, p = 30, "fd30"
    bars = "".join(f'<div class="{p}-bar" id="{p}-bx{i}" style="left:{900 + i*170}px"></div>' for i in range(5))
    css = f".{p}-bar{{position:absolute;bottom:280px;width:120px;height:440px;border-radius:18px 18px 6px 6px;background:{C['primary']};transform-origin:50% 100%;}} .{p}-cut{{left:1050px;top:830px;background:{C['red']};}}"
    html = (f'<div class="{p}-pill {p}-eyebrow" id="{p}-eb">Gauge 1 · Spending cuts</div>' + gauge(p, "g", 140, 230, 600, "AI BUDGETS")
            + bars + f'<div class="{p}-chipx {p}-cut" id="{p}-cut" style="top:820px">BUDGETS CUT = NO RETURN</div>')
    js = [rise(f"#{p}-eb", .1), pop(f"#{p}-g", .3), needle(p, "g", .6, -50)]
    for i in range(5):
        js.append(f'tl.fromTo("#{p}-bx{i}",{{scaleY:0}},{{scaleY:{.4 + i*.15:.2f},duration:.5,ease:"back.out(1.5)"}},{.5 + i*.12:.2f});')
    t = cue(n, "cutting")
    for i in range(5):
        js.append(f'tl.to("#{p}-bx{i}",{{scaleY:{.55 - i*.08:.2f},background:"{C["red"]}",duration:.5}},{t + i*.1:.2f});')
    js += [f'tl.to("#{p}-g-n",{{rotation:60,svgOrigin:"{SO(p)}",duration:1,ease:"elastic.out(1,.5)"}},{t:.2f});', pop(f"#{p}-cut", cue(n, "return"))]
    css += f" .{p}-cut{{top:820px;}}"
    frame(n, "gauge-spending", css.replace(f".{p}-cut{{left:1050px;top:830px;", f".{p}-cut{{left:1000px;"), html, js)


def f31():
    n, p = 31, "fd31"
    subs = "".join(f'<div class="{p}-card {p}-sub2" id="{p}-s{i}" style="top:{240 + i*150}px"><div class="{p}-lbl">Business #{i+1} · AI plan</div><div class="{p}-st" id="{p}-ok{i}">{icon("check" if i != 1 else "cross", 50)}<span>{"RENEWED" if i != 1 else "CANCELLED"}</span></div></div>' for i in range(4))
    css = f""".{p}-sub2{{left:900px;width:820px;height:120px;display:flex;align-items:center;justify-content:space-between;padding:0 40px;}}
.{p}-st{{display:flex;align-items:center;gap:14px;font-weight:900;font-size:28px;}}"""
    html = f'<div class="{p}-pill {p}-eyebrow" id="{p}-eb">Gauge 2 · Paying customers</div>' + gauge(p, "g", 140, 230, 600, "REPEAT REVENUE") + subs
    js = [rise(f"#{p}-eb", .1), pop(f"#{p}-g", .3), needle(p, "g", .6, 0)]
    for i in range(4):
        js.append(slide(f"#{p}-s{i}", cue(n, "businesses") + i * .2, 80))
        js.append(pop(f"#{p}-ok{i}", cue(n, "renewing") + i * .25))
    js.append(f'tl.to("#{p}-g-n",{{rotation:-55,svgOrigin:"{SO(p)}",duration:1,ease:"elastic.out(1,.5)"}},{cue(n, "repeat"):.2f});')
    frame(n, "gauge-customers", css, html, js)


def f32():
    n, p = 32, "fd32"
    css = f""".{p}-ripple{{position:absolute;left:1300px;top:460px;width:40px;height:40px;margin:-20px 0 0 -20px;border-radius:50%;border:8px solid {C['red']};}}
.{p}-loan{{left:1180px;top:400px;background:{C['red']};font-size:36px;}}
.{p}-cmp{{position:absolute;left:900px;top:680px;display:flex;gap:30px;}}"""
    rip = "".join(f'<div class="{p}-ripple" id="{p}-r{i}"></div>' for i in range(4))
    html = (f'<div class="{p}-pill {p}-eyebrow" id="{p}-eb">Gauge 3 · Debt</div>' + gauge(p, "g", 140, 230, 600, "BORROWED MONEY")
            + rip + f'<div class="{p}-chipx {p}-loan" id="{p}-loan">LOANS</div>'
            + f'<div class="{p}-cmp"><div class="{p}-card" id="{p}-pa" style="position:relative;padding:26px 40px"><div class="{p}-lbl" style="color:{C["green"]}">Paid with profits</div></div><div class="{p}-card" id="{p}-pb" style="position:relative;padding:26px 40px"><div class="{p}-lbl" style="color:{C["red"]}">Paid with loans</div></div></div>')
    js = [rise(f"#{p}-eb", .1), pop(f"#{p}-g", .3), needle(p, "g", .6, -30), pop(f"#{p}-loan", cue(n, "borrowed")),
          rise(f"#{p}-pb", cue(n, "loans")), rise(f"#{p}-pa", cue(n, "profits")),
          f'tl.to("#{p}-g-n",{{rotation:65,svgOrigin:"{SO(p)}",duration:1,ease:"elastic.out(1,.5)"}},{cue(n, "risk"):.2f});']
    for i in range(4):
        js.append(f'tl.fromTo("#{p}-r{i}",{{scale:1,opacity:.9}},{{scale:16,opacity:0,duration:1.6,ease:"power2.out"}},{cue(n, "spreads") - .3 + i*.25:.2f});')
    frame(n, "gauge-debt", css, html, js)


def f33():
    n = 33
    chart_frame(n, "waves", "How bubbles usually deflate", [(0, .9), (.2, .45), (.38, .7), (.58, .3), (.75, .4), (1, .55)],
                [(0, "PEAK"), (1, "YEARS LATER")], C["primary"], [cue(n, "waves") - .3, 3.0, cue(n, "sharp"), cue(n, "rebound"), cue(n, "another"), cue(n, "strongest")],
                [(.2, .45, "SHARP DROP", C["red"]), (.38, .7, "REBOUND", C["green"]), (.58, .3, "WEAK ONES FAIL", C["red"]), (1, .55, "STRONG KEEP BUILDING", C["primary"])])


def f34():
    n, p = 34, "fd34"
    css = f""".{p}-pie{{position:absolute;left:640px;top:180px;}} .{p}-pg{{position:absolute;left:1330px;top:330px;}}
.{p}-k{{left:1300px;top:660px;}} .{p}-t{{left:780px;top:760px;background:{C['text']};}}"""
    pie = f'''<svg class="{p}-pie" id="{p}-pie" width="560" height="560" viewBox="0 0 560 560"><circle cx="280" cy="280" r="250" fill="#E0E7FF"/>
<path id="{p}-sl" d="M280 280 L280 30 A250 250 0 0 1 516 360 Z" fill="{C['primary']}"/><circle cx="280" cy="280" r="120" fill="#fff"/>
<text x="280" y="296" text-anchor="middle" font-family="Inter" font-weight="900" font-size="44" fill="{C['text']}">INDEX</text></svg>'''
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eb">Why you should care</div>{pie}
<div class="{p}-pg" id="{p}-pg">{icon("piggy", 280)}</div><div class="{p}-chipx {p}-k" id="{p}-k">401(k)</div><div class="{p}-chipx {p}-t" id="{p}-t">BIG TECH SLICE</div>
{bot_html(p, 150, 470, 220)}'''
    js = [rise(f"#{p}-eb", .1), bot_in(p, n, .3), pop(f"#{p}-pie", cue(n, "biggest")),
          f'tl.fromTo("#{p}-sl",{{scale:0,transformOrigin:"280px 280px"}},{{scale:1,duration:.6,ease:"back.out(1.6)"}},{cue(n, "chunk"):.2f});',
          pop(f"#{p}-t", cue(n, "chunk") + .3), pop(f"#{p}-pg", cue(n, "401")), pop(f"#{p}-k", cue(n, "401") + .2),
          f'tl.to("#{p}-pg",{{y:-14,duration:.3}},{cue(n, "riding"):.2f});tl.to("#{p}-pg",{{y:0,duration:.3}},{cue(n, "riding")+.3:.2f});']
    frame(n, "your-401k", css, html, js)


def f35():
    n, p = 35, "fd35"
    items = [("Know what you own", "know"), ("Stay diversified", "diversified"), ("Don't bet money you can't lose", "bet")]
    rows = "".join(f'<div class="{p}-row" id="{p}-r{i}"><div class="{p}-box" id="{p}-bx{i}">{icon("check", 34)}</div><div class="{p}-tx">{t}</div></div>' for i, (t, _) in enumerate(items))
    css = f""".{p}-win{{left:420px;top:150px;width:1080px;height:600px;overflow:hidden;}}
.{p}-bar{{height:64px;background:rgba(238,240,255,.9);display:flex;align-items:center;padding:0 24px;gap:12px;}}
.{p}-dot{{width:16px;height:16px;border-radius:50%;}}
.{p}-body{{padding:46px 64px;}}
.{p}-row{{display:flex;align-items:center;gap:28px;height:110px;}}
.{p}-box{{width:62px;height:62px;border-radius:16px;border:3px solid rgba(124,92,255,.35);display:flex;align-items:center;justify-content:center;}}
.{p}-tx{{font-weight:800;font-size:46px;}}
.{p}-np{{left:620px;top:800px;background:{C['muted']};font-size:22px;}}"""
    html = f'''<div class="{p}-card {p}-win" id="{p}-w"><div class="{p}-bar"><div class="{p}-dot" style="background:#FF5F57"></div><div class="{p}-dot" style="background:#FEBC2E"></div><div class="{p}-dot" style="background:#28C840"></div><div class="{p}-lbl" style="margin-left:16px;font-size:22px;color:{C['muted']}">dont-panic.md</div></div><div class="{p}-body">{rows}</div></div>
<div class="{p}-chipx {p}-np" id="{p}-np">NOT FINANCIAL ADVICE</div>'''
    js = [rise(f"#{p}-w", .1)]
    for i, (_, w) in enumerate(items):
        js.append(f'gsap.set("#{p}-bx{i} svg",{{opacity:0}});')
        js.append(slide(f"#{p}-r{i}", cue(n, w) - .2))
        js.append(f'tl.to("#{p}-bx{i}",{{background:"#E7F8F1",borderColor:"{C["green"]}",duration:.2}},{cue(n, w)+.5:.2f});tl.to("#{p}-bx{i} svg",{{opacity:1,duration:.2}},{cue(n, w)+.5:.2f});')
    js.append(pop(f"#{p}-np", cue(n, "advice")))
    frame(n, "no-panic", css, html, js)


def f36():
    n, p = 36, "fd36"
    cells = "".join(f'<div class="{p}-cell" id="{p}-c{i}"></div>' for i in range(100))
    eggs = "".join(f'<div class="{p}-egg" id="{p}-e{i}" style="left:{180 + (i%3)*90}px;top:{300 + (i//3)*30}px">{icon("egg", 70)}</div>' for i in range(6))
    css = f""".{p}-grid{{left:900px;top:170px;width:620px;height:620px;padding:30px;display:grid;grid-template-columns:repeat(10,1fr);gap:10px;}}
.{p}-cell{{border-radius:8px;background:{C['primary']};opacity:.85;}}
.{p}-basket{{position:absolute;left:150px;top:420px;width:360px;height:180px;border-radius:0 0 90px 90px;background:#C9A27A;}}
.{p}-egg{{position:absolute;}}
.{p}-lab{{left:1560px;top:420px;}} .{p}-tim{{left:640px;top:820px;background:{C['green']};}}"""
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eb">Diversified = many baskets</div>{eggs}<div class="{p}-basket" id="{p}-bk"></div>
<div class="{p}-card {p}-grid" id="{p}-g">{cells}</div><div class="{p}-chipx {p}-lab" id="{p}-lab">100s OF COMPANIES</div>
<div class="{p}-chipx {p}-tim" id="{p}-tim">TIME IN THE MARKET &gt; TIMING</div>'''
    js = [rise(f"#{p}-eb", .1), rise(f"#{p}-bk", cue(n, "eggs")),
          f'tl.fromTo(".{p}-egg",{{y:-120,opacity:0}},{{y:0,opacity:1,duration:.4,stagger:.08,ease:"bounce.out"}},{cue(n, "eggs"):.2f});',
          rise(f"#{p}-g", cue(n, "index")),
          f'tl.fromTo(".{p}-cell",{{scale:0}},{{scale:1,duration:.25,stagger:.01,ease:"back.out(2)"}},{cue(n, "hundreds"):.2f});',
          pop(f"#{p}-lab", cue(n, "industries")),
          f'tl.to(["#{p}-c3","#{p}-c4","#{p}-c13","#{p}-c14"],{{background:"{C["red"]}",duration:.3}},{cue(n, "crashes"):.2f});',
          pop(f"#{p}-tim", cue(n, "time", 2))]
    frame(n, "diversify", css, html, js)


def f37():
    n, p = 37, "fd37"
    css = f""".{p}-ball{{position:absolute;left:760px;top:160px;width:420px;height:480px;transform-origin:50% 100%;}}
.{p}-chip{{position:absolute;left:880px;top:420px;}} .{p}-q{{left:1260px;top:240px;background:#fff;color:{C['text']};font-size:38px;box-shadow:0 14px 40px rgba(124,92,255,.2);}}
.{p}-ans{{position:absolute;left:0;right:0;top:720px;text-align:center;font-weight:900;font-size:76px;}}
.{p}-ans span{{color:{C['primary']};}}"""
    balloon = f'''<svg class="{p}-ball" id="{p}-ball" viewBox="0 0 420 480"><ellipse cx="210" cy="210" rx="190" ry="210" fill="{C['primary']}" opacity=".85"/><ellipse cx="150" cy="130" rx="40" ry="60" fill="#fff" opacity=".35"/><text x="210" y="250" text-anchor="middle" font-family="Inter" font-weight="900" font-size="120" fill="#fff">AI</text></svg>'''
    html = f'''{balloon}<div class="{p}-chip" id="{p}-chip">{icon("chip", 180)}</div><div class="{p}-pill {p}-q" id="{p}-q">Pop?</div>
<div class="{p}-ans" id="{p}-ans">Who survives the <span>shakeout?</span></div>{bot_html(p, 220, 480, 240)}'''
    js = [pop(f"#{p}-ball", .1), bot_in(p, n, .3), f'gsap.set("#{p}-chip",{{opacity:0}});', pop(f"#{p}-q", cue(n, "pop")),
          f'tl.to("#{p}-ball",{{scale:.55,opacity:.35,duration:1.2,ease:"power2.in"}},{cue(n, "parts"):.2f});',
          f'tl.fromTo("#{p}-chip",{{opacity:0,scale:.4}},{{opacity:1,scale:1,duration:.5,ease:"back.out(2.5)"}},{cue(n, "technology"):.2f});',
          rise(f"#{p}-ans", cue(n, "survives"))]
    frame(n, "verdict", css, html, js)


def f38():
    n, p = 38, "fd38"
    css = f""".{p}-logo{{position:absolute;left:0;right:0;top:280px;text-align:center;font-weight:900;font-size:120px;letter-spacing:-.03em;}}
.{p}-logo span{{color:{C['primary']};}}
.{p}-row{{position:absolute;left:0;right:0;top:470px;display:flex;justify-content:center;gap:28px;}}
.{p}-c{{padding:20px 36px;border-radius:999px;background:rgba(124,92,255,.12);color:{C['primary']};font-weight:800;font-size:36px;}}
.{p}-s{{padding:24px 50px;border-radius:999px;background:{C['text']};color:#fff;font-weight:800;font-size:40px;}}
.{p}-poll{{position:absolute;left:0;right:0;top:620px;display:flex;justify-content:center;gap:30px;}}
.{p}-opt{{position:relative;padding:22px 44px;font-weight:900;font-size:40px;}}
.{p}-cursor{{position:absolute;left:1180px;top:540px;width:46px;height:46px;}}"""
    html = f'''<div class="{p}-logo" id="{p}-logo">Future <span>Decoded</span></div>
<div class="{p}-poll"><div class="{p}-card {p}-opt" id="{p}-o0">🫧 Bubble?</div><div class="{p}-card {p}-opt" id="{p}-o1">🚀 Beginning?</div></div>
<div class="{p}-row" id="{p}-row"><div class="{p}-c">decoded ✓</div><div class="{p}-s" id="{p}-sb">Subscribe</div></div>
{bot_html(p, 1430, 200, 220)}
<svg class="{p}-cursor" id="{p}-cur" viewBox="0 0 24 24"><path d="M3 2 L20 12 L12 13.5 L8.5 21 Z" fill="#fff" stroke="{C['text']}" stroke-width="1.6" stroke-linejoin="round"/></svg>'''
    html = html.replace("🫧 ", "").replace("🚀 ", "")
    js = [rise(f"#{p}-logo", .1), pop(f"#{p}-o0", cue(n, "bubble")), pop(f"#{p}-o1", cue(n, "beginning")),
          rise(f"#{p}-row", cue(n, "subscribe") - .3), bot_in(p, n, .4),
          f'tl.fromTo("#{p}-cur",{{x:260,y:200,opacity:0}},{{x:0,y:0,opacity:1,duration:.7,ease:"power3.out"}},{cue(n, "subscribe"):.2f});',
          f'tl.to("#{p}-sb",{{scale:.92,duration:.1}},{cue(n, "subscribe")+.8:.2f});tl.to("#{p}-sb",{{scale:1,background:"{C["primary"]}",duration:.25}},{cue(n, "subscribe")+.9:.2f});']
    frame(n, "cta", css, html, js)


if __name__ == "__main__":
    for f in (G.f1, G.f2, G.f3, G.f4, G.f5, G.f6, G.f7):
        f()
    for f in (f8, f9, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, f26, f27, f28,
              f29, f30, f31, f32, f33, f34, f35, f36, f37, f38):
        f()
    print("ok", len(os.listdir(G.OUT)))
