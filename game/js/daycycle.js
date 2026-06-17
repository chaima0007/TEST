import * as THREE from 'three';

const SKY_KEYFRAMES = [
  { t: 0.00, color: 0x020310, ambient: 0.08 },
  { t: 0.10, color: 0x050520, ambient: 0.05 },
  { t: 0.25, color: 0xff6633, ambient: 0.25 },
  { t: 0.35, color: 0x87ceeb, ambient: 0.45 },
  { t: 0.50, color: 0x4db8ff, ambient: 0.55 },
  { t: 0.65, color: 0x87ceeb, ambient: 0.45 },
  { t: 0.75, color: 0xff7733, ambient: 0.30 },
  { t: 0.88, color: 0x1a0a2e, ambient: 0.12 },
  { t: 1.00, color: 0x020310, ambient: 0.08 },
];

function lerpColor(hexA, hexB, alpha) {
  const rA = (hexA >> 16) & 0xff, gA = (hexA >> 8) & 0xff, bA = hexA & 0xff;
  const rB = (hexB >> 16) & 0xff, gB = (hexB >> 8) & 0xff, bB = hexB & 0xff;
  return (
    (Math.round(rA + (rB - rA) * alpha) << 16) |
    (Math.round(gA + (gB - gA) * alpha) << 8) |
    Math.round(bA + (bB - bA) * alpha)
  );
}

function sampleSky(t) {
  for (let i = 0; i < SKY_KEYFRAMES.length - 1; i++) {
    const a = SKY_KEYFRAMES[i], b = SKY_KEYFRAMES[i + 1];
    if (t >= a.t && t <= b.t) {
      const alpha = (t - a.t) / (b.t - a.t);
      return {
        color: lerpColor(a.color, b.color, alpha),
        ambient: a.ambient + (b.ambient - a.ambient) * alpha,
      };
    }
  }
  return { color: SKY_KEYFRAMES[0].color, ambient: SKY_KEYFRAMES[0].ambient };
}

const CYCLE_DURATION = 300;
const TWO_PI = Math.PI * 2;

export class DayCycle {
  constructor(scene, sunLight, ambientLight) {
    this._scene = scene;
    this._sun = sunLight;
    this._ambient = ambientLight;
    this._timeOfDay = 0.35;
    this._bgColor = new THREE.Color();
  }

  update(dt) {
    this._timeOfDay = (this._timeOfDay + dt / CYCLE_DURATION) % 1;
    const t = this._timeOfDay;
    const sky = sampleSky(t);

    this._bgColor.setHex(sky.color);
    this._scene.background = this._bgColor;
    if (this._scene.fog) this._scene.fog.color.setHex(sky.color);

    this._ambient.intensity = sky.ambient;

    const sunAngle = (t - 0.25) * TWO_PI;
    this._sun.position.set(
      Math.cos(sunAngle) * 80,
      Math.sin(sunAngle) * 100,
      40
    );

    const sinAngle = Math.sin(sunAngle);
    this._sun.intensity = 0.2 + Math.max(0, sinAngle) * 1.0;

    // Sun color: warm at horizon, white at peak
    const horizonFactor = 1 - Math.min(1, Math.abs(sinAngle) * 4);
    const sunColor = lerpColor(0xffffff, 0xff8833, horizonFactor);
    this._sun.color.setHex(sunColor);
  }

  isNight() {
    return this._timeOfDay > 0.78 || this._timeOfDay < 0.22;
  }

  getTimeString() {
    const totalMinutes = Math.floor(this._timeOfDay * 24 * 60);
    const hours = Math.floor(totalMinutes / 60) % 24;
    const minutes = totalMinutes % 60;
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
  }

  getTimeOfDay() {
    return this._timeOfDay;
  }
}
