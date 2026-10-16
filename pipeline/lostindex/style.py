"""House style for @lost_index vertical videos (1080x1920, 30 fps).

Measurements were taken from the 004/005 renders: cream paper page, IBM Plex Mono
for the header, tags and typewriter captions, Instrument Serif Italic for headlines.
"""
import os
from functools import lru_cache

from PIL import ImageFont

W, H = 1080, 1920
FPS = 30
MARGIN = 72
CONTENT_W = W - 2 * MARGIN

HEADER_Y = 190          # top of header text
RULE_Y = 248
CONTENT_TOP = 300

LIGHT = {
    "bg": (232, 226, 213),
    "ink": (38, 36, 31),
    "grey": (119, 115, 106),
    "rule": (200, 193, 179),
    "tag": (92, 88, 80),
    "panel": (24, 23, 21),
    "panel_ink": (226, 220, 206),
}
DARK = {
    "bg": (19, 19, 18),
    "ink": (236, 230, 218),
    "grey": (141, 136, 126),
    "rule": (58, 56, 52),
    "tag": (170, 164, 152),
    "panel": (34, 33, 31),
    "panel_ink": (226, 220, 206),
}

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fonts")


@lru_cache(maxsize=None)
def font(name, size):
    files = {
        "mono": "IBMPlexMono-Regular.ttf",
        "mono_med": "IBMPlexMono-Medium.ttf",
        "mono_light": "IBMPlexMono-Light.ttf",
        "serif_i": "InstrumentSerif-Italic.ttf",
        "serif": "InstrumentSerif-Regular.ttf",
    }
    return ImageFont.truetype(os.path.join(FONT_DIR, files[name]), size)


HEADER_SIZE = 30
TAG_SIZE = 27
SUBLABEL_SIZE = 25
DATE_LABEL_SIZE = 27
DATE_SIZE = 58
CAPTION_SIZE = 37
CAPTION_LEADING = 1.42
BIG_SIZE = 168


SERIF_SUBS = {"ƒ": "f", "→": "–", "≈": "~", "½": "1/2"}


def serif_safe(s):
    """Instrument Serif lacks a few glyphs; swap in close equivalents."""
    for k, v in SERIF_SUBS.items():
        s = s.replace(k, v)
    return s
