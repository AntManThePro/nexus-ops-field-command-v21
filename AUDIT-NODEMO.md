# NEXUS OPS Field Command v2.1 — NO-DEMO audit

Source: `workspace/nexus-ops-v21-publish/index.html` (113,054 bytes,
GitHub `AntManThePro/nexus-ops-field-command-v21`, head `332fe8a`,
index.html blob SHA `081ad7000254ddca88970483ea34d981992b2a7d`).
Built by `build_nodemo.py` (explicit replacements only, aborts on a miss).
The source file is untouched.

## Removed entirely

- Demo toggle button and `toggleDemoMode()` / `updateDemoUI()` / `DEMO_KEY`
- `injectRandomEvent()` and the INJECT DEMO EVENT button
- `seedInitialData()` — all 6 seeded events (Marcus Hale, Diego "Reaper"
  Morales, Elena "Ghost" Ruiz, Liam "Forge" O'Connor, Priya "Spectre"
  Singh, plus the historical PPE event)
- `simulateOvernightSync()` — the 3 fictional overnight events — and the
  RUN OVERNIGHT SYNC button
- `startLiveSimulation()` / `toggleLiveMode()` and the LIVE MODE button —
  the 22% random-injection loop and the 35% KPI/chart jitter are gone
- `resetDemo()` and the RESET DEMO STATE button
- The 8-person fictional roster (Jax "Viper" Torres, Elena "Ghost" Ruiz,
  Marcus Hale, Priya "Spectre" Singh, Diego "Reaper" Morales, Sofia "Nova"
  Patel, Liam "Forge" O'Connor, Aisha Khan) with their invented risk scores
  and Alpha-7 / Bravo-2 / Charlie-9 sites
- The sample trend chart: hardcoded values [14, 9, 17, 11, 22, 15, 19],
  the illustrative 2-day projection, SAMPLE / ILLUSTR. legend
- The 6 hardcoded tactical-map positions and the hardcoded connection lines
- Every DEMO pill, DEMO count, and "demo data" label in the feed, table,
  export report, meta description, and Easter egg
- "CHAIN OF CUSTODY" / "immutable" claims — it is now the Audit Log,
  a local log only

## Fixed while stripping

- **Roster is real now:** starts empty, ADD CREW (prompt: name / role /
  site) adds a real crew member, saved in localStorage with the log.
  The Log Event form, roster modal, KPIs, and map all read that roster.
- **Policies no longer reset on reload:** `seedPolicies()` used to
  overwrite loaded policies with the 3 templates on every boot, so a
  deployed policy was lost. It now seeds only when the log has no policies.
- **Storage key bumped** to `nexusOpsState_v21_nodemo`, with migration
  from `nexusOpsState_v21_clean`: keeps real events, drops any
  `demo`-flagged event and the 6 exact seed IDs, resets the fictional
  roster to empty, logs one MIGRATION entry with kept/dropped counts,
  removes the old key. If demo events were dropped, the audit log is
  reset to that single MIGRATION entry so it never references deleted
  events.
- **End-of-Day Review** replaces overnight sync: counts open events,
  logs END_OF_DAY_REVIEW, updates "Last end-of-day review", never adds
  or changes anything. Bound to the hero button and Cmd/Ctrl+S.
- **Clear All Data** replaces Reset Demo: confirm dialog, deletes the
  new key, the old clean key, and the old demo key, then reloads.
- **KPIs are honest:** crew = roster length (was 8, with a static "+2"
  and an 86% bar), incidents = events in the log (header now "INCIDENTS
  LOGGED", not "TODAY"), critical alerts subtext computes from open
  critical events (was a static "2 require immediate action"), mean
  response defaults to 0m with "No resolved events yet" (was a static
  22m and "−9m from last week"), system-crews line and crew bar compute
  from the roster.
- **Charts compute from the log:** type chart counts only the last
  14 days (its header said so, the code did not); trend chart counts
  events per day for the last 7 days, no forecast line.
- **Map computes from the roster:** one dot per crew, grid-placed,
  zone labels are now ZONE A / B / C, badge is "N POSITIONS" (was a
  static "LIVE • 6 POSITIONS"), and it redraws on every state change
  instead of only on the animation loop. An empty roster draws the
  "No crew yet" message, no dots.
- **Export report:** no "demo roster", no "OVERNIGHT SYNC STATUS:
  COMPLETE", no "official record / UTC-5", no signed claim. It now says
  local record only, device local time, v2.1 NO-DEMO, real entries only.
  Button is now EXPORT REPORT, not GENERATE SIGNED REPORT.
- **Live clock:** dropped the hard-coded "CDT" suffix (it is CST in
  November).
- **Policy form:** the name field no longer comes pre-filled with
  "Conduct Escalation Protocol v3".
- **Keyboard:** N opens the real Log Event form, ? opens Alert Forge,
  Cmd/Ctrl+S runs End-of-Day Review. Console tip updated to match.
- **Version labels:** v2.1 NO-DEMO in the title, meta, nav, boot log,
  boot toast, export footer, and manifest. The only "v2.1 CLEAN" string
  left is the MIGRATION log text naming the key it migrated from.

## Kept (real, computed from your log)

- LOG EVENT form (crew, type, severity 1–5, details required), ACK /
  Resolve with notes, urgency formula (v2.4 as displayed), policy
  triggers and auto-alerts, gap analysis, search/filters, export report,
  audit log, PWA install prompt guard, canvas DPR sizing, note timestamp
  revive on load.

## Verification (2026-11-22, local)

- `node --check` on the extracted inline script (61,722 bytes): PASS.
- Served locally: HTTP 200 for the HTML (103,650 bytes served),
  manifest.json, favicon.ico, icon-180 / icon-192 / icon-512.
- jsdom harness (`/tmp/v21-nodemo-test/harness.js`, jsdom 31):
  **50/50 checks passed** — empty boot (KPIs 0/0/0/0m, crew sub
  "/ 0 total", alerts sub "None open", 0 positions, 0 events, only a
  LOG_STARTED audit entry), no toggle / injector / sync / seed /
  simulation functions exist, ADD CREW saves a real crew and updates
  KPIs and the map, real LOG EVENT saves, End-of-Day Review changes
  nothing and logs, real policy deploy saves and survives reload,
  reload keeps the real event, crew, and 4 policies, and migration
  from a v2.1 CLEAN key keeps only the 1 real entry, drops 7
  demo/seed events, logs MIGRATION, empties the roster, and removes
  the old key. The harness runs with a stubbed 2d canvas context so the
  drawing code actually executes, not just the null-context early return.

## Boot-error fix (2026-11-24)

Anthony opened the first NO-DEMO build on his phone and it showed
"BOOT ERROR — Check DevTools Console (F12)" with the clock frozen at
the static 09:47:22 CDT. Reproduced locally: when localStorage is
blocked (sandboxed file preview) or the saved JSON is corrupt, the
unguarded `localStorage` call inside boot threw and the catch aborted
the whole boot — clock never ticked, no toast, nothing ran. Fixed in
`build_nodemo.py`:

- Every storage call now goes through `storageGet` / `storageSet` /
  `storageRemove`, which try localStorage and fall back to in-memory
  storage for the session, setting `storageBlocked`. Only those 3
  helpers touch localStorage directly (asserted in the build).
- Corrupt saved JSON is caught in `loadState`: the log starts empty
  and a CORRUPT_STATE audit entry is written, instead of dying.
- When storage is blocked, boot shows a yellow "Local save is blocked
  in this view" banner and the app keeps working in-memory for the
  session.
- The static clock no longer carries a stale "09:47:22 CDT" — it starts
  at "--:--:--" until the first tick.
- Harness additions: blocked storage boots with no BOOT ERROR, clock
  ticking, warning shown, ADD CREW working in-memory; corrupt state
  boots with no BOOT ERROR and CORRUPT_STATE logged.

## Still unproven

- Real-phone render (layout, canvas map, Add to Home Screen icon).
- The GitHub repo description still says "demo data labeled DEMO" —
  that is repo metadata, not a file; it needs a settings edit, not a push.
