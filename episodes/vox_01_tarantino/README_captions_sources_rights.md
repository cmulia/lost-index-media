# explained no. 01 · Quentin Tarantino's film school was a video store

54.5 s colourful 2D editorial explainer (1080×1920, 30 fps) with a female narrator (Vox-style pacing), word-synced
captions, SFX and a retro funk score. Same paper-cutout motion system as what if no. 03/04, plus real photos.

Beats (narration time + 0.2 s lead): hook on shelves loop with the Tarantino photo → Video Archives counter, "high school
dropout", 5 years, schematic map pin at Manhattan Beach → "talking movies" genre labels + Roger Avary name badge →
"No, I was already a movie expert" quote, HIRED → timeline 1992 Reservoir Dogs / 1994 Pulp Fiction / Palme d'Or / 1995
Oscar (shared with Avary) → store closes, tapes pile up, ≈ 8,000 → "but here's the twist" → New Beverly + Vista photos →
"film prints only, no digital" over the New Bev's ALWAYS ON FILM marquee → marquee board "came up on tape / keeps film
running" → end card "Tape or film?".

Narration (130 words): "Quentin Tarantino's film school was a video store. A high school dropout, he spent five years
behind the counter at Video Archives in Manhattan Beach, California. The job was talking movies, with customers, and with
a co-worker named Roger Avary. Though he says he was already a movie expert. That's how he got hired. Then came Reservoir
Dogs. And Pulp Fiction: the Palme d'Or, and a screenplay Oscar he shared with Avary. When the store closed, Tarantino
bought its tapes. He's put his collection at close to eight thousand tapes and DVDs. But here's the twist. The video store
clerk now owns two Los Angeles cinemas, the New Beverly and the Vista. Their rule? Film prints only. No digital. He came up
on tape. Now he's keeping film running."

## Sources
- Dropout, Narbonne High (age given as 15 or 16, so left out): NBC News "From video clerk to box office icon"
  (nbcnews.com/id/wbna4817308); Encyclopedia.com.
- Video Archives, Manhattan Beach, ~5 years, co-worker Roger Avary: Open Culture on Tom Roston, *I Lost It at the Video
  Store* (2021); Rolling Stone (2022); TV Insider.
- "No, I was already a movie expert" and that this is how he got hired: BBC, *Quentin Tarantino: Hollywood's Boy Wonder*
  (1994), quoted by Open Culture; listed at thenewbev.com.
- Reservoir Dogs 1992; Pulp Fiction Palme d'Or 1994; Oscar, Best Original Screenplay (1995 ceremony), shared with Avary:
  Festival de Cannes; Academy Awards database.
- Bought the store's tapes when it closed; collection "close to 8,000 video tapes and DVDs" (his estimate); Video Archives
  Podcast from July 2022: Rolling Stone (2022); Podnews.
- New Beverly: bought 2007, programmed by him since Sept 2014, film prints only: thenewbev.com/about; LA Times (2017); LAist.
- Vista: bought (~$4.73 M, Dec 2020, announced 2021), "only film", reopened Nov 2023: Bisnow (citing THR/LA Times);
  Box Office Pro (2023); Time Out LA (2023).
- Not used (unverifiable): the "I went to films" quote; exact store years. Second screen at the Vista (Cinema Treasures)
  unverified, so the script says "film prints only", never "no VHS".

## Images and rights
| file | source | licence (checked in `assets/_pages/*.html`) |
|---|---|---|
| qt_2015.jpg | Gage Skidmore, 2015, Commons "Quentin Tarantino by Gage Skidmore.jpg" | CC BY-SA 3.0 |
| qt_panel.jpg | Gage Skidmore, 2015, Commons "SDCC 2015 - Quentin Tarantino (19702844696).jpg" | CC BY-SA 2.0 |
| newbev.jpg | Doug Kline ("pop culture geek"), 2011, Commons, New Beverly marquee | CC BY 2.0 |
| newbev_alt.jpg | Sean Dudley, 2022, Commons "Billy Wilder films at New Beverly Cinema.jpg" | PD-self |
| vista.jpg | Steve Peters, 2011, Commons "Vista Theater, Los Angeles.jpg" | CC BY 2.0 |

Photos are shown uncropped in content, framed with CSS `object-fit`; credits on screen and in captions.
Illustrations (shelves, counter, projector booth, marquee, desk, seats, VHS + reel stickers) are AI-generated
risograph-style props (no likenesses, no film stills, posters or logos); four of them animated into 5 s loops
(`assets/clips`). The map and all typography/graphics are drawn for this video. Narration is an AI voice (preset
"Quinn"); SFX and score are AI-generated. All platforms flagged isAiGenerated: true. Captions name no tools.
Fonts: Inter Display, IBM Plex Mono, Instrument Serif (SIL OFL).

Build: `src/scene.html` + `src/render.mjs` (frames via Playwright) → `src/runall.sh`; audio `src/mix.py`
(narration + SFX + music ducked under the voice) → loudnorm −16 LUFS, limiter; caption timing `src/caps.json` from
pocketsphinx forced alignment (`pipeline/lostindex/align.py`) of the chosen take.
