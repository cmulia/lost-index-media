"""Original diagrams for file no. 011 (Penn Station and the Landmarks Law)."""
from lostindex.diag import diagram, seg, ease_out, lerp, schematic_tag

RED = (176, 52, 40)
OCHRE = (214, 158, 74)

# (date, label, sub, row y, kind)
EVENTS = [
    ("1910", "pennsylvania station opens", None, 70, "plain"),
    ("2 aug 1962", "architects picket outside", None, 210, "plain"),
    ("28 oct 1963", "demolition begins", None, 300, "broken"),
    ("30 oct 1963", "new york times editorial", None, 390, "plain"),
    ("19 apr 1965", "landmarks law signed", "landmarks preservation commission created", 500, "key"),
    ("26 jun 1978", "supreme court upholds it", "penn central v. new york city · grand central kept", 630, "late"),
]


def broken_column(c, x, y, s, col, a):
    """A small fluted column snapped part-way up, with its fallen top beside it."""
    if a <= 0:
        return
    w, h = 34 * s, 70 * s
    base = y + h / 2
    c.rect((x - w / 2 - 6 * s, base, x + w / 2 + 6 * s, base + 8 * s), fill=col, a=a)
    top = base - h
    # shaft with a jagged break at the top
    c.polygon([(x - w / 2, base), (x + w / 2, base), (x + w / 2, top + 14 * s), (x + w / 4, top + 4 * s),
               (x + 2 * s, top + 18 * s), (x - w / 4, top + 6 * s), (x - w / 2, top + 16 * s)], col=col, a=a, width=2)
    for k in (-1, 0, 1):
        fx = x + k * w / 4
        c.line([(fx, base - 2), (fx, top + 22 * s)], col, 1.2, a * 0.7)
    # fallen drum lying on the ground, to the right
    fx0 = x + w / 2 + 16 * s
    c.rect((fx0, base - 20 * s, fx0 + 46 * s, base), col=col, width=2, a=a, radius=3)
    c.line([(fx0 + 15 * s, base - 20 * s), (fx0 + 15 * s, base)], col, 1.2, a * 0.7)
    c.line([(fx0 + 31 * s, base - 20 * s), (fx0 + 31 * s, base)], col, 1.2, a * 0.7)


@diagram
def landmarks_timeline(c, p, t, pal, beat):
    ink, grey = pal["ink"], pal["grey"]
    a0 = seg(t, 0, 0.35)
    X = 230                     # the timeline spine
    top, bot = EVENTS[0][3] + 14, EVENTS[-1][3] + 14
    # glow behind the 1965 dot first: Canvas draws replace pixels, so anything drawn after sits on top
    ky = EVENTS[4][3] + 14
    g = ease_out((t - 1.1) / 0.5)
    if t > 1.1:
        c.glow(X, ky, lerp(6, 11, g), OCHRE, seg(t, 1.1, 0.35))
    # spine draws on top-to-bottom, with a break between 1910 and 1962
    gap0, gap1 = 120, 160
    draw = seg(t, 0.05, 1.5)
    c.partial_line([(X, top), (X, gap0)], grey, 3, min(1.0, draw * 3), a0)
    if draw > 0.3:
        c.line([(X - 14, gap0 + 8), (X + 14, gap0 - 4)], grey, 2, a0)
        c.line([(X - 14, gap1 + 4), (X + 14, gap1 - 8)], grey, 2, a0)
        c.partial_line([(X, gap1), (X, bot)], grey, 3, (draw - 0.3) / 0.7, a0)

    for i, (date, lab, sub, y, kind) in enumerate(EVENTS):
        start = {"plain": 0.12 + i * 0.2, "broken": 0.12 + i * 0.2, "key": 1.1, "late": 2.1}[kind]
        a = seg(t, start, 0.35)
        if kind == "late":
            a *= 0.55            # faint: this comes in the next beat
        if a <= 0:
            continue
        cy = y + 14
        # dot on the spine
        if kind == "key":
            c.circle(X, cy, lerp(6, 11, ease_out((t - start) / 0.5)), fill=OCHRE, a=a)
            c.circle(X, cy, 6, fill=ink, a=a)
        else:
            c.circle(X, cy, 7, fill=pal["bg"], col=ink, width=2.5, a=a)
        c.text(X - 28, y, date, size=24, col=grey, a=a, anchor="ra")
        if kind == "key":
            # highlighter swipe grows left-to-right behind the label, then the label sits on it
            size = 34
            tw = c.text_w(lab, size, "mono_med")
            sw = seg(t, start + 0.1, 0.55)
            c.rect((X + 30, y - 8, X + 30 + (tw + 24) * sw, y + size + 10), fill=OCHRE, a=a * 0.45, radius=4)
            c.text(X + 42, y - 2, lab, size=size, col=ink, a=a, face="mono_med")
            c.text(X + 42, y + 50, sub, size=21, col=grey, a=seg(t, start + 0.5, 0.4))
            # bracket on the right: demolition -> law, about 18 months
            br = seg(t, start + 0.4, 0.5)
            y0, y1 = EVENTS[3][3] + 14, cy
            bx = c.w - 30
            c.partial_line([(bx - 14, y0 - 90), (bx, y0 - 90), (bx, y1), (bx - 14, y1)], RED, 2.5, br, a)
            c.text(bx - 14, (y0 - 90 + y1) / 2 + 30, "18 months", size=20, col=RED, a=br, anchor="ra")
        else:
            c.text(X + 34, y, lab, size=26, col=ink, a=a)
            if sub:
                c.text(X + 34, y + 38, sub, size=20, col=grey, a=a)
        if kind == "broken":
            broken_column(c, c.w - 120, y + 6, 0.9, RED, seg(t, start + 0.15, 0.4))

    schematic_tag(c, pal, "schematic · drawn for this video", a0)


DIAGRAMS = {"landmarks_timeline": landmarks_timeline}
