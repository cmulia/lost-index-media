#!/usr/bin/env python3
"""Shared helpers for the explained no. 03–07 builds.

  tools.py frames <episode_dir> <scratch_dir>        extract 121 JPEG frames per assets/clips/*.mp4 into <scratch>/img/<name>/fNNN.jpg
  tools.py stage  <episode_dir> <scratch_dir>        copy fonts + photos + pngs into <scratch>/{fonts,img}
  tools.py finish <scratch_dir> <episode_dir> <out_name> <dur>   loudnorm 2-pass + limiter + mux + contact sheet
  tools.py check  <mp4>                              report duration, size, bitrate, LUFS, true peak
"""
import glob, json, os, re, shutil, subprocess, sys

FONT_DIRS = ['/usr/share/fonts/opentype/inter', '/home/claude/lost-index-media/pipeline/fonts']
FONTS = ['InterDisplay-Black.otf', 'InterDisplay-ExtraBold.otf', 'InterDisplay-Bold.otf', 'InterDisplay-SemiBold.otf',
         'IBMPlexMono-Medium.ttf', 'IBMPlexMono-Regular.ttf', 'IBMPlexMono-Light.ttf', 'InstrumentSerif-Italic.ttf', 'InstrumentSerif-Regular.ttf']


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def frames(ep, sc):
    for clip in sorted(glob.glob(os.path.join(ep, 'assets/clips/*.mp4'))):
        name = os.path.splitext(os.path.basename(clip))[0]
        out = os.path.join(sc, 'img', name)
        os.makedirs(out, exist_ok=True)
        run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', clip, '-vf', 'fps=24,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
             '-frames:v', '121', '-q:v', '3', os.path.join(out, 'f%03d.jpg')])
        n = len(glob.glob(os.path.join(out, 'f*.jpg')))
        # pad to 121 if the clip was a hair short
        last = os.path.join(out, f'f{n:03d}.jpg')
        for i in range(n + 1, 122):
            shutil.copy(last, os.path.join(out, f'f{i:03d}.jpg'))
        print('frames', name, n)


def stage(ep, sc):
    os.makedirs(os.path.join(sc, 'fonts'), exist_ok=True)
    os.makedirs(os.path.join(sc, 'img'), exist_ok=True)
    for f in FONTS:
        for d in FONT_DIRS:
            p = os.path.join(d, f)
            if os.path.exists(p):
                shutil.copy(p, os.path.join(sc, 'fonts', f)); break
        else:
            print('missing font', f)
    for p in glob.glob(os.path.join(ep, 'assets/*.*')):
        if p.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            shutil.copy(p, os.path.join(sc, 'img', os.path.basename(p)))
    print('staged', sc)


def check(mp4):
    pr = json.loads(run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', mp4]).stdout)
    dur = float(pr['format']['duration']); size = int(pr['format']['size'])
    r = subprocess.run(['ffmpeg', '-nostdin', '-i', mp4, '-af', 'loudnorm=I=-16:TP=-2:print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
    m = re.search(r'\{[^{}]*"input_i"[^{}]*\}', r.stderr, re.S)
    ln = json.loads(m.group(0)) if m else {}
    v = [s for s in pr['streams'] if s['codec_type'] == 'video'][0]
    info = dict(duration=round(dur, 2), size_mb=round(size / 1e6, 1), kbps=round(size * 8 / dur / 1000), w=v['width'], h=v['height'], fps=v['r_frame_rate'],
                lufs=ln.get('input_i'), tp=ln.get('input_tp'))
    print(json.dumps(info)); return info


def finish(sc, ep, out_name, dur):
    mix = os.path.join(sc, 'mix.wav'); video = os.path.join(sc, 'video.mp4')
    r = subprocess.run(['ffmpeg', '-nostdin', '-i', mix, '-af', 'loudnorm=I=-16:TP=-2:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
    m = json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}', r.stderr, re.S).group(0))
    af = (f"loudnorm=I=-16:TP=-2:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=summary,alimiter=limit=0.70:level=false")
    norm = os.path.join(sc, 'mix_norm.wav')
    run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', mix, '-af', af, '-ar', '48000', norm])
    os.makedirs(os.path.join(ep, 'render'), exist_ok=True)
    out = os.path.join(ep, 'render', out_name)
    run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', video, '-i', norm, '-map', '0:v:0', '-map', '1:a:0', '-t', str(dur),
         '-c:v', 'libx264', '-preset', 'medium', '-b:v', '4500k', '-maxrate', '5200k', '-bufsize', '9000k', '-pix_fmt', 'yuv420p', '-r', '30',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out])
    info = check(out)
    # contact sheet: 12 frames, 4 x 3
    step = dur / 12
    run(['ffmpeg', '-nostdin', '-y', '-loglevel', 'error', '-i', out, '-vf', f"fps=1/{step:.4f},scale=360:640,tile=4x3", '-frames:v', '1', os.path.join(ep, 'render', 'contact_sheet.png')])
    print('wrote', out, 'and contact_sheet.png'); return info


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'frames': frames(sys.argv[2], sys.argv[3])
    elif cmd == 'stage': stage(sys.argv[2], sys.argv[3])
    elif cmd == 'finish': finish(sys.argv[2], sys.argv[3], sys.argv[4], float(sys.argv[5]))
    elif cmd == 'check': check(sys.argv[2])
