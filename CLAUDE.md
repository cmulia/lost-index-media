# @lost_index media repo

This repo makes and schedules the @lost_index mini-documentaries (TikTok `lost_index`, Instagram `lost_index_ig`).
Each video is "file no. NNN": an ~85–95 s vertical (1080×1920, 30 fps) true story with a quiet twist,
real archival images, original diagrams, ElevenLabs narration + sound effects, and a score.

## Layout

```
episodes/BRIEF.md               style + sourcing rules for research/scripts (read it)
episodes/BACKLOG.md             topic queue; take the first unchecked line of the next category in rotation
episodes/NNN_slug/
  script.json                   beats, captions, assets, post captions, facts (shape: see any existing episode)
  README_captions_sources_rights.md
  diagrams.py                   original animated diagrams (DIAGRAMS = {...}), uses pipeline/lostindex/diag.py
  music.json                    score spec for pipeline/lostindex/music.py (until ElevenLabs music is available)
  sfx_plan.json / sfx.json      ElevenLabs sound effects per beat
  assets/                       fetched images (+ assets/_pages/*.html = Commons wikitext for licence checks)
  audio/narration.mp3           chosen ElevenLabs take (take_1..4.mp3 kept), audio/sfx/bNN.mp3
  render/lost_index_NNN_slug.mp4 + contact_sheet.png
fetch/NNN_slug.txt              "<dest path> <url>" lines; pushing them triggers .github/workflows/fetch-assets.yml
pipeline/render.py              renderer (python3 pipeline/render.py episodes/NNN_slug [--stills t1,t2])
```

## Making one episode (what the daily scheduled task does)

1. **Topic.** Rotate categories in this order and pick the first unchecked item of the next category in
   `episodes/BACKLOG.md`: sound → screens & media → money & markets → tech → space. Check it off when scheduled.
   Next file number = highest existing `episodes/NNN_*` + 1.
2. **Research + script** (use a subagent; WebSearch budget is 200 calls per turn shared by all agents).
   Follow `episodes/BRIEF.md`. Every claim needs a reliable source; cut what can't be verified; hedge disputed
   stories ("say", "remembers it differently"). Narration 185–215 words, numbers spelled out. 13–16 beats.
   Concatenated beat texts must equal the narration exactly.
3. **Images.** Wikimedia Commons / NASA, public domain or CC0/CC BY/CC BY-SA only. This environment cannot
   reach those hosts, so write `fetch/NNN_slug.txt` with `episodes/NNN_slug/assets/<key>.jpg <upload.wikimedia.org url>`
   plus `episodes/NNN_slug/assets/_pages/<key>.html <commons File: page url>?action=raw` and push. The workflow
   rewrites Commons URLs to `Special:FilePath` (direct links 404 from runners), commits the files, and writes
   `fetch/last_run.log`. Poll `gh api repos/cmulia/lost-index-media/actions/runs`, then `git pull`.
   Confirm each licence template in the `_pages/*.html` wikitext before use. Crop/split scans with PIL when needed
   and record it in `assets` (`derived_from`, `changes`).
4. **Narration** with ElevenLabs `creative_generate_speech`, model `eleven_v4`, default 4 takes. Pick the median-length
   take (a subagent can poll/download; signed URLs on storage.googleapis.com are reachable). Voices used so far —
   pick one that suits the story and vary them:
   George `JBFqnCBsd6RMkjVDRZzb` (warm British storyteller), Kurt `42MPlPHxazRyNGWpSUyy` (wry American),
   Lily `pFZP5JQG7iQjIQuC4Bku` (velvety British newsreader), Jade `TOXPlnYC7z5SQSV2Zgc5` (calm elegant American),
   Mark Vale `PXMcl9zGUnc9w7DofLWk` (deep cinematic American), Brian (used on 004/005), Daniel `onwK4e9ZLuTAKqWW03F9`
   (steady British broadcaster), Alice `Xb7hH8MSUJpSbSDYk0k2` (clear British educator), Tom `TkBXFhNSp04NiWhhR7jP`
   (British documentary). Use `creative_list_voices` to find new ones.
5. **Sound effects**: 8–10 per episode in `sfx_plan.json` ({beat, prompt, gain, file}); generate with
   `creative_generate_in_flow` node_type `sfx`, model `eleven_text_to_sound_v2` (one flow per episode, default takes,
   never re-call to retry), download one take each, write `sfx.json`. Gains 0.28–0.5.
6. **Score**: `music.json` (bpm, root, progression, layers, texture, `swell_beat`). If the full ElevenLabs connector
   (music) is connected, generate a ~95 s instrumental bed instead and save it as `audio/music.mp3` — render.py
   uses it automatically.
7. **Diagrams**: write `diagrams.py` for beats with `"visual": {"type":"diagram","name":...,"panel":"dark|light","height":N}`.
   Label every drawing "schematic" / "illustration · drawn for this video".
8. **QC**: `python3 pipeline/render.py episodes/NNN_slug --stills ...` (one still per beat), look at them, fix,
   then full render (≈5 min). Check the contact sheet and that the mix reads ≈ −16 LUFS / −2 dBTP.
9. **Publish files**: commit the episode (videos are < 100 MB) and push to `main`. Public video URL:
   `https://raw.githubusercontent.com/cmulia/lost-index-media/main/episodes/NNN_slug/render/lost_index_NNN_slug.mp4`
10. **Schedule in Buffer** (organization "My organization" `6ad19c77eb2d5b90ec4ac866`):
    - TikTok `lost_index` channel `6ad19d37778b240e2f23725b`: `tiktok_caption`, video asset, schedulingType automatic.
    - Instagram `lost_index_ig` channel `6ad1b705778b240e2f250120`: `instagram_caption`, video asset,
      metadata.instagram {type: "reel", shouldShareToFeed: true}.
    - mode `customScheduled`, dueAt **18:00 Australia/Sydney** on the next free day (one video per day).
      The free Buffer plan allows 10 scheduled posts = 5 days × 2 channels, so schedule the new episode for the day
      after the last scheduled one, and only if fewer than 10 posts are scheduled.
    - isAiGenerated stays false (narration is credited in the caption), matching earlier posts.

## Style

Cream paper page (dark scenes for drama), header `file no. NNN` / `@lost_index`, IBM Plex Mono typewriter captions,
Instrument Serif Italic headlines (it lacks ƒ → ≈; the renderer substitutes), archival plates with a boxed tag +
source credit + italic date, end card "file no. NNN". Fonts are in `pipeline/fonts` (SIL OFL).
