import * as THREE from 'three';

// WantedSystem — niveau "recherché" 0-5 façon GTA simplifié :
// - monte si vitesse excessive prolongée, ou sur "crash" détecté (forte chute
//   de vitesse en un instant), avec un cooldown anti-spam ;
// - descend lentement quand on conduit proprement (sous le seuil, pas de crash) ;
// - fait apparaître 1-3 voitures de police (mesh boîte basse-poly, blanc/bleu)
//   qui poursuivent le joueur via un "seek" simple (direction vers la cible,
//   vitesse de rotation plafonnée, vitesse max légèrement < joueur) ;
// - se nettoie (despawn) quand le niveau retombe à 0.

const SPEED_THRESHOLD_KMH = 95; // au-dessus -> accumulation de chaleur
const HEAT_TIME_PER_LEVEL = 3.0; // secondes de vitesse excessive pour +1 étoile
const CRASH_SPEED_DROP_KMH = 45; // chute brutale de vitesse en un tick = crash
const CRASH_MIN_PRIOR_SPEED_KMH = 40; // il fallait rouler à une vitesse notable avant
const CRASH_COOLDOWN_S = 1.5; // anti-spam : un seul "crash" comptabilisé par fenêtre
const DECAY_DELAY_S = 4; // secondes de conduite propre avant que le niveau baisse
const DECAY_TIME_PER_LEVEL = 6; // secondes de conduite propre pour -1 étoile

const MAX_LEVEL = 5;
const CITY_HALF_SIZE = 100; // ville ~200x200 -> bords à ±100

const CAR_TOP_SPEED_KMH = {
  // vitesse max des poursuivants par étoile (toujours < vitesse max joueur)
  1: 70,
  2: 78,
  3: 86,
  4: 94,
  5: 102,
};
const CAR_TURN_RATE = 1.6; // rad/s, taux de rotation plafonné (IA simple)
const CAR_ACCEL_KMH_PER_S = 60; // accélération vers la vitesse cible

const HELI_ALTITUDE = 25;
const HELI_MAX_SPEED_H = 28; // m/s horizontal
const HELI_ACCEL_FACTOR = 3.5; // lerp rate toward desired velocity

function carCountForLevel(level) {
  if (level <= 0) return 0;
  if (level <= 2) return 1;
  if (level <= 4) return 2;
  return 3;
}

function buildPoliceCarMesh() {
  const group = new THREE.Group();

  const bodyMat = new THREE.MeshStandardMaterial({ color: 0xf5f7fa });
  const stripeMat = new THREE.MeshStandardMaterial({ color: 0x1565d8 });
  const cabinMat = new THREE.MeshStandardMaterial({ color: 0x111418 });

  const body = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.6, 4.2), bodyMat);
  body.position.y = 0.5;
  group.add(body);

  const cabin = new THREE.Mesh(new THREE.BoxGeometry(1.7, 0.55, 2.0), cabinMat);
  cabin.position.set(0, 1.05, -0.2);
  group.add(cabin);

  const stripe = new THREE.Mesh(new THREE.BoxGeometry(1.95, 0.18, 4.25), stripeMat);
  stripe.position.y = 0.62;
  group.add(stripe);

  // barre de gyrophares (petits cubes rouge/bleu)
  const lightBarGeo = new THREE.BoxGeometry(0.5, 0.18, 0.3);
  const redMat = new THREE.MeshStandardMaterial({ color: 0xff2222, emissive: 0xff0000, emissiveIntensity: 0.6 });
  const blueMat = new THREE.MeshStandardMaterial({ color: 0x2255ff, emissive: 0x1144ff, emissiveIntensity: 0.6 });
  const redLight = new THREE.Mesh(lightBarGeo, redMat);
  redLight.position.set(-0.35, 1.4, -0.2);
  const blueLight = new THREE.Mesh(lightBarGeo, blueMat);
  blueLight.position.set(0.35, 1.4, -0.2);
  group.add(redLight, blueLight);

  const wheelGeo = new THREE.BoxGeometry(0.4, 0.4, 0.8);
  const wheelMat = new THREE.MeshStandardMaterial({ color: 0x0a0a0a });
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

  group.userData.redLight = redLight;
  group.userData.blueLight = blueLight;

  return group;
}

function buildHelicopterMesh() {
  const group = new THREE.Group();
  const bodyMat   = new THREE.MeshStandardMaterial({ color: 0x1a1a2a, metalness: 0.5, roughness: 0.4 });
  const whiteMat  = new THREE.MeshStandardMaterial({ color: 0xf0f2f8 });
  const rotorMat  = new THREE.MeshStandardMaterial({ color: 0x111111, transparent: true, opacity: 0.75 });
  const glassMat  = new THREE.MeshStandardMaterial({ color: 0x223344, transparent: true, opacity: 0.4 });
  const spotMat   = new THREE.MeshStandardMaterial({ color: 0xffffcc, emissive: 0xffffcc, emissiveIntensity: 2.0 });
  const navRedMat = new THREE.MeshStandardMaterial({ color: 0xff2222, emissive: 0xff0000, emissiveIntensity: 1.5 });
  const navWhtMat = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 0.8 });

  const body = new THREE.Mesh(new THREE.BoxGeometry(1.8, 1.0, 4.5), bodyMat);
  group.add(body);
  const stripe = new THREE.Mesh(new THREE.BoxGeometry(1.85, 0.22, 4.55), whiteMat);
  stripe.position.y = 0.2;
  group.add(stripe);
  const cockpit = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.9, 1.5), glassMat);
  cockpit.position.set(0, 0.1, 1.6);
  group.add(cockpit);
  const tailBoom = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.5, 3.2), bodyMat);
  tailBoom.position.set(0, 0.15, -3.6);
  group.add(tailBoom);
  const fin = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.0, 1.1), bodyMat);
  fin.position.set(0, 0.75, -4.8);
  group.add(fin);
  const tailRotor = new THREE.Mesh(new THREE.BoxGeometry(0.1, 1.6, 0.18), rotorMat);
  tailRotor.position.set(0.38, 0.75, -5.0);
  group.add(tailRotor);

  const rotorHub = new THREE.Group();
  rotorHub.position.y = 0.65;
  const blade1 = new THREE.Mesh(new THREE.BoxGeometry(7.5, 0.06, 0.38), rotorMat);
  const blade2 = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.06, 7.5), rotorMat);
  rotorHub.add(blade1, blade2);
  group.add(rotorHub);
  group.userData.rotorHub = rotorHub;

  const skidMat = new THREE.MeshStandardMaterial({ color: 0x222222 });
  const skidGeo = new THREE.BoxGeometry(0.14, 0.12, 4.0);
  for (const side of [-1.1, 1.1]) {
    group.add(Object.assign(new THREE.Mesh(skidGeo, skidMat), { position: new THREE.Vector3(side, -0.65, 0) }));
    for (const z of [-1.2, 1.2]) {
      group.add(Object.assign(new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.55, 0.1), skidMat), { position: new THREE.Vector3(side, -0.3, z) }));
    }
  }

  const navRed = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.2, 0.2), navRedMat);
  navRed.position.set(-0.92, 0, 2.2);
  const navWht = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.2, 0.2), navWhtMat);
  navWht.position.set(0, -0.58, -4.9);
  group.add(navRed, navWht);
  group.userData.navRed = navRed;
  group.userData.navWht = navWht;

  const spotLens = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.18, 0.38), spotMat);
  spotLens.position.set(0, -0.72, 1.0);
  group.add(spotLens);

  return group;
}

class Helicopter {
  constructor(scene, playerPos) {
    this.scene = scene;
    this.mesh = buildHelicopterMesh();
    this.heading = 0;
    this._velX = 0;
    this._velZ = 0;
    this._blinkT = 0;

    this.mesh.position.set(playerPos.x + 15, HELI_ALTITUDE, playerPos.z + 15);
    scene.add(this.mesh);

    this.spotlight = new THREE.PointLight(0xffffaa, 3.0, 50, 1.2);
    this.spotlight.position.copy(this.mesh.position);
    scene.add(this.spotlight);
  }

  update(dt, targetPos) {
    this._blinkT += dt;
    const blink = Math.sin(this._blinkT * 2.2) > 0;
    this.mesh.userData.navRed.material.emissiveIntensity = blink ? 1.8 : 0.05;
    this.mesh.userData.navWht.material.emissiveIntensity = blink ? 0.05 : 1.2;
    if (this.mesh.userData.rotorHub) {
      this.mesh.userData.rotorHub.rotation.y += dt * 18;
    }

    const dx = targetPos.x - this.mesh.position.x;
    const dz = targetPos.z - this.mesh.position.z;
    const distH = Math.hypot(dx, dz);
    const desiredVX = distH > 4 ? (dx / distH) * HELI_MAX_SPEED_H : 0;
    const desiredVZ = distH > 4 ? (dz / distH) * HELI_MAX_SPEED_H : 0;
    const lerpRate = Math.min(1, dt * HELI_ACCEL_FACTOR);
    this._velX += (desiredVX - this._velX) * lerpRate;
    this._velZ += (desiredVZ - this._velZ) * lerpRate;

    this.mesh.position.x += this._velX * dt;
    this.mesh.position.z += this._velZ * dt;
    this.mesh.position.y = HELI_ALTITUDE;

    const spd = Math.hypot(this._velX, this._velZ);
    if (spd > 0.5) this.heading = Math.atan2(this._velX, this._velZ);
    this.mesh.rotation.y = this.heading;
    this.mesh.rotation.z = Math.min(0.18, spd / HELI_MAX_SPEED_H * 0.28) * Math.sign(this._velX);

    this.spotlight.position.set(this.mesh.position.x, this.mesh.position.y - 6, this.mesh.position.z);
  }

  dispose() {
    this.scene.remove(this.mesh);
    this.mesh.traverse((o) => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); });
    this.scene.remove(this.spotlight);
    this.spotlight.dispose();
    this.mesh = null;
  }
}

function buildBarrierMesh() {
  const group = new THREE.Group();
  const orangeMat = new THREE.MeshStandardMaterial({ color: 0xff6600, emissive: 0xff3300, emissiveIntensity: 0.3 });
  const whiteMat  = new THREE.MeshStandardMaterial({ color: 0xeeeeee });
  const baseMat   = new THREE.MeshStandardMaterial({ color: 0x222222 });

  const bar = new THREE.Mesh(new THREE.BoxGeometry(4.0, 1.0, 0.3), orangeMat);
  bar.position.y = 0.8;
  group.add(bar);
  for (const xOff of [-1.5, 0, 1.5]) {
    const stripe = new THREE.Mesh(new THREE.BoxGeometry(0.5, 1.02, 0.32), whiteMat);
    stripe.position.set(xOff, 0.8, 0);
    group.add(stripe);
  }
  const base = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.2, 0.6), baseMat);
  base.position.y = 0.1;
  group.add(base);
  return group;
}

class Roadblock {
  constructor(scene, playerPos, playerHeading) {
    this.scene = scene;
    this.barriers = [];
    this.colliders = [];
    this.timer = 50;

    const angle = playerHeading + (Math.random() - 0.5) * 0.4;
    const dist  = 55 + Math.random() * 25;
    const cx = playerPos.x + Math.sin(angle) * dist;
    const cz = playerPos.z + Math.cos(angle) * dist;

    const count  = 2 + Math.floor(Math.random() * 2); // 2-3 barrières
    const perpX  = Math.cos(angle);
    const perpZ  = -Math.sin(angle);
    const SPACING = 3.8;

    for (let i = 0; i < count; i++) {
      const off = (i - (count - 1) / 2) * SPACING;
      const bx = cx + perpX * off;
      const bz = cz + perpZ * off;

      const mesh = buildBarrierMesh();
      mesh.position.set(bx, 0, bz);
      mesh.rotation.y = angle + Math.PI / 2;
      scene.add(mesh);
      this.barriers.push(mesh);
      this.colliders.push({ x: bx, z: bz, halfWidth: 2.1, halfDepth: 0.5 });
    }
  }

  getColliders() { return this.colliders; }

  dispose() {
    for (const mesh of this.barriers) {
      this.scene.remove(mesh);
      mesh.traverse((o) => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); });
    }
    this.barriers = [];
    this.colliders = [];
  }
}

class PoliceCar {
  constructor(scene, x, z, heading) {
    this.mesh = buildPoliceCarMesh();
    this.mesh.position.set(x, 0, z);
    this.heading = heading;
    this.mesh.rotation.y = heading;
    this.speedKmh = 0;
    scene.add(this.mesh);
    this._lightBlinkT = Math.random() * 10;
  }

  update(dt, targetPos, level) {
    this._lightBlinkT += dt;
    const blink = Math.sin(this._lightBlinkT * 10) > 0;
    this.mesh.userData.redLight.material.emissiveIntensity = blink ? 1.2 : 0.1;
    this.mesh.userData.blueLight.material.emissiveIntensity = blink ? 0.1 : 1.2;

    const dx = targetPos.x - this.mesh.position.x;
    const dz = targetPos.z - this.mesh.position.z;
    const distToTarget = Math.hypot(dx, dz);

    // Seek : direction désirée vers la cible.
    const desiredHeading = Math.atan2(dx, dz);
    let diff = desiredHeading - this.heading;
    // normalise dans [-PI, PI] pour tourner du côté le plus court
    diff = Math.atan2(Math.sin(diff), Math.cos(diff));
    const maxTurn = CAR_TURN_RATE * dt;
    this.heading += Math.max(-maxTurn, Math.min(maxTurn, diff));
    this.mesh.rotation.y = this.heading;

    const topSpeed = CAR_TOP_SPEED_KMH[level] || CAR_TOP_SPEED_KMH[1];
    // ralentit un peu si très proche du joueur pour éviter de "vibrer" sur la cible
    const targetSpeed = distToTarget < 4 ? topSpeed * 0.3 : topSpeed;
    const maxDelta = CAR_ACCEL_KMH_PER_S * dt;
    if (this.speedKmh < targetSpeed) {
      this.speedKmh = Math.min(targetSpeed, this.speedKmh + maxDelta);
    } else {
      this.speedKmh = Math.max(targetSpeed, this.speedKmh - maxDelta * 2);
    }

    const speedMs = (this.speedKmh / 3.6) * dt;
    this.mesh.position.x += Math.sin(this.heading) * speedMs;
    this.mesh.position.z += Math.cos(this.heading) * speedMs;
  }

  dispose(scene) {
    scene.remove(this.mesh);
    this.mesh.traverse((obj) => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) obj.material.dispose();
    });
  }
}

export class WantedSystem {
  constructor(scene, world) {
    this.scene = scene;
    this.world = world;

    this.level = 0;
    this._heatTimer = 0;
    this._cleanTimer = 0;
    this._crashCooldown = 0;
    this._prevSpeedKmh = 0;
    this._helicopter = null;
    this._roadblocks = [];
    this._extraRoadblockTimer = 0;
    this._lastPlayerHeading = 0;

    this.cars = [];
  }

  _setLevel(newLevel, hud) {
    const clamped = Math.max(0, Math.min(MAX_LEVEL, newLevel));
    if (clamped === this.level) return;
    const prevLevel = this.level;
    this.level = clamped;
    if (hud) hud.setWanted(this.level);
    this._syncCarCount();
    // Hélicoptère : déployé à partir de 4 étoiles
    if (clamped >= 4 && !this._helicopter && this._lastPlayerPos) {
      this._helicopter = new Helicopter(this.scene, this._lastPlayerPos);
      if (hud) hud.showMessage('NIVEAU 4 — Hélicoptère déployé !', 2500);
    } else if (clamped < 4 && this._helicopter) {
      this._helicopter.dispose();
      this._helicopter = null;
    }
    // Barrages : spawn au passage de 2→3, clear si on descend sous 3
    if (clamped >= 3 && prevLevel < 3 && this._lastPlayerPos) {
      this._roadblocks.push(new Roadblock(this.scene, this._lastPlayerPos, this._lastPlayerHeading));
    } else if (clamped < 3) {
      for (const rb of this._roadblocks) rb.dispose();
      this._roadblocks = [];
    }
  }

  getHelicopterActive() {
    return this._helicopter !== null;
  }

  _syncCarCount() {
    const desired = carCountForLevel(this.level);
    while (this.cars.length > desired) {
      const car = this.cars.pop();
      car.dispose(this.scene);
    }
    while (this.cars.length < desired) {
      this.cars.push(this._spawnCar());
    }
  }

  _spawnCar() {
    const spawn = this._pickSpawnPoint();
    return new PoliceCar(this.scene, spawn.x, spawn.z, spawn.heading);
  }

  _pickSpawnPoint() {
    const playerPos = this._lastPlayerPos || { x: 0, z: 0 };
    // Apparaît à bonne distance du joueur, vers un bord de la ville,
    // sur un offset fixe pour rester simple (pas de pathfinding/voirie).
    const angle = Math.random() * Math.PI * 2;
    const dist = 40 + Math.random() * 30;
    let x = playerPos.x + Math.sin(angle) * dist;
    let z = playerPos.z + Math.cos(angle) * dist;
    x = Math.max(-CITY_HALF_SIZE + 5, Math.min(CITY_HALF_SIZE - 5, x));
    z = Math.max(-CITY_HALF_SIZE + 5, Math.min(CITY_HALF_SIZE - 5, z));
    const heading = Math.atan2(playerPos.x - x, playerPos.z - z);
    return { x, z, heading };
  }

  update(dt, vehicle, hud) {
    if (!vehicle || typeof vehicle.getPosition !== 'function') return;

    const pos = vehicle.getPosition();
    this._lastPlayerPos = pos;
    this._lastPlayerHeading = typeof vehicle.getHeading === 'function' ? vehicle.getHeading() : 0;
    const speedKmh = typeof vehicle.getSpeedKmh === 'function' ? vehicle.getSpeedKmh() : 0;

    this._crashCooldown = Math.max(0, this._crashCooldown - dt);

    const speedDrop = this._prevSpeedKmh - speedKmh;
    const crashed =
      this._crashCooldown <= 0 &&
      this._prevSpeedKmh >= CRASH_MIN_PRIOR_SPEED_KMH &&
      speedDrop >= CRASH_SPEED_DROP_KMH;

    if (crashed) {
      this._crashCooldown = CRASH_COOLDOWN_S;
      this._heatTimer = 0;
      this._cleanTimer = 0;
      this._setLevel(this.level + 1, hud);
    }

    const speeding = speedKmh > SPEED_THRESHOLD_KMH;

    if (speeding) {
      this._heatTimer += dt;
      this._cleanTimer = 0;
      if (this._heatTimer >= HEAT_TIME_PER_LEVEL) {
        this._heatTimer = 0;
        this._setLevel(this.level + 1, hud);
      }
    } else if (!crashed) {
      this._heatTimer = Math.max(0, this._heatTimer - dt * 0.5);
    }

    if (!speeding && !crashed && this.level > 0) {
      this._cleanTimer += dt;
      if (this._cleanTimer >= DECAY_DELAY_S) {
        this._cleanTimer = DECAY_DELAY_S; // ne pas accumuler indéfiniment
        this._decayAccum = (this._decayAccum || 0) + dt;
        if (this._decayAccum >= DECAY_TIME_PER_LEVEL) {
          this._decayAccum = 0;
          this._setLevel(this.level - 1, hud);
        }
      }
    } else {
      this._decayAccum = 0;
    }

    this._prevSpeedKmh = speedKmh;

    for (const car of this.cars) {
      car.update(dt, pos, this.level);
    }
    if (this._helicopter) {
      this._helicopter.update(dt, pos);
    }

    // Barrages : timer + spawn supplémentaire au niveau 5
    for (let i = this._roadblocks.length - 1; i >= 0; i--) {
      this._roadblocks[i].timer -= dt;
      if (this._roadblocks[i].timer <= 0) {
        this._roadblocks[i].dispose();
        this._roadblocks.splice(i, 1);
      }
    }
    if (this.level === 5 && this._lastPlayerPos) {
      this._extraRoadblockTimer += dt;
      if (this._extraRoadblockTimer >= 22) {
        this._roadblocks.push(new Roadblock(this.scene, this._lastPlayerPos, this._lastPlayerHeading));
        this._extraRoadblockTimer = 0;
      }
    } else {
      this._extraRoadblockTimer = 0;
    }
  }

  getRoadblockColliders() {
    const result = [];
    for (const rb of this._roadblocks) result.push(...rb.getColliders());
    return result;
  }
}
