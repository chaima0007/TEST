import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[land-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Land Rights Engine Agent",
  domain: "land_rights",
  total_entities: 8,
  avg_composite: 59.5,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { indigenous_territorial_dispossession: 3, forced_eviction_scale: 1, agroindustry_land_grab: 2, legal_remedy_access_failure: 2 },
  top_risk_entities: [
    "Brésil/Amazonie — Déforestation Terres Autochtones, Garimpeiros & Assassinats Défenseurs Fonciers",
    "Cambodge — Concessions Économiques ELC, Expulsions Forcées Villages & Impunité Investisseurs",
    "Éthiopie — Expulsions Oromia/Gambela, Investisseurs Étrangers Terres & Déplacés Internes",
  ],
  critical_alerts: [
    "Brésil/Amazonie: indigenous_territorial_dispossession",
    "Cambodge: forced_eviction_scale",
    "Éthiopie: agroindustry_land_grab",
    "Philippines: indigenous_territorial_dispossession",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_land_rights_index: 5.95,
  data_sources: [
    "global_witness_land_defenders_killings_annual_report",
    "land_matrix_initiative_global_land_deal_database",
    "fao_voluntary_guidelines_responsible_governance_tenure_implementation_report",
  ],
  entities: [
    { id: "LR-001", name: "Brésil/Amazonie — Déforestation Terres Autochtones, Garimpeiros & Assassinats Défenseurs Fonciers", country: "Amérique Latine", composite_score: 91.45, forced_eviction_scale_score: 92.0, indigenous_territorial_dispossession_score: 95.0, agroindustry_land_grab_score: 90.0, legal_remedy_access_failure_score: 88.0, risk_level: "critique", primary_pattern: "indigenous_territorial_dispossession", estimated_land_rights_index: 9.15, last_updated: "2026-06-20" },
    { id: "LR-002", name: "Cambodge — Concessions Économiques ELC, Expulsions Forcées Villages & Impunité Investisseurs", country: "Asie du Sud-Est", composite_score: 86.65, forced_eviction_scale_score: 88.0, indigenous_territorial_dispossession_score: 85.0, agroindustry_land_grab_score: 88.0, legal_remedy_access_failure_score: 85.0, risk_level: "critique", primary_pattern: "forced_eviction_scale", estimated_land_rights_index: 8.67, last_updated: "2026-06-20" },
    { id: "LR-003", name: "Éthiopie — Expulsions Oromia/Gambela, Investisseurs Étrangers Terres & Déplacés Internes", country: "Afrique de l'Est", composite_score: 83.65, forced_eviction_scale_score: 85.0, indigenous_territorial_dispossession_score: 82.0, agroindustry_land_grab_score: 85.0, legal_remedy_access_failure_score: 82.0, risk_level: "critique", primary_pattern: "agroindustry_land_grab", estimated_land_rights_index: 8.37, last_updated: "2026-06-20" },
    { id: "LR-004", name: "Philippines — Conflits Ancestral Domain Mindanao, Militarisation Terres Autochtones & NPA", country: "Asie du Sud-Est", composite_score: 80.0, forced_eviction_scale_score: 80.0, indigenous_territorial_dispossession_score: 82.0, agroindustry_land_grab_score: 78.0, legal_remedy_access_failure_score: 80.0, risk_level: "critique", primary_pattern: "indigenous_territorial_dispossession", estimated_land_rights_index: 8.0, last_updated: "2026-06-20" },
    { id: "LR-005", name: "Colombie — Restitution Terres Loi 1448, Paramilitaires & Retards Justice Post-Conflit", country: "Amérique Latine", composite_score: 53.45, forced_eviction_scale_score: 52.0, indigenous_territorial_dispossession_score: 55.0, agroindustry_land_grab_score: 50.0, legal_remedy_access_failure_score: 58.0, risk_level: "élevé", primary_pattern: "legal_remedy_access_failure", estimated_land_rights_index: 5.35, last_updated: "2026-06-20" },
    { id: "LR-006", name: "Kenya — Expulsions Maasai Loliondo, Tourisme Safari & Accès Terres Ancestrales Bloqué", country: "Afrique de l'Est", composite_score: 50.55, forced_eviction_scale_score: 48.0, indigenous_territorial_dispossession_score: 55.0, agroindustry_land_grab_score: 48.0, legal_remedy_access_failure_score: 52.0, risk_level: "élevé", primary_pattern: "indigenous_territorial_dispossession", estimated_land_rights_index: 5.06, last_updated: "2026-06-20" },
    { id: "LR-007", name: "Land Watch/FIAN — Rapport Accaparement Terres, Directives Volontaires FAO & Réformes Foncières", country: "Global", composite_score: 25.85, forced_eviction_scale_score: 22.0, indigenous_territorial_dispossession_score: 25.0, agroindustry_land_grab_score: 28.0, legal_remedy_access_failure_score: 30.0, risk_level: "modéré", primary_pattern: "agroindustry_land_grab", estimated_land_rights_index: 2.59, last_updated: "2026-06-20" },
    { id: "LR-008", name: "ONU/CESCR — Droit Logement Adéquat, Directives Expulsions & Rapporteur Spécial Logement", country: "Global", composite_score: 4.4, forced_eviction_scale_score: 4.0, indigenous_territorial_dispossession_score: 5.0, agroindustry_land_grab_score: 3.0, legal_remedy_access_failure_score: 6.0, risk_level: "faible", primary_pattern: "legal_remedy_access_failure", estimated_land_rights_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/land-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
