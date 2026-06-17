import * as THREE from 'three';

// NitroSystem — collectibles (capsules cyan) sur la route.
// 3 capsules spawn a intervalles reguliers. Le joueur les ramasse en passant
// a moins de COLLECT_RADIUS metres. Appuyer sur N consume une charge pour
// 3 secondes de boost (multiplicateur vitesse 1.5x).
// Max 3 charges.

const MAX_CHARGES    = 3;
const BOOST_DURATION = 3.0;   // secondes
const BOOST_MULT     = 1.55;  // multiplicateur vitesse max
const COLLECT_RADIUS = 5.5;   // metres
const CAPSULE_SPAWN_INTERVAL = 18; // secondes entre spawn de nouvelles capsules
const CAPSULE_COUNT  = 3;     // nombre de capsules en jeu simultanement
const SPAWN_RADIUS_MIN = 15;
const SPAWN_RADIUS_MAX = 55;

function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

function buildCapsuleMesh() {
  const group = new THREE.Group();
  const mat = new THREE.MeshStandardMaterial({
    color: 0x00eeff, emissive: 0x00ccff, emissiveIntensity: 1.2,
    transparent: true, opacity: 0.85,
  });
  const body = new THREE.Mesh(new THREE.BoxGeometry(0.6, 1.2, 0.6), mat);
  body.position.y = 1.0;
  group.add(body);
  // halo ring
  const ringMat = new THREE.MeshStandardMaterial({ color: 0x00ffff, emissive: 0x00ffff, emissiveIntensity: 2.0, transparent: true, opacity: 0.4 });
  const ring = new THREE.Mesh(new THREE.TorusGeometry(1.0, 0.08, 6, 16), ringMat);
  ring.rotation.x = Math.PI / 2;
  ring.position.y = 0.5;
  group.add(ring);
  return group;
}

class NitroCapsule {
  constructor(scene, x, z) {
    this.scene = scene;
    this.mesh = buildCapsuleMesh();
    this.mesh.position.set(x, 0, z);
    scene.add(this.mesh);
    this.x = x;
    this.z = z;
    this.collected = false;
  }

  update(dt) {
    this.mesh.rotation.y += dt * 1.5; // tourne sur lui-meme
    this.mesh.position.y = Math.sin(Date.now() * 0.003) * 0.2; // flotte
  }

  dispose() {
    this.scene.remove(this.mesh);
    this.mesh.traverse((o) => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); });
  }
}

export class NitroSystem {
  constructor(scene) {
    this.scene = scene;
    this._charges     = 0;
    this._boostTimer  = 0;
    this._capsules    = [];
    this._spawnTimer  = 0;
    this._lastBoosted = false;
  }

  getCharges()    { return this._charges; }
  isBoostActive() { return this._boostTimer > 0; }
  getBoostMultiplier() { return this._boostTimer > 0 ? BOOST_MULT : 1.0; }

  update(dt, playerPos, input) {
    // Boost timer
    if (this._boostTimer > 0) {
      this._boostTimer = Math.max(0, this._boostTimer - dt);
    }

    // Trigger boost on N press (falling edge — only when newly pressed)
    const nitroPressed = input && input.get('nitro');
    if (nitroPressed && !this._lastBoosted && this._charges > 0 && this._boostTimer <= 0) {
      this._charges--;
      this._boostTimer = BOOST_DURATION;
    }
    this._lastBoosted = nitroPressed;

    // Spawn capsules periodically until we have CAPSULE_COUNT
    this._spawnTimer -= dt;
    if (this._spawnTimer <= 0 && this._capsules.length < CAPSULE_COUNT) {
      this._spawnCapsule(playerPos);
      this._spawnTimer = CAPSULE_SPAWN_INTERVAL / CAPSULE_COUNT;
    }

    // Update + collect
    for (let i = this._capsules.length - 1; i >= 0; i--) {
      const cap = this._capsules[i];
      cap.update(dt);
      const dx = playerPos.x - cap.x;
      const dz = playerPos.z - cap.z;
      if (Math.hypot(dx, dz) < COLLECT_RADIUS) {
        this._charges = Math.min(MAX_CHARGES, this._charges + 1);
        cap.dispose();
        this._capsules.splice(i, 1);
      }
    }
  }

  _spawnCapsule(playerPos) {
    const angle = Math.random() * Math.PI * 2;
    const dist  = SPAWN_RADIUS_MIN + Math.random() * (SPAWN_RADIUS_MAX - SPAWN_RADIUS_MIN);
    const x = playerPos.x + Math.sin(angle) * dist;
    const z = playerPos.z + Math.cos(angle) * dist;
    this._capsules.push(new NitroCapsule(this.scene, x, z));
  }

  dispose() {
    for (const c of this._capsules) c.dispose();
    this._capsules = [];
  }
}
