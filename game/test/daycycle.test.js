import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { DayCycle } from '../js/daycycle.js';

function makeScene() {
  return { background: null, fog: { color: { setHex: () => {} } } };
}

function makeSunLight() {
  return { position: { set: () => {} }, intensity: 1, color: { setHex: () => {} } };
}

function makeAmbientLight() {
  return { intensity: 0.45 };
}

describe('DayCycle', () => {
  test('starts at timeOfDay 0.35', () => {
    const dc = new DayCycle(makeScene(), makeSunLight(), makeAmbientLight());
    assert.equal(dc._timeOfDay, 0.35);
  });

  test('advances timeOfDay when update(dt) is called', () => {
    const dc = new DayCycle(makeScene(), makeSunLight(), makeAmbientLight());
    dc.update(1);
    assert.ok(dc._timeOfDay > 0.35, `expected timeOfDay > 0.35, got ${dc._timeOfDay}`);
  });

  test('isNight returns true when timeOfDay is 0.85', () => {
    const dc = new DayCycle(makeScene(), makeSunLight(), makeAmbientLight());
    dc._timeOfDay = 0.85;
    assert.equal(dc.isNight(), true);
  });

  test('isNight returns false at noon', () => {
    const dc = new DayCycle(makeScene(), makeSunLight(), makeAmbientLight());
    dc._timeOfDay = 0.5;
    assert.equal(dc.isNight(), false);
  });

  test('getTimeString returns HH:MM format', () => {
    const dc = new DayCycle(makeScene(), makeSunLight(), makeAmbientLight());
    const timeStr = dc.getTimeString();
    assert.match(timeStr, /^\d{2}:\d{2}$/);
  });
});
