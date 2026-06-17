import * as THREE from 'three';

const WEATHER = {
  CLEAR:  { id: 'CLEAR',  grip: 1.00, minDur: 60,  maxDur: 120 },
  CLOUDY: { id: 'CLOUDY', grip: 0.90, minDur: 30,  maxDur: 60  },
  RAIN:   { id: 'RAIN',   grip: 0.65, minDur: 20,  maxDur: 45  },
  STORM:  { id: 'STORM',  grip: 0.45, minDur: 15,  maxDur: 30  },
};

const TRANSITIONS = {
  CLEAR:  ['CLEAR', 'CLOUDY'],
  CLOUDY: ['CLEAR', 'CLOUDY', 'RAIN'],
  RAIN:   ['CLOUDY', 'RAIN', 'STORM'],
  STORM:  ['RAIN', 'CLOUDY', 'CLEAR'],
};

const RAIN_COUNT = 1500;
const RAIN_AREA = 60;
const RAIN_SPEED = 28;
const THUNDER_MIN = 4;
const THUNDER_MAX = 8;
const THUNDER_FLASH_DURATION = 0.12;

function randRange(min, max) {
  return min + Math.random() * (max - min);
}

function buildRainSystem() {
  const positions = new Float32Array(RAIN_COUNT * 3);
  for (let i = 0; i < RAIN_COUNT; i++) {
    positions[i * 3]     = randRange(-RAIN_AREA, RAIN_AREA);
    positions[i * 3 + 1] = randRange(0, RAIN_AREA);
    positions[i * 3 + 2] = randRange(-RAIN_AREA, RAIN_AREA);
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const mat = new THREE.PointsMaterial({
    color: 0xaabbdd,
    size: 0.1,
    transparent: true,
    opacity: 0.5,
    depthWrite: false,
  });
  return new THREE.Points(geo, mat);
}

export class WeatherSystem {
  constructor(scene) {
    this._scene = scene;
    this._current = WEATHER.CLEAR;
    this._timer = randRange(WEATHER.CLEAR.minDur, WEATHER.CLEAR.maxDur);
    this._gripFactor = 1.0;

    this._rain = buildRainSystem();
    this._rain.visible = false;
    scene.add(this._rain);

    this._thunderTimer = randRange(THUNDER_MIN, THUNDER_MAX);
    this._flashTimer = 0;
    this._savedBg = null;
  }

  update(dt, playerPos) {
    this._timer -= dt;
    if (this._timer <= 0) {
      const options = TRANSITIONS[this._current.id];
      const nextId = options[Math.floor(Math.random() * options.length)];
      this._current = WEATHER[nextId];
      this._timer = randRange(this._current.minDur, this._current.maxDur);
    }

    const isWet = this._current.id === 'RAIN' || this._current.id === 'STORM';
    this._rain.visible = isWet;

    if (isWet && playerPos) {
      this._rain.position.x = playerPos.x;
      this._rain.position.z = playerPos.z;
    }

    if (isWet) {
      const pos = this._rain.geometry.attributes.position;
      const arr = pos.array;
      for (let i = 0; i < RAIN_COUNT; i++) {
        arr[i * 3 + 1] -= RAIN_SPEED * dt;
        if (arr[i * 3 + 1] < 0) {
          arr[i * 3]     = randRange(-RAIN_AREA, RAIN_AREA);
          arr[i * 3 + 1] = RAIN_AREA;
          arr[i * 3 + 2] = randRange(-RAIN_AREA, RAIN_AREA);
        }
      }
      pos.needsUpdate = true;
    }

    if (this._current.id === 'STORM') {
      if (this._flashTimer > 0) {
        this._flashTimer -= dt;
        if (this._flashTimer <= 0 && this._savedBg !== null) {
          this._scene.background = this._savedBg;
          this._savedBg = null;
        }
      } else {
        this._thunderTimer -= dt;
        if (this._thunderTimer <= 0) {
          this._savedBg = this._scene.background
            ? this._scene.background.clone()
            : new THREE.Color(0x020310);
          this._scene.background = new THREE.Color(0xccddff);
          this._flashTimer = THUNDER_FLASH_DURATION;
          this._thunderTimer = randRange(THUNDER_MIN, THUNDER_MAX);
        }
      }
    } else {
      // Restore background if storm ended mid-flash
      if (this._savedBg !== null) {
        this._scene.background = this._savedBg;
        this._savedBg = null;
        this._flashTimer = 0;
      }
      this._thunderTimer = randRange(THUNDER_MIN, THUNDER_MAX);
    }

    this._gripFactor += (this._current.grip - this._gripFactor) * Math.min(1, dt * 0.5);
  }

  getGripFactor() {
    return this._gripFactor;
  }

  getWeatherId() {
    return this._current.id;
  }

  dispose() {
    this._rain.geometry.dispose();
    this._rain.material.dispose();
    this._scene.remove(this._rain);
  }
}
