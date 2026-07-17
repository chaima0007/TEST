// Table secteurs → normes prioritaires (Caelum). Sert aux pages SEO longue traîne
// /conformite/secteur/[secteur]. Contenu substantiel (pas de page vide) : chaque secteur
// pointe vers les normes réellement pertinentes, détaillées depuis la base vérifiée.
// Les normesIds correspondent EXACTEMENT aux id de data/caelum/conformite_entreprises.json.

export type Secteur = {
  slug: string;
  nom: string;
  intro: string;
  // ids de normes (data/caelum) particulièrement pertinentes pour ce secteur
  normesIds: string[];
  note: string;
};

// Normes quasi universelles (toute société assujettie / avec un registre UBO).
const SOCLE = ["EFACT-2026", "RGPD", "UBO", "DELAIS-PAIEMENT", "LANCEURS-ALERTE"];

export const SECTEURS: Secteur[] = [
  {
    slug: "commerce-detail",
    nom: "Commerce de détail",
    intro: "Magasins, boutiques et points de vente : facturation électronique, protection des données clients et délais de paiement avec vos fournisseurs.",
    normesIds: [...SOCLE],
    note: "Programme de fidélité, fichier clients, caméras : autant de traitements de données à mettre en règle (RGPD). Vos achats fournisseurs relèvent des délais de paiement B2B.",
  },
  {
    slug: "horeca",
    nom: "Horeca (cafés, restaurants, hôtels)",
    intro: "Dans l'horeca, l'e-facturation B2B (fournisseurs), le RGPD (réservations, clients) et les délais de paiement sont incontournables.",
    normesIds: [...SOCLE],
    note: "Réservations en ligne et fichiers clients = données personnelles à protéger. Pensez aussi au registre UBO de votre société.",
  },
  {
    slug: "construction",
    nom: "Construction & bâtiment",
    intro: "Entreprises du bâtiment : facturation électronique avec vos donneurs d'ordre, délais de paiement et conformité de la chaîne de valeur.",
    normesIds: [...SOCLE, "CSDDD-OMNIBUS"],
    note: "Vos grands donneurs d'ordre peuvent vous répercuter des exigences ESG/devoir de vigilance (effet cascade CSDDD).",
  },
  {
    slug: "sante",
    nom: "Santé & professions médicales",
    intro: "Cabinets, pharmacies, maisons médicales : données de santé sensibles et, souvent, obligations de cybersécurité.",
    normesIds: [...SOCLE, "NIS2-BE", "EAA"],
    note: "Les données de santé sont sensibles (RGPD renforcé) et le secteur peut relever de NIS2 (cybersécurité). Vos services numériques au public peuvent relever de l'accessibilité (EAA).",
  },
  {
    slug: "it-numerique",
    nom: "IT & services numériques",
    intro: "Éditeurs, hébergeurs, agences : cybersécurité (NIS2), IA (AI Act), accessibilité numérique et protection des données au cœur de votre activité.",
    normesIds: [...SOCLE, "NIS2-BE", "AI-ACT", "EAA"],
    note: "Beaucoup d'acteurs numériques relèvent de NIS2 — la responsabilité du dirigeant y est renforcée. Si vous développez ou intégrez de l'IA, l'AI Act s'applique progressivement.",
  },
  {
    slug: "transport-logistique",
    nom: "Transport & logistique",
    intro: "Transporteurs et logisticiens : secteur critique, souvent concerné par la cybersécurité (NIS2) et le reporting durabilité.",
    normesIds: [...SOCLE, "NIS2-BE", "CSRD-OMNIBUS"],
    note: "Le transport est un secteur critique : vérifiez si NIS2 s'applique. Les grands groupes sont concernés par le reporting durabilité (CSRD).",
  },
  {
    slug: "services-professions-liberales",
    nom: "Services & professions libérales",
    intro: "Consultants, avocats, comptables, architectes : facturation électronique, données clients et obligations anti-blanchiment pour certaines professions.",
    normesIds: [...SOCLE, "AML-LBC"],
    note: "Vous traitez des données clients confidentielles : le RGPD est central. Certaines professions (notaires, comptables, avocats) sont soumises aux obligations anti-blanchiment (LBC/FT).",
  },
  {
    slug: "ecommerce",
    nom: "E-commerce",
    intro: "Boutiques en ligne : données clients, paiements, facturation électronique, accessibilité numérique et emballages.",
    normesIds: [...SOCLE, "EAA", "PPWR-2026", "DAC7-2024"],
    note: "Collecte massive de données (comptes, paiements, cookies) = RGPD à maîtriser. Votre site doit être accessible (EAA) ; vos emballages relèvent du PPWR. Les places de marché relèvent de DAC7.",
  },
  {
    slug: "finance-assurance",
    nom: "Finance, assurance & fintech",
    intro: "Banques, assureurs, fintechs et prestataires de paiement : résilience numérique (DORA), anti-blanchiment et cybersécurité sont au cœur de vos obligations.",
    normesIds: [...SOCLE, "DORA-2025", "AML-LBC", "NIS2-BE"],
    note: "DORA impose un cadre strict de résilience informatique et de maîtrise des prestataires tiers. Les obligations anti-blanchiment (KYC, CTIF) y sont déterminantes.",
  },
  {
    slug: "industrie-manufacture",
    nom: "Industrie & fabrication",
    intro: "Industriels et fabricants : reporting durabilité, devoir de vigilance, emballages, ajustement carbone aux frontières et transparence salariale.",
    normesIds: [...SOCLE, "CSRD-OMNIBUS", "CSDDD-OMNIBUS", "PPWR-2026", "CBAM-2026", "PAYEQUITY-2026"],
    note: "Selon votre taille, le reporting durabilité (CSRD) et le devoir de vigilance (CSDDD) s'appliquent. Si vous importez acier, aluminium, ciment, engrais, le CBAM vous concerne.",
  },
  {
    slug: "import-export",
    nom: "Import-export & négoce",
    intro: "Importateurs, négociants et distributeurs : ajustement carbone (CBAM), déforestation importée (EUDR), emballages et délais de paiement.",
    normesIds: [...SOCLE, "CBAM-2026", "EUDR", "PPWR-2026"],
    note: "Importer acier/aluminium/ciment/engrais = statut de déclarant CBAM. Mettre sur le marché bois, cacao, café, soja, caoutchouc = diligence « zéro déforestation » (EUDR).",
  },
];

export function secteurBySlug(slug: string): Secteur | undefined {
  return SECTEURS.find((s) => s.slug === slug);
}
