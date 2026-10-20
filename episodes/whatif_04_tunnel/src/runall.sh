#!/bin/bash
cd "$(dirname "$0")"; mkdir -p parts
node render.mjs video 0 25 parts/p1.mp4 > parts/l1.txt 2>&1 &
node render.mjs video 25 50 parts/p2.mp4 > parts/l2.txt 2>&1 &
wait; echo done
