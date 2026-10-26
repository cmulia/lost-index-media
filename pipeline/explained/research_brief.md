# Research + script brief — "explained" series (@lost_index)

You are researching and scripting ONE 50–58 s vertical explainer Short about a film director. Output is a single JSON file
(path given in your task). Work carefully; every claim must be verifiable. Budget: at most 20 WebSearch calls and 8 WebFetch calls.

## Tone and structure
Calm, precise, curious, lightly wry (Vox-style), female narrator. ONE true, surprising, well-sourced story, 1–2 fun facts,
ending on a QUIET TWIST (the last line reframes the story). Short sentences.
- Hook: the FIRST sentence states the surprising claim itself in under 3 s spoken (≤ 9 words). Not a scene-setter.
- Narration 125–140 words (count them), 8–10 beats, each beat 1–3 sentences. Numbers spelled out as spoken
  ("nineteen seventy-five", "twenty-five million dollars"). Avoid words a speech synth will mangle; no abbreviations.
- Hedge anything disputed or single-sourced: "he says", "his producer remembers", "the story goes".
- Never invent quotes. Quote only what a reliable source actually quotes, and keep quotes short.
- No tool names anywhere. No mention of AI.

## Sourcing (hard rule)
Every factual claim must map to at least one reliable source (major newspapers/magazines, studio/festival/academy pages,
books by reputable publishers, museum/archive pages, well-known interviews on record). Wikipedia is a starting point only —
follow its citations and verify the underlying source. If you cannot source a claim, DROP it from the narration.
List for each beat which source(s) back it.

## Images (Wikimedia Commons only)
Find 4–6 photos on commons.wikimedia.org: 2–3 of the director (different eras if possible) and 2–3 real places/objects
relevant to the story (a theatre, a location, a camera model, a prop replica in a museum, etc.). Licence must be one of:
public domain, CC0, CC BY (any version), CC BY-SA (any version). NO "fair use", no film stills, no posters, no logos.
For each give: Commons File: page URL, direct upload.wikimedia.org URL (original or /thumb/.../1600px- form), author, date,
licence (exact template name you saw, e.g. "cc-by-sa-4.0", "PD-USGov", "cc-zero"), what it shows, suggested use.
WebFetch each File: page (append ?action=raw to get wikitext) to CONFIRM the licence template before listing it.
Ask yourself: does this image show a living private person as the subject? If so skip it.

## Deliverable JSON (exact keys)
{
  "slug": "<lowercase surname>",
  "episode_no": "0N",
  "subject": "Full Name",
  "hook": "first sentence",
  "twist": "one-line description of the quiet twist",
  "mood": "2–3 sentences on the visual mood you recommend (palette, illustration style, era texture) and the music style (genre, tempo, instruments) that fit this story. Must differ from: risograph/funk (no.01), dark rainy editorial/baroque (no.02).",
  "narration": "full narration text, 125–140 words",
  "beats": [ {"i":0, "text":"exact sentence(s) of narration for this beat (concatenating all beat texts, with single spaces, must equal narration exactly)", "visual":"what is on screen (illustrated prop / photo key / diagram)", "sources":["S1"]}, ... ],
  "fun_facts": ["..."],
  "sources": {"S1": {"name":"Publication, title, year", "url":"https://..."}, ...},
  "images": [ {"key":"short_key", "file_page":"https://commons.wikimedia.org/wiki/File:...", "direct_url":"https://upload.wikimedia.org/...", "author":"...", "date":"...", "licence":"cc-by-sa-4.0", "shows":"...", "use":"hero photo / place / object"} ],
  "props_to_illustrate": ["6–8 short descriptions of objects/scenes (NO people, no film stills, posters, logos, Oscar statuettes) to generate as illustrations, each 9:16, e.g. 'a wooden katana on a stand', 'a mechanical shark skeleton on a barge'"],
  "captions": {
    "tiktok_caption": "short, 2–4 sentences with one emoji, then blank line, either/or question + 👇, blank line, 'explained no. 0N', blank line, 4–6 hashtags",
    "instagram_caption": "long: hook line + emoji, 3–5 short paragraphs telling the story with the fun facts and the twist, the either/or question + 👇, 'explained no. 0N', then a line '—', a line starting 'Sources: ' listing publications (name, year), a line starting 'Images via Wikimedia Commons: ' crediting photographers + licences, then 'Illustrations and diagrams drawn for this video.', then 6–8 hashtags",
    "youtube_title": "≤ 70 chars incl. ' #shorts'. Search-friendly: plain subject + key noun/year, no teaser. e.g. 'How Spielberg hid the broken shark in Jaws (1975) #shorts'",
    "either_or_question": "e.g. 'Practical or CGI?'"
  },
  "dropped_unverified": ["claims you considered and cut, with why"]
}
Write the JSON with Python (json.dump, ensure_ascii=False, indent=2) so it is valid. Then re-open it and check: narration word
count is 125–140; beats join to narration exactly; every caption ends with the question + 👇 and the 'explained no. 0N' line;
no tool names. Print the final word count and the hook.
