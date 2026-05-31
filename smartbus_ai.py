from flask import Flask, render_template_string

app = Flask(__name__)

page = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Smart Seva — AI Transit Command</title>
<meta name="description" content="Smart Seva: AI-powered public transport crowd management with real-time GPS tracking, demand prediction, and route optimization for Nagpur.">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
:root {
  --neon: #00f5d4;
  --neon2: #7c3aed;
  --neon3: #f59e0b;
  --bg: #04070f;
  --bg2: #080d1a;
  --bg3: #0d1424;
  --glass: rgba(255,255,255,0.04);
  --glass-border: rgba(0,245,212,0.18);
  --text: #e2e8f0;
  --muted: #64748b;
  --red: #ef4444;
  --green: #22c55e;
  --yellow: #eab308;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', sans-serif;
  background: var(--bg);
  color: var(--text);
  overflow: hidden;
  height: 100vh;
}

body::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% 20%, rgba(124,58,237,0.08) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,245,212,0.06) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

/* ── HEADER ── */
header {
  position: relative;
  z-index: 100;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  background: rgba(8,13,26,0.97);
  border-bottom: 1px solid var(--glass-border);
  backdrop-filter: blur(20px);
  box-shadow: 0 0 40px rgba(0,245,212,0.06);
}

.logo {
  font-family: 'Orbitron', monospace;
  font-size: 20px;
  font-weight: 900;
  background: linear-gradient(135deg, var(--neon), var(--neon2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  font-size: 26px;
  -webkit-text-fill-color: initial;
  filter: drop-shadow(0 0 8px var(--neon));
  animation: pulse-icon 2s infinite;
}

@keyframes pulse-icon {
  0%,100% { filter: drop-shadow(0 0 8px var(--neon)); }
  50%      { filter: drop-shadow(0 0 20px var(--neon)) brightness(1.3); }
}

.nav { display: flex; gap: 6px; }

.nav-btn {
  background: var(--glass);
  border: 1px solid rgba(100,116,139,0.25);
  color: var(--muted);
  padding: 8px 18px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 13px;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
}

.nav-btn:hover, .nav-btn.active {
  color: white;
  border-color: var(--neon);
  box-shadow: 0 0 16px rgba(0,245,212,0.3), inset 0 0 16px rgba(0,245,212,0.05);
  background: linear-gradient(135deg, rgba(0,245,212,0.12), rgba(124,58,237,0.12));
  transform: translateY(-1px);
}

.header-stats { display: flex; gap: 22px; align-items: center; }

.hstat { text-align: center; }
.hstat-val {
  font-family: 'Orbitron', monospace;
  font-size: 16px; font-weight: 700;
  color: var(--neon); text-shadow: 0 0 10px var(--neon);
}
.hstat-label { font-size: 9px; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }

.live-dot {
  width: 8px; height: 8px;
  background: var(--green); border-radius: 50%;
  box-shadow: 0 0 10px var(--green);
  animation: blink 1s infinite;
  display: inline-block; margin-right: 5px;
}

@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── VIEW SYSTEM ── */
.view { display: none; height: calc(100vh - 64px); position: relative; z-index: 1; }
.v-active { display: flex !important; }

/* ── PASSENGER SIDEBAR ── */
.sidebar {
  width: 340px;
  background: rgba(8,13,26,0.98);
  border-right: 1px solid var(--glass-border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.sidebar-header {
  padding: 16px 18px 12px;
  border-bottom: 1px solid rgba(0,245,212,0.1);
  display: flex; align-items: center; gap: 10px;
}

.sidebar-title {
  font-family: 'Orbitron', monospace;
  font-size: 12px; font-weight: 700;
  color: var(--neon); letter-spacing: 1px;
}

.search-box { padding: 10px 18px; }

.search-input {
  width: 100%;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(0,245,212,0.2);
  border-radius: 8px;
  padding: 8px 12px;
  color: white; font-size: 13px; outline: none;
  transition: border-color 0.3s;
}

.search-input:focus { border-color: var(--neon); box-shadow: 0 0 10px rgba(0,245,212,0.15); }

.bus-list { overflow-y: auto; flex: 1; padding: 8px; }

.bus-card {
  background: rgba(13,20,36,0.9);
  border: 1px solid rgba(100,116,139,0.2);
  border-radius: 12px; padding: 14px; margin-bottom: 8px;
  cursor: pointer; transition: all 0.3s ease;
  position: relative; overflow: hidden;
}
.bus-card::before {
  content: '';
  position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
  background: linear-gradient(to bottom, var(--neon), var(--neon2));
  border-radius: 3px 0 0 3px;
}
.bus-card:hover {
  border-color: var(--neon);
  box-shadow: 0 0 20px rgba(0,245,212,0.12), 0 4px 20px rgba(0,0,0,0.4);
  transform: translateX(3px);
  background: rgba(0,245,212,0.04);
}

.bus-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }

.bus-number {
  font-family: 'Orbitron', monospace;
  font-size: 18px; font-weight: 700;
  color: var(--neon); text-shadow: 0 0 8px rgba(0,245,212,0.5);
}

.eta-badge {
  background: rgba(0,245,212,0.1);
  border: 1px solid rgba(0,245,212,0.3);
  color: var(--neon);
  padding: 3px 10px; border-radius: 20px;
  font-size: 11px; font-weight: 700;
  font-family: 'Orbitron', monospace;
}

.bus-dest { font-size: 12px; color: var(--muted); margin-bottom: 8px; letter-spacing: 0.5px; }

.crowd-label { font-size: 10px; color: var(--muted); margin-bottom: 4px; display: flex; justify-content: space-between; }

.crowd-bar-container { background: rgba(255,255,255,0.06); border-radius: 4px; height: 6px; overflow: hidden; }

.crowd-bar {
  height: 100%; border-radius: 4px; transition: width 1.2s ease;
  position: relative;
}
.crowd-bar::after {
  content: '';
  position: absolute; inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3));
  animation: shimmer 2s infinite;
}
@keyframes shimmer { 0%{transform:translateX(-100%)} 100%{transform:translateX(100%)} }

.crowd-low  { background: linear-gradient(90deg, #22c55e, #4ade80); }
.crowd-med  { background: linear-gradient(90deg, #eab308, #fbbf24); }
.crowd-high { background: linear-gradient(90deg, #ef4444, #f87171); }

/* ── MAP AREA ── */
.map-area { flex: 1; position: relative; }
#map, #adminmap { height: 100%; width: 100%; }

.map-overlay {
  position: absolute; top: 12px; right: 12px; z-index: 999;
  background: rgba(8,13,26,0.9);
  border: 1px solid var(--glass-border);
  border-radius: 12px; padding: 12px 16px;
  backdrop-filter: blur(10px);
}
.map-overlay-title { font-size: 11px; font-family: 'Orbitron', monospace; color: var(--neon); margin-bottom: 8px; letter-spacing: 1px; }
.legend-item { display: flex; align-items: center; gap: 8px; font-size: 11px; color: var(--muted); margin-bottom: 4px; }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }

/* ── AI DEMAND PANEL ── */
.ai-panel {
  position: absolute; bottom: 12px; left: 12px; z-index: 999;
  background: rgba(8,13,26,0.92);
  border: 1px solid rgba(124,58,237,0.4);
  border-radius: 14px; padding: 14px 18px;
  backdrop-filter: blur(15px); width: 320px;
  box-shadow: 0 0 30px rgba(124,58,237,0.15);
}
.ai-panel-title {
  font-family: 'Orbitron', monospace; font-size: 11px;
  color: #a78bfa; letter-spacing: 1.5px; margin-bottom: 10px;
  display: flex; align-items: center; gap: 8px;
}
.ai-tag {
  background: linear-gradient(135deg, #7c3aed, #4f46e5);
  font-size: 9px; padding: 2px 8px; border-radius: 10px;
  color: white; letter-spacing: 1px;
}

/* ── ROUTE OPTIMIZATION ── */
.route-panel {
  position: absolute; top: 12px; left: 12px; z-index: 999;
  background: rgba(8,13,26,0.92);
  border: 1px solid rgba(245,158,11,0.35);
  border-radius: 14px; padding: 14px 18px;
  backdrop-filter: blur(15px); width: 240px;
  box-shadow: 0 0 25px rgba(245,158,11,0.1);
}
.route-panel-title { font-family: 'Orbitron', monospace; font-size: 11px; color: var(--neon3); letter-spacing: 1.5px; margin-bottom: 10px; }
.route-item { display: flex; align-items: center; gap: 10px; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
.route-rank { font-family: 'Orbitron', monospace; font-size: 15px; font-weight: 700; width: 22px; }
.route-rank.r1 { color: #ffd700; text-shadow: 0 0 10px #ffd700; }
.route-rank.r2 { color: #c0c0c0; }
.route-rank.r3 { color: #cd7f32; }
.route-info { flex: 1; }
.route-name { font-size: 11px; font-weight: 600; }
.route-score { font-size: 10px; color: var(--green); }
.route-bar { width: 50px; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; }
.route-bar-fill { height: 100%; border-radius: 2px; transition: width 1.5s ease; }

/* ── BUS STOP VIEW ── */
#stop {
  flex-direction: column;
  background: radial-gradient(ellipse at center, #060d1f 0%, #04070f 100%);
  overflow: auto; align-items: stretch;
}

.stop-header {
  padding: 28px 40px 18px;
  display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid rgba(0,245,212,0.1);
}
.stop-name { font-family: 'Orbitron', monospace; font-size: 26px; font-weight: 900; color: var(--neon); text-shadow: 0 0 20px var(--neon); letter-spacing: 3px; }
.stop-subtitle { font-size: 12px; color: var(--muted); margin-top: 4px; letter-spacing: 2px; }
.stop-clock { font-family: 'Orbitron', monospace; font-size: 40px; font-weight: 700; color: white; text-align: right; text-shadow: 0 0 15px rgba(255,255,255,0.3); }
.stop-date { font-size: 12px; color: var(--muted); text-align: right; margin-top: 4px; }

.voice-controls { padding: 14px 40px; display: flex; gap: 10px; align-items: center; }
.voice-label { font-size: 11px; color: var(--muted); letter-spacing: 1px; margin-right: 4px; }
.voice-btn {
  background: rgba(37,99,235,0.15); border: 1px solid rgba(37,99,235,0.4);
  color: #60a5fa; padding: 8px 18px; border-radius: 8px;
  cursor: pointer; font-weight: 600; font-size: 12px; transition: all 0.3s; letter-spacing: 0.5px;
}
.voice-btn:hover { background: rgba(37,99,235,0.3); box-shadow: 0 0 15px rgba(37,99,235,0.3); transform: translateY(-1px); }

.stop-table-container { padding: 0 30px 30px; flex: 1; }
.stop-table { width: 100%; border-collapse: collapse; border-radius: 12px; overflow: hidden; }
.stop-table thead th {
  background: rgba(0,245,212,0.08); padding: 14px 18px; text-align: left;
  font-family: 'Orbitron', monospace; font-size: 10px; color: var(--neon); letter-spacing: 2px;
  border-bottom: 1px solid rgba(0,245,212,0.2);
}
.stop-table tbody tr { border-bottom: 1px solid rgba(255,255,255,0.04); transition: background 0.3s; }
.stop-table tbody tr:hover { background: rgba(0,245,212,0.04); }
.stop-table tbody td { padding: 14px 18px; font-size: 14px; }
.arriving-soon { background: rgba(0,245,212,0.05) !important; border-left: 3px solid var(--neon) !important; }
.crowd-chip { display: inline-flex; align-items: center; gap: 5px; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.chip-low  { background: rgba(34,197,94,0.15); color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
.chip-med  { background: rgba(234,179,8,0.15); color: #fbbf24; border: 1px solid rgba(234,179,8,0.3); }
.chip-high { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.eta-cell { font-family: 'Orbitron', monospace; font-size: 16px; font-weight: 700; }
.eta-urgent { color: #f87171; text-shadow: 0 0 8px rgba(239,68,68,0.5); }
.eta-soon   { color: #fbbf24; }
.eta-ok     { color: var(--neon); }

/* ── ADMIN VIEW ── */
#admin { flex-direction: row; }

.admin-sidebar {
  width: 440px;
  background: rgba(8,13,26,0.98);
  border-right: 1px solid var(--glass-border);
  display: flex; flex-direction: column;
  overflow-y: auto;
  height: calc(100vh - 64px);
  padding: 16px; gap: 14px;
}

/* scrollbar */
.admin-sidebar::-webkit-scrollbar { width: 5px; }
.admin-sidebar::-webkit-scrollbar-track { background: transparent; }
.admin-sidebar::-webkit-scrollbar-thumb { background: rgba(0,245,212,0.2); border-radius: 10px; }

.admin-title {
  font-family: 'Orbitron', monospace; font-size: 12px;
  letter-spacing: 2px; color: var(--neon);
  padding-bottom: 12px; border-bottom: 1px solid rgba(0,245,212,0.1);
  display: flex; align-items: center; gap: 8px;
}

.card {
  background: rgba(13,20,36,0.8);
  border: 1px solid rgba(100,116,139,0.2);
  border-radius: 14px; padding: 16px;
  position: relative; overflow: hidden;
  flex-shrink: 0;
}
.card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--neon), transparent);
  opacity: 0.3;
}
.card-title { font-family: 'Orbitron', monospace; font-size: 10px; color: var(--muted); letter-spacing: 1.5px; margin-bottom: 12px; text-transform: uppercase; }

.fleet-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.fleet-stat { background: rgba(0,245,212,0.05); border: 1px solid rgba(0,245,212,0.12); border-radius: 10px; padding: 10px; text-align: center; }
.fleet-val { font-family: 'Orbitron', monospace; font-size: 22px; font-weight: 900; text-shadow: 0 0 10px rgba(0,245,212,0.5); }
.fleet-label { font-size: 9px; color: var(--muted); letter-spacing: 1px; margin-top: 2px; }

.crowd-stop-item { display: flex; align-items: center; gap: 10px; padding: 7px 0; border-bottom: 1px solid rgba(255,255,255,0.04); }
.stop-sname { flex: 1; font-size: 12px; }
.stop-count { font-family: 'Orbitron', monospace; font-size: 13px; font-weight: 700; }
.stop-mini-bar { width: 55px; height: 4px; background: rgba(255,255,255,0.08); border-radius: 2px; }
.stop-mini-fill { height: 100%; border-radius: 2px; }

/* Smart Dispatch */
.dispatch-log { font-size: 12px; line-height: 2; min-height: 24px; }

.dispatch-btn {
  width: 100%; padding: 11px;
  background: linear-gradient(135deg, rgba(0,245,212,0.15), rgba(124,58,237,0.15));
  border: 1px solid var(--neon); color: var(--neon);
  border-radius: 10px; cursor: pointer;
  font-family: 'Orbitron', monospace; font-size: 11px; letter-spacing: 2px;
  transition: all 0.3s; margin-top: 10px;
}
.dispatch-btn:hover {
  background: linear-gradient(135deg, rgba(0,245,212,0.25), rgba(124,58,237,0.25));
  box-shadow: 0 0 20px rgba(0,245,212,0.2); transform: translateY(-1px);
}

.alert-item {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 8px; background: rgba(239,68,68,0.06);
  border: 1px solid rgba(239,68,68,0.2);
  border-radius: 8px; margin-bottom: 6px; font-size: 12px;
}
.alert-dot { width: 6px; height: 6px; border-radius: 50%; background: #ef4444; margin-top: 4px; flex-shrink: 0; animation: blink 0.8s infinite; }

/* Toast */
.toast {
  position: fixed; bottom: 24px; right: 24px;
  background: rgba(8,13,26,0.95); border: 1px solid var(--neon);
  border-radius: 12px; padding: 12px 20px;
  color: var(--neon); font-family: 'Orbitron', monospace; font-size: 11px; letter-spacing: 1px;
  z-index: 9999; transform: translateX(220px); opacity: 0;
  transition: all 0.4s ease; box-shadow: 0 0 25px rgba(0,245,212,0.2);
}
.toast.show { transform: translateX(0); opacity: 1; }

/* Map dark tiles */
.leaflet-tile { filter: brightness(0.38) saturate(0.4) hue-rotate(200deg) !important; }
.leaflet-container { background: #0b1220 !important; }

/* Scrollbar global */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,245,212,0.2); border-radius: 10px; }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.bus-card { animation: fadeInUp 0.35s ease; }

@keyframes glow-pulse {
  0%,100% { box-shadow: 0 0 10px rgba(0,245,212,0.2); }
  50%      { box-shadow: 0 0 25px rgba(0,245,212,0.5); }
}
.glow-pulse { animation: glow-pulse 2.5s infinite; }
</style>
</head>
<body>

<!-- HEADER -->
<header>
  <div class="logo"><span class="logo-icon">🚌</span>SMART SEVA</div>

  <div class="nav">
    <button id="btn-passenger" class="nav-btn active" onclick="switchView('passenger')">🗺 Passenger</button>
    <button id="btn-stop"      class="nav-btn"        onclick="switchView('stop')">🚏 Bus Stop</button>
    <button id="btn-admin"     class="nav-btn"        onclick="switchView('admin')">⚡ Admin</button>
  </div>

  <div class="header-stats">
    <div class="hstat"><div class="hstat-val" id="h-buses">18</div><div class="hstat-label">Active Buses</div></div>
    <div class="hstat"><div class="hstat-val" id="h-pass">—</div><div class="hstat-label">Passengers</div></div>
    <div class="hstat"><div class="hstat-val" id="h-alert" style="color:#ef4444;text-shadow:0 0 10px #ef4444">2</div><div class="hstat-label">Alerts</div></div>
    <div style="display:flex;align-items:center;font-size:11px;color:var(--muted)"><span class="live-dot"></span>LIVE</div>
  </div>
</header>

<!-- ══════════ PASSENGER VIEW ══════════ -->
<div id="passenger" class="view v-active" style="flex-direction:row;">

  <div class="sidebar">
    <div class="sidebar-header"><span>🛰</span><div class="sidebar-title">LIVE BUS TRACKER</div></div>
    <div class="search-box">
      <input class="search-input" id="searchInput" type="text" placeholder="🔍  Search route or destination…" oninput="filterBuses()">
    </div>
    <div class="bus-list" id="busList"></div>
  </div>

  <div class="map-area">
    <div id="map"></div>

    <div class="route-panel">
      <div class="route-panel-title">⚡ OPTIMAL ROUTES</div>
      <div id="routeList"></div>
    </div>

    <div class="ai-panel">
      <div class="ai-panel-title">🤖 DEMAND FORECAST<span class="ai-tag">AI</span></div>
      <canvas id="demandChart" height="100"></canvas>
    </div>

    <div class="map-overlay">
      <div class="map-overlay-title">🗺 LEGEND</div>
      <div class="legend-item"><div class="legend-dot" style="background:#22c55e"></div>Low crowd</div>
      <div class="legend-item"><div class="legend-dot" style="background:#eab308"></div>Moderate</div>
      <div class="legend-item"><div class="legend-dot" style="background:#ef4444"></div>High crowd</div>
      <div class="legend-item"><div class="legend-dot" style="background:var(--neon)"></div>Optimized route</div>
    </div>
  </div>

</div>

<!-- ══════════ BUS STOP VIEW ══════════ -->
<div id="stop" class="view" style="display:none; flex-direction:column;">

  <div class="stop-header">
    <div>
      <div class="stop-name">🚏 SITABULDI BUS STOP</div>
      <div class="stop-subtitle"><span class="live-dot"></span>REAL-TIME ARRIVALS · NAGPUR</div>
    </div>
    <div>
      <div class="stop-clock" id="clock">00:00:00</div>
      <div class="stop-date" id="stopDate"></div>
    </div>
  </div>

  <div class="voice-controls">
    <span class="voice-label">🔊 ANNOUNCE:</span>
    <button class="voice-btn" onclick="announce('en')">🇬🇧 English</button>
    <button class="voice-btn" onclick="announce('hi')">🇮🇳 Hindi</button>
    <button class="voice-btn" onclick="announce('mr')">🟠 Marathi</button>
  </div>

  <div class="stop-table-container">
    <table class="stop-table">
      <thead>
        <tr>
          <th>BUS NO.</th><th>DESTINATION</th><th>ETA</th><th>STATUS</th><th>CROWD</th>
        </tr>
      </thead>
      <tbody id="stopBody"></tbody>
    </table>
  </div>

</div>

<!-- ══════════ ADMIN VIEW ══════════ -->
<div id="admin" class="view" style="display:none; flex-direction:row;">

  <div class="admin-sidebar">

    <div class="admin-title">⚡ DEPOT COMMAND CENTER</div>

    <!-- Fleet -->
    <div class="card glow-pulse">
      <div class="card-title">Fleet Status</div>
      <div class="fleet-grid" id="fleetGrid"></div>
    </div>

    <!-- AI Demand -->
    <div class="card">
      <div class="card-title">AI Passenger Demand · 24H Forecast</div>
      <canvas id="adminDemandChart" height="130"></canvas>
    </div>

    <!-- Route Load -->
    <div class="card">
      <div class="card-title">Route Load Distribution</div>
      <canvas id="routeChart" height="110"></canvas>
    </div>

    <!-- Stop Crowd -->
    <div class="card">
      <div class="card-title">Stop Crowd Levels</div>
      <div id="crowdStops"></div>
    </div>

    <!-- Smart Dispatch -->
    <div class="card">
      <div class="card-title">🤖 Smart Dispatch</div>
      <p style="font-size:11px;color:var(--muted);margin-bottom:10px">
        Analyses crowd level per route and auto-calculates buses needed.
      </p>
      <div class="dispatch-log" id="dispatch-log">
        <span style="color:#4ade80">✓ All routes operating normally</span>
      </div>
      <button class="dispatch-btn" onclick="smartDispatch()">⚡ ANALYSE &amp; DISPATCH BUSES</button>
    </div>

    <!-- Alerts -->
    <div class="card">
      <div class="card-title">🚨 System Alerts</div>
      <div id="alertsPanel"></div>
    </div>

  </div>

  <div class="map-area">
    <div id="adminmap"></div>
    <div class="map-overlay">
      <div class="map-overlay-title">🛰 FLEET OVERVIEW</div>
      <div class="legend-item"><div class="legend-dot" style="background:#22c55e"></div>On time</div>
      <div class="legend-item"><div class="legend-dot" style="background:#eab308"></div>Delayed</div>
      <div class="legend-item"><div class="legend-dot" style="background:#ef4444"></div>Overcrowded</div>
    </div>
  </div>

</div>

<!-- Toast -->
<div class="toast" id="toast">✓ BUS DISPATCHED</div>

<!-- ═══════════════ JAVASCRIPT ═══════════════ -->
<script>
// ── DATA ──
const CENTER = [21.1458, 79.0882];

const ROUTES = [
  { num:102, dest:"Hingna",       path:[[21.1458,79.0882],[21.1320,79.0600],[21.1200,79.0350]] },
  { num:45,  dest:"Airport",      path:[[21.1458,79.0882],[21.1600,79.0950],[21.1780,79.1200]] },
  { num:27,  dest:"Dharampeth",   path:[[21.1458,79.0882],[21.1390,79.0785],[21.1310,79.0680]] },
  { num:12,  dest:"Kamptee",      path:[[21.1458,79.0882],[21.1550,79.1100],[21.1680,79.1350]] },
  { num:55,  dest:"Wadi",         path:[[21.1458,79.0882],[21.1250,79.0780],[21.1050,79.0680]] },
  { num:88,  dest:"Railway Stn",  path:[[21.1458,79.0882],[21.1430,79.0800],[21.1350,79.0710]] },
];

const STOPS = ["Sitabuldi","Airport","Railway Stn","Wadi","Dharampeth","Hingna","Kamptee"];

const HOURS = ["6AM","7AM","8AM","9AM","10AM","11AM","12PM","1PM","2PM","3PM","4PM","5PM","6PM","7PM","8PM","9PM"];
const ACT_DEMAND  = [800,2200,5800,6400,3000,2200,2800,2400,2200,3000,4200,6800,7200,4500,2500,1200];
const PRED_DEMAND = [900,2400,6100,6700,3200,2100,2900,2600,2000,3100,4400,7000,7500,4700,2700,1100];

// ── BUS STATE ──
let buses = Array.from({ length: 18 }, (_, i) => {
  const r = ROUTES[i % ROUTES.length];
  return {
    id: i, route: r.num, dest: r.dest, path: r.path,
    pathIdx: 0, progress: Math.random(),
    lat: r.path[0][0] + (Math.random()-0.5)*0.04,
    lng: r.path[0][1] + (Math.random()-0.5)*0.04,
    eta: Math.floor(Math.random()*25)+3,
    crowd: Math.floor(Math.random()*100),
    speed: 0.0008 + Math.random()*0.0014,
    status: ["On Time","On Time","On Time","Delayed"][i%4],
    delay: 5000 
  };
});

// ── MAPS ──
const map      = L.map('map',      { zoomControl:false }).setView(CENTER, 13);
const adminmap = L.map('adminmap', { zoomControl:false }).setView(CENTER, 12);

[map, adminmap].forEach(m =>
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution:'' }).addTo(m)
);
L.control.zoom({ position:'bottomright' }).addTo(map);

// Route polylines
ROUTES.forEach((r, i) => {
  const cols = ['#00f5d4','#7c3aed','#f59e0b','#22c55e','#ef4444','#60a5fa'];
  [map, adminmap].forEach(m =>
    L.polyline(r.path, { color:cols[i], weight:2.5, opacity:0.38, dashArray:'6,6' }).addTo(m)
  );
});

// ── BUS ICON ──
function busIcon(crowd, id) {
  const color = crowd < 40 ? '#22c55e' : crowd < 70 ? '#eab308' : '#ef4444';
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="34" height="34" viewBox="0 0 34 34">
    <circle cx="17" cy="17" r="13" fill="rgba(4,7,15,0.8)" stroke="${color}" stroke-width="2"/>
    <text x="17" y="22" text-anchor="middle" font-size="14">🚌</text>
  </svg>`;
  return L.divIcon({ html:svg, className:'', iconSize:[34,34], iconAnchor:[17,17] });
}

let markers = {}, adminMarkers = {};

function lerp(a, b, t) { return a + (b - a) * t; }

// ── GPS ANIMATION ──
function updateBusPositions() {
  buses.forEach(b => {
    const seg  = b.pathIdx % (b.path.length - 1);
    const from = b.path[seg];
    const to   = b.path[seg + 1];

    b.progress += b.speed;
    if (b.progress >= 1) { b.progress = 0; b.pathIdx = (b.pathIdx + 1) % (b.path.length - 1); }

    b.lat = lerp(from[0], to[0], b.progress);
    b.lng = lerp(from[1], to[1], b.progress);

    const icon = busIcon(b.crowd, b.id);
    const popup = `<b style="color:#00f5d4">Bus ${b.route}</b><br>→ ${b.dest}<br>ETA: ${Math.ceil(b.eta)} min<br>Crowd: ${b.crowd}%`;
    if (markers[b.id]) {
      markers[b.id].setLatLng([b.lat, b.lng]).setIcon(icon);
    } else {
      markers[b.id] = L.marker([b.lat, b.lng], { icon }).bindPopup(popup).addTo(map);
    }
    if (adminMarkers[b.id]) {
      adminMarkers[b.id].setLatLng([b.lat, b.lng]).setIcon(icon);
    } else {
      adminMarkers[b.id] = L.marker([b.lat, b.lng], { icon })
        .bindPopup(`<b style="color:#00f5d4">Bus ${b.route}</b><br>Status: ${b.status}`).addTo(adminmap);
    }
  });
}

// ── PASSENGER LIST ──
function filterBuses() { renderList(document.getElementById('searchInput').value.toLowerCase()); }

function renderList(filter='') {
  const sorted   = [...buses].sort((a,b) => a.eta - b.eta);
  const filtered = filter
    ? sorted.filter(b => String(b.route).includes(filter) || b.dest.toLowerCase().includes(filter))
    : sorted;

  document.getElementById('busList').innerHTML = filtered.map(b => {
    const pct  = Math.max(5, Math.min(100, b.crowd));
    const cls  = pct < 40 ? 'crowd-low' : pct < 70 ? 'crowd-med' : 'crowd-high';
    const sCol = b.status === 'On Time' ? '#4ade80' : '#f87171';
    return `
    <div class="bus-card" onclick="focusBus(${b.id})">
      <div class="bus-card-header">
        <div class="bus-number">${b.route}</div>
        <div class="eta-badge">${Math.ceil(b.eta)} min</div>
      </div>
      <div class="bus-dest">→ ${b.dest} &nbsp;·&nbsp; <span style="color:${sCol};font-size:10px">${b.status}</span></div>
      <div class="crowd-label"><span>Crowd</span><span>${pct}%</span></div>
      <div class="crowd-bar-container"><div class="crowd-bar ${cls}" style="width:${pct}%"></div></div>
    </div>`;
  }).join('');
}

function focusBus(id) {
  const b = buses.find(x => x.id === id);
  if (b) { map.setView([b.lat, b.lng], 15, { animate:true }); markers[id]?.openPopup(); }
}

// ── BUS STOP TABLE ──
function renderStop() {
  const arr = [...buses].sort((a,b) => a.eta - b.eta).slice(0, 8);
  document.getElementById('stopBody').innerHTML = arr.map(b => {
    const pct    = Math.max(5, Math.min(100, b.crowd));
    const etaMin = Math.ceil(b.eta);
    const eCls   = etaMin < 3 ? 'eta-urgent' : etaMin < 8 ? 'eta-soon' : 'eta-ok';
    const cCls   = pct < 40 ? 'chip-low' : pct < 70 ? 'chip-med' : 'chip-high';
    const cTxt   = pct < 40 ? '● LOW' : pct < 70 ? '● MOD' : '● HIGH';
    const rCls   = etaMin < 4 ? 'arriving-soon' : '';
    const sCol   = b.status === 'On Time' ? '#4ade80' : '#f87171';
    return `
    <tr class="${rCls}">
      <td style="font-family:'Orbitron',monospace;color:var(--neon);font-weight:700">${b.route}</td>
      <td>${b.dest}</td>
      <td class="eta-cell ${eCls}">${etaMin < 2 ? 'NOW' : etaMin + ' min'}</td>
      <td><span style="font-size:11px;color:${sCol}">${b.status}</span></td>
      <td><span class="crowd-chip ${cCls}">${cTxt}</span></td>
    </tr>`;
  }).join('');
}

// ── CLOCK ──
function updateClock() {
  const now = new Date();
  document.getElementById('clock').innerText = now.toLocaleTimeString('en-IN', { hour12:false });
  document.getElementById('stopDate').innerText = now.toLocaleDateString('en-IN',
    { weekday:'long', day:'numeric', month:'long', year:'numeric' });
}

// ── ROUTE OPTIMIZATION ──
function renderRoutes() {
  const ranked = ROUTES.map(r => {
    const rb = buses.filter(b => b.route === r.num);
    const avgCrowd = rb.length ? rb.reduce((s,b)=>s+b.crowd,0)/rb.length : 50;
    const minETA   = rb.length ? Math.min(...rb.map(b=>b.eta)) : 15;
    const score    = Math.round(100 - avgCrowd * 0.5 - minETA * 0.5);
    return { ...r, score, avgCrowd: Math.round(avgCrowd), minETA: Math.round(minETA) };
  }).sort((a,b) => b.score - a.score).slice(0, 4);

  const rCls = ['r1','r2','r3',''];
  const rSym = ['①','②','③','④'];
  const bCol = ['#ffd700','#c0c0c0','#cd7f32','#64748b'];
  document.getElementById('routeList').innerHTML = ranked.map((r,i) => `
    <div class="route-item">
      <div class="route-rank ${rCls[i]}">${rSym[i]}</div>
      <div class="route-info">
        <div class="route-name">Bus ${r.num} → ${r.dest}</div>
        <div class="route-score">Score: ${r.score} · ETA ${r.minETA}min · ${r.avgCrowd}% crowd</div>
      </div>
      <div class="route-bar">
        <div class="route-bar-fill" style="width:${Math.max(5,Math.min(100,r.score))}%;background:${bCol[i]}"></div>
      </div>
    </div>`).join('');
}

// ── ADMIN ──
function renderAdmin() {
  const active     = buses.filter(b => b.status === 'On Time').length;
  const delayed    = buses.length - active;
  const overcrowded = buses.filter(b => b.crowd >= 70).length;
  const totalPass  = buses.reduce((s,b) => s + b.crowd * 2, 0);

  document.getElementById('h-buses').innerText = buses.length;
  document.getElementById('h-pass').innerText  = totalPass.toLocaleString();

  document.getElementById('fleetGrid').innerHTML = `
    <div class="fleet-stat"><div class="fleet-val" style="color:#22c55e">${active}</div><div class="fleet-label">ON TIME</div></div>
    <div class="fleet-stat"><div class="fleet-val" style="color:#eab308">${delayed}</div><div class="fleet-label">DELAYED</div></div>
    <div class="fleet-stat"><div class="fleet-val" style="color:#ef4444">${overcrowded}</div><div class="fleet-label">CROWDED</div></div>`;

  document.getElementById('crowdStops').innerHTML = STOPS.map(s => {
    const cnt = Math.floor(Math.random() * 180) + 20;
    const pct = Math.min(100, (cnt / 180) * 100);
    const col = pct < 40 ? '#22c55e' : pct < 70 ? '#eab308' : '#ef4444';
    return `
    <div class="crowd-stop-item">
      <span>🚏</span>
      <span class="stop-sname">${s}</span>
      <div class="stop-mini-bar"><div class="stop-mini-fill" style="width:${pct}%;background:${col}"></div></div>
      <span class="stop-count" style="color:${col}">${cnt}</span>
    </div>`;
  }).join('');

  document.getElementById('alertsPanel').innerHTML = [
    { msg:'Route 45 — overcrowding at Airport stop', time:'2m ago' },
    { msg:'Bus 12 delayed +8 min — traffic on Wardha Rd', time:'7m ago' },
  ].map(a => `
    <div class="alert-item">
      <div class="alert-dot"></div>
      <div>
        <div>${a.msg}</div>
        <div style="color:var(--muted);font-size:10px;margin-top:2px">${a.time}</div>
      </div>
    </div>`).join('');
}

// ── SMART DISPATCH ──
function smartDispatch() {
  const log = [];
  const routeMap = {};
  buses.forEach(b => {
    if (!routeMap[b.route] || b.crowd > routeMap[b.route].crowd) routeMap[b.route] = b;
  });
  Object.values(routeMap).forEach(b => {
    if (b.crowd >= 85) {
      log.push(`⚡ <b>2 buses dispatched</b> → Route ${b.route} (${b.dest}) — Crowd: <span style="color:#f87171">${b.crowd}%</span> CRITICAL`);
      b.eta = Math.max(1, b.eta - 4);
    } else if (b.crowd >= 65) {
      log.push(`🚌 <b>1 bus dispatched</b> → Route ${b.route} (${b.dest}) — Crowd: <span style="color:#fbbf24">${b.crowd}%</span> HIGH`);
      b.eta = Math.max(1, b.eta - 2);
    }
  });
  const el = document.getElementById('dispatch-log');
  el.innerHTML = log.length
    ? log.join('<br>')
    : `<span style="color:#4ade80">✓ All routes operating normally</span>`;
  showToast(log.length ? `⚡ ${log.length} ROUTE(S) DISPATCHED` : '✓ NO DISPATCH NEEDED');
}

// ── VOICE ANNOUNCE ──
function announce(lang) {
  speechSynthesis.cancel();
  const top = [...buses].sort((a,b) => a.eta - b.eta)[0];
  const utt = new SpeechSynthesisUtterance();
  if (lang === 'en') {
    utt.text = `Bus number ${top.route} to ${top.dest} arriving in ${Math.ceil(top.eta)} minutes`;
    utt.lang = 'en-IN';
  }
  if (lang === 'hi') {
    utt.text = `बस नंबर ${top.route} ${top.dest} के लिए ${Math.ceil(top.eta)} मिनट में आने वाली है`;
    utt.lang = 'hi-IN';
  }
  if (lang === 'mr') {
    utt.text = `बस क्रमांक ${top.route} ${top.dest} साठी ${Math.ceil(top.eta)} मिनिटांत येणार आहे`;
    utt.lang = 'mr-IN';
  }
  utt.rate = 0.92;
  speechSynthesis.speak(utt);
}

// ── TOAST ──
function showToast(msg) {
  const t = document.getElementById('toast');
  t.innerText = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 3000);
}

// ── VIEW SWITCH ──
function switchView(v) {
  document.querySelectorAll('.view').forEach(e => { e.style.display = 'none'; e.classList.remove('v-active'); });
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  const el = document.getElementById(v);
  el.style.display = 'flex';
  el.classList.add('v-active');
  document.getElementById('btn-' + v).classList.add('active');
  if (v === 'admin')     { adminmap.invalidateSize(); initAdminCharts(); }
  if (v === 'passenger') { map.invalidateSize(); }
}

// ── AI DEMAND CHART (Passenger panel) ──
new Chart(document.getElementById('demandChart').getContext('2d'), {
  type: 'bar',
  data: {
    labels: HOURS,
    datasets: [
      { label:'Actual',      data:ACT_DEMAND,  backgroundColor:'rgba(0,245,212,0.22)', borderColor:'#00f5d4', borderWidth:1.5, borderRadius:2 },
      { label:'AI Forecast', data:PRED_DEMAND, type:'line', borderColor:'#a78bfa', borderWidth:2, pointRadius:1.5, pointBackgroundColor:'#a78bfa', fill:false, tension:0.4 }
    ]
  },
  options: {
    responsive: true,
    plugins: { legend:{ labels:{ color:'#94a3b8', font:{size:9}, boxWidth:10 } } },
    scales: {
      x:{ ticks:{ color:'#4b5563', font:{size:8} }, grid:{ color:'rgba(255,255,255,0.03)' } },
      y:{ ticks:{ color:'#4b5563', font:{size:8} }, grid:{ color:'rgba(255,255,255,0.03)' } }
    }
  }
});

// ── ADMIN CHARTS ──
let adminDemandChart, routeChart;
function initAdminCharts() {
  if (adminDemandChart) return;
  adminDemandChart = new Chart(document.getElementById('adminDemandChart').getContext('2d'), {
    type: 'line',
    data: {
      labels: HOURS,
      datasets: [
        { label:'Predicted', data:PRED_DEMAND, borderColor:'#a78bfa', backgroundColor:'rgba(124,58,237,0.1)', fill:true, tension:0.4, borderWidth:2, pointRadius:0 },
        { label:'Actual',    data:ACT_DEMAND,  borderColor:'#00f5d4', backgroundColor:'rgba(0,245,212,0.05)', fill:true, tension:0.4, borderWidth:1.5, pointRadius:0 }
      ]
    },
    options: {
      responsive:true,
      plugins:{ legend:{ labels:{ color:'#94a3b8', font:{size:9}, boxWidth:10 } } },
      scales: {
        x:{ ticks:{ color:'#4b5563', font:{size:8} }, grid:{ color:'rgba(255,255,255,0.03)' } },
        y:{ ticks:{ color:'#4b5563', font:{size:8} }, grid:{ color:'rgba(255,255,255,0.03)' } }
      }
    }
  });
  routeChart = new Chart(document.getElementById('routeChart').getContext('2d'), {
    type: 'doughnut',
    data: {
      labels: ROUTES.map(r => `Bus ${r.num}`),
      datasets: [{
        data: ROUTES.map(() => Math.floor(Math.random()*600)+200),
        backgroundColor:['#00f5d4','#7c3aed','#f59e0b','#22c55e','#ef4444','#60a5fa'],
        borderWidth:0, hoverOffset:6
      }]
    },
    options: {
      responsive:true,
      plugins:{ legend:{ position:'right', labels:{ color:'#94a3b8', font:{size:9}, boxWidth:10, padding:8 } } }
    }
  });
}

// ── MAIN LOOP ──
// ETA counts down 1 second every 2 seconds
function loop() {
  buses.forEach(b => {
    b.eta = Math.max(0, b.eta - 1);
    if (b.eta < 1) b.eta = Math.floor(Math.random() * 20) + 8;
    b.crowd = Math.max(0, Math.min(100, b.crowd + Math.floor(Math.random() * 10 - 5)));
  });
  updateBusPositions();
  renderList(document.getElementById('searchInput').value.toLowerCase());
  renderStop();
  renderRoutes();
  renderAdmin();
  updateClock();
}

loop();
setInterval(loop, 2000);
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(page)

if __name__ == "__main__":
    app.run(debug=True)