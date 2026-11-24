#!/usr/bin/env python3
"""Build NEXUS OPS Field Command v2.1 NO-DEMO from the live v2.1 CLEAN file.

Source (verified against GitHub head 332fe8a, blob SHA 081ad700...):
    workspace/nexus-ops-v21-publish/index.html  (113,054 bytes)
Output:
    workspace/nexus-ops-v21-nodemo/index.html

Rules, same as the v2.2 NO-DEMO build:
- Explicit replacements only. Every replacement must match exactly once
  (or the stated count); anything missed aborts the build.
- No demo, ever: no toggle, no random injector, no live simulation,
  no seeded events, no fictional roster, no sample trend, no demo sync.
- The log starts empty. Real crew are added with ADD CREW and persist.
- The source file is never modified.
"""
import pathlib, re, sys

SRC = pathlib.Path(__file__).parent.parent / "nexus-ops-v21-publish" / "index.html"
OUT = pathlib.Path(__file__).parent / "index.html"
text = SRC.read_text()
orig_len = len(text)

def rep(old, new, count=1):
    global text
    n = text.count(old)
    assert n == count, f"REPLACEMENT MISS ({n} != {count}): {old[:120]!r}"
    text = text.replace(old, new)

def remove_between(start_marker, end_marker, label):
    """Remove text from start_marker (inclusive) to end_marker (exclusive)."""
    global text
    i = text.find(start_marker)
    assert i >= 0, f"remove_between start not found: {label} :: {start_marker[:80]!r}"
    assert text.count(start_marker) == 1, f"remove_between start not unique: {label}"
    j = text.find(end_marker, i)
    assert j >= 0, f"remove_between end not found: {label} :: {end_marker[:80]!r}"
    text = text[:i] + text[j:]

# ---------------------------------------------------------------- version
rep('content="NEXUS OPS Field Command v2.1 CLEAN - Crew event tracking, discipline alerts, and modular policy enforcement. Local file, localStorage only. Demo data is labeled DEMO. Built by DoubleA @ AntManThePro"',
    'content="NEXUS OPS Field Command v2.1 NO-DEMO - Crew event tracking, discipline alerts, and modular policy enforcement. Real entries only, local file, localStorage only. Built by DoubleA @ AntManThePro"')
rep('<title>NEXUS OPS • Field Command v2.1 CLEAN</title>',
    '<title>NEXUS OPS • Field Command v2.1 NO-DEMO</title>')
rep('<link rel="icon" href="favicon.ico?v=1">', '<link rel="icon" href="favicon.ico?v=2">')
rep('FIELD COMMAND v2.1 CLEAN', 'FIELD COMMAND v2.1 NO-DEMO')

# ---------------------------------------------------------------- header / hero
rep('''    </div>

    <!-- Top Navigation -->''',
    '''    </div>

    <!-- Storage Warning Banner (shows only when local save is blocked) -->
    <div id="storage-warning" class="hidden bg-[#ffcc00]/10 border-b border-[#ffcc00]/40 text-[#ffcc00] text-xs px-4 py-2.5">
        <div class="max-w-7xl mx-auto flex items-center gap-x-3">
            <i class="fa-solid fa-exclamation-triangle"></i>
            <div class="flex-1"><strong>Local save is blocked in this view.</strong> Entries work now but will not persist after closing. Open the live site (or a normal browser) to save.</div>
        </div>
    </div>

    <!-- Top Navigation -->''')
rep('<div class="text-xs font-mono text-[#00ff87]">SYSTEM NOMINAL • <span id="system-crews">8 CREWS IN ROSTER</span></div>',
    '<div class="text-xs font-mono text-[#00ff87]">SYSTEM NOMINAL • <span id="system-crews">0 CREWS IN ROSTER</span></div>')
rep('''                    <div class="px-4 py-1 rounded-3xl text-xs font-mono tracking-widest border border-[#00ff87]/40 text-[#00ff87] bg-[#00ff87]/5">LOCAL</div>
                    <button id="demo-toggle" onclick="toggleDemoMode()" class="px-4 py-1 rounded-3xl text-xs font-mono tracking-widest border border-white/30 text-white/70 bg-white/5">DEMO MODE: OFF</button>''',
    '''                    <div class="px-4 py-1 rounded-3xl text-xs font-mono tracking-widest border border-[#00ff87]/40 text-[#00ff87] bg-[#00ff87]/5">LOCAL</div>
                    <div class="px-4 py-1 rounded-3xl text-xs font-mono tracking-widest border border-white/30 text-white/70 bg-white/5">NO-DEMO</div>''')
rep('''                <button onclick="simulateOvernightSync()" 
                        class="flex items-center gap-x-2 px-6 py-3 rounded-3xl bg-white/5 hover:bg-white/10 border border-white/20 hover:border-[#ffcc00]/60 transition-all active:scale-[0.985]">
                    <i class="fa-solid fa-sync fa-fw"></i>
                    <span class="font-semibold text-sm">RUN OVERNIGHT SYNC</span>
                </button>''',
    '''                <button onclick="endOfDayReview()" 
                        class="flex items-center gap-x-2 px-6 py-3 rounded-3xl bg-white/5 hover:bg-white/10 border border-white/20 hover:border-[#ffcc00]/60 transition-all active:scale-[0.985]">
                    <i class="fa-solid fa-sync fa-fw"></i>
                    <span class="font-semibold text-sm">END-OF-DAY REVIEW</span>
                </button>
                <button onclick="addCrew()" 
                        class="flex items-center gap-x-2 px-5 py-3 rounded-3xl bg-white/5 hover:bg-white/10 border border-white/20 text-sm transition-all active:scale-[0.985]">
                    <i class="fa-solid fa-user-plus fa-fw"></i>
                    <span>ADD CREW</span>
                </button>''')
rep('''                <button id="inject-btn" onclick="injectRandomEvent()" 
                        class="flex items-center gap-x-2 px-5 py-3 rounded-3xl bg-white/5 hover:bg-white/10 border border-white/20 text-sm transition-all active:scale-[0.985]">
                    <i class="fa-solid fa-bolt-lightning fa-fw"></i>
                    <span>INJECT DEMO EVENT</span>
                </button>
''', '')

# ---------------------------------------------------------------- KPI cards
rep('<div id="live-clock" class="font-semibold tabular-nums">09:47:22 CDT</div>',
    '<div id="live-clock" class="font-semibold tabular-nums">--:--:--</div>')
rep('<div id="kpi-crew" class="text-5xl font-display tabular-nums mt-1">8</div>',
    '<div id="kpi-crew" class="text-5xl font-display tabular-nums mt-1">0</div>')
rep('<div class="text-xs text-white/50">/ 8 total • demo roster</div>',
    '<div class="text-xs text-white/50" id="kpi-crew-sub">/ 0 total • your roster</div>')
rep('''                    <div class="text-right">
                        <div class="text-[#00ff87] text-xs font-mono">+2</div>
                        <i class="fa-solid fa-users text-3xl text-[#00ff87]/70 group-hover:scale-110 transition"></i>
                    </div>''',
    '''                    <div class="text-right">
                        <i class="fa-solid fa-users text-3xl text-[#00ff87]/70 group-hover:scale-110 transition"></i>
                    </div>''')
rep('<div class="h-1.5 bg-gradient-to-r from-[#00ff87] to-[#60efff] w-[86%]" style="width: 86%"></div>',
    '<div id="kpi-crew-bar" class="h-1.5 bg-gradient-to-r from-[#00ff87] to-[#60efff]" style="width: 0%"></div>')
rep('<div class="section-header">INCIDENTS TODAY</div>', '<div class="section-header">INCIDENTS LOGGED</div>')
rep('<div id="kpi-incidents" class="text-5xl font-display tabular-nums mt-1">6</div>',
    '<div id="kpi-incidents" class="text-5xl font-display tabular-nums mt-1">0</div>')
rep('<div id="kpi-open" class="text-[10px] px-2 py-0.5 rounded bg-[#ff0080]/10 text-[#ff0080]">3 OPEN</div>',
    '<div id="kpi-open" class="text-[10px] px-2 py-0.5 rounded bg-[#ff0080]/10 text-[#ff0080]">0 OPEN</div>')
rep('<div id="kpi-resolved" class="text-[10px] px-2 py-0.5 rounded bg-[#00ff87]/10 text-[#00ff87]">3 RESOLVED</div>',
    '<div id="kpi-resolved" class="text-[10px] px-2 py-0.5 rounded bg-[#00ff87]/10 text-[#00ff87]">0 RESOLVED</div>')
rep('<div id="kpi-alerts" class="text-5xl font-display tabular-nums mt-1 text-[#ff0080]">3</div>',
    '<div id="kpi-alerts" class="text-5xl font-display tabular-nums mt-1 text-[#ff0080]">0</div>')
rep('<div class="text-xs text-white/50">2 require immediate action</div>',
    '<div class="text-xs text-white/50" id="kpi-alerts-sub">None open</div>')
rep('<div id="kpi-response-main" class="text-5xl font-display tabular-nums mt-1">18<span class="text-3xl align-super">m</span></div>',
    '<div id="kpi-response-main" class="text-5xl font-display tabular-nums mt-1">0<span class="text-3xl align-super">m</span></div>')
rep('<div class="text-xs"><span class="text-[#00ff87]">−9m</span> from last week</div>',
    '<div class="text-xs text-white/50">No resolved events yet</div>')
rep('<div class="mt-3 text-xs font-mono text-[#ff0080]">AVG RESPONSE: <span id="kpi-response">18m</span></div>',
    '<div class="mt-3 text-xs font-mono text-[#ff0080]">AVG RESPONSE: <span id="kpi-response">0m</span></div>')

# ---------------------------------------------------------------- command deck
rep('<div class="text-xs text-white/50">Real-time crew positions • Site Alpha-7</div>',
    '<div class="text-xs text-white/50">Crew positions from your roster</div>')
rep('<div id="map-nodes" class="text-xs px-3 py-1 rounded-2xl bg-[#00ff87]/10 text-[#00ff87] font-mono">LIVE • 6 POSITIONS</div>',
    '<div id="map-nodes" class="text-xs px-3 py-1 rounded-2xl bg-[#00ff87]/10 text-[#00ff87] font-mono">0 POSITIONS</div>')
rep('<div class="section-header">LIVE EVENT STREAM</div>', '<div class="section-header">EVENT STREAM</div>')
rep('<div class="text-xs text-white/50">Auto-updating • All field submissions</div>',
    '<div class="text-xs text-white/50">Newest first • Updates when you log an event</div>')
rep('''                            <div onclick="toggleLiveMode()" id="live-mode-btn"
                                 class="cursor-pointer flex items-center gap-x-1.5 text-xs px-3 py-1 rounded-2xl border border-[#00ff87]/40 bg-[#00ff87]/5 text-[#00ff87]">
                                <i class="fa-solid fa-play fa-fw"></i>
                                <span id="live-mode-text">LIVE MODE ON</span>
                            </div>
''', '''                            <div class="flex items-center gap-x-1.5 text-xs px-3 py-1 rounded-2xl border border-white/20 text-white/60">
                                <span>REAL ENTRIES ONLY</span>
                            </div>
''')

# ---------------------------------------------------------------- archive / analytics / policy
rep('<div class="text-xs px-3 py-1 bg-white/5 rounded-2xl font-mono text-white/60" id="event-count">6 EVENTS • DEMO DATA</div>',
    '<div class="text-xs px-3 py-1 bg-white/5 rounded-2xl font-mono text-white/60" id="event-count">0 EVENTS</div>')
rep('<span>INCIDENTS BY TYPE (LAST 14 DAYS)</span>', '<span>INCIDENTS BY TYPE (LAST 14 DAYS)</span>')
rep('<div class="section-header mb-4">RESPONSE TIME TREND + PREDICTION</div>',
    '<div class="section-header mb-4">EVENTS PER DAY — LAST 7 DAYS</div>')
rep('''                            <div>SAMPLE TREND: <span class="text-[#ffcc00]">illustrative only — not a forecast</span></div>
                            <div class="font-mono text-white/50">SAMPLE</div>''',
    '''                            <div>COUNTS FROM YOUR LOG: <span class="text-[#ffcc00]">no forecast</span></div>
                            <div class="font-mono text-white/50">REAL</div>''')
rep('''                                All actions logged to immutable Chain of Custody.
''', '''                                All actions logged to the Audit Log.
''')
rep('<p class="text-sm text-white/60">Add, edit, or deploy new policy modules. Changes take effect instantly across all live events.</p>',
    '<p class="text-sm text-white/60">Add, edit, or deploy new policy modules. Changes take effect instantly across all events in this log.</p>')
rep('<span>Policy changes are versioned and logged to the Chain of Custody. All future and retroactive events are re-evaluated automatically.</span>',
    '<span>Policy changes are logged to the Audit Log. All future and retroactive events are re-evaluated automatically.</span>')

# ---------------------------------------------------------------- bottom bar
rep('<span>VIEW CHAIN OF CUSTODY LOG</span>', '<span>VIEW AUDIT LOG</span>')
rep('<div><span id="footer-events">6 events in this file</span> • Last overnight sync: <span id="last-sync">Not run this session</span></div>',
    '<div><span id="footer-events">0 events in this file</span> • Last end-of-day review: <span id="last-sync">Not run this session</span></div>')
rep('<span>GENERATE SIGNED REPORT</span>', '<span>EXPORT REPORT</span>')
rep('''                <button onclick="resetDemo()" class="px-5 py-2 rounded-2xl border border-white/20 hover:bg-white/5 flex items-center gap-x-2 text-xs font-medium text-white/70">
                    <i class="fa-solid fa-undo"></i>
                    <span>RESET DEMO STATE</span>
                </button>''',
    '''                <button onclick="clearAllData()" class="px-5 py-2 rounded-2xl border border-white/20 hover:bg-white/5 flex items-center gap-x-2 text-xs font-medium text-white/70">
                    <i class="fa-solid fa-undo"></i>
                    <span>CLEAR ALL DATA</span>
                </button>''')

# ---------------------------------------------------------------- log event modal + egg
rep("localStorage.setItem('nexusWarningDismissed','1')", "storageSet('nexusWarningDismissed','1')")
rep('<!-- Log Event Modal (real entry; demo injection is separate) -->',
    '<!-- Log Event Modal (real entry) -->')
rep('<div class="text-sm text-white/60 mb-6">A real entry for this file. Demo events are only made with INJECT DEMO EVENT when Demo Mode is on.</div>',
    '<div class="text-sm text-white/60 mb-6">A real entry for this file. Nothing here is invented — if it is in the log, you typed it.</div>')
rep('''                <div>
                    <label class="text-xs tracking-widest text-white/60 block mb-1.5">CREW</label>
                    <select id="form-crew" class="w-full bg-black/40 border border-white/20 px-4 py-3 rounded-2xl text-sm"></select>
                </div>''',
    '''                <div>
                    <label class="text-xs tracking-widest text-white/60 block mb-1.5">CREW</label>
                    <select id="form-crew" class="w-full bg-black/40 border border-white/20 px-4 py-3 rounded-2xl text-sm"></select>
                    <button type="button" onclick="addCrew()" class="mt-2 text-xs px-3 py-1.5 rounded-2xl border border-white/30 hover:bg-white/10">+ ADD CREW</button>
                </div>''')
rep('Easter egg, in fine print as promised: the caped ant in the hard hat hides in the keyboard — press N for a demo event (or the real Log Event form when Demo Mode is off), ? to jump to Alert Forge, and Cmd/Ctrl+S for the demo overnight sync. He files the paperwork too, but only in DEMO.',
    'Easter egg, in fine print as promised: the caped ant in the hard hat hides in the keyboard — press N for the real Log Event form, ? to jump to Alert Forge, and Cmd/Ctrl+S for the end-of-day review. He files the paperwork too, and every entry is one you typed.')
rep('<input id="policy-name" value="Conduct Escalation Protocol v3" class="w-full bg-black/40 border border-white/20 px-4 py-3 rounded-2xl text-sm">',
    '<input id="policy-name" placeholder="Policy name" class="w-full bg-black/40 border border-white/20 px-4 py-3 rounded-2xl text-sm">')

# ---------------------------------------------------------------- state keys
rep('''        let liveMode = true;
        let liveInterval = null;
        let mapAnimationFrame = null;
        let demoMode = false;
        const STATE_KEY = 'nexusOpsState_v21_clean';
        const LEGACY_STATE_KEY = 'nexusOpsState_v21';
        const DEMO_KEY = 'nexusOpsDemo_v21_clean';''',
    '''        let mapAnimationFrame = null;
        const STATE_KEY = 'nexusOpsState_v21_nodemo';
        const LEGACY_STATE_KEY = 'nexusOpsState_v21_clean';
        // Safe storage: localStorage can be blocked (sandboxed file preview)
        // or hold corrupt JSON. Never let storage kill the boot — fall back
        // to in-memory storage for the session and flag it.
        const __memStore = {};
        let storageBlocked = false;
        function storageGet(k) { try { return localStorage.getItem(k); } catch (e) { storageBlocked = true; return (__memStore[k] !== undefined ? __memStore[k] : null); } }
        function storageSet(k, v) { try { localStorage.setItem(k, v); } catch (e) { storageBlocked = true; __memStore[k] = v; } }
        function storageRemove(k) { try { localStorage.removeItem(k); } catch (e) { storageBlocked = true; delete __memStore[k]; } }''')

# ---------------------------------------------------------------- crews: fictional roster -> empty, persisted
remove_between('        // Sample crews with risk profiles (algorithmic depth)\n        const crews = [',
               '        // Initial seed policies (modular)',
               'fictional crew roster')
rep('        // Initial seed policies (modular)',
    '''        // Crew roster — starts empty. Real crew are added by DoubleA with ADD CREW.
        // No fictional roster, no seeded names. Persisted in saveState.
        let crews = [];

        // Initial seed policies (modular)''')
rep('''        function seedPolicies() {
            policies = [''',
    '''        function seedPolicies() {
            if (policies.length > 0) return; // already loaded — do not overwrite real policies
            policies = [''')

# ---------------------------------------------------------------- save / load state
rep("localStorage.setItem(STATE_KEY, JSON.stringify(state));", "storageSet(STATE_KEY, JSON.stringify(state));")
rep("const state = { events, policies, auditLog, lastSync: new Date().toISOString() };",
    "const state = { events, policies, crews, auditLog, lastSync: new Date().toISOString() };")
remove_between('        function loadState() {',
               '        function updateDemoUI() {',
               'old loadState')
rep('        function updateDemoUI() {',
    '''        function loadState() {
            let saved = storageGet(STATE_KEY);
            let migratedFrom = null;
            let corruptSaved = false;
            if (!saved) { saved = storageGet(LEGACY_STATE_KEY); if (saved) migratedFrom = LEGACY_STATE_KEY; }
            if (saved) {
                let parsed = null;
                try { parsed = JSON.parse(saved); } catch (e) { parsed = null; }
                if (!parsed) { parsed = {}; corruptSaved = true; }
                events = parsed.events || [];
                policies = parsed.policies || [];
                crews = parsed.crews || [];
                auditLog = parsed.auditLog || [];
                events.forEach(e => {
                    e.timestamp = new Date(e.timestamp);
                    (e.notes || []).forEach(n => { n.time = new Date(n.time); });
                    if (e.acknowledgedAt) e.acknowledgedAt = new Date(e.acknowledgedAt);
                });
                auditLog.forEach(a => a.timestamp = new Date(a.timestamp));
                if (migratedFrom) {
                    const SEED_IDS = ["EVT-2401", "EVT-2402", "EVT-2403", "EVT-2404", "EVT-2405", "EVT-2398"];
                    const before = events.length;
                    events = events.filter(e => !e.demo && SEED_IDS.indexOf(e.id) === -1);
                    const dropped = before - events.length;
                    crews = []; // the old roster was fictional — never carry it forward
                    auditLog = [];
                    logAudit("MIGRATION", "Migrated from v2.1 CLEAN (" + migratedFrom + "): kept " + events.length + " real events, dropped " + dropped + " demo/seed events, roster reset to empty.");
                    storageRemove(LEGACY_STATE_KEY);
                    saveState();
                }
            }
            if (corruptSaved) logAudit("CORRUPT_STATE", "Saved data could not be read — started with an empty log.");
            if (events.length === 0 && auditLog.length === 0) {
                logAudit("LOG_STARTED", "NEXUS OPS v2.1 NO-DEMO log started. Empty — every entry from here is typed by DoubleA.");
            }
        }
        function addCrew() {
            const name = (prompt("Crew name (real name):") || "").trim();
            if (!name) return;
            const role = (prompt("Role (e.g. Field Lead, Technician):", "Technician") || "Technician").trim();
            const site = (prompt("Site:", "") || "").trim();
            const crew = { id: "C-" + Date.now().toString().slice(-6), name: name, role: role, site: site || "—", risk: 1.0 };
            crews.push(crew);
            logAudit("CREW_ADDED", "Added crew: " + name + (site ? " (" + site + ")" : ""));
            saveState();
            updateAllUI();
            if (!document.getElementById('event-form-modal').classList.contains('hidden')) showEventForm();
            showToast("Crew added: " + name, "success");
        }
        function updateDemoUI() {''')

# ---------------------------------------------------------------- remove demo UI functions, replace with nothing
remove_between('        function updateDemoUI() {',
               '        function showEventForm() {',
               'updateDemoUI + toggleDemoMode')

# ---------------------------------------------------------------- showEventForm / submit / roster
rep('''        function showEventForm() {
            const sel = document.getElementById('form-crew');
            sel.innerHTML = crews.map(c => `<option value="${c.id}">${c.name} (${c.id}) — ${c.site}</option>`).join('');''',
    '''        function showEventForm() {
            const sel = document.getElementById('form-crew');
            if (crews.length === 0) {
                sel.innerHTML = '<option value="">No crew yet — add crew first</option>';
            } else {
                sel.innerHTML = crews.map(c => `<option value="${c.id}">${c.name} (${c.id}) — ${c.site}</option>`).join('');
            }''')
rep('''            const crewId = document.getElementById('form-crew').value;
            const type = document.getElementById('form-type').value;''',
    '''            const crewId = document.getElementById('form-crew').value;
            if (!crewId) { alert('Add a crew member first (ADD CREW), then log the event.'); return; }
            const type = document.getElementById('form-type').value;''')
rep('            addEvent(type, crewId, details, sev, false);',
    '            addEvent(type, crewId, details, sev);')
rep("""            header.innerHTML = '<div class="font-display text-3xl">CREW ROSTER</div><div class="text-xs text-white/50">' + crews.length + ' crew in this demo roster — not a live headcount</div>';
            body.innerHTML = '<div class="space-y-2">' + crews.map(c =>
                '<div class="flex justify-between text-sm p-3 bg-black/40 rounded-2xl border border-white/10"><div><div class="font-semibold">' + c.name + '</div><div class="text-xs text-white/50">' + c.role + ' • ' + c.site + '</div></div><div class="font-mono text-xs text-[#ffcc00]">risk ×' + c.risk.toFixed(1) + '</div></div>').join('') + '</div>';""",
    """            header.innerHTML = '<div class="font-display text-3xl">CREW ROSTER</div><div class="text-xs text-white/50">' + crews.length + ' crew in your roster — added by you</div>';
            if (crews.length === 0) {
                body.innerHTML = '<div class="p-6 text-center text-sm text-white/60">No crew yet. Add your real crew with ADD CREW below — no names are pre-filled.</div><div class="text-center mt-2"><button onclick="addCrew()" class="px-5 py-2.5 rounded-2xl bg-[#00ff87] text-black font-bold text-sm">+ ADD CREW</button></div>';
            } else {
                body.innerHTML = '<div class="space-y-2">' + crews.map(c =>
                    '<div class="flex justify-between text-sm p-3 bg-black/40 rounded-2xl border border-white/10"><div><div class="font-semibold">' + c.name + '</div><div class="text-xs text-white/50">' + c.role + ' • ' + c.site + '</div></div><div class="font-mono text-xs text-[#ffcc00]">risk ×' + (c.risk || 1).toFixed(1) + '</div></div>').join('') + '</div><div class="text-center mt-4"><button onclick="addCrew()" class="px-5 py-2 rounded-2xl border border-white/30 text-sm">+ ADD CREW</button></div>';
            }""")

# ---------------------------------------------------------------- remove seed data
remove_between('        function seedInitialData() {',
               '        function getCrewById(id) {',
               'seedInitialData (6 fictional events)')

# ---------------------------------------------------------------- policies: no demo flag on auto alerts
rep('''                            demo: !!newEvent.demo,
''', '')

# ---------------------------------------------------------------- addEvent: no demo
rep('        function addEvent(type, crewId, details = "", severity = 3, isDemo = null) {',
    '        function addEvent(type, crewId, details = "", severity = 3) {')
rep('''            if (isDemo === null) isDemo = demoMode;
''', '')
rep('                location: crew.site || "Alpha-7",', '                location: crew.site || "—",')
rep('''                demo: !!isDemo,
''', '')
rep("            logAudit(\"EVENT_CREATED\", `${type} reported for ${crew.name}${newEvent.demo ? ' [DEMO]' : ''}`, newEvent.id);",
    "            logAudit(\"EVENT_CREATED\", `${type} reported for ${crew.name}`, newEvent.id);")
rep("            showToast(`${type} event logged${newEvent.demo ? ' [DEMO]' : ''}`, \"success\");",
    "            showToast(`${type} event logged`, \"success\");")

# ---------------------------------------------------------------- remove random injector
remove_between('        function injectRandomEvent() {',
               '        function acknowledgeEvent(eventId) {',
               'injectRandomEvent')

# ---------------------------------------------------------------- KPIs: honest defaults
rep('''            const avgResponse = resolved.length > 0 ? 
                Math.round(resolved.reduce((sum, e) => sum + e.responseTime, 0) / resolved.length) : 22;''',
    '''            const avgResponse = resolved.length > 0 ?
                Math.round(resolved.reduce((sum, e) => sum + e.responseTime, 0) / resolved.length) : 0;''')
rep("""            document.getElementById('kpi-crew').innerHTML = crews.length;""",
    """            document.getElementById('kpi-crew').innerHTML = crews.length;
            const cs = document.getElementById('system-crews');
            if (cs) cs.textContent = crews.length + (crews.length === 1 ? ' CREW IN ROSTER' : ' CREWS IN ROSTER');
            const kcs = document.getElementById('kpi-crew-sub');
            if (kcs) kcs.textContent = '/ ' + crews.length + ' total • your roster';
            const kas = document.getElementById('kpi-alerts-sub');
            if (kas) kas.textContent = criticalAlerts === 0 ? 'None open' : criticalAlerts + (criticalAlerts === 1 ? ' requires immediate action' : ' require immediate action');
            const bar = document.getElementById('kpi-crew-bar');
            if (bar) bar.style.width = crews.length > 0 ? '100%' : '0%';""")

# ---------------------------------------------------------------- feed / table: no demo pills
rep("""                            <span class="status-pill ${statusColor} border border-current/40">${evt.status}</span>${evt.demo ? '<span class="status-pill text-[#ff0080] border border-[#ff0080]/40">DEMO</span>' : ''}""",
    """                            <span class="status-pill ${statusColor} border border-current/40">${evt.status}</span>""")
rep("""                        <div class="font-semibold">${evt.type.replace(/_/g, ' ')}${evt.demo ? ' <span class="text-[10px] px-2 py-px rounded bg-[#ff0080]/10 text-[#ff0080]">DEMO</span>' : ''}</div>""",
    """                        <div class="font-semibold">${evt.type.replace(/_/g, ' ')}</div>""")
rep('''            const demoCount = events.filter(e => e.demo).length;
            const daySpan = events.length ? Math.max(1, Math.ceil((Math.max(...events.map(e => e.timestamp)) - Math.min(...events.map(e => e.timestamp))) / 86400000)) : 0;
            document.getElementById('event-count').innerHTML = `${events.length} EVENTS • ${daySpan} DAY${daySpan === 1 ? '' : 'S'}${demoCount ? ' • ' + demoCount + ' DEMO' : ''}`;''',
    '''            const daySpan = events.length ? Math.max(1, Math.ceil((Math.max(...events.map(e => e.timestamp)) - Math.min(...events.map(e => e.timestamp))) / 86400000)) : 0;
            document.getElementById('event-count').innerHTML = events.length === 0 ? '0 EVENTS' : `${events.length} EVENTS • ${daySpan} DAY${daySpan === 1 ? '' : 'S'}`;''')

# ---------------------------------------------------------------- tactical map: roster positions only
rep('''            ctx.fillText("ALPHA-7", 38, 32);
            ctx.fillText("BRAVO-2", 310, 32);
            ctx.fillText("CHARLIE-9", 180, 195);''',
    '''            ctx.fillText("ZONE A", 38, 32);
            ctx.fillText("ZONE B", 310, 32);
            ctx.fillText("ZONE C", 180, 195);''')
remove_between('            // Crew positions (static-ish with slight animation offset)',
               '            crewPositions.forEach(pos => {',
               'hardcoded crew positions')
rep('            crewPositions.forEach(pos => {',
    '''            // Crew positions — one dot per crew in your roster, placed on a grid.
            // No positions are invented: an empty roster draws no dots.
            const time = Date.now() / 900;
            const crewPositions = crews.slice(0, 8).map((c, i) => ({
                x: 70 + (i % 4) * 110,
                y: 85 + Math.floor(i / 4) * 110,
                id: c.id, active: true
            }));
            if (crewPositions.length === 0) {
                ctx.fillStyle = 'rgba(255,255,255,0.5)';
                ctx.font = '12px monospace';
                ctx.fillText('No crew yet — add crew to see positions.', 95, 170);
            }
            crewPositions.forEach(pos => {''')
rep("""            const canvas = document.getElementById('tactical-map');
            const fitted = fitCanvas(canvas, 520, 340);""",
    """            const canvas = document.getElementById('tactical-map');
            const mn = document.getElementById('map-nodes');
            if (mn) mn.textContent = crews.length + ' POSITION' + (crews.length === 1 ? '' : 'S');
            const fitted = fitCanvas(canvas, 520, 340);""")
rep("""            drawTypeChart();
            drawTrendChart();
            saveState();
        }""",
    """            drawTypeChart();
            drawTrendChart();
            updateTacticalMap();
            saveState();
        }""")
rep('''            incidents.forEach((inc, i) => {
                const p = crewPositions.find(cp => cp.id === inc.crewId) || crewPositions[i % crewPositions.length];''',
    '''            incidents.forEach((inc, i) => {
                if (crewPositions.length === 0) return;
                const p = crewPositions.find(cp => cp.id === inc.crewId) || crewPositions[i % crewPositions.length];''')
remove_between('            // Connection lines (team links)',
               '        }\n        \n        function startMapAnimation() {',
               'hardcoded connection lines')
# the removal above leaves updateTacticalMap's closing brace; verify later

# ---------------------------------------------------------------- type chart: last 14 days only
rep('            const counts = types.map(t => events.filter(e => e.type === t).length);',
    '''            const cutoff14 = Date.now() - 14 * 86400000;
            const counts = types.map(t => events.filter(e => e.type === t && e.timestamp.getTime() >= cutoff14).length);''')

# ---------------------------------------------------------------- trend chart: real counts, no forecast
rep('''            // SAMPLE 7-day data + illustrative projection — not real events, not a forecast.
            const days = ['18', '19', '20', '21', '22', '23', '24'];
            const values = [14, 9, 17, 11, 22, 15, 19];
            const pred = [21, 24]; // illustrative next 2 days
            
            const maxVal = 28;''',
    '''            // Real counts from your log: events per day, last 7 days. No forecast.
            const days = [];
            const values = [];
            for (let i = 6; i >= 0; i--) {
                const d = new Date();
                d.setDate(d.getDate() - i);
                const start = new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime();
                values.push(events.filter(e => e.timestamp.getTime() >= start && e.timestamp.getTime() < start + 86400000).length);
                days.push(String(d.getDate()));
            }

            const maxVal = Math.max(...values, 5);''')
remove_between('            // Prediction dashed',
               '            // Dots',
               'illustrative prediction line')
rep('''            ctx.fillStyle = '#60efff';
            ctx.fillRect(310, 18, 14, 3);
            ctx.fillStyle = '#ffffff';
            ctx.fillText('SAMPLE', 330, 23);

            ctx.fillStyle = '#ffcc00';
            ctx.fillRect(380, 18, 14, 3);
            ctx.fillStyle = '#ffffff';
            ctx.fillText('ILLUSTR.', 400, 23);''',
    '''            ctx.fillStyle = '#60efff';
            ctx.fillRect(310, 18, 14, 3);
            ctx.fillStyle = '#ffffff';
            ctx.fillText('EVENTS', 330, 23);''')

# ---------------------------------------------------------------- remove overnight sync, replace with End-of-Day Review
remove_between('        function simulateOvernightSync() {',
               '        function runGapAnalysis() {',
               'simulateOvernightSync (3 fictional overnight events)')
rep('        function runGapAnalysis() {',
    '''        function endOfDayReview() {
            const openNow = events.filter(e => e.status !== "RESOLVED").length;
            logAudit("END_OF_DAY_REVIEW", "End-of-day review: " + openNow + " open event" + (openNow === 1 ? "" : "s") + ", " + events.length + " total in this log. Nothing added or changed.");
            const ls = document.getElementById('last-sync');
            if (ls) ls.textContent = "Reviewed just now";
            showToast("End-of-day review: " + openNow + " open. Nothing added or changed.", "success");
            updateAllUI();
        }

        function runGapAnalysis() {''')

# ---------------------------------------------------------------- remove live mode + simulation
remove_between('        function toggleLiveMode() {',
               '        function clearEventFeed() {',
               'toggleLiveMode + startLiveSimulation (they sit together)')

# ---------------------------------------------------------------- audit log / export
rep('''            header.innerHTML = `<div class="font-display text-3xl">CHAIN OF CUSTODY</div><div class="text-xs text-white/50">Immutable audit trail • All actions timestamped</div>`;''',
    '''            header.innerHTML = `<div class="font-display text-3xl">AUDIT LOG</div><div class="text-xs text-white/50">Local log • All actions timestamped</div>`;''')
rep('''ACTIVE CREW: ${crews.length} / ${crews.length} (demo roster)''',
    '''ACTIVE CREW: ${crews.length}''')
rep('''RESOLVED TODAY: ${resolvedCount}''',
    '''RESOLVED: ${resolvedCount}''')
rep('''OVERNIGHT SYNC STATUS: COMPLETE
CHAIN OF CUSTODY ENTRIES: ${auditLog.length}

This document serves as official record. All timestamps UTC-5.
NEXUS OPS Field Command v2.1 CLEAN • Local file — demo events marked [DEMO]: ${events.filter(e => e.demo).length} of ${events.length}''',
    '''AUDIT LOG ENTRIES: ${auditLog.length}

Local record only — this file lives in this browser only. Export regularly.
Timestamps are device local time.
NEXUS OPS Field Command v2.1 NO-DEMO • Real entries only''')
rep('''            logAudit("REPORT_EXPORTED", "Signed daily mission report generated");''',
    '''            logAudit("REPORT_EXPORTED", "Daily mission report exported");''')

# ---------------------------------------------------------------- live clock: drop the hard-coded CDT
rep('''                el.innerHTML = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }) + " CDT";''',
    '''                el.innerHTML = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });''')

# ---------------------------------------------------------------- keyboard / boot: replace live init
remove_between('        function initializeLive() {',
               '        function resetDemo() {',
               'initializeLive (N inject + Cmd+S sync)')
rep('        function resetDemo() {',
    '''        function initializeLive() {
            // Keyboard shortcuts — all real actions only
            document.addEventListener('keydown', function(e) {
                if (e.key.toLowerCase() === 'n' && document.activeElement.tagName === "BODY") {
                    e.preventDefault();
                    showEventForm();
                }
                if (e.key === "?" && document.activeElement.tagName === "BODY") {
                    e.preventDefault();
                    switchTab(2);
                    showToast("Alert Forge opened. Review highest urgency items.", "info");
                }
                if (e.key.toLowerCase() === 's' && e.metaKey) {
                    e.preventDefault();
                    endOfDayReview();
                }
            });

            // Easter egg / pro touch
            console.log('%c[NEXUS OPS] Pro tip: Press N for a new incident, ? for alerts, Cmd+S for end-of-day review.', 'color:#64748b');
        }

        function clearAllData() {
            if (!confirm("Clear all data? This deletes every incident, crew, policy change and audit entry stored in this browser. This cannot be undone. Export a report first if you need a copy.")) return;
            storageRemove(STATE_KEY);
            storageRemove(LEGACY_STATE_KEY);
            storageRemove('nexusOpsDemo_v21_clean');
            location.reload();
        }

        function resetDemo() {''')
remove_between('        function resetDemo() {',
               '        // ============================================\n        // BOOT SEQUENCE',
               'resetDemo')
rep('''                loadState();
                seedPolicies();
                seedInitialData();
                updateDemoUI();''',
    '''                loadState();
                seedPolicies();
                if (storageBlocked) {
                    const sw = document.getElementById('storage-warning');
                    if (sw) sw.classList.remove('hidden');
                }''')
rep("if (window.location.protocol === 'file:' && !localStorage.getItem('nexusWarningDismissed')) {", "if (window.location.protocol === 'file:' && !storageGet('nexusWarningDismissed')) {")
rep('''            console.log("%c[NEXUS OPS v2.1 CLEAN] Booting Field Command Dashboard...", "color:#00ff87");''',
    '''            console.log("%c[NEXUS OPS v2.1 NO-DEMO] Booting Field Command Dashboard...", "color:#00ff87");''')
rep('''                    showToast("NEXUS OPS v2.1 CLEAN online. Demo Mode is " + (demoMode ? "ON" : "OFF") + ".", "success");''',
    '''                    showToast("NEXUS OPS v2.1 NO-DEMO online. " + events.length + " events in this log.", "success");''')
rep('                window.NEXUS = { events, policies, addEvent, simulateOvernightSync, calculateUrgency };',
    '                window.NEXUS = { events, policies, crews, addEvent, addCrew, endOfDayReview, calculateUrgency };')

# ---------------------------------------------------------------- version sweep
# One intentional hit remains: the MIGRATION log text, which names the old
# v2.1 CLEAN key it migrated from. Every user-facing label must say NO-DEMO.
n = text.count('v2.1 CLEAN')
assert n == 1, f"v2.1 CLEAN left: {n} hits (expected exactly 1, the migration log)"
assert 'Migrated from v2.1 CLEAN' in text

# ---------------------------------------------------------------- storage safety checks
assert text.count('localStorage.') == 3, f"direct localStorage calls left: {text.count('localStorage.')}"
assert '09:47:22' not in text, "stale static clock time left"

# ---------------------------------------------------------------- forbidden checks
for bad in ['demoMode', 'injectRandomEvent', 'toggleDemoMode', 'updateDemoUI',
            'simulateOvernightSync', 'seedInitialData', 'startLiveSimulation',
            'toggleLiveMode', 'liveMode', 'liveInterval', 'resetDemo',
            'Math.random', 'godmode', 'TwistedGenius', 'DEMO MODE',
            'INJECT DEMO', 'CHAIN OF CUSTODY', 'OVERNIGHT SYNC', 'LIVE EVENT',
            'SAMPLE', 'ILLUSTR', 'demo roster', 'Demo data', 'DEMO DATA']:
    assert bad not in text, f"FORBIDDEN STILL PRESENT: {bad}"
# 'demo' (lowercase) may only appear in the migration filter (e.demo) and the
# old demo key literal in clearAllData — count and report, do not fail silently
demo_hits = [l for l in text.splitlines() if 'demo' in l.lower() and 'NO-DEMO' not in l]
print(f"lowercase/uppercase 'demo' lines left (excluding NO-DEMO): {len(demo_hits)}")
for l in demo_hits:
    print("  ", l.strip()[:160])

OUT.write_text(text)
print(f"WROTE {OUT} ({len(text)} chars, source was {orig_len})")
