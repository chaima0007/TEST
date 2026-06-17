import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import { createWorld } from '../js/world.js';
import { DetectiveSystem } from '../js/detective.js';

const vehicleMock = {
  getPosition: () => ({ x: 0, z: 0 }),
  getSpeedKmh: () => 60,
  getHeading: () => 0,
};

const sceneMock = { add: () => {} };

describe('DetectiveSystem ("Le Detectif")', () => {
  test('starts inactive', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const detective = new DetectiveSystem(scene, world);

    assert.equal(detective.active, false);
  });

  test('does not spawn when wantedLevel < 2', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const detective = new DetectiveSystem(scene, world);
    detective._cooldown = 0;

    detective.update(1 / 60, vehicleMock, null, 1);

    assert.equal(detective.active, false);
  });

  test('spawns when wantedLevel >= 2 and cooldown is 0', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const detective = new DetectiveSystem(scene, world);
    detective._cooldown = 0;

    detective.update(1 / 60, vehicleMock, null, 2);

    assert.equal(detective.active, true);
    assert.ok(detective.mesh !== null, 'mesh should be set after spawning');
  });
});
