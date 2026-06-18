// world.js — NEXUS CITY : Ville Surréaliste d'Open City
// 5 districts à identité radicale, architecture impossible, et structures
// interactives : portails de téléportation, trampolines, couloirs de vitesse.
// 100% procédural — zéro texture externe — zéro dépendance externe.

import * as THREE from 'three';
import { StreetFurnitureSystem } from './streetfurniture.js';

// ── Grille de la ville ────────────────────────────────────────────────────────

const CITY_SIZE  = 5;
const BLOCK_SIZE = 28;
const ROAD_WIDTH = 10;
const CELL       = BLOCK_SIZE + ROAD_WIDTH; // 38
const HALF_CITY  = (CITY_SIZE * CELL) / 2;  // 95

function blockCenter(i) {
  return -HALF_CITY + CELL * i + CELL / 2;
}

// ── Helpers géométrie ─────────────────────────────────────────────────────────

function smat(color, rough = 0.6, metal = 0, emissive = 0, eInt = 0) {
  return new THREE.MeshStandardMaterial({
    color, roughness: rough, metalness: metal,
    emissive: emissive || color,
    emissiveIntensity: emissive ? eInt : 0,
  });
}
function lmat(color) {
  return new THREE.MeshLambertMaterial({ color });
}
function addMesh(scene, geo, mat, x, y, z, rx = 0, ry = 0, rz = 0, shadow = true) {
  const m = new THREE.Mesh(geo, mat);
  m.position.set(x, y, z);
  m.rotation.set(rx, ry, rz);
  if (shadow) { m.castShadow = true; m.receiveShadow = true; }
  scene.add(m);
  return m;
}
function box(w, h, d) { return new THREE.BoxGeometry(w, h, d); }
function cyl(r, h, segs = 8) { return new THREE.CylinderGeometry(r, r, h, segs); }
function cone(r, h, segs = 7) { return new THREE.ConeGeometry(r, h, segs); }
function sph(r, ws = 10, hs = 8) { return new THREE.SphereGeometry(r, ws, hs); }
function tor(r, tube, rs = 8, ts = 24) { return new THREE.TorusGeometry(r, tube, rs, ts); }
const rand = (lo, hi) => lo + Math.random() * (hi - lo);
const randi = (n) => Math.floor(Math.random() * n);

// ── District par indice de bloc ───────────────────────────────────────────────

function district(i, j) {
  if (j === 0) return 'nord';
  if (j === 4) return 'sud';
  if (i === 0) return 'ouest';
  if (i === 4) return 'est';
  return 'centre';
}

// ── Palettes par district ─────────────────────────────────────────────────────

const PALETTES = {
  nord:   [0x88bbd8, 0x6699cc, 0x9bb8d4, 0xaaccee, 0xc8ddf0, 0x557799],
  sud:    [0x3a7a3a, 0x8a6a20, 0x5a9a30, 0xb07a10, 0x406030, 0xc08040],
  ouest:  [0x7a2060, 0x501040, 0x8a1a50, 0x300820, 0xaa3070, 0x601848],
  est:    [0x0a1a2e, 0x0d2137, 0x102840, 0x081528, 0x0f1f32, 0x0c1e30],
  centre: [0xb0b8c8, 0xc0c8d8, 0x909aa8, 0xa8b0c0, 0xd0d8e8, 0x808898],
};

// ─────────────────────────────────────────────────────────────────────────────
//  CONSTRUCTEURS DE BÂTIMENTS PAR DISTRICT
// ─────────────────────────────────────────────────────────────────────────────

// NORD — Cristaux de glace : cônes + cylindres iridescents
function buildNord(scene, colliders, cx, cz, w, d, h) {
  const col = PALETTES.nord[randi(PALETTES.nord.length)];
  const mat = smat(col, 0.15, 0.75, col, 0.12);
  const rCyl = Math.min(w, d) * 0.38;

  // Fût principal
  addMesh(scene, cyl(rCyl, h * 0.7, 7), mat, cx, h * 0.35, cz);
  // Pointe cristalline
  addMesh(scene, cone(rCyl * 0.9, h * 0.5, 7), mat, cx, h * 0.85, cz);
  // Anneau de glace à mi-hauteur
  if (h > 12) {
    addMesh(scene, tor(rCyl * 1.3, 0.18, 5, 14), mat, cx, h * 0.45, cz, Math.PI / 2);
  }
  colliders.push({ x: cx, z: cz, halfWidth: rCyl + 0.3, halfDepth: rCyl + 0.3 });
}

// SUD — Bulbes organiques sur tiges mécaniques
function buildSud(scene, colliders, cx, cz, w, d, h) {
  const stemCol = 0x3a3028;
  const bulbCol = PALETTES.sud[randi(PALETTES.sud.length)];
  const stemR   = Math.min(w, d) * 0.18;
  const bulbR   = Math.min(w, d) * 0.44;

  // Tige
  addMesh(scene, cyl(stemR, h * 0.65, 6), lmat(stemCol), cx, h * 0.325, cz);
  // Bulbe principal
  const bulb = new THREE.Mesh(sph(bulbR, 10, 8), smat(bulbCol, 0.6, 0.1, bulbCol, 0.08));
  bulb.position.set(cx, h * 0.70, cz);
  bulb.castShadow = true;
  scene.add(bulb);
  // Bulbe secondaire plus petit
  if (h > 8) {
    const b2 = new THREE.Mesh(sph(bulbR * 0.55, 8, 6), smat(bulbCol, 0.65, 0.1));
    b2.position.set(cx + stemR * 2, h * 0.82, cz + stemR * 2);
    scene.add(b2);
  }
  colliders.push({ x: cx, z: cz, halfWidth: bulbR + 0.2, halfDepth: bulbR + 0.2 });
}

// OUEST — Architecture renversée : socle étroit, couronne large
function buildOuest(scene, colliders, cx, cz, w, d, h) {
  const col  = PALETTES.ouest[randi(PALETTES.ouest.length)];
  const mat  = smat(col, 0.4, 0.5, col, 0.15);
  const wBot = w * 0.35;
  const dBot = d * 0.35;

  // Pilier étroit
  addMesh(scene, box(wBot, h * 0.55, dBot), mat, cx, h * 0.275, cz);
  // Couronne inversée (large en haut)
  addMesh(scene, box(w * 1.1, h * 0.45, d * 1.1), mat, cx, h * 0.775, cz);
  // Tenon décoratif sous la couronne
  addMesh(scene, box(w * 0.6, 0.5, d * 0.6), smat(0x220011, 0.3, 0.7), cx, h * 0.55, cz);

  colliders.push({ x: cx, z: cz, halfWidth: w * 0.55 + 0.2, halfDepth: d * 0.55 + 0.2 });
}

// EST — Tours penchées cyberpunk avec bandes néon
function buildEst(scene, colliders, cx, cz, w, d, h) {
  const bodyCol = PALETTES.est[randi(PALETTES.est.length)];
  const neonCol = [0xff00cc, 0x00ffcc, 0xffcc00, 0x0099ff, 0xff4400][randi(5)];
  const tilt    = (Math.random() - 0.5) * 0.14; // inclinaison ±8°
  const mat     = smat(bodyCol, 0.2, 0.4);

  const tower = new THREE.Mesh(box(w, h, d), mat);
  tower.position.set(cx, h / 2, cz);
  tower.rotation.z = tilt;
  tower.castShadow = true;
  scene.add(tower);

  // Bandes néon sur la façade (3-5 bandes)
  const nMat = smat(neonCol, 0.05, 0.1, neonCol, 1.2);
  const bands = 2 + randi(4);
  for (let k = 0; k < bands; k++) {
    const yOff = (h * 0.15) + (k / bands) * h * 0.7;
    const strip = new THREE.Mesh(box(w * 1.02, 0.18, 0.12), nMat);
    strip.position.set(cx, yOff, cz + d / 2 + 0.06);
    strip.rotation.z = tilt;
    scene.add(strip);
  }

  colliders.push({ x: cx, z: cz, halfWidth: w / 2 + 0.3, halfDepth: d / 2 + 0.3 });
}

// CENTRE — Obélisques de miroir + boîtes déconstruites
function buildCentre(scene, colliders, cx, cz, w, d, h) {
  const mirrorMat = smat(0xdde8f0, 0.05, 0.95);
  const angle     = (randi(4)) * Math.PI / 4;

  if (Math.random() < 0.5) {
    // Obélisque fin et très haut
    const obelisk = new THREE.Mesh(box(w * 0.4, h, d * 0.4), mirrorMat);
    obelisk.position.set(cx, h / 2, cz);
    obelisk.rotation.y = angle;
    obelisk.castShadow = true;
    scene.add(obelisk);
    // Pointe en losange
    addMesh(scene, box(w * 0.5, w * 0.5, d * 0.5), mirrorMat, cx, h + w * 0.25, cz, 0, angle, Math.PI / 4);
  } else {
    // Boîte déconstruite (rotation libre)
    const m = new THREE.Mesh(box(w, h * 0.6, d), smat(PALETTES.centre[randi(PALETTES.centre.length)], 0.3, 0.5));
    m.position.set(cx, h * 0.3, cz);
    m.rotation.y = angle * 0.5;
    m.castShadow = true;
    scene.add(m);
    // Bloc secondaire décalé
    const m2 = new THREE.Mesh(box(w * 0.7, h * 0.45, d * 0.7), mirrorMat);
    m2.position.set(cx + w * 0.15, h * 0.825, cz + d * 0.15);
    m2.rotation.y = -angle * 0.3;
    m2.castShadow = true;
    scene.add(m2);
  }

  colliders.push({ x: cx, z: cz, halfWidth: w / 2 + 0.2, halfDepth: d / 2 + 0.2 });
}

// ─────────────────────────────────────────────────────────────────────────────
//  LANDMARKS (1 par district)
// ─────────────────────────────────────────────────────────────────────────────

function buildLandmarkNord(scene, x, z) {
  // Cathédrale cristalline : 3 grandes spires + arcade
  const mat = smat(0xaaddff, 0.05, 0.8, 0x88ccff, 0.3);
  // Tour centrale
  addMesh(scene, cyl(2.2, 28, 8), mat, x, 14, z);
  addMesh(scene, cone(2.2, 18, 8), mat, x, 37, z);
  // Tours latérales
  for (const dx of [-6, 6]) {
    addMesh(scene, cyl(1.2, 18, 7), mat, x + dx, 9, z);
    addMesh(scene, cone(1.2, 12, 7), mat, x + dx, 24, z);
  }
  // Arcade au sol (torus couché)
  addMesh(scene, tor(5, 0.55, 6, 20), mat, x, 2.5, z, Math.PI / 2);
}

function buildLandmarkSud(scene, x, z) {
  // Arbre mécanique géant
  const trunkMat = smat(0x2a2010, 0.7, 0.2);
  const leafMat  = smat(0x1a5a10, 0.5, 0.1, 0x2a7a20, 0.08);
  const pipeMat  = smat(0x554433, 0.5, 0.4);

  addMesh(scene, cyl(1.8, 22, 8), trunkMat, x, 11, z);
  // Branches (cylindres penchés)
  for (let k = 0; k < 6; k++) {
    const ang = (k / 6) * Math.PI * 2;
    const bx = x + Math.cos(ang) * 4; const bz = z + Math.sin(ang) * 4;
    const branch = new THREE.Mesh(cyl(0.55, 9, 5), pipeMat);
    branch.position.set(bx, 18, bz);
    branch.rotation.z = Math.PI / 3.5;
    branch.rotation.y = ang;
    scene.add(branch);
  }
  // Canopée (sphères vertes)
  for (const [dx, dy, dz] of [[0,0,0],[-4,4,0],[4,4,0],[0,4,-4],[0,4,4]]) {
    const c = new THREE.Mesh(sph(4 - Math.abs(dy) * 0.2, 10, 7), leafMat);
    c.position.set(x + dx, 26 + dy, z + dz);
    scene.add(c);
  }
}

function buildLandmarkOuest(scene, x, z) {
  // Pyramide inversée suspendue sur une aiguille
  const needleMat = smat(0x8a1a5a, 0.2, 0.7);
  const pyrMat    = smat(0x601848, 0.15, 0.8, 0xaa2060, 0.12);

  // Aiguille du bas
  addMesh(scene, cyl(0.4, 14, 5), needleMat, x, 7, z);
  // Pyramide inversée (boîte large en haut, étroite en bas)
  addMesh(scene, box(18, 2, 18), pyrMat, x, 16.5, z);
  addMesh(scene, box(12, 2, 12), pyrMat, x, 14.5, z);
  addMesh(scene, box(6,  2, 6 ), pyrMat, x, 12.5, z);
  addMesh(scene, box(1.5,2, 1.5), pyrMat, x, 10.5, z);
  // Lévitation glow en dessous
  addMesh(scene, cyl(7, 0.3, 16), smat(0xaa2080, 0.1, 0.2, 0xff44bb, 0.6), x, 15.5, z, false);
}

function buildLandmarkEst(scene, x, z) {
  // Panneau billboard géant incliné + écran émissif
  const frameMat  = smat(0x0a0a18, 0.3, 0.5);
  const screenMat = smat(0x001a08, 0.1, 0.0, 0x00ff88, 0.7);
  const accentMat = smat(0xff0088, 0.05, 0.1, 0xff0088, 1.5);

  // Pieds du panneau
  for (const dx of [-7, 7]) {
    addMesh(scene, cyl(0.6, 20, 6), frameMat, x + dx, 10, z);
  }
  // Écran incliné
  const screen = new THREE.Mesh(box(18, 9, 0.6), screenMat);
  screen.position.set(x, 22, z);
  screen.rotation.z = 0.05;
  screen.castShadow = true;
  scene.add(screen);
  // Liseré néon autour
  for (const [bw, bh, bx, by, bz] of [
    [18.4, 0.3, 0, 26.6, 0.35], [18.4, 0.3, 0, 17.4, 0.35],
    [0.3, 9.4, -9.3, 22, 0.35], [0.3, 9.4,  9.3, 22, 0.35],
  ]) {
    addMesh(scene, box(bw, bh, bz), accentMat, x + bx, by, z + 0.35);
  }
}

function buildLandmarkCentre(scene, x, z) {
  // Fontaine miroir : sphère centrale + anneaux concentriques
  const mirrorMat = smat(0xeef4ff, 0.02, 0.98);
  const glowMat   = smat(0x88ccff, 0.1, 0.1, 0x88ccff, 0.5);

  // Socle
  addMesh(scene, cyl(4, 1.0, 12), smat(0xc0cce0, 0.3, 0.6), x, 0.5, z);
  // Colonne centrale
  addMesh(scene, cyl(0.8, 8, 8), mirrorMat, x, 4.5, z);
  // Grande sphère miroir
  const sphere = new THREE.Mesh(sph(3.5, 16, 12), mirrorMat);
  sphere.position.set(x, 10, z);
  scene.add(sphere);
  // Anneaux flottants
  for (let k = 0; k < 3; k++) {
    const ring = new THREE.Mesh(tor(4 + k * 2, 0.18, 6, 22), glowMat);
    ring.position.set(x, 10 + k * 0.5, z);
    ring.rotation.x = k * 0.6;
    ring.rotation.y = k * 1.0;
    scene.add(ring);
  }
}

// ─────────────────────────────────────────────────────────────────────────────
//  PORTAILS DE TÉLÉPORTATION
// ─────────────────────────────────────────────────────────────────────────────

function buildPortal(scene, x, z, color, label) {
  const rimMat  = smat(color, 0.1, 0.5, color, 1.4);
  const coreMat = smat(color, 0.05, 0.0, color, 0.6);
  const coreTrans = new THREE.MeshStandardMaterial({
    color, emissive: color, emissiveIntensity: 0.5,
    transparent: true, opacity: 0.35, depthWrite: false,
  });

  // Anneau extérieur
  addMesh(scene, tor(3.5, 0.45, 10, 32), rimMat, x, 4, z, Math.PI / 2);
  // Anneau intérieur
  addMesh(scene, tor(2.4, 0.22, 8, 24), rimMat, x, 4, z, Math.PI / 2);
  // Disque de transport (semi-transparent)
  const disc = new THREE.Mesh(new THREE.CircleGeometry(3.2, 24), coreTrans);
  disc.position.set(x, 4, z);
  scene.add(disc);
  // Piliers de support
  for (const dx of [-3.8, 3.8]) {
    addMesh(scene, cyl(0.28, 8, 6), smat(color, 0.3, 0.6), x + dx, 4, z);
  }
  return { x, z };
}

// ─────────────────────────────────────────────────────────────────────────────
//  TRAMPOLINES (jump pads)
// ─────────────────────────────────────────────────────────────────────────────

function buildJumpPad(scene, x, z, power, neonSigns) {
  const padMat  = smat(0x00ff88, 0.1, 0.2, 0x00ff88, 1.0);
  const rimMat  = smat(0x004422, 0.2, 0.6, 0x00ff44, 0.6);

  // Disque
  addMesh(scene, new THREE.CylinderGeometry(2.2, 2.2, 0.22, 16), padMat, x, 0.11, z, false, false);
  addMesh(scene, tor(2.2, 0.18, 8, 20), rimMat, x, 0.22, z, Math.PI / 2, 0, 0, false);
  // Flèche centrale (pointe vers le haut)
  addMesh(scene, cone(0.5, 0.9, 4), padMat, x, 0.8, z, 0, Math.PI / 4);

  // Ajoute à neonSigns pour le pulsatile
  neonSigns.push({ mat: padMat, base: 0.8, phase: Math.random() * Math.PI * 2 });
  return { x, z, power };
}

// ─────────────────────────────────────────────────────────────────────────────
//  COULOIRS DE VITESSE (speed boosts)
// ─────────────────────────────────────────────────────────────────────────────

function buildSpeedBoost(scene, x, z, hw, hd, neonSigns) {
  const boostMat = smat(0xffcc00, 0.05, 0.1, 0xffaa00, 0.9);
  const stripe = new THREE.Mesh(box(hw * 2, 0.08, hd * 2), boostMat);
  stripe.position.set(x, 0.04, z);
  scene.add(stripe);
  // Flèches directionnelles
  for (let k = -1; k <= 1; k++) {
    addMesh(scene, cone(0.4, 0.7, 4), boostMat, x + k * (hw * 0.6), 0.45, z, 0, Math.PI / 4);
  }
  neonSigns.push({ mat: boostMat, base: 0.7, phase: 0 });
  return { x, z, hw, hd };
}

// ─────────────────────────────────────────────────────────────────────────────
//  EXPORT PRINCIPAL
// ─────────────────────────────────────────────────────────────────────────────

export function createWorld(scene) {
  const colliders       = [];
  const missionLocations = [];
  const streetLamps     = [];
  const neonSigns       = [];
  const jumpPads        = [];
  const speedBoosts     = [];
  const portals         = [];

  // ── Sol de base ────────────────────────────────────────────────────────────
  const groundSize = CITY_SIZE * CELL + ROAD_WIDTH;
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(groundSize, groundSize),
    lmat(0x1a1a22)
  );
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  scene.add(ground);

  // ── Couches de sol par district (couleur d'ambiance) ──────────────────────
  const DIST_GROUND = {
    nord:   0x0a1830, // bleu glace profond
    sud:    0x0f1808, // jungle sombre
    ouest:  0x1a0318, // violet abyssal
    est:    0x020408, // noir cyberpunk
    centre: 0x141820, // ardoise miroir
  };
  const distQuads = [
    ['nord',   -HALF_CITY,          -HALF_CITY,           HALF_CITY * 2, CELL * 1.5],
    ['sud',    -HALF_CITY,           HALF_CITY - CELL * 2, HALF_CITY * 2, CELL * 2],
    ['ouest',  -HALF_CITY,          -HALF_CITY,           CELL * 1.5,   HALF_CITY * 2],
    ['est',     HALF_CITY - CELL * 2,-HALF_CITY,           CELL * 2,     HALF_CITY * 2],
    ['centre', -CELL * 2.5,         -CELL * 2.5,           CELL * 5,     CELL * 5],
  ];
  for (const [d, x0, z0, sw, sh] of distQuads) {
    const dg = new THREE.Mesh(
      new THREE.PlaneGeometry(sw, sh),
      lmat(DIST_GROUND[d])
    );
    dg.rotation.x = -Math.PI / 2;
    dg.position.set(x0 + sw / 2, 0.005, z0 + sh / 2);
    dg.receiveShadow = true;
    scene.add(dg);
  }

  // ── Routes ─────────────────────────────────────────────────────────────────
  const roadMat    = lmat(0x1c1c22);
  const roadLength = CITY_SIZE * CELL + ROAD_WIDTH;
  const roadGeoH   = new THREE.PlaneGeometry(roadLength, ROAD_WIDTH);
  const roadGeoV   = new THREE.PlaneGeometry(ROAD_WIDTH, roadLength);

  const roadZs = [], roadXs = [];
  for (let i = 0; i <= CITY_SIZE; i++) {
    const c = -HALF_CITY + CELL * i;
    roadZs.push(c); roadXs.push(c);
  }

  for (const z of roadZs) {
    const r = new THREE.Mesh(roadGeoH, roadMat);
    r.rotation.x = -Math.PI / 2; r.position.set(0, 0.01, z);
    r.receiveShadow = true; scene.add(r);
  }
  for (const x of roadXs) {
    const r = new THREE.Mesh(roadGeoV, roadMat);
    r.rotation.x = -Math.PI / 2; r.position.set(x, 0.01, 0);
    r.receiveShadow = true; scene.add(r);
  }

  // ── Marquages au sol ───────────────────────────────────────────────────────
  const LANE_COLORS = { nord: 0x8899cc, sud: 0x448844, ouest: 0x883366, est: 0x00ccff, centre: 0xaaaacc };
  const laneSegLen = 4, laneGap = 4, laneWidth = 0.38;
  const laneGeoH = new THREE.PlaneGeometry(laneSegLen, laneWidth);
  const laneGeoV = new THREE.PlaneGeometry(laneWidth, laneSegLen);

  function laneMat(zVal) {
    const j = roadZs.indexOf(zVal);
    const dist = j === 0 ? 'nord' : j >= 4 ? 'sud' : 'centre';
    return new THREE.MeshBasicMaterial({ color: LANE_COLORS[dist] });
  }

  for (const z of roadZs) {
    const lm = laneMat(z);
    for (let x = -HALF_CITY; x <= HALF_CITY; x += laneSegLen + laneGap) {
      const seg = new THREE.Mesh(laneGeoH, lm);
      seg.rotation.x = -Math.PI / 2; seg.position.set(x, 0.02, z);
      scene.add(seg);
    }
  }
  for (const x of roadXs) {
    const lm = new THREE.MeshBasicMaterial({ color: x <= roadXs[0] ? LANE_COLORS.ouest : x >= roadXs[4] ? LANE_COLORS.est : LANE_COLORS.centre });
    for (let z = -HALF_CITY; z <= HALF_CITY; z += laneSegLen + laneGap) {
      const seg = new THREE.Mesh(laneGeoV, lm);
      seg.rotation.x = -Math.PI / 2; seg.position.set(x, 0.02, z);
      scene.add(seg);
    }
  }

  // ── Bâtiments (par district) ───────────────────────────────────────────────
  const margin = 3;
  let buildingCount = 0;
  const TARGET = 95;

  for (let i = 0; i < CITY_SIZE; i++) {
    for (let j = 0; j < CITY_SIZE; j++) {
      if (buildingCount >= TARGET) break;
      const cx = blockCenter(i);
      const cz = blockCenter(j);
      const dist = district(i, j);

      // Place centrale : pas de bâtiments → landmark + mission
      if (i === 2 && j === 2) {
        buildLandmarkCentre(scene, cx, cz);
        missionLocations.push({ name: 'Place des Miroirs', x: cx + 12, z: cz });
        continue;
      }
      // Landmark de district (1 par district, au bloc angulaire)
      if (i === 0 && j === 0) { buildLandmarkNord(scene, cx, cz); continue; }
      if (i === 4 && j === 4) { buildLandmarkSud(scene, cx, cz); continue; }
      if (i === 0 && j === 4) { buildLandmarkOuest(scene, cx, cz); continue; }
      if (i === 4 && j === 0) { buildLandmarkEst(scene, cx, cz); continue; }

      // Mini-parcelles dans chaque bloc
      const sub = 2;
      const usable = BLOCK_SIZE - margin * 2;
      const lotSize = usable / sub;

      for (let a = 0; a < sub; a++) {
        for (let b = 0; b < sub; b++) {
          if (buildingCount >= TARGET) break;
          if (Math.random() < 0.1) continue; // vide ponctuel

          const lcx = cx - usable / 2 + lotSize * a + lotSize / 2;
          const lcz = cz - usable / 2 + lotSize * b + lotSize / 2;
          const w = lotSize * (0.5 + Math.random() * 0.38);
          const d = lotSize * (0.5 + Math.random() * 0.38);
          const h = 5 + Math.random() * (dist === 'est' ? 30 : dist === 'nord' ? 25 : 18);

          switch (dist) {
            case 'nord':   buildNord(scene, colliders, lcx, lcz, w, d, h);   break;
            case 'sud':    buildSud(scene, colliders, lcx, lcz, w, d, h);    break;
            case 'ouest':  buildOuest(scene, colliders, lcx, lcz, w, d, h);  break;
            case 'est':    buildEst(scene, colliders, lcx, lcz, w, d, h);    break;
            default:       buildCentre(scene, colliders, lcx, lcz, w, d, h); break;
          }
          buildingCount++;
        }
      }
    }
  }

  // ── Portails de téléportation ──────────────────────────────────────────────
  // Portail A : Nord (z=-57), Portail B : Sud (z=+57)
  const pA = buildPortal(scene, blockCenter(2), roadZs[1] - 8, 0x00ccff);
  const pB = buildPortal(scene, blockCenter(2), roadZs[4] + 8, 0xff44aa);
  portals.push({ a: pA, b: pB });
  missionLocations.push({ name: 'Portail Nord', x: pA.x, z: pA.z });
  missionLocations.push({ name: 'Portail Sud', x: pB.x, z: pB.z });

  // ── Trampolines (jump pads) ────────────────────────────────────────────────
  const padPositions = [
    [roadXs[2] + 5, roadZs[2] + 5, 14],   // intersection centrale
    [blockCenter(4), roadZs[1], 18],        // Est-Nord
    [blockCenter(0), roadZs[3], 16],        // Ouest-Sud
    [roadXs[1], roadZs[1], 12],             // Nord-Ouest
    [blockCenter(2), roadZs[3] + 5, 20],    // Centre-Sud
  ];
  for (const [px, pz, power] of padPositions) {
    jumpPads.push(buildJumpPad(scene, px, pz, power, neonSigns));
  }

  // ── Couloirs de vitesse ────────────────────────────────────────────────────
  const boostData = [
    [roadXs[2], roadZs[1] + 19, 3.5, 8],   // axe vertical centre-nord
    [roadXs[3] + 5, roadZs[2], 8, 3.5],    // axe horizontal est
    [blockCenter(2), roadZs[3] - 10, 3.5, 7], // centre-sud
    [roadXs[1] + 5, roadZs[3], 8, 3.5],    // ouest-sud
  ];
  for (const [bx, bz, hw, hd] of boostData) {
    speedBoosts.push(buildSpeedBoost(scene, bx, bz, hw, hd, neonSigns));
  }

  // ── Lampadaires surréalistes ───────────────────────────────────────────────
  const LAMP_STYLES = {
    nord:   { pole: 0x334466, lamp: 0xaaccff, glow: 0xaaccff },
    sud:    { pole: 0x3a2a10, lamp: 0xaaff44, glow: 0x88ff22 },
    ouest:  { pole: 0x440022, lamp: 0xff88cc, glow: 0xff44aa },
    est:    { pole: 0x0a0a22, lamp: 0x00ccff, glow: 0x00aaff },
    centre: { pole: 0x333344, lamp: 0xfff3c4, glow: 0xffee99 },
  };

  for (let i = 0; i <= CITY_SIZE; i++) {
    for (let j = 0; j <= CITY_SIZE; j++) {
      if ((i + j) % 2 !== 0) continue;
      const x = -HALF_CITY + CELL * i + ROAD_WIDTH / 2 + 0.8;
      const z = -HALF_CITY + CELL * j + ROAD_WIDTH / 2 + 0.8;
      const d = district(Math.min(i, CITY_SIZE - 1), Math.min(j, CITY_SIZE - 1));
      const style = LAMP_STYLES[d];

      const pole = new THREE.Mesh(new THREE.BoxGeometry(0.22, 5.5, 0.22), lmat(style.pole));
      pole.position.set(x, 2.75, z);
      scene.add(pole);

      const lampMat = new THREE.MeshStandardMaterial({ color: style.lamp, emissive: style.glow, emissiveIntensity: 0 });
      const lamp = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.28, 0.55), lampMat);
      lamp.position.set(x, 5.6, z);
      scene.add(lamp);
      streetLamps.push(lamp);
    }
  }

  // ── Enseignes néon Est + ambiance ─────────────────────────────────────────
  const NEON_COLS = [0xff0088, 0x00ffcc, 0xff6600, 0xaaff00, 0x0099ff];
  const estCx = (roadXs[4] + roadXs[5]) / 2 + 8;
  for (let j = 0; j < CITY_SIZE; j++) {
    const cz  = (roadZs[j] + roadZs[j + 1]) / 2;
    const col = NEON_COLS[j % NEON_COLS.length];
    const signH = 0.9 + j * 0.18;
    const signW = 2.2 + j * 0.25;
    const nm = smat(col, 0.05, 0.1, col, 1.0);
    const sign = new THREE.Mesh(new THREE.BoxGeometry(0.12, signH, signW), nm);
    sign.position.set(estCx, 5 + j * 1.2, cz);
    scene.add(sign);
    neonSigns.push({ mat: nm, base: 0.9 + j * 0.06, phase: j * Math.PI * 0.55 });
  }

  // Néons supplémentaires Ouest (violet)
  const ouestCx = roadXs[0] - 8;
  for (let j = 0; j < CITY_SIZE; j++) {
    const cz = (roadZs[j] + roadZs[j + 1]) / 2;
    const col = [0xcc00ff, 0xff00aa, 0x8800ff, 0xff00cc, 0xaa00ff][j];
    const nm = smat(col, 0.05, 0.1, col, 1.0);
    const sign = new THREE.Mesh(new THREE.BoxGeometry(0.12, 1.0 + j * 0.15, 2.0 + j * 0.2), nm);
    sign.position.set(ouestCx, 6 + j * 1.0, cz);
    scene.add(sign);
    neonSigns.push({ mat: nm, base: 0.85, phase: j * Math.PI * 0.42 });
  }

  // ── Arbres de trottoir ─────────────────────────────────────────────────────
  const TREE_STYLES = {
    nord:  { trunkC: 0x5566aa, leafC: 0x334488, wr: 1.4, hr: 1.3 },
    sud:   { trunkC: 0x4a3210, leafC: 0x1a6a10, wr: 2.0, hr: 1.8 },
    ouest: { trunkC: 0x550033, leafC: 0x8800cc, wr: 1.5, hr: 1.2 },
    est:   { trunkC: 0x0a0a20, leafC: 0x003344, wr: 1.3, hr: 1.8 },
    centre:{ trunkC: 0x666677, leafC: 0x445566, wr: 1.6, hr: 1.4 },
  };
  const trunkGeo = new THREE.CylinderGeometry(0.28, 0.36, 2.8, 7);

  function addTree(tx, tz, idx, d) {
    const ts = TREE_STYLES[d] || TREE_STYLES.centre;
    const trunk = new THREE.Mesh(trunkGeo, lmat(ts.trunkC));
    trunk.position.set(tx, 1.4, tz);
    trunk.castShadow = true;
    scene.add(trunk);
    const leafGeo = new THREE.SphereGeometry(ts.wr, 8, 6);
    const leaves  = new THREE.Mesh(leafGeo, lmat(ts.leafC));
    leaves.position.set(tx, 3.5 + ts.hr * 0.5, tz);
    leaves.scale.y = ts.hr / ts.wr;
    leaves.castShadow = true;
    scene.add(leaves);
  }

  let _ti = 0;
  for (const rz of [roadZs[1], roadZs[3]]) {
    for (let bi = 0; bi < CITY_SIZE; bi++) {
      const d = bi === 0 ? 'ouest' : bi === 4 ? 'est' : 'centre';
      addTree(blockCenter(bi), rz + 6.2, _ti++, d);
    }
  }
  for (const rx of [roadXs[1], roadXs[3]]) {
    for (let bi = 0; bi < CITY_SIZE; bi++) {
      const d = bi === 0 ? 'nord' : bi === 4 ? 'sud' : 'centre';
      addTree(rx + 6.2, blockCenter(bi), _ti++, d);
    }
  }

  // ── Voitures garées ────────────────────────────────────────────────────────
  const parkedGeo   = new THREE.BoxGeometry(1.9, 0.75, 3.8);
  const parkedColors= [0x2244bb, 0x882222, 0x227744, 0x998822, 0x445566, 0x774466, 0x33557a];
  const parkedMats  = parkedColors.map(c => lmat(c));
  let _pmi = 0;
  for (const rz of [roadZs[1], roadZs[2], roadZs[3]]) {
    for (let bi = 0; bi < CITY_SIZE; bi += 2) {
      const m = new THREE.Mesh(parkedGeo, parkedMats[_pmi++ % parkedMats.length]);
      const cx = blockCenter(bi), pz = rz + 3.3;
      m.position.set(cx, 0.375, pz); m.rotation.y = Math.PI / 2; m.castShadow = true;
      scene.add(m);
      colliders.push({ x: cx, z: pz, halfWidth: 1.9, halfDepth: 0.95 });
    }
  }
  for (const rx of [roadXs[1], roadXs[2], roadXs[3]]) {
    for (let bi = 1; bi < CITY_SIZE; bi += 2) {
      const m = new THREE.Mesh(parkedGeo, parkedMats[_pmi++ % parkedMats.length]);
      const cz = blockCenter(bi), px = rx + 3.3;
      m.position.set(px, 0.375, cz); m.castShadow = true;
      scene.add(m);
      colliders.push({ x: px, z: cz, halfWidth: 0.95, halfDepth: 1.9 });
    }
  }

  // ── Mobilier urbain ────────────────────────────────────────────────────────
  new StreetFurnitureSystem(scene, roadXs, roadZs, colliders);

  // ── Marqueur Garage ────────────────────────────────────────────────────────
  const garageX = blockCenter(0);
  const garageZ = -HALF_CITY + ROAD_WIDTH / 2;
  const garageMat = new THREE.MeshStandardMaterial({ color: 0x004422, emissive: 0x00ff66, emissiveIntensity: 0.55 });
  const garagePad = new THREE.Mesh(new THREE.BoxGeometry(5, 0.12, 5), garageMat);
  garagePad.position.set(garageX, 0.06, garageZ);
  scene.add(garagePad);

  missionLocations.push(
    { name: 'Garage',  x: garageX,                z: garageZ },
    { name: 'Banque',  x: HALF_CITY - ROAD_WIDTH / 2, z: blockCenter(CITY_SIZE - 1) },
    { name: 'Port',    x: -HALF_CITY + ROAD_WIDTH / 2, z: HALF_CITY - ROAD_WIDTH / 2 },
    { name: 'Arène',   x: blockCenter(2),          z: roadZs[3] - 5 },
  );

  // ── Point de spawn ─────────────────────────────────────────────────────────
  const spawnBlockJ = Math.floor(CITY_SIZE / 2);
  const spawnX = -HALF_CITY + ROAD_WIDTH / 2;
  const spawnZ = -HALF_CITY + CELL * spawnBlockJ;
  const spawnPoint = { x: spawnX, z: spawnZ, rotationY: Math.PI / 2 };

  return {
    colliders,
    spawnPoint,
    missionLocations,
    streetLamps,
    neonSigns,
    garagePos: { x: garageX, z: garageZ },
    roadLines: { xs: roadXs.slice(), zs: roadZs.slice() },
    jumpPads,
    speedBoosts,
    portals,
  };
}
