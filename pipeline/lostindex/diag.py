"""Helpers for drawing animated diagrams in the @lost_index style.

Episode diagrams.py files define functions fn(img, draw, p, t, pal, beat) and register
them in DIAGRAMS. Wrap them with @diagram to get a 2x supersampled Canvas:

    @diagram
    def cutaway(c, p, t, pal, beat):
        c.line([(100, 100), (400, 100)], pal["panel_ink"], 2)
"""
import math

from PIL import Image, ImageDraw

from . import style as S

SS = 2


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def seg(t, start, dur):
    """0..1 progress of a sub-animation starting at time `start` lasting `dur` seconds."""
    return ease((t - start) / dur) if dur > 0 else float(t >= start)


def lerp(a, b, x):
    return a + (b - a) * x


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.im = Image.new("RGBA", (w * SS, h * SS), bg)
        self.d = ImageDraw.Draw(self.im)

    def _c(self, col, a=1.0):
        if len(col) == 4:
            return col
        return (col[0], col[1], col[2], int(255 * clamp(a)))

    def _p(self, pts):
        return [(x * SS, y * SS) for x, y in pts]

    def line(self, pts, col, width=2, a=1.0):
        if a <= 0:
            return
        self.d.line(self._p(pts), fill=self._c(col, a), width=max(1, int(width * SS)), joint="curve")

    def partial_line(self, pts, col, width, frac, a=1.0):
        """Draw a polyline up to `frac` of its length (for draw-on animations)."""
        if frac <= 0:
            return
        lens = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        total = sum(lens) * clamp(frac)
        out = [pts[0]]
        for i, L in enumerate(lens):
            if total >= L:
                out.append(pts[i + 1])
                total -= L
            else:
                f = total / L if L else 0
                out.append((lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)))
                break
        if len(out) > 1:
            self.line(out, col, width, a)

    def dashed(self, p0, p1, col, width=2, dash=10, gap=8, a=1.0, frac=1.0):
        L = math.dist(p0, p1) * clamp(frac)
        if L <= 0:
            return
        ux, uy = (p1[0] - p0[0]) / math.dist(p0, p1), (p1[1] - p0[1]) / math.dist(p0, p1)
        s = 0.0
        while s < L:
            e = min(L, s + dash)
            self.line([(p0[0] + ux * s, p0[1] + uy * s), (p0[0] + ux * e, p0[1] + uy * e)], col, width, a)
            s = e + gap

    def rect(self, box, col=None, fill=None, width=2, a=1.0, radius=0):
        b = [box[0] * SS, box[1] * SS, box[2] * SS, box[3] * SS]
        if radius:
            self.d.rounded_rectangle(b, radius * SS, fill=self._c(fill, a) if fill else None,
                                     outline=self._c(col, a) if col else None, width=int(width * SS))
        else:
            self.d.rectangle(b, fill=self._c(fill, a) if fill else None,
                             outline=self._c(col, a) if col else None, width=int(width * SS))

    def circle(self, cx, cy, r, col=None, fill=None, width=2, a=1.0):
        b = [(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS]
        self.d.ellipse(b, fill=self._c(fill, a) if fill else None, outline=self._c(col, a) if col else None,
                       width=int(width * SS))

    def ellipse(self, box, col=None, fill=None, width=2, a=1.0):
        b = [box[0] * SS, box[1] * SS, box[2] * SS, box[3] * SS]
        self.d.ellipse(b, fill=self._c(fill, a) if fill else None, outline=self._c(col, a) if col else None,
                       width=int(width * SS))

    def arc(self, box, start, end, col, width=2, a=1.0):
        b = [box[0] * SS, box[1] * SS, box[2] * SS, box[3] * SS]
        self.d.arc(b, start, end, fill=self._c(col, a), width=int(width * SS))

    def polygon(self, pts, fill=None, col=None, a=1.0, width=2):
        self.d.polygon(self._p(pts), fill=self._c(fill, a) if fill else None,
                       outline=self._c(col, a) if col else None, width=int(width * SS))

    def text(self, x, y, s, size=24, col=(0, 0, 0), a=1.0, face="mono", anchor="la"):
        if a <= 0 or not s:
            return
        if face.startswith("serif"):
            s = S.serif_safe(s)
        f = S.font(face, int(size * SS))
        self.d.text((x * SS, y * SS), s, font=f, fill=self._c(col, a), anchor=anchor)

    def text_w(self, s, size=24, face="mono"):
        return S.font(face, int(size * SS)).getlength(s) / SS

    def arrow(self, p0, p1, col, width=2, head=12, a=1.0, both=False):
        self.line([p0, p1], col, width, a)

        def hd(pa, pb):
            ang = math.atan2(pb[1] - pa[1], pb[0] - pa[0])
            l = (pb[0] - head * math.cos(ang - 0.45), pb[1] - head * math.sin(ang - 0.45))
            r = (pb[0] - head * math.cos(ang + 0.45), pb[1] - head * math.sin(ang + 0.45))
            self.line([l, pb, r], col, width, a)
        hd(p0, p1)
        if both:
            hd(p1, p0)

    def glow(self, cx, cy, r, col, a=1.0):
        for k in range(6, 0, -1):
            rr = r * (1 + k * 0.5)
            self.circle(cx, cy, rr, fill=col, a=a * 0.06 * (7 - k) / 6)
        self.circle(cx, cy, r, fill=col, a=a)

    def finish(self, img):
        small = self.im.resize((self.w, self.h), Image.LANCZOS)
        img.alpha_composite(small)


def diagram(fn):
    def wrapped(img, draw, p, t, pal, beat):
        w, h = img.size
        c = Canvas(w, h, (0, 0, 0, 0))
        fn(c, p, t, pal, beat)
        c.finish(img)
    wrapped.__name__ = fn.__name__
    return wrapped


def label(c, x, y, s, pal, a=1.0, size=22, col=None):
    c.text(x, y, s, size=size, col=col or pal["grey"], a=a)


def schematic_tag(c, pal, s="schematic · drawn for this video", a=1.0):
    c.text(c.w / 2, c.h - 34, s, size=18, col=pal["grey"], a=a * 0.85, anchor="ma")
