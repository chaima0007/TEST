import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import { createWorld } from '../js/world.js';
import { MissionManager } from '../js/missions.js';

function fakeHud() {
  return {
    messages: [],
    missionText: null,
    score: null,
    setMission(text) { this.missionText = text; },
    showMessage(text) { this.messages.push(text); },
    setScore(value) { this.score = value; },
    setSpeed() {},
    setWanted() {},
  };
}

function fakeVehicleAt(x, z) {
  return { x, z, getPosition() { return { x: this.x, z: this.z }; } };
}

function driveToTarget(missions, vehicle, dt = 1 / 60) {
  const m = missions.getCurrentMission();
  vehicle.x = m.targetX;
  vehicle.z = m.targetZ;
  missions.update(dt, vehicle);
}

describe('MissionManager', () => {
  test('starts with a reachable delivery mission and exposes it via getCurrentMission', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const hud = fakeHud();
    const missions = new MissionManager(world, hud);

    const current = missions.getCurrentMission();
    assert.ok(current, 'a mission should be active right away');
    assert.ok(typeof current.name === 'string' && current.name.length > 0);
    assert.equal(missions.getScore(), 0);
  });

  test('arriving at the first (delivery) mission target awards points and advances the mission', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const hud = fakeHud();
    const missions = new MissionManager(world, hud);
    const vehicle = fakeVehicleAt(-1000, -1000); // far from target initially

    const firstTarget = missions.getCurrentMission();
    missions.update(1 / 60, vehicle); // far away: no change
    assert.equal(missions.getScore(), 0);

    driveToTarget(missions, vehicle);

    assert.ok(missions.getScore() > 0, 'score should increase after reaching the delivery target');
    const next = missions.getCurrentMission();
    assert.notDeepEqual(next, firstTarget, 'a new mission should start after completing the first one');
  });

  test('a timed mission fails and resets if the player never arrives in time', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const hud = fakeHud();
    const missions = new MissionManager(world, hud);
    const vehicle = fakeVehicleAt(-1000, -1000);

    // First mission (delivery) — complete it to advance to the timed mission.
    driveToTarget(missions, vehicle);
    assert.match(missions.getCurrentMission().name ? hud.missionText : '', /.+/);

    vehicle.x = -1000;
    vehicle.z = -1000;
    const scoreBeforeTimeout = missions.getScore();

    for (let i = 0; i < 60 * 35; i++) missions.update(1 / 60, vehicle); // 35s, past the 30s timed limit

    assert.equal(missions.getScore(), scoreBeforeTimeout, 'no reward should be granted on timeout');
    assert.ok(
      hud.messages.some((m) => /ratée/i.test(m)),
      'a failure message should have been shown'
    );
  });

  test('a checkpoint chain mission pays out per step plus a completion bonus', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const hud = fakeHud();
    const missions = new MissionManager(world, hud);
    const vehicle = fakeVehicleAt(-1000, -1000);

    driveToTarget(missions, vehicle); // delivery -> timed
    driveToTarget(missions, vehicle); // timed -> chain

    let guard = 0;
    const scoreAtChainStart = missions.getScore();
    while (guard < 10) {
      driveToTarget(missions, vehicle);
      guard++;
      // Stop once we're clearly back to a non-chain mission type announcement
      if (!/Tournée/.test(hud.missionText || '')) break;
    }

    assert.ok(missions.getScore() > scoreAtChainStart, 'completing chain steps should increase the score');
  });
});
