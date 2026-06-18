import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { WitnessAgent } from '../js/witness.js';

function makePed(x = 0, z = 0) {
  return { active: true, mesh: { position: { x, y: 0, z } } };
}

describe('WitnessAgent', () => {
  test('démarre avec 0 témoins', () => {
    const wa = new WitnessAgent();
    assert.equal(wa.getWitnessCount(), 0);
  });

  test('report() ajoute des témoins', () => {
    const wa = new WitnessAgent();
    wa.report([makePed(0, 0), makePed(5, 5)], 1);
    assert.equal(wa.getWitnessCount(), 2);
  });

  test('les témoins expirent après leur TTL', () => {
    const wa = new WitnessAgent();
    wa.report([makePed()], 1); // TTL ≈ 30s
    for (let i = 0; i < 31; i++) wa.update(1, []); // simule 31 s en pas entiers
    assert.equal(wa.getWitnessCount(), 0, 'Témoin toujours actif après expiration');
  });

  test('hasNearbyWitness() true si témoin dans le rayon (22m)', () => {
    const wa = new WitnessAgent();
    wa.report([makePed(10, 0)], 1);
    wa.update(0.016, []);
    assert.ok(wa.hasNearbyWitness({ x: 0, z: 0 }), 'Témoin proche non détecté');
  });

  test('hasNearbyWitness() false si tous les témoins sont loin (> 22m)', () => {
    const wa = new WitnessAgent();
    wa.report([makePed(50, 50)], 1);
    wa.update(0.016, []);
    assert.ok(!wa.hasNearbyWitness({ x: 0, z: 0 }));
  });
});
