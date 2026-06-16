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

    this.overlay.appendChild(this.missionEl);
    this.overlay.appendChild(this.wantedEl);
    this.overlay.appendChild(this.speedEl);
    this.overlay.appendChild(this.toastEl);
    this.root.appendChild(this.overlay);

    this._wantedLevel = 0;
    this._toastHideTimer = null;
    this._toastRemoveTimer = null;
  }

  setSpeed(kmh) {
    const value = Math.max(0, Math.round(kmh || 0));
    this.speedValueEl.textContent = String(value);
  }

  setMission(text) {
    this.missionTextEl.textContent = text || '—';
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
}
