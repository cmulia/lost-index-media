"""Beat timing from the narration take.

No forced aligner is available offline, so beats are placed by character share of the
spoken text and then snapped to the nearest pause found by ffmpeg silencedetect.
"""
import json
import re
import subprocess

TAG_RE = re.compile(r"\[[^\]]*\]")


def clean(text):
    return re.sub(r"\s+", " ", TAG_RE.sub("", text)).strip()


def audio_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def silences(path, noise_db=-36, min_d=0.16):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
                        f"silencedetect=noise={noise_db}dB:d={min_d}", "-f", "null", "-"],
                       capture_output=True, text=True)
    starts, out = [], []
    for line in p.stderr.splitlines():
        m = re.search(r"silence_start: ([\d.]+)", line)
        if m:
            starts.append(float(m.group(1)))
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m and starts:
            out.append((starts.pop(), float(m.group(1))))
    return out


def weight(text):
    # spoken weight: characters, with punctuation pauses
    t = clean(text)
    w = len(t)
    w += 6 * len(re.findall(r"[.!?…]", t)) + 3 * len(re.findall(r"[,;:—–]", t))
    return max(w, 1)


def align(script, narration_path, lead_in=0.15, end_card=2.0):
    dur = audio_duration(narration_path)
    sil = silences(narration_path)
    speech_start = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
    speech_end = dur
    if sil and sil[-1][1] >= dur - 0.05:
        speech_end = sil[-1][0]
    beats = script["beats"]
    ws = [weight(b["text"]) for b in beats]
    total = sum(ws)
    span = speech_end - speech_start
    bounds = [speech_start]
    acc = 0
    used = set()
    for i, w in enumerate(ws[:-1]):
        acc += w
        est = speech_start + span * acc / total
        best, bd = None, 1.4
        for j, (s0, s1) in enumerate(sil):
            if j in used or s1 <= bounds[-1] + 0.4:
                continue
            mid = (s0 + s1) / 2
            if abs(mid - est) < bd:
                best, bd = j, abs(mid - est)
        if best is not None:
            used.add(best)
            s0, s1 = sil[best]
            bounds.append(min(s1, s0 + 0.32))
        else:
            bounds.append(max(est, bounds[-1] + 0.5))
    bounds.append(speech_end)

    out = []
    for i, b in enumerate(beats):
        a_start = bounds[i]
        a_end = bounds[i + 1]
        # speech end inside the beat = start of last pause before next beat
        se = a_end
        for s0, s1 in sil:
            if a_start + 0.3 < s0 < a_end and s1 >= a_end - 0.05:
                se = s0
        start = lead_in + a_start if i > 0 else 0.0
        end = lead_in + a_end if i < len(beats) - 1 else lead_in + dur + 0.25
        item = {"start": round(start, 3), "end": round(end, 3), "speech_end": round(lead_in + se, 3)}
        big = b.get("big")
        if big:
            txt = clean(b["text"]).lower()
            k = txt.find(big.lower().strip(".").split()[0]) if big.strip() else -1
            frac = (k / max(1, len(txt))) if k >= 0 else 0.15
            item["big_time"] = round(lead_in + a_start + (se - a_start) * frac, 3)
        out.append(item)
    total_dur = lead_in + dur + 0.25 + end_card
    return {"narration_duration": dur, "lead_in": lead_in, "beats": out,
            "end_card_start": round(lead_in + dur + 0.25, 3), "duration": round(total_dur, 3)}


if __name__ == "__main__":
    import sys
    sc = json.load(open(sys.argv[1]))
    print(json.dumps(align(sc, sys.argv[2]), indent=1))
