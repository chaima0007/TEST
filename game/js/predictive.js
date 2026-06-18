// predictive.js — Agent de police prédictif (style Minority Report)
// Enregistre l'historique des positions du joueur et calcule une trajectoire
// projetée N frames en avant par régression linéaire pondérée (vitesse +
// accélération). Quand le wanted ≥ 3, le résultat sert à positionner un
// marqueur d'interception avant que le joueur n'arrive.
// Aucune dépendance Three.js.

const HISTORY_MAX  = 20;
const MIN_SAMPLES  = 5;

export class PredictivePoliceAgent {
  constructor() {
    this._history    = []; // { x, z }
    this._predicted  = null;
    this._confidence = 0;
  }

  // À appeler chaque frame (ou toutes les N frames) avec la position joueur.
  record(x, z) {
    this._history.push({ x, z });
    if (this._history.length > HISTORY_MAX) this._history.shift();
  }

  // Calcule la position prédite dans `lookahead` frames.
  // Utilise vélocité moyenne + correction d'accélération sur les 8 derniers pts.
  predict(lookahead = 90) {
    if (this._history.length < MIN_SAMPLES) {
      this._predicted  = null;
      this._confidence = 0;
      return null;
    }

    const pts = this._history.slice(-8);
    // Vélocité moyenne (delta positions)
    let vx = 0, vz = 0;
    for (let i = 1; i < pts.length; i++) {
      vx += pts[i].x - pts[i - 1].x;
      vz += pts[i].z - pts[i - 1].z;
    }
    vx /= (pts.length - 1);
    vz /= (pts.length - 1);

    // Accélération (delta vélocités) — correction de 2nd ordre
    let ax = 0, az = 0;
    if (pts.length >= 4) {
      const v1x = pts[pts.length-1].x - pts[pts.length-2].x;
      const v0x = pts[1].x - pts[0].x;
      const v1z = pts[pts.length-1].z - pts[pts.length-2].z;
      const v0z = pts[1].z - pts[0].z;
      ax = (v1x - v0x) / (pts.length - 1);
      az = (v1z - v0z) / (pts.length - 1);
    }

    const last = this._history[this._history.length - 1];
    this._predicted = {
      x: last.x + vx * lookahead + 0.5 * ax * lookahead * lookahead,
      z: last.z + vz * lookahead + 0.5 * az * lookahead * lookahead,
    };
    this._confidence = Math.min(1, this._history.length / HISTORY_MAX);
    return { ...this._predicted, confidence: this._confidence };
  }

  getPredicted()  { return this._predicted; }
  getConfidence() { return this._confidence; }

  // Réinitialise l'historique (ex : téléportation/respawn).
  reset() {
    this._history    = [];
    this._predicted  = null;
    this._confidence = 0;
  }
}
