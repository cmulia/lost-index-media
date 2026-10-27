"""Mix narration + SFX + music for explained no. 08 (Carpenter) on the 51.0 s timeline.
Run from the episode directory:  python3 src/mix.py  -> mix.wav (then loudnorm/limiter + mux in tools.py finish)."""
import subprocess, wave, sys
import numpy as np

SR = 48000
DUR = 51.0
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

S = {k: load('sfx/' + k + '.mp3') for k in ['mask_stretch', 'shop_bell', 'register', 'scissors', 'spray', 'leaves', 'projector', 'coins', 'plaster', 'wind_night']}
# hook: the rubber mask
place(sfx, S['mask_stretch'], 0.0, 0.40, fi=0.0)
place(sfx, S['wind_night'], 0.3, 0.14, length=2.8, fi=0.4, fo=0.5)
# Carpenter, budget counter
place(sfx, S['projector'], 3.2, 0.20, length=4.6, fi=0.3, fo=0.8)
place(sfx, S['register'], 7.3, 0.30)
# magic shop
place(sfx, S['shop_bell'], 12.9, 0.42)
# Kirk mask, $1.98
place(sfx, S['mask_stretch'], 15.3, 0.30)
place(sfx, S['register'], 20.8, 0.45)
# the changes
place(sfx, S['scissors'], 21.7, 0.40)
place(sfx, S['spray'], 24.9, 0.40, fo=0.4)
# South Pasadena, leaves
place(sfx, S['leaves'], 28.9, 0.42, fi=0.1, fo=0.6)
place(sfx, S['wind_night'], 27.1, 0.12, length=5.0, fi=0.6, fo=0.8)
# earnings
place(sfx, S['coins'], 33.1, 0.40, fo=0.4)
# Shatner: plaster cast
place(sfx, S['plaster'], 38.6, 0.32, fi=0.2, fo=0.6)
# twist: night porch
place(sfx, S['wind_night'], 42.8, 0.30, length=6.0, fi=0.6, fo=1.0)
place(sfx, S['mask_stretch'], 48.0, 0.22, fo=0.4)

m = load('music.mp3')
place(mus, m, 0.0, 1.0, length=DUR, fi=0.0, fo=2.0)


def movavg(x, n):
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n)]))
    return (c[n:n + len(x)] - c[:len(x)]) / n


env = np.sqrt(movavg(vox[:, 0].astype(np.float64) ** 2, int(.25 * SR)))
speaking = np.clip(env / 0.05, 0, 1)
speaking = movavg(speaking, int(.15 * SR))
tt = np.arange(N) / SR
base = np.interp(tt, [0, 42.5, 42.9, 48.0, 48.4, DUR], [1, 1, 0.8, 0.8, 1.4, 1.4])
mus *= (0.85 * base * (1 - 0.35 * speaking))[:, None].astype(np.float32)

mix = vox + 1.3 * sfx + mus
mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('vox', vox), ('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(int(DUR))))
