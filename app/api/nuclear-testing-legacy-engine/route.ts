import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[nuclear-testing-legacy-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Nuclear Testing Legacy Engine Agent",
  domain: "nuclear_testing_legacy",
  total_entities: 8,
  avg_composite: 59.23,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { radiation_contamination_scale: 2, health_cancer_mortality: 2, state_denial_reparations: 2, displaced_communities: 2 },
  top_risk_entities: [
    "Marshall Islands/USA — 67 Tests Bikini/Enewetak, Populations Irradiées & Déni Compensation",
    "Kazakhstan/URSS — 456 Tests Semipalatinsk, 1,5M Irradiés & Cancers Générationnels",
    "Algérie/France — 17 Tests Reggane/Hamoudia, Populations Touareg Contaminées & Secret Défense",
  ],
  critical_alerts: [
    "Marshall Islands/USA: radiation_contamination_scale",
    "Kazakhstan/URSS: health_cancer_mortality",
    "Algérie/France: state_denial_reparations",
    "Polynésie/France: health_cancer_mortality",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_nuclear_testing_legacy_index: 5.92,
  data_sources: [
    "ican_nuclear_testing_humanitarian_consequences_global_report",
    "atomic_heritage_foundation_nuclear_testing_legacy_database",
    "tpnw_treaty_prohibition_nuclear_weapons_victim_assistance_article_6_7",
  ],
  entities: [
    { entity_id: "NT-001", name: "Marshall Islands/USA — 67 Tests Bikini/Enewetak, Populations Irradiées & Déni Compensation", country: "Océanie/Amérique du Nord", composite_score: 89.7, radiation_contamination_scale_score: 92.0, health_cancer_mortality_score: 90.0, displaced_communities_score: 88.0, state_denial_reparations_score: 88.0, risk_level: "critique", primary_pattern: "radiation_contamination_scale", estimated_nuclear_testing_legacy_index: 8.97, last_updated: "2026-06-20" },
    { entity_id: "NT-002", name: "Kazakhstan/URSS — 456 Tests Semipalatinsk, 1,5M Irradiés & Cancers Générationnels", country: "Asie Centrale", composite_score: 85.15, radiation_contamination_scale_score: 88.0, health_cancer_mortality_score: 85.0, displaced_communities_score: 82.0, state_denial_reparations_score: 85.0, risk_level: "critique", primary_pattern: "health_cancer_mortality", estimated_nuclear_testing_legacy_index: 8.52, last_updated: "2026-06-20" },
    { entity_id: "NT-003", name: "Algérie/France — 17 Tests Reggane/Hamoudia, Populations Touareg Contaminées & Secret Défense", country: "Afrique du Nord", composite_score: 83.45, radiation_contamination_scale_score: 82.0, health_cancer_mortality_score: 80.0, displaced_communities_score: 85.0, state_denial_reparations_score: 88.0, risk_level: "critique", primary_pattern: "state_denial_reparations", estimated_nuclear_testing_legacy_index: 8.35, last_updated: "2026-06-20" },
    { entity_id: "NT-004", name: "Polynésie/France — 193 Tests Mururoa/Fangataufa, Vétérans Malades & Indemnisation Minime", country: "Océanie/France", composite_score: 80.4, radiation_contamination_scale_score: 80.0, health_cancer_mortality_score: 82.0, displaced_communities_score: 78.0, state_denial_reparations_score: 82.0, risk_level: "critique", primary_pattern: "health_cancer_mortality", estimated_nuclear_testing_legacy_index: 8.04, last_updated: "2026-06-20" },
    { entity_id: "NT-005", name: "USA/Nevada — Downwinders, Communautés Mormons Irradiées & RECA Compensation Partielle", country: "Amérique du Nord", composite_score: 53.45, radiation_contamination_scale_score: 52.0, health_cancer_mortality_score: 55.0, displaced_communities_score: 50.0, state_denial_reparations_score: 58.0, risk_level: "élevé", primary_pattern: "state_denial_reparations", estimated_nuclear_testing_legacy_index: 5.35, last_updated: "2026-06-20" },
    { entity_id: "NT-006", name: "Australie/UK — 12 Tests Maralinga, Peuple Anangu Déplacé & Décontamination Incomplète", country: "Océanie", composite_score: 51.15, radiation_contamination_scale_score: 48.0, health_cancer_mortality_score: 52.0, displaced_communities_score: 55.0, state_denial_reparations_score: 50.0, risk_level: "élevé", primary_pattern: "displaced_communities", estimated_nuclear_testing_legacy_index: 5.12, last_updated: "2026-06-20" },
    { entity_id: "NT-007", name: "TPNW/TICE — Traité Interdiction Tests, Compensation Victimes & Assainissement Sites", country: "Global", composite_score: 26.1, radiation_contamination_scale_score: 22.0, health_cancer_mortality_score: 28.0, displaced_communities_score: 30.0, state_denial_reparations_score: 25.0, risk_level: "modéré", primary_pattern: "radiation_contamination_scale", estimated_nuclear_testing_legacy_index: 2.61, last_updated: "2026-06-20" },
    { entity_id: "NT-008", name: "ONU/UNSCEAR — Comité Effets Rayonnements Ionisants, Rapports Scientifiques & Suivi", country: "Global", composite_score: 4.4, radiation_contamination_scale_score: 4.0, health_cancer_mortality_score: 5.0, displaced_communities_score: 3.0, state_denial_reparations_score: 6.0, risk_level: "faible", primary_pattern: "displaced_communities", estimated_nuclear_testing_legacy_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/nuclear-testing-legacy-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
