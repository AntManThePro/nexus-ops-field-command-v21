# NEXUS OPS // Field Command v2.1 CLEAN

A separate live page. It does **not** replace the v2.2 CLEAN build
(`workspace/nexus-ops-clean/nexus-ops-master-v2.2-clean.html`) and it does
not touch the live QA Brain.

## What it is

A single-file crew discipline dashboard — the older v2.1 cut, cleaned up:

- **Command Deck** — KPI cards plus a canvas tactical map (Alpha-7 / Bravo-2 / Charlie-9)
- **Event Archive** — searchable table for No-Call, Violation, Attendance, Resignation events, with ACK / Resolve
- **Alert Forge** — urgency score per open event, highest first
- **Response Analytics** — incidents-by-type chart and a response-time trend
- **Policy Nexus** — 3 seed policies plus a deploy-new-policy form

## Data

- Local file, localStorage only. No backend, no FieldPulse link, no live crew data.
- Saves under localStorage key `nexusOpsState_v21_clean` (one-time migration from the old `nexusOpsState_v21` key). Reset Demo State wipes it.
- The 8-crew roster and 6 seed events are **demo data, labeled DEMO**.
- Demo Mode toggle (off by default) gates random injection, the live simulation, and the overnight sync. Real entries go through the LOG EVENT form and are saved non-demo.
- The trend chart is sample data, labeled SAMPLE — not a forecast.

## Files

- `index.html` — cleaned copy (audit fixes applied, see below)
- `nexus-ops-v2.1-original.html` — the pasted original, untouched
- `AUDIT.md` — full defect list, fixes, and what is still unproven
- `build_clean.py` — the script that built the clean file from the original (explicit replacements only)
- `manifest.json`, `favicon.ico`, `icons/` — custom NEXUS shield/N icon set

## Audit fixes in the cleaned copy

- Banned `godmode2025.net` branding stripped (0 hits left)
- Counts compute from the actual data: crew = roster length (8), incidents = events in the file, no more "47 crews" or incidents +5
- Urgency code aligned to the displayed v2.4 formula
- Demo Mode toggle off by default; demo events marked DEMO in the feed, table, and archive header
- Real LOG EVENT form (crew, type, severity 1–5, details required)
- `deployNewPolicy()` reads the trigger-type chips instead of hardcoding them
- Canvases sized by `clientWidth`/`clientHeight` × `devicePixelRatio`, with a resize redraw and a null-context guard
- Trend chart labeled SAMPLE; type-chart labels fixed
- Crew KPI drill opens a real roster instead of a dead-end message
- PWA install prompt guarded; fake icon console log removed; header avatar is the local icon
- Export report: mean response uses resolved-with-time events only, footer is clean
- Note timestamps revived on load

## Easter egg

In fine small print at the bottom of the page: the caped ant in the hard hat hides in the keyboard — N for a demo event (or the real Log Event form when Demo Mode is off), ? for Alert Forge, Cmd/Ctrl+S for the demo overnight sync.

## Deploy

- Branch: `main`, publish directory: root, build command: none
- Intended as a private Netlify site under Team login, like the other NEXUS manager sites — not public.
- Live site: https://nexus-ops-field-command-v21.netlify.app/

## Verification (2026-11-06, local; publish edits re-checked 2026-11-19)

- JS syntax check passes; local serve HTTP 200 for the page, manifest, and icons
- jsdom harness: 20/20 checks passed (boot, 6 demo seeds, KPIs 8 / 6, urgency matches the displayed formula, demo OFF creates nothing, demo ON marks everything DEMO, real log saves non-demo, policy deploy reads chips, clean-key persistence, empty state, 390px resize, canvas null-context guard)
- Real-phone render still needed
