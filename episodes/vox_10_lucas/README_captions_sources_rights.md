# explained no. 10 · George Lucas turned down a raise for Star Wars

56.0 s explainer (1080×1920, 30 fps), "explained" format (narrator "Quinn", word-synced captions, header EXPLAINED NO. 10 /
@LOST_INDEX, end card "The raise or the rights?") in a 1970s toy-catalogue look: hard-flash product shots on seamless
mustard, tangerine and teal paper, halftone dots, taped-in white-border snapshots; a dry 1970s library-funk score (original).

Narration (132 words): "George Lucas turned down a raise for Star Wars. Reportedly paid one hundred fifty thousand dollars to write and direct it, he was urged to ask for more. Instead, he asked Fox for something vaguer. The rights to any sequels, and to the merchandise. Fox, the story goes, thought it had the better deal. At Christmas nineteen seventy-seven, the toys were not ready. So the toymaker sold an empty box with a certificate. Shoppers bought it anyway. By nineteen ninety-nine, Fortune reported, merchandise had earned twice as much as the films. Lucas kept those rights thirty-five years. In twenty twelve he sold his company to Disney for about four billion dollars. His reason, he said: Star Wars could live beyond him. A raise is paid once. A story, he bet, keeps paying."

## Beats and sources
- 0: George Lucas turned down a raise for Star Wars. [S1]
- 1: Reportedly paid one hundred fifty thousand dollars to write and direct it, he was urged to ask for more. [S1]
- 2: Instead, he asked Fox for something vaguer. The rights to any sequels, and to the merchandise. [S1, S2]
- 3: Fox, the story goes, thought it had the better deal. [S2, S1]
- 4: At Christmas nineteen seventy-seven, the toys were not ready. So the toymaker sold an empty box with a certificate. [S3]
- 5: Shoppers bought it anyway. [S3]
- 6: By nineteen ninety-nine, Fortune reported, merchandise had earned twice as much as the films. [S2]
- 7: Lucas kept those rights thirty-five years. In twenty twelve he sold his company to Disney for about four billion dollars. [S4, S2]
- 8: His reason, he said: Star Wars could live beyond him. A raise is paid once. A story, he bet, keeps paying. [S4]

## Sources
- S1: Brian Jay Jones, George Lucas: A Life (Little, Brown, 2016), p.161 (as cited by Wikipedia 'George Lucas', note on the US$150,000 fee and the licensing/merchandising/sequel negotiation); confirm page before publishing — https://en.wikipedia.org/wiki/George_Lucas
- S2: Fortune/CNN Money, 'Star Wars' feature, 19 May 1999 (Lucas traded a large directing fee for sequel and merchandising rights; Fox thought it had the better deal; merchandise earned twice the films, $4.5 billion) — https://money.cnn.com/1999/05/19/fortune/fortune_starwars/
- S3: The Strong National Museum of Play, 'Star Wars Day: the action figures that almost weren't' (Early Bird Certificate Package, Christmas 1977, figures promised from February 1978) — https://www.museumofplay.org/blog/star-wars-day-the-action-figures-that-almost-werent/
- S4: NPR, 'The Force Is Strong With This One: Disney Buys Lucasfilm For $4B', 30 Oct 2012 (US$4.05 billion, about half cash, rest Disney stock; Lucas: 'I've always believed that Star Wars could live beyond me') — https://www.npr.org/sections/thetwo-way/2012/10/30/163976651/the-force-is-strong-with-this-one-disney-buys-lucasfilm-for-4b

## Hedged / dropped
- The $150,000 fee is hedged ("reportedly"); "Fox thought it had the better deal" is hedged ("the story goes").
- Merchandise ≈ twice the films is attributed on screen and in narration to Fortune (1999).
- Exact fee figures and the '$500,000 raise' (only a single secondary site; sources differ), so narration says 'reportedly' and gives only the $150,000 base fee from the Jones biography as cited by Wikipedia (page not checked directly).
- Alan Ladd Jr. as the Fox executive who agreed: not confirmed to a primary-quality source in budget.
- 'Fox thought merchandising worthless' stated as fact: softened to 'the story goes ... easy part of the bargain' (Fortune says executives thought they had the better end).
- Lucas giving sale proceeds to education: NPR piece did not mention it; dropped.
- Year of the contract (1973 vs 1975): sources inconsistent; avoided.
- Mann's Chinese Theatre 1977 photo: none found on Commons.

## Images
| key | what | author | licence | source |
|---|---|---|---|---|
| lucas_2024.jpg | George Lucas, Cannes 2024 | Kevin Payravi | CC BY-SA 4.0 (cc-by-sa-all) | https://commons.wikimedia.org/wiki/File:George_Lucas_2024.jpg |
| lucas_2009.jpg | George Lucas, Venice 2009 | nicolas genin | CC BY-SA 2.0 | https://commons.wikimedia.org/wiki/File:George_Lucas_cropped_2009.jpg |
| lucas_2025.jpg | George Lucas, Comic-Con 2025 | Gage Skidmore | CC BY-SA 3.0 | https://commons.wikimedia.org/wiki/File:George_Lucas_by_Gage_Skidmore.jpg |
| lucas_2015_crop.jpg | George Lucas at the State Department, Kennedy Center Honors 2015 (derived: cropped to Lucas from lucas_2015.jpg) | U.S. Department of State | PD-USGov-DOS | https://commons.wikimedia.org/wiki/File:Secretary_Kerry_Chats_With_2015_Kennedy_Center_Honors_Recipient_George_Lucas_(23244763499).jpg |
| skywalker_ranch.jpg | Skywalker Ranch, Ewok Lake | Mike McCune | CC BY 2.0 | https://commons.wikimedia.org/wiki/File:Skywalker_Ranch_Ewok_Lake.jpg |
| letterman_dac.jpg | Letterman Digital Arts Center (Lucasfilm), Building B, San Francisco | Frank Schulenburg | CC BY-SA 4.0 | https://commons.wikimedia.org/wiki/File:Letterman_Digital_Arts_Center,_Building_B.jpg |

Licence templates confirmed in `assets/_pages/*.html` (Commons wikitext). Photos shown unaltered except crop; credited on screen.
`lucas_2015_crop.jpg`: derived_from `lucas_2015.jpg`, changes: cropped (x 46.2–62.5 %, y 6–62 %) to show Lucas only.

## AI disclosure
Illustrations (contract desk, pegboard of blank-card figures, empty gift box, cash register, toy-box tower, vault), the register
cutout, three subtle motion loops (empty box, toy tower, vault) and the narration voice are AI-generated; sound effects and score
are AI-generated. No people or real likenesses in generated images; no trademarked characters or designs.
Posts are labelled AI-generated on all platforms. Diagrams (fee counter, films vs merchandise bars, 1977→2012 counter) are drawn in code.
Narration takes: Quinn 52.3 s (used), Vesper 53.1 s.

## Build
`pipeline/explained/build.sh vox_10_lucas <port> prep|stills|video 56`, `src/mix.py`, then
`pipeline/explained/tools.py finish` (loudnorm −16 LUFS / −2 dBTP). Fetch list: `fetch/vox_10_lucas.txt`.
