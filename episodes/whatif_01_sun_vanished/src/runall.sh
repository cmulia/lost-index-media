#!/bin/bash
cd "$(dirname "$0")"
node render.mjs video 0 14 parts/p1.mp4 > parts/l1.txt 2>&1 &
node render.mjs video 14 28 parts/p2.mp4 > parts/l2.txt 2>&1 &
node render.mjs video 28 42 parts/p3.mp4 > parts/l3.txt 2>&1 &
node render.mjs video 42 55 parts/p4.mp4 > parts/l4.txt 2>&1 &
wait
echo done
