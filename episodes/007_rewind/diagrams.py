"""Original diagrams for file no. 007 (rewind). Generic shapes only: no logos, no real interfaces."""
import math

from lostindex.diag import diagram, seg, ease, ease_out, lerp, clamp, schematic_tag

RED = (178, 48, 40)


@diagram
def stores(c, p, t, pal, beat):
    ink, grey = pal["ink"], pal["grey"]
    W, H = c.w, c.h
    x0, x1, y0, y1 = 110, W - 90, H - 170, 120
    a = seg(t, 0, 0.5)
    c.line([(x0, y0), (x1, y0)], ink, 2, a)
    for yr in (1985, 1995, 2004, 2015, 2025):
        x = lerp(x0, x1, (yr - 1985) / 40)
        c.line([(x, y0), (x, y0 + 10)], ink, 2, a)
        c.text(x, y0 + 20, str(yr), size=22, col=grey, a=a, anchor="ma")
    pts = [(1985, 1), (2004, 9000), (2025, 1)]
    P = [(lerp(x0, x1, (yr - 1985) / 40), lerp(y0, y1, n / 9000)) for yr, n in pts]
    # only the rise is drawn during this beat's first part; fall follows later in the beat
    rise = seg(t, 0.5, 2.2)
    fall = seg(t, 3.4, 1.6)
    c.partial_line([P[0], P[1]], ink, 4, rise, a)
    if fall > 0:
        c.partial_line([P[1], P[2]], RED, 4, fall, a)
    labs = [(P[0], "1 store · dallas · 1985", 0.4, "la", (10, -50)),
            (P[1], "about 9,000 · 2004", 2.6, "ma", (0, -54)),
            (P[2], "1 · bend, oregon", 5.0, "ra", (-10, -50))]
    for (x, y), s, st, anc, (dx, dy) in labs:
        aa = seg(t, st, 0.5)
        c.circle(x, y, 8, fill=RED if st > 4 else ink, a=aa)
        c.text(x + dx, y + dy, s, size=24, col=ink, a=aa, anchor=anc)
    c.text(x0, y0 + 70, "only sourced points shown · lines are not data", size=18, col=grey, a=a * 0.85)


def disc(c, cx, cy, r, a):
    for k in range(8):
        rr = r * (1 - k * 0.09)
        v = 200 - k * 6 + (12 if k % 2 else 0)
        c.circle(cx, cy, rr, fill=(v, v, v + 4), a=a)
    c.circle(cx, cy, r, col=(120, 120, 124), width=2, a=a)
    c.circle(cx, cy, r * 0.17, fill=(232, 226, 213), col=(120, 120, 124), width=2, a=a)
    c.arc((cx - r * 0.8, cy - r * 0.8, cx + r * 0.8, cy + r * 0.8), 200, 250, (255, 255, 255), 6, a * 0.7)


def mailer(c, box, a, open_frac=1.0, ink=(38, 36, 31)):
    x0, y0, x1, y1 = box
    c.rect(box, fill=(246, 243, 236), col=ink, width=2, a=a)
    c.rect((x0, y0, x1, y0 + (y1 - y0) * 0.36), fill=RED, a=a)
    # flap
    fy = y0 + (y1 - y0) * 0.36
    tip = lerp(fy + 70, fy - 70, open_frac)
    c.polygon([(x0, fy), ((x0 + x1) / 2, tip), (x1, fy)], fill=RED if open_frac < 0.5 else (196, 70, 60), col=ink, a=a)
    for k in range(3):
        c.line([(x0 + 40, y1 - 120 + k * 30), (x0 + 300, y1 - 120 + k * 30)], (150, 146, 138), 3, a)


def postmark(c, cx, cy, s, a, ink=(38, 36, 31)):
    c.circle(cx, cy, 70, col=ink, width=3, a=a)
    c.circle(cx, cy, 56, col=ink, width=1.5, a=a)
    c.text(cx, cy - 12, s, size=26, col=ink, a=a, anchor="ma", face="mono_med")
    for k in range(4):
        y = cy - 30 + k * 20
        pts = [(cx + 80 + i * 12, y + 6 * math.sin(i * 0.9)) for i in range(16)]
        c.line(pts, ink, 2, a)


@diagram
def mailer_1998(c, p, t, pal, beat):
    W, H = c.w, c.h
    a = seg(t, 0, 0.5)
    box = (W * 0.18, H * 0.38, W * 0.82, H * 0.86)
    mailer(c, box, a, open_frac=1 - seg(t, 2.4, 0.6))
    k = ease_out(clamp((t - 0.5) / 1.6))
    cy = lerp(H * 0.2, H * 0.55, k)
    if t < 2.5:
        disc(c, W / 2, cy, 120, a * (1 - seg(t, 2.1, 0.3)))
    postmark(c, W * 0.30, H * 0.30, "1998", seg(t, 2.9, 0.15))
    schematic_tag(c, pal, "illustration · generic mailer, no logo", a)


@diagram
def stream(c, p, t, pal, beat):
    ink = pal["ink"]
    W, H = c.w, c.h
    a = seg(t, 0, 0.4)
    k = seg(t, 0.4, 1.4)
    cy = H * 0.45
    r = 130
    # the disc squashes into a bar
    w = lerp(2 * r, W - 200, k)
    h = lerp(2 * r, 16, k)
    if k < 0.98:
        c.ellipse((W / 2 - w / 2, cy - h / 2, W / 2 + w / 2, cy + h / 2), fill=(205, 205, 210), col=(120, 120, 124), a=a)
    else:
        c.rect((100, cy - 8, W - 100, cy + 8), fill=(200, 194, 182), a=a, radius=8)
        fill = seg(t, 2.0, max(1.0, beat["end"] - beat["start"] - 2.4))
        c.rect((100, cy - 8, lerp(100, W - 100, fill), cy + 8), fill=RED, a=a, radius=8)
        c.circle(lerp(100, W - 100, fill), cy, 16, fill=RED, a=a)
        c.polygon([(W / 2 - 40, cy + 90), (W / 2 - 40, cy + 190), (W / 2 + 50, cy + 140)], fill=ink, a=seg(t, 1.9, 0.3))
        c.text(100, cy + 40, "0:00", size=22, col=pal["grey"], a=a)
    schematic_tag(c, pal, "illustration · generic player, not a real interface", a)


@diagram
def mailer_2023(c, p, t, pal, beat):
    W, H = c.w, c.h
    a = seg(t, 0, 0.5)
    box = (W * 0.18, H * 0.38, W * 0.82, H * 0.86)
    mailer(c, box, a, open_frac=1 - seg(t, 0.8, 0.8))
    postmark(c, W * 0.30, H * 0.30, "sep 2023", seg(t, 1.9, 0.15))
    c.text(W / 2, H * 0.62, "empty", size=30, col=pal["grey"], a=seg(t, 1.6, 0.6), anchor="ma", face="serif_i")
    schematic_tag(c, pal, "illustration · generic mailer, no logo", a)


DIAGRAMS = {"stores": stores, "mailer_1998": mailer_1998, "stream": stream, "mailer_2023": mailer_2023}
