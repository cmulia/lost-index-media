#!/usr/bin/env python3
"""Render a @lost_index episode.

    python3 pipeline/render.py episodes/006_speakers            # full render
    python3 pipeline/render.py episodes/006_speakers --stills 3,12.5,40   # preview stills
    python3 pipeline/render.py episodes/006_speakers --audio-only

Episode folder layout:
    script.json            beats, captions, assets, captions for posts (see episodes/BRIEF.md)
    music.json             score spec for lostindex.music.compose (ignored if audio/music.* exists)
    sfx.json               [{"beat": i, "file": "audio/sfx/x.mp3", "offset": 0.0, "gain": 0.45}]
    diagrams.py            optional: DIAGRAMS = {"name": fn(img, draw, p, t, pal, beat)}
    assets/<key>.jpg       fetched source images
    audio/narration.mp3    chosen ElevenLabs take
"""
import argparse
import glob
import importlib.util
import json
import os
import subprocess
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lostindex import align as AL          # noqa: E402
from lostindex import audio as AU          # noqa: E402
from lostindex import frames as FR         # noqa: E402
from lostindex import music as MU          # noqa: E402
from lostindex import style as S           # noqa: E402

_TL = None


def load_diagrams(ep):
    p = os.path.join(ep, "diagrams.py")
    if not os.path.exists(p):
        return {}
    spec = importlib.util.spec_from_file_location("ep_diagrams", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "DIAGRAMS", {})


def build_timeline(ep, refresh_timing=True):
    script = json.load(open(os.path.join(ep, "script.json")))
    for b in script["beats"]:
        b["caption"] = AL.clean(b.get("caption") or b["text"])
        if not b.get("keep_case"):
            b["caption"] = b["caption"].lower()
    tpath = os.path.join(ep, "timing.json")
    narr = os.path.join(ep, "audio", "narration.mp3")
    if refresh_timing or not os.path.exists(tpath):
        timing = AL.align(script, narr)
        ov = os.path.join(ep, "timing_overrides.json")
        if os.path.exists(ov):
            for k, v in json.load(open(ov)).items():
                timing["beats"][int(k)].update(v)
        json.dump(timing, open(tpath, "w"), indent=1)
    timing = json.load(open(tpath))
    return script, timing, FR.Timeline(script, timing, ep, load_diagrams(ep))


def _init(ep):
    global _TL
    _, _, _TL = build_timeline(ep, refresh_timing=False)


def _frame(t):
    return FR.render_frame(_TL, t).tobytes()


def make_audio(ep, script, timing):
    os.makedirs(os.path.join(ep, "audio"), exist_ok=True)
    dur = timing["duration"]
    music_files = sorted(glob.glob(os.path.join(ep, "audio", "music.*")))
    if music_files:
        music = AU.carry_score(AU.decode(music_files[0]), dur)
        mj = os.path.join(ep, "music.json")
        level = json.load(open(mj)).get("file_level", 0.20) if os.path.exists(mj) else 0.20
    else:
        spec = json.load(open(os.path.join(ep, "music.json")))
        if "swell_beat" in spec:
            spec["swell_at"] = timing["beats"][spec["swell_beat"]]["start"]
        music = MU.compose(spec, dur, seed=int(script["file_no"]))
        AU.write_wav(os.path.join(ep, "audio", "score_composed.wav"), music)
        level = spec.get("level", 0.20)
    sfx = []
    sp = os.path.join(ep, "sfx.json")
    if os.path.exists(sp):
        for it in json.load(open(sp)):
            b = timing["beats"][it["beat"]]
            base = b["start"] if it.get("anchor", "start") == "start" else b.get("big_time", b["start"])
            sfx.append({"path": os.path.join(ep, it["file"]), "t": max(0.0, base + it.get("offset", 0.0)),
                        "gain": it.get("gain", 0.45), "max_len": it.get("max_len"), "fade_out": it.get("fade_out")})
    out = os.path.join(ep, "audio", "mix.wav")
    AU.mix(os.path.join(ep, "audio", "narration.mp3"), music, sfx, dur, timing["lead_in"], out,
           music_level=level, end_card_start=timing["end_card_start"])
    return out


def render_video(ep, script, timing, mix_path, workers=4):
    os.makedirs(os.path.join(ep, "render"), exist_ok=True)
    out = os.path.join(ep, "render", f"lost_index_{script['file_no']}_{script['slug']}.mp4")
    nframes = int(round(timing["duration"] * S.FPS))
    times = [i / S.FPS for i in range(nframes)]
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{S.W}x{S.H}",
           "-r", str(S.FPS), "-i", "-", "-i", mix_path, "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-maxrate", "4500k", "-bufsize", "9000k",
           "-pix_fmt", "yuv420p",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", out]
    ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    with Pool(workers, initializer=_init, initargs=(ep,)) as pool:
        for i, fb in enumerate(pool.imap(_frame, times, chunksize=8)):
            ff.stdin.write(fb)
            if i % 300 == 0:
                print(f"  frame {i}/{nframes}  {time.time() - t0:.0f}s", flush=True)
    ff.stdin.close()
    ff.wait()
    return out


def contact_sheet(video, out_png, every=5):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf",
                    f"fps=1/{every},scale=270:480,tile=8x2", "-frames:v", "1", out_png], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ep")
    ap.add_argument("--stills", default=None)
    ap.add_argument("--audio-only", action="store_true")
    ap.add_argument("--keep-timing", action="store_true")
    ap.add_argument("--remux", action="store_true", help="rebuild audio only and swap it into the existing render")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    ep = a.ep.rstrip("/")
    script, timing, tl = build_timeline(ep, refresh_timing=not a.keep_timing)
    if a.stills:
        os.makedirs(os.path.join(ep, "preview"), exist_ok=True)
        for s in a.stills.split(","):
            t = float(s)
            FR.render_frame(tl, t).save(os.path.join(ep, "preview", f"still_{t:06.2f}.png"))
        print("stills written")
        return
    mix = make_audio(ep, script, timing)
    I, TP = AU.measure(mix)
    print(f"mix: {I:.1f} LUFS, {TP:.1f} dBTP, duration {timing['duration']:.1f}s")
    if a.audio_only:
        return
    if a.remux:
        # keep the rendered frames, swap in the new mix
        out = os.path.join(ep, "render", f"lost_index_{script['file_no']}_{script['slug']}.mp4")
        tmp = out + ".remux.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-i", mix, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
                        "-shortest", tmp], check=True)
        os.replace(tmp, out)
        print("remuxed", out)
        return
    out = render_video(ep, script, timing, mix, a.workers)
    contact_sheet(out, os.path.join(ep, "render", "contact_sheet.png"))
    print("wrote", out)


if __name__ == "__main__":
    main()
