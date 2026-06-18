// ResolveurAgent — Ronde 22 — PREMIUM
// Director IA inspiré de: Left 4 Dead AI Director, dynamic difficulty (Resident Evil 4),
// et narrative directors des jeux AAA modernes.
// Monitore l'état du jeu en temps réel — détecte les situations critiques et génère
// des résolutions dynamiques adaptées (nitro, bonus, événements, signalisation).

const ANALYZE_DURATION = 1.6; // secondes d'analyse avant d'afficher la résolution
const UI_DURATION      = 9;   // secondes d'affichage du panneau
const COOLDOWN_DEFAULT = 32;  // secondes entre deux analyses

const SITUATIONS = [
  {
    id:    'CERNÉ',
    label: 'Joueur encerclé',
    color: '#ff3300',
    detect(ctx) {
      return ctx.wanted >= 3
        && ctx.policeDist.filter(d => d < 32).length >= 3
        && ctx.speed < 14;
    },
    resolutions: [
      { label: 'Charge Nitro d\'urgence',  action: 'grant_nitro',  bonus: 0,   msg: 'Charge nitro accordée — fuyez !' },
      { label: 'Impulsion de vitesse',      action: 'speed_boost',  bonus: 100, msg: 'Boost de fuite activé +100 pts !' },
    ],
  },
  {
    id:    'ÉPAVE',
    label: 'Véhicule critique',
    color: '#ff6600',
    detect(ctx) { return ctx.damage > 0.78; },
    resolutions: [
      { label: 'Garage d\'urgence signalé', action: 'show_garage', bonus: 100, msg: 'Garage de secours — 150m !' },
      { label: 'Bonus survie avancé',        action: 'score_bonus', bonus: 600, msg: 'Bonus survie exceptionnel : +600 !' },
    ],
  },
  {
    id:    'INACTIF',
    label: 'Joueur stationnaire',
    color: '#ffaa00',
    detect(ctx) { return ctx.idleTime > 28 && ctx.wanted === 0; },
    resolutions: [
      { label: 'Flash mob surprise',   action: 'trigger_flashmob', bonus: 200, msg: 'Flash mob déclenché — bougez !' },
      { label: 'Mission express',      action: 'score_bonus',      bonus: 350, msg: 'Bonus activité : +350 !' },
    ],
  },
  {
    id:    'REVANCHE',
    label: 'Fuite réussie (wanted ≥ 3)',
    color: '#00ffcc',
    detect(ctx) { return ctx.justEscaped; },
    resolutions: [
      { label: 'Prime de fuite légendaire', action: 'score_bonus', bonus: 900, msg: 'Fuite réussie ! Prime : +900 !' },
    ],
  },
  {
    id:    'RECORD',
    label: 'Vitesse record',
    color: '#aa55ff',
    detect(ctx) { return ctx.speed > 140 && ctx.wanted === 0; },
    resolutions: [
      { label: 'Bonus vitesse pure',  action: 'score_bonus', bonus: 400, msg: 'Vitesse record ! Bonus : +400 !' },
    ],
  },
];

export class ResolveurAgent {
  constructor() {
    this._cooldown     = 8; // délai initial avant premier scan
    this._uiTimer      = 0;
    this._analyzeTimer = 0;
    this._active       = false;
    this._situation    = null;
    this._resolution   = null;
    this._resolveCount = 0;
    this._idleTimer    = 0;
    this._lastPos      = null;
    this._lastWanted   = 0;
    this._pendingBonus = 0;
    this._pendingNitro = false;
    this._pendingEvent = false;
    this._blinkPhase   = 0;

    this._buildPanel();
  }

  _buildPanel() {
    this._el = document.createElement('div');
    this._el.style.cssText = `
      position:fixed;bottom:130px;left:50%;transform:translateX(-50%);
      background:rgba(0,12,28,0.93);
      border:1px solid rgba(0,200,255,0.28);
      border-radius:11px;padding:12px 22px;
      font-family:'Segoe UI',Arial,sans-serif;font-size:12px;
      color:#00c8ff;pointer-events:none;z-index:270;
      opacity:0;transition:opacity .4s;text-align:center;min-width:290px;
      box-shadow:0 0 24px rgba(0,200,255,0.10);
    `;
    document.body.appendChild(this._el);
  }

  update(dt, vehicle, wanted, vehicleDamage, nitro) {
    this._blinkPhase += dt * 4;

    // Cooldown
    if (this._cooldown > 0) this._cooldown -= dt;

    // UI fade timer
    if (this._uiTimer > 0) {
      this._uiTimer      -= dt;
      this._analyzeTimer  = Math.min(ANALYZE_DURATION, this._analyzeTimer + dt);
      this._renderPanel();
      this._el.style.opacity = '1';
      if (this._uiTimer <= 0) {
        this._el.style.opacity = '0';
        this._active           = false;
      }
    }

    // Don't scan if cooldown active or UI showing
    if (this._cooldown > 0 || this._uiTimer > 0) return;

    // Build context
    const pos    = vehicle.getPosition();
    const speed  = Math.abs(vehicle.getSpeedKmh());
    const damage = vehicleDamage ? vehicleDamage.getDamage() : 0;

    // Idle tracking
    if (this._lastPos) {
      const moved = Math.hypot(pos.x - this._lastPos.x, pos.z - this._lastPos.z);
      if (moved > 2) this._idleTimer = 0;
      else           this._idleTimer += dt;
    }
    this._lastPos = { x: pos.x, z: pos.z };

    // Escape detection
    const justEscaped = this._lastWanted >= 3 && wanted.level === 0;
    this._lastWanted   = wanted.level;

    const policeDist = wanted.cars
      .filter(c => c.mesh)
      .map(c => Math.hypot(c.mesh.position.x - pos.x, c.mesh.position.z - pos.z));

    const ctx = { wanted: wanted.level, speed, damage, idleTime: this._idleTimer, justEscaped, policeDist };

    const sit = SITUATIONS.find(s => s.detect(ctx));
    if (sit) this._trigger(sit, nitro);
  }

  _trigger(situation, nitro) {
    const res = situation.resolutions[Math.floor(Math.random() * situation.resolutions.length)];

    this._active       = true;
    this._situation    = situation.id;
    this._resolution   = res;
    this._uiTimer      = UI_DURATION;
    this._analyzeTimer = 0;
    this._cooldown     = COOLDOWN_DEFAULT;
    this._resolveCount++;
    this._idleTimer    = 0;

    // Apply action immediately
    switch (res.action) {
      case 'grant_nitro':
        if (nitro) nitro._charges = Math.min(3, (nitro._charges || 0) + 1);
        this._pendingNitro = true;
        break;
      case 'score_bonus':
      case 'speed_boost':
      case 'show_garage':
      case 'trigger_flashmob':
        this._pendingBonus = res.bonus;
        if (res.action === 'trigger_flashmob') this._pendingEvent = true;
        break;
    }
  }

  _renderPanel() {
    const analyzing = this._analyzeTimer < ANALYZE_DURATION;
    const sit = SITUATIONS.find(s => s.id === this._situation);
    const color = sit?.color || '#00c8ff';

    if (analyzing) {
      const prog  = this._analyzeTimer / ANALYZE_DURATION;
      const bars  = Math.round(prog * 14);
      const bar   = '█'.repeat(bars) + '░'.repeat(14 - bars);
      const dots  = '.'.repeat(Math.floor(this._blinkPhase % 4));
      this._el.innerHTML = `
        <div style="font-size:10px;letter-spacing:1.5px;color:#0088aa;margin-bottom:6px;">◈ RÉSOLVEUR IA — ANALYSE${dots}</div>
        <div style="color:${color};font-weight:700;margin-bottom:5px;">${sit?.label || '...'}</div>
        <div style="font-family:'Courier New';font-size:9px;color:#005566;letter-spacing:2px;">${bar}</div>
        <div style="font-size:10px;color:#003344;margin-top:4px;">Calcul en cours${dots}</div>
      `;
    } else {
      const bonus = this._resolution?.bonus || 0;
      const timeLeft = Math.round(Math.max(0, this._uiTimer));
      this._el.innerHTML = `
        <div style="font-size:10px;letter-spacing:1.5px;color:#0088aa;margin-bottom:6px;">◈ RÉSOLVEUR IA — RÉSOLUTION #${this._resolveCount}</div>
        <div style="color:${color};font-weight:800;font-size:13px;margin-bottom:3px;">${this._resolution?.label || ''}</div>
        <div style="font-size:11px;color:#88ddff;margin-top:4px;">${this._resolution?.msg || ''}</div>
        ${bonus > 0 ? `<div style="color:#ffaa00;font-size:11px;font-weight:700;margin-top:4px;">+ ${bonus} pts</div>` : ''}
        <div style="font-size:9px;color:#004455;margin-top:6px;border-top:1px solid rgba(0,200,255,0.12);padding-top:5px;">
          Prochain scan dans ${Math.round(this._cooldown)}s · ${this._resolveCount} résolution(s) totale(s)
        </div>
      `;
    }
  }

  // Pop notification for main.js _showNotif
  popNotif() {
    if (!this._resolution || this._analyzeTimer < ANALYZE_DURATION) return null;
    const n = this._resolution._notified ? null : this._resolution.msg;
    if (this._resolution) this._resolution._notified = true;
    return n;
  }

  popBonus()       { const b = this._pendingBonus; this._pendingBonus = 0; return b; }
  popNitroGrant()  { const n = this._pendingNitro; this._pendingNitro = false; return n; }
  popEvent()       { const e = this._pendingEvent;  this._pendingEvent  = false; return e; }

  isActive()           { return this._active; }
  getSituation()       { return this._situation || '—'; }
  getResolutionLabel() { return this._resolution?.label || '—'; }
  getResolveCount()    { return this._resolveCount; }
  getCooldown()        { return this._cooldown; }
  isAnalyzing()        { return this._uiTimer > 0 && this._analyzeTimer < ANALYZE_DURATION; }
}
