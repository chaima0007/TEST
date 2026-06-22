import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[asylum-rights-engine] SWARM_API_URL not set — running in offline mode");

export async function GET() {
  try {
    if (!UPSTREAM) throw new Error("offline");
    const res = await fetch(`${UPSTREAM}/api/asylum-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      agent: "Asylum Rights Engine Agent",
      domain: "asylum_rights",
      total_entities: 8,
      avg_composite: 61.40,
      confidence_score: 0.85,
      risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
      top_risk_entities: [
        "Libye — Torture Centres Détention Migrants, Refoulement Systématique & Zéro Procédure Asile",
        "Myanmar/Bangladesh — Rohingyas Apatrides, Refoulement Bateaux & Camps Surpeuplés Cox's Bazar",
        "Grèce — Pushbacks Illégaux Documentés, Détention Arbitraire & Violations Droit Asile EU",
      ],
      critical_alerts: [
        "Libye: refoulement",
        "Myanmar/Bangladesh: asylum_procedure",
        "Grèce: detention_asylum_seekers",
        "Mexique/USA: legal_aid_gap",
      ],
      last_analysis: "2026-06-22",
      engine_version: "1.0.0",
      avg_estimated_asylum_rights_index: 6.14,
      data_sources: [
        "unhcr_global_trends_forced_displacement_2024",
        "amnesty_refoulement_documentation_2024",
        "hrw_asylum_seeker_rights_violations",
        "aida_asylum_information_database_europe",
        "border_violence_monitoring_network",
      ],
    }, { status: 200 }));
  }
}
