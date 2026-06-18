import { test, describe } from 'node:test';
import assert from 'node:assert/strict';
import { DialogueAgent, LINES } from '../js/dialogue.js';

// Helper : crée un piéton minimal avec personnalité
function makePed(personalityName = 'TOURISTE') {
  return {
    active: true,
    mesh: { position: { x: 0, y: 0, z: 0 } },
    personality: { name: personalityName },
  };
}

describe('DialogueAgent', () => {
  test('trigger() retourne une réplique non nulle', () => {
    const agent = new DialogueAgent();
    const ped   = makePed('TOURISTE');
    const text  = agent.trigger(ped, 'drole');
    assert.ok(typeof text === 'string' && text.length > 0);
  });

  test('TOURISTE → réplique drôle', () => {
    const agent = new DialogueAgent();
    const ped   = makePed('TOURISTE');
    const text  = agent.trigger(ped); // mood déduit de la personnalité
    assert.ok(LINES.drole.includes(text), `Réplique inattendue : ${text}`);
  });

  test('NERVEUX → réplique triste', () => {
    const agent = new DialogueAgent();
    const ped   = makePed('NERVEUX');
    const text  = agent.trigger(ped);
    assert.ok(LINES.triste.includes(text), `Réplique inattendue : ${text}`);
  });

  test('PRESSÉ → réplique sérieuse', () => {
    const agent = new DialogueAgent();
    const ped   = makePed('PRESSÉ');
    const text  = agent.trigger(ped);
    assert.ok(LINES.serieux.includes(text), `Réplique inattendue : ${text}`);
  });

  test('context "crash" → réplique contextuelle', () => {
    const agent = new DialogueAgent();
    const ped   = makePed('COSTAUD');
    const text  = agent.trigger(ped, null, 'crash');
    assert.ok(LINES.crash.includes(text), `Réplique crash inattendue : ${text}`);
  });

  test('context "police" → réplique contextuelle', () => {
    const agent = new DialogueAgent();
    const ped   = makePed();
    const text  = agent.trigger(ped, null, 'police');
    assert.ok(LINES.police.includes(text));
  });

  test('context "boss" → réplique boss', () => {
    const agent = new DialogueAgent();
    const ped   = makePed();
    const text  = agent.trigger(ped, null, 'boss');
    assert.ok(LINES.boss.includes(text));
  });

  test('trigger() ignore un piéton qui parle déjà', () => {
    const agent = new DialogueAgent();
    const ped   = makePed();
    const first  = agent.trigger(ped, 'drole');
    const second = agent.trigger(ped, 'serieux');
    assert.equal(second, null, 'Double déclenchement autorisé à tort');
    assert.equal(agent.getActiveCount(), 1);
  });

  test('getActiveCount() reflète le nombre de bulles actives', () => {
    const agent = new DialogueAgent();
    const ped1 = makePed();
    const ped2 = makePed('PRESSÉ');
    agent.trigger(ped1, 'drole');
    agent.trigger(ped2, 'serieux');
    assert.equal(agent.getActiveCount(), 2);
  });

  test('la bulle expire après sa durée de vie', () => {
    const agent = new DialogueAgent();
    const ped   = makePed();
    agent.trigger(ped, 'drole');
    // Simule update sans camera/renderer (mode test headless)
    for (let i = 0; i < 300; i++) {
      agent.update(1/60, [ped], null, null, null, {});
    }
    assert.equal(agent.getActiveCount(), 0, 'Bulle toujours active après expiration');
  });

  test('getActiveEntries() retourne texte et humeur', () => {
    const agent = new DialogueAgent();
    const ped   = makePed('JOGGEUR');
    agent.trigger(ped, 'drole');
    const entries = agent.getActiveEntries();
    assert.equal(entries.length, 1);
    assert.equal(entries[0].mood, 'drole');
    assert.ok(typeof entries[0].text === 'string');
    assert.ok(entries[0].timer > 0);
  });

  test('lignes drôle, sérieux, triste sont toutes non vides', () => {
    for (const key of ['drole', 'serieux', 'triste', 'police', 'crash', 'pluie', 'nuit', 'boss']) {
      assert.ok(LINES[key].length >= 4, `Pool ${key} trop court (${LINES[key].length})`);
    }
  });
});
