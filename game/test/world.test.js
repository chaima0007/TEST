import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import { createWorld } from '../js/world.js';

function pointInsideAnyCollider(x, z, colliders, margin = 0) {
  return colliders.some((c) => {
    return (
      x > c.x - c.halfWidth - margin &&
      x < c.x + c.halfWidth + margin &&
      z > c.z - c.halfDepth - margin &&
      z < c.z + c.halfDepth + margin
    );
  });
}

describe('createWorld', () => {
  test('spawn point is not inside any building collider (regression: spawn used to be wedged in a block)', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    const { spawnPoint, colliders } = world;
    assert.equal(
      pointInsideAnyCollider(spawnPoint.x, spawnPoint.z, colliders, 1.5),
      false,
      `spawn point (${spawnPoint.x}, ${spawnPoint.z}) overlaps a building collider`
    );
  });

  test('mission locations are not inside any building collider', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    for (const loc of world.missionLocations) {
      assert.equal(
        pointInsideAnyCollider(loc.x, loc.z, world.colliders, 1),
        false,
        `mission location "${loc.name}" (${loc.x}, ${loc.z}) overlaps a building collider`
      );
    }
  });

  test('exposes roadLines additively alongside colliders/spawnPoint/missionLocations', () => {
    const scene = new THREE.Scene();
    const world = createWorld(scene);
    assert.ok(Array.isArray(world.colliders) && world.colliders.length > 0);
    assert.ok(Array.isArray(world.missionLocations) && world.missionLocations.length > 0);
    assert.ok(typeof world.spawnPoint.x === 'number');
    assert.ok(Array.isArray(world.roadLines.xs) && world.roadLines.xs.length > 0);
    assert.ok(Array.isArray(world.roadLines.zs) && world.roadLines.zs.length > 0);
  });
});
