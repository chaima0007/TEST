import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Housing Forced Eviction Rights Engine Agent",
  domain: "housing_forced_eviction_rights",
  total_entities: 8,
  avg_composite: 57.34,
  confidence_score: 0.88,
  avg_estimated_housing_forced_eviction_rights_index: 5.73,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "un_sr_adequate_housing_reports_2023",
    "habitat_international_coalition_2023",
    "human_rights_watch_forced_evictions_2022",
    "unhcr_internal_displacement_monitor_2023",
  ],
  critical_alerts: [],
  entities: [
    { entity_id: "ZW", name: "Zimbabwe", composite_score: 85.55, risk_level: "critique", estimated_housing_forced_eviction_rights_index: 8.55 },
    { entity_id: "KH", name: "Cambodge", composite_score: 79.3, risk_level: "critique", estimated_housing_forced_eviction_rights_index: 7.93 },
    { entity_id: "ET", name: "Éthiopie (déplacés internes)", composite_score: 77.55, risk_level: "critique", estimated_housing_forced_eviction_rights_index: 7.75 },
    { entity_id: "KE", name: "Kenya (bidonvilles)", composite_score: 72.75, risk_level: "critique", estimated_housing_forced_eviction_rights_index: 7.28 },
    { entity_id: "BR", name: "Brésil (favelas)", composite_score: 52.7, risk_level: "élevé", estimated_housing_forced_eviction_rights_index: 5.27 },
    { entity_id: "IN", name: "Inde (démolitions urbaines)", composite_score: 49.35, risk_level: "élevé", estimated_housing_forced_eviction_rights_index: 4.93 },
    { entity_id: "US", name: "États-Unis (sans-abri urbains)", composite_score: 32.95, risk_level: "modéré", estimated_housing_forced_eviction_rights_index: 3.29 },
    { entity_id: "SE", name: "Suède (modèle logement social)", composite_score: 8.55, risk_level: "faible", estimated_housing_forced_eviction_rights_index: 0.86 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[housing-forced-eviction-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/housing-forced-eviction-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
