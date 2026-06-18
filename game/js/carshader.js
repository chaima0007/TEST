import * as THREE from 'three';

// CarShaderAgent — Ronde 21
// Inspiré de: Forza Horizon 5, Gran Turismo 7, Need for Speed Unbound
// Techniques: CubeCamera environment map temps réel, clearcoat shimmer,
//             saleté progressive (crash → roughness ↑, envMap ↓), réparation garage.

export class CarShaderAgent {
  constructor(scene, renderer, vehicle, traffic) {
    this._scene    = scene;
    this._renderer = renderer;
    this._vehicle  = vehicle;
    this._traffic  = traffic;
    this._dirt     = 0;
    this._time     = 0;
    this._frame    = 0;
    this._bodyMat  = null;
    this._chromeMats = [];

    this._buildCubeCamera(scene);
    this._upgradeVehicle();
  }

  _buildCubeCamera(scene) {
    this._cubeRT = new THREE.WebGLCubeRenderTarget(64, {
      format: THREE.RGBAFormat,
      generateMipmaps: true,
      minFilter: THREE.LinearMipmapLinearFilter,
    });
    this._cubeCamera = new THREE.CubeCamera(0.5, 700, this._cubeRT);
    scene.add(this._cubeCamera);
  }

  _upgradeVehicle() {
    const mesh = this._vehicle.mesh;
    if (!mesh) return;

    mesh.traverse(child => {
      if (!child.isMesh || !child.material) return;
      const m = child.material;

      // Body material (high metalness PBR)
      if (m === this._vehicle._bodyMat) {
        m.metalness        = 0.74;
        m.roughness        = 0.20;
        m.envMap           = this._cubeRT.texture;
        m.envMapIntensity  = 1.9;
        m.needsUpdate      = true;
        this._bodyMat      = m;

      // Chrome / hub materials (mirror-like)
      } else if (m.metalness >= 0.8) {
        m.envMap          = this._cubeRT.texture;
        m.envMapIntensity = 2.5;
        m.needsUpdate     = true;
        this._chromeMats.push(m);

      // Cabin / glass: subtle env
      } else if (m.metalness > 0.3) {
        m.envMap          = this._cubeRT.texture;
        m.envMapIntensity = 0.8;
        m.needsUpdate     = true;
      }
    });
  }

  _upgradeTrafficCar(carMesh) {
    if (!carMesh) return;
    carMesh.traverse(child => {
      if (!child.isMesh || !child.material) return;
      const m = child.material;
      if (m.metalness > 0.3 && m.metalness < 0.85 && !m._csUpgraded) {
        m.metalness      = Math.min(0.72, m.metalness + 0.12);
        m.roughness      = Math.max(0.18, m.roughness  - 0.06);
        m.envMap         = this._cubeRT.texture;
        m.envMapIntensity = 0.85;
        m._csUpgraded    = true;
        m.needsUpdate    = true;
      }
    });
  }

  onCrash(intensity) {
    this._dirt = Math.min(1, this._dirt + intensity * 0.22);
    this._applyDirt();
  }

  onRepair() {
    this._dirt = 0;
    this._applyDirt();
  }

  _applyDirt() {
    if (!this._bodyMat) return;
    this._bodyMat.roughness       = 0.20 + this._dirt * 0.62;
    this._bodyMat.envMapIntensity = Math.max(0.25, 1.9 - this._dirt * 1.65);
    this._bodyMat.needsUpdate     = true;
  }

  update(dt, vehicle, dayCycle) {
    this._time  += dt;
    this._frame += 1;

    // Update cube camera position (player car)
    const pos = vehicle.getPosition();
    this._cubeCamera.position.set(pos.x, 1.0, pos.z);

    // Re-render cube map every 45 frames (~0.75s) — cheap 64px × 6 faces
    if (this._frame % 45 === 0) {
      this._cubeCamera.update(this._renderer, this._scene);
    }

    // Upgrade newly spawned traffic cars periodically
    if (this._frame % 90 === 0 && this._traffic) {
      for (const car of this._traffic.cars) {
        if (car.active && car.mesh) this._upgradeTrafficCar(car.mesh);
      }
    }

    // Clearcoat shimmer: micro-oscillation on roughness (pearlescent effect, NFS Unbound)
    if (this._bodyMat && this._dirt < 0.25) {
      const shimmer = Math.sin(this._time * 3.4 + 1.1) * 0.012;
      this._bodyMat.roughness = Math.max(0.12, (0.20 - this._dirt * 0.15) + shimmer);
    }

    // Slow natural cleaning
    this._dirt = Math.max(0, this._dirt - dt * 0.004);

    // Night: reduce reflection intensity (avoid over-bright interior)
    if (this._bodyMat) {
      const nightMult = dayCycle.isNight() ? 0.55 : 1.0;
      const baseEnv   = Math.max(0.25, 1.9 - this._dirt * 1.65);
      this._bodyMat.envMapIntensity = baseEnv * nightMult;
    }
  }

  getDirtLevel()    { return this._dirt; }
  hasEnvMap()       { return !!this._cubeRT; }
}
