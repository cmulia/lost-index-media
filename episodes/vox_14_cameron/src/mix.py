"""Mix narration + SFX + music for explained no. 14 (Cameron) on the 47.6 s timeline.
Run from the episode directory:  python3 src/mix.py  -> mix.wav (then loudnorm/limiter + mux in tools.py finish)."""
import subprocess, wave, sys
import numpy as np

SR = 48000
DUR = 47.6
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

S = {k: load('sfx/' + k + '.mp3') for k in ['coin','fever','fire','pencil','typewriter','pen_sign','clapper','projector','cash_register','chair']}
place(sfx, S['coin'], 1.55, 0.40)
place(sfx, S['fever'], 6.9, 0.30, fi=0.4, fo=1.0)
place(sfx, S['fire'], 9.9, 0.36, fo=0.6)
place(sfx, S['pencil'], 13.7, 0.34, fo=0.3)
place(sfx, S['typewriter'], 15.7, 0.30, fo=0.3)
place(sfx, S['pen_sign'], 20.7, 0.34)
place(sfx, S['chair'], 23.2, 0.36)
place(sfx, S['clapper'], 25.05, 0.40)
place(sfx, S['projector'], 29.3, 0.28, fi=0.2, fo=1.0)
place(sfx, S['cash_register'], 38.5, 0.32)
place(sfx, S['chair'], 41.3, 0.40)

m = load('music.mp3')
place(mus, m, 0.0, 1.0, length=DUR, fi=0.0, fo=2.0)


def movavg(x, n):
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n)]))
    return (c[n:n + len(x)] - c[:len(x)]) / n


env = np.sqrt(movavg(vox[:, 0].astype(np.float64) ** 2, int(.25 * SR)))
speaking = np.clip(env / 0.05, 0, 1)
speaking = movavg(speaking, int(.15 * SR))
tt = np.arange(N) / SR
base = np.interp(tt, [0, 9.5, 10.0, 38.0, 38.5, 42.5, 42.8, 45.4, 45.8, DUR], [1, 1, 0.9, 0.9, 1.0, 1.0, 1.05, 1.05, 1.4, 1.4])
mus *= (0.65 * base * (1 - 0.35 * speaking))[:, None].astype(np.float32)

mix = vox + 1.3 * sfx + mus
mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('vox', vox), ('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(int(DUR))))
