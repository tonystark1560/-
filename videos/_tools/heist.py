"""Crypto Heists — vertical (1080x1920) dark cyber scene kit, built on the Long Night frame builder.

Extra frame-spec keys on top of longnight.Ep: bg kinds servers | city | room | grid | bridge | black,
props listed in heist_prop(), actions listed in HEp.action().
"""
import longnight
from longnight import C, W, H, GROUND, Ep
from hf import pop, shake

K = dict(btc="#F7931A", bnb="#F3BA2F", cyan="#38E1FF", navy="#0A1020", panel="#101830", line="#1E2A48", green="#3CF2A0", red="#FF3B30")

_bg0, _prop0 = longnight.bg_svg, longnight.prop


def grid_floor(y0=1100, color="rgba(56,225,255,.28)"):
    v = "".join(f'<line x1="{540 + (i - 10) * 30}" y1="{y0}" x2="{540 + (i - 10) * 260}" y2="{H}" stroke="{color}" stroke-width="2"/>' for i in range(21))
    hz = "".join(f'<line x1="0" y1="{y0 + (k * k) * 9}" x2="{W}" y2="{y0 + (k * k) * 9}" stroke="{color}" stroke-width="2"/>' for k in range(1, 16))
    return v + hz


def bg_svg(kind, p):
    if kind == "servers":
        racks = ""
        for i, x in enumerate(range(-20, W, 230)):
            racks += f'<rect x="{x}" y="260" width="200" height="1300" rx="8" fill="#0C1426" stroke="#1A2744" stroke-width="4"/>'
            for j in range(22):
                c = [K["green"], K["cyan"], "#2B3A5E"][(i * 7 + j * 3) % 3]
                racks += f'<rect x="{x + 16}" y="{290 + j * 56}" width="168" height="40" rx="4" fill="#111C34"/><circle class="{p}-led" cx="{x + 34}" cy="{310 + j * 56}" r="5" fill="{c}"/><circle cx="{x + 54}" cy="{310 + j * 56}" r="5" fill="#2B3A5E"/>'
        body = f'<rect width="{W}" height="{H}" fill="#060A16"/>{racks}<rect x="0" y="1560" width="{W}" height="{H - 1560}" fill="#050812"/>'
        return f'<svg width="{W}" height="{H}">{body}</svg>'
    if kind == "city":
        b = ""
        for i in range(14):
            x, h = i * 80 - 20, 300 + (i * 173) % 420
            b += f'<rect x="{x}" y="{1250 - h}" width="76" height="{h}" fill="#0B1222"/>' + "".join(
                f'<rect x="{x + 12 + (k % 3) * 20}" y="{1270 - h + (k // 3) * 40}" width="10" height="16" fill="{"#FFD27A" if (i + k) % 4 == 0 else "#18233D"}"/>' for k in range(3 * (h // 60)))
        body = (f'<defs><linearGradient id="cg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050816"/><stop offset="1" stop-color="#1A1440"/></linearGradient></defs>'
                f'<rect width="{W}" height="{H}" fill="url(#cg)"/>{longnight.stars(50, 700)}{b}<rect x="0" y="1250" width="{W}" height="{H - 1250}" fill="#070A14"/>')
        return f'<svg width="{W}" height="{H}">{body}</svg>'
    if kind == "room":
        body = (f'<rect width="{W}" height="{H}" fill="#070910"/>' + "".join(f'<rect x="{x}" y="0" width="6" height="{GROUND}" fill="#0B0E18"/>' for x in range(0, W, 120))
                + f'<rect x="0" y="{GROUND}" width="{W}" height="{H - GROUND}" fill="#0D101A"/><rect x="0" y="{GROUND}" width="{W}" height="18" fill="#161B2A"/>')
        return f'<svg width="{W}" height="{H}">{body}</svg>'
    if kind == "grid":
        body = f'<rect width="{W}" height="{H}" fill="#04060E"/><rect x="0" y="1060" width="{W}" height="60" fill="rgba(56,225,255,.12)"/>{grid_floor()}'
        return f'<svg width="{W}" height="{H}">{body}</svg>'
    if kind == "bridge":
        body = (f'<rect width="{W}" height="{H}" fill="#05070F"/>{longnight.stars(60, 900)}{grid_floor(1300, "rgba(243,186,47,.16)")}'
                f'<path d="M0 900 L300 900 L260 1500 L0 1500 Z" fill="#141C34"/><path d="M{W} 900 L{W - 300} 900 L{W - 260} 1500 L{W} 1500 Z" fill="#141C34"/>'
                f'<rect x="0" y="880" width="300" height="24" fill="{K["bnb"]}"/><rect x="{W - 300}" y="880" width="300" height="24" fill="{K["bnb"]}"/>')
        return f'<svg width="{W}" height="{H}">{body}</svg>'
    return _bg0(kind, p)


def coin(ident, x, y, s=1.0, kind="btc", cls=""):
    col, letter = (K["btc"], "B") if kind == "btc" else (K["bnb"], "BNB")
    fs = 70 if kind == "btc" else 34
    return (f'<div class="{cls}" id="{ident}" style="position:absolute;left:{x}px;top:{y}px;width:{110 * s:.0f}px;height:{110 * s:.0f}px;border-radius:50%;background:{col};'
            f'border:{7 * s:.0f}px solid rgba(0,0,0,.22);display:flex;align-items:center;justify-content:center;font-weight:900;font-size:{fs * s:.0f}px;color:#fff;box-shadow:0 6px 0 rgba(0,0,0,.35)">{letter}</div>')


def person(color="#5B6B8C", head="#E9B48A"):
    return (f'<circle cx="60" cy="40" r="32" fill="{head}"/><path d="M8 170 Q8 86 60 86 Q112 86 112 170 Z" fill="{color}"/>')


HACKER = ('<path d="M200 40 C 300 40 350 120 350 220 L350 330 L50 330 L50 220 C 50 120 100 40 200 40 Z" fill="#1A2133"/>'
          '<ellipse cx="200" cy="215" rx="95" ry="110" fill="#04050A"/>'
          '<path d="M30 600 Q30 330 200 320 Q370 330 370 600 Z" fill="#1A2133"/><path d="M150 330 L200 420 L250 330" stroke="#0C1020" stroke-width="10" fill="none"/>')


def heist_prop(kind, ident, x, y, s=1.0, o=None):
    o = o or {}
    pos = f"position:absolute;left:{x}px;top:{y}px"
    if kind == "coin":
        return coin(ident, x, y, s, o.get("k", "btc"))
    if kind == "coins":
        n, k = o.get("n", 6), o.get("k", "btc")
        return "".join(coin(f"{ident}-{i}", x + (i % o.get("cols", 3)) * 125 * s, y + (i // o.get("cols", 3)) * 125 * s, s, k, f"{ident}-c") for i in range(n))
    if kind == "wallet":
        col = o.get("col", K["cyan"])
        return (f'<div id="{ident}" style="{pos};width:{o.get("w", 380)}px;padding:34px 26px;border-radius:28px;background:{K["panel"]};border:5px solid {col};text-align:center;'
                f'font-weight:900;font-size:40px;letter-spacing:.06em;color:{col};text-transform:uppercase;box-shadow:0 0 50px {col}55">{o.get("label", "")}'
                f'<div style="font-size:30px;color:{C["text"]};margin-top:10px;letter-spacing:.02em">{o.get("sub", "")}</div></div>')
    if kind == "tower":
        wins = "".join(f'<rect x="{30 + (k % 5) * 56}" y="{150 + (k // 5) * 70}" width="32" height="40" fill="{K["bnb"] if (k * 7) % 5 else "#2A2410"}"/>' for k in range(5 * 14))
        return (f'<svg id="{ident}" style="{pos};overflow:visible" width="{340 * s:.0f}" height="{1150 * s:.0f}" viewBox="0 0 340 1150"><rect x="0" y="100" width="340" height="1050" fill="#121A30"/>'
                f'<rect x="0" y="100" width="340" height="14" fill="{K["bnb"]}"/>{wins}<rect x="150" y="0" width="40" height="100" fill="#121A30"/></svg>'
                f'<div style="position:absolute;left:{x - 60}px;top:{y + 20}px;width:{340 * s + 120:.0f}px;text-align:center;font-weight:900;font-size:44px;color:{K["bnb"]};letter-spacing:.12em">{o.get("label", "")}</div>')
    if kind == "hacker":
        return (f'<svg id="{ident}" style="{pos};overflow:visible" width="{400 * s:.0f}" height="{600 * s:.0f}" viewBox="0 0 400 600">{HACKER}'
                f'<rect x="90" y="470" width="220" height="140" rx="10" fill="#C9D3E6"/><rect x="100" y="480" width="200" height="120" rx="6" fill="#0A0F1C"/>'
                f'<circle cx="200" cy="540" r="16" fill="{K["cyan"]}" opacity=".7"/></svg>')
    if kind == "person":
        return f'<svg id="{ident}" style="{pos};overflow:visible" width="{120 * s:.0f}" height="{170 * s:.0f}" viewBox="0 0 120 170">{person(o.get("col", "#5B6B8C"))}</svg>'
    if kind == "users":
        n, cols = o.get("n", 12), o.get("cols", 4)
        return "".join(f'<svg class="{ident}-u" id="{ident}-{i}" style="position:absolute;left:{x + (i % cols) * 190}px;top:{y + (i // cols) * 230}px;overflow:visible" width="120" height="170" viewBox="0 0 120 170">'
                       f'<g id="{ident}-{i}-b">{person(o.get("col", "#5B6B8C"))}</g></svg>' for i in range(n))
    if kind == "screen":
        return (f'<div id="{ident}" style="{pos};width:{o.get("w", 800)}px;min-height:{o.get("h", 500)}px;border-radius:22px;background:{o.get("bgc", "#0D1428")};border:6px solid {o.get("bc", "#26324F")};'
                f'padding:36px 40px;box-sizing:border-box;font-weight:800;font-size:{o.get("fs", 38)}px;color:{C["text"]};box-shadow:0 30px 80px rgba(0,0,0,.6)">{o.get("html", "")}</div>')
    if kind == "terminal":
        lines = o.get("lines", [])
        return (f'<div id="{ident}" style="{pos};width:{o.get("w", 860)}px;border-radius:18px;background:#03070C;border:4px solid #1B3B2E;padding:30px 34px;box-sizing:border-box;'
                f'font-family:monospace;font-weight:700;font-size:{o.get("fs", 34)}px;color:{K["green"]};line-height:1.5">'
                + "".join(f'<div class="{ident}-ln" id="{ident}-{i}">{t}</div>' for i, t in enumerate(lines)) + '</div>')
    if kind == "clock":
        return (f'<div id="{ident}" style="{pos};padding:20px 40px;border-radius:18px;background:#000;border:5px solid #331010;font-family:monospace;font-weight:900;'
                f'font-size:{o.get("fs", 150)}px;color:{K["red"]};letter-spacing:.04em;text-shadow:0 0 30px rgba(255,59,48,.7)">{o.get("t", "17:15")}</div>')
    if kind == "big":
        return (f'<div id="{ident}" style="{pos};width:{o.get("w", W)}px;text-align:center;font-weight:900;font-size:{o.get("fs", 200)}px;line-height:1;color:{o.get("col", C["text"])};'
                f'text-shadow:0 8px 0 rgba(0,0,0,.4)">{o.get("pre", "")}<span id="{ident}-n">{o.get("v", "0")}</span>{o.get("suf", "")}</div>'
                + (f'<div id="{ident}-cap" style="position:absolute;left:{x}px;top:{y + o.get("fs", 200) * 1.05:.0f}px;width:{o.get("w", W)}px;text-align:center;font-weight:800;font-size:44px;letter-spacing:.14em;color:{C["gray"]};text-transform:uppercase">{o["cap"]}</div>' if o.get("cap") else ""))
    if kind == "lock":
        col = o.get("col", K["red"])
        return (f'<svg id="{ident}" style="{pos};overflow:visible" width="{300 * s:.0f}" height="{380 * s:.0f}" viewBox="0 0 300 380">'
                f'<path id="{ident}-sh" d="M70 170 L70 110 A80 80 0 0 1 230 110 L230 170" stroke="{col}" stroke-width="34" fill="none"/><rect x="20" y="160" width="260" height="210" rx="30" fill="{col}"/>'
                f'<circle cx="150" cy="250" r="26" fill="#111"/><rect x="140" y="250" width="20" height="60" fill="#111"/></svg>')
    if kind == "shield":
        return (f'<svg id="{ident}" style="{pos};overflow:visible" width="{420 * s:.0f}" height="{500 * s:.0f}" viewBox="0 0 420 500"><path d="M210 10 L400 80 L400 240 C 400 380 300 460 210 490 C 120 460 20 380 20 240 L20 80 Z" fill="{K["bnb"]}"/>'
                f'<path d="M210 50 L362 106 L362 240 C 362 350 285 420 210 448 C 135 420 58 350 58 240 L58 106 Z" fill="#141008"/>'
                f'<text x="210" y="290" text-anchor="middle" font-family="Inter" font-weight="900" font-size="96" fill="{K["bnb"]}">{o.get("label", "SAFU")}</text></svg>')
    if kind == "key":
        col = o.get("col", K["bnb"])
        return (f'<div id="{ident}" style="{pos};display:flex;align-items:center;gap:16px"><svg width="{200 * s:.0f}" height="{90 * s:.0f}" viewBox="0 0 200 90"><circle cx="45" cy="45" r="38" fill="none" stroke="{col}" stroke-width="16"/>'
                f'<rect x="80" y="37" width="115" height="16" fill="{col}"/><rect x="150" y="53" width="14" height="26" fill="{col}"/><rect x="176" y="53" width="14" height="20" fill="{col}"/></svg>'
                f'<div style="font-weight:900;font-size:{44 * s:.0f}px;color:{col}">{o.get("label", "")}</div></div>')
    if kind == "chain":
        n, labels = o.get("n", 5), o.get("labels", [])
        out = []
        for i in range(n):
            bx = x + i * 205
            out.append(f'<div class="{ident}-b" id="{ident}-{i}" style="position:absolute;left:{bx}px;top:{y}px;width:160px;height:160px;border-radius:18px;background:{K["panel"]};border:5px solid {o.get("col", K["btc"])};'
                       f'display:flex;align-items:center;justify-content:center;font-weight:900;font-size:34px;color:{C["text"]}">{labels[i] if i < len(labels) else ""}</div>')
            if i < n - 1:
                out.append(f'<div class="{ident}-l" id="{ident}-l{i}" style="position:absolute;left:{bx + 160}px;top:{y + 70}px;width:45px;height:20px;background:{o.get("col", K["btc"])}"></div>')
        return "".join(out)
    if kind == "ceo":
        return (f'<svg id="{ident}" style="{pos};overflow:visible" width="{420 * s:.0f}" height="{520 * s:.0f}" viewBox="0 0 420 520">'
                f'<circle cx="210" cy="120" r="80" fill="#D9A77E"/><path d="M130 100 Q210 10 290 100 Q280 50 210 40 Q140 50 130 100 Z" fill="#1B1B1F"/>'
                f'<path d="M40 520 Q40 230 210 220 Q380 230 380 520 Z" fill="#1E2538"/><path d="M180 222 L210 300 L240 222 Z" fill="#E9EEF7"/>'
                f'<rect x="300" y="250" width="16" height="170" fill="#666"/><rect x="284" y="210" width="48" height="70" rx="22" fill="#2B2B2B"/></svg>'
                + (f'<div id="{ident}-live" style="position:absolute;left:{x + 10}px;top:{y - 70}px;padding:8px 22px;border-radius:8px;background:{K["red"]};font-weight:900;font-size:36px;color:#fff">{o.get("lt", "LIVE")}</div>' if o.get("live", True) else ""))
    if kind == "rig":
        return "".join(f'<svg id="{ident}-{i}" style="position:absolute;left:{x + i * 250}px;top:{y}px" width="220" height="260" viewBox="0 0 220 260"><rect width="220" height="260" rx="14" fill="#1A2238"/>'
                       + "".join(f'<circle cx="{60 + (k % 2) * 100}" cy="{70 + (k // 2) * 120}" r="42" fill="#0C1120" stroke="#2F3D60" stroke-width="6"/><path d="M{60 + (k % 2) * 100} {70 + (k // 2) * 120} l30 -12 M{60 + (k % 2) * 100} {70 + (k // 2) * 120} l-30 12" stroke="#3E5080" stroke-width="8"/>' for k in range(4))
                       + '</svg>' for i in range(o.get("n", 3)))
    if kind == "arrow":
        L = o.get("len", 500)
        return (f'<svg id="{ident}" style="{pos};overflow:visible" width="{L}" height="80" viewBox="0 0 {L} 80"><line id="{ident}-ln" x1="0" y1="40" x2="{L - 50}" y2="40" stroke="{o.get("col", K["red"])}" stroke-width="18" stroke-linecap="round"/>'
                f'<path d="M{L - 70} 0 L{L} 40 L{L - 70} 80 Z" fill="{o.get("col", K["red"])}"/></svg>')
    if kind == "stamp":
        col = o.get("col", K["red"])
        return (f'<div id="{ident}" style="{pos};padding:18px 40px;border:10px solid {col};border-radius:16px;font-weight:900;font-size:{o.get("fs", 90)}px;color:{col};'
                f'letter-spacing:.06em;transform:rotate({o.get("rot", -10)}deg);text-transform:uppercase;background:rgba(0,0,0,.35)">{o.get("t", "")}</div>')
    if kind == "stop":
        return (f'<svg id="{ident}" style="{pos};overflow:visible" width="{460 * s:.0f}" height="{460 * s:.0f}" viewBox="0 0 460 460"><path d="M135 10 L325 10 L450 135 L450 325 L325 450 L135 450 L10 325 L10 135 Z" fill="{K["red"]}" stroke="#fff" stroke-width="16"/>'
                f'<text x="230" y="{262 + (0 if len(o.get("t", "HALT")) < 6 else 0)}" text-anchor="middle" font-family="Inter" font-weight="900" font-size="{o.get("fs", 110)}" fill="#fff">{o.get("t", "HALT")}</text></svg>')
    if kind == "planet":
        col = o.get("col", "#627EEA")
        return (f'<div id="{ident}" style="{pos};width:{230 * s:.0f}px;height:{230 * s:.0f}px;border-radius:50%;background:radial-gradient(circle at 35% 30%,{col},#0A0F1E 85%);'
                f'border:4px solid {col};display:flex;align-items:center;justify-content:center;font-weight:900;font-size:{38 * s:.0f}px;color:#fff;text-align:center">{o.get("label", "")}</div>')
    if kind == "proof":
        return (f'<div id="{ident}" style="{pos};width:{o.get("w", 520)}px;padding:34px;border-radius:20px;background:#EDEFF4;color:#141A2A;font-weight:800;font-size:34px;box-shadow:0 20px 0 rgba(0,0,0,.35)">'
                f'<div style="font-weight:900;font-size:44px;margin-bottom:18px">{o.get("title", "PROOF")}</div>'
                + "".join(f'<div style="height:18px;border-radius:9px;background:#C4CAD8;margin:14px 0;width:{90 - k * 13}%"></div>' for k in range(4))
                + f'<div style="margin-top:14px;font-size:30px;color:#58617A">{o.get("sub", "")}</div></div>')
    if kind == "redwash":
        return f'<div id="{ident}" style="position:absolute;left:-200px;top:-200px;width:{W + 400}px;height:{H + 400}px;background:rgba(255,40,30,.32);opacity:0"></div>'
    if kind == "ice":
        return f'<div id="{ident}" style="position:absolute;left:-200px;top:-200px;width:{W + 400}px;height:{H + 400}px;background:rgba(120,200,255,.22);opacity:0"></div>'
    if kind == "bridgedeck":
        return (f'<div id="{ident}" style="position:absolute;left:300px;top:{y}px;width:{W - 600}px;height:30px;background:{K["bnb"]};opacity:.85"></div>'
                + "".join(f'<div style="position:absolute;left:{300 + i * 80}px;top:{y + 30}px;width:8px;height:120px;background:{K["bnb"]};opacity:.5"></div>' for i in range(7)))
    return _prop0(kind, ident, x, y, s, o)


longnight.bg_svg = bg_svg
longnight.prop = heist_prop


class HEp(Ep):
    def build(self, n, f):
        f = dict(f)
        f.setdefault("base", 1.0)
        f.setdefault("zoom", 1.05)
        return super().build(n, f)

    def action(self, p, n, d, cue, f, w, act, arg=None):
        t = cue(w) if isinstance(w, str) else float(w)
        if act == "count":
            ident, v, dur, v0 = arg + (0,) * (4 - len(arg))
            return [f'tl.fromTo("#{p}-{ident}-n",{{textContent:{v0}}},{{textContent:{v},duration:{dur},ease:"power2.out",snap:{{textContent:1}}}},{t:.2f});']
        if act == "fly":
            ident, dx, dy = arg
            return [f'tl.to("#{p}-{ident}",{{x:{dx},y:{dy},duration:.9,ease:"power3.in"}},{t:.2f});']
        if act == "flyall":
            cls, dx, dy = arg
            return [f'tl.to(".{p}-{cls}",{{x:{dx},y:{dy},opacity:0,duration:.8,ease:"power3.in",stagger:.05}},{t:.2f});']
        if act == "popall":
            return [f'tl.fromTo(".{p}-{arg}",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.35,ease:"back.out(2.5)",stagger:.08}},{t:.2f});']
        if act == "type":
            return [f'tl.fromTo(".{p}-{arg}-ln",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:.2,stagger:.35}},{t:.2f});']
        if act == "alarm":
            return [f'tl.to("#{p}-{arg}",{{opacity:{1 if i % 2 == 0 else 0},duration:.18}},{t + i * .36:.2f});' for i in range(8)]
        if act == "freeze":
            return [f'tl.to("#{p}-{arg}",{{opacity:1,duration:.5}},{t:.2f});']
        if act == "redden":
            return [f'tl.to("#{p}-{arg}",{{fill:"{K["red"]}",duration:.25}},{t:.2f});']
        if act == "reddenall":
            return [f'tl.to(".{p}-{arg}",{{filter:"sepia(1) saturate(6) hue-rotate(-50deg)",duration:.2,stagger:.12}},{t:.2f});']
        if act == "glitch":
            return [f'tl.to("#{p}-{arg}",{{x:{dx},opacity:{op},duration:.05}},{t + i * .06:.2f});' for i, (dx, op) in enumerate([(14, .6), (-12, 1), (8, .4), (-6, 1), (0, 1)])]
        if act == "stamp":
            return [f'tl.fromTo("#{p}-{arg}",{{scale:2.4,opacity:0}},{{scale:1,opacity:1,duration:.3,ease:"power4.in"}},{t:.2f});', shake(f"#{p}-cam", t + .3, 10)]
        if act == "draw":
            return [f'tl.fromTo("#{p}-{arg}",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.6,ease:"power2.out"}},{t:.2f});']
        if act == "chainin":
            return [f'tl.fromTo(".{p}-{arg}-b",{{y:-80,opacity:0}},{{y:0,opacity:1,duration:.3,ease:"back.out(2)",stagger:.25}},{t:.2f});',
                    f'tl.fromTo(".{p}-{arg}-l",{{opacity:0}},{{opacity:1,duration:.2,stagger:.25}},{t + .2:.2f});']
        if act == "rewind":
            return [f'tl.to(".{p}-{arg}-b",{{rotation:-8,duration:.12,yoyo:true,repeat:5}},{t:.2f});', f'tl.to("#{p}-{arg}-4",{{opacity:.2,y:60,duration:.5}},{t + .3:.2f});',
                    f'tl.to("#{p}-{arg}-l3",{{opacity:0,duration:.3}},{t + .3:.2f});']
        if act == "blink":
            return [f'tl.to(".{p}-led",{{opacity:{.2 if i % 2 == 0 else 1},duration:.12}},{t + i * .24:.2f});' for i in range(int(max(2, (d - t) / .24)))]
        if act == "zoomin":
            return [f'tl.to("#{p}-cam",{{scale:{arg or 1.3},duration:.8,ease:"power2.inOut"}},{t:.2f});']
        if act == "dimout":
            return [f'tl.to("#{p}-{arg}",{{opacity:.15,duration:.4}},{t:.2f});']
        return super().action(p, n, d, cue, f, w, act, arg)
