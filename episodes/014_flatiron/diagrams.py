"""Original diagrams for file no. 014 (the Flatiron and "23 skidoo")."""
import math

from lostindex.diag import diagram, seg, ease, lerp, clamp, schematic_tag

RED = (176, 52, 40)
OCHRE = (214, 158, 74)
WIND = (62, 98, 136)


def point_on(pts, f):
    """Point at fraction f along a polyline."""
    lens = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(lens) * clamp(f)
    for i, L in enumerate(lens):
        if total <= L:
            k = total / L if L else 0
            return (lerp(pts[i][0], pts[i + 1][0], k), lerp(pts[i][1], pts[i + 1][1], k))
        total -= L
    return pts[-1]


def head(c, pa, pb, col, a, size=13, width=3):
    ang = math.atan2(pb[1] - pa[1], pb[0] - pa[0])
    l = (pb[0] - size * math.cos(ang - 0.5), pb[1] - size * math.sin(ang - 0.5))
    r = (pb[0] - size * math.cos(ang + 0.5), pb[1] - size * math.sin(ang + 0.5))
    c.line([l, pb, r], col, width, a)


def flow(c, pts, col, t, start, dur, a=1.0, width=3, n_particles=4, speed=0.45):
    """Draw a streamline on, give it an arrow head, then send particles along it."""
    f = seg(t, start, dur)
    c.partial_line(pts, col, width, f, a * 0.55)
    if f > 0.05:
        tip = point_on(pts, f)
        prev = point_on(pts, max(0.0, f - 0.04))
        head(c, prev, tip, col, a * 0.9, width=width)
    if f >= 1:
        for k in range(n_particles):
            q = ((t - start - dur) * speed + k / n_particles) % 1.0
            x, y = point_on(pts, q)
            c.circle(x, y, 4.5, fill=col, a=a * math.sin(math.pi * q))


@diagram
def wind_wedge(c, p, t, pal, beat):
    ink, grey = pal["ink"], pal["grey"]
    W, H = c.w, c.h
    a = seg(t, 0, 0.5)

    # streets (plan view, north up). 23rd St across the top of the block, 22nd St along its base.
    y23, y22 = 300, 650
    c.line([(40, y23 - 34), (W - 40, y23 - 34)], pal["rule"], 2, a)
    c.line([(40, y23 + 6), (W - 40, y23 + 6)], pal["rule"], 2, a)
    c.text(W - 46, y23 - 25, "23rd st", size=20, col=grey, a=a, anchor="ra")
    c.line([(40, y22 + 14), (W - 40, y22 + 14)], pal["rule"], 2, a)
    c.text(W - 46, y22 + 24, "22nd st", size=20, col=grey, a=a, anchor="ra")

    # the block: Fifth Avenue straight on the west, Broadway slanting on the east
    px = 380
    prow = [(px - 9, y23 + 18), (px + 9, y23 + 18)]
    block = [prow[0], prow[1], (px + 250, y22), (px - 9, y22)]
    c.polygon(block, fill=(205, 197, 181), a=a)
    c.line(block + [block[0]], ink, 3, a)
    c.text(px - 66, 470, "fifth", size=22, col=grey, a=a, anchor="ra")
    c.text(px - 66, 498, "ave", size=22, col=grey, a=a, anchor="ra")
    c.text(px + 196, 430, "broadway", size=22, col=grey, a=a, anchor="la")
    c.text(px + 76, 560, "the", size=20, col=ink, a=a * 0.8, anchor="ma")
    c.text(px + 76, 586, "flatiron", size=20, col=ink, a=a * 0.8, anchor="ma")

    # north arrow + Madison Square
    c.text(70, 40, "madison square", size=22, col=grey, a=a)
    c.arrow((W - 70, 88), (W - 70, 40), ink, 2, 10, a)
    c.text(W - 70, 96, "n", size=20, col=ink, a=a, anchor="ma")

    # prow width callout
    ca = seg(t, 0.5, 0.5)
    c.line([(px + 12, y23 + 18), (px + 150, y23 + 18)], RED, 2, ca)
    c.text(px + 158, y23 + 6, "prow ≈ 6.5 ft", size=24, col=RED, a=ca, face="mono_med")

    # the north wind, arriving from Madison Square
    for k, x in enumerate((px - 150, px - 80, px + 80, px + 150)):
        flow(c, [(x, 80), (x, 220)], WIND, t, 0.4 + 0.08 * k, 0.6, n_particles=2, speed=0.9)
    # the stream that hits the point and splits down both facades
    west = [(px - 4, 70), (px - 4, y23 - 10), (px - 34, y23 + 40), (px - 40, y22 - 10)]
    east = [(px + 4, 70), (px + 4, y23 - 10), (px + 40, y23 + 30), (px + 290, y22 - 20)]
    flow(c, west, WIND, t, 0.8, 1.2, n_particles=5)
    flow(c, east, WIND, t, 0.8, 1.2, n_particles=5)
    sa = seg(t, 1.8, 0.4)
    c.text(px - 172, 150, "north wind", size=22, col=WIND, a=sa, anchor="ra", face="mono_med")
    c.text(px - 66, 400, "splits", size=22, col=WIND, a=sa, anchor="ra", face="mono_med")
    c.text(px + 150, 400, "splits", size=22, col=WIND, a=sa, face="mono_med")

    # downdraft curling at the 23rd St corner (shown as a swirl)
    da = seg(t, 2.2, 0.6)
    if da > 0:
        cx, cy = px - 70, y23 - 6
        rot = t * 2.6
        pts = []
        for i in range(60):
            q = i / 59 * da
            ang = rot + q * 2.2 * math.pi
            rr = 10 + 34 * q
            pts.append((cx + rr * math.cos(ang), cy + rr * 0.55 * math.sin(ang)))
        c.line(pts, WIND, 3, 0.85 * da)
        head(c, pts[-3], pts[-1], WIND, 0.85 * da)
        c.text(cx - 50, cy + 40, "downdraft", size=22, col=WIND, a=da, anchor="ra", face="mono_med")

    # a few pedestrians at the corner, jostled once the gust arrives
    pa = seg(t, 0.3, 0.4)
    gust = seg(t, 2.0, 0.6)
    for k, (x, y) in enumerate(((px - 120, y23 - 14), (px - 96, y23 - 22), (px + 30, y23 - 18), (px + 62, y23 - 10),
                                (px - 140, y23 + 30))):
        jx = gust * 3.5 * math.sin(t * 9 + k * 1.7)
        jy = gust * 2.5 * math.cos(t * 11 + k)
        c.circle(x + jx, y + jy, 6, fill=ink, a=pa)

    schematic_tag(c, pal, "schematic · drawn for this video · not to scale", a)


@diagram
def skidoo_timeline(c, p, t, pal, beat):
    ink, grey = pal["panel_ink"], pal["grey"]
    W, H = c.w, c.h
    a = seg(t, 0, 0.5)
    y0, x0, x1 = 420, 70, W - 70
    y_lo, y_hi = 1898.5, 1906.8

    def X(year):
        return lerp(x0, x1, (year - y_lo) / (y_hi - y_lo))

    c.partial_line([(x0, y0), (x1, y0)], grey, 3, seg(t, 0, 0.8))
    for yr in range(1899, 1907):
        c.line([(X(yr), y0 - 8), (X(yr), y0 + 8)], grey, 2, a * 0.7)

    def marker(year, start, up, year_txt, line1, line2=None, col=ink, hl=False):
        m = seg(t, start, 0.45)
        if m <= 0:
            return
        x = X(year)
        if hl:
            c.glow(x, y0, 11, col, a=m)
        else:
            c.circle(x, y0, 9, fill=col, a=m)
        d = -1 if up else 1
        c.line([(x, y0 + d * 16), (x, y0 + d * 52)], col, 2, m)
        ty = y0 - 150 if up else y0 + 66
        c.text(x, ty, year_txt, size=46, col=col, a=m, face="serif_i", anchor="ma")
        c.text(x, ty + 56, line1, size=22, col=col, a=m, anchor="ma", face="mono_med")
        if line2:
            c.text(x, ty + 86, line2, size=20, col=grey, a=m, anchor="ma")

    marker(1899.2, 0.4, True, "1899", "“twenty-three”", "= clear out", col=OCHRE, hl=True)
    marker(1901.0, 1.0, False, "1901", "“skidoo”", "in print")
    # the building opens, with a tiny wedge icon
    marker(1902.75, 1.5, True, "oct 1902", "flatiron opens", None)
    ia = seg(t, 1.5, 0.45)
    xb = X(1902.75)
    c.polygon([(xb - 3, y0 - 214), (xb + 3, y0 - 214), (xb + 18, y0 - 166), (xb - 3, y0 - 166)], fill=ink, a=ia)
    marker(1906.0, 2.0, False, "1906", "“23 skidoo”", "catches on")

    # bracket: the slang came first
    ba = seg(t, 2.6, 0.7)
    xa, xbb = X(1899.2), X(1902.75)
    yb = 140
    c.partial_line([(xa, yb + 16), (xa, yb), (xbb, yb), (xbb, yb + 16)], RED, 3, ba)
    c.text((xa + xbb) / 2, yb - 40, "three years before the building", size=22, col=RED,
           a=seg(t, 3.0, 0.4), anchor="ma", face="mono_med")

    schematic_tag(c, pal, "illustration · drawn for this video", a)


DIAGRAMS = {"wind_wedge": wind_wedge, "skidoo_timeline": skidoo_timeline}
