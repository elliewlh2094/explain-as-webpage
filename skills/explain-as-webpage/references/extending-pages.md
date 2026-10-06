# Extending Pages

How to answer follow-up questions about a topic that already has a page, without letting any page grow past its length budget. A topic grows into a **page tree**: one hub page (the first page) and child pages that each answer a new set of questions.

```
~/Documents/explainers/<repo-name>/
├── <hub>.html             # the first page of the topic
├── <hub>--<child>.html    # one child page per new set of questions
└── <hub>--<child2>.html
```

The tree has two levels only. A follow-up on a child page that needs a new page becomes another child of the hub. In document mode the directory is `~/Documents/explainers/<topic-slug>/`. A tree can also be planned from the first build, for a faithful guided reading of long material (§6).

## 1. Read what exists

- Find the pages: the path the user gives, or `<hub>.html` and `<hub>--*.html` in the output directory.
- Read the hub and the child page the question is about: the conclusion, the core questions (`h2`), the terms, and the current prose length (command in §5).

## 2. Place each new question

| The new question | Place it in |
|---|---|
| Asks for more detail on a question the page already answers, and the answer fits in ~150 words (~300 CJK characters) with no new figure | a `<details>` at the end of that section |
| Is a new question: another mechanism, what a file or function does, a related method | a child page |
| Shows that the page's conclusion or causal chain is wrong or incomplete | a revision of the existing page: conclusion, Figure 1, the affected section |
| Asks to follow the material's order (a question-driven page should become a guided reading) | a re-plan: rebuild the topic as a §6 tree |

Rules:

- `<details>` content counts toward the page's length budget (`writing-rules.md`). If the page would go over budget, use a child page.
- A `<details>` holds text, a table, or a code excerpt. If the answer needs a figure, it is a child page.
- Group related new questions: one child page answers 3–5 of them. Do not make one page per question.
- If the topic would pass ~6 child pages, propose a new topic (a new hub) instead.
- A re-plan keeps the topic's directory and the hub's file name. Copy the existing pages to a backup outside the output directory first. You may move figures to child pages and renumber them; the §4 rule against renumbering does not apply. An interactive figure that moves keeps working only if its element ids and the ids in its script (`f<n>-…`) are renamed with it. The confirmation for a re-plan is §6's.

## 3. Confirm once

Use the same single message as SKILL.md step 4, with these items instead of items 1 and 2 and the output path in item 4 (child pages go next to the hub):

1. Each new question, where it goes (`<details>` / child page / revision), and why.
2. For each child page: its core questions, tier, and file name `<hub>--<child-slug>.html`.
3. What changes on existing pages: the new `<details>`, the link to the child page, the page tree.

Pages in one topic keep one language. Do not build until the user answers.

## 4. Build

**Child page.** Copy `assets/template.html` and follow `writing-rules.md`. For "what does this file or module do" questions, use the code walkthrough skeleton in `page-types.md`. Also:

- Breadcrumb: `project » <a href="<hub>.html">Hub title</a> » child topic`.
- Do not repeat what the hub explains. Give a one-sentence reminder and link the hub section (`<hub>.html#q2`).
- Each page stands alone: define every term at its first use on this page, even if the hub defines it too.

**Existing pages.** Change only what the placement needs:

- At the end of the hub section that the child page goes deeper into, add one line: "More: <a href="<hub>--<child>.html">child title</a>".
- Add the page tree block (`<div class="pages">` from the template) to **every** page of the topic. Use the same list on all pages: hub first, then children in reading order, with `class="sub"` on children. Put `aria-current="page"` on the page's own entry. If the hub was a single page, add the block now.
- Add new entries to Terms and Sources. Update the date in the sidebar head.
- Do not renumber existing figures.

## 5. Self-check

Run SKILL.md step 6 on every new **and** every changed page. Then run these in the output directory (`H` is the hub slug):

```bash
H=<hub-slug>
# The page tree is the same on every page: must print exactly one line
for f in $H.html $H--*.html; do sed -n '/<div class="pages">/,/<\/div>/p' "$f" | sed 's/ aria-current="page"//' | md5sum; done | uniq -c
# Each page marks itself as current: must print nothing
for f in $H.html $H--*.html; do grep -qE "href=\"$f\"[^>]*aria-current=\"page\"" "$f" || echo "no current mark: $f"; done
# Every linked page exists: must print nothing
grep -oh 'href="[^"#:]*\.html' $H.html $H--*.html | sed 's/href="//' | sort -u | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
```

Prose length of one page (only the `<main class="content">` part, without tables, code, figures, captions, and source lines; compare with the budget in `writing-rules.md`). Run it before and after the change:

```bash
python3 - "$F" <<'EOF'
import re, sys
s = open(sys.argv[1], encoding="utf-8").read().split('<main class="content">')[1].split("</main>")[0]
s = re.sub(r'<p class="src">[\s\S]*?</p>', " ", s)
s = re.sub(r"<(style|script|svg|pre|table|figcaption)[\s\S]*?</\1>", " ", s)
t = re.sub(r"<[^>]+>", " ", s)
print("CJK chars:", len(re.findall(r"[一-鿿]", t)), " English words:", len(re.findall(r"[A-Za-z][A-Za-z'-]*", t)))
EOF
```

Run checks over many pages from a script file (`bash check.sh`), not with `bash -c "$(…)"`: Claude Code's safety check cannot read a script passed to `bash -c` and may refuse to run it.

## 6. A tree from the first build (faithful guided reading)

When the user picks faithful guided reading for long material, or a page per stage for a plan (`sources-and-research.md` §3), plan the whole tree before building anything.

**Plan the tree in the learning brief.**

- Map every section of the material to one page and one `h2`: a table "material section → page → `h2`". Neighbouring sections may share an `h2`. A section you leave out on purpose (an advert, a sign-up request, a repeated summary) gets the row "skipped" with the reason.
- Group the sections into at most ~6 child pages, 3–5 questions each, and keep each page within its length budget (`writing-rules.md`). If the material needs more pages, propose question-driven coverage for part of it instead.
- The hub carries the conclusion, Figure 1 as the structure of the whole material (the spine of its page type in `page-types.md`, one node per child page, each child's node a link to its page), and one short section per child: 2–4 sentences and a "More:" link. The hub's own questions are about the whole material ("What is the plan?", "Why this order?"). A summary card figure with one card per child, each title a link, can replace the short sections (`../explainer-figure/references/cards.md`).
- Figure 1 of a child page lists that part's sections in the material's order (Recipe 7, three per row), each box a link to the `h2` that covers it. The reader sees where they are in the original and can jump to any section.
- A recurring part of the material (a recap at the end of each chapter, a summary box per lesson) gets the same `h2` on every child page, in the same place. If the material lacks it for one part, keep the `h2` and say so; do not invent the missing content.

**Confirm once.** In the single message of SKILL.md step 4, item 1 lists the planned tree: each page's file name (`<hub>.html`, `<hub>--<child-slug>.html`), the material sections it covers, and its questions. Item 2 gives the tier per page.

**Build.** Build the hub first, with its "More:" links and the page tree block already listing every child. Then build the children in reading order (§4 "Child page"). Every page carries the same page tree block. For four or more pages, generate the shared parts (the page tree block, the breadcrumbs, and Figure 1 of each page) from one list in a temporary script kept outside the output directory, and delete the script after the self-check; hand-copied blocks drift apart.

**Self-check.** Run §5 on every page. Then walk the mapping table: every row points to a page that exists and an `h2` (or `h3`) that answers that section, and every "skipped" row has a reason. Report the skipped sections to the user. In the output directory, with one row per line (`section|page file|id`, or `section||skip`):

```bash
while IFS='|' read -r sec page id; do
  if [ "$id" = skip ]; then echo "skipped: $sec"; continue; fi
  grep -qE "<h[23] id=\"$id\"" "$page" || echo "MISSING: $sec -> $page#$id"
done <<'EOF'
Introduction|<hub>.html|q1
Self-promotion paragraph||skip
EOF
```

It must print only the "skipped" rows.
