"""Shared helpers for hand-built HyperFrames frames (orchestrator-authored)."""
import json, os, re

GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>'
FONTS = "\n".join(
    f"@font-face{{font-family:'Inter';src:url('assets/fonts/Inter-{n}.otf') format('opentype');font-weight:{w};font-style:normal;}}"
    for n, w in [("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700), ("ExtraBold", 800), ("Black", 900)])


class Project:
    def __init__(self, root):
        self.root = root
        self.out = os.path.join(root, "compositions", "frames")
        os.makedirs(self.out, exist_ok=True)
        sb = open(os.path.join(root, "STORYBOARD.md")).read()
        m = re.search(r"format: (\d+)x(\d+)", sb)
        self.w, self.h = (int(m.group(1)), int(m.group(2))) if m else (1920, 1080)
        self.frames = {int(n): (slug, float(d)) for n, d, slug in
                       re.findall(r"## Frame (\d+) .*?- duration: ([\d.]+)s.*?- src: compositions/frames/\d+-([a-z0-9-]+)\.html", sb, re.S)}
        meta = json.load(open(os.path.join(root, "audio_meta.json")))
        self.words = {v["frame"]: v["words"] for v in meta["voices"]}

    def dur(self, n):
        return self.frames[n][1]

    def cue(self, n, word, nth=1, frac=0.5):
        k = 0
        w0 = re.sub(r"[^a-z0-9$%]", "", word.lower())
        for w in self.words.get(n, []):
            if re.sub(r"[^a-z0-9$%]", "", w["text"].lower()).startswith(w0):
                k += 1
                if k == nth:
                    return round(w["start"], 2)
        return round(frac * self.dur(n), 2)

    def write(self, n, css, html, js, bg_html="", bg_js=""):
        slug, d = self.frames[n]
        fid = f"{n:02d}-{slug}"
        p = f"f{n:02d}"
        doc = f"""<template>
<style>{FONTS}
#root{{position:absolute;inset:0;width:{self.w}px;height:{self.h}px;overflow:hidden;font-family:'Inter',sans-serif;}}
{css}</style>
<div id="root" data-composition-id="{fid}" data-width="{self.w}" data-height="{self.h}">
<div class="clip" id="{p}-bg" data-start="0" data-duration="{d}" data-track-index="0" style="position:absolute;inset:0;overflow:hidden">{bg_html}</div>
<div class="clip" id="{p}-stage" data-start="0" data-duration="{d}" data-track-index="1" style="position:absolute;inset:0">{html}</div>
</div>
{GSAP}
<script>
(function(){{
const tl = gsap.timeline({{ paused: true }});
{bg_js}
{chr(10).join(js)}
window.__timelines = window.__timelines || {{}};
window.__timelines["{fid}"] = tl;
}})();
</script>
</template>
"""
        open(os.path.join(self.out, fid + ".html"), "w").write(doc)


# ---------- motion ----------
def pop(sel, t, s0=.5, d=.45):
    return f'tl.fromTo("{sel}",{{scale:{s0},opacity:0}},{{scale:1,opacity:1,duration:{d},ease:"back.out(2)"}},{t:.2f});'


def rise(sel, t, dy=40):
    return f'tl.fromTo("{sel}",{{y:{dy},opacity:0}},{{y:0,opacity:1,duration:.55,ease:"power3.out"}},{t:.2f});'


def slide(sel, t, dx=-60):
    return f'tl.fromTo("{sel}",{{x:{dx},opacity:0}},{{x:0,opacity:1,duration:.55,ease:"power3.out"}},{t:.2f});'


def fade(sel, t, d=.5, to=1):
    return f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:{to},duration:{d}}},{t:.2f});'


def draw(sel, t, d=1.0, length=2000, ease="power2.inOut"):
    return f'tl.fromTo("{sel}",{{strokeDasharray:{length},strokeDashoffset:{length}}},{{strokeDashoffset:0,duration:{d},ease:"{ease}"}},{t:.2f});'


def stamp(sel, t, rot=-10):
    return f'tl.fromTo("{sel}",{{scale:2.6,opacity:0,rotation:{rot}}},{{scale:1,opacity:1,rotation:{rot},duration:.32,ease:"power4.in"}},{t:.2f});'


def shake(sel, t, amp=10):
    return "".join(f'tl.to("{sel}",{{x:{dx},duration:.05}},{t + i*0.05:.2f});' for i, dx in enumerate([amp, -amp, amp*.7, -amp*.7, 0]))


def push(sel, d, s1=1.08, x=0, y=0):
    """slow camera push-in over the whole frame"""
    return f'tl.fromTo("{sel}",{{scale:1,x:0,y:0}},{{scale:{s1},x:{x},y:{y},duration:{d:.2f},ease:"none"}},0);'


def bob(sel, start, end, amp=8, period=1.6):
    js, t, up = [], start, True
    while t < end - 0.05:
        dur = min(period / 2, end - t)
        js.append(f'tl.to("{sel}",{{y:{-amp if up else 0},duration:{dur:.3f},ease:"sine.inOut"}},{t:.3f});')
        t += dur
        up = not up
    return "".join(js)


def pixel(m, pal, size, cls="", ident=""):
    h, w = len(m), max(len(r) for r in m)
    rects = "".join(f'<rect x="{x}" y="{y}" width="1.02" height="1.02" fill="{pal[ch]}"/>'
                    for y, row in enumerate(m) for x, ch in enumerate(row) if ch in pal)
    idattr = f' id="{ident}"' if ident else ""
    return (f'<svg{idattr} class="{cls}" viewBox="0 0 {w} {h}" width="{size}" height="{size*h/w:.0f}" '
            f'shape-rendering="crispEdges">{rects}</svg>')
