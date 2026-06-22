import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[saas-advertising-child-labor-rights] SWARM_API_URL non défini — mode dégradé activé");
}

export async function GET() {
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/saas_advertising_child_labor_rights`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      entities: [
        { name: "Salesforce", composite_score: 95.20, risk_level: "critique", estimated_index: 9.52 },
        { name: "HubSpot", composite_score: 89.45, risk_level: "critique", estimated_index: 8.95 },
        { name: "Slack", composite_score: 81.95, risk_level: "critique", estimated_index: 8.20 },
        { name: "Zoom", composite_score: 76.95, risk_level: "critique", estimated_index: 7.70 },
        { name: "Adobe", composite_score: 57.95, risk_level: "élevé", estimated_index: 5.80 },
        { name: "SAP", composite_score: 47.95, risk_level: "élevé", estimated_index: 4.80 },
        { name: "Oracle", composite_score: 28.95, risk_level: "modéré", estimated_index: 2.90 },
        { name: "ServiceNow", composite_score: 10.00, risk_level: "faible", estimated_index: 1.00 },
      ],
      avg_composite: 61.02,
      generatedAt: new Date().toISOString(),
      mode: "fallback",
    }, { status: 502 }));
  }
}
