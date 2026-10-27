#!/bin/bash
cd "$(dirname "$0")"; mkdir -p parts
node render.mjs video 0 17.0 parts/p1.mp4 > parts/l1.txt 2>&1 &
node render.mjs video 17.0 34.0 parts/p2.mp4 > parts/l2.txt 2>&1 &
node render.mjs video 34.0 51.0 parts/p3.mp4 > parts/l3.txt 2>&1 &
wait
printf "file 'p1.mp4'\nfile 'p2.mp4'\nfile 'p3.mp4'\n" > parts/list.txt
ffmpeg -nostdin -y -loglevel error -f concat -safe 0 -i parts/list.txt -c copy video.mp4
echo done
