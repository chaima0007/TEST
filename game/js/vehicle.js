import * as THREE from 'three';

// --- Tuning constants (arcade-style, not a real physics sim) ---------------
const MAX_SPEED_KMH = 150;          // top speed, forward
const MAX_SPEED_MS = MAX_SPEED_KMH / 3.6;
const MAX_REVERSE_MS = 45 / 3.6;    // reverse is slower than forward
const ACCEL = 16;                   // m/s^2 while accelerating
const BRAKE_DECEL = 26;             // m/s^2 while braking/reversing input opposes motion
const HANDBRAKE_DECEL = 38;         // m/s^2 while space is held
const NATURAL_FRICTION = 6;         // m/s^2 drag when no throttle input
const MAX_STEER_RATE = 2.6;         // rad/s of steering angle change
const MAX_STEER_ANGLE = 0.55;       // rad, max front-wheel steer angle
const WHEELBASE = 2.6;              // meters, used for simple bicycle-model turning
const COLLISION_RADIUS = 1.35;      // approximate car footprint as a circle for collision response
const RESTITUTION = 0.25;           // how much speed "bounces back" on hard impact

function clamp(v, min, max) {
  return Math.max(min, Math.min(max, v));
}

// Build a realistic low-poly car mesh with lights, windows, mirrors, door lines.
function buildCarMesh() {
  const group = new THREE.Group();

  const bodyMat  = new THREE.MeshStandardMaterial({ color: 0xcc2222, metalness: 0.45, roughness: 0.40 });
  const cabinMat = new THREE.MeshStandardMaterial({ color: 0x0a0e18, metalness: 0.15, roughness: 0.35 });
  const wheelMat = new THREE.MeshStandardMaterial({ color: 0x0a0a0a, metalness: 0.05, roughness: 0.85 });
  const hubMat   = new THREE.MeshStandardMaterial({ color: 0xcccccc, metalness: 0.8,  roughness: 0.25 });
  const glassMat = new THREE.MeshStandardMaterial({ color: 0x4477aa, metalness: 0.1,  roughness: 0.05, transparent: true, opacity: 0.42, depthWrite: false });
  const chromeMat= new THREE.MeshStandardMaterial({ color: 0xdddddd, metalness: 0.9,  roughness: 0.15 });
  const darkMat  = new THREE.MeshStandardMaterial({ color: 0x080808, metalness: 0.1,  roughness: 0.9  });
  const headlightMat = new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 0, roughness: 0.05, metalness: 0.1 });
  const taillightMat = new THREE.MeshStandardMaterial({ color: 0xff1100, emissive: 0xff1100, emissiveIntensity: 0, roughness: 0.05, metalness: 0.1 });

  // ── Corps principal ─────────────────────────────────────────────────
  const body = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.60, 4.2), bodyMat);
  body.position.y = 0.56;
  body.castShadow = true;
  group.add(body);

  // ── Capot avant (légèrement surélevé) ──────────────────────────────
  const hood = new THREE.Mesh(new THREE.BoxGeometry(1.84, 0.08, 1.50), bodyMat);
  hood.position.set(0, 0.90, 1.20);
  hood.castShadow = true;
  group.add(hood);

  // ── Coffre arrière ──────────────────────────────────────────────────
  const trunk = new THREE.Mesh(new THREE.BoxGeometry(1.84, 0.10, 0.80), bodyMat);
  trunk.position.set(0, 0.90, -1.65);
  group.add(trunk);

  // ── Habitacle (toit) ────────────────────────────────────────────────
  const cabin = new THREE.Mesh(new THREE.BoxGeometry(1.60, 0.52, 2.0), cabinMat);
  cabin.position.set(0, 1.02, -0.25);
  cabin.castShadow = true;
  group.add(cabin);

  // ── Pare-brise avant ────────────────────────────────────────────────
  const windshield = new THREE.Mesh(new THREE.BoxGeometry(1.48, 0.44, 0.08), glassMat);
  windshield.position.set(0, 1.00, 0.77);
  windshield.rotation.x = -0.25;
  group.add(windshield);

  // ── Vitre arrière ───────────────────────────────────────────────────
  const rearGlass = new THREE.Mesh(new THREE.BoxGeometry(1.44, 0.40, 0.08), glassMat);
  rearGlass.position.set(0, 0.98, -1.23);
  rearGlass.rotation.x = 0.25;
  group.add(rearGlass);

  // ── Vitres latérales ────────────────────────────────────────────────
  for (const x of [-0.805, 0.805]) {
    const sideWin = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.36, 1.60), glassMat);
    sideWin.position.set(x, 1.02, -0.20);
    group.add(sideWin);
  }

  // ── Lignes de portes (creux sombre sur les flancs) ──────────────────
  for (const x of [-0.96, 0.96]) {
    const doorLine = new THREE.Mesh(new THREE.BoxGeometry(0.018, 0.40, 1.95), darkMat);
    doorLine.position.set(x, 0.56, 0.05);
    group.add(doorLine);
    // Poignée de porte
    const handle = new THREE.Mesh(new THREE.BoxGeometry(0.020, 0.05, 0.22), chromeMat);
    handle.position.set(x, 0.72, 0.15);
    group.add(handle);
  }

  // ── Pare-chocs avant ────────────────────────────────────────────────
  const bumperF = new THREE.Mesh(new THREE.BoxGeometry(1.85, 0.28, 0.28), bodyMat);
  bumperF.position.set(0, 0.36, 2.17);
  group.add(bumperF);

  // ── Calandre avant ──────────────────────────────────────────────────
  const grille = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.16, 0.12), darkMat);
  grille.position.set(0, 0.46, 2.22);
  group.add(grille);
  // Barre de calandre (chrome)
  const grilleBar = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.030, 0.14), chromeMat);
  grilleBar.position.set(0, 0.52, 2.21);
  group.add(grilleBar);

  // ── Phares avant ────────────────────────────────────────────────────
  for (const x of [-0.70, 0.70]) {
    const hl = new THREE.Mesh(new THREE.BoxGeometry(0.30, 0.14, 0.10), headlightMat);
    hl.position.set(x, 0.60, 2.18);
    group.add(hl);
    // Contour chrome
    const rim = new THREE.Mesh(new THREE.BoxGeometry(0.32, 0.16, 0.06), chromeMat);
    rim.position.set(x, 0.60, 2.21);
    group.add(rim);
  }

  // ── Feux arrière ────────────────────────────────────────────────────
  for (const x of [-0.72, 0.72]) {
    const tl = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.14, 0.10), taillightMat);
    tl.position.set(x, 0.62, -2.14);
    group.add(tl);
  }

  // ── Pare-chocs arrière ──────────────────────────────────────────────
  const bumperR = new THREE.Mesh(new THREE.BoxGeometry(1.85, 0.22, 0.22), bodyMat);
  bumperR.position.set(0, 0.34, -2.16);
  group.add(bumperR);

  // ── Toit — bordure chrome ───────────────────────────────────────────
  const roofRim = new THREE.Mesh(new THREE.BoxGeometry(1.62, 0.030, 2.02), chromeMat);
  roofRim.position.set(0, 1.285, -0.25);
  group.add(roofRim);

  // ── Antenne ─────────────────────────────────────────────────────────
  const antenna = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.010, 0.28, 5), chromeMat);
  antenna.position.set(0.55, 1.44, -0.80);
  group.add(antenna);

  // ── Rétroviseurs latéraux ───────────────────────────────────────────
  for (const x of [-1.02, 1.02]) {
    const mirror = new THREE.Mesh(new THREE.BoxGeometry(0.085, 0.052, 0.120), darkMat);
    mirror.position.set(x, 0.95, 0.82);
    group.add(mirror);
    const mirrorFace = new THREE.Mesh(new THREE.BoxGeometry(0.078, 0.046, 0.010), glassMat);
    mirrorFace.position.set(x, 0.95, 0.88);
    group.add(mirrorFace);
  }

  // ── Roues améliorées (pneu + jante rayons) ─────────────────────────
  const tireGeo = new THREE.CylinderGeometry(0.42, 0.42, 0.28, 18);
  const hubGeo  = new THREE.CylinderGeometry(0.18, 0.18, 0.30, 12);
  const spokeGeo = new THREE.BoxGeometry(0.055, 0.30, 0.06);
  const wheelPositions = [
    [-1.02, 0.42, 1.38],
    [ 1.02, 0.42, 1.38],
    [-1.02, 0.42, -1.38],
    [ 1.02, 0.42, -1.38],
  ];
  for (const [x, y, z] of wheelPositions) {
    const tire = new THREE.Mesh(tireGeo, wheelMat);
    tire.rotation.x = Math.PI / 2;
    tire.position.set(x, y, z);
    tire.castShadow = true;
    group.add(tire);

    // Jante centrale
    const hub = new THREE.Mesh(hubGeo, hubMat);
    hub.rotation.x = Math.PI / 2;
    hub.position.set(x, y, z);
    group.add(hub);

    // 5 rayons
    for (let i = 0; i < 5; i++) {
      const spoke = new THREE.Mesh(spokeGeo, hubMat);
      spoke.rotation.x = Math.PI / 2;
      spoke.rotation.z = (i / 5) * Math.PI * 2;
      spoke.position.set(x, y, z);
      group.add(spoke);
    }
  }

  // ── Plaque d'immatriculation avant ─────────────────────────────────
  const plate = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.11, 0.025), mat(0xfafafa, 0.5));
  plate.position.set(0, 0.38, 2.26);
  group.add(plate);

  // Refs exportées
  group._bodyMat      = bodyMat;
  group._headlightMat = headlightMat;
  group._taillightMat = taillightMat;

  return group;

  function mat(color, rough, metal = 0) {
    return new THREE.MeshStandardMaterial({ color, roughness: rough, metalness: metal });
  }
}

export class Vehicle {
  constructor(scene, spawnPoint) {
    this.mesh = buildCarMesh();
    this._bodyMat      = this.mesh._bodyMat;
    this._headlightMat = this.mesh._headlightMat;
    this._taillightMat = this.mesh._taillightMat;

    const sp = spawnPoint || { x: 0, z: 0, rotationY: 0 };
    this.mesh.position.set(sp.x, 0, sp.z);
    this.heading = sp.rotationY || 0;
    this.mesh.rotation.y = this.heading;

    scene.add(this.mesh);

    this.speed = 0;
    this.steerAngle = 0;
    this._impactIntensity = 0;
    this._gripFactor = 1.0;
    this._lateralSpeed = 0; // sideways slide velocity (m/s)
    this._handbrakeActive = false;
    this._boostMultiplier = 1.0; // set externally by nitro system
    this._damageFactor = 1.0;   // set externally by VehicleDamageSystem

    // Restore saved color from localStorage (browser only)
    if (typeof localStorage !== 'undefined') {
      const saved = localStorage.getItem('moonbow_car_color');
      if (saved && this._bodyMat) this._bodyMat.color.setHex(parseInt(saved, 16));
    }
  }

  // Change body color and persist the choice.
  setBodyColor(hexInt) {
    if (this._bodyMat) {
      this._bodyMat.color.setHex(hexInt);
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem('moonbow_car_color', hexInt.toString(16).padStart(6, '0'));
      }
    }
  }

  setGripFactor(f) {
    this._gripFactor = Math.max(0.1, Math.min(1.0, f));
  }

  update(dt, input, colliders) {
    if (dt <= 0) return;
    this._impactIntensity = 0;

    const forward = input.get('forward');
    const back = input.get('back');
    const left = input.get('left');
    const right = input.get('right');
    const handbrake = input.get('brake');

    // --- Throttle / brake / reverse -----------------------------------
    if (forward) {
      this.speed += ACCEL * dt;
    } else if (back) {
      if (this.speed > 0) {
        // Braking while still moving forward
        this.speed -= BRAKE_DECEL * dt;
      } else {
        // Already stopped/reversing: accelerate backwards
        this.speed -= ACCEL * 0.7 * dt;
      }
    } else {
      // No throttle input: less grip = less rolling friction (car slides longer on wet road)
      const drop = NATURAL_FRICTION * this._gripFactor * dt;
      if (Math.abs(this.speed) <= drop) {
        this.speed = 0;
      } else {
        this.speed -= Math.sign(this.speed) * drop;
      }
    }

    // Handbrake: reduced effectiveness on wet/slippery surfaces
    if (handbrake) {
      const drop = HANDBRAKE_DECEL * this._gripFactor * dt;
      if (Math.abs(this.speed) <= drop) {
        this.speed = 0;
      } else {
        this.speed -= Math.sign(this.speed) * drop;
      }
    }

    this.speed = clamp(this.speed, -MAX_REVERSE_MS, MAX_SPEED_MS * this._boostMultiplier * this._damageFactor);

    // Drift/slide model: handbrake + steering builds lateral velocity
    this._handbrakeActive = handbrake;
    const LATERAL_BUILDUP = 9;
    const LATERAL_GRIP = 14;
    let steerInputVal = 0;
    if (left) steerInputVal += 1;
    if (right) steerInputVal -= 1;
    if (handbrake && Math.abs(this.speed) > 8) {
      this._lateralSpeed -= steerInputVal * LATERAL_BUILDUP * dt * this._gripFactor;
    } else {
      const lateralDrop = LATERAL_GRIP * dt;
      if (Math.abs(this._lateralSpeed) <= lateralDrop) {
        this._lateralSpeed = 0;
      } else {
        this._lateralSpeed -= Math.sign(this._lateralSpeed) * lateralDrop;
      }
    }
    this._lateralSpeed = clamp(this._lateralSpeed, -MAX_SPEED_MS * 0.45, MAX_SPEED_MS * 0.45);

    // --- Steering --------------------------------------------------------
    // Steering authority scales down at low speed so the car can't spin in
    // place, and also scales down slightly at very high speed for stability.
    const speedRatio = clamp(Math.abs(this.speed) / MAX_SPEED_MS, 0, 1);
    const lowSpeedFactor = clamp(Math.abs(this.speed) / 2.5, 0, 1); // ramps up over first ~2.5 m/s
    const highSpeedFactor = 1 - 0.35 * speedRatio;
    const steerAuthority = lowSpeedFactor * highSpeedFactor;

    let steerInput = 0;
    if (left) steerInput += 1;
    if (right) steerInput -= 1;

    const targetSteer = steerInput * MAX_STEER_ANGLE * steerAuthority * this._gripFactor;
    const steerDelta = clamp(targetSteer - this.steerAngle, -MAX_STEER_RATE * dt, MAX_STEER_RATE * dt);
    this.steerAngle += steerDelta;

    // Reversing should invert the apparent steering so it feels natural
    // (turning the wheel left while reversing swings the rear the other way).
    const steerForHeading = this.speed >= 0 ? this.steerAngle : -this.steerAngle;

    // Simple bicycle-model heading change: angular velocity = v/L * tan(steer)
    if (Math.abs(this.speed) > 0.05) {
      const angularVelocity = (this.speed / WHEELBASE) * Math.tan(steerForHeading);
      this.heading += angularVelocity * dt;
    }

    // Slight extra drift/slide feeling under handbrake: bleed a bit of heading
    // change even as speed drops, handled implicitly since angularVelocity
    // depends on current (still nonzero) speed during the handbrake decel ramp.

    // Keep heading normalized to (-PI, PI] so it stays well-behaved for any
    // future consumer (HUD compass, AI heading comparisons, etc).
    if (this.heading > Math.PI) this.heading -= Math.PI * 2;
    else if (this.heading <= -Math.PI) this.heading += Math.PI * 2;

    // --- Integrate position ----------------------------------------------
    const dirX = Math.sin(this.heading);
    const dirZ = Math.cos(this.heading);

    const perpX = Math.cos(this.heading);
    const perpZ = -Math.sin(this.heading);
    let nextX = this.mesh.position.x + dirX * this.speed * dt + perpX * this._lateralSpeed * dt;
    let nextZ = this.mesh.position.z + dirZ * this.speed * dt + perpZ * this._lateralSpeed * dt;

    // --- Collision resolution: treat car as a circle vs AABB colliders ---
    if (colliders && colliders.length) {
      for (const c of colliders) {
        const halfW = c.halfWidth;
        const halfD = c.halfDepth;
        const minX = c.x - halfW;
        const maxX = c.x + halfW;
        const minZ = c.z - halfD;
        const maxZ = c.z + halfD;

        // Closest point on the AABB to the car's (prospective) center
        const closestX = clamp(nextX, minX, maxX);
        const closestZ = clamp(nextZ, minZ, maxZ);

        const dx = nextX - closestX;
        const dz = nextZ - closestZ;
        const distSq = dx * dx + dz * dz;

        if (distSq < COLLISION_RADIUS * COLLISION_RADIUS) {
          const dist = Math.sqrt(distSq);
          let normalX, normalZ;

          if (dist > 1e-5) {
            normalX = dx / dist;
            normalZ = dz / dist;
          } else {
            // Center is exactly on/inside the box edge (rare): push out along
            // whichever axis has the smallest penetration.
            const penLeft = nextX - minX;
            const penRight = maxX - nextX;
            const penTop = nextZ - minZ;
            const penBottom = maxZ - nextZ;
            const minPen = Math.min(penLeft, penRight, penTop, penBottom);
            if (minPen === penLeft) { normalX = -1; normalZ = 0; }
            else if (minPen === penRight) { normalX = 1; normalZ = 0; }
            else if (minPen === penTop) { normalX = 0; normalZ = -1; }
            else { normalX = 0; normalZ = 1; }
          }

          const penetration = COLLISION_RADIUS - dist;
          // Push the car back out along the collision normal.
          nextX += normalX * penetration;
          nextZ += normalZ * penetration;

          // Kill the velocity component heading into the wall, and bounce a
          // small fraction of it back out (mild restitution) so hitting a
          // building at speed feels like an impact rather than a hard stop.
          const velX = dirX * this.speed;
          const velZ = dirZ * this.speed;
          const velIntoWall = velX * (-normalX) + velZ * (-normalZ); // positive if moving into the wall
          if (velIntoWall > 0) {
            const fractionInto = clamp(velIntoWall / Math.max(Math.abs(this.speed), 0.001), 0, 1);
            // Scale overall forward speed down by how much of it was driving
            // into the wall, then shave off a bit more for the "bounce".
            this.speed *= (1 - fractionInto) * (1 - RESTITUTION * 0.5);

            // 8 m/s (~29 km/h) straight into a wall counts as a "hard" impact.
            this._impactIntensity = Math.max(this._impactIntensity, clamp(velIntoWall / 8, 0, 1));
          }
        }
      }
    }

    this.mesh.position.x = nextX;
    this.mesh.position.z = nextZ;
    this.mesh.rotation.y = this.heading;
  }

  getPosition() {
    return { x: this.mesh.position.x, z: this.mesh.position.z };
  }

  getSpeedKmh() {
    return this.speed * 3.6;
  }

  getHeading() {
    return this.heading;
  }

  // 0..1, how hard the car hit something during the most recent update() call.
  getImpactIntensity() {
    return this._impactIntensity;
  }

  getLateralSpeed() { return this._lateralSpeed; }
  isHandbraking()   { return this._handbrakeActive; }
  setBoostMultiplier(m) { this._boostMultiplier = Math.max(1.0, Math.min(2.0, m)); }
  setDamageFactor(f)    { this._damageFactor    = Math.max(0.35, Math.min(1.0, f)); }
}
