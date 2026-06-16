import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import { Vehicle } from '../js/vehicle.js';

function fakeInput(overrides = {}) {
  const base = { forward: false, back: false, left: false, right: false, brake: false };
  const state = { ...base, ...overrides };
  return { get: (action) => !!state[action] };
}

describe('Vehicle', () => {
  test('accelerates forward and moves from spawn under sustained throttle', () => {
    const scene = new THREE.Scene();
    const vehicle = new Vehicle(scene, { x: 0, z: 0, rotationY: 0 });
    const input = fakeInput({ forward: true });

    for (let i = 0; i < 240; i++) vehicle.update(1 / 60, input, []); // 4 simulated seconds

    assert.ok(vehicle.getSpeedKmh() > 50, `expected meaningful speed, got ${vehicle.getSpeedKmh()}`);
    const pos = vehicle.getPosition();
    assert.ok(Math.abs(pos.x) > 1 || Math.abs(pos.z) > 1, 'vehicle should have moved from spawn');
  });

  test('natural friction brings the car to a stop with no throttle', () => {
    const scene = new THREE.Scene();
    const vehicle = new Vehicle(scene, { x: 0, z: 0, rotationY: 0 });
    vehicle.update(1 / 60, fakeInput({ forward: true }), []);
    for (let i = 0; i < 60; i++) vehicle.update(1 / 60, fakeInput({ forward: true }), []);
    assert.ok(vehicle.getSpeedKmh() > 0);

    for (let i = 0; i < 300; i++) vehicle.update(1 / 60, fakeInput(), []); // no input, 5s
    assert.equal(vehicle.getSpeedKmh(), 0);
  });

  test('a collider directly ahead stops forward progress instead of clipping through', () => {
    const scene = new THREE.Scene();
    const vehicle = new Vehicle(scene, { x: 0, z: 0, rotationY: 0 }); // heading 0 -> moves toward +Z
    const colliders = [{ x: 0, z: 5, halfWidth: 3, halfDepth: 3 }];
    const input = fakeInput({ forward: true });

    for (let i = 0; i < 600; i++) vehicle.update(1 / 60, input, colliders); // 10s, would reach ~150km/h unobstructed

    const pos = vehicle.getPosition();
    assert.ok(pos.z < 5 - 3 + 0.5, `vehicle should not pass through the collider, got z=${pos.z}`);
  });

  test('reverse moves the car backward and is capped below forward top speed', () => {
    const scene = new THREE.Scene();
    const vehicle = new Vehicle(scene, { x: 0, z: 0, rotationY: 0 });
    const input = fakeInput({ back: true });

    for (let i = 0; i < 300; i++) vehicle.update(1 / 60, input, []); // 5s

    assert.ok(vehicle.getSpeedKmh() < 0, 'reversing should report negative speed');
    assert.ok(Math.abs(vehicle.getSpeedKmh()) < 150, 'reverse top speed must stay below forward top speed');
  });

  test('reports a nonzero impact intensity on a hard collision, and zero otherwise', () => {
    const scene = new THREE.Scene();
    const vehicle = new Vehicle(scene, { x: 0, z: 0, rotationY: 0 });
    const colliders = [{ x: 0, z: 5, halfWidth: 3, halfDepth: 3 }];
    const input = fakeInput({ forward: true });

    assert.equal(vehicle.getImpactIntensity(), 0, 'no impact before moving');

    let sawHardImpact = false;
    for (let i = 0; i < 300; i++) {
      vehicle.update(1 / 60, input, colliders);
      if (vehicle.getImpactIntensity() > 0.3) sawHardImpact = true;
    }
    assert.ok(sawHardImpact, 'expected a strong impact intensity while ramming the collider at speed');

    // Once settled against the wall under continued throttle, the car keeps nudging into it
    // each frame (held back by collision resolution), so a small residual impact is expected —
    // but it should be far below the initial hard-impact magnitude, not still climbing.
    for (let i = 0; i < 30; i++) vehicle.update(1 / 60, input, colliders);
    assert.ok(vehicle.getImpactIntensity() < 0.1, `expected a small settled-state impact, got ${vehicle.getImpactIntensity()}`);
  });
});
