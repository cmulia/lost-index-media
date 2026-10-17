"""Original diagrams for file no. 006 (speakers). All drawn for this video."""
import math

from lostindex.diag import diagram, seg, ease, lerp, clamp, schematic_tag

OCHRE = (214, 158, 74)


@diagram
def icons(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    W, H = c.w, c.h
    cells = [(W * 0.27, H * 0.30), (W * 0.73, H * 0.30), (W * 0.27, H * 0.72), (W * 0.73, H * 0.72)]
    names = ["phone", "earbuds", "car", "stadium"]
    for i, (cx, cy) in enumerate(cells):
        a = 1.0 if i == 0 else seg(t, 0.15 + i * 0.85, 0.35)   # phone on frame one (hook)
        if a <= 0:
            continue
        s = 1.0
        if i == 0:   # phone
            c.rect((cx - 70, cy - 130, cx + 70, cy + 130), col=ink, width=3, a=a, radius=22)
            c.line([(cx - 22, cy - 112), (cx + 22, cy - 112)], ink, 3, a)
            dot = (cx, cy + 112)
        elif i == 1:  # earbud
            c.circle(cx - 10, cy - 50, 54, col=ink, width=3, a=a)
            c.rect((cx + 14, cy - 30, cx + 46, cy + 120), col=ink, width=3, a=a, radius=16)
            dot = (cx - 22, cy - 50)
        elif i == 2:  # car side profile
            pts = [(cx - 170, cy + 50), (cx - 170, cy + 5), (cx - 120, cy - 5), (cx - 70, cy - 70), (cx + 60, cy - 70),
                   (cx + 120, cy - 8), (cx + 170, cy + 2), (cx + 170, cy + 50)]
            c.line(pts + [(cx - 170, cy + 50)], ink, 3, a)
            c.circle(cx - 100, cy + 52, 28, col=ink, fill=pal["panel"], width=3, a=a)
            c.circle(cx + 105, cy + 52, 28, col=ink, fill=pal["panel"], width=3, a=a)
            c.line([(cx - 5, cy - 70), (cx - 5, cy + 46)], ink, 2, a)
            dot = (cx - 45, cy + 22)
        else:  # stadium line-array
            for k in range(6):
                y0 = cy - 140 + k * 46
                c.rect((cx - 60 + k * 4, y0, cx + 60 - k * 4, y0 + 38), col=ink, width=3, a=a)
            c.line([(cx, cy - 175), (cx, cy - 140)], ink, 2, a)
            dot = (cx, cy - 140 + 2 * 46 + 19)
        pulse = 0.75 + 0.25 * math.sin(t * 5 + i)
        c.glow(dot[0], dot[1], 9, OCHRE, a * pulse)
        c.text(cx, cy + 165, names[i], size=22, col=pal["grey"], a=a, anchor="ma")


@diagram
def siemens(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    W, H = c.w, c.h
    cx, cy = W * 0.5, H * 0.46
    a = seg(t, 0.0, 0.6)
    # pot magnet cross-section: outer U and centre pole
    c.partial_line([(cx - 230, cy - 170), (cx - 230, cy + 170), (cx + 230, cy + 170), (cx + 230, cy - 170)], ink, 3,
                   seg(t, 0.1, 1.2), a)
    c.partial_line([(cx - 60, cy + 170), (cx - 60, cy - 120), (cx + 60, cy - 120), (cx + 60, cy + 170)], ink, 3,
                   seg(t, 0.4, 1.0), a)
    # hatching inside the walls
    for k in range(9):
        y = cy - 150 + k * 38
        c.line([(cx - 230, y + 12), (cx - 200, y - 12)], pal["grey"], 1.5, a * 0.6)
        c.line([(cx + 200, y + 12), (cx + 230, y - 12)], pal["grey"], 1.5, a * 0.6)
    # coil ring (two cross-sections either side of the pole), sliding up and down
    off = 34 * math.sin(t * 2.6) * seg(t, 1.4, 0.8)
    ca = seg(t, 1.2, 0.5)
    for sx in (-1, 1):
        x0 = cx + sx * 92
        c.rect((x0 - 22, cy - 90 + off, x0 + 22, cy + 10 + off), col=OCHRE, width=3, a=ca)
        for k in range(4):
            c.line([(x0 - 22, cy - 70 + k * 22 + off), (x0 + 22, cy - 70 + k * 22 + off)], OCHRE, 1.5, ca * 0.8)
    c.arrow((cx + 300, cy - 110), (cx + 300, cy + 40), ink, 2, 14, ca, both=True)
    c.text(cx + 322, cy - 50, "moves", size=22, col=pal["grey"], a=ca)
    c.text(cx - 230, cy + 196, "magnet", size=22, col=pal["grey"], a=a)
    c.text(cx + 92, cy - 132 + off, "coil", size=22, col=OCHRE, a=ca, anchor="ms")
    schematic_tag(c, pal, "schematic · after siemens, 1874 · not the patent drawing", a)


@diagram
def stereo(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    W, H = c.w, c.h
    a = seg(t, 0.0, 0.5)
    L = (W * 0.2, H * 0.24)
    R = (W * 0.8, H * 0.24)
    for (x, y), lab in ((L, "left"), (R, "right")):
        c.rect((x - 46, y - 70, x + 46, y + 70), col=ink, width=3, a=a, radius=8)
        c.circle(x, y + 22, 30, col=ink, width=3, a=a)
        c.circle(x, y - 38, 12, col=ink, width=2, a=a)
        c.text(x, y + 92, lab, size=22, col=pal["grey"], a=a, anchor="ma")
    hx, hy = W * 0.5, H * 0.70
    c.circle(hx, hy, 52, col=ink, width=3, a=a)
    c.line([(hx - 18, hy - 52), (hx, hy - 72), (hx + 18, hy - 52)], ink, 3, a)  # nose (facing up)
    c.ellipse((hx - 66, hy - 16, hx - 50, hy + 16), col=ink, width=3, a=a)
    c.ellipse((hx + 50, hy - 16, hx + 66, hy + 16), col=ink, width=3, a=a)
    # phantom source drifting left -> right
    k = ease(clamp((t - 0.6) / max(1.0, (beat["end"] - beat["start"]) - 1.4)))
    sx = lerp(L[0] + 40, R[0] - 40, k)
    sy = H * 0.40
    c.glow(sx, sy, 10, OCHRE, seg(t, 0.4, 0.4))
    for r in range(3):
        ph = (t * 0.9 + r / 3) % 1
        c.arc((sx - 30 - ph * 90, sy - 30 - ph * 90, sx + 30 + ph * 90, sy + 30 + ph * 90), 40, 140, OCHRE, 2,
              (1 - ph) * 0.8 * seg(t, 0.4, 0.4))
    c.dashed((L[0] + 40, sy), (R[0] - 40, sy), pal["grey"], 1.5, 8, 10, a * 0.5)
    schematic_tag(c, pal, "two channels · schematic", a)


@diagram
def cutaway(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    W, H = c.w, c.h
    cx, cy = W * 0.40, H * 0.47
    a = seg(t, 0.0, 0.5)
    x_move = 9 * math.sin(t * 2 * math.pi * 1.3) * seg(t, 1.6, 0.6)
    # magnet block (back) + pole piece
    c.rect((cx - 250, cy - 110, cx - 150, cy + 110), col=ink, width=3, a=a)
    for k in range(10):
        y = cy - 100 + k * 21
        c.line([(cx - 245, y + 8), (cx - 230, y - 8)], pal["grey"], 1.2, a * 0.6)
    c.rect((cx - 150, cy - 30, cx - 70, cy + 30), col=ink, width=3, a=a)
    c.line([(cx - 150, cy - 110), (cx - 80, cy - 110), (cx - 80, cy - 46)], ink, 3, a)
    c.line([(cx - 150, cy + 110), (cx - 80, cy + 110), (cx - 80, cy + 46)], ink, 3, a)
    # voice coil (highlighted) on the pole
    cxv = cx - 62 + x_move
    ca = seg(t, 0.5, 0.5)
    c.rect((cxv - 40, cy - 44, cxv + 8, cy - 32), fill=OCHRE, a=ca)
    c.rect((cxv - 40, cy + 32, cxv + 8, cy + 44), fill=OCHRE, a=ca)
    # cone: from coil former out to the rim
    rim_x = cx + 230 + x_move
    c.line([(cxv + 8, cy - 38), (rim_x, cy - 250)], ink, 3, a)
    c.line([(cxv + 8, cy + 38), (rim_x, cy + 250)], ink, 3, a)
    # dust cap
    c.arc((cxv - 10, cy - 46, cxv + 50, cy + 46), 270, 90, ink, 3, a)
    # surround (half rolls) and basket
    c.arc((rim_x - 18, cy - 272, rim_x + 18, cy - 236), 270, 90, ink, 3, a)
    c.arc((rim_x - 18, cy + 236, rim_x + 18, cy + 272), 270, 90, ink, 3, a)
    c.line([(cx - 80, cy - 110), (cx + 248, cy - 280)], pal["grey"], 2, a * 0.8)
    c.line([(cx - 80, cy + 110), (cx + 248, cy + 280)], pal["grey"], 2, a * 0.8)
    # spider
    for k in range(3):
        c.line([(cxv + 10, cy - 60 - k * 8), (cx + 40, cy - 110 - k * 8)], pal["grey"], 1.5, a * 0.7)
        c.line([(cxv + 10, cy + 60 + k * 8), (cx + 40, cy + 110 + k * 8)], pal["grey"], 1.5, a * 0.7)
    # pressure arcs
    pa = seg(t, 1.6, 0.6)
    for r in range(4):
        ph = (t * 1.3 + r / 4) % 1
        rr = 60 + ph * 240
        c.arc((rim_x + 30 - rr, cy - rr, rim_x + 30 + rr, cy + rr), -40, 40, OCHRE, 2.5, pa * (1 - ph))
    # labels with leaders
    la = seg(t, 0.9, 0.6)
    lab = [("magnet", (cx - 200, cy + 118), (cx - 230, cy + 300)),
           ("coil", (cxv - 16, cy + 44), (cx - 40, cy + 330)),
           ("cone", (cx + 120, cy + 170), (cx + 150, cy + 330)),
           ("air", (rim_x + 180, cy), (rim_x + 150, cy - 300))]
    for s, p0, p1 in lab:
        c.line([p0, p1], pal["grey"], 1.5, la * 0.8)
        c.text(p1[0], p1[1] + (6 if p1[1] > cy else -30), s, size=24, col=OCHRE if s == "coil" else ink, a=la,
               anchor="ma")
    schematic_tag(c, pal, "moving-coil speaker · schematic, not to scale", a)


DIAGRAMS = {"icons": icons, "siemens": siemens, "stereo": stereo, "cutaway": cutaway}
