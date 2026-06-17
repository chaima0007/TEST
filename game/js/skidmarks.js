import * as THREE from 'three';

const MAX_MARKS = 180;      // max segments before oldest are reused
const MARK_WIDTH = 0.38;    // m — matches tire width
const MARK_SPACING = 0.8;   // m — minimum distance before new segment
const REAR_TIRE_LOCAL = [
  { x: -1.0, z: -1.4 }, // rear-left
  { x:  1.0, z: -1.4 }, // rear-right
];

const _sharedMaterial = new THREE.MeshBasicMaterial({
  color: 0x111111,
  transparent: true,
  opacity: 0.65,
  depthWrite: false,
});

export class SkidMarkSystem {
  constructor(scene) {
    this._pool = [];
    this._poolIndex = 0;
    this._lastPos = {};

    for (let i = 0; i < MAX_MARKS; i++) {
      const geometry = new THREE.PlaneGeometry(MARK_WIDTH, MARK_SPACING);
      const mesh = new THREE.Mesh(geometry, _sharedMaterial);
      mesh.rotation.x = -Math.PI / 2;
      mesh.position.y = -100; // hidden initially
      scene.add(mesh);
      this._pool.push(mesh);
    }
  }

  update(dt, vehicle, isDrifting) {
    if (!isDrifting) {
      this._lastPos = {};
      return;
    }

    const pos = vehicle.getPosition();
    const heading = vehicle.getHeading();
    const cosH = Math.cos(heading);
    const sinH = Math.sin(heading);

    for (let t = 0; t < REAR_TIRE_LOCAL.length; t++) {
      const tire = REAR_TIRE_LOCAL[t];

      // Transform local tire offset to world space
      const worldX = pos.x + tire.x * cosH + tire.z * sinH;
      const worldZ = pos.z - tire.x * sinH + tire.z * cosH;

      const last = this._lastPos[t];
      if (last !== undefined) {
        const dx = worldX - last.x;
        const dz = worldZ - last.z;
        const dist = Math.sqrt(dx * dx + dz * dz);
        if (dist < MARK_SPACING) continue;
      }

      // Place a mark at this tire position
      const mesh = this._pool[this._poolIndex % MAX_MARKS];
      this._poolIndex++;

      mesh.position.x = worldX;
      mesh.position.y = 0.025;
      mesh.position.z = worldZ;
      mesh.rotation.y = heading;

      this._lastPos[t] = { x: worldX, z: worldZ };
    }
  }
}
