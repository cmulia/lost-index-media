# explained no. 05 · Alfred Hitchcock had to fund Psycho himself

57.0 s explainer (1080×1920, 30 fps), same "explained" format as no. 01–04 (female narrator "Quinn", word-synced captions,
header EXPLAINED NO. 05 / @LOST_INDEX, end card with an either/or question) in a new look for the topic: mid-century
monochrome paper, Saul Bass-style flat cut-out illustrations with coarse halftone grain, one accent red, dry cool-jazz noir score
that drops out for "Thank you."

Beats (narration time + 0.2 s lead): hook on the 1956 Library of Congress portrait, "He paid for Psycho himself." → DECLINED
memo, Paramount 1959, "they expected it to flop" (1925 portrait inset) → the deal: $250,000 fee crossed out, 60/40 pie
(schematic) → camera loop, checklist (black and white, television crew, Universal lot), budget counter to ≈ $800,000 →
syrup tin + 70-shot grid, "chocolate syrup." → lobby loop, the rule sign, watch cutout → motel loop, counter to $15,000,000,
"his share $5–6 million" (trade papers), Psycho house photo → five nomination cards, each stamped LOST, "He always lost." →
podium loop, 1972 portrait, "Thank you." → end card "Fee or ownership?".

Narration (138 words): "Alfred Hitchcock had to fund Psycho himself. In nineteen fifty-nine, Paramount balked at it. They
expected it to flop. So he skipped his quarter million dollar fee and paid for it himself, in return for sixty percent of
the film. Black and white. His television crew. About eight hundred thousand dollars. The shower scene took seven days and
more than seventy shots. The blood was chocolate syrup. Then a rule: nobody admitted after the film starts. A cardboard
Hitchcock stood in lobbies, pointing at his watch. By nineteen sixty-six, he said, it had made fifteen million dollars.
Trade papers put his share at five or six million. It also earned him a best director nomination. His fifth. He lost. He
always lost. In nineteen sixty-eight the Academy gave him an honorary award instead. His whole speech: Thank you."

## Sources
- Paramount's reluctance, deferred fee and 60 % of the negative, TV crew, budget just under $807k–$810k, $15M gross by 1966
  (Hitchcock's own figure), trade papers' $5–6M share: AFI Catalog of Feature Films (Psycho, 1960, history notes citing
  Variety Sep/Nov 1960 and NYT 1959/1961/1966); Variety (1960); The National (2010).
- $250,000 fee: The National (2010); Stephen Rebello, *Alfred Hitchcock and the Making of Psycho* (1990). Narration says
  "quarter million dollar fee".
- Shower scene seven days, 70+ setups, chocolate syrup: Rebello; TCM; AFI.
- "No one admitted after the start" policy and the lobby cutout pointing at his watch: BFI Sight & Sound (Linda Williams);
  TCM.
- Five Best Director nominations, no wins (Rebecca, Lifeboat, Spellbound, Rear Window, Psycho): The Hollywood Reporter
  (2012); Academy Awards database.
- Irving G. Thalberg Memorial Award, 40th Academy Awards (10 Apr 1968); the Academy's transcript of the speech records
  "Thank you" (the editor's note says he added "very much indeed" after the mic was cut): Academy acceptance-speech
  database, entry 040-26; oscars.org 40th ceremony page.
- Left out (unverified or disputed): "bought up all copies of the novel" (NYT 1959 called the rumour unfounded, per AFI);
  "Paramount lied about soundstage availability"; exact lobby-card wording.

## Images and rights
| file | source | licence (checked in `assets/_pages/*.html`) |
|---|---|---|
| hitch_1956.jpg | Fred Palumbo, New York World-Telegram & Sun, 1956, Library of Congress | PD-NYWT&S (public domain) |
| hitch_1925.jpg | unknown photographer (Daily Mail, 1927), portrait dated 1925 | PD-UK-unknown / PD-US-expired |
| hitch_1972.jpg | Jack Mitchell, c. 1972 | cc-by-sa-all (CC BY-SA 4.0 applied) |
| psycho_house.jpg | Rob Young, Psycho house set, Universal Studios backlot, 2008 | CC BY 2.0 |
| walk_of_fame.jpg | Sailko, Hitchcock's star on the Walk of Fame, 2010 | CC BY-SA 3.0 |
| bates_motel.jpg | Sidvics, 2011 (fetched, not used) | CC BY-SA 3.0 |

Photos are shown uncropped in content, framed with CSS `object-fit`; credits on screen and in captions. Illustrations (memo,
pie chart, camera, syrup, lobby, watch, motel, podium) are AI-generated flat cut-out props (no likenesses, film stills, posters
or logos); four animated into 5 s loops (`assets/clips`). The 60/40 pie, 70-shot grid, nomination cards and typography are
drawn for this video. Narration is an AI voice (preset "Quinn", the series narrator; Vesper and Sloane takes kept in
`audio/takes`); SFX and score are AI-generated (`sfx.json`). isAiGenerated: true on all platforms. Captions name no tools.
Fonts: Inter Display, IBM Plex Mono, Instrument Serif (OFL).

Build: `src/scene.html` + `src/render.mjs` (Playwright, port 8781) → `src/runall.sh`; audio `src/mix.py` → two-pass loudnorm
−16 LUFS / −2 dBTP + limiter (measured −16.0 LUFS, −4.5 dBTP); captions `src/caps.json` from pocketsphinx forced alignment
of the chosen take (`src/narration_words.json`).
