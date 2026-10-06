# Icons

`assets/icons/lucide.svg` holds 106 icons from one library, Lucide (lucide-static 1.52.0, ISC License; some icons come from Feather, MIT License; full text in `assets/icons/LICENSE`). Every icon is a 24×24 line drawing with the same stroke, so icons from this file always look like one set. Do not mix in icons from other libraries, and do not download icons while building a page.

An icon helps the reader recognise a thing at a glance: a rocket, a database, a person. It never replaces the label. Use an icon only next to a label that names the same thing.

## Names

| Group | Icons |
|---|---|
| Files and code | `file` `file-text` `file-code` `file-type` `files` `folder` `archive` `inbox` `notebook` `book-open` `code` `terminal` `git-branch` `git-commit-horizontal` `package` `puzzle` `list-tree` `list-checks` |
| Computing and data | `cpu` `server` `database` `cloud` `network` `app-window` `smartphone` `mouse-pointer` `bot` `brain` `sparkles` `chart-line` `chart-column` `gauge` `settings` `search` `link` `lock` `key` `shield` `shield-check` |
| People and messages | `user` `users` `message-square` `circle-help` `info` `triangle-alert` `id-card` `pencil` `tag` |
| Status and time | `check` `x` `circle-check` `circle-x` `clock` `timer` `hourglass` `refresh-cw` `play` `target` `trophy` `scale` `layers` `lightbulb` `eye` `image` `camera` `palette` `gamepad-2` `move-3d` `square-dashed` `box` |
| Science and body | `flask-conical` `microscope` `activity` `heart` `heart-pulse` `droplet` `glass-water` `pill` `bone` `thermometer` |
| Space and industry | `rocket` `satellite` `earth` `globe` `moon` `sun` `flame` `fuel` `factory` `tower-control` `wrench` `recycle` `weight` `coins` `banknote` |
| Home and emergency | `house` `backpack` `flashlight` `battery-full` `briefcase-medical` `radio` `siren` `map` `tent` `utensils` `shirt` |

To find an icon, search the file: `grep -o 'id="i-[a-z0-9-]*"' assets/icons/lucide.svg`. Organs, cells, and other shapes that are not in the set are drawn as pictorial figures, not icons.

## Use an icon

Give the reference the class `icon`. Its colour is the text colour, or the concept colour when the element or its card has a class `c1`–`c5`.

| Where | Markup |
|---|---|
| Inside an SVG figure | `<use href="#i-rocket" class="icon" x="162" y="132" width="20" height="20"/>` |
| Next to a card title or a word in the text | `<svg class="icon" aria-hidden="true"><use href="#i-rocket"/></svg>Booster` |

- In SVG, use 20×20 next to 14px text and 24×24 at most; put x and y on the 10px grid when you can. Leave 10px between the icon and its label.
- In a figure, give the icon the concept class of the part it marks (`class="icon c1"`), or none.
- The SVG's `aria-label` already describes the figure; the icon adds nothing to it. In HTML, keep `aria-hidden="true"` because the label next to it carries the meaning.

## Copy the symbols into the page

The page holds only the icons it uses, between `<!-- icons:start -->` and `<!-- icons:end -->` in its hidden `<svg><defs>`. After the figures are drawn, run this command. It reads every `href="#i-…"` on the page, copies those symbols and the license notice from the icon file into that block, removes symbols the page no longer uses, and prints the names that the set does not have. Run it again after every change to the icons. It prints nothing when every icon is found.

```bash
S=<this skill's folder>/assets/icons/lucide.svg
python3 - "$F" "$S" <<'EOF'
import re, sys
page, sprite = (open(p, encoding="utf-8").read() for p in sys.argv[1:3])
notice = re.match(r"<!--.*?-->", sprite, re.S).group(0)
symbols = {n: line for line, n in re.findall(r'(?m)^(<symbol id="i-([\w-]+)".*</symbol>)$', sprite)}
head, rest = page.split("<!-- icons:start -->"); _, tail = rest.split("<!-- icons:end -->")
used = sorted(set(re.findall(r'href="#i-([\w-]+)"', head + tail)))
for n in used:
    if n not in symbols: print("missing:", n)
found = [symbols[n] for n in used if n in symbols]
block = "\n".join([notice] + found) + "\n" if found else ""
open(sys.argv[1], "w", encoding="utf-8").write(head + "<!-- icons:start -->" + block + "<!-- icons:end -->" + tail)
EOF
```

If a name is missing, choose another icon from the table, or leave the label without an icon. Do not draw an icon by hand in the icon style.

## Adding icons to the set (maintainers)

Take the file `icons/<name>.svg` from the same version of the `lucide-static` npm package, and add its inner elements as one line, `<symbol id="i-<name>" viewBox="0 0 24 24">…</symbol>`, in alphabetical order. Add the name to the table above. When you change the version, update it in the notice at the top of `lucide.svg` and here.
