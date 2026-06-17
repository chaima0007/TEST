// architect.js — L'Architecte : boss final, maître de la ville.
// Apparaît quand le joueur atteint $15 000 ou survit 5 étoiles pendant 60s.
// Coordonne la police, pose des embuscades, dialogue en temps réel.

import * as THREE from 'three';

const SPAWN_SCORE   = 15000;
const TOP_SPEED_MS  = 120 / 3.6;
const ACCEL_MS2     = 9;
const TURN_RATE     = 1.6;          // rad/s max
const SPAWN_DIST    = 60;
const DESPAWN_DIST  = 200;
const COMMAND_INTERVAL = 28;        // s between coordinated attacks
const WANTED_5_TIME = 60;           // s at 5 stars → triggers spawn too

const DIALOGUES = {
  spawn:   ['Je contrôle cette ville.', 'Tu pensais m\'échapper ?', 'Bienvenue dans mon réseau.'],
  command: ['Tous les agents : en position.', 'Je ferme les issues.', 'Déployez les barrages.'],
  close:   ['Tu es rapide. Mais pas assez.', 'Intéressant.', 'Je te vois.'],
  escape:  ['Va. Profite. Pour l\'instant.'],
  taunt:   ['Chaque seconde que tu roules, tu me coûtes. Et tu paies.'],
};

function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

function buildArchitectMesh() {
  const g = new THREE.Group();

  const bodyMat = new THREE.MeshStandardMaterial({ color: 0x060608, metalness: 0.95, roughness: 0.08 });
  const cabinMat = new THREE.MeshStandardMaterial({ color: 0x08080f, metalness: 0.3, roughness: 0.25 });
  const redMat = new THREE.MeshStandardMaterial({ color: 0xff0011, emissive: 0xff0011, emissiveIntensity: 1.5 });

  // Long luxury body
  const body = new THREE.Mesh(new THREE.BoxGeometry(2.1, 0.58, 5.2), bodyMat);
  body.position.y = 0.56;
  g.add(body);

  // Low swept cabin
  const cabin = new THREE.Mesh(new THREE.BoxGeometry(1.75, 0.38, 2.3), cabinMat);
  cabin.position.set(0, 0.97, -0.5);
  g.add(cabin);

  // Red accent stripe along body
  const stripe = new THREE.Mesh(new THREE.BoxGeometry(2.12, 0.05, 5.2), redMat);
  stripe.position.set(0, 0.28, 0);
  g.add(stripe);

  // Glowing red headlights
  const hlGeo = new THREE.BoxGeometry(0.35, 0.14, 0.1);
  for (const xOff of [-0.78, 0.78]) {
    const hl = new THREE.Mesh(hlGeo, redMat);
    hl.position.set(xOff, 0.57, 2.62);
    g.add(hl);
  }

  // Wheels
  const wGeo = new THREE.CylinderGeometry(0.44, 0.44, 0.34, 14);
  const wMat = new THREE.MeshStandardMaterial({ color: 0x050505, metalness: 0.3 });
  for (const [x, y, z] of [[-1.05,0.44,1.5],[1.05,0.44,1.5],[-1.05,0.44,-1.5],[1.05,0.44,-1.5]]) {
    const w = new THREE.Mesh(wGeo, wMat);
    w.rotation.x = Math.PI / 2;
    w.position.set(x, y, z);
    g.add(w);
  }

  // Red point light under chassis — projects a menacing glow on the road
  const light = new THREE.PointLight(0xff0022, 1.2, 12);
  light.position.set(0, 0.3, 0);
  g.add(light);

  return g;
}

export class ArchitectSystem {
  constructor(scene, world) {
    this._scene = scene;
    this._world = world;
    this.active = false;
    this.mesh = null;

    this._pos = new THREE.Vector3();
    this._heading = 0;
    this._speed = 0;
    this._cooldown = 0;
    this._commandTimer = COMMAND_INTERVAL * 0.5; // first command sooner
    this._wantedHighTimer = 0;
    this._lastScore = 0;
    this._tauntTimer = 18;
    this._despawnFlag = false;
  }

  // Returns { raisedWanted: bool } so main.js can act on coordination signals.
  update(dt, vehicle, hud, wantedSystem, totalScore) {
    const result = { raisedWanted: false };
    if (!vehicle) return result;

    const playerPos = vehicle.getPosition();

    // Track 5-star timer for alternate spawn condition
    if (wantedSystem && wantedSystem.level >= 5) {
      this._wantedHighTimer += dt;
    } else {
      this._wantedHighTimer = 0;
    }

    if (this._cooldown > 0) { this._cooldown -= dt; return result; }

    // Spawn condition
    if (!this.active) {
      const scoreThresh  = totalScore >= SPAWN_SCORE;
      const wantedThresh = this._wantedHighTimer >= WANTED_5_TIME;
      if (scoreThresh || wantedThresh) {
        this._spawn(playerPos, hud);
      }
      return result;
    }

    if (!this.mesh) return result;

    // Despawn if too far (player escaped or drove off)
    const dist = Math.hypot(playerPos.x - this._pos.x, playerPos.z - this._pos.z);
    if (dist > DESPAWN_DIST) {
      if (hud) hud.showMessage(`L'ARCHITECTE : ${pick(DIALOGUES.escape)}`, 3500);
      this._despawn();
      return result;
    }

    // Seek player
    const dx = playerPos.x - this._pos.x;
    const dz = playerPos.z - this._pos.z;
    const targetH = Math.atan2(dx, dz);
    let diff = targetH - this._heading;
    while (diff >  Math.PI) diff -= Math.PI * 2;
    while (diff < -Math.PI) diff += Math.PI * 2;
    this._heading += Math.sign(diff) * Math.min(Math.abs(diff), TURN_RATE * dt);

    // Accelerate toward top speed, ease off when very close
    const targetSpeed = dist < 15 ? TOP_SPEED_MS * 0.4 : TOP_SPEED_MS;
    this._speed += (targetSpeed - this._speed) * Math.min(1, ACCEL_MS2 * dt / TOP_SPEED_MS);

    this._pos.x += Math.sin(this._heading) * this._speed * dt;
    this._pos.z += Math.cos(this._heading) * this._speed * dt;
    this.mesh.position.set(this._pos.x, 0, this._pos.z);
    this.mesh.rotation.y = this._heading;

    // Close-proximity taunt
    if (dist < 22 && this._tauntTimer <= 0) {
      if (hud) hud.showMessage(`L'ARCHITECTE : ${pick(DIALOGUES.close)}`, 2500);
      this._tauntTimer = 14 + Math.random() * 8;
    }
    this._tauntTimer -= dt;

    // Coordinated command attack
    this._commandTimer -= dt;
    if (this._commandTimer <= 0) {
      this._commandTimer = COMMAND_INTERVAL;
      if (hud) hud.showMessage(`L'ARCHITECTE : ${pick(DIALOGUES.command)}`, 3000);
      result.raisedWanted = true;
    }

    return result;
  }

  _spawn(playerPos, hud) {
    const angle = Math.random() * Math.PI * 2;
    this._pos.set(
      playerPos.x + Math.sin(angle) * SPAWN_DIST,
      0,
      playerPos.z + Math.cos(angle) * SPAWN_DIST
    );
    this._heading = Math.atan2(playerPos.x - this._pos.x, playerPos.z - this._pos.z);
    this._speed = 0;
    this.mesh = buildArchitectMesh();
    this.mesh.position.set(this._pos.x, 0, this._pos.z);
    this.mesh.rotation.y = this._heading;
    this._scene.add(this.mesh);
    this.active = true;
    this._commandTimer = COMMAND_INTERVAL * 0.5;
    this._tauntTimer = 6;
    if (hud) hud.showMessage(`L'ARCHITECTE : ${pick(DIALOGUES.spawn)}`, 4000);
  }

  _despawn() {
    if (this.mesh) {
      this._scene.remove(this.mesh);
      this.mesh.traverse(o => {
        if (o.geometry) o.geometry.dispose();
        if (o.material) o.material.dispose();
      });
      this.mesh = null;
    }
    this.active = false;
    this._speed = 0;
    this._wantedHighTimer = 0;
    this._cooldown = 120;
  }

  getPosition() {
    return this.active ? { x: this._pos.x, z: this._pos.z } : null;
  }
}
