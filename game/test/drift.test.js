import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { DriftSystem } from '../js/drift.js';

function makeVehicle(latSpd, speedKmh) {
  return { getLateralSpeed: () => latSpd, getSpeedKmh: () => speedKmh };
}

describe('DriftSystem', () => {
  it('starts with score 0 and not drifting', () => {
    const ds = new DriftSystem();
    assert.equal(ds.getScore(), 0);
    assert.equal(ds.isDrifting(), false);
  });

  it('detects drift when lateral speed exceeds threshold at speed', () => {
    const ds = new DriftSystem();
    ds.update(0.016, makeVehicle(5.0, 80));
    assert.equal(ds.isDrifting(), true);
  });

  it('does not detect drift below speed threshold', () => {
    const ds = new DriftSystem();
    ds.update(0.016, makeVehicle(5.0, 20));
    assert.equal(ds.isDrifting(), false);
  });

  it('does not detect drift below lateral threshold', () => {
    const ds = new DriftSystem();
    ds.update(0.016, makeVehicle(1.0, 80));
    assert.equal(ds.isDrifting(), false);
  });

  it('banks score after drift ends if above minimum', () => {
    const ds = new DriftSystem();
    const driftVehicle = makeVehicle(5.0, 80);
    // Simulate 120 frames of drifting at 60fps (2 seconds, enough to exceed DRIFT_MIN_SCORE=60)
    for (let i = 0; i < 120; i++) {
      ds.update(1 / 60, driftVehicle);
    }
    assert.equal(ds.isDrifting(), true);
    assert.ok(ds.getSessionScore() > 0, 'session score should be positive during drift');
    // End the drift with one frame of no-drift
    ds.update(1 / 60, makeVehicle(0, 80));
    assert.equal(ds.isDrifting(), false);
    assert.ok(ds.getScore() >= 60, `banked score ${ds.getScore()} should be >= DRIFT_MIN_SCORE (60)`);
    assert.ok(ds.getLastBanked() > 0, 'lastBanked should be set after banking');
  });
});
