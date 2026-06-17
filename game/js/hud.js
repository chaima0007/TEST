// HUD — overlay DOM (vitesse, mission, étoiles wanted, messages temporaires).
// Construit son propre <style>, ne dépend d'aucun CSS externe.
// Le conteneur racine reste pointer-events:none pour ne jamais bloquer le jeu.

const STYLE_ID = 'hud-style';

const STYLE = `
#hud-overlay {
  position: fixed;
  inset: 0;
  pointer-events: none;
  font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
  user-select: none;
  z-index: 10;
}

#hud-mission {
  position: fixed;
  top: 16px;
  left: 16px;
  max-width: 50vw;
  padding: 10px 18px;
  background: rgba(10, 14, 22, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  color: #f3f6fa;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.2px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(2px);
}

#hud-mission .hud-label {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: #9fd3ff;
  margin-bottom: 2px;
}

#hud-score {
  position: fixed;
  top: 70px;
  left: 16px;
  padding: 6px 14px;
  background: rgba(10, 14, 22, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  color: #ffce3d;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.3px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(2px);
}

#hud-wanted {
  position: fixed;
  top: 16px;
  right: 16px;
  padding: 8px 14px;
  background: rgba(10, 14, 22, 0.55);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  display: flex;
  gap: 4px;
  font-size: 22px;
  line-height: 1;
}

#hud-wanted .star {
  color: rgba(255, 255, 255, 0.25);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
  transition: color 0.15s ease, transform 0.15s ease;
}

#hud-wanted .star.filled {
  color: #ffce3d;
  text-shadow: 0 0 6px rgba(255, 206, 61, 0.9), 0 1px 2px rgba(0, 0, 0, 0.6);
}

#hud-wanted.pulse {
  animation: hud-wanted-pulse 0.35s ease;
}

@keyframes hud-wanted-pulse {
  0% { transform: scale(1); }
  40% { transform: scale(1.12); }
  100% { transform: scale(1); }
}

#hud-speed {
  position: fixed;
  bottom: 22px;
  right: 22px;
  text-align: right;
  color: #f3f6fa;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
}

#hud-speed .hud-speed-value {
  font-size: 48px;
  font-weight: 800;
  line-height: 1;
}

#hud-speed .hud-speed-unit {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 1px;
  color: #c9d6e4;
}

.score-delta {
  position: fixed;
  right: 22px;
  bottom: 110px;
  font-size: 22px;
  font-weight: 800;
  color: #51cf66;
  text-shadow: 0 0 8px rgba(81,207,102,0.8);
  pointer-events: none;
  animation: score-fly 1.4s ease-out forwards;
}

@keyframes score-fly {
  0%   { opacity: 1; transform: translateY(0);    }
  70%  { opacity: 1; transform: translateY(-28px); }
  100% { opacity: 0; transform: translateY(-48px); }
}

#hud-toast {
  position: fixed;
  top: 22%;
  left: 50%;
  transform: translate(-50%, -10px);
  padding: 14px 28px;
  background: rgba(10, 14, 22, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  color: #ffffff;
  font-size: 22px;
  font-weight: 700;
  text-align: center;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
  opacity: 0;
  transition: opacity 0.25s ease, transform 0.25s ease;
  white-space: nowrap;
}

#hud-toast.visible {
  opacity: 1;
  transform: translate(-50%, 0);
}

#hud-pause {
  position: fixed;
  inset: 0;
  display: none;
  align-items: center;
  justify-content: center;
  background: rgba(6, 8, 12, 0.72);
  pointer-events: none;
  z-index: 20;
}

#hud-pause.visible {
  display: flex;
}

#hud-pause .hud-pause-panel {
  min-width: 280px;
  max-width: 90vw;
  padding: 24px 32px;
  background: rgba(14, 18, 26, 0.92);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 12px;
  color: #f3f6fa;
  text-align: left;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
}

#hud-pause h2 {
  margin: 0 0 14px;
  font-size: 20px;
  font-weight: 800;
  letter-spacing: 0.4px;
  color: #9fd3ff;
}

#hud-pause ul {
  list-style: none;
  margin: 0 0 16px;
  padding: 0;
  font-size: 14px;
  line-height: 1.8;
}

#hud-pause li span {
  display: inline-block;
  min-width: 110px;
  color: #ffce3d;
  font-weight: 700;
}

#hud-pause .hud-pause-score {
  font-size: 14px;
  font-weight: 700;
  color: #f3f6fa;
  border-top: 1px solid rgba(255, 255, 255, 0.15);
  padding-top: 10px;
}

#hud-pause .hud-pause-hint {
  margin-top: 12px;
  font-size: 12px;
  color: #c9d6e4;
}

#hud-radar {
  position: fixed;
  bottom: 22px;
  left: 22px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 0 0 2px rgba(255,255,255,0.18), 0 4px 16px rgba(0,0,0,0.5);
}

#hud-combo {
  position: fixed;
  bottom: 200px;
  left: 22px;
  padding: 4px 12px;
  background: rgba(10,14,22,0.55);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 6px;
  color: #ffce3d;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.5px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

#hud-combo.visible {
  opacity: 1;
}

#hud-clock {
  position: fixed;
  top: 16px;
  left: 50%;
  transform: translateX(-50%);
  padding: 6px 18px;
  background: rgba(10, 14, 22, 0.62);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  color: #f3f6fa;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 2px;
  text-shadow: 0 1px 2px rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  gap: 8px;
}

#hud-clock .hud-weather-icon {
  font-size: 16px;
}

#hud-agents {
  position: fixed;
  top: 70px;
  right: 16px;
  width: 220px;
  display: flex;
  flex-direction: column;
  gap: 5px;
  pointer-events: none;
}

.agent-card {
  padding: 6px 10px;
  background: rgba(8, 10, 18, 0.72);
  border: 1px solid rgba(255,255,255,0.1);
  border-left: 3px solid #444;
  border-radius: 6px;
  font-size: 11px;
  line-height: 1.5;
  color: #c9d6e4;
  transition: border-color 0.3s ease, opacity 0.3s ease;
}

.agent-card.active {
  opacity: 1;
}

.agent-card.inactive {
  opacity: 0.45;
}

.agent-card .agent-name {
  font-weight: 800;
  font-size: 11px;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  display: block;
  margin-bottom: 2px;
}

.agent-card .agent-status {
  color: #f3f6fa;
  font-size: 10px;
}

.agent-card.spectre  { border-left-color: #aa33ff; }
.agent-card.fantome  { border-left-color: #ffd700; }
.agent-card.police   { border-left-color: #4488ff; }
.agent-card.meteo    { border-left-color: #44aaff; }
.agent-card.trafic   { border-left-color: #55cc88; }

.agent-bar {
  height: 3px;
  background: rgba(255,255,255,0.1);
  border-radius: 2px;
  margin-top: 4px;
  overflow: hidden;
}
.agent-bar-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s ease;
}
`;

function injectStyle() {
  if (document.getElementById(STYLE_ID)) return;
  const styleEl = document.createElement('style');
  styleEl.id = STYLE_ID;
  styleEl.textContent = STYLE;
  document.head.appendChild(styleEl);
}

export class HUD {
  constructor(rootEl) {
    injectStyle();

    this.root = rootEl || document.body;

    this.overlay = document.createElement('div');
    this.overlay.id = 'hud-overlay';

    this.missionEl = document.createElement('div');
    this.missionEl.id = 'hud-mission';
    this.missionEl.innerHTML = '<span class="hud-label">Objectif</span><span class="hud-mission-text">—</span>';
    this.missionTextEl = this.missionEl.querySelector('.hud-mission-text');

    this.scoreEl = document.createElement('div');
    this.scoreEl.id = 'hud-score';
    this.scoreEl.textContent = '$0';

    this.wantedEl = document.createElement('div');
    this.wantedEl.id = 'hud-wanted';
    this.starEls = [];
    for (let i = 0; i < 5; i++) {
      const star = document.createElement('span');
      star.className = 'star';
      star.textContent = '★';
      this.wantedEl.appendChild(star);
      this.starEls.push(star);
    }

    this.speedEl = document.createElement('div');
    this.speedEl.id = 'hud-speed';
    this.speedEl.innerHTML = '<span class="hud-speed-value">0</span><span class="hud-speed-unit"> km/h</span>';
    this.speedValueEl = this.speedEl.querySelector('.hud-speed-value');

    this.toastEl = document.createElement('div');
    this.toastEl.id = 'hud-toast';

    this.pauseEl = document.createElement('div');
    this.pauseEl.id = 'hud-pause';
    this.pauseEl.innerHTML = `
      <div class="hud-pause-panel">
        <h2>Pause</h2>
        <ul>
          <li><span>WASD / Flèches</span>Conduire</li>
          <li><span>Espace</span>Frein à main</li>
          <li><span>Tactile</span>Boutons à l'écran sur mobile</li>
        </ul>
        <div class="hud-pause-score">Score : <span class="hud-pause-score-value">0</span></div>
        <div class="hud-pause-hint">Échap ou P pour reprendre</div>
      </div>
    `;
    this.pauseScoreValueEl = this.pauseEl.querySelector('.hud-pause-score-value');

    const RADAR_SIZE = 160;
    this.radarCanvas = document.createElement('canvas');
    this.radarCanvas.id = 'hud-radar';
    this.radarCanvas.width = RADAR_SIZE;
    this.radarCanvas.height = RADAR_SIZE;
    this._radarCtx = this.radarCanvas.getContext('2d');
    this._radarSize = RADAR_SIZE;

    this.comboEl = document.createElement('div');
    this.comboEl.id = 'hud-combo';

    // Horloge + météo (centre haut)
    this.clockEl = document.createElement('div');
    this.clockEl.id = 'hud-clock';
    this.clockEl.innerHTML = '<span class="hud-weather-icon">☀️</span><span class="hud-clock-time">06:00</span>';
    this._clockTimeEl = this.clockEl.querySelector('.hud-clock-time');
    this._weatherIconEl = this.clockEl.querySelector('.hud-weather-icon');

    // Panneau agents (droite, sous les étoiles)
    this.agentsEl = document.createElement('div');
    this.agentsEl.id = 'hud-agents';
    this._agentCards = {};
    const agentDefs = [
      { id: 'spectre', name: 'Le Spectre', cls: 'spectre' },
      { id: 'fantome', name: 'La Fantome', cls: 'fantome' },
      { id: 'police',  name: 'Police',     cls: 'police'  },
      { id: 'meteo',   name: 'Meteo',      cls: 'meteo'   },
      { id: 'trafic',  name: 'Trafic',     cls: 'trafic'  },
    ];
    for (const def of agentDefs) {
      const card = document.createElement('div');
      card.className = `agent-card inactive ${def.cls}`;
      card.innerHTML = `<span class="agent-name">${def.name}</span><span class="agent-status">—</span><div class="agent-bar"><div class="agent-bar-fill" style="width:0%;background:#888"></div></div>`;
      this.agentsEl.appendChild(card);
      this._agentCards[def.id] = {
        el: card,
        statusEl: card.querySelector('.agent-status'),
        barEl: card.querySelector('.agent-bar-fill'),
      };
    }

    this.overlay.appendChild(this.missionEl);
    this.overlay.appendChild(this.scoreEl);
    this.overlay.appendChild(this.wantedEl);
    this.overlay.appendChild(this.speedEl);
    this.overlay.appendChild(this.toastEl);
    this.overlay.appendChild(this.pauseEl);
    this.overlay.appendChild(this.radarCanvas);
    this.overlay.appendChild(this.comboEl);
    this.overlay.appendChild(this.clockEl);
    this.overlay.appendChild(this.agentsEl);
    this.root.appendChild(this.overlay);

    this._wantedLevel = 0;
    this._toastHideTimer = null;
    this._toastRemoveTimer = null;
    this._score = 0;
    this._paused = false;

    window.addEventListener('keydown', (e) => {
      if (e.code === 'Escape' || e.code === 'KeyP') {
        this._togglePause();
      }
    });
  }

  _togglePause() {
    this._paused = !this._paused;
    this.pauseEl.classList.toggle('visible', this._paused);
  }

  isPaused() {
    return this._paused;
  }

  setSpeed(kmh) {
    const value = Math.max(0, Math.round(kmh || 0));
    this.speedValueEl.textContent = String(value);
    // Couleur dynamique : vert → orange → rouge (façon GTA V / NFS)
    const color = value < 80 ? '#51cf66' : value < 120 ? '#ffa94d' : '#ff4444';
    this.speedValueEl.style.color = color;
    if (value > 120) {
      this.speedValueEl.style.textShadow = `0 0 12px ${color}`;
    } else {
      this.speedValueEl.style.textShadow = '0 1px 3px rgba(0,0,0,0.7)';
    }
  }

  setMission(text) {
    this.missionTextEl.textContent = text || '—';
  }

  setScore(value) {
    const next = Math.max(0, Math.round(value || 0));
    const delta = next - this._score;
    this._score = next;
    this.scoreEl.textContent = `$${this._score}`;
    this.pauseScoreValueEl.textContent = String(this._score);
    // Animation score delta : un "+N" qui monte et disparaît
    if (delta > 0) this._showScoreDelta(`+${delta}`);
  }

  _showScoreDelta(text) {
    const el = document.createElement('div');
    el.className = 'score-delta';
    el.textContent = text;
    document.body.appendChild(el);
    el.addEventListener('animationend', () => el.remove());
  }

  setWanted(level) {
    const clamped = Math.max(0, Math.min(5, Math.round(level)));
    if (clamped === this._wantedLevel) return;
    this._wantedLevel = clamped;
    this.starEls.forEach((star, i) => {
      star.classList.toggle('filled', i < clamped);
    });
    this.wantedEl.classList.remove('pulse');
    // restart animation
    void this.wantedEl.offsetWidth;
    this.wantedEl.classList.add('pulse');
  }

  showMessage(text, durationMs = 2500) {
    clearTimeout(this._toastHideTimer);
    clearTimeout(this._toastRemoveTimer);

    this.toastEl.textContent = text;
    this.toastEl.classList.remove('visible');
    // force reflow so the transition restarts even for back-to-back calls
    void this.toastEl.offsetWidth;
    this.toastEl.classList.add('visible');

    this._toastHideTimer = setTimeout(() => {
      this.toastEl.classList.remove('visible');
    }, Math.max(0, durationMs));

    this._toastRemoveTimer = setTimeout(() => {
      this.toastEl.textContent = '';
    }, Math.max(0, durationMs) + 300);
  }

  setTime(timeString) {
    if (this._clockTimeEl) this._clockTimeEl.textContent = timeString;
  }

  setWeather(weatherId) {
    const icons = { CLEAR: '☀️', CLOUDY: '☁️', RAIN: '🌧️', STORM: '⛈️' };
    if (this._weatherIconEl) this._weatherIconEl.textContent = icons[weatherId] || '☀️';
  }

  // Mise à jour du panneau agents — appelé chaque frame
  // agents: { spectre, fantome, police, meteo, trafic }
  // Chaque entrée : { status: string, bar: 0-1, color: '#hex', active: bool }
  updateAgents(agents) {
    for (const [id, data] of Object.entries(agents)) {
      const card = this._agentCards[id];
      if (!card) continue;
      card.el.className = `agent-card ${id} ${data.active ? 'active' : 'inactive'}`;
      card.statusEl.textContent = data.status || '—';
      card.barEl.style.width = `${Math.round((data.bar || 0) * 100)}%`;
      card.barEl.style.background = data.color || '#888';
    }
  }

  // mult: number 1-5 (1 = hidden, >1 = visible badge)
  setCombo(mult) {
    if (mult <= 1) {
      this.comboEl.classList.remove('visible');
    } else {
      this.comboEl.textContent = `COMBO x${mult}`;
      this.comboEl.classList.add('visible');
    }
  }

  // Heading-up radar: forward = up, player always centered.
  // opts: { playerPos{x,z}, playerHeading, target{targetX,targetZ}|null,
  //         policeCars[{x,z}], rivalPos{x,z}|null }
  updateRadar({ playerPos, playerHeading, target = null, policeCars = [], rivalPos = null, fantomePos = null, checkpointPos = null }) {
    const ctx = this._radarCtx;
    const size = this._radarSize;
    const center = size / 2;
    const worldRadius = 90; // world metres shown at canvas edge
    const scale = center / worldRadius;

    ctx.clearRect(0, 0, size, size);

    // Background disc
    ctx.beginPath();
    ctx.arc(center, center, center, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(8,10,16,0.78)';
    ctx.fill();

    // Faint crosshairs for orientation
    ctx.strokeStyle = 'rgba(255,255,255,0.08)';
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(center, 2); ctx.lineTo(center, size - 2); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(2, center); ctx.lineTo(size - 2, center); ctx.stroke();

    // Project a world (x,z) to canvas (px,py) relative to player, heading-up.
    const toCanvas = (wx, wz) => {
      const dx = wx - playerPos.x;
      const dz = wz - playerPos.z;
      const cosH = Math.cos(playerHeading);
      const sinH = Math.sin(playerHeading);
      // right component → canvas x, forward component → canvas -y (up)
      return {
        x: center + (dx * cosH - dz * sinH) * scale,
        y: center - (dx * sinH + dz * cosH) * scale,
      };
    };

    // Mission target (blue dot)
    if (target) {
      const t = toCanvas(target.targetX, target.targetZ);
      ctx.beginPath();
      ctx.arc(t.x, t.y, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#4fc3f7';
      ctx.fill();
    }

    // Police cars (red dots)
    for (const car of policeCars) {
      const c = toCanvas(car.x, car.z);
      if (c.x < 0 || c.x > size || c.y < 0 || c.y > size) continue;
      ctx.beginPath();
      ctx.arc(c.x, c.y, 3, 0, Math.PI * 2);
      ctx.fillStyle = '#ff4444';
      ctx.fill();
    }

    // Le Spectre (violet dot)
    if (rivalPos) {
      const r = toCanvas(rivalPos.x, rivalPos.z);
      ctx.beginPath();
      ctx.arc(r.x, r.y, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#aa33ff';
      ctx.strokeStyle = '#cc88ff';
      ctx.lineWidth = 1.5;
      ctx.fill();
      ctx.stroke();
    }

    // La Fantôme (point doré)
    if (fantomePos) {
      const f = toCanvas(fantomePos.x, fantomePos.z);
      ctx.beginPath();
      ctx.arc(f.x, f.y, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#ffd700';
      ctx.strokeStyle = '#fff8a0';
      ctx.lineWidth = 1.5;
      ctx.fill();
      ctx.stroke();
    }

    // Checkpoint de la Fantôme (étoile blanche)
    if (checkpointPos) {
      const c = toCanvas(checkpointPos.x, checkpointPos.z);
      ctx.beginPath();
      ctx.arc(c.x, c.y, 6, 0, Math.PI * 2);
      ctx.strokeStyle = '#ffd700';
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(c.x, c.y - 6);
      ctx.lineTo(c.x + 2, c.y - 2);
      ctx.lineTo(c.x + 6, c.y - 2);
      ctx.lineTo(c.x + 3, c.y + 1);
      ctx.lineTo(c.x + 4, c.y + 5);
      ctx.lineTo(c.x, c.y + 3);
      ctx.lineTo(c.x - 4, c.y + 5);
      ctx.lineTo(c.x - 3, c.y + 1);
      ctx.lineTo(c.x - 6, c.y - 2);
      ctx.lineTo(c.x - 2, c.y - 2);
      ctx.closePath();
      ctx.fillStyle = '#ffd700';
      ctx.fill();
    }

    // Player (yellow triangle pointing up — always centered, heading already baked into projection)
    ctx.save();
    ctx.translate(center, center);
    ctx.beginPath();
    ctx.moveTo(0, -8);
    ctx.lineTo(5.5, 6);
    ctx.lineTo(-5.5, 6);
    ctx.closePath();
    ctx.fillStyle = '#ffce3d';
    ctx.fill();
    ctx.restore();

    // Outer ring
    ctx.beginPath();
    ctx.arc(center, center, center - 1, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(255,255,255,0.22)';
    ctx.lineWidth = 2;
    ctx.stroke();
  }
}
