"""Mix narration + SFX + music for explained no. 19 (Greta Gerwig) on the 50.2 s timeline.
Run from the episode directory:  python3 src/mix.py  -> mix.wav (then loudnorm/limiter + mux in tools.py finish)."""
import subprocess, wave, sys
import numpy as np

SR = 48000
DUR = 50.2
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

S = {k: load('sfx/' + k + '.mp3') for k in ['lid','build','sparkle','stir','pour','empty_tin','press','spray','globe','ding']}
for k, t, g, kw in [('lid',0.3,0.40,{}),('build',3.6,0.30,{'fo':0.5}),('sparkle',8.5,0.34,{}),('stir',12.9,0.34,{'fo':0.3}),('pour',18.7,0.36,{'fo':0.3}),
                    ('empty_tin',22.9,0.40,{'fo':0.3}),('press',29.5,0.38,{'fo':0.3}),('spray',35.6,0.32,{'fo':0.3}),('globe',41.1,0.34,{'fo':0.3}),('ding',45.6,0.40,{})]:
    place(sfx, S[k], t, g, **kw)

m = load('music.mp3')
place(mus, m, 0.0, 1.0, length=DUR, fi=0.0, fo=2.0)


def movavg(x, n):
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n)]))
    return (c[n:n + len(x)] - c[:len(x)]) / n


env = np.sqrt(movavg(vox[:, 0].astype(np.float64) ** 2, int(.25 * SR)))
speaking = np.clip(env / 0.05, 0, 1)
speaking = movavg(speaking, int(.15 * SR))
tt = np.arange(N) / SR
base = np.interp(tt, [0, 3.4, 3.8, 22.5, 23.0, 40.5, 41.0, 47.8, 48.2, DUR], [1.2, 1.2, 0.95, 0.95, 0.85, 0.85, 1.0, 1.0, 1.7, 1.7])
mus *= (0.65 * base * (1 - 0.35 * speaking))[:, None].astype(np.float32)

mix = vox + 1.3 * sfx + mus
mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('vox', vox), ('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(int(DUR))))
