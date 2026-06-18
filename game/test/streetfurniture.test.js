import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { StreetFurnitureSystem } from '../js/streetfurniture.js';

const ROAD_XS = [-95, -57, -19, 19, 57, 95];
const ROAD_ZS = [-95, -57, -19, 19, 57, 95];

function makeScene() { return { add: () => {} }; }

describe('StreetFurnitureSystem', () => {
  test('construit au moins 40 éléments au total', () => {
    const sfs = new StreetFurnitureSystem(makeScene(), ROAD_XS, ROAD_ZS, []);
    assert.ok(sfs.getTotalCount() >= 40, `getTotalCount() = ${sfs.getTotalCount()}`);
  });

  test('comprend des bollards', () => {
    const sfs = new StreetFurnitureSystem(makeScene(), ROAD_XS, ROAD_ZS, []);
    assert.ok(sfs.getBollardCount() > 0, `getBollardCount() = ${sfs.getBollardCount()}`);
  });

  test('comprend des bancs', () => {
    const sfs = new StreetFurnitureSystem(makeScene(), ROAD_XS, ROAD_ZS, []);
    assert.ok(sfs.getBenchCount() > 0, `getBenchCount() = ${sfs.getBenchCount()}`);
  });

  test('les bollards ajoutent des colliders dans le tableau fourni', () => {
    const colliders = [];
    new StreetFurnitureSystem(makeScene(), ROAD_XS, ROAD_ZS, colliders);
    assert.ok(colliders.length > 0, 'Aucun collider bollard inséré');
  });

  test('tous les colliders bollards ont halfWidth et halfDepth positifs', () => {
    const colliders = [];
    new StreetFurnitureSystem(makeScene(), ROAD_XS, ROAD_ZS, colliders);
    assert.ok(
      colliders.every(c => c.halfWidth > 0 && c.halfDepth > 0),
      'Collider avec halfWidth/halfDepth invalide',
    );
  });
});
