import * as THREE from 'three';
import { buildDetailedCharacter, CharacterAnimator } from './characters.js';

// TrafficSystem — vie ambiante de la ville : voitures de circulation qui
// roulent sur la grille de rues, et piétons qui errent sur les trottoirs.
// Pas de pathfinding réel : les voitures suivent une ligne de route (X ou Z
// constant) et choisissent une nouvelle direction (tout droit ou virage à
// angle droit) à chaque carrefour ; les piétons marchent en ligne à peu près
// droite et changent de direction au hasard s'ils sont sur le point de
// rentrer dans un bâtiment. Même esprit "IA simple" que police.js.

const CITY_HALF_SIZE = 100; // ville ~200x200 -> bords à ±100, cf. police.js
const ACTIVE_RADIUS = 120; // distance au joueur au-delà de laquelle on respawn ailleurs
const INTERSECTION_EPS = 0.6; // tolérance pour détecter qu'on est sur un carrefour

const TRAFFIC_CAR_COUNT = 8;
const PEDESTRIAN_COUNT = 12;

const CAR_SPEED_RANGE = [6, 11]; // m/s, ~22-40 km/h en ville
const LANE_OFFSET = 2.4; // décalage par rapport à la ligne centrale de la route (sens de circulation)
const CAR_FOLLOW_DIST = 14; // m — distance devant laquelle une voiture commence à ralentir pour le joueur

const PED_SPEED_RANGE = [0.8, 1.6]; // m/s, marche lente
const PED_TURN_RATE = 2.2; // rad/s, rotation plafonnée comme les voitures de police
const PED_RADIUS = 0.4; // rayon approximatif pour le test de collision avec les bâtiments
const PED_SIDEWALK_MARGIN = 1.0; // marge gardée par rapport au bord des bâtiments
const PED_SCATTER_RADIUS = 9; // m — en-dessous, le piéton prend peur et s'enfuit

// Cinq types de personnalité : chaque piéton se voit assigner l'un d'eux à
// sa création et conserve ces traits pour toute sa durée de vie, ce qui
// crée une foule visuellement variée dont chaque individu a un comportement
// reconnaissable.
const PERSONALITIES = [
  { name: 'TOURISTE',    speedMult: 0.65, turnMult: 1.0, panicMult: 1.2, pauseChance: 0.025 },
  { name: 'PRESSÉ',      speedMult: 1.6,  turnMult: 2.5, panicMult: 2.0, pauseChance: 0.003 },
  { name: 'JOGGEUR',     speedMult: 2.4,  turnMult: 1.8, panicMult: 1.4, pauseChance: 0.001 },
  { name: 'NERVEUX',     speedMult: 1.0,  turnMult: 3.5, panicMult: 3.5, pauseChance: 0.04  },
  { name: 'COSTAUD',     speedMult: 0.9,  turnMult: 0.7, panicMult: 0.6, pauseChance: 0.008 },
];

const carColors = [0x2255cc, 0xcc8822, 0x227744, 0x999999, 0xaa3344, 0x445566, 0xddcc55];

function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

function buildTrafficCarMesh(color) {
  const group = new THREE.Group();
  const bodyMat = new THREE.MeshStandardMaterial({ color, metalness: 0.2, roughness: 0.6 });
  const cabinMat = new THREE.MeshStandardMaterial({ color: 0x1a1d22, metalness: 0.1, roughness: 0.5 });

  const body = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.55, 4.0), bodyMat);
  body.position.y = 0.5;
  group.add(body);

  const cabin = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.5, 1.9), cabinMat);
  cabin.position.set(0, 0.95, -0.2);
  group.add(cabin);

  const wheelGeo = new THREE.BoxGeometry(0.35, 0.35, 0.7);
  const wheelMat = new THREE.MeshStandardMaterial({ color: 0x0a0a0a });
  const wheelOffsets = [
    [-0.9, 0.22, 1.25],
    [0.9, 0.22, 1.25],
    [-0.9, 0.22, -1.25],
    [0.9, 0.22, -1.25],
  ];
  for (const [x, y, z] of wheelOffsets) {
    const wheel = new THREE.Mesh(wheelGeo, wheelMat);
    wheel.position.set(x, y, z);
    group.add(wheel);
  }

  return group;
}


// Trouve la ligne de route la plus proche d'une coordonnée donnée, parmi une
// liste de lignes (roadLines.xs ou .zs).
function nearestLine(lines, value) {
  let best = lines[0];
  let bestDist = Infinity;
  for (const l of lines) {
    const d = Math.abs(l - value);
    if (d < bestDist) {
      bestDist = d;
      best = l;
    }
  }
  return best;
}

// ── PathClearanceAgent ────────────────────────────────────────────────────────
// Vérifie en temps réel qu'une entité a la voie libre avant d'avancer.
// Utilisé par TrafficCar (évitement voiture-à-voiture) et Pedestrian
// (évitement piéton-à-piéton). Un seul agent partagé par TrafficSystem.

export class PathClearanceAgent {
  constructor() {
    this._cars = [];
    this._peds = [];
  }

  // Appelé chaque frame par TrafficSystem avant les mises à jour individuelles
  register(cars, peds) {
    this._cars = cars;
    this._peds = peds;
  }

  // posX/posZ : position actuelle de l'entité
  // heading   : direction de déplacement en radians (0=+Z, π/2=+X)
  // lookDist  : distance de regard en mètres
  // self      : référence de l'entité (exclue du test)
  // laneHalf  : demi-largeur de couloir testé (mètres)
  // Retourne  : { clear, distance, type:'car'|'ped'|null }
  check(posX, posZ, heading, lookDist, self, laneHalf = 2.0) {
    const dirX = Math.sin(heading);
    const dirZ = Math.cos(heading);
    let minDist = Infinity;
    let hitType  = null;

    const scan = (pool, half, label) => {
      for (const e of pool) {
        if (e === self || !e.active || !e.mesh) continue;
        const dx = e.mesh.position.x - posX;
        const dz = e.mesh.position.z - posZ;
        const fwd = dx * dirX + dz * dirZ;          // composante avant
        if (fwd < 0.5 || fwd > lookDist) continue;
        const lat = Math.abs(dx * dirZ - dz * dirX); // composante latérale
        if (lat > half) continue;
        if (fwd < minDist) { minDist = fwd; hitType = label; }
      }
    };

    scan(this._cars, laneHalf, 'car');
    scan(this._peds, laneHalf * 0.45, 'ped');

    return { clear: hitType === null, distance: minDist, type: hitType };
  }
}

// ── IntegrityAgent ────────────────────────────────────────────────────────────
// Détecte et répare automatiquement les états pathologiques :
//   • entités hors limites  → marque pour respawn
//   • entités coincées dans un bâtiment → éjecte vers l'extérieur
//   • voitures bloquées trop longtemps (speed≈0) → respawn
// Rend le système auto-correct sans intervention manuelle.

export class IntegrityAgent {
  constructor() {
    this._stuckFrames = new WeakMap(); // TrafficCar → nb de frames à speed≈0
  }

  // Retourne le nombre de corrections appliquées ce frame.
  repair(cars, peds, colliders) {
    let fixes = 0;

    // Voitures : hors-limites, coincées dans bâtiment, bloquées
    for (const car of cars) {
      if (!car.active || !car.mesh) continue;
      const p = car.mesh.position;

      if (Math.abs(p.x) > CITY_HALF_SIZE + 8 || Math.abs(p.z) > CITY_HALF_SIZE + 8) {
        car.active = false; // déclenchera respawnNear au prochain _syncEntities
        this._stuckFrames.set(car, 0);
        fixes++;
        continue;
      }

      if (colliders && this._insideAny(p.x, p.z, colliders)) {
        // Éjecte vers le centre : direction opposée à la position
        p.x += p.x > 0 ? -3 : 3;
        p.z += p.z > 0 ? -3 : 3;
        car.speed = 0;
        fixes++;
      }

      // Détection blocage prolongé (voiture coincée contre un mur)
      const cnt = this._stuckFrames.get(car) || 0;
      if (typeof car.speed === 'number' && Math.abs(car.speed) < 0.2) {
        const newCnt = cnt + 1;
        this._stuckFrames.set(car, newCnt);
        if (newCnt >= 120) { // ~2 s à 60 fps
          car.active = false;
          this._stuckFrames.set(car, 0);
          fixes++;
        }
      } else {
        this._stuckFrames.set(car, 0);
      }
    }

    // Piétons : hors-limites seulement (les piétons gèrent leur propre évitement)
    for (const ped of peds) {
      if (!ped.active || !ped.mesh) continue;
      const p = ped.mesh.position;
      if (Math.abs(p.x) > CITY_HALF_SIZE + 5 || Math.abs(p.z) > CITY_HALF_SIZE + 5) {
        ped.active = false;
        fixes++;
      }
    }

    return fixes;
  }

  _insideAny(x, z, colliders) {
    for (const c of colliders) {
      if (Math.abs(x - c.x) < c.halfWidth && Math.abs(z - c.z) < c.halfDepth) return true;
    }
    return false;
  }
}

class TrafficCar {
  constructor(scene, roadLines) {
    this.roadLines = roadLines;
    this.mesh = buildTrafficCarMesh(carColors[Math.floor(Math.random() * carColors.length)]);
    scene.add(this.mesh);
    this.speed = CAR_SPEED_RANGE[0] + Math.random() * (CAR_SPEED_RANGE[1] - CAR_SPEED_RANGE[0]);
    this.active = false;

    // AI Drives — independent needs that create emergent behaviour
    // urgency : 0=calm  1=late/stressed → drives faster, less gap
    // caution : 0=bold  1=nervous      → slows near police, brakes earlier
    this._urgency    = Math.random();
    this._caution    = Math.random() * 0.25;
    this._urgencyVel = (Math.random() - 0.5) * 0.004; // Wiener drift direction
  }

  // (Ré)apparaît sur une ligne de route au hasard, à bonne distance du
  // joueur, en partant d'un carrefour pour rester cohérent avec la grille.
  respawnNear(playerPos) {
    const { xs, zs } = this.roadLines;
    const axis = Math.random() < 0.5 ? 'x' : 'z';
    this.axis = axis; // 'x' => la voiture roule le long de X, sur une ligne Z fixe

    if (axis === 'x') {
      this.fixedCoord = zs[Math.floor(Math.random() * zs.length)];
      // Position de départ : carrefour le plus proche d'un point aléatoire
      // autour du joueur, décalé d'une "voie" pour ne pas rouler au centre.
      const around = playerPos.x + (Math.random() * 2 - 1) * ACTIVE_RADIUS * 0.6;
      this.moving = nearestLine(xs, around);
      this.dir = Math.random() < 0.5 ? 1 : -1;
      this.mesh.position.set(this.moving, 0, this.fixedCoord + this.dir * LANE_OFFSET);
      this.mesh.rotation.y = this.dir > 0 ? Math.PI / 2 : -Math.PI / 2;
    } else {
      this.fixedCoord = xs[Math.floor(Math.random() * xs.length)];
      const around = playerPos.z + (Math.random() * 2 - 1) * ACTIVE_RADIUS * 0.6;
      this.moving = nearestLine(zs, around);
      this.dir = Math.random() < 0.5 ? 1 : -1;
      this.mesh.position.set(this.fixedCoord + this.dir * -LANE_OFFSET, 0, this.moving);
      this.mesh.rotation.y = this.dir > 0 ? 0 : Math.PI;
    }
    this.active = true;
  }

  _applyPosition() {
    if (this.axis === 'x') {
      this.mesh.position.x = this.moving;
      this.mesh.position.z = this.fixedCoord + this.dir * LANE_OFFSET;
      this.mesh.rotation.y = this.dir > 0 ? Math.PI / 2 : -Math.PI / 2;
    } else {
      this.mesh.position.x = this.fixedCoord + this.dir * -LANE_OFFSET;
      this.mesh.position.z = this.moving;
      this.mesh.rotation.y = this.dir > 0 ? 0 : Math.PI;
    }
  }

  // Evolve urgency/caution drives. Called every frame the car is updated.
  // wantedLevel 0-5 raises caution toward police presence.
  _updateDrives(dt, wantedLevel) {
    // Urgency does a bounded random walk (Wiener process with reflection)
    this._urgency = clamp(
      this._urgency + this._urgencyVel + (Math.random() - 0.5) * 0.003,
      0, 1
    );
    // Gently reverse direction when near extremes so it doesn't rail
    if (this._urgency > 0.9 || this._urgency < 0.1) this._urgencyVel *= -1;

    // Caution ramps up toward wantedLevel / 5 with inertia
    const targetCaution = (wantedLevel / 5) * 0.9;
    this._caution += (targetCaution - this._caution) * Math.min(1, dt * 0.5);
    this._caution = clamp(this._caution, 0, 1);
  }

  // Heading en radians depuis axis/dir (convention Vehicle : 0=+Z, π/2=+X)
  _getHeading() {
    if (this.axis === 'x') return this.dir > 0 ? Math.PI / 2 : -Math.PI / 2;
    return this.dir > 0 ? 0 : Math.PI;
  }

  // playerPos : {x, z} optionnel — ralentit si le joueur est devant.
  // pathAgent : PathClearanceAgent — ralentit/stoppe si un autre véhicule/piéton bloque.
  update(dt, playerPos = null, wantedLevel = 0, pathAgent = null) {
    if (!this.active) return;
    const { xs, zs } = this.roadLines;
    const crossLines = this.axis === 'x' ? zs : xs;

    this._updateDrives(dt, wantedLevel);

    // Drives multiplier: urgency pushes speed up, caution pulls it down.
    // Net range: ~0.63× (calm+nervous near police) to ~1.45× (stressed+bold)
    const driveMult = (1 + this._urgency * 0.45) * (1 - this._caution * 0.38);

    let effectiveSpeed = this.speed * driveMult;

    // ── Freinage joueur devant ──────────────────────────────────────────
    if (playerPos) {
      const movingPlayer = this.axis === 'x' ? playerPos.x : playerPos.z;
      const fixedPlayer  = this.axis === 'x' ? playerPos.z : playerPos.x;
      const fixedDist = Math.abs(fixedPlayer - this.fixedCoord);
      const aheadDist = (movingPlayer - this.moving) * this.dir;
      const followDist = CAR_FOLLOW_DIST * (1 + this._caution * 0.6);
      if (fixedDist < 3.5 && aheadDist > 0 && aheadDist < followDist) {
        effectiveSpeed *= clamp(aheadDist / followDist, 0.15, 1);
      }
    }

    // ── PathClearanceAgent : évitement voiture-à-voiture et piétons ───
    if (pathAgent) {
      const { clear, distance } = pathAgent.check(
        this.mesh.position.x, this.mesh.position.z,
        this._getHeading(), CAR_FOLLOW_DIST * 1.3, this, 2.2
      );
      if (!clear) {
        const stopZone = 3.5; // distance d'arrêt complet (m)
        effectiveSpeed = distance <= stopZone
          ? 0
          : effectiveSpeed * clamp((distance - stopZone) / (CAR_FOLLOW_DIST - stopZone), 0.05, 1);
      }
    }

    this.moving += this.dir * effectiveSpeed * dt;

    // Carrefour le plus proche sur la ligne perpendiculaire : si on vient de
    // le franchir, on choisit (au hasard) de continuer tout droit ou de
    // tourner à angle droit sur cette nouvelle ligne.
    const crossing = nearestLine(crossLines, this.moving);
    if (Math.abs(this.moving - crossing) < INTERSECTION_EPS && !this._justTurnedAt) {
      this._justTurnedAt = crossing;
      if (Math.random() < 0.35) {
        // Virage à angle droit : on échange les rôles des deux axes. La
        // coordonnée perpendiculaire (carrefour) devient la nouvelle ligne
        // fixe, et l'ancienne ligne fixe devient le nouveau point de départ
        // sur l'axe de déplacement.
        const newMoving = this.fixedCoord;
        this.axis = this.axis === 'x' ? 'z' : 'x';
        this.fixedCoord = crossing;
        this.moving = newMoving;
        this.dir = Math.random() < 0.5 ? 1 : -1;
      }
    } else if (Math.abs(this.moving - crossing) > INTERSECTION_EPS * 3) {
      this._justTurnedAt = null;
    }

    this._applyPosition();
  }

  dispose(scene) {
    scene.remove(this.mesh);
    this.mesh.traverse((obj) => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) obj.material.dispose();
    });
  }
}

class Pedestrian {
  constructor(scene) {
    this.mesh = buildDetailedCharacter();
    scene.add(this.mesh);
    this.personality = PERSONALITIES[Math.floor(Math.random() * PERSONALITIES.length)];
    this.speed = (PED_SPEED_RANGE[0] + Math.random() * (PED_SPEED_RANGE[1] - PED_SPEED_RANGE[0])) * this.personality.speedMult;
    this.heading = Math.random() * Math.PI * 2;
    this.active = false;
    this._pauseTimer = 0; // > 0 : le piéton est à l'arrêt momentanément
    this._panicking = false;
  }

  respawnNear(playerPos, colliders) {
    // Essaie quelques positions aléatoires autour du joueur jusqu'à en
    // trouver une qui n'est pas à l'intérieur d'un bâtiment.
    for (let attempt = 0; attempt < 12; attempt++) {
      const angle = Math.random() * Math.PI * 2;
      const dist = 5 + Math.random() * ACTIVE_RADIUS * 0.7;
      let x = playerPos.x + Math.sin(angle) * dist;
      let z = playerPos.z + Math.cos(angle) * dist;
      x = clamp(x, -CITY_HALF_SIZE + 3, CITY_HALF_SIZE - 3);
      z = clamp(z, -CITY_HALF_SIZE + 3, CITY_HALF_SIZE - 3);

      if (!this._collides(x, z, colliders)) {
        this.mesh.position.set(x, 0, z);
        this.heading = Math.random() * Math.PI * 2;
        this.mesh.rotation.y = this.heading;
        this.active = true;
        return;
      }
    }
    // Pas trouvé de point libre : reste inactif pour ce cycle, on retentera
    // au prochain appel de _syncEntities.
  }

  _collides(x, z, colliders) {
    if (!colliders) return false;
    for (const c of colliders) {
      const halfW = c.halfWidth + PED_SIDEWALK_MARGIN;
      const halfD = c.halfDepth + PED_SIDEWALK_MARGIN;
      if (Math.abs(x - c.x) < halfW && Math.abs(z - c.z) < halfD) {
        return true;
      }
    }
    return false;
  }

  // playerPos : {x, z} optionnel — réaction à la proximité du joueur.
  // pathAgent : PathClearanceAgent — contournement des autres piétons/voitures.
  update(dt, colliders, playerPos = null, pathAgent = null) {
    if (!this.active) return;
    const p = this.personality;

    // --- Réaction au joueur : fuite si trop proche --------------------
    if (playerPos) {
      const pdx = this.mesh.position.x - playerPos.x;
      const pdz = this.mesh.position.z - playerPos.z;
      const distToPlayer = Math.hypot(pdx, pdz);
      if (distToPlayer < PED_SCATTER_RADIUS) {
        this._panicking = true;
        this._pauseTimer = 0;
        const awayAngle = Math.atan2(pdx, pdz);
        let diff = awayAngle - this.heading;
        diff = Math.atan2(Math.sin(diff), Math.cos(diff));
        const maxTurn = PED_TURN_RATE * p.turnMult * dt * 6;
        this.heading += clamp(diff, -maxTurn, maxTurn);
        this.mesh.rotation.y = this.heading;
        const panicSpeed = this.speed * p.panicMult;
        const nx = this.mesh.position.x + Math.sin(this.heading) * panicSpeed * dt;
        const nz = this.mesh.position.z + Math.cos(this.heading) * panicSpeed * dt;
        if (!this._collides(nx, nz, colliders) && Math.abs(nx) < CITY_HALF_SIZE - 2 && Math.abs(nz) < CITY_HALF_SIZE - 2) {
          this.mesh.position.x = nx;
          this.mesh.position.z = nz;
        }
        CharacterAnimator.update(this.mesh, panicSpeed, dt);
        return;
      }
    }
    this._panicking = false;

    // --- Pause aléatoire (personnalité : le touriste s'arrête souvent) --
    if (this._pauseTimer > 0) {
      this._pauseTimer -= dt;
      CharacterAnimator.update(this.mesh, 0, dt);
      return;
    }
    if (Math.random() < p.pauseChance) {
      this._pauseTimer = 0.8 + Math.random() * 1.5;
      CharacterAnimator.update(this.mesh, 0, dt);
      return;
    }

    const dirX = Math.sin(this.heading);
    const dirZ = Math.cos(this.heading);
    const nextX = this.mesh.position.x + dirX * this.speed * dt;
    const nextZ = this.mesh.position.z + dirZ * this.speed * dt;

    const blocked =
      this._collides(nextX, nextZ, colliders) ||
      Math.abs(nextX) > CITY_HALF_SIZE - 2 ||
      Math.abs(nextZ) > CITY_HALF_SIZE - 2;

    if (blocked) {
      const targetHeading = Math.random() * Math.PI * 2;
      let diff = targetHeading - this.heading;
      diff = Math.atan2(Math.sin(diff), Math.cos(diff));
      const maxTurn = PED_TURN_RATE * p.turnMult * dt * 8;
      this.heading += clamp(diff, -maxTurn, maxTurn);
      this.mesh.rotation.y = this.heading;
      CharacterAnimator.update(this.mesh, 0, dt);
      return;
    }

    // Dérive aléatoire selon la personnalité
    if (Math.random() < 0.01 * p.turnMult) {
      this._wanderTarget = this.heading + (Math.random() * 2 - 1) * 1.2;
    }
    if (this._wanderTarget !== undefined) {
      let diff = this._wanderTarget - this.heading;
      diff = Math.atan2(Math.sin(diff), Math.cos(diff));
      const maxTurn = PED_TURN_RATE * p.turnMult * dt;
      this.heading += clamp(diff, -maxTurn, maxTurn);
    }

    // ── PathClearanceAgent : évitement piéton-à-piéton ────────────────
    if (pathAgent) {
      const { clear, distance } = pathAgent.check(
        this.mesh.position.x, this.mesh.position.z,
        this.heading, 2.0, this, 0.65
      );
      if (!clear && distance < 1.3) {
        // Dévie légèrement sur le côté pour contourner
        this.heading += (Math.random() < 0.5 ? 1 : -1) * 0.9;
        this.mesh.rotation.y = this.heading;
        CharacterAnimator.update(this.mesh, 0, dt);
        return;
      }
    }

    this.mesh.position.x = nextX;
    this.mesh.position.z = nextZ;
    this.mesh.rotation.y = this.heading;
    CharacterAnimator.update(this.mesh, this.speed, dt);
  }

  dispose(scene) {
    scene.remove(this.mesh);
    this.mesh.traverse((obj) => {
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) obj.material.dispose();
    });
  }
}

export class TrafficSystem {
  constructor(scene, world) {
    this.scene = scene;
    this.world = world;
    this.colliders = (world && world.colliders) || [];
    this.roadLines = (world && world.roadLines) || this._fallbackRoadLines();

    this.cars = [];
    for (let i = 0; i < TRAFFIC_CAR_COUNT; i++) {
      this.cars.push(new TrafficCar(scene, this.roadLines));
    }

    this.pedestrians = [];
    for (let i = 0; i < PEDESTRIAN_COUNT; i++) {
      this.pedestrians.push(new Pedestrian(scene));
    }

    // Agents autonomes de surveillance
    this._pathAgent      = new PathClearanceAgent();
    this._integrityAgent = new IntegrityAgent();
  }

  _fallbackRoadLines() {
    const CITY_SIZE = 5;
    const BLOCK_SIZE = 28;
    const ROAD_WIDTH = 10;
    const CELL = BLOCK_SIZE + ROAD_WIDTH;
    const HALF_CITY = (CITY_SIZE * CELL) / 2;
    const lines = [];
    for (let i = 0; i <= CITY_SIZE; i++) lines.push(-HALF_CITY + CELL * i);
    return { xs: lines.slice(), zs: lines.slice() };
  }

  // wantedLevel : niveau police 0-5, feed aux AI drives.
  // lod         : LODManager — les entités distantes mettent à jour moins souvent.
  update(dt, playerPos, wantedLevel = 0, lod = null) {
    if (!playerPos) return;
    this._syncEntities(playerPos);

    // IntegrityAgent : répare les états pathologiques AVANT la mise à jour
    this._integrityAgent.repair(this.cars, this.pedestrians, this.colliders);

    // PathClearanceAgent : enregistre les entités actives pour ce frame
    this._pathAgent.register(this.cars, this.pedestrians);

    for (let i = 0; i < this.cars.length; i++) {
      const car = this.cars[i];
      if (!car.active) continue;
      if (lod) {
        const dist = this._distTo(car.mesh.position, playerPos);
        if (!lod.shouldUpdate(dist, i)) continue;
      }
      car.update(dt, playerPos, wantedLevel, this._pathAgent);
    }
    for (let i = 0; i < this.pedestrians.length; i++) {
      const ped = this.pedestrians[i];
      if (!ped.active) continue;
      if (lod) {
        const dist = this._distTo(ped.mesh.position, playerPos);
        if (!lod.shouldUpdate(dist, i + this.cars.length)) continue;
      }
      ped.update(dt, this.colliders, playerPos, this._pathAgent);
    }
  }

  // Despawn/respawn des entités trop loin du joueur, pour garder un nombre
  // d'objets actifs constant sans simuler toute la ville (cf. police.js qui
  // fait apparaître ses voitures près du joueur plutôt que partout).
  _syncEntities(playerPos) {
    for (const car of this.cars) {
      if (!car.active || this._distTo(car.mesh.position, playerPos) > ACTIVE_RADIUS) {
        car.respawnNear(playerPos);
      }
    }
    for (const ped of this.pedestrians) {
      if (!ped.active || this._distTo(ped.mesh.position, playerPos) > ACTIVE_RADIUS) {
        ped.respawnNear(playerPos, this.colliders);
      }
    }
  }

  _distTo(meshPos, playerPos) {
    const dx = meshPos.x - playerPos.x;
    const dz = meshPos.z - playerPos.z;
    return Math.hypot(dx, dz);
  }

  getCarPositions() {
    return this.cars.filter((c) => c.active).map((c) => ({ x: c.mesh.position.x, z: c.mesh.position.z }));
  }

  // AABBs for active traffic cars and pedestrians, in the same {x, z,
  // halfWidth, halfDepth} shape as world.colliders, so the player vehicle's
  // existing building-collision code can also treat traffic as solid instead
  // of letting the player drive straight through it. Traffic cars only ever
  // face along X or Z (see TrafficCar), so an axis-aligned box is exact.
  getColliders() {
    const list = [];
    for (const car of this.cars) {
      if (!car.active) continue;
      const halfLength = 2.0; // half of the 4.0m car mesh length
      const halfWidthM = 0.9; // half of the 1.8m car mesh width
      if (car.axis === 'x') {
        list.push({ x: car.mesh.position.x, z: car.mesh.position.z, halfWidth: halfLength, halfDepth: halfWidthM });
      } else {
        list.push({ x: car.mesh.position.x, z: car.mesh.position.z, halfWidth: halfWidthM, halfDepth: halfLength });
      }
    }
    for (const ped of this.pedestrians) {
      if (!ped.active) continue;
      list.push({ x: ped.mesh.position.x, z: ped.mesh.position.z, halfWidth: PED_RADIUS, halfDepth: PED_RADIUS });
    }
    return list;
  }

  dispose() {
    for (const car of this.cars) car.dispose(this.scene);
    for (const ped of this.pedestrians) ped.dispose(this.scene);
    this.cars = [];
    this.pedestrians = [];
  }
}
