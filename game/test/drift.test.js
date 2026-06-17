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

  // --- Grip coherence (validates physics stays consistent across weather states) ---

  it('drift score scales with forward speed — faster = more points per second', () => {
    // Both vehicles drift equally hard laterally; only fwd speed differs.
    // Score formula: angle_deg × fwdSpeed_ms × factor — so higher speed MUST yield more pts.
    const dsLow  = new DriftSystem();
    const dsHigh = new DriftSystem();
    const DT = 1 / 60;
    const FRAMES = 60; // 1 second of drift

    for (let i = 0; i < FRAMES; i++) {
      dsLow.update(DT,  makeVehicle(5.0, 50));   // 50 km/h forward
      dsHigh.update(DT, makeVehicle(5.0, 120));  // 120 km/h forward
    }

    assert.ok(
      dsHigh.getSessionScore() > dsLow.getSessionScore(),
      `score at 120km/h (${dsHigh.getSessionScore()}) should exceed score at 50km/h (${dsLow.getSessionScore()})`
    );
  });

  it('session score resets to 0 after banking', () => {
    const ds = new DriftSystem();
    for (let i = 0; i < 120; i++) ds.update(1 / 60, makeVehicle(5.0, 80));
    ds.update(1 / 60, makeVehicle(0, 80)); // end drift
    assert.equal(ds.getSessionScore(), 0, 'session score must reset after banking');
  });

  it('does not bank score below minimum threshold (prevents grind spam)', () => {
    const ds = new DriftSystem();
    // Very short drift — only 10 frames (≈ 0.17s) — score unlikely to reach DRIFT_MIN_SCORE=60
    for (let i = 0; i < 10; i++) ds.update(1 / 60, makeVehicle(5.0, 80));
    ds.update(1 / 60, makeVehicle(0, 80));
    assert.equal(ds.getScore(), 0, 'sub-threshold drift should not bank any score');
  });

  it('drift detection is lateral-speed-independent of grip factor — grip is a vehicle concern', () => {
    // DriftSystem only reads lateral speed; grip is applied upstream in vehicle.js.
    // A drift with high lateral speed should always be detected regardless of
    // what grip factor the vehicle had when generating that lateral speed.
    const ds = new DriftSystem();
    // Simulate the result of drifting with low grip: same lateral speed, same fwd speed.
    // DriftSystem must fire identically.
    ds.update(0.016, makeVehicle(5.0, 80));
    assert.equal(ds.isDrifting(), true, 'DriftSystem must detect based on lateral speed alone');
  });
});
