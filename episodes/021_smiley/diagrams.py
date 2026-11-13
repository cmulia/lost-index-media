"""Original diagrams for file no. 021 (the smiley, 1982)."""
import math
from lostindex.diag import diagram, seg, ease, ease_out, lerp, clamp, schematic_tag

AMBER = (226, 170, 84)
RED = (214, 96, 72)
GREEN = (120, 190, 130)


def face(c, cx, cy, r, col, a, mouth="smile", eyes=True, width=5):
    c.circle(cx, cy, r, col=col, width=width, a=a)
    if eyes:
        c.circle(cx - r * 0.35, cy - r * 0.25, r * 0.07, fill=col, a=a)
        c.circle(cx + r * 0.35, cy - r * 0.25, r * 0.07, fill=col, a=a)
    if mouth == "smile":
        c.arc((cx - r * 0.55, cy - r * 0.45, cx + r * 0.55, cy + r * 0.55), 20, 160, col, width, a)
    elif mouth == "frown":
        c.arc((cx - r * 0.55, cy + r * 0.05, cx + r * 0.55, cy + r * 1.05), 200, 340, col, width, a)


@diagram
def elevator(c, p, t, pal, beat):
    ink = pal["ink"]
    a = seg(t, 0, 0.4)
    # elevator shaft
    x0, x1, y0, y1 = 90, 350, 90, 640
    c.rect((x0, y0, x1, y1), col=ink, width=3, a=a)
    c.line([((x0 + x1) / 2, y0), ((x0 + x1) / 2, y0 + 30)], ink, 2, a)
    k = ease(clamp(t / 2.2))
    cy = lerp(y0 + 40, y1 - 190, k)
    c.rect((x0 + 40, cy, x1 - 40, cy + 150), col=ink, width=3, a=a)
    c.line([((x0 + x1) / 2, y0 + 30), ((x0 + x1) / 2, cy)], ink, 2, a * 0.7)
    # mercury droplets
    for i in range(5):
        d = seg(t, 1.2 + i * 0.25, 0.8)
        px = x0 + 90 + i * 30
        c.circle(px, cy + 150 + d * 70, 11, fill=(190, 196, 205), col=ink, width=1, a=d * a)
    # warning note
    nx, ny = 410, 130
    n = seg(t, 0.6, 0.5)
    c.rect((nx, ny, nx + 440, ny + 150), col=RED, width=3, a=n, radius=6)
    c.text(nx + 24, ny + 26, "WARNING!", size=44, col=RED, a=n)
    c.text(nx + 24, ny + 88, "elevator contaminated", size=27, col=ink, a=n)
    # the joke
    j = seg(t, 2.4, 0.6)
    c.text(nx, 340, "...but it was a joke.", size=38, col=AMBER, a=j)
    c.text(nx, 410, "no tone of voice in text,", size=27, col=pal["grey"], a=seg(t, 3.0, 0.5))
    c.text(nx, 450, "so some readers missed it.", size=27, col=pal["grey"], a=seg(t, 3.0, 0.5))
    schematic_tag(c, pal, "schematic · drawn for this video", a)


@diagram
def sideways(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    a = seg(t, 0, 0.4)
    cx = c.w / 2
    # typed text
    typed = ":-)"
    n = int(clamp(t / 0.9) * 3 + 0.001)
    c.text(cx, 130, typed[:n], size=200, col=ink, a=a, anchor="ma")
    # rotate: face fades in as the text turns
    k = ease(clamp((t - 1.2) / 1.4))
    c.text(cx, 420, "read it sideways", size=34, col=pal["grey"], a=seg(t, 1.0, 0.5), anchor="ma")
    if k > 0:
        fy = 560
        c.arrow((cx - 200, 380), (cx - 200, 470), AMBER, 3, a=k)
        face(c, cx, fy, 90 * (0.6 + 0.4 * k), AMBER, k, "smile", eyes=True, width=6)
        c.text(cx + 140, fy - 10, ":  eyes", size=26, col=pal["grey"], a=seg(t, 2.6, 0.4))
        c.text(cx + 140, fy + 24, "-  nose", size=26, col=pal["grey"], a=seg(t, 2.8, 0.4))
        c.text(cx + 140, fy + 58, ")  mouth", size=26, col=pal["grey"], a=seg(t, 3.0, 0.4))
    schematic_tag(c, pal, "schematic · drawn for this video", a)


@diagram
def markers(c, p, t, pal, beat):
    ink = pal["ink"]
    a = seg(t, 0, 0.4)
    for i, (txt, col, mouth, lab1, lab2, t0) in enumerate([
            (":-)", GREEN, "smile", "joke", "post is a joke", 0.2),
            (":-(", RED, "frown", "not a joke", "post is serious", 1.8)]):
        cx = 250 + i * 440
        m = seg(t, t0, 0.5)
        c.text(cx, 90, txt, size=140, col=col, a=m, anchor="ma")
        face(c, cx, 440, 100, col, m, mouth, True, 6)
        c.text(cx, 590, lab1, size=38, col=ink, a=m, anchor="ma")
        c.text(cx, 640, lab2, size=26, col=pal["grey"], a=m, anchor="ma")
    schematic_tag(c, pal, "schematic · drawn for this video", a)


@diagram
def timeline(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    a = seg(t, 0, 0.4)
    x0, x1 = 90, c.w - 90
    y = 360
    c.line([(x0, y), (x1, y)], ink, 2, a)

    def X(yr):
        return lerp(x0, x1, (yr - 1982) / 20.0)
    marks = [(1982, "sep 1982", "post is written", 0), (2002, "sep 2002", "found again", 2)]
    for yr, l1, l2, i in marks:
        m = seg(t, 0.3 + i * 1.3, 0.5)
        c.line([(X(yr), y - 16), (X(yr), y + 16)], ink, 3, m)
        anc = "la" if i == 0 else "ra"
        c.text(X(yr), y + 36, l1, size=29, col=ink, a=m, anchor=anc)
        c.text(X(yr), y + 72, l2, size=27, col=pal["grey"], a=m, anchor=anc)
    # smiley spreads (solid bar), original post "missing" (dashed)
    k = clamp((t - 0.6) / 2.0)
    c.partial_line([(X(1982), y - 110), (X(2002), y - 110)], AMBER, 6, k, a)
    c.text(X(1982), y - 170, ":-)  keeps spreading", size=32, col=AMBER, a=seg(t, 0.8, 0.5))
    c.dashed((X(1982) + 30, y + 150), (X(2002) - 30, y + 150), pal["grey"], 3, 14, 12, a=seg(t, 1.4, 0.4), frac=clamp((t - 1.4) / 1.6))
    c.text(c.w / 2, y + 180, "the original post: nowhere to be found", size=30, col=RED, a=seg(t, 2.2, 0.6), anchor="ma")
    c.text(c.w / 2, y + 232, "about twenty years", size=27, col=pal["grey"], a=seg(t, 3.0, 0.5), anchor="ma")
    schematic_tag(c, pal, "schematic · drawn for this video", a)


@diagram
def tapes(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    a = seg(t, 0, 0.4)
    # a tape reel pair
    def reel(cx, cy, r, ang):
        c.circle(cx, cy, r, col=ink, width=4, a=a)
        c.circle(cx, cy, r * 0.25, col=ink, width=3, a=a)
        for i in range(3):
            th = ang + i * 2 * math.pi / 3
            c.line([(cx + r * 0.25 * math.cos(th), cy + r * 0.25 * math.sin(th)),
                    (cx + r * 0.85 * math.cos(th), cy + r * 0.85 * math.sin(th))], ink, 3, a * 0.8)
    ang = t * 3.2
    reel(300, 250, 120, ang)
    reel(780, 250, 120, ang)
    c.line([(300, 370), (390, 440), (690, 440), (780, 370)], ink, 3, a)
    c.rect((470, 410, 610, 470), col=ink, width=3, a=a)
    c.text(540, 482, "drive", size=24, col=pal["grey"], a=a, anchor="ma")
    # label
    c.text(c.w / 2, 560, "backup tape, october 1982", size=32, col=ink, a=seg(t, 0.4, 0.5), anchor="ma")
    # search steps
    s1 = seg(t, 1.2, 0.5)
    c.text(c.w / 2, 620, "step 1: find a drive that can still read it", size=28, col=pal["grey"], a=s1, anchor="ma")
    s2 = seg(t, 2.6, 0.5)
    c.text(c.w / 2, 664, "step 2: dig out the post  (done)", size=28, col=GREEN, a=s2, anchor="ma")
    schematic_tag(c, pal, "schematic · drawn for this video", a)


DIAGRAMS = {"elevator": elevator, "sideways": sideways, "markers": markers, "timeline": timeline, "tapes": tapes}
