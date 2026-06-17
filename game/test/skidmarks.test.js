import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import { SkidMarkSystem } from '../js/skidmarks.js';

const mockScene = { add: () => {} };
const mockVehicle = {
  mesh: { position: { x: 0, y: 0, z: 0 } },
  getHeading: () => 0,
  getPosition: () => ({ x: 0, z: 0 }),
};

describe('SkidMarkSystem', () => {
  test('constructs without error', () => {
    assert.doesNotThrow(() => new SkidMarkSystem(mockScene));
  });

  test('update when drifting does not throw', () => {
    const system = new SkidMarkSystem(mockScene);
    assert.doesNotThrow(() => system.update(1 / 60, mockVehicle, true));
  });
});
