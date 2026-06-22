import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[risk-alerts] SWARM_API_URL non défini — mode dégradé activé");
}

type Severity = "CRITIQUE" | "ÉLEVÉ" | "MODÉRÉ" | "INFO";
type AlertStatus = "ACTIF" | "ACQUITTÉ" | "RÉSOLU";

interface RiskAlert {
  id: string;
  severity: Severity;
  status: AlertStatus;
  agentId: string;
  entityId: string;
  score: number;
  threshold: number;
  message: string;
  triggeredAt: string;
  actions: string[];
}

const THRESHOLDS = { CRITIQUE: 60, ÉLEVÉ: 40, MODÉRÉ: 20 } as const;
const ACTIONS: Record<Severity, string[]> = {
  CRITIQUE: ["Audit CSDDD immédiat", "Suspension contrats fournisseurs", "Notification autorités", "Plan remédiation 30 j"],
  ÉLEVÉ: ["Révision plan vigilance", "Justificatifs partenaires", "Suivi mensuel renforcé"],
  MODÉRÉ: ["Surveillance trimestrielle", "Formation équipes conformité"],
  INFO: ["Documenter et archiver"],
};

function severity(score: number): Severity {
  if (score >= 60) return "CRITIQUE";
  if (score >= 40) return "ÉLEVÉ";
  if (score >= 20) return "MODÉRÉ";
  return "INFO";
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/alerts`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    const now = new Date();
    const scores = [96, 89, 82, 76, 58, 47];
    const agents = ["influencer-marketing-agency", "content-creator-platform", "brand-ambassador-program"];
    const alerts: RiskAlert[] = [];
    for (const agent of agents) {
      scores.forEach((sc, i) => {
        if (sc < 20) return;
        const sev = severity(sc);
        alerts.push({
          id: `ALT-${Math.random().toString(36).slice(2, 8).toUpperCase()}`,
          severity: sev,
          status: sev === "CRITIQUE" ? "ACTIF" : "ACQUITTÉ",
          agentId: agent,
          entityId: `${agent.slice(0, 3).toUpperCase()}-00${i + 1}`,
          score: sc,
          threshold: THRESHOLDS[sev] ?? 20,
          message: `Score ${sc} dépasse seuil ${sev.toLowerCase()} (${THRESHOLDS[sev] ?? 20})`,
          triggeredAt: new Date(now.getTime() - i * 600000).toISOString(),
          actions: ACTIONS[sev],
        });
      });
    }
    return sealResponse(NextResponse.json({ alerts, generatedAt: now.toISOString(), mode: "fallback" }));
  }
}
