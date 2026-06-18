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
import { MonetizationAgent } from './monetization.js';
import { LODManager } from './lod.js';
import { ArchitectSystem } from './architect.js';
import { MusicAgent } from './music.js';
import { DialogueAgent } from './dialogue.js';
import { VehicleDamageSystem } from './vehicledamage.js';
import { DistrictSystem }      from './district.js';
import { SignalAgent }          from './signal.js';
import { ReputationAgent }      from './reputation.js';
import { WitnessAgent }         from './witness.js';
import { CityPulseAgent }       from './citypulse.js';
import { PredictivePoliceAgent } from './predictive.js';
import { EmotionEngine }        from './emotion.js';
import { FlashMobAgent }        from './flashmob.js';
import { HonkCascadeAgent, NEAR_MISS_DIST } from './honkcascade.js';
import { CopConfusionAgent }    from './copconfusion.js';
import { TrendRadarAgent }     from './trendradar.js';
import { AtmosphereAgent }     from './atmosphereagent.js';
import { WeatherFXAgent }      from './weatherfx.js';
import { CarShaderAgent }      from './carshader.js';
import { CommandantAgent }     from './commandant.js';
import { ResolveurAgent }      from './resolveur.js';
import { BackroomAgent }       from './backroom.js';
import { MonsterAgent }        from './monster.js';
import { DreamZoneAgent }      from './dreamzone.js';

const MAX_SPEED_KMH = 150;
const MAX_SPEED_MS  = MAX_SPEED_KMH / 3.6;

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb);
scene.fog = new THREE.Fog(0x87ceeb, 80, 260);

const sun = new THREE.DirectionalLight(0xffffff, 1.1);
sun.position.set(60, 100, 40);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.near = 1;
sun.shadow.camera.far = 400;
sun.shadow.camera.left   = -160;
sun.shadow.camera.right  =  160;
sun.shadow.camera.top    =  160;
sun.shadow.camera.bottom = -160;
sun.shadow.bias = -0.001;
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
const detective    = new DetectiveSystem(scene, world);
const architect    = new ArchitectSystem(scene, world);
const monetization = new MonetizationAgent(hud);
const lod = new LODManager();
const _audioCtx = audio.getContext();
const musicAgent = _audioCtx ? new MusicAgent(_audioCtx, _audioCtx.destination) : null;
const dialogueAgent = new DialogueAgent();
const vehicleDamage = new VehicleDamageSystem();
const district     = new DistrictSystem();
const signals      = new SignalAgent(scene, world.roadLines.xs, world.roadLines.zs);
const reputation   = new ReputationAgent();
const witness      = new WitnessAgent();
const cityPulse    = new CityPulseAgent();
const predictive   = new PredictivePoliceAgent();
const emotion      = new EmotionEngine();

// Marqueur de prédiction policière (anneau semi-transparent)
const _predRingGeo = new THREE.TorusGeometry(2.2, 0.22, 8, 24);
const _predRingMat = new THREE.MeshBasicMaterial({ color: 0xff2200, transparent: true, opacity: 0.7 });
const _predRing    = new THREE.Mesh(_predRingGeo, _predRingMat);
_predRing.rotation.x = -Math.PI / 2;
_predRing.visible = false;
scene.add(_predRing);

const flashMob     = new FlashMobAgent();
const honkCascade  = new HonkCascadeAgent();
const copConfusion = new CopConfusionAgent();

// Ronde 21 — Visual Excellence Agents
const trendRadar   = new TrendRadarAgent();
const atmosphere   = new AtmosphereAgent(scene);
const weatherFX    = new WeatherFXAgent(scene);
const carShader    = new CarShaderAgent(scene, renderer, vehicle, traffic);
atmosphere.registerLamps(world.streetLamps);

// Ronde 22 — Premium Agents
const commandant   = new CommandantAgent();
const resolveur    = new ResolveurAgent();

// Ronde 23 — Onirique & Horreur
const backroom  = new BackroomAgent(scene);
const monster   = new MonsterAgent(scene);
const dreamzone = new DreamZoneAgent(scene);

// Sprite "!" pour les klaxons (partagé entre toutes les voitures klaxonnantes)
const _honkSprites = new Map(); // mesh → { sprite, timer }
function _getHonkSprite(mesh) {
  if (_honkSprites.has(mesh)) return _honkSprites.get(mesh);
  const el = document.createElement('div');
  el.style.cssText = `
    position:fixed;pointer-events:none;
    font-size:22px;font-weight:900;color:#ffdd00;
    text-shadow:0 0 8px #ff8800;
    transform:translate(-50%,-50%);
    z-index:200;transition:opacity .2s;
  `;
  el.textContent = '📯';
  document.body.appendChild(el);
  const entry = { el, timer: 0 };
  _honkSprites.set(mesh, entry);
  return entry;
}

let   _signalViolationTime = -Infinity;
const SIGNAL_COOLDOWN_S    = 10;

// ── RadioSystem — stations switchables avec la touche R ──────────────────────
const RADIO_STATIONS = [
  { name: 'AUTO',              style: null    },
  { name: 'Radio Néon',        style: 'city'  },
  { name: 'Fréquence Sombre',  style: 'night' },
  { name: 'CHASE FM',          style: 'chase' },
  { name: 'Radio Némésis',     style: 'boss'  },
];
let _radioIdx = 0;
let _lastRKey  = false;

const _notifEl = document.createElement('div');
_notifEl.style.cssText = `
  position:fixed;bottom:76px;left:50%;transform:translateX(-50%);
  background:rgba(8,10,20,.88);border:1px solid rgba(255,255,255,.2);
  padding:5px 20px;border-radius:20px;
  font-family:'Segoe UI',Arial,sans-serif;font-size:13px;
  color:#ffe87a;font-weight:700;pointer-events:none;
  opacity:0;transition:opacity .3s;z-index:300;
`;
document.body.appendChild(_notifEl);
let _notifTimer = 0;
function _showNotif(text) {
  _notifEl.textContent = text;
  _notifEl.style.opacity = '1';
  _notifTimer = 2.5;
}

// Colour picker wired once — swatches from monetization unlocks
const ALL_COLORS = [
  { color: 0x2255cc, name: 'Bleu Standard',  scoreReq: 0     },
  { color: 0xff2244, name: 'Rouge Turbo',     scoreReq: 2000  },
  { color: 0x00ff88, name: 'Vert Néon',       scoreReq: 5000  },
  { color: 0xffd700, name: 'Or Champion',     scoreReq: 10000 },
  { color: 0xff00ff, name: 'Rose Fantôme',    scoreReq: 25000 },
  { color: 0x00eeff, name: 'Cyan Nitro',      scoreReq: 50000 },
];
function refreshColorPicker() {
  const maxScore = parseInt(localStorage.getItem('moonbow_highscore') || '0', 10);
  const currentHex = parseInt(localStorage.getItem('moonbow_car_color') || '2255cc', 16);
  const options = ALL_COLORS.map(c => ({ ...c, locked: c.scoreReq > maxScore }));
  hud.setColorOptions(options, currentHex, (hex) => vehicle.setBodyColor(hex));
}
refreshColorPicker();

// Score persistant (localStorage)
const HS_KEY = 'moonbow_highscore';
let highScore = parseInt(localStorage.getItem(HS_KEY) || '0', 10);
hud.setRecord(highScore);

// Bonus cumulatif accordé par le Résolveur (persiste pendant la session)
let _resolveurBonusTotal = 0;

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

// ── Physique verticale (jump pads) ────────────────────────────────────────────
let _jumpVy = 0;
let _jumpY  = 0;
const IMPACT_AUDIO_THRESHOLD = 0.08;
const IMPACT_AUDIO_COOLDOWN_S = 0.25;

// NEXUS status — résume ce que les systèmes font en temps réel
const _nexusPhrases = [
  (v, d, w, dc, wx) => `Physique véhicule ${Math.round(Math.abs(v.getSpeedKmh()))} km/h`,
  (v, d, w, dc, wx) => d.isDrifting() ? `Drift actif — calcul score +${d.getSessionScore()}` : `Moteur IA trafic actif`,
  (v, d, w, dc, wx) => w.level > 0 ? `Police niveau ${w.level} — pathfinding actif` : `Surveillance réseau calme`,
  (v, d, w, dc, wx) => `Météo ${wx.getWeatherId()} — adhérence ${Math.round(wx.getGripFactor()*100)}%`,
  (v, d, w, dc, wx) => dc.isNight() ? `Mode nuit — lampadaires + Fantôme` : `Cycle jour ${dc.getTimeString()}`,
  (v, d, w, dc, wx) => {
    const dmg = vehicleDamage.getDamage();
    return `${district.getCurrent().name} | Carrosserie ${dmg > 0.05 ? Math.round(dmg*100)+'%' : 'OK'} | ${RADIO_STATIONS[_radioIdx].name}`;
  },
  (v, d, w, dc, wx) => {
    const rep = reputation.getStatus(district.getCurrent().id);
    const wit = witness.getWitnessCount();
    return `Réputation ${district.getCurrent().name}: ${rep}${wit > 0 ? ` | ${wit} TÉMOIN(S) actif(s)` : ''}`;
  },
  (v, d, w, dc, wx) => {
    const mood = emotion.getMoodLabel();
    const bpm  = cityPulse.getBpm();
    const conf = Math.round(predictive.getConfidence() * 100);
    return `Humeur ville: ${mood} | BPM ${bpm}${conf > 0 ? ` | Prédiction ${conf}%` : ''}`;
  },
  (v, d, w, dc, wx) => {
    const honks = honkCascade.getHonkingCount();
    const dance = flashMob.isActive() ? `Flash mob! ${flashMob.getDancerCount()} danseurs` : `CD ${Math.round(flashMob.getCooldown())}s`;
    return `${dance}${honks > 0 ? ` | ${honks} klaxon(s) en cascade` : ''}`;
  },
  (v, d, w, dc, wx) => {
    const rain  = Math.round(weatherFX.getIntensity() * 100);
    const dirt  = Math.round(carShader.getDirtLevel() * 100);
    const stars = Math.round(atmosphere.getStarOpacity() * 100);
    return `VisualFX: Ciel ${stars}% étoiles | Pluie ${rain}% | Carrosserie saleté ${dirt}%`;
  },
  (v, d, w, dc, wx) => {
    if (commandant.isActive()) return `COMMANDANT: ${commandant.getPlanLabel()} | Menace ${Math.round(commandant.getThreatLevel() * 100)}%`;
    return `COMMANDANT en veille | RÉSOLVEUR: ${resolveur.getResolveCount()} résolution(s) — bonus +${_resolveurBonusTotal}`;
  },
  (v, d, w, dc, wx) => {
    if (backroom.isActive()) return `BACKROOM — Entité à ${Math.round(backroom.getEntityDist())}m | Fuite ${Math.round(backroom.getEscapePct() * 100)}%`;
    if (monster.isActive()) return `${monster.getMonsterType()} — Distance ${Math.round(monster.getDistance())}m | Peur ${Math.round(monster.getFearLevel() * 100)}%`;
    return `ONIRIQUE — Zones visitées ${dreamzone.getVisitedCount()}/${dreamzone.getTotalCount()} | ${monster.getScareCount()} frayeur(s)`;
  },
];
let _nexusIdx = 0;
let _nexusFlip = 0;
function _nexusStatus(vehicle, drift, wanted, dayCycle, weather) {
  _nexusFlip += 1;
  if (_nexusFlip > 180) { _nexusFlip = 0; _nexusIdx = (_nexusIdx + 1) % _nexusPhrases.length; }
  return _nexusPhrases[_nexusIdx](vehicle, drift, wanted, dayCycle, weather);
}

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

  lod.tick();

  // --- Touche R : changement de station radio ---
  const rKeyNow = input.codes.has('KeyR');
  if (rKeyNow && !_lastRKey) {
    _radioIdx = (_radioIdx + 1) % RADIO_STATIONS.length;
    _showNotif(`[ ${RADIO_STATIONS[_radioIdx].name} ]`);
  }
  _lastRKey = rKeyNow;
  if (_notifTimer > 0) { _notifTimer -= dt; if (_notifTimer <= 0) _notifEl.style.opacity = '0'; }

  // --- Systèmes environnementaux ---
  dayCycle.update(dt);
  weather.update(dt, vehicle.getPosition());
  vehicle.setGripFactor(weather.getGripFactor());

  // --- Gameplay ---
  // Nitro boost + grip
  vehicle.setBoostMultiplier(nitro.getBoostMultiplier());
  vehicle.update(dt, input, world.colliders.concat(traffic.getColliders(), wanted.getRoadblockColliders()));
  vehicleDamage.update(dt);
  vehicle.setDamageFactor(vehicleDamage.getSpeedFactor());
  vehicleDamage.updateVisuals(vehicle._bodyMat);
  updateFollowCamera(camera, vehicle, dt);
  missions.update(dt, vehicle);
  wanted.update(dt, vehicle, hud);
  traffic.update(dt, vehicle.getPosition(), wanted.level, lod);
  rival.update(dt, vehicle, hud);
  fantome.update(dt, vehicle, hud, dayCycle.isNight());
  detective.update(dt, vehicle, hud, wanted.level);

  const playerPos = vehicle.getPosition();

  // --- Physique verticale (jump pads) ────────────────────────────────────────
  _jumpVy -= 18 * dt;
  _jumpY   = Math.max(0, _jumpY + _jumpVy * dt);
  vehicle.mesh.position.y = _jumpY;

  // --- Jump pads ─────────────────────────────────────────────────────────────
  for (const pad of world.jumpPads) {
    if (pad._cd > 0) { pad._cd -= dt; continue; }
    const dx = playerPos.x - pad.x, dz = playerPos.z - pad.z;
    if (_jumpY < 0.5 && dx * dx + dz * dz < 12) {
      _jumpVy = pad.power * 0.55;
      pad._cd = 2.8;
      emotion.pushEvent('drift', 2);
      _showNotif('💥 TRAMPOLINE — envol !');
    }
  }

  // --- Couloirs de vitesse ────────────────────────────────────────────────────
  for (const boost of world.speedBoosts) {
    if (Math.abs(playerPos.x - boost.x) < boost.hw && Math.abs(playerPos.z - boost.z) < boost.hd) {
      vehicle.speed = Math.min(vehicle.speed + 8 * dt, MAX_SPEED_MS * 1.45);
    }
  }

  // --- Portails de téléportation ──────────────────────────────────────────────
  for (const portal of world.portals) {
    if (!portal._cd || portal._cd <= 0) {
      const dA = Math.hypot(playerPos.x - portal.a.x, playerPos.z - portal.a.z);
      const dB = Math.hypot(playerPos.x - portal.b.x, playerPos.z - portal.b.z);
      if (_jumpY < 0.5 && dA < 4) {
        vehicle.mesh.position.set(portal.b.x + 5, 0, portal.b.z);
        _jumpVy = 0; _jumpY = 0;
        portal._cd = 3;
        _showNotif('⬛ PORTAIL — Téléportation !');
        emotion.pushEvent('crash', 0.5);
      } else if (_jumpY < 0.5 && dB < 4) {
        vehicle.mesh.position.set(portal.a.x + 5, 0, portal.a.z);
        _jumpVy = 0; _jumpY = 0;
        portal._cd = 3;
        _showNotif('⬛ PORTAIL — Retour au Nord !');
        emotion.pushEvent('crash', 0.5);
      }
    }
    if (portal._cd > 0) portal._cd -= dt;
  }

  // --- DistrictSystem : changement de quartier ---
  const districtChange = district.update(playerPos.x, playerPos.z, scene.fog);
  if (districtChange) _showNotif(`${districtChange.name} — ${districtChange.desc}`);

  // --- SignalAgent : feux tricolores ---
  signals.update(dt);
  if (signals.isViolation(playerPos.x, playerPos.z, Math.abs(vehicle.getSpeedKmh()))
      && elapsedS - _signalViolationTime > SIGNAL_COOLDOWN_S) {
    _signalViolationTime = elapsedS;
    _showNotif('Feu rouge grillé !');
    if (wanted.level < 5) wanted._setLevel(Math.min(5, wanted.level + 1), hud);
  }

  // --- ReputationAgent : crime / conduite pacifique ---
  if (wanted.level === 0 && !drift.isDrifting()) {
    reputation.addPeaceful(district.getCurrent().id, dt * 0.3);
  }

  // --- WitnessAgent ---
  witness.update(dt, traffic.pedestrians);

  // --- FlashMobAgent — flash mobs piétons tous les 45s ---
  flashMob.update(dt, traffic.pedestrians, playerPos);
  if (flashMob.isActive() && flashMob.getDancerCount() > 0) {
    // Notification au démarrage (quand timeLeft ≈ DANCE_DURATION)
    if (flashMob.getTimeLeft() > 6.8) _showNotif(`Flash mob ! ${flashMob.getDancerCount()} piétons envahissent la rue !`);
  }

  // --- HonkCascadeAgent — cascade de klaxons sur quasi-frôlement ---
  honkCascade.update(dt, traffic.cars);
  // Détecte quasi-frôlement : joueur trop proche d'une voiture à vitesse > 30 km/h
  if (Math.abs(vehicle.getSpeedKmh()) > 30) {
    for (const car of traffic.cars) {
      if (!car.active || !car.mesh) continue;
      const hx = car.mesh.position.x - playerPos.x;
      const hz = car.mesh.position.z - playerPos.z;
      if (hx * hx + hz * hz < NEAR_MISS_DIST * NEAR_MISS_DIST) {
        honkCascade.triggerAt(car.mesh.position.x, car.mesh.position.z);
        break; // un déclencheur par frame suffit
      }
    }
  }
  // Met à jour les sprites "!" flottants au-dessus des voitures klaxonnantes
  for (const [mesh, ttl] of honkCascade.getAll()) {
    const entry = _getHonkSprite(mesh);
    // Projette la position 3D → écran
    const pos3 = mesh.position.clone();
    pos3.y += 2.5;
    pos3.project(camera);
    const sx = (pos3.x * 0.5 + 0.5) * window.innerWidth;
    const sy = (-pos3.y * 0.5 + 0.5) * window.innerHeight;
    entry.el.style.left = sx + 'px';
    entry.el.style.top  = sy + 'px';
    entry.el.style.opacity = String(Math.min(1, ttl));
    entry.el.style.display = 'block';
  }
  // Cache les sprites expirés
  for (const [mesh, entry] of _honkSprites) {
    if (!honkCascade.isHonking(mesh)) { entry.el.style.display = 'none'; }
  }

  // --- CopConfusionAgent — policier qui confond une civile avec le joueur ---
  copConfusion.update(dt, wanted.level, wanted.cars, traffic.cars);
  const confusionMsg = copConfusion.popMessage();
  if (confusionMsg) _showNotif(confusionMsg);

  // --- Garage : réparation auto quand le joueur arrive au garage ---
  const _gp = world.garagePos;
  if (vehicleDamage.getDamage() > 0 && _gp &&
      Math.hypot(playerPos.x - _gp.x, playerPos.z - _gp.z) < 5.5) {
    vehicleDamage.repair(vehicle._bodyMat);
    carShader.onRepair();
    _showNotif('Garage — véhicule réparé !');
  }

  combo.update(dt, playerPos, traffic.getCarPositions());
  drift.update(dt, vehicle);
  nitro.update(dt, playerPos, input);
  const boostNow  = nitro.isBoostActive();
  const nitroFired = boostNow && !lastBoostActive;
  smoke.update(dt, vehicle, drift.isDrifting());
  skids.update(dt, vehicle, drift.isDrifting());
  sparks.update(dt);

  const camViolation = speedCams.update(dt, vehicle, hud);
  if (camViolation && wanted.level < 5) wanted._setLevel(wanted.level + 1, hud);

  // Lampadaires : s'allument la nuit
  const nightIntensity = dayCycle.isNight() ? 1.4 : 0;
  for (const lamp of world.streetLamps) lamp.material.emissiveIntensity = nightIntensity;

  // Phares + feux du joueur (nuit)
  const isNight = dayCycle.isNight();
  if (vehicle._headlightMat) vehicle._headlightMat.emissiveIntensity = isNight ? 2.2 : 0;
  if (vehicle._taillightMat) vehicle._taillightMat.emissiveIntensity = isNight ? 1.8 : 0;

  // Phares + feux des voitures de trafic (nuit)
  for (const car of traffic.cars) {
    if (!car.active || !car.mesh) continue;
    if (car.mesh._hlMat) car.mesh._hlMat.emissiveIntensity = isNight ? 1.6 : 0;
    if (car.mesh._tlMat) car.mesh._tlMat.emissiveIntensity = isNight ? 1.4 : 0;
  }

  // Enseignes néon — pulsation sinusoïdale (Quartier Est)
  for (const ns of world.neonSigns) {
    ns.mat.emissiveIntensity = ns.base + Math.sin(now * 0.0015 + ns.phase) * 0.35;
  }

  // Brouillard dynamique selon météo (densité réduite sous la pluie)
  const targetFogFar = weather.getWeatherId() === 'rain' ? 180 : 260;
  scene.fog.far += (targetFogFar - scene.fog.far) * 0.008;

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
    architectPos: architect.getPosition(),
  });

  hud.setSpeed(vehicle.getSpeedKmh());

  const baseScore = missions.getScore() + rival.getScore() + combo.getScore() + fantome.getScore() + drift.getScore() + _resolveurBonusTotal;
  const monoBonus = monetization.update(
    dt, vehicle, wanted.level, drift,
    nitroFired,
    detective.popEscaped(),
    fantome.popWin(),
    baseScore
  );
  const emotionMult = emotion.getScoreMult() * cityPulse.getScoreMult();
  const totalScore = Math.round((baseScore + monoBonus) * emotionMult);
  hud.setScore(totalScore);

  // L'Architecte reacts to the player's actual score this frame
  const archResult = architect.update(dt, vehicle, hud, wanted, totalScore);
  if (archResult.raisedWanted && wanted.level < 5) wanted._setLevel(wanted.level + 1, hud);

  // MusicAgent — station radio manuelle ou sélection automatique
  const _musicState = (() => {
    const radioStyle = RADIO_STATIONS[_radioIdx].style;
    return radioStyle !== null ? radioStyle
      : architect.active ? 'boss'
      : wanted.level > 0 ? 'chase'
      : dayCycle.isNight() ? 'night'
      : 'city';
  })();
  if (musicAgent) musicAgent.setState(_musicState);

  // CityPulseAgent — pouls BPM synchronisé sur la musique
  cityPulse.setMusicState(_musicState);
  cityPulse.update(dt);
  ambientLight.intensity = 0.45 + cityPulse.getAmbientBoost();

  // EmotionEngine — événements wanted / drift / nitro / peaceful
  if (wanted.level > 0)       emotion.pushEvent('wanted', wanted.level / 5 * dt);
  if (drift.isDrifting())      emotion.pushEvent('drift',  drift.getDriftAngle() / 45 * dt);
  if (nitro.isBoostActive())   emotion.pushEvent('nitro',  dt);
  if (wanted.level === 0 && !drift.isDrifting() && Math.abs(vehicle.getSpeedKmh()) < 30)
                               emotion.pushEvent('peaceful', dt);
  emotion.update(dt);

  // --- Ronde 21 — Visual Excellence Agents ---
  trendRadar.update(dt);
  const _trendNotif = trendRadar.popNotif();
  if (_trendNotif) _showNotif(_trendNotif);
  atmosphere.update(dt, dayCycle);
  backroom.applySceneOverride(scene);
  weatherFX.update(dt, weather.getWeatherId(), playerPos);
  carShader.update(dt, vehicle, dayCycle);

  // --- Ronde 22 — Premium Agents ---
  commandant.update(dt, wanted, hud);
  const _cmdRadio = commandant.popRadioMessage();
  if (_cmdRadio) _showNotif(_cmdRadio);

  resolveur.update(dt, vehicle, wanted, vehicleDamage, nitro);
  const _resNotif = resolveur.popNotif();
  if (_resNotif) _showNotif(_resNotif);
  const _resBonus = resolveur.popBonus();
  if (_resBonus > 0) _resolveurBonusTotal += _resBonus;
  const _resNitro = resolveur.popNitroGrant();
  if (_resNitro) nitro._charges = Math.min(3, nitro._charges + 1);

  // --- Ronde 23 — Onirique & Horreur ---
  backroom.update(dt, playerPos, vehicle, dayCycle.isNight(), wanted.level);
  const _backNotif = backroom.popNotif();
  if (_backNotif) _showNotif(_backNotif);

  monster.update(dt, playerPos, dayCycle.isNight(), wanted.level, vehicle);
  const _monNotif = monster.popNotif();
  if (_monNotif) _showNotif(_monNotif);

  dreamzone.update(dt, playerPos, vehicleDamage);
  const _dzNotif = dreamzone.popNotif();
  if (_dzNotif) _showNotif(_dzNotif);
  const _dzBonus = dreamzone.popBonus();
  if (_dzBonus > 0) _resolveurBonusTotal += _dzBonus;
  const _dzHeal = dreamzone.popHeal();
  if (_dzHeal) { vehicleDamage.repair(vehicle._bodyMat); carShader.onRepair(); _showNotif('✨ Zone sacrée — Véhicule réparé !'); }
  const _dzTeleport = dreamzone.popTeleport();
  if (_dzTeleport) {
    const _tpAngle = Math.random() * Math.PI * 2;
    vehicle.mesh.position.set(Math.cos(_tpAngle) * 60, 0, Math.sin(_tpAngle) * 60);
    _showNotif('⬛ VORTEX COSMIQUE — Téléportation !');
  }

  // Teinte émotionnelle de la lumière ambiante
  const _tint = emotion.getColorTint();
  ambientLight.color.setRGB(_tint.r * 0.45, _tint.g * 0.45, _tint.b * 0.45 + cityPulse.getAmbientBoost());

  // PredictivePoliceAgent — interception prédictive (wanted ≥ 3)
  predictive.record(playerPos.x, playerPos.z);
  if (wanted.level >= 3) {
    const pred = predictive.predict(90);
    if (pred) {
      _predRing.position.set(pred.x, 0.3, pred.z);
      _predRing.visible = true;
      _predRingMat.opacity = 0.4 + pred.confidence * 0.5;
    }
  } else {
    _predRing.visible = false;
    if (wanted.level === 0) predictive.reset();
  }

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

  const dailyStatus = monetization.getDailyStatus();
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
        : traffic.crowdAgent.getActiveSignals() > 0
          ? `FOULE PANIQUE — ${traffic.crowdAgent.getActiveSignals()} signal(s)`
          : witness.getWitnessCount() > 0
            ? `${witness.getWitnessCount()} TÉMOIN(S) — Rep. ${reputation.getStatus(district.getCurrent().id)}`
            : `${district.getCurrent().name} | Combo x${combo.getMultiplier()}`,
      bar: witness.getWitnessCount() > 0
        ? Math.min(1, witness.getWitnessCount() / 6)
        : drift.isDrifting() ? Math.min(1, drift.getSessionScore() / 300) : combo.getMultiplier() / 5,
      color: witness.getWitnessCount() > 0 ? '#ff8800'
        : drift.isDrifting() ? '#ff6622'
        : traffic.crowdAgent.getActiveSignals() > 0 ? '#ff4422'
        : combo.getMultiplier() >= 3 ? '#ff9944' : '#55cc88',
    },
    monetisation: {
      active: dailyStatus.pct < 1,
      status: `${dailyStatus.label} | ${dailyStatus.text}`,
      bar: dailyStatus.pct,
      color: dailyStatus.pct >= 1 ? '#44ff88' : '#ffaa00',
    },
    nexus: {
      active: true,
      status: _nexusStatus(vehicle, drift, wanted, dayCycle, weather),
      bar: 1,
      color: '#00c8ff',
    },
    architecte: {
      active: architect.active,
      status: architect.active
        ? `EN CHASSE | dist ${Math.round(Math.hypot(playerPos.x - architect.mesh.position.x, playerPos.z - architect.mesh.position.z))}m`
        : totalScore >= 15000 ? `ALERTE — $${totalScore.toLocaleString()} atteint` : `Seuil $15 000 | Actuel $${totalScore.toLocaleString()}`,
      bar: architect.active ? 1 : Math.min(1, totalScore / 15000),
      color: architect.active ? '#ff0022' : '#880011',
    },
    emotion: {
      active: emotion.getMood() !== 'neutral',
      status: `${emotion.getMoodLabel()} | agressivité ${Math.round(emotion.getAggression())} sérénité ${Math.round(emotion.getSerenity())}`,
      bar: Math.max(emotion.getAggression(), emotion.getSerenity(), emotion.getEntropy()) / 100,
      color: emotion.getMood() === 'chaotic' ? '#ff2200' : emotion.getMood() === 'serene' ? '#44ddff' : '#ffaa00',
    },
    cityPulse: {
      active: cityPulse.isPeak(),
      status: `BPM ${cityPulse.getBpm()} | Beat ${Math.round(cityPulse.getIntensity() * 100)}% | Trafic ×${cityPulse.getTrafficMult().toFixed(2)}`,
      bar: cityPulse.getIntensity(),
      color: '#ff66cc',
    },
    predictive: {
      active: wanted.level >= 3 && predictive.getConfidence() > 0,
      status: wanted.level >= 3
        ? `Interception prédictive | confiance ${Math.round(predictive.getConfidence() * 100)}%`
        : 'En veille (wanted < 3)',
      bar: predictive.getConfidence(),
      color: '#ff4422',
    },
    flashMob: {
      active: flashMob.isActive(),
      status: flashMob.isActive()
        ? `FLASH MOB ! ${flashMob.getDancerCount()} danseurs | ${Math.round(flashMob.getTimeLeft())}s restant`
        : `Prochain mob dans ${Math.round(flashMob.getCooldown())}s`,
      bar: flashMob.isActive() ? flashMob.getTimeLeft() / 7 : Math.max(0, 1 - flashMob.getCooldown() / 45),
      color: '#ff88ff',
    },
    honkCascade: {
      active: honkCascade.getHonkingCount() > 0,
      status: `${honkCascade.getHonkingCount()} voiture(s) en panique | total: ${honkCascade.getTotalHonks()} klaxons`,
      bar: Math.min(1, honkCascade.getHonkingCount() / 8),
      color: '#ffdd00',
    },
    copConfusion: {
      active: copConfusion.isConfused(),
      status: copConfusion.isConfused()
        ? `POLICIER CONFUS ! Poursuite d'une civile | ${Math.round(copConfusion.getTimeLeft())}s`
        : `${copConfusion.getConfusionCount()} confusion(s) totale(s)`,
      bar: copConfusion.isConfused() ? copConfusion.getTimeLeft() / 9 : 0,
      color: '#ff9944',
    },
    trendRadar: {
      active: true,
      status: trendRadar.getStatusLine(),
      bar: trendRadar.getActiveCount() / trendRadar.getTotalCount(),
      color: '#00ffaa',
    },
    atmosphere: {
      active: true,
      status: `Sky gradient GLSL | God rays ${Math.round(atmosphere.getRayIntensity() * 100)}% | Étoiles ${Math.round(atmosphere.getStarOpacity() * 100)}%`,
      bar: 1,
      color: '#4499ff',
    },
    weatherFX: {
      active: weatherFX.isActive(),
      status: `Pluie volumétrique ${Math.round(weatherFX.getIntensity() * 100)}% | Flaques PBR + éclairs`,
      bar: weatherFX.getIntensity(),
      color: '#55aaff',
    },
    carShader: {
      active: true,
      status: `CubeMap env. + Clearcoat shimmer | Saleté ${Math.round(carShader.getDirtLevel() * 100)}%`,
      bar: 1 - carShader.getDirtLevel(),
      color: '#ffcc44',
    },
    commandant: {
      active: commandant.isActive(),
      status: commandant.isActive()
        ? `${commandant.getPlanLabel()} | Menace ${Math.round(commandant.getThreatLevel() * 100)}% | Rotation ${commandant.getTimeToNext() === Infinity ? '∞' : Math.round(commandant.getTimeToNext()) + 's'}`
        : 'En veille (wanted < 3)',
      bar: commandant.getThreatLevel(),
      color: commandant.getPlan() === 'FORCE_MAX' ? '#ff0000' : '#ff5500',
    },
    resolveur: {
      active: resolveur.isActive(),
      status: resolveur.isActive()
        ? (resolveur.isAnalyzing()
          ? `ANALYSE: ${resolveur.getSituation()}...`
          : `RÉSOLUTION: ${resolveur.getResolutionLabel()} | ${resolveur.getResolveCount()} résolution(s)`)
        : `En veille | ${resolveur.getResolveCount()} résolution(s) | CD ${Math.round(resolveur.getCooldown())}s`,
      bar: resolveur.isActive() ? 1 : Math.max(0, 1 - resolveur.getCooldown() / 32),
      color: resolveur.isAnalyzing() ? '#00aaff' : '#00ffcc',
    },
    backroom: {
      active: backroom.isActive(),
      status: backroom.isActive()
        ? `BACKROOM | Entité ${Math.round(backroom.getEntityDist())}m | ${Math.round(backroom.getTimer())}s | Fuite ${Math.round(backroom.getEscapePct() * 100)}%`
        : 'En veille — tourne à droite la nuit',
      bar: backroom.isActive() ? backroom.getEscapePct() : 0,
      color: '#c8b040',
    },
    monster: {
      active: monster.isActive(),
      status: monster.isActive()
        ? `${monster.getMonsterType()} | Dist. ${Math.round(monster.getDistance())}m | Peur ${Math.round(monster.getFearLevel() * 100)}%`
        : `${monster.getScareCount()} frayeur(s) | CD ${Math.round(monster.getCooldown())}s`,
      bar: monster.isActive() ? monster.getFearLevel() : 0,
      color: '#880033',
    },
    dreamzone: {
      active: true,
      status: `Zones magiques ${dreamzone.getVisitedCount()}/${dreamzone.getTotalCount()} visitées`,
      bar: dreamzone.getTotalCount() > 0 ? dreamzone.getVisitedCount() / dreamzone.getTotalCount() : 0,
      color: '#aa44ff',
    },
  });

  if (nitroFired) audio.playNitro();
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
    vehicleDamage.addImpact(impact);
    const dmgPct = Math.round(vehicleDamage.getDamage() * 100);
    if (dmgPct >= 75 && Math.round((vehicleDamage.getDamage() - impact * 0.22) * 100) < 75)
      _showNotif(`Carrosserie ${dmgPct}% — vitesse reduite !`);
    if (impact > 0.35) {
      sparks.emit(playerPos.x, playerPos.z, impact);
      traffic.crowdAgent.broadcast('crash', playerPos.x, playerPos.z, 18, impact);
      // Réputation et témoins
      reputation.addCrime(district.getCurrent().id, Math.ceil(impact * 3));
      const nearPeds = traffic.pedestrians.filter(p => p.active && p.mesh &&
        Math.hypot(p.mesh.position.x - playerPos.x, p.mesh.position.z - playerPos.z) < 15);
      witness.report(nearPeds, impact);
      if (witness.hasNearbyWitness(playerPos)) _showNotif('Des témoins alertent la police !');
      // EmotionEngine — crash brutal
      emotion.pushEvent('crash', impact);
      carShader.onCrash(impact);
    }
  }

  // Sirène police active → foule inquiète dans un rayon plus large
  if (wanted.level >= 2 && Math.floor(elapsedS) % 4 === 0) {
    traffic.crowdAgent.broadcast('police', playerPos.x, playerPos.z, 30, wanted.level / 5, 3);
  }
  // L'Architecte → vague de panique maximale
  if (architect.active && Math.floor(elapsedS) % 6 === 0) {
    const apos = architect.getPosition();
    if (apos) traffic.crowdAgent.broadcast('boss', apos.x, apos.z, 35, 1.0, 5);
  }

  // DialogueAgent — bulles de dialogue contextuelles au-dessus des piétons
  dialogueAgent.update(dt, traffic.pedestrians, playerPos, camera, renderer, {
    wantedLevel: wanted.level,
    weatherId: weather.getWeatherId(),
    isNight: dayCycle.isNight(),
    architectActive: architect.active,
    recentCrash: impact > 0.35,
  });
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
    HUD.submitScore(highScore);
    refreshColorPicker(); // unlock new swatches when record broken
  }

  if (wanted.level !== lastWantedLevel) audio.playUiBlip();
  lastWantedLevel = wanted.level;

  // Velocity motion blur: CSS filter scales with speed above 110 km/h.
  // Max 2.8 px at top speed — felt rather than seen.
  const absSpd = Math.abs(vehicle.getSpeedKmh());
  const blurPx = absSpd > 110 ? ((absSpd - 110) / 40) * 2.8 : 0;
  renderer.domElement.style.filter = blurPx > 0.15 ? `blur(${blurPx.toFixed(2)}px)` : '';

  renderer.render(scene, camera);
}

animate();
