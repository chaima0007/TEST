import * as THREE from 'three';
import { createWorld } from './world.js';
import { Vehicle } from './vehicle.js';
import { createFollowCamera, updateFollowCamera } from './camera.js';
import { InputManager } from './input.js';
import { MissionManager } from './missions.js';
import { WantedSystem } from './police.js';
import { HUD } from './hud.js';
import { TrafficSystem } from './traffic.js';
import { AudioSystem } from './audio.js';
import { RivalSystem } from './rival.js';
import { ComboSystem } from './combo.js';

const MAX_SPEED_KMH = 150; // doit suivre vehicle.js, utilisé seulement pour le ratio audio moteur

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb);
scene.fog = new THREE.Fog(0x87ceeb, 80, 260);

const sun = new THREE.DirectionalLight(0xffffff, 1.1);
sun.position.set(60, 100, 40);
scene.add(sun);
scene.add(new THREE.AmbientLight(0xffffff, 0.45));

const world = createWorld(scene);
const vehicle = new Vehicle(scene, world.spawnPoint);
const camera = createFollowCamera(renderer);
const input = new InputManager();
const hud = new HUD(document.getElementById('hud-root'));
const missions = new MissionManager(world, hud);
const wanted = new WantedSystem(scene, world);
const traffic = new TrafficSystem(scene, world);
const rival = new RivalSystem(scene, world);
const combo = new ComboSystem();
const audio = new AudioSystem();

window.addEventListener('resize', () => {
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
});

let lastTime = performance.now();
let lastScore = missions.getScore() + rival.getScore() + combo.getScore();
let lastWantedLevel = wanted.level;
let cameraShake = 0;
let lastImpactSoundTime = -Infinity;
const IMPACT_AUDIO_THRESHOLD = 0.08; // ignore barely-grazing contacts
const IMPACT_AUDIO_COOLDOWN_S = 0.25; // avoid spamming the thump while grinding against a wall

function animate() {
  requestAnimationFrame(animate);
  const now = performance.now();
  const dt = Math.min((now - lastTime) / 1000, 0.05);
  lastTime = now;

  if (hud.isPaused()) {
    // Freeze gameplay entirely while the pause overlay is up: no movement,
    // no mission timers ticking down, no police chase, no engine/siren audio.
    audio.setEngineIntensity(0);
    audio.setSirenActive(false);
    renderer.render(scene, camera);
    return;
  }

  // One-frame-stale traffic positions are an acceptable trade-off here: it
  // avoids reordering the whole loop just to let the player collide with
  // cars/pedestrians instead of driving straight through them.
  vehicle.update(dt, input, world.colliders.concat(traffic.getColliders()));
  updateFollowCamera(camera, vehicle, dt);
  missions.update(dt, vehicle);
  wanted.update(dt, vehicle, hud);
  traffic.update(dt, vehicle.getPosition());
  rival.update(dt, vehicle, hud);

  const playerPos = vehicle.getPosition();
  combo.update(dt, playerPos, traffic.getCarPositions());
  hud.setCombo(combo.getMultiplier());
  hud.updateRadar({
    playerPos,
    playerHeading: vehicle.getHeading(),
    target: missions.getCurrentMission(),
    policeCars: wanted.cars.map((c) => ({ x: c.mesh.position.x, z: c.mesh.position.z })),
    rivalPos: rival.active && rival.mesh ? { x: rival.mesh.position.x, z: rival.mesh.position.z } : null,
  });

  hud.setSpeed(vehicle.getSpeedKmh());
  const totalScore = missions.getScore() + rival.getScore() + combo.getScore();
  hud.setScore(totalScore);

  audio.setEngineIntensity(Math.min(1, Math.abs(vehicle.getSpeedKmh()) / MAX_SPEED_KMH));
  audio.setSirenActive(wanted.level > 0);

  const impact = vehicle.getImpactIntensity();
  const elapsedS = now / 1000;
  if (impact > IMPACT_AUDIO_THRESHOLD && elapsedS - lastImpactSoundTime > IMPACT_AUDIO_COOLDOWN_S) {
    audio.playCollision(impact);
    lastImpactSoundTime = elapsedS;
    cameraShake = Math.min(1, cameraShake + impact * 0.7);
  }
  if (cameraShake > 0.001) {
    camera.position.x += (Math.random() - 0.5) * cameraShake * 1.8;
    camera.position.y += Math.random() * cameraShake * 0.8;
    camera.position.z += (Math.random() - 0.5) * cameraShake * 1.8;
    cameraShake *= 0.78; // décroissance exponentielle par frame
  } else {
    cameraShake = 0;
  }

  if (totalScore > lastScore) audio.playUiBlip();
  lastScore = totalScore;


  if (wanted.level !== lastWantedLevel) audio.playUiBlip();
  lastWantedLevel = wanted.level;

  renderer.render(scene, camera);
}

animate();
