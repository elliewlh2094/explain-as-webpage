# Sources and Research

How to read material that is not the user's project, how to cite it, and when to use a helper skill. SKILL.md step 1 sends you here in document mode.

## 1. Modes and output path

| Mode | The user gives | Default output path |
|---|---|---|
| project | a repo, report, or code path | `~/Documents/explainers/<repo-name>/<topic-slug>.html` |
| document | a web article URL, a PDF, a Markdown or text file, or pasted text | `~/Documents/explainers/<topic-slug>/<topic-slug>.html` |

- The mode follows the material, not the current directory. A document read while the agent works inside some repo still uses the document path.
- If the user also asks questions the document does not answer, say so in the confirmation. Answer them only as labelled general background (`writing-rules.md`), or leave them out.
- A video URL is out of scope. Say so and stop; do not download subtitles.

## 2. Get the full text

Build the page from the full text, never from a summary.

| Material | Do this |
|---|---|
| A static web page (article, blog post, essay) | Download it with `curl` and strip the tags locally (commands below) |
| A GitHub gist or repo file | Download the raw text: drop the `#file-…` part of a gist URL and append `/raw`; for a repo file, use its `raw.githubusercontent.com` URL |
| A page that needs JavaScript or a login (e.g. a post on X) | A web-reading helper skill, with the user's consent (§5). Without one, ask the user to save the page as PDF |
| A PDF | `pdftotext -layout`. If it is not installed, read the PDF in chunks of at most 20 pages |
| Markdown, plain text, pasted text | Read it directly |

```bash
T=$(mktemp -d)   # temporary; delete it after the page is built: rm -rf "$T"
curl -sL -o "$T/page.html" "<url>"
python3 - "$T/page.html" > "$T/page.txt" <<'EOF'
import html, re, sys
s = open(sys.argv[1], encoding="utf-8", errors="replace").read()
s = re.sub(r"<!--[\s\S]*?-->|<(script|style|nav|header|footer)\b[\s\S]*?</\1>", " ", s, flags=re.I)
s = re.sub(r"<(br|p|div|h[1-6]|li|tr)\b[^>]*>", "\n", s, flags=re.I)
s = html.unescape(re.sub(r"<[^>]+>", " ", s))
print(re.sub(r"\n\s*\n+", "\n\n", re.sub(r"[ \t]+", " ", s)).strip())
EOF
pdftotext -layout "<file.pdf>" "$T/doc.txt"
wc -w "$T"/*.txt                 # material length
```

- Fetch tools that answer through a model (e.g. WebFetch in Claude Code) return a summary, not the text, and may refuse to reproduce a long article. Use them only for a quick outline, or when `curl` is blocked. If the page then rests on a summary, say so in the report.
- Check that the text is complete: its last paragraph matches the end of the article, and the word count is plausible.
- `pdftotext` can turn rare glyphs into `�` (e.g. the `@` in a handle). Check every quote against the PDF.

## 3. Outline, candidate questions, and long material

In document mode, the confirmation (SKILL.md step 4, item 1) always shows:

- **The outline:** each section heading of the material with its approximate length.
- **5–8 candidate questions**, numbered, phrased as the reader would ask them and taken from the material's sections. Users often only say "make this easier to read", so let them pick questions instead of writing them.

Put the outline and the numbered candidates in the message text. A structured question tool allows few options per question (4 in `AskUserQuestion`), so do not spend one option per candidate: offer the recommended set (e.g. "1, 2, 3, 5"), one or two alternative sets, and let the user type their own numbers. This keeps the other questions free for tier, language and path, and helpers.

If the material is longer than about 3,000 words (about 6,000 CJK characters), it does not fit one page budget (`writing-rules.md`). Also offer two ways to cover it:

| Choice | Result | Cost |
|---|---|---|
| **Question-driven** | One page answers the 3–5 chosen questions. Everything else is a link to the original | 1 page |
| **Faithful guided reading** | A page tree from the first build: a hub page plus up to about 6 child pages, named and linked as in `extending-pages.md`. Every section of the material maps to a section of some page | 1 + children |

## 4. Citing and quoting

- Cite each fact by the material's section heading or PDF page in a `.src` line, e.g. "Source: *LLM Wiki*, § Architecture". Put the full URL or file path in Sources.
- Explain in your own words. Quote at most two sentences at a time, in quotation marks, with the source. Never reproduce whole sections.
- An opinion in the material is the author's opinion. Write it as such ("Karpathy proposes …"), not as an established fact.
- A number from the material is a fact with a source. A number you add from elsewhere is general background and is labelled so.

## 5. Helper skills

The platform lists the installed skills, with names and descriptions, in your context. Before the confirmation, check that list for a skill that does the job better than the built-in method in §2. Do not search the file system for skills and do not install anything.

| Capability | Typical examples (names differ between installs) | Worth proposing when |
|---|---|---|
| Read web pages | a browser skill or tool (e.g. `chrome-browser`, `built-in-browser`), a fetch MCP server | the page needs JavaScript or a login |
| Read PDFs | a PDF skill (e.g. `pdf`) | the PDF has tables, scanned pages, or text that `pdftotext` garbles |

Rules:

- Name each helper and the step it is for in the confirmation (SKILL.md step 4, item 4). Use it only if the user agrees. If no helper is listed or the user declines, use the built-in method.
- A helper only gets the material. Page structure, writing rules, and the self-check still come from this skill.
- Keep a helper's intermediate files in a temporary directory and delete them afterwards. If the helper asks the user its own questions, say so in the confirmation.
- Report which helpers you used, or which built-in method you fell back to.
