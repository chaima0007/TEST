/**
 * fantome.js — La Fantome: the mysterious white car that races at night.
 */

import * as THREE from 'three';

const TOP_SPEED_KMH = 125;
const TURN_RATE = 1.8;
const ACCEL_KMH_S = 80;

const TOP_SPEED_MS = TOP_SPEED_KMH / 3.6;
const ACCEL_MS2 = ACCEL_KMH_S / 3.6;

const SPAWN_DISTANCE = 30;
const CHECKPOINT_MIN = 70;
const CHECKPOINT_MAX = 180;
const CHECKPOINT_RADIUS = 8;
const INITIAL_COOLDOWN = 15;

const DIALOGUES = {
  challenge: [
    "Tu crois pouvoir me battre, petit conducteur ?",
    "Cette nuit, la route m'appartient... suis-moi si tu l'oses.",
    "Personne ne m'a jamais devancee. Cette nuit sera differente ?"
  ],
  win: [
    "Impressionnant... tu m'as battue. Jusqu'a la prochaine nuit.",
    "La victoire est tienne cette fois. Mais je reviendrai."
  ],
  lose: [
    "Ha ! La route m'obeit toujours. Tu n'etais pas a la hauteur.",
    "La Fantome ne perd jamais. Reviens quand tu seras pret."
  ]
};

function pick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function buildFantomeMesh() {
  const group = new THREE.Group();

  // Body
  const bodyMat = new THREE.MeshStandardMaterial({
    color: 0xfff8e7,
    metalness: 0.7,
    roughness: 0.2
  });
  const bodyGeo = new THREE.BoxGeometry(1.85, 0.52, 4.2);
  const body = new THREE.Mesh(bodyGeo, bodyMat);
  body.position.set(0, 0.5, 0);
  group.add(body);

  // Cabin
  const cabinMat = new THREE.MeshStandardMaterial({
    color: 0x222211,
    metalness: 0.5,
    roughness: 0.4
  });
  const cabinGeo = new THREE.BoxGeometry(1.5, 0.48, 1.9);
  const cabin = new THREE.Mesh(cabinGeo, cabinMat);
  cabin.position.set(0, 0.94, -0.25);
  group.add(cabin);

  // Gold accent stripes
  const goldMat = new THREE.MeshStandardMaterial({
    color: 0xffd700,
    emissive: 0xffaa00,
    emissiveIntensity: 0.8,
    metalness: 0.8,
    roughness: 0.2
  });
  const stripeGeo = new THREE.BoxGeometry(0.06, 0.08, 3.8);

  const stripeL = new THREE.Mesh(stripeGeo, goldMat);
  stripeL.position.set(-0.94, 0.32, 0);
  group.add(stripeL);

  const stripeR = new THREE.Mesh(stripeGeo, goldMat);
  stripeR.position.set(0.94, 0.32, 0);
  group.add(stripeR);

  // Wheels: dark tires + small gold rim box
  const tireMat = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.9 });
  const rimMat = new THREE.MeshStandardMaterial({ color: 0xffd700, metalness: 0.9, roughness: 0.1 });

  const tireGeo = new THREE.BoxGeometry(0.22, 0.4, 0.4);
  const rimGeo = new THREE.BoxGeometry(0.24, 0.22, 0.22);

  const wheelPositions = [
    [-0.97, 0.25, 1.4],
    [0.97, 0.25, 1.4],
    [-0.97, 0.25, -1.4],
    [0.97, 0.25, -1.4]
  ];

  for (const [wx, wy, wz] of wheelPositions) {
    const tire = new THREE.Mesh(tireGeo, tireMat);
    tire.position.set(wx, wy, wz);
    group.add(tire);

    const rim = new THREE.Mesh(rimGeo, rimMat);
    rim.position.set(wx, wy, wz);
    group.add(rim);
  }

  return group;
}

function buildCheckpointMarker() {
  const group = new THREE.Group();

  const torusGeo = new THREE.TorusGeometry(4, 0.3, 8, 24);
  const goldMat = new THREE.MeshStandardMaterial({
    color: 0xffd700,
    emissive: 0xffaa00,
    emissiveIntensity: 0.6,
    metalness: 0.8,
    roughness: 0.2
  });

  const torus = new THREE.Mesh(torusGeo, goldMat);
  torus.rotation.x = Math.PI / 2;
  torus.position.y = 2;
  group.add(torus);

  return group;
}

export class FantomeSystem {
  constructor(scene, world) {
    this._scene = scene;
    this._world = world;
    this._score = 0;
    this._winsCount = 0;

    this._cooldown = INITIAL_COOLDOWN;
    this._active = false;
    this._racing = false;

    this._fantomeMesh = null;
    this._checkpointMarker = null;
    this._checkpointPos = new THREE.Vector3();

    this._fantomePos = new THREE.Vector3();
    this._fantomeHeading = 0;
    this._fantomeSpeed = 0;
    this._winFlag = false;
  }

  // Public property aliases expected by main.js
  get active() { return this._active; }
  get mesh() { return this._fantomeMesh; }
  get _speed() { return this._fantomeSpeed; }

  getScore() {
    return this._score;
  }

  // Returns true once after the player wins a race, then resets.
  popWin() {
    if (!this._winFlag) return false;
    this._winFlag = false;
    return true;
  }

  update(dt, vehicle, hud, isNight) {
    // Despawn if daytime arrives during a race
    if (this._active && !isNight) {
      this._despawn(false);
      return;
    }

    if (!isNight) {
      return;
    }

    // Cooldown phase — waiting to spawn
    if (!this._active) {
      this._cooldown -= dt;
      if (this._cooldown <= 0) {
        this._spawn(vehicle, hud);
      }
      return;
    }

    // Active race phase
    if (this._racing) {
      this._updateFantomeAI(dt);
      this._updateCheckpointMarker(dt);
      this._checkRaceConditions(vehicle, hud);
    }
  }

  _spawn(vehicle, hud) {
    const playerPos = vehicle.position
      ? vehicle.position
      : (vehicle.chassisBody ? vehicle.chassisBody.position : new THREE.Vector3());

    const angle = Math.random() * Math.PI * 2;

    // Fantome spawns 30m from player
    this._fantomePos.set(
      playerPos.x + Math.cos(angle) * SPAWN_DISTANCE,
      0,
      playerPos.z + Math.sin(angle) * SPAWN_DISTANCE
    );
    this._fantomeHeading = angle + Math.PI; // face roughly toward player area
    this._fantomeSpeed = 0;

    // Checkpoint spawns 70-180m away in random direction
    const cpAngle = Math.random() * Math.PI * 2;
    const cpDist = CHECKPOINT_MIN + Math.random() * (CHECKPOINT_MAX - CHECKPOINT_MIN);
    this._checkpointPos.set(
      playerPos.x + Math.cos(cpAngle) * cpDist,
      0,
      playerPos.z + Math.sin(cpAngle) * cpDist
    );

    // Build meshes
    this._fantomeMesh = buildFantomeMesh();
    this._fantomeMesh.position.copy(this._fantomePos);
    this._scene.add(this._fantomeMesh);

    this._checkpointMarker = buildCheckpointMarker();
    this._checkpointMarker.position.copy(this._checkpointPos);
    this._scene.add(this._checkpointMarker);

    this._active = true;
    this._racing = true;

    // Challenge dialogue
    if (hud && hud.showDialogue) {
      hud.showDialogue("La Fantome", pick(DIALOGUES.challenge));
    }
  }

  _despawn(resetCooldown = true) {
    if (this._fantomeMesh) {
      this._scene.remove(this._fantomeMesh);
      this._fantomeMesh = null;
    }
    if (this._checkpointMarker) {
      this._scene.remove(this._checkpointMarker);
      this._checkpointMarker = null;
    }

    this._active = false;
    this._racing = false;
    this._fantomeSpeed = 0;

    if (resetCooldown) {
      this._cooldown = 30 + Math.random() * 30;
    }
  }

  _playerWins(hud) {
    this._winsCount += 1;
    this._score += 600;
    this._winFlag = true;

    if (hud && hud.showDialogue) {
      hud.showDialogue("La Fantome", pick(DIALOGUES.win));
    }
    if (hud && hud.addScore) {
      hud.addScore(600);
    }

    this._despawn(true);
  }

  _fantomeWins(hud) {
    if (hud && hud.showDialogue) {
      hud.showDialogue("La Fantome", pick(DIALOGUES.lose));
    }

    this._despawn(true);
  }

  _updateFantomeAI(dt) {
    if (!this._fantomeMesh) return;

    // Seek checkpoint using atan2
    const dx = this._checkpointPos.x - this._fantomePos.x;
    const dz = this._checkpointPos.z - this._fantomePos.z;
    const targetHeading = Math.atan2(dx, dz);

    // Compute shortest angular difference
    let headingDiff = targetHeading - this._fantomeHeading;
    while (headingDiff > Math.PI) headingDiff -= Math.PI * 2;
    while (headingDiff < -Math.PI) headingDiff += Math.PI * 2;

    // Clamp turn rate
    const maxTurn = TURN_RATE * dt;
    const turnAmount = Math.max(-maxTurn, Math.min(maxTurn, headingDiff));
    this._fantomeHeading += turnAmount;

    // Accelerate toward top speed
    this._fantomeSpeed = Math.min(
      TOP_SPEED_MS,
      this._fantomeSpeed + ACCEL_MS2 * dt
    );

    // Move
    this._fantomePos.x += Math.sin(this._fantomeHeading) * this._fantomeSpeed * dt;
    this._fantomePos.z += Math.cos(this._fantomeHeading) * this._fantomeSpeed * dt;

    // Sync mesh
    this._fantomeMesh.position.set(this._fantomePos.x, 0, this._fantomePos.z);
    this._fantomeMesh.rotation.y = this._fantomeHeading;
  }

  _updateCheckpointMarker(dt) {
    if (this._checkpointMarker) {
      this._checkpointMarker.rotation.y += dt * 1.2;
    }
  }

  _checkRaceConditions(vehicle, hud) {
    const playerPos = vehicle.position
      ? vehicle.position
      : (vehicle.chassisBody ? vehicle.chassisBody.position : null);

    if (!playerPos) return;

    const cpX = this._checkpointPos.x;
    const cpZ = this._checkpointPos.z;

    // Player distance to checkpoint
    const pdx = playerPos.x - cpX;
    const pdz = playerPos.z - cpZ;
    const playerDist = Math.sqrt(pdx * pdx + pdz * pdz);

    // Fantome distance to checkpoint
    const fdx = this._fantomePos.x - cpX;
    const fdz = this._fantomePos.z - cpZ;
    const fantomeDist = Math.sqrt(fdx * fdx + fdz * fdz);

    if (playerDist < CHECKPOINT_RADIUS) {
      this._playerWins(hud);
    } else if (fantomeDist < CHECKPOINT_RADIUS) {
      this._fantomeWins(hud);
    }
  }
}
