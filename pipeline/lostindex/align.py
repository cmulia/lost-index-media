"""Beat timing from the narration take.

Preferred: word-level forced alignment of the known script against the take with
pocketsphinx (pip install pocketsphinx; its English model ships inside the wheel). Beats then
start on their first spoken word and captions type out word by word with the voice.
Fallback when pocketsphinx is missing or the alignment fails: beats are placed by character
share of the spoken text and snapped to the nearest pause found by ffmpeg silencedetect.
"""
import bisect
import json
import os
import re
import subprocess
import sys

TAG_RE = re.compile(r"\[[^\]]*\]")
WORD_RE = re.compile(r"[a-z0-9']+")


def clean(text):
    return re.sub(r"\s+", " ", TAG_RE.sub("", text)).strip()


def words_of(text):
    return WORD_RE.findall(clean(text).lower().replace("’", "'"))


# crude pronunciations for words missing from the CMU dictionary (names, acronyms)
_LETTER = {"a": "EY", "b": "B IY", "c": "S IY", "d": "D IY", "e": "IY", "f": "EH F", "g": "JH IY", "h": "EY CH",
           "i": "AY", "j": "JH EY", "k": "K EY", "l": "EH L", "m": "EH M", "n": "EH N", "o": "OW", "p": "P IY",
           "q": "K Y UW", "r": "AA R", "s": "EH S", "t": "T IY", "u": "Y UW", "v": "V IY",
           "w": "D AH B AH L Y UW", "x": "EH K S", "y": "W AY", "z": "Z IY"}
_L2P = {"a": "AE", "b": "B", "c": "K", "d": "D", "e": "EH", "f": "F", "g": "G", "h": "HH", "i": "IH", "j": "JH",
        "k": "K", "l": "L", "m": "M", "n": "N", "o": "AA", "p": "P", "q": "K", "r": "R", "s": "S", "t": "T",
        "u": "AH", "v": "V", "w": "W", "x": "K S", "y": "Y", "z": "Z"}
_DIGIT = {"0": "Z IY R OW", "1": "W AH N", "2": "T UW", "3": "TH R IY", "4": "F AO R", "5": "F AY V",
          "6": "S IH K S", "7": "S EH V AH N", "8": "EY T", "9": "N AY N"}


def _guess_phones(w, prons):
    if w.endswith("'s") and w[:-2] in prons:
        return prons[w[:-2]] + " Z"
    if w.isdigit():
        return " ".join(_DIGIT[c] for c in w)
    if len(w) <= 4 and not re.search(r"[aeiouy]", w):
        return " ".join(_LETTER[c] for c in w if c in _LETTER)
    return " ".join(_L2P[c] for c in w if c in _L2P) or "AH"


def force_align(script, narration_path):
    """[(word, start, end)] in seconds for every spoken word of the narration, or None."""
    try:
        from pocketsphinx import Decoder, get_model_path
    except ImportError:
        print("align: pocketsphinx not installed, using pause-snapping fallback", file=sys.stderr)
        return None
    words = [w for b in script["beats"] for w in words_of(b["text"])]
    model = os.path.join(get_model_path(), "en-us")
    dic = os.path.join(model, "cmudict-en-us.dict")
    prons = {}
    for line in open(dic):
        parts = line.split()
        if parts and "(" not in parts[0]:
            prons[parts[0]] = " ".join(parts[1:])
    dec = Decoder(hmm=os.path.join(model, "en-us"), dict=dic, samprate=16000, loglevel="FATAL")
    for w in sorted({w for w in words if w not in prons}):
        dec.add_word(w, _guess_phones(w, prons), True)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", narration_path, "-f", "s16le", "-ac", "1", "-ar", "16000", "-"],
                         capture_output=True, check=True).stdout
    try:
        dec.set_align_text(" ".join(words))
        dec.start_utt()
        dec.process_raw(raw, full_utt=True)
        dec.end_utt()
        segs = [(re.sub(r"\(\d+\)$", "", s.word), s.start_frame / 100, (s.end_frame + 1) / 100) for s in dec.seg()]
    except Exception as e:  # noqa: BLE001
        print(f"align: forced alignment failed ({e}), using fallback", file=sys.stderr)
        return None
    segs = [s for s in segs if s[0] not in ("<s>", "</s>", "<sil>") and not s[0].startswith(("[", "+"))]
    if [s[0] for s in segs] != words:
        print(f"align: aligned {len(segs)} of {len(words)} words, using fallback", file=sys.stderr)
        return None
    return segs


def _progress_knots(beat_words):
    """[(time, fraction of the beat's spoken text done)] for word-synced caption typing."""
    total = sum(len(w) + 1 for w, _, _ in beat_words) or 1
    knots, done = [], 0
    for w, s, e in beat_words:
        knots.append((round(s, 3), round(done / total, 4)))
        done += len(w) + 1
        knots.append((round(e, 3), round(done / total, 4)))
    return knots


def progress_at(knots, t):
    """Caption fraction (0..1) at absolute time t, interpolated between word knots."""
    if not knots or t <= knots[0][0]:
        return 0.0
    if t >= knots[-1][0]:
        return 1.0
    i = bisect.bisect_right([k[0] for k in knots], t)
    (t0, f0), (t1, f1) = knots[i - 1], knots[i]
    return f0 if t1 <= t0 else f0 + (f1 - f0) * (t - t0) / (t1 - t0)


def _time_at(knots, frac):
    for (t0, f0), (t1, f1) in zip(knots, knots[1:]):
        if f1 >= frac:
            return t0 if f1 <= f0 else t0 + (t1 - t0) * (frac - f0) / (f1 - f0)
    return knots[-1][0]


def align_words(script, segs, dur, lead_in, end_card):
    out, i = [], 0
    per_beat = []
    for b in script["beats"]:
        n = len(words_of(b["text"]))
        per_beat.append(segs[i:i + n])
        i += n
    for k, (b, bw) in enumerate(zip(script["beats"], per_beat)):
        first = bw[0][1]
        prev_end = per_beat[k - 1][-1][2] if k else 0.0
        start = 0.0 if k == 0 else lead_in + max(prev_end, first - 0.12)
        item = {"start": round(start, 3), "speech_end": round(lead_in + bw[-1][2], 3)}
        knots = [(round(lead_in + t, 3), f) for t, f in _progress_knots(bw)]
        item["progress"] = knots
        big = (b.get("big") or "").strip()
        if big:
            token = re.sub(r"[^\w']", " ", big.lower()).split()
            cap = (b.get("caption") or clean(b["text"])).lower()
            pos = cap.find(token[0]) if token else -1
            if pos >= 0:
                item["big_time"] = round(_time_at(knots, pos / max(1, len(cap))), 3)
            else:
                item["big_time"] = round(lead_in + first + 0.15 * (bw[-1][2] - first), 3)
        out.append(item)
    for k, item in enumerate(out):
        item["end"] = out[k + 1]["start"] if k + 1 < len(out) else round(lead_in + dur + 0.25, 3)
    return {"narration_duration": dur, "lead_in": lead_in, "beats": out, "aligned": "pocketsphinx",
            "end_card_start": round(lead_in + dur + 0.25, 3), "duration": round(lead_in + dur + 0.25 + end_card, 3)}


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
    segs = force_align(script, narration_path)
    if segs:
        return align_words(script, segs, dur, lead_in, end_card)
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
