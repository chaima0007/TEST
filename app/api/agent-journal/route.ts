import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[agent-journal] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/journal`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    const now = new Date();
    const entries = [
      { id: "EVT-001", timestamp: new Date(now.getTime() - 120000).toISOString(), eventType: "SCAN_STARTED", agentId: "influencer-marketing-agency", message: "Analyse démarrée" },
      { id: "EVT-002", timestamp: new Date(now.getTime() - 90000).toISOString(), eventType: "SCORE_COMPUTED", agentId: "influencer-marketing-agency", entityId: "INF-001", score: 96, riskLevel: "critique", message: "Score critique détecté" },
      { id: "EVT-003", timestamp: new Date(now.getTime() - 60000).toISOString(), eventType: "THRESHOLD_BREACH", agentId: "influencer-marketing-agency", entityId: "INF-001", score: 96, message: "⚠ Seuil critique dépassé (96 ≥ 60)" },
      { id: "EVT-004", timestamp: new Date(now.getTime() - 45000).toISOString(), eventType: "ALERT_TRIGGERED", agentId: "influencer-marketing-agency", entityId: "INF-001", score: 96, message: "🔴 Alerte déclenchée" },
      { id: "EVT-005", timestamp: new Date(now.getTime() - 5000).toISOString(), eventType: "REVALIDATION", agentId: "influencer-marketing-agency", message: "Revalidation ISR planifiée — 30 s" },
    ];
    return sealResponse(NextResponse.json({ entries, total: entries.length, mode: "fallback", generatedAt: now.toISOString() }));
  }
}
