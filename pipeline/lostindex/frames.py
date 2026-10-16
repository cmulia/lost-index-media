"""Frame composer for @lost_index videos.

A timeline is a list of beats (from script.json + timing.json). render_frame(tl, t)
returns the RGB frame at time t. Everything is drawn with PIL so the pipeline runs
anywhere with Python + ffmpeg.
"""
import math
import os
import random
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

from . import style as S

XFADE = 0.24          # crossfade between beats (s)
EL_FADE = 0.32        # element fade-in (s)
BIG_FADE = 0.38
KB_ZOOM = 0.075       # Ken Burns zoom over one asset run


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


# ---------------------------------------------------------------- backgrounds

@lru_cache(maxsize=None)
def background(dark):
    pal = S.DARK if dark else S.LIGHT
    rng = np.random.default_rng(7 if dark else 3)
    base = np.zeros((S.H, S.W, 3), np.float32) + np.array(pal["bg"], np.float32)
    # soft paper mottling + vignette
    low = rng.normal(0, 1, (S.H // 240 + 2, S.W // 240 + 2)).astype(np.float32)
    low = np.array(Image.fromarray(low).resize((S.W, S.H), Image.BICUBIC))
    yy, xx = np.mgrid[0:S.H, 0:S.W].astype(np.float32)
    vig = ((xx - S.W / 2) / (S.W * 0.75)) ** 2 + ((yy - S.H / 2) / (S.H * 0.75)) ** 2
    amt = 1.0 if dark else 1.4
    base += (low * amt)[..., None]
    base -= (vig * (10 if dark else 9))[..., None]
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), "RGB")


@lru_cache(maxsize=None)
def grain_tile(i):
    rng = np.random.default_rng(100 + i)
    g = rng.normal(0, 1, (S.H // 2, S.W // 2)).astype(np.float32)
    g = np.array(Image.fromarray(g).resize((S.W, S.H), Image.BILINEAR))
    return g


def add_grain(img, t, amount):
    if amount <= 0:
        return img
    a = np.asarray(img).astype(np.float32)
    a += grain_tile(int(t * 12) % 6)[..., None] * amount
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB")


# ---------------------------------------------------------------- assets

@lru_cache(maxsize=64)
def load_asset(path, grade="archival"):
    im = Image.open(path)
    if im.mode in ("P", "LA", "L", "RGBA", "I;16", "I", "F", "CMYK"):
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA")
            bg = Image.new("RGBA", im.size, (240, 236, 228, 255))
            bg.alpha_composite(im)
            im = bg
        im = im.convert("RGB")
    im = im.convert("RGB")
    if max(im.size) > 2400:
        im.thumbnail((2400, 2400), Image.LANCZOS)
    if grade == "archival":
        im = ImageEnhance.Color(im).enhance(0.84)
        im = ImageEnhance.Contrast(im).enhance(0.96)
        a = np.asarray(im).astype(np.float32)
        a = a * np.array([1.025, 1.0, 0.95], np.float32) + np.array([4, 3, 1], np.float32)
        im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return im


def kenburns(src, box_w, box_h, p, focus=(0.5, 0.5), zoom0=1.0, zoom1=1.0 + KB_ZOOM):
    """Cover-crop src to box aspect, zoomed by lerp(zoom0, zoom1, p) around focus."""
    sw, sh = src.size
    ar = box_w / box_h
    if sw / sh > ar:
        ch = sh
        cw = sh * ar
    else:
        cw = sw
        ch = sw / ar
    z = zoom0 + (zoom1 - zoom0) * p
    cw /= z
    ch /= z
    fx = focus[0] * sw
    fy = focus[1] * sh
    x0 = min(max(fx - cw / 2, 0), sw - cw)
    y0 = min(max(fy - ch / 2, 0), sh - ch)
    return src.resize((box_w, box_h), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))


@lru_cache(maxsize=32)
def shadow(w, h, dark):
    pad = 40
    sh = Image.new("L", (w + 2 * pad, h + 2 * pad), 0)
    d = ImageDraw.Draw(sh)
    d.rectangle([pad, pad + 10, pad + w, pad + h + 10], fill=70 if not dark else 140)
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    return sh, pad


# ---------------------------------------------------------------- text helpers

def wrap(text, fnt, width):
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if fnt.getlength(trial) <= width or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def fit_big(text, width, max_lines=2, size=S.BIG_SIZE):
    while size > 70:
        f = S.font("serif_i", size)
        lines = wrap(text, f, width)
        if len(lines) <= max_lines and all(f.getlength(l) <= width for l in lines):
            return f, lines
        size -= 8
    f = S.font("serif_i", size)
    return f, wrap(text, f, width)


def rgba(c, a):
    return (c[0], c[1], c[2], int(255 * max(0.0, min(1.0, a))))


def draw_header(d, pal, label, alpha=1.0):
    f = S.font("mono", S.HEADER_SIZE)
    fm = S.font("mono_med", S.HEADER_SIZE)
    d.text((S.MARGIN, S.HEADER_Y), label, font=f, fill=rgba(pal["ink"], alpha))
    handle = "@lost_index"
    hw = fm.getlength(handle)
    x = S.W - S.MARGIN - hw
    d.text((x, S.HEADER_Y), handle, font=fm, fill=rgba(pal["ink"], alpha))
    # little waveform mark before the handle
    wx0, wy = x - 50, S.HEADER_Y + 20
    pts = [(wx0 + i * 1.0, wy - 6 * math.sin(i / 34 * 4 * math.pi) * (0.55 + 0.45 * math.sin(i / 34 * math.pi)))
           for i in range(0, 35)]
    d.line(pts, fill=rgba(pal["ink"], alpha), width=3, joint="curve")
    d.line([(S.MARGIN, S.RULE_Y), (S.W - S.MARGIN, S.RULE_Y)], fill=rgba(pal["rule"], alpha), width=2)


def draw_tag(d, x, y, label, sublabel, pal, alpha):
    if not label:
        return y
    f = S.font("mono", S.TAG_SIZE)
    fs = S.font("mono", S.SUBLABEL_SIZE)
    tw = f.getlength(label)
    pad_x, pad_y = 14, 8
    h = S.TAG_SIZE + 2 * pad_y + 4
    d.rectangle([x, y, x + tw + 2 * pad_x, y + h], outline=rgba(pal["tag"], alpha), width=2)
    d.text((x + pad_x, y + pad_y - 2), label, font=f, fill=rgba(pal["ink"], alpha))
    if sublabel:
        d.text((x + tw + 2 * pad_x + 18, y + pad_y), sublabel, font=fs, fill=rgba(pal["grey"], alpha))
    return y + h


def draw_date(d, x, y, date_label, date, pal, alpha):
    if not date:
        return y
    f = S.font("mono", S.DATE_LABEL_SIZE)
    fd = S.font("serif_i", S.DATE_SIZE)
    cx = x
    if date_label:
        d.text((x, y + 20), date_label, font=f, fill=rgba(pal["grey"], alpha))
        cx = x + f.getlength(date_label) + 22
    d.text((cx, y), S.serif_safe(date), font=fd, fill=rgba(pal["ink"], alpha))
    return y + S.DATE_SIZE + 6


def draw_caption(d, x, y, width, text, nchars, pal, alpha, size=S.CAPTION_SIZE):
    if not text:
        return y
    f = S.font("mono", size)
    lines = wrap(text, f, width)
    lh = int(size * S.CAPTION_LEADING)
    left = nchars
    for line in lines:
        if left <= 0:
            break
        part = line[:left]
        d.text((x, y), part, font=f, fill=rgba(pal["ink"], alpha))
        left -= len(line) + 1
        y += lh
    return y + lh * 0


def caption_height(text, width, size=S.CAPTION_SIZE):
    if not text:
        return 0
    f = S.font("mono", size)
    return len(wrap(text, f, width)) * int(size * S.CAPTION_LEADING)


def draw_big(d, x, y, width, text, pal, alpha, rise=0.0, align="left", max_lines=2, size=S.BIG_SIZE):
    if not text:
        return y
    text = S.serif_safe(text)
    f, lines = fit_big(text, width, max_lines=max_lines, size=size)
    lh = int(f.size * 1.0)
    yy = y + rise
    for line in lines:
        lx = x if align == "left" else (x + width - f.getlength(line) if align == "right" else x + (width - f.getlength(line)) / 2)
        d.text((lx, yy), line, font=f, fill=rgba(pal["ink"], alpha))
        yy += lh
    return y + lh * len(lines) + 10


# ---------------------------------------------------------------- beat layout

def plate_box(beat, asset_img):
    """Decide where the photo/diagram sits for this beat."""
    vis = beat["visual"]
    if vis.get("type") == "diagram":
        h = vis.get("height", 760)
        return ("wide", (S.MARGIN, S.CONTENT_TOP, S.W - S.MARGIN, S.CONTENT_TOP + h))
    w, h = asset_img.size
    ar = w / h
    layout = vis.get("layout")
    if layout is None:
        if beat.get("dark") and vis.get("fullbleed", ar < 0.9):
            layout = "fullbleed"
        elif ar < 0.95:
            layout = "portrait"
        else:
            layout = "wide"
    if layout == "fullbleed":
        return ("fullbleed", (0, 0, S.W, S.H))
    if layout == "portrait":
        bw = vis.get("width", 470)
        bh = int(min(bw / ar, vis.get("max_height", 640)))
        return ("portrait", (S.MARGIN, S.CONTENT_TOP, S.MARGIN + bw, S.CONTENT_TOP + bh))
    bw = S.CONTENT_W
    bh = int(max(min(bw / ar, vis.get("max_height", 720)), 440))
    return ("wide", (S.MARGIN, S.CONTENT_TOP, S.W - S.MARGIN, S.CONTENT_TOP + bh))


class Timeline:
    def __init__(self, script, timing, ep_dir, diagrams=None):
        self.script = script
        self.ep_dir = ep_dir
        self.diagrams = diagrams or {}
        self.label = script.get("series_label") or f"file no. {script['file_no']}"
        self.beats = []
        for i, (b, tm) in enumerate(zip(script["beats"], timing["beats"])):
            bb = dict(b)
            bb.update(tm)
            bb["i"] = i
            self.beats.append(bb)
        self.end_card_start = timing["end_card_start"]
        self.duration = timing["duration"]
        # asset runs for continuous Ken Burns
        run_start = {}
        prev = None
        for b in self.beats:
            key = self._asset_key(b)
            if key and key == prev:
                b["run_start"] = run_start[key]
            else:
                b["run_start"] = b["start"]
                run_start[key] = b["start"]
            prev = key
        for j, b in enumerate(self.beats):
            key = self._asset_key(b)
            k = j
            while k + 1 < len(self.beats) and self._asset_key(self.beats[k + 1]) == key and key:
                k += 1
            b["run_end"] = self.beats[k]["end"]

    def _asset_key(self, b):
        v = b.get("visual") or {}
        if v.get("type") == "photo":
            return "photo:%s:%s:%s:%s:%s" % (v["asset"], bool(b.get("dark")), v.get("focus"), v.get("zoom_from"),
                                              v.get("layout"))
        if v.get("type") == "diagram":
            return "diagram:" + v.get("name", str(b["i"]))
        return None

    def asset_path(self, key):
        d = os.path.join(self.ep_dir, "assets")
        for ext in (".jpg", ".jpeg", ".png", ".tif", ".webp"):
            p = os.path.join(d, key + ext)
            if os.path.exists(p):
                return p
        raise FileNotFoundError(f"asset {key} not found in {d}")

    def beat_at(self, t):
        for b in self.beats:
            if t < b["end"]:
                return b
        return self.beats[-1]


def render_beat(tl, b, t, img=None):
    """Render beat b at absolute time t (t may run slightly past b['end'] for crossfades)."""
    dark = bool(b.get("dark"))
    pal = S.DARK if dark else S.LIGHT
    lt = t - b["start"]
    vis = b.get("visual") or {"type": "type_only"}
    frame = background(dark).copy().convert("RGBA")
    ov = Image.new("RGBA", (S.W, S.H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    a_el = ease(lt / EL_FADE)
    run_p = (t - b["run_start"]) / max(0.5, (b["run_end"] - b["run_start"]))
    run_p = max(0.0, min(1.0, run_p))
    same_as_prev = b["run_start"] < b["start"] - 1e-6
    a_plate = 1.0 if same_as_prev else ease(lt / EL_FADE)

    text_x, text_w = S.MARGIN, S.CONTENT_W
    y = S.CONTENT_TOP
    layout = "type"

    if vis["type"] == "photo":
        src = load_asset(tl.asset_path(vis["asset"]), vis.get("grade", "archival"))
        layout, box = plate_box(b, src)
        bw, bh = box[2] - box[0], box[3] - box[1]
        z0 = vis.get("zoom_from", 1.0)
        z1 = vis.get("zoom_to", 1.0 + KB_ZOOM)
        crop = kenburns(src, bw, bh, ease(run_p) * 0.6 + run_p * 0.4, tuple(vis.get("focus", (0.5, 0.5))), z0, z1)
        if layout == "fullbleed":
            arr = np.asarray(crop).astype(np.float32)
            yy = np.linspace(0, 1, S.H, dtype=np.float32)[:, None, None]
            shade = 0.52 + 0.30 * (1 - np.clip(np.abs(yy - 0.55) / 0.55, 0, 1))
            arr *= shade * vis.get("brightness", 1.0)
            crop = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
            frame.alpha_composite(Image.blend(background(True), crop, a_plate).convert("RGBA"))
        else:
            sh, pad = shadow(bw, bh, dark)
            sha = sh.point(lambda v: int(v * a_plate))
            frame.paste((0, 0, 0, 255), (box[0] - pad, box[1] - pad), sha)
            pl = crop.convert("RGBA")
            if a_plate < 1:
                pl.putalpha(int(255 * a_plate))
            frame.alpha_composite(pl, (box[0], box[1]))
    elif vis["type"] == "diagram":
        layout, box = plate_box(b, None)
        fn = tl.diagrams.get(vis.get("name"))
        panel_dark = vis.get("panel", "dark") == "dark"
        ppal = dict(S.DARK if panel_dark else S.LIGHT)
        if panel_dark:
            sh, pad = shadow(box[2] - box[0], box[3] - box[1], dark)
            frame.paste((0, 0, 0, 255), (box[0] - pad, box[1] - pad), sh.point(lambda v: int(v * a_plate)))
        pimg = Image.new("RGBA", (box[2] - box[0], box[3] - box[1]), rgba(ppal["panel"] if panel_dark else ppal["bg"], 1.0))
        if fn:
            fn(pimg, ImageDraw.Draw(pimg), run_p, t - b["run_start"], ppal, b)
        if a_plate < 1:
            pimg.putalpha(pimg.getchannel("A").point(lambda v: int(v * a_plate)))
        frame.alpha_composite(pimg, (box[0], box[1]))

    # text blocks
    caption = b.get("caption") or ""
    spoken = max(0.6, b.get("speech_end", b["end"]) - b["start"] - 0.05)
    nchars = int(len(caption) * min(1.0, max(0.0, (lt - 0.08) / spoken)))
    big = b.get("big")
    big_t = b.get("big_time", b["start"]) - b["start"]
    a_big = ease((lt - big_t) / BIG_FADE)
    rise = (1 - ease_out((lt - big_t) / 0.6)) * 16

    if layout == "fullbleed":
        dpal = S.DARK
        cy = S.CONTENT_TOP
        draw_caption(d, S.MARGIN, cy, 640, caption, nchars, dpal, 1.0)
        if big:
            draw_big(d, S.MARGIN, 1180, S.CONTENT_W, big, dpal, a_big, rise, align=vis.get("big_align", "center"))
        draw_tag(d, S.MARGIN, 1600, b.get("label"), b.get("sublabel"), dpal, a_el)
        draw_date(d, S.MARGIN, 1660, b.get("date_label"), b.get("date"), dpal, a_el)
    elif layout == "portrait":
        bx = box
        cx = bx[2] + 34
        cw = S.W - S.MARGIN - cx
        draw_caption(d, cx, bx[1] + 6, cw, caption, nchars, pal, 1.0, size=34)
        y = bx[3] + 30
        y = draw_tag(d, S.MARGIN, y, b.get("label"), b.get("sublabel"), pal, a_el) + 26
        y = draw_date(d, S.MARGIN, y, b.get("date_label"), b.get("date"), pal, a_el) + 30
        if big:
            draw_big(d, S.MARGIN, y + 10, S.CONTENT_W, big, pal, a_big, rise)
    elif layout == "wide":
        y = box[3] + 30
        y = draw_tag(d, S.MARGIN, y, b.get("label"), b.get("sublabel"), pal, a_el) + 26
        y = draw_date(d, S.MARGIN, y, b.get("date_label"), b.get("date"), pal, a_el) + 34
        if big:
            y = draw_big(d, S.MARGIN, y, S.CONTENT_W, big, pal, a_big, rise) + 24
        else:
            y += 40
        draw_caption(d, S.MARGIN, y, S.CONTENT_W, caption, nchars, pal, 1.0)
    else:  # type only
        y = S.CONTENT_TOP + 40
        if big:
            f, lines = fit_big(big, S.CONTENT_W, max_lines=3, size=b.get("big_size", 190))
            y = draw_big(d, S.MARGIN, y, S.CONTENT_W, big, pal, a_big, rise, max_lines=3, size=b.get("big_size", 190)) + 50
        draw_caption(d, S.MARGIN, y, S.CONTENT_W, caption, nchars, pal, 1.0)
        tail = y + caption_height(caption, S.CONTENT_W) + 40
        tail = draw_tag(d, S.MARGIN, max(tail, 1500), b.get("label"), b.get("sublabel"), pal, a_el) + 26
        draw_date(d, S.MARGIN, tail, b.get("date_label"), b.get("date"), pal, a_el)

    draw_header(d, S.DARK if layout == "fullbleed" else pal, tl.label)
    frame.alpha_composite(ov)
    return frame.convert("RGB")


def render_end_card(tl, t):
    lt = t - tl.end_card_start
    frame = background(True).copy().convert("RGBA")
    ov = Image.new("RGBA", (S.W, S.H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    pal = S.DARK
    a = ease(lt / 0.6)
    f = S.font("serif_i", 150)
    txt = f"file no. {tl.script['file_no']}"
    tw = f.getlength(txt)
    x = (S.W - tw) / 2
    d.text((x, 820 + (1 - ease_out(lt / 0.9)) * 18), txt, font=f, fill=rgba(pal["ink"], a))
    fm = S.font("mono", 34)
    h = "@lost_index"
    d.text((x + tw - fm.getlength(h) - 6, 990), h, font=fm, fill=rgba(pal["grey"], ease((lt - 0.4) / 0.6)))
    draw_header(d, pal, tl.label, 1.0)
    frame.alpha_composite(ov)
    return frame.convert("RGB")


def render_frame(tl, t):
    if t >= tl.end_card_start:
        img = render_end_card(tl, t)
        dt = t - tl.end_card_start
        if dt < XFADE * 1.6:
            prev = render_beat(tl, tl.beats[-1], t)
            img = Image.blend(prev, img, ease(dt / (XFADE * 1.6)))
        return add_grain(img, t, 3.0)
    b = tl.beat_at(t)
    img = render_beat(tl, b, t)
    dt = t - b["start"]
    if b["i"] > 0 and dt < XFADE:
        prev = render_beat(tl, tl.beats[b["i"] - 1], t)
        img = Image.blend(prev, img, ease(dt / XFADE))
    return add_grain(img, t, 3.0 if b.get("dark") else 2.4)
