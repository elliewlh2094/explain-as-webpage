# Writing Rules

How to structure and write the page. The goal: a reader who stopped understanding the agent's work can follow one causal thread from "why" to "what improved", using their own project as the example.

## Page skeleton (in this order)

1. **Title + conclusion box** (`admonition tip`): 2–4 sentences. State what the technique does for *this* project and the single most important result. A reader who stops here has the main point.
2. **Causal chain** (`h2` + Figure 1): cause → mechanism → consequence → fix → measured result. 3–6 nodes. This figure is the spine of the page.
3. **One `h2` per core question**, in the order of the chain's nodes. The heading is the question, written as the reader would ask it. Each section:
   - opens with a one- or two-sentence answer;
   - explains with one figure (or table) next to the text;
   - ends, where possible, with the project's real number that proves the point.
4. **Counterfactual** (table or before/after figure): the same project case without and with the technique.
5. **Limits** (optional, short): what the technique does not fix, what is still open.
6. **Terms** (every technical term on the page, with its English original, one line each) and **Sources** (file paths with section names).

**Package or architecture pages** (the question is "what does this code do and why is it built this way"): Figure 1 is the main flow of one unit of work through the modules (input → steps → output). The causal chain becomes a "risk → design decision" figure: for each decision, the problem it prevents, with the test or record that enforces it. End with what works today and what does not yet.

**Code walkthrough pages** (usually a child page; the question is "what does this file or module do, and why is it written this way"):

1. Conclusion box: the file's job in one sentence, its inputs and outputs, and the design decision that matters most.
2. Figure 1: the call flow of one run through the file's main functions (entry point → functions → output). Put line ranges in `sm` labels.
3. One `h2` per question, still phrased as the reader asks it ("Why does `evaluate_bpb` report bits per byte, not loss?"). Answer with a code excerpt and point at the key line.
4. A function table: name, lines, what it does (one clause), called by. List only the functions the page discusses or the reader will meet first.
5. Design decisions: decision → the risk it prevents → where the code enforces it.

Do not add: scope/authority tables, "how to read this document" guides, change history, timelines of how the analysis evolved, or summaries of other documents. Link to the source report instead.

## Figures and text belong together

- Put each figure directly after the paragraph that introduces it. Never collect figures at the end.
- The paragraph names the figure and what to look at: "In Figure 3, the red points are the matches RANSAC rejects."
- The caption says what the reader should conclude, not what the figure is: "Averaging all matches lands far from the true offset; the inlier fit does not." — not "Comparison of two methods."
- Each figure has one message. If you need "and" to describe it, make two figures or a stepper.
- Prefer a mechanism figure (what happens and why) over a data plot (distribution, ROC). Use a data plot only after the mechanism is clear, and only if it proves a claim on the page.

## Sentences (about 80% of ASD-STE100)

- One idea per sentence. Aim for ≤ 25 words (≤ 40 CJK characters).
- Active voice, present tense: "RANSAC rejects the outliers", not "outliers are rejected".
- One term per concept. Do not alternate synonyms (e.g. pick "wall-clock time" and never switch to "real time").
- **Define every technical term at its first use**, including inside the conclusion box: one short clause, with the English original in parentheses, e.g. 內點率（inlier ratio，同意模型的匹配佔全部匹配的比例）. Stop there unless the user asks for more. Project identifiers count too (phase names, task IDs, experiment names): say in a few words what each one is.
- **Explain every pattern you point out.** If the page says "A almost equals B", say in the same place why, and when it stops holding. An unexplained pattern makes the reader wonder whether it is a coincidence.
- Prefer concrete project nouns (`uav_0`, waypoint 5, `down_camera_lightglue.py`) over abstract ones ("the system", "the module").
- No filler: delete "it is worth noting", "basically", "in order to".
- Write in the page language (SKILL.md step 4) and follow its rules below. Keep code identifiers, file paths, and standard abbreviations (RANSAC, RTF, EKF) in their original form in every language.

## Language

**English.** Plain international English: many readers are not native speakers.

- Use US spelling and keep it consistent.
- Prefer one exact verb to a phrasal verb or an idiom: "remove", not "get rid of"; "check", not "keep an eye on".
- Give every number its unit. Write symbols as they are in the code (`val_bpb`, not "validation BPB").
- Term definitions do not need a second language unless the user asks.

**Traditional Chinese.** Taiwan usage by default: 程式、資料、檔案、預設、執行、網路、品質. Do not use 程序 for "program", 文件 for "file", 默認, 運行, 網絡, 質量, 視頻. Give the English original of each term at its first use.

**Fixed labels.** Set `<html lang>` and use these labels for the page language:

| Element | English (`lang="en"`) | Traditional Chinese (`lang="zh-Hant"`) |
|---|---|---|
| Conclusion box title | Conclusion | 結論 |
| Inference box title | Inference | 推論 |
| Terms / Sources sections | Terms / Sources | 名詞 / 來源 |
| Figure caption prefix | Figure 1. | 圖 1　(full-width space) |
| Page tree label | Pages in this topic | 本主題頁面 |
| Link to a child page | More: | 延伸閱讀： |

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

## Formulas

No math library. Use HTML: `RTF = Δt<sub>sim</sub> / Δt<sub>wall</sub>`, `x<sup>2</sup>`, Unicode symbols (×, ÷, ≤, ≈, Σ, θ). Put an important formula on its own line in a `<p style="text-align:center">`. Follow every formula with a worked example using a project number.

## Code excerpts

Show at most ~15 lines per excerpt, only the lines the explanation refers to, with the file path and line range above the block. Point at the key line in the text ("line 4 is where the threshold applies").
