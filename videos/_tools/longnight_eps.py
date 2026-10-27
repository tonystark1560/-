"""Frame specs for 'The Dimmers' parts 1–6 (Rules of the Long Night)."""
from longnight import GROUND

G = GROUND


def cole_at(x, s=1.2, hold=None, **o):
    return ("cole", x, G - 570 * s, s, dict(hold=hold, **o))


def ruth_at(x, s=1.15, **o):
    return ("ruth", x, G - 560 * s, s, o)


def bear_at(x, s=1.1, **o):
    return ("bear", x, G - 256 * s + 6, s, o)


def lamp_light(x, s=1.2, r=380):
    return (x + 232 * s, G - 570 * s + 378 * s, r)


EDGE = [(-60, G - 760, 1.0), (840, G - 720, .95)]
EDGE3 = EDGE + [(620, G - 820, .8)]

EPS = {
1: (dict(MATCHES=23, OIL="4L", FLARES=5), [
    dict(bg="yard", loc="Rule 1", actors=[cole_at(330, hold="lantern")], light=lamp_light(330), dimmers=EDGE,
         ev=[("flickers", "flicker"), ("light", "grow", 1.15), ("dark", "lean", 70)], tags=[("No wind", "wind", "")]),
    dict(bg="sunset", loc="Brooks Range, Alaska · Nov 18", nohud=True, tags=[("Sunset 1:42 PM", "sets", "gold"), ("64 days of dark", "sixty", "")],
         ev=[("sets", "sun_set")]),
    dict(bg="cabin", loc="Cabin · Polar night", actors=[cole_at(120, s=1.15), bear_at(560, flip=True)], tags=[("11 polar nights", "eleven", "gold"), ("Bear: afraid of nothing", "husky", "white")]),
    dict(bg="cabin", loc="Cabin · 8:40 PM", props=[("radio", 330, 820, 1.0, dict(id="radio"))],
         tags=[("Kettle Creek: blackout", "kettle", ""), ("Another town: blackout", "another", ""), ("Signal lost", "silent", "white")], ev=[("silent", "wave_stop", "radio")]),
    dict(bg="cabin", loc="Cabin · 9:14 PM", actors=[bear_at(380, s=1.25)], bubbles=[("Grrrr…", 600, 820, "growls")], ev=[("growls", "shake", 8)]),
    dict(bg="yard", loc="Porch · 9:16 PM", actors=[cole_at(330, hold="lantern")], light=lamp_light(330, r=420), tags=[("No wind", "wind", "white")]),
    dict(bg="yard", loc="Porch · 9:17 PM", actors=[cole_at(330, hold="lantern")], light=lamp_light(330, r=420),
         ev=[("once", "flicker"), ("twice", "flicker"), ("bends", "bend", "cole-flame"), ("breathing", "shrink", .8)], tags=[("Flame bends to the dark", "bends", "")]),
    dict(bg="yard", loc="Porch · 9:17 PM", actors=[cole_at(330, hold="lantern")], light=lamp_light(330, r=420), dimmers=EDGE3,
         ev=[("leaning", "lean", 90)], tags=[("Too thick", "thick", "")]),
    dict(bg="yard", loc="Porch · 9:18 PM", actors=[cole_at(330, hold="flaregun"), bear_at(640, flip=True)], light=lamp_light(330, r=380), dimmers=EDGE3,
         bubbles=[("Woof!", 700, 800, "barks")], ev=[("fires", "flare"), ("fires", "counter", ("FLARES", 4))], counters=dict(FLARES=5)),
    dict(bg="yard", loc="Porch · 9:18 PM", actors=[cole_at(330, hold="flaregun")], light=lamp_light(330, r=600), glow="red", dimmers=EDGE3, counters=dict(FLARES=4),
         ev=[("snap", "retreat")]),
    dict(bg="yard", loc="Yard · Morning (still dark)", counters=dict(FLARES=4),
         props=[("tracks", 0, 0, 1, dict(id="tk", pts=[(300 + 330 * __import__('math').cos(a / 6), 1050 + 180 * __import__('math').sin(a / 6), a * 9) for a in range(0, 30, 2)]))],
         ev=[("circle", "tracks", "tk")], tags=[("Tracks stop at the light", "stop", "")]),
    dict(bg="black", loc="Rule 1", counters=dict(FLARES=4), card=("Rule 1:<br><em>They can't cross the light</em>", "rule"), tags=[("Part 2 →", "part", "gold")]),
]),
2: (dict(MATCHES=23, OIL="4L", FLARES=4, BATTERY=2), [
    dict(bg="black", loc="Rule 2", nohud=True, props=[("match", 520, 760, 1, dict(id="m"))], tags=[("Light = ammo", "ammo", "gold")]),
    dict(bg="cabin", loc="Inventory", props=[("items", 300, 560, 1, dict(id="it", items=["Matches · 23", "Lamp oil · 4L", "Flares · 4", "Batteries · 2"]))],
         ev=[("matches", "pop", "it-0"), ("oil", "pop", "it-1"), ("flares", "pop", "it-2"), ("batteries", "pop", "it-3")]),
    dict(bg="forest", loc="Ruth's cabin · 3 miles", props=[], over=[], tags=[("Ruth · retired nurse", "ruth", "white"), ("No smoke · 2 days", "chimney", "")]),
    dict(bg="trail", loc="Creek trail · 10:02 PM", actors=[cole_at(260, hold="headlamp"), bear_at(620)], light=(450, 860, 460), glow="white", tags=[("Bear goes first", "first", "white")], ev=[("first", "bob", "bear")]),
    dict(bg="trail", loc="Creek trail · 10:21 PM", actors=[cole_at(260, hold="headlamp"), bear_at(620)], light=(450, 860, 460), glow="white",
         ev=[("dim", "beam_dim")], counters=dict(BATTERY=2), tags=[("Batteries: new", "new", "white")]),
    dict(bg="black", loc="Rule 2", card=("Rule 2:<br><em>They drink light.</em><br><i>Electric goes first</i>", "rule")),
    dict(bg="ruth", loc="Ruth's cabin · 10:40 PM", actors=[ruth_at(400, sit=True)], props=[("candles", 530, 1150, 1, dict(id="cd", n=8))], light=(530, 1000, 430),
         dimmers=[(640, 360, .55), (780, 380, .5)], ev=[("alive", "pop", "ruth")]),
    dict(bg="ruth", loc="Ruth's cabin · 10:41 PM", actors=[ruth_at(400, sit=True)], props=[("candles", 530, 1150, 1, dict(id="cd", n=8))], light=(530, 1000, 430),
         bubbles=[("3 days…", 640, 760, "three")], tags=[("Don't let them go out", "candles", "")]),
    dict(bg="ruth", loc="Candles left", props=[("candles", 540, 1080, 1, dict(id="cd", n=4))], light=(540, 980, 380), counters=dict(CANDLES=4), tags=[("Each one half gone", "half", "")]),
    dict(bg="ruth", loc="Ruth's cabin · 10:44 PM", actors=[bear_at(600, flip=True)], props=[("candles", 400, 1150, 1, dict(id="cd", n=4))], light=(400, 1020, 400), counters=dict(CANDLES=4),
         bubbles=[("*whine*", 640, 800, "whines")], ev=[("bends", "bend", "cd-f2")]),
    dict(bg="ruth", loc="Ruth's cabin · 10:44 PM", props=[("candles", 540, 1080, 1, dict(id="cd", n=4))], light=(540, 980, 380), counters=dict(CANDLES=4), dimmers=[(780, 640, .8)],
         ev=[("out", "candle_out", "cd-f1"), ("out", "counter", ("CANDLES", 3)), ("out", "shrink", .55), ("out", "lean", -120)]),
]),
3: (dict(FLARES=4, OIL="4L", CANDLES=3), [
    dict(bg="ruth", loc="Ruth's cabin · 10:45 PM", actors=[ruth_at(300, sit=True)], light=(420, 1000, 420), dimmers=[(760, 560, .9)], ev=[("colder", "shrink", .7), ("closer", "lean", -160)]),
    dict(bg="ruth", loc="Ruth's cabin · 10:45 PM", actors=[cole_at(200, hold="torch")], light=(500, 900, 420), dimmers=[(760, 560, .9)], counters=dict(OIL="4L"),
         ev=[("lights", "fire", 2.0), ("lamp", "counter", ("OIL", "3L"))]),
    dict(bg="ruth", loc="Ruth's cabin · 10:46 PM", actors=[cole_at(200, hold="torch")], light=(500, 900, 760), glow="fire", dimmers=[(780, 560, .9)], counters=dict(OIL="3L"),
         ev=[("shrieks", "shake", 18), ("shrieks", "retreat")], tags=[("*SHRIEK*", "shrieks", "")]),
    dict(bg="black", loc="Rule 3", counters=dict(OIL="3L"), card=("Rule 3:<br><em>They hate fire.</em><br><i>Not batteries</i>", "rule")),
    dict(bg="ruth", loc="Ruth's cabin", actors=[ruth_at(160), cole_at(560, hold="torch", flip=True)], counters=dict(OIL="3L"), light=(500, 900, 700), glow="fire",
         bubbles=[("Generator?", 120, 520, "generator"), ("Now.", 640, 520, "now")]),
    dict(bg="trail", loc="Creek trail · 11:10 PM", actors=[ruth_at(160, s=1.0), cole_at(400, s=1.1, hold="torch"), bear_at(700, s=1.0)], light=(560, 900, 520), glow="fire", counters=dict(OIL="3L"),
         ev=[("husky", "bob", "bear")], tags=[("4 flares left", "flares", "gold")]),
    dict(bg="trail", loc="Creek trail · 11:24 PM", actors=[cole_at(300, s=1.1, hold="torch"), bear_at(620, s=1.0)], light=(500, 900, 520), glow="fire", counters=dict(OIL="3L"),
         props=[("wall", 0, 300, 1, dict(id="wl"))], ev=[("wall", "shake", 8)], tags=[("A wall of dark", "wall", "")]),
    dict(bg="trail", loc="Creek trail · 11:24 PM", actors=[cole_at(300, s=1.1, hold="flaregun")], light=(500, 900, 520), glow="fire", counters=dict(OIL="3L"),
         props=[("wall", 0, 300, 1, dict(id="wl"))], ev=[("fires", "flare"), ("fires", "counter", ("FLARES", 3)), ("splits", "wall_split", "wl")]),
    dict(bg="yard", loc="Cole's cabin · 12:02 AM", props=[("generator", 520, 1040, 1, dict(id="gen")), ("flood", 880, 640, 1, dict(id="fl"))], light=(700, 900, 300), glow="white", counters=dict(FLARES=3, OIL="3L"),
         ev=[("snap", "white", 3.2)]),
    dict(bg="yard", loc="Cole's cabin · 12:03 AM", actors=[ruth_at(140)], props=[("generator", 520, 1040, 1, dict(id="gen"))], light=(600, 900, 900), glow="white", counters=dict(FLARES=3, OIL="3L"),
         bubbles=[("Ha!", 160, 560, "laughs")], ev=[("gasoline", "drip", "gen")], tags=[("Fuel leak", "leaking", "")]),
    dict(bg="black", loc="Generator", counters=dict(FLARES=3, OIL="3L"), props=[("gauge", 330, 640, 1, dict(id="g", v="6H"))], ev=[("six", "pop", "g")]),
]),
4: (dict(FLARES=3, CANDLES=3, FUEL="6H"), [
    dict(bg="yard", loc="Cole's cabin · 12:10 AM", props=[("generator", 520, 1040, 1, dict(id="gen")), ("flood", 880, 640, 1, dict(id="fl"))], light=(700, 900, 820), glow="white",
         ev=[("wins", "shrink", .5)], tags=[("6 hours of power", "six", "gold")]),
    dict(bg="cabin", loc="Radio · 12:14 AM", props=[("radio", 330, 820, 1, dict(id="radio"))], tags=[("Kettle Creek airstrip", "kettle", "white"), ("Floodlights + fuel", "floodlights", "gold"), ("Come south", "south", "")]),
    dict(bg="trail", loc="Route · 40 miles south", props=[("snowmachine", 260, 1000, 1, dict(id="sm"))], light=(700, 1130, 300), glow="white", tags=[("40 miles", "forty", ""), ("1 headlight", "headlight", "white")]),
    dict(bg="yard", loc="Loading up", props=[("items", 300, 560, 1, dict(id="it", items=["Candles · 3", "Flares · 3", "Bear · in the sled"]))],
         ev=[("candles", "pop", "it-0"), ("flares", "pop", "it-1"), ("sled", "pop", "it-2")]),
    dict(bg="black", loc="Rule 4", card=("Rule 4:<br><em>Never travel in the dark.</em><br><i>Unless it's coming anyway</i>", "rule")),
    dict(bg="trail", loc="Mile 10", props=[("snowmachine", 260, 1000, 1, dict(id="sm"))], light=(700, 1130, 360), glow="white", ev=[("flicker", "hl_dim", "sm"), ("flicker", "flicker")]),
    dict(bg="trail", loc="Mile 18", props=[("snowmachine", 260, 1000, 1, dict(id="sm")), ("tracks", 0, 0, 1, dict(id="tk", pts=[(860, 1200, 0), (900, 1280, 0), (860, 1360, 0)]))],
         light=(700, 1130, 360), glow="white", ev=[("step", "step", "tk-t0"), (("step"), "shake", 4), ("pushed", "step", "tk-t1")] + [], tags=[("Something is running with us", "alongside", "")]),
    dict(bg="trail", loc="Mile 21", props=[("snowmachine", 260, 1000, 1, dict(id="sm"))], light=(700, 1130, 360), glow="white", ev=[("dies", "darkout"), ("dies", "shake", 10)]),
    dict(bg="black", loc="Mile 21 · No light", bubbles=[("COLE!", 360, 700, "screams")], props=[("flare", 520, 1000, 1, dict(id="fl"))], ev=[("fumbles", "shake", 6)]),
    dict(bg="trail", loc="Mile 21 · No light", props=[("snowmachine", 260, 1000, 1, dict(id="sm"))], light=(520, 1100, 260), glow="red", tags=[("Bear?", "empty", ""), ("Gone into the dark", "gone", "white")]),
]),
5: (dict(FLARES=3, CANDLES=3), [
    dict(bg="trail", loc="Rule 5", actors=[cole_at(330, hold="flaregun")], light=(560, 900, 380), glow="red", card=("Never chase your dog<br><i>into the dark</i>", "never", 300)),
    dict(bg="trail", loc="Mile 21 · Off trail", actors=[cole_at(330, hold="flaregun")], light=(560, 900, 380), glow="red", ev=[("lights", "counter", ("FLARES", 2)), ("lights", "flare", 1.4)], tags=[("20 yards of safety", "twenty", "")]),
    dict(bg="trail", loc="Mile 21 · Off trail", actors=[cole_at(500, hold="flaregun", flip=True)], light=(560, 900, 380), glow="red", counters=dict(FLARES=2), bubbles=[("Woof!", 60, 700, "bark")]),
    dict(bg="trail", loc="Mile 21 · Off trail", actors=[ruth_at(200), cole_at(560, hold="flaregun", flip=True)], light=(560, 900, 440), glow="red", counters=dict(FLARES=2),
         bubbles=[("That's not the way!", 120, 520, "way"), ("Woof!", 60, 380, "again"), ("Woof!", 700, 380, "calling")]),
    dict(bg="river", loc="Frozen river", actors=[cole_at(260, s=.9), ruth_at(420, s=.85)], counters=dict(FLARES=2), ev=[("shining", "show", "moonglow")],
         over=[("moon", 830, 160, 1, dict(id="moonglow"))]),
    dict(bg="river", loc="Frozen river · Moonlight", counters=dict(FLARES=2), over=[("moon", 830, 160, 1, dict(id="mn"))], dimmers=[(-40, 760, .7), (880, 760, .7)], tags=[("Rule 5: they won't cross moonlit ice", "rule", "green")], ev=[("moon", "pop", "mn")]),
    dict(bg="river", loc="Frozen river", actors=[bear_at(380, s=1.3)], counters=dict(FLARES=2), over=[("moon", 830, 160, 1, dict(id="mn"))], ev=[("wagging", "wag"), ("happy", "bob", "bear")], tags=[("Good boy", "happy", "gold")]),
    dict(bg="river", loc="River south · 3:10 AM", actors=[cole_at(260, s=.85), ruth_at(420, s=.8), bear_at(560, s=.8)], counters=dict(FLARES=2), over=[("moon", 830, 160, 1, dict(id="mn"))],
         dimmers=[(-60, 700, .8), (900, 700, .8), (-40, 1000, .6), (920, 1000, .6)], ev=[("moves", "lean", 40)]),
    dict(bg="aurora", loc="Sky · 4:00 AM", counters=dict(FLARES=2), over=[("auroraband", 0, 120, 1, dict(id="au"))], ev=[("explodes", "show", "au"), ("explodes", "shake", 5)], tags=[("Aurora", "aurora", "green")]),
    dict(bg="aurora", loc="Under the aurora", actors=[cole_at(260, s=.9), ruth_at(440, s=.85), bear_at(620, s=.85)], counters=dict(FLARES=2), over=[("auroraband", 0, 120, 1, dict(id="au"))],
         dimmers=[(-40, 760, .8), (880, 760, .8)], ev=[("fall", "retreat")], tags=[("Safe · 1 hour", "safe", "green")]),
    dict(bg="aurora", loc="Kettle Creek · ahead", counters=dict(FLARES=2), props=[("townlights", 200, 1080, 1, dict(id="tl"))], ev=[("one", "town_out", "tl")], tags=[("The town is going dark", "out", "")]),
]),
6: (dict(FLARES=2, CANDLES=3, FUEL="20 MIN"), [
    dict(bg="aurora", loc="Rule 6", actors=[cole_at(360, s=1.1)], props=[("townlights", 200, 1080, 1, dict(id="tl"))], card=("Run <em>toward</em><br>the last light", "toward", 300), ev=[("run", "slide", ("cole", 260))]),
    dict(bg="airstrip", loc="Kettle Creek airstrip · 5:20 AM", light=(760, 1000, 620), glow="white", ev=[("flickering", "flicker")], tags=[("12 survivors", "twelve", "white"), ("Fuel: 20 min", "fuel", "")]),
    dict(bg="airstrip", loc="Kettle Creek airstrip", light=(780, 1050, 500), glow="white", dimmers=[(160, 640, .8), (420, 600, .8), (900, 600, .8), (-40, 760, .9)], ev=[("surrounds", "lean", 50)]),
    dict(bg="cabin", loc="The math", props=[("items", 280, 520, 1, dict(id="it", items=["Fuel · 20 min", "Flares · 2", "Candles · 3", "Snowmachine · full tank"]))],
         ev=[("twenty", "pop", "it-0"), ("flares", "pop", "it-1"), ("candles", "pop", "it-2"), ("snowmachine", "pop", "it-3")]),
    dict(bg="airstrip", loc="Runway · 5:31 AM", props=[("snowmachine", 260, 1020, 1, dict(id="sm"))], actors=[ruth_at(700, s=1.0)], light=(540, 1100, 380), glow="red",
         ev=[("lights", "flare", 1.3), ("lights", "counter", ("FLARES", 1))]),
    dict(bg="airstrip", loc="Runway · 5:32 AM", counters=dict(FLARES=1), props=[("bonfire", 290, 600, 1, dict(id="bf"))], light=(540, 1000, 520), glow="fire", dimmers=[(-60, 600, .9), (860, 600, .9)],
         ev=[("fire", "fire", 2.2), ("scream", "shake", 18), ("scream", "retreat")], tags=[("30 feet of fire", "thirty", "gold")]),
    dict(bg="airstrip", loc="Runway · 5:41 AM", counters=dict(FLARES=1), props=[("bonfire", 290, 600, 1, dict(id="bf"))], light=(540, 1000, 900), glow="fire", dimmers=[(-60, 600, .9), (860, 600, .9)],
         ev=[("shrink", "shrink", .55), ("leans", "lean", 120)], tags=[("10 min", "ten", ""), ("5 min", "five", "")]),
    dict(bg="airstrip", loc="Runway · 5:46 AM", counters=dict(FLARES=1), actors=[bear_at(420, s=1.3)], light=(560, 1000, 520), glow="fire", dimmers=[(780, 560, .9)],
         bubbles=[("Woof! Woof!", 520, 720, "barking")], tags=[("Not one step back", "step", "gold")]),
    dict(bg="black", loc="Runway · 5:48 AM", counters=dict(FLARES=1), props=[("watch", 310, 640, 1, dict(id="w"))], ev=[("date", "pop", "w")], tags=[("End of the long night", "end", "gold")]),
    dict(bg="aurora", loc="Horizon · 5:49 AM", counters=dict(FLARES=1), props=[("sunline", 0, 1180, 1, dict(id="sl"))], ev=[("gold", "show", "sl")], tags=[("First sunrise in 64 days", "sunrise", "gold")]),
    dict(bg="sunset", loc="Kettle Creek · Sunrise", counters=dict(FLARES=1), dimmers=[(-40, 560, .9), (320, 520, .9), (640, 560, .9), (860, 600, .9)],
         ev=[("burn", "burn"), ("hits", "shake", 6)], tags=[("They burn", "burn", "")]),
    dict(bg="black", loc="Final rule", nohud=True, card=("Light is ammo.<br><em>Never waste it.</em>", "final", 380), tags=[("Next winter: 300 days", "winter", ""), ("Follow for more rules", "away", "gold")]),
]),
}
