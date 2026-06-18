// reputation.js — Mémoire de la ville par quartier
// Chaque district accumule des points de réputation (-100 à +100).
// Crimes → réputation baisse, conduite pacifique → remonte lentement.
// getMultiplier() affecte le score, shouldFlee() déclenche la fuite des PNJ.
// Aucune dépendance Three.js.

const DISTRICT_IDS = ['centre', 'nord', 'sud', 'ouest', 'est'];
const CLAMP = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

export class ReputationAgent {
  constructor() {
    this._rep = {};
    for (const id of DISTRICT_IDS) this._rep[id] = 0;
  }

  // Enregistre un crime dans un quartier (severity: 1 = minor, 3 = brutal).
  addCrime(districtId, severity = 1) {
    const id = DISTRICT_IDS.includes(districtId) ? districtId : 'centre';
    this._rep[id] = CLAMP(this._rep[id] - severity * 7, -100, 100);
  }

  // Conduite pacifique : récupération lente (+1 par appel nominal).
  addPeaceful(districtId, amount = 1) {
    const id = DISTRICT_IDS.includes(districtId) ? districtId : 'centre';
    this._rep[id] = CLAMP(this._rep[id] + amount, -100, 100);
  }

  getRep(districtId) {
    return this._rep[DISTRICT_IDS.includes(districtId) ? districtId : 'centre'] ?? 0;
  }

  // Multiplicateur de score : 0.5× (criminel) → 1.5× (bienfaiteur).
  getMultiplier(districtId) {
    return 1.0 + this.getRep(districtId) / 200;
  }

  // True si les PNJ du quartier doivent fuir le joueur.
  shouldFlee(districtId) {
    return this.getRep(districtId) < -30;
  }

  getStatus(districtId) {
    const r = this.getRep(districtId);
    if (r >=  50) return 'HÉROS';
    if (r >=  15) return 'Apprécié';
    if (r >  -15) return 'Neutre';
    if (r >  -50) return 'MÉFIANCE';
    return 'BANNI';
  }

  getAll() { return { ...this._rep }; }
}
