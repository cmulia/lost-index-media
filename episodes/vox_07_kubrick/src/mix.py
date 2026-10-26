"""Mix narration + SFX + music for explained no. 07 (Kubrick) on the 57.0 s timeline.
Run from the episode directory:  python3 src/mix.py  -> mix.wav (then loudnorm/limiter + mux in tools.py finish)."""
import subprocess, wave, sys
import numpy as np

SR = 48000
DUR = 57.0
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

S = {k: load('sfx/' + k + '.mp3') for k in ['candle', 'room', 'film_can', 'lens_click', 'rocket', 'lens_set', 'saw', 'camera_run', 'video_hum', 'applause', 'coins', 'wind_night', 'blow', 'swoosh']}
# hook: a candle lit
place(sfx, S['candle'], 0.05, 0.45, fi=0.0)
place(sfx, S['room'], 1.0, 0.16, length=3.0, fi=0.5, fo=0.5)
# candlelight alone: the room
place(sfx, S['swoosh'], 4.0, 0.25)
place(sfx, S['room'], 4.1, 0.26, length=6.3, fi=0.5, fo=0.8)
place(sfx, S['candle'], 8.7, 0.22, start=1.0, fo=0.4)
# film stock, fastest lens
place(sfx, S['swoosh'], 10.4, 0.25)
place(sfx, S['film_can'], 10.7, 0.40)
for i in range(4):
    place(sfx, S['lens_click'], 11.0 + i * .3, 0.22, length=0.25, fo=0.05)
place(sfx, S['lens_set'], 13.1, 0.45)
place(sfx, S['lens_click'], 13.6, 0.30)
# ten lenses: rocket, clicks
place(sfx, S['swoosh'], 15.5, 0.25)
place(sfx, S['rocket'], 15.6, 0.28, fi=0.3, fo=1.0)
for i in range(10):
    place(sfx, S['lens_click'], 16.0 + i * .12, 0.18, length=0.12, fo=0.03)
place(sfx, S['lens_set'], 20.4, 0.30)
# one problem: cross-section, the saw
place(sfx, S['swoosh'], 21.8, 0.25)
place(sfx, S['lens_click'], 22.1, 0.30)
place(sfx, S['film_can'], 24.3, 0.25)
place(sfx, S['swoosh'], 26.0, 0.22)
place(sfx, S['saw'], 28.9, 0.42, fi=0.1, fo=0.6)
place(sfx, S['camera_run'], 30.3, 0.22, length=1.0, fi=0.1, fo=0.4)
# three wicks, side camera
place(sfx, S['swoosh'], 31.3, 0.25)
place(sfx, S['candle'], 31.4, 0.30, start=0.8, fo=0.5)
place(sfx, S['room'], 31.5, 0.14, length=2.2, fi=0.3, fo=0.5)
place(sfx, S['video_hum'], 33.6, 0.35, fo=0.5)
place(sfx, S['camera_run'], 35.0, 0.18, length=2.6, fi=0.3, fo=0.5)
# Oscars, lost money
place(sfx, S['swoosh'], 37.8, 0.25)
place(sfx, S['applause'], 37.9, 0.24, fi=0.3, fo=1.4)
for i in range(4):
    place(sfx, S['coins'], 38.4 + i * .22, 0.22, length=0.3, fo=0.1)
place(sfx, S['coins'], 40.1, 0.35)
# directors' poll
place(sfx, S['swoosh'], 42.1, 0.25)
place(sfx, S['wind_night'], 42.2, 0.16, length=3.6, fi=0.5, fo=0.6)
for i in range(6):
    place(sfx, S['lens_click'], 43.6 + i * .2, 0.14, length=0.12, fo=0.03)
# the moon
place(sfx, S['swoosh'], 45.9, 0.25)
place(sfx, S['wind_night'], 46.0, 0.32, length=5.4, fi=0.5, fo=0.8)
place(sfx, S['lens_set'], 47.9, 0.25)
place(sfx, S['candle'], 51.4, 0.30, start=0.8, fo=0.4)
place(sfx, S['room'], 51.5, 0.16, length=2.6, fi=0.4, fo=0.6)
# end card: the candle goes out
place(sfx, S['blow'], 53.95, 0.50)
place(sfx, S['swoosh'], 54.1, 0.22)

m = load('music.mp3')
place(mus, m, 0.0, 1.0, length=DUR, fi=0.0, fo=2.0)


def movavg(x, n):
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n)]))
    return (c[n:n + len(x)] - c[:len(x)]) / n


env = np.sqrt(movavg(vox[:, 0].astype(np.float64) ** 2, int(.25 * SR)))
speaking = np.clip(env / 0.05, 0, 1)
speaking = movavg(speaking, int(.15 * SR))
tt = np.arange(N) / SR
base = np.interp(tt, [0, 45.6, 46.0, 54.0, 54.4, DUR], [1, 1, 0.75, 0.75, 1.4, 1.4])
mus *= (0.85 * base * (1 - 0.35 * speaking))[:, None].astype(np.float32)

mix = vox + 1.3 * sfx + mus
mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('vox', vox), ('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(int(DUR))))
