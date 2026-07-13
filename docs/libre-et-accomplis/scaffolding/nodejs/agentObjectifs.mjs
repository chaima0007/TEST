/**
 * Libre & Accomplis — Agent Objectifs (scaffolding Node.js).
 *
 * Décompose les objectifs de l'utilisateur en micro-objectifs hebdomadaires
 * et suit la progression. Règles validées par l'Expert en Comportement
 * (approche *Atomic Habits* : petits pas mesurables, une semaine à la fois) :
 *   - Un objectif inconnu du catalogue produit success=false, jamais un
 *     plan inventé.
 *   - La progression n'est jamais négative ni supérieure à 100 %.
 */

const CATALOGUE_MICRO_OBJECTIFS = {
  perte_de_poids: [
    'Marcher 30 minutes par jour',
    'Préparer 3 repas équilibrés cette semaine',
    'Boire 1,5 L d’eau par jour',
  ],
  prise_de_muscle: [
    'Faire 2 séances de renforcement cette semaine',
    'Atteindre son quota de protéines 5 jours sur 7',
    'Dormir au moins 7 h par nuit',
  ],
  energie: [
    'Se coucher avant 23 h 4 soirs cette semaine',
    'Faire une pause de 5 min toutes les 2 h de travail',
    'Prendre un petit-déjeuner complet chaque matin',
  ],
};

export class AgentObjectifs {
  constructor(base) {
    this.base = base;
  }

  /** Décompose les objectifs de l'utilisateur en micro-objectifs hebdomadaires. */
  decomposerObjectifs(userId) {
    const utilisateur = this.base.getUtilisateur(userId);
    const objectifs = utilisateur.objectifs ?? [];
    if (objectifs.length === 0) {
      return { success: false, raison: 'aucun_objectif_defini' };
    }

    const inconnus = objectifs.filter((o) => !CATALOGUE_MICRO_OBJECTIFS[o]);
    if (inconnus.length > 0) {
      return { success: false, raison: 'objectif_inconnu', objectifs: inconnus };
    }

    let compteur = 0;
    const microObjectifs = objectifs.flatMap((objectif) =>
      CATALOGUE_MICRO_OBJECTIFS[objectif].map((titre) => ({
        id: ++compteur,
        objectif,
        titre,
        semaine: 1,
        fait: false,
      })),
    );
    this.base.setMicroObjectifs(userId, microObjectifs);
    return { success: true, microObjectifs };
  }

  /** Marque un micro-objectif comme accompli. */
  validerMicroObjectif(userId, microId) {
    this.base.validerMicroObjectif(userId, microId);
    return this.progression(userId);
  }

  /** Retourne la progression globale de l'utilisateur. */
  progression(userId) {
    const liste = this.base.getMicroObjectifs(userId);
    if (liste.length === 0) {
      return { success: false, raison: 'aucun_micro_objectif' };
    }
    const faits = liste.filter((m) => m.fait).length;
    return {
      success: true,
      total: liste.length,
      faits,
      pourcentage: Math.round((faits / liste.length) * 100),
    };
  }
}
