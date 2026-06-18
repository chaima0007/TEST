// witness.js — Système de témoins : les piétons qui assistent à un crime
// appellent la police. Tant qu'un témoin est proche du joueur, le wanted
// level ne peut pas baisser (pression maintenue).
// Utilise Map<mesh, {ttl}> pour ne pas garder de référence forte aux piétons.
// Aucune dépendance Three.js.

const WITNESS_TTL     = 30; // secondes avant qu'un témoin "oublie"
const PROXIMITY_RANGE = 22; // mètres — témoin "actif" s'il est dans ce rayon

export class WitnessAgent {
  constructor() {
    this._witnesses = new Map(); // mesh → { ttl, x, z }
  }

  // Marque une liste de piétons comme témoins d'un crime.
  // severity 0-1 allonge la durée de mémorisation.
  report(peds, severity = 1) {
    for (const ped of peds) {
      if (!ped?.mesh) continue;
      const existing = this._witnesses.get(ped.mesh);
      const ttl = WITNESS_TTL * (0.5 + severity * 0.5);
      if (!existing || existing.ttl < ttl) {
        this._witnesses.set(ped.mesh, {
          ttl,
          x: ped.mesh.position.x,
          z: ped.mesh.position.z,
        });
      }
    }
  }

  // Vieillissement des témoins.
  update(dt, pedestrians) {
    for (const [mesh, w] of this._witnesses) {
      // Mise à jour de la position
      w.x = mesh.position.x;
      w.z = mesh.position.z;
      w.ttl -= dt;
      if (w.ttl <= 0) this._witnesses.delete(mesh);
    }
  }

  // Retourne true si au moins un témoin est à moins de PROXIMITY_RANGE du joueur.
  hasNearbyWitness(playerPos) {
    if (!playerPos) return false;
    for (const [, w] of this._witnesses) {
      const dx = w.x - playerPos.x;
      const dz = w.z - playerPos.z;
      if (dx * dx + dz * dz < PROXIMITY_RANGE * PROXIMITY_RANGE) return true;
    }
    return false;
  }

  getWitnessCount() { return this._witnesses.size; }

  // Vide tous les témoins (ex : joueur échappé très loin).
  clear() { this._witnesses.clear(); }
}
