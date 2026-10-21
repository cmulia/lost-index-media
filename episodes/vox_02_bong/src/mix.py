"""Mix narration + ElevenLabs SFX + music for explained no. 02 (Bong Joon Ho) on the 57.5 s timeline."""
import subprocess, wave
import numpy as np

SR = 48000
DUR = 57.5
N = int(DUR * SR)
A = 'audio/'
LEAD = 0.2   # narration starts here


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

S = {k: load(k + '.mp3') for k in ['rain', 'thunder', 'stairs', 'stone', 'doorbell', 'pencil', 'page', 'flash', 'applause', 'flood', 'switch', 'swoosh', 'tick']}
# hook: rain on the stairs
place(sfx, S['rain'], 0.0, 0.22, length=4.5, fi=0.0, fo=0.5)
place(sfx, S['thunder'], 0.0, 0.20, fi=0.0, fo=1.0)
# tutoring
place(sfx, S['page'], 4.35, 0.45)
place(sfx, S['tick'], 4.6, 0.25)
place(sfx, S['doorbell'], 6.9, 0.22)
place(sfx, S['tick'], 7.9, 0.25)
place(sfx, S['pencil'], 10.0, 0.40, length=0.7, fo=0.2)
# the con
place(sfx, S['swoosh'], 10.85, 0.22)
for t in (12.75, 13.05, 13.7, 13.9, 14.1, 14.3, 14.5):
    place(sfx, S['tick'], t, 0.20)
# peeping -> the set
place(sfx, S['swoosh'], 15.2, 0.22)
place(sfx, S['stairs'], 15.4, 0.14, fi=0.3, fo=0.6)
place(sfx, S['swoosh'], 18.4, 0.28)
place(sfx, S['stone'], 19.95, 0.45)
place(sfx, S['pencil'], 21.35, 0.30, length=1.4, fo=0.3)
# Palme, Globes
place(sfx, S['swoosh'], 23.45, 0.22)
place(sfx, S['flash'], 24.45, 0.40, fo=0.6)
place(sfx, S['applause'], 24.7, 0.16, fi=0.3, fo=1.2)
place(sfx, S['swoosh'], 27.25, 0.22)
place(sfx, S['tick'], 30.1, 0.25)
# Oscars
place(sfx, S['page'], 32.65, 0.45)
place(sfx, S['applause'], 33.3, 0.22, fi=0.2, fo=1.2)
for i in range(4):
    place(sfx, S['tick'], 33.85 + i * .22, 0.22)
# the film's flood
place(sfx, S['rain'], 38.35, 0.30, length=8.4, fi=0.4, fo=0.4)
place(sfx, S['thunder'], 38.45, 0.24, fo=0.8)
# the real flood
place(sfx, S['flood'], 44.2, 0.30, length=2.6, fi=0.3, fo=0.8)
# half underground
place(sfx, S['rain'], 48.0, 0.12, length=6.6, fi=1.0, fo=1.0)
place(sfx, S['switch'], 49.0, 0.6, length=1.6, fo=0.3)
place(sfx, S['stone'], 55.4, 0.30)

# music: ducked under the voice, dipped for the twist
m = load('music.mp3')
place(mus, m, 0.0, 1.0, length=DUR, fi=0.0, fo=2.0)
def movavg(x, n):
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n)]))
    return (c[n:n + len(x)] - c[:len(x)]) / n


env = np.sqrt(movavg(vox[:, 0].astype(np.float64) ** 2, int(.25 * SR)))
speaking = np.clip(env / 0.05, 0, 1)
speaking = movavg(speaking, int(.15 * SR))
tt = np.arange(N) / SR
base = np.interp(tt, [0, 46.4, 46.9, 47.9, 48.7, 54.4, 54.9, DUR], [1, 1, 0, 0, 1, 1, 2.2, 2.2])
mus *= (0.40 * base * (1 - 0.55 * speaking))[:, None].astype(np.float32)

mix = vox + 1.3 * sfx + mus
mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
with wave.open('mix.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('vox', vox), ('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(57)))
