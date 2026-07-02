// Contrats partagés entre les agents du pipeline de prospection.
// L'orchestrateur enchaîne : Scout → Qualifier → Copywriter → Sequencer → Mailer.

export type ProspectStatus =
  | "new"
  | "qualified"
  | "contacted"
  | "followup"
  | "replied"
  | "won"
  | "lost"
  | "optout";

export type MessageStatus = "draft" | "scheduled" | "sent" | "failed" | "skipped";

export type AgentName =
  | "orchestrator"
  | "scout"
  | "qualifier"
  | "copywriter"
  | "sequencer"
  | "mailer";

// Entreprise détectée sans site internet, avant insertion en base
export interface DiscoveredBusiness {
  name: string;
  category: string;
  city: string;
  address?: string;
  phone?: string;
  email?: string;
  googlePlaceId?: string;
  rating?: number;
  reviewCount?: number;
  source: "places" | "csv" | "manual";
}

export interface ScoutParams {
  // ex: "plombier", "restaurant", "coiffeur"
  categories: string[];
  // ex: "Lyon", "Bordeaux"
  cities: string[];
  maxPerSearch?: number;
}

export interface EmailDraft {
  step: 1 | 2 | 3 | 4;
  subject: string;
  body: string;
}

// Résumé standard retourné par chaque agent (persisté dans AgentRun.output)
export interface AgentSummary {
  agent: AgentName;
  processed: number;
  created?: number;
  skipped?: number;
  sent?: number;
  failed?: number;
  details?: string[];
}

export interface OrchestratorReport {
  startedAt: string;
  finishedAt: string;
  dryRun: boolean;
  steps: AgentSummary[];
}
