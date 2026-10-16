"""Original diagrams for file no. 009 (the first actual bug)."""
import math

from lostindex.diag import diagram, seg, ease, lerp, clamp, schematic_tag

RED = (176, 52, 40)
OCHRE = (214, 158, 74)


def moth(c, cx, cy, s, col, a, flap=0.0):
    wing = 1 - 0.35 * flap
    c.polygon([(cx, cy), (cx - 60 * s * wing, cy - 34 * s), (cx - 70 * s * wing, cy + 6 * s), (cx - 30 * s, cy + 26 * s)],
              fill=col, a=a)
    c.polygon([(cx, cy), (cx + 60 * s * wing, cy - 34 * s), (cx + 70 * s * wing, cy + 6 * s), (cx + 30 * s, cy + 26 * s)],
              fill=col, a=a)
    c.ellipse((cx - 8 * s, cy - 24 * s, cx + 8 * s, cy + 34 * s), fill=col, a=a)
    c.line([(cx - 3 * s, cy - 22 * s), (cx - 20 * s, cy - 50 * s)], col, 2, a)
    c.line([(cx + 3 * s, cy - 22 * s), (cx + 20 * s, cy - 50 * s)], col, 2, a)


@diagram
def relay(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    W, H = c.w, c.h
    a = seg(t, 0, 0.5)
    # coil
    cx, cy = W * 0.36, H * 0.62
    c.rect((cx - 130, cy - 70, cx + 130, cy + 70), col=ink, width=3, a=a, radius=10)
    for k in range(12):
        x = cx - 112 + k * 20
        c.line([(x, cy - 70), (x + 10, cy + 70)], pal["grey"], 1.5, a * 0.7)
    c.text(cx, cy + 92, "coil", size=22, col=pal["grey"], a=a, anchor="ma")
    # hinged armature above the coil, pulled down towards it
    pivot = (cx - 190, cy - 120)
    c.line([(pivot[0], pivot[1]), (pivot[0], cy + 70)], pal["grey"], 3, a)
    blocked = seg(t, 1.4, 0.3)
    chatter = 0.5 + 0.5 * math.sin(t * 14)
    drop = lerp(lerp(0, 46, chatter), 18, blocked)          # tip drop in px
    L = 600
    tip = (pivot[0] + L, pivot[1] + drop)
    c.line([pivot, tip], ink, 7, a)
    c.circle(pivot[0], pivot[1], 11, fill=ink, a=a)
    c.text(pivot[0] + 60, pivot[1] - 50, "armature", size=22, col=pal["grey"], a=a)
    # contacts: one under the armature tip, one fixed below
    fixed_y = pivot[1] + 92
    c.rect((tip[0] - 16, tip[1] + 2, tip[0] + 16, tip[1] + 16), fill=OCHRE, a=a)
    c.rect((tip[0] - 16, fixed_y, tip[0] + 16, fixed_y + 14), fill=OCHRE, a=a)
    c.line([(tip[0], fixed_y + 14), (tip[0], fixed_y + 170)], ink, 4, a)
    c.text(tip[0] + 34, fixed_y + 120, "contacts", size=22, col=pal["grey"], a=a)
    # the moth, wedged in the gap
    ma = seg(t, 1.0, 0.4)
    moth(c, tip[0], (tip[1] + 16 + fixed_y) / 2 + 4, 0.55, (206, 192, 166), ma,
         flap=(0.5 + 0.5 * math.sin(t * 24)) * (1 - blocked))
    c.text(W - 50, 50, "relay #70 · panel f", size=22, col=ink, a=seg(t, 1.8, 0.5), anchor="ra")
    schematic_tag(c, pal, "schematic · not the mark ii's actual relay", a)


@diagram
def museum_card(c, p, t, pal, beat):
    W, H = c.w, c.h
    a = seg(t, 0, 0.5)
    box = (W * 0.08, H * 0.22, W * 0.92, H * 0.70)
    c.rect((box[0] + 8, box[1] + 10, box[2] + 8, box[3] + 10), fill=(0, 0, 0), a=a * 0.12)
    c.rect(box, fill=(244, 240, 230), col=(170, 164, 150), width=1.5, a=a)
    ink = (40, 38, 34)
    c.text(box[0] + 40, box[1] + 50, 'first computer "bug"', size=34, col=ink, a=a, face="mono_med")
    c.text(box[0] + 40, box[1] + 120, "9 september", size=34, col=ink, a=a)
    x = box[0] + 40 + c.text_w("9 september ", 34)
    c.text(x, box[1] + 120, "1945", size=34, col=ink, a=a)
    s = seg(t, 1.0, 0.5)
    w45 = c.text_w("1945", 34)
    c.partial_line([(x - 4, box[1] + 142), (x + w45 + 4, box[1] + 142)], RED, 4, s)
    c.text(x + w45 + 24, box[1] + 120, "1947", size=34, col=RED, a=seg(t, 1.6, 0.3), face="mono_med")
    c.text(box[0] + 40, box[1] + 200, "harvard mark ii · relay #70", size=24, col=(110, 106, 98), a=a)
    c.text(box[2] - 24, box[3] - 40, "reconstruction · not the original card", size=18, col=(130, 126, 118), a=a,
           anchor="ra")
    schematic_tag(c, pal, "illustration · drawn for this video", a)


DIAGRAMS = {"relay": relay, "museum_card": museum_card}
