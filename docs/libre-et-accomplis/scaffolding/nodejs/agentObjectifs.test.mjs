/**
 * Libre & Accomplis — Tests de l'Agent Objectifs (Node.js).
 * Exécution : node --test docs/libre-et-accomplis/scaffolding/nodejs/*.test.mjs
 */
import test from 'node:test';
import assert from 'node:assert/strict';

import { BaseConnaissances } from './baseConnaissances.mjs';
import { AgentObjectifs } from './agentObjectifs.mjs';

function creerAgent(objectifs = ['perte_de_poids']) {
  const base = new BaseConnaissances();
  base.ajouterUtilisateur({ id: 1, objectifs });
  return { base, agent: new AgentObjectifs(base) };
}

test('décompose un objectif en micro-objectifs hebdomadaires', () => {
  const { agent } = creerAgent();

  const resultat = agent.decomposerObjectifs(1);

  assert.equal(resultat.success, true);
  assert.equal(resultat.microObjectifs.length, 3);
  assert.ok(resultat.microObjectifs.every((m) => m.fait === false && m.semaine === 1));
});

test('refuse un objectif hors catalogue plutôt que d’inventer un plan', () => {
  const { agent } = creerAgent(['devenir_astronaute']);

  const resultat = agent.decomposerObjectifs(1);

  assert.equal(resultat.success, false);
  assert.equal(resultat.raison, 'objectif_inconnu');
  assert.deepEqual(resultat.objectifs, ['devenir_astronaute']);
});

test('refuse quand aucun objectif n’est défini', () => {
  const { agent } = creerAgent([]);

  const resultat = agent.decomposerObjectifs(1);

  assert.equal(resultat.success, false);
  assert.equal(resultat.raison, 'aucun_objectif_defini');
});

test('suit la progression après validation de micro-objectifs', () => {
  const { agent } = creerAgent(['perte_de_poids', 'energie']);
  agent.decomposerObjectifs(1);

  agent.validerMicroObjectif(1, 1);
  const progression = agent.validerMicroObjectif(1, 2);

  assert.equal(progression.success, true);
  assert.equal(progression.total, 6);
  assert.equal(progression.faits, 2);
  assert.equal(progression.pourcentage, 33);
});

test('progression sans micro-objectifs -> success=false', () => {
  const { agent } = creerAgent();

  const progression = agent.progression(1);

  assert.equal(progression.success, false);
  assert.equal(progression.raison, 'aucun_micro_objectif');
});

test('valider un micro-objectif inconnu lève une erreur', () => {
  const { agent } = creerAgent();
  agent.decomposerObjectifs(1);

  assert.throws(() => agent.validerMicroObjectif(1, 42), /inconnu/);
});
