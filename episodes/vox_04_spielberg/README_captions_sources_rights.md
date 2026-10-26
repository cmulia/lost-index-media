# explained no. 04 · Jaws is scary because its shark kept breaking

57.8 s explainer (1080×1920, 30 fps), "explained" format (narrator "Quinn", word-synced captions, header EXPLAINED NO. 04 /
@LOST_INDEX, end card "Show the monster, or hide it?") in a sun-bleached 1970s seaside look: faded cyan and sea-green
Kodachrome gouache illustrations, bone-white sand, lifeguard red and warning yellow accents, hand-inked nautical-chart
lines, a dry Rhodes-and-upright-bass score that ends on two low notes.

Beats (narration time + 0.2 s lead): hook over the shark-skeleton loop → nautical chart, Edgartown aerial, 1993 portrait, "age
27." → skeleton loop, card "mechanical sharks: three, all nicknamed Bruce — after his lawyer", corroded valve inset, "in salt
water, they rarely worked" → day grid 55 → 159 (schematic), budget bar doubling → barrels loop, "suggest the shark instead",
YELLOW BARRELS, UNDERWATER SHOTS (water overlay), piano inset "two low notes" → marquee loop, OPENED 20 JUNE 1975, counter to
$100,000,000 → 2023 portrait, quote card "just good fortune" (BBC, 2022), "and nightmares, for years" → faded skeleton,
UNIVERSAL BACK LOT, three red Xs, "and rotted away" → museum-atrium illustration, "a fourth, from the same mould", Universal
Hollywood replica photo (labelled as a tour replica), "it was never in the film" → end card with the Menemsha photo.

Narration (138 words): "Jaws is scary because its shark kept breaking. In nineteen seventy-four, a twenty-seven-year-old
Steven Spielberg shot Jaws off Martha's Vineyard. The crew built three mechanical sharks, nicknamed Bruce after Spielberg's
lawyer. In salt water they rarely worked. A fifty-five day shoot stretched to one hundred and fifty-nine. The budget more
than doubled. So he suggested the shark instead. Yellow barrels. Underwater shots. Two low notes from John Williams. Jaws
opened in June nineteen seventy-five, the first film to pass one hundred million dollars in America. Spielberg now calls the
breakdowns good fortune. He also says the shoot gave him nightmares for years. The three sharks were dumped on a back lot and
rotted away. A fourth, from the same mould, now hangs in the Academy Museum. Spielberg thanked it for his career. It was never
in the film."

The chosen Quinn take was sped up 4 % (atempo 1.04) to land the length; the original is kept in `audio/takes`.

## Sources
- Three mechanical sharks nicknamed Bruce after lawyer Bruce Ramer; salt-water failures: Associated Press (2020); NPR (2019,
  2025); History.com.
- 55-day schedule stretched to 159; budget more than doubled; opened 20 June 1975; first film to pass $100M (Guinness
  specifies US rentals): Guinness World Records (2015); CBS Sunday Morning (2025); NPR (2025). Exact $4M → $9M figures left out.
- "It was just good fortune that the shark kept breaking": BBC Desert Island Discs (Dec 2022) via The Hollywood Reporter.
- Nightmares for years: NPR (Sept 2025); Parade / People (June 2025).
- The three sharks dumped on the Universal back lot; the fourth cast from the mould after filming, 25 years in a Sun Valley
  junkyard, restored by Greg Nicotero, installed in the Academy Museum (Nov 2020); Spielberg's "Thank you for a robust career"
  at the Sept 2025 exhibition opening: AP (2020); NPR (2019, 2025); THR (2025); ABC7 (2025).
- Two-note theme and Spielberg's first reaction: Laurent Bouzereau, *Spielberg: The First Ten Years* (via SYFY, 2023).
- Left out (unverified): the "godsend" and "Hitchcockian" quotes; "first summer blockbuster" (characterisation).

## Images and rights
| file | source | licence (checked in `assets/_pages/*.html`) |
|---|---|---|
| spielberg_1993_hero.jpg | GianAngelo Pistoia, Venice Film Festival, 1993 | CC BY-SA 3.0 |
| spielberg_2023.jpg | Martin Kraft, Berlinale 2023 | CC BY-SA 4.0 |
| edgartown_harbor_aerial.jpg | Don Ramey Logan, Edgartown Harbor aerial, 2017 | CC BY-SA 4.0 |
| menemsha_harbor.jpg | Elkman, Menemsha, Martha's Vineyard, 2003 | CC BY-SA 2.5 |
| bruce_replica_universal_hollywood.jpg | TaurusEmerald, tour replica, Universal Studios Hollywood, 2025 | CC BY-SA 4.0 |
| spielberg_1990.jpg, jaws_shark_universal_florida.jpg | fetched, not used (Alan Light CC BY 2.0; Rmkf1982 CC BY-SA 3.0) | |

Illustrations (shark skeleton on a barge, barrels, valve, boat, clapperboard, piano, blank marquee, museum atrium) are
AI-generated gouache props (no likenesses, film stills, posters or logos); four animated into 5 s loops (`assets/clips`).
The chart lines, day grid, budget bars and typography are drawn for this video. Narration is an AI voice (preset "Quinn";
Sloane and Vesper takes kept); SFX and score are AI-generated (`sfx.json`). isAiGenerated: true on all platforms. Captions
name no tools. Fonts: Inter Display, IBM Plex Mono, Instrument Serif (OFL).

Build: `src/scene.html` + `src/render.mjs` (Playwright, port 8783) → `src/runall.sh`; audio `src/mix.py` → two-pass loudnorm
−16 LUFS / −2 dBTP + limiter; captions `src/caps.json` from pocketsphinx forced alignment (`src/narration_words.json`).
