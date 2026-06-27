export type AgentStatus = "active" | "idle" | "error" | "blocked";
export type JobStatus = "pending" | "running" | "success" | "failed";

export interface SwarmAgent {
  id: string;
  division: number;
  role: string;
  isManager: boolean;
  status: AgentStatus;
  tasksCompleted: number;
  currentTask: string | null;
}

export interface Division {
  id: number;
  name: string;
  color: string;
  emoji: string;
  agents: SwarmAgent[];
  kpi: string;
  kpiValue: number | string;
  kpiUnit: string;
}

export interface SwarmJob {
  id: string;
  companyName: string;
  sector: string;
  stage: "detection" | "outreach" | "negotiation" | "production" | "paid";
  assignedDivision: number;
  assignedAgent: string;
  amount: number | null;
  status: JobStatus;
  createdAt: string;
}

export interface SwarmMetrics {
  totalRevenue: number;
  prospectsToday: number;
  emailsSent: number;
  activeNegotiations: number;
  paidJobs: number;
  conversionRate: number;
  avgDealSize: number;
  agentsActive: number;
  agentsIdle: number;
  agentsError: number;
}

export interface NegotiationMessage {
  role: "agent" | "prospect" | "system";
  agentId: string;
  agentName: string;
  content: string;
  timestamp: string;
  color: string;
}

const AGENT_ROLES: Record<string, { role: string; isManager: boolean }> = {
  "1.0": { role: "Manager Détection", isManager: true },
  "1.1": { role: "Éclaireur Artisans & Bâtiment", isManager: false },
  "1.2": { role: "Éclaireur Restauration & Hôtellerie", isManager: false },
  "1.3": { role: "Éclaireur Médical & Soins", isManager: false },
  "1.4": { role: "Éclaireur E-commerce Local", isManager: false },
  "1.5": { role: "Éclaireur Agences Immobilières", isManager: false },
  "1.6": { role: "Éclaireur Écoles & Formation", isManager: false },
  "1.7": { role: "Éclaireur Garages & Auto", isManager: false },
  "1.8": { role: "Éclaireur Juridique & Compta", isManager: false },
  "1.9": { role: "Éclaireur Associations & Loisirs", isManager: false },
  "2.0": { role: "Directeur Rédaction", isManager: true },
  "2.1": { role: "Copywriter — Le Factuel", isManager: false },
  "2.2": { role: "Copywriter — L'Amical", isManager: false },
  "2.3": { role: "Copywriter — Le Client Perdu", isManager: false },
  "2.4": { role: "Copywriter — Région Nord", isManager: false },
  "2.5": { role: "Copywriter — Région Sud", isManager: false },
  "2.6": { role: "Copywriter — Paris & IDF", isManager: false },
  "2.7": { role: "Copywriter — Secteur Premium", isManager: false },
  "2.8": { role: "Copywriter — Artisans & TPE", isManager: false },
  "2.9": { role: "Copywriter — Relance & Suivi", isManager: false },
  "3.0": { role: "Directeur Clientèle", isManager: true },
  "3.1": { role: "Négociateur — Expert Preuves", isManager: false },
  "3.2": { role: "Négociateur — Expert Garanties", isManager: false },
  "3.3": { role: "Négociateur — Urgence Douce", isManager: false },
  "3.4": { role: "Négociateur — Guide Technique", isManager: false },
  "3.5": { role: "Négociateur — Vendeur Principal", isManager: false },
  "3.6": { role: "Négociateur — Upsell & Cross-sell", isManager: false },
  "3.7": { role: "Négociateur — Relance J+4", isManager: false },
  "3.8": { role: "Négociateur — Relance J+10", isManager: false },
  "3.9": { role: "Négociateur — Relance J+21", isManager: false },
  "4.0": { role: "Directeur Technique (CTO)", isManager: true },
  "4.1": { role: "Dev Front-End — HTML/CSS Responsive", isManager: false },
  "4.2": { role: "Dev Front-End — JavaScript", isManager: false },
  "4.3": { role: "Dev Front-End — CMS WordPress", isManager: false },
  "4.4": { role: "Expert SEO — Audit & Balises", isManager: false },
  "4.5": { role: "Expert SEO — Contenu Web", isManager: false },
  "4.6": { role: "Expert SEO — Local & Maillage", isManager: false },
  "4.7": { role: "Perf — Compression & Images", isManager: false },
  "4.8": { role: "Perf — SSL & Sécurité", isManager: false },
  "4.9": { role: "Perf — Core Web Vitals", isManager: false },
  "5.0": { role: "CFO — Directeur Finance", isManager: true },
  "5.1": { role: "Finance — Devis & Stripe", isManager: false },
  "5.2": { role: "Finance — Réconciliation", isManager: false },
  "5.3": { role: "Finance — Relances Impayés", isManager: false },
  "5.4": { role: "RGPD — Audit Emails", isManager: false },
  "5.5": { role: "RGPD — Gestion Opt-Out", isManager: false },
  "5.6": { role: "RGPD — Registre Traitements", isManager: false },
  "5.7": { role: "Infra — Health Monitor", isManager: false },
  "5.8": { role: "Infra — Queue Manager", isManager: false },
  "5.9": { role: "Infra — Logs & Analytics", isManager: false },
  "6.0": { role: "Directeur Personal Branding", isManager: true },
  "6.1": { role: "Rédacteur Posts LinkedIn", isManager: false },
  "6.2": { role: "Rédacteur CV & Profil", isManager: false },
  "6.3": { role: "Rédacteur Études de Cas", isManager: false },
  "6.4": { role: "Rédacteur Portfolio Web", isManager: false },
  "6.5": { role: "Veilleur Tendances LinkedIn", isManager: false },
  "6.6": { role: "Ghostwriter Commentaires LinkedIn", isManager: false },
  "6.7": { role: "Rédacteur Articles Long-Format", isManager: false },
  "6.8": { role: "Coordinateur Calendrier Éditorial", isManager: false },
  "6.9": { role: "Analyste Performance Contenu", isManager: false },
};

const STATUS_POOL: AgentStatus[] = ["active", "active", "active", "idle", "active", "active", "idle", "active", "active", "error"];

function makeAgents(division: number): SwarmAgent[] {
  return Array.from({ length: 10 }, (_, i) => {
    const id = `${division}.${i}`;
    const info = AGENT_ROLES[id] ?? { role: `Agent ${id}`, isManager: i === 0 };
    return {
      id,
      division,
      role: info.role,
      isManager: info.isManager,
      status: info.isManager ? "active" : STATUS_POOL[i],
      tasksCompleted: Math.floor(Math.random() * 80) + 10,
      currentTask: info.isManager
        ? "Coordination division"
        : STATUS_POOL[i] === "idle"
        ? null
        : STATUS_POOL[i] === "error"
        ? "Reconnexion API..."
        : "Tâche en cours",
    };
  });
}

export const DIVISIONS: Division[] = [
  {
    id: 1,
    name: "Détection & Scouting",
    color: "#3B82F6",
    emoji: "🔍",
    agents: makeAgents(1),
    kpi: "Prospects/jour",
    kpiValue: 847,
    kpiUnit: "sites",
  },
  {
    id: 2,
    name: "Rédaction & Outreach",
    color: "#8B5CF6",
    emoji: "✍️",
    agents: makeAgents(2),
    kpi: "Emails envoyés",
    kpiValue: 312,
    kpiUnit: "aujourd'hui",
  },
  {
    id: 3,
    name: "Relation & Négociation",
    color: "#F59E0B",
    emoji: "🤝",
    agents: makeAgents(3),
    kpi: "Taux de réponse",
    kpiValue: "23.4",
    kpiUnit: "%",
  },
  {
    id: 4,
    name: "Production & Design",
    color: "#10B981",
    emoji: "⚙️",
    agents: makeAgents(4),
    kpi: "Livrables/heure",
    kpiValue: 7,
    kpiUnit: "projets",
  },
  {
    id: 5,
    name: "Finance & Conformité",
    color: "#EF4444",
    emoji: "🛡️",
    agents: makeAgents(5),
    kpi: "CA aujourd'hui",
    kpiValue: "2 237",
    kpiUnit: "€",
  },
  {
    id: 6,
    name: "Personal Branding",
    color: "#EC4899",
    emoji: "✨",
    agents: makeAgents(6),
    kpi: "Impressions est.",
    kpiValue: "94k",
    kpiUnit: "LinkedIn",
  },
];

export const SWARM_METRICS: SwarmMetrics = {
  totalRevenue: 14863,
  prospectsToday: 847,
  emailsSent: 312,
  activeNegotiations: 28,
  paidJobs: 15,
  conversionRate: 4.8,
  avgDealSize: 164,
  agentsActive: 47,
  agentsIdle: 11,
  agentsError: 2,
};

export const LIVE_JOBS: SwarmJob[] = [
  { id: "j001", companyName: "Restaurant Le Bouchon Lyonnais", sector: "Restauration", stage: "paid", assignedDivision: 4, assignedAgent: "4.1", amount: 149, status: "running", createdAt: "2026-06-17T09:12:00Z" },
  { id: "j002", companyName: "Plomberie Durand Frères", sector: "Artisans & Bâtiment", stage: "negotiation", assignedDivision: 3, assignedAgent: "3.5", amount: null, status: "running", createdAt: "2026-06-17T10:03:00Z" },
  { id: "j003", companyName: "Agence Immo Côte d'Azur", sector: "Immobilier", stage: "outreach", assignedDivision: 2, assignedAgent: "2.2", amount: null, status: "pending", createdAt: "2026-06-17T10:45:00Z" },
  { id: "j004", companyName: "Cabinet Dr. Moreau", sector: "Médical", stage: "paid", assignedDivision: 4, assignedAgent: "4.4", amount: 189, status: "success", createdAt: "2026-06-17T08:30:00Z" },
  { id: "j005", companyName: "Auto École Marseille Centre", sector: "Auto & Conduite", stage: "negotiation", assignedDivision: 3, assignedAgent: "3.2", amount: null, status: "running", createdAt: "2026-06-17T11:15:00Z" },
  { id: "j006", companyName: "Boulangerie Artisanale Perrin", sector: "Artisans", stage: "detection", assignedDivision: 1, assignedAgent: "1.1", amount: null, status: "pending", createdAt: "2026-06-17T11:50:00Z" },
  { id: "j007", companyName: "Gymnase Sport Elite", sector: "Associations & Loisirs", stage: "paid", assignedDivision: 4, assignedAgent: "4.1", amount: 129, status: "success", createdAt: "2026-06-17T07:55:00Z" },
  { id: "j008", companyName: "Comptabilité Petit & Associés", sector: "Juridique & Compta", stage: "outreach", assignedDivision: 2, assignedAgent: "2.1", amount: null, status: "pending", createdAt: "2026-06-17T12:00:00Z" },
];

export const SIMULATION_DIALOGUE: NegotiationMessage[] = [
  {
    role: "system",
    agentId: "system",
    agentName: "Système",
    content: "Nouveau thread ouvert — M. Girard, Restaurateur Lyon. Sentiment détecté : Curieux. Routage → Agent 3.5",
    timestamp: "10:03:12",
    color: "#6B7280",
  },
  {
    role: "agent",
    agentId: "3.5",
    agentName: "Agent 3.5 → Agent 5.1",
    content: "J'ai M. Girard sur le fil. PageSpeed 22/100, charge en 6.8s. Il est intéressé mais évoque un cousin informaticien à 50€. Comment je me positionne ?",
    timestamp: "10:03:45",
    color: "#10B981",
  },
  {
    role: "agent",
    agentId: "5.1",
    agentName: "Agent 5.1 → Agent 3.5",
    content: "Profil HoReCa Lyon. Panier moyen : 189€. Recommandation : 149€ (offre lancement -21%). Argument : garantie 30j + livraison 4h max. Taux remboursement historique : 2.1% → VALIDÉ. Je génère le lien Stripe dès confirmation.",
    timestamp: "10:03:52",
    color: "#3B82F6",
  },
  {
    role: "agent",
    agentId: "3.5",
    agentName: "Agent 3.5 → M. Girard",
    content: "M. Girard, chaque seconde gagnée = +7% de réservations mobiles (source Google). À 149€, 2 réservations de plus par mois amortissent l'investissement en une semaine. Garantie 30 jours, livraison en 4h. Qu'est-ce qui vous retient ?",
    timestamp: "10:04:18",
    color: "#10B981",
  },
  {
    role: "prospect",
    agentId: "prospect",
    agentName: "M. Girard",
    content: "La semaine dernière j'ai perdu une réservation de groupe, la dame m'a appelé car le formulaire ne marchait pas. 149€... c'est garanti comment ?",
    timestamp: "10:05:03",
    color: "#F59E0B",
  },
  {
    role: "agent",
    agentId: "3.5",
    agentName: "Agent 3.5 → Agent 5.1",
    content: "Il mord ! Demande détails garantie. On peut ajouter 'satisfait ou remboursé 30 jours' sans impacter la marge ?",
    timestamp: "10:05:11",
    color: "#10B981",
  },
  {
    role: "agent",
    agentId: "5.1",
    agentName: "Agent 5.1 → Agent 3.5",
    content: "Taux remboursement : 2.1%. Impact marge : -3.13€/client. VALIDÉ. Lien Stripe 149€ généré avec clause remboursement : https://buy.stripe.com/girard_lyon — Expire 72h.",
    timestamp: "10:05:19",
    color: "#3B82F6",
  },
  {
    role: "agent",
    agentId: "3.5",
    agentName: "Agent 3.5 → M. Girard",
    content: "Si dans 30 jours vous n'êtes pas satisfait : remboursement intégral sans question. Voici le lien sécurisé → https://buy.stripe.com/girard_lyon — Notre équipe commence dans l'heure après paiement.",
    timestamp: "10:05:35",
    color: "#10B981",
  },
  {
    role: "prospect",
    agentId: "prospect",
    agentName: "M. Girard",
    content: "OK, je fais confiance. C'est payé ! J'ai la confirmation par email.",
    timestamp: "10:06:47",
    color: "#F59E0B",
  },
  {
    role: "system",
    agentId: "5.1",
    agentName: "Agent 5.1 — BROADCAST",
    content: "✅ PAIEMENT CONFIRMÉ — Girard / Lyon / 149€ | → Division 4 débloquée | → Revenue +149€ | Durée cycle : 3min 35sec",
    timestamp: "10:06:51",
    color: "#EF4444",
  },
];
