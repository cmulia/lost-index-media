"""Original diagrams for file no. 018 (Sputnik's beep)."""
from lostindex.diag import diagram, seg, ease, ease_out, lerp, clamp, schematic_tag

AMBER = (226, 170, 84)
RED = (214, 96, 72)


def beeps(c, y, pattern, x0, x1, t, col, a, h=46, speed=1.2):
    """Draw a pulse train; pattern = list of (on, off) seconds, revealed left to right over time."""
    total = sum(on + off for on, off in pattern)
    reveal = clamp(t / speed)
    sc = (x1 - x0) / total
    c.line([(x0, y + h), (x1, y + h)], col, 2, a * 0.5)
    pos = 0.0
    for on, off in pattern:
        if pos / total > reveal:
            break
        xa, xb = x0 + pos * sc, x0 + (pos + on) * sc
        c.rect((xa, y, xb, y + h), fill=col, a=a)
        pos += on + off


@diagram
def pulse(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    a = seg(t, 0, 0.4)
    x0, x1 = 90, c.w - 90
    c.text(x0, 70, "what a listener heard", size=35, col=ink, a=a)
    c.text(x0, 150, "normal inside", size=29, col=pal["grey"], a=a)
    beeps(c, 190, [(0.3, 0.3)] * 8, x0, x1, t, AMBER, a, speed=1.6)
    c.text(x0, 270, "0.3 s on · 0.3 s off", size=27, col=pal["grey"], a=seg(t, 1.0, 0.5))
    b = seg(t, 2.0, 0.5)
    c.text(x0, 380, "too hot or too cold", size=29, col=pal["grey"], a=b)
    beeps(c, 420, [(0.3, 0.3), (0.3, 0.3), (0.6, 0.3), (0.6, 0.3), (0.3, 0.3), (0.3, 0.3)], x0, x1,
          max(0.0, t - 2.0), RED, b, speed=1.6)
    c.text(x0, 500, "the beeps change length", size=27, col=pal["grey"], a=seg(t, 3.4, 0.5))
    # thermometer
    tx, ty = c.w - 150, 560
    k = seg(t, 2.4, 0.8)
    c.rect((tx - 12, ty, tx + 12, ty + 110), col=ink, width=2, a=b, radius=12)
    c.circle(tx, ty + 128, 24, col=ink, fill=RED, width=2, a=b)
    c.rect((tx - 6, lerp(ty + 104, ty + 12, k), tx + 6, ty + 110), fill=RED, a=b)
    schematic_tag(c, pal, "schematic · drawn for this video", a)


@diagram
def timeline(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    a = seg(t, 0, 0.4)
    x0, x1 = 90, c.w - 90
    y = 330
    c.line([(x0, y), (x1, y)], ink, 2, a)
    days = 92.0  # 4 Oct 1957 -> 4 Jan 1958

    def X(d):
        return lerp(x0, x1, d / days)
    marks = [(0, "4 oct 1957", "launch"), (22, "26 oct", "batteries dead"), (92, "4 jan 1958", "falls, burns up")]
    for i, (d, l1, l2) in enumerate(marks):
        m = seg(t, 0.3 + i * 0.9, 0.4)
        c.line([(X(d), y - 14), (X(d), y + 14)], ink, 3, m)
        anc = "la" if i == 0 else ("ra" if i == 2 else "ma")
        dy = 110 if i == 1 else 0
        if i == 1:
            c.line([(X(d), y + 14), (X(d), y + 30 + dy)], ink, 1, m * 0.6)
            anc = "la"
        c.text(X(d), y + 34 + dy, l1, size=29, col=ink, a=m, anchor=anc)
        c.text(X(d), y + 70 + dy, l2, size=27, col=pal["grey"], a=m, anchor=anc)
    # signal trace: beeps until day 22, then flat line
    k = clamp((t - 0.4) / 2.2)
    end_d = lerp(0, days, k)
    sy = y - 120
    d = 0.0
    while d < min(end_d, 22):
        c.rect((X(d), sy - 30, X(d + 0.9), sy), fill=AMBER, a=a)
        d += 1.8
    if end_d > 22:
        c.line([(X(22), sy), (X(end_d), sy)], pal["grey"], 2, a)
        c.text(X(22) + 14, sy - 66, "silence", size=32, col=pal["grey"], a=seg(t, 1.6, 0.5), face="mono")
    c.text(x0, sy - 66, "signal", size=32, col=AMBER, a=a)
    c.text(x0, 600, "the ball kept orbiting, silent, for ten more weeks", size=27, col=pal["grey"],
           a=seg(t, 2.8, 0.6))
    schematic_tag(c, pal, "schematic · drawn for this video", a)


DIAGRAMS = {"pulse": pulse, "timeline": timeline}
