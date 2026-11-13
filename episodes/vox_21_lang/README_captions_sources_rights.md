# explained no. 21 — Fritz Lang (vox_21_lang)

Posts Thu 26 Nov 2026 (Sydney): YouTube + Instagram 11:00, TikTok 13:00. Opening style C (name the object on screen, the scratched reel, and say why it shouldn't exist). Runtime 50.5 s.

**YouTube title:** The lost Metropolis footage found in Buenos Aires (2008) #shorts  
**Question (final spoken line + on screen):** Keep scratched footage, or hide the damage?  
**First comment (Instagram; pin on YouTube):** Keep it. The scratches show the film really survived, and I'd rather see honest damage than a smooth fake.

## Beats

0. This scratched little film reel holds footage everyone thought was gone.  _(sources: S2, S3)_
1. In nineteen twenty-seven, Fritz Lang premiered Metropolis at about two and a half hours.  _(sources: S4)_
2. Soon it was trimmed, and the cuts vanished.  _(sources: S3, S4)_
3. Even careful restorations were still missing about a quarter of the film.  _(sources: S1)_
4. In two thousand eight, a Buenos Aires curator pulled out reels until she found a scene nobody knew.  _(sources: S3)_
5. The story goes that a collector carried a print to Argentina in nineteen twenty-eight.  _(sources: S2, S4)_
6. More than twenty minutes came back, badly scratched.  _(sources: S3, S1)_
7. In twenty ten, a restoration premiered in Berlin, nearly whole again.  _(sources: S1, S4)_
8. It was never hidden. The museum had been on a distribution list since the nineteen twenties. Someone just had to ask.  _(sources: S3, S2)_
9. Keep scratched footage, or hide the damage?  _(sources: none)_

## Sources

- S1: Film Comment, "A Tale of Two Cities: Metropolis Restored", Chris Fujiwara, May-June 2010 — https://www.filmcomment.com/article/a-tale-of-two-cities-metropolis-restored
- S2: Associated Press via CBS News, "Original Metropolis Found After 80 Years", 4 July 2008 — https://www.cbsnews.com/news/original-metropolis-found-after-80-years/
- S3: NPR, interview transcript on the Buenos Aires Metropolis discovery, 2008 — https://www.npr.org/transcripts/92728652
- S4: Wikipedia, Metropolis (1927 film), restoration section (citing Bruce Bennett, Kino film notes, 2010); runtime figures (about 153 min premiere, 148 min restoration) — https://en.wikipedia.org/wiki/Metropolis_(1927_film)

## Images

| key | file | author | licence |
|---|---|---|---|
| lang_harbou_1924 | https://commons.wikimedia.org/wiki/File:Fritz_Lang_und_Thea_von_Harbou,_1923_od._1924_crop.jpg | Waldemar Titzenthaler (1869-1937) | PD-old-auto-expired, deathyear 1937 (template confirmed in assets/_pages) |

Illustrations (reel, cut, cans, trunk, frame, door), the reel cutout and the three motion loops (door, frame, trunk) were generated for this video (provenance in src/higgsfield_provenance.txt); they show no people. The film-strip diagram in beat 3 is drawn in code and labelled "schematic". No stills from Metropolis are used.

## Dropped / hedged

- Route/owner chain of the Buenos Aires print and its 16mm dupe origin: sources conflict, so only "the story goes" (AP version).
- Exact missing minutes: NPR says more than twenty, Wikipedia about 25; used "more than twenty".
- Runtime card (153 vs 148 min) is from the Wikipedia/Kino figures, shown as approximate.

## AI disclosure

Narration, sound effects, music and illustrations are AI-generated; isAiGenerated = true on all platforms. The archival photo is real and credited on screen.

## Build

src/scene.html (deterministic renderAt), caps from forced alignment (src/caps.json), mix src/mix.py, pipeline/explained/build.sh + tools.py finish (-16 LUFS, <= -2 dBTP).
