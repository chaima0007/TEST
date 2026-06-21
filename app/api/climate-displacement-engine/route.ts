import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[climate-displacement-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Climate Displacement Engine Agent",
  domain: "climate_displacement",
  total_entities: 8,
  avg_composite: 60.86,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { return_resettlement_impossibility: 2, displacement_scale_severity: 2, legal_protection_gap: 3, adaptation_finance_absence: 1 },
  top_risk_entities: [
    "Tuvalu/Kiribati — Submersion Totale Prévue 2050, 100% Population Déplacée & Souveraineté Perdue",
    "Bangladesh — 20M Déplacés Cyclones/Inondations, Deltas Submergés & Migration Urbaine Forcée",
    "Sahel/Afrique — Désertification 10M Déplacés, Conflit Eau/Terre & Aucun Statut Légal",
  ],
  critical_alerts: [
    "Tuvalu/Kiribati: return_resettlement_impossibility",
    "Bangladesh: displacement_scale_severity",
    "Sahel/Afrique: legal_protection_gap",
    "Philippines: return_resettlement_impossibility",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_climate_displacement_index: 6.09,
  data_sources: [
    "idmc_global_report_internal_displacement_annual",
    "unhcr_climate_change_displacement_legal_protection_gap_report",
    "world_bank_groundswell_climate_migration_projections_2050",
  ],
  entities: [
    { entity_id: "CD-001", name: "Tuvalu/Kiribati — Submersion Totale Prévue 2050, 100% Population Déplacée & Souveraineté Perdue", country: "Océanie", composite_score: 94.85, displacement_scale_severity_score: 95.0, legal_protection_gap_score: 95.0, adaptation_finance_absence_score: 92.0, return_resettlement_impossibility_score: 98.0, risk_level: "critique", primary_pattern: "return_resettlement_impossibility", estimated_climate_displacement_index: 9.49, last_updated: "2026-06-21" },
    { entity_id: "CD-002", name: "Bangladesh — 20M Déplacés Cyclones/Inondations, Deltas Submergés & Migration Urbaine Forcée", country: "Asie du Sud", composite_score: 89.1, displacement_scale_severity_score: 92.0, legal_protection_gap_score: 88.0, adaptation_finance_absence_score: 90.0, return_resettlement_impossibility_score: 85.0, risk_level: "critique", primary_pattern: "displacement_scale_severity", estimated_climate_displacement_index: 8.91, last_updated: "2026-06-21" },
    { entity_id: "CD-003", name: "Sahel/Afrique — Désertification 10M Déplacés, Conflit Eau/Terre & Aucun Statut Légal", country: "Afrique Sub-Saharienne", composite_score: 87.3, displacement_scale_severity_score: 88.0, legal_protection_gap_score: 90.0, adaptation_finance_absence_score: 88.0, return_resettlement_impossibility_score: 82.0, risk_level: "critique", primary_pattern: "legal_protection_gap", estimated_climate_displacement_index: 8.73, last_updated: "2026-06-21" },
    { entity_id: "CD-004", name: "Philippines — Typhons Annuels, 4M Déplacés/An & Reconstruction Zones Rouge Impossible", country: "Asie du Sud-Est", composite_score: 83.0, displacement_scale_severity_score: 85.0, legal_protection_gap_score: 80.0, adaptation_finance_absence_score: 82.0, return_resettlement_impossibility_score: 85.0, risk_level: "critique", primary_pattern: "return_resettlement_impossibility", estimated_climate_displacement_index: 8.3, last_updated: "2026-06-21" },
    { entity_id: "CD-005", name: "USA/Alaska — Villages Autochtones Érodés, Relocalisation Fédérale Lente & Cultures Perdues", country: "Amérique du Nord", composite_score: 52.95, displacement_scale_severity_score: 52.0, legal_protection_gap_score: 48.0, adaptation_finance_absence_score: 55.0, return_resettlement_impossibility_score: 58.0, risk_level: "élevé", primary_pattern: "adaptation_finance_absence", estimated_climate_displacement_index: 5.3, last_updated: "2026-06-21" },
    { entity_id: "CD-006", name: "Europe/Méditerranée — Migrations Climatiques Mélangées, Distinction Réfugiés Inexistante & Refoulements", country: "Europe", composite_score: 49.4, displacement_scale_severity_score: 48.0, legal_protection_gap_score: 55.0, adaptation_finance_absence_score: 45.0, return_resettlement_impossibility_score: 50.0, risk_level: "élevé", primary_pattern: "legal_protection_gap", estimated_climate_displacement_index: 4.94, last_updated: "2026-06-21" },
    { entity_id: "CD-007", name: "IDMC/UNHCR — Monitoring Déplacements, Plaidoyer Statut Légal & Nansen Initiative", country: "Global", composite_score: 25.85, displacement_scale_severity_score: 22.0, legal_protection_gap_score: 25.0, adaptation_finance_absence_score: 28.0, return_resettlement_impossibility_score: 30.0, risk_level: "modéré", primary_pattern: "displacement_scale_severity", estimated_climate_displacement_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "CD-008", name: "ONU/Résolution — Reconnaissance Réfugiés Climatiques, Agenda Nansen & Lacunes Convention 1951", country: "Global", composite_score: 4.4, displacement_scale_severity_score: 4.0, legal_protection_gap_score: 5.0, adaptation_finance_absence_score: 3.0, return_resettlement_impossibility_score: 6.0, risk_level: "faible", primary_pattern: "legal_protection_gap", estimated_climate_displacement_index: 0.44, last_updated: "2026-06-21" },
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
