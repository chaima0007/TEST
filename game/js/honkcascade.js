// honkcascade.js — Cascade de klaxons par contagion
// Quand le joueur frôle une voiture, celle-ci klaxonne, et la panique se propage
// de voiture en voiture dans un rayon de 12m avec un délai de 0.25s par vague.
// Renvoie un Map<mesh, ttl> que main.js utilise pour afficher des "!" flottants.
// Aucune dépendance Three.js.

const HONK_TTL       = 1.8;  // durée d'affichage du "!" (secondes)
const CASCADE_RADIUS = 12;   // rayon de propagation (m)
const MAX_WAVE       = 5;    // profondeur max de la cascade
const WAVE_DELAY     = 0.22; // délai entre chaque vague (s)
const NEAR_MISS_DIST = 4.5;  // distance (m) pour déclencher une cascade

export { NEAR_MISS_DIST };

export class HonkCascadeAgent {
  constructor() {
    this._honking = new Map(); // mesh → ttl restant
    this._queue   = [];        // { x, z, delay, wave }
    this._totalHonks = 0;
  }

  // À appeler quand le joueur frôle un véhicule
  triggerAt(cx, cz) {
    // Lance la première vague au point de contact
    this._queue.push({ x: cx, z: cz, delay: 0, wave: 0 });
  }

  update(dt, trafficCars) {
    // Vieillissement des klaxons actifs
    for (const [mesh, ttl] of this._honking) {
      const next = ttl - dt;
      if (next <= 0) this._honking.delete(mesh);
      else           this._honking.set(mesh, next);
    }

    // Traitement de la queue de propagation
    const remaining = [];
    for (const job of this._queue) {
      job.delay -= dt;
      if (job.delay > 0) { remaining.push(job); continue; }

      // Déclenche les voitures proches non encore klaxonnantes
      let newSources = [];
      for (const car of trafficCars) {
        if (!car.active || !car.mesh) continue;
        if (this._honking.has(car.mesh)) continue;
        const dx = car.mesh.position.x - job.x;
        const dz = car.mesh.position.z - job.z;
        if (dx * dx + dz * dz < CASCADE_RADIUS * CASCADE_RADIUS) {
          this._honking.set(car.mesh, HONK_TTL);
          this._totalHonks++;
          newSources.push({ x: car.mesh.position.x, z: car.mesh.position.z });
        }
      }

      // Planifie la vague suivante depuis chaque nouvelle source
      if (job.wave < MAX_WAVE) {
        for (const src of newSources) {
          remaining.push({ x: src.x, z: src.z, delay: WAVE_DELAY, wave: job.wave + 1 });
        }
      }
    }
    this._queue = remaining;
  }

  isHonking(mesh)     { return this._honking.has(mesh); }
  getHonkTtl(mesh)    { return this._honking.get(mesh) ?? 0; }
  getHonkingCount()   { return this._honking.size; }
  getTotalHonks()     { return this._totalHonks; }
  getAll()            { return this._honking; }
}
