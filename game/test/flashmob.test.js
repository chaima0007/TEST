import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { FlashMobAgent } from '../js/flashmob.js';

function makePed(x = 0, z = 0) {
  return {
    active: true,
    mesh: { position: { x, y: 0, z }, rotation: { y: 0 } },
  };
}

describe('FlashMobAgent', () => {
  test('démarre inactif et avec un cooldown court (< 45s)', () => {
    const fm = new FlashMobAgent();
    assert.ok(!fm.isActive());
    assert.ok(fm.getCooldown() < 45);
  });

  test('ne se déclenche pas si moins de 3 piétons proches', () => {
    const fm = new FlashMobAgent();
    const peds = [makePed(1, 0), makePed(2, 0)]; // 2 seulement
    // Avance jusqu'à cooldown 0
    fm.update(30, peds, { x: 0, z: 0 });
    assert.ok(!fm.isActive(), 'Flash mob déclenché avec seulement 2 piétons');
  });

  test('se déclenche quand ≥ 3 piétons sont à portée après le cooldown', () => {
    const fm = new FlashMobAgent();
    const peds = [makePed(1, 0), makePed(2, 0), makePed(3, 0), makePed(4, 0)];
    fm.update(50, peds, { x: 0, z: 0 }); // dépasse le cooldown
    assert.ok(fm.isActive(), 'Flash mob non déclenché avec 4 piétons');
    assert.ok(fm.getDancerCount() >= 3);
  });

  test('se termine après DANCE_DURATION secondes', () => {
    const fm = new FlashMobAgent();
    const peds = Array.from({ length: 5 }, (_, i) => makePed(i, 0));
    fm.update(50, peds, { x: 0, z: 0 });
    assert.ok(fm.isActive());
    fm.update(8, peds, { x: 0, z: 0 }); // 7s de danse + marge
    assert.ok(!fm.isActive(), 'Flash mob toujours actif après 8s');
  });

  test('getDancerCount() capé à MAX_DANCERS (10)', () => {
    const fm = new FlashMobAgent();
    const peds = Array.from({ length: 20 }, (_, i) => makePed(i * 0.5, 0));
    fm.update(50, peds, { x: 0, z: 0 });
    assert.ok(fm.getDancerCount() <= 10, `getDancerCount=${fm.getDancerCount()} > 10`);
  });
});
