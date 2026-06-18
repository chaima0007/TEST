import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { CityPulseAgent } from '../js/citypulse.js';

describe('CityPulseAgent', () => {
  test('démarre avec intensité 0 et bpm 88', () => {
    const cp = new CityPulseAgent();
    assert.equal(cp.getIntensity(), 0);
    assert.equal(cp.getBpm(), 88);
  });

  test('setMusicState() synchronise le BPM', () => {
    const cp = new CityPulseAgent();
    cp.setMusicState('chase');
    assert.equal(cp.getBpm(), 128);
    cp.setMusicState('boss');
    assert.equal(cp.getBpm(), 140);
  });

  test('setBpm() est borné [40, 240]', () => {
    const cp = new CityPulseAgent();
    cp.setBpm(999);
    assert.equal(cp.getBpm(), 240);
    cp.setBpm(0);
    assert.equal(cp.getBpm(), 40);
  });

  test('phase progresse et reste dans [0, 1)', () => {
    const cp = new CityPulseAgent();
    cp.update(0.5);
    const p = cp.getPhase();
    assert.ok(p >= 0 && p < 1, `phase=${p} hors limites`);
  });

  test('isPeak() vrai quand intensité > 0.85 (attaque du beat)', () => {
    const cp = new CityPulseAgent();
    // Phase ≈ 0.05 → intensité ≈ 0.5 — pas encore peak
    // Pour atteindre le pic : phase 0..0.1 → intensity=phase/0.1
    // On avance très peu pour rester dans la zone d'attaque
    const bps = 88 / 60; // ~1.467 bps
    // dt tel que phase = 0.09 → intensity = 0.9 > 0.85
    cp.update(0.09 / bps);
    assert.ok(cp.isPeak(), `isPeak faux, intensity=${cp.getIntensity()}`);
  });

  test('getTrafficMult() dans [0.8, 1.3] et getScoreMult() dans [1.0, 1.3]', () => {
    const cp = new CityPulseAgent();
    for (let i = 0; i < 120; i++) {
      cp.update(0.016);
      const tm = cp.getTrafficMult();
      const sm = cp.getScoreMult();
      assert.ok(tm >= 0.799 && tm <= 1.301, `trafficMult=${tm}`);
      assert.ok(sm >= 1.0 && sm <= 1.301, `scoreMult=${sm}`);
    }
  });
});
