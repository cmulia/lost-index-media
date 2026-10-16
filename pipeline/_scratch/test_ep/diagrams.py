import math
def demo(img, d, p, t, pal, beat):
    w, h = img.size
    cx, cy = w/2, h/2
    for k in range(1, 6):
        r = 60*k*(0.6+0.4*p)
        d.ellipse([cx-r*1.6, cy-r, cx+r*1.6, cy+r], outline=pal["panel_ink"], width=2)
    d.ellipse([cx-18, cy-18, cx+18, cy+18], fill=pal["panel_ink"])
DIAGRAMS = {"demo": demo}
