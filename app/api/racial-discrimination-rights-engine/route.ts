import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) console.warn("[racial-discrimination-rights-engine] SWARM_API_URL not set");

const MOCK = {
  agent: "Racial Discrimination Rights Engine Agent",
  domain: "racial_discrimination_rights",
  total_entities: 8,
  avg_composite: 60.98,
  confidence_score: 0.88,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  critical_alerts: [
    "Myanmar: systemic_racism",
    "Israël/Palestine: institutional_discrimination",
    "USA: police_brutality",
    "Brésil: police_brutality",
  ],
  data_sources: [
    "un_cerd_reports_2024",
    "amnesty_apartheid_report_2022",
    "hrw_racial_discrimination_2024",
    "unodc_criminal_justice_race",
  ],
  entities: [
    { id: "RDR-001", name: "Myanmar — Génocide Rohingya, Apartheid de Facto", country: "Myanmar", composite_score: 95.55, risk_level: "critique", primary_pattern: "systemic_racism", estimated_racial_discrimination_rights_index: 9.56 },
    { id: "RDR-002", name: "Israël/Palestine — Apartheid Documenté Amnesty International", country: "Israël/Palestine", composite_score: 89.45, risk_level: "critique", primary_pattern: "institutional_discrimination", estimated_racial_discrimination_rights_index: 8.95 },
    { id: "RDR-003", name: "USA — Racisme Systémique, Incarcération Masse Noire", country: "États-Unis", composite_score: 81.70, risk_level: "critique", primary_pattern: "police_brutality", estimated_racial_discrimination_rights_index: 8.17 },
    { id: "RDR-004", name: "Brésil — Violence Policière Contre Noirs, Favelas Militarisées", country: "Brésil", composite_score: 77.20, risk_level: "critique", primary_pattern: "police_brutality", estimated_racial_discrimination_rights_index: 7.72 },
    { id: "RDR-005", name: "France — Discrimination Banlieues, Violences Policières Racisés", country: "France", composite_score: 55.20, risk_level: "élevé", primary_pattern: "police_brutality", estimated_racial_discrimination_rights_index: 5.52 },
    { id: "RDR-006", name: "UK — Windrush Scandal, Discrimination Institutionnelle", country: "Royaume-Uni", composite_score: 47.10, risk_level: "élevé", primary_pattern: "economic_racial_exclusion", estimated_racial_discrimination_rights_index: 4.71 },
    { id: "RDR-007", name: "Afrique du Sud — Transformation Post-Apartheid Inégale", country: "Afrique du Sud", composite_score: 31.10, risk_level: "modéré", primary_pattern: "economic_racial_exclusion", estimated_racial_discrimination_rights_index: 3.11 },
    { id: "RDR-008", name: "Nouvelle-Zélande — Te Tiriti Meilleure Pratique Droits Maoris", country: "Nouvelle-Zélande", composite_score: 10.55, risk_level: "faible", primary_pattern: "systemic_racism", estimated_racial_discrimination_rights_index: 1.06 },
  ],
};

export async function GET() {
  try {
    const upstream = await fetch(`${SWARM_API_URL}/racial-discrimination-rights-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse({ error: "upstream_unavailable" }), { status: 502 });
  }
}
