# NEXUS OPS Field Command v2.1 — CLEAN audit

Source: `workspace/user/files/Pasted_text-2.txt` (2,098 lines), preserved intact as `original.html`.
Cleaned: `nexus-ops-v2.1-clean.html` (112,076 bytes), built by `build_clean.py` (explicit replacements only — it fails loudly on any missed match).
Icons: `icons/icon-180.png`, `icon-192.png`, `icon-512.png` (real PNGs, NEXUS shield/N) + `manifest.json`.
Status: **cleaned locally only. NOT published, NOT pushed to GitHub, NOT live.** No deploy decision made.

## Defects found in the paste

1. Banned branding: `godmode2025.net` — 2 hits (header `@AntManThePro • godmode2025.net`, export footer). `TwistedGenius`: 0 hits.
2. Fake counts everywhere: "47 CREWS ONLINE" vs 8 crews in the roster array; KPI crew 24/28 vs 8; "142 EVENTS • 31 DAYS" vs 6 seed events; "47 events processed today" vs 6; incidents KPI added `+ 5 // + historical flavor`; event-count days were `events.length / 4.2`.
3. Urgency formula mismatch: the Alert Forge panel shows `(severity² × 1.8) + (minutes ÷ 4.2) + (risk × 11) − (ack ? 28 : 0)`, the code used `1.85 / 4.1 / ×12 / −29`.
4. Demo data with no label and no off switch: INJECT EVENT, the 12.5s live simulation (22% chance per tick), and Overnight Sync all invented random/canned events in a real record tool. Seed events were presented as real.
5. `deployNewPolicy()` ignored the trigger-type chips and hardcoded `["NO_CALL", "VIOLATION"]`.
6. Canvas sizing: fixed `width`/`height` attributes, no `devicePixelRatio`, no resize handler. Charts/map drew at backing-store size.
7. Trend chart: hardcoded values `[14, 9, 17, 11, 22, 15, 19]`, projection `[21, 24]`, labeled "NEXUS PREDICT … CONF 81%".
8. Dead end: crew KPI drill showed "would open here in production build."
9. PWA install banner called `deferredPrompt.prompt()` with no guard — crashes if the prompt never fired.
10. Export report: mean response divided by all events instead of resolved-with-time events; footer carried the banned domain.
11. External avatar: DiceBear URL for the header avatar. Fake console log claiming an icon at `/artifacts/imagine_images/5s2hF.jpg` (no such file in the paste).
12. Note timestamps were not revived on load (JSON round-trip left them strings).

## Fixes made

- Banned branding: 0 hits in the clean file (grep verified).
- All counts now compute from the actual data: crew = roster length (8), incidents = events in the file, event-count = real day span from timestamps, footer = events in the file.
- Urgency code now matches the displayed v2.4 formula exactly.
- Demo Mode toggle (header, persisted, OFF by default): gates INJECT DEMO EVENT, live-simulation injection, and Overnight Sync. Seed events and every demo-created event are marked `demo:true` and shown with a DEMO pill in the feed and table, plus a DEMO count in the archive header. Overnight Sync off-demo logs the skip and adds nothing.
- Real LOG EVENT form/modal (crew dropdown from the roster, type, severity 1–5, details required) saves a non-demo event. `N` key opens it when Demo Mode is off, injects demo when on.
- `deployNewPolicy()` now reads the chips it shows; deploying with none selected is refused.
- Canvases: `fitCanvas()` reads `clientWidth`/`clientHeight`, multiplies by `devicePixelRatio`, draws in design-pixel coords (520×340 map, 460×240 charts), plus a debounced resize redraw. Draw functions guard a null 2d context instead of throwing.
- Trend chart labeled SAMPLE / ILLUSTR., "not a forecast"; type-chart labels fixed (`/_/g`).
- Crew KPI drill now opens a real roster modal (8 crew, role, site, risk).
- PWA prompt guarded; fake icon console log removed; header avatar is the local icon; export footer is clean and the mean-response math uses resolved-with-time events only.
- localStorage key bumped to `nexusOpsState_v21_clean` with a one-time migration from the old `nexusOpsState_v21` key; note timestamps revived on load.
- Title/meta/splash/boot/report strings say v2.1 CLEAN, not v2.1.

## Verification (local, 2026-11-06 evening)

- `node --check` on the extracted inline script: PASS.
- Served locally, HTTP 200 for the HTML (112,169 bytes), manifest, and icon-192.
- jsdom harness (`/tmp/v21-harness.js`, jsdom 31): **20/20 checks passed** — boot, 6 demo seeds, KPIs 8 / 6, urgency 55 matches the displayed formula for the open sev-4 Marcus Hale event, demo OFF inject/sync create nothing, demo ON inject/sync create DEMO-marked events, real LOG EVENT saves non-demo, policy deploy reads chips, clean-key persistence, legacy key not written, empty state (0 events, no crash), 390px resize, canvas null-context guard. jsdom has no 2d canvas context, so canvas drawing itself was verified only as "does not throw" — see below.
- Known engine behavior kept, not a bug I introduced: injecting or syncing an event that pushes a crew over a policy threshold also creates a POLICY_ALERT event (e.g. Marcus Hale hits 2× NO_CALL), so one injection can add 2 events. Both are DEMO-marked.

## Left unproven / still needs a real phone test

- Real-browser render (Tailwind CDN, Font Awesome, canvas map/charts at phone width, PWA install prompt) — jsdom cannot prove this. The tactical map zones are drawn in a fixed 520×340 design space scaled to fit, so check the map on a phone: zones must not look cramped at ~390px.
- No live deploy: nothing pushed, no Netlify site linked. If Anthony wants it live, that is a separate decision (new repo or a page next to the v2.2 CLEAN build — do not overwrite the v2.2 clean file or the live QA Brain).
- The 8-crew roster and 6 seed events are still demo data, just labeled now. Real crew names / real events have to come from Anthony — nothing here is connected to FieldPulse.

## Post-live-check fix (2026-11-19)

The fresh live load caught two static labels the first audit missed:
- Incidents card pills said "4 OPEN" / "5 RESOLVED" (static HTML, never updated). Real seed counts are 3 open-or-acknowledged / 3 resolved. Fixed: pills now carry `kpi-open` / `kpi-resolved` ids and `updateKPIs()` writes the computed counts, so they stay honest as events change.
- Tactical map badge said "LIVE • 47 NODES". The map draws 6 crew positions. Fixed to "LIVE • 6 POSITIONS".
Both fixes are in `build_clean.py`, so a rebuild reproduces them. Re-verified locally (syntax + jsdom harness) and re-checked on the live page after redeploy.
