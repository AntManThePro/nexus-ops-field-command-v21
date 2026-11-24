# NEXUS OPS // Field Command v2.1 NO-DEMO

A separate live page. It does **not** replace the local v2.2 NO-DEMO build
(`workspace/nexus-ops-clean/nexus-ops-master-v2.2-nodemo.html`) and it does
not touch the live QA Brain.

## What it is

A single-file crew discipline dashboard — the older v2.1 cut, with every
demo removed:

- **Command Deck** — KPI cards plus a canvas tactical map (positions come
  from your roster only; an empty roster draws no dots)
- **Event Archive** — searchable table for No-Call, Violation, Attendance,
  Resignation events, with ACK / Resolve
- **Alert Forge** — urgency score per open event, highest first
- **Response Analytics** — incidents-by-type chart (last 14 days, from your
  log) and events-per-day for the last 7 days (from your log, no forecast)
- **Policy Nexus** — 3 seed policies plus a deploy-new-policy form

## Data — no demo, ever

- Local file, localStorage only. No backend, no FieldPulse link, no live
  crew data.
- Saves under localStorage key `nexusOpsState_v21_nodemo`. On first load it
  migrates from the old `nexusOpsState_v21_clean` key: real events are kept,
  demo/seed events are dropped, the fictional roster is reset to empty, and
  a MIGRATION audit entry records what was kept and dropped. The old key is
  then removed.
- The log starts empty. The only audit entry at first boot is LOG_STARTED.
- **Crew roster starts empty.** Add real crew with ADD CREW (hero button,
  Log Event form, or the roster modal). Crew are saved with the log.
  There are no pre-filled names, nicknames, risk scores, or sites.
- No demo toggle, no random injector, no live simulation, no overnight
  sync. The old overnight sync is now **End-of-Day Review**: it only counts
  open events and logs the count. It never adds, resolves, or changes
  anything.
- **Clear All Data** replaces Reset Demo State. It deletes every incident,
  crew, policy change, and audit entry in this browser, after a confirm.
  Export a report first if you need a copy.
- The trend chart is computed from your log. There is no sample data, no
  illustrative projection, and no forecast anywhere in the app.
- The audit log is a local log, not a chain of custody — it lives in this
  browser only and can be cleared. Export regularly.

## Files

- `index.html` — v2.1 NO-DEMO (built by `build_nodemo.py`, see below)
- `build_nodemo.py` — the script that built this file from the live
  v2.1 CLEAN file (explicit replacements only, aborts on a missed match)
- `AUDIT-NODEMO.md` — what was removed, what was fixed, verification
- `manifest.json`, `favicon.ico`, `icons/` — custom NEXUS shield/N icon set
- The v2.1 CLEAN source lives in `workspace/nexus-ops-v21-publish/`
  (index.html, 113,054 bytes, GitHub head 332fe8a, blob SHA
  081ad7000254ddca88970483ea34d981992b2a7d) and is untouched.

## Easter egg

In fine small print at the bottom of the page: the caped ant in the hard
hat hides in the keyboard — N for the real Log Event form, ? to jump to
Alert Forge, and Cmd/Ctrl+S for the end-of-day review. He files the
paperwork too, and every entry is one you typed.

## Deploy

- Repo: `AntManThePro/nexus-ops-field-command-v21`, branch `main`,
  publish directory: root, build command: none
- Private Netlify site under Team login, like the other NEXUS manager
  sites — not public.
- Live site: https://nexus-ops-field-command-v21.netlify.app/

## Verification (2026-11-22, local)

- `node --check` on the extracted inline script: PASS
- Served locally: HTTP 200 for the page, manifest.json, favicon.ico,
  and icon-180 / icon-192 / icon-512
- jsdom harness: **50/50 checks passed** — empty boot (KPIs 0, only a
  LOG_STARTED audit entry), no toggle / injector / sync / seed / simulation
  functions exist, ADD CREW saves a real crew and updates KPIs and the map,
  real LOG EVENT saves, End-of-Day Review changes nothing and logs,
  real policy deploy saves (and is not overwritten on reload — the old
  seedPolicies overwrite bug is fixed), reload keeps the real event, crew,
  and policies, and migration from a v2.1 CLEAN key keeps only the 1 real
  entry, drops 7 demo/seed events, logs MIGRATION, empties the roster,
  and removes the old key.
- **Boot-error fix (Nov 24):** the first NO-DEMO build died on open in a
  sandboxed file preview — any localStorage failure or corrupt saved JSON
  threw inside boot and the whole app showed BOOT ERROR with a frozen
  clock. All storage access now goes through safe helpers that fall back
  to in-memory storage for the session, corrupt saved data is logged as
  CORRUPT_STATE and the log starts empty instead of dying, and a yellow
  banner says local save is blocked in this view. The harness covers it:
  blocked storage boots fine with the warning shown and ADD CREW working
  in-memory; corrupt state boots fine with CORRUPT_STATE logged.
- Real-phone render still needed.
