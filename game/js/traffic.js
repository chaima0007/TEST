import * as THREE from 'three';

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

function buildPedestrianMesh() {
  const group = new THREE.Group();
  const shirtColors = [0xcc4444, 0x4477cc, 0x44aa66, 0xccaa33, 0x9955cc, 0x777777];
  const skinColors = [0xe0b08a, 0xc68a5e, 0x8d5a3c, 0xf0c9a0];

  const bodyMat = new THREE.MeshStandardMaterial({
    color: shirtColors[Math.floor(Math.random() * shirtColors.length)],
    roughness: 0.8,
  });
  const headMat = new THREE.MeshStandardMaterial({
    color: skinColors[Math.floor(Math.random() * skinColors.length)],
    roughness: 0.8,
  });

  const body = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.9, 0.28), bodyMat);
  body.position.y = 0.65;
  group.add(body);

  const head = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.32, 0.32), headMat);
  head.position.y = 1.28;
  group.add(head);

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

class TrafficCar {
  constructor(scene, roadLines) {
    this.roadLines = roadLines;
    this.mesh = buildTrafficCarMesh(carColors[Math.floor(Math.random() * carColors.length)]);
    scene.add(this.mesh);
    this.speed = CAR_SPEED_RANGE[0] + Math.random() * (CAR_SPEED_RANGE[1] - CAR_SPEED_RANGE[0]);
    this.active = false;
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

  // playerPos: {x, z} optionnel — si fourni, la voiture ralentit si le joueur
  // est juste devant elle dans son sens de marche (comportement de suivi).
  update(dt, playerPos = null) {
    if (!this.active) return;
    const { xs, zs } = this.roadLines;
    const crossLines = this.axis === 'x' ? zs : xs;

    let effectiveSpeed = this.speed;
    if (playerPos) {
      // Distance et position relative du joueur sur l'axe de déplacement.
      const movingPlayer = this.axis === 'x' ? playerPos.x : playerPos.z;
      const fixedPlayer  = this.axis === 'x' ? playerPos.z : playerPos.x;
      const fixedDist = Math.abs(fixedPlayer - this.fixedCoord);
      const aheadDist = (movingPlayer - this.moving) * this.dir;
      if (fixedDist < 3.5 && aheadDist > 0 && aheadDist < CAR_FOLLOW_DIST) {
        // Joueur devant dans la même voie : vitesse progressivement réduite.
        effectiveSpeed *= clamp(aheadDist / CAR_FOLLOW_DIST, 0.15, 1);
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
    this.mesh = buildPedestrianMesh();
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

  // playerPos: {x, z} optionnel — si fourni, le piéton réagit à la proximité
  // du véhicule du joueur selon sa personnalité.
  update(dt, colliders, playerPos = null) {
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
        // Tourner dos au véhicule
        const awayAngle = Math.atan2(pdx, pdz);
        let diff = awayAngle - this.heading;
        diff = Math.atan2(Math.sin(diff), Math.cos(diff));
        const maxTurn = PED_TURN_RATE * p.turnMult * dt * 6;
        this.heading += clamp(diff, -maxTurn, maxTurn);
        this.mesh.rotation.y = this.heading;
        // Sprint
        const panicSpeed = this.speed * p.panicMult;
        const nx = this.mesh.position.x + Math.sin(this.heading) * panicSpeed * dt;
        const nz = this.mesh.position.z + Math.cos(this.heading) * panicSpeed * dt;
        if (!this._collides(nx, nz, colliders) && Math.abs(nx) < CITY_HALF_SIZE - 2 && Math.abs(nz) < CITY_HALF_SIZE - 2) {
          this.mesh.position.x = nx;
          this.mesh.position.z = nz;
        }
        return;
      }
    }
    this._panicking = false;

    // --- Pause aléatoire (personnalité : le touriste s'arrête souvent) --
    if (this._pauseTimer > 0) {
      this._pauseTimer -= dt;
      return;
    }
    if (Math.random() < p.pauseChance) {
      this._pauseTimer = 0.8 + Math.random() * 1.5;
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
      return;
    }

    // Dérive aléatoire selon la personnalité (le nerveux change souvent de direction)
    if (Math.random() < 0.01 * p.turnMult) {
      this._wanderTarget = this.heading + (Math.random() * 2 - 1) * 1.2;
    }
    if (this._wanderTarget !== undefined) {
      let diff = this._wanderTarget - this.heading;
      diff = Math.atan2(Math.sin(diff), Math.cos(diff));
      const maxTurn = PED_TURN_RATE * p.turnMult * dt;
      this.heading += clamp(diff, -maxTurn, maxTurn);
    }

    this.mesh.position.x = nextX;
    this.mesh.position.z = nextZ;
    this.mesh.rotation.y = this.heading;
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
    // Repli si roadLines absent (ancienne version de world.js) : reconstruit
    // la même grille que celle utilisée pour générer les routes.
    this.roadLines = (world && world.roadLines) || this._fallbackRoadLines();

    this.cars = [];
    for (let i = 0; i < TRAFFIC_CAR_COUNT; i++) {
      this.cars.push(new TrafficCar(scene, this.roadLines));
    }

    this.pedestrians = [];
    for (let i = 0; i < PEDESTRIAN_COUNT; i++) {
      this.pedestrians.push(new Pedestrian(scene));
    }
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

  update(dt, playerPos) {
    if (!playerPos) return;
    this._syncEntities(playerPos);

    for (const car of this.cars) car.update(dt, playerPos);
    for (const ped of this.pedestrians) ped.update(dt, this.colliders, playerPos);
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
