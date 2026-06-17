import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { WeatherSystem } from '../js/weather.js';

function makeScene() {
  return { add: () => {}, remove: () => {}, background: null };
}

describe('WeatherSystem', () => {
  test('starts with CLEAR weather', () => {
    const ws = new WeatherSystem(makeScene());
    assert.equal(ws.getWeatherId(), 'CLEAR');
  });

  test('grip factor is 1.0 initially', () => {
    const ws = new WeatherSystem(makeScene());
    assert.equal(ws.getGripFactor(), 1.0);
  });

  test('update(dt) does not crash', () => {
    const ws = new WeatherSystem(makeScene());
    ws.update(1 / 60, { x: 0, z: 0 });
  });

  test('grip factor stays at 1.0 during CLEAR weather after many updates', () => {
    const ws = new WeatherSystem(makeScene());
    // Lock into CLEAR so the timer never triggers a transition
    ws._current = { id: 'CLEAR', grip: 1.0, minDur: 600, maxDur: 600 };
    ws._timer = 600;
    for (let i = 0; i < 100; i++) {
      ws.update(1 / 60, { x: 0, z: 0 });
    }
    assert.ok(ws.getGripFactor() >= 0.95, `expected gripFactor >= 0.95, got ${ws.getGripFactor()}`);
  });
});
