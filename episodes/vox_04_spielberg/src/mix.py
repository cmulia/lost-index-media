"""Mix narration + SFX + music for explained no. 04 (Spielberg) on the 57.8 s timeline.
Run from the episode directory:  python3 src/mix.py  -> mix.wav (then loudnorm/limiter + mux in tools.py finish)."""
import subprocess, wave, sys
import numpy as np

SR = 48000
DUR = 57.8
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

S = {k: load('sfx/' + k + '.mp3') for k in ['waves', 'hydraulic', 'sputter', 'splash', 'pages', 'register', 'barrel', 'underwater', 'piano', 'crowd', 'counter', 'creak', 'museum', 'swoosh']}
# hook: harbour, a machine straining
place(sfx, S['waves'], 0.0, 0.22, length=3.2, fi=0.0, fo=0.5)
place(sfx, S['sputter'], 1.3, 0.24, fo=0.3)
# 1974: chart + harbour
place(sfx, S['swoosh'], 3.1, 0.25)
place(sfx, S['waves'], 3.2, 0.14, length=6.0, fi=0.5, fo=0.8)
place(sfx, S['pages'], 5.0, 0.28, length=0.9, fo=0.2)
# Bruce x3, rarely worked
place(sfx, S['swoosh'], 9.3, 0.25)
place(sfx, S['hydraulic'], 9.5, 0.30, fo=0.4)
place(sfx, S['splash'], 12.0, 0.28)
place(sfx, S['sputter'], 15.0, 0.30, fo=0.3)
place(sfx, S['hydraulic'], 15.9, 0.20, start=1.2, fo=0.4)
# days + budget
place(sfx, S['swoosh'], 17.0, 0.25)
place(sfx, S['pages'], 17.4, 0.40, length=3.2, fo=0.3)
place(sfx, S['counter'], 18.6, 0.35, length=2.0, fo=0.3)
place(sfx, S['register'], 21.3, 0.40)
# hide the shark
place(sfx, S['swoosh'], 22.6, 0.25)
place(sfx, S['waves'], 22.7, 0.18, length=7.2, fi=0.4, fo=0.6)
place(sfx, S['barrel'], 25.2, 0.45, fo=0.4)
place(sfx, S['underwater'], 26.4, 0.40, length=3.4, fi=0.3, fo=0.6)
place(sfx, S['piano'], 27.8, 0.55, fo=0.5)
# opening
place(sfx, S['swoosh'], 30.0, 0.25)
place(sfx, S['crowd'], 30.1, 0.26, fi=0.3, fo=1.0)
place(sfx, S['counter'], 34.3, 0.45, length=2.0, fo=0.4)
place(sfx, S['register'], 36.1, 0.35)
# good fortune, nightmares
place(sfx, S['swoosh'], 36.6, 0.25)
place(sfx, S['pages'], 38.5, 0.22, length=0.6, fo=0.2)
place(sfx, S['underwater'], 41.0, 0.22, length=2.0, fi=0.4, fo=0.6)
# back lot
place(sfx, S['swoosh'], 43.0, 0.25)
place(sfx, S['creak'], 43.1, 0.40, fi=0.3, fo=0.6)
# museum
place(sfx, S['swoosh'], 46.3, 0.25)
place(sfx, S['museum'], 46.4, 0.30, length=8.2, fi=0.4, fo=0.8)
place(sfx, S['crowd'], 50.7, 0.16, start=0.5, length=1.8, fi=0.3, fo=0.6)
place(sfx, S['splash'], 53.2, 0.14, fo=0.5)
# end card
place(sfx, S['swoosh'], 54.9, 0.22)
place(sfx, S['waves'], 55.0, 0.12, length=2.8, fi=0.3, fo=1.0)

m = load('music.mp3')
place(mus, m, 0.0, 1.0, length=DUR, fi=0.0, fo=2.0)


def movavg(x, n):
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n)]))
    return (c[n:n + len(x)] - c[:len(x)]) / n


env = np.sqrt(movavg(vox[:, 0].astype(np.float64) ** 2, int(.25 * SR)))
speaking = np.clip(env / 0.05, 0, 1)
speaking = movavg(speaking, int(.15 * SR))
tt = np.arange(N) / SR
base = np.interp(tt, [0, 52.9, 53.3, 54.8, 55.2, DUR], [1, 1, 0.35, 0.35, 1.6, 1.6])
mus *= (0.38 * base * (1 - 0.55 * speaking))[:, None].astype(np.float32)

mix = vox + 1.3 * sfx + mus
mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('vox', vox), ('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(int(DUR))))
