import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import { createWorld } from '../js/world.js';
import { WantedSystem } from '../js/police.js';

function fakeVehicleAt(x, z) {
  let speed = 0;
  return {
    setSpeed: (v) => { speed = v; },
    getPosition: () => ({ x, z }),
    getSpeedKmh: () => speed,
    getHeading: () => 0,
  };
}

describe('WantedSystem', () => {
  test('sustained speeding escalates the wanted level and spawns police cars', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const wanted = new WantedSystem(scene, world);
    const vehicle = fakeVehicleAt(-50, -50);

    for (let i = 0; i < 720; i++) { // 12s ramp to 140 km/h then hold
      vehicle.setSpeed(Math.min(140, (i / 120) * 140));
      wanted.update(1 / 60, vehicle, null);
    }

    assert.ok(wanted.level > 0, 'wanted level should have escalated');
    assert.equal(wanted.cars.length > 0, true, 'police cars should have spawned');
  });

  test('a smooth deceleration to a legal speed does not falsely trigger crash detection', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const wanted = new WantedSystem(scene, world);
    const vehicle = fakeVehicleAt(-50, -50);

    for (let i = 0; i < 720; i++) {
      vehicle.setSpeed(Math.min(140, (i / 120) * 140));
      wanted.update(1 / 60, vehicle, null);
    }
    const levelBeforeBraking = wanted.level;

    for (let i = 0; i < 60; i++) { // smooth 1s deceleration to 30 km/h, no instant jump
      vehicle.setSpeed(Math.max(30, 140 - (i / 60) * 110));
      wanted.update(1 / 60, vehicle, null);
    }

    assert.equal(wanted.level, levelBeforeBraking, 'smooth braking must not be misread as a crash');
  });

  test('clean driving below the threshold decays the wanted level back to 0 and despawns police', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const wanted = new WantedSystem(scene, world);
    const vehicle = fakeVehicleAt(-50, -50);

    for (let i = 0; i < 720; i++) {
      vehicle.setSpeed(Math.min(140, (i / 120) * 140));
      wanted.update(1 / 60, vehicle, null);
    }
    for (let i = 0; i < 60; i++) {
      vehicle.setSpeed(Math.max(30, 140 - (i / 60) * 110));
      wanted.update(1 / 60, vehicle, null);
    }
    assert.ok(wanted.level > 0, 'precondition: should be wanted before the clean-driving window');

    for (let i = 0; i < 1800; i++) wanted.update(1 / 60, vehicle, null); // 30s clean at 30 km/h

    assert.equal(wanted.level, 0, 'wanted level should fully decay after sustained clean driving');
    assert.equal(wanted.cars.length, 0, 'police cars should despawn once wanted level reaches 0');
  });
});
