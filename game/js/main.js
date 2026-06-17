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
import { DayCycle } from './daycycle.js';
import { WeatherSystem } from './weather.js';
import { FantomeSystem } from './fantome.js';
import { DriftSystem } from './drift.js';
import { NitroSystem } from './nitro.js';
import { TireSmokeSystem, SparkSystem } from './particles.js';
import { SpeedCamSystem } from './speedcam.js';
import { SkidMarkSystem } from './skidmarks.js';
import { DetectiveSystem } from './detective.js';

const MAX_SPEED_KMH = 150;

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
const ambientLight = new THREE.AmbientLight(0xffffff, 0.45);
scene.add(ambientLight);

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
const dayCycle = new DayCycle(scene, sun, ambientLight);
const weather = new WeatherSystem(scene);
const fantome = new FantomeSystem(scene, world);
const drift  = new DriftSystem();
const nitro  = new NitroSystem(scene);
const smoke    = new TireSmokeSystem(scene);
const sparks   = new SparkSystem(scene);
const skids    = new SkidMarkSystem(scene);
const speedCams  = new SpeedCamSystem(scene, world);
const detective  = new DetectiveSystem(scene, world);

// Score persistant (localStorage)
const HS_KEY = 'moonbow_highscore';
let highScore = parseInt(localStorage.getItem(HS_KEY) || '0', 10);
hud.setRecord(highScore);

window.addEventListener('resize', () => {
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
});

let lastTime = performance.now();
let lastScore = 0;
let lastBoostActive = false;
let lastWantedLevel = wanted.level;
let cameraShake = 0;
let lastImpactSoundTime = -Infinity;
const IMPACT_AUDIO_THRESHOLD = 0.08;
const IMPACT_AUDIO_COOLDOWN_S = 0.25;

function animate() {
  requestAnimationFrame(animate);
  const now = performance.now();
  const dt = Math.min((now - lastTime) / 1000, 0.05);
  lastTime = now;

  if (hud.isPaused()) {
    audio.setEngineIntensity(0);
    audio.setSirenActive(false);
    renderer.render(scene, camera);
    return;
  }

  // --- Systèmes environnementaux ---
  dayCycle.update(dt);
  weather.update(dt, vehicle.getPosition());
  vehicle.setGripFactor(weather.getGripFactor());

  // --- Gameplay ---
  // Nitro boost + grip
  vehicle.setBoostMultiplier(nitro.getBoostMultiplier());
  vehicle.update(dt, input, world.colliders.concat(traffic.getColliders(), wanted.getRoadblockColliders()));
  updateFollowCamera(camera, vehicle, dt);
  missions.update(dt, vehicle);
  wanted.update(dt, vehicle, hud);
  traffic.update(dt, vehicle.getPosition());
  rival.update(dt, vehicle, hud);
  fantome.update(dt, vehicle, hud, dayCycle.isNight());
  detective.update(dt, vehicle, hud, wanted.level);

  const playerPos = vehicle.getPosition();
  combo.update(dt, playerPos, traffic.getCarPositions());
  drift.update(dt, vehicle);
  nitro.update(dt, playerPos, input);
  smoke.update(dt, vehicle, drift.isDrifting());
  skids.update(dt, vehicle, drift.isDrifting());
  sparks.update(dt);

  const camViolation = speedCams.update(dt, vehicle, hud);
  if (camViolation && wanted.level < 5) wanted._setLevel(wanted.level + 1, hud);

  // Lampadaires : s'allument la nuit
  const nightIntensity = dayCycle.isNight() ? 1.4 : 0;
  for (const lamp of world.streetLamps) lamp.material.emissiveIntensity = nightIntensity;

  // --- HUD ---
  hud.setCombo(combo.getMultiplier());
  hud.setTime(dayCycle.getTimeString());
  hud.setWeather(weather.getWeatherId());

  hud.updateRadar({
    playerPos,
    playerHeading: vehicle.getHeading(),
    target: missions.getCurrentMission(),
    policeCars: wanted.cars.map((c) => ({ x: c.mesh.position.x, z: c.mesh.position.z })),
    rivalPos: rival.active && rival.mesh ? { x: rival.mesh.position.x, z: rival.mesh.position.z } : null,
    fantomePos: fantome.active && fantome.mesh ? { x: fantome.mesh.position.x, z: fantome.mesh.position.z } : null,
    checkpointPos: fantome.active && fantome._checkpointPos ? fantome._checkpointPos : null,
    speedCams: speedCams.getCameraPositions(),
    nitroCapsules: nitro._capsules.map(c => ({ x: c.x, z: c.z })),
  });

  hud.setSpeed(vehicle.getSpeedKmh());

  const totalScore = missions.getScore() + rival.getScore() + combo.getScore() + fantome.getScore() + drift.getScore();
  hud.setScore(totalScore);

  // --- Panneau agents temps réel ---
  const spectreState = rival.active
    ? `${rival._state} | dist ${rival.mesh ? Math.round(Math.hypot(playerPos.x - rival.mesh.position.x, playerPos.z - rival.mesh.position.z)) : '?'}m | ${Math.round(rival._challengeTimeLeft)}s`
    : `Cooldown ${Math.round(Math.max(0, rival._cooldown))}s`;

  const fantomeState = fantome.active
    ? `COURSE | fantome ${Math.round(fantome._speed)} km/h`
    : `Nuit: ${dayCycle.isNight() ? 'oui' : 'non'} | ${Math.round(Math.max(0, fantome._cooldown))}s`;

  const policeState = wanted.level > 0
    ? `Niveau ${wanted.level} | ${wanted.cars.length} voiture(s)${wanted.getHelicopterActive() ? ' + HELI' : ''}`
    : 'Calme';

  const detectiveState = detective.active
    ? (detective.isTailing() ? 'EN FILATURE - CHALEUR x2' : 'En suivi...')
    : `Cooldown ${Math.round(Math.max(0, detective._cooldown))}s`;

  const grip = weather.getGripFactor();
  const meteoState = `${weather.getWeatherId()} | Adherence ${Math.round(grip * 100)}%`;

  hud.updateAgents({
    spectre: {
      active: rival.active,
      status: spectreState,
      bar: rival.active ? rival._challengeTimeLeft / 22 : Math.max(0, 1 - rival._cooldown / 70),
      color: '#aa33ff',
    },
    fantome: {
      active: fantome.active,
      status: fantomeState,
      bar: fantome.active ? fantome._speed / 125 : (dayCycle.isNight() ? Math.max(0, 1 - fantome._cooldown / 60) : 0),
      color: '#ffd700',
    },
    detective: {
      active: detective.active,
      status: detectiveState,
      bar: detective.active ? (detective.isTailing() ? 1 : 0.4) : 0,
      color: detective.isTailing() ? '#ff3333' : '#cc4444',
    },
    police: {
      active: wanted.level > 0,
      status: policeState,
      bar: wanted.level / 5,
      color: wanted.level >= 4 ? '#ff4444' : '#4488ff',
    },
    meteo: {
      active: true,
      status: meteoState,
      bar: 1 - grip,
      color: grip < 0.6 ? '#55aaff' : '#44aaff',
    },
    trafic: {
      active: true,
      status: drift.isDrifting()
        ? `DRIFT ${Math.round(drift.getDriftAngle())}° +${drift.getSessionScore()}`
        : `Combo x${combo.getMultiplier()} | ${Math.round(vehicle.getSpeedKmh())} km/h`,
      bar: drift.isDrifting() ? Math.min(1, drift.getSessionScore() / 300) : combo.getMultiplier() / 5,
      color: drift.isDrifting() ? '#ff6622' : combo.getMultiplier() >= 3 ? '#ff9944' : '#55cc88',
    },
  });

  const boostNow = nitro.isBoostActive();
  if (boostNow && !lastBoostActive) audio.playNitro();
  lastBoostActive = boostNow;
  hud.setNitro(nitro.getCharges(), boostNow);
  hud.setDrift(drift.isDrifting(), drift.getDriftAngle(), drift.getSessionScore());

  // --- Audio ---
  audio.setEngineIntensity(Math.min(1, Math.abs(vehicle.getSpeedKmh()) / MAX_SPEED_KMH));
  audio.setSirenActive(wanted.level > 0);
  audio.setDriftActive(drift.isDrifting());
  audio.setChaseIntensity(wanted.level / 5);

  const impact = vehicle.getImpactIntensity();
  const elapsedS = now / 1000;
  if (impact > IMPACT_AUDIO_THRESHOLD && elapsedS - lastImpactSoundTime > IMPACT_AUDIO_COOLDOWN_S) {
    audio.playCollision(impact);
    lastImpactSoundTime = elapsedS;
    cameraShake = Math.min(1, cameraShake + impact * 0.7);
    if (impact > 0.35) sparks.emit(playerPos.x, playerPos.z, impact);
  }
  if (cameraShake > 0.001) {
    camera.position.x += (Math.random() - 0.5) * cameraShake * 1.8;
    camera.position.y += Math.random() * cameraShake * 0.8;
    camera.position.z += (Math.random() - 0.5) * cameraShake * 1.8;
    cameraShake *= 0.78;
  } else {
    cameraShake = 0;
  }

  if (totalScore > lastScore) audio.playUiBlip();
  lastScore = totalScore;

  // Record localStorage
  if (totalScore > highScore) {
    highScore = totalScore;
    localStorage.setItem(HS_KEY, String(highScore));
    hud.setRecord(highScore);
  }

  if (wanted.level !== lastWantedLevel) audio.playUiBlip();
  lastWantedLevel = wanted.level;

  renderer.render(scene, camera);
}

animate();
