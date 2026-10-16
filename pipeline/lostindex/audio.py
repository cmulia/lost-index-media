"""Mix narration + score + sound effects, duck the score under the voice, loudness-normalise."""
import json
import re
import subprocess

import numpy as np

SR = 48000


def decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def write_wav(path, x):
    x = np.clip(x, -1, 1).astype(np.float32)
    p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                        "-c:a", "pcm_s24le", path], input=x.tobytes(), check=True)
    return p


def moving_avg(x, win):
    win = max(1, int(win))
    c = np.cumsum(np.concatenate([[0.0], x]))
    out = (c[win:] - c[:-win]) / win
    pad = np.full(win - 1, out[-1] if len(out) else 0)
    return np.concatenate([out, pad])


def rms(x):
    return float(np.sqrt(np.mean(x ** 2)) + 1e-12)


def carry_score(m, duration, drop_db=12.0, xfade=3.0, min_tail=2.0):
    """Generated scores often fade out early. If the track goes quiet more than `min_tail`
    seconds before the video ends, loop back over an earlier loud stretch of the same track
    with equal-power crossfades so the bed carries to the end card, then fade out."""
    win = SR
    nwin = m.shape[0] // win
    if nwin < 20:
        return m
    lev = np.array([20 * np.log10(rms(m[i * win:(i + 1) * win]) + 1e-9) for i in range(nwin)])
    ref = np.median(lev[: int(nwin * 0.6)])
    loud = np.where(lev > ref - drop_db)[0]
    if not len(loud):
        return m
    t_end = (loud[-1] + 1)
    if duration - t_end <= min_tail:
        return m
    a = max(5, t_end - 40)
    seg = m[a * SR:t_end * SR]
    out = m[:t_end * SR].copy()
    xf = int(xfade * SR)
    ramp = np.linspace(0, np.pi / 2, xf)[:, None]
    while out.shape[0] < int((duration + 1) * SR):
        head = out[-xf:] * np.cos(ramp) + seg[:xf] * np.sin(ramp)
        out = np.concatenate([out[:-xf], head, seg[xf:]])
    out = out[: int((duration + 1) * SR)]
    f = int(3.5 * SR)
    out[-f:] *= np.linspace(1, 0, f)[:, None] ** 1.5
    return out


def mix(narration_path, music, sfx, duration, lead_in, out_path, music_level=0.20, duck_depth=0.55,
        end_card_start=None):
    n = int(duration * SR)
    out = np.zeros((n, 2), np.float32)
    v = decode(narration_path)
    v *= 0.89 / (np.max(np.abs(v)) + 1e-9)
    i0 = int(lead_in * SR)
    vv = np.zeros((n, 2), np.float32)
    vv[i0:i0 + v.shape[0]] = v[: max(0, n - i0)]
    speech = vv[np.abs(vv[:, 0]) > 0.02]
    v_rms = rms(speech) if speech.size else 0.1

    # score, ducked under the voice
    m = np.zeros((n, 2), np.float32)
    mm = music[:n]
    m[: mm.shape[0]] = mm
    m *= music_level * v_rms / (rms(m[m[:, 0] != 0]) if np.any(m) else 1)
    env = moving_avg(np.abs(vv[:, 0]), 0.20 * SR)
    active = np.clip(env / (v_rms * 0.35), 0, 1)
    active = moving_avg(active, 0.45 * SR)
    gain = 1 - duck_depth * active
    if end_card_start:
        k = int(end_card_start * SR)
        ramp = np.clip((np.arange(n) - k) / (0.8 * SR), 0, 1)
        gain = gain * (1 + 0.6 * ramp)
    m *= gain[:, None].astype(np.float32)

    out += vv + m
    for item in sfx:
        s = decode(item["path"])
        s *= item.get("gain", 0.45) / (np.max(np.abs(s)) + 1e-9)
        if item.get("fade_out"):
            fo = int(item["fade_out"] * SR)
            if fo < s.shape[0]:
                s[-fo:] *= np.linspace(1, 0, fo)[:, None]
        if item.get("max_len"):
            ml = int(item["max_len"] * SR)
            if s.shape[0] > ml:
                s = s[:ml]
                f = min(int(0.4 * SR), ml)
                s[-f:] *= np.linspace(1, 0, f)[:, None]
        j = int(item["t"] * SR)
        if j < n:
            k = min(n, j + s.shape[0])
            out[j:k] += s[: k - j]
    # tail fade
    f = int(0.6 * SR)
    out[-f:] *= np.linspace(1, 0, f)[:, None]
    tmp = out_path + ".pre.wav"
    write_wav(tmp, out * 0.7)
    loudnorm(tmp, out_path)
    return out_path


def loudnorm(src, dst, I=-16.0, TP=-2.0, LRA=11.0):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", src, "-af",
                        f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    js = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p.stderr, re.S).group(0))
    af = (f"loudnorm=I={I}:TP={TP}:LRA={LRA}:measured_I={js['input_i']}:measured_TP={js['input_tp']}:"
          f"measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}:offset={js['target_offset']}:"
          f"linear=true,alimiter=limit={10 ** (TP / 20):.4f}:level=disabled")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", af, "-ar", str(SR), "-c:a", "pcm_s24le", dst],
                   check=True)


def measure(path):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
                        "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p.stderr, re.S).group(0))
    return float(js["input_i"]), float(js["input_tp"])
