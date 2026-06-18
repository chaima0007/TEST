// citypulse.js — Pouls de la ville synchronisé sur le BPM de la musique
// La ville bat comme un coeur : intensité 0-1 par beat, attaque rapide /
// décroissance lente. Affecte l'éclairage ambiant, le score et la vitesse
// du trafic de manière subtile et synchronisée.
// Aucune dépendance Three.js.

const BPM_MAP = {
  city:  88,
  chase: 128,
  night: 100,
  boss:  140,
};

export class CityPulseAgent {
  constructor() {
    this._bpm       = 88;
    this._phase     = 0; // 0..1 dans le beat courant
    this._intensity = 0; // 0..1
  }

  // Synchronise le BPM sur l'état musical en cours.
  setMusicState(state) {
    this._bpm = BPM_MAP[state] ?? 88;
  }

  setBpm(bpm) {
    this._bpm = Math.max(40, Math.min(240, bpm));
  }

  update(dt) {
    const bps = this._bpm / 60;
    this._phase = (this._phase + dt * bps) % 1;

    // Enveloppe par beat : attaque 10 %, décroissance 90 %
    if (this._phase < 0.1) {
      this._intensity = this._phase / 0.1;           // montée rapide
    } else {
      this._intensity = Math.max(0, 1 - (this._phase - 0.1) / 0.9); // descente lente
    }
  }

  getIntensity()    { return this._intensity; }
  getPhase()        { return this._phase; }
  getBpm()          { return this._bpm; }

  // Facteur vitesse trafic : 0.8× (repos) → 1.3× (beat peak)
  getTrafficMult()  { return 0.8 + this._intensity * 0.5; }

  // Multiplicateur de score pendant le pic — combo rythmique
  getScoreMult()    { return 1.0 + this._intensity * 0.3; }

  // Boost lumière ambiante à injecter dans la scène Three.js
  getAmbientBoost() { return this._intensity * 0.12; }

  // Vrai dès que l'intensité dépasse 85 % (beat franc)
  isPeak()          { return this._intensity > 0.85; }
}
