# Pictorial Figures

The figure type follows the question (`SKILL.md` § Choosing the figure type); how a node looks follows the thing it stands for. This file has two parts:

- **§ Drawn objects**: the one style for every object drawn in any figure, such as a robot in a data-flow figure or a person in a timeline, and the parts library that draws them.
- **Recipes P1–P5**: layouts for a whole pictorial figure, which shows *where* the parts are: what goes in which layer of a backpack, where the water of the body is, what a game object holds, where an object moves. Use one when position, containment, or pose carries the meaning. For causes, flows, and steps, use a mechanism figure (`svg-recipes.md`), with its concrete nodes drawn as objects.

The object can be the real thing (a backpack) or a metaphor for an abstract one (a jar for a game object). A metaphor needs one sentence in the paragraph that says where it stops holding (`../explainer-page/references/writing-rules.md` § Reader).

## Drawn objects

Every object drawn in a figure (a person, a robot, a backpack) has one style: a 4px outline and flat fills. The template's `ink` classes carry it.

| Class | Use |
|---|---|
| `ink` | outline and light fill: the concept colour's `--cb` when the object or its `<use>` has `c1`–`c5`, the page background otherwise |
| `ink dark` | dark parts: wheels, nozzles, hubs |
| `ink glass` | windows, lenses, sensors, rotors |
| `ink hollow` | the outline only: a cut-open container's outline, drawn over its clipped layers (Recipe P1) |
| `ink-edge`, then `ink-fill` | several shapes with one outer outline (a person): the same shapes twice, first with an 8px outline, then filled without one |
| `ink-shade` | at most one shade layer: the body again, clipped to the side away from the light (the light comes from the top left) |
| `ink-track` | the faint dashed path of an object's poses (Recipe P5) |
| `ink-level` | with `c1`–`c5`, on a second copy of an object clipped at a level: a deeper fill for the filled part (water in a body, fuel in a tank; Recipe P2) |

These rules come from test drawings; each one prevents a failure that was seen.

- **Fills come only from these classes.** No gradients, no new colours.
- **Keep separate parts at least 11px apart** (2 × 4px + 3px). Closer, the outlines join them into one blob.
- **Draw at the needed size; never use `scale()`.** It makes the outline thinner, and `vector-effect` does not reach inside a `<use>`.
- **Inside an object that a `<use>` shows, use only the `ink` classes.** A rule with an ancestor (`svg .box`, `.c1 .ink`) never reaches the shapes inside a `<use>`, so `box` and `line` turn black there. Put the concept class on the object's `<g>` or on the `<use>`.
- **An object with a front faces +x.** Turn it with `rotate()`; do not mirror it.
- **Draw a specific real thing from sources.** A named rocket, a product, or a building gets its recognisable features (proportions, fins, engines, windows) from what you can read about it: official descriptions, dimensions, descriptions of photos. Build them from basic shapes; do not use a generic shape in its place. In the report, list the features and their sources. If the sources are not enough, ask the user (`../explainer-page/references/sources-and-research.md`).

### Parts library

`scripts/parts.py` prints the geometry of an object; do not write the coordinates of a whole object by hand. It needs only Python 3.

```bash
P=<this skill's folder>/scripts/parts.py
python3 $P person --id f2-person --height 150 --cls c1    # front view, 100 tall or more
python3 $P robot --id f3-robot --size 80 --view top       # wheeled robot, top or side view
python3 $P drone --id f3-drone --size 120 --view side     # quadcopter, top or side view
python3 $P cylinder --w 60 --h 70 --cls c2 --at 400,120   # also pill, rect --r "16 16 0 0", ogive; --fill dark|glass|hollow
python3 $P pose --ref f6-robot --path "M70 140 H190 Q230 140 250 100" --at 0,0.5,1 --angles t,t,90
python3 $P sheet > /tmp/parts.svg                         # every part on one sheet (SKILL.md § Self-check)
```

- `person`, `robot`, and `drone` print a `<g id>` for the figure's `<defs>`. Show it with `<use href="#f3-robot" transform="translate(x y) rotate(a)"/>`.
- `--at X,Y[,ANGLE]` prints the object placed instead, for one copy.
- Basic shapes print centred on (0, 0). `rect --r` gives the four corner radii: top-left, top-right, bottom-right, bottom-left.

### Combining basic shapes

For an object the library does not have, combine basic shapes: one command per part, in drawing order (back to front), inside one `<g>`. A backpack (front view) and a car (top view, facing +x):

```bash
P=<this skill's folder>/scripts/parts.py
python3 $P pill --w 44 --h 16 --at 0,-72                                  # backpack: handle
python3 $P rect --w 100 --h 130 --r "34 34 12 12" --cls c1                # body
python3 $P rect --w 64 --h 44 --r "8 8 10 10" --at 0,28                   # front pocket
python3 $P rect --w 26 --h 12 --r "4 4 4 4" --fill dark --at -32,-27      # car: one of four wheels (±32, ±27)
python3 $P rect --w 120 --h 56 --r "18 18 18 18" --cls c2                 # body
python3 $P rect --w 16 --h 42 --r "6 6 6 6" --fill glass --at 22,0       # windscreen
python3 $P rect --w 12 --h 38 --r "5 5 5 5" --fill glass --at -40,0      # rear window
```

```html
<g id="f1-backpack" transform="translate(170 120)">
  <g class="ink" transform="translate(0 -72)"><rect x="-22" y="-8" width="44" height="16" rx="8"/></g>
  <g class="ink c1"><path d="M-16 -65 H16 A34 34 0 0 1 50 -31 V53 A12 12 0 0 1 38 65 H-38 A12 12 0 0 1 -50 53 V-31 A34 34 0 0 1 -16 -65 Z"/></g>
  <g class="ink" transform="translate(0 28)"><path d="M-24 -22 H24 A8 8 0 0 1 32 -14 V12 A10 10 0 0 1 22 22 H-22 A10 10 0 0 1 -32 12 V-14 A8 8 0 0 1 -24 -22 Z"/></g>
</g>
```

### Check drawn objects

Run these after the screenshots in `SKILL.md` § Self-check, for every figure with drawn objects.

1. **Next to the parts sheet.** Outlines, fills, and proportions match the sheet; an object combined from basic shapes looks like the objects of the library. The command puts `/tmp/figures.png` (the figure-only screenshot) next to the sheet:

```bash
python3 <this skill's folder>/scripts/parts.py sheet > /tmp/parts.svg
printf '<body style="margin:0;display:flex;align-items:flex-start"><img src="figures.png" style="width:900px"><img src="parts.svg" style="width:720px"></body>' > /tmp/side.html
google-chrome --headless=new --disable-gpu --hide-scrollbars --window-size=1620,1200 --screenshot=/tmp/side.png file:///tmp/side.html; rm /tmp/side.html
```

2. **Zoomed in where shapes meet**: a joint, a wheel under a body, the place where two stages separate. No gap, no stray corner, no outline thinner than the rest. The command sets the figure's `viewBox` to the region (x y width height in the figure's own coordinates) and takes the screenshot at 4× pixels; a region of about 3:2 fits the window (here: Figure 4):

```bash
python3 - "$F" 4 "300 40 120 80" <<'EOF'
import re, sys
s = open(sys.argv[1], encoding="utf-8").read()
n, box = sys.argv[2], sys.argv[3]
s = re.sub(r'(<figure id="fig-%s".*?<svg[^>]*?viewBox=")[^"]*' % n, lambda m: m.group(1) + box, s, count=1, flags=re.S)
s = s.replace("</body>", "<style>.side,.topbar{display:none!important}.main{margin-left:0}.content>*:not(#fig-%s){display:none}#fig-%s svg{width:auto;min-width:0;height:440px}</style></body>" % (n, n))
open("/tmp/zoom.html", "w", encoding="utf-8").write(s)
EOF
google-chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=4 --window-size=900,500 --screenshot=/tmp/zoom.png file:///tmp/zoom.html; rm /tmp/zoom.html
```

## Rules for every pictorial figure

These rules come from test drawings; each one prevents a failure that was seen.

- **Build the object from the parts library's shapes** (§ Parts library): rounded rectangles, pills, circles, cylinders. Do not trace a detailed outline by hand: the shapes drift and the object looks broken. The label, not the detail, tells the reader what the object is.
- **Drawing left, notes right.** Put the object at x = 10–380 and the notes at x ≥ 430. Each note is one leader: a `pin` (r = 3) on the part, a horizontal `lead` line to x = 420, and the text at x = 430 (a bold line, and an `sm` line 20px below). Keep notes at least 40px apart vertically, one note per part, and never let two leaders cross.
- **Every `id` stays inside the figure's own `<svg><defs>`** and starts with the figure number (`f2-…`). A `clipPath` in the page's shared, hidden `<svg>` works in the browser, but the figure-only screenshot commands hide that block, and Chrome then ignores the clip: the drawing disappears.
- **Colours:** the object and its parts are drawn objects (§ Drawn objects): `ink` shapes, the parts that are key concepts with their concept class (`ink c1`). Content inside the object that is not a physical part (a list of components, a field in a panel) stays `box`, as in any figure. Semantic colours (`bad`, `good`, `warn`) only mark a problem or a fix, next to the part, as in any figure.
- **Clip in a wrapper `<g>`.** Put `clip-path` on a `<g>` around the shapes, not on an element that has a `transform`: the clip then moves with the transform, and the clipped part ends up in the wrong place or disappears.
- **Scale:** a drawing is a schematic. The caption says "示意，不按比例" / "Schematic, not to scale", unless the sizes come from data (then give the source, as for any number).
- **Icons** may label a part (`icons.md`), but the object itself is drawn, not an icon.
- **Notes stay in the figure.** The paragraph points to a part and says what to notice; it does not restate the notes (`../explainer-page/references/writing-rules.md` § Figures and text, *Do not repeat the figure in the text*).
- **Check the screenshot for text on shapes.** The text bounds of a figure can be inside the canvas and still cover a shape or a line. Only the figure screenshot (`SKILL.md` § Self-check) shows this; move the label or shorten it.

## Recipe P1 — Layered container

A container cut open to show its layers: what goes where, and why. Draw each layer as an `ink` rectangle with its concept class, exactly over the container's bounding box and clipped to the container's shape; then draw the container's outline on top with `ink hollow`. The layers' outer edges then lie under that outline, and the edges between layers become lines of the same 4px.

```bash
P=<this skill's folder>/scripts/parts.py
python3 $P pill --w 56 --h 18 --at 250,62                               # handle
python3 $P rect --w 40 --h 100 --r "10 10 10 10" --at 130,280           # side pocket
python3 $P rect --w 220 --h 290 --r "30 30 30 30" --fill hollow --at 250,215   # body outline; the same path is the clip
```

```html
<figure id="fig-1">
<svg viewBox="0 0 720 380" role="img" aria-label="A backpack cut open in three layers: daily items on top, heavy items in the middle against the back, light bulky items at the bottom.">
  <defs><clipPath id="f1-body"><path transform="translate(250 215)" d="M-80 -145 H80 A30 30 0 0 1 110 -115 V115 A30 30 0 0 1 80 145 H-80 A30 30 0 0 1 -110 115 V-115 A30 30 0 0 1 -80 -145 Z"/></clipPath></defs>
  <g class="ink" transform="translate(250 62)"><rect x="-28" y="-9" width="56" height="18" rx="9"/></g>
  <g class="ink" transform="translate(130 280)"><path d="M-10 -50 H10 A10 10 0 0 1 20 -40 V40 A10 10 0 0 1 10 50 H-10 A10 10 0 0 1 -20 40 V-40 A10 10 0 0 1 -10 -50 Z"/></g>
  <g clip-path="url(#f1-body)">
    <rect class="ink c1" x="140" y="70" width="220" height="80"/>
    <rect class="ink c2" x="140" y="150" width="220" height="110"/>
    <rect class="ink c3" x="140" y="260" width="220" height="100"/>
  </g>
  <g class="ink hollow" transform="translate(250 215)"><path d="M-80 -145 H80 A30 30 0 0 1 110 -115 V115 A30 30 0 0 1 80 145 H-80 A30 30 0 0 1 -110 115 V-115 A30 30 0 0 1 -80 -145 Z"/></g>
  <text x="250" y="106" text-anchor="middle" class="b">Daily items</text><text x="250" y="126" text-anchor="middle" class="sm">torch, whistle, ID</text>
  <text x="250" y="201" text-anchor="middle" class="b">Heavy items</text><text x="250" y="221" text-anchor="middle" class="sm">water, canned food</text>
  <text x="250" y="306" text-anchor="middle" class="b">Light, bulky</text><text x="250" y="326" text-anchor="middle" class="sm">clothes, blanket</text>
  <text x="110" y="350" text-anchor="middle" class="sm">pocket</text>
  <circle class="pin" cx="340" cy="110" r="3"/><line class="lead" x1="340" y1="110" x2="420" y2="110"/>
  <text x="430" y="106" class="b">Top</text><text x="430" y="126" class="sm">used most; no digging</text>
  <circle class="pin" cx="340" cy="205" r="3"/><line class="lead" x1="340" y1="205" x2="420" y2="205"/>
  <text x="430" y="201" class="b">Middle, against the back</text><text x="430" y="221" class="sm">keeps the weight close to the body</text>
  <circle class="pin" cx="340" cy="310" r="3"/><line class="lead" x1="340" y1="310" x2="420" y2="310"/>
  <text x="430" y="306" class="b">Bottom</text><text x="430" y="326" class="sm">light items fill the base</text>
</svg>
<figcaption>Figure 1. Daily items on top, heavy items in the middle against the back, light items at the bottom. Schematic, not to scale.</figcaption>
</figure>
```

- 2–4 layers. A layer's height can follow a real share (and then says so); otherwise make the layers about equal.
- Other containers use the same steps: a cup (a path with straight sides), a cell (an ellipse), a building (a rectangle with a roof path).

### P1 with actors and flow arrows

When the question asks both where things sit and who reads or writes them, draw the actors outside the container and connect them to the layers with arrows. The arrows show the direction in which information moves. The notes about each layer go inside the layer, not on leader lines.

```html
<figure id="fig-4">
<svg viewBox="0 0 720 360" role="img" aria-label="A git repo folder in three layers: schema, wiki, and raw sources. On the left, the LLM follows the schema, reads the raw sources, and writes the wiki. On the right, you read the wiki, pick the raw sources, and revise the schema with the LLM.">
  <defs><clipPath id="f4-body"><path transform="translate(360 200)" d="M-110 -140 H110 A10 10 0 0 1 120 -130 V130 A10 10 0 0 1 110 140 H-110 A10 10 0 0 1 -120 130 V-130 A10 10 0 0 1 -110 -140 Z"/></clipPath>
  <g id="f4-you">
    <g class="ink-edge"><circle cx="0" cy="-44.7" r="10.3"/><path d="M-7.3 -23.5 H7.3 A7.3 7.3 0 0 1 14.7 -16.1 V8.8 H-14.7 V-16.1 A7.3 7.3 0 0 1 -7.3 -23.5 Z"/><path d="M-14.7 4.4 H-5.5 V50.4 A4.6 4.6 0 0 1 -14.7 50.4 Z"/><path d="M5.5 4.4 H14.7 V50.4 A4.6 4.6 0 0 1 5.5 50.4 Z"/><rect x="-4.4" y="-4.4" width="8.8" height="41.1" rx="4.4" transform="translate(-9.5 -16.9) rotate(25)"/><rect x="-4.4" y="-4.4" width="8.8" height="41.1" rx="4.4" transform="translate(9.5 -16.9) rotate(-25)"/></g>
    <g class="ink-fill"><circle cx="0" cy="-44.7" r="10.3"/><path d="M-7.3 -23.5 H7.3 A7.3 7.3 0 0 1 14.7 -16.1 V8.8 H-14.7 V-16.1 A7.3 7.3 0 0 1 -7.3 -23.5 Z"/><path d="M-14.7 4.4 H-5.5 V50.4 A4.6 4.6 0 0 1 -14.7 50.4 Z"/><path d="M5.5 4.4 H14.7 V50.4 A4.6 4.6 0 0 1 5.5 50.4 Z"/><rect x="-4.4" y="-4.4" width="8.8" height="41.1" rx="4.4" transform="translate(-9.5 -16.9) rotate(25)"/><rect x="-4.4" y="-4.4" width="8.8" height="41.1" rx="4.4" transform="translate(9.5 -16.9) rotate(-25)"/></g>
    <clipPath id="f4-you-shade"><rect x="0" y="-110" width="110" height="220"/></clipPath>
    <g class="ink-shade" clip-path="url(#f4-you-shade)"><circle cx="0" cy="-44.7" r="10.3"/><path d="M-7.3 -23.5 H7.3 A7.3 7.3 0 0 1 14.7 -16.1 V8.8 H-14.7 V-16.1 A7.3 7.3 0 0 1 -7.3 -23.5 Z"/><path d="M-14.7 4.4 H-5.5 V50.4 A4.6 4.6 0 0 1 -14.7 50.4 Z"/><path d="M5.5 4.4 H14.7 V50.4 A4.6 4.6 0 0 1 5.5 50.4 Z"/><rect x="-4.4" y="-4.4" width="8.8" height="41.1" rx="4.4" transform="translate(-9.5 -16.9) rotate(25)"/><rect x="-4.4" y="-4.4" width="8.8" height="41.1" rx="4.4" transform="translate(9.5 -16.9) rotate(-25)"/></g>
  </g>
  </defs>
  <g class="ink" transform="translate(298 49)"><path d="M-40 -13 H40 A8 8 0 0 1 48 -5 V13 H-48 V-5 A8 8 0 0 1 -40 -13 Z"/></g><text x="262" y="54" class="sm">git repo</text>
  <g clip-path="url(#f4-body)">
    <rect class="ink c3" x="240" y="60" width="240" height="60"/>
    <rect class="ink c1" x="240" y="120" width="240" height="130"/>
    <rect class="ink c2" x="240" y="250" width="240" height="90"/>
  </g>
  <g class="ink hollow" transform="translate(360 200)"><path d="M-110 -140 H110 A10 10 0 0 1 120 -130 V130 A10 10 0 0 1 110 140 H-110 A10 10 0 0 1 -120 130 V-130 A10 10 0 0 1 -110 -140 Z"/></g>
  <text x="360" y="86" text-anchor="middle" class="b c3">schema</text><text x="360" y="106" text-anchor="middle" class="sm">CLAUDE.md / AGENTS.md</text>
  <text x="360" y="156" text-anchor="middle" class="b c1">wiki</text><text x="360" y="176" text-anchor="middle" class="sm">summary, entity, concept pages</text>
  <text x="360" y="196" text-anchor="middle" class="sm">index.md, log.md</text><text x="360" y="226" text-anchor="middle" class="sm">written only by the LLM</text>
  <text x="360" y="281" text-anchor="middle" class="b c2">raw/ sources</text><text x="360" y="301" text-anchor="middle" class="sm">articles, papers, images, data</text>
  <text x="360" y="321" text-anchor="middle" class="sm">read only; the source of truth</text>
  <rect class="box" x="10" y="150" width="120" height="60" rx="6"/>
  <text x="70" y="176" text-anchor="middle" class="b">LLM</text><text x="70" y="196" text-anchor="middle" class="sm">follows schema</text>
  <path class="line" d="M236 90 H70 V148" marker-end="url(#arr)"/><text x="155" y="82" text-anchor="middle" class="sm">rules</text>
  <path class="line" d="M236 300 H70 V212" marker-end="url(#arr)"/><text x="155" y="292" text-anchor="middle" class="sm">reads</text>
  <line class="line" x1="130" y1="180" x2="236" y2="180" marker-end="url(#arr)"/><text x="184" y="172" text-anchor="middle" class="sm">writes</text>
  <use href="#f4-you" transform="translate(650 180)"/>
  <text x="604" y="218" text-anchor="end" class="b">You</text><text x="604" y="236" text-anchor="end" class="sm">pick, ask, judge</text>
  <line class="line" x1="484" y1="180" x2="609" y2="180" marker-end="url(#arr)"/><text x="540" y="172" text-anchor="middle" class="sm">reads</text>
  <path class="line" d="M650 241 V300 H484" marker-end="url(#arr)"/><text x="566" y="292" text-anchor="middle" class="sm">picks sources</text>
  <path class="line" d="M650 119 V90 H484" marker-end="url(#arr)"/><text x="566" y="82" text-anchor="middle" class="sm">revises with the LLM</text>
</svg>
<figcaption>Figure 4. Information flows from the raw sources through the LLM into the wiki and on to you; the only arrow into the wiki comes from the LLM. Folder names are illustrative.</figcaption>
</figure>
```

- The container keeps the P1 coordinates, moved to x = 240–480; one actor on each side. An abstract actor (the LLM) is a box (120 × 60) at x = 10; a person (you) is drawn: `parts.py person --height 110`, centred at x = 650, with its label to the left of its feet.
- At most 3 arrows per side. Route them so they never cross: the top one leaves above the actor, the middle one is straight, the bottom one leaves below.
- Each arrow ends 2px outside the container's outline (x = 236 or 484) or the person's bounding rectangle, and has one verb in `sm` above its horizontal part.
- The paragraph says which arrows to compare ("only one arrow reaches the wiki"), not what each arrow says.

## Recipe P2 — Silhouette with leaders

A figure of a person (or an animal, a vehicle) with a filled region and notes. Draw the person once in `<defs>` with the parts library, show it with `<use>`, then show it again with a concept class and `ink-level`, inside a `<g>` clipped by a rectangle: the clipped copy is the filled region (a level, a zone).

```bash
python3 <this skill's folder>/scripts/parts.py person --id f2-person --height 340
```

```html
<figure id="fig-2">
<svg viewBox="0 0 720 400" role="img" aria-label="A person filled with water to about 60 percent of the height; a bar splits the body water into intracellular fluid, about two thirds, and interstitial fluid and plasma, about one third.">
  <defs>
  <g id="f2-person">
    <g class="ink-edge"><circle cx="0" cy="-138.3" r="31.7"/><path d="M-22.7 -81.6 H22.7 A22.7 22.7 0 0 1 45.3 -58.9 V27.2 H-45.3 V-58.9 A22.7 22.7 0 0 1 -22.7 -81.6 Z"/><path d="M-45.3 13.6 H-13.6 V154.1 A15.9 15.9 0 0 1 -45.3 154.1 Z"/><path d="M13.6 13.6 H45.3 V154.1 A15.9 15.9 0 0 1 13.6 154.1 Z"/><rect x="-13.6" y="-13.6" width="27.2" height="126.9" rx="13.6" transform="translate(-29.5 -61.2) rotate(25)"/><rect x="-13.6" y="-13.6" width="27.2" height="126.9" rx="13.6" transform="translate(29.5 -61.2) rotate(-25)"/></g>
    <g class="ink-fill"><circle cx="0" cy="-138.3" r="31.7"/><path d="M-22.7 -81.6 H22.7 A22.7 22.7 0 0 1 45.3 -58.9 V27.2 H-45.3 V-58.9 A22.7 22.7 0 0 1 -22.7 -81.6 Z"/><path d="M-45.3 13.6 H-13.6 V154.1 A15.9 15.9 0 0 1 -45.3 154.1 Z"/><path d="M13.6 13.6 H45.3 V154.1 A15.9 15.9 0 0 1 13.6 154.1 Z"/><rect x="-13.6" y="-13.6" width="27.2" height="126.9" rx="13.6" transform="translate(-29.5 -61.2) rotate(25)"/><rect x="-13.6" y="-13.6" width="27.2" height="126.9" rx="13.6" transform="translate(29.5 -61.2) rotate(-25)"/></g>
    <clipPath id="f2-person-shade"><rect x="0" y="-340" width="340" height="680"/></clipPath>
    <g class="ink-shade" clip-path="url(#f2-person-shade)"><circle cx="0" cy="-138.3" r="31.7"/><path d="M-22.7 -81.6 H22.7 A22.7 22.7 0 0 1 45.3 -58.9 V27.2 H-45.3 V-58.9 A22.7 22.7 0 0 1 -22.7 -81.6 Z"/><path d="M-45.3 13.6 H-13.6 V154.1 A15.9 15.9 0 0 1 -45.3 154.1 Z"/><path d="M13.6 13.6 H45.3 V154.1 A15.9 15.9 0 0 1 13.6 154.1 Z"/><rect x="-13.6" y="-13.6" width="27.2" height="126.9" rx="13.6" transform="translate(-29.5 -61.2) rotate(25)"/><rect x="-13.6" y="-13.6" width="27.2" height="126.9" rx="13.6" transform="translate(29.5 -61.2) rotate(-25)"/></g>
  </g>
  <clipPath id="f2-level"><rect x="30" y="172" width="250" height="220"/></clipPath>
  </defs>
  <use href="#f2-person" transform="translate(150 206)"/>
  <g clip-path="url(#f2-level)"><use href="#f2-person" class="c5 ink-level" transform="translate(150 206)"/></g>
  <line class="line dash" x1="30" y1="172" x2="250" y2="172"/>
  <text x="260" y="168" class="b c5">Body water ≈ 60%</text><text x="260" y="188" class="sm">of body weight (adult)</text>
  <path class="lead" d="M440 110 V100 H610 V110"/><text x="525" y="92" text-anchor="middle" class="sm">2/3 of body water</text>
  <path class="lead" d="M610 110 V100 H700 V110"/><text x="655" y="92" text-anchor="middle" class="sm">1/3</text>
  <rect class="box c1" x="440" y="120" width="170" height="60"/>
  <rect class="box c2" x="610" y="120" width="70" height="60"/>
  <rect class="box c3" x="680" y="120" width="20" height="60"/>
  <text x="525" y="146" text-anchor="middle" class="b">Intracellular</text><text x="525" y="166" text-anchor="middle" class="sm">≈ 40% of weight</text>
  <circle class="pin" cx="645" cy="150" r="3"/><line class="lead" x1="645" y1="150" x2="645" y2="220"/>
  <text x="645" y="240" text-anchor="middle" class="b">Interstitial</text><text x="645" y="260" text-anchor="middle" class="sm">≈ 15%</text>
  <circle class="pin" cx="690" cy="150" r="3"/><line class="lead" x1="690" y1="150" x2="690" y2="290"/>
  <text x="700" y="310" text-anchor="end" class="b">Plasma</text><text x="700" y="330" text-anchor="end" class="sm">≈ 5%</text>
  <path class="line dash" d="M250 320 H525 V184" marker-end="url(#arr)"/>
  <text x="390" y="312" text-anchor="middle" class="sm">split the 60%</text>
</svg>
<figcaption>Figure 2. Most of the body's water is inside the cells; the plasma in the blood vessels is a small part. Schematic; shares are textbook approximations.</figcaption>
</figure>
```

- The clip rectangle sets the level: here its top is at y = 172, 60% of the figure's height up from the feet (y = 36 to 376).
- Here the notes sit on a bar to the right instead of single leaders, because the three parts are shares of one whole. The bar widths follow the shares (2/3, 1/4 and 3/4 of the remaining 1/3, rounded to the 10px grid).
- The figure has no face, hands, or clothes. The library's person reads like a mannequin; that is enough for an explainer and stays stable.

## Recipe P3 — Object and its parts

An object drawn as a container with labelled parts inside, for "what is it made of" questions. A metaphor fits here: a jar is a game object, the things in it are its components.

```html
<figure id="fig-3">
<svg viewBox="0 0 720 380" role="img" aria-label="A jar stands for a GameObject: the lid holds its name; inside are a Transform, a Mesh Renderer, a Box Collider, and a script, each with one job.">
  <g class="ink" transform="translate(250 78)"><path d="M-75 -15 H75 V15 H-75 V-15 Z"/></g>
  <g class="ink" transform="translate(250 225)"><path d="M-94 -135 H94 A36 36 0 0 1 130 -99 V107 A28 28 0 0 1 102 135 H-102 A28 28 0 0 1 -130 107 V-99 A36 36 0 0 1 -94 -135 Z"/></g>
  <g class="ink" transform="translate(250 55)"><path d="M-89 -16 H89 A6 6 0 0 1 95 -10 V10 A6 6 0 0 1 89 16 H-89 A6 6 0 0 1 -95 10 V-10 A6 6 0 0 1 -89 -16 Z"/></g>
  <text x="250" y="60" text-anchor="middle" class="b">GameObject: Player</text>
  <rect class="box" x="150" y="120" width="200" height="44" rx="6"/>
  <use href="#i-move-3d" class="icon" x="162" y="132" width="20" height="20"/><text x="194" y="147" class="b">Transform</text>
  <rect class="box" x="150" y="174" width="200" height="44" rx="6"/>
  <use href="#i-eye" class="icon" x="162" y="186" width="20" height="20"/><text x="194" y="201" class="b">Mesh Renderer</text>
  <rect class="box" x="150" y="228" width="200" height="44" rx="6"/>
  <use href="#i-square-dashed" class="icon" x="162" y="240" width="20" height="20"/><text x="194" y="255" class="b">Box Collider</text>
  <rect class="box c1" x="150" y="282" width="200" height="44" rx="6"/>
  <use href="#i-file-code" class="icon c1" x="162" y="294" width="20" height="20"/><text x="194" y="309" class="b c1">PlayerMove.cs</text>
  <circle class="pin" cx="336" cy="55" r="3"/><line class="lead" x1="336" y1="55" x2="420" y2="55"/>
  <text x="430" y="59" class="sm">name, tag, layer (the lid)</text>
  <circle class="pin" cx="340" cy="142" r="3"/><line class="lead" x1="340" y1="142" x2="420" y2="142"/>
  <text x="430" y="146" class="sm">position, rotation, scale</text>
  <circle class="pin" cx="340" cy="196" r="3"/><line class="lead" x1="340" y1="196" x2="420" y2="196"/>
  <text x="430" y="200" class="sm">draws the mesh on screen</text>
  <circle class="pin" cx="340" cy="250" r="3"/><line class="lead" x1="340" y1="250" x2="420" y2="250"/>
  <text x="430" y="254" class="sm">gives the collision shape</text>
  <circle class="pin" cx="340" cy="304" r="3"/><line class="lead" x1="340" y1="304" x2="420" y2="304"/>
  <text x="430" y="308" class="sm">your script: the behaviour</text>
</svg>
<figcaption>Figure 3. A GameObject is an empty, named jar; what it can do depends on the components put into it.</figcaption>
</figure>
```

- The jar, its neck, and its lid are drawn objects (`parts.py rect`); the components inside are abstract, so they stay boxes. Part boxes are 200 × 44 with 10px between them; at most 5 parts. With more, group them, or use summary cards (`cards.md`).
- Single-line notes (`sm` only) are enough when the part's label already names it.
- The icons need their symbols on the page: run the copy command in `icons.md`.

## Recipe P4 — Interface layout

A software window drawn as a container: its panels as rectangles in their real positions, and the user's action as one dashed arrow. Use it for "which panel does what" and "where do I drag this" questions.

```html
<figure id="fig-5">
<svg viewBox="0 0 720 360" role="img" aria-label="The Unity editor: Hierarchy on the left lists the objects in the scene, the Scene and Game view in the middle shows the result, the Inspector on the right shows the components of the selected object, and Project at the bottom holds the files. A dashed arrow drags bird.png from Project into the Sprite field in the Inspector.">
  <g class="ink" transform="translate(360 35)"><path d="M-344 -15 H344 A6 6 0 0 1 350 -9 V15 H-350 V-9 A6 6 0 0 1 -344 -15 Z"/></g>
  <g class="ink" transform="translate(90 150)"><path d="M-80 -100 H80 V100 H-80 V-100 Z"/></g>
  <g class="ink" transform="translate(350 150)"><path d="M-180 -100 H180 V100 H-180 V-100 Z"/></g>
  <g class="ink" transform="translate(620 195)"><path d="M-90 -145 H90 V139 A6 6 0 0 1 84 145 H-90 V-145 Z"/></g>
  <g class="ink" transform="translate(270 295)"><path d="M-260 -45 H260 V45 H-254 A6 6 0 0 1 -260 39 V-45 Z"/></g>
  <g class="ink dark" transform="translate(358 35)"><polygon points="7 0 -5 -7 -5 7"/></g><text x="380" y="40" class="sm">Play: test the game</text>
  <text x="20" y="72" class="b">Hierarchy</text><text x="20" y="92" class="sm">objects in the scene</text>
  <text x="30" y="122" class="sm">Main Camera</text><text x="30" y="144" class="b c1">bird</text>
  <text x="180" y="72" class="b">Scene / Game View</text><text x="180" y="92" class="sm">editing view / what the camera sees</text>
  <g class="ink c1"><circle cx="350" cy="170" r="22"/></g>
  <text x="540" y="72" class="b">Inspector</text><text x="540" y="92" class="sm">the selected object</text>
  <text x="540" y="122" class="b c1">bird</text>
  <rect class="box c2" x="540" y="134" width="160" height="30" rx="4"/><text x="550" y="154" class="sm">Transform</text>
  <rect class="box c2" x="540" y="172" width="160" height="56" rx="4"/><text x="550" y="192" class="sm">Sprite Renderer</text>
  <rect class="box muted" x="550" y="200" width="140" height="20" rx="3"/><text x="556" y="215" class="sm">Sprite: bird</text>
  <text x="540" y="256" class="sm">+ Add Component</text>
  <text x="20" y="272" class="b">Project</text><text x="20" y="292" class="sm">every file: images, sounds, scripts, fonts</text>
  <use href="#i-image" class="icon" x="30" y="304" width="20" height="20"/><text x="56" y="320" class="sm">bird.png</text>
  <path class="line dash" d="M60 328 H480 Q510 328 510 298 V210 H548" marker-end="url(#arr)"/>
  <text x="340" y="320" text-anchor="middle" class="sm">drag into the Sprite field</text>
</svg>
<figcaption>Figure 5. Each panel does one job: Project holds files, Hierarchy lists objects, the Inspector changes the selected one, and the view shows the result. Schematic layout, not a screenshot.</figcaption>
</figure>
```

- Put each panel's name and one `sm` line inside the panel, not on leader lines: the panels fill the canvas.
- The window and its panels are `ink` rectangles (`parts.py rect`) that share their edges; the round corners are only on the outside. The content of a panel (component rows, a field) stays `box`. The selected object and the field the action changes take their concept colours.
- One action per figure, as one dashed arrow that does not cross any label.
- The caption says "Schematic layout, not a screenshot" / "版面為示意，不是實際截圖". If the reader must find a real button, a screenshot is clearer: ask the user for one from their own copy of the program.

## Recipe P5 — Object and poses

One object at several poses along a path: a robot avoiding a box, a booster turning back. Use a stepper (L2): each frame shows only the current pose, and the faint track grows with the steps: each step adds the part from the previous pose to this one. The reader sees where the object came from, and the path still ahead does not distract.

```bash
P=<this skill's folder>/scripts/parts.py
python3 $P robot --id f6-robot --size 60 --view top --cls c1
python3 $P pose --ref f6-robot --path "M70 140 H190 Q230 140 250 100 Q270 50 360 50 Q450 50 470 100 Q490 140 530 140 H650" --at 0,0.25,0.5,0.75,1
```

```html
<figure id="fig-6" class="stepper">
<svg viewBox="0 0 720 200" role="img" aria-label="A robot drives around a box in five steps; the dashed track shows the path so far.">
  <defs>
  <g id="f6-robot" class="c1">
    <g class="ink dark"><path d="M-10.8 -27 H10.8 A2.4 2.4 0 0 1 13.2 -24.6 V24.6 A2.4 2.4 0 0 1 10.8 27 H-10.8 A2.4 2.4 0 0 1 -13.2 24.6 V-24.6 A2.4 2.4 0 0 1 -10.8 -27 Z"/></g>
    <g class="ink"><path d="M-21.6 -21 H21.6 A8.4 8.4 0 0 1 30 -12.6 V12.6 A8.4 8.4 0 0 1 21.6 21 H-21.6 A8.4 8.4 0 0 1 -30 12.6 V-12.6 A8.4 8.4 0 0 1 -21.6 -21 Z"/></g>
    <clipPath id="f6-robot-shade"><rect x="-60" y="0" width="120" height="60"/></clipPath>
    <g class="ink-shade" clip-path="url(#f6-robot-shade)"><path d="M-21.6 -21 H21.6 A8.4 8.4 0 0 1 30 -12.6 V12.6 A8.4 8.4 0 0 1 21.6 21 H-21.6 A8.4 8.4 0 0 1 -30 12.6 V-12.6 A8.4 8.4 0 0 1 -21.6 -21 Z"/></g>
    <g class="ink glass"><circle cx="-4.8" cy="0" r="8.4"/></g>
    <g class="ink dark"><polygon points="24 0 14.4 -6.6 14.4 6.6"/></g>
  </g>
  </defs>
  <rect class="box muted" x="300" y="110" width="120" height="80" rx="6"/><text x="360" y="155" text-anchor="middle" class="sm">box</text>
  <use href="#f6-robot" data-step="1" data-caption="Step 1: the robot starts on the left." transform="translate(70 140) rotate(0)"/>
  <path class="ink-track" data-step="2+" d="M70 140 L190 140 Q213.1 140 229.5 126.7"/>
  <use href="#f6-robot" data-step="2" data-caption="Step 2: it turns before the box." transform="translate(229.5 126.7) rotate(-39.1)"/>
  <path class="ink-track" data-step="3+" d="M229.5 126.7 Q241.5 116.9 250 100 Q270 50 360 50"/>
  <use href="#f6-robot" data-step="3" data-caption="Step 3: it passes above the box." transform="translate(360 50) rotate(-0.1)"/>
  <path class="ink-track" data-step="4+" d="M360 50 Q450 50 470 100 Q478.5 116.9 490.5 126.7"/>
  <use href="#f6-robot" data-step="4" data-caption="Step 4: it turns back down." transform="translate(490.5 126.7) rotate(39.1)"/>
  <path class="ink-track" data-step="5+" d="M490.5 126.7 Q506.9 140 530 140 L650 140"/>
  <use href="#f6-robot" data-step="5" data-caption="Step 5: it is past the box." transform="translate(650 140) rotate(0)"/>
</svg>
<figcaption>Figure 6. The robot leaves its straight line only to pass the box. Schematic, not to scale.</figcaption>
</figure>
```

- Define the object once in the figure's `<defs>`. `pose` prints one `<use>` per step, and before each one the part of the track that step adds (`data-step="k+"`); add a `data-caption` to each `<use>`.
- `pose` takes each position and angle from the track, so the object sits on it. `--angles` gives each step `t` (along the track), `t+90`, `t-90`, or a fixed angle: a booster flies tail first.
- Split a turn of more than 90° into steps. A stepper has at most 8 steps (`../explainer-page/references/writing-rules.md` § Length budget).
- Two objects that fly together and then separate: put both in one `<g transform>` until the step they separate, then give each its own pose. For an object that first appears at step k (the booster after separation), give `pose --first k`, so its poses and track parts get the right step numbers.
