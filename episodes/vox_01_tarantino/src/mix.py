"""Mix narration + ElevenLabs SFX + music for explained no. 01 (Tarantino) on the 54.5 s timeline."""
import subprocess, wave
import numpy as np

SR = 48000
DUR = 54.5
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

S = {k: load(k + '.mp3') for k in ['vhs_insert', 'rewind', 'register', 'bell', 'applause', 'projector', 'static', 'tapes_pile', 'swoosh', 'pop', 'neon']}
S['rewind'] *= 1.0; S['static'] *= 1.0; S['bell'] *= 1.0   # already peak-normalised by load()
# hook + counter
place(sfx, S['vhs_insert'], 0.0, 0.30, fi=0.0)
place(sfx, S['swoosh'], 3.4, 0.30)
place(sfx, S['static'], 3.7, 0.22, fo=0.3)
place(sfx, S['pop'], 4.25, 0.40)
for i in range(5):
    place(sfx, S['pop'], 5.5 + i * .14, 0.16)
place(sfx, S['swoosh'], 6.95, 0.28)
place(sfx, S['pop'], 8.18, 0.38)
# talking movies
place(sfx, S['swoosh'], 10.2, 0.30)
for i in range(6):
    place(sfx, S['pop'], 11.75 + i * .27, 0.22)
place(sfx, S['bell'], 14.6, 0.40)
# quote
place(sfx, S['swoosh'], 16.2, 0.28)
place(sfx, S['register'], 19.72, 0.40)
# timeline
place(sfx, S['swoosh'], 20.8, 0.28)
place(sfx, S['projector'], 20.9, 0.12, length=7.7, fi=0.6, fo=0.6)
for t in (21.55, 23.4, 26.25):
    place(sfx, S['pop'], t, 0.28)
place(sfx, S['applause'], 24.55, 0.26, fo=0.8)
# tapes
place(sfx, S['swoosh'], 28.55, 0.28)
place(sfx, S['bell'], 29.3, 0.30)
place(sfx, S['tapes_pile'], 30.8, 0.45)
place(sfx, S['tapes_pile'], 31.55, 0.30)
place(sfx, S['rewind'], 33.5, 0.30, length=1.1, fo=0.25)
place(sfx, S['register'], 34.55, 0.28)
# twist + cinemas
place(sfx, S['swoosh'], 36.1, 0.28)
for t in (36.38, 36.52, 36.77, 36.86):
    place(sfx, S['pop'], t, 0.26)
place(sfx, S['swoosh'], 37.55, 0.30)
place(sfx, S['neon'], 37.9, 0.30)
place(sfx, S['pop'], 39.75, 0.32)
place(sfx, S['swoosh'], 41.7, 0.28)
place(sfx, S['swoosh'], 43.0, 0.28)
# film only
place(sfx, S['projector'], 44.0, 0.26, length=3.9, fi=0.3, fo=0.5)
place(sfx, S['pop'], 45.3, 0.34)
place(sfx, S['pop'], 46.85, 0.34)
# marquee
place(sfx, S['swoosh'], 47.75, 0.28)
place(sfx, S['neon'], 48.0, 0.26)
place(sfx, S['vhs_insert'], 48.6, 0.24)
place(sfx, S['projector'], 50.1, 0.22, length=1.6, fi=0.1, fo=0.6)
place(sfx, S['swoosh'], 51.3, 0.24)

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
base = np.interp(tt, [0, 36.15, 36.3, 37.5, 37.9, 51.0, 51.4, DUR], [1, 1, .35, .35, 1, 1, 2.6, 2.6])
mus *= (0.40 * base * (1 - 0.55 * speaking))[:, None].astype(np.float32)

mix = vox + 1.3 * sfx + mus
mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
with wave.open('mix.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('vox', vox), ('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(54)))
