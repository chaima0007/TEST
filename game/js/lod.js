// LODManager — Data-Oriented update throttling for all game entities.
// Entities are bucketed by distance from player; distant ones update less often.
// No heap allocations per frame: all math is integer arithmetic on a frame counter.
//
// Tiers:
//   FULL  (dist < 50m)  — every frame          → player interaction zone
//   MID   (dist < 120m) — every 3rd frame       → visible, not interacting
//   LOW   (dist ≥ 120m) — every 8th frame       → background / despawn boundary
//
// Stagger: pass the entity's index so same-tier entities don't all update on
// the same frame, spreading CPU cost evenly across the burst.

const NEAR = 50;
const MID  = 120;

export class LODManager {
  constructor() {
    this._frame = 0;
  }

  // Call once per game loop iteration, before updating any entities.
  tick() {
    this._frame = (this._frame + 1) & 0x7fff; // wraps at 32 767, never overflows
  }

  // Returns true if this entity should run its full update this frame.
  // dist   — world-space distance from player in metres
  // stagger — integer unique to this entity (use its pool index) to avoid
  //           all MID/LOW entities firing on the same frame
  shouldUpdate(dist, stagger = 0) {
    if (dist < NEAR) return true;
    if (dist < MID)  return ((this._frame + stagger) % 3) === 0;
    return             ((this._frame + stagger) % 8) === 0;
  }

  getTier(dist) {
    if (dist < NEAR) return 'FULL';
    if (dist < MID)  return 'MID';
    return 'LOW';
  }

  getFrame() { return this._frame; }
}
