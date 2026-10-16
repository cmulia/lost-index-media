"""Small additive-synthesis composer for ambient documentary beds.

Stand-in until ElevenLabs music is available: soft pads, felt keys, arpeggios, bass,
bells, a few pulse/tick percussion voices and noise textures, with FFT reverb.
All original, generated from scratch.
"""
import numpy as np

SR = 48000
NOTE = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6,
        "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}


def midi(name):
    n, o = name[:-1], int(name[-1])
    return 12 * (o + 1) + NOTE[n]


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def env_adsr(n, a, r, sustain_len):
    e = np.ones(n, np.float32)
    na, nr = int(a * SR), int(r * SR)
    if na:
        e[:na] = np.linspace(0, 1, na) ** 2
    s_end = min(n, int(sustain_len * SR))
    if s_end < n:
        rel = np.linspace(1, 0, n - s_end) ** 2
        e[s_end:] *= rel
    return e


def place(buf, sig, t0):
    i = int(t0 * SR)
    if i >= buf.shape[0]:
        return
    j = min(buf.shape[0], i + sig.shape[0])
    buf[i:j] += sig[: j - i]


def pad_note(f, dur, rng, bright=1.0):
    n = int((dur + 2.0) * SR)
    t = np.arange(n) / SR
    out = np.zeros((n, 2), np.float32)
    for ch, det in ((0, -0.0035), (1, 0.0035)):
        s = np.zeros(n, np.float32)
        for k in range(1, 7):
            amp = (1 / k ** 1.7) * (bright if k > 2 else 1)
            ph = rng.uniform(0, 2 * np.pi)
            s += amp * np.sin(2 * np.pi * f * k * (1 + det) * t + ph)
        trem = 1 + 0.08 * np.sin(2 * np.pi * rng.uniform(0.08, 0.15) * t + rng.uniform(0, 6))
        out[:, ch] = s * trem
    e = env_adsr(n, 1.4, 2.0, dur + 0.2)
    return out * e[:, None] * 0.18


def key_note(f, vel=1.0, length=3.5, felt=0.6):
    n = int(length * SR)
    t = np.arange(n) / SR
    s = np.zeros(n, np.float32)
    B = 0.00035
    for k in range(1, 9):
        fk = f * k * np.sqrt(1 + B * k * k)
        if fk > 9000:
            break
        amp = (1 / k ** (1.6 + felt)) * vel
        s += amp * np.sin(2 * np.pi * fk * t) * np.exp(-t * (0.9 + 0.75 * k))
    att = np.minimum(1, t / 0.006)
    s *= att
    # tiny hammer thump
    s[: int(0.012 * SR)] += (np.random.default_rng(int(f)).normal(0, 1, int(0.012 * SR)) *
                              np.linspace(0.05, 0, int(0.012 * SR)) * vel)
    return np.stack([s, s], 1) * 0.30


def bell_note(f, vel=1.0, length=6.0):
    n = int(length * SR)
    t = np.arange(n) / SR
    s = np.zeros(n, np.float32)
    for ratio, amp, dec in ((1, 1, 0.6), (2.76, 0.45, 1.3), (5.40, 0.25, 2.2), (8.93, 0.12, 3.5)):
        s += amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t * dec)
    s *= np.minimum(1, t / 0.003) * vel
    return np.stack([s, s], 1) * 0.16


def bass_note(f, dur):
    n = int((dur + 0.6) * SR)
    t = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * t) + 0.28 * np.sin(2 * np.pi * 2 * f * t) + 0.08 * np.sin(2 * np.pi * 3 * f * t)
    e = np.minimum(1, t / 0.03) * np.exp(-t * 0.5)
    e *= env_adsr(n, 0.0, 0.5, dur)
    return np.stack([s * e, s * e], 1).astype(np.float32) * 0.22


def kick(vel=1.0):
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 42 + 80 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 9) * vel
    return np.stack([s, s], 1).astype(np.float32) * 0.35


def tick(rng, vel=1.0, bright=1.0):
    n = int(0.03 * SR)
    s = rng.normal(0, 1, n).astype(np.float32)
    s = np.diff(np.concatenate([[0], s])) if bright > 0.5 else s
    s *= np.exp(-np.arange(n) / SR * 260) * vel
    return np.stack([s, s], 1) * 0.10


def fft_filter(x, lo=None, hi=None):
    X = np.fft.rfft(x, axis=0)
    fr = np.fft.rfftfreq(x.shape[0], 1 / SR)
    g = np.ones_like(fr)
    if hi:
        g *= 1 / np.sqrt(1 + (fr / hi) ** 4)
    if lo:
        g *= 1 / np.sqrt(1 + (lo / np.maximum(fr, 1e-3)) ** 4)
    X *= g[:, None] if x.ndim == 2 else g
    return np.fft.irfft(X, n=x.shape[0], axis=0).astype(np.float32)


def reverb(x, seconds=2.6, mix=0.35, seed=1):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = rng.normal(0, 1, (n, 2)).astype(np.float32) * np.exp(-t * 6.9 / seconds)[:, None]
    ir = fft_filter(ir, lo=150, hi=6000)
    ir[: int(0.012 * SR)] = 0
    ir /= np.sqrt((ir ** 2).sum(0, keepdims=True))
    L = x.shape[0] + n
    nfft = 1 << (L - 1).bit_length()
    X = np.fft.rfft(x, nfft, axis=0)
    I = np.fft.rfft(ir, nfft, axis=0)
    wet = np.fft.irfft(X * I, nfft, axis=0)[: x.shape[0]].astype(np.float32)
    return x * (1 - mix) + wet * mix * 3.0


def texture(kind, n, rng):
    if not kind:
        return np.zeros((n, 2), np.float32)
    if kind == "vinyl":
        hiss = fft_filter(rng.normal(0, 1, (n, 2)).astype(np.float32), lo=1500, hi=9000) * 0.010
        clicks = np.zeros((n, 2), np.float32)
        for _ in range(int(n / SR * 7)):
            i = rng.integers(0, n - 200)
            a = rng.uniform(0.02, 0.12) * (1 if rng.random() > 0.1 else 3)
            c = rng.normal(0, 1, 60) * np.exp(-np.arange(60) / 9) * a
            clicks[i:i + 60, rng.integers(0, 2)] += c
        rumble = fft_filter(rng.normal(0, 1, (n, 2)).astype(np.float32), hi=90) * 0.02
        return hiss + clicks + rumble
    if kind == "tape":
        hiss = fft_filter(rng.normal(0, 1, (n, 2)).astype(np.float32), lo=400, hi=7000) * 0.016
        wob = 1 + 0.25 * np.sin(2 * np.pi * 0.7 * np.arange(n) / SR)
        return hiss * wob[:, None].astype(np.float32)
    if kind == "air":
        return fft_filter(rng.normal(0, 1, (n, 2)).astype(np.float32), lo=200, hi=2500) * 0.012
    if kind == "room":
        return fft_filter(rng.normal(0, 1, (n, 2)).astype(np.float32), lo=80, hi=900) * 0.02
    if kind == "hum":
        t = np.arange(n) / SR
        s = 0.012 * np.sin(2 * np.pi * 60 * t) + 0.006 * np.sin(2 * np.pi * 120 * t)
        hiss = fft_filter(rng.normal(0, 1, (n, 2)).astype(np.float32), lo=2000, hi=8000) * 0.006
        return np.stack([s, s], 1).astype(np.float32) + hiss
    return np.zeros((n, 2), np.float32)


def compose(spec, duration, seed=0):
    """spec: dict with bpm, root, progression (list of semitone lists), bars_per_chord,
    layers {pad, keys, arp, bass, bell, pulse, tick}, texture, arp_pattern, swell_at (s)."""
    rng = np.random.default_rng(seed)
    n = int((duration + 1.0) * SR)
    dry = np.zeros((n, 2), np.float32)
    wet = np.zeros((n, 2), np.float32)
    perc = np.zeros((n, 2), np.float32)
    bpm = spec.get("bpm", 70)
    beat = 60 / bpm
    bar = beat * spec.get("beats_per_bar", 4)
    bpc = spec.get("bars_per_chord", 2)
    chord_len = bar * bpc
    root = midi(spec.get("root", "D3"))
    prog = spec["progression"]
    L = spec.get("layers", {})
    arp_pat = spec.get("arp_pattern", [0, 1, 2, 3, 2, 1])
    arp_div = spec.get("arp_div", 2)  # notes per beat
    keys_in = spec.get("keys_in", bar * 1)
    arp_in = spec.get("arp_in", duration * 0.3)
    arp_out = spec.get("arp_out", duration - 6)
    perc_in = spec.get("perc_in", bar * 2)
    perc_out = spec.get("perc_out", duration - 5)
    t = 0.0
    ci = 0
    while t < duration + 0.5:
        chord = prog[ci % len(prog)]
        notes = [root + s for s in chord]
        if L.get("pad"):
            for m in notes:
                place(wet, pad_note(hz(m + 12 * spec.get("pad_oct", 0)), chord_len, rng,
                                    spec.get("pad_bright", 0.8)) * L["pad"], t)
        if L.get("bass"):
            place(dry, bass_note(hz(notes[0] - 12), chord_len) * L["bass"], t)
        if L.get("keys") and t >= keys_in - 1e-6:
            hits = spec.get("keys_hits", [0, 2.5])
            for hb in hits:
                tt = t + hb * beat
                if tt < duration:
                    for k, m in enumerate(notes[:4]):
                        place(wet, key_note(hz(m + 12), vel=0.8 - 0.1 * k, felt=spec.get("felt", 0.6)) * L["keys"],
                              tt + k * 0.018)
        if L.get("arp"):
            steps = int(chord_len / beat * arp_div)
            for s in range(steps):
                tt = t + s * beat / arp_div
                if arp_in <= tt < arp_out:
                    m = notes[arp_pat[s % len(arp_pat)] % len(notes)] + 12 * spec.get("arp_oct", 2)
                    vel = 0.55 + 0.25 * ((s % 4) == 0)
                    place(wet, key_note(hz(m), vel=vel, length=1.6, felt=1.0) * L["arp"], tt)
        if L.get("bell"):
            for s in spec.get("bell_beats", [0]):
                tt = t + s * beat
                if tt < duration:
                    m = notes[rng.integers(0, len(notes))] + 24
                    place(wet, bell_note(hz(m), vel=0.9) * L["bell"], tt)
        if L.get("pulse") or L.get("tick"):
            for s in range(int(chord_len / beat)):
                tt = t + s * beat
                if perc_in <= tt < perc_out:
                    if L.get("pulse") and s % spec.get("pulse_every", 2) == 0:
                        place(perc, kick(0.8) * L["pulse"], tt)
                    if L.get("tick"):
                        for sub in range(spec.get("tick_div", 1)):
                            place(perc, tick(rng, 0.9 if sub == 0 else 0.5) * L["tick"], tt + sub * beat / spec.get("tick_div", 1))
        t += chord_len
        ci += 1
    wet = reverb(wet, spec.get("reverb", 2.8), 0.42, seed + 3)
    mix = dry + wet + reverb(perc, 1.2, 0.2, seed + 5) + texture(spec.get("texture"), n, rng) * spec.get("texture_gain", 1.0)
    # gentle arrangement envelope: fade in, optional swell, fade out
    tt = np.arange(n) / SR
    g = np.clip(tt / 2.5, 0, 1)
    sw = spec.get("swell_at")
    if sw:
        g = g * (1 + 0.35 * np.exp(-((tt - sw) / 4.0) ** 2))
    g *= np.clip((duration + 0.8 - tt) / 2.8, 0, 1)
    mix *= g[:, None].astype(np.float32)
    mix = fft_filter(mix, lo=35, hi=spec.get("lowpass", 9000))
    peak = np.max(np.abs(mix)) + 1e-9
    return (mix / peak * 0.7).astype(np.float32)
