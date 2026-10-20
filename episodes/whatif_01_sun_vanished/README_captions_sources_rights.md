# what if no. 01 · What if the Sun vanished?

A new silent "what if" format for @lost_index: a 55 s low-poly 3D simulation (1080×1920, 30 fps) with on-screen
stats and captions, music and sound effects, and **no narration**. It's fiction built on real numbers. Ends with the real fact.

Scheduled 23 Oct 2026, 10:00 Australia/Sydney, on TikTok, Instagram (reel) and YouTube Shorts.

## Story (beats)

| t (s) | shot | on screen |
|---|---|---|
| 0–5.6 | Bondi Beach, wide | LOCATION · Bondi Beach, Sydney · a summer afternoon · 26°C — *Just another afternoon at Bondi.* |
| 5.6–9.6 | tilt up to the Sun | DISTANCE TO THE SUN · 149.6 million km · light takes 8 min 20 s — *At 2:00 pm, the Sun vanishes.* |
| 9.6–16 | space: the Sun blinks out, a shell of last light heads for Earth | THE SUN · Gone — *But its last light is still on the way.* |
| 16–28 | beach, clock 00:00 → 08:20 | TIME SINCE THE SUN VANISHED — *Nobody notices. / Not yet.* |
| 28 | instant blackout, stars | 08:20 — *8 minutes, 20 seconds later.* |
| 29.3 | the Moon goes out | THE MOON · Gone too — *1.3 seconds after that, the Moon goes out too.* |
| 33–37.5 | phone torches | AIR TEMPERATURE — *Phones become the only light.* |
| 37.5–43.5 | one week later: ice, bonfire | ONE WEEK LATER · −18°C — *A week later, Bondi is frozen.* |
| 43.5–49 | space: Earth leaves its orbit in a straight line | EARTH'S ORBIT · None · 107,000 km/h — *And Earth drifts off into the dark.* |
| 49–55 | back to the sunny beach | *This is fiction. But the sunlight on your skin right now left the Sun 8 minutes 20 seconds ago.* |

Easter egg: a man in a yellow bucket hat and a red-and-white striped shirt sits in a deck chair eating an ice cream
in every beach shot, including the blackout and the frozen week ("Did you spot him? 👀").

## Facts used

- Mean Earth–Sun distance ≈ 149.6 million km; sunlight takes ≈ 499 s (8 min 19–20 s) to arrive.
- Changes in gravity also travel at the speed of light (confirmed by GW170817), so Earth keeps orbiting for the same 8 min 20 s.
- Moonlight is reflected sunlight; the Moon is ≈ 384,400 km ≈ 1.3 light-seconds away. With a near-quarter afternoon Moon,
  its last light reaches us ≈ 1.3 s after the Sun's.
- Earth's mean orbital speed ≈ 29.8 km/s ≈ 107,000 km/h; without the Sun it continues in a straight line.
- Temperature: estimates say the average surface would fall below 0 °F (−18 °C) within about a week and to about −100 °F
  (≈ −73 °C) within a year. David Stevenson, Caltech ("If the Sun ceased to exist…", Caltech Question of the Month);
  Wonderopolis. Labelled "estimated" on screen.

## Rights

- 3D animation, models and layout: made for this video (three.js r169, MIT), rendered headless. Space shots are
  labelled "Illustration · not to scale".
- Fonts: Instrument Serif (SIL OFL, `pipeline/fonts`).
- Music and all sound effects: synthesised for this video (`src/audio.py`, using `pipeline/lostindex/music.py`).
  ElevenLabs was tried first but the workspace had no credits left this month, and no generation was charged.
- No third-party images or recordings.

## Rebuild

```
cd src && npm i three@0.169.0 && python3 -m http.server 8765 &   # serve scene.html (needs fonts next to it)
node render.mjs stills 2,12,30,40,52          # check frames
./runall.sh                                    # 4 parallel chunks -> parts/p1..p4.mp4
python3 audio.py mix.wav                       # score + SFX
# concat parts, mux with mix.wav, loudnorm to -16 LUFS / -2 dBTP
```

## Post captions

See `captions.json`.
