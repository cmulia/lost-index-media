# SFX + music brief (ElevenLabs Full connector, tools mcp__ElevenLabs_Full__*)

You are producing sound effects and one instrumental score for ONE episode. Inputs: an episode directory and a plan JSON
(`sfx_plan.json`) in it: {"episode": ..., "video_seconds": N, "music": {"prompt": "...", "duration_seconds": N+1},
"sfx": [{"file": "name", "prompt": "...", "duration_seconds": S}, ...]}.

Rules (strict — generations cost credits):
1. Load tool schemas first with ToolSearch: "select:mcp__ElevenLabs_Full__creative_create_flow,mcp__ElevenLabs_Full__creative_add_flow_node,mcp__ElevenLabs_Full__creative_run_flow_nodes,mcp__ElevenLabs_Full__creative_get_flow_run_status,mcp__ElevenLabs_Full__creative_get_flow,mcp__ElevenLabs_Full__creative_get_model_schema".
2. Create ONE flow for the episode (creative_create_flow, name "explained no. 0N <slug> audio"). Reuse its flow_id for everything.
3. Add every SFX node with creative_add_flow_node: node_type "sfx", model_id "eleven_text_to_sound_v2", prompt = the plan's prompt,
   model_parameters {"duration_seconds": S} (ALWAYS set it explicitly; if the schema uses a different key name, check creative_get_model_schema once and use that key), label = file name.
   Add the music node: node_type "music", model_id "eleven_music_v2_5", prompt = plan prompt,
   model_parameters {"duration_seconds": N+1, "instrumental": true, "lyrics_type": "instrumental"} (check creative_get_model_schema for exact key names if a run complains).
4. Run nodes with creative_run_flow_nodes in WAVES OF AT MOST 3 node_ids per call. For SFX pass generations_count 1. For the music node pass generations_count 1 (one score take only).
   Poll creative_get_flow_run_status with the session_ids, waiting poll_after_seconds, until all_completed or has_failures.
   NEVER run a node twice. If a node fails, record it and move on (do not retry).
5. Collect each generation's audio URL (storage.googleapis.com signed URLs are reachable with curl; the CloudFront/other hosts are not).
   Download with: curl -sS -L -o <dest> "<url>". SFX → <episode>/audio/sfx/<file>.mp3 (take 1). Music: download the take (if two exist, both) to
   <episode>/audio/music_take1.mp3 and music_take2.mp3, measure each with `ffprobe -v error -show_entries format=duration -of csv=p=0`,
   copy the one whose length is closest to N+1 to <episode>/audio/music.mp3 (keep both takes).
   If a URL is not an mp3 (wav/other), still save it with the right extension and then convert to mp3 with `ffmpeg -nostdin -y -loglevel error -i in -c:a libmp3lame -b:a 192k out.mp3`.
6. Write <episode>/sfx.json: {"flow_id": ..., "sfx": {file: {"node_id":..., "duration": measured_seconds, "url": ...}}, "music": {...}}.
7. Report: the flow_id, a table of file → measured duration, any failures. Do not describe the audio; just the facts.
