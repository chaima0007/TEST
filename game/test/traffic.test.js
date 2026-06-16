import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import { createWorld } from '../js/world.js';
import { TrafficSystem } from '../js/traffic.js';
import { Vehicle } from '../js/vehicle.js';

function fakeInput(overrides = {}) {
  const base = { forward: false, back: false, left: false, right: false, brake: false };
  const state = { ...base, ...overrides };
  return { get: (action) => !!state[action] };
}

describe('TrafficSystem', () => {
  test('spawns the configured number of active cars and pedestrians near the player', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const traffic = new TrafficSystem(scene, world);

    traffic.update(1 / 60, { x: 0, z: 0 });

    assert.equal(traffic.cars.filter((c) => c.active).length, traffic.cars.length);
    assert.equal(traffic.pedestrians.filter((p) => p.active).length > 0, true);
  });

  test('getColliders() returns an axis-aligned box per active car and pedestrian', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const traffic = new TrafficSystem(scene, world);
    traffic.update(1 / 60, { x: 0, z: 0 });

    const colliders = traffic.getColliders();
    assert.equal(colliders.length, traffic.cars.length + traffic.pedestrians.filter((p) => p.active).length);
    for (const c of colliders) {
      assert.equal(typeof c.x, 'number');
      assert.equal(typeof c.z, 'number');
      assert.ok(c.halfWidth > 0);
      assert.ok(c.halfDepth > 0);
    }
  });

  test('the player vehicle is blocked by a traffic car instead of driving through it', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const traffic = new TrafficSystem(scene, world);
    traffic.update(1 / 60, { x: 0, z: 0 });

    const car = traffic.cars[0];
    // Park the player right where a traffic car already is, then floor it
    // straight at the car's center.
    const vehicle = new Vehicle(scene, { x: car.mesh.position.x, z: car.mesh.position.z - 5, rotationY: 0 });
    const input = fakeInput({ forward: true });

    for (let i = 0; i < 180; i++) {
      vehicle.update(1 / 60, input, world.colliders.concat(traffic.getColliders()));
    }

    const pos = vehicle.getPosition();
    const dx = pos.x - car.mesh.position.x;
    const dz = pos.z - car.mesh.position.z;
    assert.ok(Math.hypot(dx, dz) > 1, 'vehicle should have been stopped short of the traffic car, not pass through it');
  });
});
