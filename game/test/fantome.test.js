import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { FantomeSystem } from '../js/fantome.js';

function makeScene() {
  return { add: () => {}, remove: () => {} };
}

// vehicle.position is what _spawn() reads (vehicle.position or vehicle.chassisBody.position)
function makeVehicle(x = 0, z = 0) {
  return { position: { x, z } };
}

describe('FantomeSystem', () => {
  test('starts inactive with score 0', () => {
    const fs = new FantomeSystem(makeScene(), {});
    assert.equal(fs._active, false);
    assert.equal(fs.getScore(), 0);
  });

  test('does not spawn during day (isNight=false)', () => {
    const fs = new FantomeSystem(makeScene(), {});
    fs.update(100, makeVehicle(), null, false);
    assert.equal(fs._active, false);
  });

  test('cooldown decrements when isNight=true and spawns once cooldown expires', () => {
    const fs = new FantomeSystem(makeScene(), {});
    fs._cooldown = 1;
    fs.update(2, makeVehicle(), null, true);
    assert.equal(fs._active, true);
  });

  test('getScore returns 0 initially', () => {
    const fs = new FantomeSystem(makeScene(), {});
    assert.equal(fs.getScore(), 0);
  });
});
