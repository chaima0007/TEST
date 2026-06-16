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

// Build a simple low-poly car mesh out of primitives.
function buildCarMesh() {
  const group = new THREE.Group();

  const bodyMat = new THREE.MeshStandardMaterial({ color: 0xcc2222, metalness: 0.3, roughness: 0.5 });
  const cabinMat = new THREE.MeshStandardMaterial({ color: 0x111722, metalness: 0.1, roughness: 0.4 });
  const wheelMat = new THREE.MeshStandardMaterial({ color: 0x0a0a0a, metalness: 0.1, roughness: 0.8 });

  // Main body
  const body = new THREE.Mesh(new THREE.BoxGeometry(1.9, 0.6, 4.2), bodyMat);
  body.position.y = 0.55;
  body.castShadow = true;
  group.add(body);

  // Cabin (greenhouse), set back slightly toward the rear like a sedan
  const cabin = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.55, 2.0), cabinMat);
  cabin.position.set(0, 1.0, -0.25);
  cabin.castShadow = true;
  group.add(cabin);

  // Front bumper hint so the "forward" direction is visually obvious
  const bumper = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.35, 0.3), bodyMat);
  bumper.position.set(0, 0.4, 2.1);
  group.add(bumper);

  // Wheels: cylinders rotated so their axis points along local X
  const wheelGeo = new THREE.CylinderGeometry(0.42, 0.42, 0.32, 16);
  const wheelOffsets = [
    [-1.0, 0.42, 1.4],
    [1.0, 0.42, 1.4],
    [-1.0, 0.42, -1.4],
    [1.0, 0.42, -1.4],
  ];
  for (const [x, y, z] of wheelOffsets) {
    const wheel = new THREE.Mesh(wheelGeo, wheelMat);
    wheel.rotation.x = Math.PI / 2;
    wheel.position.set(x, y, z);
    wheel.castShadow = true;
    group.add(wheel);
  }

  return group;
}

export class Vehicle {
  constructor(scene, spawnPoint) {
    this.mesh = buildCarMesh();

    const sp = spawnPoint || { x: 0, z: 0, rotationY: 0 };
    this.mesh.position.set(sp.x, 0, sp.z);
    this.heading = sp.rotationY || 0;
    this.mesh.rotation.y = this.heading;

    scene.add(this.mesh);

    // Forward speed along the car's own facing direction (signed: + forward, - reverse)
    this.speed = 0;
    // Current steering angle (radians), eases toward input-driven target for smoothness
    this.steerAngle = 0;
  }

  update(dt, input, colliders) {
    if (dt <= 0) return;

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
      // No throttle input: natural engine/rolling friction decelerates toward 0
      const drop = NATURAL_FRICTION * dt;
      if (Math.abs(this.speed) <= drop) {
        this.speed = 0;
      } else {
        this.speed -= Math.sign(this.speed) * drop;
      }
    }

    // Handbrake: strong extra deceleration regardless of throttle state
    if (handbrake) {
      const drop = HANDBRAKE_DECEL * dt;
      if (Math.abs(this.speed) <= drop) {
        this.speed = 0;
      } else {
        this.speed -= Math.sign(this.speed) * drop;
      }
    }

    this.speed = clamp(this.speed, -MAX_REVERSE_MS, MAX_SPEED_MS);

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

    const targetSteer = steerInput * MAX_STEER_ANGLE * steerAuthority;
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

    let nextX = this.mesh.position.x + dirX * this.speed * dt;
    let nextZ = this.mesh.position.z + dirZ * this.speed * dt;

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
}
