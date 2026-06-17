import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import { TireSmokeSystem } from '../js/particles.js';

const mockScene = { add: () => {} };
const mockVehicle = {
  mesh: { position: { x: 0, y: 0, z: 0 } },
  getHeading: () => 0,
};

describe('TireSmokeSystem', () => {
  test('constructs without error', () => {
    assert.doesNotThrow(() => new TireSmokeSystem(mockScene));
  });

  test('update does not throw when isDrifting=false', () => {
    const system = new TireSmokeSystem(mockScene);
    assert.doesNotThrow(() => system.update(1 / 60, mockVehicle, false));
  });
});
