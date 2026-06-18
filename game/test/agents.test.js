import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { PathClearanceAgent, IntegrityAgent } from '../js/traffic.js';

// Helper : crée une fausse entité active avec mesh positionné
function makeEntity(x, z, speed = 5) {
  return {
    active: true,
    speed,
    mesh: { position: { x, z } },
  };
}

describe('PathClearanceAgent', () => {
  test('retourne clear:true quand aucune entité devant', () => {
    const agent = new PathClearanceAgent();
    const self = makeEntity(0, 0);
    agent.register([self], []);
    const result = agent.check(0, 0, 0, 20, self);
    assert.equal(result.clear, true);
    assert.equal(result.type, null);
  });

  test('détecte une voiture à 8 m directement devant (heading=0, +Z)', () => {
    const agent = new PathClearanceAgent();
    const self    = makeEntity(0, 0);
    const blocker = makeEntity(0, 8);  // 8 m en avant sur Z
    agent.register([self, blocker], []);
    const result = agent.check(0, 0, 0, 20, self, 2.0);
    assert.equal(result.clear, false);
    assert.equal(result.type, 'car');
    assert.ok(result.distance > 7 && result.distance < 9);
  });

  test('ignore une voiture derrière (fwd < 0.5)', () => {
    const agent = new PathClearanceAgent();
    const self    = makeEntity(0, 0);
    const behind  = makeEntity(0, -10);  // 10 m derrière
    agent.register([self, behind], []);
    const result = agent.check(0, 0, 0, 20, self);
    assert.equal(result.clear, true);
  });

  test('ignore une voiture sur le côté (hors couloir)', () => {
    const agent = new PathClearanceAgent();
    const self   = makeEntity(0, 0);
    const side   = makeEntity(8, 5);  // loin sur le côté
    agent.register([self, side], []);
    const result = agent.check(0, 0, 0, 20, self, 2.0);
    assert.equal(result.clear, true);
  });

  test('détecte un piéton devant (heading=π/2, +X)', () => {
    const agent = new PathClearanceAgent();
    const self  = makeEntity(0, 0);
    const ped   = makeEntity(5, 0);  // 5 m à droite = devant si heading=π/2
    agent.register([self], [ped]);
    const result = agent.check(0, 0, Math.PI / 2, 10, self, 2.0);
    assert.equal(result.clear, false);
    assert.equal(result.type, 'ped');
  });

  test('exclut self du test', () => {
    const agent = new PathClearanceAgent();
    const self = makeEntity(0, 0);
    agent.register([self], []);
    const result = agent.check(0, 0, 0, 20, self);
    assert.equal(result.clear, true);
  });
});

describe('IntegrityAgent', () => {
  test('marque hors-limites pour respawn', () => {
    const agent = new IntegrityAgent();
    const car = makeEntity(200, 0);  // bien hors de CITY_HALF_SIZE=100
    car.speed = 0;
    const result = agent.repair([car], [], []);
    assert.equal(car.active, false);
    assert.ok(result >= 1);
  });

  test('éjecte une voiture coincée dans un collider', () => {
    const agent = new IntegrityAgent();
    const car = makeEntity(10, 10);
    car.speed = 5;
    const colliders = [{ x: 10, z: 10, halfWidth: 5, halfDepth: 5 }];
    agent.repair([car], [], colliders);
    // La position doit avoir bougé
    assert.ok(car.mesh.position.x !== 10 || car.mesh.position.z !== 10);
  });

  test('marque pour respawn après 120 frames de blocage', () => {
    const agent = new IntegrityAgent();
    const car = makeEntity(0, 0);
    car.speed = 0;
    const colliders = [];
    for (let i = 0; i < 120; i++) {
      agent.repair([car], [], colliders);
      if (!car.active) break;
    }
    assert.equal(car.active, false);
  });

  test('remet le compteur bloqué à zéro quand la voiture repart', () => {
    const agent = new IntegrityAgent();
    const car = makeEntity(0, 0);
    car.speed = 0;
    for (let i = 0; i < 50; i++) agent.repair([car], [], []);
    // Voiture repart
    car.speed = 8;
    agent.repair([car], [], []);
    // 70 frames supplémentaires : ne doit PAS déclencher respawn
    car.speed = 0;
    for (let i = 0; i < 70; i++) agent.repair([car], [], []);
    assert.equal(car.active, true); // compteur remis à zéro → pas encore 120
  });

  test('piétons hors-limites sont marqués pour respawn', () => {
    const agent = new IntegrityAgent();
    const ped = makeEntity(150, 0);
    agent.repair([], [ped], []);
    assert.equal(ped.active, false);
  });

  test('ne répare pas les entités déjà inactives', () => {
    const agent = new IntegrityAgent();
    const car = makeEntity(200, 0);
    car.active = false;
    const fixes = agent.repair([car], [], []);
    assert.equal(fixes, 0);
  });
});
