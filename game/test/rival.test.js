import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import { createWorld } from '../js/world.js';
import { RivalSystem } from '../js/rival.js';

function fakeVehicleAt(x, z) {
  return {
    getPosition: () => ({ x, z }),
  };
}

function fakeHud() {
  const messages = [];
  return { showMessage: (text) => messages.push(text), messages };
}

describe('RivalSystem ("Le Spectre")', () => {
  test('stays inactive until its spawn cooldown elapses, then appears and announces itself', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const rival = new RivalSystem(scene, world);
    const vehicle = fakeVehicleAt(0, 0);
    const hud = fakeHud();

    assert.equal(rival.active, false);

    // Up to 71s, covers the max cooldown. Checking the HUD announcement
    // (rather than rival.active at the end of the loop) avoids flakiness:
    // Le Spectre could spawn AND already be caught/escaped again well
    // within this window, which would flip `active` back to false even
    // though the spawn we're testing for did happen.
    for (let i = 0; i < 71 * 60; i++) rival.update(1 / 60, vehicle, hud);

    assert.ok(hud.messages.some((m) => m.includes('LE SPECTRE')), 'expected a spawn announcement on the HUD');
  });

  test('awards a score bonus and despawns once the player survives the challenge out of catch range', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const rival = new RivalSystem(scene, world);
    const hud = fakeHud();

    // Force an immediate, deterministic spawn instead of waiting on the
    // random cooldown, then keep the player far away so Le Spectre can
    // chase but never actually catch up before the challenge times out.
    rival._spawn({ x: 0, z: 0 }, hud);
    assert.equal(rival.active, true);
    const farVehicle = fakeVehicleAt(100000, 100000);

    for (let i = 0; i < 23 * 60; i++) rival.update(1 / 60, farVehicle, hud); // 23s > CHALLENGE_DURATION_S

    assert.equal(rival.active, false, 'Le Spectre should have despawned after the challenge ended');
    assert.ok(rival.getScore() > 0, 'escaping should award a score bonus');
    assert.ok(hud.messages.some((m) => m.includes('semé')), 'expected an escape message on the HUD');
  });

  test('catches the player who stays within range and despawns without awarding a bonus', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const rival = new RivalSystem(scene, world);
    const hud = fakeHud();

    rival._spawn({ x: 0, z: 0 }, hud);
    // The player parks right on top of Le Spectre's spawn point, so the
    // catch radius is satisfied immediately and stays satisfied.
    const spawnPos = { x: rival.mesh.position.x, z: rival.mesh.position.z };
    const stillVehicle = fakeVehicleAt(spawnPos.x, spawnPos.z);

    for (let i = 0; i < 5 * 60; i++) rival.update(1 / 60, stillVehicle, hud); // well past CATCH_HOLD_S

    assert.equal(rival.active, false, 'Le Spectre should have despawned after catching the player');
    assert.equal(rival.getScore(), 0, 'getting caught should not award a bonus');
    assert.ok(hud.messages.some((m) => m.includes('rattrapé')), 'expected a catch message on the HUD');
  });
});
