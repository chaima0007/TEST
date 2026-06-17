import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { NitroSystem } from '../js/nitro.js';

function makeScene() {
  return { add: () => {}, remove: () => {} };
}

const mockInput = { get: (k) => k === 'nitro' };
const noInput   = { get: () => false };
const playerPos = { x: 0, z: 0 };

describe('NitroSystem', () => {
  test('starts with 0 charges', () => {
    const system = new NitroSystem(makeScene());
    assert.equal(system.getCharges(), 0);
  });

  test('boost is not active initially', () => {
    const system = new NitroSystem(makeScene());
    assert.equal(system.isBoostActive(), false);
  });

  test('collecting a capsule adds a charge', () => {
    const system = new NitroSystem(makeScene());
    // Spawn capsule close to the player (within COLLECT_RADIUS of 5.5m)
    system._spawnCapsule({ x: 0, z: 0 });
    // Manually place the capsule at (3, 0) so it's within collection range
    const cap = system._capsules[system._capsules.length - 1];
    cap.x = 3;
    cap.z = 0;
    cap.mesh.position.set(3, 0, 0);

    system.update(1 / 60, playerPos, noInput);

    assert.equal(system.getCharges(), 1);
  });

  test('pressing N with a charge activates boost', () => {
    const system = new NitroSystem(makeScene());
    system._charges = 1;
    system.update(1 / 60, playerPos, mockInput);
    assert.equal(system.isBoostActive(), true);
  });
});
