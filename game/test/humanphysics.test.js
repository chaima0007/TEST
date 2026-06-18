import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { HumanPhysicsAgent } from '../js/humanphysics.js';

// Helper : crée un mesh minimal avec userData.bones
function makeMesh() {
  const bone = () => ({ rotation: { x: 0, y: 0, z: 0 }, position: { x: 0, y: 1.65, z: 0 } });
  return {
    position: { x: 0, y: 0, z: 0 },
    rotation: { x: 0, y: 0, z: 0 },
    userData: {
      animPhase: 0,
      bones: {
        headGroup: { rotation: { x: 0, y: 0, z: 0 }, position: { x: 0, y: 1.65, z: 0 } },
        uArmL: bone(), uArmR: bone(),
        lArmL: bone(), lArmR: bone(),
        uLegL: bone(), uLegR: bone(),
        lLegL: bone(), lLegR: bone(),
        footL: bone(), footR: bone(),
      },
    },
  };
}

describe('HumanPhysicsAgent', () => {
  test('applique un lean avant positif quand la vitesse augmente', () => {
    const agent = new HumanPhysicsAgent();
    const mesh  = makeMesh();
    // Plusieurs frames à vitesse constante pour que le ressort se stabilise
    for (let i = 0; i < 60; i++) agent.update(mesh, 3.0, 0, 1/60, {});
    assert.ok(mesh.rotation.x > 0, `lean avant attendu, obtenu ${mesh.rotation.x}`);
  });

  test('lean revient à zéro quand vitesse = 0', () => {
    const agent = new HumanPhysicsAgent();
    const mesh  = makeMesh();
    for (let i = 0; i < 60; i++) agent.update(mesh, 3.0, 0, 1/60, {});
    for (let i = 0; i < 120; i++) agent.update(mesh, 0, 0, 1/60, {});
    assert.ok(Math.abs(mesh.rotation.x) < 0.02, `lean résiduel trop grand : ${mesh.rotation.x}`);
  });

  test('lean latéral en virage (angVel > 0)', () => {
    const agent = new HumanPhysicsAgent();
    const mesh  = makeMesh();
    for (let i = 0; i < 60; i++) agent.update(mesh, 1.5, 2.0, 1/60, {});
    // angVel positif → lean Z négatif (inclinaison dans le virage)
    assert.ok(mesh.rotation.z < 0, `lean latéral attendu négatif, obtenu ${mesh.rotation.z}`);
  });

  test('stumble démarre un timer et modifie rotation', () => {
    const agent = new HumanPhysicsAgent();
    const mesh  = makeMesh();
    agent.update(mesh, 0, 0, 1/60, { stumble: true });
    // Pendant le trébuchement : rotation x doit être différente du lean normal
    agent.update(mesh, 0, 0, 1/60, {});
    assert.equal(agent.isDown(mesh), true);
  });

  test('stumble se termine après ~0.55 s', () => {
    const agent = new HumanPhysicsAgent();
    const mesh  = makeMesh();
    agent.update(mesh, 0, 0, 1/60, { stumble: true });
    for (let i = 0; i < 40; i++) agent.update(mesh, 0, 0, 1/60, {});
    assert.equal(agent.isDown(mesh), false);
  });

  test('head tracking oriente le regard vers la cible', () => {
    const agent = new HumanPhysicsAgent();
    const mesh  = makeMesh();
    // Cible à droite (+X) → tête devrait pivoter vers +Y (headYaw > 0)
    const headTarget = { x: 10, z: 0 };
    for (let i = 0; i < 30; i++) agent.update(mesh, 0, 0, 1/60, { headTarget });
    const headYaw = mesh.userData.bones.headGroup.rotation.y;
    assert.ok(headYaw > 0.1, `headYaw attendu positif, obtenu ${headYaw}`);
  });

  test('tête revient à la position neutre sans cible', () => {
    const agent = new HumanPhysicsAgent();
    const mesh  = makeMesh();
    const headTarget = { x: 10, z: 0 };
    for (let i = 0; i < 30; i++) agent.update(mesh, 0, 0, 1/60, { headTarget });
    for (let i = 0; i < 60; i++) agent.update(mesh, 0, 0, 1/60, {});
    const headYaw = mesh.userData.bones.headGroup.rotation.y;
    assert.ok(Math.abs(headYaw) < 0.05, `headYaw résiduel trop grand : ${headYaw}`);
  });

  test('chute déplace mesh.position.y vers le bas puis le remet à 0', () => {
    const agent = new HumanPhysicsAgent();
    const mesh  = makeMesh();
    agent.update(mesh, 0, 0, 1/60, { fall: true });
    // Pendant la chute position Y doit descendre
    let minY = 0;
    for (let i = 0; i < 30; i++) {
      agent.update(mesh, 0, 0, 1/60, {});
      minY = Math.min(minY, mesh.position.y);
    }
    assert.ok(minY < -0.1, `position Y en chute attendue négative, obtenu ${minY}`);
    // Après relèvement complet (≈1.9s) position Y revient à 0
    for (let i = 0; i < 90; i++) agent.update(mesh, 0, 0, 1/60, {});
    assert.ok(mesh.position.y === 0, `position Y finale non réinitialisée : ${mesh.position.y}`);
  });
});
