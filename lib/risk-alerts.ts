export type AlertSeverity = "CRITIQUE" | "ÉLEVÉ" | "MODÉRÉ" | "INFO";
export type AlertStatus = "ACTIF" | "ACQUITTÉ" | "RÉSOLU";

export interface RiskAlert {
  id: string;
  severity: AlertSeverity;
  status: AlertStatus;
  agentId: string;
  domain: string;
  entityId: string;
  score: number;
  threshold: number;
  message: string;
  triggeredAt: string;
  resolvedAt?: string;
  actions: string[];
}

export const THRESHOLDS = {
  CRITIQUE: 60,
  ÉLEVÉ: 40,
  MODÉRÉ: 20,
} as const;

export const ALERT_COLOR: Record<AlertSeverity, string> = {
  CRITIQUE: "#dc2626",
  ÉLEVÉ: "#ea580c",
  MODÉRÉ: "#d97706",
  INFO: "#6366f1",
};

export const ALERT_BG: Record<AlertSeverity, string> = {
  CRITIQUE: "#fef2f2",
  ÉLEVÉ: "#fff7ed",
  MODÉRÉ: "#fffbeb",
  INFO: "#eef2ff",
};

function makeId(): string {
  return "ALT-" + Math.random().toString(36).slice(2, 8).toUpperCase();
}

function severityFromScore(score: number): AlertSeverity {
  if (score >= THRESHOLDS.CRITIQUE) return "CRITIQUE";
  if (score >= THRESHOLDS.ÉLEVÉ) return "ÉLEVÉ";
  if (score >= THRESHOLDS.MODÉRÉ) return "MODÉRÉ";
  return "INFO";
}

const CORRECTIVE_ACTIONS: Record<AlertSeverity, string[]> = {
  CRITIQUE: [
    "Audit de conformité CSDDD immédiat",
    "Suspension des contrats fournisseurs concernés",
    "Notification aux autorités compétentes",
    "Plan de remédiation sous 30 jours",
  ],
  ÉLEVÉ: [
    "Révision du plan de vigilance",
    "Demande de justificatifs aux partenaires",
    "Mise en place d'un suivi mensuel",
  ],
  MODÉRÉ: [
    "Surveillance trimestrielle renforcée",
    "Formation équipes achats & conformité",
  ],
  INFO: ["Documenter et archiver"],
};

export function generateAlerts(
  agentId: string,
  domain: string,
  entities: Array<{ entity: string; composite_score: number; risk_level: string }>
): RiskAlert[] {
  const now = new Date();
  return entities
    .filter(e => e.composite_score >= THRESHOLDS.MODÉRÉ)
    .map(e => {
      const severity = severityFromScore(e.composite_score);
      return {
        id: makeId(),
        severity,
        status: severity === "CRITIQUE" ? "ACTIF" : "ACQUITTÉ",
        agentId,
        domain,
        entityId: e.entity,
        score: e.composite_score,
        threshold: THRESHOLDS[severity] ?? THRESHOLDS.MODÉRÉ,
        message: `Entité ${e.entity} — score ${e.composite_score} dépasse le seuil ${severity.toLowerCase()} (${THRESHOLDS[severity] ?? THRESHOLDS.MODÉRÉ})`,
        triggeredAt: new Date(now.getTime() - Math.random() * 3600000).toISOString(),
        actions: CORRECTIVE_ACTIONS[severity],
      };
    });
}
