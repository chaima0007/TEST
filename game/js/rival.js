import * as THREE from 'three';

// RivalSystem — "Le Spectre", un personnage hors du commun façon GTA :
// un rival de course masqué et reconnaissable (carrosserie noire mate,
// néons violets, aileron XXL) qui surgit par surprise pour défier le
// joueur en pleine ville. Réutilise un comportement de "seek" simple,
// dans le même esprit que police.js, mais avec sa propre identité
// visuelle et ses propres règles : un défi chronométré (le semer ou se
// faire rattraper), pas une arrestation.

const SPAWN_COOLDOWN_MIN_S = 35;
const SPAWN_COOLDOWN_MAX_S = 70;
const CHALLENGE_DURATION_S = 22; // temps à survivre pour semer Le Spectre
const CATCH_RADIUS = 5.5; // distance pour considérer qu'il vous a rattrapé
const CATCH_HOLD_S = 1.2; // temps consécutif sous CATCH_RADIUS avant capture
const TOP_SPEED_KMH = 132; // légèrement plus rapide que la police, mais < vitesse max joueur
const TURN_RATE = 1.9; // rad/s, IA simple comme police.js
const ACCEL_KMH_PER_S = 70;
const SPAWN_DIST_MIN = 35;
const SPAWN_DIST_MAX = 55;
const TAUNT_INTERVAL_MIN_S = 6;
const TAUNT_INTERVAL_MAX_S = 10;
const BONUS_ESCAPE = 400;
const TAUNT_ORBIT_RADIUS = 8; // m — distance autour du joueur pendant l'état TAUNT
const TAUNT_ORBIT_DURATION_S = 3.5; // durée de l'orbite avant de reprendre la chasse
const REVENGE_COOLDOWN_REDUCTION = 8; // s de moins par fuite subie (Le Spectre revient plus vite s'il a honte)

// Trois pools de répliques selon l'état émotionnel du Spectre.
const TAUNTS_HUNT = [
  "Le Spectre : « Tu ne peux pas m’échapper… »",
  'Le Spectre : « Cours, cours ! »',
  'Le Spectre : « Intéressant. »',
];
const TAUNTS_CLOSE = [
  "Le Spectre : « Je t’ai ! »",
  'Le Spectre : « Trop facile. »',
  'Le Spectre : « Joli essai. »',
];
const TAUNTS_ANGRY = [
  "Le Spectre : « Tu m’as eu une fois. Une seule ! »",
  'Le Spectre : « Revanche ! »',
  'Le Spectre : « Cette fois, tu ne passeras pas. »',
];

function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

function buildRivalMesh() {
  const group = new THREE.Group();

  const bodyMat = new THREE.MeshStandardMaterial({ color: 0x0d0d12, metalness: 0.6, roughness: 0.3 });
  const neonMat = new THREE.MeshStandardMaterial({ color: 0xaa33ff, emissive: 0xaa33ff, emissiveIntensity: 1.1 });
  const cabinMat = new THREE.MeshStandardMaterial({ color: 0x05050a, metalness: 0.4, roughness: 0.3 });
  const wheelMat = new THREE.MeshStandardMaterial({ color: 0x0a0a0a });

  const body = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.55, 4.3), bodyMat);
  body.position.y = 0.5;
  group.add(body);

  const cabin = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.5, 1.8), cabinMat);
  cabin.position.set(0, 0.95, -0.3);
  group.add(cabin);

  // Néons le long des flancs : la "signature" visuelle du personnage.
  const stripeL = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.1, 3.6), neonMat);
  stripeL.position.set(-0.96, 0.35, 0);
  group.add(stripeL);
  const stripeR = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.1, 3.6), neonMat);
  stripeR.position.set(0.96, 0.35, 0);
  group.add(stripeR);

  // Aileron XXL à l'arrière, signature "course-poursuite".
  const standGeo = new THREE.BoxGeometry(0.15, 0.5, 0.15);
  const standL = new THREE.Mesh(standGeo, bodyMat);
  standL.position.set(-0.7, 0.75, -2.0);
  const standR = new THREE.Mesh(standGeo, bodyMat);
  standR.position.set(0.7, 0.75, -2.0);
  group.add(standL, standR);
  const wing = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.1, 0.6), neonMat);
  wing.position.set(0, 1.05, -2.0);
  group.add(wing);

  const wheelGeo = new THREE.BoxGeometry(0.4, 0.4, 0.8);
  const wheelOffsets = [
    [-0.95, 0.25, 1.35],
    [0.95, 0.25, 1.35],
    [-0.95, 0.25, -1.35],
    [0.95, 0.25, -1.35],
  ];
  for (const [x, y, z] of wheelOffsets) {
    const wheel = new THREE.Mesh(wheelGeo, wheelMat);
    wheel.position.set(x, y, z);
    group.add(wheel);
  }

  return group;
}

// États de Le Spectre : HUNT (chasse directe), TAUNT (orbite provocatrice autour
// du joueur quand il est très près), RETREAT (recul après avoir été semé).
const STATE_HUNT   = 'HUNT';
const STATE_TAUNT  = 'TAUNT';

export class RivalSystem {
  constructor(scene, world) {
    this.scene = scene;
    this.world = world;
    this.active = false;
    this.mesh = null;
    this.speedKmh = 0;
    this.heading = 0;
    this._state = STATE_HUNT;
    this._orbitAngle = 0; // angle courant lors de l'orbite TAUNT
    this._orbitTimer = 0;
    this._score = 0;
    this._catchTimer = 0;
    this._tauntTimer = 0;
    this._challengeTimeLeft = 0;
    this._cooldown = SPAWN_COOLDOWN_MIN_S + Math.random() * (SPAWN_COOLDOWN_MAX_S - SPAWN_COOLDOWN_MIN_S);
    // Mémoire entre les rencontres : Le Spectre adapte son comportement.
    this._timesEscaped = 0; // nombre de fois que le joueur l'a semé
    this._timesCaught = 0;  // nombre de fois qu'il a rattrapé le joueur
  }

  getScore() {
    return this._score;
  }

  // Réplique contextuelle selon l'état émotionnel et la distance.
  _pickTaunt(dist) {
    let pool = TAUNTS_HUNT;
    if (this._timesEscaped > 0) pool = TAUNTS_ANGRY;
    if (dist < 12)              pool = TAUNTS_CLOSE;
    return pool[Math.floor(Math.random() * pool.length)];
  }

  update(dt, vehicle, hud) {
    if (!vehicle || typeof vehicle.getPosition !== 'function') return;
    const pos = vehicle.getPosition();

    if (!this.active) {
      this._cooldown -= dt;
      if (this._cooldown <= 0) {
        this._spawn(pos, hud);
      }
      return;
    }

    this._challengeTimeLeft -= dt;
    this._tauntTimer -= dt;

    const dx = pos.x - this.mesh.position.x;
    const dz = pos.z - this.mesh.position.z;
    const dist = Math.hypot(dx, dz);

    // --- Machine d'états --------------------------------------------------
    // TAUNT : Le Spectre est très proche — il orbite autour du joueur pour
    //         le narguer avant de reprendre la chasse.
    if (this._state === STATE_TAUNT) {
      this._orbitAngle += 1.8 * dt; // vitesse angulaire de l'orbite
      this._orbitTimer -= dt;

      const tx = pos.x + Math.sin(this._orbitAngle) * TAUNT_ORBIT_RADIUS;
      const tz = pos.z + Math.cos(this._orbitAngle) * TAUNT_ORBIT_RADIUS;
      const odx = tx - this.mesh.position.x;
      const odz = tz - this.mesh.position.z;
      const desiredH = Math.atan2(odx, odz);
      let diff = desiredH - this.heading;
      diff = Math.atan2(Math.sin(diff), Math.cos(diff));
      this.heading += clamp(diff, -TURN_RATE * 3 * dt, TURN_RATE * 3 * dt);
      this.mesh.rotation.y = this.heading;
      this.speedKmh = Math.min(TOP_SPEED_KMH * 0.25, this.speedKmh + ACCEL_KMH_PER_S * dt);
      const speedMs = (this.speedKmh / 3.6) * dt;
      this.mesh.position.x += Math.sin(this.heading) * speedMs;
      this.mesh.position.z += Math.cos(this.heading) * speedMs;

      if (this._orbitTimer <= 0) this._state = STATE_HUNT; // reprend la chasse
      if (this._tauntTimer <= 0 && hud) {
        hud.showMessage(this._pickTaunt(dist), 1800);
        this._tauntTimer = TAUNT_INTERVAL_MIN_S;
      }
      if (this._challengeTimeLeft <= 0) { this._escaped(hud); return; }
      return;
    }

    // --- HUNT : poursuite directe -----------------------------------------
    // Transition vers TAUNT si Le Spectre est très proche mais n'a pas encore
    // capturé le joueur — il orbite pour montrer qu'il contrôle la situation.
    if (dist < CATCH_RADIUS * 1.8 && dist > CATCH_RADIUS && this._state === STATE_HUNT) {
      this._state = STATE_TAUNT;
      this._orbitTimer = TAUNT_ORBIT_DURATION_S;
      this._orbitAngle = Math.atan2(this.mesh.position.x - pos.x, this.mesh.position.z - pos.z);
    }

    const closing = dist < 10;
    const desiredHeading = Math.atan2(dx, dz);
    let diff = desiredHeading - this.heading;
    diff = Math.atan2(Math.sin(diff), Math.cos(diff));
    const turnRate = closing ? TURN_RATE * 2.2 : TURN_RATE;
    const maxTurn = turnRate * dt;
    this.heading += clamp(diff, -maxTurn, maxTurn);
    this.mesh.rotation.y = this.heading;

    const targetSpeed = dist < 4 ? TOP_SPEED_KMH * 0.1 : closing ? TOP_SPEED_KMH * 0.35 : TOP_SPEED_KMH;
    const maxDelta = ACCEL_KMH_PER_S * dt;
    if (this.speedKmh < targetSpeed) {
      this.speedKmh = Math.min(targetSpeed, this.speedKmh + maxDelta);
    } else {
      this.speedKmh = Math.max(targetSpeed, this.speedKmh - maxDelta * 2);
    }

    const speedMs = (this.speedKmh / 3.6) * dt;
    this.mesh.position.x += Math.sin(this.heading) * speedMs;
    this.mesh.position.z += Math.cos(this.heading) * speedMs;

    if (dist < CATCH_RADIUS) {
      this._catchTimer += dt;
      if (this._catchTimer >= CATCH_HOLD_S) {
        this._caught(hud);
        return;
      }
    } else {
      this._catchTimer = 0;
    }

    if (this._tauntTimer <= 0 && hud) {
      hud.showMessage(this._pickTaunt(dist), 1800);
      this._tauntTimer = TAUNT_INTERVAL_MIN_S + Math.random() * (TAUNT_INTERVAL_MAX_S - TAUNT_INTERVAL_MIN_S);
    }

    if (this._challengeTimeLeft <= 0) {
      this._escaped(hud);
    }
  }

  _spawn(playerPos, hud) {
    const angle = Math.random() * Math.PI * 2;
    const dist = SPAWN_DIST_MIN + Math.random() * (SPAWN_DIST_MAX - SPAWN_DIST_MIN);
    const x = playerPos.x + Math.sin(angle) * dist;
    const z = playerPos.z + Math.cos(angle) * dist;
    this.heading = Math.atan2(playerPos.x - x, playerPos.z - z);
    this.speedKmh = 0;

    this.mesh = buildRivalMesh();
    this.mesh.position.set(x, 0, z);
    this.mesh.rotation.y = this.heading;
    this.scene.add(this.mesh);

    this.active = true;
    this._challengeTimeLeft = CHALLENGE_DURATION_S;
    this._catchTimer = 0;
    this._tauntTimer = 2;

    if (hud) {
      hud.showMessage(`LE SPECTRE apparaît : tenez ${CHALLENGE_DURATION_S}s sans qu'il vous rattrape !`, 3200);
    }
  }

  _despawn() {
    if (this.mesh) {
      this.scene.remove(this.mesh);
      this.mesh.traverse((obj) => {
        if (obj.geometry) obj.geometry.dispose();
        if (obj.material) obj.material.dispose();
      });
      this.mesh = null;
    }
    this.active = false;
    this._state = STATE_HUNT;
    // Plus Le Spectre a été semé, plus il revient vite (honte → rage).
    const angerReduction = Math.min(this._timesEscaped * REVENGE_COOLDOWN_REDUCTION, SPAWN_COOLDOWN_MIN_S - 8);
    this._cooldown = Math.max(8, SPAWN_COOLDOWN_MIN_S - angerReduction + Math.random() * (SPAWN_COOLDOWN_MAX_S - SPAWN_COOLDOWN_MIN_S) * 0.5);
  }

  _escaped(hud) {
    this._timesEscaped++;
    this._score += BONUS_ESCAPE;
    const msg = this._timesEscaped > 1
      ? `Le Spectre humilié x${this._timesEscaped} ! (+${BONUS_ESCAPE}) Il revient plus vite…`
      : `Vous avez semé LE SPECTRE ! (+${BONUS_ESCAPE})`;
    if (hud) hud.showMessage(msg, 2800);
    this._despawn();
  }

  _caught(hud) {
    this._timesCaught++;
    if (hud) hud.showMessage('LE SPECTRE vous a rattrapé… il reviendra.', 2800);
    this._despawn();
  }
}
