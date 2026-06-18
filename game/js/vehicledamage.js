// vehicledamage.js — Système de dégâts cumulatifs (carrosserie, vitesse, visuels)
// Aucune dépendance Three.js : fonctionne en environnement headless (tests Node.js).

export class VehicleDamageSystem {
  constructor() {
    this._damage      = 0;   // 0 = intact → 1 = épave
    this._repairTimer = 0;   // secondes avant début de l'auto-réparation
  }

  // Ajoute l'impact d'une collision (intensity 0-1).
  addImpact(intensity) {
    this._damage      = Math.min(1, this._damage + intensity * 0.22);
    this._repairTimer = 8; // aucune réparation pendant 8 s après le dernier choc
  }

  // Doit être appelé chaque frame avec dt (secondes).
  update(dt) {
    if (this._repairTimer > 0) {
      this._repairTimer -= dt;
    } else if (this._damage > 0) {
      this._damage = Math.max(0, this._damage - dt * 0.003);
    }
  }

  // Multiplicateur de vitesse max : 1.0 intact, descend sous 40 % de dégâts.
  getSpeedFactor() {
    if (this._damage <= 0.4) return 1.0;
    return Math.max(0.35, 1.0 - (this._damage - 0.4) * 1.1);
  }

  getDamage() { return this._damage; }

  // Applique les effets visuels sur le matériau de carrosserie Three.js.
  // Sûr à appeler avec null (pas de mesh actif en test).
  updateVisuals(bodyMat) {
    if (!bodyMat) return;
    const d = this._damage;
    bodyMat.roughness = 0.5 + d * 0.45;
    if (d > 0.55) {
      if (bodyMat.emissive) bodyMat.emissive.setHex(0xff4400);
      bodyMat.emissiveIntensity = (d - 0.55) * 1.5;
    } else {
      bodyMat.emissiveIntensity = 0;
    }
    bodyMat.needsUpdate = true;
  }

  // Réparation immédiate (garage).
  repair(bodyMat) {
    this._damage      = 0;
    this._repairTimer = 0;
    if (bodyMat) {
      bodyMat.roughness          = 0.5;
      bodyMat.emissiveIntensity  = 0;
      bodyMat.needsUpdate        = true;
    }
  }
}
