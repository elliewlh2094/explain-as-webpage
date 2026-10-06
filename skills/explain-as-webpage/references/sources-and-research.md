# Sources and Research

How to read material that is not the user's project, how to research a topic the user only names, how to cite and grade sources, and when to use a helper skill. SKILL.md step 1 sends you here in document and topic modes.

## 1. Modes and output path

| Mode | The user gives | Default output path |
|---|---|---|
| project | a repo, report, or code path | `~/Documents/explainers/<repo-name>/<topic-slug>.html` |
| document | a web article URL, a PDF, a Markdown or text file, or pasted text | `~/Documents/explainers/<topic-slug>/<topic-slug>.html` |
| topic | only a topic and questions | same as document |

- The mode follows the material, not the current directory. A document read while the agent works inside some repo still uses the document path. If the sandbox cannot write to that path, still propose it and say that writing there needs the user's approval; do not move the output into a folder of the current repository.
- If the user also asks questions the document does not answer, say so in the confirmation, and research them as in topic mode (§7), or leave them out.
- Material you cannot read (a video, a paywalled paper, a login-only page) is not a reason to stop: propose a way to get its text (§2, *Material you cannot read*). Do not download subtitles or work around access yourself.

## 2. Get the full text

Build the page from the full text, never from a summary.

| Material | Do this |
|---|---|
| A static web page (article, blog post, essay) | Download it with `curl` and strip the tags locally (commands below) |
| A GitHub gist or repo file | Download the raw text: drop the `#file-…` part of a gist URL and append `/raw`; for a repo file, use its `raw.githubusercontent.com` URL |
| A page that needs JavaScript (the downloaded HTML has no article text) | Look for the public data the page loads: an API base URL in the HTML or in the small scripts it loads (e.g. `environment.js` on spacex.com names `cmsBaseUrl`), then download the JSON. For Wikipedia, use the MediaWiki API (below) |
| A page that needs a login, or a JavaScript page with no public data (e.g. a post on X) | A web-reading helper skill, with the user's consent (§5). Without one, ask the user to save the page as PDF |
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

- Wikipedia as plain text: `curl -sG "https://en.wikipedia.org/w/api.php" --data-urlencode "titles=<Page_title>" -d action=query -d prop=extracts -d explaintext=1 -d format=json -d redirects=1`. The text is in `query.pages.*.extract`.
- `curl` error 60 (`unable to get local issuer certificate`) on a site that opens in a browser usually means the server does not send its intermediate certificate (seen on several Taiwan government sites). Never switch off verification (`-k`). Add the missing certificate instead: its URL is in the site certificate (Authority Information Access, `CA Issuers`).

  ```bash
  H=<host>
  timeout 20 openssl s_client -connect "$H:443" -servername "$H" </dev/null 2>/dev/null | openssl x509 -noout -ext authorityInfoAccess   # prints CA Issuers - URI:…
  curl -s -o "$T/inter.crt" "<CA Issuers URI>"
  openssl x509 -inform DER -in "$T/inter.crt" -out "$T/inter.pem" 2>/dev/null || cp "$T/inter.crt" "$T/inter.pem"
  cat /etc/ssl/certs/ca-certificates.crt "$T/inter.pem" > "$T/bundle.pem"   # macOS: /etc/ssl/cert.pem
  curl -sL --cacert "$T/bundle.pem" -o "$T/page.html" "<url>"
  ```
- Fetch tools that answer through a model (e.g. WebFetch in Claude Code) return a summary, not the text, and may refuse to reproduce a long article. Use them only for a quick outline, or when `curl` is blocked. If the page then rests on a summary, say so in the report.
- Check that the text is complete: its last paragraph matches the end of the article, and the word count is plausible.
- `pdftotext` can turn rare glyphs into `�` (e.g. the `@` in a handle). Check every quote against the PDF.

### Material you cannot read

When the user names material you cannot read (a video or a podcast, a paper behind an institution's paywall, a private or login-only page), say why in the confirmation and propose ways to get it, the highest fidelity first. Never try to get around a paywall or a login yourself; the user decides what they can legitimately access.

| Order | The user provides | Example | Treat it as |
|---|---|---|---|
| 1 | The full text, obtained with their own access | the paper's PDF from their library; the page saved as PDF | the material itself (the table above) |
| 2 | A transcript or an export of the original | a video's subtitle file; a meeting transcript | the material's text; the page says it is a transcript |
| 3 | Notes made by an AI tool that can read the original | NotebookLM notes on a YouTube video or on a paper | secondary (grade g3, §8); the rules below |

For order 3, give the user two or three prompts to ask the tool, so that the notes follow the original and keep positions. For example: "List each part of the video in order, with its title and timestamp." and "For each part, say what it covers; keep quotes, code, and numbers, with timestamps." Notes that only answer broad questions ("is it worth watching", "what is the main claim") repeat each other and cannot be cited.

When the page is built from AI notes:

- Put a note box (title Note / 說明) under the conclusion: the page is built from the tool's notes on the original, not from the original.
- In Sources, grade the notes g3 and list the original with "not read directly".
- Cite the notes by their section headings, and the original's positions (timestamps, pages) where the notes give them. If they give none, say so in the note box.
- Keep the content apart: separate the tool's own judgements (e.g. "well worth watching", advice the notes do not attribute to the author) from the original's content. Leave them out, or list them under Limits as the tool's addition.
- Check technical facts (API names, formulas, numbers) against primary sources, such as the official documentation or the paper, as a light pass (§7).

## 3. Outline, candidate questions, long material, and plans

In document mode, the confirmation (SKILL.md step 4, item 1) always shows:

- **The outline:** each section of the material with its approximate length. Use the original's own structure: its chapters, sections, or the steps of a tutorial. When the text you read is an intermediary (AI notes, a summary) whose headings are its own questions, take the structure from what it reports about the original (e.g. "Step 1–5"), not from its headings. If it does not show the structure, say so and suggest the prompts in §2.
- **5–8 candidate questions**, numbered, phrased as the reader would ask them and taken from the material's sections. Users often only say "make this easier to read", so let them pick questions instead of writing them.
- **How to organise the page**, whatever the length:

  | Choice | Result | Suggest it when the request says |
  |---|---|---|
  | **The material's own order** | one `h2` per section of the original, in its order, so the reader can follow and review it: a single page for short material, a page tree for long material (below) | review, notes, guide me through, follow along |
  | **Question-driven** | one page that answers the 3–5 chosen questions; everything else is a link to the original | "I don't understand X", "why does it …" |

Put the numbered candidates inside the question itself: in the question text, or in the option descriptions. Text written before a structured question tool can go unseen, for example when the user interrupts the tool and answers in a message. A structured question tool allows few options per question (4 in `AskUserQuestion`), so do not spend one option per candidate: offer the organisation choice and the question sets as options of one question (e.g. "In the material's order (7 sections)", "Questions 1, 2, 3, 5"), and let the user type their own numbers. This keeps the other questions free for tier, language and path, and helpers.

If the material is longer than about 3,000 words (about 6,000 CJK characters), it does not fit one page budget (`writing-rules.md`). The material's own order then becomes **faithful guided reading**: a page tree from the first build, a hub page plus up to about 6 child pages, planned and built as in `extending-pages.md` §6. Every section of the material maps to a section of some page. Say the page count in the option (e.g. "In the material's order: hub + 5 pages").

If the material is a plan (stages with tasks and checks, `page-types.md` § Roadmap and plan pages), offer one child page per stage whatever its length, and ask whether to expand its units into steps (§6). For a plan, the recommended answer to both is yes.

## 4. Citing and quoting

- Cite each fact by the material's section heading or PDF page in a `.src` line, e.g. "Source: *LLM Wiki*, § Architecture". Put the full URL or file path in Sources.
- Explain in your own words. Quote at most two sentences at a time, in quotation marks, with the source. Never reproduce whole sections.
- An opinion in the material is the author's opinion. Write it as such ("Karpathy proposes …"), not as an established fact.
- A number from the material is a fact with a source. A number you add from elsewhere is general background and is labelled so.
- When you check a name (an API, a function, a standard) against a primary source and it has no entry for it, write what the source does list ("the 2021.3 documentation lists `FindWithTag`, which returns one active GameObject with the tag"), not that the name does not exist. A missing page is not proof.

## 5. Helper skills

The platform lists the installed skills, with names and descriptions, in your context. Before the confirmation, check that list for a skill that does the job better than the built-in method in §2. Do not search the file system for skills and do not install anything.

| Capability | Typical examples (names differ between installs) | Worth proposing when |
|---|---|---|
| Read web pages | a browser skill or tool (e.g. `chrome-browser`, `built-in-browser`), a fetch MCP server | the page needs JavaScript or a login |
| Read PDFs | a PDF skill (e.g. `pdf`) | the PDF has tables, scanned pages, or text that `pdftotext` garbles |
| Research | a research skill (e.g. `deep-research`) | the user picks deep research in topic mode (§7) |

Rules:

- Before proposing a helper, check that it can run here: the tools or libraries its instructions use are installed (e.g. `python3 -c "import pdfplumber"`, `command -v pdftotext`). If it needs an install, say so in the confirmation; installing is the user's decision (ask first), and a helper that falls back to the built-in method adds nothing.
- Name each helper and the step it is for in the confirmation (SKILL.md step 4, item 4). Use it only if the user agrees. If no helper is listed or the user declines, use the built-in method.
- A helper only gets the material. Page structure, writing rules, and the self-check still come from this skill.
- Keep a helper's intermediate files in a temporary directory outside the repository and the output directory, and delete them afterwards, including files its subagents download (e.g. under `/tmp`; check what a folder holds before deleting it). A research helper may by default write notes and a report into the current directory and spawn several subagents: point it at the temporary directory, and say in the confirmation that it runs subagents and takes longer (minutes, not seconds). If the helper asks the user its own questions, say so in the confirmation.
- Check a helper's numbers against its own notes before using them; a summary can disagree with the notes it summarises.
- Report which helpers you used, or which built-in method you fell back to.

## 6. Expanding material into steps

A plan or a guide often says what to do but not how. When the user agrees in the confirmation, add the how:

- Keep the material's goals, tasks, and checks unchanged. The added content explains them; it does not replace or extend them.
- Label it. Every page with added content carries a note box (`admonition`, title Note / 說明, `writing-rules.md` fixed labels) that says which fields come from the material, which are general practice, and the versions assumed (e.g. Ubuntu 24.04, ROS 2 Jazzy, C++17). The Sources section repeats this in one line.
- Use the official way: commands, file layouts, and APIs as the official documentation for that version describes them. Keep excerpts within the limits in `writing-rules.md`.
- Verify what can break. If a web tool is available, check version-specific commands and APIs against the official documentation, as a light research pass (§7); otherwise say in the report that they are unverified.
- Do not add numbers the material does not give (prices, durations, results), except as labelled general background.

## 7. Topic mode: research

The user names a topic and asks questions, with no material. The page is then built from sources you find.

1. **Primary sources first.** Look for the paper, the official documentation or repository, the standard, or the responsible agency. Once found, read each one as a document (§2) and cite it by heading or page. Search results and summaries point to sources; they are not sources.
2. **Scan before the confirmation.** Run a few searches, just enough to draft the outline and the candidate questions (§3). Do not build from the scan.
3. **Ask for the depth in the confirmation** (SKILL.md step 4, item 4):

   | Depth | Sources | Rule |
   |---|---|---|
   | Light | about 5–10 | Primary or authoritative sources first (§8). Every key claim has a source |
   | Deep | more | Every key claim has at least two independent sources. Where sources disagree, the page says so. Also ask whether to save the notes as `<topic-slug>.research.md` next to the page; the default is no |

   A research helper skill (e.g. `deep-research`) can run the deep pass, with the user's consent (§5).
4. **No web tool:** say so in the confirmation and ask the user for material. Never fall back silently to writing from memory.
5. **Your own knowledge** may connect and explain sourced facts, labelled as general background. It is never the only support for a key claim.
6. **Record the access date** of every source as you read it.
7. **Fast-moving topics** (a launch programme, a young technique): the conclusion box says "as of <date>".
8. **Every case you cite traces to a sentence.** Before a real-world case goes on the page ("the team tested one nail and went back to two"), find the sentence in the source that says it. Summarising a source in your own words is fine; adding an outcome the source does not state is not.

## 8. Source grades

In topic mode, every item in Sources carries a grade and an access date. Grades are optional in document and project modes.

| Grade | Class | English | 繁體中文 | Typical sources |
|---|---|---|---|---|
| 1 | `grade g1` | Primary | 原始材料 | the paper, the official documentation or code, the user's own material |
| 2 | `grade g2` | Authoritative | 權威或同儕審查 | standards bodies, government agencies, professional societies, peer-reviewed reviews, textbooks |
| 3 | `grade g3` | Secondary | 二手整理 | tutorials, blog posts, news articles, encyclopedias |
| 4 | `grade g4` | Emerging | 新興或個人說法 | one person's post or talk, a newly coined term, a preprint nobody has followed up |

- Write each Sources item on one line, so the self-check can read it: `<li><span class="grade g1">原始材料</span> Author, <a href="…">title</a> — what was taken. 存取日期 2026-10-03</li>`.
- A claim that only grade 4 sources support goes in an Emerging view box (`admonition`, title Emerging view / 新興說法) that names who makes it. Do not write it as settled.
- When grade 1–2 sources disagree, say so in the section, with both sources.

## 9. High-risk topics

Health and medicine, emergency preparedness and personal safety, law, and personal finance are high-risk: a wrong page can hurt the reader. For these topics, in any mode:

- **Authoritative sources only** for every claim the reader could act on: grade 1–2 (§8), such as government agencies, professional societies, and clinical or official guidelines. For readers in Taiwan, prefer Taiwan's own agencies and societies (for example the Ministry of Health and Welfare and its Health Promotion Administration, the National Fire Agency, the Central Weather Administration) and add international sources only where they agree or fill a gap.
- **Research is required.** Offer light or deep research in the confirmation, never "from memory". Say in the confirmation that the topic is high-risk and the page will carry a caution box.
- **A caution box** (`admonition danger`, title Caution / 注意) right after the conclusion box: the page is general information, does not replace a professional (a doctor, a lawyer, the local authority), and says when to contact one.
- **No individual advice:** no doses, no "stop taking X", no advice for one person's legal or financial case. Name the kinds of treatment or options and what they do; leave choices to the professional.
- **Medical topics** have a section "When should I see a doctor?" with the warning signs the sources list, including when it is urgent.
- **Guidance that changes** (recommended supplies, regulations): the conclusion box says "as of <date>", and Sources record access dates (§8).
