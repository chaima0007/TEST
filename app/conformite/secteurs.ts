// Table secteurs → normes prioritaires (Caelum). Sert aux pages SEO longue traîne
// /conformite/secteur/[secteur]. Contenu substantiel (pas de page vide) : chaque secteur
// pointe vers les normes réellement pertinentes, détaillées depuis la base vérifiée.

export type Secteur = {
  slug: string;
  nom: string;
  intro: string;
  // ids de normes (data/caelum) particulièrement pertinentes pour ce secteur
  normesIds: string[];
  note: string;
};

export const SECTEURS: Secteur[] = [
  {
    slug: "commerce-detail",
    nom: "Commerce de détail",
    intro: "Magasins, boutiques et points de vente : la facturation électronique et la protection des données clients sont vos priorités.",
    normesIds: ["EFACT-2026", "RGPD", "LANCEURS-ALERTE"],
    note: "Programme de fidélité, fichier clients, caméras : autant de traitements de données à mettre en règle (RGPD).",
  },
  {
    slug: "horeca",
    nom: "Horeca (cafés, restaurants, hôtels)",
    intro: "Dans l'horeca, l'e-facturation B2B (fournisseurs) et le RGPD (réservations, clients) sont incontournables.",
    normesIds: ["EFACT-2026", "RGPD", "LANCEURS-ALERTE"],
    note: "Réservations en ligne et fichiers clients = données personnelles à protéger.",
  },
  {
    slug: "construction",
    nom: "Construction & bâtiment",
    intro: "Entreprises du bâtiment : facturation électronique avec vos donneurs d'ordre et conformité de la chaîne de valeur.",
    normesIds: ["EFACT-2026", "RGPD", "LANCEURS-ALERTE"],
    note: "Vos grands donneurs d'ordre peuvent vous répercuter des exigences ESG/devoir de vigilance (effet cascade).",
  },
  {
    slug: "sante",
    nom: "Santé & professions médicales",
    intro: "Cabinets, pharmacies, maisons médicales : données de santé sensibles et, souvent, obligations de cybersécurité.",
    normesIds: ["EFACT-2026", "RGPD", "NIS2-BE", "LANCEURS-ALERTE"],
    note: "Les données de santé sont sensibles (RGPD renforcé) et le secteur peut relever de NIS2 (cybersécurité).",
  },
  {
    slug: "it-numerique",
    nom: "IT & services numériques",
    intro: "Éditeurs, hébergeurs, agences : cybersécurité (NIS2) et protection des données au cœur de votre activité.",
    normesIds: ["EFACT-2026", "RGPD", "NIS2-BE", "LANCEURS-ALERTE"],
    note: "Beaucoup d'acteurs numériques relèvent de NIS2 — la responsabilité du dirigeant y est renforcée.",
  },
  {
    slug: "transport-logistique",
    nom: "Transport & logistique",
    intro: "Transporteurs et logisticiens : secteur critique, souvent concerné par la cybersécurité (NIS2).",
    normesIds: ["EFACT-2026", "RGPD", "NIS2-BE", "LANCEURS-ALERTE"],
    note: "Le transport est un secteur critique : vérifiez si NIS2 s'applique à votre entreprise.",
  },
  {
    slug: "services-professions-liberales",
    nom: "Services & professions libérales",
    intro: "Consultants, avocats, comptables, architectes : facturation électronique et données clients.",
    normesIds: ["EFACT-2026", "RGPD", "LANCEURS-ALERTE"],
    note: "En tant que professionnel, vous traitez des données clients confidentielles : le RGPD est central.",
  },
  {
    slug: "ecommerce",
    nom: "E-commerce",
    intro: "Boutiques en ligne : données clients, paiements et facturation électronique.",
    normesIds: ["EFACT-2026", "RGPD", "LANCEURS-ALERTE"],
    note: "Collecte massive de données (comptes, paiements, cookies) = RGPD à maîtriser absolument.",
  },
];

export function secteurBySlug(slug: string): Secteur | undefined {
  return SECTEURS.find((s) => s.slug === slug);
}
