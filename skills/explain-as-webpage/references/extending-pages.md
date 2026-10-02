# Extending Pages

How to answer follow-up questions about a topic that already has a page, without letting any page grow past its length budget. A topic grows into a **page tree**: one hub page (the first page) and child pages that each answer a new set of questions.

```
~/Documents/explainers/<repo-name>/
├── <hub>.html             # the first page of the topic
├── <hub>--<child>.html    # one child page per new set of questions
└── <hub>--<child2>.html
```

The tree has two levels only. A follow-up on a child page that needs a new page becomes another child of the hub.

## 1. Read what exists

- Find the pages: the path the user gives, or `<hub>.html` and `<hub>--*.html` in the output directory.
- Read the hub and the child page the question is about: the conclusion, the core questions (`h2`), the terms, and the current prose length (command in §5).

## 2. Place each new question

| The new question | Place it in |
|---|---|
| Asks for more detail on a question the page already answers, and the answer fits in ~150 words (~300 CJK characters) with no new figure | a `<details>` at the end of that section |
| Is a new question: another mechanism, what a file or function does, a related method | a child page |
| Shows that the page's conclusion or causal chain is wrong or incomplete | a revision of the existing page: conclusion, Figure 1, the affected section |

Rules:

- `<details>` content counts toward the page's length budget (`writing-rules.md`). If the page would go over budget, use a child page.
- A `<details>` holds text, a table, or a code excerpt. If the answer needs a figure, it is a child page.
- Group related new questions: one child page answers 3–5 of them. Do not make one page per question.
- If the topic would pass ~6 child pages, propose a new topic (a new hub) instead.

## 3. Confirm once

Use the same single message as SKILL.md step 4, with these items instead of items 1–3:

1. Each new question, where it goes (`<details>` / child page / revision), and why.
2. For each child page: its core questions, tier, and file name `<hub>--<child-slug>.html`.
3. What changes on existing pages: the new `<details>`, the link to the child page, the page tree.

Pages in one topic keep one language. Do not build until the user answers.

## 4. Build

**Child page.** Copy `assets/template.html` and follow `writing-rules.md`. For "what does this file or module do" questions, use the code walkthrough skeleton. Also:

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

Prose length of one page (excludes tables, code, figures, and captions; compare with the budget in `writing-rules.md`). Run it before and after the change:

```bash
python3 - "$F" <<'EOF'
import re, sys
s = open(sys.argv[1], encoding="utf-8").read()
s = re.sub(r"<(style|script|svg|pre|table|figcaption)[\s\S]*?</\1>", " ", s)
t = re.sub(r"<[^>]+>", " ", s)
print("CJK chars:", len(re.findall(r"[一-鿿]", t)), " English words:", len(re.findall(r"[A-Za-z][A-Za-z'-]*", t)))
EOF
```
