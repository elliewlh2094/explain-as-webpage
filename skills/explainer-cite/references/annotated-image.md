# Annotated Images

Use this when the reader needs labels on a cited image. The labels, leaders, symbols, and concept colours follow `../../explainer-figure/references/svg-recipes.md` § Symbols and `pictorial.md`. This file adds only what a photo changes.

Do not annotate an ND image. It stays whole.

## Recipe

Put the image in an `<svg>`, with a margin for the labels. This photo already names its LIDAR and encoders, so the labels add only the symbols:

```html
<figure id="fig-2">
<svg viewBox="0 0 720 240" role="img" aria-label="Two views of a four-wheeled robot. A leader marks the LIDAR on top as the symbol z, and another marks a wheel encoder as the symbol v.">
  <image href="robot.assets/robot-sensors.webp" x="120" y="10" width="480" height="219"/>
  <circle cx="233" cy="49" r="6" fill="var(--bg)"/><line class="lead" style="stroke:var(--bg);stroke-width:4" x1="233" y1="49" x2="108" y2="49"/>
  <circle class="pin" cx="233" cy="49" r="3"/><line class="lead" x1="233" y1="49" x2="108" y2="49"/>
  <text x="100" y="54" text-anchor="end" class="b"><tspan class="sym c1">z</tspan> laser scan</text>
  <circle cx="570" cy="84" r="6" fill="var(--bg)"/><line class="lead" style="stroke:var(--bg);stroke-width:4" x1="570" y1="84" x2="610" y2="84"/>
  <circle class="pin" cx="570" cy="84" r="3"/><line class="lead" x1="570" y1="84" x2="610" y2="84"/>
  <text x="618" y="89" class="b"><tspan class="sym c2">v</tspan> wheel speed</text>
</svg>
<figcaption>Figure 2. Each sensor gives the filter one symbol.</figcaption>
</figure>
<p class="src">Image source: Guffanti et al., <a href="https://doi.org/10.3390/s25113553">Comparison of Two System Identification Approaches…</a>, Figure 1. License: <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Annotations added by this page.</p>
```

## Rules

- **Keep the image's shape.** Set `height` to `width` × file height ÷ file width. With another shape, the `<image>` box is larger than the picture, and the overlap check then measures the wrong area.
- **Find a point.** A point (px, py) in the file sits at (x + px × width ÷ file width, y + py × width ÷ file width) in the figure. Read it from the file, not from a guess, and check it in a screenshot.
- **Put labels outside the image.** A photo has no fixed background colour, so a label on it has no known contrast. The overlap check reports a label on an image as `text-on-image`.
- **Draw each leader twice.** First draw the same line in `--bg`, 4px wide, with a `--bg` dot under the pin. Then draw the `lead` and the `pin`. A 1px `--muted` line alone disappears on a dark part of a photo.
- **Keep leaders off the image's own words.** The white line under a leader cuts a letter in two. The overlap check cannot read words in a photo, so look for this in the screenshot.
- **Use the image's own labels.** When the original already names a part, do not name it again. Add only what the page needs: the symbol (for example, a leader from the original's "LIDAR" to `z`).
- **Say who added the labels.** The caption or the source line says `Annotations added by this page.` (`標註為本頁加上`).

## Check

The explainer-figure self-check still applies (`../../explainer-figure/SKILL.md` § Self-check).

- The overlap check reports a leader through a label, and a label on the image. It does not see a leader through a word in the image.
- In the intent check, the screenshot with every word hidden hides only this page's labels. The words in the image stay.
- Do not add `data-touch` to a label to pass `text-on-image`. Move the label.
