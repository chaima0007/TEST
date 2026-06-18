// streetfurniture.js — Mobilier urbain procédural
// Bollards (avec colliders AABB), bancs, poubelles — répartis sur trottoirs.
// Prend un tableau `colliders` en entrée pour y pousser les colliders bollards.

import * as THREE from 'three';

const BOLLARD_R = 0.18;
const BOLLARD_H = 0.9;
const BENCH_MAT_COLOR = 0x8b6914;
const TRASH_COLOR = 0x336633;

export class StreetFurnitureSystem {
  constructor(scene, roadXs, roadZs, colliders) {
    this._bollardCount = 0;
    this._benchCount   = 0;
    this._trashCount   = 0;

    this._buildBollards(scene, roadXs, roadZs, colliders);
    this._buildBenches(scene, roadXs, roadZs);
    this._buildTrash(scene, roadXs, roadZs);
  }

  getTotalCount()   { return this._bollardCount + this._benchCount + this._trashCount; }
  getBollardCount() { return this._bollardCount; }
  getBenchCount()   { return this._benchCount; }

  _buildBollards(scene, roadXs, roadZs, colliders) {
    const geo = new THREE.CylinderGeometry(BOLLARD_R, BOLLARD_R + 0.04, BOLLARD_H, 7);
    const mat = new THREE.MeshLambertMaterial({ color: 0xddcc44 });
    const hw = BOLLARD_R + 0.05; // collider half-extent

    // 4 croisements intérieurs × 4 coins = 16 bollards
    for (const rx of [roadXs[1], roadXs[3]]) {
      for (const rz of [roadZs[1], roadZs[3]]) {
        for (const [dx, dz] of [[-1,-1],[-1,1],[1,-1],[1,1]]) {
          const x = rx + dx * 5.8;
          const z = rz + dz * 5.8;
          const mesh = new THREE.Mesh(geo, mat);
          mesh.position.set(x, BOLLARD_H / 2, z);
          mesh.castShadow = true;
          scene.add(mesh);
          colliders.push({ x, z, halfWidth: hw, halfDepth: hw });
          this._bollardCount++;
        }
      }
    }
  }

  _buildBenches(scene, roadXs, roadZs) {
    const seatGeo = new THREE.BoxGeometry(1.6, 0.1, 0.55);
    const backGeo = new THREE.BoxGeometry(1.6, 0.4, 0.08);
    const mat = new THREE.MeshLambertMaterial({ color: BENCH_MAT_COLOR });

    for (const rz of [roadZs[1], roadZs[2], roadZs[3]]) {
      for (let bi = 0; bi < roadXs.length - 1; bi++) {
        const cx = (roadXs[bi] + roadXs[bi + 1]) / 2;
        const bz = rz + 6.5;

        const seat = new THREE.Mesh(seatGeo, mat);
        seat.position.set(cx, 0.5, bz);
        scene.add(seat);

        const back = new THREE.Mesh(backGeo, mat);
        back.position.set(cx, 0.8, bz + 0.24);
        scene.add(back);

        this._benchCount++;
      }
    }
  }

  _buildTrash(scene, roadXs, roadZs) {
    const geo = new THREE.CylinderGeometry(0.22, 0.2, 0.75, 8);
    const mat = new THREE.MeshLambertMaterial({ color: TRASH_COLOR });

    for (const rz of [roadZs[1], roadZs[2], roadZs[3]]) {
      for (let bi = 0; bi < roadXs.length - 1; bi++) {
        const cx = (roadXs[bi] + roadXs[bi + 1]) / 2;
        const mesh = new THREE.Mesh(geo, mat);
        mesh.position.set(cx + 1.2, 0.375, rz + 6.5);
        scene.add(mesh);
        this._trashCount++;
      }
    }
  }
}
