// characters.js — Expert Character Artist IA pour Open City.
// Personnages ultra-détaillés : visage avec iris/cils/lèvres volumétriques,
// mains à 4 doigts, ceinture, col de chemise, semelle de chaussure,
// 3 morphologies corporelles, 10 coiffures, balancement hanches + épaules.
// Zéro texture externe — 100% géométrie Three.js procédurale.

import * as THREE from 'three';

// ── Palettes ──────────────────────────────────────────────────────────────────

const SKIN_TONES = [
  0xfde9d0, // albâtre
  0xf5cba7, // très clair
  0xf0b27a, // clair
  0xe59866, // médium clair
  0xca8a56, // médium
  0xb5703a, // médium foncé
  0x935a2b, // foncé
  0x7b4621, // très foncé
  0x5e3015, // profond
  0x3d1f0a, // ébène
];

const SHIRT_COLORS  = [0x2e86c1,0xe74c3c,0x27ae60,0x8e44ad,0xd35400,0x2c3e50,0xf1c40f,0x1abc9c,0xecf0f1,0x7f8c8d];
const PANTS_COLORS  = [0x1a252f,0x2c3e50,0x566573,0x6e2f1a,0x1c4e6b,0x2e4057,0x4a235a,0x3d2b1f,0x1e8449,0x424949];
const HAIR_COLORS   = [0x1a0a00,0x4a2c0a,0xb5651d,0xd4a017,0x808080,0xf0e0c0,0x2c1810,0x000000,0xff4444,0x9b59b6];
const EYE_COLORS    = [0x3d2b1f,0x1a6b3c,0x1a4b8c,0x6b4c11,0x2c6b5a,0x5a2d82,0x2471a3,0x148f77];

// 3 morphologies : slim / medium / athletic
const BODY_TYPES = [
  { torsoW: 0.36, legW: 0.13, armW: 0.10, neckW: 0.12 },  // slim
  { torsoW: 0.42, legW: 0.15, armW: 0.12, neckW: 0.14 },  // medium
  { torsoW: 0.50, legW: 0.175, armW: 0.14, neckW: 0.16 }, // athletic
];

function rand(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

// ── Material helpers ──────────────────────────────────────────────────────────

function mat(color, rough = 0.75, metal = 0, emissive = 0, emissiveInt = 0) {
  return new THREE.MeshStandardMaterial({
    color,
    roughness: rough,
    metalness: metal,
    emissive: emissive || color,
    emissiveIntensity: emissive ? emissiveInt : 0,
  });
}

function matTransp(color, opacity, rough = 0.1, metal = 0.0) {
  return new THREE.MeshStandardMaterial({
    color, roughness: rough, metalness: metal,
    transparent: true, opacity, depthWrite: false,
  });
}

// ── Hair styles ───────────────────────────────────────────────────────────────

const HAIR_BUILDERS = [
  // 0 — Short buzz cut
  (grp, hm) => {
    grp.add(mesh(new THREE.BoxGeometry(0.32, 0.10, 0.35), hm, 0, 0.06, -0.02));
  },
  // 1 — Medium tousled
  (grp, hm) => {
    grp.add(mesh(new THREE.BoxGeometry(0.34, 0.14, 0.36), hm, 0, 0.08, -0.02));
    grp.add(mesh(new THREE.BoxGeometry(0.30, 0.08, 0.10), hm, 0, 0.02, 0.17));
  },
  // 2 — Afro
  (grp, hm) => {
    const a = new THREE.Mesh(new THREE.SphereGeometry(0.22, 10, 8), hm);
    a.position.set(0, 0.06, 0); a.scale.set(1, 0.92, 1);
    grp.add(a);
  },
  // 3 — Long straight + queue-de-cheval
  (grp, hm) => {
    grp.add(mesh(new THREE.BoxGeometry(0.32, 0.12, 0.35), hm, 0, 0.07, -0.02));
    grp.add(mesh(new THREE.BoxGeometry(0.26, 0.42, 0.07), hm, 0, -0.14, -0.18));
    // attache
    grp.add(mesh(new THREE.BoxGeometry(0.07, 0.05, 0.07), hm, 0, -0.12, -0.18));
  },
  // 4 — Chignon
  (grp, hm) => {
    grp.add(mesh(new THREE.BoxGeometry(0.30, 0.10, 0.32), hm, 0, 0.07, -0.01));
    const b = new THREE.Mesh(new THREE.SphereGeometry(0.09, 7, 6), hm);
    b.position.set(0, 0.17, -0.12); grp.add(b);
  },
  // 5 — Mohawk
  (grp, hm) => {
    grp.add(mesh(new THREE.BoxGeometry(0.09, 0.22, 0.32), hm, 0, 0.17, -0.02));
  },
  // 6 — Casquette
  (grp, hm) => {
    grp.add(mesh(new THREE.BoxGeometry(0.36, 0.06, 0.36), hm, 0, 0.04, -0.02)); // fond
    grp.add(mesh(new THREE.BoxGeometry(0.34, 0.04, 0.20), hm, 0, 0.02, 0.17));  // visière
  },
  // 7 — Boucles courtes (sphères)
  (grp, hm) => {
    for (const [x, y, z] of [[-0.08,0.05,-0.05],[0.08,0.05,-0.05],[0,0.08,0.05],[0,0.02,-0.12]]) {
      const s = new THREE.Mesh(new THREE.SphereGeometry(0.10, 7, 5), hm);
      s.position.set(x, y, z); s.scale.set(1.1, 0.85, 1);
      grp.add(s);
    }
  },
  // 8 — Tresses longues (plaques latérales)
  (grp, hm) => {
    grp.add(mesh(new THREE.BoxGeometry(0.30, 0.10, 0.32), hm, 0, 0.07, 0));
    for (const x of [-0.13, 0.13]) {
      grp.add(mesh(new THREE.BoxGeometry(0.07, 0.48, 0.06), hm, x, -0.16, 0));
    }
  },
  // 9 — Chauve
  (grp) => { /* rien — crâne peau visible */ },
];

// ── Mini mesh helper ──────────────────────────────────────────────────────────

function mesh(geo, material, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0) {
  const m = new THREE.Mesh(geo, material);
  m.position.set(x, y, z);
  m.rotation.set(rx, ry, rz);
  m.castShadow = true;
  return m;
}

// ── Face builder ──────────────────────────────────────────────────────────────

function buildFace(headGroup, skinColor, eyeColor, hairColor, hairStyle, isFemale) {
  const skinMat     = mat(skinColor, 0.65);
  const hairMat     = mat(hairColor, 0.88);
  const eyeWhiteMat = mat(0xfafafa, 0.4);
  const irisMat     = mat(eyeColor, 0.3);
  const pupilMat    = mat(0x060606, 0.2);
  const specMat     = mat(0xffffff, 0.0);
  const lipMat      = mat(Math.max(0, skinColor - 0x301820), 0.7);
  const browMat     = mat(hairColor, 0.88);
  const lidMat      = mat(skinColor - 0x0a0808, 0.65);

  // ── Yeux (blanc → iris → pupille → spéculaire) ──────────────────────
  for (const xOff of [-0.085, 0.085]) {
    // Globe oculaire (blanc légèrement aplati)
    const globe = new THREE.Mesh(new THREE.SphereGeometry(0.048, 9, 7), eyeWhiteMat);
    globe.position.set(xOff, 0.042, 0.142);
    globe.scale.z = 0.62;
    headGroup.add(globe);

    // Iris (disque coloré)
    const iris = new THREE.Mesh(new THREE.SphereGeometry(0.033, 8, 6), irisMat);
    iris.position.set(xOff, 0.042, 0.168);
    iris.scale.z = 0.28;
    headGroup.add(iris);

    // Pupille
    const pupil = new THREE.Mesh(new THREE.SphereGeometry(0.020, 7, 5), pupilMat);
    pupil.position.set(xOff, 0.042, 0.172);
    pupil.scale.z = 0.25;
    headGroup.add(pupil);

    // Point de reflet
    const spec = new THREE.Mesh(new THREE.SphereGeometry(0.007, 4, 3), specMat);
    spec.position.set(xOff + 0.013, 0.056, 0.174);
    headGroup.add(spec);

    // Paupière supérieure
    const lid = new THREE.Mesh(new THREE.BoxGeometry(0.105, 0.014, 0.018), lidMat);
    lid.position.set(xOff, 0.065, 0.158);
    lid.rotation.x = -0.18;
    headGroup.add(lid);
  }

  // ── Sourcils (arch léger) ───────────────────────────────────────────
  for (const [xOff, tilt] of [[-0.085, 0.08], [0.085, -0.08]]) {
    const brow = new THREE.Mesh(new THREE.BoxGeometry(0.075, 0.013, 0.014), browMat);
    brow.position.set(xOff, 0.108, 0.157);
    brow.rotation.z = tilt;
    headGroup.add(brow);
  }

  // ── Nez (arrête + pointe) ────────────────────────────────────────────
  const noseBridge = new THREE.Mesh(new THREE.BoxGeometry(0.030, 0.048, 0.030), skinMat);
  noseBridge.position.set(0, -0.008, 0.162);
  headGroup.add(noseBridge);
  const noseTip = new THREE.Mesh(new THREE.BoxGeometry(0.052, 0.024, 0.038), skinMat);
  noseTip.position.set(0, -0.032, 0.168);
  headGroup.add(noseTip);

  // ── Lèvres (supérieure + inférieure volumétriques) ──────────────────
  const lipTop = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.022, 0.025), lipMat);
  lipTop.position.set(0, -0.082, 0.162);
  headGroup.add(lipTop);
  const lipBot = new THREE.Mesh(new THREE.BoxGeometry(0.096, 0.020, 0.028), lipMat);
  lipBot.position.set(0, -0.106, 0.162);
  headGroup.add(lipBot);

  // ── Oreilles ────────────────────────────────────────────────────────
  const headW = isFemale ? 0.300 : 0.330;
  for (const xOff of [-(headW / 2 + 0.012), (headW / 2 + 0.012)]) {
    const ear = new THREE.Mesh(new THREE.BoxGeometry(0.022, 0.058, 0.042), skinMat);
    ear.position.set(xOff, 0.010, 0.002);
    headGroup.add(ear);
    // Lobe
    const lobe = new THREE.Mesh(new THREE.SphereGeometry(0.014, 5, 4), skinMat);
    lobe.position.set(xOff, -0.025, 0.002);
    headGroup.add(lobe);
  }

  // ── Coiffure ─────────────────────────────────────────────────────────
  HAIR_BUILDERS[hairStyle % HAIR_BUILDERS.length](headGroup, hairMat);
}

// ── Hand builder ──────────────────────────────────────────────────────────────

function buildHand(parent, skinMat, side) {
  const s = side === 'L' ? -1 : 1;
  const palmGeo = new THREE.BoxGeometry(0.115, 0.10, 0.075);
  const palm = new THREE.Mesh(palmGeo, skinMat);
  palm.position.set(0, -0.16, 0);
  parent.add(palm);

  // 4 doigts (groupe de 4 petites boîtes côte à côte)
  const fingerGeo = new THREE.BoxGeometry(0.022, 0.08, 0.022);
  for (let i = 0; i < 4; i++) {
    const f = new THREE.Mesh(fingerGeo, skinMat);
    f.position.set((i - 1.5) * 0.026, -0.255, 0.006);
    parent.add(f);
  }

  // Pouce
  const thumbGeo = new THREE.BoxGeometry(0.022, 0.06, 0.022);
  const thumb = new THREE.Mesh(thumbGeo, skinMat);
  thumb.position.set(s * 0.068, -0.20, 0.012);
  thumb.rotation.z = s * 0.35;
  parent.add(thumb);
}

// ── Main character builder ────────────────────────────────────────────────────

export function buildDetailedCharacter() {
  const skinColor  = rand(SKIN_TONES);
  const shirtColor = rand(SHIRT_COLORS);
  const pantsColor = rand(PANTS_COLORS);
  const eyeColor   = rand(EYE_COLORS);
  const hairColor  = rand(HAIR_COLORS);
  const hairStyle  = Math.floor(Math.random() * HAIR_BUILDERS.length);
  const isFemale   = Math.random() > 0.48;
  const body       = rand(BODY_TYPES);
  const hasGlasses = Math.random() < 0.18;
  const hasBackpack = Math.random() < 0.22;

  const skinMat  = mat(skinColor, 0.65);
  const shirtMat = mat(shirtColor, 0.82);
  const pantsMat = mat(pantsColor, 0.85);
  const shoeMat  = mat(0x111111, 0.72);
  const soleMat  = mat(0x2a2a2a, 0.8);
  const beltMat  = mat(0x1a0f00, 0.72, 0.1);
  const collarMat= mat(shirtColor - 0x101010, 0.80);

  const root = new THREE.Group();

  // ── Chaussures + semelles ──────────────────────────────────────────────
  const shoeGeo = new THREE.BoxGeometry(body.legW + 0.02, 0.10, 0.28);
  const soleGeo = new THREE.BoxGeometry(body.legW + 0.04, 0.04, 0.30);
  for (const [sx, side] of [[-0.115, 'L'], [0.115, 'R']]) {
    const shoe = new THREE.Mesh(shoeGeo, shoeMat);
    shoe.position.set(sx, 0.07, 0.01);
    shoe.castShadow = true;
    root.add(shoe);
    const sole = new THREE.Mesh(soleGeo, soleMat);
    sole.position.set(sx, 0.02, 0.01);
    root.add(sole);
  }

  // ── Jambes inférieures ─────────────────────────────────────────────────
  const lLegGeo = new THREE.BoxGeometry(body.legW, 0.38, 0.15);
  const lLegL = new THREE.Mesh(lLegGeo, pantsMat);
  const lLegR = new THREE.Mesh(lLegGeo, pantsMat);
  lLegL.position.set(-0.115, 0.31, 0); lLegL.castShadow = true;
  lLegR.position.set( 0.115, 0.31, 0); lLegR.castShadow = true;
  root.add(lLegL, lLegR);

  // ── Jambes supérieures ─────────────────────────────────────────────────
  const uLegGeo = new THREE.BoxGeometry(body.legW + 0.025, 0.40, 0.17);
  const uLegL = new THREE.Mesh(uLegGeo, pantsMat);
  const uLegR = new THREE.Mesh(uLegGeo, pantsMat);
  uLegL.position.set(-0.115, 0.68, 0); uLegL.castShadow = true;
  uLegR.position.set( 0.115, 0.68, 0); uLegR.castShadow = true;
  root.add(uLegL, uLegR);

  // ── Torse ─────────────────────────────────────────────────────────────
  const torso = new THREE.Mesh(new THREE.BoxGeometry(body.torsoW, 0.54, 0.25), shirtMat);
  torso.position.set(0, 1.10, 0);
  torso.castShadow = true;
  root.add(torso);

  // ── Ceinture ──────────────────────────────────────────────────────────
  const belt = new THREE.Mesh(new THREE.BoxGeometry(body.torsoW + 0.02, 0.045, 0.26), beltMat);
  belt.position.set(0, 0.84, 0);
  root.add(belt);
  // Boucle de ceinture
  const buckle = new THREE.Mesh(new THREE.BoxGeometry(0.055, 0.04, 0.015), mat(0xaaaaaa, 0.3, 0.8));
  buckle.position.set(0, 0.84, 0.132);
  root.add(buckle);

  // ── Col de chemise ─────────────────────────────────────────────────────
  for (const [xOff, zRot] of [[-0.07, 0.3], [0.07, -0.3]]) {
    const collar = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.065, 0.018), collarMat);
    collar.position.set(xOff, 1.35, 0.118);
    collar.rotation.z = zRot;
    root.add(collar);
  }

  // ── Bras supérieurs ────────────────────────────────────────────────────
  const uArmGeo = new THREE.BoxGeometry(body.armW, 0.33, 0.14);
  const uArmL = new THREE.Mesh(uArmGeo, shirtMat);
  const uArmR = new THREE.Mesh(uArmGeo, shirtMat);
  uArmL.position.set(-(body.torsoW / 2 + 0.08), 1.20, 0); uArmL.castShadow = true;
  uArmR.position.set( (body.torsoW / 2 + 0.08), 1.20, 0); uArmR.castShadow = true;
  root.add(uArmL, uArmR);

  // ── Avant-bras + mains ─────────────────────────────────────────────────
  const lArmGeo = new THREE.BoxGeometry(body.armW - 0.02, 0.30, 0.12);
  const lArmL = new THREE.Mesh(lArmGeo, skinMat);
  const lArmR = new THREE.Mesh(lArmGeo, skinMat);
  lArmL.position.set(-(body.torsoW / 2 + 0.08), 0.86, 0); lArmL.castShadow = true;
  lArmR.position.set( (body.torsoW / 2 + 0.08), 0.86, 0); lArmR.castShadow = true;
  root.add(lArmL, lArmR);
  buildHand(lArmL, skinMat, 'L');
  buildHand(lArmR, skinMat, 'R');

  // ── Cou ───────────────────────────────────────────────────────────────
  const neck = new THREE.Mesh(
    new THREE.CylinderGeometry(body.neckW * 0.44, body.neckW * 0.50, 0.16, 8),
    skinMat
  );
  neck.position.set(0, 1.43, 0);
  root.add(neck);

  // ── Tête ──────────────────────────────────────────────────────────────
  const headW = isFemale ? 0.300 : 0.330;
  const headGroup = new THREE.Group();
  headGroup.position.set(0, 1.655, 0);

  // Crâne principal (légèrement arrondi)
  const skull = new THREE.Mesh(
    new THREE.BoxGeometry(headW, 0.35, 0.34),
    mat(skinColor, 0.65)
  );
  skull.castShadow = true;
  headGroup.add(skull);
  // Mâchoire légèrement plus étroite
  const jaw = new THREE.Mesh(
    new THREE.BoxGeometry(headW * 0.88, 0.12, 0.30),
    mat(skinColor, 0.65)
  );
  jaw.position.set(0, -0.20, 0);
  headGroup.add(jaw);

  buildFace(headGroup, skinColor, eyeColor, hairColor, hairStyle, isFemale);

  // ── Lunettes (optionnelles) ─────────────────────────────────────────
  if (hasGlasses) {
    const frameMat = mat(0x111111, 0.5, 0.3);
    for (const xOff of [-0.085, 0.085]) {
      // Monture ronde
      const frame = new THREE.Mesh(
        new THREE.TorusGeometry(0.038, 0.006, 4, 12),
        frameMat
      );
      frame.position.set(xOff, 0.042, 0.172);
      frame.rotation.x = Math.PI / 2;
      headGroup.add(frame);
    }
    // Pont central
    const bridge = new THREE.Mesh(new THREE.BoxGeometry(0.034, 0.006, 0.008), frameMat);
    bridge.position.set(0, 0.042, 0.174);
    headGroup.add(bridge);
  }

  root.add(headGroup);

  // ── Sac à dos (optionnel) ───────────────────────────────────────────
  if (hasBackpack) {
    const packMat = mat(rand([0x2e4057,0x922b21,0x1e8449,0x6c3483,0x1a5276]), 0.88);
    const pack = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.38, 0.12), packMat);
    pack.position.set(0, 1.08, -0.165);
    root.add(pack);
    // Sangles
    const strapMat = mat(0x5d6d7e, 0.85);
    for (const xOff of [-0.08, 0.08]) {
      const strap = new THREE.Mesh(new THREE.BoxGeometry(0.025, 0.42, 0.022), strapMat);
      strap.position.set(xOff, 1.09, -0.072);
      root.add(strap);
    }
  }

  // ── Références os pour animation ────────────────────────────────────
  root.userData.bones = {
    headGroup,
    torso,
    uArmL, uArmR,
    lArmL, lArmR,
    uLegL, uLegR,
    lLegL, lLegR,
  };
  root.userData.animPhase = Math.random() * Math.PI * 2;

  return root;
}

// ── CharacterAnimator ─────────────────────────────────────────────────────────

const WALK_FREQ   = 2.4;   // Hz
const ARM_SWING   = 0.32;  // rad
const LEG_SWING   = 0.40;  // rad
const HEAD_BOB    = 0.028; // m
const HIP_SWAY    = 0.035; // m lateral
const TORSO_TWIST = 0.055; // rad shoulder counter-rotation

export class CharacterAnimator {
  static update(mesh, speed, dt) {
    const b = mesh.userData.bones;
    if (!b) return;

    mesh.userData.animPhase += dt * WALK_FREQ * Math.PI * 2 * clamp(speed / 1.5, 0, 1);
    const t  = mesh.userData.animPhase;
    const sw = clamp(speed / 1.5, 0, 1);

    // ── Swing des jambes (genou semi-plié en retour) ───────────────────
    b.uLegL.rotation.x =  Math.sin(t)           * LEG_SWING * sw;
    b.uLegR.rotation.x = -Math.sin(t)           * LEG_SWING * sw;
    b.lLegL.rotation.x =  Math.max(0, -Math.sin(t)) * LEG_SWING * 0.55 * sw;
    b.lLegR.rotation.x =  Math.max(0,  Math.sin(t)) * LEG_SWING * 0.55 * sw;

    // ── Swing des bras (inverse jambes) ────────────────────────────────
    b.uArmL.rotation.x = -Math.sin(t) * ARM_SWING * sw;
    b.uArmR.rotation.x =  Math.sin(t) * ARM_SWING * sw;
    b.lArmL.rotation.x =  Math.max(0, Math.sin(t))  * ARM_SWING * 0.42 * sw;
    b.lArmR.rotation.x =  Math.max(0, -Math.sin(t)) * ARM_SWING * 0.42 * sw;

    // ── Balancement des hanches (déplacement latéral du torse) ────────
    if (b.torso) {
      b.torso.position.x = Math.sin(t * 2) * HIP_SWAY * sw;
      // Counter-rotation épaules vs hanches
      b.torso.rotation.y = -Math.sin(t) * TORSO_TWIST * sw;
    }

    // ── Bob de tête + micro-sway ────────────────────────────────────────
    b.headGroup.position.y = 1.655 + Math.abs(Math.sin(t * 2)) * HEAD_BOB * sw;
    b.headGroup.rotation.y = Math.sin(t * 0.28) * 0.038;
  }
}
