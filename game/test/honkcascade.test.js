import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { HonkCascadeAgent } from '../js/honkcascade.js';

function makeCar(x = 0, z = 0) {
  return { active: true, mesh: { position: { x, y: 0, z } } };
}

describe('HonkCascadeAgent', () => {
  test('démarre avec 0 voiture klaxonnante', () => {
    const hc = new HonkCascadeAgent();
    assert.equal(hc.getHonkingCount(), 0);
  });

  test('triggerAt() fait klaxonner les voitures proches lors du prochain update', () => {
    const hc = new HonkCascadeAgent();
    const cars = [makeCar(5, 0), makeCar(8, 0), makeCar(50, 0)]; // 3e trop loin
    hc.triggerAt(0, 0);
    hc.update(0.016, cars); // première frame
    assert.ok(hc.getHonkingCount() >= 2, `seulement ${hc.getHonkingCount()} voiture(s) klaxonnante(s)`);
    assert.ok(!hc.isHonking(cars[2].mesh), 'voiture lointaine ne devrait pas klaxonner');
  });

  test('les klaxons expirent après leur TTL (1.8s)', () => {
    const hc = new HonkCascadeAgent();
    const cars = [makeCar(3, 0)];
    hc.triggerAt(0, 0);
    // Simule en petits pas : la vague de propagation s'éteint avant expiration
    for (let i = 0; i < 130; i++) hc.update(0.016, cars); // ≈ 2.1s > TTL 1.8s
    assert.equal(hc.getHonkingCount(), 0, 'klaxon toujours actif après expiration');
  });

  test('la cascade se propage par vagues (wave delay)', () => {
    const hc = new HonkCascadeAgent();
    // 3 voitures en ligne séparées par 11m (dans le rayon de 12m)
    const cars = [makeCar(11, 0), makeCar(22, 0), makeCar(33, 0)];
    hc.triggerAt(0, 0);
    hc.update(0, cars);     // vague 0 → voiture 0
    const after0 = hc.getHonkingCount();
    hc.update(0.25, cars);  // vague 1 → voiture 1
    const after1 = hc.getHonkingCount();
    hc.update(0.25, cars);  // vague 2 → voiture 2
    const after2 = hc.getHonkingCount();
    assert.ok(after1 >= after0, `pas de propagation : after0=${after0} after1=${after1}`);
    assert.ok(after2 >= after1, `pas de propagation : after1=${after1} after2=${after2}`);
  });

  test('getTotalHonks() accumule toutes les voitures déclenchées', () => {
    const hc = new HonkCascadeAgent();
    const cars = [makeCar(3, 0), makeCar(5, 0)];
    hc.triggerAt(0, 0);
    hc.update(0, cars);
    assert.ok(hc.getTotalHonks() >= 1);
  });
});
