// Overlap check for the SVG figures of an explainer page (explainer-figure SKILL.md § Self-check).
// The Self-check command inserts this file at the end of the page body, opens the page in headless
// Chrome with --dump-dom, and prints the report element (id overlap-report). One line per problem;
// the report is empty when every figure passes.
//   text-overlap       two text boxes overlap
//   line-through-text  a stroked line or shape edge runs through a text box
//   text-on-edge       a text box is partly inside and partly outside a filled shape (or a <use>)
// data-touch on an element or an ancestor excludes it from the last two checks.
(function () {
  var SKIP = 'defs, clipPath, marker, symbol, mask, pattern';

  function shown(el, svg) {
    for (var e = el; e && e !== svg; e = e.parentNode) {
      var cs = getComputedStyle(e);
      if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') return false;
    }
    return true;
  }
  function touch(el) { return !!el.closest('[data-touch]'); }
  function inset(r, d) { return { l: r.left + d, t: r.top + d, r: r.right - d, b: r.bottom - d }; }
  function hits(b, x, y) { return x > b.l && x < b.r && y > b.t && y < b.b; }
  function num(v) { return Math.round(parseFloat(v)); }
  function describe(el) {
    var tag = el.tagName.toLowerCase(), cls = el.getAttribute('class');
    var name = tag + (cls ? '.' + cls.trim().split(/\s+/).join('.') : ''), a = function (k) { return num(el.getAttribute(k)); };
    if (tag === 'text') return 'text "' + el.textContent.trim() + '"';
    if (tag === 'line') return name + ' ' + [a('x1'), a('y1'), a('x2'), a('y2')].join(' ');
    if (tag === 'rect') return name + ' ' + [a('x'), a('y'), a('width'), a('height')].join(' ');
    if (tag === 'circle') return name + ' ' + [a('cx'), a('cy'), a('r')].join(' ');
    if (tag === 'ellipse') return name + ' ' + [a('cx'), a('cy'), a('rx'), a('ry')].join(' ');
    if (tag === 'use') return name + ' ' + el.getAttribute('href');
    var d = el.getAttribute('d') || el.getAttribute('points') || '';
    return name + ' ' + (d.length > 24 ? d.slice(0, 24) + ' …' : d);
  }
  // 5 × 3 sample points on a text box, in screen coordinates.
  function grid(r) {
    var pts = [];
    [0.05, 0.275, 0.5, 0.725, 0.95].forEach(function (fx) {
      [0.25, 0.5, 0.75].forEach(function (fy) { pts.push([r.left + fx * r.width, r.top + fy * r.height]); });
    });
    return pts;
  }

  function checkFrame(svg) {
    var out = [];
    var texts = [].filter.call(svg.querySelectorAll('text'), function (t) {
      return !t.closest(SKIP) && shown(t, svg) && t.textContent.trim();
    }).map(function (t) { return { el: t, r: t.getBoundingClientRect(), s: t.textContent.trim() }; });
    var shapes = [].filter.call(svg.querySelectorAll('line, path, polyline, polygon, rect, circle, ellipse'), function (e) {
      return !e.closest(SKIP) && shown(e, svg) && !touch(e);
    });
    var uses = [].filter.call(svg.querySelectorAll('use'), function (u) {
      return !u.closest(SKIP) && shown(u, svg) && !touch(u);
    });

    // 1. Text boxes that overlap. The same text redrawn in the same place (a later frame) is not a problem.
    for (var i = 0; i < texts.length; i++) for (var j = i + 1; j < texts.length; j++) {
      var a = texts[i], b = texts[j], p = inset(a.r, 1), q = inset(b.r, 1);
      if (p.l >= q.r || q.l >= p.r || p.t >= q.b || q.t >= p.b) continue;
      if (a.s === b.s && Math.abs(a.r.left - b.r.left) < 1 && Math.abs(a.r.top - b.r.top) < 1) continue;
      out.push(['text-overlap', a.s, describe(b.el)]);
    }

    texts.forEach(function (t) {
      if (touch(t.el)) return;
      var box = inset(t.r, 1), pts = grid(t.r);
      shapes.forEach(function (e) {
        var cs = getComputedStyle(e), m = e.getScreenCTM();
        if (!m) return;
        // 2. A stroked outline sampled every 2 screen pixels along its length.
        if (cs.stroke !== 'none' && parseFloat(cs.strokeWidth) > 0) {
          var len = e.getTotalLength(), scale = Math.hypot(m.a, m.b) || 1, step = 2 / scale;
          for (var s = 0; s <= len; s += step) {
            var pt = e.getPointAtLength(s), x = m.a * pt.x + m.c * pt.y + m.e, y = m.b * pt.x + m.d * pt.y + m.f;
            if (hits(box, x, y)) { out.push(['line-through-text', t.s, describe(e)]); break; }
          }
        }
        // 3. Part of the text box inside a filled shape, part outside.
        if (cs.fill !== 'none' && e.tagName !== 'line') {
          var inv = m.inverse(), n = 0;
          pts.forEach(function (sp) {
            var lp = new DOMPoint(sp[0], sp[1]).matrixTransform(inv);
            if (e.isPointInFill(lp)) n++;
          });
          if (n > 0 && n < pts.length) out.push(['text-on-edge', t.s, describe(e)]);
        }
      });
      // 3 for <use>: its shapes sit in a shadow tree, so hit-test the same points (not its bounding box,
      // which is larger than a rotated object).
      uses.forEach(function (u) {
        var n = 0;
        pts.forEach(function (sp) { if (document.elementsFromPoint(sp[0], sp[1]).indexOf(u) >= 0) n++; });
        if (n > 0 && n < pts.length) out.push(['text-on-edge', t.s, describe(u)]);
      });
    });
    return out;
  }

  function run() {
    var lines = [], seen = {};
    document.querySelectorAll('figure').forEach(function (fig, fi) {
      var svg = fig.querySelector('svg');
      if (!svg) return;
      var name = fig.id || 'figure-' + (fi + 1), btn = fig.querySelectorAll('.stepper-bar button');
      var count = fig.querySelector('.stepper-bar .count'), frames = 1;
      if (btn.length && count) {
        frames = parseInt(count.textContent.split('/')[1], 10) || 1;
        for (var k = 0; k < frames; k++) btn[0].click();
      }
      for (var f = 1; f <= frames; f++) {
        if (f > 1) btn[1].click();
        fig.scrollIntoView({ block: 'start' });
        checkFrame(svg).forEach(function (o) {
          var key = name + o.join('|');
          if (seen[key]) return;
          seen[key] = 1;
          lines.push(name + (frames > 1 ? ' [frame ' + f + ']' : '') + ' ' + o[0] + ': "' + o[1] + '" × ' + o[2]);
        });
      }
    });
    var pre = document.createElement('pre');
    pre.id = 'overlap-report';
    pre.textContent = lines.map(function (l) { return l + '\n'; }).join('');
    document.body.appendChild(pre);
  }

  window.addEventListener('load', function () { document.fonts.ready.then(run); });
})();
