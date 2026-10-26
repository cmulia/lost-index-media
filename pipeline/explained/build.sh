#!/bin/bash
# usage: build.sh <slug> <port> stills "t1,t2,..."   |  build.sh <slug> <port> prep   |  build.sh <slug> <port> video <dur>
set -e
SLUG=$1; PORT=$2; MODE=$3; ARG=$4
REPO=/home/claude/lost-index-media; EP=$REPO/episodes/$SLUG
SC=${EXPLAINED_SCRATCH:-/tmp/explained_build}/$SLUG
TOOLS=$REPO/pipeline/explained/tools.py
mkdir -p $SC/stills
if [ "$MODE" = prep ]; then
  python3 -I $TOOLS stage $EP $SC
  python3 -I $TOOLS frames $EP $SC
  cp $EP/src/caps.json $SC/caps.json
fi
# inject caps + port
python3 - "$EP" "$SC" "$PORT" <<'EOF'
import sys, json, re
ep, sc, port = sys.argv[1:4]
html = open(f'{ep}/src/scene.html').read()
caps = open(f'{ep}/src/caps.json').read().strip()
html = re.sub(r'const CAPS = /\*CAPS\*/.*?;\n', 'const CAPS = /*CAPS*/' + caps + ';\n', html, count=1, flags=re.S)
open(f'{sc}/scene.html', 'w').write(html)
r = open('/home/claude/lost-index-media/episodes/vox_02_bong/src/render.mjs').read().replace('127.0.0.1:8770', f'127.0.0.1:{port}')
open(f'{sc}/render.mjs', 'w').write(r)
EOF
cd $SC
if ! curl -s -o /dev/null http://127.0.0.1:$PORT/scene.html; then (python3 -m http.server $PORT --bind 127.0.0.1 > http.log 2>&1 &) ; sleep 1; fi
if [ "$MODE" = stills ]; then
  rm -f stills/*.png; node render.mjs stills "$ARG" 2>&1 | grep -v "^still" | head -20
  python3 - <<'EOF'
from PIL import Image; import glob
fs = sorted(glob.glob('stills/s_*.png'), key=lambda p: float(p.split('s_')[1][:-4]))
ims = [Image.open(p).convert('RGB').resize((324, 576)) for p in fs]
cols = 5; rows = (len(ims) + cols - 1) // cols
sheet = Image.new('RGB', (324 * cols, 576 * rows), 'white')
for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 324, (i // cols) * 576))
sheet.save('stills_sheet.jpg', quality=88); print(len(fs), 'stills ->', 'stills_sheet.jpg')
EOF
elif [ "$MODE" = video ]; then
  DUR=$ARG; A=$(python3 -c "print(round($DUR/3,1))"); B=$(python3 -c "print(round(2*$DUR/3,1))")
  mkdir -p parts
  node render.mjs video 0 $A parts/p1.mp4 > parts/l1.txt 2>&1 &
  node render.mjs video $A $B parts/p2.mp4 > parts/l2.txt 2>&1 &
  node render.mjs video $B $DUR parts/p3.mp4 > parts/l3.txt 2>&1 &
  wait
  printf "file 'p1.mp4'\nfile 'p2.mp4'\nfile 'p3.mp4'\n" > parts/list.txt
  ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i parts/list.txt -c copy video.mp4
  grep -h -iE "pageerror|error" parts/l*.txt | head -5; ffprobe -v error -show_entries format=duration -of csv=p=0 video.mp4
  echo RENDER_DONE
fi
