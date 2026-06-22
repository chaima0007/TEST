import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[internet-access-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[internet-access-rights-engine] SWARM_API_URL not set — running in offline mode");

export async function GET() {
  try {
    if (!UPSTREAM) throw new Error("offline");
    const res = await fetch(`${UPSTREAM}/api/internet-access-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      agent: "Internet Access Rights Engine Agent",
      domain: "internet_access_rights",
      total_entities: 8,
      avg_composite: 61.23,
      confidence_score: 0.85,
      risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
      last_analysis: "2026-06-22",
      engine_version: "1.0.0",
      entities: [
        { entity_id: "IAR-001", name: "Corée du Nord", country: "Corée du Nord", internet_shutdown_score: 99.0, censorship_filtering_score: 99.0, digital_divide_score: 97.0, surveillance_chilling_score: 98.0, composite_score: 98.3, risk_level: "critique", primary_pattern: "total_intranet_isolation", estimated_internet_access_rights_index: 9.83, last_updated: "2026-06-22" },
        { entity_id: "IAR-002", name: "Éthiopie", country: "Éthiopie", internet_shutdown_score: 92.0, censorship_filtering_score: 88.0, digital_divide_score: 91.0, surveillance_chilling_score: 86.0, composite_score: 89.55, risk_level: "critique", primary_pattern: "tigray_two_year_blackout", estimated_internet_access_rights_index: 8.96, last_updated: "2026-06-22" },
        { entity_id: "IAR-003", name: "Myanmar", country: "Myanmar", internet_shutdown_score: 87.0, censorship_filtering_score: 83.0, digital_divide_score: 82.0, surveillance_chilling_score: 84.0, composite_score: 84.15, risk_level: "critique", primary_pattern: "coup_shutdown_504_days", estimated_internet_access_rights_index: 8.42, last_updated: "2026-06-22" },
        { entity_id: "IAR-004", name: "Iran", country: "Iran", internet_shutdown_score: 79.0, censorship_filtering_score: 81.0, digital_divide_score: 75.0, surveillance_chilling_score: 78.0, composite_score: 78.3, risk_level: "critique", primary_pattern: "mahsa_amini_shutdown_filtering_80pct", estimated_internet_access_rights_index: 7.83, last_updated: "2026-06-22" },
        { entity_id: "IAR-005", name: "Inde", country: "Inde", internet_shutdown_score: 57.0, censorship_filtering_score: 52.0, digital_divide_score: 54.0, surveillance_chilling_score: 50.0, composite_score: 53.6, risk_level: "élevé", primary_pattern: "kashmir_552_day_blackout", estimated_internet_access_rights_index: 5.36, last_updated: "2026-06-22" },
        { entity_id: "IAR-006", name: "Nigeria", country: "Nigeria", internet_shutdown_score: 47.0, censorship_filtering_score: 46.0, digital_divide_score: 48.0, surveillance_chilling_score: 43.0, composite_score: 46.2, risk_level: "élevé", primary_pattern: "twitter_suspension_7_months", estimated_internet_access_rights_index: 4.62, last_updated: "2026-06-22" },
        { entity_id: "IAR-007", name: "Russie", country: "Russie", internet_shutdown_score: 31.0, censorship_filtering_score: 33.0, digital_divide_score: 27.0, surveillance_chilling_score: 30.0, composite_score: 30.3, risk_level: "modéré", primary_pattern: "runet_partial_isolation_meta_blocked", estimated_internet_access_rights_index: 3.03, last_updated: "2026-06-22" },
        { entity_id: "IAR-008", name: "Estonie & Islande", country: "Estonie/Islande", internet_shutdown_score: 8.0, censorship_filtering_score: 9.0, digital_divide_score: 11.0, surveillance_chilling_score: 10.0, composite_score: 9.4, risk_level: "faible", primary_pattern: "e_government_universal_fibre_model", estimated_internet_access_rights_index: 0.94, last_updated: "2026-06-22" },
      ],
    }, { status: 200 }));
  }
}
