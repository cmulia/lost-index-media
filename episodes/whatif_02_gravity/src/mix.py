"""Mix ElevenLabs SFX + music for what if no. 02 onto the 44.1 s timeline."""
import subprocess, sys, wave
import numpy as np

SR = 48000
DUR = 44.1
N = int(DUR * SR)
A = 'audio/'
OFF, ON = 6.5, 27.3


def load(name):
    raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', A + name, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def norm(x, peak=0.9):
    return x / (np.max(np.abs(x)) + 1e-9) * peak


def fade(x, fi=0.02, fo=0.05):
    n = x.shape[0]
    a, b = int(fi * SR), int(fo * SR)
    if a: x[:a] *= np.linspace(0, 1, a)[:, None]
    if b: x[-b:] *= np.linspace(1, 0, b)[:, None]
    return x


def place(buf, x, t0, gain=1.0, length=None, fi=0.02, fo=0.05):
    if length is not None:
        need = int(length * SR)
        if x.shape[0] < need:  # loop
            reps = need // x.shape[0] + 1
            x = np.concatenate([x] * reps)
        x = x[:need]
    x = fade(x.copy(), fi, fo) * gain
    i = int(t0 * SR)
    j = min(N, i + x.shape[0])
    if j > i:
        buf[i:j] += x[:j - i]


def env(points):
    tt = np.arange(N) / SR
    xs, ys = zip(*points)
    return np.interp(tt, xs, ys).astype(np.float32)[:, None]


sfx = np.zeros((N, 2), np.float32)
mus = np.zeros((N, 2), np.float32)

amb = norm(load('amb_venice.mp3'))
place(sfx, amb, 0.0, 0.7, length=OFF + 0.6, fo=0.8)
place(sfx, amb, 31.0, 0.6, length=4.6, fi=0.3, fo=0.6)
place(sfx, norm(load('off_bwoom.mp3')), OFF - 0.25, 0.55)
place(sfx, norm(load('float_air.mp3')), OFF + 0.2, 0.26, length=ON - OFF - 0.1, fi=1.0, fo=0.05)
pig = norm(load('pigeons.mp3'))
place(sfx, pig, 8.3, 0.35)
place(sfx, pig, 20.3, 0.30)
place(sfx, norm(load('crowd_whoa.mp3')), 8.6, 0.38)
place(sfx, norm(load('blobs.mp3')), 15.9, 0.42)
place(sfx, norm(load('rise_whoosh.mp3')), 23.7, 0.45)
tick = norm(load('tick.mp3'))
for k in range(1, 10):
    t = OFF + k * (ON - OFF) / 10
    place(sfx, tick, t, 0.18 if k < 7 else 0.34)
place(sfx, norm(load('on_slam.mp3')), ON - 0.18, 0.55)
place(sfx, norm(load('splash.mp3')), ON + 0.05, 0.75)
place(sfx, norm(load('drips_laugh.mp3')), 31.0, 0.40)
place(sfx, norm(load('space_hum.mp3')), 35.5, 0.28, length=DUR - 35.5, fi=0.4, fo=1.0)

ma = norm(load(sys.argv[1] if len(sys.argv) > 1 else 'music_a.mp3'))
place(mus, ma, 0.0, 0.42, length=ON - 0.02, fo=0.03)
mb = norm(load(sys.argv[2] if len(sys.argv) > 2 else 'music_b.mp3'))
place(mus, mb, 31.2, 0.40, length=DUR - 31.2, fi=0.8, fo=1.5)

mix = sfx + mus
mix[-int(0.4 * SR):] *= np.linspace(1, 0, int(0.4 * SR))[:, None]
mix = norm(mix, 0.89)
with wave.open('mix.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(44)))
