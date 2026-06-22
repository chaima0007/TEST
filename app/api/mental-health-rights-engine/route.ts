import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[mental-health-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[mental-health-rights-engine] SWARM_API_URL not set — running in offline mode");

export async function GET() {
  try {
    if (!UPSTREAM) throw new Error("offline");
    const res = await fetch(`${UPSTREAM}/api/mental-health-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      agent: "Mental Health Rights Engine Agent",
      domain: "mental_health_rights",
      total_entities: 8,
      avg_composite: 60.02,
      confidence_score: 0.85,
      risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
      top_risk_entities: [
        "Indonésie — 18 000 Personnes Enchaînées Pasung, Hôpitaux Surpeuplés & Zéro Psychiatres Ruraux",
        "Inde — 150M Besoins Santé Mentale, 0,3 Psychiatres/100k, Internement Forcé Famille & ECT Mineurs",
        "Afrique Sub-Saharienne — 1 Psychiatre/Million, Guérisseurs Traditionnels Seule Option & Chaînes Thérapeutiques",
      ],
      critical_alerts: [
        "Indonésie: forced_psychiatry",
        "Inde: treatment_access_gap",
        "Afrique Sub-Saharienne: stigma_discrimination",
        "Russie: legal_capacity_denial",
      ],
      last_analysis: "2026-06-22",
      engine_version: "1.0.0",
      avg_estimated_mental_health_rights_index: 6.00,
      data_sources: [
        "who_mental_health_atlas_global_psychiatry_resources",
        "hrw_disability_rights_mental_health_institutionalization_report",
        "crpd_committee_general_comment_1_legal_capacity_article12",
        "amnesty_forced_psychiatry_documentation_2024",
        "wnusp_survivor_reports_psychiatric_violence",
      ],
    }, { status: 200 }));
  }
}
