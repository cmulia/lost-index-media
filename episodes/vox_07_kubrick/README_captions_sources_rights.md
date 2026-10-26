# explained no. 07 · Kubrick's candlelit film used lenses built for the moon

57.0 s explainer (1080×1920, 30 fps), "explained" format (narrator "Quinn", word-synced captions, header EXPLAINED NO. 07 /
@LOST_INDEX, end card "Candlelight or studio lights?") in a parchment look: cream paper, umber-ink copperplate-engraving
illustrations, candle-amber highlights, a slow felt-piano and synth-pad score.

Beats (narration time + 0.2 s lead): hook on the three-wick candle loop with the 1949 LOOK portrait → chandelier loop, BARRY
LYNDON · 1975, 1963 set photo, "by candlelight alone", "no fill light" credit → light ladder (schematic), lens sticker, "the
fastest lens made" → ten lens discs: six → NASA, three → Kubrick, Zeiss Planar photo → cross-section engraving, "millimetres
from the film", Mitchell BNC photo and a saw line, "cut apart until it did" → candle loop, THREE WICKS PER CANDLE, monitor
with focus grid, "watched from the side" → ledger engraving, four laurel cards (Cinematography, Art Direction, Costume Design,
Scoring Adaptation), "four Oscars. and a loss in America." → Childwickbury photo, poll card counting to no. 12 → moon
engraving, "and the moon lenses?", Zeiss 2022 card "there is no evidence", candle loop, "their famous pictures are of candles."

Narration (139 words): "Kubrick's candlelit film used lenses built for the moon. In nineteen seventy-five, Stanley Kubrick
shot the interiors of Barry Lyndon by candlelight alone. Film stock could barely see in the dark. He needed the fastest lens
made. Zeiss had built ten for NASA's Apollo program. Six went to NASA. Kubrick bought three. One problem. The rear glass sat
millimetres from the film. Zeiss said it could not fit a movie camera. Kubrick had one cut apart until it did. The candles had
three wicks. Focus was so thin a video camera watched actors from the side. The film won four Oscars. It also lost money in
America. Directors now rank it the twelfth greatest film ever made. And the moon lenses? Zeiss now says there is no evidence
they ever saw the moon. Their famous pictures are of candles."

## Sources
- Candlelight-only interiors, no fill light; Zeiss Planar 50 mm f/0.7, ten made, six to NASA, three bought by Kubrick; rear
  element a few millimetres from the film; Mitchell BNC reworked by Ed DiGiulio; three-wick candles; side-on video camera
  for focus: American Cinematographer (March 1976, DiGiulio sidebar via theasc.com); ZEISS press release (21 Sep 2022);
  PetaPixel (2021); Digital Camera World (2022).
- Four Oscars of seven nominations at the 48th Academy Awards (1976): oscars.org ceremony page / Academy database.
- Budget about $11M, worldwide ≈ $20.3M, did not cover US costs: The Numbers; New Statesman (2025); The Spectator (2025).
- Twelfth in the Sight & Sound 2022 directors' poll: The Spectator (2025) plus a mirror of the list; the BFI page itself could
  not be fetched in this environment.
- Zeiss (2022): "there is no evidence" the lenses were ever used to photograph the moon.
- Left out (unverified): "Kubrick's own favourite film" (not supported); exact rear-element distance in mm (sources give 4–5).

## Images and rights
| file | source | licence (checked in `assets/_pages/*.html`) |
|---|---|---|
| kubrick_1949.jpg | Phillip A. Harrington, LOOK magazine, 1949, Library of Congress LOOK collection | PD-Look (public domain; editorial use) |
| kubrick_1963_strangelove_set.jpg | Columbia Pictures publicity photo, 1963, copyright not renewed | PD-US-not renewed |
| zeiss_planar_07_lens.jpg | Gbentinck, Stanley Kubrick exhibition, San Francisco, 2016 | CC BY-SA 4.0 |
| zeiss_planar_07_on_camera.jpg | Gbentinck, same exhibition | CC BY-SA 4.0 |
| mitchell_bnc_lacma.jpg | Matthew J. Cotter, Stanley Kubrick: The Exhibition, LACMA, 2013 | CC BY-SA 2.0 |
| childwickbury_manor.jpg | Colin, Childwickbury Manor, 2020 | CC BY-SA 4.0 |

Illustrations (candle, lens, cross-section, camera, chandelier, monitor, moon, ledger) are AI-generated engraving-style props
(no likenesses, film stills, posters or logos); four animated into 5 s loops (`assets/clips`). The light ladder, lens discs,
laurel cards, poll counter and typography are drawn for this video. Narration is an AI voice (preset "Quinn"; alternate take
kept); SFX and score are AI-generated (`sfx.json`). isAiGenerated: true on all platforms. Captions name no tools. Fonts: Inter
Display, IBM Plex Mono, Instrument Serif (OFL).

Build: `src/scene.html` + `src/render.mjs` (Playwright, port 8785) → `src/runall.sh`; audio `src/mix.py` → two-pass loudnorm
−16 LUFS / −2 dBTP + limiter; captions `src/caps.json` from pocketsphinx forced alignment (`src/narration_words.json`).
