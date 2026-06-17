import * as THREE from 'three';

const TRIGGER_SPEED_KMH = 80;
const DETECT_RADIUS     = 14;
const FLASH_DURATION    = 0.4;
const MAX_CAMERAS       = 7;

function buildCamMesh() {
  const group  = new THREE.Group();
  const dark   = new THREE.MeshStandardMaterial({ color: 0x222222, metalness: 0.7 });
  const flashM = new THREE.MeshStandardMaterial({ color: 0xffcc00, emissive: 0xff8800, emissiveIntensity: 0.5 });

  const pole = new THREE.Mesh(new THREE.BoxGeometry(0.22, 4.5, 0.22), dark);
  pole.position.y = 2.25;
  group.add(pole);

  const arm = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.14, 1.6), dark);
  arm.position.set(0, 4.55, -0.75);
  group.add(arm);

  const body = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.55, 0.65), dark);
  body.position.set(0, 4.55, -1.55);
  group.add(body);

  const lens = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.22, 0.12), flashM);
  lens.position.set(0, 4.55, -1.9);
  group.add(lens);
  group.userData.lens = lens;

  return group;
}

export class SpeedCamSystem {
  constructor(scene, world) {
    this.scene    = scene;
    this._cameras = [];
    this._cooldowns = new Map();

    if (!world || !world.roadLines) return;

    const { xs, zs } = world.roadLines;
    const candidates = [];
    for (let i = 1; i < xs.length - 1; i++) {
      for (let j = 1; j < zs.length - 1; j++) {
        if (Math.random() < 0.4) candidates.push({ x: xs[i], z: zs[j] });
      }
    }
    candidates.sort(() => Math.random() - 0.5);
    const picked = candidates.slice(0, MAX_CAMERAS);

    for (const p of picked) {
      const mesh = buildCamMesh();
      const offset = ROAD_SIDE_OFFSET();
      mesh.position.set(p.x + offset.x, 0, p.z + offset.z);
      mesh.rotation.y = Math.random() > 0.5 ? 0 : Math.PI / 2;
      scene.add(mesh);
      this._cameras.push({ mesh, x: p.x, z: p.z, flashTimer: 0 });
    }
  }

  getCameraPositions() {
    return this._cameras.map(c => ({ x: c.x, z: c.z }));
  }

  // Returns true if a new violation was just triggered this frame
  update(dt, vehicle, hud) {
    if (!vehicle) return false;
    const pos     = vehicle.getPosition();
    const speedKmh = Math.abs(vehicle.getSpeedKmh());
    let triggered = false;

    for (const cam of this._cameras) {
      // Flash animation
      if (cam.flashTimer > 0) {
        cam.flashTimer -= dt;
        cam.mesh.userData.lens.material.emissiveIntensity = cam.flashTimer > 0.18 ? 4.0 : 0.5;
      } else {
        cam.mesh.userData.lens.material.emissiveIntensity = 0.5;
      }

      const key  = `${cam.x}|${cam.z}`;
      const dist = Math.hypot(pos.x - cam.x, pos.z - cam.z);
      const cdLeft = this._cooldowns.get(key) || 0;

      if (cdLeft > 0) {
        this._cooldowns.set(key, cdLeft - dt);
        continue;
      }

      if (dist < DETECT_RADIUS && speedKmh > TRIGGER_SPEED_KMH) {
        cam.flashTimer = FLASH_DURATION;
        this._cooldowns.set(key, 8); // 8s cooldown per camera
        if (hud) hud.showMessage(`RADAR ${Math.round(speedKmh)} km/h — Limite 80 !`, 2000);
        triggered = true;
      }
    }
    return triggered;
  }
}

function ROAD_SIDE_OFFSET() {
  const side = Math.random() > 0.5 ? 1 : -1;
  return Math.random() > 0.5
    ? { x: side * 6, z: 0 }
    : { x: 0, z: side * 6 };
}
