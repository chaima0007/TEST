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

    this.cars = [];
  }

  _setLevel(newLevel, hud) {
    const clamped = Math.max(0, Math.min(MAX_LEVEL, newLevel));
    if (clamped === this.level) return;
    this.level = clamped;
    if (hud) hud.setWanted(this.level);
    this._syncCarCount();
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
  }
}
