"""Mix narration + SFX + music for explained no. 03 (Miyazaki) on the 57.8 s timeline.
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

S = {k: load('sfx/' + k + '.mp3') for k in ['sheathe', 'sword_set', 'scissors', 'film_run', 'vhs', 'office', 'chair', 'stamp', 'laugh_room', 'projector', 'coins', 'applause', 'wind_chime', 'page', 'swoosh']}
# hook: the sword
place(sfx, S['sheathe'], 0.05, 0.42, fi=0.0)
place(sfx, S['sword_set'], 2.3, 0.35)
# 1999: film strip, scissors
place(sfx, S['swoosh'], 4.0, 0.25)
place(sfx, S['film_run'], 4.1, 0.26, length=5.4, fi=0.3, fo=0.6)
place(sfx, S['page'], 9.6, 0.30)
for t in (10.9, 11.6, 12.3):
    place(sfx, S['scissors'], t, 0.32)
place(sfx, S['scissors'], 12.95, 0.45)
# burned before: VHS
place(sfx, S['swoosh'], 13.9, 0.25)
place(sfx, S['vhs'], 14.1, 0.45)
place(sfx, S['scissors'], 17.8, 0.35)
place(sfx, S['stamp'], 18.2, 0.35)
# boardroom
place(sfx, S['swoosh'], 19.0, 0.25)
place(sfx, S['office'], 19.1, 0.22, length=11.3, fi=0.5, fo=0.8)
place(sfx, S['chair'], 19.4, 0.30)
place(sfx, S['sheathe'], 20.9, 0.45, fo=0.3)
place(sfx, S['sword_set'], 22.5, 0.40)
place(sfx, S['chair'], 26.1, 0.25)
place(sfx, S['sword_set'], 27.45, 0.55)
place(sfx, S['stamp'], 27.6, 0.30)
# Miyazaki laughs
place(sfx, S['swoosh'], 30.5, 0.25)
place(sfx, S['laugh_room'], 30.6, 0.22, fi=0.3, fo=0.8)
place(sfx, S['page'], 36.5, 0.32)
place(sfx, S['stamp'], 40.05, 0.45)
# uncut, box office
place(sfx, S['swoosh'], 41.2, 0.25)
place(sfx, S['projector'], 41.3, 0.26, length=4.5, fi=0.3, fo=0.6)
place(sfx, S['coins'], 43.9, 0.40)
place(sfx, S['coins'], 44.8, 0.28)
# Oscar, stayed home
place(sfx, S['swoosh'], 45.9, 0.25)
place(sfx, S['applause'], 46.0, 0.24, fi=0.3, fo=1.4)
place(sfx, S['swoosh'], 49.3, 0.22)
place(sfx, S['wind_chime'], 49.4, 0.30, length=5.2, fi=0.5, fo=0.8)
place(sfx, S['page'], 50.6, 0.25)
# end card
place(sfx, S['swoosh'], 54.9, 0.22)
place(sfx, S['sword_set'], 55.2, 0.28)

m = load('music.mp3')
place(mus, m, 0.0, 1.0, length=DUR, fi=0.0, fo=2.0)


def movavg(x, n):
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n)]))
    return (c[n:n + len(x)] - c[:len(x)]) / n


env = np.sqrt(movavg(vox[:, 0].astype(np.float64) ** 2, int(.25 * SR)))
speaking = np.clip(env / 0.05, 0, 1)
speaking = movavg(speaking, int(.15 * SR))
tt = np.arange(N) / SR
base = np.interp(tt, [0, 39.4, 39.9, 41.0, 41.4, 54.8, 55.2, DUR], [1, 1, 0.3, 0.3, 1, 1, 1.5, 1.5])
mus *= (0.95 * base * (1 - 0.55 * speaking))[:, None].astype(np.float32)

mix = vox + 1.3 * sfx + mus
mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('vox', vox), ('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(int(DUR))))
