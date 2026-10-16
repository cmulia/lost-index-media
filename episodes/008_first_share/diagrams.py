"""Original diagrams for file no. 008 (the oldest share). Schematics, drawn for this video."""
import math
import random

from lostindex.diag import diagram, seg, ease, ease_out, lerp, clamp, schematic_tag

OCHRE = (186, 128, 46)
PAPER = (226, 214, 188)
INK = (58, 46, 32)


def scribble(c, x0, x1, y, seed, col, a, width=2):
    rnd = random.Random(seed)
    x = x0
    while x < x1:
        w = rnd.uniform(26, 70)
        pts = [(x + i * w / 8, y + rnd.uniform(-3, 3)) for i in range(9)]
        c.line(pts, col, width, a)
        x += w + rnd.uniform(10, 18)


@diagram
def payouts(c, p, t, pal, beat):
    W, H = c.w, c.h
    a = seg(t, 0, 0.5)
    c.rect((30, 60, W - 30, H - 90), fill=PAPER, a=a)
    y = H * 0.5
    x0, x1 = 90, W - 90
    c.partial_line([(x0, y), (x1, y)], INK, 3, seg(t, 0.3, 1.5), a)

    def X(yr):
        return lerp(x0, x1, (yr - 1606) / (1650 - 1606))
    c.line([(X(1606), y - 30), (X(1606), y + 30)], INK, 3, seg(t, 0.4, 0.3))
    c.text(X(1606), y - 70, "1606", size=30, col=INK, a=seg(t, 0.4, 0.3), anchor="ma", face="serif_i")
    c.text(X(1606), y + 44, "paid in full", size=20, col=INK, a=seg(t, 0.6, 0.3), anchor="ma")
    n = 18
    for i in range(n):
        yr = 1610 + i * 40 / (n - 1)
        aa = seg(t, 1.2 + i * 0.12, 0.2)
        c.line([(X(yr), y - 16), (X(yr) + 4, y + 16)], OCHRE, 3, aa)
    c.text(X(1630), y + 44, "payouts noted on the paper", size=20, col=INK, a=seg(t, 2.6, 0.4), anchor="ma")
    c.line([(X(1650), y - 30), (X(1650), y + 30)], INK, 3, seg(t, 3.0, 0.3))
    c.text(X(1650), y - 70, "1650", size=30, col=INK, a=seg(t, 3.0, 0.3), anchor="ma", face="serif_i")
    schematic_tag(c, pal, "schematic · ticks are not individual payments", a)


def ledger_page(c, box, a, highlight=None, rows=7, seed=3):
    x0, y0, x1, y1 = box
    c.rect(box, fill=PAPER, a=a)
    c.line([(x0 + 30, y0 + 70), (x1 - 30, y0 + 70)], INK, 2, a)
    cols = [x0 + 30, x0 + (x1 - x0) * 0.58, x0 + (x1 - x0) * 0.78, x1 - 30]
    heads = ["name", "account", "guilders"]
    for i, h in enumerate(heads):
        c.text(cols[i] + 8, y0 + 28, h, size=20, col=INK, a=a * 0.8)
    for cx in cols[1:3]:
        c.line([(cx, y0 + 20), (cx, y1 - 20)], INK, 1.2, a * 0.6)
    rh = (y1 - y0 - 100) / rows
    for r in range(rows):
        yy = y0 + 100 + r * rh
        c.line([(x0 + 30, yy + rh * 0.75), (x1 - 30, yy + rh * 0.75)], INK, 1, a * 0.25)
        if highlight is not None and r == highlight:
            continue
        scribble(c, cols[0] + 8, cols[1] - 30, yy + rh * 0.45, seed + r, (110, 96, 76), a * 0.7)
        scribble(c, cols[1] + 10, cols[2] - 20, yy + rh * 0.45, seed + 50 + r, (110, 96, 76), a * 0.6)
        scribble(c, cols[2] + 10, cols[3] - 20, yy + rh * 0.45, seed + 90 + r, (110, 96, 76), a * 0.6)
    return cols, rh


@diagram
def ledger(c, p, t, pal, beat):
    W, H = c.w, c.h
    a = seg(t, 0, 0.5)
    box = (40, 40, W - 40, H - 100)
    cols, rh = ledger_page(c, box, a, highlight=3)
    yy = 40 + 100 + 3 * rh
    ha = seg(t, 0.8, 0.6)
    c.rect((box[0] + 20, yy, box[2] - 20, yy + rh * 0.8), fill=(232, 190, 110), a=ha * 0.55)
    c.text(cols[0] + 10, yy + rh * 0.12, "p. harmensz", size=26, col=INK, a=ha, face="serif_i")
    c.text(cols[2] + 10, yy + rh * 0.12, "ƒ150", size=26, col=INK, a=ha, face="serif_i")
    c.text(W / 2, H - 70, "the share = this line", size=22, col=pal["ink"], a=seg(t, 1.6, 0.5), anchor="ma")
    schematic_tag(c, pal, "schematic · capital book, not the real page", a)


@diagram
def transfer(c, p, t, pal, beat):
    W, H = c.w, c.h
    a = seg(t, 0, 0.5)
    lb = (30, 90, W / 2 - 15, H - 120)
    rb = (W / 2 + 15, 90, W - 30, H - 120)
    for b, s in ((lb, "seller"), (rb, "buyer")):
        c.rect(b, fill=PAPER, a=a)
        c.text((b[0] + b[2]) / 2, 50, s, size=24, col=pal["ink"], a=a, anchor="ma")
        for r in range(6):
            y = b[1] + 60 + r * 70
            c.line([(b[0] + 20, y + 30), (b[2] - 20, y + 30)], INK, 1, a * 0.25)
            if r != 2:
                scribble(c, b[0] + 30, b[2] - 40, y + 10, r * 7 + (0 if s == "seller" else 99), (110, 96, 76), a * 0.6)
    k = ease(clamp((t - 0.8) / 1.8))
    y = lb[1] + 60 + 2 * 70
    x = lerp(lb[0] + 20, rb[0] + 20, k)
    c.rect((x, y - 8, x + (lb[2] - lb[0]) - 40, y + 34), fill=(232, 190, 110), a=a * 0.8)
    c.text(x + 16, y - 4, "1 share · ƒ", size=24, col=INK, a=a, face="serif_i")
    # quill
    qx, qy = x + 300, y - 40
    c.line([(qx, qy), (qx + 60, qy - 90)], INK, 3, a)
    c.polygon([(qx + 60, qy - 90), (qx + 100, qy - 150), (qx + 72, qy - 80)], fill=(240, 236, 226), col=INK, a=a)
    c.text(W / 2, H - 80, "a bookkeeper moves the line", size=22, col=pal["ink"], a=seg(t, 2.6, 0.5), anchor="ma")
    schematic_tag(c, pal, "schematic · a transfer in the company's books", a)


@diagram
def book_entry(c, p, t, pal, beat):
    W, H = c.w, c.h
    a = seg(t, 0, 0.5)
    y = H * 0.48
    c.rect((40, y - 70, 380, y + 70), fill=PAPER, a=a)
    c.rect((60, y - 18, 360, y + 22), fill=(232, 190, 110), a=a * 0.6)
    c.text(76, y - 18, "p. harmensz · ƒ150", size=26, col=INK, a=a, face="serif_i")
    c.text(210, y + 90, "1602 · a line in the capital book", size=20, col=pal["grey"], a=a, anchor="ma")
    k = seg(t, 0.8, 1.6)
    c.partial_line([(390, y), (W - 390, y)], pal["ink"], 2, k)
    ra = seg(t, 2.2, 0.5)
    c.rect((W - 380, y - 70, W - 40, y + 70), fill=(30, 30, 28), a=ra)
    c.rect((W - 360, y - 18, W - 60, y + 22), fill=(232, 190, 110), a=ra * 0.35)
    c.text(W - 348, y - 16, "ACC 0001 · 1 SH", size=24, col=(226, 220, 206), a=ra)
    c.text(W - 210, y + 90, "2025 · book entry", size=20, col=pal["grey"], a=ra, anchor="ma")
    schematic_tag(c, pal, "schematic · eu csdr, art. 3", a)


DIAGRAMS = {"payouts": payouts, "ledger": ledger, "transfer": transfer, "book_entry": book_entry}
