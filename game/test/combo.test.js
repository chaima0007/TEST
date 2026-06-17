import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { ComboSystem } from '../js/combo.js';

describe('ComboSystem', () => {
  test('starts at multiplier 1 and score 0', () => {
    const combo = new ComboSystem();
    assert.equal(combo.getMultiplier(), 1);
    assert.equal(combo.getScore(), 0);
  });

  test('triggers a near-miss bonus when a traffic car is within the near-miss zone', () => {
    const combo = new ComboSystem();
    const player = { x: 0, z: 0 };
    const traffic = [{ x: 5, z: 0 }]; // 5m away — inside the 2.8m–7m zone

    combo.update(1 / 60, player, traffic);

    assert.ok(combo.getScore() > 0, 'near-miss should award bonus points');
    assert.equal(combo.getMultiplier(), 2, 'first near-miss should raise mult to 2x');
  });

  test('does not trigger when the vehicle is too close (real collision)', () => {
    const combo = new ComboSystem();
    const player = { x: 0, z: 0 };
    const traffic = [{ x: 1.5, z: 0 }]; // 1.5m — inside collision zone, not near-miss

    combo.update(1 / 60, player, traffic);

    assert.equal(combo.getScore(), 0, 'a collision-distance contact should not reward near-miss bonus');
    assert.equal(combo.getMultiplier(), 1);
  });

  test('does not double-count one continuous near-miss pass', () => {
    const combo = new ComboSystem();
    const player = { x: 0, z: 0 };
    const traffic = [{ x: 5, z: 0 }];

    for (let i = 0; i < 10; i++) combo.update(1 / 60, player, traffic);

    assert.equal(combo.getMultiplier(), 2, 'staying inside the zone should only count once');
  });

  test('caps multiplier at 5x after many consecutive near-misses', () => {
    const combo = new ComboSystem();
    const traffic1 = [{ x: 5, z: 0 }];
    const trafficFar = [{ x: 100, z: 0 }];
    const player = { x: 0, z: 0 };

    for (let round = 0; round < 10; round++) {
      combo.update(1 / 60, player, traffic1); // enter zone
      combo.update(1 / 60, player, trafficFar); // exit zone so next entry counts
    }

    assert.equal(combo.getMultiplier(), 5, 'multiplier should be capped at 5x');
  });

  test('decays back to 1x after the grace period without any near-miss', () => {
    const combo = new ComboSystem();
    const player = { x: 0, z: 0 };
    combo.update(1 / 60, player, [{ x: 5, z: 0 }]); // trigger a near-miss
    combo.update(1 / 60, player, [{ x: 100, z: 0 }]); // exit zone
    assert.equal(combo.getMultiplier(), 2);

    // Simulate grace period + decay step + small safety margin for float accumulation
    for (let i = 0; i < Math.ceil((3.5 + 1.8) * 60) + 10; i++) {
      combo.update(1 / 60, player, [{ x: 100, z: 0 }]);
    }

    assert.equal(combo.getMultiplier(), 1, 'multiplier should have decayed back to 1x');
  });
});
