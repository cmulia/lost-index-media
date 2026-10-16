"""Original diagrams for file no. 010 (the first photo from space)."""
import math

from lostindex.diag import diagram, seg, ease, ease_out, lerp, clamp, schematic_tag

OCHRE = (214, 158, 74)


def axis(c, pal, a, top_km=110):
    ink = pal["panel_ink"] if pal.get("panel") == (34, 33, 31) else pal["ink"]
    x = 170
    y0, y1 = c.h - 90, 70

    def Y(km):
        return lerp(y0, y1, km / top_km)
    c.line([(x, y0), (x, y1)], ink, 2, a)
    for km in range(0, top_km + 1, 10):
        w = 16 if km % 50 == 0 else 8
        c.line([(x - w, Y(km)), (x, Y(km))], ink, 2, a)
        if km % 20 == 0:
            c.text(x - 26, Y(km) - 12, f"{km} km", size=20, col=pal["grey"], a=a, anchor="ra")
    return x, Y, ink


@diagram
def altitude_balloon(c, p, t, pal, beat):
    a = seg(t, 0, 0.5)
    x, Y, ink = axis(c, pal, a)
    k = seg(t, 0.5, 1.4)
    top = lerp(0, 22, k)
    c.rect((x + 50, Y(top), x + 110, Y(0)), fill=(170, 164, 150), a=a)
    bx, by = x + 80, Y(top) - 54
    c.ellipse((bx - 34, by - 44, bx + 34, by + 40), col=ink, width=3, a=k)
    c.line([(bx - 10, by + 38), (bx, by + 54)], ink, 2, k)
    c.line([(bx + 10, by + 38), (bx, by + 54)], ink, 2, k)
    c.text(x + 150, Y(22) - 30, "explorer ii balloon · 1935", size=24, col=ink, a=seg(t, 1.6, 0.5))
    c.text(x + 150, Y(22) + 4, "22 km · 13.7 mi", size=24, col=pal["grey"], a=seg(t, 1.6, 0.5))
    c.text(x + 150, Y(22) + 38, "the highest photographs, until 1946", size=20, col=pal["grey"], a=seg(t, 2.0, 0.5))
    schematic_tag(c, pal, "schematic · to scale", a)


@diagram
def altitude_v2(c, p, t, pal, beat):
    a = seg(t, 0, 0.3)
    x, Y, ink = axis(c, pal, a)
    c.rect((x + 50, Y(22), x + 110, Y(0)), fill=(110, 106, 98), a=a * 0.7)
    c.text(x + 130, Y(22) - 12, "balloon", size=18, col=pal["grey"], a=a)
    k = ease_out(clamp((t - 0.2) / 2.6))
    top = lerp(0, 105, k)
    c.rect((x + 190, Y(top), x + 214, Y(0)), fill=OCHRE, a=a)
    # karman line
    ka = seg(t, 1.6, 0.6)
    c.dashed((x, Y(100)), (c.w - 40, Y(100)), pal["grey"], 2, 12, 10, ka)
    c.text(c.w - 40, Y(100) + 12, "100 km · the edge of space (a later convention)", size=20, col=pal["grey"], a=ka,
           anchor="ra")
    if k > 0.98:
        aa = seg(t, 2.9, 0.4)
        c.line([(x + 180, Y(105)), (x + 224, Y(105))], ink, 3, aa)
        c.text(x + 240, Y(105) - 40, "v-2 no. 13 · ~105 km · 65 mi", size=24, col=ink, a=aa)
    schematic_tag(c, pal, "schematic · to scale", a)


@diagram
def filmstrip(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    W, H = c.w, c.h
    a = seg(t, 0, 0.4)
    sx0, sx1 = W * 0.30, W * 0.70
    fh = 230
    off = (t * 70) % fh
    c.rect((sx0, -10, sx1, H + 10), fill=(22, 21, 20), a=a)
    for k in range(-1, H // fh + 2):
        y = k * fh - off + 20
        c.rect((sx0 + 50, y, sx1 - 50, y + fh - 30), fill=(92, 90, 86), a=a)
        for s in range(5):
            yy = y + s * fh / 5
            c.rect((sx0 + 14, yy, sx0 + 32, yy + 22), fill=(200, 196, 186), a=a, radius=3)
            c.rect((sx1 - 32, yy, sx1 - 14, yy + 22), fill=(200, 196, 186), a=a, radius=3)
    n = int(t / 1.5) + 1
    c.rect((W - 250, 40, W - 40, 110), fill=(22, 21, 20), col=ink, width=2, a=a)
    c.text(W - 145, 52, f"{n:03d}", size=44, col=OCHRE, a=a, anchor="ma", face="mono_med")
    c.text(W - 145, 126, "frame", size=20, col=pal["grey"], a=a, anchor="ma")
    c.text(60, 60, "1 frame / 1.5 s", size=26, col=ink, a=a)
    schematic_tag(c, pal, "schematic · frames left blank", a)


DIAGRAMS = {"altitude_balloon": altitude_balloon, "altitude_v2": altitude_v2, "filmstrip": filmstrip}
