"""Mix ElevenLabs SFX + music for what if no. 03 (internet off) on the 50 s timeline."""
import subprocess, wave
import numpy as np

SR = 48000
DUR = 50.0
N = int(DUR * SR)
A = 'audio/'
OUT = 7.5      # outage
BACK = 41.0    # back online


def load(name):
    raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', A + name, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
    return x / (np.max(np.abs(x)) + 1e-9) * 0.9


def place(buf, x, t0, gain=1.0, length=None, start=0.0, fi=0.01, fo=0.04):
    x = x[int(start * SR):]
    if length is not None:
        need = int(length * SR)
        if x.shape[0] < need:
            x = np.concatenate([x] * (need // x.shape[0] + 1))
        x = x[:need]
    x = x.copy()
    a, b = int(fi * SR), int(fo * SR)
    if a: x[:a] *= np.linspace(0, 1, a)[:, None]
    if b: x[-b:] *= np.linspace(1, 0, b)[:, None]
    i = int(t0 * SR); j = min(N, i + x.shape[0])
    if j > i: buf[i:j] += x[:j - i] * gain


sfx = np.zeros((N, 2), np.float32)
mus = np.zeros((N, 2), np.float32)
S = {k: load(k + '.mp3') for k in ['typing', 'click', 'pop', 'swoosh', 'outage', 'error', 'tension', 'counter', 'underwater', 'ping_flood', 'reboot']}

# title + windows
place(sfx, S['typing'], 0.05, 0.22, length=0.9, fo=0.2)
place(sfx, S['error'], 2.62, 0.30)
place(sfx, S['swoosh'], 4.35, 0.32)
for t in (4.8, 5.08, 5.36):
    place(sfx, S['pop'], t, 0.32)
place(sfx, S['click'], 6.55, 0.45)
place(sfx, S['outage'], OUT - 0.02, 0.75)
place(sfx, S['error'], OUT + 0.35, 0.28)
place(sfx, S['tension'], OUT + 0.4, 0.30, length=25.4 - OUT - 0.4, fi=1.2, fo=1.5)
place(sfx, S['click'], 9.2, 0.45)
place(sfx, S['error'], 9.3, 0.26)
place(sfx, S['swoosh'], 10.25, 0.32)
# counters
place(sfx, S['typing'], 10.7, 0.22, length=0.8, fo=0.2)
place(sfx, S['counter'], 11.3, 0.30, length=1.5, fo=0.3)
place(sfx, S['counter'], 13.0, 0.30, length=1.4, fo=0.3)
place(sfx, S['pop'], 14.6, 0.30)
place(sfx, S['swoosh'], 16.6, 0.32)
# split
place(sfx, S['swoosh'], 17.25, 0.28)
place(sfx, S['error'], 18.8, 0.34)
place(sfx, S['counter'], 19.15, 0.26, length=1.4, fo=0.3)
place(sfx, S['swoosh'], 22.35, 0.34)
# twist / map
place(sfx, S['typing'], 23.15, 0.22, length=0.8, fo=0.2)
place(sfx, S['underwater'], 25.3, 0.42, length=33.3 - 25.3, fi=1.0, fo=0.8)
place(sfx, S['tension'], 33.2, 0.22, length=BACK - 33.2, fi=0.8, fo=0.3, start=3.0)
place(sfx, S['pop'], 27.0, 0.28)
place(sfx, S['pop'], 28.9, 0.28)
place(sfx, S['swoosh'], 30.1, 0.30)
place(sfx, S['typing'], 31.2, 0.18, length=1.3, fo=0.3)
# outages
place(sfx, S['swoosh'], 33.3, 0.32)
place(sfx, S['typing'], 33.5, 0.22, length=0.9, fo=0.2)
place(sfx, S['pop'], 34.0, 0.30)
place(sfx, S['pop'], 37.3, 0.30)
place(sfx, S['error'], 37.6, 0.20)
# back online
place(sfx, S['reboot'], BACK - 0.05, 0.55)
place(sfx, S['ping_flood'], 42.0, 0.42)
place(sfx, S['typing'], 46.7, 0.22, length=0.7, fo=0.2)
place(sfx, S['swoosh'], 46.45, 0.28)

m = load('music.mp3')
place(mus, m, 0.0, 0.40, length=OUT, fo=0.015)            # hard cut at the outage
place(mus, m, BACK, 0.42, length=DUR - BACK, start=18.0, fi=0.05, fo=2.5)  # back online: brighter second half

mix = sfx + mus
mix[-int(0.4 * SR):] *= np.linspace(1, 0, int(0.4 * SR))[:, None]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
with wave.open('mix.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(50)))
