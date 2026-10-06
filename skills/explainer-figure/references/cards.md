# Summary Cards

A summary card figure replaces prose or a list when the page describes 4–6 parallel items with the same fields: the three layers of a system, the roles in a team, the options a reader chooses from. Each card represents one item (a card is "a container for content representing a single entity", [component.gallery](https://component.gallery/components/card/)). The reader compares the cards field by field, so every card has the same fields in the same order.

The cards are HTML, not SVG. They use the CSS grid of the template (`../explain-as-webpage/assets/template.html`), so on a narrow screen they become one column instead of scrolling sideways.

## When to use cards, a table, or a diagram

| The items | Use |
|---|---|
| 4–6 items, each with the same 2–4 short fields of words | cards |
| items compared by numbers, or more than 4 fields | a table: numbers line up in columns |
| items connected by flow, cause, or time | a mechanism figure (`svg-recipes.md`) |
| 3 items or fewer | prose or a short list |

## Structure

```html
<p>… In <a href="#fig-3">Figure 3</a>, compare what each layer stores and who can change it.</p>
<figure id="fig-3" class="cards">
<div class="card-grid cols-3">
  <div class="card c1"><p class="card-title">Raw sources</p>
    <dl><dt>Stores</dt><dd>articles, papers, notes as given</dd>
        <dt>Changed by</dt><dd>nobody; read only</dd></dl></div>
  <!-- one div.card per item, the same dt labels in the same order -->
</div>
<figcaption>Figure 3. Only the LLM writes the wiki; people change it through sources and questions.</figcaption>
</figure>
```

- **Grid:** no class for 4 cards (2 columns, two rows); `cols-3` for 5–6 cards. Do not use 1 row of 4 or more: the cards become too narrow for CJK text.
- **Title:** the item's name, at most ~12 CJK or ~24 Latin characters. Give the English original in the Terms table, not in the title.
- **Fields:** 2–4 `dt`/`dd` pairs. Each `dd` is at most 2 lines (~40 CJK characters or ~25 words). A field that needs more belongs in the text under the figure.
- **Colour:** add a concept class (`c1`–`c5`) to a card only when the item is one of the page's key concepts and has that colour in other figures (`svg-recipes.md` § Concept colours). Otherwise use no class: the top border is the neutral blue. Do not use `bad` / `good` on cards; if one item is the problem, say so in its fields.
- **Legend:** colours that are not explained by the card titles get a legend under the grid: `<p class="card-legend"><span class="chip c1">…</span> …</p>`.
- **Numbers** in a field carry their unit and source, like numbers in any figure (`../explain-as-webpage/references/writing-rules.md` § Figures and text). The source line goes under the figure.

## Limits

- At most 2 card figures per page and 6 cards per figure. A card figure counts as one figure in the length budget.
- The text inside a card is never below 13px; the template sets this, so do not shrink it with inline styles.
- No SVG drawings inside a card. An icon before the title is allowed (`icons.md`).
- The paragraph before the figure says what to compare across the cards. The caption states the conclusion, not "Overview of the layers".

## Check

Screenshot the card figure alone with the one-figure command in `SKILL.md` § Self-check (`#fig-N` instead of `#fig-4`). The cards in one row have similar heights; if one card is much taller, shorten its fields. The 390px check of explain-as-webpage (step 6) covers the narrow layout: the cards stack in one column and the page does not overflow.
