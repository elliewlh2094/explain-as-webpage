#!/usr/bin/env python3
"""Cited images of explainer pages (explainer-cite SKILL.md).

  license SOURCE QUERY  who made an image and under which license
  prepare SRC OUT.webp  crop, shrink, and compress one image
  check HUB.html        the asset check of one topic; prints nothing when it passes

Standard library only. prepare uses Pillow when it is installed, and prints fallback commands when not.
"""
import argparse
import glob
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "explainer-cite (explain-as-webpage plugin)"  # Wikimedia refuses requests without one. No personal data.
FREE = re.compile(r"^(cc0|public domain|cc[ -]by([ -]sa)?([ -]\d|$))", re.I)
MAX_WIDTH, MAX_KB, MAX_HEIGHT, MAX_FOLDER_KB, COLUMN = 1440, 200, 540, 1024, 720


# ---- license ----

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def show(**fields):
    """One record. The class is restricted unless the license name is a known free one."""
    for k, v in fields.items():
        if v:
            print(f"{k}: {v}")
        if k == "license":
            print("class:", "free" if FREE.match(v) else "restricted")
            if re.search(r"\bnd\b", v, re.I):
                print("note: no derivatives, so whole image only: no crop, no annotation")
    print()


def cc_name(url):
    """The license name of a Creative Commons URL, or the URL itself."""
    m = re.search(r"creativecommons\.org/(?:licenses/([a-z-]+)/([\d.]+)|publicdomain/(zero|mark))", url)
    if not m:
        return url
    if m[3]:
        return "CC0" if m[3] == "zero" else "Public domain"
    return f"CC {m[1].upper()} {m[2]}"


def commons(q, limit):
    p = dict(action="query", format="json", prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=MAX_WIDTH)
    if q.startswith("File:"):
        p["titles"] = q
    else:  # filetype:bitmap leaves out SVG, audio, and video files
        p.update(generator="search", gsrnamespace=6, gsrsearch=q + " filetype:bitmap", gsrlimit=limit)
    pages = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)))
    for page in pages.get("query", {}).get("pages", {}).values():
        if "imageinfo" not in page:
            sys.exit(f"not found on Commons: {page.get('title', q)}")
        i = page["imageinfo"][0]
        meta = i.get("extmetadata", {})

        def field(key):  # Artist and others are HTML
            return html.unescape(re.sub(r"<[^>]+>", "", meta.get(key, {}).get("value", ""))).strip()

        show(title=page["title"], author=field("Artist"), license=field("LicenseShortName") or "unknown",
             license_url=field("LicenseUrl"), page=i["descriptionurl"],
             # A file narrower than the request comes unscaled, while thumbwidth still says the requested width.
             image=i.get("thumburl", i["url"]), image_size=f"{min(i.get('thumbwidth', i['width']), i['width'])}x{min(i.get('thumbheight', i['height']), i['height'])}")


def openverse(q, limit):
    p = dict(q=q, license="cc0,pdm,by,by-sa", page_size=limit)
    for r in json.loads(get("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(p)))["results"]:
        name = {"cc0": "CC0", "pdm": "Public domain"}.get(r["license"], f"CC {r['license'].upper()} {r['license_version']}")
        show(title=r.get("title"), author=r.get("creator"), license=name, license_url=r.get("license_url"),
             page=r.get("foreign_landing_url"), image=r.get("url"), image_size=f"{r.get('width')}x{r.get('height')}")


def nasa(q, limit):
    p = dict(q=q, media_type="image", page_size=limit)
    for item in json.loads(get("https://images-api.nasa.gov/search?" + urllib.parse.urlencode(p)))["collection"]["items"]:
        d = item["data"][0]
        # NASA has no license field. Its own images are public domain; a Credit that names someone else is not.
        credit = re.findall(r"Credits?:\s*([^\n<]+)", d.get("description", ""))
        credit = credit[-1].strip() if credit else ""
        name = "unknown" if credit and "nasa" not in credit.lower() else "Public domain"
        show(title=d.get("title"), author=d.get("photographer") or credit or d.get("center"), license=name,
             page=f"https://images.nasa.gov/details/{d['nasa_id']}", image=item["links"][0]["href"], sizes=item["href"])


def crossref(doi, _limit):
    w = json.loads(get("https://api.crossref.org/works/" + urllib.parse.quote(doi)))["message"]
    urls = [x["URL"] for x in w.get("license", []) if x.get("content-version") == "vor"] or [x["URL"] for x in w.get("license", [])]
    authors = [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in w.get("author", [])]
    show(title=(w.get("title") or [""])[0], author=", ".join(authors),
         license=cc_name(urls[0]) if urls else "unknown", license_url=urls[0] if urls else "", page=f"https://doi.org/{doi}")


def arxiv(arxiv_id, _limit):
    url = f"https://arxiv.org/abs/{arxiv_id}"
    page = get(url)

    def meta(name):
        return [html.unescape(v) for v in re.findall(rf'<meta name="citation_{name}" content="([^"]*)"', page)]

    m = re.search(r'class="abs-license"><a href="([^"]+)"', page)
    name = "unknown" if not m else "arXiv default license" if "arxiv.org/licenses" in m[1] else cc_name(m[1])
    show(title="".join(meta("title")), author="; ".join(meta("author")), license=name, license_url=m[1] if m else "", page=url)


# ---- prepare ----

def fallback(a, crop):
    """No Pillow: give the commands that still work. The result stays PNG, which is larger."""
    stem = os.path.splitext(a.out)[0]
    print("Pillow is not installed, so the output stays PNG and is larger than WebP. Say so in the confirmation; installing it is the user's decision.")
    if not crop:
        print(f"No crop: copy the file as it is.\n  cp '{a.src}' '{stem}{os.path.splitext(a.src)[1]}'")
        return
    x, y, w, h = crop
    print(f"PDF page: pdftoppm -f N -l N -r <dpi> -x {x} -y {y} -W {w} -H {h} -singlefile -png source.pdf '{stem}'")
    src = "file://" + os.path.abspath(a.src)
    print("Image (at least 500px wide, the narrowest Chrome window):")
    print(f"""  T=$(mktemp --suffix=.html); printf '<body style="margin:0"><img src="{src}" style="display:block;margin:-{y}px 0 0 -{x}px">' > "$T"
  google-chrome --headless=new --disable-gpu --hide-scrollbars --window-size={w},{h} --screenshot='{os.path.abspath(stem)}.png' "file://$T"; rm "$T\"""")


def prepare(a):
    crop = [int(v) for v in a.crop.split(",")] if a.crop else None
    try:
        from PIL import Image, ImageOps
    except ImportError:
        fallback(a, crop)
        return 0
    im = ImageOps.exif_transpose(Image.open(a.src))
    im = im.convert("RGBA" if im.mode in ("RGBA", "LA") or "transparency" in im.info else "RGB")
    if crop:
        x, y, w, h = crop
        im = im.crop((x, y, x + w, y + h))
    if im.width > a.width:
        im = im.resize((a.width, round(im.height * a.width / im.width)), Image.LANCZOS)
    im.save(a.out, "WEBP", quality=80)  # saving without exif= also drops the source's metadata
    if a.kind == "flat":  # line art is smaller lossy, PDF figures lossless: keep the smaller file
        lossy = os.path.getsize(a.out)
        tmp = a.out + ".tmp"
        im.save(tmp, "WEBP", lossless=True)
        if os.path.getsize(tmp) < lossy:
            os.replace(tmp, a.out)
        else:
            os.remove(tmp)
    kb = os.path.getsize(a.out) / 1024
    ref = "/".join(os.path.abspath(a.out).split(os.sep)[-2:])
    print(f"{a.out}: {im.width}x{im.height}, {kb:.0f} KB")
    print(f'<img src="{ref}" alt="FILL" width="{im.width}" height="{im.height}">')
    shown = im.height * min(COLUMN, im.width) / im.width
    problems = []
    if kb > MAX_KB:
        problems.append(f"{kb:.0f} KB is over {MAX_KB} KB: crop tighter, or use a smaller --width")
    if shown > MAX_HEIGHT:
        problems.append(f"shown {shown:.0f} CSS px tall, over {MAX_HEIGHT}: crop to the part the page discusses")
    for p in problems:
        print(p, file=sys.stderr)
    return 1 if problems else 0


# ---- check ----

IMAGE = re.compile(r"<(?:img|image)\b[^>]*>", re.I)
REF = re.compile(r"""(?<![\w-])(?:src|href|xlink:href)\s*=\s*["']([^"']*)""", re.I)
FIGURE = re.compile(r"""<figure\b.*?</figure>(?:\s*<p class="src">.*?</p>)?""", re.S | re.I)
CREDIT = re.compile(r"(?:Image source|圖片來源)\s*[:：]\s*\S.*?(?:License|授權)\s*[:：]\s*\S", re.S | re.I)


def attr(tag, name):
    m = re.search(rf"""(?<![\w-]){name}\s*=\s*["']?(\d+)""", tag)
    return int(m[1]) if m else 0


def check_page(name, text, assets, used, say):
    text = re.sub(r"<!--.*?-->|<script\b.*?</script>", "", text, flags=re.S | re.I)
    for tag in IMAGE.findall(text):
        m = REF.search(tag)
        ref = m[1] if m else ""
        w, h = attr(tag, "width"), attr(tag, "height")
        if re.match(r"(https?:)?//", ref):
            say(f"{name}: external image: {ref}")
        elif not ref.startswith(assets + "/"):
            say(f"{name}: image outside {assets}/: {ref[:60]}")
        elif not os.path.isfile(ref):
            say(f"{name}: missing file: {ref}")
        else:
            used.add(ref[len(assets) + 1:])
        if w and h * min(COLUMN, w) / w > MAX_HEIGHT:
            say(f"{name}: {ref} is shown over {MAX_HEIGHT} CSS px tall")
    for block in FIGURE.findall(text):
        if IMAGE.search(block) and not CREDIT.search(re.sub(r"<[^>]+>", "", block)):
            fig = re.search(r"""<figure\b[^>]*\bid=["']([^"']+)""", block)
            say(f"{name}: {fig[1] if fig else 'a figure'}: no 'Image source: ... License: ...' in the caption or source line")
    if IMAGE.search(FIGURE.sub("", text)):
        say(f"{name}: an image outside a <figure>")


def check(a):
    os.chdir(os.path.dirname(os.path.abspath(a.page)))
    hub = os.path.basename(a.page).rsplit(".", 1)[0].split("--")[0]
    assets, used, lines = f"{hub}.assets", set(), []
    for page in [f"{hub}.html"] + sorted(glob.glob(f"{hub}--*.html")):
        with open(page, encoding="utf-8") as f:
            check_page(page, f.read(), assets, used, lines.append)
    if os.path.isdir(assets):
        total = 0
        for f in sorted(os.listdir(assets)):
            kb = os.path.getsize(os.path.join(assets, f)) / 1024
            total += kb
            if f not in used:
                lines.append(f"{assets}/{f}: no page uses it")
            if kb > MAX_KB:
                lines.append(f"{assets}/{f}: {kb:.0f} KB is over {MAX_KB} KB")
        if total > MAX_FOLDER_KB:
            lines.append(f"{assets}/: {total:.0f} KB is over {MAX_FOLDER_KB} KB")
    print("".join(line + "\n" for line in dict.fromkeys(lines)), end="")  # two uses of one missing file: one line
    return 1 if lines else 0


def main():
    ap = argparse.ArgumentParser(description="Cited images of explainer pages (explainer-cite SKILL.md).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("license", help="print author, license, class, and links")
    s.add_argument("source", choices=["commons", "openverse", "nasa", "crossref", "arxiv"])
    s.add_argument("query", help="commons: File:Name.jpg or search words; openverse, nasa: search words; crossref: a DOI; arxiv: an id")
    s.add_argument("--limit", type=int, default=5, help="results of a search (default 5)")
    s = sub.add_parser("prepare", help="crop, shrink, and compress one image to WebP")
    s.add_argument("src")
    s.add_argument("out", help="<hub>.assets/<name>.webp")
    s.add_argument("--kind", choices=["photo", "flat"], default="photo", help="flat: screenshot, line art, or PDF figure")
    s.add_argument("--crop", help="X,Y,W,H in source pixels")
    s.add_argument("--width", type=int, default=MAX_WIDTH, help=f"largest width (default {MAX_WIDTH})")
    s = sub.add_parser("check", help="the asset check of the topic of one page")
    s.add_argument("page")
    a = ap.parse_args()
    if a.cmd == "license":
        try:
            globals()[a.source](a.query, a.limit)
        except (urllib.error.URLError, TimeoutError) as e:
            sys.exit(f"{a.source}: {e}")
        return 0
    return prepare(a) if a.cmd == "prepare" else check(a)


if __name__ == "__main__":
    sys.exit(main())
