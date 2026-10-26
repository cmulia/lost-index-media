#!/usr/bin/env python3
"""Force-align narration takes and build caps.json.

  caps_build.py align <narration.txt> <take.mp3> [<take2.mp3> ...]   -> prints duration + alignment status per take, writes <take>.words.json
  caps_build.py caps  <narration.txt> <lines.txt> <take.words.json> <out caps.json> [lead=0.2]
lines.txt: one caption line per line; joined with single spaces they must equal the narration exactly.
"""
import json, re, subprocess, sys
sys.path.insert(0, '/home/claude/lost-index-media/pipeline/lostindex')
import align  # noqa: E402

WORD_RE = align.WORD_RE


def dur(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True).stdout.strip())


def do_align(narr, takes):
    text = open(narr).read().strip()
    script = {'beats': [{'text': text}]}
    for t in takes:
        segs = align.force_align(script, t)
        d = dur(t)
        # pause stats
        gaps = []
        if segs:
            for a, b in zip(segs, segs[1:]):
                g = b[1] - a[2]
                if g > 0.25: gaps.append(round(g, 2))
            json.dump(segs, open(t + '.words.json', 'w'))
        print(f"{t}: {d:.2f}s aligned={'yes' if segs else 'NO'} words={len(segs) if segs else 0} speech_end={segs[-1][2] if segs else None} pauses>0.25s={len(gaps)} {gaps[:12]}")


def build_caps(narr, lines_path, words_path, out, lead=0.2):
    text = open(narr).read().strip()
    lines = [l.rstrip('\n') for l in open(lines_path) if l.strip()]
    assert ' '.join(lines) == text, 'lines do not join back to the narration'
    segs = json.load(open(words_path))
    caps, k = [], 0
    for line in lines:
        row = []
        for tok in line.split():
            n = len(WORD_RE.findall(tok.lower().replace('’', "'")))
            if n == 0:
                continue
            ws = segs[k:k + n]; k += n
            row.append([tok, round(ws[0][1] + lead, 2), round(ws[-1][2] + lead, 2)])
        caps.append(row)
    assert k == len(segs), f'consumed {k} of {len(segs)} words'
    json.dump(caps, open(out, 'w'), ensure_ascii=False)
    print('caps lines', len(caps), 'last word ends', caps[-1][-1][2])


if __name__ == '__main__':
    if sys.argv[1] == 'align': do_align(sys.argv[2], sys.argv[3:])
    else: build_caps(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], float(sys.argv[6]) if len(sys.argv) > 6 else 0.2)
