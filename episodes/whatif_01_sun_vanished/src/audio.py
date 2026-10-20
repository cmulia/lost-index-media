"""Score + sound design for 'What if the Sun vanished?' — all synthesised from scratch."""
import sys, wave
import numpy as np
sys.path.insert(0, '/home/user/lost-index-media/pipeline/lostindex')
from music import SR, compose, fft_filter, reverb, place, bell_note, key_note

DUR = 55.0
N = int(DUR * SR)
rng = np.random.default_rng(7)
t_all = np.arange(N) / SR


def noise(n, lo=None, hi=None, ch=2):
    return fft_filter(rng.normal(0, 1, (n, ch)).astype(np.float32), lo=lo, hi=hi)


def env(n, pts):
    """piecewise-linear envelope from [(t, g), ...] in seconds (relative)."""
    tt = np.arange(n) / SR
    xs, ys = zip(*pts)
    return np.interp(tt, xs, ys).astype(np.float32)


def seg(a, b):
    return int(a * SR), int(b * SR)


def stereo(m):
    return np.stack([m, m], 1).astype(np.float32)


# ---------------- ambience ----------------
def beach_amb(dur, level=1.0, crowd=1.0):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    # surf: a swell every ~6 s, washing up and hissing out
    surf = noise(n, lo=120, hi=3500)
    period = 6.3
    ph = (tt % period) / period
    wash = np.where(ph < 0.18, (ph / 0.18) ** 1.5, np.exp(-(ph - 0.18) * 4.5))
    wash = 0.25 + 0.75 * wash
    roar = noise(n, hi=400) * 0.6
    sea = surf * (wash ** 1.3)[:, None] * 0.11 + roar * 0.05
    # crowd murmur: band-limited noise with syllable-rate modulation
    mur = noise(n, lo=280, hi=1800)
    mod = fft_filter(np.abs(rng.normal(0, 1, (n, 2))).astype(np.float32), hi=6)
    mur = mur * (0.4 + mod * 1.4) * 0.03 * crowd
    out = sea + mur
    # gulls
    for k in range(int(dur / 3.2)):
        t0 = rng.uniform(0, dur - 1.5)
        calls = rng.integers(1, 4)
        for c in range(calls):
            ln = rng.uniform(0.18, 0.32)
            m = int(ln * SR)
            s = np.arange(m) / SR
            f = 1900 + 900 * np.sin(np.pi * s / ln) - 700 * s / ln
            phs = 2 * np.pi * np.cumsum(f) / SR
            g = np.sin(phs) + 0.5 * np.sin(2 * phs) + 0.25 * np.sin(3 * phs)
            g *= np.sin(np.pi * s / ln) ** 2 * rng.uniform(0.006, 0.016)
            pan = rng.uniform(0.2, 0.8)
            sig = np.stack([g * (1 - pan), g * pan], 1).astype(np.float32)
            place(out, sig, t0 + c * (ln + 0.08))
    return out * level * 2.5


def night_amb(dur):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    surf = noise(n, lo=80, hi=1400)
    ph = (tt % 6.3) / 6.3
    wash = 0.3 + 0.7 * np.where(ph < 0.18, (ph / 0.18) ** 1.5, np.exp(-(ph - 0.18) * 4.5))
    return surf * wash[:, None] * 0.07


def wind_fire(dur):
    n = int(dur * SR)
    tt = np.arange(n) / SR
    out = np.zeros((n, 2), np.float32)
    # howling wind: sum of resonant bands drifting in pitch
    base = noise(n, lo=150, hi=2500)
    for cf, sp in ((420, 0.13), (690, 0.09), (980, 0.17)):
        f = cf * (1 + 0.35 * np.sin(2 * np.pi * sp * tt + rng.uniform(0, 6)))
        car = np.sin(2 * np.pi * np.cumsum(f) / SR)
        amp = fft_filter(np.abs(rng.normal(0, 1, n)).astype(np.float32), hi=1.5)
        out += stereo(car * amp * 0.035) * (1 + 0.2 * rng.normal(0, 1, (1, 2)).astype(np.float32))
    gust = 0.5 + 0.5 * np.sin(2 * np.pi * 0.11 * tt) ** 2
    out += base * gust[:, None] * 0.05
    # fire: low roar + crackles
    out += noise(n, lo=60, hi=500) * 0.03
    for k in range(int(dur * 14)):
        t0 = rng.uniform(0, dur)
        m = int(rng.uniform(0.002, 0.01) * SR)
        c = rng.normal(0, 1, m) * np.exp(-np.arange(m) / (m / 3)) * rng.uniform(0.03, 0.15)
        pan = rng.uniform(0.3, 0.7)
        place(out, np.stack([c * (1 - pan), c * pan], 1).astype(np.float32), t0)
    return out


# ---------------- one-shots ----------------
def whoosh(ln=1.4, up=True, level=0.5):
    n = int(ln * SR)
    s = np.arange(n) / SR
    x = rng.normal(0, 1, (n, 2)).astype(np.float32)
    out = np.zeros_like(x)
    # sweep a band through the noise (chunked filtering)
    ch = 2048
    for i in range(0, n, ch):
        k = i / n
        cf = (300 + 3500 * k ** 2) if up else (3800 - 3500 * k ** 0.5)
        out[i:i + ch] = fft_filter(x[i:i + ch], lo=cf * 0.5, hi=cf * 1.6)
    e = np.sin(np.pi * np.clip(s / ln, 0, 1)) ** 2
    return out * e[:, None] * level


def boom(ln=6.0, f0=55, f1=24, level=1.0, crack=0.4):
    n = int(ln * SR)
    s = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-s * 1.6)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-s * 0.9)
    sub *= np.minimum(1, s / 0.01)
    body = fft_filter(rng.normal(0, 1, n).astype(np.float32), hi=220) * np.exp(-s * 2.2) * 1.2
    hit = fft_filter(rng.normal(0, 1, n).astype(np.float32), lo=300, hi=5000) * np.exp(-s * 14) * crack
    m = (sub * 0.9 + body + hit).astype(np.float32)
    return reverb(stereo(m), 3.5, 0.3, 11) * level


def power_down(ln=2.2, level=0.35):
    n = int(ln * SR)
    s = np.arange(n) / SR
    f = 380 * np.exp(-s * 2.0) + 30
    ph = 2 * np.pi * np.cumsum(f) / SR
    m = (np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sign(np.sin(ph)) * 0.3) * np.exp(-s * 1.2)
    return stereo(m) * level


def reverse_suck(ln=1.0, level=0.5):
    w = whoosh(ln, True, 1.0)
    s = np.arange(w.shape[0]) / SR
    return w * (s / ln)[:, None] ** 2 * level


def clock_tick(level=0.5, hi=True):
    n = int(0.09 * SR)
    s = np.arange(n) / SR
    click = rng.normal(0, 1, n) * np.exp(-s * 900)
    tone = np.sin(2 * np.pi * (2600 if hi else 1900) * s) * np.exp(-s * 60) * 0.5
    body = np.sin(2 * np.pi * 700 * s) * np.exp(-s * 90) * 0.4
    return reverb(stereo((click + tone + body).astype(np.float32)), 0.8, 0.15, 5) * level


def phone_click(level=0.12):
    n = int(0.05 * SR)
    s = np.arange(n) / SR
    m = (np.sin(2 * np.pi * 3200 * s) * np.exp(-s * 160) + rng.normal(0, 1, n) * np.exp(-s * 700) * 0.6)
    return stereo(m.astype(np.float32)) * level


def gasp_crowd(ln=3.5, level=0.25):
    """a breathy collective inhale, then nervous murmuring."""
    n = int(ln * SR)
    s = np.arange(n) / SR
    breath = noise(n, lo=500, hi=4000)
    e1 = np.clip(s / 0.25, 0, 1) * np.exp(-np.clip(s - 0.25, 0, None) * 5)
    mur = noise(n, lo=250, hi=1500)
    mod = fft_filter(np.abs(rng.normal(0, 1, (n, 2))).astype(np.float32), hi=7)
    e2 = np.clip((s - 0.5) / 0.8, 0, 1) * np.clip((ln - s) / 1.0, 0, 1)
    return (breath * e1[:, None] * 0.35 + mur * (0.3 + mod * 1.5) * e2[:, None] * 0.12) * level / 0.12


def shimmer_out(level=0.25):
    out = np.zeros((int(3 * SR), 2), np.float32)
    for i, m in enumerate([88, 84, 81, 76]):
        place(out, bell_note(440 * 2 ** ((m - 69) / 12), 0.8, 3.0), i * 0.09)
    return reverb(out, 3.0, 0.5, 9) * level


def riser(ln, level=0.2):
    n = int(ln * SR)
    s = np.arange(n) / SR
    f = 880 * (1 + 0.004 * np.sin(2 * np.pi * 5 * s))
    m = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR)
    e = (s / ln) ** 2
    return reverb(stereo((m * e).astype(np.float32)), 2.0, 0.4, 13) * level


# ---------------- build ----------------
sfx = np.zeros((N, 2), np.float32)
# beach (0–28, cut hard at the blackout; space shot is quiet-ish)
b1 = beach_amb(9.6, 1.0)
place(sfx, b1 * env(b1.shape[0], [(0, 1), (9.3, 1), (9.6, 0)])[:, None], 0.0)
b2 = beach_amb(12.0, 1.0)
place(sfx, b2 * env(b2.shape[0], [(0, 0.0), (0.15, 1), (11.0, 0.85), (12.0, 0.85)])[:, None], 16.0)
# ticks: fast & soft during the time-lapse, then one per second
tk = []
tt = 19.0
while tt < 25.0:
    tk.append((tt, 0.08 + 0.12 * (tt - 19) / 6))
    tt += 0.25 + 0.75 * ((tt - 19) / 6) ** 2
for x in (25.0, 26.0, 27.0):
    tk.append((x, 0.5))
for x, lv in tk:
    place(sfx, clock_tick(lv), x)
# Sun vanishes in space (flash at 10.5)
place(sfx, whoosh(1.0, True, 0.35), 9.1)
place(sfx, reverse_suck(0.9, 0.6), 9.65)
place(sfx, boom(5.0, 70, 28, 0.85, 0.25), 10.5)
place(sfx, night_amb(5.4) * 0.0, 10.6)
# back to the beach
place(sfx, whoosh(1.0, False, 0.25), 15.6)
# blackout at 28.0
place(sfx, boom(7.0, 60, 22, 1.05, 0.6), 28.0)
place(sfx, power_down(2.2, 0.45), 28.0)
na = night_amb(9.5)
place(sfx, na * env(na.shape[0], [(0, 0), (1.5, 0), (3.0, 1), (9.0, 1), (9.5, 0)])[:, None], 28.0)
place(sfx, gasp_crowd(4.0, 0.22), 28.35)
place(sfx, shimmer_out(0.22), 29.3)
# phones
for x in [33.4, 33.7, 33.85, 34.3, 34.6, 35.0, 35.3, 35.7]:
    place(sfx, phone_click(0.10), x)
# frozen week
place(sfx, whoosh(1.2, True, 0.3), 37.0)
wf = wind_fire(6.4)
place(sfx, 1.6 * wf * env(wf.shape[0], [(0, 0), (0.6, 1), (5.6, 1), (6.4, 0)])[:, None], 37.4)
# drifting earth
place(sfx, whoosh(1.4, False, 0.3), 43.2)
# back to reality
place(sfx, riser(1.2, 0.12), 47.9)
b3 = beach_amb(6.0, 0.9)
place(sfx, b3 * env(b3.shape[0], [(0, 0), (0.6, 1), (5.2, 1), (6.0, 0)])[:, None], 49.0)

# ---------------- score ----------------
bright = {"bpm": 100, "root": "D3",
          "progression": [[0, 4, 7, 12], [-5, -1, 2, 7], [-3, 0, 4, 9], [-7, -3, 0, 5]],
          "bars_per_chord": 1, "layers": {"pad": 0.22, "keys": 0.42, "bass": 0.32, "arp": 0.38, "tick": 0.22, "pulse": 0.18},
          "arp_pattern": [0, 2, 1, 3, 2, 1, 3, 2], "arp_div": 2, "arp_in": 0.0, "arp_oct": 1, "arp_out": 999,
          "keys_hits": [0, 1.5, 2.5], "felt": 0.4, "tick_div": 2, "perc_in": 2.4, "perc_out": 999,
          "texture": None, "pad_bright": 1.0, "reverb": 2.0, "lowpass": 10000}
mb = compose(bright, 30.0, seed=21)
dark = {"bpm": 56, "root": "D2",
        "progression": [[0, 7, 12, 15], [-2, 5, 10, 14], [-4, 3, 8, 12], [-5, 2, 7, 10]],
        "bars_per_chord": 1, "layers": {"pad": 0.55, "bass": 0.32, "bell": 0.22, "keys": 0.18},
        "bell_beats": [0, 2.5], "keys_hits": [1], "felt": 1.0, "keys_in": 4.3,
        "texture": "air", "texture_gain": 0.6, "pad_bright": 0.6, "reverb": 4.0, "lowpass": 6500, "swell_at": 12}
md = compose(dark, 21.5, seed=33)
soft = {"bpm": 100, "root": "D3",
        "progression": [[0, 4, 7, 12], [-5, -1, 2, 7], [-3, 0, 4, 9], [-7, -3, 0, 5]],
        "bars_per_chord": 1, "layers": {"pad": 0.3, "keys": 0.45, "bass": 0.25, "arp": 0.3},
        "arp_pattern": [0, 2, 1, 3], "arp_div": 2, "arp_in": 0.0, "arp_oct": 1, "arp_out": 999,
        "keys_hits": [0, 2.5], "felt": 0.5, "keys_in": 0, "texture": None, "reverb": 2.6}
ms = compose(soft, 6.5, seed=44)

mus = np.zeros((N, 2), np.float32)
# bright bed: 0–9.6 (beach), ducked under the space shot, back at 16, hard stop at 28.0
mbe = env(mb.shape[0], [(0, 1), (9.4, 1), (9.7, 0.0), (15.9, 0.0), (16.2, 1.0), (27.98, 1.0), (28.0, 0)])
place(mus, mb * mbe[:, None] * 0.55, 0.0)
# suspense: high sustained string note creeping in 20–28
n = int(8.0 * SR); s = np.arange(n) / SR
f = 880 * (1 + 0.003 * np.sin(2 * np.pi * 5.5 * s))
st = (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(2 * np.pi * np.cumsum(2 * f) / SR)) * (s / 8) ** 1.6
st[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
place(mus, reverb(stereo(st.astype(np.float32)), 1.5, 0.3, 4) * 0.08, 20.0)
# space shot drone 9.6–16
n = int(6.6 * SR); s = np.arange(n) / SR
dr = (np.sin(2 * np.pi * 36.7 * s) + 0.5 * np.sin(2 * np.pi * 55 * s) + 0.25 * np.sin(2 * np.pi * 73.4 * s)) * np.clip(s / 0.4, 0, 1) * np.clip((6.6 - s) / 0.5, 0, 1)
place(mus, reverb(stereo(dr.astype(np.float32)), 3, 0.4, 6) * 0.12, 9.6)
# dark score from 29.0 to 49
mde = env(md.shape[0], [(0, 0.0), (1.2, 1.0), (19.2, 1.0), (20.2, 0.0)])
place(mus, md * mde[:, None] * 0.62, 29.0)
# soft return at 49
place(mus, ms * env(ms.shape[0], [(0, 0), (0.8, 1), (6.0, 1), (6.5, 1)])[:, None] * 0.5, 49.0)

mix = sfx * 1.0 + mus * 1.0
for nm, a in (("sfx", sfx), ("mus", mus)):
    print(nm, " ".join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(55)))
mix[int((DUR - 0.6) * SR):] *= np.linspace(1, 0, N - int((DUR - 0.6) * SR))[:, None]
mix /= (np.max(np.abs(mix)) + 1e-9) / 0.89


def write(path, x):
    x = np.clip(x, -1, 1)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype('<i2').tobytes())


write(sys.argv[1] if len(sys.argv) > 1 else 'mix.wav', mix)
write('music_only.wav', mus / (np.max(np.abs(mus)) + 1e-9) * 0.8)
write('sfx_only.wav', sfx / (np.max(np.abs(sfx)) + 1e-9) * 0.8)
print('ok')
