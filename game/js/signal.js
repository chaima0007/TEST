// signal.js — Feux de circulation procéduraux avec état rouge/jaune/vert
// Les 16 croisements intérieurs de la grille ont chacun un feu cycle 20 s.
// Décalages de phase pour éviter que tous les feux changent en même temps.
// Infractions détectables par isViolation() → intégration avec le wanted.

import * as THREE from 'three';

const CYCLE      = 20; // durée d'un cycle complet (secondes)
const GREEN_END  = 10; // 0-10 s → vert
const YELLOW_END = 12; // 10-12 s → jaune   12-20 s → rouge

function _phase(time, offset) {
  return (time + offset) % CYCLE;
}
function _stateAt(time, offset) {
  const p = _phase(time, offset);
  if (p < GREEN_END)  return 'green';
  if (p < YELLOW_END) return 'yellow';
  return 'red';
}

export class SignalAgent {
  constructor(scene, roadXs, roadZs) {
    this._time    = 0;
    this._signals = [];
    this._build(scene, roadXs, roadZs);
  }

  _build(scene, roadXs, roadZs) {
    const poleMat  = new THREE.MeshLambertMaterial({ color: 0x2a2a2a });
    const houseGeo = new THREE.BoxGeometry(0.28, 1.05, 0.22);
    const houseMat = new THREE.MeshLambertMaterial({ color: 0x111111 });
    const poleGeo  = new THREE.CylinderGeometry(0.07, 0.09, 3.6, 6);
    const litGeo   = new THREE.BoxGeometry(0.18, 0.2, 0.15);

    // Croisements intérieurs uniquement : roadXs[1..N-2] × roadZs[1..N-2]
    for (let i = 1; i < roadXs.length - 1; i++) {
      for (let j = 1; j < roadZs.length - 1; j++) {
        const rx     = roadXs[i];
        const rz     = roadZs[j];
        const cx     = rx + 6;
        const cz     = rz + 6;
        const offset = (i * 5 + j * 3) % CYCLE;

        const pole = new THREE.Mesh(poleGeo, poleMat);
        pole.position.set(cx, 1.8, cz);
        scene.add(pole);

        const house = new THREE.Mesh(houseGeo, houseMat);
        house.position.set(cx, 3.8, cz);
        scene.add(house);

        // Rouge (haut), jaune (milieu), vert (bas)
        const redMat = new THREE.MeshStandardMaterial({
          color: 0x991100, emissive: new THREE.Color(0x000000), emissiveIntensity: 0,
        });
        const yellowMat = new THREE.MeshStandardMaterial({
          color: 0x886600, emissive: new THREE.Color(0x000000), emissiveIntensity: 0,
        });
        const greenMat = new THREE.MeshStandardMaterial({
          color: 0x006622, emissive: new THREE.Color(0x00ff44), emissiveIntensity: 1.8,
        });

        for (const [mat, dy] of [[redMat, 0.35], [yellowMat, 0], [greenMat, -0.35]]) {
          const l = new THREE.Mesh(litGeo, mat);
          l.position.set(cx, 3.8 + dy, cz - 0.12);
          scene.add(l);
        }

        this._signals.push({ x: rx, z: rz, offset, state: 'green', redMat, yellowMat, greenMat });
      }
    }
  }

  update(dt) {
    this._time += dt;
    for (const sig of this._signals) {
      const state = _stateAt(this._time, sig.offset);
      sig.state = state;
      const isR = state === 'red';
      const isY = state === 'yellow';
      const isG = state === 'green';

      sig.redMat.emissiveIntensity    = isR ? 1.8 : 0;
      sig.yellowMat.emissiveIntensity = isY ? 1.8 : 0;
      sig.greenMat.emissiveIntensity  = isG ? 1.8 : 0;
      sig.redMat.emissive.setHex(    isR ? 0xff2200 : 0x000000);
      sig.yellowMat.emissive.setHex( isY ? 0xffaa00 : 0x000000);
      sig.greenMat.emissive.setHex(  isG ? 0x00ff44 : 0x000000);
    }
  }

  // Retourne true si le joueur grille un feu rouge à cette position et vitesse.
  isViolation(x, z, speedKmh) {
    if (speedKmh < 15) return false;
    for (const sig of this._signals) {
      if (sig.state !== 'red') continue;
      if (Math.abs(x - sig.x) < 5.5 && Math.abs(z - sig.z) < 5.5) return true;
    }
    return false;
  }

  getSignalCount() { return this._signals.length; }
  getSignals()     { return this._signals; }
}
