# Sources and Licenses

How to get an image and its license from each source. The classes and what they allow are in `../SKILL.md` § License classes. `C` is the path to `scripts/cite.py`, and `T` is a temporary folder outside the output directory.

## 1. Free-license libraries

`cite.py license` prints one record per image. With search words, it prints the first 5 results (`--limit N`).

```
$ python3 "$C" license commons "File:Differential drive.png"
title: File:Differential drive.png
author: Patrik at English Wikibooks
license: Public domain
class: free
page: https://commons.wikimedia.org/wiki/File:Differential_drive.png
image: https://upload.wikimedia.org/wikipedia/commons/2/28/Differential_drive.png?…
image_size: 596x443
```

Download the `image` URL into `$T`. Wikimedia refuses a request with no User-Agent. Do not put an email address or a name in it:

```bash
curl -sSL -A 'explainer-cite (explain-as-webpage plugin)' -o "$T/source.png" '<image URL>'
```

| Library | Query | What to know |
|---|---|---|
| Wikimedia Commons | `commons "File:Name.jpg"`, or search words | Use the printed `image` URL. A thumbnail URL you build yourself returns HTTP 400, because Commons accepts only standard widths. The file can be wider than 1440px; `prepare` shrinks it. |
| Openverse | `openverse "<words>"` | The query asks only for CC0, public domain, CC BY, and CC BY-SA. The search endpoint can stop answering for a while. The command then exits with a timeout: use Commons instead. |
| NASA Image and Video Library | `nasa "<words>"` | NASA has no license field. The record is `Public domain` unless the description's `Credit:` names someone else; then it is `unknown`. `image` is a medium size. `sizes` is a JSON list of the file's sizes (`~orig`, `~large`, `~medium`). |

## 2. Public web pages

Capture only a page that anyone can open. The site's copyright notice gives the license. With no open license, the screenshot is restricted, so it needs its own row in the confirmation.

```bash
google-chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size=720,900 --virtual-time-budget=5000 --screenshot="$T/page.png" "<URL>"
python3 "$C" prepare "$T/page.png" <hub>.assets/<name>.webp --kind flat --crop X,Y,W,H
```

- The scale factor 2 gives a file 1440px wide. `--crop` values are pixels of that file.
- Look at the screenshot before you crop. A cookie wall or a login form in it means stop. Do not crop it away.
- A screenshot can show private data or the names of other people. Crop to the interface the page discusses.

## 3. Images in the user's material

**A PDF figure.** Render the page at low resolution to find the figure, then crop at 300 dpi. Coordinates scale with the resolution: a value at `-r 300` is 5 times the value at `-r 60`.

```bash
pdftoppm -f 1 -l 1 -r 60 -png -singlefile paper.pdf "$T/page"     # read the position from this image
pdftoppm -f 1 -l 1 -r 300 -x 1275 -y 840 -W 1125 -H 690 -png -singlefile paper.pdf "$T/fig"
python3 "$C" prepare "$T/fig.png" <hub>.assets/<name>.webp --kind flat
```

A PDF can hold a photo as one embedded image. `pdfimages` gives that image at its own resolution:

```bash
pdfimages -list -f 1 -l 3 paper.pdf                  # width, height, and type of each image
pdfimages -png -f 2 -l 2 paper.pdf "$T/img"
```

**The license of a paper.** The license of the paper is the license of its figures, unless a figure's caption says otherwise (for example, "reprinted from …").

| Paper | Command | What to know |
|---|---|---|
| has a DOI | `license crossref <doi>` | Journal pages often refuse `curl`, and Crossref does not. No `license` in the record means unknown. |
| on arXiv | `license arxiv <id>` | The default arXiv license does not allow changes, so it prints `restricted`. The authors' repository can hold the same figure under a free license. |

For a figure's caption in a paper on PubMed Central, read the full-text XML from Europe PMC: `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML`.

**A file in a project.** Copy it from the repository. The user's own project belongs to the user. For someone else's repository, read its `LICENSE`. An image with no license of its own falls under the repository's license, and the source line says so.

## 4. No Pillow

`prepare` needs Pillow to write WebP. Without it, `prepare` prints commands that give a PNG, and the check for 200 KB can then fail. Say so in the confirmation. Installing Pillow is the user's decision.

## 5. The source line

- An author's name goes first, as the source gives it. With more than two authors, write the first and "et al."
- A library's page, not the image file, is the link: the page shows the license.
- State every change this page made: `Cropped by this page.`, `Annotations added by this page.`
- With CC BY-SA, a changed image stays under CC BY-SA: `Cropped by this page; released under CC BY-SA 4.0.`
- A restricted image the user accepted says so in Sources: the license, and that the user chose to use it.
