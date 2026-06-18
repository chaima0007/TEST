// emotion.js — Moteur émotionnel de la ville (EmotionEngine)
// Capture le style de jeu (agressivité, sérénité, entropie) et dérive un
// "mood" global qui colore l'ambiance visuelle, le score et le comportement
// des systèmes. La ville ressent ce que le joueur fait — et réagit.
// Aucune dépendance Three.js.

const CLAMP = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

// Décroissance par seconde pour chaque dimension
const DECAY = { aggression: 4, serenity: 2, entropy: 5 };

// Seuils pour la transition de mood
const THRESHOLD_TENSE   = 25;
const THRESHOLD_CHAOTIC = 55;
const THRESHOLD_SERENE  = 30;

export class EmotionEngine {
  constructor() {
    this._aggression = 0; // 0-100
    this._serenity   = 0; // 0-100
    this._entropy    = 0; // 0-100
    this._mood       = 'neutral';
  }

  // Envoie un événement émotionnel.
  // type: 'crash'|'drift'|'wanted'|'nitro'|'peaceful'
  pushEvent(type, intensity = 1) {
    const i = Math.max(0, intensity);
    switch (type) {
      case 'crash':    this._aggression = CLAMP(this._aggression + i * 14, 0, 100); break;
      case 'wanted':   this._aggression = CLAMP(this._aggression + i *  8, 0, 100); break;
      case 'drift':    this._entropy    = CLAMP(this._entropy    + i *  7, 0, 100); break;
      case 'nitro':    this._entropy    = CLAMP(this._entropy    + i *  4, 0, 100); break;
      case 'peaceful': this._serenity   = CLAMP(this._serenity   + i *  4, 0, 100); break;
    }
  }

  update(dt) {
    this._aggression = CLAMP(this._aggression - DECAY.aggression * dt, 0, 100);
    this._serenity   = CLAMP(this._serenity   - DECAY.serenity   * dt, 0, 100);
    this._entropy    = CLAMP(this._entropy    - DECAY.entropy    * dt, 0, 100);
    this._updateMood();
  }

  _updateMood() {
    const a = this._aggression;
    const s = this._serenity;
    const e = this._entropy;

    if (a < THRESHOLD_TENSE && s < THRESHOLD_SERENE && e < THRESHOLD_TENSE) {
      this._mood = 'neutral';
    } else if (a >= THRESHOLD_CHAOTIC) {
      this._mood = 'chaotic';
    } else if (a >= THRESHOLD_TENSE && a > s) {
      this._mood = 'tense';
    } else if (s >= THRESHOLD_SERENE && s > a) {
      this._mood = 'serene';
    } else {
      this._mood = 'neutral';
    }
  }

  getMood()        { return this._mood; }
  getAggression()  { return this._aggression; }
  getSerenity()    { return this._serenity; }
  getEntropy()     { return this._entropy; }

  // Teinte RGB normalisée (0-1) pour le tint visuel de la scène.
  getColorTint() {
    return {
      r: 1.0 + this._aggression / 250,   // plus rouge sous stress
      g: 1.0 - this._entropy    / 350,   // moins vert sous chaos
      b: 1.0 + this._serenity   / 300,   // plus bleu sous sérénité
    };
  }

  // Multiplicateur de score basé sur l'humeur active.
  getScoreMult() {
    switch (this._mood) {
      case 'chaotic': return 1.5;  // risque/récompense élevé
      case 'serene':  return 1.3;  // bonus pacifiste
      case 'tense':   return 1.1;
      default:        return 1.0;
    }
  }

  // Label affichable dans le HUD.
  getMoodLabel() {
    const LABELS = {
      neutral: 'ÉQUILIBRÉ',
      tense:   'TENDU',
      chaotic: 'CHAOS',
      serene:  'SÉRÉNITÉ',
    };
    return LABELS[this._mood] ?? 'ÉQUILIBRÉ';
  }
}
