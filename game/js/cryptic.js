// CrypticAgent — Ronde 24 — IMMERSION TOTALE
// Messages qui brisent le quatrième mur. NEXUS dont le log se corrompt.
// Typewriter effect + glitchs de caractères selon la peur.

const BACKROOM_MSGS = [
  "TU N'ES PAS CENSÉ ÊTRE ICI",
  "COURS",
  "IL ARRIVE",
  "LA SORTIE N'EXISTE PAS",
  "NIVEAU — ∞",
  "NE TE RETOURNE PAS",
  "TU AS QUITTÉ LA RÉALITÉ\nAU MAUVAIS ENDROIT",
  "// ERREUR : RÉALITÉ NON TROUVÉE",
  "TOUTES LES PORTES MÈNENT ICI",
  "TU ES LE SEUL ICI\nTU AS TOUJOURS ÉTÉ SEUL ICI",
  "LE TEMPS NE COMPTE PAS\nLÀ OÙ TU ES",
];

const MONSTER_MSGS = {
  OMBRE:  [
    "ELLE EST DANS TES ANGLES MORTS",
    "L'OMBRE EST RÉELLE",
    "ELLE A TOUJOURS ÉTÉ LÀ",
    "ELLE IMITE TA FORME",
  ],
  BÊTE:   [
    "LE SOL TREMBLE",
    "ELLE SENT LA PEUR",
    "9 TONNES — 5.5 M/S",
    "LES DENTS D'ABORD",
  ],
  CYCLOPE: [
    "IL A TOUJOURS REGARDÉ",
    "TU N'ES QU'UNE PROIE",
    "IL NE DORT JAMAIS",
    "DEPUIS COMBIEN DE TEMPS\nT'OBSERVE-T-IL ?",
  ],
};

const DREAM_MSGS = [
  "✦ BIENVENUE DANS L'ENTRE-DEUX ✦",
  "LE MONDE RÉEL ÉTAIT UN RÊVE",
  "TU ÉTAIS ICI AVANT DE NAÎTRE",
  "∞ LA LUMIÈRE SE SOUVIENT DE TOI ∞",
  "CE LIEU EXISTE DEPUIS TOUJOURS",
];

const NEXUS_CORRUPT = [
  "// NEXUS : sys█ème... [ERREUR]",
  "// NE█US : donn███ corrompues",
  "// N████ : ███ ████ ███ [NULL]",
  "// [NEXUS HORS LIGNE — RÉALITÉ INSTABLE]",
  "// NEXUS : entité détect██ à ██m",
  "// ERR_REALITY_BREACH : 0x▓▓▓▓",
  "// ████████████████████████████",
];

const GLYPHS = '█▓▒░▪▫◆◇○●■□▲△▼▽◉╳╱╲╔╗╚╝';

function corrupt(text, rate) {
  return text.split('').map(c => {
    if (c === ' ' || c === '\n') return c;
    return Math.random() < rate ? GLYPHS[(Math.random() * GLYPHS.length) | 0] : c;
  }).join('');
}

export class CrypticAgent {
  constructor() {
    this._pending      = [];
    this._currentMsg   = '';
    this._displayed    = '';
    this._typeIdx      = 0;
    this._typeTimer    = 0;
    this._holdTimer    = 0;
    this._fadePhase    = false;
    this._active       = false;
    this._cooldown     = 15;
    this._nexusCooldown = 0;
    this._corruptRate  = 0;
    this._currentColor = '#dd0000';
    this._buildOverlay();
  }

  _buildOverlay() {
    // Message principal centré — typewriter
    this._el = document.createElement('div');
    this._el.style.cssText = `
      position:fixed;top:36%;left:50%;transform:translateX(-50%);
      font-family:'Courier New',monospace;font-size:15px;font-weight:900;
      letter-spacing:5px;text-align:center;line-height:1.8;
      pointer-events:none;z-index:9200;opacity:0;
      white-space:pre;max-width:80vw;
    `;
    document.body.appendChild(this._el);

    // Ligne NEXUS corrompue (coin bas-droite)
    this._nexusEl = document.createElement('div');
    this._nexusEl.style.cssText = `
      position:fixed;bottom:192px;right:22px;
      font-family:'Courier New',monospace;font-size:9px;font-weight:700;
      color:rgba(0,200,255,0.40);letter-spacing:1px;text-align:right;
      pointer-events:none;z-index:9200;opacity:0;transition:opacity 0.35s;
    `;
    document.body.appendChild(this._nexusEl);
  }

  _applyStyle(color) {
    this._currentColor = color;
    this._el.style.color = color;
    const hex = color.replace('#', '');
    const r = parseInt(hex.slice(0,2), 16);
    const g = parseInt(hex.slice(2,4), 16);
    const b = parseInt(hex.slice(4,6), 16);
    this._el.style.textShadow =
      `0 0 22px rgba(${r},${g},${b},0.9), 0 0 55px rgba(${r},${g},${b},0.35)`;
  }

  push(msg, color = '#cc0000') {
    this._pending.push({ msg, color });
  }

  pushImmediate(msg, color = '#cc0000') {
    this._pending.unshift({ msg, color });
    this._cooldown = 0;
  }

  _next() {
    if (!this._pending.length) return;
    const { msg, color } = this._pending.shift();
    this._currentMsg = msg;
    this._displayed  = '';
    this._typeIdx    = 0;
    this._typeTimer  = 0;
    this._holdTimer  = 0;
    this._fadePhase  = false;
    this._active     = true;
    this._applyStyle(color);
    this._el.style.opacity = '1';
  }

  update(dt, backroomActive, fearLevel, monsterType, dreamActive) {
    this._cooldown      = Math.max(0, this._cooldown - dt);
    this._nexusCooldown = Math.max(0, this._nexusCooldown - dt);

    // ── Auto-push selon contexte ────────────────────────
    if (this._cooldown <= 0 && !this._active && !this._pending.length) {
      if (backroomActive) {
        const pool = BACKROOM_MSGS;
        this.push(pool[(Math.random() * pool.length) | 0], '#cc0000');
        this._cooldown = 7 + Math.random() * 9;
      } else if (monsterType && monsterType !== '—' && fearLevel > 0.30) {
        const pool = MONSTER_MSGS[monsterType] || [];
        if (pool.length) {
          this.push(pool[(Math.random() * pool.length) | 0], '#bb0000');
          this._cooldown = 10 + Math.random() * 8;
        }
      } else if (dreamActive) {
        const pool = DREAM_MSGS;
        this.push(pool[(Math.random() * pool.length) | 0], '#7722ff');
        this._cooldown = 12 + Math.random() * 12;
      }
    }

    // ── Ligne NEXUS corrompue ───────────────────────────
    if (this._nexusCooldown <= 0 && (backroomActive || fearLevel > 0.55)) {
      const msg = NEXUS_CORRUPT[(Math.random() * NEXUS_CORRUPT.length) | 0];
      this._nexusEl.textContent = msg;
      this._nexusEl.style.opacity = '1';
      this._nexusCooldown = 4 + Math.random() * 5;
      setTimeout(() => { this._nexusEl.style.opacity = '0'; }, 2200);
    }

    // ── Typewriter + fondu ──────────────────────────────
    if (!this._active) {
      if (this._pending.length) this._next();
      return;
    }

    const CHAR_SPEED = 0.042;
    const HOLD_TIME  = 2.6;
    const FADE_DUR   = 0.9;

    if (!this._fadePhase) {
      // Frappe des caractères
      this._typeTimer += dt;
      while (this._typeTimer >= CHAR_SPEED && this._typeIdx < this._currentMsg.length) {
        this._typeTimer -= CHAR_SPEED;
        this._typeIdx++;
      }
      this._displayed = this._currentMsg.slice(0, this._typeIdx);

      // Corruption et curseur
      this._corruptRate = (backroomActive || fearLevel > 0.65) ? 0.035 : 0;
      const cursor = this._typeIdx < this._currentMsg.length ? '█' : '';
      const display = this._corruptRate > 0
        ? corrupt(this._displayed, this._corruptRate) + cursor
        : this._displayed + cursor;
      this._el.textContent = display;

      if (this._typeIdx >= this._currentMsg.length) {
        this._holdTimer += dt;
        if (this._holdTimer >= HOLD_TIME) this._fadePhase = true;
      }
    } else {
      // Fondu avec corruption croissante
      const op = parseFloat(this._el.style.opacity) - dt / FADE_DUR;
      if (op <= 0) {
        this._el.style.opacity  = '0';
        this._el.textContent    = '';
        this._active            = false;
        this._cooldown          = Math.max(this._cooldown, 4);
      } else {
        this._el.style.opacity = op.toFixed(3);
        this._el.textContent   = corrupt(this._displayed, 0.12 + (1 - op) * 0.35);
      }
    }
  }

  isActive() { return this._active; }
}
