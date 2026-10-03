# SVG Recipes

All figures are inline `<svg>` inside a `<figure id="fig-N">`. The template already defines the CSS classes and arrow markers used below. Draw on a fixed grid so nothing drifts.

## Layout rules (these prevent broken figures)

- **Canvas:** `viewBox="0 0 720 H"`, H a multiple of 20. Leave a 10px margin on every side. Never set `width`/`height` attributes; CSS scales the SVG.
- **Phones:** the SVG keeps a 540px minimum width and the figure scrolls sideways; the page never does. Do not design for 390px; design for 720 and keep every label ≥ 12px.
- **Grid:** every x/y is a multiple of 10. Boxes are typically 140–160 wide, 50–60 tall. Gaps between boxes are 30.
- **Text fits the box:** at 14px, budget ~14px per CJK character and ~8px per Latin character, plus 24px padding. If a label does not fit, shorten it; do not shrink the font below 12px.
- **One line per `<text>`.** SVG does not wrap. For two lines, use two `<text>` elements 20px apart.
- **Centred labels:** `text-anchor="middle"`, x = box centre. For one line, y = box top + height/2 + 5. For two lines at 14px and 12px, y = top + h/2 − 4 and top + h/2 + 16.
- **Arrows:** a `<line class="line" … marker-end="url(#arr)">` from the edge of one box to the edge of the next (not centre to centre). Horizontal flows: same y for both ends. Bends: use `<path class="line" d="M x y H x2 V y2">`.
- **Max nodes per row:** 4 at width 720. For 5–6, wrap to a second row and connect with a down-then-left path.
- **`role="img"` and `aria-label`** on every SVG: one sentence that says what the figure shows.
- After building, screenshot and check (SKILL.md step 6). Fix any overflow by editing coordinates, not by adding CSS.

## Colour meaning (use consistently on the whole page)

| Class | Meaning |
|---|---|
| `box bad`, `line bad`, `dot bad`, `#arr-bad` | the problem, a wrong value, a rejected item |
| `box good`, `line good`, `dot good`, `#arr-good` | the fix, a correct value, an accepted item |
| `box warn` | a consequence, a risk |
| `box` (blue) | a neutral mechanism or component |
| `box muted` | background context, a panel, an inactive part |
| `dash` | estimated, optional, or "would happen if" |

Text in `class="sm"` is grey 12px: use it for units, sub-labels, and annotations. Colour text with `class="bad"` / `class="good"` (e.g. `class="b bad"`), never with a `fill` attribute: the template's CSS overrides `fill` on `<text>`.

## Recipe 1 — Causal chain (Figure 1 of a mechanism page)

Use the four-box chain in `assets/template.html` as the base. Each box: bold name on line 1, a short measured fact on line 2 (`sm`). Colour the boxes by meaning (cause `bad`, consequence `warn`, fix `good`). If a link is an inference, draw its arrow with `dash`.

## Recipe 2 — Before / after (counterfactual)

Two panels side by side, same scale, same project case:

```html
<svg viewBox="0 0 720 260" role="img" aria-label="…">
  <rect class="box muted" x="10" y="30" width="340" height="220" rx="6"/>
  <text x="180" y="20" text-anchor="middle" class="b">Without X</text>
  <rect class="box muted" x="370" y="30" width="340" height="220" rx="6"/>
  <text x="540" y="20" text-anchor="middle" class="b">With X</text>
  <!-- draw the same elements in both panels; offset the right panel by +360 in x -->
</svg>
```

Put the key number under each panel in `bad` / `good` colour. The reader's eye should go left → right and see one difference.

## Recipe 3 — Components and data flow (L0, e.g. a package)

- Boxes = modules/files (label with the file name in `code` style: use the file name as bold text and its one-line job as `sm`).
- Arrows = data or calls, labelled with the data type in `sm` text placed 8px above the arrow's midpoint.
- Group boxes that belong to one layer inside a `box muted` panel with the layer name at its top-left (`sm`, `text-anchor="start"`).
- Draw the main path left → right or top → bottom; side paths (logs, audit) in `dash`.
- At most ~8 boxes. If the package has more, draw the main path only and list the rest in a table.

## Recipe 4 — Two time axes / timeline

For "simulated time vs wall-clock time" type questions: two horizontal axes, one above the other, ticks every 60–80px, the same events marked on both with vertical `dash` lines between them. The stretch between the axes *is* the explanation. Label each axis at its left end.

## Recipe 5 — Points and residuals (data-driven)

For scatter-like content (matches, inliers, measurements), compute coordinates with a throwaway script (Python/Node) that prints `<circle>` elements, paste the output into the page, and **delete the script**. Keep ≤ ~200 elements per figure. Reserve the areas where labels and the legend go, and have the script reject layouts that put a point inside them; do not nudge labels by hand afterwards. Map data to the canvas with a fixed linear scale and draw the axes with tick labels in `sm`.

## Recipe 6 — Argument map (Figure 1 of an argument page)

The claim on top, the reasons under it, the material's evidence under each reason. Arrows point **up**: evidence supports a reason, a reason supports the claim. The main limit is a dashed `warn` box beside the claim.

```html
<svg viewBox="0 0 720 250" role="img" aria-label="…">
  <rect class="box" x="210" y="10" width="300" height="50" rx="6"/>
  <text x="360" y="31" text-anchor="middle" class="b">Claim</text><text x="360" y="51" text-anchor="middle" class="sm">the author's main point</text>
  <rect class="box warn dash" x="540" y="10" width="170" height="50" rx="6"/>
  <text x="625" y="31" text-anchor="middle" class="b">Limit</text><text x="625" y="51" text-anchor="middle" class="sm">when it does not hold</text>
  <line class="line dash" x1="540" y1="35" x2="512" y2="35" marker-end="url(#arr)"/>
  <rect class="box" x="10" y="110" width="220" height="50" rx="6"/>
  <text x="120" y="131" text-anchor="middle" class="b">Reason 1</text><text x="120" y="151" text-anchor="middle" class="sm">one clause</text>
  <line class="line" x1="120" y1="110" x2="280" y2="62" marker-end="url(#arr)"/>
  <!-- Reason 2 at x=250 (centre 360) with a straight arrow up; Reason 3 at x=490 (centre 600), arrow to (440,62) -->
  <rect class="box muted" x="10" y="190" width="220" height="50" rx="6"/>
  <text x="120" y="211" text-anchor="middle">Example</text><text x="120" y="231" text-anchor="middle" class="sm">§ section of the material</text>
  <line class="line" x1="120" y1="190" x2="120" y2="162" marker-end="url(#arr)"/>
</svg>
```

- 2–4 reasons. With 2, use boxes 300 wide at x=10 and x=410.
- An example that is your own, not the material's, gets `dash` and goes in an Inference box in the text.

## Recipe 7 — Roadmap (Figure 1 of a roadmap page)

Stages left to right under a time axis. Each stage box: name (bold) and duration (`sm`). Under each stage, its deliverable in a `good` box. Arrows between stages are prerequisites.

```html
<svg viewBox="0 0 720 200" role="img" aria-label="…">
  <line class="line" x1="10" y1="30" x2="708" y2="30" marker-end="url(#arr)"/>
  <text x="10" y="20" class="sm">week 0</text><text x="190" y="20" class="sm">week 4</text>
  <!-- one tick label per stage start: x = 10, 190, 370, 550 -->
  <rect class="box" x="10" y="50" width="150" height="60" rx="6"/>
  <text x="85" y="76" text-anchor="middle" class="b">Stage 1</text><text x="85" y="96" text-anchor="middle" class="sm">4 weeks</text>
  <line class="line" x1="160" y1="80" x2="188" y2="80" marker-end="url(#arr)"/>
  <rect class="box" x="190" y="50" width="150" height="60" rx="6"/>
  <text x="265" y="76" text-anchor="middle" class="b">Stage 2</text><text x="265" y="96" text-anchor="middle" class="sm">6 weeks</text>
  <rect class="box good" x="10" y="140" width="150" height="50" rx="6"/>
  <text x="85" y="170" text-anchor="middle">deliverable</text>
  <line class="line good" x1="85" y1="110" x2="85" y2="138" marker-end="url(#arr-good)"/>
</svg>
```

- Up to 4 stages per row (x = 10, 190, 370, 550). For 5–8 stages use a second row at y + 170 and connect the rows with a down-then-left path.
- Do not scale box widths to duration; durations go in the `sm` label. Equal boxes keep labels readable.

**Three per row, snake order** (a plan's hub map, or a stage's list of units): boxes 200×60 at x = 10, 260, 510; row r at y = 40 + 100r. Odd rows run right to left, so the reader's eye never jumps back to the left edge; a vertical arrow under the last box of a row leads to the next row. Line 1 is the name in bold (≤ ~12 CJK or ~22 Latin characters), line 2 the deliverable in `sm good` (≤ ~14 CJK characters). On a hub, wrap each box in a link to its child page, so the figure is also the navigation:

```html
<a href="plan--stage-1.html"><rect class="box" x="10" y="40" width="200" height="60" rx="6"/>
  <text x="110" y="66" text-anchor="middle" class="b">Stage 1</text>
  <text x="110" y="86" text-anchor="middle" class="sm good">deliverable</text></a>
<line class="line" x1="210" y1="70" x2="258" y2="70" marker-end="url(#arr)"/>
<!-- row 0 ends with the box at x=510: down arrow x=610 from y=100 to y=138; row 1 runs right to left -->
```

## Recipe 8 — Decision tree (Figure 1 of a practical guide)

Questions on the left, lists (the outcomes) on the right in `good` boxes. Branches are bent paths labelled with the answer.

```html
<svg viewBox="0 0 720 240" role="img" aria-label="…">
  <rect class="box" x="10" y="100" width="180" height="60" rx="6"/>
  <text x="100" y="126" text-anchor="middle" class="b">Question 1?</text><text x="100" y="146" text-anchor="middle" class="sm">e.g. who is at home</text>
  <path class="line" d="M190 120 H230 V60 H268" marker-end="url(#arr)"/><text x="236" y="85" class="sm">yes</text>
  <path class="line" d="M190 140 H230 V200 H268" marker-end="url(#arr)"/><text x="236" y="180" class="sm">no</text>
  <rect class="box" x="270" y="30" width="180" height="60" rx="6"/>
  <text x="360" y="56" text-anchor="middle" class="b">Question 2?</text><text x="360" y="76" text-anchor="middle" class="sm">the next decision</text>
  <rect class="box good" x="270" y="170" width="180" height="60" rx="6"/>
  <text x="360" y="196" text-anchor="middle" class="b">List C</text><text x="360" y="216" text-anchor="middle" class="sm">see Table 2</text>
  <path class="line" d="M450 50 H490 V35 H528" marker-end="url(#arr)"/>
  <path class="line" d="M450 70 H490 V105 H528" marker-end="url(#arr)"/>
  <rect class="box good" x="530" y="10" width="180" height="50" rx="6"/><text x="620" y="40" text-anchor="middle" class="b">List A</text>
  <rect class="box good" x="530" y="80" width="180" height="50" rx="6"/><text x="620" y="110" text-anchor="middle" class="b">List B</text>
</svg>
```

- At most 3 levels of questions and 5 outcomes. Each outcome points to the table that lists its items; the figure does not list items.
- If there is no real decision, draw a grouped checklist instead: one `box muted` panel per category with its name on top and 3–6 items as `sm` lines, 20px apart.

## Recipe 9 — Evolution (Figure 1 of an evolution page)

Stages left to right, each with its name and period. Under each arrow, the problem that pushed the next stage. Recent or disputed stages use `dash`.

```html
<svg viewBox="0 0 720 160" role="img" aria-label="…">
  <rect class="box muted" x="10" y="40" width="130" height="60" rx="6"/>
  <text x="75" y="66" text-anchor="middle" class="b">Stage A</text><text x="75" y="86" text-anchor="middle" class="sm">2020–2022</text>
  <line class="line" x1="140" y1="70" x2="198" y2="70" marker-end="url(#arr)"/>
  <text x="170" y="125" text-anchor="middle" class="sm">problem that</text><text x="170" y="141" text-anchor="middle" class="sm">pushed B</text>
  <rect class="box" x="200" y="40" width="130" height="60" rx="6"/>
  <text x="265" y="66" text-anchor="middle" class="b">Stage B</text><text x="265" y="86" text-anchor="middle" class="sm">2023–2024</text>
  <!-- next stages at x = 390, 580; problem labels centred at 360, 550 -->
  <rect class="box dash" x="580" y="40" width="130" height="60" rx="6"/>
  <text x="645" y="66" text-anchor="middle" class="b">Stage D</text><text x="645" y="86" text-anchor="middle" class="sm">2026, emerging</text>
</svg>
```

- Up to 4 stages per row; for 5–6, wrap to a second row as in Recipe 7.
- Problem labels sit under the arrows, at most 2 lines of ~12 Latin or ~8 CJK characters each.

## Stepper (L2)

```html
<figure id="fig-3" class="stepper">
<svg viewBox="0 0 720 240" role="img" aria-label="…">
  <!-- base layer: always visible, no data-step -->
  <g data-step="1+" data-caption="Step 1: …">…</g>  <!-- visible from step 1 on -->
  <g data-step="2"  data-caption="Step 2: …">…</g>  <!-- visible only at step 2 -->
  <g data-step="3+" data-caption="Step 3: …">…</g>
</svg>
<figcaption>Figure 3. …</figcaption>
</figure>
```

- `n` = only at step n; `n+` = from step n onward. Use `n+` to build a picture up, `n` for a frame that must disappear (a rejected candidate, a temporary highlight).
- Exactly one group per step carries `data-caption`. The caption is one sentence: what changed and why it matters.
- 3–8 steps. Each step changes one thing.
- Draw the final state first, check it in a screenshot, then split it into steps.
- The script in the template adds ◀ ▶ ▷ controls; do not write a second stepper script.

To look at every figure of a page at once (labels that crowd an arrow, text that leaves its box), screenshot a temporary copy that hides everything but the figures. Use Python for the edit: CSS and scripts contain characters that clash with `sed` delimiters.

```bash
python3 - "$F" <<'EOF'
import sys
s = open(sys.argv[1], encoding="utf-8").read()
s = s.replace("</body>", "<style>.side,.topbar{display:none!important}.main{margin-left:0}"
              ".content>*:not(figure){display:none}</style></body>")
open("/tmp/figures.html", "w", encoding="utf-8").write(s)
EOF
google-chrome --headless=new --disable-gpu --hide-scrollbars --window-size=900,2400 --screenshot=/tmp/figures.png file:///tmp/figures.html
```

To inspect one figure or one stepper frame, screenshot a temporary copy that hides everything else and clicks ▶ n−1 times (here: Figure 4, frame 3; delete the copy afterwards):

```bash
sed "s|</body>|<style>.side,.topbar{display:none!important}.main{margin-left:0}.content>*:not(#fig-4){display:none}</style><script>var b=document.querySelectorAll('#fig-4 .stepper-bar button');for(var i=1;i<3;i++)b[1].click();</script></body>|" "$F" > /tmp/frame.html
```

## Slider (L1)

One slider per figure, a few lines of page-specific script placed after the figure:

```html
<figure id="fig-4">
<svg viewBox="0 0 720 160" role="img" aria-label="…">
  <rect class="box muted" x="10" y="60" width="700" height="40" rx="4"/>
  <rect id="f4-bar" class="box warn" x="10" y="60" width="140" height="40" rx="4"/>
  <text id="f4-out" x="360" y="140" text-anchor="middle" class="b"></text>
</svg>
<p><label>RTF <input id="f4-in" type="range" min="0.05" max="1" step="0.05" value="0.2"></label></p>
<figcaption>Figure 4. …</figcaption>
</figure>
<script>
(function () {
  var inp = document.getElementById('f4-in'), bar = document.getElementById('f4-bar'), out = document.getElementById('f4-out');
  function draw() {
    var rtf = +inp.value, wall = 500 / rtf;                  // 500 s of simulated mission
    bar.setAttribute('width', wall / (500 / 0.05) * 700);    // full width at the slider's minimum RTF
    out.textContent = 'RTF ' + rtf.toFixed(2) + ' → ' + Math.round(wall / 60) + ' min wall-clock';
  }
  inp.oninput = draw; draw();
})();
</script>
```

- Prefix every id with the figure number (`f4-…`) so scripts never collide.
- Anchor the slider to the reader's case: add one `<button data-…>` per real project operating point that sets the slider (or mark them on the scale with a `dot` and an `sm` label).
- Choose `step` so every operating point is reachable exactly: a range input snaps to `min + k × step` (e.g. `step="0.0005"` turns 0.2233 into 0.2235). Check the displayed value after clicking each button.
- The figure must still say something useful at the slider's initial value (screenshots and print show only that).
