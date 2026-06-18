import * as THREE from 'three';
import { StreetFurnitureSystem } from './streetfurniture.js';

// Ville en grille : un sol clair (trottoirs/blocs) recouvert d'une croix de
// routes sombres avec marquages, et des immeubles (boîtes) posés sur les
// blocs entre les routes. Tout est généré ici, aucune dépendance externe.
//
// Disposition : la zone couvre ~200x200 unités, centrée sur (0,0).
// On découpe l'espace en CITY_SIZE x CITY_SIZE blocs ; chaque bloc a une
// largeur BLOCK_SIZE et est séparé de ses voisins par une route de largeur
// ROAD_WIDTH. Les bâtiments sont placés à l'intérieur de chaque bloc, avec
// une marge par rapport aux routes pour ne jamais déborder dessus.

const CITY_SIZE = 5; // blocs par côté (5x5 = 25 blocs)
const BLOCK_SIZE = 28; // taille d'un bloc (zone bâtissable) en unités
const ROAD_WIDTH = 10; // largeur des routes entre les blocs
const CELL = BLOCK_SIZE + ROAD_WIDTH; // pas de la grille
const HALF_CITY = (CITY_SIZE * CELL) / 2; // ~190/2, proche de 100 -> aire ~200x200

function blockCenter(i) {
  // centre du bloc d'indice i (0..CITY_SIZE-1) sur un axe, en coordonnées monde.
  // Les routes ont leurs lignes centrales à -HALF_CITY + CELL*k (k=0..CITY_SIZE) ;
  // un bloc occupe l'espace entre deux routes consécutives, donc son centre
  // est au milieu de cet intervalle.
  return -HALF_CITY + CELL * i + CELL / 2;
}

export function createWorld(scene) {
  const colliders = [];
  const missionLocations = [];

  // --- Sol (trottoirs / terrain de base) ---------------------------------
  const groundSize = CITY_SIZE * CELL + ROAD_WIDTH;
  const groundGeo = new THREE.PlaneGeometry(groundSize, groundSize);
  const groundMat = new THREE.MeshLambertMaterial({ color: 0xb9b6ad });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  ground.position.set(0, 0, 0);
  ground.receiveShadow = true;
  scene.add(ground);

  // --- Routes (croix de bandes sombres sur toute la grille) --------------
  const roadMat = new THREE.MeshLambertMaterial({ color: 0x2b2b2f });
  const roadLength = CITY_SIZE * CELL + ROAD_WIDTH;

  // Géométries de routes réutilisées (une orientation horizontale, une verticale)
  const roadGeoH = new THREE.PlaneGeometry(roadLength, ROAD_WIDTH); // le long de X
  const roadGeoV = new THREE.PlaneGeometry(ROAD_WIDTH, roadLength); // le long de Z

  // Lignes de routes horizontales (constant en Z) et verticales (constant en X),
  // une par "rue" entre/autour des blocs : CITY_SIZE + 1 rues par direction.
  const roadZs = [];
  const roadXs = [];
  for (let i = 0; i <= CITY_SIZE; i++) {
    const c = -HALF_CITY + CELL * i;
    roadZs.push(c);
    roadXs.push(c);
  }

  for (const z of roadZs) {
    const road = new THREE.Mesh(roadGeoH, roadMat);
    road.rotation.x = -Math.PI / 2;
    road.position.set(0, 0.01, z);
    scene.add(road);
  }
  for (const x of roadXs) {
    const road = new THREE.Mesh(roadGeoV, roadMat);
    road.rotation.x = -Math.PI / 2;
    road.position.set(x, 0.01, 0);
    scene.add(road);
  }

  // --- Marquages au sol (bandes claires au centre des routes) ------------
  const laneMat = new THREE.MeshBasicMaterial({ color: 0xe8d97a });
  const laneSegLen = 4;
  const laneGap = 4;
  const laneWidth = 0.4;
  const laneGeo = new THREE.PlaneGeometry(laneSegLen, laneWidth);

  for (const z of roadZs) {
    for (let x = -HALF_CITY; x <= HALF_CITY; x += laneSegLen + laneGap) {
      const seg = new THREE.Mesh(laneGeo, laneMat);
      seg.rotation.x = -Math.PI / 2;
      seg.position.set(x, 0.02, z);
      scene.add(seg);
    }
  }
  const laneGeoV = new THREE.PlaneGeometry(laneWidth, laneSegLen);
  for (const x of roadXs) {
    for (let z = -HALF_CITY; z <= HALF_CITY; z += laneSegLen + laneGap) {
      const seg = new THREE.Mesh(laneGeoV, laneMat);
      seg.rotation.x = -Math.PI / 2;
      seg.position.set(x, 0.02, z);
      scene.add(seg);
    }
  }

  // --- Bâtiments -----------------------------------------------------------
  // Géométrie de boîte unitaire réutilisée pour tous les bâtiments (on la
  // redimensionne via scale), seules les couleurs/matériaux varient un peu.
  const buildingGeo = new THREE.BoxGeometry(1, 1, 1);
  const palette = [
    0xb0b8c4, 0x9aa6b2, 0xc9b896, 0xa8a39a, 0x8e9b8f,
    0xb98b6e, 0x7e8fa0, 0xc2a98f, 0x96a3ab, 0xab9b8a,
  ];
  const buildingMats = palette.map((c) => new THREE.MeshLambertMaterial({ color: c }));

  const margin = 3; // marge entre bâtiments et bord du bloc / route
  let buildingCount = 0;
  const targetMaxBuildings = 90;

  // Ligne de blocs utilisée pour positionner le spawn (rue calme, loin des bords)
  const spawnBlockJ = Math.floor(CITY_SIZE / 2);

  for (let i = 0; i < CITY_SIZE; i++) {
    for (let j = 0; j < CITY_SIZE; j++) {
      if (buildingCount >= targetMaxBuildings) break;

      const cx = blockCenter(i);
      const cz = blockCenter(j);

      // Le bloc central de la grille reste dégagé : on y place une petite
      // place avec des points de mission plutôt que des immeubles, pour
      // garantir des endroits "atteignables, pas dans un bâtiment".
      const isPlazaBlock = i === Math.floor(CITY_SIZE / 2) && j === Math.floor(CITY_SIZE / 2);

      if (isPlazaBlock) {
        missionLocations.push({ name: 'Place centrale', x: cx, z: cz });
        continue;
      }

      // Découpe chaque bloc en une mini-grille 2x2 de parcelles pour
      // accueillir plusieurs immeubles par bloc, avec une marge interne.
      const sub = 2;
      const usable = BLOCK_SIZE - margin * 2;
      const lotSize = usable / sub;

      for (let a = 0; a < sub; a++) {
        for (let b = 0; b < sub; b++) {
          if (buildingCount >= targetMaxBuildings) break;
          // Sauter aléatoirement quelques parcelles pour casser la régularité
          // et laisser des petits vides (parkings/terrains) entre bâtiments.
          const skip = Math.random() < 0.12;
          if (skip) continue;

          const lotCx = cx - usable / 2 + lotSize * a + lotSize / 2;
          const lotCz = cz - usable / 2 + lotSize * b + lotSize / 2;

          const w = lotSize * (0.55 + Math.random() * 0.35);
          const d = lotSize * (0.55 + Math.random() * 0.35);
          const h = 4 + Math.random() * 22;

          const mat = buildingMats[Math.floor(Math.random() * buildingMats.length)];
          const mesh = new THREE.Mesh(buildingGeo, mat);
          mesh.scale.set(w, h, d);
          mesh.position.set(lotCx, h / 2, lotCz);
          mesh.castShadow = true;
          mesh.receiveShadow = true;
          scene.add(mesh);

          colliders.push({
            x: lotCx,
            z: lotCz,
            halfWidth: w / 2,
            halfDepth: d / 2,
          });

          buildingCount++;
        }
      }
    }
  }

  // --- Lampadaires (petits accents environnementaux) ----------------------
  const poleGeo = new THREE.BoxGeometry(0.25, 5, 0.25);
  const poleMat = new THREE.MeshLambertMaterial({ color: 0x33363b });
  const lampGeo = new THREE.BoxGeometry(0.6, 0.3, 0.6);
  // MeshStandardMaterial pour activer l'emissive la nuit
  const streetLamps = [];

  for (let i = 0; i <= CITY_SIZE; i++) {
    for (let j = 0; j <= CITY_SIZE; j++) {
      if ((i + j) % 2 !== 0) continue;
      const x = -HALF_CITY + CELL * i + ROAD_WIDTH / 2 + 0.8;
      const z = -HALF_CITY + CELL * j + ROAD_WIDTH / 2 + 0.8;

      const pole = new THREE.Mesh(poleGeo, poleMat);
      pole.position.set(x, 2.5, z);
      scene.add(pole);

      const lampMat = new THREE.MeshStandardMaterial({ color: 0xfff3c4, emissive: 0xffee99, emissiveIntensity: 0 });
      const lamp = new THREE.Mesh(lampGeo, lampMat);
      lamp.position.set(x, 5, z);
      scene.add(lamp);
      streetLamps.push(lamp);
    }
  }

  // --- Points de mission supplémentaires -----------------------------------
  // Choisis sur des routes/places dégagées (pas dans un bâtiment), répartis
  // dans la ville pour donner des objectifs variés.
  missionLocations.push(
    { name: 'Garage', x: blockCenter(0) , z: -HALF_CITY + ROAD_WIDTH / 2 },
    { name: 'Banque', x: HALF_CITY - ROAD_WIDTH / 2, z: blockCenter(CITY_SIZE - 1) },
    { name: 'Port', x: -HALF_CITY + ROAD_WIDTH / 2, z: HALF_CITY - ROAD_WIDTH / 2 },
  );

  // --- Voitures garées (obstacles statiques en bord de route) ---------------
  // Placement déterministe sur des routes intérieures, aux centres de blocs
  // (blockCenter) pour éviter les intersections.
  const parkedGeo = new THREE.BoxGeometry(1.9, 0.75, 3.8);
  const parkedColors = [0x2244bb, 0x882222, 0x227744, 0x998822, 0x445566, 0x774466, 0x33557a];
  const parkedMats = parkedColors.map((c) => new THREE.MeshLambertMaterial({ color: c }));
  let _pmi = 0;

  // Routes horizontales (constant Z) → voitures face à X (rotation.y = PI/2)
  for (const rz of [roadZs[1], roadZs[2], roadZs[3]]) {
    for (let bi = 0; bi < CITY_SIZE; bi += 2) {
      const cx = blockCenter(bi);
      const pz = rz + 3.3; // bord droit de la chaussée
      const mesh = new THREE.Mesh(parkedGeo, parkedMats[_pmi++ % parkedMats.length]);
      mesh.position.set(cx, 0.375, pz);
      mesh.rotation.y = Math.PI / 2;
      mesh.castShadow = true;
      scene.add(mesh);
      // Après rotation PI/2 : longueur 3.8 → monde X, largeur 1.9 → monde Z
      colliders.push({ x: cx, z: pz, halfWidth: 1.9, halfDepth: 0.95 });
    }
  }

  // Routes verticales (constant X) → voitures face à Z (rotation.y = 0)
  for (const rx of [roadXs[1], roadXs[2], roadXs[3]]) {
    for (let bi = 1; bi < CITY_SIZE; bi += 2) {
      const cz = blockCenter(bi);
      const px = rx + 3.3; // bord droit de la chaussée
      const mesh = new THREE.Mesh(parkedGeo, parkedMats[_pmi++ % parkedMats.length]);
      mesh.position.set(px, 0.375, cz);
      // rotation.y = 0 : longueur 3.8 → monde Z, largeur 1.9 → monde X
      mesh.castShadow = true;
      scene.add(mesh);
      colliders.push({ x: px, z: cz, halfWidth: 0.95, halfDepth: 1.9 });
    }
  }

  // --- Arbres de trottoir --------------------------------------------------
  // Tronc cylindrique + sphère feuillage — pas de collider (minces + sur trottoir).
  const trunkGeo = new THREE.CylinderGeometry(0.28, 0.35, 2.8, 7);
  const trunkMat = new THREE.MeshLambertMaterial({ color: 0x7a5c3a });
  const leafGeo  = new THREE.SphereGeometry(1.7, 8, 6);
  const leafPalette = [0x2d7a3a, 0x3a8a28, 0x4a7a30];
  const leafMats = leafPalette.map((c) => new THREE.MeshLambertMaterial({ color: c }));

  function addTree(tx, tz, idx) {
    const trunk = new THREE.Mesh(trunkGeo, trunkMat);
    trunk.position.set(tx, 1.4, tz);
    trunk.castShadow = true;
    scene.add(trunk);
    const leaves = new THREE.Mesh(leafGeo, leafMats[idx % leafMats.length]);
    leaves.position.set(tx, 3.7, tz);
    leaves.castShadow = true;
    scene.add(leaves);
  }

  // Arbres le long de routes horizontales (côté +Z)
  let _ti = 0;
  for (const rz of [roadZs[1], roadZs[3]]) {
    for (let bi = 0; bi < CITY_SIZE; bi++) {
      addTree(blockCenter(bi), rz + 6.2, _ti++);
    }
  }
  // Arbres le long de routes verticales (côté +X)
  for (const rx of [roadXs[1], roadXs[3]]) {
    for (let bi = 0; bi < CITY_SIZE; bi++) {
      addTree(rx + 6.2, blockCenter(bi), _ti++);
    }
  }

  // --- Mobilier urbain (bollards avec colliders, bancs, poubelles) ---------
  new StreetFurnitureSystem(scene, roadXs, roadZs, colliders);

  // --- Enseignes néon — Quartier Est (x > 57) ------------------------------
  // Panneaux émissifs sur la façade est des bâtiments ; pulsés dans main.js.
  const neonSigns = [];
  const NEON_COLS = [0xff0088, 0x00ffcc, 0xff6600, 0xaaff00, 0x0099ff];
  const estCx = (roadXs[4] + roadXs[5]) / 2 + 8; // x ≈ 84, dans Quartier Est
  for (let j = 0; j < CITY_SIZE; j++) {
    const cz  = (roadZs[j] + roadZs[j + 1]) / 2;
    const col = NEON_COLS[j % NEON_COLS.length];
    const signH = 0.9 + j * 0.18;
    const signW = 2.2 + j * 0.25;
    const mat   = new THREE.MeshStandardMaterial({
      color: col, emissive: col, emissiveIntensity: 1.0,
    });
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(0.12, signH, signW), mat);
    mesh.position.set(estCx, 5 + j * 1.2, cz);
    scene.add(mesh);
    neonSigns.push({ mat, base: 0.9 + j * 0.06, phase: j * Math.PI * 0.55 });
  }

  // --- Marqueur Garage (sol lumineux) --------------------------------------
  const garageX = blockCenter(0);
  const garageZ = -HALF_CITY + ROAD_WIDTH / 2;
  const garagePadMat = new THREE.MeshStandardMaterial({
    color: 0x004422, emissive: 0x00ff66, emissiveIntensity: 0.55,
  });
  const garagePad = new THREE.Mesh(new THREE.BoxGeometry(5, 0.12, 5), garagePadMat);
  garagePad.position.set(garageX, 0.06, garageZ);
  scene.add(garagePad);

  // --- Point de spawn -------------------------------------------------------
  // Sur la route horizontale qui traverse la rangée de blocs spawnBlockJ,
  // orienté pour rouler le long de cette rue (axe X), loin des bâtiments.
  const spawnX = -HALF_CITY + ROAD_WIDTH / 2;
  const spawnZ = -HALF_CITY + CELL * spawnBlockJ; // ligne de route, pas le centre d'un bloc
  const spawnPoint = {
    x: spawnX,
    z: spawnZ,
    rotationY: Math.PI / 2, // face vers +X, le long de la rue
  };

  return {
    colliders,
    spawnPoint,
    missionLocations,
    streetLamps,
    neonSigns,
    garagePos: { x: garageX, z: garageZ },
    roadLines: {
      xs: roadXs.slice(),
      zs: roadZs.slice(),
    },
  };
}
