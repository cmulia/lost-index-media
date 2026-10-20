# what if no. 03 · What if the internet switched off for one hour?

Silent 50 s short (1080×1920, 30 fps) in a new 2D kinetic-typography style: off-white editorial page, Inter Display
+ IBM Plex Mono, yellow highlighter labels, browser windows with yellow title bars, a pixel cursor, typewriter text,
split-screen wipe, a dotted world map with undersea cables drawing on, notification flood. No AI imagery; every
frame is HTML/SVG rendered for this video (`src/scene.html`, `src/render.mjs`).

## Beats
| t (s) | scene |
|---|---|
| 0–4.6 | title card + Wi-Fi icon that cuts out |
| 4.6–10.6 | 11:59:57 → 12:00:00, maps / messages / checkout windows glitch to offline |
| 10.6–17 | IN ONE HOUR OFFLINE: ≈16 billion emails · ≈30 million Visa payments · maps, chats, card machines go quiet |
| 17–23 | split screen: card terminal DECLINED / departures board DELAYED |
| 23–33.4 | twist: "The internet isn't in the sky." map of cables; ≈99% of data crossing oceans; ≈570 cables; cable cross-section, "about as thick as a garden hose" |
| 33.4–41 | real outages: Meta 4 Oct 2021 (~6 h); CrowdStrike 19 Jul 2024 (≈8.5 M PCs, 4,000+ flights cancelled) |
| 41–46.6 | 13:00:00 Back online, notification flood (incl. "Bucket Hat Guy" 👀) |
| 46.6–50 | This is fiction. The cables are real. |

## Facts and sources
- Emails: Radicati Group, Email Statistics Report 2024–2028 (exec. summary): ≈392.5 B/day forecast for 2026 → ≈16 B/hour (our division). Forecast; counts sent + received.
- Visa: Fiscal 2025 Annual Report, 257.5 B processed transactions → ≈30 M/hour average (our division).
- Undersea cables: TeleGeography, "Do submarine cables account for over 99% of intercontinental data traffic?" (2023) and Submarine Cable FAQ ("as wide as a garden hose"); ≈570 in service (TeleGeography, Feb 2025).
- Meta outage: Meta Engineering, "More details about the Oct. 4 Facebook outage" (5 Oct 2021).
- CrowdStrike: Microsoft blog (20 Jul 2024, ≈8.5 M devices); CrowdStrike RCA (Channel File 291); Cirium: 4,295 flights cancelled by 17:00 London, 19 Jul 2024 (via NBC).

## Rights
- All graphics drawn for this video. Map: Natural Earth land (public domain) via world-atlas (ISC), d3-geo (ISC). Map and cable cross-section are labelled schematic.
- Fonts: Inter Display, IBM Plex Mono (SIL OFL).
- Sound effects and music: ElevenLabs (flow "lost_index · what if 03 · internet off"). Mix: `src/mix.py`.
