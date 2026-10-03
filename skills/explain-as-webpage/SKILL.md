---
name: explain-as-webpage
description: Builds one self-contained HTML explainer page (Read the Docs look, inline SVG diagrams, optional step-by-step animation) that teaches an unfamiliar technique, method, or idea, using the user's own material as the examples - their project's code, data, and reports, or a document they give (web article URL, PDF, Markdown or text file). Use when the user wants to understand why a technique is used in their project, what a package the agent built does, or how a chain of causes leads to a result; when they want an article, PDF, or notes turned into an easier-to-read page; or when they ask for an explainer, primer, visual explanation, or knowledge page. Also use for follow-up questions on an existing page: it extends the page or adds linked child pages. Picks the cheapest presentation tier and confirms it before building. Writes in the user's language. 觸發詞：解釋、說明、看不懂、為什麼要這樣做、圖解、知識網頁、知識文件、學習筆記、整理成網頁、這篇文章、這份 PDF、追問、補充頁面。
---

# Explain as Webpage

## Overview

Turn "I don't understand why the agent did X" (or "I can't get through this article") into one HTML page the user can read in 15 minutes and reopen later. The page is built from the user's own material: real file paths, numbers, and code from their project, or the sections and examples of a document they give. It is organised around the questions the user is stuck on and one causal chain, not around a survey of the topic.

Each page is a single `.html` file. No build step, no external URLs, no extra figure or script folders. When the user keeps asking about a topic, the topic grows into a hub page plus linked child pages, and each page keeps its own length budget.

## When to Use

- The user must judge or modify something they do not understand (an algorithm, a package an agent wrote, a performance analysis).
- A long Markdown report exists but the user cannot find the causal thread in it.
- The user gives an article, PDF, or notes and wants a page that is easier to read.
- The user asks for an explainer, primer, diagram, or "knowledge page".

**When NOT to use:** a one-line answer is enough; the user wants project documentation that lives in the repo (write normal docs); the user wants a video, or gives a video as the material (out of scope: the agent cannot watch it, and the highest tier is an in-browser step animation).

## Process

**Follow-up on an existing page?** If the user asks more about a topic that already has a page (they name the page, or the output directory has one on this topic), read `references/extending-pages.md` first. It changes how steps 2, 4, 5, and 6 apply.

### 1. Identify the material and gather context

| Mode | The user gives | Read it with | Cite facts as |
|---|---|---|---|
| project | a repo, report, or code path | file reads | `path` + section heading or line |
| document | a web article URL, PDF, Markdown or text file, pasted text | full text via `curl` / `pdftotext` | the material's heading or page |

In document mode, first read `references/sources-and-research.md`: how to get the full text (not a summary), long material, quoting, helper skills, and the output path. Read only what the questions need: the report, the package directory, the code path, the document's sections. Record each fact you will use together with its source. Do not invent numbers. If the material has no measured result for a claim, say so on the page.

### 2. Write a learning brief (internal, not shown as-is)

- **Core questions** (3–5): phrased the way the user would ask them, e.g. "Why can't we just average the matches?"
- **Causal chain**: cause → mechanism → consequence → fix → measured result. One line per link, each link backed by a fact or marked as inference.
- **Counterfactual pairs**: the same project case without and with the technique, with real numbers. In document mode, only if the material gives such a case.
- **Key concepts**: at most 5 the reader must learn. Every other technical term still gets a one-clause definition at first use (see `writing-rules.md`).

### 3. Choose the presentation tier

Pick the **lowest** tier that answers every core question.

| Tier | Form | Use when a core question is about | Relative cost |
|---|---|---|---|
| **L0** | Text + static inline SVG | Structure, composition, a causal chain, before/after | 1× |
| **L1** | L0 + `<details>`, one slider or toggle | A trade-off: the result depends on a parameter | ~1.5× |
| **L2** | L1 + stepper (multi-frame SVG with prev/next/play) | A process: an iterative algorithm, events over time | ~2–3× |

Examples: a package's module responsibilities and data flow → L0. Real-time factor vs wall-clock duration → L1. RANSAC's sample–fit–count loop, or lockstep timing → L2. Escalate only for the question that needs it; the rest of the page stays L0.

### 4. Confirm once, then build

Send **one** message (use a structured question tool if the platform has one, e.g. `AskUserQuestion` in Claude Code, with at most 4 questions; otherwise a plain message) containing:

1. The core questions — ask the user to add, remove, or reword. In document mode, also show the material's outline and 5–8 numbered candidate questions in the message text, and for long material the coverage choice (`sources-and-research.md` §3).
2. The proposed tier (and page count), why, and the cheaper alternative with what it would lose.
3. The page language: the language the user asks for; otherwise the language the user writes in. All pages of one topic use one language.
4. The output path, and any helper skill you plan to use and for which step (`sources-and-research.md` §5). Default path in project mode: `~/Documents/explainers/<repo-name>/<topic-slug>.html`, where `<repo-name>` is the basename of the git top-level directory; offer "inside the project" as an alternative. Document mode: `~/Documents/explainers/<topic-slug>/<topic-slug>.html`.

**Do not build until the user answers.**

### 5. Build the page

1. Copy `assets/template.html` to the output path. Set `lang`, title, sidebar head, breadcrumb.
2. Follow `references/writing-rules.md` for page structure and prose.
3. Follow `references/svg-recipes.md` for every figure (grid, sizes, colours, stepper, slider).
4. Delete all demo content and every `FILL` marker.

### 6. Self-check

Run these checks and fix every failure before reporting:

```bash
F=<output path>
grep -c 'FILL' "$F"                 # must be 0
grep -nE '(src=|url\()["'\'']?https?://' "$F"   # must print nothing (no external resources; <a href> links in Sources are fine)
wc -c < "$F"                        # should be ≤ ~150 KB
```

Then, if `google-chrome` / `chromium` is available, render and **look at** both widths:

```bash
google-chrome --headless=new --disable-gpu --hide-scrollbars --window-size=1280,2400 --screenshot=/tmp/wide.png "file://$F"
P="${F%.html}.narrow.html"; printf '<iframe id="f" src="%s" width="390" height="2400" style="border:0"></iframe><script>f.onload=function(){var d=f.contentDocument.documentElement;document.title=d.scrollWidth>d.clientWidth?"OVERFLOW":"ok"}</script>' "$(basename "$F")" > "$P"
google-chrome --headless=new --disable-gpu --allow-file-access-from-files --virtual-time-budget=3000 --dump-dom "file://$P" | grep -o '<title>[^<]*'   # must print <title>ok
google-chrome --headless=new --disable-gpu --allow-file-access-from-files --window-size=500,2400 --screenshot=/tmp/narrow.png "file://$P"; rm "$P"
```

Chrome windows are at least 500px wide, so the narrow check renders the page in a 390px iframe; `OVERFLOW` means the whole page scrolls sideways (a failure). Look for text overflowing boxes, overlapping labels, arrows that miss their targets, and empty figures. If no browser is available, say so in the report. If the page is part of a page tree, also run the checks in `references/extending-pages.md` §5. To inspect one figure or stepper frame, see `references/svg-recipes.md` § Stepper.

Content checklist:

- [ ] The conclusion box answers the main question in 2–4 sentences.
- [ ] Every core question has its own `h2`, and the heading is the question.
- [ ] The causal chain figure comes before the question sections, and the sections follow its order.
- [ ] Every figure sits next to the paragraph that explains it, and that paragraph refers to it by number.
- [ ] Every number has a source; every inference is inside an "Inference" admonition.
- [ ] Every technical term and project identifier is defined at first use, with its English original.
- [ ] Every pattern the page points out ("A ≈ B") comes with why it holds and when it does not.
- [ ] Reading time ≤ 15 minutes (see the length budget in `writing-rules.md`).

### 7. Report

Tell the user: the file path, how to open it (`xdg-open <path>` / `open <path>`), the questions the page answers, which helper skills you used (or which built-in method you fell back to), and anything you could not verify.

## Red Flags

- Building before the user confirmed questions, tier, and path.
- Choosing L2 because it looks impressive, not because a question is about a process.
- Long preambles (scope tables, reading guides, change history) before the first answer.
- Figures that show data (histograms, ROC curves) without a mechanism figure that explains *why*.
- Prose that restates a long report section by section instead of following one causal chain.
- Generic textbook examples where a project example exists.
- Writing a document-mode page from a fetch tool's summary instead of the full text, without saying so.
- Leaving helper scripts, image files, or extra folders next to the page.
- Adding a new question to a page that is already at its length budget, instead of a child page.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The topic is big; the page must be long." | The page answers 3–5 questions. Everything else is a link to the source report. |
| "An animation is always clearer." | Animation helps only for processes. For structure, a static figure is faster to read. |
| "I'll draw it in ASCII/Markdown first." | ASCII diagrams break with fonts and widths. Draw SVG on the grid in `svg-recipes.md`. |
| "The user can read the report for the numbers." | The page exists because the report did not work. Bring the key numbers onto the page. |
