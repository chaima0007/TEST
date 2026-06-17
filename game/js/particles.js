import * as THREE from 'three';

// Rear tire local offsets (from vehicle.js geometry)
const REAR_TIRE_LOCAL = [
  { x: -1.0, z: -1.4 }, // rear-left
  { x:  1.0, z: -1.4 }, // rear-right
];
const MAX_PARTICLES = 300;
const PARTICLE_LIFETIME = 0.75; // seconds
const EMIT_RATE = 25; // particles/second/tire while drifting

export class TireSmokeSystem {
  constructor(scene) {
    this._positions = new Float32Array(MAX_PARTICLES * 3);
    this._lifetimes = new Float32Array(MAX_PARTICLES);
    this._velocities = new Float32Array(MAX_PARTICLES * 3);

    // Start all particles hidden below the scene
    for (let i = 0; i < MAX_PARTICLES; i++) {
      this._positions[i * 3 + 1] = -100;
    }

    const geometry = new THREE.BufferGeometry();
    const posAttr = new THREE.BufferAttribute(this._positions, 3);
    posAttr.setUsage(THREE.DynamicDrawUsage);
    geometry.setAttribute('position', posAttr);

    const material = new THREE.PointsMaterial({
      color: 0xcccccc,
      size: 1.4,
      transparent: true,
      opacity: 0.5,
      depthWrite: false,
      sizeAttenuation: true,
    });

    this._points = new THREE.Points(geometry, material);
    scene.add(this._points);

    // Fractional particle accumulator per tire
    this._emitAccum = [0, 0];
  }

  update(dt, vehicle, isDrifting) {
    const pos = vehicle.mesh.position;
    const heading = vehicle.getHeading();
    const cosH = Math.cos(heading);
    const sinH = Math.sin(heading);

    // Emit new particles from rear tires when drifting
    if (isDrifting) {
      for (let t = 0; t < REAR_TIRE_LOCAL.length; t++) {
        const tire = REAR_TIRE_LOCAL[t];
        this._emitAccum[t] += EMIT_RATE * dt;

        while (this._emitAccum[t] >= 1) {
          this._emitAccum[t] -= 1;
          this._spawnParticle(pos, tire, cosH, sinH);
        }
      }
    }

    // Update all particles
    for (let i = 0; i < MAX_PARTICLES; i++) {
      if (this._lifetimes[i] <= 0) continue;

      this._lifetimes[i] -= dt;

      const pi = i * 3;
      // Apply gravity to vy
      this._velocities[pi + 1] -= 2.5 * dt;

      // Integrate position
      this._positions[pi]     += this._velocities[pi]     * dt;
      this._positions[pi + 1] += this._velocities[pi + 1] * dt;
      this._positions[pi + 2] += this._velocities[pi + 2] * dt;

      // Hide expired particles
      if (this._lifetimes[i] <= 0) {
        this._positions[pi + 1] = -100;
      }
    }

    this._points.geometry.attributes.position.needsUpdate = true;
  }

  _spawnParticle(pos, tire, cosH, sinH) {
    // Find a dead slot
    let slot = -1;
    for (let i = 0; i < MAX_PARTICLES; i++) {
      if (this._lifetimes[i] <= 0) {
        slot = i;
        break;
      }
    }
    if (slot === -1) return; // pool exhausted

    // Transform local tire offset to world space
    const worldX = pos.x + tire.x * cosH + tire.z * sinH;
    const worldZ = pos.z - tire.x * sinH + tire.z * cosH;

    const pi = slot * 3;
    this._positions[pi]     = worldX;
    this._positions[pi + 1] = 0.3;
    this._positions[pi + 2] = worldZ;

    // Random velocity
    this._velocities[pi]     = (Math.random() - 0.5) * 3.0; // ±1.5
    this._velocities[pi + 1] = 1.0 + Math.random() * 1.5;   // 1.0–2.5
    this._velocities[pi + 2] = (Math.random() - 0.5) * 3.0; // ±1.5

    this._lifetimes[slot] = PARTICLE_LIFETIME;
  }
}

// Étincelles oranges/jaunes émises lors d'une collision forte
const MAX_SPARKS = 120;
const SPARK_LIFETIME = 0.55;

export class SparkSystem {
  constructor(scene) {
    this._pos = new Float32Array(MAX_SPARKS * 3);
    this._vel = new Float32Array(MAX_SPARKS * 3);
    this._life = new Float32Array(MAX_SPARKS);
    for (let i = 0; i < MAX_SPARKS; i++) this._pos[i * 3 + 1] = -100;

    const geo = new THREE.BufferGeometry();
    const attr = new THREE.BufferAttribute(this._pos, 3);
    attr.setUsage(THREE.DynamicDrawUsage);
    geo.setAttribute('position', attr);
    const mat = new THREE.PointsMaterial({ color: 0xff8800, size: 0.55, transparent: true, opacity: 0.9, depthWrite: false, sizeAttenuation: true });
    this._points = new THREE.Points(geo, mat);
    scene.add(this._points);
  }

  // Emit burst at world position (x, y, z), intensity 0-1
  emit(x, z, intensity) {
    const count = Math.round(6 + intensity * 22);
    const speed = 4 + intensity * 10;
    for (let i = 0; i < count; i++) {
      let slot = -1;
      for (let j = 0; j < MAX_SPARKS; j++) {
        if (this._life[j] <= 0) { slot = j; break; }
      }
      if (slot === -1) break;
      const p = slot * 3;
      this._pos[p]     = x;
      this._pos[p + 1] = 0.6;
      this._pos[p + 2] = z;
      const angle = Math.random() * Math.PI * 2;
      const vUp   = 1.5 + Math.random() * 3;
      this._vel[p]     = Math.cos(angle) * speed * Math.random();
      this._vel[p + 1] = vUp;
      this._vel[p + 2] = Math.sin(angle) * speed * Math.random();
      this._life[slot] = SPARK_LIFETIME * (0.5 + Math.random() * 0.5);
    }
  }

  update(dt) {
    for (let i = 0; i < MAX_SPARKS; i++) {
      if (this._life[i] <= 0) continue;
      this._life[i] -= dt;
      const p = i * 3;
      this._pos[p]     += this._vel[p] * dt;
      this._pos[p + 1] += this._vel[p + 1] * dt;
      this._pos[p + 2] += this._vel[p + 2] * dt;
      this._vel[p + 1] -= 9.8 * dt; // gravity
      if (this._life[i] <= 0) this._pos[p + 1] = -100;
    }
    this._points.geometry.attributes.position.needsUpdate = true;
  }
}
