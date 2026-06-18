import * as THREE from 'three';

// AtmosphereAgent — Ronde 21
// Inspiré de: Red Dead Redemption 2, Cyberpunk 2077, Horizon Forbidden West, GTA VI
// Techniques: gradient sky shader GLSL, étoiles dynamiques, god rays volumétriques,
//             lune, halos néon au sol, sync fog/background couleur temps réel.

const SKY_VERT = `
varying vec3 vWorldPos;
void main() {
  vWorldPos = position;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
`;

const SKY_FRAG = `
uniform vec3 uZenith;
uniform vec3 uMid;
uniform vec3 uHorizon;
varying vec3 vWorldPos;
void main() {
  float t = clamp((vWorldPos.y / 480.0 + 1.0) / 2.0, 0.0, 1.0);
  vec3 col;
  if (t > 0.52) {
    col = mix(uMid, uZenith, (t - 0.52) / 0.48);
  } else {
    col = mix(uHorizon, uMid, t / 0.52);
  }
  gl_FragColor = vec4(col, 1.0);
}
`;

// Palettes horaires (r, g, b en 0-1 pour ShaderMaterial)
const P = {
  day:    { z: [0.042, 0.10, 0.36], m: [0.10, 0.35, 0.69], h: [0.50, 0.81, 0.96] },
  golden: { z: [0.04, 0.02, 0.20], m: [0.67, 0.20, 0.00], h: [1.00, 0.42, 0.07] },
  sunset: { z: [0.03, 0.00, 0.16], m: [0.40, 0.07, 0.50], h: [1.00, 0.20, 0.00] },
  night:  { z: [0.00, 0.01, 0.03], m: [0.00, 0.02, 0.06], h: [0.01, 0.05, 0.10] },
  dawn:   { z: [0.00, 0.06, 0.19], m: [0.80, 0.27, 0.00], h: [1.00, 0.55, 0.20] },
};

function pv3(arr) { return new THREE.Vector3(arr[0], arr[1], arr[2]); }
function pc(arr)  { return new THREE.Color(arr[0], arr[1], arr[2]); }

function lerpPalKey(a, b, t) {
  return {
    z: a.z.map((v, i) => v + (b.z[i] - v) * t),
    m: a.m.map((v, i) => v + (b.m[i] - v) * t),
    h: a.h.map((v, i) => v + (b.h[i] - v) * t),
  };
}

function getPalette(h) {
  if (h >= 8  && h < 16)  return P.day;
  if (h >= 16 && h < 18.5) return P.golden;
  if (h >= 18.5 && h < 21) return P.sunset;
  if (h >= 21 || h < 5.5)  return P.night;
  // dawn 5.5-8: lerp from night→day via dawn
  const t = Math.min(1, (h - 5.5) / 2.5);
  return lerpPalKey(P.dawn, P.day, t);
}

export class AtmosphereAgent {
  constructor(scene) {
    this._scene = scene;
    this._time  = 0;

    this._buildSky(scene);
    this._buildStars(scene);
    this._buildGodRays(scene);
    this._buildNeonHalos(scene);

    this._starOpacity  = 0;
    this._rayIntensity = 0;
  }

  _buildSky(scene) {
    const geo = new THREE.SphereGeometry(480, 24, 16);
    this._skyUniforms = {
      uZenith:  { value: pv3(P.day.z) },
      uMid:     { value: pv3(P.day.m) },
      uHorizon: { value: pv3(P.day.h) },
    };
    const mat = new THREE.ShaderMaterial({
      vertexShader:   SKY_VERT,
      fragmentShader: SKY_FRAG,
      uniforms:       this._skyUniforms,
      side:           THREE.BackSide,
      depthWrite:     false,
      fog:            false,
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.renderOrder = -10;
    scene.add(mesh);
    this._skyMesh = mesh;
  }

  _buildStars(scene) {
    const N   = 2200;
    const pos = new Float32Array(N * 3);
    for (let i = 0; i < N; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi   = Math.acos(1 - Math.random() * 0.97);
      const r     = 448;
      pos[i*3]   = r * Math.sin(phi) * Math.cos(theta);
      pos[i*3+1] = r * Math.cos(phi);
      pos[i*3+2] = r * Math.sin(phi) * Math.sin(theta);
    }
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));

    this._starsMat = new THREE.PointsMaterial({
      color: 0xddeeff, size: 0.85, sizeAttenuation: true,
      transparent: true, opacity: 0, fog: false, depthWrite: false,
    });
    this._stars = new THREE.Points(geo, this._starsMat);
    this._stars.renderOrder = -9;
    scene.add(this._stars);

    // Lune
    const moonGeo = new THREE.SphereGeometry(5, 14, 10);
    this._moonMat = new THREE.MeshBasicMaterial({
      color: 0xeef8ff, transparent: true, opacity: 0, fog: false,
    });
    this._moon = new THREE.Mesh(moonGeo, this._moonMat);
    this._moon.position.set(-140, 210, -320);
    this._moon.renderOrder = -8;
    scene.add(this._moon);
  }

  _buildGodRays(scene) {
    this._godRays = [];
    const SUN = new THREE.Vector3(60, 100, 40).normalize();
    for (let i = 0; i < 6; i++) {
      const geo = new THREE.PlaneGeometry(5 + i * 10, 160 + i * 55);
      const mat = new THREE.MeshBasicMaterial({
        color: 0xfff6d0, transparent: true, opacity: 0,
        blending: THREE.AdditiveBlending, depthWrite: false,
        side: THREE.DoubleSide, fog: false,
      });
      const mesh = new THREE.Mesh(geo, mat);
      const dist = 100 + i * 22;
      mesh.position.copy(SUN.clone().multiplyScalar(dist));
      mesh.lookAt(new THREE.Vector3(0, 0, 0));
      mesh.rotation.z = (i / 6) * Math.PI;
      mesh.renderOrder = -7;
      scene.add(mesh);
      this._godRays.push({ mesh, mat, base: 0.055 - i * 0.007 });
    }
  }

  _buildNeonHalos(scene) {
    this._halos = [];
    const geo = new THREE.PlaneGeometry(4.5, 4.5);
    for (let i = 0; i < 32; i++) {
      const mat = new THREE.MeshBasicMaterial({
        color: 0xfff5b0, transparent: true, opacity: 0,
        blending: THREE.AdditiveBlending, depthWrite: false, fog: false,
      });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.rotation.x = -Math.PI / 2;
      mesh.position.y = 0.06;
      mesh.visible    = false;
      mesh.renderOrder = -5;
      scene.add(mesh);
      this._halos.push(mesh);
    }
  }

  registerLamps(streetLamps) {
    for (let i = 0; i < Math.min(streetLamps.length, this._halos.length); i++) {
      const lamp = streetLamps[i];
      const halo = this._halos[i];
      halo.position.set(lamp.position.x, 0.06, lamp.position.z);
      halo.visible = true;
    }
  }

  update(dt, dayCycle) {
    this._time += dt;
    const ts    = dayCycle.getTimeString();
    const parts = ts ? ts.split(':') : ['12', '00'];
    const h     = parseInt(parts[0], 10) + (parseInt(parts[1], 10) || 0) / 60;
    const isNight = dayCycle.isNight();

    const pal = getPalette(h);

    // Sky uniforms: lerp toward target
    const speed = dt * 0.9;
    const u     = this._skyUniforms;
    u.uZenith.value.lerp(pv3(pal.z), speed);
    u.uMid.value.lerp(   pv3(pal.m), speed);
    u.uHorizon.value.lerp(pv3(pal.h), speed);

    // Sync scene background + fog to horizon color
    const hc = pc(pal.h);
    this._scene.background.lerp(hc, dt * 1.2);
    this._scene.fog.color.lerp(hc, dt * 1.2);

    // Stars + moon
    const starTarget = (isNight || h < 6 || h >= 20.5) ? 0.95 : 0;
    this._starOpacity += (starTarget - this._starOpacity) * dt * 1.8;
    this._starsMat.opacity = this._starOpacity;
    this._moonMat.opacity  = this._starOpacity * 0.92;

    // God rays: visible by day, peak at dawn/sunset
    const isDawn   = h >= 5.5 && h < 8.5;
    const isSunset = h >= 15.5 && h < 20;
    const rayStr   = isNight ? 0 : (isDawn || isSunset) ? 1 : 0.3;
    this._rayIntensity += (rayStr - this._rayIntensity) * dt * 1.5;
    for (let i = 0; i < this._godRays.length; i++) {
      const ray   = this._godRays[i];
      const pulse = 0.75 + Math.sin(this._time * 0.38 + i * 1.05) * 0.25;
      ray.mat.opacity += (ray.base * this._rayIntensity * pulse - ray.mat.opacity) * dt * 2.5;
    }

    // Neon halos: night only
    const haloTarget = isNight ? 0.14 : 0;
    for (const halo of this._halos) {
      if (!halo.visible) continue;
      halo.material.opacity += (haloTarget - halo.material.opacity) * dt * 2;
    }
  }

  getStarOpacity()   { return this._starOpacity; }
  getRayIntensity()  { return this._rayIntensity; }
}
