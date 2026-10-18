"""Original diagrams for file no. 013 (the airship dock on the Empire State Building)."""
import math

from lostindex.diag import diagram, seg, ease, lerp, clamp, schematic_tag

RED = (176, 52, 40)
OCHRE = (214, 158, 74)
SKY = (120, 150, 170)


def grow(pts, base_y, top_y, frac):
    """Clip a silhouette so it appears to rise from base_y up to top_y as frac goes 0 -> 1."""
    clip = lerp(base_y, top_y, clamp(frac))
    return [(x, max(y, clip)) for x, y in pts]


def hull(cx, cy, L, Hh, ang, n=48, k=2.6):
    """Cigar-shaped airship outline (superellipse) centred on (cx, cy), rotated by ang radians."""
    ca, sa = math.cos(ang), math.sin(ang)
    out = []
    for i in range(n):
        th = 2 * math.pi * i / n
        c, s = math.cos(th), math.sin(th)
        x = (L / 2) * math.copysign(abs(c) ** (2 / k), c)
        y = (Hh / 2) * math.copysign(abs(s) ** (2 / k), s)
        out.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return out


def rot(cx, cy, ang, pts):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def airship(c, cx, cy, L, Hh, ang, ink, fill, a, width=2.5):
    """Hull + tail fins + gondola. Nose points along +x before rotation."""
    if a <= 0:
        return
    fins = [[(-L * 0.36, -Hh * 0.30), (-L * 0.50, -Hh * 0.78), (-L * 0.50, -Hh * 0.22)],
            [(-L * 0.36, Hh * 0.30), (-L * 0.50, Hh * 0.78), (-L * 0.50, Hh * 0.22)]]
    for f in fins:
        c.polygon(rot(cx, cy, ang, f), fill=fill, col=ink, a=a, width=width * 0.8)
    c.polygon(hull(cx, cy, L, Hh, ang), fill=fill, col=ink, a=a, width=width)
    # longitudinal girders, faint
    for yy in (-0.18, 0.18):
        c.line(rot(cx, cy, ang, [(-L * 0.42, Hh * yy), (L * 0.42, Hh * yy)]), ink, 1, a * 0.35)
    gx = L * 0.16
    c.polygon(rot(cx, cy, ang, [(gx - 26, Hh / 2 - 2), (gx + 22, Hh / 2 - 2), (gx + 16, Hh / 2 + 14),
                                (gx - 20, Hh / 2 + 14)]), fill=ink, a=a)


# ---------------------------------------------------------------- beat 3: the height race

@diagram
def mast_height(c, p, t, pal, beat):
    ink, grey = pal["ink"], pal["grey"]
    W, H = c.w, c.h
    ground = H - 92
    top = 92
    ft = (ground - top) / 1250.0           # px per foot, 1,250 ft fills the panel

    def Y(feet):
        return ground - feet * ft

    a0 = seg(t, 0.0, 0.4)
    c.line([(40, ground), (W - 40, ground)], grey, 2, a0)
    for k in (250, 500, 750, 1000, 1250):
        c.dashed((40, Y(k)), (78, Y(k)), grey, 1.5, 4, 4, a0 * 0.8)
        c.text(84, Y(k) - 10, f"{k:,}", size=17, col=grey, a=a0 * 0.8)

    # Chrysler Building, to the same scale (1,046 ft with its spire)
    ch = W * 0.22
    cpts = [(ch - 95, ground), (ch - 95, Y(330)), (ch - 72, Y(330)), (ch - 72, Y(560)), (ch - 56, Y(560)),
            (ch - 56, Y(800)), (ch - 46, Y(840)), (ch - 34, Y(880)), (ch - 22, Y(915)), (ch - 8, Y(950)),
            (ch, Y(1046)), (ch + 8, Y(950)), (ch + 22, Y(915)), (ch + 34, Y(880)), (ch + 46, Y(840)),
            (ch + 56, Y(800)), (ch + 56, Y(560)), (ch + 72, Y(560)), (ch + 72, Y(330)), (ch + 95, Y(330)),
            (ch + 95, ground)]
    gc = seg(t, 0.15, 1.1)
    c.polygon(grow(cpts, ground, Y(1046), gc), fill=grey, a=0.55 * seg(t, 0.15, 0.2))
    # crown arches
    ca = seg(t, 1.1, 0.4)
    for k, fy in enumerate((805, 845, 885)):
        w = 52 - k * 12
        c.arc((ch - w, Y(fy) - 10, ch + w, Y(fy) + 34), 180, 360, pal["bg"], 2, ca * 0.9)
    c.text(ch, ground + 16, "chrysler", size=22, col=ink, a=seg(t, 0.4, 0.4), anchor="ma")
    c.text(ch + 22, Y(1046) - 40, "1,046 ft", size=40, col=ink, a=seg(t, 1.2, 0.4), face="serif_i")

    # Empire State Building, setbacks to the 86th-floor roof (~1,050 ft)
    ex = W * 0.55
    roof = 1050
    epts = [(ex - 128, ground), (ex - 128, Y(85)), (ex - 104, Y(85)), (ex - 104, Y(260)), (ex - 84, Y(260)),
            (ex - 84, Y(880)), (ex - 66, Y(880)), (ex - 66, Y(980)), (ex - 50, Y(980)), (ex - 50, Y(roof)),
            (ex + 50, Y(roof)), (ex + 50, Y(980)), (ex + 66, Y(980)), (ex + 66, Y(880)), (ex + 84, Y(880)),
            (ex + 84, Y(260)), (ex + 104, Y(260)), (ex + 104, Y(85)), (ex + 128, Y(85)), (ex + 128, ground)]
    ge = seg(t, 0.0, 1.2)
    c.polygon(grow(epts, ground, Y(roof), ge), fill=ink, a=0.88 * seg(t, 0.0, 0.2))
    for k in range(6):                    # window piers
        x = ex - 60 + k * 24
        c.line([(x, max(Y(870), lerp(ground, Y(870), ge))), (x, Y(270))], pal["bg"], 1, 0.25 * seg(t, 0.8, 0.4))
    c.text(ex, ground + 16, "empire state", size=22, col=ink, a=seg(t, 0.4, 0.4), anchor="ma")
    ra = seg(t, 1.0, 0.4)
    c.line([(ex + 54, Y(roof) + 4), (ex + 132, Y(960))], grey, 1.5, ra)
    c.text(ex + 138, Y(960) - 4, "86th-floor roof", size=21, col=grey, a=ra)
    c.text(ex + 138, Y(960) + 22, "≈ 1,050 ft", size=21, col=grey, a=ra)

    # the mooring mast, in red: ~200 ft more, to 1,250 ft
    mpts = [(ex - 34, Y(roof)), (ex - 26, Y(1110)), (ex - 18, Y(1160)), (ex - 10, Y(1205)), (ex - 5, Y(1235)),
            (ex - 3, Y(1250)), (ex + 3, Y(1250)), (ex + 5, Y(1235)), (ex + 10, Y(1205)), (ex + 18, Y(1160)),
            (ex + 26, Y(1110)), (ex + 34, Y(roof))]
    gm = seg(t, 1.5, 0.9)
    if gm > 0:
        c.polygon(grow(mpts, Y(roof), Y(1250), gm), fill=RED, a=0.95)
    pa = seg(t, 2.3, 0.4)
    c.line([(ex - 14, Y(1224)), (ex + 14, Y(1224))], pal["bg"], 3, pa)
    c.line([(ex + 16, Y(1224)), (ex + 132, Y(1224))], grey, 1.5, pa)
    c.text(ex + 138, Y(1224) - 12, "102nd-floor platform", size=21, col=grey, a=pa)
    c.text(ex + 24, Y(1250) - 64, "1,250 ft", size=48, col=RED, a=seg(t, 2.2, 0.4), face="serif_i")
    c.text(ex + 138, Y(1135) - 12, "mooring mast", size=21, col=RED, a=seg(t, 1.9, 0.4), face="mono_med")
    c.text(ex + 138, Y(1135) + 16, "+ ≈ 200 ft", size=21, col=RED, a=seg(t, 1.9, 0.4))

    # dashed line across from the Chrysler tip: only the mast clears it
    c.dashed((ch, Y(1046)), (ex + 34, Y(1046)), RED, 2, 10, 7, seg(t, 2.6, 0.2) * 0.9, frac=seg(t, 2.6, 0.8))

    # a small airship, nose in at the tip
    sa = seg(t, 3.0, 0.6)
    bob = math.sin(t * 1.6) * 3
    L = 150
    airship(c, ex - 3 - L / 2 - 6, Y(1250) + 10 + bob, L, 40, 0.0, ink, pal["bg"], sa, width=2)
    schematic_tag(c, pal, "schematic · drawn for this video · heights approximate", a0)


# ---------------------------------------------------------------- beat 5: the three-minute touch

@diagram
def mast_approach(c, p, t, pal, beat):
    ink, grey = pal["panel_ink"], pal["grey"]
    W, H = c.w, c.h
    a0 = seg(t, 0.0, 0.4)
    mx = W * 0.74                          # mast axis
    tip_y = 238
    crown_y = 560

    # tower crown (setback shoulders) and the mast, close up
    tower = [(mx - 150, H), (mx - 150, crown_y + 120), (mx - 112, crown_y + 120), (mx - 112, crown_y + 40),
             (mx - 78, crown_y + 40), (mx - 78, crown_y), (mx + 78, crown_y), (mx + 78, crown_y + 40),
             (mx + 112, crown_y + 40), (mx + 112, crown_y + 120), (mx + 150, crown_y + 120), (mx + 150, H)]
    c.polygon(tower, fill=(58, 56, 52), col=ink, a=a0, width=2)
    mast = [(mx - 58, crown_y), (mx - 44, crown_y - 120), (mx - 30, crown_y - 220), (mx - 16, tip_y + 40),
            (mx - 8, tip_y + 8), (mx + 8, tip_y + 8), (mx + 16, tip_y + 40), (mx + 30, crown_y - 220),
            (mx + 44, crown_y - 120), (mx + 58, crown_y)]
    c.polygon(mast, fill=(72, 70, 65), col=ink, a=a0, width=2)
    for k in range(5):                     # vertical fins of the mast
        x = mx - 30 + k * 15
        c.line([(x, crown_y - 6), (lerp(x, mx, 0.7), tip_y + 50)], ink, 1, a0 * 0.4)
    c.rect((mx - 10, tip_y - 6, mx + 10, tip_y + 10), fill=OCHRE, a=a0)      # mooring cone / arm
    c.text(mx + 26, tip_y - 6, "mooring arm", size=19, col=grey, a=seg(t, 0.5, 0.4))

    # updrafts racing up the walls, curling out toward the airship's tail (loop forever)
    for k in range(5):
        ph = ((t * 0.55 + k / 5) % 1.0)
        x0 = mx - 175 - (k % 2) * 34
        y0 = H - 30 - k * 8
        y1 = crown_y - 110 - ph * 170
        pts = []
        for i in range(14):
            s = i / 13
            y = lerp(y0, y1, s)
            x = x0 - 70 * s ** 2.2 - 230 * s ** 5
            pts.append((x, y))
        fade = math.sin(ph * math.pi)
        c.partial_line(pts, SKY, 2.5, clamp(ph * 1.6), a0 * fade * 0.9)
        if ph > 0.55:
            end = pts[min(13, int(13 * clamp(ph * 1.6)))]
            prev = pts[max(0, min(13, int(13 * clamp(ph * 1.6))) - 1)]
            c.arrow(prev, end, SKY, 2.5, 12, a0 * fade * 0.9)
    c.text(46, H - 70, "updrafts", size=21, col=SKY, a=seg(t, 0.8, 0.4))

    # the airship noses in from the left on a line, then is buffeted, tail lifting
    arrive = seg(t, 0.2, 2.0)
    L, Hh = 420, 104
    nose_x = lerp(-120, mx - 22, arrive)
    nose_y = tip_y + 2 + (1 - arrive) * 70
    buffet = seg(t, 1.8, 0.8)
    ang = -(0.05 + 0.07 * math.sin(t * 2.3) + 0.04 * math.sin(t * 5.1)) * buffet   # negative = tail up
    cx = nose_x - (L / 2) * math.cos(ang)
    cy = nose_y - (L / 2) * math.sin(ang)
    airship(c, cx, cy, L, Hh, ang, ink, (46, 45, 42), 1.0, width=2.5)
    # the mooring line from the nose to the mast
    la = seg(t, 1.6, 0.5)
    c.line([(nose_x, nose_y), (mx - 10, tip_y + 2)], OCHRE, 2, la)

    # stopwatch: about three minutes
    sw = seg(t, 2.2, 0.4)
    sx, sy, r = 110, 116, 52
    c.circle(sx, sy, r, col=ink, width=3, a=sw)
    c.rect((sx - 9, sy - r - 16, sx + 9, sy - r - 4), fill=ink, a=sw)
    for k in range(12):
        an = k / 12 * 2 * math.pi
        c.line([(sx + (r - 10) * math.sin(an), sy - (r - 10) * math.cos(an)),
                (sx + (r - 4) * math.sin(an), sy - (r - 4) * math.cos(an))], ink, 2, sw)
    sweep = clamp((t - 2.4) / 2.0) * 0.30   # three of ten minutes on the dial
    an = sweep * 2 * math.pi
    if sweep > 0:
        pts = [(sx, sy)] + [(sx + (r - 14) * math.sin(an * i / 16), sy - (r - 14) * math.cos(an * i / 16))
                            for i in range(17)]
        c.polygon(pts, fill=OCHRE, a=sw * 0.35)
    c.line([(sx, sy), (sx + (r - 12) * math.sin(an), sy - (r - 12) * math.cos(an))], OCHRE, 3, sw)
    c.circle(sx, sy, 4, fill=ink, a=sw)
    c.text(sx + r + 22, sy - 26, "≈ 3 min", size=40, col=ink, a=seg(t, 3.0, 0.4), face="mono_med")
    c.text(sx + r + 22, sy + 24, "of contact, reported", size=20, col=grey, a=seg(t, 3.6, 0.4))
    schematic_tag(c, pal, "illustration · drawn for this video", a0)


DIAGRAMS = {"mast_height": mast_height, "mast_approach": mast_approach}
