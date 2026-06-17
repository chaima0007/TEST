import * as THREE from 'three';

// DetectiveSystem — "Le Detectif", une voiture de police banalisee qui apparait
// au niveau 2+ de recherche. Aucune sirene, aucun marquage visible. Elle suit
// silencieusement le joueur et accelere le gain de chaleur ("wanted heat")
// lorsqu'elle est suffisamment proche.

const SPAWN_DIST = 45;          // m from player at spawn
const TAIL_RADIUS = 18;         // m — this close = actively tailing
const LOSE_SPEED_KMH = 118;    // player must exceed this speed for 3s to shake him
const TOP_SPEED_KMH = 105;     // faster than regular police but slightly slower than player max
const TURN_RATE = 1.8;
const ACCEL_KMH_S = 75;
const HEAT_MULT_WHEN_TAILING = 2.2; // multiplier on wanted heat rate when detective is close
const SPAWN_COOLDOWN_S = 40;
const SHAKE_TIME_S = 3;

function buildDetectiveMesh() {
  const group = new THREE.Group();

  const bodyMat = new THREE.MeshStandardMaterial({ color: 0x1a2035 });
  const cabinMat = new THREE.MeshStandardMaterial({ color: 0x0d1020 });
  const wheelMat = new THREE.MeshStandardMaterial({ color: 0x0a0a0a });

  // Plain dark navy body — looks like a civilian car
  const body = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.58, 4.1), bodyMat);
  body.position.y = 0.52;
  group.add(body);

  // Dark cabin
  const cabin = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.5, 2.0), cabinMat);
  cabin.position.set(0, 0.96, -0.2);
  group.add(cabin);

  // Small hidden red dot — only lights up when actively tailing
  const dotMat = new THREE.MeshStandardMaterial({
    color: 0xff0000,
    emissive: 0xff0000,
    emissiveIntensity: 0,
  });
  const dot = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.1, 0.1), dotMat);
  dot.position.set(0, 0.85, 1.9);
  group.add(dot);
  group.userData.dot = dot;

  // Black wheels
  const wheelGeo = new THREE.BoxGeometry(0.4, 0.4, 0.8);
  const wheelOffsets = [
    [-0.95, 0.25, 1.3],
    [0.95, 0.25, 1.3],
    [-0.95, 0.25, -1.3],
    [0.95, 0.25, -1.3],
  ];
  wheelOffsets.forEach(([x, y, z]) => {
    const wheel = new THREE.Mesh(wheelGeo, wheelMat);
    wheel.position.set(x, y, z);
    group.add(wheel);
  });

  return group;
}

export class DetectiveSystem {
  constructor(scene, world) {
    this.scene = scene;
    this.world = world;

    this.active = false;
    this.mesh = null;
    this._cooldown = 25;
    this._tailTimer = 0;
    this._shakeTimer = 0;
    this._speed = 0;
    this._heading = 0;
    this._escapedFlag = false;
  }

  isTailing() {
    return this._tailTimer > 1.5;
  }

  // Returns true once after the detective loses the player's trail.
  popEscaped() {
    if (!this._escapedFlag) return false;
    this._escapedFlag = false;
    return true;
  }

  _spawn(playerPos, hud) {
    const angle = Math.random() * Math.PI * 2;
    const x = playerPos.x + Math.sin(angle) * SPAWN_DIST;
    const z = playerPos.z + Math.cos(angle) * SPAWN_DIST;

    this.mesh = buildDetectiveMesh();
    this.mesh.position.set(x, 0, z);
    this._heading = Math.atan2(playerPos.x - x, playerPos.z - z);
    this.mesh.rotation.y = this._heading;
    this._speed = 0;
    this._tailTimer = 0;
    this._shakeTimer = 0;
    this.active = true;

    this.scene.add(this.mesh);

    if (hud && typeof hud.showMessage === 'function') {
      hud.showMessage('Un vehicule suspect vous suit...', 3000);
    }
  }

  _despawn(hud, message) {
    if (this.mesh) {
      this.scene.remove(this.mesh);
      this.mesh.traverse((obj) => {
        if (obj.geometry) obj.geometry.dispose();
        if (obj.material) obj.material.dispose();
      });
      this.mesh = null;
    }
    this.active = false;
    this._tailTimer = 0;
    this._shakeTimer = 0;
    this._speed = 0;
    this._cooldown = SPAWN_COOLDOWN_S;

    if (hud && typeof hud.showMessage === 'function' && message) {
      hud.showMessage(message, 3000);
    }
  }

  update(dt, vehicle, hud, wantedLevel) {
    if (!vehicle || typeof vehicle.getPosition !== 'function') return false;

    // Tick cooldown
    if (this._cooldown > 0) {
      this._cooldown = Math.max(0, this._cooldown - dt);
    }

    // Despawn if wanted level drops below 2
    if (this.active && wantedLevel < 2) {
      this._despawn(hud, null);
      return false;
    }

    // Spawn when conditions are met
    if (!this.active && wantedLevel >= 2 && this._cooldown <= 0) {
      const pos = vehicle.getPosition();
      this._spawn(pos, hud);
    }

    if (!this.active || !this.mesh) return false;

    const playerPos = vehicle.getPosition();
    const playerSpeedKmh = typeof vehicle.getSpeedKmh === 'function' ? vehicle.getSpeedKmh() : 0;

    // Distance to player
    const dx = playerPos.x - this.mesh.position.x;
    const dz = playerPos.z - this.mesh.position.z;
    const dist = Math.hypot(dx, dz);

    // Seek AI — same turn-rate pattern as PoliceCar in police.js
    const desiredHeading = Math.atan2(dx, dz);
    let diff = desiredHeading - this._heading;
    diff = Math.atan2(Math.sin(diff), Math.cos(diff));
    const maxTurn = TURN_RATE * dt;
    this._heading += Math.max(-maxTurn, Math.min(maxTurn, diff));
    this.mesh.rotation.y = this._heading;

    // Accelerate toward top speed (slow near player to avoid jitter)
    const targetSpeed = dist < 4 ? TOP_SPEED_KMH * 0.3 : TOP_SPEED_KMH;
    const maxDelta = ACCEL_KMH_S * dt;
    if (this._speed < targetSpeed) {
      this._speed = Math.min(targetSpeed, this._speed + maxDelta);
    } else {
      this._speed = Math.max(targetSpeed, this._speed - maxDelta * 2);
    }

    const speedMs = (this._speed / 3.6) * dt;
    this.mesh.position.x += Math.sin(this._heading) * speedMs;
    this.mesh.position.z += Math.cos(this._heading) * speedMs;

    // Tailing check
    const dot = this.mesh.userData.dot;
    if (dist < TAIL_RADIUS) {
      this._tailTimer += dt;
      if (dot) dot.material.emissiveIntensity = 0.8;
    } else {
      this._tailTimer = 0;
      if (dot) dot.material.emissiveIntensity = 0;
    }

    // Shake / lose-trail check
    if (playerSpeedKmh > LOSE_SPEED_KMH) {
      this._shakeTimer += dt;
      if (this._shakeTimer >= SHAKE_TIME_S) {
        this._escapedFlag = true;
        this._despawn(hud, 'LE DETECTIF : piste perdue.');
        return false;
      }
    } else {
      this._shakeTimer = 0;
    }

    return this.isTailing();
  }
}
