"""Original diagrams for file no. 020 (the first SMS, 1992)."""
from lostindex.diag import diagram, seg, ease, ease_out, lerp, clamp, schematic_tag

AMBER = (226, 170, 84)
RED = (214, 96, 72)
GREEN = (120, 196, 140)


def node(c, cx, cy, w, h, l1, l2, col, a, pal):
    c.rect((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), col=col, width=3, a=a, radius=10)
    c.text(cx, cy - 14, l1, size=28, col=pal["panel_ink"], a=a, anchor="ma")
    if l2:
        c.text(cx, cy + 20, l2, size=22, col=pal["grey"], a=a, anchor="ma")


@diagram
def route(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    a = seg(t, 0, 0.4)
    c.text(90, 70, "the path of one message", size=35, col=ink, a=a)
    ys = 300
    xs = [c.w * f for f in (0.14, 0.38, 0.62, 0.86)]
    labs = [("test pc", "sema group"), ("sms centre", "vodafone"), ("radio mast", "gsm"), ("handset", "orbitel 901")]
    for i, (x, (l1, l2)) in enumerate(zip(xs, labs)):
        k = seg(t, 0.3 + i * 0.7, 0.4)
        node(c, x, ys, 190, 130, l1, l2, AMBER if i in (0, 3) else ink, k, pal)
        if i:
            m = seg(t, 0.3 + i * 0.7 - 0.35, 0.5)
            c.arrow((xs[i - 1] + 98, ys), (x - 98, ys), AMBER, 3, a=m)
    # packet travelling
    k = clamp((t - 0.6) / 3.0)
    px = lerp(xs[0], xs[3], ease(k))
    c.rect((px - 12, ys + 100, px + 12, ys + 124), fill=AMBER, a=a * (1 if k < 1 else 0.0))
    c.text(px, ys + 134, "merry christmas", size=24, col=AMBER, a=a * (1 if k < 1 else 0.0), anchor="ma")
    c.text(90, 560, "one-way: computer to handset", size=27, col=pal["grey"], a=seg(t, 3.0, 0.6))
    schematic_tag(c, pal, "schematic · drawn for this video", a)


@diagram
def composer(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    a = seg(t, 0, 0.4)
    c.text(90, 70, "typed on an office pc", size=35, col=ink, a=a)
    c.rect((90, 150, c.w - 90, 520), col=ink, width=3, a=a, radius=8)
    c.text(120, 180, "to:   orbitel 901", size=26, col=pal["grey"], a=a)
    c.text(120, 222, "sent: 3 dec 1992", size=26, col=pal["grey"], a=a)
    c.line([(120, 272), (c.w - 120, 272)], ink, 1, a * 0.5)
    msg = "merry christmas"
    n = int(len(msg) * clamp((t - 0.6) / 2.2))
    shown = msg[:n]
    c.text(120, 320, shown, size=52, col=AMBER, a=a)
    cur = c.text_w(shown, size=52)
    blink = 1.0 if int(t * 2) % 2 == 0 else 0.2
    c.rect((120 + cur + 4, 322, 120 + cur + 28, 376), fill=AMBER, a=a * blink)
    c.text(90, 590, "15 characters. two words.", size=27, col=pal["grey"], a=seg(t, 3.0, 0.6))
    schematic_tag(c, pal, "illustration · drawn for this video", a)


@diagram
def oneway(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    a = seg(t, 0, 0.4)
    c.text(90, 70, "one-way street", size=35, col=ink, a=a)
    xa, xb, y = c.w * 0.2, c.w * 0.8, 280
    node(c, xa, y, 230, 130, "pc", "can send", AMBER, a, pal)
    node(c, xb, y, 230, 130, "handset", "can only receive", ink, a, pal)
    k = seg(t, 0.5, 0.9)
    c.arrow((xa + 120, y - 30), (lerp(xa + 120, xb - 120, ease(k)), y - 30), AMBER, 4, a=a)
    b = seg(t, 1.8, 0.8)
    c.dashed((xb - 120, y + 40), (xa + 120, y + 40), RED, 3, a=b, frac=ease(b))
    m = seg(t, 2.6, 0.4)
    mx = c.w / 2
    c.line([(mx - 26, y + 14), (mx + 26, y + 66)], RED, 6, m)
    c.line([(mx - 26, y + 66), (mx + 26, y + 14)], RED, 6, m)
    c.text(mx, 430, "no way to text back", size=32, col=RED, a=seg(t, 2.8, 0.5), anchor="ma")
    schematic_tag(c, pal, "schematic · drawn for this video", a)


@diagram
def nft(c, p, t, pal, beat):
    ink = pal["panel_ink"]
    a = seg(t, 0, 0.4)
    c.text(90, 70, "from message to auction", size=35, col=ink, a=a)
    y = 280
    xs = [c.w * f for f in (0.16, 0.5, 0.84)]
    labs = [("replica", "of the message"), ("nft", "paris auction"), ("unhcr", "un refugee agency")]
    for i, (x, (l1, l2)) in enumerate(zip(xs, labs)):
        k = seg(t, 0.3 + i * 0.9, 0.4)
        node(c, x, y, 230, 130, l1, l2, GREEN if i == 2 else (AMBER if i == 1 else ink), k, pal)
        if i:
            m = seg(t, 0.3 + i * 0.9 - 0.4, 0.5)
            c.arrow((xs[i - 1] + 120, y), (x - 120, y), ink, 3, a=m)
    s = seg(t, 1.6, 0.6)
    c.text(c.w / 2, 150, "about 100,000 euros", size=30, col=AMBER, a=s, anchor="ma")
    c.text(90, 500, "the replica was sold, not the original", size=27, col=pal["grey"], a=seg(t, 3.0, 0.6))
    schematic_tag(c, pal, "schematic · drawn for this video", a)


DIAGRAMS = {"route": route, "composer": composer, "oneway": oneway, "nft": nft}
