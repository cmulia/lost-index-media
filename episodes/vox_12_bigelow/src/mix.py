"""Mix narration + SFX + music for explained no. 12 (Bigelow) on the 56.0 s timeline.
Run from the episode directory:  python3 src/mix.py  -> mix.wav (then loudnorm/limiter + mux in tools.py finish)."""
import subprocess, wave, sys
import numpy as np

SR = 48000
DUR = 56.0
N = int(DUR * SR)
A = 'audio/'
LEAD = 0.2   # narration starts here
OUT = sys.argv[1] if len(sys.argv) > 1 else 'mix.wav'


def load(name, norm=True):
    raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', A + name, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
    return x / (np.max(np.abs(x)) + 1e-9) * 0.9 if norm else x


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


vox = np.zeros((N, 2), np.float32)
sfx = np.zeros((N, 2), np.float32)
mus = np.zeros((N, 2), np.float32)
place(vox, load('narration.mp3'), LEAD, 1.0, fi=0.0, fo=0.05)

S = {k: load('sfx/' + k + '.mp3') for k in ['wind', 'stamp', 'visor', 'coins', 'envelope', 'hush', 'applause', 'boom', 'seat', 'whoosh']}
# hook: desert wind over the field notebook
place(sfx, S['wind'], 0.0, 0.30, fi=0.0, fo=1.0)
# date stamp, then the bomb-suit helmet
place(sfx, S['stamp'], 3.9, 0.46)
place(sfx, S['visor'], 4.5, 0.26, fi=0.2, fo=0.8)
# the money
place(sfx, S['coins'], 12.1, 0.32, fo=0.6)
place(sfx, S['whoosh'], 13.9, 0.24)
# the envelope
place(sfx, S['hush'], 19.85, 0.28, fi=0.3, fo=0.6)
place(sfx, S['envelope'], 20.85, 0.42)
# first woman
place(sfx, S['boom'], 25.8, 0.40)
place(sfx, S['applause'], 27.6, 0.20, fi=0.4, fo=1.6)
# Best Picture stamp
place(sfx, S['stamp'], 30.75, 0.40)
# Avatar's three
place(sfx, S['whoosh'], 36.45, 0.24)
# on his feet
place(sfx, S['seat'], 47.9, 0.42)
place(sfx, S['applause'], 48.2, 0.16, fi=0.5, fo=1.5)
# twist: desert again
place(sfx, S['wind'], 49.7, 0.18, fi=0.4, fo=1.0)
# end card
place(sfx, S['whoosh'], 53.4, 0.26)

m = load('music.mp3')
place(mus, m, 0.0, 1.0, length=DUR, fi=0.0, fo=2.0)


def movavg(x, n):
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n)]))
    return (c[n:n + len(x)] - c[:len(x)]) / n


env = np.sqrt(movavg(vox[:, 0].astype(np.float64) ** 2, int(.25 * SR)))
speaking = np.clip(env / 0.05, 0, 1)
speaking = movavg(speaking, int(.15 * SR))
tt = np.arange(N) / SR
base = np.interp(tt, [0, 19.6, 20.0, 25.5, 25.9, 42.2, 42.6, 49.4, 49.8, 53.1, 53.5, DUR], [1, 1, 0.85, 0.85, 1.05, 1.05, 0.9, 0.9, 1.05, 1.05, 1.4, 1.4])
mus *= (0.65 * base * (1 - 0.35 * speaking))[:, None].astype(np.float32)

mix = vox + 1.3 * sfx + mus
mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('vox', vox), ('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(int(DUR))))
