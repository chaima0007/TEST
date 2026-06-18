// ─── Registre de la flotte d'agents — Caelum Partners ────────────────────────
//
// Source de vérité unique : tous les agents, leur rôle, leur statut premium et
// leurs capacités. Les agents premium (COMMANDANT, RÉSOLVEUR) orchestrent et
// débloquent les agents opérationnels.

export interface AgentDef {
  id: string;
  name: string;
  role: string;
  premium: boolean;
  capabilities: string[];
}

export const FLEET: AgentDef[] = [
  { id: "sentinel", name: "SENTINEL", role: "Sécurité & protection Zero-Trust", premium: false, capabilities: ["compliance", "RGPD", "anti-fraude"] },
  { id: "oracle", name: "ORACLE", role: "Analytics & intelligence", premium: false, capabilities: ["KPIs", "scoring", "rétroaction"] },
  { id: "hermes", name: "HERMES", role: "Prospection LinkedIn & vente", premium: false, capabilities: ["outreach manuel", "A/B accroches", "suivi"] },
  { id: "nexus", name: "NEXUS", role: "SEO & indexation", premium: false, capabilities: ["SEO", "sitemap", "indexation"] },
  { id: "forge", name: "FORGE", role: "Développement & déploiement", premium: false, capabilities: ["build", "déploiement", "reprise de run"] },
  { id: "echo", name: "ECHO", role: "Support client 24h/24", premium: false, capabilities: ["FAQ", "tickets", "réponses"] },
  { id: "prism", name: "PRISM", role: "Social media & viralité", premium: false, capabilities: ["contenu", "calendrier", "viralité"] },
  { id: "atlas", name: "ATLAS", role: "Veille concurrentielle", premium: false, capabilities: ["veille", "benchmark"] },
  { id: "nexagen", name: "NEXAGEN", role: "Simulation succès futur", premium: false, capabilities: ["Monte-Carlo", "projection"] },
  // Agents premium
  { id: "commandant", name: "COMMANDANT", role: "Chef d'orchestre — décide la stratégie (succès × respect × ROI)", premium: true, capabilities: ["planification", "simulation 50 scénarios", "porte de conformité", "ROI"] },
  { id: "resolveur", name: "RÉSOLVEUR", role: "Déblocage — diagnostique et corrige les frictions", premium: true, capabilities: ["diagnostic", "remédiation", "reprise", "ajustement de seuil"] },
];

export const getAgent = (id: string): AgentDef | undefined => FLEET.find((a) => a.id === id);
export const premiumAgents = (): AgentDef[] => FLEET.filter((a) => a.premium);
