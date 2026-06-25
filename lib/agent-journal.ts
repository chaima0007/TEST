export type JournalEventType =
  | "SCAN_STARTED"
  | "SCORE_COMPUTED"
  | "RISK_ELEVATED"
  | "THRESHOLD_BREACH"
  | "ALERT_TRIGGERED"
  | "CERT_VERIFIED"
  | "UPSTREAM_ERROR"
  | "REVALIDATION";

export interface JournalEntry {
  id: string;
  timestamp: string;
  eventType: JournalEventType;
  agentId: string;
  entityId?: string;
  score?: number;
  riskLevel?: string;
  message: string;
  metadata?: Record<string, unknown>;
}

export interface AgentJournal {
  agentId: string;
  domain: string;
  entries: JournalEntry[];
  lastUpdated: string;
  totalScans: number;
  breachCount: number;
}

function makeId(): string {
  return Math.random().toString(36).slice(2, 10).toUpperCase();
}

export function buildJournal(
  agentId: string,
  domain: string,
  entities: Array<{ entity: string; composite_score: number; risk_level: string }>,
  avgComposite: number
): AgentJournal {
  const now = new Date();
  const entries: JournalEntry[] = [];

  entries.push({
    id: makeId(),
    timestamp: new Date(now.getTime() - 120000).toISOString(),
    eventType: "SCAN_STARTED",
    agentId,
    message: `Analyse démarrée — domaine : ${domain}`,
    metadata: { domain, totalEntities: entities.length },
  });

  for (const ent of entities) {
    entries.push({
      id: makeId(),
      timestamp: new Date(now.getTime() - 90000 + Math.random() * 60000).toISOString(),
      eventType: "SCORE_COMPUTED",
      agentId,
      entityId: ent.entity,
      score: ent.composite_score,
      riskLevel: ent.risk_level,
      message: `Score calculé : ${ent.composite_score} — risque ${ent.risk_level}`,
    });

    if (ent.composite_score >= 60) {
      entries.push({
        id: makeId(),
        timestamp: new Date(now.getTime() - 60000 + Math.random() * 30000).toISOString(),
        eventType: "THRESHOLD_BREACH",
        agentId,
        entityId: ent.entity,
        score: ent.composite_score,
        riskLevel: ent.risk_level,
        message: `⚠ Seuil critique dépassé (${ent.composite_score} ≥ 60) pour ${ent.entity}`,
        metadata: { threshold: 60, delta: +(ent.composite_score - 60).toFixed(2) },
      });

      entries.push({
        id: makeId(),
        timestamp: new Date(now.getTime() - 45000 + Math.random() * 20000).toISOString(),
        eventType: "ALERT_TRIGGERED",
        agentId,
        entityId: ent.entity,
        score: ent.composite_score,
        riskLevel: ent.risk_level,
        message: `🔴 Alerte déclenchée — action corrective requise pour ${ent.entity}`,
      });
    }
  }

  entries.push({
    id: makeId(),
    timestamp: new Date(now.getTime() - 5000).toISOString(),
    eventType: "REVALIDATION",
    agentId,
    score: avgComposite,
    message: `Revalidation ISR — prochain cycle dans 30 s`,
    metadata: { avgComposite, revalidate: 30 },
  });

  entries.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime());

  return {
    agentId,
    domain,
    entries,
    lastUpdated: now.toISOString(),
    totalScans: entities.length,
    breachCount: entries.filter(e => e.eventType === "THRESHOLD_BREACH").length,
  };
}

export const EVENT_COLOR: Record<JournalEventType, string> = {
  SCAN_STARTED: "#6366f1",
  SCORE_COMPUTED: "#0369a1",
  RISK_ELEVATED: "#ea580c",
  THRESHOLD_BREACH: "#dc2626",
  ALERT_TRIGGERED: "#b91c1c",
  CERT_VERIFIED: "#16a34a",
  UPSTREAM_ERROR: "#9f1239",
  REVALIDATION: "#6b7280",
};
