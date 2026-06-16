import * as THREE from 'three';

// Offset of the camera relative to the car, expressed in the car's local
// space (X = right, Y = up, Z = forward). The camera sits behind (-Z) and
// above (+Y) the car.
const LOCAL_OFFSET = new THREE.Vector3(0, 4.2, -8.5);
// Point the camera looks toward, also in the car's local space — slightly
// ahead of and above the car so the horizon/road ahead is visible.
const LOCAL_LOOK_AT = new THREE.Vector3(0, 1.2, 4);

// Damping rates (per second). Higher = snappier, lower = floatier.
// Using the frame-rate-independent exponential smoothing formula:
//   factor = 1 - exp(-lambda * dt)
const POSITION_LAMBDA = 5.0;
const LOOKAT_LAMBDA = 7.0;

export function createFollowCamera(renderer) {
  const canvas = renderer.domElement;
  const aspect = canvas.clientWidth && canvas.clientHeight
    ? canvas.clientWidth / canvas.clientHeight
    : window.innerWidth / window.innerHeight;

  const camera = new THREE.PerspectiveCamera(65, aspect, 0.1, 1000);
  camera.position.set(0, 6, -10);
  camera.lookAt(0, 0, 0);

  // Internal smoothed look-at target persists across frames.
  camera.userData.smoothedLookAt = new THREE.Vector3(0, 0, 0);
  camera.userData.initialized = false;

  return camera;
}

export function updateFollowCamera(camera, vehicle, dt) {
  const pos = vehicle.getPosition();
  const heading = vehicle.getHeading();

  // Rotate the local offset/look-at by the car's heading (rotation around Y)
  // and translate to the car's world position.
  const cosH = Math.cos(heading);
  const sinH = Math.sin(heading);

  function localToWorld(local) {
    const worldX = pos.x + local.x * cosH + local.z * sinH;
    const worldZ = pos.z - local.x * sinH + local.z * cosH;
    const worldY = local.y;
    return new THREE.Vector3(worldX, worldY, worldZ);
  }

  const desiredPosition = localToWorld(LOCAL_OFFSET);
  const desiredLookAt = localToWorld(LOCAL_LOOK_AT);

  if (!camera.userData.initialized) {
    camera.position.copy(desiredPosition);
    camera.userData.smoothedLookAt.copy(desiredLookAt);
    camera.userData.initialized = true;
  } else {
    // Frame-rate independent exponential damping: the camera always closes
    // the same proportion of the remaining gap per unit time, regardless of
    // how dt is chunked across frames.
    const posFactor = 1 - Math.exp(-POSITION_LAMBDA * dt);
    const lookFactor = 1 - Math.exp(-LOOKAT_LAMBDA * dt);

    camera.position.lerp(desiredPosition, posFactor);
    camera.userData.smoothedLookAt.lerp(desiredLookAt, lookFactor);
  }

  camera.lookAt(camera.userData.smoothedLookAt);
}
