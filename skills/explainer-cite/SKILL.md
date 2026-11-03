---
name: explainer-cite
description: Cites an existing raster image on an explainer-page page. It takes the image from a free-license library, a public web page, or the user's material, checks its license, crops and compresses it into the topic's asset folder, and annotates it. Used only by the explainer-page skill, which reads this file when a figure brief has the type "cited image". Not for general image search, download, or editing.
disable-model-invocation: true
user-invocable: false
---

# Explainer Cite

## Overview

Most figures are drawn (`../explainer-figure/SKILL.md`). This skill covers the figures where the reader must see the real thing. The input is one figure brief of the type "cited image". The output is an image file in `<hub>.assets/`, a `<figure id="fig-N">` element, and one source record.

The three skills must sit side by side in the same `skills/` folder, because they refer to each other by relative paths.

## Cite or draw

Cite an image when:

- the reader must recognise a real thing (a specific machine, place, organ, or product), and a drawn object could only show a generic shape;
- the reader must find a place in a real interface (which button, which field);
- the page discusses that very image (a paper's result figure or architecture figure).

Draw the figure when it shows structure, a mechanism, a cause, or how symbols map to parts. A cited image can add to a mechanism figure. It does not replace one, because a photo does not show why something happens.

## Process

`C=<this skill's folder>/scripts/cite.py`. Run `python3 "$C" -h` for all options.

**Before the confirmation (explainer-page step 4):**

1. Pick the source and look up the license. Commands and fields are in `references/sources-and-licenses.md`.

   | Source | Get the license from |
   |---|---|
   | free-license library | `python3 "$C" license commons\|openverse\|nasa "<file or search words>"` |
   | public web page | the site's copyright notice; no open license means restricted. `references/sources-and-licenses.md` § 2 has the screenshot commands |
   | the user's material | PDF: `python3 "$C" license crossref <doi>`, or `arxiv <id>`; a project of the user's own: the user owns it |

2. Propose candidates for the user to choose from. Do not download images in bulk before the confirmation.
3. Write the source record now, not after the page is built: file name, author, title, license and its link, class, page link, and the changes this page makes.
4. Give explainer-page each image's origin and class for the confirmation. Each restricted image gets its own row: origin, license, use on the page, and the changes this page makes.

**After the confirmation (step 5):**

5. Put the source file in a temporary folder outside the output directory: `T=$(mktemp -d)`.
6. Crop, shrink, and compress it. `--kind photo` is the default; use `--kind flat` for a screenshot, line art, or a PDF figure. The command prints the file's size and an `<img>` tag.

   ```bash
   python3 "$C" prepare "$T/source.jpg" <hub>.assets/robot-sensors.webp --crop X,Y,W,H --width 1440
   ```

7. Place the image: § Figure, and `references/annotated-image.md` when the reader needs labels on it.
8. Run § Asset check, then delete `$T`.

## License classes

| Class | Licenses | What the page may do |
|---|---|---|
| free | CC0, public domain, CC BY, CC BY-SA; images in a repository under MIT, Apache-2.0, or BSD | crop, shrink, annotate |
| restricted | CC BY-NC, CC BY-ND, all rights reserved, unknown | only what the user agrees to in the confirmation |

`cite.py license` prints the class. It prints `restricted` for every license name it does not know. Check the name against this table before you use a `free` result.

- An ND image stays whole. Do not crop or annotate it. Shrink it only.
- Treat an unknown license as all rights reserved.
- An image in a repository with no license of its own falls under the repository's license. Write "under the repository's license" in the source line, because that is an inference. A photo from a dataset or another person may not fall under it, so the source line also says that its rights are unconfirmed.
- NASA has no license field. An image is restricted when its `Credit:` names someone else; `cite.py` handles this.

Stop at a login wall, paywall, or cookie wall. Use another source, or ask the user for the material (`../explainer-page/references/sources-and-research.md` § Material you cannot read).

## Asset folder

- `<hub>.assets/` sits next to the hub page. `<hub>` is the hub's file name without `.html`. A single page is its own hub.
- Every page of a topic uses the same folder. A child page also writes `src="<hub>.assets/…"`.
- Create the folder only for a page that cites an image. It holds only files that a page uses.
- Name a file in lowercase kebab-case after what it shows (`robot-sensors.webp`). Do not use the figure number: it changes when the page changes.
- Limits: width ≤ 1440px, each file ≤ 200 KB, shown height ≤ 540 CSS px, folder ≤ 1 MB. `prepare` and § Asset check report the numbers. Crop a tall image to the part the page discusses.
- Never embed an image as base64: two or three photos pass the 150 KB limit of the HTML file.

## Figure

Without labels, put the `<img>` tag from `prepare` in a `<figure>`. Replace `FILL` in `alt` with what the image shows, not the caption's words. The source line follows the figure directly:

```html
<figure id="fig-2">
<img src="robot.assets/robot-sensors.webp" alt="Two views of a four-wheeled robot: assembled, with a LIDAR on top, and from above, with its electronics." width="550" height="251">
<figcaption>Figure 2. The LIDAR sits above the body, so the body does not block its view.</figcaption>
</figure>
<p class="src">Image source: Guffanti et al., <a href="https://doi.org/10.3390/s25113553">Comparison of Two System Identification Approaches…</a>, Figure 1. License: <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</p>
```

The asset check reads the labels `Image source:` and `License:` (`圖片來源：` and `授權：` on a Traditional Chinese page). Add the changes this page made after the license: `Cropped by this page.` An image also gets a line in the page's Sources section, with the same author and license.

CC BY-SA continues after a change. Write: `Cropped by this page; released under CC BY-SA 4.0.`

## Asset check

Run it on any page of the topic. It prints nothing when every page and every file passes:

```bash
python3 "$C" check <hub>.html
```

It prints one line for each of these: an image that is external, missing, outside `<hub>.assets/`, outside a `<figure>`, or shown too tall; a figure with no author and license; a file in the folder that no page uses; a file or folder over its limit.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The image is on the web, so I can use it." | A page with no license is all rights reserved. List the image as restricted and let the user decide. |
| "I'll fill in the credit when the page is done." | The record gets lost, and the page then has an image with no author. Write it when you take the image. |
| "A cropped NC image is a new image." | A change does not remove the license. It stays restricted. |
| "The label is easier to read on the photo." | A photo has no fixed background colour, so the contrast is unknown. Put labels outside it. |
