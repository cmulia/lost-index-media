"""Mix narration + SFX + music for explained no. 06 (Nolan) on the 57.0 s timeline.
Run from the episode directory:  python3 src/mix.py [out.wav]"""
import subprocess, wave, sys
import numpy as np

SR = 48000
DUR = 57.0
N = int(DUR * SR)
A = 'audio/'
LEAD = 0.2
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

S = {k: load('sfx/' + k + '.mp3') for k in ['cans', 'tear', 'wind', 'clap', 'pencil', 'jet', 'desert', 'metronome', 'projector', 'rotary', 'flip', 'applause', 'swoosh']}
# hook: film cans
place(sfx, S['cans'], 0.05, 0.45, fi=0.0)
place(sfx, S['metronome'], 0.3, 0.10, length=3.8, fi=0.5, fo=0.6)
# pay slip
place(sfx, S['swoosh'], 4.2, 0.25)
place(sfx, S['tear'], 6.3, 0.45)
place(sfx, S['cans'], 7.05, 0.25, start=0.2)
place(sfx, S['cans'], 8.6, 0.25, start=0.2)
# Saturdays: wind-up camera, pencil ticks, clap
place(sfx, S['swoosh'], 10.2, 0.25)
place(sfx, S['wind'], 10.4, 0.30, fo=0.8)
place(sfx, S['pencil'], 12.2, 0.40, length=2.4, fo=0.3)
for i in range(3):
    place(sfx, S['clap'], 14.85 + i * 1.3 + (0 if i < 2 else 0.2), 0.30)
place(sfx, S['wind'], 17.7, 0.22, start=1.5, length=1.8, fi=0.2, fo=0.5)
# first takes + UCL
place(sfx, S['clap'], 19.55, 0.5)
place(sfx, S['swoosh'], 21.3, 0.25)
# twenty years on, Tenet
place(sfx, S['swoosh'], 26.0, 0.25)
place(sfx, S['projector'], 26.1, 0.14, length=3.6, fi=0.3, fo=0.5)
place(sfx, S['swoosh'], 29.8, 0.28)
place(sfx, S['jet'], 29.9, 0.42, fi=0.2, fo=0.8)
place(sfx, S['cans'], 34.1, 0.22, start=0.2)
# Trinity
place(sfx, S['swoosh'], 36.3, 0.25)
place(sfx, S['desert'], 36.4, 0.32, length=4.9, fi=0.4, fo=0.6)
# Oscars
place(sfx, S['swoosh'], 41.3, 0.25)
place(sfx, S['applause'], 41.4, 0.24, fi=0.3, fo=1.2)
for i in range(7):
    place(sfx, S['pencil'], 41.7 + i * .18, 0.18, length=0.15, fo=0.05)
place(sfx, S['applause'], 43.4, 0.18, start=1.0, fi=0.2, fo=1.4)
# no email
place(sfx, S['swoosh'], 45.7, 0.25)
place(sfx, S['rotary'], 46.0, 0.35)
place(sfx, S['flip'], 50.0, 0.45)
place(sfx, S['metronome'], 50.5, 0.12, length=3.5, fi=0.5, fo=0.8)
# end card
place(sfx, S['swoosh'], 54.0, 0.22)
place(sfx, S['clap'], 54.3, 0.3)

m = load('music.mp3')
place(mus, m, 0.0, 1.0, length=DUR, fi=0.0, fo=2.0)


def movavg(x, n):
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n)]))
    return (c[n:n + len(x)] - c[:len(x)]) / n


env = np.sqrt(movavg(vox[:, 0].astype(np.float64) ** 2, int(.25 * SR)))
speaking = np.clip(env / 0.05, 0, 1)
speaking = movavg(speaking, int(.15 * SR))
tt = np.arange(N) / SR
base = np.interp(tt, [0, 45.5, 46.2, 53.9, 54.3, DUR], [1, 1, 0.45, 0.45, 1.5, 1.5])
mus *= (0.50 * base * (1 - 0.55 * speaking))[:, None].astype(np.float32)

mix = vox + 1.3 * sfx + mus
mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('vox', vox), ('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(int(DUR))))
