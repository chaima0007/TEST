// DriftSystem — awards combo points for sustained sideways slides.
// Detects drift by checking lateral velocity from Vehicle.getLateralSpeed().
// Points accumulate while sliding (angle × speed), banked on exit if above minimum.

const DRIFT_LAT_THRESHOLD = 2.8;  // m/s sideways to count as drifting
const DRIFT_MIN_FWD_KMH   = 30;   // must be moving forward
const DRIFT_MIN_SCORE     = 60;   // minimum to bank a drift run
const DRIFT_POINTS_FACTOR = 0.12; // angle_deg × fwdSpeed_ms × factor = pts/s

export class DriftSystem {
  constructor() {
    this._drifting   = false;
    this._driftTimer = 0;
    this._driftScore = 0;  // current (unbanked) drift session score
    this._totalScore = 0;  // banked score
    this._driftAngle = 0;  // degrees, for HUD display
    this._lastBanked = 0;  // score of last banked run (for fly-in)
  }

  getScore()       { return this._totalScore; }
  isDrifting()     { return this._drifting; }
  getDriftAngle()  { return this._driftAngle; }
  getSessionScore(){ return Math.round(this._driftScore); }
  getLastBanked()  { return this._lastBanked; }

  update(dt, vehicle) {
    if (!vehicle || typeof vehicle.getLateralSpeed !== 'function') return;

    const latSpd  = vehicle.getLateralSpeed();
    const fwdKmh  = Math.abs(vehicle.getSpeedKmh());
    const fwdMs   = fwdKmh / 3.6;
    const sliding = Math.abs(latSpd) > DRIFT_LAT_THRESHOLD && fwdKmh > DRIFT_MIN_FWD_KMH;

    if (sliding) {
      this._drifting   = true;
      this._driftTimer += dt;
      this._driftAngle  = Math.abs(Math.atan2(latSpd, fwdMs) * 180 / Math.PI);
      const ptsPerSec   = Math.min(250, this._driftAngle * fwdMs * DRIFT_POINTS_FACTOR);
      this._driftScore += ptsPerSec * dt;
      this._lastBanked  = 0;
    } else {
      if (this._drifting) {
        if (this._driftScore >= DRIFT_MIN_SCORE) {
          this._lastBanked  = Math.round(this._driftScore);
          this._totalScore += this._lastBanked;
        }
        this._driftScore = 0;
        this._driftTimer = 0;
        this._driftAngle = 0;
      }
      this._drifting = false;
    }
  }
}
