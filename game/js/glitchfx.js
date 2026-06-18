// GlitchFXAgent — Ronde 24 — IMMERSION TOTALE
// Effets visuels de rupture appliqués via DOM/CSS, sans toucher au pipeline Three.js.
// Aberration chromatique (R/B décalés), bloom couleur, scanlines, flash de capture.

export class GlitchFXAgent {
  constructor() {
    this._t                 = 0;
    this._chromIntensity    = 0;
    this._bloomAlpha        = 0;
    this._scanOpacity       = 0;
    this._motionBlurPx      = 0; // synchronisé depuis main.js
    this._buildOverlays();
  }

  _buildOverlays() {
    // ── Aberration rouge (décalée à droite) ─────────────
    this._aberR = document.createElement('div');
    this._aberR.style.cssText = `
      position:fixed;inset:0;pointer-events:none;z-index:9000;
      mix-blend-mode:screen;opacity:0;
      background:rgba(255,0,0,0.07);
    `;
    document.body.appendChild(this._aberR);

    // ── Aberration bleue (décalée à gauche) ─────────────
    this._aberB = document.createElement('div');
    this._aberB.style.cssText = `
      position:fixed;inset:0;pointer-events:none;z-index:9000;
      mix-blend-mode:screen;opacity:0;
      background:rgba(0,100,255,0.07);
    `;
    document.body.appendChild(this._aberB);

    // ── Flash soudain (blanc ou couleur) ────────────────
    this._flashEl = document.createElement('div');
    this._flashEl.style.cssText = `
      position:fixed;inset:0;pointer-events:none;z-index:9010;
      background:rgba(0,0,0,0);
    `;
    document.body.appendChild(this._flashEl);

    // ── Bloom coloré (glow intérieur autour de l'écran) ─
    this._bloomEl = document.createElement('div');
    this._bloomEl.style.cssText = `
      position:fixed;inset:0;pointer-events:none;z-index:8998;
      box-shadow:inset 0 0 0px rgba(0,0,0,0);
      transition:box-shadow 0.5s ease;
    `;
    document.body.appendChild(this._bloomEl);

    // ── Scanlines (lignes CRT, backroom uniquement) ──────
    this._scanEl = document.createElement('div');
    this._scanEl.style.cssText = `
      position:fixed;inset:0;pointer-events:none;z-index:8997;
      background:repeating-linear-gradient(
        0deg,
        rgba(0,0,0,0) 0px, rgba(0,0,0,0) 1px,
        rgba(0,0,0,0.055) 2px, rgba(0,0,0,0.055) 3px
      );
      opacity:0;transition:opacity 0.4s;
    `;
    document.body.appendChild(this._scanEl);

    // ── Grain de film (noise overlay animé) ─────────────
    this._grainEl = document.createElement('canvas');
    this._grainEl.style.cssText = `
      position:fixed;inset:0;pointer-events:none;z-index:8996;
      opacity:0;mix-blend-mode:overlay;
    `;
    this._grainEl.width  = 160;
    this._grainEl.height = 120;
    this._grainCtx = this._grainEl.getContext('2d');
    document.body.appendChild(this._grainEl);
    this._grainTimer = 0;
  }

  // ── API publique ───────────────────────────────────────

  triggerFlash(color = 'rgba(255,255,255,0.75)', holdMs = 40, fadeMs = 150) {
    this._flashEl.style.transition = 'none';
    this._flashEl.style.background = color;
    setTimeout(() => {
      this._flashEl.style.transition = `background ${fadeMs}ms ease`;
      this._flashEl.style.background = 'rgba(0,0,0,0)';
    }, holdMs);
  }

  // Synchronisé depuis main.js pour que le filter CSS ne se batte pas avec le motion blur
  setMotionBlur(px) { this._motionBlurPx = px; }

  update(dt, { backroomActive, fearLevel, monsterActive, dreamActive, dreamColor }) {
    this._t += dt;

    // ── Aberration chromatique ─────────────────────────
    const targetChrom = backroomActive
      ? 0.65 + Math.sin(this._t * 3.2) * 0.3
      : monsterActive && fearLevel > 0.28 ? fearLevel * 0.55 : 0;

    this._chromIntensity += (targetChrom - this._chromIntensity) * Math.min(1, dt * 3.5);

    if (this._chromIntensity > 0.01) {
      const shift = (this._chromIntensity * 5).toFixed(1);
      const op    = (this._chromIntensity * 0.80).toFixed(3);
      this._aberR.style.opacity    = op;
      this._aberR.style.transform  = `translateX(${shift}px)`;
      this._aberB.style.opacity    = op;
      this._aberB.style.transform  = `translateX(-${shift}px)`;
    } else {
      this._aberR.style.opacity = '0';
      this._aberB.style.opacity = '0';
    }

    // ── Bloom coloré ───────────────────────────────────
    if (dreamActive && dreamColor !== null) {
      const r = (dreamColor >> 16) & 0xff;
      const g = (dreamColor >> 8)  & 0xff;
      const b =  dreamColor        & 0xff;
      const a = (0.40 + Math.sin(this._t * 1.3) * 0.18).toFixed(2);
      this._bloomEl.style.boxShadow = `inset 0 0 130px rgba(${r},${g},${b},${a})`;
    } else if (backroomActive) {
      const a = (0.14 + Math.sin(this._t * 0.85) * 0.05).toFixed(2);
      this._bloomEl.style.boxShadow = `inset 0 0 90px rgba(200,178,90,${a})`;
    } else {
      this._bloomEl.style.boxShadow = 'inset 0 0 0px rgba(0,0,0,0)';
    }

    // ── Scanlines (Backroom) ────────────────────────────
    const scanTarget = backroomActive ? 1 : fearLevel > 0.55 && monsterActive ? 0.55 : 0;
    this._scanEl.style.opacity = scanTarget.toFixed(2);

    // ── Grain de film ──────────────────────────────────
    const grainTarget = backroomActive ? 0.18 : fearLevel > 0.4 ? fearLevel * 0.12 : 0;
    const grainOpNow  = parseFloat(this._grainEl.style.opacity || '0');
    const grainOpNew  = grainOpNow + (grainTarget - grainOpNow) * Math.min(1, dt * 2);
    this._grainEl.style.opacity = grainOpNew.toFixed(3);

    if (grainOpNew > 0.01) {
      this._grainTimer += dt;
      if (this._grainTimer > 0.05) {  // rafraîchi à 20 fps
        this._grainTimer = 0;
        const ctx = this._grainCtx;
        const id  = ctx.createImageData(160, 120);
        const buf = id.data;
        for (let i = 0; i < buf.length; i += 4) {
          const v = (Math.random() * 255) | 0;
          buf[i] = buf[i+1] = buf[i+2] = v;
          buf[i+3] = 200;
        }
        ctx.putImageData(id, 0, 0);
      }
    }

    // ── Clignotements aléatoires ───────────────────────
    if (backroomActive && Math.random() < 0.004) {
      this.triggerFlash('rgba(200,180,80,0.12)', 30, 80);
    }
    if (monsterActive && fearLevel > 0.80 && Math.random() < 0.007) {
      this.triggerFlash('rgba(180,0,0,0.18)', 25, 100);
    }
  }
}
