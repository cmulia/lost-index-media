# explained no. 06 · Christopher Nolan's first film cost about six thousand dollars

57.0 s explainer (1080×1920, 30 fps), "explained" format (narrator "Quinn", word-synced captions, header EXPLAINED NO. 06 /
@LOST_INDEX, end card "Real plane or computer graphics?") in a blueprint look: navy drafting paper with a faint grid,
white/cyan technical line-work illustrations, one amber accent, minimal metronome-and-piano score.

Beats (narration time + 0.2 s lead): hook with the 2013 portrait and a film-can sticker → torn pay slip, RENT / FILM STOCK
("half and half — he says") → Bolex loop, calendar of fourteen Saturdays across one year (schematic), checklist (black and
white, 16 mm, held the camera himself) → clapperboard TAKE 1, "mostly first takes" → UCL portico photo, "producer Emma
Thomas, first week at university" → 2026 portrait, "known for avoiding computer graphics" → jet loop, Tenet tag, Victorville
boneyard photo, quote card "more efficient than a model" (Total Film, 2020) → tower loop, Trinity, "no computer graphics at
all" → cream card: counter to 7 Oscars with the seven categories, "Best Picture: accepted by Emma Thomas" → desk illustration,
"has never used email", "no smartphone either", "time to think, he says" → end card.

Narration (139 words): "Christopher Nolan's first film cost about six thousand dollars. It was nineteen ninety-eight. Half his
pay went on rent, he says, and half on film stock. So he shot on Saturdays, fourteen of them, spread across a year. Black and
white. Sixteen millimetre. He held the camera himself. Most of it is first takes. His producer was Emma Thomas, whom he met
in his first week at university. Twenty years on, he was known for avoiding computer graphics. For Tenet he crashed a real
Boeing seven forty-seven. More efficient than a model, he said. For Oppenheimer, the first atomic test. No computer graphics
at all. It won seven Oscars. Emma Thomas accepted Best Picture. And the man who will not fake an atom bomb has never used
email. No smartphone either. It gives him time to think, he says."

## Sources
- Following (1998): budget — Nolan's own on-record figure is £3,500 (Guerilla Film Makers Handbook interview, via Chris Jones);
  Emma Thomas gave $6,000 (Variety, 2024, via Wikipedia's citation) and SCMP states US$6,000; narration says "about six
  thousand dollars". Half his pay on rent / half on film stock, Saturdays, ~a year, 16 mm black and white, operating the
  camera himself, mostly first takes: Guerilla Film Makers Handbook interview; Mental Floss (2012); The Criterion Collection;
  PA Media (2024).
- Met Emma Thomas in his first week at University College London; she has produced all his features: NPR (2024); Variety (2024).
- Tenet 747 found in the Victorville boneyard, "more efficient" than miniatures and visual effects: Total Film / GamesRadar
  (2020). The common "cheaper than CGI" paraphrase was not used.
- Oppenheimer's Trinity test staged without computer graphics: Total Film / GamesRadar (2022). Narration limits the claim to
  the test.
- Seven Oscars at the 96th Academy Awards (Picture, Director, Actor, Supporting Actor, Cinematography, Editing, Score); Emma
  Thomas accepted Best Picture: NPR (2024); Academy database.
- Never used email, no smartphone, "gives me time to think": The Hollywood Reporter (2014, 2023) via Entrepreneur (2015) and
  ET Online (2023); 60 Minutes (May 2026) via Complex; flip phone for travelling (Tonight Show, July 2026) via CinemaBlend — the
  last two used only in captions, hedged with "he says".
- Left out (unverified): "writes on a computer with no internet"; the Alex Haw head-shaving pause; "fourteen months";
  nomination counts.

## Images and rights
| file | source | licence (checked in `assets/_pages/*.html`) |
|---|---|---|
| nolan_2013.jpg | Richard Goldschmidt, London, May 2013 | CC BY 3.0 |
| nolan_2026.jpg | Philip Romano (WikiPortraits), New York, July 2026 | CC BY-SA 4.0 |
| ucl_portico.jpg | Karlunun, UCL Wilkins Building portico, 2022 | CC BY-SA 4.0 |
| victorville.jpg | Bobak Ha'Eri, Southern California Logistics Airport aerial, 2009 | CC BY 3.0 |
| imax_camera.jpg | Atlant, IMAX camera, Montreal Science Centre, 2005 | CC BY 2.5 |
| bolex_h16.jpg | yohey1028, Bolex H16 (fetched, not used; the camera on screen is illustrated) | PD-self |

Photos are shown uncropped in content, framed with CSS `object-fit`; credits on screen and in captions. Illustrations (film
cans, pay slip, 16 mm camera, clapperboard, jumbo jet, test tower, desk, projector) are AI-generated blueprint-style props
(no likenesses, film stills, posters, logos or livery); four animated into 5 s loops (`assets/clips`). The calendar, Oscar
counter and typography are drawn for this video. Narration is an AI voice (preset "Quinn"; Vesper take kept); SFX and score
are AI-generated (`sfx.json`). isAiGenerated: true on all platforms. Captions name no tools. Fonts: Inter Display, IBM Plex
Mono, Instrument Serif (OFL).

Build: `src/scene.html` + `src/render.mjs` (Playwright, port 8782) → `src/runall.sh`; audio `src/mix.py` → two-pass loudnorm
−16 LUFS / −2 dBTP + limiter; captions `src/caps.json` from pocketsphinx forced alignment (`src/narration_words.json`).
