import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { PredictivePoliceAgent } from '../js/predictive.js';

describe('PredictivePoliceAgent', () => {
  test('renvoie null avec moins de 5 échantillons', () => {
    const pa = new PredictivePoliceAgent();
    pa.record(0, 0);
    pa.record(1, 0);
    pa.record(2, 0);
    pa.record(3, 0);
    assert.equal(pa.predict(), null);
  });

  test('renvoie une position {x, z} avec 5+ échantillons', () => {
    const pa = new PredictivePoliceAgent();
    for (let i = 0; i < 6; i++) pa.record(i * 2, 0);
    const result = pa.predict(10);
    assert.ok(result !== null);
    assert.ok(typeof result.x === 'number');
    assert.ok(typeof result.z === 'number');
  });

  test('la confiance croît avec le nombre de points (max 1.0)', () => {
    const pa = new PredictivePoliceAgent();
    for (let i = 0; i < 5; i++) pa.record(i, 0);
    pa.predict();
    const c1 = pa.getConfidence();
    for (let i = 5; i < 20; i++) pa.record(i, 0);
    pa.predict();
    const c2 = pa.getConfidence();
    assert.ok(c2 > c1, `confiance n'a pas progressé: c1=${c1} c2=${c2}`);
    assert.ok(c2 <= 1.0, `confiance dépasse 1.0: ${c2}`);
  });

  test('la prédiction suit la direction de déplacement', () => {
    const pa = new PredictivePoliceAgent();
    // Déplacement constant vers x+ (vx=5 par frame)
    for (let i = 0; i < 10; i++) pa.record(i * 5, 0);
    const result = pa.predict(1); // lookahead=1
    assert.ok(result.x > 45, `prédiction x=${result.x} devrait dépasser 45`);
  });

  test('reset() efface l\'historique et retourne null', () => {
    const pa = new PredictivePoliceAgent();
    for (let i = 0; i < 10; i++) pa.record(i, 0);
    pa.predict();
    pa.reset();
    assert.equal(pa.predict(), null);
    assert.equal(pa.getConfidence(), 0);
    assert.equal(pa.getPredicted(), null);
  });
});
