# explained no. 02 · Before Parasite, Bong Joon Ho was a rich family's tutor

57.5 s dark editorial explainer (1080×1920, 30 fps), same "explained" format as no. 01 (female narrator, word-synced
captions) but a different mood for the topic: night/moss/bone/ochre palette, Instrument Serif Italic headlines,
rain overlay, cut-paper gouache illustrations, tense baroque chamber score that drops out for "Three died."

Beats (narration time + 0.2 s lead): hook, Bong photo over rainy stairs, "the tutor." → tutoring desk with index cards
(girlfriend: English tutor → "vouches" → Bong: math tutor, crossed out, "bad at math") → "the con." referral chain,
real life vs the film → keyhole onto the glass mansion, "peeping into strangers' lives" → keyhole opens: "Not a real
house. A set." with schematic set plan → Palme d'Or (cast photo) → Golden Globes "one-inch tall barrier of subtitles"
with a subtitle bar + ruler → four Oscars checklist → the film's flood: a water tank (schematic) → real flood photo,
banjiha with rising water, "Three died." → street-level cross-section, "≈ 200,000 households still live half
underground" → end card "The basements in Parasite are real." / "Subtitles or dubbed?".

Narration (142 words): "Before Parasite, Bong Joon Ho was a rich family's tutor. His girlfriend taught their son English,
and vouched for him as the math tutor. He says he was bad at math. That's how the con in Parasite begins: a friend
vouches for you. He says it felt like peeping into strangers' lives. That glass mansion? Not a real house. A set, built
from scratch. Parasite won the Palme d'Or, a first for Korea. At the Golden Globes, he urged us to overcome the one-inch
tall barrier of subtitles. Then four Oscars, including Best Picture, the first ever not in English. The film's flood?
Shot in a giant water tank. Three years later, a real flood trapped a family in a Seoul semi-basement. Three died. Seoul
vowed to phase these homes out. About two hundred thousand households still live half underground."

## Sources
- Tutoring job via his girlfriend (now wife), "really bad at math", origin of the idea: The Hollywood Reporter, "Making of
  Parasite" (8 Nov 2019) and "10 things to know" (2020). "Peeping into" strangers' lives (paraphrased; wording varies):
  Time Out; Dazed; Rolling Stone.
- Park house built as a set from scratch by production designer Lee Ha-jun; basement and bunker separate sets: Dezeen
  (2020); Vice; Apartment Therapy.
- Flood scenes shot in a water tank (reportedly Goyang Aqua Studio): actress Park So-dam via Asia Economy (2021);
  El Espectador; location guides. Labelled "per the cast and crew" on screen.
- Palme d'Or, 25 May 2019, first Korean winner: Festival de Cannes; RogerEbert.com; VOA.
- Golden Globes, 5 Jan 2020, "Once you overcome the one-inch tall barrier of subtitles…" (interpreter Sharon Choi):
  The Hollywood Reporter; Korea Times.
- Four Oscars at the 92nd Academy Awards, 9 Feb 2020; first non-English-language Best Picture: THR winners list.
- 8 Aug 2022 Sillim-dong semi-basement deaths (three family members): Korea JoongAng Daily; Korea Times; CNN.
- Seoul's 10 Aug 2022 pledge to phase out basement homes: Korea Times; Al Jazeera. ≈ 200,000 households (Seoul Institute,
  202,741 end-2021; Asia Economy Oct 2025 still ~200,000); slow progress and budget cut: Asia Economy (2025);
  Kyunghyang (2026).
- Left out (unverified): "fired after two months", the sauna story, "Bong-tail" nickname.

## Images and rights
| file | source | licence (checked in `assets/_pages/*.html`) |
|---|---|---|
| bong_2017.jpg | Dick Thomas Johnson, Okja Japan premiere, 22 Jun 2017 | CC BY 2.0 |
| bong_2025.jpg | Kevin Paul (PaulLim11), Okja panel, 23 Mar 2025 | CC BY 4.0 |
| cast_2019.jpg | Kinocine, Parasite director and cast, Seoul, 22 Apr 2019 | CC BY-SA 4.0 |
| flood_2022.jpg | YaMaDa, Han River floods, 10 Aug 2022 | CC BY-SA 4.0 |
| bong_2006.jpg, jahamun.jpg | fetched, not used (Greg Dunlap CC BY 2.0; Aatu Dorochenko CC BY-SA 4.0) | |

Illustrations (rainy stairs, semi-basement, glass mansion, tutoring desk, storyboards, hillside, scholar's stone,
peach) are AI-generated cut-paper props (no likenesses, film stills, posters or logos); four animated into 5 s loops
(`assets/clips`). Index cards, referral chain, set plan, water tank, cross-section and typography are drawn for this
video. Narration is an AI voice (preset "Quinn", same narrator as no. 01); SFX and score are AI-generated.
isAiGenerated: true on all platforms. Captions name no tools. Fonts: Inter Display, IBM Plex Mono, Instrument Serif (OFL).

Build: `src/scene.html` + `src/render.mjs` → `src/runall.sh`; audio `src/mix.py` → loudnorm −16 LUFS + limiter;
captions `src/caps.json` from pocketsphinx forced alignment of the chosen take (`src/narration_words.json`).
