"""Mix narration + SFX + music for explained no. 15 (Satyajit Ray) on the 52.6 s timeline.
Run from the episode directory:  python3 src/mix.py  -> mix.wav (then loudnorm/limiter + mux in tools.py finish)."""
import subprocess, wave, sys
import numpy as np

SR = 48000
DUR = 52.6
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

S = {k: load('sfx/' + k + '.mp3') for k in ['jewellery','coins','rain','camera_stop','stamp','projector','applause','monitor','lamp','page']}
place(sfx, S['jewellery'], 1.2, 0.40)
place(sfx, S['coins'], 8.4, 0.32, fo=0.4)
place(sfx, S['rain'], 12.1, 0.30, fi=0.4, fo=1.2)
place(sfx, S['camera_stop'], 15.5, 0.34, fo=0.3)
place(sfx, S['stamp'], 19.5, 0.40)
place(sfx, S['projector'], 21.8, 0.28, fi=0.2, fo=0.8)
place(sfx, S['applause'], 25.0, 0.26, fi=0.3, fo=1.5)
place(sfx, S['monitor'], 31.3, 0.30, fi=0.4, fo=1.0)
place(sfx, S['lamp'], 40.4, 0.40)
place(sfx, S['page'], 47.3, 0.36)

m = load('music.mp3')
place(mus, m, 0.0, 1.0, length=DUR, fi=0.0, fo=2.0)


def movavg(x, n):
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n)]))
    return (c[n:n + len(x)] - c[:len(x)]) / n


env = np.sqrt(movavg(vox[:, 0].astype(np.float64) ** 2, int(.25 * SR)))
speaking = np.clip(env / 0.05, 0, 1)
speaking = movavg(speaking, int(.15 * SR))
tt = np.arange(N) / SR
base = np.interp(tt, [0, 12.0, 12.5, 24.5, 25.0, 39.0, 39.5, 41.6, 42.0, 50.4, 50.8, DUR], [1.3, 1.2, 0.9, 0.9, 0.72, 0.72, 0.8, 0.8, 1.1, 1.1, 1.8, 1.8])
mus *= (0.65 * base * (1 - 0.35 * speaking))[:, None].astype(np.float32)

mix = vox + 1.3 * sfx + mus
mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('vox', vox), ('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(int(DUR))))
