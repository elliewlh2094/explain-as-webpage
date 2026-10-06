---
name: explainer-figure
description: Draws the figures of an explain-as-webpage page (inline SVG on a fixed grid, a step-by-step stepper, or a slider) from the figure brief that explain-as-webpage writes, and checks each figure in a screenshot. Used only by the explain-as-webpage skill, which reads this file during its build step. Not for standalone charts, plots, dashboards, or diagrams.
disable-model-invocation: true
user-invocable: false
---

# Explainer Figure

## Overview

explain-as-webpage decides what each figure must show. This skill decides how to draw it. The input is one figure brief per figure. The output is a `<figure id="fig-N">` element in the page that explain-as-webpage copied from `../explain-as-webpage/assets/template.html`.

All styles come from that template: use its CSS classes and arrow markers. Do not add colours, fonts, or stylesheets of your own.

Both skills must sit side by side in the same `skills/` folder, because each refers to the other by a relative path.

## Figure brief

explain-as-webpage writes one brief per figure in its learning brief:

| Field | Content |
|---|---|
| Number and place | `fig-N` and the section (`h2`) it belongs to |
| Question | the core question it answers, in the reader's words |
| Type | one row of the table in § Choosing the figure type |
| Content | the facts it shows, each with its source and unit; "schematic" if no source gives values |
| Form | static, slider (L1), or stepper (L2) |
| Message | the one sentence the caption will state |

If a field is missing, take it from the page's learning brief. Do not invent facts to fill a figure.

## Choosing the figure type

| The question is about | Figure | Where in `references/svg-recipes.md` |
|---|---|---|
| why something happens | causal chain | Recipe 1 |
| the same case without and with a technique | before / after | Recipe 2 |
| the parts of a package and the data between them | components and data flow | Recipe 3 |
| two clocks, or events over time | time axes / timeline | Recipe 4 |
| measured values (matches, errors, rates) | points, bars, or curves on axes | Recipe 5, § Axes and scales |
| the spine of an argument, plan, guide, or evolution page | Recipes 6–9 | `../explain-as-webpage/references/page-types.md` picks one |
| a process that runs in steps | stepper | § Stepper |
| a result that depends on a parameter | slider | § Slider |

Draw a mechanism figure (what happens and why) by default. Draw a numeric figure only after the mechanism is clear, and only if it proves a claim on the page.

## Process

1. Read the brief, then `references/svg-recipes.md`: the layout rules and the colour meaning first, then the recipe.
2. Draw on the grid. For a stepper, draw the final state first, check it, then split it into steps.
3. Run the self-check below. Fix every failure by editing coordinates, not by adding CSS.
4. Put the figure directly after the paragraph that introduces it. The paragraph, the caption, and the source line follow `../explain-as-webpage/references/writing-rules.md` § Figures and text.

## Self-check

Look at the figures after the page check of explain-as-webpage (its step 6), one figure at a time if needed.

- Every label fits inside its box, and no label crosses a line or another label.
- Every arrow starts and ends at a box edge.
- Every number shows its unit, axis title, or legend inside the figure.
- The figure has one message, and the caption can state it.

To look at every figure of a page at once (labels that crowd an arrow, text that leaves its box, a number whose meaning the figure, caption, and source line do not give), screenshot a temporary copy that hides everything but the figures and the source lines. Use Python for the edit: CSS and scripts contain characters that clash with `sed` delimiters.

```bash
python3 - "$F" <<'EOF'
import sys
s = open(sys.argv[1], encoding="utf-8").read()
s = s.replace("</body>", "<style>.side,.topbar{display:none!important}.main{margin-left:0}"
              ".content>*:not(figure):not(.src){display:none}</style></body>")
open("/tmp/figures.html", "w", encoding="utf-8").write(s)
EOF
google-chrome --headless=new --disable-gpu --hide-scrollbars --window-size=900,2400 --screenshot=/tmp/figures.png file:///tmp/figures.html; rm /tmp/figures.html
```

To inspect one figure or one stepper frame, screenshot a temporary copy that hides everything else and clicks ▶ n−1 times (here: Figure 4, frame 3):

```bash
sed "s|</body>|<style>.side,.topbar{display:none!important}.main{margin-left:0}.content>*:not(#fig-4){display:none}</style><script>var b=document.querySelectorAll('#fig-4 .stepper-bar button');for(var i=1;i<3;i++)b[1].click();</script></body>|" "$F" > /tmp/frame.html
google-chrome --headless=new --disable-gpu --hide-scrollbars --window-size=900,800 --screenshot=/tmp/frame.png file:///tmp/frame.html; rm /tmp/frame.html
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll draw it in ASCII/Markdown first." | ASCII diagrams break with fonts and widths. Draw SVG on the grid in `references/svg-recipes.md`. |
| "A new colour will make this part stand out." | Colours carry one meaning on the whole page (§ Colour meaning). A new colour has no meaning for the reader. |
| "The label is close enough; nobody will notice." | Overlaps are what the reader notices first. Check the screenshot and move the coordinates. |
