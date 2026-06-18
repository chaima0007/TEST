import * as THREE from 'three';

// CommandantAgent — Ronde 22 — PREMIUM
// Généraliste tactique inspiré de: Rainbow Six, Ghost Recon, GTA V FIB, XCOM
// Orchestre la réponse policière avec plans militaires évolutifs, radio intercept,
// visualisation tactique et escalade dramatique vers FORCE MAXIMALE.

const PLANS = [
  {
    id:       'POURSUITE',
    label:    'OPÉRATION POURSUITE',
    desc:     'Approche frontale — contact direct, toutes unités en poursuite',
    color:    '#ffaa00',
    minWanted: 3,
    duration: 14,
  },
  {
    id:       'FLANQUEMENT',
    label:    'OPÉRATION FLANQUEMENT',
    desc:     'Pince tactique — unités sur les flancs gauche et droit',
    color:    '#ff7700',
    minWanted: 3,
    duration: 12,
  },
  {
    id:       'ENCERCLEMENT',
    label:    'OPÉRATION ENCERCLEMENT',
    desc:     'Bouclage de secteur — sortie coupée, barrage déployé',
    color:    '#ff3300',
    minWanted: 4,
    duration: 12,
  },
  {
    id:       'FORCE_MAX',
    label:    '⚠ FORCE MAXIMALE',
    desc:     'Toutes unités, hélicoptère, barrages — reddition immédiate exigée',
    color:    '#ff0000',
    minWanted: 5,
    duration: Infinity,
  },
];

const RADIO = [
  '📡 Alpha 1 — coupez la route nationale !',
  '📡 Bravo 2 — flanquez par la gauche !',
  '📡 Hélicoptère Romeo, confirmez contact visuel',
  '📡 Toutes unités — la cible NE DOIT PAS PASSER',
  '📡 Delta 3 — déployez le barrage route Est',
  '📡 Echo 4, interceptez sur l\'axe principal',
  '📡 COMMANDANT : encerclement initié, secteur Ouest',
  '📡 Romeo Sierra — la cible accélère, doublez !',
  '📡 Bravo 1, tenez position — approche par le nord',
  '📡 Contact visuel perdu — resserrez le dispositif !',
  '📡 Delta 7 — ne laissez pas rejoindre le port',
  '📡 COMMANDANT à tous — FORCE MAXIMALE autorisée !',
  '📡 Unité Charlie — converge sur les coordonnées !',
  '📡 Tous véhicules : formation triangle, lancez !',
];

export class CommandantAgent {
  constructor() {
    this._planIdx    = 0;
    this._planTimer  = 0;
    this._radioTimer = 0;
    this._radioQueue = [];
    this._radioInterval = 9;
    this._active     = false;
    this._wasActive  = false;
    this._threatPct  = 0;
    this._frame      = 0;
    this._panel      = null;
    this._lastMsg    = '📡 En attente d\'ordres...';
    this._blinkPhase = 0;

    this._buildPanel();
  }

  _buildPanel() {
    const el = document.createElement('div');
    el.style.cssText = `
      position:fixed;top:88px;right:20px;
      background:rgba(4,0,0,0.90);
      border:1px solid rgba(255,40,40,0.35);
      border-radius:9px;padding:13px 16px;
      font-family:'Courier New',monospace;font-size:11px;
      color:#ff4444;pointer-events:none;z-index:240;
      opacity:0;transition:opacity .35s;width:240px;
      box-shadow:0 0 22px rgba(255,10,10,0.12);
    `;
    document.body.appendChild(el);
    this._panel = el;
  }

  update(dt, wanted, hud) {
    this._frame++;
    this._blinkPhase += dt * 3;
    const wasActive = this._wasActive;
    this._active    = wanted.level >= 3;
    this._wasActive = this._active;

    if (!this._active) {
      this._panel.style.opacity = '0';
      this._planIdx   = 0;
      this._planTimer = 0;
      this._threatPct = Math.max(0, this._threatPct - dt * 0.6);
      return;
    }

    // First activation: dramatic radio announce
    if (!wasActive && this._active) {
      this._radioQueue.push('⚔ COMMANDANT ACTIVÉ — Opération de neutralisation en cours !');
      this._planIdx  = 0;
      this._planTimer = 0;
    }

    // Threat level tracks wanted level
    const targetThreat = (wanted.level - 2) / 3;
    this._threatPct += (targetThreat - this._threatPct) * Math.min(1, dt * 1.2);

    // Plan timer + escalation
    const plan = PLANS[this._planIdx];
    this._planTimer += dt;

    if (plan.duration !== Infinity && this._planTimer >= plan.duration) {
      this._planTimer = 0;
      const nextIdx = this._planIdx + 1;
      if (nextIdx < PLANS.length && wanted.level >= PLANS[nextIdx].minWanted) {
        this._planIdx = nextIdx;
        const newPlan = PLANS[this._planIdx];
        this._radioQueue.push(`⚔ COMMANDANT : ${newPlan.label} initiée !`);

        // FORCE MAXIMALE: escalate wanted to 5
        if (newPlan.id === 'FORCE_MAX' && wanted.level < 5) {
          wanted._setLevel(5, hud);
        }
      }
    }

    // Downgrade plan if wanted drops
    while (this._planIdx > 0 && wanted.level < PLANS[this._planIdx].minWanted) {
      this._planIdx--;
      this._planTimer = 0;
    }

    // Radio messages
    this._radioTimer += dt;
    if (this._radioTimer >= this._radioInterval) {
      this._radioTimer = 0;
      const msg = RADIO[Math.floor(Math.random() * RADIO.length)];
      this._radioQueue.push(msg);
      this._lastMsg = msg;
    }
    if (this._radioQueue.length > 0) {
      this._lastMsg = this._radioQueue[this._radioQueue.length - 1];
    }

    this._renderPanel(wanted, dt);
  }

  _renderPanel(wanted, dt) {
    const plan   = PLANS[this._planIdx];
    const pct    = Math.round(this._threatPct * 100);
    const filled = Math.round(this._threatPct * 10);
    const bar    = '█'.repeat(filled) + '░'.repeat(10 - filled);
    const isMax  = plan.id === 'FORCE_MAX';
    const blink  = isMax ? (Math.sin(this._blinkPhase) > 0 ? '▌' : ' ') : '';

    const timeLeft = plan.duration === Infinity
      ? '∞'
      : `${Math.round(Math.max(0, plan.duration - this._planTimer))}s`;

    const borderAlpha = isMax
      ? (0.4 + Math.sin(this._blinkPhase * 2) * 0.3).toFixed(2)
      : '0.35';

    this._panel.style.opacity      = '1';
    this._panel.style.borderColor  = `rgba(255,40,40,${borderAlpha})`;
    this._panel.style.boxShadow    = isMax
      ? `0 0 ${28 + Math.sin(this._blinkPhase) * 8}px rgba(255,0,0,0.22)`
      : '0 0 22px rgba(255,10,10,0.12)';

    this._panel.innerHTML = `
      <div style="color:${plan.color};font-weight:900;font-size:12.5px;letter-spacing:0.8px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;">
        <span>⚔ COMMANDANT${blink}</span>
        <span style="font-size:10px;background:rgba(255,40,40,0.15);padding:1px 6px;border-radius:3px;border:1px solid rgba(255,40,40,0.3);">WL${wanted.level}</span>
      </div>
      <div style="color:${plan.color};font-size:11.5px;font-weight:700;margin-bottom:3px;">${plan.label}</div>
      <div style="color:#cc4444;font-size:10px;line-height:1.4;margin-bottom:9px;">${plan.desc}</div>
      <div style="border-top:1px solid rgba(255,40,40,0.18);padding-top:7px;margin-bottom:7px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:4px;font-size:10px;">
          <span style="color:#ff9999;">Menace</span>
          <span style="color:${plan.color};font-weight:700;">${pct}%</span>
        </div>
        <div style="font-family:'Courier New';font-size:9px;letter-spacing:1px;color:${plan.color};margin-bottom:6px;">${bar}</div>
        <div style="display:flex;justify-content:space-between;font-size:10px;color:#cc4444;">
          <span>Unités: <strong style="color:#ff8888;">${wanted.cars.length}${wanted.getHelicopterActive() ? ' + HELI' : ''}</strong></span>
          <span>Rotation: ${timeLeft}</span>
        </div>
      </div>
      <div style="border-top:1px solid rgba(255,40,40,0.18);padding-top:7px;font-size:10px;color:#ff9999;line-height:1.4;">${this._lastMsg}</div>
    `;
  }

  popRadioMessage()   { return this._radioQueue.shift() || null; }
  isActive()          { return this._active; }
  getPlan()           { return PLANS[this._planIdx]?.id || 'POURSUITE'; }
  getPlanLabel()      { return PLANS[this._planIdx]?.label || ''; }
  getThreatLevel()    { return this._threatPct; }
  getTimeToNext() {
    const p = PLANS[this._planIdx];
    return p.duration === Infinity ? Infinity : Math.max(0, p.duration - this._planTimer);
  }
}
