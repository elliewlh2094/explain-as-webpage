# Writing Rules

How to structure and write the page. The goal: a reader who stopped understanding the agent's work can follow one causal thread from "why" to "what improved", using their own project as the example.

## Page skeleton (in this order)

1. **Title + conclusion box** (`admonition tip`): 2–4 sentences. State what the technique does for *this* project and the single most important result. A reader who stops here has the main point.
2. **Spine figure** (`h2` + Figure 1): for a technique, the causal chain: cause → mechanism → consequence → fix → measured result, 3–6 nodes. Other page types use another spine (`page-types.md`). This figure is the spine of the page.
3. **One `h2` per core question**, in the order of the spine's nodes. The heading is the question, written as the reader would ask it. Each section:
   - opens with a one- or two-sentence answer;
   - explains with one figure (or table) next to the text;
   - ends, where possible, with the project's real number that proves the point.
4. **Counterfactual** (table or before/after figure): the same project case without and with the technique. Required in project mode; in other modes only if the material gives such a case (`page-types.md` says what replaces it).
5. **Limits** (optional, short): what the technique does not fix, what is still open.
6. **Terms** (every technical term on the page, with its English original, one line each) and **Sources** (file paths with section names).

For package, code walkthrough, argument, roadmap, practical guide, and evolution pages, follow the skeleton in `page-types.md`.

Do not add: scope/authority tables, "how to read this document" guides, change history, timelines of how the analysis evolved, or summaries of other documents. Link to the source report instead.

## Figures and text belong together

- Put each figure directly after the paragraph that introduces it. Never collect figures at the end.
- The paragraph names the figure and what to look at: "In Figure 3, the red points are the matches RANSAC rejects."
- The caption says what the reader should conclude, not what the figure is: "Averaging all matches lands far from the true offset; the inlier fit does not." — not "Comparison of two methods."
- Each figure has one message. If you need "and" to describe it, make two figures or a stepper.
- Prefer a mechanism figure (what happens and why) over a data plot (distribution, ROC). Use a data plot only after the mechanism is clear, and only if it proves a claim on the page.
- **Every number in a figure tells the reader what it means.** This covers axes, bars, sliders, and a single number inside a box. Using only the figure, its caption, and its source line, the reader can answer four questions; do not leave them to guess:
  1. *What is measured*: the quantity the reader compares.
  2. *The unit*: metres, °C, tokens, seconds. Pick the unit from the question, not because it is easy to measure: file size in bytes is not the cost of loading a file into a model (9.8 KB and 11.8 KB of rules can both be about 3.7k tokens). A quantity without a unit gets its definition and range instead (AUC: area under the ROC curve, 0 to 1).
  3. *How to read it*: which direction is better, where the baseline is, what a reference line means.
  4. *Where it comes from*: measured, computed, estimated, or schematic. Mark estimates as estimates.

  Put axis titles, units, and the legend inside the figure (`../explainer-figure/references/svg-recipes.md` § Axes and scales), how to read it in the paragraph or the caption, and the origin in the source line. Use one unit per figure. If no source supports the numbers, draw a schematic without values and say so. In the report (SKILL.md step 7), give the unit of each figure with numbers and why you chose it.

## Sentences (about 80% of ASD-STE100)

- One idea per sentence. Aim for ≤ 25 words (≤ 40 CJK characters).
- Active voice, present tense: "RANSAC rejects the outliers", not "outliers are rejected".
- One term per concept. Do not alternate synonyms (e.g. pick "wall-clock time" and never switch to "real time").
- **Define every technical term at its first use**, including inside the conclusion box: one short clause, with the English original in parentheses, e.g. 內點率（inlier ratio，同意模型的匹配佔全部匹配的比例）. Stop there unless the user asks for more. Project identifiers count too (phase names, task IDs, experiment names): say in a few words what each one is.
- **Explain every pattern you point out.** If the page says "A almost equals B", say in the same place why, and when it stops holding. An unexplained pattern makes the reader wonder whether it is a coincidence.
- Prefer concrete project nouns (`uav_0`, waypoint 5, `down_camera_lightglue.py`) over abstract ones ("the system", "the module").
- Give every number its unit, in every language: "2.7 kg", "3.7k tokens", "15 秒".
- No filler: delete "it is worth noting", "basically", "in order to".
- Write in the page language (SKILL.md step 4) and follow its rules below. Keep code identifiers, file paths, and standard abbreviations (RANSAC, RTF, EKF) in their original form in every language.

## Language

**English.** Plain international English: many readers are not native speakers.

- Use US spelling and keep it consistent.
- Prefer one exact verb to a phrasal verb or an idiom: "remove", not "get rid of"; "check", not "keep an eye on".
- Write symbols as they are in the code (`val_bpb`, not "validation BPB").
- Term definitions do not need a second language unless the user asks.

**Traditional Chinese.** Taiwan usage by default: 程式、資料、檔案、預設、執行、網路、品質. Do not use 程序 for "program", 文件 for "file", 默認, 運行, 網絡, 質量, 視頻. Give the English original of each term at its first use.

**Fixed labels.** Set `<html lang>` and use these labels for the page language:

| Element | English (`lang="en"`) | Traditional Chinese (`lang="zh-Hant"`) |
|---|---|---|
| Conclusion box title | Conclusion | 結論 |
| Inference box title | Inference | 推論 |
| Note box title (added content, `sources-and-research.md` §6) | Note | 說明 |
| Emerging view box title (`sources-and-research.md` §8) | Emerging view | 新興說法 |
| Caution box title (high-risk topics) | Caution | 注意 |
| Access date in Sources | Accessed | 存取日期 |
| Source grades g1–g4 | Primary / Authoritative / Secondary / Emerging | 原始材料／權威或同儕審查／二手整理／新興或個人說法 |
| Terms / Sources sections | Terms / Sources | 名詞 / 來源 |
| Figure caption prefix | Figure 1. | 圖 1　(full-width space) |
| Page tree label | Pages in this topic | 本主題頁面 |
| Link to a child page | More: | 延伸閱讀： |

## Reader

The confirmation (SKILL.md step 4, item 3) fixes the reader. Write every page of a topic for that reader:

| Reader | New terms per page | Formulas | Code | Analogies |
|---|---|---|---|---|
| General public | at most ~3 key concepts; everyday words first, the technical term in brackets | none, or one in words | none | welcome, with their limit |
| Non-specialist university student | at most 5 key concepts | simple ones, each with a worked example | none, unless asked | welcome, with their limit |
| Engineer or specialist (default in project mode) | as the topic needs | as needed | short excerpts | only where they save time |

Every analogy says where it stops holding, in the same place: "Like a thermostat, the controller compares and corrects; unlike a thermostat, it also reacts to how fast the error changes."

## Ground the symbols in one running example

When a page explains a technique for a domain (EKF for robots, a codec for video), the reader must see the domain object behind every symbol, or the page reads as pure mathematics.

- Early on, introduce one concrete example that the whole page reuses: a specific robot, file, or patient case, with what it knows and what it does not.
- Give a table: symbol → general name → what it is in the example ("P: covariance: how unsure the robot is about where it is; drawn as an ellipse").
- Narrate every process step (a stepper, a table of steps) in the example's words, with numbers actually computed for the example, not invented. Say that the numbers are illustrative and where they come from.
- Explain each formula once by intuition in the example's terms ("3 m of travel with 2° of heading doubt is about 10 cm of sideways doubt").

## Facts, inferences, sources

- A fact is something a file, log, measurement, or the code states, or, in document mode, something the user's document states. Give its source in a `.src` line under the table/figure or inline as `code`. Cite a document by its section heading or page (`sources-and-research.md` §4).
- An inference is your reasoning beyond the sources. Put it in an `admonition warning` titled "Inference" (or the reader's-language equivalent).
- If the project or document has no measurement for a claim, write that explicitly. Do not borrow numbers from the web as if they were the material's numbers. Textbook background is allowed if labelled as general background.

## Length budget

| Tier | Prose (excluding tables, code, captions) | Figures |
|---|---|---|
| L0 | ≤ ~1,800 words / ~3,500 CJK characters | 2–5 |
| L1 | same | 2–5, at most 2 interactive |
| L2 | same | 2–6, at most 2 steppers, ≤ 8 steps each |

Between two figures or tables, keep prose under ~250 words (~500 CJK characters). If a section needs more, it is two questions — split it or cut it.

## Label tables

A two-column table whose first column is a short label (e.g. "What to do / Steps / What the check proves / Result") uses `<table class="kv">`. Without it, CJK labels wrap one or two characters per line, because the long second column takes the width. Put a list of steps in an `<ol>` inside the cell, not as ①②③ in one paragraph. The same applies to a table with more columns: keep its short columns (names, symbols, formulas) on one line with `style="white-space:nowrap"` on those cells, and let the long description column wrap. A formula broken across two lines is misread.

## Formulas

No math library. Use HTML: `RTF = Δt<sub>sim</sub> / Δt<sub>wall</sub>`, `x<sup>2</sup>`, Unicode symbols (×, ÷, ≤, ≈, Σ, θ). Put an important formula on its own line in a `<p style="text-align:center">`. Follow every formula with a worked example using a project number.

Do not use combining marks such as x̄, μ̄, or x̂ (a letter plus U+0304 or U+0302): the mark drifts away from its letter in many fonts. Write the distinction another way: `x<sup>−</sup>` for a prior estimate, a subscript (`x<sub>pred</sub>`), or a word. Inside SVG text, use a superscript character (x⁻) or a `<tspan>`. Say once on the page what the mark means.

## Code excerpts

Show at most ~15 lines per excerpt, only the lines the explanation refers to, with the file path and line range above the block. Point at the key line in the text ("line 4 is where the threshold applies").
