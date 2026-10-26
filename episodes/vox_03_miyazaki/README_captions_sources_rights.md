# explained no. 03 · Studio Ghibli once gave Harvey Weinstein a samurai sword

57.8 s explainer (1080×1920, 30 fps), "explained" format (narrator "Quinn", word-synced captions, header EXPLAINED NO. 03 /
@LOST_INDEX, end card "Sword or lawyers?") in a sketchbook look: soft gouache and watercolour on cream paper with pencil
underdrawing, moss green, slate blue, ochre and one lacquer-red accent; airy solo-piano score with celesta.

Beats (narration time + 0.2 s lead): hook on the katana with a NO CUTS tag → film strip + scissors, MIRAMAX · PRINCESS
MONONOKE · 1999, running-time bar 135 → 90 (schematic), "forty-five minutes shorter" → VHS and reel, NAUSICAÄ · US RELEASE,
card "cut by ≈ 20 min, and retitled" → boardroom loop, PRODUCER TOSHIO SUZUKI, katana sticker, "a blunt replica, a colleague
remembers", red card "MONONOKE HIME, NO CUT" (per Steve Alpert's memoir) → Venice 2008 portrait, ASKED IN 2005 HE LAUGHED,
quote cards "Actually, my producer did that." / "I defeated him." (The Guardian, 2005) → cinema loop, marquee PRINCESS MONONOKE
135 MIN · UNCUT, counter to ≈ $2,400,000 (1999 US run) → theatre-seat loop, SPIRITED AWAY · ACADEMY AWARD · MARCH 2003, "four
years later, an Oscar." → desk loop, Ghibli Museum photo, "Miyazaki stayed home." → end card with the Ghibli studio photo.

Narration (129 words): "Studio Ghibli once gave Harvey Weinstein a samurai sword. In nineteen ninety-nine, Miramax was
releasing Princess Mononoke in America. Weinstein wanted it cut from a hundred and thirty-five minutes to ninety. Ghibli had
been burned before. A distributor once cut Nausicaa by twenty minutes. So producer Toshio Suzuki bought a katana. A blunt
replica, a colleague remembers. He presented it in a Miramax conference room, shouting: Mononoke Hime, no cut. The story went
that Miyazaki posted it himself. Asked in two thousand five, he laughed. Actually, my producer did that. Then, smiling: I
defeated him. The film opened uncut in America. It made about two million dollars. Four years later Spirited Away won the
Oscar. Miyazaki stayed home. He didn't want, he said, to visit a country bombing Iraq."

The chosen Quinn take was sped up 4 % (atempo 1.04) to land the length; the original is kept in `audio/takes`.

## Sources
- The sword, "Actually, my producer did that", New York demands for cuts, "I defeated him": The Guardian (Xan Brooks, 14 Sep
  2005), confirmed via Cartoon Brew's same-day repost and Kotaku.
- Suzuki bought a blunt replica katana and presented it in a Miramax conference room shouting "Mononoke Hime, NO CUT":
  Steve Alpert, *Sharing a House with the Never-Ending Man* (Stone Bridge, 2020), reported by Kotaku, SlashFilm, Cartoon Brew
  (May 2020) and The Playlist (June 2020). Weinstein wanted 135 min cut to 90: same.
- Nausicaä cut by about 22 minutes and retitled Warriors of the Wind: SlashFilm (2022). Narration rounds to "twenty minutes".
- 1999 US gross $2,374,107: Variety's 1999 top-250 via Nausicaa.net; Box Office Mojo's larger total includes re-releases.
- Spirited Away won Best Animated Feature on 23 Mar 2003; Miyazaki absent: Animation World Network (2003).
- "I didn't want to visit a country that was bombing Iraq": Los Angeles Times, Comic-Con 2009, via Cartoon Brew.
- Left out (unverified): origin of the Ghibli name; the Japanese box-office record; the exact contract wording.

## Images and rights
| file | source | licence (checked in `assets/_pages/*.html`) |
|---|---|---|
| miyazaki_venice_2008.jpg | Thomas Schulz, Venice Film Festival, 2008 | CC BY-SA 2.0 |
| ghibli_museum_2024.jpg | Jakub Hałun, Ghibli Museum, Mitaka, 2024 | CC BY 4.0 |
| studio_ghibli_koganei.jpg | Akonnchiroll, Studio Ghibli, Koganei, 2023 | CC BY-SA 4.0 |
| miyazaki_comiccon_2009.jpg, miyazaki_gaslamp_2009.jpg, katana_tnm.jpg | fetched, not used (Natasha Baucas CC BY 2.0; William Tung CC BY-SA 2.0; CT Snow CC BY 2.0) | |

Illustrations (katana on a stand, film strip, boardroom, VHS and reel, storyboards, cinema, theatre seat, desk) are
AI-generated gouache props (no likenesses, film stills, posters or logos); four animated into 5 s loops (`assets/clips`).
The running-time bar, counter and typography are drawn for this video. Narration is an AI voice (preset "Quinn"; alternate
takes kept); SFX and score are AI-generated (`sfx.json`). isAiGenerated: true on all platforms. Captions name no tools.
Fonts: Inter Display, IBM Plex Mono, Instrument Serif (OFL).

Build: `src/scene.html` + `src/render.mjs` (Playwright, port 8784) → `src/runall.sh`; audio `src/mix.py` → two-pass loudnorm
−16 LUFS / −2 dBTP + limiter; captions `src/caps.json` from pocketsphinx forced alignment (`src/narration_words.json`).
