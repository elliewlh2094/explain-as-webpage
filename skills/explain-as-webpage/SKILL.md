---
name: explain-as-webpage
description: Builds one self-contained HTML explainer page (Read the Docs look, inline SVG diagrams, optional step-by-step animation) that teaches the user an unfamiliar technique, method, or design by using their own project's code, data, and reports as the examples. Use when the user wants to understand why a technique is used in their project, what a package or module the agent built actually does, or how a chain of causes leads to a result; or when they ask for an explainer, primer, visual explanation, or knowledge page. Picks the cheapest presentation tier that answers the questions and confirms it with the user before building. 觸發詞：解釋、說明、看不懂、為什麼要這樣做、圖解、知識網頁、學習筆記、解說頁面。
---

# Explain as Webpage

## Overview

Turn "I don't understand why the agent did X" into one HTML page the user can read in 15 minutes and reopen later. The page is built from the user's own project: real file paths, real numbers, real code. It is organised around the questions the user is stuck on and one causal chain, not around a survey of the topic.

The page is a single `.html` file. No build step, no external URLs, no extra figure or script folders.

## When to Use

- The user must judge or modify something they do not understand (an algorithm, a package an agent wrote, a performance analysis).
- A long Markdown report exists but the user cannot find the causal thread in it.
- The user asks for an explainer, primer, diagram, or "knowledge page".

**When NOT to use:** a one-line answer is enough; the user wants project documentation that lives in the repo (write normal docs); the user wants a video (out of scope: the highest tier is an in-browser step animation).

## Process

### 1. Gather project context

Read only what the questions need: the report, the package directory, the code path. Record each fact you will use together with its source (`path` plus section heading or line). Do not invent numbers. If the project has no measured result for a claim, say so on the page.

### 2. Write a learning brief (internal, not shown as-is)

- **Core questions** (3–5): phrased the way the user would ask them, e.g. "Why can't we just average the matches?"
- **Causal chain**: cause → mechanism → consequence → fix → measured result. One line per link, each link backed by a fact or marked as inference.
- **Counterfactual pairs**: the same project case without and with the technique, with real numbers.
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

Send **one** message (use a structured question tool if the platform has one, e.g. `AskUserQuestion` in Claude Code; otherwise a plain message) containing:

1. The core questions — ask the user to add, remove, or reword.
2. The proposed tier, why, and the cheaper alternative with what it would lose.
3. The output path. Default: `~/Documents/explainers/<repo-name>/<topic-slug>.html`, where `<repo-name>` is the basename of the git top-level directory. Offer "inside the project" as an alternative.
4. The page language (default: the language the user writes in).

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
google-chrome --headless=new --disable-gpu --window-size=390,2400  --screenshot=/tmp/narrow.png "file://$F"   # keep scrollbars: a page-level horizontal scrollbar is a failure
```

Look for text overflowing boxes, overlapping labels, arrows that miss their targets, empty figures, and (in the narrow shot) a horizontal scrollbar for the whole page. If no browser is available, say so in the report.

To inspect one figure or one stepper frame, screenshot a temporary copy that hides everything else and clicks ▶ n−1 times (delete the copy afterwards):

```bash
sed "s|</body>|<style>.side,.topbar{display:none!important}.main{margin-left:0}.content>*:not(#fig-4){display:none}</style><script>var b=document.querySelectorAll('#fig-4 .stepper-bar button');for(var i=1;i<3;i++)b[1].click();</script></body>|" "$F" > /tmp/frame.html
```

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

Tell the user: the file path, how to open it (`xdg-open <path>` / `open <path>`), the questions the page answers, and anything you could not verify.

## Red Flags

- Building before the user confirmed questions, tier, and path.
- Choosing L2 because it looks impressive, not because a question is about a process.
- Long preambles (scope tables, reading guides, change history) before the first answer.
- Figures that show data (histograms, ROC curves) without a mechanism figure that explains *why*.
- Prose that restates a long report section by section instead of following one causal chain.
- Generic textbook examples where a project example exists.
- Leaving helper scripts, image files, or extra folders next to the page.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The topic is big; the page must be long." | The page answers 3–5 questions. Everything else is a link to the source report. |
| "An animation is always clearer." | Animation helps only for processes. For structure, a static figure is faster to read. |
| "I'll draw it in ASCII/Markdown first." | ASCII diagrams break with fonts and widths. Draw SVG on the grid in `svg-recipes.md`. |
| "The user can read the report for the numbers." | The page exists because the report did not work. Bring the key numbers onto the page. |
