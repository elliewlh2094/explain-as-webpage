#!/usr/bin/env python3
"""Parts library for drawn objects in explainer figures (references/pictorial.md § Drawn objects).

Each subcommand prints an SVG fragment that uses the template's object classes (ink, ink-edge,
ink-fill, ink-shade, ink-track). Sizes go straight into the coordinates; nothing uses scale(), so
every outline stays 4px. Objects are centred on (0, 0); objects with a front face +x.

  parts.py person --id f2-person --height 150 --cls c1     a person, front view, one outer outline
  parts.py robot  --id f3-robot --size 80 --view top       a wheeled robot, top or side view
  parts.py drone  --id f3-drone --size 120 --view top      a quadcopter, top or side view
  parts.py pill | rect | cylinder | ogive ...              basic shapes
  parts.py pose --ref f4-robot --path "M60 200 Q360 20 660 200" --at 0,.5,1 --angles t,t,90
  parts.py sheet > parts.svg                               the overview sheet of every part

Without --at, an object prints as a <g id> for the figure's <defs>; place it with
<use href="#ID" transform="translate(x y) rotate(a)"/>. With --at X,Y[,A] it prints placed.
"""
import argparse
import math
import re
import sys
from pathlib import Path


def n(v):
    """Round to 0.1 and drop a trailing .0, so the output is short and the same on every run."""
    v = round(v + 0.0, 1)
    return str(int(v)) if v == int(v) else str(v)


def pts(*xy):
    return " ".join(n(v) for v in xy)


def place(at):
    if not at:
        return ""
    x, y, *a = [float(v) for v in at.split(",")]
    rot = f" rotate({n(a[0])})" if a and a[0] else ""
    return f' transform="translate({n(x)} {n(y)}){rot}"'


def attrs(cls, extra=""):
    return f' class="{cls}"' + extra if cls else extra


# ---- basic shapes: each returns SVG element strings (without a class) ----

def rect_d(x, y, w, h, r=(0, 0, 0, 0)):
    """A rectangle path with its own radius per corner: top-left, top-right, bottom-right, bottom-left."""
    tl, tr, br, bl = [min(v, w / 2, h / 2) for v in r]
    d = f"M{pts(x + tl, y)} H{n(x + w - tr)}"
    d += f" A{pts(tr, tr)} 0 0 1 {pts(x + w, y + tr)}" if tr else ""
    d += f" V{n(y + h - br)}"
    d += f" A{pts(br, br)} 0 0 1 {pts(x + w - br, y + h)}" if br else ""
    d += f" H{n(x + bl)}"
    d += f" A{pts(bl, bl)} 0 0 1 {pts(x, y + h - bl)}" if bl else ""
    d += f" V{n(y + tl)}"
    d += f" A{pts(tl, tl)} 0 0 1 {pts(x + tl, y)}" if tl else ""
    return d + " Z"


def rect(x, y, w, h, r=(0, 0, 0, 0)):
    return f'<path d="{rect_d(x, y, w, h, r)}"/>'


def pill(cx, cy, w, h, angle=0):
    """A pill: a rectangle whose short ends are half circles."""
    rot = f' transform="rotate({n(angle)} {pts(cx, cy)})"' if angle else ""
    rr = min(w, h) / 2
    return f'<rect x="{n(cx - w / 2)}" y="{n(cy - h / 2)}" width="{n(w)}" height="{n(h)}" rx="{n(rr)}"{rot}/>'


def circle(cx, cy, r):
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}"/>'


def ellipse(cx, cy, rx, ry):
    return f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}"/>'


def polygon(*xy):
    return f'<polygon points="{" ".join(pts(xy[i], xy[i + 1]) for i in range(0, len(xy), 2))}"/>'


def cylinder(w, h):
    """An upright cylinder (a database, a tank): the body, then the top ellipse on it."""
    ry = min(w * 0.14, h / 4)
    x0, x1, top, bot = -w / 2, w / 2, -h / 2 + ry, h / 2 - ry
    body = f'<path d="M{pts(x0, top)} V{n(bot)} A{pts(w / 2, ry)} 0 0 0 {pts(x1, bot)} V{n(top)} Z"/>'
    return [body, ellipse(0, top, w / 2, ry)]


def ogive(w, h, nose):
    """A body with a pointed nose toward +x (a rocket stage, a missile, a bullet); w is the length."""
    x0, x1, r = -w / 2, w / 2 - nose, h / 2
    return f'<path d="M{pts(x0, -r)} H{n(x1)} Q{pts(x1 + nose * 0.75, -r)} {pts(w / 2, 0)} Q{pts(x1 + nose * 0.75, r)} {pts(x1, r)} H{n(x0)} Z"/>'


# ---- objects ----

def group(oid, cls, at, parts, shade=None):
    """parts: (class, elements) pairs in drawing order, each wrapped in <g class>; the pair ("SHADE", "")
    marks where the shade goes: shade = (clip rectangle (x, y, w, h), elements), drawn in ink-shade."""
    out = [f'<g id="{oid}"' + (f' class="{cls}"' if cls else "") + place(at) + ">"]
    for c, e in parts:
        if c != "SHADE":
            out.append(f'  <g class="{c}">{e}</g>')
        elif shade:
            (sx, sy, sw, sh), shapes = shade
            out.append(f'  <clipPath id="{oid}-shade"><rect x="{n(sx)}" y="{n(sy)}" width="{n(sw)}" height="{n(sh)}"/></clipPath>')
            out.append(f'  <g class="ink-shade" clip-path="url(#{oid}-shade)">{"".join(shapes)}</g>')
    out.append("</g>")
    return "\n".join(out)


def person(height):
    """Front view. Height = 5 head diameters. One outer outline: every part drawn as an 8px ink-edge
    layer, then covered by an ink-fill layer. Parts that must stay apart (head and torso, the two legs)
    keep a gap of at least 11px (2 × 4px outline + 3px), or the outline joins them."""
    if height < 100:
        sys.exit("person: --height must be at least 100; below that the legs and the neck join")
    k = height / 150
    r, cy = 14 * k, -61 * k
    top = cy + r + max(11 * k, 11)
    tw, bottom = 40 * k, 12 * k
    torso = rect(-tw / 2, top, tw, bottom - top, (10 * k, 10 * k, 0, 0))
    gap = max(12 * k, 11)
    lw = (tw - gap) / 2  # the outer edges of the legs line up with the sides of the torso
    legs = []
    for side in (-1, 1):
        x0 = gap / 2 if side > 0 else -gap / 2 - lw
        ly, foot = bottom - 6 * k, 75 * k - lw / 2
        legs.append(f'<path d="M{pts(x0, ly)} H{n(x0 + lw)} V{n(foot)} A{pts(lw / 2, lw / 2)} 0 0 1 {pts(x0, foot)} Z"/>')
    aw, al, sy = 12 * k, 56 * k, top + 9 * k
    arms = []
    for side in (-1, 1):
        sx = side * 13 * k
        rot = -25 * side
        arms.append(f'<rect x="{n(-aw / 2)}" y="{n(-aw / 2)}" width="{n(aw)}" height="{n(al)}" rx="{n(aw / 2)}" transform="translate({pts(sx, sy)}) rotate({rot})"/>')
    shapes = [circle(0, cy, r), torso] + legs + arms
    body = "".join(shapes)
    return [("ink-edge", body), ("ink-fill", body), ("SHADE", "")], ((0, -height, height, 2 * height), shapes)


def robot(size, view):
    """A wheeled robot facing +x. size = body length."""
    L = size
    if view == "top":
        w = 0.7 * L
        parts = [("ink dark", rect(-0.22 * L, -w / 2 - 0.1 * L, 0.44 * L, w + 0.2 * L, (0.04 * L,) * 4)),
                 ("ink", rect(-L / 2, -w / 2, L, w, (0.14 * L,) * 4)), ("SHADE", ""),
                 ("ink glass", circle(-0.08 * L, 0, 0.14 * L)),
                 ("ink dark", polygon(0.4 * L, 0, 0.24 * L, -0.11 * L, 0.24 * L, 0.11 * L))]
        return parts, ((-L, 0, 2 * L, L), [rect(-L / 2, -w / 2, L, w, (0.14 * L,) * 4)])
    body = rect(-L / 2, -0.32 * L, L, 0.36 * L, (0.08 * L,) * 4)
    parts = [("ink", rect(-0.14 * L, -0.5 * L, 0.14 * L, 0.2 * L)),
             ("ink glass", rect(-0.2 * L, -0.56 * L, 0.26 * L, 0.1 * L, (0.04 * L,) * 4)),
             ("ink", body), ("SHADE", ""),
             ("ink glass", rect(0.36 * L, -0.24 * L, 0.1 * L, 0.12 * L, (0.03 * L,) * 4)),
             ("ink dark", circle(-0.28 * L, 0.1 * L, 0.13 * L)), ("ink dark", circle(0.28 * L, 0.1 * L, 0.13 * L))]
    return parts, ((-L, -0.14 * L, 2 * L, L), [body])


def drone(size, view):
    """A quadcopter facing +x. size = span from rotor tip to rotor tip."""
    S = size
    if view == "top":
        c, rr = 0.3 * S, 0.2 * S
        arms = "".join(f'<rect x="0" y="{n(-0.03 * S)}" width="{n(c * math.sqrt(2))}" height="{n(0.06 * S)}" transform="rotate({a})"/>'
                       for a in (45, 135, 225, 315))
        rotors = [("ink glass", circle(sx * c, sy * c, rr)) for sx in (-1, 1) for sy in (-1, 1)]
        hubs = [("ink dark", circle(sx * c, sy * c, 0.035 * S)) for sx in (-1, 1) for sy in (-1, 1)]
        body = rect(-0.14 * S, -0.14 * S, 0.28 * S, 0.28 * S, (0.06 * S,) * 4)
        parts = [("ink", arms)] + rotors + hubs + [("ink", body), ("SHADE", ""),
                                                    ("ink dark", polygon(0.11 * S, 0, 0.03 * S, -0.06 * S, 0.03 * S, 0.06 * S))]
        return parts, ((-S, 0, 2 * S, S), [body])
    body = rect(-0.16 * S, -0.06 * S, 0.32 * S, 0.14 * S, (0.05 * S,) * 4)
    parts = [("ink dark", rect(-0.14 * S, 0.08 * S, 0.04 * S, 0.1 * S)), ("ink dark", rect(0.1 * S, 0.08 * S, 0.04 * S, 0.1 * S)),
             ("ink", rect(-0.42 * S, -0.08 * S, 0.84 * S, 0.04 * S)),
             ("ink dark", rect(-0.4 * S, -0.14 * S, 0.03 * S, 0.06 * S)), ("ink dark", rect(0.37 * S, -0.14 * S, 0.03 * S, 0.06 * S)),
             ("ink glass", ellipse(-0.385 * S, -0.16 * S, 0.12 * S, 0.025 * S)), ("ink glass", ellipse(0.385 * S, -0.16 * S, 0.12 * S, 0.025 * S)),
             ("ink", body), ("SHADE", ""), ("ink glass", circle(0.1 * S, 0.02 * S, 0.035 * S))]
    return parts, ((-S, 0.01 * S, 2 * S, S), [body])


# ---- pose ----

def parse_path(d):
    """Absolute M, L, H, V, Q, C only. Returns the control points of each command, and points
    sampled along the path, each as (x, y, command index, t within the command)."""
    toks = re.findall(r"[MLHVQCZ]|-?\d*\.?\d+(?:e-?\d+)?", d)
    cmds, out, i, cmd, cur = [], [], 0, None, (0.0, 0.0)
    while i < len(toks):
        if toks[i] in "MLHVQCZ":
            cmd = toks[i]
            i += 1
            if cmd == "Z":
                continue
        need = {"M": 2, "L": 2, "H": 1, "V": 1, "Q": 4, "C": 6}[cmd]
        v = [float(t) for t in toks[i:i + need]]
        i += need
        if cmd == "M":
            cur = (v[0], v[1])
            out.append((*cur, 0, 0.0))
            cmd = "L"
            continue
        if cmd in "LHV":
            end = (v[0], v[1]) if cmd == "L" else (v[0], cur[1]) if cmd == "H" else (cur[0], v[0])
            ctrl = [cur, end]
        else:
            ctrl = [cur] + [(v[j], v[j + 1]) for j in range(0, need, 2)]
        cmds.append(ctrl)
        for s in range(1, 201):
            out.append((*split(ctrl, s / 200)[1][0], len(cmds) - 1, s / 200))
        cur = ctrl[-1]
    return cmds, out


def split(ctrl, t):
    """de Casteljau: the control points of the curve before and after t."""
    left, right, pts_ = [ctrl[0]], [ctrl[-1]], ctrl
    while len(pts_) > 1:
        pts_ = [(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t) for a, b in zip(pts_, pts_[1:])]
        left.append(pts_[0])
        right.append(pts_[-1])
    return left, right[::-1]


def sub_path(cmds, a, b):
    """The track from position a to position b, each (command index, t), as a path."""
    d = ""
    for ci in range(a[0], b[0] + 1):
        t0, t1 = (a[1] if ci == a[0] else 0.0), (b[1] if ci == b[0] else 1.0)
        if t1 - t0 < 1e-9 and a[0] != b[0]:  # a pose at the very end or start of a command
            continue
        c = split(cmds[ci], t1)[0]
        c = split(c, t0 / t1)[1] if t1 else [c[0]] * len(c)
        d = d or "M" + pts(*c[0])
        d += " " + "LQC"[len(c) - 2] + pts(*[v for q in c[1:] for v in q])
    return d


def pose(ref, d, at, angles, cls, track, first=1):
    cmds, samples = parse_path(d)
    lengths = [0.0]
    for a, b in zip(samples, samples[1:]):
        lengths.append(lengths[-1] + math.dist(a[:2], b[:2]))
    total = lengths[-1]
    fr = [float(v) for v in at.split(",")]
    ang = angles.split(",") if angles else ["t"] * len(fr)
    if len(ang) != len(fr):
        sys.exit("pose: --angles needs one value per --at value")
    out, prev = [], (0, 0.0)
    for k, (f, a) in enumerate(zip(fr, ang), first):
        target = max(0.0, min(1.0, f)) * total
        j = next((i for i, L in enumerate(lengths) if L >= target), len(lengths) - 1)
        j = max(j, 1)
        (x0, y0, c0, t0), (x1, y1, c1, t1) = samples[j - 1], samples[j]
        span = lengths[j] - lengths[j - 1] or 1
        u = (target - lengths[j - 1]) / span
        x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        here = (c1, (t0 if c0 == c1 else 0.0) + (t1 - (t0 if c0 == c1 else 0.0)) * u)
        if track and here != prev:  # the track grows with the steps: the part up to this pose appears now
            out.append(f'<path class="ink-track" data-step="{k}+" d="{sub_path(cmds, prev, here)}"/>')
        prev = here
        tangent = math.degrees(math.atan2(y1 - y0, x1 - x0))
        m = re.fullmatch(r"t([+-]\d+(?:\.\d+)?)?", a.strip())
        rot = tangent + float(m.group(1) or 0) if m else float(a)
        rot = (rot + 180) % 360 - 180
        out.append(f'<use href="#{ref}"' + (f' class="{cls}"' if cls else "") + f' data-step="{k}" transform="translate({pts(x, y)}) rotate({n(rot)})"/>')
    return "\n".join(out)


# ---- overview sheet ----

def sheet():
    tpl = Path(__file__).resolve().parents[2] / "explainer-page" / "assets" / "template.html"
    style = re.search(r"<style>(.*?)</style>", tpl.read_text(encoding="utf-8"), re.S).group(1)
    cells = []

    def obj(oid, at, parts_shade, cls=""):
        parts, shade = parts_shade
        return group(oid, cls, at, parts, shade)

    def label(x, y, t, sub=""):
        s = f'<text x="{x}" y="{y}" text-anchor="middle" class="b">{t}</text>'
        return s + (f'<text x="{x}" y="{y + 18}" text-anchor="middle" class="sm">{sub}</text>' if sub else "")

    cells.append('<text x="10" y="24" class="b">Basic shapes</text>')
    cells.append(f'<g class="ink" transform="translate(70 80)">{pill(0, 0, 90, 34)}</g>' + label(70, 140, "pill", "90 × 34"))
    cells.append(f'<g class="ink" transform="translate(200 80)">{rect(-45, -30, 90, 60, (16, 16, 0, 0))}</g>' + label(200, 140, "rect", "corners 16 16 0 0"))
    cells.append(f'<g class="ink c1" transform="translate(330 80)">{"".join(cylinder(70, 80))}</g>' + label(330, 140, "cylinder", "c1, 70 × 80"))
    cells.append(f'<g class="ink c2" transform="translate(470 80)">{ogive(120, 40, 40)}</g>' + label(470, 140, "ogive", "c2, nose 40"))
    cells.append(f'<g class="ink dark" transform="translate(580 80)">{circle(0, 0, 18)}</g><g class="ink glass" transform="translate(650 80)">{circle(0, 0, 18)}</g>'
                 + label(615, 140, "dark · glass"))
    cells.append('<text x="10" y="194" class="b">Person 150 · 120 · 100</text>')
    cells.append(obj("s-p150", "70,300", person(150), "c1") + obj("s-p120", "180,315", person(120)) + obj("s-p100", "270,325", person(100), "c3"))
    cells.append(label(170, 410, "", "one outer outline; 4px at every size"))
    cells.append('<text x="370" y="194" class="b">Robot, facing +x</text>')
    cells.append(obj("s-rt", "440,280", robot(100, "top"), "c2") + obj("s-rt2", "610,280,-35", robot(70, "top")))
    cells.append(obj("s-rs", "440,400", robot(100, "side"), "c2") + obj("s-rs2", "610,410", robot(70, "side")))
    cells.append(label(525, 450, "", "top 100 · top 70 at −35° · side 100 · side 70"))
    cells.append('<text x="10" y="494" class="b">Drone</text>')
    cells.append(obj("s-dt", "90,590", drone(140, "top"), "c5") + obj("s-dt2", "240,590,30", drone(100, "top")))
    cells.append(obj("s-ds", "390,590", drone(140, "side"), "c5") + label(240, 690, "", "top 140 · top 100 at 30° · side 140"))
    cells.append('<text x="490" y="494" class="b">Pose: 4 steps on a path</text>')
    cells.append('<defs>' + group("s-pr", "", "", *robot(44, "top")) + "</defs>")
    cells.append(pose("s-pr", "M510 650 Q590 520 680 610", "0,0.33,0.66,1", "", "", True))
    cells.append(label(600, 690, "", "robot 44, angle from the tangent"))
    body = "\n".join(cells)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 710" width="1080" height="1065">\n'
            f'<style><![CDATA[{style}\nsvg {{ background: var(--bg); }}]]></style>\n{body}\n</svg>\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, need_id=True):
        p.add_argument("--id", required=need_id, help="id, starting with the figure number (f3-robot)")
        p.add_argument("--cls", default="", help="concept class c1-c5")
        p.add_argument("--at", default="", help="X,Y[,ANGLE]: print placed instead of for <defs>")

    p = sub.add_parser("person", help="a person, front view")
    common(p)
    p.add_argument("--height", type=float, default=150)
    for name, dflt in (("robot", 80), ("drone", 120)):
        p = sub.add_parser(name, help=f"a {name}, top or side view, facing +x")
        common(p)
        p.add_argument("--size", type=float, default=dflt)
        p.add_argument("--view", choices=("top", "side"), default="top")
    p = sub.add_parser("pill", help="a pill, w × h, centred")
    common(p, False)
    p.add_argument("--w", type=float, required=True)
    p.add_argument("--h", type=float, required=True)
    p = sub.add_parser("rect", help="a rectangle with a radius per corner")
    common(p, False)
    p.add_argument("--w", type=float, required=True)
    p.add_argument("--h", type=float, required=True)
    p.add_argument("--r", default="0 0 0 0", help="radii: top-left top-right bottom-right bottom-left")
    p = sub.add_parser("cylinder", help="an upright cylinder (a database, a tank)")
    common(p, False)
    p.add_argument("--w", type=float, required=True)
    p.add_argument("--h", type=float, required=True)
    p = sub.add_parser("ogive", help="a body with a pointed nose toward +x")
    common(p, False)
    p.add_argument("--w", type=float, required=True, help="length")
    p.add_argument("--h", type=float, required=True, help="diameter")
    p.add_argument("--nose", type=float, required=True, help="nose length")
    for p in [sub.choices[c] for c in ("pill", "rect", "cylinder", "ogive")]:
        p.add_argument("--fill", choices=("light", "dark", "glass"), default="light")
    p = sub.add_parser("pose", help="<use> elements along a path, one per stepper step")
    p.add_argument("--ref", required=True, help="the id of the object in <defs>")
    p.add_argument("--path", required=True, help="the track: absolute M L H V Q C")
    p.add_argument("--at", required=True, help="positions along the track, 0-1, comma-separated")
    p.add_argument("--angles", default="", help="per step: t (tangent), t+90, t-90, or degrees")
    p.add_argument("--cls", default="")
    p.add_argument("--first", type=int, default=1, help="the stepper step of the first pose (default 1)")
    p.add_argument("--no-track", action="store_true", help="do not print the faint track")
    sub.add_parser("sheet", help="the overview sheet of every part, as an SVG file")
    argv = sys.argv[1:]  # let "--at -30,20" through: argparse takes a value that starts with "-" for an option
    for i in range(len(argv) - 2, -1, -1):
        if argv[i] in ("--at", "--angles") and argv[i + 1].startswith("-"):
            argv[i:i + 2] = [argv[i] + "=" + argv[i + 1]]
    a = ap.parse_args(argv)

    if a.cmd in ("person", "robot", "drone"):
        parts, shade = person(a.height) if a.cmd == "person" else robot(a.size, a.view) if a.cmd == "robot" else drone(a.size, a.view)
        print(group(a.id, a.cls, a.at, parts, shade))
    elif a.cmd in ("pill", "rect", "cylinder", "ogive"):
        if a.cmd == "pill":
            el = pill(0, 0, a.w, a.h)
        elif a.cmd == "rect":
            r = [float(v) for v in a.r.split()]
            el = rect(-a.w / 2, -a.h / 2, a.w, a.h, tuple(r))
        elif a.cmd == "cylinder":
            el = "".join(cylinder(a.w, a.h))
        else:
            el = ogive(a.w, a.h, a.nose)
        cls = "ink" + {"light": "", "dark": " dark", "glass": " glass"}[a.fill] + (" " + a.cls if a.cls else "")
        idattr = f' id="{a.id}"' if a.id else ""
        print(f'<g{idattr} class="{cls}"{place(a.at)}>{el}</g>')
    elif a.cmd == "pose":
        print(pose(a.ref, a.path, a.at, a.angles, a.cls, not a.no_track, a.first))
    else:
        sys.stdout.write(sheet())


if __name__ == "__main__":
    main()
