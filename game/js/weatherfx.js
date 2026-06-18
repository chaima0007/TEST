import * as THREE from 'three';

// WeatherFXAgent — Ronde 21
// Inspiré de: Cyberpunk 2077, GTA V, Red Dead Redemption 2
// Techniques: pluie volumétrique 3000 particules, flaques PBR réfléchissantes,
//             éclairs dynamiques (flash DOM + PointLight), transition douce.

const RAIN_COUNT = 3000;

export class WeatherFXAgent {
  constructor(scene) {
    this._scene     = scene;
    this._intensity = 0;
    this._target    = 0;
    this._time      = 0;

    this._buildRain(scene);
    this._buildPuddles(scene);
    this._buildLightning(scene);

    this._lightningTimer = 0;
    this._nextLightning  = 10 + Math.random() * 15;
    this._flashVal       = 0;
  }

  _buildRain(scene) {
    const pos = new Float32Array(RAIN_COUNT * 3);
    const vel = new Float32Array(RAIN_COUNT * 3);
    for (let i = 0; i < RAIN_COUNT; i++) {
      pos[i*3]   = (Math.random() - 0.5) * 160;
      pos[i*3+1] = Math.random() * 60;
      pos[i*3+2] = (Math.random() - 0.5) * 160;
      vel[i*3]   = (Math.random() - 0.5) * 2.5;   // dérive vent X
      vel[i*3+1] = -(28 + Math.random() * 16);     // chute
      vel[i*3+2] = (Math.random() - 0.5) * 2.5;
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    this._rainPos    = pos;
    this._rainVel    = vel;
    this._rainPosAttr = geo.attributes.position;

    this._rainMat = new THREE.PointsMaterial({
      color: 0xaabbdd, size: 0.20, sizeAttenuation: true,
      transparent: true, opacity: 0,
      blending: THREE.AdditiveBlending, depthWrite: false,
    });
    this._rainMesh = new THREE.Points(geo, this._rainMat);
    this._rainMesh.renderOrder = 12;
    scene.add(this._rainMesh);
  }

  _buildPuddles(scene) {
    this._puddles = [];
    const spots = [
      [-28,  0], [ 28,  0], [  0, -28], [  0,  28],
      [-55, 55], [ 55, -55], [-18, -65], [ 18,  65],
      [-72, -15], [ 72,  15], [ 0,   0], [-40, -40],
      [ 40,  40], [-80,  0], [ 80,   0], [  0, -80],
    ];
    for (const [x, z] of spots) {
      const w   = 2.5 + Math.random() * 5;
      const d   = w * (0.4 + Math.random() * 0.4);
      const geo = new THREE.PlaneGeometry(w, d);
      const mat = new THREE.MeshStandardMaterial({
        color: 0x0d1e30, metalness: 0.96, roughness: 0.03,
        transparent: true, opacity: 0, depthWrite: false,
        envMapIntensity: 3.0,
      });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.rotation.x = -Math.PI / 2;
      mesh.rotation.z = Math.random() * Math.PI;
      mesh.position.set(x, 0.022, z);
      mesh.renderOrder = 2;
      scene.add(mesh);
      this._puddles.push(mat);
    }
  }

  _buildLightning(scene) {
    this._flashEl = document.createElement('div');
    this._flashEl.style.cssText = `
      position:fixed;inset:0;pointer-events:none;
      background:#c8dcff;opacity:0;z-index:9998;
    `;
    document.body.appendChild(this._flashEl);

    this._lightPt = new THREE.PointLight(0xaabbff, 0, 400);
    this._lightPt.position.set(0, 90, 0);
    scene.add(this._lightPt);
  }

  update(dt, weatherId, playerPos) {
    this._time += dt;

    // Resolve target intensity from weather system ID
    const id = weatherId || 'clear';
    this._target = id === 'storm' ? 1.0 : id === 'rain' ? 0.68 : 0;

    this._intensity += (this._target - this._intensity) * Math.min(1, dt * 1.3);

    // Follow player (keep rain box around them)
    if (playerPos) {
      this._rainMesh.position.set(playerPos.x, 0, playerPos.z);
    }

    // Update rain particles
    this._rainMat.opacity = this._intensity * 0.62;
    if (this._intensity > 0.02) {
      const p = this._rainPos;
      const v = this._rainVel;
      for (let i = 0; i < RAIN_COUNT; i++) {
        p[i*3]   += v[i*3]   * dt;
        p[i*3+1] += v[i*3+1] * dt;
        p[i*3+2] += v[i*3+2] * dt;
        if (p[i*3+1] < -1) {
          p[i*3]   = (Math.random() - 0.5) * 160;
          p[i*3+1] = 56 + Math.random() * 8;
          p[i*3+2] = (Math.random() - 0.5) * 160;
        }
      }
      this._rainPosAttr.needsUpdate = true;
    }

    // Puddles appear as rain intensifies
    const puddleTarget = this._intensity * 0.72;
    for (const mat of this._puddles) {
      mat.opacity += (puddleTarget - mat.opacity) * dt * 0.7;
    }

    // Lightning (only when raining enough)
    if (this._intensity > 0.25) {
      this._lightningTimer += dt;
      if (this._lightningTimer >= this._nextLightning) {
        this._lightningTimer = 0;
        this._nextLightning  = 4 + Math.random() * 20 / this._intensity;
        this._flashVal       = 1;
        // Move lightning strike position randomly
        this._lightPt.position.set(
          (Math.random() - 0.5) * 200,
          80,
          (Math.random() - 0.5) * 200
        );
      }
    }

    // Flash decay
    if (this._flashVal > 0) {
      this._flashVal -= dt * 9;
      if (this._flashVal < 0) this._flashVal = 0;
      const f = Math.max(0, this._flashVal);
      this._flashEl.style.opacity = String((f * 0.22).toFixed(3));
      this._lightPt.intensity     = f * 10;
    } else {
      this._flashEl.style.opacity = '0';
      this._lightPt.intensity     = 0;
    }
  }

  getIntensity()    { return this._intensity; }
  isActive()        { return this._intensity > 0.08; }
  getLightningFlash() { return this._flashVal; }
}
