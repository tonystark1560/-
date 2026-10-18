"""Generates compositions/frames/*.html for the trial (orchestrator-authored frames)."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "compositions", "frames")
os.makedirs(OUT, exist_ok=True)

C = dict(bg="#EEF0FF", primary="#7C5CFF", text="#1B1F3B", muted="#5B6178", light="#9AA0B8",
         cyan="#22D3EE", violet="#8B5CF6", red="#E24040", green="#0EA674", cyandark="#0891B2",
         blue="#BFD7FF", lilac="#E3D4FF", peach="#FFE1EC")
GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'

FONTS = "\n".join(
    f"@font-face{{font-family:'Inter';src:url('assets/fonts/Inter-{n}.otf') format('opentype');font-weight:{w};font-style:normal;}}"
    for n, w in [("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700), ("ExtraBold", 800), ("Black", 900)])

# 12x12 pixel robot. v violet body, c cyan, w white, k ink, m cyan mouth
ROBOT = [
    "....cc......",
    "....cc......",
    "..vvvvvvvv..",
    "..vwwvvwwv..",
    "..vwkvvwkv..",
    "..vvvvvvvv..",
    "..vvmmmmvv..",
    "...vvvvvv...",
    ".ccvvvvvvcc.",
    ".c.vvvvvv.c.",
    "...vv..vv...",
    "...cc..cc...",
]
PIX = {"v": C["violet"], "c": C["cyan"], "w": "#FFFFFF", "k": C["text"], "m": C["cyan"]}


def robot(p, size=300):
    rects = []
    for y, row in enumerate(ROBOT):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            cls = ""
            if ch == "k":
                cls = f' class="{p}-pupil"'
            elif ch == "w":
                cls = f' class="{p}-eyewhite"'
            elif y <= 1:
                cls = f' class="{p}-antenna"'
            rects.append(f'<rect x="{x}" y="{y}" width="1.02" height="1.02" fill="{PIX[ch]}"{cls}/>')
    return (f'<svg class="{p}-robot" viewBox="0 0 12 12" width="{size}" height="{size}" '
            f'shape-rendering="crispEdges">{"".join(rects)}</svg>')


def tulip(p, size=360):
    m = [
        "....r..r....",
        "...rrrrrr...",
        "...rprrpr...",
        "...rrrrrr...",
        "....rrrr....",
        ".....gg.....",
        "..g..gg..g..",
        "..gg.gg.gg..",
        "...ggggg....",
        ".....gg.....",
        "....bbbb....",
        "....bbbb....",
    ]
    col = {"r": "#FF5C8A", "p": "#FF9DB8", "g": C["green"], "b": "#C9A27A"}
    rects = "".join(f'<rect x="{x}" y="{y}" width="1.02" height="1.02" fill="{col[ch]}"/>'
                    for y, row in enumerate(m) for x, ch in enumerate(row) if ch != ".")
    return f'<svg class="{p}-tulip" viewBox="0 0 12 12" width="{size}" height="{size}" shape-rendering="crispEdges">{rects}</svg>'


def house(p, size=200):
    m = [
        ".....r......",
        "....rrr.....",
        "...rrrrr....",
        "..rrrrrrr...",
        ".rrrrrrrrr..",
        "..wwwwwww...",
        "..wbbwddw...",
        "..wbbwddw...",
        "..wwwwddw...",
    ]
    col = {"r": C["primary"], "w": "#FFFFFF", "b": C["cyan"], "d": C["violet"]}
    rects = "".join(f'<rect x="{x}" y="{y}" width="1.02" height="1.02" fill="{col[ch]}"/>'
                    for y, row in enumerate(m) for x, ch in enumerate(row) if ch != ".")
    return f'<svg class="{p}-house" viewBox="0 0 12 9" width="{size}" height="{size*0.75}" shape-rendering="crispEdges">{rects}</svg>'


def person(p, color, extra=""):
    m = ["..xx..", "..xx..", ".xxxx.", "x.xx.x", "..xx..", ".x..x."]
    rects = "".join(f'<rect x="{x}" y="{y}" width="1.02" height="1.02" fill="{color}"/>'
                    for y, row in enumerate(m) for x, ch in enumerate(row) if ch == "x")
    return f'<svg class="{p}-person {extra}" viewBox="0 0 6 6" width="120" height="120" shape-rendering="crispEdges">{rects}</svg>'


def base_css(p):
    return f"""
{FONTS}
#root{{position:absolute;inset:0;width:1920px;height:1080px;overflow:hidden;font-family:'Inter',sans-serif;color:{C['text']};}}
.{p}-bg{{position:absolute;inset:0;background:{C['bg']};overflow:hidden;}}
.{p}-blob{{position:absolute;border-radius:50%;filter:blur(110px);opacity:.85;}}
.{p}-b1{{width:900px;height:900px;left:-200px;top:-260px;background:{C['blue']};}}
.{p}-b2{{width:820px;height:820px;right:-180px;top:120px;background:{C['lilac']};}}
.{p}-b3{{width:700px;height:700px;left:520px;bottom:-420px;background:{C['peach']};}}
.{p}-stage{{position:absolute;inset:0;}}
.{p}-card{{position:absolute;background:rgba(255,255,255,.88);border-radius:22px;box-shadow:0 18px 50px rgba(124,92,255,.14),0 2px 6px rgba(27,31,59,.06);}}
.{p}-pill{{position:absolute;display:inline-flex;align-items:center;gap:10px;padding:12px 26px;border-radius:999px;font-weight:700;font-size:26px;letter-spacing:.08em;text-transform:uppercase;}}
.{p}-robotwrap{{position:absolute;}}
.{p}-robot{{display:block;filter:drop-shadow(0 14px 22px rgba(124,92,255,.35));}}
"""


def bg_html(p, d):
    return (f'<div class="clip {p}-bg" id="{p}-bg" data-start="0" data-duration="{d}" data-track-index="0">'
            f'<div class="{p}-blob {p}-b1" id="{p}-b1"></div><div class="{p}-blob {p}-b2" id="{p}-b2"></div>'
            f'<div class="{p}-blob {p}-b3" id="{p}-b3"></div></div>')


def bg_js(p, d):
    return (f'tl.fromTo("#{p}-b1",{{x:0,y:0}},{{x:140,y:60,duration:{d},ease:"none"}},0);'
            f'tl.fromTo("#{p}-b2",{{x:0,y:0}},{{x:-120,y:-50,duration:{d},ease:"none"}},0);'
            f'tl.fromTo("#{p}-b3",{{x:0,y:0}},{{x:-90,y:-40,duration:{d},ease:"none"}},0);')


def blink(p, sel, at):
    # deterministic one-off blink: eyes squash and return
    return (f'tl.to("{sel} .{p}-eyewhite, {sel} .{p}-pupil",{{scaleY:0.1,transformOrigin:"50% 50%",duration:0.08}},{at});'
            f'tl.to("{sel} .{p}-eyewhite, {sel} .{p}-pupil",{{scaleY:1,duration:0.1}},{at + 0.1});')


def bob(p, sel, start, end, amp=10, period=1.6):
    # explicit up/down tweens instead of repeat/yoyo (seek-safe)
    js, t, up = [], start, True
    while t < end - 0.05:
        dur = min(period / 2, end - t)
        js.append(f'tl.to("{sel}",{{y:{-amp if up else 0},duration:{dur:.3f},ease:"sine.inOut"}},{t:.3f});')
        t += dur
        up = not up
    return "".join(js)


def write(frame_id, p, d, css, html, js, k=1.0):
    doc = f"""<template>
<style>{base_css(p)}{css}</style>
<div id="root" data-composition-id="{frame_id}" data-width="1920" data-height="1080">
{bg_html(p, d)}
<div class="clip {p}-stage" id="{p}-stage" data-start="0" data-duration="{d}" data-track-index="1">
{html}
</div>
</div>
{GSAP}
<script>
(function(){{
const tl = gsap.timeline({{ paused: true }});
{bg_js(p, d)}
{js}
const K = {k:.5f};
if (K !== 1) tl.getChildren(false, true, true).forEach(c => {{ if (c.startTime() > 0.001) c.startTime(c.startTime() * K); }});
window.__timelines = window.__timelines || {{}};
window.__timelines["{frame_id}"] = tl;
}})();
</script>
</template>
"""
    with open(os.path.join(OUT, frame_id + ".html"), "w") as f:
        f.write(doc)


import re as _re
_sb = open(os.path.join(ROOT, "STORYBOARD.md")).read()
DUR = {int(n): float(d) for n, d in _re.findall(r"## Frame (\d+) .*?- duration: ([\d.]+)s", _sb, _re.S)}
OLD = {1: 16.725, 2: 7.253, 3: 11.861, 4: 9.28, 5: 16.256, 6: 14.123, 7: 6.507}
meta = json.load(open(os.path.join(ROOT, "audio_meta.json")))
VDUR = {v["frame"]: v["duration_s"] for v in meta["voices"]}


def K(n):
    return VDUR[n] / OLD[n]


# ---------------- Frame 1: the bad week ----------------
def f1():
    p, d = "fd01", DUR[1]
    tickers = ["AI CHIPS", "CLOUD", "AI MODELS", "SERVERS", "ROBOTICS", "AI APPS"]
    cards = []
    for i, t in enumerate(tickers):
        col, row = i % 3, i // 3
        x, y = 640 + col * 380, 200 + row * 320
        cards.append(f'''<div class="{p}-card {p}-tick" id="{p}-t{i}" style="left:{x}px;top:{y}px;width:340px;height:280px;">
<div class="{p}-tname">{t}</div>
<div class="{p}-arrow {p}-up" id="{p}-up{i}">▲</div><div class="{p}-arrow {p}-down" id="{p}-dn{i}">▼</div>
<svg class="{p}-spark" viewBox="0 0 300 140" width="300" height="140">
<path id="{p}-g{i}" d="M0 120 L50 105 L95 112 L140 80 L190 70 L235 40 L300 18" fill="none" stroke="{C['green']}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
<path id="{p}-r{i}" d="M0 18 L60 30 L110 70 L150 62 L200 105 L250 98 L300 132" fill="none" stroke="{C['red']}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
</svg></div>''')
    css = f"""
.{p}-tick{{padding:26px 28px;overflow:hidden;}}
.{p}-tick::after{{content:'';position:absolute;inset:0;border-radius:22px;background:{C['red']};opacity:var(--redden,0);pointer-events:none;}}
.{p}-tname{{font-weight:800;font-size:30px;letter-spacing:.04em;}}
.{p}-arrow{{position:absolute;right:28px;top:22px;font-size:36px;font-weight:900;}}
.{p}-up{{color:{C['green']};}} .{p}-down{{color:{C['red']};opacity:0;}}
.{p}-spark{{position:absolute;left:20px;bottom:20px;}}
.{p}-eyebrow{{left:120px;top:110px;background:{C['primary']};color:#fff;}}
.{p}-hero{{position:absolute;left:110px;top:230px;font-weight:900;font-size:84px;line-height:.95;letter-spacing:-.03em;}}
.{p}-hero span{{color:{C['red']};}}
.{p}-robotwrap{{left:150px;top:520px;}}
.{p}-meter{{left:640px;top:820px;width:1100px;height:56px;padding:0;overflow:hidden;border-radius:999px;}}
.{p}-meterfill{{position:absolute;left:8px;top:8px;bottom:8px;width:1084px;border-radius:999px;background:linear-gradient(90deg,{C['green']},{C['cyan']});transform-origin:0 50%;}}
.{p}-meterlbl{{position:absolute;left:30px;top:13px;font-weight:800;font-size:24px;letter-spacing:.1em;color:#fff;}}
"""
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eyebrow">Mid-October 2026</div>
<div class="{p}-hero" id="{p}-hero">A really<br><span>bad week</span></div>
<div class="{p}-robotwrap" id="{p}-bot">{robot(p, 300)}</div>
{''.join(cards)}
<div class="{p}-card {p}-meter" id="{p}-meter"><div class="{p}-meterfill" id="{p}-fill"></div><div class="{p}-meterlbl">VALUE</div></div>'''
    js = [f'tl.fromTo("#{p}-eyebrow",{{y:-30,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"back.out(2)"}},0.15);',
          f'tl.fromTo("#{p}-bot",{{y:80,opacity:0}},{{y:0,opacity:1,duration:.6,ease:"back.out(1.6)"}},0.3);']
    for i in range(6):
        js.append(f'tl.fromTo("#{p}-t{i}",{{scale:.6,opacity:0}},{{scale:1,opacity:1,duration:.45,ease:"back.out(1.8)"}},{0.6 + i*0.25:.2f});')
        js.append(f'gsap.set("#{p}-g{i}",{{strokeDasharray:420,strokeDashoffset:420}});gsap.set("#{p}-r{i}",{{strokeDasharray:420,strokeDashoffset:420}});')
        js.append(f'tl.to("#{p}-g{i}",{{strokeDashoffset:0,duration:1.2,ease:"power2.out"}},{0.8 + i*0.25:.2f});')
    js.append(f'tl.fromTo("#{p}-hero",{{x:-60,opacity:0}},{{x:0,opacity:1,duration:.6,ease:"power3.out"}},3.5);')
    js.append(f'tl.fromTo("#{p}-meter",{{y:40,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"power2.out"}},5.6);')
    # "up and up" - cards nudge upward
    js.append(f'tl.to(".{p}-tick",{{y:-14,duration:.6,ease:"power2.out",stagger:.06}},9.6);')
    js.append(blink(p, f"#{p}-bot", 7.8))
    # suddenly dropped hard
    for i in range(6):
        t = 11.3 + i * 0.22
        js.append(f'tl.to("#{p}-g{i}",{{opacity:0,duration:.15}},{t:.2f});')
        js.append(f'tl.to("#{p}-r{i}",{{strokeDashoffset:0,duration:.55,ease:"power3.in"}},{t:.2f});')
        js.append(f'tl.to("#{p}-up{i}",{{opacity:0,duration:.1}},{t:.2f});tl.to("#{p}-dn{i}",{{opacity:1,duration:.1}},{t:.2f});')
        js.append(f'tl.to("#{p}-t{i}",{{"--redden":0.08,y:20,duration:.4,ease:"power3.in"}},{t:.2f});')
    # mascot startled
    js.append(f'tl.to("#{p}-bot",{{y:-60,duration:.18,ease:"power2.out"}},12.1);tl.to("#{p}-bot",{{y:0,duration:.35,ease:"bounce.out"}},12.28);')
    js.append(f'tl.to("#{p}-bot .{p}-pupil",{{x:0.35,duration:.2}},12.1);')
    # wiping out value: meter drains + turns red
    js.append(f'tl.to("#{p}-fill",{{scaleX:.18,background:"linear-gradient(90deg,{C["red"]},#FF8A8A)",duration:3.0,ease:"power2.inOut"}},13.1);')
    js.append(f'tl.to("#{p}-hero",{{x:-6,duration:.05}},12.7);tl.to("#{p}-hero",{{x:6,duration:.05}},12.75);tl.to("#{p}-hero",{{x:0,duration:.05}},12.8);')
    write("01-bad-week", p, d, css, html, "\n".join(js), k=K(1))


# ---------------- Frame 2: is this it? ----------------
def f2():
    p, d = "fd02", DUR[2]
    css = f"""
.{p}-robotwrap{{left:420px;top:560px;}}
.{p}-balloon{{position:absolute;left:820px;top:90px;width:520px;height:600px;transform-origin:50% 100%;}}
.{p}-q{{left:1300px;top:150px;background:#fff;color:{C['text']};font-size:40px;box-shadow:0 14px 40px rgba(124,92,255,.2);}}
.{p}-needle{{position:absolute;left:1500px;top:330px;width:340px;height:14px;}}
"""
    balloon = f'''<svg class="{p}-balloon" id="{p}-balloon" viewBox="0 0 520 600">
<defs><radialGradient id="{p}-bg1" cx="35%" cy="30%" r="75%"><stop offset="0" stop-color="#C9B8FF"/><stop offset=".55" stop-color="{C['primary']}"/><stop offset="1" stop-color="#4B2FD1"/></radialGradient></defs>
<path d="M260 560 C 250 590, 300 600, 230 640" stroke="{C['muted']}" stroke-width="5" fill="none"/>
<ellipse cx="260" cy="260" rx="230" ry="260" fill="url(#{p}-bg1)"/>
<ellipse cx="185" cy="160" rx="55" ry="80" fill="#fff" opacity=".35"/>
<path d="M240 515 L280 515 L268 545 L252 545 Z" fill="#4B2FD1"/>
<text x="260" y="300" text-anchor="middle" font-family="Inter" font-weight="900" font-size="150" fill="#fff">AI</text>
</svg>'''
    needle = f'''<svg class="{p}-needle" id="{p}-needle" viewBox="0 0 340 14"><rect x="40" y="5" width="300" height="4" fill="{C['muted']}"/><path d="M0 7 L40 3 L40 11 Z" fill="{C['text']}"/><circle cx="330" cy="7" r="7" fill="{C['red']}"/></svg>'''
    string = f'<svg style="position:absolute;left:560px;top:600px" width="560" height="140" viewBox="0 0 560 140"><path id="{p}-str" d="M10 120 C 200 40, 380 140, 520 20" stroke="{C["muted"]}" stroke-width="4" fill="none"/></svg>'
    html = f'''{string}{balloon}<div class="{p}-robotwrap" id="{p}-bot">{robot(p, 260)}</div>
<div class="{p}-pill {p}-q" id="{p}-q">Is this it?</div>{needle}'''
    js = [f'tl.fromTo("#{p}-bot",{{x:-120,opacity:0}},{{x:0,opacity:1,duration:.5,ease:"power3.out"}},0.05);',
          f'tl.fromTo("#{p}-balloon",{{scale:.2,opacity:0}},{{scale:1,opacity:1,duration:.8,ease:"back.out(1.4)"}},0.2);',
          f'tl.fromTo("#{p}-str",{{opacity:0}},{{opacity:1,duration:.4}},0.4);']
    # slow inflate with wobble (explicit tweens)
    t, sgn = 1.0, 1
    scale = 1.0
    while t < 6.2:
        scale += 0.025
        js.append(f'tl.to("#{p}-balloon",{{rotation:{3*sgn},scale:{scale:.3f},duration:.55,ease:"sine.inOut"}},{t:.2f});')
        t += 0.55
        sgn = -sgn
    js.append(f'tl.fromTo("#{p}-q",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.45,ease:"back.out(2.4)"}},3.8);')
    js.append(f'tl.fromTo("#{p}-needle",{{x:420,opacity:0}},{{x:0,opacity:1,duration:.9,ease:"power2.out"}},5.2);')
    # tension at "popping?"
    for k, dx in enumerate([8, -8, 6, -6, 0]):
        js.append(f'tl.to("#{p}-balloon",{{x:{dx},duration:.06}},{6.25 + k*0.06:.2f});')
    js.append(f'tl.to("#{p}-bot .{p}-pupil",{{x:0.3,y:-0.25,duration:.25}},3.9);')
    js.append(blink(p, f"#{p}-bot", 2.0))
    js.append(bob(p, f"#{p}-bot", 0.6, d, amp=8))
    write("02-is-this-it", p, d, css, html, "\n".join(js), k=K(2))


# ---------------- Frame 3: roadmap ----------------
def f3():
    p, d = "fd03", DUR[3]
    items = [("What is a bubble?", 2.8), ("Why AI looks like one", 4.7), ("Why it might not be", 6.8), ("What it means for you", 8.5)]
    rows = "".join(f'''<div class="{p}-row" id="{p}-row{i}"><div class="{p}-box" id="{p}-box{i}"><svg viewBox="0 0 24 24" width="34" height="34"><path id="{p}-chk{i}" d="M5 12.5 L10 17 L19 7" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/></svg></div><div class="{p}-txt">{t}</div></div>'''
                   for i, (t, _) in enumerate(items))
    css = f"""
.{p}-win{{left:380px;top:120px;width:1020px;height:700px;overflow:hidden;}}
.{p}-bar{{height:64px;background:rgba(238,240,255,.9);display:flex;align-items:center;padding:0 24px;gap:12px;border-bottom:1.5px solid rgba(124,92,255,.15);}}
.{p}-dot{{width:16px;height:16px;border-radius:50%;}}
.{p}-title{{margin-left:18px;font-weight:600;font-size:22px;color:{C['muted']};}}
.{p}-chip{{margin-left:auto;padding:8px 18px;border-radius:999px;background:rgba(124,92,255,.12);color:#4C2FC9;font-weight:800;font-size:18px;letter-spacing:.1em;}}
.{p}-body{{padding:50px 64px;}}
.{p}-h{{font-weight:900;font-size:64px;letter-spacing:-.02em;margin-bottom:34px;}}
.{p}-row{{display:flex;align-items:center;gap:28px;height:96px;}}
.{p}-box{{width:52px;height:52px;border-radius:14px;border:3px solid rgba(124,92,255,.35);display:flex;align-items:center;justify-content:center;}}
.{p}-txt{{font-weight:700;font-size:40px;}}
.{p}-prog{{position:absolute;left:64px;right:64px;bottom:40px;height:12px;border-radius:999px;background:rgba(124,92,255,.12);overflow:hidden;}}
.{p}-progfill{{position:absolute;inset:0;background:{C['primary']};transform-origin:0 50%;}}
.{p}-robotwrap{{left:1330px;top:560px;}}
"""
    html = f'''<div class="{p}-card {p}-win" id="{p}-win"><div class="{p}-bar"><div class="{p}-dot" style="background:#FF5F57"></div><div class="{p}-dot" style="background:#FEBC2E"></div><div class="{p}-dot" style="background:#28C840"></div><div class="{p}-title">decode.md</div><div class="{p}-chip" id="{p}-chip">DECODING…</div></div>
<div class="{p}-body"><div class="{p}-h" id="{p}-h">Today</div>{rows}</div><div class="{p}-prog"><div class="{p}-progfill" id="{p}-pf"></div></div></div>
<div class="{p}-robotwrap" id="{p}-bot">{robot(p, 240)}</div>'''
    js = [f'tl.fromTo("#{p}-win",{{y:60,scale:.94,opacity:0}},{{y:0,scale:1,opacity:1,duration:.6,ease:"power3.out"}},0.05);',
          f'tl.fromTo("#{p}-h",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:.4}},0.3);',
          f'tl.fromTo("#{p}-chip",{{scale:0}},{{scale:1,duration:.4,ease:"back.out(2.5)"}},1.3);',
          f'tl.fromTo("#{p}-pf",{{scaleX:0}},{{scaleX:1,duration:{d-1.5:.2f},ease:"none"}},1.3);',
          f'tl.fromTo("#{p}-bot",{{x:200,opacity:0}},{{x:0,opacity:1,duration:.6,ease:"back.out(1.5)"}},0.9);']
    for i, (_, t) in enumerate(items):
        js.append(f'tl.fromTo("#{p}-row{i}",{{x:-40,opacity:0}},{{x:0,opacity:1,duration:.4,ease:"power3.out"}},{t-0.15:.2f});')
        js.append(f'gsap.set("#{p}-chk{i}",{{strokeDasharray:30,strokeDashoffset:30}});')
        js.append(f'tl.to("#{p}-box{i}",{{background:"{C["primary"]}",borderColor:"{C["primary"]}",duration:.2}},{t+0.9:.2f});')
        js.append(f'tl.to("#{p}-chk{i}",{{strokeDashoffset:0,duration:.3,ease:"power2.out"}},{t+0.95:.2f});')
    js.append(f'tl.to("#{p}-row3 .{p}-txt",{{color:"{C["primary"]}",duration:.3}},9.5);')
    js.append(blink(p, f"#{p}-bot", 3.6) + blink(p, f"#{p}-bot", 8.0))
    js.append(bob(p, f"#{p}-bot", 1.5, d, amp=10))
    write("03-roadmap", p, d, css, html, "\n".join(js), k=K(3))


# ---------------- Frame 4: definition ----------------
def f4():
    p, d = "fd04", DUR[4]
    css = f"""
.{p}-chart{{left:560px;top:110px;width:1220px;height:740px;}}
.{p}-eyebrow{{left:120px;top:150px;background:{C['primary']};color:#fff;}}
.{p}-def{{position:absolute;left:120px;top:250px;width:400px;font-weight:900;font-size:76px;line-height:1;letter-spacing:-.02em;}}
.{p}-def span{{color:{C['primary']};}}
.{p}-robotwrap{{left:170px;top:560px;}}
"""
    chart = f'''<div class="{p}-card {p}-chart" id="{p}-chart"><svg width="1220" height="740" viewBox="0 0 1220 740">
<line x1="90" y1="660" x2="1160" y2="660" stroke="{C['light']}" stroke-width="3"/><line x1="90" y1="60" x2="90" y2="660" stroke="{C['light']}" stroke-width="3"/>
<text x="1160" y="700" text-anchor="end" font-family="Inter" font-weight="700" font-size="24" fill="{C['muted']}">TIME</text>
<text x="110" y="70" font-family="Inter" font-weight="700" font-size="24" fill="{C['muted']}">PRICE</text>
<ellipse id="{p}-bub" cx="800" cy="350" rx="300" ry="190" fill="rgba(124,92,255,.10)" stroke="rgba(124,92,255,.45)" stroke-width="4"/>
<ellipse id="{p}-shine" cx="700" cy="270" rx="60" ry="26" fill="#fff" opacity=".7"/>
<line id="{p}-real" x1="90" y1="520" x2="1160" y2="520" stroke="{C['cyan']}" stroke-width="6" stroke-dasharray="18 14"/>
<g id="{p}-reallbl"><rect x="880" y="534" width="260" height="50" rx="25" fill="{C['cyandark']}"/><text x="1010" y="568" text-anchor="middle" font-family="Inter" font-weight="800" font-size="24" fill="#fff">REAL VALUE</text></g>
<path id="{p}-price" d="M90 600 L250 575 L380 545 L500 470 L620 380 L720 300 L820 230 L920 170" fill="none" stroke="{C['primary']}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
<path id="{p}-more" d="M920 170 L1010 120 L1100 80" fill="none" stroke="{C['primary']}" stroke-width="10" stroke-linecap="round" stroke-dasharray="4 22"/>
<g id="{p}-ppl">{''.join(f'<g transform="translate({560+k*110},590) scale(0.6)"><rect x="18" y="0" width="24" height="24" fill="{C["violet"]}"/><rect x="10" y="28" width="40" height="40" fill="{C["violet"]}"/><rect x="0" y="28" width="10" height="10" fill="{C["violet"]}"/><rect x="50" y="10" width="10" height="28" fill="{C["violet"]}"/></g>' for k in range(4))}</g>
</svg></div>'''
    html = f'''<div class="{p}-pill {p}-eyebrow" id="{p}-eyebrow">Bubble (n.)</div>
<div class="{p}-def" id="{p}-def">Price <span>&gt;</span> worth</div>
<div class="{p}-robotwrap" id="{p}-bot">{robot(p, 230)}</div>{chart}'''
    js = [f'tl.fromTo("#{p}-chart",{{y:50,opacity:0}},{{y:0,opacity:1,duration:.6,ease:"power3.out"}},0.05);',
          f'tl.fromTo("#{p}-bot",{{y:80,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"back.out(1.6)"}},0.3);',
          f'tl.fromTo("#{p}-eyebrow",{{y:-24,opacity:0}},{{y:0,opacity:1,duration:.4,ease:"back.out(2)"}},1.5);',
          f'gsap.set("#{p}-price",{{strokeDasharray:1100,strokeDashoffset:1100}});',
          f'tl.to("#{p}-price",{{strokeDashoffset:0,duration:2.0,ease:"power2.in"}},2.4);',
          f'tl.fromTo("#{p}-def",{{x:-40,opacity:0}},{{x:0,opacity:1,duration:.5,ease:"power3.out"}},3.3);',
          f'tl.fromTo("#{p}-bub",{{scale:0,opacity:0,transformOrigin:"50% 50%"}},{{scale:1,opacity:1,duration:.8,ease:"back.out(1.5)"}},4.1);',
          f'tl.fromTo("#{p}-shine",{{opacity:0}},{{opacity:.7,duration:.4}},4.6);',
          f'gsap.set("#{p}-real",{{strokeDashoffset:600}});',
          f'tl.fromTo("#{p}-real",{{opacity:0}},{{opacity:1,strokeDashoffset:0,duration:.8,ease:"power2.out"}},5.4);',
          f'tl.fromTo("#{p}-reallbl",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.4}},5.8);',
          f'tl.fromTo("#{p}-ppl g",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.35,stagger:.15,ease:"back.out(2)"}},6.8);',
          f'gsap.set("#{p}-more",{{opacity:0}});',
          f'tl.to("#{p}-more",{{opacity:1,duration:.4}},8.3);',
          f'tl.to("#{p}-bub",{{scale:1.08,duration:{d-8.3:.2f},ease:"sine.inOut",transformOrigin:"50% 50%"}},8.3);',
          blink(p, f"#{p}-bot", 2.2), bob(p, f"#{p}-bot", 1.0, d, amp=8)]
    write("04-definition", p, d, css, html, "\n".join(js), k=K(4))


# ---------------- Frame 5: tulips ----------------
def f5():
    p, d = "fd05", DUR[5]
    css = f"""
.{p}-place{{left:120px;top:110px;background:#fff;color:{C['text']};box-shadow:0 12px 30px rgba(124,92,255,.18);}}
.{p}-tulipcard{{left:120px;top:210px;width:520px;height:620px;display:flex;align-items:center;justify-content:center;}}
.{p}-tag{{position:absolute;left:470px;top:250px;padding:14px 24px;border-radius:14px;background:{C['primary']};color:#fff;font-weight:900;font-size:40px;transform-origin:0 50%;}}
.{p}-eq{{position:absolute;left:700px;top:430px;font-weight:900;font-size:120px;color:{C['primary']};}}
.{p}-housecard{{left:860px;top:300px;width:360px;height:360px;display:flex;align-items:center;justify-content:center;}}
.{p}-plant{{left:1300px;top:150px;width:470px;height:260px;display:flex;align-items:center;justify-content:center;gap:24px;}}
.{p}-plant .{p}-x{{position:absolute;inset:0;}}
.{p}-chain{{left:1300px;top:450px;width:470px;height:380px;}}
.{p}-chain .{p}-person{{position:absolute;bottom:40px;}}
.{p}-price{{position:absolute;font-weight:900;font-size:34px;color:{C['green']};}}
.{p}-pot{{width:140px;height:140px;}}
.{p}-lbl{{font-weight:800;font-size:30px;}}
"""
    pot = f'<svg class="{p}-pot" viewBox="0 0 6 6" shape-rendering="crispEdges"><rect x="2" y="0" width="2" height="2" fill="{C["green"]}"/><rect x="1" y="2" width="4" height="1" fill="#C9A27A"/><rect x="1.5" y="3" width="3" height="3" fill="#C9A27A"/></svg>'
    cross = f'<svg class="{p}-x" viewBox="0 0 470 260"><path id="{p}-x1" d="M60 40 L410 220" stroke="{C["red"]}" stroke-width="16" stroke-linecap="round"/><path id="{p}-x2" d="M410 40 L60 220" stroke="{C["red"]}" stroke-width="16" stroke-linecap="round"/></svg>'
    ppl = "".join(f'<div id="{p}-pp{k}" style="position:absolute;left:{30+k*150}px;bottom:40px">{person(p, [C["violet"], C["primary"], C["cyan"]][k])}</div>'
                  f'<div class="{p}-price" id="{p}-pr{k}" style="left:{60+k*150}px;top:{150-k*40}px">{"$"*(k+1)}</div>' for k in range(3))
    arrows = f'<svg style="position:absolute;inset:0" viewBox="0 0 470 380"><path id="{p}-a1" d="M120 250 Q 165 200 200 250" stroke="{C["muted"]}" stroke-width="5" fill="none"/><path id="{p}-a2" d="M270 250 Q 315 200 350 250" stroke="{C["muted"]}" stroke-width="5" fill="none"/></svg>'
    html = f'''<div class="{p}-pill {p}-place" id="{p}-place">Netherlands · 1600s</div>
<div class="{p}-card {p}-tulipcard" id="{p}-tc">{tulip(p, 380)}</div>
<div class="{p}-tag" id="{p}-tag">PRICE ↑</div>
<div class="{p}-eq" id="{p}-eq">=</div>
<div class="{p}-card {p}-housecard" id="{p}-hc">{house(p, 260)}</div>
<div class="{p}-card {p}-plant" id="{p}-plant">{pot}<div class="{p}-lbl">TO PLANT</div>{cross}</div>
<div class="{p}-card {p}-chain" id="{p}-chain"><div class="{p}-lbl" style="position:absolute;left:30px;top:24px">TO RESELL</div>{arrows}{ppl}</div>'''
    js = [f'tl.fromTo("#{p}-tc",{{y:60,opacity:0}},{{y:0,opacity:1,duration:.6,ease:"power3.out"}},0.1);',
          f'tl.fromTo("#{p}-tc svg",{{scale:.3,transformOrigin:"50% 100%"}},{{scale:1,duration:.9,ease:"back.out(1.6)"}},1.5);',
          f'tl.fromTo("#{p}-place",{{y:-24,opacity:0}},{{y:0,opacity:1,duration:.4,ease:"back.out(2)"}},2.8);',
          f'tl.fromTo("#{p}-tag",{{scale:0,rotation:-20}},{{scale:1,rotation:-6,duration:.5,ease:"back.out(2.2)"}},6.8);',
          f'tl.to("#{p}-tag",{{scale:1.25,duration:1.4,ease:"power2.in"}},7.6);',
          f'tl.fromTo("#{p}-eq",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.35,ease:"back.out(3)"}},9.6);',
          f'tl.fromTo("#{p}-hc",{{scale:.5,opacity:0}},{{scale:1,opacity:1,duration:.5,ease:"back.out(2)"}},10.2);',
          f'tl.fromTo("#{p}-plant",{{x:80,opacity:0}},{{x:0,opacity:1,duration:.5,ease:"power3.out"}},11.2);',
          f'gsap.set(["#{p}-x1","#{p}-x2"],{{strokeDasharray:400,strokeDashoffset:400}});',
          f'tl.to("#{p}-x1",{{strokeDashoffset:0,duration:.25}},13.0);tl.to("#{p}-x2",{{strokeDashoffset:0,duration:.25}},13.2);',
          f'tl.fromTo("#{p}-chain",{{x:80,opacity:0}},{{x:0,opacity:1,duration:.5,ease:"power3.out"}},13.6);']
    for k in range(3):
        js.append(f'tl.fromTo("#{p}-pp{k}",{{y:30,opacity:0}},{{y:0,opacity:1,duration:.3,ease:"back.out(2)"}},{13.9+k*0.5:.2f});')
        js.append(f'tl.fromTo("#{p}-pr{k}",{{y:20,opacity:0}},{{y:0,opacity:1,duration:.3,ease:"back.out(2)"}},{14.1+k*0.5:.2f});')
    js.append(f'gsap.set(["#{p}-a1","#{p}-a2"],{{strokeDasharray:200,strokeDashoffset:200}});')
    js.append(f'tl.to("#{p}-a1",{{strokeDashoffset:0,duration:.3}},14.6);tl.to("#{p}-a2",{{strokeDashoffset:0,duration:.3}},15.1);')
    write("05-tulips", p, d, css, html, "\n".join(js), k=K(5))


# ---------------- Frame 6: the loop ----------------
def f6():
    p, d = "fd06", DUR[6]
    nodes = [("PRICE ↑", 960, 230, 1.9, "pr"), ("EXCITEMENT", 1290, 700, 3.4, "ex"), ("BUYING", 630, 700, 6.0, "by")]
    css = f"""
.{p}-node{{position:absolute;width:330px;height:150px;margin-left:-165px;margin-top:-75px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:42px;letter-spacing:.02em;}}
.{p}-title{{left:120px;top:120px;background:{C['primary']};color:#fff;}}
.{p}-robotwrap{{left:1530px;top:140px;}}
.{p}-crowd{{position:absolute;left:110px;top:430px;width:400px;display:flex;flex-wrap:wrap;gap:6px;}}
"""
    ndiv = "".join(f'<div class="{p}-card {p}-node" id="{p}-{k}" style="left:{x}px;top:{y}px">{t}</div>' for t, x, y, _, k in nodes)
    loop = f'''<svg style="position:absolute;left:0;top:0" width="1920" height="1080" viewBox="0 0 1920 1080">
<defs><marker id="{p}-ah" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{C['primary']}"/></marker>
<marker id="{p}-ahr" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{C['red']}"/></marker></defs>
<path id="{p}-e1" d="M1110 300 Q 1300 420 1300 610" stroke="{C['primary']}" stroke-width="10" fill="none" marker-end="url(#{p}-ah)"/>
<path id="{p}-e2" d="M1120 760 Q 960 840 800 760" stroke="{C['primary']}" stroke-width="10" fill="none" marker-end="url(#{p}-ah)"/>
<path id="{p}-e3" d="M620 610 Q 620 420 810 300" stroke="{C['primary']}" stroke-width="10" fill="none" marker-end="url(#{p}-ah)"/>
<path id="{p}-r1" d="M1300 610 Q 1300 420 1110 300" stroke="{C['red']}" stroke-width="10" fill="none" marker-end="url(#{p}-ahr)"/>
<path id="{p}-r2" d="M800 760 Q 960 840 1120 760" stroke="{C['red']}" stroke-width="10" fill="none" marker-end="url(#{p}-ahr)"/>
<path id="{p}-r3" d="M810 300 Q 620 420 620 610" stroke="{C['red']}" stroke-width="10" fill="none" marker-end="url(#{p}-ahr)"/>
<circle id="{p}-dot" cx="0" cy="0" r="16" fill="{C['cyan']}"/>
</svg>'''
    crowd = "".join(f'<div id="{p}-c{k}">{person(p, C["violet"])}</div>' for k in range(5))
    html = f'''<div class="{p}-pill {p}-title" id="{p}-title">The bubble loop</div>{loop}{ndiv}
<div class="{p}-crowd" id="{p}-crowd">{crowd}</div>
<div class="{p}-robotwrap" id="{p}-bot">{robot(p, 220)}</div>'''
    js = [f'tl.fromTo("#{p}-title",{{y:-24,opacity:0}},{{y:0,opacity:1,duration:.4,ease:"back.out(2)"}},0.1);',
          f'tl.fromTo("#{p}-bot",{{x:120,opacity:0}},{{x:0,opacity:1,duration:.5,ease:"back.out(1.5)"}},0.3);',
          f'gsap.set(["#{p}-r1","#{p}-r2","#{p}-r3"],{{opacity:0}});gsap.set("#{p}-dot",{{opacity:0}});']
    for t, x, y, at, k in nodes:
        js.append(f'tl.fromTo("#{p}-{k}",{{scale:.4,opacity:0}},{{scale:1,opacity:1,duration:.45,ease:"back.out(2)"}},{at:.2f});')
    for i, at in [(1, 2.8), (2, 5.3), (3, 7.0)]:
        js.append(f'tl.fromTo("#{p}-e{i}",{{opacity:0,strokeDasharray:700,strokeDashoffset:700}},{{opacity:1,strokeDashoffset:0,duration:.5,ease:"power2.out"}},{at:.2f});')
    js.append(f'tl.fromTo("#{p}-crowd > div",{{y:30,opacity:0}},{{y:0,opacity:1,duration:.3,stagger:.12,ease:"back.out(2)"}},6.0);')
    # dot travels around the loop, faster each lap (seek-safe: explicit motionless keyframes via x/y attr tweens)
    pts = [(960, 300), (1300, 610), (960, 790), (620, 610)]
    t, lap_dur = 7.4, 1.0
    js.append(f'tl.set("#{p}-dot",{{opacity:1,attr:{{cx:{pts[0][0]},cy:{pts[0][1]}}}}},{t});')
    while t < 9.4:
        for j in range(1, 5):
            px, py = pts[j % 4]
            js.append(f'tl.to("#{p}-dot",{{attr:{{cx:{px},cy:{py}}},duration:{lap_dur/4:.3f},ease:"none"}},{t:.3f});')
            t += lap_dur / 4
        lap_dur *= 0.7
    # pulse nodes as the loop accelerates
    js.append(f'tl.to(["#{p}-pr","#{p}-ex","#{p}-by"],{{scale:1.06,duration:.3}},8.0);tl.to(["#{p}-pr","#{p}-ex","#{p}-by"],{{scale:1,duration:.3}},8.3);')
    # until one day: no new buyers
    js.append(f'tl.to("#{p}-dot",{{opacity:0,duration:.3}},{t:.3f});')
    js.append(f'tl.to("#{p}-crowd > div",{{y:40,opacity:0,duration:.3,stagger:.08}},10.8);')
    js.append(f'tl.to("#{p}-by",{{opacity:.45,duration:.4}},11.3);')
    # reverses
    js.append(f'tl.to(["#{p}-e1","#{p}-e2","#{p}-e3"],{{opacity:0,duration:.25}},12.3);')
    js.append(f'tl.to(["#{p}-r1","#{p}-r2","#{p}-r3"],{{opacity:1,duration:.25}},12.3);')
    js.append(f'tl.to("#{p}-pr",{{color:"{C["red"]}",duration:.2}},12.7);')
    js.append(f'tl.to("#{p}-pr",{{y:40,rotation:-4,duration:.6,ease:"bounce.out"}},13.0);')
    js.append(f'tl.to("#{p}-bot .{p}-pupil",{{y:0.3,duration:.2}},13.0);')
    js.append(blink(p, f"#{p}-bot", 4.5))
    write("06-loop", p, d, css, html, "\n".join(js), k=K(6))


# ---------------- Frame 7: feels like the future + end card ----------------
def f7():
    p, d = "fd07", DUR[7]
    css = f"""
.{p}-bubble{{position:absolute;left:660px;top:120px;width:600px;height:600px;border-radius:50%;
 background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.95) 0 6%,rgba(255,255,255,.15) 14%,rgba(190,215,255,.25) 45%,rgba(227,212,255,.45) 70%,rgba(124,92,255,.35) 100%);
 box-shadow:inset 0 0 60px rgba(124,92,255,.35),0 30px 80px rgba(124,92,255,.25);}}
.{p}-robotwrap{{left:830px;top:290px;}}
.{p}-spark{{position:absolute;width:26px;height:26px;background:{C['cyan']};clip-path:polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%);}}
.{p}-future{{position:absolute;left:0;right:0;top:760px;text-align:center;font-weight:900;font-size:84px;letter-spacing:-.02em;}}
.{p}-future span{{color:{C['primary']};}}
.{p}-end{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:34px;background:{C['bg']};}}
.{p}-logo{{font-weight:900;font-size:110px;letter-spacing:-.03em;}}
.{p}-logo span{{color:{C['primary']};}}
.{p}-row{{display:flex;gap:26px;align-items:center;}}
.{p}-chip{{padding:16px 30px;border-radius:999px;background:rgba(124,92,255,.12);color:{C['primary']};font-weight:800;font-size:34px;}}
.{p}-sub{{padding:22px 46px;border-radius:999px;background:{C['text']};color:#fff;font-weight:800;font-size:38px;}}
.{p}-cursor{{position:absolute;left:1180px;top:640px;width:46px;height:46px;}}
.{p}-endbot{{position:absolute;left:1380px;top:260px;}}
"""
    sparks = "".join(f'<div class="{p}-spark" id="{p}-s{k}" style="left:{x}px;top:{y}px"></div>'
                     for k, (x, y) in enumerate([(620, 180), (1270, 230), (600, 560), (1300, 600), (940, 90), (1180, 690)]))
    html = f'''<div class="{p}-bubble" id="{p}-bub"></div>
<div class="{p}-robotwrap" id="{p}-bot">{robot(p, 260)}</div>{sparks}
<div class="{p}-future" id="{p}-fut">Feels like <span>the future</span></div>
'''
    js = [f'tl.fromTo("#{p}-bot",{{y:60,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"back.out(1.6)"}},0.05);',
          f'tl.fromTo("#{p}-bub",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.9,ease:"elastic.out(1,.6)"}},2.2);',
          f'tl.fromTo(".{p}-spark",{{scale:0,rotation:0}},{{scale:1,rotation:90,duration:.5,stagger:.12,ease:"back.out(3)"}},3.0);',
          f'tl.to("#{p}-bot .{p}-pupil",{{y:-0.3,duration:.3}},3.5);',
          f'tl.fromTo("#{p}-fut",{{y:40,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"power3.out"}},5.0);',
          bob(p, f"#{p}-bot", 0.6, 6.6, amp=16, period=2.0),
          f'tl.to("#{p}-bub",{{scale:1.04,duration:3.0,ease:"sine.inOut"}},3.2);',
]
    write("07-future", p, d, css, html, "\n".join(js), k=K(7))


if __name__ == "__main__":
    for fn in (f1, f2, f3, f4, f5, f6, f7):
        fn()
    print("ok", sorted(os.listdir(OUT)))
