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

## Recipe 1 — Causal chain (Figure 1 of every page)

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
