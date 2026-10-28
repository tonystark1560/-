"""Rules of the Long Night — vertical (1080x1920) dark flat-illustration scene kit.

A frame spec is a dict:
  bg: yard | cabin | forest | ruth | river | aurora | airstrip | sunset | black | trail
  loc: HUD location line
  counters: {"MATCHES": 23, ...}  (episode carries them; per-frame overrides)
  light: (cx, cy, r) darkness hole around a light source, or None for no darkness
  glow: "warm" | "red" | "white" | "green" | "fire" color of the light pool
  actors: [("cole"|"ruth"|"bear", x, y, scale, {opts})]
  dimmers: [(x, y, scale)]
  props: [(kind, x, y, scale, {opts})]
  card: (big text html, cue)  — centered title card
  tags: [(text, cue, color)]
  bubbles: [(text, x, y, cue)]
  ev: [(cue, action, arg)]  actions: flicker, grow, shrink, lean, retreat, flare, fire, shake, counter, bark, burn,
                            darkout, show, pop, beam_dim, sun, aurora, town_out, wall_split, candle_out, step
"""
import sys
sys.path.insert(0, "/home/user/-/videos/_tools")
from hf import pop, rise, fade, shake, push, bob

W, H = 1080, 1920
GROUND = 1240
C = dict(ink="#05070C", snow="#9FB0C6", snow2="#7E8EA6", sky1="#070B14", sky2="#141C2E", pine="#0B111C", wood="#2A1D14",
         wood2="#3A2A1D", warm="#FFB347", red="#FF3B30", white="#E8F1FF", green="#3CF2A0", gold="#FFC83D", coat="#55704A",
         hat="#6B4A2E", skin="#E9B48A", beard="#4A3424", rcoat="#B8342E", hair="#C9C9CF", husky="#8E99A8", text="#F2F4F8",
         gray="#8A93A3")

CSS = f"""
.hud-loc{{position:absolute;left:0;right:0;top:70px;text-align:center;font-weight:800;font-size:30px;letter-spacing:.22em;color:{C['gray']};text-transform:uppercase;}}
.hud-row{{position:absolute;left:0;right:0;top:122px;display:flex;justify-content:center;gap:16px;}}
.ctr{{display:flex;align-items:center;gap:10px;padding:10px 18px;border-radius:10px;background:rgba(10,14,22,.78);border:2px solid rgba(255,255,255,.12);font-weight:900;font-size:28px;letter-spacing:.08em;color:{C['text']};}}
.ctr b{{color:{C['gold']};}}
.tag{{position:absolute;left:50%;padding:12px 26px;border-radius:10px;font-weight:900;font-size:36px;letter-spacing:.06em;text-transform:uppercase;color:#fff;background:{C['red']};white-space:nowrap;box-shadow:0 8px 0 rgba(0,0,0,.35);}}
.tag.gold{{background:{C['gold']};color:#111;}} .tag.white{{background:#fff;color:#111;}} .tag.green{{background:{C['green']};color:#062;}}
.card{{position:absolute;left:70px;right:70px;padding:50px 40px;border-radius:24px;background:rgba(8,11,18,.92);border:3px solid rgba(255,255,255,.14);text-align:center;font-weight:900;font-size:72px;line-height:1.05;color:#fff;text-transform:uppercase;}}
.card em{{font-style:normal;color:{C['gold']};}} .card i{{font-style:normal;color:{C['red']};}}
.bub{{position:absolute;padding:14px 26px;border-radius:26px;background:#fff;font-weight:900;font-size:40px;color:#111;text-transform:uppercase;white-space:nowrap;box-shadow:0 8px 0 rgba(0,0,0,.35);}}
.dark{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(4,6,11,0) 42%,rgba(4,6,11,.55) 62%,rgba(4,6,11,.93) 74%);box-shadow:0 0 0 3000px rgba(4,6,11,.93);}}
.pool{{position:absolute;border-radius:50%;}}
.dim{{position:absolute;filter:blur(1.5px);transform-origin:50% 100%;}}
"""

POOL = {"warm": "rgba(255,170,70,.42)", "red": "rgba(255,50,40,.5)", "white": "rgba(220,235,255,.38)", "green": "rgba(60,242,160,.30)", "fire": "rgba(255,120,30,.55)"}


# ---------------- backgrounds ----------------
def pines(xs, base, h, color, w=150):
    out = []
    for i, x in enumerate(xs):
        hh = h * (0.8 + 0.25 * ((i * 37) % 5) / 4)
        out.append(f'<path d="M{x} {base - hh} L{x - w/2:.0f} {base} L{x + w/2:.0f} {base} Z" fill="{color}"/>'
                   f'<path d="M{x} {base - hh*1.25:.0f} L{x - w/3:.0f} {base - hh*0.45:.0f} L{x + w/3:.0f} {base - hh*0.45:.0f} Z" fill="{color}"/>')
    return "".join(out)


def stars(n=70, maxy=900):
    return "".join(f'<circle cx="{(i*373) % W}" cy="{(i*211) % maxy + 20}" r="{1.4 + (i % 3)*.8:.1f}" fill="#fff" opacity="{.35 + (i % 5)*.12:.2f}"/>' for i in range(n))


def sky(top=C["sky1"], bot=C["sky2"]):
    return f'<defs><linearGradient id="skyg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bot}"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#skyg)"/>'


def snow_ground(y=GROUND, c1=C["snow"], c2=C["snow2"]):
    return (f'<path d="M0 {y} Q 300 {y-40} 560 {y} T {W} {y-20} L{W} {H} L0 {H} Z" fill="{c2}"/>'
            f'<path d="M0 {y+60} Q 400 {y+20} 760 {y+70} T {W} {y+50} L{W} {H} L0 {H} Z" fill="{c1}"/>')


def cabin_ext(x, y, s=1.0, lit=True):
    win = "#FFB347" if lit else "#1A2233"
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M0 120 L190 0 L380 120 Z" fill="#2B1E15"/><path d="M-10 120 L190 -6 L390 120" stroke="#EEF3FA" stroke-width="16" fill="none"/>'
            f'<rect x="20" y="120" width="340" height="230" fill="{C["wood"]}"/>' + "".join(f'<rect x="20" y="{130+i*36}" width="340" height="6" fill="#1D140E"/>' for i in range(6))
            + f'<rect x="60" y="170" width="90" height="80" fill="{win}"/><rect x="230" y="200" width="80" height="150" fill="#140E09"/><rect x="290" y="40" width="30" height="80" fill="#3A2A1D"/></g>')


def bg_svg(kind, p):
    if kind == "black":
        return f'<svg width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#04060B"/></svg>'
    if kind in ("yard", "forest", "trail"):
        body = sky() + stars() + pines(range(-40, W + 120, 140), GROUND - 60, 360, "#0F1726", 170) + snow_ground()
        if kind == "yard":
            body += cabin_ext(20, GROUND - 400, 1.15)
        else:
            body += pines([-20, 90, 960, 1080], GROUND + 160, 620, C["pine"], 240)
        return f'<svg width="{W}" height="{H}">{body}</svg>'
    if kind == "cabin":
        planks = "".join(f'<rect x="0" y="{i*80}" width="{W}" height="74" fill="{C["wood2"] if i % 2 else C["wood"]}"/>' for i in range(17))
        body = (planks + f'<rect x="120" y="360" width="360" height="300" rx="10" fill="#0D1422" stroke="#1D140E" stroke-width="26"/>' + f'<line x1="300" y1="360" x2="300" y2="660" stroke="#1D140E" stroke-width="16"/>'
                + f'<rect x="0" y="{GROUND}" width="{W}" height="{H-GROUND}" fill="#1E150F"/>'
                + f'<rect x="700" y="{GROUND-330}" width="240" height="330" rx="12" fill="#151515"/><rect x="740" y="{GROUND-230}" width="160" height="110" rx="8" fill="#FF8A2B"/><rect x="790" y="{GROUND-600}" width="50" height="270" fill="#151515"/>')
        return f'<svg width="{W}" height="{H}">{body}</svg>'
    if kind == "ruth":
        planks = "".join(f'<rect x="0" y="{i*80}" width="{W}" height="74" fill="{"#22180F" if i % 2 else "#1A120C"}"/>' for i in range(17))
        body = planks + f'<rect x="580" y="380" width="380" height="300" rx="10" fill="#060A12" stroke="#120C08" stroke-width="26"/><rect x="0" y="{GROUND}" width="{W}" height="{H-GROUND}" fill="#140E0A"/>'
        return f'<svg width="{W}" height="{H}">{body}</svg>'
    if kind == "river":
        body = (sky() + stars() + pines(range(-40, W + 120, 120), GROUND - 160, 300, "#0B1220", 150)
                + f'<path d="M0 {GROUND-160} L{W} {GROUND-160} L{W} {H} L0 {H} Z" fill="#5E7390"/>'
                + f'<path id="{p}-ice" d="M380 {GROUND-160} L700 {GROUND-160} L1000 {H} L80 {H} Z" fill="#B9D3F0" opacity=".85"/>'
                + pines([-40, 60, 1000, 1110], H - 200, 700, C["pine"], 260))
        return f'<svg width="{W}" height="{H}">{body}</svg>'
    if kind == "aurora":
        body = sky("#03070F", "#0B1A22") + stars(90) + snow_ground(GROUND, "#6E8BA0", "#56708A") + pines(range(-40, W + 120, 150), GROUND - 40, 260, "#081018", 160)
        return f'<svg width="{W}" height="{H}">{body}</svg>'
    if kind == "airstrip":
        lights = "".join(f'<circle cx="{120 + i*120}" cy="{GROUND+250}" r="10" fill="#FFD27A"/>' for i in range(8))
        body = (sky() + stars() + snow_ground() + f'<rect x="0" y="{GROUND+200}" width="{W}" height="120" fill="#3B4659"/>' + lights
                + f'<path d="M560 {GROUND-260} Q 800 {GROUND-420} 1040 {GROUND-260} L1040 {GROUND+40} L560 {GROUND+40} Z" fill="#2A3240"/><rect x="680" y="{GROUND-160}" width="240" height="200" fill="#0A0E16"/>'
                + f'<rect x="120" y="{GROUND-500}" width="16" height="520" fill="#2A3240"/><rect x="80" y="{GROUND-520}" width="96" height="40" rx="6" fill="#DDE7F5"/>')
        return f'<svg width="{W}" height="{H}">{body}</svg>'
    if kind == "sunset":
        body = (f'<defs><linearGradient id="ssg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A2140"/><stop offset=".55" stop-color="#7A4A6A"/><stop offset=".72" stop-color="#E8875A"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#ssg)"/>'
                + f'<circle id="{p}-sun" cx="540" cy="{GROUND-120}" r="110" fill="#FFD27A"/>' + pines(range(-40, W + 120, 140), GROUND, 320, "#1A1424", 170) + snow_ground(GROUND + 20, "#C9B6C8", "#A48FA8"))
        return f'<svg width="{W}" height="{H}">{body}</svg>'
    raise ValueError(kind)


# ---------------- characters / props ----------------
def cole(ident, x, y, s=1.0, hold=None, flip=False):
    tr = f"translate({x},{y}) scale({-s if flip else s},{s})" + (" translate(-260,0)" if flip else "")
    extra = ""
    if hold == "lantern":
        extra = f'<g id="{ident}-lamp"><line x1="232" y1="300" x2="232" y2="340" stroke="#222" stroke-width="5"/><rect x="208" y="340" width="48" height="70" rx="10" fill="#2C2C2C"/><ellipse id="{ident}-flame" cx="232" cy="378" rx="14" ry="24" fill="{C["warm"]}"/></g>'
    if hold == "flaregun":
        extra = f'<rect x="210" y="280" width="70" height="26" rx="6" fill="#E85D1F"/><rect x="216" y="300" width="18" height="40" rx="4" fill="#E85D1F"/>'
    if hold == "torch":
        extra = f'<rect x="222" y="200" width="14" height="140" fill="#6B4423"/><path id="{ident}-flame" d="M229 120 C 270 170 255 205 229 215 C 203 205 188 170 229 120 Z" fill="#FF8A2B"/><path d="M229 155 C 248 180 240 200 229 205 C 218 200 210 180 229 155 Z" fill="#FFD27A"/>'
    if hold == "headlamp":
        extra = f'<rect x="140" y="44" width="34" height="22" rx="6" fill="#DDE7F5"/>'
    return (f'<svg id="{ident}" style="position:absolute;left:0;top:0;overflow:visible" width="{W}" height="{H}"><g transform="{tr}">'
            f'<rect x="88" y="420" width="38" height="140" rx="12" fill="#2A2A30"/><rect x="138" y="420" width="38" height="140" rx="12" fill="#2A2A30"/>'
            f'<rect x="80" y="545" width="56" height="26" rx="10" fill="#1A1A1E"/><rect x="132" y="545" width="56" height="26" rx="10" fill="#1A1A1E"/>'
            f'<path d="M70 190 Q 132 160 194 190 L206 440 L58 440 Z" fill="{C["coat"]}"/><rect x="70" y="430" width="136" height="16" fill="#3E5235"/>'
            f'<rect x="186" y="200" width="44" height="130" rx="20" fill="{C["coat"]}" transform="rotate(-12 208 210)"/>'
            f'<circle cx="132" cy="120" r="56" fill="{C["skin"]}"/><path d="M80 130 Q 132 220 184 130 Q 160 170 132 172 Q 104 170 80 130 Z" fill="{C["beard"]}"/>'
            f'<path d="M70 104 Q 132 30 194 104 L194 84 Q 132 10 70 84 Z" fill="{C["hat"]}"/><rect x="66" y="84" width="132" height="30" rx="14" fill="#8A6A48"/>'
            f'<circle cx="112" cy="122" r="6" fill="#111"/><circle cx="152" cy="122" r="6" fill="#111"/>{extra}</g></svg>')


def ruth(ident, x, y, s=1.0, sit=False):
    legs = (f'<rect x="70" y="420" width="140" height="40" rx="18" fill="#2A2A30"/>' if sit else
            f'<rect x="90" y="420" width="34" height="140" rx="12" fill="#2A2A30"/><rect x="136" y="420" width="34" height="140" rx="12" fill="#2A2A30"/>')
    return (f'<svg id="{ident}" style="position:absolute;left:0;top:0;overflow:visible" width="{W}" height="{H}"><g transform="translate({x},{y}) scale({s})">{legs}'
            f'<path d="M74 196 Q 130 166 186 196 L200 440 L60 440 Z" fill="{C["rcoat"]}"/>'
            f'<circle cx="130" cy="124" r="52" fill="{C["skin"]}"/><path d="M76 120 Q 80 60 130 62 Q 182 60 186 120 Q 170 90 130 88 Q 92 90 76 120 Z" fill="{C["hair"]}"/><circle cx="130" cy="56" r="26" fill="{C["hair"]}"/>'
            f'<circle cx="112" cy="128" r="12" fill="none" stroke="#222" stroke-width="4"/><circle cx="148" cy="128" r="12" fill="none" stroke="#222" stroke-width="4"/></g></svg>')


def bear(ident, x, y, s=1.0, flip=False, sit=False):
    tr = f"translate({x},{y}) scale({-s if flip else s},{s})" + (" translate(-320,0)" if flip else "")
    body = (f'<path d="M60 120 Q 160 70 250 110 L262 190 L70 196 Z" fill="{C["husky"]}"/><path d="M80 170 Q 160 210 250 168 L250 196 L80 200 Z" fill="#E6ECF3"/>'
            f'<rect x="84" y="186" width="22" height="70" rx="8" fill="{C["husky"]}"/><rect x="124" y="186" width="22" height="70" rx="8" fill="#E6ECF3"/>'
            f'<rect x="206" y="186" width="22" height="70" rx="8" fill="{C["husky"]}"/><rect x="236" y="186" width="22" height="70" rx="8" fill="#E6ECF3"/>'
            f'<path id="{ident}-tail" d="M64 130 Q 10 90 34 50 Q 56 92 80 120 Z" fill="{C["husky"]}"/>'
            f'<path d="M232 110 Q 250 50 300 60 L330 92 Q 320 120 280 128 Z" fill="{C["husky"]}"/><path d="M290 96 L332 92 Q 326 116 296 120 Z" fill="#E6ECF3"/>'
            f'<path d="M246 64 L254 20 L274 58 Z" fill="{C["husky"]}"/><path d="M270 60 L286 22 L298 64 Z" fill="{C["husky"]}"/><circle cx="292" cy="78" r="6" fill="#111"/><circle cx="330" cy="92" r="7" fill="#111"/>')
    return f'<svg id="{ident}" style="position:absolute;left:0;top:0;overflow:visible" width="{W}" height="{H}"><g transform="{tr}">{body}</g></svg>'


DIMMER = ("M110 0 C140 0 160 40 155 90 C150 130 135 150 140 180 C190 200 205 260 200 340 L215 620 L190 625 L170 380 L160 700 L130 700 L115 420 "
          "L100 700 L70 700 L62 380 L45 625 L20 620 L35 340 C30 260 45 200 90 180 C95 150 70 130 65 90 C60 40 80 0 110 0 Z")


def dimmer(ident, x, y, s=1.0):
    return (f'<svg class="dim" id="{ident}" style="left:{x}px;top:{y}px;overflow:visible" width="{230*s:.0f}" height="{700*s:.0f}" viewBox="0 0 230 700">'
            f'<path d="{DIMMER}" fill="#020306"/><path d="{DIMMER}" fill="none" stroke="rgba(120,140,170,.18)" stroke-width="4"/></svg>')


def prop(kind, ident, x, y, s=1.0, o=None):
    o = o or {}
    if kind == "radio":
        return (f'<svg id="{ident}" style="position:absolute;left:{x}px;top:{y}px;overflow:visible" width="{420*s:.0f}" height="{260*s:.0f}" viewBox="0 0 420 260">'
                f'<rect x="0" y="40" width="420" height="220" rx="24" fill="#3A3A3A"/><circle cx="110" cy="150" r="70" fill="#222"/>' + "".join(f'<circle cx="110" cy="150" r="{r}" fill="none" stroke="#444" stroke-width="5"/>' for r in (20, 40, 60))
                + f'<rect x="220" y="100" width="160" height="50" rx="8" fill="#9BE07A"/><line x1="300" y1="40" x2="380" y2="-60" stroke="#888" stroke-width="8"/>'
                + "".join(f'<path class="{ident}-wave" d="M{390 + i*30} {-40 - i*10} q 20 30 0 60" stroke="#9BE07A" stroke-width="6" fill="none"/>' for i in range(3)) + '</svg>')
    if kind == "tracks":
        pts = o.get("pts", [])
        return "".join(f'<div class="{ident}-tr" id="{ident}-t{i}" style="position:absolute;left:{px}px;top:{py}px;width:26px;height:44px;border-radius:50%;background:#3E4A5E;transform:rotate({a}deg)"></div>' for i, (px, py, a) in enumerate(pts))
    if kind == "candles":
        n = o.get("n", 6)
        import math
        out = []
        for i in range(n):
            a = 2 * math.pi * i / n
            cx, cy = x + 200 * math.cos(a), y + 60 * math.sin(a)
            out.append(f'<div id="{ident}-c{i}" style="position:absolute;left:{cx-12:.0f}px;top:{cy-60:.0f}px;width:24px;height:60px;border-radius:4px;background:#EFE6D2"><div id="{ident}-f{i}" style="position:absolute;left:4px;top:-30px;width:16px;height:28px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:{C["warm"]};box-shadow:0 0 24px {C["warm"]}"></div></div>')
        return "".join(out)
    if kind == "flare":
        return (f'<div id="{ident}" style="position:absolute;left:{x}px;top:{y}px"><div style="width:20px;height:90px;background:#C62828;border-radius:4px"></div>'
                f'<div id="{ident}-fl" style="position:absolute;left:-30px;top:-70px;width:80px;height:80px;border-radius:50%;background:radial-gradient(circle,#fff 0,#FF6A55 35%,rgba(255,59,48,0) 70%)"></div></div>')
    if kind == "generator":
        return (f'<svg id="{ident}" style="position:absolute;left:{x}px;top:{y}px" width="{300*s:.0f}" height="{220*s:.0f}" viewBox="0 0 300 220"><rect x="0" y="40" width="300" height="160" rx="16" fill="#C9A227"/><rect x="30" y="70" width="140" height="100" rx="10" fill="#333"/><circle cx="230" cy="120" r="34" fill="#333"/><rect x="20" y="190" width="40" height="30" fill="#222"/><rect x="240" y="190" width="40" height="30" fill="#222"/></svg>'
                f'<div id="{ident}-drip" style="position:absolute;left:{x+260}px;top:{y+200}px;width:16px;height:22px;border-radius:50% 50% 50% 50%/40% 40% 60% 60%;background:#7FD3FF;opacity:0"></div>')
    if kind == "flood":
        return (f'<svg id="{ident}" style="position:absolute;left:{x}px;top:{y}px" width="120" height="600"><rect x="52" y="60" width="16" height="540" fill="#2A3240"/><rect x="10" y="20" width="100" height="50" rx="8" fill="#DDE7F5"/></svg>')
    if kind == "snowmachine":
        return (f'<svg id="{ident}" style="position:absolute;left:{x}px;top:{y}px;overflow:visible" width="{560*s:.0f}" height="{240*s:.0f}" viewBox="0 0 560 240">'
                f'<rect x="20" y="190" width="380" height="20" rx="10" fill="#222"/><path d="M60 120 L330 110 L400 170 L40 180 Z" fill="#C62828"/><rect x="120" y="80" width="120" height="40" rx="14" fill="#222"/>'
                f'<circle id="{ident}-hl" cx="392" cy="140" r="16" fill="#FFF3C4"/><rect x="420" y="150" width="140" height="50" rx="10" fill="#6B4423"/></svg>')
    if kind == "gauge":
        return (f'<div id="{ident}" style="position:absolute;left:{x}px;top:{y}px;width:420px;height:420px;border-radius:50%;background:#111;border:12px solid #444;display:flex;align-items:center;justify-content:center;flex-direction:column">'
                f'<div style="font-weight:900;font-size:40px;color:{C["gray"]}">{WORDS.get("FUEL", "FUEL")}</div><div id="{ident}-v" style="font-weight:900;font-size:110px;color:{C["red"]}">{o.get("v", "6H")}</div></div>')
    if kind == "watch":
        return (f'<div id="{ident}" style="position:absolute;left:{x}px;top:{y}px;width:460px;height:460px;border-radius:50%;background:#1A1A1A;border:20px solid #7A6A50;display:flex;align-items:center;justify-content:center;flex-direction:column">'
                f'<div style="font-weight:900;font-size:56px;color:{C["gray"]}">{WORDS.get("JAN", "JAN")}</div><div style="font-weight:900;font-size:180px;color:{C["gold"]};line-height:1">21</div></div>')
    if kind == "items":
        its = o.get("items", [])
        return "".join(f'<div class="ctr" id="{ident}-{i}" style="position:absolute;left:{x}px;top:{y + i*130}px;font-size:46px;padding:20px 30px">{t}</div>' for i, t in enumerate(its))
    if kind == "bonfire":
        return (f'<svg id="{ident}" style="position:absolute;left:{x}px;top:{y}px;overflow:visible" width="500" height="700" viewBox="0 0 500 700">'
                f'<path id="{ident}-o" d="M250 0 C 420 220 470 420 400 560 C 360 640 140 640 100 560 C 30 420 80 220 250 0 Z" fill="#FF6A1F"/>'
                f'<path d="M250 180 C 360 320 380 460 330 540 C 300 590 200 590 170 540 C 120 460 140 320 250 180 Z" fill="#FFB347"/>'
                f'<path d="M250 340 C 310 420 320 500 290 540 C 270 565 230 565 210 540 C 180 500 190 420 250 340 Z" fill="#FFE7A0"/></svg>')
    if kind == "townlights":
        return "".join(f'<div class="{ident}-l" id="{ident}-{i}" style="position:absolute;left:{x + i*70}px;top:{y + (i % 3)*14}px;width:22px;height:22px;border-radius:50%;background:#FFD27A;box-shadow:0 0 22px #FFD27A"></div>' for i in range(10))
    if kind == "moon":
        return f'<div id="{ident}" style="position:absolute;left:{x}px;top:{y}px;width:170px;height:170px;border-radius:50%;background:#F4F1DE;box-shadow:0 0 90px rgba(244,241,222,.7)"></div>'
    if kind == "auroraband":
        return (f'<svg id="{ident}" style="position:absolute;left:0;top:{y}px;overflow:visible" width="{W}" height="800">'
                + "".join(f'<path d="M-100 {300 + i*90} C 200 {120 + i*80} 500 {420 + i*60} 1200 {160 + i*90}" stroke="rgba(60,242,160,{.55 - i*.12:.2f})" stroke-width="{120 - i*25}" fill="none" style="filter:blur(18px)"/>' for i in range(4)) + '</svg>')
    if kind == "sunline":
        return f'<div id="{ident}" style="position:absolute;left:-200px;right:-200px;top:{y}px;height:40px;border-radius:50%;background:#FFD27A;box-shadow:0 0 120px 60px rgba(255,190,90,.65)"></div>'
    if kind == "match":
        return (f'<div id="{ident}" style="position:absolute;left:{x}px;top:{y}px"><div style="width:22px;height:300px;background:#D9B27C;border-radius:6px"></div>'
                f'<div style="position:absolute;left:-6px;top:-30px;width:34px;height:44px;border-radius:50%;background:#7A1E14"></div>'
                f'<div id="{ident}-fl" style="position:absolute;left:-34px;top:-130px;width:90px;height:130px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:radial-gradient(circle at 50% 70%,#FFF3C4 0,#FFB347 40%,rgba(255,120,30,0) 75%)"></div></div>')
    if kind == "wall":
        return (f'<div id="{ident}-a" style="position:absolute;left:{x}px;top:{y}px;width:{W//2}px;height:260px;background:#020306;filter:blur(6px);border-radius:40px"></div>'
                f'<div id="{ident}-b" style="position:absolute;left:{x + W//2}px;top:{y}px;width:{W//2}px;height:260px;background:#020306;filter:blur(6px);border-radius:40px"></div>')
    raise ValueError(kind)


LABELS, WORDS = {}, {}


# ---------------- frame builder ----------------
class Ep:
    def __init__(self, P, counters):
        self.P, self.counters = P, dict(counters)

    def build(self, n, f):
        P = self.P
        p = f"f{n:02d}"
        d = P.dur(n)
        cue = lambda w, nth=1, frac=.5: P.cue(n, w, nth, frac)
        js, cam = [], []
        cam.append(f'<div style="position:absolute;inset:0">{bg_svg(f.get("bg", "yard"), p)}</div>')
        light = f.get("light")
        glow = f.get("glow", "warm")
        if light:
            cx, cy, r = light
            cam.append(f'<div class="pool" id="{p}-pool" style="left:{cx-r*1.1:.0f}px;top:{cy-r*1.1:.0f}px;width:{r*2.2:.0f}px;height:{r*2.2:.0f}px;background:radial-gradient(circle,{POOL[glow]},rgba(0,0,0,0) 70%)"></div>')
        for k, (kind, x, y, s, o) in enumerate(f.get("props", [])):
            cam.append(prop(kind, f"{p}-{o.get('id', kind + str(k))}", x, y, s, o))
        for i, (x, y, s) in enumerate(f.get("dimmers", [])):
            cam.append(dimmer(f"{p}-d{i}", x, y, s))
        for (kind, x, y, s, o) in f.get("actors", []):
            ident = f"{p}-{o.get('id', kind)}"
            if kind == "cole":
                cam.append(cole(ident, x, y, s, o.get("hold"), o.get("flip", False)))
            elif kind == "ruth":
                cam.append(ruth(ident, x, y, s, o.get("sit", False)))
            elif kind == "bear":
                cam.append(bear(ident, x, y, s, o.get("flip", False)))
        if light:
            cx, cy, r = light
            cam.append(f'<div class="dark" id="{p}-dark" style="left:{cx-r}px;top:{cy-r}px;width:{2*r}px;height:{2*r}px"></div>')
        for k, (kind, x, y, s, o) in enumerate(f.get("over", [])):
            cam.append(prop(kind, f"{p}-{o.get('id', kind + str(k))}", x, y, s, o))
        hud = []
        if f.get("loc"):
            hud.append(f'<div class="hud-loc" id="{p}-loc">{f["loc"]}</div>')
        ctr = dict(self.counters)
        ctr.update(f.get("counters", {}))
        if ctr and not f.get("nohud"):
            hud.append('<div class="hud-row">' + "".join(f'<div class="ctr" id="{p}-c-{k}">{LABELS.get(k, k)} <b id="{p}-cv-{k}">{v}</b></div>' for k, v in ctr.items()) + '</div>')
        for i, (text, w, col) in enumerate(f.get("tags", [])):
            hud.append(f'<div class="tag {col}" id="{p}-tag{i}" style="top:{230 + i*90}px">{text}</div>')
            js.append(f'tl.fromTo("#{p}-tag{i}",{{scale:.4,opacity:0,xPercent:-50,x:0}},{{scale:1,opacity:1,xPercent:-50,duration:.35,ease:"back.out(2.5)"}},{cue(w):.2f});')
        if f.get("card"):
            text, w, top = f["card"] + ((520,) if len(f["card"]) == 2 else ())
            hud.append(f'<div class="card" id="{p}-card" style="top:{top}px">{text}</div>')
            js.append(f'tl.fromTo("#{p}-card",{{scale:.7,opacity:0}},{{scale:1,opacity:1,duration:.45,ease:"back.out(2)"}},{cue(w):.2f});')
        for i, (text, x, y, w) in enumerate(f.get("bubbles", [])):
            hud.append(f'<div class="bub" id="{p}-b{i}" style="left:{x}px;top:{y}px">{text}</div>')
            js.append(pop(f"#{p}-b{i}", cue(w)))
        # ambient
        z0 = f.get("base", 1.22)
        js.append(f'tl.fromTo("#{p}-cam",{{scale:{z0}}},{{scale:{z0 * f.get("zoom", 1.06):.3f},duration:{d:.2f},ease:"none"}},0);')
        for i in range(len(f.get("dimmers", []))):
            js.append(f'tl.fromTo("#{p}-d{i}",{{rotation:-2}},{{rotation:2,duration:{d/2:.2f},ease:"sine.inOut"}},0);tl.to("#{p}-d{i}",{{rotation:-1,duration:{d/2:.2f},ease:"sine.inOut"}},{d/2:.2f});')
        if light:
            js.append(f'tl.fromTo("#{p}-pool",{{opacity:.85}},{{opacity:1,duration:{d:.2f},ease:"none"}},0);')
        for ev in f.get("ev", []):
            js += self.action(p, n, d, cue, f, *ev)
        P.write(n, CSS, f'<div class="cam" id="{p}-cam" style="position:absolute;inset:0;transform-origin:50% 18%">{"".join(cam)}</div>{"".join(hud)}', js)

    def action(self, p, n, d, cue, f, w, act, arg=None):
        t = cue(w) if isinstance(w, str) else float(w)
        dk = f"#{p}-dark"
        if act == "flicker":
            seq = [.82, 1.0, .7, .95, .78, 1.0]
            out = [f'tl.to("{dk}",{{scale:{v},duration:.07}},{t + i*.08:.2f});' for i, v in enumerate(seq)]
            out += [f'tl.to("#{p}-pool",{{opacity:{.4 if i % 2 == 0 else 1},duration:.07}},{t + i*.08:.2f});' for i in range(len(f.get("dimmers", [])))]
            return out
        if act == "grow":
            return [f'tl.to("{dk}",{{scale:{arg or 1.5},duration:.5,ease:"power2.out"}},{t:.2f});', f'tl.to("#{p}-pool",{{scale:{arg or 1.5},duration:.5}},{t:.2f});']
        if act == "shrink":
            return [f'tl.to("{dk}",{{scale:{arg or .6},duration:{f.get("shrink_d", 1.2)},ease:"power2.in"}},{t:.2f});', f'tl.to("#{p}-pool",{{scale:{arg or .6},duration:1.2}},{t:.2f});']
        if act == "darkout":
            return [f'tl.to("{dk}",{{scale:.02,duration:.25,ease:"power4.in"}},{t:.2f});', f'tl.to("#{p}-pool",{{opacity:0,duration:.25}},{t:.2f});']
        if act == "lean":
            return [f'tl.to(".dim",{{x:"+={arg or 0}",scaleY:1.06,duration:1.4,ease:"sine.inOut"}},{t:.2f});'] if False else [
                f'tl.to("#{p}-d{i}",{{x:{(arg or 60) * (1 if i % 2 == 0 else -1)},duration:1.4,ease:"sine.inOut"}},{t + i*.1:.2f});' for i in range(len(f.get("dimmers", [])))]
        if act == "retreat":
            return [f'tl.to("#{p}-d{i}",{{x:{-500 if i % 2 == 0 else 500},opacity:0,duration:.45,ease:"power3.in"}},{t:.2f});' for i in range(len(f.get("dimmers", [])))]
        if act == "burn":
            return [f'tl.to("#{p}-d{i}",{{opacity:0,scaleY:.2,filter:"blur(12px)",duration:1.2,ease:"power2.in"}},{t + i*.12:.2f});' for i in range(len(f.get("dimmers", [])))]
        if act == "flare":
            return [f'tl.to("#{p}-pool",{{background:"radial-gradient(circle,{POOL["red"]},rgba(0,0,0,0) 70%)",scale:1.6,duration:.3}},{t:.2f});',
                    f'tl.to("{dk}",{{scale:{arg or 1.7},duration:.35,ease:"power3.out"}},{t:.2f});', shake(f"#{p}-cam", t, 14)]
        if act == "fire":
            return [f'tl.to("#{p}-pool",{{background:"radial-gradient(circle,{POOL["fire"]},rgba(0,0,0,0) 70%)",scale:{arg or 1.8},duration:.5}},{t:.2f});',
                    f'tl.to("{dk}",{{scale:{arg or 1.8},duration:.6,ease:"power3.out"}},{t:.2f});']
        if act == "white":
            return [f'tl.to("#{p}-pool",{{background:"radial-gradient(circle,{POOL["white"]},rgba(0,0,0,0) 70%)",scale:{arg or 2.2},duration:.2}},{t:.2f});',
                    f'tl.to("{dk}",{{scale:{arg or 2.4},duration:.25,ease:"power4.out"}},{t:.2f});']
        if act == "shake":
            return [shake(f"#{p}-cam", t, arg or 14)]
        if act == "counter":
            k, v = arg
            return [f'tl.to("#{p}-cv-{k}",{{color:"#FF3B30",duration:.05}},{t:.2f});', f'tl.set("#{p}-cv-{k}",{{textContent:"{v}"}},{t:.2f});',
                    f'tl.fromTo("#{p}-c-{k}",{{scale:1.3}},{{scale:1,duration:.4,ease:"back.out(3)"}},{t:.2f});']
        if act == "show":
            return [f'tl.fromTo("#{p}-{arg}",{{opacity:0}},{{opacity:1,duration:.4}},{t:.2f});']
        if act == "pop":
            return [pop(f"#{p}-{arg}", t)]
        if act == "hide":
            return [f'tl.to("#{p}-{arg}",{{opacity:0,duration:.3}},{t:.2f});']
        if act == "slide":
            ident, dx = arg
            return [f'tl.to("#{p}-{ident}",{{x:{dx},duration:{f.get("slide_d", 1.6)},ease:"power1.inOut"}},{t:.2f});']
        if act == "bob":
            return [bob(f"#{p}-{arg}", t, d, 10, .5)]
        if act == "wag":
            return [f'tl.to("#{p}-bear-tail",{{rotation:{12 if i % 2 else -12},svgOrigin:"70 120",duration:.18}},{t + i*.18:.2f});' for i in range(12)]
        if act == "tracks":
            return [f'tl.fromTo(".{p}-{arg}-tr",{{opacity:0}},{{opacity:1,duration:.15,stagger:.22}},{t:.2f});']
        if act == "candle_out":
            return [f'tl.to("#{p}-{arg}",{{skewX:35,x:14,duration:.5}},{t:.2f});'] if False else [f'tl.to("#{p}-{arg}",{{opacity:0,scale:.2,duration:.35}},{t:.2f});']
        if act == "bend":
            return [f'tl.to("#{p}-{arg}",{{skewX:-35,x:-10,duration:.6,ease:"sine.inOut"}},{t:.2f});']
        if act == "town_out":
            return [f'tl.to("#{p}-{arg}-{9 - i}",{{opacity:0,duration:.1}},{t + i*.28:.2f});' for i in range(10)]
        if act == "wall_split":
            return [f'tl.to("#{p}-{arg}-a",{{x:-700,duration:.6,ease:"power3.in"}},{t:.2f});', f'tl.to("#{p}-{arg}-b",{{x:700,duration:.6,ease:"power3.in"}},{t:.2f});']
        if act == "step":
            return [f'tl.fromTo("#{p}-{arg}",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.15}},{t:.2f});']
        if act == "sun_set":
            return [f'tl.to("#{p}-sun",{{attr:{{cy:{GROUND + 200}}},duration:{max(1.5, d - t - .5):.2f},ease:"power1.in"}},{t:.2f});']
        if act == "rise_y":
            ident, dy = arg
            return [f'tl.to("#{p}-{ident}",{{y:{dy},duration:1.6,ease:"power2.out"}},{t:.2f});']
        if act == "drip":
            return [f'tl.fromTo("#{p}-{arg}-drip",{{opacity:1,y:0}},{{opacity:0,y:70,duration:.6,ease:"power2.in"}},{t + i*.7:.2f});' for i in range(int(max(1, (d - t) / .7)))]
        if act == "beam_dim":
            return [f'tl.to("#{p}-pool",{{opacity:.25,scale:.55,duration:2.2,ease:"power1.in"}},{t:.2f});', f'tl.to("{dk}",{{scale:.55,duration:2.2,ease:"power1.in"}},{t:.2f});']
        if act == "hl_dim":
            return [f'tl.to("#{p}-{arg}-hl",{{opacity:.15,duration:.08}},{t + i*.16:.2f});tl.to("#{p}-{arg}-hl",{{opacity:1,duration:.08}},{t + i*.16 + .08:.2f});' for i in range(5)]
        if act == "wave_stop":
            return [f'tl.to(".{p}-{arg}-wave",{{opacity:0,duration:.2}},{t:.2f});']
        raise ValueError(act)
