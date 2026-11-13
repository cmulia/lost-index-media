"""Original diagrams for file no. 019 (the Trojan Room coffee pot). Generic shapes only, no real screenshots."""
import math

from lostindex.diag import diagram, seg, ease, ease_out, lerp, clamp, schematic_tag

AMBER = (226, 170, 84)
RED = (178, 48, 40)
TAG = "schematic · drawn for this video"


def pot(c, cx, base, h, col, level, a, w=None):
    """A simple glass coffee pot outline with a coffee level 0..1."""
    w = w or h * 0.62
    x0, x1 = cx - w / 2, cx + w / 2
    top = base - h
    c.rect((x0, top, x1, base), col=col, width=3, a=a, radius=10)
    c.line([(x1, top + h * 0.2), (x1 + w * 0.28, top + h * 0.2), (x1 + w * 0.28, top + h * 0.7), (x1, top + h * 0.7)], col, 3, a)
    c.line([(x0 - 6, top), (x1 + 6, top)], col, 4, a)
    if level > 0:
        ly = base - (h - 14) * level
        c.rect((x0 + 5, ly, x1 - 5, base - 5), fill=(120, 78, 44), a=a * 0.9, radius=6)


@diagram
def stairs(c, p, t, pal, beat):
    ink, grey = pal["ink"], pal["grey"]
    a = seg(t, 0, 0.4)
    W, H = c.w, c.h
    n = 5
    x0, y0 = 90, H - 200
    sw, sh = 120, 70
    pts = [(x0, y0)]
    for i in range(n):
        pts += [(x0 + i * sw, y0 - (i + 1) * sh), (x0 + (i + 1) * sw, y0 - (i + 1) * sh)]
    c.line(pts, ink, 4, a)
    # the climber
    k = seg(t, 0.4, 2.4)
    i = min(n - 1, int(k * n))
    f = k * n - i if k < 1 else 1.0
    px = x0 + (i + f) * sw + 20
    py = y0 - (i + (1 if f > 0.35 else f / 0.35)) * sh - 22
    if k >= 1:
        px, py = x0 + n * sw - 70, y0 - n * sh - 22
    c.circle(px, py - 30, 11, fill=ink, a=a)
    c.line([(px, py - 19), (px, py + 14)], ink, 5, a)
    c.line([(px, py + 14), (px - 9 + 18 * (f % 1 > 0.5), py + 34)], ink, 5, a)
    # the pot at the top, empty
    pa = seg(t, 2.6, 0.5)
    pot(c, x0 + n * sw + 20, y0 - n * sh, 150, ink, 0.0, pa)
    c.text(x0 + n * sw + 20, y0 - n * sh + 20, "empty", size=34, col=RED, a=pa, anchor="ma")
    c.text(90, H - 150, "on the way up: a wasted trip", size=34, col=ink, a=a)
    c.text(90, H - 104, "several flights of stairs, pot already drained", size=24, col=grey, a=seg(t, 0.8, 0.5))
    schematic_tag(c, pal, TAG, a)


def box(c, x0, y0, x1, y1, ink, a, fill=None):
    c.rect((x0, y0, x1, y1), col=ink, width=3, a=a, radius=12, fill=fill)


@diagram
def pipeline(c, p, t, pal, beat):
    ink, grey = pal["ink"], pal["grey"]
    a = seg(t, 0, 0.4)
    W, H = c.w, c.h
    items = [("camera", "points at the pot"), ("cable", "to a computer"),
             ("frame grabber", "turns video into a picture"), ("their screens", "on other floors")]
    bw, bh, gap = 560, 100, 62
    x0 = (W - bw) / 2
    y = 70
    ys = []
    for i, (l1, l2) in enumerate(items):
        st = 0.2 + i * 0.7
        m = seg(t, st, 0.4)
        box(c, x0, y, x0 + bw, y + bh, ink, m, fill=(46, 44, 40))
        c.text(x0 + 26, y + 16, l1, size=34, col=ink, a=m)
        c.text(x0 + 26, y + 62, l2, size=24, col=grey, a=m)
        ys.append(y)
        if i < len(items) - 1:
            c.arrow((W / 2, y + bh), (W / 2, y + bh + gap), AMBER, 4, a=seg(t, st + 0.3, 0.4))
        y += bh + gap
    # data dot travelling down
    k = clamp((t - 0.6) / 3.2)
    if 0 < k < 1:
        yy = lerp(ys[0] + bh / 2, ys[-1] + bh / 2, k)
        c.glow(W / 2 + bw / 2 - 40, yy, 9, AMBER, a=0.9)
    c.text(x0, H - 78, "illustration: a generic chain, not the real wiring", size=20, col=grey, a=seg(t, 3.0, 0.5))
    schematic_tag(c, pal, TAG, a)


@diagram
def webcam(c, p, t, pal, beat):
    ink, grey = pal["ink"], pal["grey"]
    a = seg(t, 0, 0.4)
    W, H = c.w, c.h
    N = 32
    cell = 14
    gx, gy = (W - N * cell) / 2, 130
    k = seg(t, 0.3, 1.4)
    shown = int(lerp(1, N, ease_out(k)) + 0.5)
    shown = max(shown, 1)
    cw = N * cell / shown
    # coarse grey pot picture, drawn on an N x N grid, sampled at `shown` resolution
    def val(u, v):
        x, y = u * N, v * N
        g = 150 - 40 * v
        if 9 <= x <= 21 and 8 <= y <= 27:       # pot body
            g = 70
            if y >= 18:
                g = 25                           # coffee
            if y < 9 or x in (9, 20):
                g = 200
        if 21 < x <= 24 and 11 <= y <= 22 and (x > 23 or y < 12 or y > 21):  # handle
            g = 200
        if 8 <= x <= 22 and 7 <= y < 8:
            g = 215
        return g
    c.rect((gx - 4, gy - 4, gx + N * cell + 4, gy + N * cell + 4), col=ink, width=2, a=a)
    for iy in range(shown):
        for ix in range(shown):
            g = int(val((ix + 0.5) / shown, (iy + 0.5) / shown))
            x, y = gx + ix * cw, gy + iy * cw
            c.rect((x, y, x + cw + 0.6, y + cw + 0.6), fill=(g, g, g), a=a)
    # dimension labels
    m = seg(t, 1.8, 0.5)
    c.line([(gx, gy - 24), (gx + N * cell, gy - 24)], AMBER, 2, m)
    c.text(W / 2, gy - 66, "128 pixels", size=32, col=AMBER, a=m, anchor="ma")
    c.line([(gx - 28, gy), (gx - 28, gy + N * cell)], AMBER, 2, m)
    c.text(gx - 44, gy + N * cell / 2 - 18, "128", size=32, col=AMBER, a=m, anchor="ra")
    c.text(W / 2, gy + N * cell + 28, "greyscale · refreshed a few times a minute", size=26, col=ink, a=seg(t, 2.4, 0.5), anchor="ma")
    c.text(W / 2, gy + N * cell + 70, "pot and grid simplified here, drawn at 32 × 32", size=20, col=grey, a=seg(t, 2.6, 0.5), anchor="ma")
    schematic_tag(c, pal, TAG + " · not a real screenshot", a)


@diagram
def timeline(c, p, t, pal, beat):
    ink, grey = pal["ink"], pal["grey"]
    a = seg(t, 0, 0.4)
    W, H = c.w, c.h
    x0, x1, y = 90, W - 90, 330
    c.line([(x0, y), (x1, y)], ink, 2, a)
    for yr in (1991, 1993, 1995, 1997, 1999, 2001):
        x = lerp(x0, x1, (yr - 1991) / 10.2)
        c.line([(x, y), (x, y + 8)], ink, 2, a * 0.7)
        c.text(x, y + 16, str(yr), size=22, col=grey, a=a, anchor="ma")
    marks = [(1991, "1991", "pointed at the pot", "la", 0),
             (1993.85, "nov 1993", "on the web", "ma", 1),
             (2001.64, "22 aug 2001", "switched off", "ra", 0)]
    for i, (yr, l1, l2, anc, up) in enumerate(marks):
        x = lerp(x0, x1, (yr - 1991) / 10.2)
        m = seg(t, 0.3 + i * 0.9, 0.5)
        c.circle(x, y, 9, fill=AMBER if i < 2 else RED, a=m)
        ty = y - 170 if up else y + 90
        c.line([(x, y - 12 if up else y + 12), (x, ty + (90 if up else 0))], ink, 1, m * 0.6)
        c.text(x, ty, l1, size=36, col=ink, a=m, anchor=anc)
        c.text(x, ty + 46, l2, size=28, col=grey, a=m, anchor=anc)
    # live segment
    k = seg(t, 0.4, 2.4)
    xa = lerp(x0, x1, (1993.85 - 1991) / 10.2)
    xe = lerp(x0, x1, (2001.64 - 1991) / 10.2)
    c.line([(xa, y), (lerp(xa, xe, k), y)], AMBER, 6, a)
    c.text(lerp(xa, xe, 0.5), y + 250, "anyone with a browser could check the pot", size=26, col=grey, a=seg(t, 2.6, 0.5), anchor="ma")
    schematic_tag(c, pal, TAG, a)


@diagram
def price(c, p, t, pal, beat):
    ink, grey = pal["ink"], pal["grey"]
    a = seg(t, 0, 0.4)
    W, H = c.w, c.h
    k = seg(t, 0.3, 1.6)
    c.text(W / 2, 100, "sold on eBay · august 2001", size=28, col=grey, a=a, anchor="ma")
    c.text(W / 2, 200, "£" + format(int(3350 * k), ","), size=150, col=ink, a=a, anchor="ma", face="serif")
    pa = seg(t, 2.0, 0.5)
    pot(c, W / 2 - 120, 650, 190, ink, 0.6, pa)
    c.text(W / 2 + 10, 520, "a krups machine", size=30, col=ink, a=pa)
    c.text(W / 2 + 10, 566, "from the pot's later years", size=24, col=grey, a=pa)
    c.text(W / 2 + 10, 606, "buyer: spiegel online", size=24, col=grey, a=seg(t, 2.5, 0.5))
    c.text(W / 2 + 10, 646, "not the original pot", size=26, col=RED, a=seg(t, 3.2, 0.5))
    schematic_tag(c, pal, TAG, a)


DIAGRAMS = {"stairs": stairs, "pipeline": pipeline, "webcam": webcam, "timeline": timeline, "price": price}
