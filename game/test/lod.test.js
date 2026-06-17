import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { LODManager } from '../js/lod.js';

describe('LODManager', () => {
  it('always updates entities within 50m (FULL tier)', () => {
    const lod = new LODManager();
    for (let frame = 0; frame < 20; frame++) {
      lod.tick();
      assert.equal(lod.shouldUpdate(0,    0), true, `frame ${frame} dist=0`);
      assert.equal(lod.shouldUpdate(25,   0), true, `frame ${frame} dist=25`);
      assert.equal(lod.shouldUpdate(49.9, 0), true, `frame ${frame} dist=49.9`);
    }
  });

  it('updates MID-tier entities (50-120m) every 3rd frame', () => {
    const lod = new LODManager();
    let trueCount = 0;
    for (let i = 0; i < 9; i++) {
      lod.tick();
      if (lod.shouldUpdate(80, 0)) trueCount++;
    }
    // In 9 frames with stagger=0: frames where frame%3===0 → 3 times
    assert.equal(trueCount, 3, `expected 3 updates in 9 frames, got ${trueCount}`);
  });

  it('updates LOW-tier entities (≥120m) every 8th frame', () => {
    const lod = new LODManager();
    let trueCount = 0;
    for (let i = 0; i < 16; i++) {
      lod.tick();
      if (lod.shouldUpdate(150, 0)) trueCount++;
    }
    // In 16 frames: frame%8===0 at frame 8 and 16 → 2 times
    assert.equal(trueCount, 2, `expected 2 updates in 16 frames, got ${trueCount}`);
  });

  it('stagger spreads same-tier updates across frames (no same-frame spike)', () => {
    const lod = new LODManager();
    lod.tick(); // frame = 1
    // With stagger 0,1,2 and frame=1: only stagger=2 fires (1+2=3, %3=0)
    const a = lod.shouldUpdate(80, 0);
    const b = lod.shouldUpdate(80, 1);
    const c = lod.shouldUpdate(80, 2);
    const total = [a, b, c].filter(Boolean).length;
    assert.equal(total, 1, 'exactly one entity should update per stagger group per cycle');
  });

  it('getTier returns correct bucket string', () => {
    const lod = new LODManager();
    assert.equal(lod.getTier(0),   'FULL');
    assert.equal(lod.getTier(49),  'FULL');
    assert.equal(lod.getTier(50),  'MID');
    assert.equal(lod.getTier(119), 'MID');
    assert.equal(lod.getTier(120), 'LOW');
    assert.equal(lod.getTier(999), 'LOW');
  });
});
