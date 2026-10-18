"""Original diagrams for file no. 015 (the Wyckoff House)."""
from lostindex.diag import diagram, seg, ease, lerp, clamp, schematic_tag

RED = (176, 52, 40)
OCHRE = (214, 158, 74)


def house_glyph(c, cx, base_y, s, col, a, fill=None):
    """Low Dutch farmhouse in elevation: body, steep roof with flared eaves, chimney."""
    w, h = 120 * s, 46 * s
    x0, x1 = cx - w / 2, cx + w / 2
    if fill:
        c.rect((x0, base_y - h, x1, base_y), fill=fill, a=a * 0.35)
    c.rect((x0, base_y - h, x1, base_y), col=col, width=2, a=a)
    roof = [(x0 - 14 * s, base_y - h + 6 * s), (x0 + 6 * s, base_y - h - 8 * s), (cx - 34 * s, base_y - h - 44 * s),
            (cx + 34 * s, base_y - h - 44 * s), (x1 - 6 * s, base_y - h - 8 * s), (x1 + 14 * s, base_y - h + 6 * s)]
    c.line(roof, col, 2, a)
    c.rect((cx + 14 * s, base_y - h - 58 * s, cx + 26 * s, base_y - h - 40 * s), col=col, width=2, a=a)
    c.rect((cx - 8 * s, base_y - 30 * s, cx + 8 * s, base_y), col=col, width=2, a=a)
    for wx in (x0 + 18 * s, x1 - 34 * s):
        c.rect((wx, base_y - 32 * s, wx + 16 * s, base_y - 16 * s), col=col, width=1.5, a=a)


@diagram
def name_timeline(c, p, t, pal, beat):
    ink, grey = pal["ink"], pal["grey"]
    W, H = c.w, c.h
    a0 = seg(t, 0, 0.4)

    # the name, built at 1664
    first, last = "Pieter Claesen ", "Wyckoff"
    size = 74
    full_w = c.text_w(first + last, size, "serif_i")
    x0 = (W - full_w) / 2
    c.text(x0, 70, first.strip(), size=size, col=ink, a=a0, face="serif_i")
    n = int(len(last) * clamp((t - 0.75) / 1.1) + 0.999) if t > 0.75 else 0
    c.text(x0 + c.text_w(first, size, "serif_i"), 70, last[:n], size=size, col=RED, a=1.0, face="serif_i")
    c.text(W / 2, 178, "claesen = “son of claes”", size=21, col=grey, a=a0, anchor="ma")
    c.text(W / 2, 208, "wyckoff = a surname he chose", size=21, col=RED, a=seg(t, 1.9, 0.4), anchor="ma")

    # axis with a break between 1664 and 1901
    ay = 470
    xs = [96, 276, 456, 676, 836]
    brk = 566
    c.partial_line([(40, ay), (brk - 12, ay)], ink, 3, seg(t, 0.05, 0.5))
    fr2 = seg(t, 0.45, 0.4)
    c.partial_line([(brk + 12, ay), (W - 40, ay)], ink, 3, fr2)
    for dx in (-12, 12):
        c.line([(brk + dx - 7, ay + 12), (brk + dx + 7, ay - 12)], ink, 2, fr2)

    events = [
        ("1630s", ["arrives as", "pieter claesen"], 0.15, ink),
        ("c. 1652", ["oldest room"], 0.35, ink),
        ("1664", ["english take over;", "surnames needed"], 0.55, RED),
        ("1901", ["family leaves"], 1.9, ink),
        ("1965", ["landmark no. 1"], 2.2, ink),
    ]
    for i, ((yr, desc, st, col), x) in enumerate(zip(events, xs)):
        a = seg(t, st, 0.35)
        if a <= 0:      # PIL writes RGBA pixels directly: an alpha-0 shape would punch a hole
            continue
        c.line([(x, ay - 12), (x, ay + 12)], col, 3, a)
        c.circle(x, ay, 6, fill=col, a=a)
        c.text(x, ay - 78, yr, size=44, col=col, a=a, face="serif_i", anchor="ma")
        row = 1 if i % 2 else 0          # stagger labels so neighbours never collide
        ty = ay + 30 + row * 84
        if row:
            c.line([(x, ay + 16), (x, ty - 6)], grey, 1.5, a * 0.6)
        for k, line in enumerate(desc):
            c.text(x, ty + k * 28, line, size=20, col=grey if col is ink else col, a=a, anchor="ma")
    # pulse ring on 1664 while the name builds
    pr = clamp((t - 0.75) / 1.2)
    if 0 < pr < 1:
        c.circle(xs[2], ay, 6 + 26 * pr, col=RED, width=2, a=(1 - pr) * 0.8)

    if t > 0.35:
        house_glyph(c, xs[1], ay - 96, 0.62, ink, seg(t, 0.35, 0.35), fill=OCHRE)

    c.text(W / 2, 668, "the name came after the english took over.", size=20, col=grey, a=seg(t, 2.4, 0.5), anchor="ma")
    schematic_tag(c, pal, "schematic · not to scale · drawn for this video", a0)


@diagram
def move_request(c, p, t, pal, beat):
    ink, grey = pal["panel_ink"], pal["grey"]
    W, H = c.w, c.h
    a0 = seg(t, 0, 0.4)
    # late phase (after the pause): objection
    obj = ease((p - 0.70) / 0.08)
    c.text(36, 34, "plan view", size=20, col=grey, a=a0)

    # existing street, ending short of the house
    y0, y1 = 380, 470
    end = 400
    fr = seg(t, 0.0, 0.7)
    c.partial_line([(0, y0), (end, y0)], ink, 3, fr)
    c.partial_line([(0, y1), (end, y1)], ink, 3, fr)
    c.line([(end, y0), (end, y1)], ink, 3, seg(t, 0.6, 0.2))
    c.dashed((0, (y0 + y1) / 2), (end - 20, (y0 + y1) / 2), grey, 2, dash=18, gap=14, a=a0 * 0.7, frac=fr)
    c.text(30, y0 - 44, "ditmas avenue", size=24, col=ink, a=a0)

    # the house footprint (main block + wing)
    hx0, hx1, hy0, hy1 = 560, 690, 372, 478
    ha = seg(t, 0.2, 0.4)
    c.rect((hx0 - 70, hy0 + 30, hx0, hy1), col=ink, fill=OCHRE, width=2, a=ha)
    c.rect((hx0, hy0, hx1, hy1), col=ink, fill=OCHRE, width=2, a=ha)
    c.text((hx0 - 70 + hx1) / 2, hy1 + 22, "wyckoff house", size=22, col=ink, a=ha, anchor="ma")

    # proposed extension, straight through the house
    ext = seg(t, 0.9, 1.1)
    ea = 1 - obj
    c.dashed((end, y0), (W, y0), RED, 3, dash=16, gap=10, a=ea, frac=ext)
    c.dashed((end, y1), (W, y1), RED, 3, dash=16, gap=10, a=ea, frac=ext)
    c.text(W - 30, y0 - 44, "proposed extension", size=22, col=RED, a=seg(t, 1.5, 0.4) * ea, anchor="ra")

    # dashed arrow lifting the house aside
    mv = seg(t, 2.2, 0.6)
    ga = mv * ea
    dy = 210
    gy0 = hy0 + dy
    for bx in ((hx0 - 70, hy0 + 30, hx0, hy1), (hx0, hy0, hx1, hy1)):
        dashed_rect(c, (bx[0], bx[1] + dy, bx[2], bx[3] + dy), RED, ga)
    if ga > 0:
        ax = (hx0 + hx1) / 2 - 20
        c.arrow((ax, hy1 + 50), (ax, lerp(hy1 + 50, gy0 - 14, mv)), RED, 3, head=14, a=ga)
    c.text(hx1 + 30, gy0 + 40, "? move it", size=26, col=RED, a=seg(t, 2.6, 0.4) * ea)

    # the objection stamp
    if obj > 0:
        sc = lerp(1.18, 1.0, ease_out_local(obj))
        cx, cy = W * 0.5, 190
        bw, bh = 470 * sc, 160 * sc
        c.rect((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), col=RED, width=4, a=obj)
        c.rect((cx - bw / 2 + 9, cy - bh / 2 + 9, cx + bw / 2 - 9, cy + bh / 2 - 9), col=RED, width=1.5, a=obj)
        c.text(cx, cy - 58 * sc, "objected", size=int(50 * sc), col=RED, a=obj, face="mono_med", anchor="ma")
        c.text(cx, cy + 22 * sc, "· borough historian ·", size=int(22 * sc), col=RED, a=obj, anchor="ma")
    schematic_tag(c, pal, "schematic · not to scale · drawn for this video", a0)


def dashed_rect(c, box, col, a):
    x0, y0, x1, y1 = box
    for p0, p1 in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        c.dashed(p0, p1, col, 2, dash=10, gap=7, a=a)


def ease_out_local(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


DIAGRAMS = {"name_timeline": name_timeline, "move_request": move_request}
