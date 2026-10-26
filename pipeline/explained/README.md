# Runbook: one "explained" Short per run (credit-efficient)

This is the prompt the daily scheduled task follows. One run = ONE episode, start to finish, in a fresh session.
For this series these rules override the "file no." steps in CLAUDE.md (narration voice/tool, isAiGenerated, the
"skip if 5 days are queued" rule). Everything else in CLAUDE.md still applies (sourcing, captions never name tools,
commit-pinned URLs, never run git while a render writes its mp4).

## 0. Decide whether to run
- Clone if needed: `git clone --depth 1 https://github.com/cmulia/lost-index-media` (attach the repo first if the session lacks it).
- Open `episodes/EXPLAINED_BACKLOG.md`. Take the first unchecked line → number NN, slug (lowercase surname), target date.
- Buffer (org `6ad19c77eb2d5b90ec4ac866`): `execute_query posts(filter:{status:[scheduled]})`. If a video is already scheduled
  on the target date, or the backlog has no unchecked lines, or every line through 16 Nov 2026 is done: stop and say so.
- Target date must be in the future and must be the day after the last scheduled video (never two videos on one day).

## 1. Research + script — ONE subagent, model "sonnet"
- `Agent(model: "sonnet")` with `pipeline/explained/research_brief.md`, the backlog angle, episode no. NN, output
  `$EXPLAINED_SCRATCH/research/vox_NN_<slug>.json`. Budget in the brief: ≤ 20 WebSearch, ≤ 8 WebFetch.
- Narration 125–135 words (that lands 50–56 s with Quinn). Hook under 3 s. Hedge disputed claims. Drop what isn't sourced.
- You (main) read only the JSON summary fields you need (hook, narration, beats, images, captions). Don't re-research.

## 2. Visuals — Higgsfield (keep it lean)
- `generate_image_batch` model `gpt_image_2_5`, **6** props at 9:16 in ONE call, a style that fits the topic and differs
  from earlier episodes (01 risograph, 02 dark rainy editorial, 03 gouache sketchbook, 04 1970s Kodachrome seaside,
  05 Saul Bass monochrome + red, 06 navy blueprint, 07 parchment copperplate). No people, no real likenesses, film stills,
  posters, logos or Oscar statuettes. Prompts always end "no people, no text, vertical composition".
- `remove_background` on **1** prop (sticker cutout).
- `generate_video_batch` model `kling3_0`, mode "pro", 9:16, duration 5, sound "off",
  declined_preset_id "24bae836-2c4a-48e0-89b6-49fcc0b21612", start_image = image job_id, prompt starts
  "Keep the illustration style exactly, no people, no text. Very subtle motion only: …". **3 loops** total, 2 per call max.
- Make ONE 4×2 thumbnail sheet of the props (PIL) and look at it once. Don't view props one by one.
- CloudFront result URLs are downloadable directly with curl here; still list them in `fetch/vox_NN_<slug>.txt` for provenance.

## 3. Commons photos — fetch workflow
- Write `fetch/vox_NN_<slug>.txt` (image URL + `assets/_pages/<key>.html <File: url>?action=raw`), commit + push with the
  episode's assets in ONE commit, then wait for the `fetch-assets` run (one `until` loop with `gh api …/actions/runs`,
  not repeated polls), `git pull --rebase`, confirm every licence template with one grep over `_pages/*.html`.

## 4. Narration — Higgsfield text2speech_v2
- `generate_audio_batch`: model `text2speech_v2`, variant "elevenlabs", voice_type "preset".
  **2 takes**: Quinn `80914268-dfae-4f76-8306-36f2d55f58f8` + one alternate (Vesper `c3204739-4084-41a3-9dc5-c805b307ec18`).
- `pip install --break-system-packages -q pocketsphinx`, then `python3 -I pipeline/explained/caps_build.py align narration.txt take1.mp3 take2.mp3`.
  Pick Quinn if 50–56 s; if 56–58.5 s use `ffmpeg -af atempo=1.04` and re-align; if longer, trim the script ~10 words and make
  one more Quinn take (never more than 3 takes total).
- Write caption lines (3–6 words, break at commas/clauses), then `caps_build.py caps …` (asserts the lines rejoin exactly).

## 5. SFX + score — ONE subagent, model "sonnet"
- Write `episodes/vox_NN_<slug>/sfx_plan.json` (10 SFX, explicit durations; one music prompt, duration = video length + 1).
- `Agent(model: "sonnet")` with `pipeline/explained/sfx_brief.md`. One flow, waves of ≤ 3, generations_count 1 everywhere
  (one score take), never re-run a node. Launch it right after the script is final, in parallel with visuals.

## 6. Scene + render
- Copy the closest earlier `src/scene.html` (read ONE reference only) and restyle; `renderAt(t)` deterministic, returns a promise.
  Header "EXPLAINED NO. NN" / "@LOST_INDEX", beat 0 fully visible on frame one, credits on every photo,
  "schematic · drawn for this video" on drawn diagrams, end card = either/or question + small sources/credits footer.
- `pipeline/explained/build.sh vox_NN_<slug> <port> prep`, then `stills "t1,…"` (one per beat) → look at `stills_sheet.jpg`
  ONCE, fix everything you see in one edit pass, re-render only the changed stills ONCE. No third pass unless something is broken.
- `build.sh … video <dur>` as a background job (≈ 12–15 min on 2 cores; never two renders at once). Only after it prints
  RENDER_DONE: `src/mix.py` (adapt an earlier one; cumsum moving-average ducking) then
  `python3 -I pipeline/explained/tools.py finish <scratch>/vox_NN_<slug> episodes/vox_NN_<slug> explained_NN_<slug>.mp4 <dur>`
  (two-pass loudnorm I=-16 TP=-2 linear + alimiter 0.70; x264 4.5 Mb/s, AAC 192k, faststart). Must report ≈ −16 LUFS, TP ≤ −2.
- Look at `render/contact_sheet.png` once.

## 7. Publish + schedule
- Copy render.mjs/runall.sh into `src/`, write `captions.json` (from the research JSON; YouTube description = Instagram caption
  with `#shorts` first in the hashtag line) and `README_captions_sources_rights.md` (short: beats, narration, sources, image table,
  AI disclosure, build). Tick the backlog line. Commit + push everything (no untracked files).
- Pinned URL `https://raw.githubusercontent.com/cmulia/lost-index-media/<sha>/episodes/vox_NN_<slug>/render/explained_NN_<slug>.mp4`
  must return 200 with the right size.
- `create_post` ×3, mode customScheduled, schedulingType automatic, dueAt with +11:00
  (from 2 Nov 2026: YouTube + Instagram 11:00, TikTok 13:00):
  - YouTube `6ad1beaa778b240e2f2551bf`: text = instagram caption with `#shorts` first; metadata.youtube {title (≤ 70 chars,
    plain subject + key noun/year + " #shorts"), categoryId "27", privacy "public", madeForKids false, notifySubscribers true,
    embeddable true, license "youtube", isAiGenerated true}.
  - Instagram `6ad1b705778b240e2f250120`: instagram caption; metadata.instagram {type "reel", shouldShareToFeed true, isAiGenerated true}.
  - TikTok `6ad19d37778b240e2f23725b`: tiktok caption; metadata.tiktok {isAiGenerated true}.
- Send the mp4 to the user (SendUserFile) with one line: episode, hook, date/times, length, LUFS.

## Credit rules (why this is cheap)
- One episode per fresh session. Keep the conversation short: no file dumps, `head`/`grep` instead of reading big files,
  one stills sheet + one re-check + one contact sheet, no repeated polling (use one background `until` loop per wait).
- Subagents on Sonnet for research and audio. Higgsfield per episode ≈ 34 credits (6 images, 1 cutout, 3 loops, 2–3 takes).
  ElevenLabs per episode ≈ 1,000 credits (10 SFX + 1 score take).
- Never regenerate to "try again" unless the asset is unusable; say what was regenerated and why in the summary.
