// flashmob.js — Agent Flash Mob
// Toutes les 45s, les piétons proches convergent vers un point et tournent en
// rond comme si une sono invisible jouait — avant de reprendre leur vie normale
// les yeux dans le vague. Aucune dépendance Three.js.

const COOLDOWN       = 45;   // secondes entre deux flash mobs
const DANCE_DURATION = 7;    // durée de la danse (s)
const TRIGGER_RADIUS = 22;   // rayon de recrutement (m)
const MIN_DANCERS    = 3;    // minimum de participants
const MAX_DANCERS    = 10;   // maximum de participants
const DANCE_RADIUS   = 4.5;  // rayon de la ronde

export class FlashMobAgent {
  constructor() {
    this._cooldown   = COOLDOWN * 0.4; // premier flash mob plus tôt
    this._active     = false;
    this._timer      = 0;
    this._center     = { x: 0, z: 0 };
    this._dancers    = [];
    this._offsets    = []; // phase angulaire initiale par danseur
    this._savedDirs  = []; // direction originale (restaurée après)
  }

  update(dt, pedestrians, playerPos) {
    if (this._active) {
      this._timer -= dt;
      const progress = 1 - this._timer / DANCE_DURATION;

      for (let i = 0; i < this._dancers.length; i++) {
        const ped = this._dancers[i];
        if (!ped.active || !ped.mesh) continue;

        // Phase : convergence (0-20%), danse (20-80%), dispersion (80-100%)
        if (progress < 0.2) {
          // Approche du centre
          const t = progress / 0.2;
          const angle = this._offsets[i];
          const tx = this._center.x + Math.cos(angle) * DANCE_RADIUS;
          const tz = this._center.z + Math.sin(angle) * DANCE_RADIUS;
          ped.mesh.position.x += (tx - ped.mesh.position.x) * Math.min(1, dt * 5 * t);
          ped.mesh.position.z += (tz - ped.mesh.position.z) * Math.min(1, dt * 5 * t);
        } else if (progress < 0.80) {
          // Rotation autour du centre + rebond vertical en rythme
          const spin = (progress - 0.2) / 0.6;
          const angle = this._offsets[i] + spin * Math.PI * 4; // 2 tours complets
          ped.mesh.position.x = this._center.x + Math.cos(angle) * DANCE_RADIUS;
          ped.mesh.position.z = this._center.z + Math.sin(angle) * DANCE_RADIUS;
          ped.mesh.position.y = Math.abs(Math.sin(angle * 3)) * 0.55; // saut chorégraphié
          ped.mesh.rotation.y = angle + Math.PI / 2;
        } else {
          // Atterrissage progressif
          ped.mesh.position.y *= 0.85;
        }
      }

      if (this._timer <= 0) {
        // Remise à terre et libération
        for (const ped of this._dancers) {
          if (ped.mesh) ped.mesh.position.y = 0;
        }
        this._active   = false;
        this._cooldown = COOLDOWN;
        this._dancers  = [];
        this._offsets  = [];
      }
    } else {
      this._cooldown -= dt;
      if (this._cooldown <= 0) {
        const candidates = pedestrians.filter(p =>
          p.active && p.mesh &&
          Math.hypot(p.mesh.position.x - playerPos.x, p.mesh.position.z - playerPos.z) < TRIGGER_RADIUS
        );
        if (candidates.length >= MIN_DANCERS) {
          this._active   = true;
          this._timer    = DANCE_DURATION;
          // Centre légèrement décalé du joueur pour qu'il assiste au spectacle
          this._center   = {
            x: playerPos.x + (Math.random() - 0.5) * 10,
            z: playerPos.z + (Math.random() - 0.5) * 10,
          };
          this._dancers  = candidates.slice(0, MAX_DANCERS);
          this._offsets  = this._dancers.map((_, i) =>
            (i / this._dancers.length) * Math.PI * 2
          );
        } else {
          this._cooldown = 12; // réessaie dans 12s si pas assez de monde
        }
      }
    }
  }

  isActive()       { return this._active; }
  getDancerCount() { return this._dancers.length; }
  getCenter()      { return { ...this._center }; }
  getTimeLeft()    { return Math.max(0, this._timer); }
  getCooldown()    { return Math.max(0, this._cooldown); }
}
