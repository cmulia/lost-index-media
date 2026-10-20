# @lost_index media repo

This repo makes and schedules the @lost_index mini-documentaries (TikTok `lost_index`, Instagram `lost_index_ig`).
Each video is "file no. NNN": a 45–60 s vertical (1080×1920, 30 fps) true story with a quiet twist,
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
   `episodes/BACKLOG.md`: sound → screens & media → money & markets → tech → space. Sound stories perform best:
   when a sound item fits, prefer one with something to *hear* (and let the SFX carry it). Check it off when scheduled.
   Next file number = highest existing `episodes/NNN_*` + 1.
2. **Research + script** (use a subagent; WebSearch budget is 200 calls per turn shared by all agents).
   Follow `episodes/BRIEF.md`. Every claim needs a reliable source; cut what can't be verified; hedge disputed
   stories ("say", "remembers it differently"). Narration 120–140 words (45–60 s), numbers spelled out, 8–11 beats.
   Hook: the first sentence states the surprising claim in under 3 s; beat 0 has the strongest image and a `big`
   headline (the renderer shows beat 0 fully on frame one — no fade-in). Captions end with a short question (👇).
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
6. **Score**: use the full ElevenLabs connector (`mcp__ElevenLabs_Full__*`): add a `music` node, model
   `eleven_music_v2_5`, model_parameters `{"duration_seconds": <video length rounded up>, "instrumental": true,
   "lyrics_type": "instrumental"}`, a 1–3 sentence sound-only prompt (genre, mood, instruments, tempo, how it evolves),
   run with default takes, save the take closest in length as `audio/music.mp3` (render.py uses it automatically;
   optional `"file_level"` in music.json, default 0.20). Render once first without music to learn the exact length.
   Fallback if that connector is missing: `music.json` spec for the built-in composer (bpm, root, progression, layers,
   texture, `swell_beat`).
7. **Diagrams**: write `diagrams.py` for beats with `"visual": {"type":"diagram","name":...,"panel":"dark|light","height":N}`.
   Label every drawing "schematic" / "illustration · drawn for this video".
8. **QC**: first `pip install pocketsphinx` (its English model is inside the wheel; HuggingFace/Whisper model hosts are
   blocked here). `pipeline/lostindex/align.py` force-aligns the script to the narration word by word, so beats start on
   their first spoken word and captions type in sync with the voice. After any render, `timing.json` must say
   `"aligned": "pocketsphinx"`; if it doesn't (stderr says why), fix the words it couldn't align before publishing —
   the fallback timing drifts by seconds. Then `python3 pipeline/render.py episodes/NNN_slug --stills ...` (one still
   per beat), look at them, fix, then full render (≈5 min). Check the contact sheet and that the mix reads ≈ −16 LUFS / −2 dBTP.
   Never run git commands (pull/rebase/autostash) while a render is writing its mp4.
9. **Publish files**: commit the episode (videos must stay < 100 MB; render.py caps video at 4.5 Mb/s) and push to
   `main`. Use a commit-pinned public URL for Buffer (raw.githubusercontent caches a 404 on `main` paths for minutes):
   `https://raw.githubusercontent.com/cmulia/lost-index-media/<full commit sha>/episodes/NNN_slug/render/lost_index_NNN_slug.mp4`
   and check it returns HTTP 200 with the right content-length before scheduling.
10. **Schedule in Buffer** (organization "My organization" `6ad19c77eb2d5b90ec4ac866`):
    - TikTok `lost_index` channel `6ad19d37778b240e2f23725b`: `tiktok_caption`, video asset, schedulingType automatic.
    - Instagram `lost_index_ig` channel `6ad1b705778b240e2f250120`: `instagram_caption`, video asset,
      metadata.instagram {type: "reel", shouldShareToFeed: true}.
    - YouTube `Lost Index` channel `6ad1beaa778b240e2f2551bf` (Shorts): `instagram_caption` with `#shorts` as the
      first hashtag, video asset, metadata.youtube {title: "<search-friendly title, ≤ 70 chars> #shorts", categoryId: "27",
      privacy: "public", madeForKids: false, notifySubscribers: true, embeddable: true, license: "youtube",
      isAiGenerated: false}. YouTube is the strongest channel and Shorts are found through search, so the title
      names the subject plainly with a year or key noun people would type ("The first photo of Earth from space
      (1946, V-2 rocket)", "Why Blockbuster turned down Netflix for $50 million"), not a teaser.
    - mode `customScheduled` on the next free day, timed to the **US Eastern evening peak** (all three platforms'
      2026 best-time studies put Shorts/Reels/TikTok engagement at 18:00–23:00 audience-local time):
      YouTube + Instagram at **19:00 US Eastern**, TikTok at **21:00 US Eastern** (TikTok's evening window peaks later).
      In Sydney time that is YouTube/Instagram **10:00** and TikTok **12:00** until 1 Nov 2026 (EDT), then **11:00** and
      **13:00** from 2 Nov 2026 (EST) until US clocks change again on 8 Mar 2027 (back to 10:00/12:00). Always write dueAt
      with the Sydney offset (+11:00 in AEDT). One video per day; never schedule two different videos for the same day.
      Keep about 5 days queued: schedule the new episode for the day after the last scheduled one, and skip if 5 or
      more days are already queued. Timing is a test (set 21 Oct 2026, based on <1 week of data where content, not
      time, explained the differences): after 2–4 weeks, check each platform's audience-location/active-hours
      analytics and compare TikTok 12:00 vs earlier 10:00 posts before changing it again.
    - Captions never name the tools used to make the video (no "ElevenLabs", "Higgsfield", "Kling", "GPT Image",
      no "narration voiced with…" lines). Keep sources, image credits/licences and "drawn for this video" notes.
    - isAiGenerated: false when the visuals are archival/drawn (history files), true when the visuals themselves are
      AI-generated (e.g. Higgsfield images/clips), so the platform's own AI label stays accurate.

## Style

Cream paper page (dark scenes for drama), header `file no. NNN` / `@lost_index`, IBM Plex Mono typewriter captions,
Instrument Serif Italic headlines (it lacks ƒ → ≈; the renderer substitutes), archival plates with a boxed tag +
source credit + italic date, end card "file no. NNN". Fonts are in `pipeline/fonts` (SIL OFL).
