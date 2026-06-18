import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { ReputationAgent } from '../js/reputation.js';

describe('ReputationAgent', () => {
  test('démarre à 0 dans chaque quartier', () => {
    const ra = new ReputationAgent();
    for (const id of ['centre', 'nord', 'sud', 'ouest', 'est']) {
      assert.equal(ra.getRep(id), 0, `Réputation non nulle au départ pour ${id}`);
    }
  });

  test('addCrime() réduit la réputation', () => {
    const ra = new ReputationAgent();
    ra.addCrime('centre', 1);
    assert.ok(ra.getRep('centre') < 0, `Réputation attendue négative`);
  });

  test('addPeaceful() augmente la réputation', () => {
    const ra = new ReputationAgent();
    ra.addCrime('nord', 5); // on baisse d'abord
    const after = ra.getRep('nord');
    ra.addPeaceful('nord', 10);
    assert.ok(ra.getRep('nord') > after);
  });

  test('réputation plancher à -100', () => {
    const ra = new ReputationAgent();
    for (let i = 0; i < 20; i++) ra.addCrime('centre', 5);
    assert.equal(ra.getRep('centre'), -100);
  });

  test('réputation plafond à +100', () => {
    const ra = new ReputationAgent();
    for (let i = 0; i < 200; i++) ra.addPeaceful('est', 1);
    assert.equal(ra.getRep('est'), 100);
  });

  test('getMultiplier() = 1.5 pour réputation +100', () => {
    const ra = new ReputationAgent();
    for (let i = 0; i < 200; i++) ra.addPeaceful('sud', 1);
    assert.ok(Math.abs(ra.getMultiplier('sud') - 1.5) < 0.001);
  });

  test('getMultiplier() = 0.5 pour réputation -100', () => {
    const ra = new ReputationAgent();
    for (let i = 0; i < 20; i++) ra.addCrime('nord', 5);
    assert.ok(Math.abs(ra.getMultiplier('nord') - 0.5) < 0.001);
  });

  test('shouldFlee() true quand réputation < -30', () => {
    const ra = new ReputationAgent();
    for (let i = 0; i < 5; i++) ra.addCrime('ouest', 1);
    assert.ok(ra.shouldFlee('ouest'), `shouldFlee attendu true (rep=${ra.getRep('ouest')})`);
  });
});
