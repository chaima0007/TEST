import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { EmotionEngine } from '../js/emotion.js';

describe('EmotionEngine', () => {
  test('démarre en humeur neutre avec valeurs à 0', () => {
    const ee = new EmotionEngine();
    assert.equal(ee.getMood(), 'neutral');
    assert.equal(ee.getAggression(), 0);
    assert.equal(ee.getSerenity(), 0);
    assert.equal(ee.getEntropy(), 0);
  });

  test('crash augmente l\'agressivité', () => {
    const ee = new EmotionEngine();
    ee.pushEvent('crash', 1);
    assert.ok(ee.getAggression() > 0, 'agressivité devrait augmenter après crash');
  });

  test('peaceful augmente la sérénité', () => {
    const ee = new EmotionEngine();
    ee.pushEvent('peaceful', 1);
    assert.ok(ee.getSerenity() > 0, 'sérénité devrait augmenter');
  });

  test('drift et nitro augmentent l\'entropie', () => {
    const ee = new EmotionEngine();
    ee.pushEvent('drift', 1);
    ee.pushEvent('nitro', 1);
    assert.ok(ee.getEntropy() > 0, 'entropie devrait augmenter');
  });

  test('mood devient tense quand agressivité ≥ 25 et > sérénité', () => {
    const ee = new EmotionEngine();
    // 3 crashs : 3 × 14 = 42 > seuil TENSE(25) mais < CHAOTIC(55)
    ee.pushEvent('crash', 2);  // +28
    ee.update(0);              // recalcul sans décroissance
    assert.equal(ee.getMood(), 'tense', `humeur=${ee.getMood()}`);
  });

  test('mood devient chaotic quand agressivité ≥ 55', () => {
    const ee = new EmotionEngine();
    ee.pushEvent('crash', 4); // 4 × 14 = 56 ≥ 55
    ee.update(0);
    assert.equal(ee.getMood(), 'chaotic', `humeur=${ee.getMood()}`);
  });

  test('mood devient serene quand sérénité ≥ 30 et domine', () => {
    const ee = new EmotionEngine();
    ee.pushEvent('peaceful', 8); // 8 × 4 = 32 ≥ 30
    ee.update(0);
    assert.equal(ee.getMood(), 'serene', `humeur=${ee.getMood()}`);
  });

  test('getScoreMult() : chaotic=1.5, serene=1.3, tense=1.1, neutral=1.0', () => {
    const make = (mood) => {
      const ee = new EmotionEngine();
      if (mood === 'chaotic')  ee.pushEvent('crash', 4);
      if (mood === 'serene')   ee.pushEvent('peaceful', 8);
      if (mood === 'tense')    ee.pushEvent('crash', 2);
      ee.update(0);
      return ee;
    };
    assert.equal(make('chaotic').getScoreMult(), 1.5);
    assert.equal(make('serene').getScoreMult(), 1.3);
    assert.equal(make('tense').getScoreMult(), 1.1);
    assert.equal(new EmotionEngine().getScoreMult(), 1.0);
  });
});
