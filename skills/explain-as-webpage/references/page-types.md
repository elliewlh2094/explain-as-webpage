# Page Types

Pick one page type in SKILL.md step 2, from what the material is. The type decides Figure 1 (the spine of the page) and the section skeleton. Everything else in `writing-rules.md` applies to every type: the conclusion box, question headings, figures next to their text, terms, sources, and the length budget.

| Type | Use when the material is | Figure 1 (spine) | Recipe in `../explainer-figure/references/svg-recipes.md` |
|---|---|---|---|
| Mechanism (default) | a technique, an algorithm, a physical or biological mechanism | causal chain | 1 |
| Package or architecture | a code package: what it does and why it is built this way | main flow through the modules | 3 |
| Code walkthrough | one file or module (usually a child page) | call flow through its functions | 3 |
| Argument | an essay, an opinion piece, a way of thinking | argument map | 6 |
| Roadmap or plan | a roadmap, a learning or project plan, a curriculum: stages with tasks and checks | roadmap of stages; a page tree by default | 7 |
| Practical guide | how to prepare for or decide something | decision tree or grouped checklist | 8 |
| Evolution | an idea that changed through named stages | evolution of stages | 9 |

A page has one type. If one question needs another shape (e.g. a mechanism inside a roadmap), give that section its own figure; Figure 1 stays the spine. The "counterfactual" in `writing-rules.md` is required only in project mode; each type below says what replaces it when the material gives no such case.

## Mechanism (default)

Use the skeleton in `writing-rules.md` as it is.

## Package or architecture pages

The question is "what does this code do and why is it built this way". Figure 1 is the main flow of one unit of work through the modules (input → steps → output). The causal chain becomes a "risk → design decision" figure: for each decision, the problem it prevents, with the test or record that enforces it. End with what works today and what does not yet.

## Code walkthrough pages

Usually a child page; the question is "what does this file or module do, and why is it written this way".

1. Conclusion box: the file's job in one sentence, its inputs and outputs, and the design decision that matters most.
2. Figure 1: the call flow of one run through the file's main functions (entry point → functions → output). Put line ranges in `sm` labels.
3. One `h2` per question, still phrased as the reader asks it ("Why does `evaluate_bpb` report bits per byte, not loss?"). Answer with a code excerpt and point at the key line.
4. A function table: name, lines, what it does (one clause), called by. List only the functions the page discusses or the reader will meet first.
5. Design decisions: decision → the risk it prevents → where the code enforces it.

## Argument pages

1. Conclusion box: the author's main claim in one sentence, the 2–3 reasons that carry it, and where the argument is weakest. Write it as the author's claim ("Graham argues …"), not as an established fact.
2. Figure 1: argument map. The claim at the top, 2–4 reasons under it, the material's example or evidence under each reason, and the main limit as a dashed box.
3. One `h2` per question, usually one reason per section: what the author says, the example the author gives, and when it does not hold.
4. Instead of a counterfactual: "Where is the argument weak?" Counterexamples, missing evidence, other views. Each one has a source or sits in an Inference box.
5. If the material gives advice, end with "How do I apply it?": 3–5 concrete actions, each tied to a section.

## Roadmap and plan pages

A plan is material made of stages, each with tasks, deliverables, and checks: a roadmap, a learning plan, a project plan, a curriculum. Its reader needs to know, for every step, what to do, how to do it, and how to tell it worked. A shorter checklist is not an explanation.

**Structure.** Build a page tree from the first build, whatever the length (`extending-pages.md` §6): the hub and one child page per stage. Split a stage whose unit cards do not fit one page's length budget (roughly more than 6–8 units) into two children; merge stages too small to fill a page. The confirmation still offers a single page as the cheaper alternative, and asks whether to expand units into steps (`sources-and-research.md` §6).

**Hub page:**

1. Conclusion box: the goal, the total duration, the stages in one line, and the one ordering decision that matters most (why X comes before Y).
2. Figure 1: the stages as a roadmap (Recipe 7), each box linking to its child page.
3. Questions about the whole plan, usually: What does each stage produce? (a table: stage, duration, result, checkpoint, link) Why this order? (if the material names common mistakes, a table "mistake → how the plan avoids it") What connects the stages? (a project or artifact reused from stage to stage, with a figure of its parts) What do I cut when I fall behind? (each checkpoint and its first cuts)
4. Leave unit details to the child pages; the hub links to them.
5. Instead of a counterfactual: "What goes wrong if I skip ahead?", only if the material says so.

**Child page** (one stage, or part of one):

1. Conclusion box: the stage's goal, its duration, and what the reader has at its end.
2. Figure 1: the stage's units in order, each with its practice task or deliverable (Recipe 7).
3. One `h2` per question. Group consecutive units under one question ("Weeks 1–3: how do I set up the tools and read C++ types?") and give each unit an `h3`.
4. Each unit is a card: a `<table class="kv">` with four rows: what to do (from the material); steps (an `<ol>`; put the key command or a code excerpt under the table when it helps); what the check proves; result (what the reader has afterwards).
5. The stage's milestone or checkpoint as a two-column table: the item, and what it checks.
6. Resources, if the material lists them: the one or two it recommends most for each unit, with the material's reason.
7. At least one figure besides Figure 1: a mechanism figure for the idea the stage hinges on, e.g. a causal chain for "why a stalled motor resets the microcontroller", the control loop a robot closes, or two executor timelines. A list of units in boxes does not explain anything by itself.

**Explain every check.** For each acceptance item, milestone, or checkpoint, say what it proves and which mistake it would catch: "the build has no warnings" proves the warning flags are on; "a test fails when the formula is broken" proves the tests protect something. A check the reader does not understand becomes a box they tick without doing the work.

## Practical guide pages

1. Conclusion box: who the guide is for, the first decision the reader must make, and the minimum version (what to do if the reader does only one thing).
2. Figure 1: decision tree (questions → branches → which list applies). If there is no real decision, a grouped checklist (one panel per category).
3. One `h2` per question; each section ends with an action.
4. The full checklist as a table: item, why, how much or when. The table, not the prose, carries the list.
5. Instead of a counterfactual: "What are the common mistakes?" A table: the mistake, why it is a problem, what the source advises.
6. Sources say *what* to do more often than *why*. When a column holds your reasoning rather than a source's words (the "why" column, the problems in the mistakes table), say so in the source line under the table: "The Why column is general background unless a source is named."

## Evolution pages

1. Conclusion box: the stages in order in one line, the problem that pushed each change, and which stages are established and which are recent claims.
2. Figure 1: evolution. Stages left to right, each with its name and period; under each arrow, the problem that pushed the next stage. Recent or disputed stages are dashed boxes.
3. One `h2` per stage or per transition ("Why was prompt engineering not enough?").
4. A comparison table: stage, what is engineered, a typical example, source.
5. Instead of a counterfactual: the same task done at two stages, if a source shows it.
