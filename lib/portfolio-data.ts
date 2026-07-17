export interface PortfolioProject {
  project_id: string;
  client_alias: string;
  sector: string;
  city: string;
  problem: string;
  solution: string;
  deliverables: string[];
  result_score: number;
  result_loadtime_before: number;
  result_loadtime_after: number;
  revenue_eur: number;
  completed_at: string;
  tags: string[];
  agent_ids: string[];
}

export interface PortfolioSkill {
  category: string;
  skills: { name: string; level: number }[];
}

export interface PortfolioStat {
  label: string;
  value: string;
  delta?: string;
  color: string;
}

export const PORTFOLIO_STATS: PortfolioStat[] = [
  { label: "Projets livrés", value: "47", delta: "+12 ce mois", color: "indigo" },
  { label: "CA généré", value: "7 843€", delta: "+2 237€ ce cycle", color: "green" },
  { label: "Score PageSpeed moy. après", value: "91/100", delta: "+54 pts", color: "blue" },
  { label: "Taux de conversion", value: "68%", delta: "négociation → paiement", color: "pink" },
];

export const PORTFOLIO_PROJECTS: PortfolioProject[] = [
  {
    project_id: "proj_rest_girard",
    client_alias: "Restaurant Le Bouchon Lyonnais",
    sector: "Restauration",
    city: "Lyon",
    problem: "Site web non responsive, PageSpeed 21/100, temps de chargement 7,8s. Perte estimée de 30% des réservations en ligne.",
    solution: "Refonte complète en HTML5/CSS3 responsive, optimisation images, mise en cache, intégration Google Maps et système de réservation.",
    deliverables: ["Site optimisé responsive", "Rapport d'audit technique", "Guide mise à jour contenu", "Intégration Google Business"],
    result_score: 94,
    result_loadtime_before: 7800,
    result_loadtime_after: 1200,
    revenue_eur: 149,
    completed_at: "2026-06-17T06:04:32Z",
    tags: ["Restauration", "SEO", "Performance", "Mobile"],
    agent_ids: ["4.1", "4.7", "5.1", "5.3"],
  },
  {
    project_id: "proj_med_moreau",
    client_alias: "Cabinet Dr. Moreau",
    sector: "Médical",
    city: "Paris",
    problem: "Site vitrine obsolète, aucune présence mobile, formulaire de contact non fonctionnel. PageSpeed 18/100.",
    solution: "Nouveau site médical RGPD-compliant avec formulaire sécurisé, agenda de rendez-vous intégré, mentions légales conformes.",
    deliverables: ["Site médical RGPD", "Formulaire rendez-vous sécurisé", "Mentions légales", "Politique confidentialité"],
    result_score: 89,
    result_loadtime_before: 9100,
    result_loadtime_after: 1400,
    revenue_eur: 189,
    completed_at: "2026-06-17T06:03:11Z",
    tags: ["Médical", "RGPD", "Sécurité", "Mobile"],
    agent_ids: ["4.4", "4.8", "5.1", "5.4"],
  },
  {
    project_id: "proj_sport_elite",
    client_alias: "Gymnase Sport Elite",
    sector: "Associations",
    city: "Lyon",
    problem: "Site association vieillissant, impossible à mettre à jour sans développeur, aucune intégration réseaux sociaux.",
    solution: "CMS léger intégré, galerie photos optimisée, liens Instagram/Facebook, planning des cours en ligne mis à jour automatiquement.",
    deliverables: ["Site avec CMS intégré", "Galerie optimisée", "Intégration réseaux sociaux", "Planning en ligne"],
    result_score: 91,
    result_loadtime_before: 6500,
    result_loadtime_after: 980,
    revenue_eur: 129,
    completed_at: "2026-06-17T06:01:55Z",
    tags: ["Sport", "CMS", "Réseaux sociaux", "Performance"],
    agent_ids: ["4.1", "4.6", "5.1"],
  },
  {
    project_id: "proj_garage_moto",
    client_alias: "Garage Moto Azur",
    sector: "Garages",
    city: "Nice",
    problem: "Aucun site web actif, présence Google Maps inexistante, perte de clientèle locale au profit des concurrents numériques.",
    solution: "Création from scratch d'un site vitrine moderne, fiche Google Business optimisée, photos professionnelles des services.",
    deliverables: ["Site vitrine complet", "Google Business optimisé", "Portfolio services", "SEO local"],
    result_score: 88,
    result_loadtime_before: 0,
    result_loadtime_after: 1100,
    revenue_eur: 159,
    completed_at: "2026-06-17T06:02:44Z",
    tags: ["Automobile", "SEO local", "Création", "Google Business"],
    agent_ids: ["4.1", "4.3", "5.1", "5.2"],
  },
  {
    project_id: "proj_elec_bonneau",
    client_alias: "Électricité Bonneau",
    sector: "Artisans & Bâtiment",
    city: "Bordeaux",
    problem: "Site non sécurisé (HTTP), PageSpeed 28/100, formulaire de devis cassé depuis 6 mois. Perte de leads estimée à 40%.",
    solution: "Migration HTTPS, optimisation complète, nouveau formulaire de devis avec notification email, badge NF élec intégré.",
    deliverables: ["Migration HTTPS", "Formulaire devis", "Optimisation images", "Badge qualifications"],
    result_score: 92,
    result_loadtime_before: 6200,
    result_loadtime_after: 1050,
    revenue_eur: 129,
    completed_at: "2026-06-16T14:22:00Z",
    tags: ["Artisan", "HTTPS", "Devis en ligne", "NF Élec"],
    agent_ids: ["4.2", "4.7", "5.1", "5.3"],
  },
  {
    project_id: "proj_creperie_morvan",
    client_alias: "Crêperie Bretonne Morvan",
    sector: "Restauration",
    city: "Rennes",
    problem: "Site avec musique automatique au chargement, images non compressées (12 Mo), aucune carte des menus en ligne.",
    solution: "Refonte UX complète, menu digital interactif, galerie photos optimisée, intégration avis Google et TripAdvisor.",
    deliverables: ["Site UX moderne", "Menu digital", "Galerie optimisée", "Widget avis"],
    result_score: 87,
    result_loadtime_before: 8100,
    result_loadtime_after: 1350,
    revenue_eur: 149,
    completed_at: "2026-06-15T10:15:00Z",
    tags: ["Restauration", "UX", "Menu digital", "Avis clients"],
    agent_ids: ["4.1", "4.5", "5.1"],
  },
];

export const PORTFOLIO_SKILLS: PortfolioSkill[] = [
  {
    category: "Architecture IA",
    skills: [
      { name: "Multi-agent orchestration", level: 98 },
      { name: "LangGraph / CrewAI", level: 95 },
      { name: "Anthropic Claude API", level: 97 },
      { name: "Prompt engineering", level: 96 },
    ],
  },
  {
    category: "Développement",
    skills: [
      { name: "Next.js 16 / React 19", level: 92 },
      { name: "Python / FastAPI", level: 90 },
      { name: "Prisma / SQLite", level: 85 },
      { name: "TypeScript", level: 91 },
    ],
  },
  {
    category: "Business & Vente",
    skills: [
      { name: "Négociation commerciale", level: 88 },
      { name: "Prospection automatisée", level: 95 },
      { name: "Copywriting IA", level: 92 },
      { name: "Stripe / Paiements", level: 80 },
    ],
  },
  {
    category: "Marketing",
    skills: [
      { name: "Personal branding LinkedIn", level: 90 },
      { name: "SEO technique", level: 85 },
      { name: "A/B testing", level: 82 },
      { name: "RGPD / Conformité", level: 88 },
    ],
  },
];
