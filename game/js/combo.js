// ComboSystem — multiplicateur de score façon arcade qui récompense la
// prise de risque : frôler un véhicule de circulation (near-miss) sans
// le percuter fait monter le multiplicateur (1x→5x). Une série de
// near-miss consécutifs maintient le combo ; l'absence de frisson pendant
// quelques secondes le fait redescendre. Chaque near-miss confirmé rapporte
// des points bonus proportionnels au multiplicateur courant.

const NEAR_MISS_INNER = 2.8; // m — en dessous : collision réelle, pas un near-miss
const NEAR_MISS_OUTER = 7.0; // m — au-dessus : pas assez proche pour compter
const DECAY_GRACE_S = 3.5; // secondes sans near-miss avant que le mult diminue
const DECAY_STEP_S = 1.8; // secondes entre chaque -1 de multiplicateur
const BONUS_BASE = 20; // points de base par near-miss

export class ComboSystem {
  constructor() {
    this._mult = 1;
    this._score = 0;
    this._decayGrace = 0; // temps restant avant de commencer à perdre des niveaux
    this._decayStep = 0; // décompte entre chaque palier de décroissance
    this._inNearMissZone = false; // évite de compter le même frôlement plusieurs fois
  }

  getScore() {
    return this._score;
  }

  getMultiplier() {
    return this._mult;
  }

  // playerPos: {x, z}
  // trafficPositions: [{x, z}] (actifs uniquement)
  update(dt, playerPos, trafficPositions) {
    let anyNearMiss = false;
    for (const tp of trafficPositions) {
      const d = Math.hypot(tp.x - playerPos.x, tp.z - playerPos.z);
      if (d > NEAR_MISS_INNER && d < NEAR_MISS_OUTER) {
        anyNearMiss = true;
        break;
      }
    }

    if (anyNearMiss) {
      if (!this._inNearMissZone) {
        // Front d'entrée : on compte ce near-miss
        const bonus = BONUS_BASE * this._mult;
        this._score += bonus;
        this._mult = Math.min(5, this._mult + 1);
        this._inNearMissZone = true;
      }
      // Réinitialise le compte à rebours de décroissance à chaque near-miss actif.
      this._decayGrace = DECAY_GRACE_S;
      this._decayStep = DECAY_STEP_S;
      return;
    }

    this._inNearMissZone = false;

    if (this._mult === 1) return; // déjà au minimum, rien à faire

    if (this._decayGrace > 0) {
      this._decayGrace -= dt;
      return;
    }

    this._decayStep -= dt;
    if (this._decayStep <= 0) {
      this._mult = Math.max(1, this._mult - 1);
      this._decayStep = DECAY_STEP_S;
    }
  }
}
