export type ContentType = "linkedin_post" | "case_study" | "cv_update" | "article" | "newsletter";
export type ContentStatus = "planned" | "in_progress" | "ready" | "published";

export interface EditorialItem {
  item_id: string;
  week: number;
  day: number;
  date: string;
  content_type: ContentType;
  title: string;
  hook?: string;
  status: ContentStatus;
  agent_id: string;
  estimated_impressions?: number;
  topic: string;
  tags: string[];
}

export interface WeeklyTheme {
  week: number;
  start_date: string;
  end_date: string;
  theme: string;
  color: string;
}

export const WEEKLY_THEMES: WeeklyTheme[] = [
  { week: 25, start_date: "2026-06-15", end_date: "2026-06-21", theme: "Lancement du Swarm : les coulisses", color: "#6366f1" },
  { week: 26, start_date: "2026-06-22", end_date: "2026-06-28", theme: "Les ventes autonomes expliquées", color: "#EC4899" },
  { week: 27, start_date: "2026-06-29", end_date: "2026-07-05", theme: "Études de cas clients réels", color: "#10b981" },
  { week: 28, start_date: "2026-07-06", end_date: "2026-07-12", theme: "Personal branding & crédibilité", color: "#f59e0b" },
];

export const EDITORIAL_ITEMS: EditorialItem[] = [
  // Week 25
  {
    item_id: "ed_w25_mon",
    week: 25,
    day: 1,
    date: "2026-06-16",
    content_type: "linkedin_post",
    title: "J'ai déployé 50 agents IA ce matin",
    hook: "J'ai déployé 50 agents IA autonomes ce matin. Voici ce qu'ils ont accompli en 24h 👇",
    status: "published",
    agent_id: "6.1",
    estimated_impressions: 12400,
    topic: "Lancement Swarm",
    tags: ["IA", "Automatisation", "Swarm"],
  },
  {
    item_id: "ed_w25_wed",
    week: 25,
    day: 3,
    date: "2026-06-18",
    content_type: "linkedin_post",
    title: "L'architecture : 5 divisions, 50 agents",
    hook: "Voici comment j'ai organisé 50 agents IA en 5 divisions spécialisées 🏗️",
    status: "ready",
    agent_id: "6.1",
    estimated_impressions: 9800,
    topic: "Architecture technique",
    tags: ["Architecture", "LangGraph", "CrewAI"],
  },
  {
    item_id: "ed_w25_fri",
    week: 25,
    day: 5,
    date: "2026-06-20",
    content_type: "case_study",
    title: "Lyon Restaurant : 149€ en 3min35",
    hook: "Un restaurateur lyonnais sceptique. Mon agent de négociation. Résultat en 3min35.",
    status: "ready",
    agent_id: "6.3",
    estimated_impressions: 11200,
    topic: "Négociation commerciale",
    tags: ["CaseStudy", "Négociation", "Restauration"],
  },
  // Week 26
  {
    item_id: "ed_w26_mon",
    week: 26,
    day: 1,
    date: "2026-06-22",
    content_type: "linkedin_post",
    title: "Comment je fixe le prix en 8 secondes",
    hook: "Mon agent 5.1 fixe le prix en 8 secondes. Voici son algorithme exact 💡",
    status: "planned",
    agent_id: "6.1",
    estimated_impressions: 14800,
    topic: "Tarification automatique",
    tags: ["Pricing", "IA", "Vente"],
  },
  {
    item_id: "ed_w26_tue",
    week: 26,
    day: 2,
    date: "2026-06-23",
    content_type: "newsletter",
    title: "Newsletter #1 : Les coulisses du Swarm",
    status: "planned",
    agent_id: "6.7",
    estimated_impressions: 3200,
    topic: "Newsletter mensuelle",
    tags: ["Newsletter", "Behind the scenes"],
  },
  {
    item_id: "ed_w26_thu",
    week: 26,
    day: 4,
    date: "2026-06-25",
    content_type: "linkedin_post",
    title: "3 erreurs que j'ai faites en construisant le Swarm",
    hook: "J'ai passé 3 semaines à construire le Swarm. J'ai fait 3 erreurs majeures.",
    status: "planned",
    agent_id: "6.1",
    estimated_impressions: 13500,
    topic: "Lessons learned",
    tags: ["Erreurs", "Apprentissage", "IA"],
  },
  {
    item_id: "ed_w26_fri",
    week: 26,
    day: 5,
    date: "2026-06-26",
    content_type: "linkedin_post",
    title: "Mon agent 5.4 a bloqué 23 emails non-RGPD",
    hook: "Mon agent RGPD a bloqué 23 emails avant l'envoi ce matin. Voici pourquoi c'est une bonne nouvelle 🔒",
    status: "planned",
    agent_id: "6.1",
    estimated_impressions: 10400,
    topic: "RGPD & conformité",
    tags: ["RGPD", "Conformité", "IA éthique"],
  },
  // Week 27
  {
    item_id: "ed_w27_mon",
    week: 27,
    day: 1,
    date: "2026-06-29",
    content_type: "case_study",
    title: "Paris Médecin : site RGPD en 48h",
    hook: "Un médecin parisien m'a contacté un lundi. Son site était en ligne le mercredi.",
    status: "planned",
    agent_id: "6.3",
    estimated_impressions: 9600,
    topic: "Étude de cas médicale",
    tags: ["Médical", "RGPD", "CaseStudy"],
  },
  {
    item_id: "ed_w27_wed",
    week: 27,
    day: 3,
    date: "2026-07-01",
    content_type: "article",
    title: "Pourquoi les artisans français perdent des clients à cause de leur site web",
    status: "planned",
    agent_id: "6.7",
    estimated_impressions: 7800,
    topic: "Marché artisans",
    tags: ["Artisans", "Site web", "France"],
  },
  {
    item_id: "ed_w27_fri",
    week: 27,
    day: 5,
    date: "2026-07-03",
    content_type: "linkedin_post",
    title: "Nice Garage : créer de zéro une présence en ligne",
    hook: "Aucun site. Aucune présence Google. Un garage niçois invisible depuis 12 ans.",
    status: "planned",
    agent_id: "6.1",
    estimated_impressions: 8900,
    topic: "Création from scratch",
    tags: ["Garage", "SEO local", "Création"],
  },
  // Week 28
  {
    item_id: "ed_w28_mon",
    week: 28,
    day: 1,
    date: "2026-07-06",
    content_type: "cv_update",
    title: "Mise à jour CV : Architecte Swarm IA",
    status: "planned",
    agent_id: "6.2",
    topic: "Personal branding",
    tags: ["CV", "IA", "Architecte"],
  },
  {
    item_id: "ed_w28_wed",
    week: 28,
    day: 3,
    date: "2026-07-08",
    content_type: "linkedin_post",
    title: "Pourquoi j'ai nommé mes agents avec des backstories",
    hook: "Mes 50 agents IA ont des noms, des rôles, des backstories. Voici pourquoi ce détail change tout 🎭",
    status: "planned",
    agent_id: "6.1",
    estimated_impressions: 16300,
    topic: "Design des agents",
    tags: ["Design", "Prompt engineering", "IA"],
  },
  {
    item_id: "ed_w28_fri",
    week: 28,
    day: 5,
    date: "2026-07-10",
    content_type: "newsletter",
    title: "Newsletter #2 : Bilan du premier mois",
    status: "planned",
    agent_id: "6.7",
    estimated_impressions: 3800,
    topic: "Bilan mensuel",
    tags: ["Newsletter", "Bilan", "Métriques"],
  },
];

export const TYPE_META: Record<ContentType, { label: string; color: string; bg: string }> = {
  linkedin_post: { label: "LinkedIn", color: "text-blue-700", bg: "bg-blue-50" },
  case_study: { label: "Étude de cas", color: "text-purple-700", bg: "bg-purple-50" },
  cv_update: { label: "CV", color: "text-amber-700", bg: "bg-amber-50" },
  article: { label: "Article", color: "text-green-700", bg: "bg-green-50" },
  newsletter: { label: "Newsletter", color: "text-pink-700", bg: "bg-pink-50" },
};

export const STATUS_META: Record<ContentStatus, { label: string; color: string; dot: string }> = {
  published: { label: "Publié", color: "text-green-700", dot: "bg-green-500" },
  ready: { label: "Prêt", color: "text-blue-700", dot: "bg-blue-500" },
  in_progress: { label: "En cours", color: "text-amber-700", dot: "bg-amber-500" },
  planned: { label: "Planifié", color: "text-slate-500", dot: "bg-slate-300" },
};
