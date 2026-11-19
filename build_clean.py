#!/usr/bin/env python3
"""Build nexus-ops-v2.1-clean.html from original.html (Pasted_text-2.txt).
All edits are explicit string replacements; any missed replacement fails loudly.
"""
import pathlib, sys
base = pathlib.Path(__file__).parent
src = (base / "original.html").read_text()
out = src

def rep(old, new, count=1):
    global out
    if old not in out:
        print(f"MISS: {old[:120]!r}")
        sys.exit(1)
    out = out.replace(old, new, count)

# --- Head / branding / icons ---
rep('<meta name="description" content="NEXUS OPS Field Command v2.1 - Real-time crew event tracking, automated discipline alerts, and modular policy enforcement. Zero delays. Unbeatable documentation. Built by DoubleA @ AntManThePro">',
    '<meta name="description" content="NEXUS OPS Field Command v2.1 CLEAN - Crew event tracking, discipline alerts, and modular policy enforcement. Local file, localStorage only. Demo data is labeled DEMO. Built by DoubleA @ AntManThePro">')
rep('<title>NEXUS OPS • Field Command v2.1</title>',
    '<title>NEXUS OPS • Field Command v2.1 CLEAN</title>\n    <link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">\n    <link rel="icon" type="image/png" sizes="512x512" href="icons/icon-512.png">\n    <link rel="apple-touch-icon" sizes="180x180" href="icons/icon-180.png">\n    <link rel="manifest" href="manifest.json">')
rep('<div class="text-[10px] text-white/50">@AntManThePro • godmode2025.net</div>',
    '<div class="text-[10px] text-white/50">@AntManThePro</div>')
rep('<img src="https://api.dicebear.com/7.x/avataaars/svg?seed=AntManThePro&backgroundColor=0a0a0f" class="w-full h-full object-cover" alt="DoubleA">',
    '<img src="icons/icon-192.png" class="w-full h-full object-cover" alt="NEXUS">')
rep('SYSTEM NOMINAL • 47 CREWS ONLINE',
    'SYSTEM NOMINAL • <span id="system-crews">8 CREWS IN ROSTER</span>')
rep('<div class="text-[9px] text-white/50 -mt-1 tracking-[3px]">FIELD COMMAND v2.1</div>',
    '<div class="text-[9px] text-white/50 -mt-1 tracking-[3px]">FIELD COMMAND v2.1 CLEAN</div>')

# --- Hero: demo toggle + real log-event button, honest LIVE badge ---
rep('<div class="px-4 py-1 rounded-3xl text-xs font-mono tracking-widest border border-[#00ff87]/40 text-[#00ff87] bg-[#00ff87]/5">LIVE</div>',
    '<div class="px-4 py-1 rounded-3xl text-xs font-mono tracking-widest border border-[#00ff87]/40 text-[#00ff87] bg-[#00ff87]/5">LOCAL</div>\n                    <button id="demo-toggle" onclick="toggleDemoMode()" class="px-4 py-1 rounded-3xl text-xs font-mono tracking-widest border border-white/30 text-white/70 bg-white/5">DEMO MODE: OFF</button>')
rep('''                <button onclick="injectRandomEvent()" 
                        class="flex items-center gap-x-2 px-5 py-3 rounded-3xl bg-[#00ff87] hover:bg-[#00ff87]/90 text-black font-bold text-sm transition-all active:scale-[0.985]">
                    <i class="fa-solid fa-bolt-lightning fa-fw"></i>
                    <span>INJECT EVENT</span>
                </button>''',
    '''                <button onclick="showEventForm()" 
                        class="flex items-center gap-x-2 px-5 py-3 rounded-3xl bg-[#00ff87] hover:bg-[#00ff87]/90 text-black font-bold text-sm transition-all active:scale-[0.985]">
                    <i class="fa-solid fa-plus fa-fw"></i>
                    <span>LOG EVENT</span>
                </button>
                <button id="inject-btn" onclick="injectRandomEvent()" 
                        class="flex items-center gap-x-2 px-5 py-3 rounded-3xl bg-white/5 hover:bg-white/10 border border-white/20 text-sm transition-all active:scale-[0.985]">
                    <i class="fa-solid fa-bolt-lightning fa-fw"></i>
                    <span>INJECT DEMO EVENT</span>
                </button>''')

# --- KPIs: honest initial values ---
rep('<div id="kpi-crew" class="text-5xl font-display tabular-nums mt-1">24</div>',
    '<div id="kpi-crew" class="text-5xl font-display tabular-nums mt-1">8</div>')
rep('<div class="text-xs text-white/50">/ 28 total • 2 on leave</div>',
    '<div class="text-xs text-white/50">/ 8 total • demo roster</div>')
rep('<div id="kpi-incidents" class="text-5xl font-display tabular-nums mt-1">9</div>',
    '<div id="kpi-incidents" class="text-5xl font-display tabular-nums mt-1">6</div>')
rep('''                        <div class="flex items-center gap-x-1.5 text-xs">
                            <span class="text-[#ffcc00]">+3 from sync</span>
                        </div>''',
    '''                        <div class="flex items-center gap-x-1.5 text-xs">
                            <span class="text-white/50">events in this file</span>
                        </div>''')
rep('<div class="text-xs px-3 py-1 bg-white/5 rounded-2xl font-mono text-white/60" id="event-count">142 EVENTS • 31 DAYS</div>',
    '<div class="text-xs px-3 py-1 bg-white/5 rounded-2xl font-mono text-white/60" id="event-count">6 EVENTS • DEMO DATA</div>')
rep('<div class="font-mono text-[#ff0080]" id="highest-urgency">142.6</div>',
    '<div class="font-mono text-[#ff0080]" id="highest-urgency">—</div>')
rep('<div>NEXUS PREDICT: <span class="text-[#ffcc00]">High risk window 22:00–02:00</span></div>',
    '<div>SAMPLE TREND: <span class="text-[#ffcc00]">illustrative only — not a forecast</span></div>')
rep('<div class="font-mono text-[#00ff87]">CONF 81%</div>',
    '<div class="font-mono text-white/50">SAMPLE</div>')
rep('<div>47 events processed today • Last overnight sync: <span id="last-sync">Today 05:41 CDT</span></div>',
    '<div><span id="footer-events">6 events in this file</span> • Last overnight sync: <span id="last-sync">Not run this session</span></div>')

# --- Canvas fixed heights so clientHeight is stable ---
rep('<canvas id="tactical-map" width="520" height="340" class="w-full"></canvas>',
    '<canvas id="tactical-map" width="520" height="340" class="w-full" style="height:340px"></canvas>')
rep('<canvas id="type-chart" width="460" height="240" class="w-full"></canvas>',
    '<canvas id="type-chart" width="460" height="240" class="w-full" style="height:240px"></canvas>')
rep('<canvas id="trend-chart" width="460" height="240" class="w-full"></canvas>',
    '<canvas id="trend-chart" width="460" height="240" class="w-full" style="height:240px"></canvas>')

# --- Urgency formula in the UI already says v2.4; keep it, code must match it ---
# (code fix is below)

# --- Real Log Event modal, inserted before Event Detail Modal ---
rep('''    <!-- Event Detail Modal -->''',
    '''    <!-- Log Event Modal (real entry; demo injection is separate) -->
    <div id="event-form-modal" onclick="if (event.target.id === 'event-form-modal') hideEventForm()" class="hidden fixed inset-0 bg-black/90 backdrop-blur z-[110] flex items-center justify-center p-6">
        <div onclick="event.stopImmediatePropagation()" class="glass w-full max-w-lg rounded-3xl border border-white/20 p-8">
            <div class="font-display text-2xl tracking-tight mb-1">Log Event</div>
            <div class="text-sm text-white/60 mb-6">A real entry for this file. Demo events are only made with INJECT DEMO EVENT when Demo Mode is on.</div>
            <div class="space-y-5">
                <div>
                    <label class="text-xs tracking-widest text-white/60 block mb-1.5">CREW</label>
                    <select id="form-crew" class="w-full bg-black/40 border border-white/20 px-4 py-3 rounded-2xl text-sm"></select>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="text-xs tracking-widest text-white/60 block mb-1.5">TYPE</label>
                        <select id="form-type" class="w-full bg-black/40 border border-white/20 px-4 py-3 rounded-2xl text-sm">
                            <option value="NO_CALL">No-Call / No-Show</option>
                            <option value="VIOLATION">Policy Violation</option>
                            <option value="ATTENDANCE">Attendance Anomaly</option>
                            <option value="RESIGN">Resignation</option>
                        </select>
                    </div>
                    <div>
                        <label class="text-xs tracking-widest text-white/60 block mb-1.5">SEVERITY (1-5)</label>
                        <select id="form-severity" class="w-full bg-black/40 border border-white/20 px-4 py-3 rounded-2xl text-sm">
                            <option value="1">1 — Minimal</option>
                            <option value="2">2 — Low</option>
                            <option value="3" selected>3 — Medium</option>
                            <option value="4">4 — High</option>
                            <option value="5">5 — Critical</option>
                        </select>
                    </div>
                </div>
                <div>
                    <label class="text-xs tracking-widest text-white/60 block mb-1.5">DETAILS (required)</label>
                    <textarea id="form-details" rows="3" placeholder="What happened, in plain words…" class="w-full bg-black/40 border border-white/20 px-4 py-3 rounded-2xl text-sm"></textarea>
                </div>
            </div>
            <div class="flex gap-x-3 mt-8">
                <button onclick="hideEventForm()" class="flex-1 py-3 rounded-2xl border border-white/30 text-sm">CANCEL</button>
                <button onclick="submitRealEvent()" class="flex-1 py-3 rounded-2xl bg-[#00ff87] text-black font-bold text-sm">SAVE EVENT</button>
            </div>
        </div>
    </div>

    <!-- Event Detail Modal -->''')

# ================= JS =================
# State keys + demo mode + helpers, inserted after liveInterval decl
rep('''        let liveInterval = null;
        let mapAnimationFrame = null;''',
    '''        let liveInterval = null;
        let mapAnimationFrame = null;
        let demoMode = false;
        const STATE_KEY = 'nexusOpsState_v21_clean';
        const LEGACY_STATE_KEY = 'nexusOpsState_v21';
        const DEMO_KEY = 'nexusOpsDemo_v21_clean';
        // Urgency formula shown in Alert Forge (v2.4):
        // urgency = (severity^2 x 1.8) + (minutes_open / 4.2) + (crew_risk x 11) - (acknowledged ? 28 : 0)''')

# saveState / loadState: new key + migration + notes revive
rep("""        function saveState() {
            const state = { events, policies, auditLog, lastSync: new Date().toISOString() };
            localStorage.setItem('nexusOpsState_v21', JSON.stringify(state));
        }""",
    """        function saveState() {
            const state = { events, policies, auditLog, lastSync: new Date().toISOString() };
            localStorage.setItem(STATE_KEY, JSON.stringify(state));
        }""")
rep("""        function loadState() {
            const saved = localStorage.getItem('nexusOpsState_v21');
            if (saved) {
                const parsed = JSON.parse(saved);
                events = parsed.events || [];
                policies = parsed.policies || [];
                auditLog = parsed.auditLog || [];
                
                // Re-hydrate dates
                events.forEach(e => e.timestamp = new Date(e.timestamp));
                auditLog.forEach(a => a.timestamp = new Date(a.timestamp));
            }
        }""",
    """        function loadState() {
            let saved = localStorage.getItem(STATE_KEY);
            if (!saved) saved = localStorage.getItem(LEGACY_STATE_KEY); // one-time migration from v2.1
            if (saved) {
                const parsed = JSON.parse(saved);
                events = parsed.events || [];
                policies = parsed.policies || [];
                auditLog = parsed.auditLog || [];

                // Re-hydrate dates, including note timestamps (were strings after JSON round-trip)
                events.forEach(e => {
                    e.timestamp = new Date(e.timestamp);
                    (e.notes || []).forEach(n => { n.time = new Date(n.time); });
                    if (e.acknowledgedAt) e.acknowledgedAt = new Date(e.acknowledgedAt);
                });
                auditLog.forEach(a => a.timestamp = new Date(a.timestamp));
            }
            try { demoMode = localStorage.getItem(DEMO_KEY) === '1'; } catch (e) { demoMode = false; }
        }
        function updateDemoUI() {
            const btn = document.getElementById('demo-toggle');
            if (btn) {
                btn.textContent = demoMode ? 'DEMO MODE: ON' : 'DEMO MODE: OFF';
                btn.className = demoMode
                    ? 'px-4 py-1 rounded-3xl text-xs font-mono tracking-widest border border-[#ff0080]/60 text-[#ff0080] bg-[#ff0080]/10'
                    : 'px-4 py-1 rounded-3xl text-xs font-mono tracking-widest border border-white/30 text-white/70 bg-white/5';
            }
            const inj = document.getElementById('inject-btn');
            if (inj) inj.style.opacity = demoMode ? '1' : '0.55';
        }
        function toggleDemoMode() {
            demoMode = !demoMode;
            try { localStorage.setItem(DEMO_KEY, demoMode ? '1' : '0'); } catch (e) {}
            updateDemoUI();
            showToast(demoMode ? 'Demo Mode ON — random events will be marked [DEMO].' : 'Demo Mode OFF — no random events will be created.', demoMode ? 'info' : 'success');
        }
        function showEventForm() {
            const sel = document.getElementById('form-crew');
            sel.innerHTML = crews.map(c => `<option value="${c.id}">${c.name} (${c.id}) — ${c.site}</option>`).join('');
            const m = document.getElementById('event-form-modal');
            m.classList.remove('hidden'); m.classList.add('flex');
        }
        function hideEventForm() {
            const m = document.getElementById('event-form-modal');
            m.classList.remove('flex'); m.classList.add('hidden');
        }
        function submitRealEvent() {
            const crewId = document.getElementById('form-crew').value;
            const type = document.getElementById('form-type').value;
            const sev = parseInt(document.getElementById('form-severity').value, 10);
            const details = document.getElementById('form-details').value.trim();
            if (!details) { alert('Details are required.'); return; }
            addEvent(type, crewId, details, sev, false);
            document.getElementById('form-details').value = '';
            hideEventForm();
        }
        function showCrewRoster() {
            const modal = document.getElementById('event-modal');
            const header = document.getElementById('modal-header');
            const body = document.getElementById('modal-body');
            header.innerHTML = '<div class="font-display text-3xl">CREW ROSTER</div><div class="text-xs text-white/50">' + crews.length + ' crew in this demo roster — not a live headcount</div>';
            body.innerHTML = '<div class="space-y-2">' + crews.map(c =>
                '<div class="flex justify-between text-sm p-3 bg-black/40 rounded-2xl border border-white/10"><div><div class="font-semibold">' + c.name + '</div><div class="text-xs text-white/50">' + c.role + ' • ' + c.site + '</div></div><div class="font-mono text-xs text-[#ffcc00]">risk ×' + c.risk.toFixed(1) + '</div></div>').join('') + '</div>';
            document.getElementById('modal-ack-btn').style.display = 'none';
            document.getElementById('modal-resolve-btn').style.display = 'none';
            modal.classList.remove('hidden'); modal.classList.add('flex');
        }""")

# Seed events: mark demo
for eid in ['"EVT-2401"', '"EVT-2402"', '"EVT-2403"', '"EVT-2404"', '"EVT-2405"', '"EVT-2398"']:
    # add demo:true after id line — handled by a targeted pass below instead
    pass

# Simpler: after seedInitialData's events array, mark all seeds demo in one place.
rep('''            logAudit("SYSTEM", "Initial seed data loaded with 6 events");''',
    '''            events.forEach(e => { e.demo = true; });
            logAudit("SYSTEM", "Initial seed data loaded with 6 DEMO events");''')

# Urgency: align code to displayed formula
rep('''            const crew = getCrewById(event.crewId);
            const severityFactor = Math.pow(event.severity, 1.85);
            const timeFactor = minutesOpen / 4.1;
            const riskFactor = (crew.risk || 1) * 12;
            const ackPenalty = (event.status === "ACKNOWLEDGED" || event.status === "RESOLVED") ? 29 : 0;''',
    '''            const crew = getCrewById(event.crewId);
            const severityFactor = Math.pow(event.severity, 2) * 1.8;
            const timeFactor = minutesOpen / 4.2;
            const riskFactor = (crew.risk || 1) * 11;
            const ackPenalty = (event.status === "ACKNOWLEDGED" || event.status === "RESOLVED") ? 28 : 0;''')

# addEvent: accept isDemo, mark it, log honestly
rep('''        function addEvent(type, crewId, details = "", severity = 3) {''',
    '''        function addEvent(type, crewId, details = "", severity = 3, isDemo = null) {
            if (isDemo === null) isDemo = demoMode;''')
rep('''                severity: severity,
                status: "OPEN",
                details: details || getDefaultDetails(type),''',
    '''                severity: severity,
                status: "OPEN",
                demo: !!isDemo,
                details: details || getDefaultDetails(type),''')
rep('''            logAudit("EVENT_CREATED", `${type} reported for ${crew.name}`, newEvent.id);''',
    '''            logAudit("EVENT_CREATED", `${type} reported for ${crew.name}${newEvent.demo ? ' [DEMO]' : ''}`, newEvent.id);''')
rep('''            showToast(`${type} event logged`, "success");''',
    '''            showToast(`${type} event logged${newEvent.demo ? ' [DEMO]' : ''}`, "success");''')

# injectRandomEvent: demo-gated
rep('''        function injectRandomEvent() {
            const types = ["NO_CALL", "VIOLATION", "ATTENDANCE", "NO_CALL", "VIOLATION"];''',
    '''        function injectRandomEvent() {
            if (!demoMode) { showToast("Demo Mode is OFF — turn it on to inject a demo event. Use LOG EVENT for a real entry.", "info"); return; }
            const types = ["NO_CALL", "VIOLATION", "ATTENDANCE", "NO_CALL", "VIOLATION"];''')
rep('''            const evt = addEvent(type, randomCrew.id, details, sev);''',
    '''            const evt = addEvent(type, randomCrew.id, details, sev, true);''')

# updateKPIs: no +5, crew from roster, footer count
rep('''            document.getElementById('kpi-crew').innerHTML = '24';
            document.getElementById('kpi-incidents').innerHTML = openIncidents + 5; // + historical flavor
            document.getElementById('kpi-alerts').innerHTML = criticalAlerts;''',
    '''            document.getElementById('kpi-crew').innerHTML = crews.length;
            document.getElementById('kpi-incidents').innerHTML = events.length;
            document.getElementById('kpi-alerts').innerHTML = criticalAlerts;
            const fe = document.getElementById('footer-events');
            if (fe) fe.textContent = events.length + ' events in this file';''')

# renderEventFeed: DEMO pill
rep('''                            <span class="status-pill ${statusColor} border border-current/40">${evt.status}</span>''',
    '''                            <span class="status-pill ${statusColor} border border-current/40">${evt.status}</span>${evt.demo ? '<span class="status-pill text-[#ff0080] border border-[#ff0080]/40">DEMO</span>' : ''}''')

# renderTable: honest day span + DEMO tag
rep('''            document.getElementById('event-count').innerHTML = `${events.length} EVENTS • ${Math.ceil(events.length / 4.2)} DAYS`;''',
    '''            const demoCount = events.filter(e => e.demo).length;
            const daySpan = events.length ? Math.max(1, Math.ceil((Math.max(...events.map(e => e.timestamp)) - Math.min(...events.map(e => e.timestamp))) / 86400000)) : 0;
            document.getElementById('event-count').innerHTML = `${events.length} EVENTS • ${daySpan} DAY${daySpan === 1 ? '' : 'S'}${demoCount ? ' • ' + demoCount + ' DEMO' : ''}`;''')
rep('''                    <td class="py-3.5 px-4">
                        <div class="font-semibold">${evt.type.replace('_', ' ')}</div>''',
    '''                    <td class="py-3.5 px-4">
                        <div class="font-semibold">${evt.type.replace(/_/g, ' ')}${evt.demo ? ' <span class="text-[10px] px-2 py-px rounded bg-[#ff0080]/10 text-[#ff0080]">DEMO</span>' : ''}</div>''')

# Policy chips: track selection, read it on deploy
rep('''            types.forEach(t => {
                const chip = document.createElement('div');
                chip.className = `cursor-pointer px-3 py-1 text-xs rounded-2xl border border-white/30 select-none ${t === "NO_CALL" || t === "VIOLATION" ? 'bg-[#ff0080]/20 border-[#ff0080]/60' : ''}`;
                chip.innerHTML = t.replace('_', ' ');
                chip.onclick = () => {
                    chip.classList.toggle('bg-[#ff0080]/20');
                    chip.classList.toggle('border-[#ff0080]/60');
                };
                chipContainer.appendChild(chip);
            });''',
    '''            types.forEach(t => {
                const chip = document.createElement('div');
                const selected = (t === "NO_CALL" || t === "VIOLATION");
                chip.dataset.type = t;
                chip.dataset.selected = selected ? "1" : "0";
                chip.className = `cursor-pointer px-3 py-1 text-xs rounded-2xl border border-white/30 select-none ${selected ? 'bg-[#ff0080]/20 border-[#ff0080]/60' : ''}`;
                chip.innerHTML = t.replace(/_/g, ' ');
                chip.onclick = () => {
                    const on = chip.dataset.selected !== "1";
                    chip.dataset.selected = on ? "1" : "0";
                    chip.classList.toggle('bg-[#ff0080]/20', on);
                    chip.classList.toggle('border-[#ff0080]/60', on);
                };
                chipContainer.appendChild(chip);
            });''')
rep('''            // Get selected types from chips (simplified)
            const selectedTypes = ["NO_CALL", "VIOLATION"]; // For demo, we hardcode some. In real would read chips.''',
    '''            const selectedTypes = [...document.querySelectorAll('#policy-type-chips > div')]
                .filter(ch => ch.dataset.selected === "1").map(ch => ch.dataset.type);
            if (selectedTypes.length === 0) { alert("Pick at least one trigger event type."); return; }''')

# --- Canvas sizing: fitCanvas helper + use it in all three draw functions ---
rep('''        function updateTacticalMap() {
            const canvas = document.getElementById('tactical-map');
            if (!canvas) return;
            const ctx = canvas.getContext('2d', { alpha: true });
            
            const W = canvas.width;
            const H = canvas.height;''',
    '''        // Size a canvas from its CSS size x devicePixelRatio, drawing in design-pixel coords.
        function fitCanvas(canvas, designW, designH) {
            if (!canvas) return null;
            const dpr = window.devicePixelRatio || 1;
            const cw = canvas.clientWidth || designW;
            const ch = canvas.clientHeight || designH;
            canvas.width = Math.round(cw * dpr);
            canvas.height = Math.round(ch * dpr);
            const ctx = canvas.getContext('2d');
            if (!ctx) return null;
            ctx.setTransform(dpr * (cw / designW), 0, 0, dpr * (ch / designH), 0, 0);
            return { ctx, W: designW, H: designH };
        }
        function updateTacticalMap() {
            const canvas = document.getElementById('tactical-map');
            const fitted = fitCanvas(canvas, 520, 340);
            if (!fitted) return;
            const { ctx, W, H } = fitted;''')
rep('''        function drawTypeChart() {
            const canvas = document.getElementById('type-chart');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);''',
    '''        function drawTypeChart() {
            const canvas = document.getElementById('type-chart');
            const fitted = fitCanvas(canvas, 460, 240);
            if (!fitted) return;
            const { ctx } = fitted;
            ctx.clearRect(0, 0, 460, 240);''')
rep('''                ctx.fillText(t.replace('_', '\\n'), x + 6, baseY + 18);''',
    '''                ctx.fillText(t.replace(/_/g, ' '), x + 6, baseY + 18);''')
rep('''        function drawTrendChart() {
            const canvas = document.getElementById('trend-chart');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Fake 7-day data + prediction
            const days = ['18', '19', '20', '21', '22', '23', '24'];
            const values = [14, 9, 17, 11, 22, 15, 19];
            const pred = [21, 24]; // predicted next 2 days''',
    '''        function drawTrendChart() {
            const canvas = document.getElementById('trend-chart');
            const fitted = fitCanvas(canvas, 460, 240);
            if (!fitted) return;
            const { ctx } = fitted;
            ctx.clearRect(0, 0, 460, 240);

            // SAMPLE 7-day data + illustrative projection — not real events, not a forecast.
            const days = ['18', '19', '20', '21', '22', '23', '24'];
            const values = [14, 9, 17, 11, 22, 15, 19];
            const pred = [21, 24]; // illustrative next 2 days''')
rep('''            // Legend
            ctx.fillStyle = '#60efff';
            ctx.fillRect(310, 18, 14, 3);
            ctx.fillStyle = '#ffffff';
            ctx.fillText('ACTUAL', 330, 23);
            
            ctx.fillStyle = '#ffcc00';
            ctx.fillRect(380, 18, 14, 3);
            ctx.fillStyle = '#ffffff';
            ctx.fillText('PREDICT', 400, 23);''',
    '''            // Legend
            ctx.fillStyle = '#60efff';
            ctx.fillRect(310, 18, 14, 3);
            ctx.fillStyle = '#ffffff';
            ctx.fillText('SAMPLE', 330, 23);

            ctx.fillStyle = '#ffcc00';
            ctx.fillRect(380, 18, 14, 3);
            ctx.fillStyle = '#ffffff';
            ctx.fillText('ILLUSTR.', 400, 23);''')

# showKPIDrill crew: real roster instead of dead-end toast
rep('''            } else {
                showToast("Crew roster drill-down would open here in production build.", "info");
            }''',
    '''            } else {
                showCrewRoster();
            }''')

# Overnight sync: demo-gated, honest counts, no fake critical claim
rep('''        function simulateOvernightSync() {
            const btns = document.querySelectorAll('button');
            btns.forEach(b => b.disabled = true);
            
            showToast("Syncing overnight field logs...", "info");''',
    '''        function simulateOvernightSync() {
            const btns = document.querySelectorAll('button');
            if (!demoMode) {
                showToast("Overnight sync is a demo — turn Demo Mode on to run the sample sync.", "info");
                logAudit("OVER NIGHT_SYNC", "Sample sync skipped: Demo Mode is OFF. No events added.");
                return;
            }
            btns.forEach(b => b.disabled = true);

            showToast("Syncing overnight field logs (DEMO)...", "info");''')
rep('''                    events.unshift(evt);
                    checkAndTriggerPolicies(evt);
                });
                
                logAudit("OVER NIGHT_SYNC", `Processed 3 overnight submissions. 1 new critical alert generated.`);
                
                updateAllUI();
                document.getElementById('last-sync').innerHTML = "Just now";
                
                showToast("Overnight sync complete. 1 new discipline gap flagged.", "success");''',
    '''                    evt.demo = true;
                    events.unshift(evt);
                    checkAndTriggerPolicies(evt);
                });

                const openNow = events.filter(e => e.status !== "RESOLVED").length;
                logAudit("OVER NIGHT_SYNC", `Processed 3 DEMO overnight submissions. ${openNow} events open now.`);

                updateAllUI();
                document.getElementById('last-sync').innerHTML = "Just now";

                showToast("Demo overnight sync complete. 3 demo events added.", "success");''')

# Live simulation: only inject in demo mode
rep('''                // 22% chance to inject a minor event
                if (Math.random() < 0.22) {
                    const lowSevTypes = ["ATTENDANCE", "NO_CALL"];
                    const type = lowSevTypes[Math.floor(Math.random() * lowSevTypes.length)];
                    const crew = crews[Math.floor(Math.random() * crews.length)];
                    addEvent(type, crew.id, undefined, type === "NO_CALL" ? 3 : 2);
                }''',
    '''                // 22% chance to inject a minor event — demo only
                if (demoMode && Math.random() < 0.22) {
                    const lowSevTypes = ["ATTENDANCE", "NO_CALL"];
                    const type = lowSevTypes[Math.floor(Math.random() * lowSevTypes.length)];
                    const crew = crews[Math.floor(Math.random() * crews.length)];
                    addEvent(type, crew.id, undefined, type === "NO_CALL" ? 3 : 2, true);
                }''')

# Keyboard: N opens real form when demo off, injects demo when on
rep('''                if (e.key.toLowerCase() === 'n' && document.activeElement.tagName === "BODY") {
                    e.preventDefault();
                    injectRandomEvent();
                }''',
    '''                if (e.key.toLowerCase() === 'n' && document.activeElement.tagName === "BODY") {
                    e.preventDefault();
                    if (demoMode) injectRandomEvent(); else showEventForm();
                }''')

# Export report: no banned branding, honest math, demo note
rep('''            const resolvedCount = events.filter(e => e.status === "RESOLVED").length;
            const avgResp = Math.round(events.filter(e => e.responseTime).reduce((a,b) => a + b.responseTime, 0) / Math.max(1, events.length));''',
    '''            const resolvedCount = events.filter(e => e.status === "RESOLVED").length;
            const resolvedWithTime = events.filter(e => e.responseTime);
            const avgResp = resolvedWithTime.length ? Math.round(resolvedWithTime.reduce((a,b) => a + b.responseTime, 0) / resolvedWithTime.length) : 0;''')
rep('''ACTIVE CREW: 24 / 28''',
    '''ACTIVE CREW: ${crews.length} / ${crews.length} (demo roster)''')
rep('''NEXUS v2.1 • godmode2025.net • UNRULY OPS READY''',
    '''NEXUS OPS Field Command v2.1 CLEAN • Local file — demo events marked [DEMO]: ${events.filter(e => e.demo).length} of ${events.length}''')

# PWA prompt: guard undefined deferredPrompt
rep('''                        banner.querySelector('button').onclick = () => {
                            deferredPrompt.prompt();
                            banner.remove();
                        };''',
    '''                        banner.querySelector('button').onclick = () => {
                            if (deferredPrompt) deferredPrompt.prompt();
                            banner.remove();
                        };''')

# Remove fake icon console log
rep('''                console.log("%c[READY] Custom app icon generated and available in /artifacts/imagine_images/5s2hF.jpg", "color:#ffcc00");
''', '')
rep('''            console.log("%c[NEXUS OPS v2.1] Booting Field Command Dashboard...", "color:#00ff87");''',
    '''            console.log("%c[NEXUS OPS v2.1 CLEAN] Booting Field Command Dashboard...", "color:#00ff87");''')
rep('''                    showToast("NEXUS OPS v2.1 online. All systems nominal.", "success");''',
    '''                    showToast("NEXUS OPS v2.1 CLEAN online. Demo Mode is " + (demoMode ? "ON" : "OFF") + ".", "success");''')

# resetDemo: new key (and legacy, so a reset really clears)
rep('''            localStorage.removeItem('nexusOpsState_v21');''',
    '''            localStorage.removeItem(STATE_KEY);
            localStorage.removeItem(LEGACY_STATE_KEY);''')

# Boot: apply demo UI + resize redraw
rep('''                loadState();
                seedPolicies();
                seedInitialData();''',
    '''                loadState();
                seedPolicies();
                seedInitialData();
                updateDemoUI();
                let resizeTimer = null;
                window.addEventListener('resize', () => {
                    clearTimeout(resizeTimer);
                    resizeTimer = setTimeout(() => { updateTacticalMap(); drawTypeChart(); drawTrendChart(); }, 150);
                });''')

# Policy alert events created by the engine are also demo-derived when the trigger was demo;
# mark them in checkAndTriggerPolicies (they inherit the triggering event's flag via newEvent)
rep('''                            details: `POLICY BREACH: ${policy.name} — ${recent.length} occurrences in ${policy.periodHours}h window. ${policy.action}`,''',
    '''                            demo: !!newEvent.demo,
                            details: `POLICY BREACH: ${policy.name} — ${recent.length} occurrences in ${policy.periodHours}h window. ${policy.action}`,''')

(base / "nexus-ops-v2.1-clean.html").write_text(out)
print("wrote", len(out), "bytes")
# sanity: banned must be gone
for bad in ("godmode2025", "TwistedGenius", "imagine_images"):
    assert bad not in out, bad
print("banned check: 0 hits")
