"""Mix narration + SFX + music for explained no. 05 (Hitchcock) on the 57.0 s timeline.
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

S = {k: load('sfx/' + k + '.mp3') for k in ['stamp', 'pen', 'paper', 'coins', 'register', 'camera', 'shower', 'syrup', 'rope', 'tick', 'counter', 'applause', 'mic', 'swoosh']}
# hook: paper slide + pen
place(sfx, S['paper'], 0.05, 0.35, fi=0.0)
place(sfx, S['pen'], 1.2, 0.30)
# Paramount balked: memo, stamp
place(sfx, S['swoosh'], 3.05, 0.25)
place(sfx, S['paper'], 3.4, 0.35)
place(sfx, S['stamp'], 7.0, 0.55)
# the deal: cheque crossed out, coins, pie
place(sfx, S['swoosh'], 8.1, 0.25)
place(sfx, S['pen'], 9.1, 0.40)
place(sfx, S['coins'], 10.4, 0.35)
place(sfx, S['register'], 12.1, 0.35)
for t in (12.5, 12.8, 13.1, 13.4):
    place(sfx, S['tick'], t, 0.22)
# camera, checklist, ledger
place(sfx, S['swoosh'], 14.5, 0.25)
place(sfx, S['camera'], 14.6, 0.22, length=4.8, fi=0.2, fo=0.6)
for t in (14.7, 15.8, 16.8):
    place(sfx, S['tick'], t, 0.3)
place(sfx, S['counter'], 17.3, 0.40, fo=0.3)
# shower: water, shot grid clicks, syrup
place(sfx, S['swoosh'], 19.5, 0.25)
place(sfx, S['shower'], 19.6, 0.30, length=5.2, fi=0.3, fo=0.8)
for i in range(14):
    place(sfx, S['tick'], 21.3 + i * .11, 0.16)
place(sfx, S['syrup'], 23.3, 0.45)
# the rule: lobby, rope, sign, ticks
place(sfx, S['swoosh'], 24.9, 0.25)
place(sfx, S['rope'], 25.1, 0.40)
place(sfx, S['stamp'], 25.7, 0.25)
place(sfx, S['rope'], 28.7, 0.30)
for i in range(6):
    place(sfx, S['tick'], 30.8 + i * .5, 0.35)
# the money: counter, register
place(sfx, S['swoosh'], 32.2, 0.25)
place(sfx, S['counter'], 34.7, 0.45, length=2.0, fo=0.4)
place(sfx, S['register'], 36.6, 0.35)
place(sfx, S['coins'], 37.1, 0.30)
# nominations: cards + stamps
place(sfx, S['swoosh'], 40.0, 0.25)
for i in range(5):
    place(sfx, S['paper'], 41.0 + i * .32, 0.32)
for i in range(5):
    place(sfx, S['stamp'], 44.2 + i * .14, 0.30)
# 1968: applause, mic
place(sfx, S['swoosh'], 47.0, 0.25)
place(sfx, S['applause'], 47.1, 0.22, fi=0.3, fo=1.5)
place(sfx, S['mic'], 51.5, 0.28, fo=0.4)
place(sfx, S['applause'], 53.7, 0.16, fi=0.2, fo=1.8)
# end card
place(sfx, S['swoosh'], 54.0, 0.22)
place(sfx, S['paper'], 54.3, 0.3)

# music: ducked under the voice, out for "Thank you", back for the end card
m = load('music.mp3')
place(mus, m, 0.0, 1.0, length=DUR, fi=0.0, fo=2.0)


def movavg(x, n):
    c = np.cumsum(np.concatenate([np.zeros(n // 2 + 1), x, np.zeros(n)]))
    return (c[n:n + len(x)] - c[:len(x)]) / n


env = np.sqrt(movavg(vox[:, 0].astype(np.float64) ** 2, int(.25 * SR)))
speaking = np.clip(env / 0.05, 0, 1)
speaking = movavg(speaking, int(.15 * SR))
tt = np.arange(N) / SR
base = np.interp(tt, [0, 51.0, 51.8, 53.9, 54.3, DUR], [1, 1, 0.12, 0.12, 1.6, 1.6])
mus *= (0.38 * base * (1 - 0.55 * speaking))[:, None].astype(np.float32)

mix = vox + 1.3 * sfx + mus
mix[-int(0.5 * SR):] *= np.linspace(1, 0, int(0.5 * SR))[:, None]
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.89
with wave.open(OUT, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
for nm, a in (('vox', vox), ('sfx', sfx), ('mus', mus)):
    print(nm, ' '.join(f"{20*np.log10(np.sqrt((a[i*SR:(i+1)*SR]**2).mean())+1e-9):.0f}" for i in range(int(DUR))))
