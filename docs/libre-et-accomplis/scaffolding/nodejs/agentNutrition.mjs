/**
 * Libre & Accomplis — Agent Nutrition (scaffolding Node.js).
 *
 * Règles de sécurité validées par l'Expert en Santé :
 *   - Jamais de recette contenant un allergène de l'utilisateur.
 *   - En l'absence de recette compatible, répondre success=false plutôt
 *     que de proposer une recette à risque.
 */
import { TAGS_PAR_OBJECTIF } from './baseConnaissances.mjs';

export class AgentNutrition {
  constructor(base) {
    this.base = base;
  }

  proposerRecette(userId) {
    const utilisateur = this.base.getUtilisateur(userId);
    const recettes = this.base.getRecettes({ allergies: utilisateur.allergies ?? [] });
    const recette = this.#selectionnerMeilleureRecette(recettes, utilisateur.objectifs ?? []);

    if (!recette) {
      return { success: false, raison: 'aucune_recette_compatible' };
    }
    return {
      id: recette.id,
      nom: recette.nom,
      ingredients: recette.ingredients,
      tags: recette.tags,
      success: true,
    };
  }

  #selectionnerMeilleureRecette(recettes, objectifs) {
    if (recettes.length === 0) return null;

    const tagsRecherches = new Set(objectifs.flatMap((o) => TAGS_PAR_OBJECTIF[o] ?? []));
    const score = (r) => r.tags.filter((t) => tagsRecherches.has(t)).length;
    return recettes.reduce((best, r) => (score(r) > score(best) ? r : best));
  }
}
