// characters.js — Expert Character Artist IA pour Open City.
// Crée des humanoids détaillés : visage avec yeux/nez/bouche, corps proportionné,
// membres articulés, 8 tons de peau, 6 coupes de cheveux, vêtements variés.
// Zéro texture externe — 100% géométrie Three.js procédurale.

import * as THREE from 'three';

// ── Palette ───────────────────────────────────────────────────────────────────

const SKIN_TONES = [
  0xf5cba7, // très clair
  0xf0b27a, // clair
  0xe59866, // médium clair
  0xca8a56, // médium
  0xb5703a, // médium foncé
  0x935a2b, // foncé
  0x7b4621, // très foncé
  0x5e3015, // profond
];

const SHIRT_COLORS  = [0x2e86c1,0xe74c3c,0x27ae60,0x8e44ad,0xd35400,0x2c3e50,0xf1c40f,0x1abc9c];
const PANTS_COLORS  = [0x1a252f,0x2c3e50,0x566573,0x6e2f1a,0x1c4e6b,0x2e4057,0x4a235a,0x3d2b1f];
const HAIR_COLORS   = [0x1a0a00,0x4a2c0a,0xb5651d,0xd4a017,0x808080,0xf0e0c0,0x2c1810,0x000000];
const EYE_COLORS    = [0x3d2b1f,0x1a6b3c,0x1a4b8c,0x6b4c11,0x2c6b5a,0x5a2d82];

function rand(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

// ── Material helpers ──────────────────────────────────────────────────────────

function mat(color, rough = 0.75, metal = 0, emissive = 0, emissiveInt = 0) {
  return new THREE.MeshStandardMaterial({ color, roughness: rough, metalness: metal,
    emissive: emissive || color, emissiveIntensity: emissive ? emissiveInt : 0 });
}

// ── Hair styles ───────────────────────────────────────────────────────────────

const HAIR_BUILDERS = [
  // Short buzz cut
  (grp, skinMat, hairMat) => {
    const cap = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.10, 0.35), hairMat);
    cap.position.set(0, 0.06, -0.02);
    grp.add(cap);
  },
  // Medium tousled
  (grp, skinMat, hairMat) => {
    const cap = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.14, 0.36), hairMat);
    cap.position.set(0, 0.08, -0.02);
    grp.add(cap);
    const bang = new THREE.Mesh(new THREE.BoxGeometry(0.30, 0.08, 0.10), hairMat);
    bang.position.set(0, 0.02, 0.17);
    grp.add(bang);
  },
  // Afro
  (grp, skinMat, hairMat) => {
    const afro = new THREE.Mesh(new THREE.SphereGeometry(0.22, 8, 6), hairMat);
    afro.position.set(0, 0.06, 0);
    afro.scale.set(1, 0.9, 1);
    grp.add(afro);
  },
  // Long straight (back plate)
  (grp, skinMat, hairMat) => {
    const cap = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.12, 0.35), hairMat);
    cap.position.set(0, 0.07, -0.02);
    grp.add(cap);
    const tail = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.38, 0.07), hairMat);
    tail.position.set(0, -0.12, -0.18);
    grp.add(tail);
  },
  // Bun
  (grp, skinMat, hairMat) => {
    const cap = new THREE.Mesh(new THREE.BoxGeometry(0.30, 0.10, 0.32), hairMat);
    cap.position.set(0, 0.07, -0.01);
    grp.add(cap);
    const bun = new THREE.Mesh(new THREE.SphereGeometry(0.08, 6, 5), hairMat);
    bun.position.set(0, 0.16, -0.1);
    grp.add(bun);
  },
  // Mohawk
  (grp, skinMat, hairMat) => {
    const strip = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.20, 0.32), hairMat);
    strip.position.set(0, 0.16, -0.02);
    grp.add(strip);
  },
];

// ── Face builder ──────────────────────────────────────────────────────────────

function buildFace(headGroup, skinColor, eyeColor, hairColor, hairStyle) {
  const skinMat = mat(skinColor, 0.78);
  const hairMat = mat(hairColor, 0.9);
  const eyeWhiteMat = mat(0xf0f0f0, 0.5);
  const pupilMat    = mat(eyeColor, 0.3);
  const lipMat      = mat(skinColor - 0x201010, 0.8);
  const browMat     = mat(hairColor, 0.9);

  // Eyes (white + pupil)
  for (const xOff of [-0.08, 0.08]) {
    const white = new THREE.Mesh(new THREE.SphereGeometry(0.045, 7, 6), eyeWhiteMat);
    white.position.set(xOff, 0.04, 0.15);
    white.scale.z = 0.6;
    headGroup.add(white);

    const pupil = new THREE.Mesh(new THREE.SphereGeometry(0.026, 6, 5), pupilMat);
    pupil.position.set(xOff, 0.04, 0.175);
    pupil.scale.z = 0.5;
    headGroup.add(pupil);
  }

  // Eyebrows
  for (const xOff of [-0.08, 0.08]) {
    const brow = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.012, 0.012), browMat);
    brow.position.set(xOff, 0.10, 0.16);
    headGroup.add(brow);
  }

  // Nose
  const nose = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.045, 0.04), skinMat);
  nose.position.set(0, -0.02, 0.165);
  headGroup.add(nose);

  // Mouth (thin dark line)
  const mouth = new THREE.Mesh(new THREE.BoxGeometry(0.09, 0.012, 0.012), lipMat);
  mouth.position.set(0, -0.09, 0.165);
  headGroup.add(mouth);

  // Ears
  for (const xOff of [-0.165, 0.165]) {
    const ear = new THREE.Mesh(new THREE.BoxGeometry(0.025, 0.055, 0.04), skinMat);
    ear.position.set(xOff, 0.01, 0);
    headGroup.add(ear);
  }

  // Hair
  const hairStyleIdx = hairStyle % HAIR_BUILDERS.length;
  HAIR_BUILDERS[hairStyleIdx](headGroup, skinMat, hairMat);
}

// ── Limb builder ──────────────────────────────────────────────────────────────

function buildLimb(scene_or_group, upperGeo, lowerGeo, mat, upperPos, lowerOffset) {
  const upper = new THREE.Mesh(upperGeo, mat);
  upper.position.copy(upperPos);
  const lower = new THREE.Mesh(lowerGeo, mat);
  lower.position.copy(lowerOffset);
  upper.add(lower);
  return { upper, lower };
}

// ── Main character builder ────────────────────────────────────────────────────

export function buildDetailedCharacter() {
  const skinColor = rand(SKIN_TONES);
  const shirtColor = rand(SHIRT_COLORS);
  const pantsColor = rand(PANTS_COLORS);
  const eyeColor   = rand(EYE_COLORS);
  const hairColor  = rand(HAIR_COLORS);
  const hairStyle  = Math.floor(Math.random() * HAIR_BUILDERS.length);
  const isFemale   = Math.random() > 0.5;

  const skinMat  = mat(skinColor, 0.78);
  const shirtMat = mat(shirtColor, 0.85);
  const pantsMat = mat(pantsColor, 0.85);
  const shoeMat  = mat(0x1a1a1a, 0.7);

  const root = new THREE.Group();

  // ── Feet
  const shoeGeo = new THREE.BoxGeometry(0.16, 0.1, 0.26);
  const footL = new THREE.Mesh(shoeGeo, shoeMat);
  const footR = new THREE.Mesh(shoeGeo, shoeMat);
  footL.position.set(-0.115, 0.05, 0);
  footR.position.set( 0.115, 0.05, 0);
  root.add(footL, footR);

  // ── Lower legs
  const lLegGeo = new THREE.BoxGeometry(0.14, 0.38, 0.15);
  const lLegL = new THREE.Mesh(lLegGeo, pantsMat);
  const lLegR = new THREE.Mesh(lLegGeo, pantsMat);
  lLegL.position.set(-0.115, 0.3, 0);
  lLegR.position.set( 0.115, 0.3, 0);
  root.add(lLegL, lLegR);

  // ── Upper legs
  const uLegGeo = new THREE.BoxGeometry(0.165, 0.38, 0.17);
  const uLegL = new THREE.Mesh(uLegGeo, pantsMat);
  const uLegR = new THREE.Mesh(uLegGeo, pantsMat);
  uLegL.position.set(-0.115, 0.67, 0);
  uLegR.position.set( 0.115, 0.67, 0);
  root.add(uLegL, uLegR);

  // ── Torso
  const torsoW = isFemale ? 0.34 : 0.42;
  const torso = new THREE.Mesh(new THREE.BoxGeometry(torsoW, 0.52, 0.24), shirtMat);
  torso.position.set(0, 1.12, 0);
  root.add(torso);

  // ── Upper arms (hanging from shoulders)
  const uArmGeo = new THREE.BoxGeometry(0.12, 0.32, 0.13);
  const uArmL = new THREE.Mesh(uArmGeo, shirtMat);
  const uArmR = new THREE.Mesh(uArmGeo, shirtMat);
  uArmL.position.set(-(torsoW / 2 + 0.08), 1.22, 0);
  uArmR.position.set( (torsoW / 2 + 0.08), 1.22, 0);
  root.add(uArmL, uArmR);

  // ── Lower arms
  const lArmGeo = new THREE.BoxGeometry(0.10, 0.28, 0.11);
  const lArmL = new THREE.Mesh(lArmGeo, skinMat);
  const lArmR = new THREE.Mesh(lArmGeo, skinMat);
  lArmL.position.set(-(torsoW / 2 + 0.08), 0.88, 0);
  lArmR.position.set( (torsoW / 2 + 0.08), 0.88, 0);
  root.add(lArmL, lArmR);

  // ── Neck
  const neck = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.14, 0.14), skinMat);
  neck.position.set(0, 1.43, 0);
  root.add(neck);

  // ── Head
  const headW = isFemale ? 0.3 : 0.33;
  const head = new THREE.Mesh(
    new THREE.BoxGeometry(headW, 0.34, 0.33),
    mat(skinColor, 0.78)
  );
  const headGroup = new THREE.Group();
  headGroup.position.set(0, 1.65, 0);
  headGroup.add(head);
  buildFace(headGroup, skinColor, eyeColor, hairColor, hairStyle);
  root.add(headGroup);

  // Store bone refs for animation
  root.userData.bones = {
    headGroup,
    uArmL, uArmR,
    lArmL, lArmR,
    uLegL, uLegR,
    lLegL, lLegR,
    footL, footR,
  };
  root.userData.animPhase = Math.random() * Math.PI * 2; // random start phase

  return root;
}

// ── CharacterAnimator — called every frame ────────────────────────────────────

const WALK_FREQ   = 2.4;  // Hz (steps per second)
const ARM_SWING   = 0.32; // rad
const LEG_SWING   = 0.38; // rad
const HEAD_BOB    = 0.025; // m

export class CharacterAnimator {
  // Call once per frame for each animated character.
  // mesh: the root group returned by buildDetailedCharacter()
  // speed: movement speed in m/s (0 = idle, >0 = walking)
  // dt: delta time in seconds
  static update(mesh, speed, dt) {
    const b = mesh.userData.bones;
    if (!b) return;

    const phase = mesh.userData.animPhase;
    mesh.userData.animPhase += dt * WALK_FREQ * Math.PI * 2 * clamp(speed / 1.5, 0, 1);

    const t  = phase;
    const sw = clamp(speed / 1.5, 0, 1); // swing intensity 0-1

    // Leg swing (alternating)
    b.uLegL.rotation.x =  Math.sin(t) * LEG_SWING * sw;
    b.uLegR.rotation.x = -Math.sin(t) * LEG_SWING * sw;
    b.lLegL.rotation.x =  Math.max(0, -Math.sin(t)) * LEG_SWING * 0.5 * sw;
    b.lLegR.rotation.x =  Math.max(0,  Math.sin(t)) * LEG_SWING * 0.5 * sw;

    // Arm swing (counter to legs)
    b.uArmL.rotation.x = -Math.sin(t) * ARM_SWING * sw;
    b.uArmR.rotation.x =  Math.sin(t) * ARM_SWING * sw;
    b.lArmL.rotation.x = Math.max(0, Math.sin(t)) * ARM_SWING * 0.4 * sw;
    b.lArmR.rotation.x = Math.max(0,-Math.sin(t)) * ARM_SWING * 0.4 * sw;

    // Head bob
    b.headGroup.position.y = 1.65 + Math.abs(Math.sin(t * 2)) * HEAD_BOB * sw;

    // Idle micro-sway (breathing)
    b.headGroup.rotation.y = Math.sin(t * 0.3) * 0.04;
  }
}
