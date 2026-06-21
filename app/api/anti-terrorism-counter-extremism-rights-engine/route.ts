import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Anti-Terrorism Counter-Extremism Rights Engine Agent",
  domain: "anti_terrorism_counter_extremism_rights",
  total_entities: 8,
  avg_composite: 58.98,
  confidence_score: 0.88,
  avg_estimated_anti_terrorism_counter_extremism_rights_index: 5.9,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_sr_human_rights_counter_terrorism_2023",
    "amnesty_international_antiterrorism_laws_2022",
    "human_rights_watch_security_laws_2023",
    "civil_liberties_union_europe_surveillance_2023",
  ],
  critical_alerts: [],
  entities: [
    { entity_id: "CHN_xinjiang", name: "Chine — Sécurité Xinjiang", composite_score: 90.3, risk_level: "critique", estimated_anti_terrorism_counter_extremism_rights_index: 9.03 },
    { entity_id: "EGY_law94_2015", name: "Égypte — Loi antiterroriste 94/2015", composite_score: 81.15, risk_level: "critique", estimated_anti_terrorism_counter_extremism_rights_index: 8.12 },
    { entity_id: "RUS_yarovaya", name: "Russie — Loi Yarovaya", composite_score: 81.35, risk_level: "critique", estimated_anti_terrorism_counter_extremism_rights_index: 8.13 },
    { entity_id: "SAU_antiterrorism", name: "Arabie Saoudite — Lois antiterrorisme", composite_score: 78.9, risk_level: "critique", estimated_anti_terrorism_counter_extremism_rights_index: 7.89 },
    { entity_id: "TUR_post2016", name: "Turquie — Législation post-coup 2016", composite_score: 53.35, risk_level: "élevé", estimated_anti_terrorism_counter_extremism_rights_index: 5.33 },
    { entity_id: "PAK_anti_terror", name: "Pakistan — Lois antiterroristes", composite_score: 47.0, risk_level: "élevé", estimated_anti_terrorism_counter_extremism_rights_index: 4.7 },
    { entity_id: "FRA_silt_renseignement", name: "France — SILT / Renseignement", composite_score: 28.15, risk_level: "modéré", estimated_anti_terrorism_counter_extremism_rights_index: 2.81 },
    { entity_id: "CAN_oversight_model", name: "Canada — Modèle de surveillance antiterroriste", composite_score: 11.6, risk_level: "faible", estimated_anti_terrorism_counter_extremism_rights_index: 1.16 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[anti-terrorism-counter-extremism-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/anti-terrorism-counter-extremism-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
