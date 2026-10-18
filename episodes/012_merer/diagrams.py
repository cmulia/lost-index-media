"""Original diagrams for file no. 012 (the pyramid builder's logbook)."""
import math

from lostindex.diag import diagram, seg, lerp, clamp, schematic_tag

RED = (176, 52, 40)
SEA = (178, 192, 192)
PAPYRUS = (214, 196, 156)
INK_BROWN = (92, 62, 36)


def dashed_path(c, pts, col, width=3, dash=12, gap=9, frac=1.0, a=1.0):
    """Dashed polyline drawn on up to `frac` of its length."""
    lens = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    total = sum(lens) * clamp(frac)
    pos = 0.0
    for i, L in enumerate(lens):
        if pos >= total:
            break
        take = min(L, total - pos)
        p0, p1 = pts[i], pts[i + 1]
        q = (lerp(p0[0], p1[0], take / L), lerp(p0[1], p1[1], take / L)) if L else p0
        c.dashed(p0, q, col, width, dash, gap, a)
        pos += L
    return pos


def point_on(pts, frac):
    lens = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    d = sum(lens) * clamp(frac)
    for i, L in enumerate(lens):
        if d <= L:
            f = d / L if L else 0
            return (lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f))
        d -= L
    return pts[-1]


def pyramid_glyph(c, x, y, s, col, a):
    c.polygon([(x - s, y + s * 0.8), (x, y - s * 0.8), (x + s, y + s * 0.8)], fill=col, a=a)


# ---------------------------------------------------------------- map

COAST = [(0, 112), (120, 108), (210, 96), (280, 84), (340, 78), (400, 80), (470, 90), (560, 104), (640, 114),
         (720, 118), (820, 112), (936, 104)]
# gulf of suez: its head (suez) sits about level with giza, cut off from the mediterranean by the isthmus
GULF_W = [(668, 300), (676, 380), (692, 460), (712, 550), (738, 650), (764, 760)]
GULF_E = [(668, 300), (700, 370), (732, 450), (770, 540), (820, 640), (884, 700), (936, 720), (936, 760)]
NILE = [(284, 760), (298, 670), (288, 590), (304, 510), (300, 440), (312, 360), (306, 300)]
ROSETTA = [(306, 300), (282, 230), (258, 160), (238, 98)]
DAMIETTA = [(306, 300), (340, 230), (380, 160), (430, 88)]
TURA = (322, 470)
GIZA = (240, 330)
ROUTE = [(316, 470), (306, 430), (304, 392), (298, 360), (286, 340)]


@diagram
def egypt_map(c, p, t, pal, beat):
    ink, grey = pal["ink"], pal["grey"]
    W, H = c.w, c.h
    a0 = seg(t, 0, 0.5)
    c.rect((1, 1, W - 1, H - 1), col=pal["rule"], width=2, a=a0)
    # seas
    sa = seg(t, 0.1, 0.8) * 0.55
    c.polygon([(0, 0), (W, 0)] + list(reversed(COAST)), fill=SEA, a=sa)
    c.polygon(GULF_W + list(reversed(GULF_E)), fill=SEA, a=sa)
    # coastlines and river, drawn on
    c.partial_line(COAST, ink, 2.5, seg(t, 0, 0.9))
    c.partial_line(GULF_W, ink, 2.5, seg(t, 0.3, 0.9))
    c.partial_line(GULF_E, ink, 2.5, seg(t, 0.4, 0.9))
    c.partial_line(NILE, (64, 92, 104), 5, seg(t, 0.2, 1.0))
    c.partial_line(ROSETTA, (64, 92, 104), 3.5, seg(t, 0.9, 0.5))
    c.partial_line(DAMIETTA, (64, 92, 104), 3.5, seg(t, 0.9, 0.5))
    la = seg(t, 0.9, 0.5)
    c.text(W / 2 + 40, 26, "mediterranean sea", size=32, col=grey, a=la, face="serif_i", anchor="ma")
    c.text(272, 640, "nile", size=32, col=grey, a=la, face="serif_i", anchor="ra")
    c.text(872, 714, "red sea", size=32, col=grey, a=la, face="serif_i", anchor="ma")
    c.text(850, 330, "sinai", size=26, col=grey, a=la * 0.8, face="serif_i", anchor="la")
    c.text(530, 380, "eastern desert", size=26, col=grey, a=la * 0.7, face="serif_i", anchor="ma")
    # north arrow
    c.arrow((W - 56, 236), (W - 56, 176), grey, 2.5, 12, a=la)
    c.text(W - 56, 244, "n", size=22, col=grey, a=la, anchor="ma")

    # wadi al-jarf: the find spot (pulsing)
    wj = point_on(GULF_W, 0.55)
    da = seg(t, 1.2, 0.3)
    for k in range(2):
        ph = ((t - 1.2) * 0.8 + k * 0.5) % 1.0
        if t > 1.2:
            c.circle(wj[0], wj[1], 12 + 34 * ph, col=RED, width=2.5, a=da * (1 - ph) * 0.8)
    c.circle(wj[0], wj[1], 11, fill=RED, a=da)
    wa = seg(t, 1.4, 0.4)
    c.text(wj[0] - 28, wj[1] - 36, "wadi al-jarf", size=27, col=ink, a=wa, face="mono_med", anchor="ra")
    c.text(wj[0] - 28, wj[1] + 2, "papyri found 2013", size=22, col=RED, a=wa, anchor="ra")
    c.text(wj[0] - 28, wj[1] + 32, "ancient harbour", size=20, col=grey, a=wa, anchor="ra")

    # giza and tura
    ga = seg(t, 2.0, 0.4)
    pyramid_glyph(c, GIZA[0], GIZA[1], 20, ink, ga)
    c.text(GIZA[0] - 32, GIZA[1] - 30, "giza", size=27, col=ink, a=ga, face="mono_med", anchor="ra")
    c.text(GIZA[0] - 32, GIZA[1] + 4, "akhet-khufu", size=21, col=grey, a=ga, anchor="ra")
    c.circle(TURA[0], TURA[1], 7, fill=ink, a=ga)
    c.text(TURA[0] + 22, TURA[1] - 16, "tura", size=27, col=ink, a=ga, face="mono_med")
    c.text(TURA[0] + 22, TURA[1] + 18, "limestone quarries", size=21, col=grey, a=ga)
    # the boat route tura -> giza, drawn on, with a little boat at its head
    rf = seg(t, 2.5, 1.3)
    if rf > 0:
        dashed_path(c, ROUTE, RED, 3, 10, 7, rf)
        bx, by = point_on(ROUTE, rf)
        c.polygon([(bx - 12, by - 3), (bx + 12, by - 3), (bx + 7, by + 5), (bx - 7, by + 5)], fill=RED, a=1.0)
        c.line([(bx, by - 3), (bx, by - 18)], RED, 2)
    schematic_tag(c, pal, "schematic map · drawn for this video · not to scale", a0)


# ---------------------------------------------------------------- logbook strip

# one illustrative 10-day week in half-day cells; a round trip takes about 4 days
CYCLE = ["load", "down", "night", "down", "arrive", "up", "night", "up"]
CELLS = [CYCLE[k % len(CYCLE)] for k in range(20)]
LEGEND = [("load", "load stone · tura"), ("down", "sail downriver"), ("arrive", "arrive · akhet-khufu"),
          ("up", "sail back upriver"), ("night", "night at she-khufu / camp")]


def icon(c, kind, x, y, s, col, a, bg):
    if a <= 0:
        return
    if kind == "load":
        c.rect((x - s, y - s * 0.55, x + s, y + s * 0.55), fill=col, a=a)
        c.line([(x - s * 0.15, y - s * 0.55), (x - s * 0.15, y + s * 0.55)], bg, 2, a)
        c.line([(x - s, y), (x - s * 0.15, y)], bg, 2, a)
    elif kind in ("down", "up"):
        c.polygon([(x - s, y), (x + s, y), (x + s * 0.6, y + s * 0.45), (x - s * 0.6, y + s * 0.45)], fill=col, a=a)
        c.line([(x, y), (x, y - s * 0.95)], col, 2.5, a)
        c.polygon([(x + 2, y - s * 0.9), (x + 2, y - s * 0.2), (x + s * 0.55, y - s * 0.25)], fill=col, a=a)
        d = 1 if kind == "down" else -1
        ay = y + s * 0.95
        c.arrow((x - d * s * 0.7, ay), (x + d * s * 0.7, ay), col, 2.5, 8, a)
    elif kind == "night":
        c.circle(x, y, s * 0.7, fill=col, a=a)
        c.circle(x + s * 0.32, y - s * 0.18, s * 0.6, fill=bg, a=a)
    elif kind == "arrive":
        pyramid_glyph(c, x, y, s * 0.9, col, a)


@diagram
def logbook_days(c, p, t, pal, beat):
    ink, grey = pal["panel_ink"], pal["grey"]
    W, H = c.w, c.h
    dur = max(3.0, beat.get("end", 8.0) - beat.get("start", 0.0))
    a0 = seg(t, 0, 0.5)
    c.text(40, 40, "one ten-day week", size=34, col=ink, a=a0, face="serif_i")
    c.text(W - 40, 52, "in half-day steps", size=22, col=grey, a=a0, anchor="ra")
    x0, cw, gap = 30, 85, 3.6
    ytop, chh = 160, 108
    for d in range(10):
        x = x0 + d * (cw + gap)
        c.text(x + cw / 2, ytop - 40, f"day {d + 1}", size=19, col=grey, a=seg(t, 0.1 + d * 0.04, 0.4), anchor="ma")
        for h in range(2):
            y = ytop + h * (chh + 6)
            c.rect((x, y, x + cw, y + chh), col=(110, 100, 84), width=1.5, a=seg(t, 0.1 + d * 0.04, 0.4))
    # fill cells one by one
    t_first, t_last = 0.5, dur * 0.80
    step = (t_last - t_first) / 20
    for k, kind in enumerate(CELLS):
        d, h = divmod(k, 2)
        x = x0 + d * (cw + gap)
        y = ytop + h * (chh + 6)
        ca = seg(t, t_first + k * step, 0.22)
        if ca <= 0:
            continue
        c.rect((x + 2, y + 2, x + cw - 2, y + chh - 2), fill=PAPYRUS, a=ca)
        icon(c, kind, x + cw / 2, y + chh / 2 - 8, 22, INK_BROWN, ca, PAPYRUS)
        c.text(x + 8, y + chh - 26, "am" if h == 0 else "pm", size=15, col=(140, 118, 84), a=ca * 0.9)
    # round-trip brackets under the strip
    by = ytop + 2 * chh + 6 + 26
    for n in range(3):
        k0, k1 = n * 8, min(20, n * 8 + 8)
        tb = t_first + (k1 - 1) * step + 0.15
        ba = seg(t, tb, 0.35)
        if ba <= 0:
            continue
        xa = x0 + (k0 // 2) * (cw + gap) + 4
        xb = x0 + ((k1 - 1) // 2) * (cw + gap) + cw - 4
        if n < 2:
            c.line([(xa, by), (xa, by + 14), (xb, by + 14), (xb, by)], ink, 2, ba)
            c.text((xa + xb) / 2, by + 26, f"round trip {n + 1}", size=21, col=ink, a=ba, anchor="ma")
        else:
            c.line([(xa, by), (xa, by + 14)], ink, 2, ba)
            c.dashed((xa, by + 14), (xb + 30, by + 14), ink, 2, 8, 6, ba)
            c.text((xa + xb) / 2 + 10, by + 26, "trip 3…", size=21, col=ink, a=ba, anchor="ma")
    # legend
    la = seg(t, 1.0, 0.6)
    ly = 524
    for i, (kind, txt) in enumerate(LEGEND):
        col_x = 60 if i < 3 else 500
        yy = ly + (i % 3) * 64
        c.rect((col_x - 6, yy - 26, col_x + 52, yy + 30), fill=PAPYRUS, a=la, radius=4)
        icon(c, kind, col_x + 23, yy - 4, 16, INK_BROWN, la, PAPYRUS)
        c.text(col_x + 72, yy - 14, txt, size=22, col=ink, a=la)
    schematic_tag(c, pal, "illustration · drawn for this video · not a transcription of the papyrus", a0)


DIAGRAMS = {"egypt_map": egypt_map, "logbook_days": logbook_days}
