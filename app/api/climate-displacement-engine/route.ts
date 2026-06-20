import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[climate-displacement-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Climate Displacement Engine Agent",
  domain: "climate_displacement",
  total_entities: 8,
  avg_composite: 59.65,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { displacement_scale: 3, state_protection_failure: 2, international_legal_gap: 2, adaptation_resource_denial: 1 },
  top_risk_entities: [
    "Bangladesh/Delta — 30M Menacés Hausse Mer, Cyclones & Déplacement Structurel",
    "Îles Pacifique/Tuvalu — Submersion Totale, 11 000 Habitants & Disparition d'une Nation",
    "Sahel/Afrique — 50M Déplacés Sécheresse, Conflits Eau & Désertification Massive",
  ],
  critical_alerts: [
    "Bangladesh/Delta: displacement_scale",
    "Îles Pacifique/Tuvalu: international_legal_gap",
    "Sahel/Afrique: state_protection_failure",
    "Syrie/Moyen-Orient: adaptation_resource_denial",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_climate_displacement_index: 5.96,
  data_sources: [
    "idmc_global_report_internal_displacement_annual",
    "unhcr_global_trends_forced_displacement_annual_report",
    "ipcc_sixth_assessment_report_impacts_adaptation_vulnerability_chapter_climate_migration",
  ],
  entities: [
    { entity_id: "CD-001", name: "Bangladesh/Delta — 30M Menacés Hausse Mer, Cyclones & Déplacement Structurel", country: "Asie du Sud", composite_score: 89.1, displacement_scale_score: 92.0, state_protection_failure_score: 88.0, international_legal_gap_score: 90.0, adaptation_resource_denial_score: 85.0, risk_level: "critique", primary_pattern: "displacement_scale", estimated_climate_displacement_index: 8.91, last_updated: "2026-06-20" },
    { entity_id: "CD-002", name: "Îles Pacifique/Tuvalu — Submersion Totale, 11 000 Habitants & Disparition d'une Nation", country: "Océanie", composite_score: 88.65, displacement_scale_score: 88.0, state_protection_failure_score: 85.0, international_legal_gap_score: 92.0, adaptation_resource_denial_score: 90.0, risk_level: "critique", primary_pattern: "international_legal_gap", estimated_climate_displacement_index: 8.87, last_updated: "2026-06-20" },
    { entity_id: "CD-003", name: "Sahel/Afrique — 50M Déplacés Sécheresse, Conflits Eau & Désertification Massive", country: "Afrique Sub-Saharienne", composite_score: 83.9, displacement_scale_score: 85.0, state_protection_failure_score: 80.0, international_legal_gap_score: 88.0, adaptation_resource_denial_score: 82.0, risk_level: "critique", primary_pattern: "state_protection_failure", estimated_climate_displacement_index: 8.39, last_updated: "2026-06-20" },
    { entity_id: "CD-004", name: "Syrie/Moyen-Orient — Sécheresse 2006-2010, Déplacement Préalable & Conflit Armé", country: "Moyen-Orient", composite_score: 75.95, displacement_scale_score: 72.0, state_protection_failure_score: 75.0, international_legal_gap_score: 80.0, adaptation_resource_denial_score: 78.0, risk_level: "critique", primary_pattern: "adaptation_resource_denial", estimated_climate_displacement_index: 7.6, last_updated: "2026-06-20" },
    { entity_id: "CD-005", name: "Inde/Orissa — 8M Déplacés Catastrophes, Communautés Côtières & Barrage Sardar", country: "Asie du Sud", composite_score: 53.85, displacement_scale_score: 52.0, state_protection_failure_score: 55.0, international_legal_gap_score: 58.0, adaptation_resource_denial_score: 50.0, risk_level: "élevé", primary_pattern: "displacement_scale", estimated_climate_displacement_index: 5.39, last_updated: "2026-06-20" },
    { entity_id: "CD-006", name: "USA/Puerto Rico — Ouragan Maria, Déplacement Non Reconnu & Inégalité Reconstruction", country: "Amérique du Nord", composite_score: 52.75, displacement_scale_score: 48.0, state_protection_failure_score: 52.0, international_legal_gap_score: 55.0, adaptation_resource_denial_score: 58.0, risk_level: "élevé", primary_pattern: "state_protection_failure", estimated_climate_displacement_index: 5.28, last_updated: "2026-06-20" },
    { entity_id: "CD-007", name: "Europe/Méditerranée — Réfugiés Climatiques Refoulés, Convention 1951 Inadaptée", country: "Europe", composite_score: 28.6, displacement_scale_score: 25.0, state_protection_failure_score: 30.0, international_legal_gap_score: 32.0, adaptation_resource_denial_score: 28.0, risk_level: "modéré", primary_pattern: "international_legal_gap", estimated_climate_displacement_index: 2.86, last_updated: "2026-06-20" },
    { entity_id: "CD-008", name: "ONU/UNHCR/IPCC — Cadre Nansen, Principes Directeurs & Vide Juridique International", country: "Global", composite_score: 4.4, displacement_scale_score: 4.0, state_protection_failure_score: 5.0, international_legal_gap_score: 3.0, adaptation_resource_denial_score: 6.0, risk_level: "faible", primary_pattern: "displacement_scale", estimated_climate_displacement_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/climate-displacement-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
