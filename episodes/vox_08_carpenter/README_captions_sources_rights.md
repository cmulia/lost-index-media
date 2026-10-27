# explained no. 08 · Michael Myers wore a Captain Kirk mask

51.0 s explainer (1080×1920, 30 fps), "explained" format (narrator "Quinn", word-synced captions, header EXPLAINED NO. 08 /
@LOST_INDEX, end card "Blank mask or famous face?") in a 1970s drive-in screenprint look: black ground, midnight teal and
pumpkin orange, halftone grain; a tense minimal analog-synth score (original, not the Halloween theme).

Narration (127 words): "Michael Myers wore a Captain Kirk mask. John Carpenter made Halloween for about three hundred twenty-five thousand dollars. A custom mask cost too much. So Tommy Lee Wallace, the production designer, visited a Hollywood magic shop. He bought a rubber mask of the Star Trek captain. The story goes that it cost one dollar ninety-eight. He widened the eye holes, removed the eyebrows, and spray-painted the face white. They shot in South Pasadena, and trucked in dried leaves to fake an Illinois autumn. It earned about forty-seven million dollars. William Shatner says he wondered if it was a joke. He recognized it, he says, as the death mask made of his own face. The faceless killer was a famous face all along, with the expression taken away."

## Beats and sources
- 0: Michael Myers wore a Captain Kirk mask. [S1, S2]
- 1: John Carpenter made Halloween for about three hundred twenty-five thousand dollars. [S3]
- 2: A custom mask cost too much. So Tommy Lee Wallace, the production designer, visited a Hollywood magic shop. [S1, S2]
- 3: He bought a rubber mask of the Star Trek captain. The story goes that it cost one dollar ninety-eight. [S2]
- 4: He widened the eye holes, removed the eyebrows, and spray-painted the face white. [S1, S2]
- 5: They shot in South Pasadena, and trucked in dried leaves to fake an Illinois autumn. [S3]
- 6: It earned about forty-seven million dollars. [S3]
- 7: William Shatner says he wondered if it was a joke. He recognized it, he says, as the death mask made of his own face. [S1]
- 8: The faceless killer was a famous face all along, with the expression taken away. [S1, S4]

## Sources
- S1: The Hollywood Reporter, William Shatner on the Michael Myers mask — https://www.hollywoodreporter.com/movies/movie-features/william-shatner-capt-kirk-michael-myers-halloween-mask-joke-1235033482/
- S2: Far Out Magazine, The actor whose face inspired the Halloween mask (quotes Carpenter; $1.98) — https://faroutmagazine.co.uk/the-actor-who-inspired-halloween-mask/
- S3: Den of Geek, Halloween: The Ingredients of a Horror Classic — https://www.denofgeek.com/movies/halloween-the-ingredients-of-a-horror-classic
- S4: StarTrek.com, Michael Myers Halloween mask was Shatner's face (Shatner trick-or-treating video) — https://www.startrek.com/news/michael-myers-halloween-mask-was-shatners-face

Hedged: the $1.98 price ("the story goes", single source); Shatner's death-mask account is attributed to him ("he says").
Cut as unverified:
- Exact purchase price $1.98: only found in Far Out (secondary); hedged as 'the story goes'.
- Date of purchase, shop name: only 'a magic shop on Hollywood Boulevard' (THR); name dropped.
- Mask cast from Shatner's Star Trek death mask: Shatner's own claim; kept as 'he says'. Whether the Kirk mask was actually moulded from it is unverified.
- Later fate of the original mask: not found reliably; dropped.
- Budget variants: $300,000 (Carpenter's pledge) vs $325,000; used about $325,000.
- Box office: $47 million (Den of Geek); other sources say higher with reissues; used 'about forty-seven million'.
- Exact Shatner trick-or-treating quote: StarTrek.com has no direct quote; hedged as 'he says'.
- Shatner photos: none used.

## Images
| key | what | author | licence | source |
|---|---|---|---|---|
| carpenter_2001.jpg | John Carpenter, 2001 | Thomas Peter Schulz | CC BY-SA 3.0 (migrated) / GFDL | https://commons.wikimedia.org/wiki/File:JohnCarpenter01.jpg |
| carpenter_2012.jpg | John Carpenter, 2012 | Kyle Cassidy | CC BY-SA 4.0 | https://commons.wikimedia.org/wiki/File:Portrait_of_John_Carpenter.jpg |
| south_pasadena_mission.jpg | Mission St. & Meridian Ave., South Pasadena | Cbl62 | CC BY-SA 3.0 | https://commons.wikimedia.org/wiki/File:South_Pasadena_Historic_District,_Mission_and_Meridian.jpg |

Licence templates confirmed in `assets/_pages/*.html` (Commons wikitext). Photos shown unaltered except crop; credited on screen.

## AI disclosure
Illustrations (mask, shelf, spray, street, cast, porch, mask cutout), three subtle motion loops and the narration voice are
AI-generated; sound effects and score are AI-generated. Masks are drawn as generic blank craft masks (no character or real-person
likeness); a first pass of two props that came out resembling the film's mask was discarded and regenerated. Posts are labelled
AI-generated on all platforms. Diagrams (budget counter, cost vs box office bars) are drawn in code for this video.

## Build
`pipeline/explained/build.sh vox_08_carpenter <port> prep|stills|video 51`, `src/mix.py`, then
`pipeline/explained/tools.py finish` (loudnorm −16 LUFS / −2 dBTP). Fetch list: `fetch/vox_08_carpenter.txt`.
