import * as THREE from 'three';
import { createWorld } from './world.js';
import { Vehicle } from './vehicle.js';
import { createFollowCamera, updateFollowCamera } from './camera.js';
import { InputManager } from './input.js';
import { MissionManager } from './missions.js';
import { WantedSystem } from './police.js';
import { HUD } from './hud.js';

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

window.addEventListener('resize', () => {
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
});

let lastTime = performance.now();

function animate() {
  requestAnimationFrame(animate);
  const now = performance.now();
  const dt = Math.min((now - lastTime) / 1000, 0.05);
  lastTime = now;

  vehicle.update(dt, input, world.colliders);
  updateFollowCamera(camera, vehicle, dt);
  missions.update(dt, vehicle);
  wanted.update(dt, vehicle, hud);
  hud.setSpeed(vehicle.getSpeedKmh());

  renderer.render(scene, camera);
}

animate();
