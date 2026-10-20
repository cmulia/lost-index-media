"""Mix ElevenLabs SFX + music for what if no. 03 (internet off) on the 50 s timeline."""
import subprocess, wave
import numpy as np

SR = 48000
DUR = 50.0
N = int(DUR * SR)
A = 'audio/'


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
S = {k: load(k + '.mp3') for k in ['pop', 'swoosh', 'jump', 'fall_wind', 'rumble', 'whoosh_big', 'weightless', 'splash', 'drill', 'tick', 'ding', 'harbour']}
place(sfx, S['harbour'], 0.0, 0.30, length=10.0, fi=0.05, fo=0.6)
place(sfx, S['swoosh'], 3.9, 0.30)
place(sfx, S['pop'], 4.6, 0.32); place(sfx, S['pop'], 5.1, 0.24)
place(sfx, S['swoosh'], 6.9, 0.26); place(sfx, S['pop'], 7.25, 0.30)
for k in range(10): place(sfx, S['tick'], 7.75 + k * 0.11, 0.14)
place(sfx, S['ding'], 8.9, 0.26)
place(sfx, S['swoosh'], 9.55, 0.30)
for t in (10.0, 10.55, 11.1): place(sfx, S['tick'], t, 0.45)
place(sfx, S['ding'], 11.65, 0.40)
place(sfx, S['jump'], 12.1, 0.45)
place(sfx, S['fall_wind'], 12.6, 0.30, length=25.7 - 12.6, fi=0.6, fo=0.2)
place(sfx, S['rumble'], 15.4, 0.22, length=25.6 - 15.4, fi=1.0, fo=0.3)
for t in (15.35, 19.55, 22.75): place(sfx, S['whoosh_big'], t, 0.40)
place(sfx, S['weightless'], 25.6, 0.42)
place(sfx, S['whoosh_big'], 27.9, 0.40)
place(sfx, S['fall_wind'], 28.0, 0.26, length=3.4, fi=0.3, fo=1.2, start=3.0)
place(sfx, S['splash'], 31.7, 0.50)
place(sfx, S['swoosh'], 36.2, 0.30)
place(sfx, S['drill'], 37.1, 0.26, length=5.0, fi=0.4, fo=1.2)
place(sfx, S['pop'], 38.2, 0.30)
for k in range(12): place(sfx, S['tick'], 38.0 + k * 0.11, 0.12)
place(sfx, S['ding'], 39.4, 0.30)
place(sfx, S['pop'], 40.5, 0.26); place(sfx, S['pop'], 41.6, 0.26)
place(sfx, S['swoosh'], 44.3, 0.30); place(sfx, S['pop'], 45.8, 0.28); place(sfx, S['weightless'], 45.9, 0.22); place(sfx, S['harbour'], 46.0, 0.18, length=4.0, fi=0.8, fo=0.4)

m = load('music.mp3')
place(mus, m, 0.0, 0.36, length=DUR, fi=0.02, fo=1.5)

mix = sfx + mus
mix[-int(0.4 * SR):] *= np.linspace(1, 0, int(0.4 * SR))[:, None]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
with wave.open('mix.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(50)))
