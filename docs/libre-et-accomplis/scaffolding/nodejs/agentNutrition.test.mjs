/**
 * Libre & Accomplis — Tests de l'Agent Nutrition (Node.js).
 * Exécution : node --test docs/libre-et-accomplis/scaffolding/nodejs/*.test.mjs
 */
import test from 'node:test';
import assert from 'node:assert/strict';

import { BaseConnaissances } from './baseConnaissances.mjs';
import { AgentNutrition } from './agentNutrition.mjs';

function creerAgent() {
  const base = new BaseConnaissances();
  return { base, agent: new AgentNutrition(base) };
}

test('propose une recette sans allergène', () => {
  const { base, agent } = creerAgent();
  base.ajouterUtilisateur({ id: 123, allergies: ['noix'], objectifs: ['perte_de_poids'] });

  const recette = agent.proposerRecette(123);

  assert.equal(recette.success, true);
  assert.ok(!recette.ingredients.includes('noix'));
});

test('propose une recette protéinée pour la prise de muscle', () => {
  const { base, agent } = creerAgent();
  base.ajouterUtilisateur({ id: 456, allergies: [], objectifs: ['prise_de_muscle'] });

  const recette = agent.proposerRecette(456);

  assert.equal(recette.success, true);
  assert.ok(recette.tags.includes('proteines'));
});

test('refuse plutôt que de proposer une recette à risque', () => {
  const { base, agent } = creerAgent();
  base.ajouterUtilisateur({
    id: 789,
    allergies: ['quinoa', 'poulet', 'avoine', 'oeuf'],
    objectifs: [],
  });

  const reponse = agent.proposerRecette(789);

  assert.equal(reponse.success, false);
  assert.equal(reponse.raison, 'aucune_recette_compatible');
});

test('lève une erreur pour un utilisateur inconnu', () => {
  const { agent } = creerAgent();
  assert.throws(() => agent.proposerRecette(999), /inconnu/);
});
