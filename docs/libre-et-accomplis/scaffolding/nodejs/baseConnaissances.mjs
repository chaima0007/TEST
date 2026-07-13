/**
 * Libre & Accomplis — Base de connaissances centralisée (scaffolding Node.js).
 *
 * Version en mémoire pour le développement et les tests locaux. En production,
 * remplacée par Neo4j (relations) + PostgreSQL (données) + Redis (cache),
 * avec la même interface publique.
 */

export const TAGS_PAR_OBJECTIF = {
  perte_de_poids: ['leger', 'faible_calories'],
  prise_de_muscle: ['proteines'],
  energie: ['glucides_complexes'],
};

const RECETTES_PAR_DEFAUT = [
  {
    id: 1,
    nom: 'Salade de quinoa aux légumes',
    ingredients: ['quinoa', 'tomate', 'concombre', 'citron'],
    tags: ['leger', 'faible_calories', 'vegan'],
  },
  {
    id: 2,
    nom: 'Poulet grillé et brocoli',
    ingredients: ['poulet', 'brocoli', 'huile_olive'],
    tags: ['proteines', 'leger'],
  },
  {
    id: 3,
    nom: 'Granola maison aux noix',
    ingredients: ['avoine', 'noix', 'miel'],
    tags: ['glucides_complexes', 'energie'],
  },
  {
    id: 4,
    nom: 'Omelette aux épinards',
    ingredients: ['oeuf', 'epinard', 'fromage'],
    tags: ['proteines'],
  },
];

export class BaseConnaissances {
  constructor() {
    this.utilisateurs = new Map();
    this.recettes = RECETTES_PAR_DEFAUT.map((r) => ({ ...r }));
    this.microObjectifs = new Map();
  }

  ajouterUtilisateur(utilisateur) {
    if (utilisateur.id === undefined) {
      throw new Error("Un utilisateur doit avoir un champ 'id'.");
    }
    // Pas de doublon : un id existant met à jour le profil.
    this.utilisateurs.set(utilisateur.id, { ...utilisateur });
  }

  getUtilisateur(userId) {
    const utilisateur = this.utilisateurs.get(userId);
    if (!utilisateur) {
      throw new Error(`Utilisateur ${userId} inconnu dans la base de connaissances.`);
    }
    return { ...utilisateur };
  }

  /** Remplace les micro-objectifs de l'utilisateur (pas de doublons). */
  setMicroObjectifs(userId, microObjectifs) {
    this.getUtilisateur(userId);
    this.microObjectifs.set(userId, microObjectifs.map((m) => ({ ...m })));
  }

  getMicroObjectifs(userId) {
    return (this.microObjectifs.get(userId) ?? []).map((m) => ({ ...m }));
  }

  validerMicroObjectif(userId, microId) {
    const liste = this.microObjectifs.get(userId) ?? [];
    const micro = liste.find((m) => m.id === microId);
    if (!micro) {
      throw new Error(`Micro-objectif ${microId} inconnu pour l'utilisateur ${userId}.`);
    }
    micro.fait = true;
  }

  ajouterRecette(recette) {
    this.recettes.push({ ...recette });
  }

  /** Exclut strictement les recettes contenant un allergène (règle de sécurité). */
  getRecettes({ allergies = [] } = {}) {
    const interdits = new Set(allergies);
    return this.recettes
      .filter((r) => !r.ingredients.some((i) => interdits.has(i)))
      .map((r) => ({ ...r }));
  }
}
