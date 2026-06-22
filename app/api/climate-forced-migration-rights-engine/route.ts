import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[climate-forced-migration-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Climate Forced Migration Rights Engine Agent",
  domain: "climate_forced_migration_rights",
  total_entities: 8,
  avg_composite: 61.61,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { climate_displacement_severity: 3, loss_damage_reparation_absence: 2, legal_protection_climate_migrants_gap: 3 },
  top_risk_entities: [
    "Bangladesh — 13M Déplacés Climatiques 2050, Cyclones & Montée Eaux, Zéro Statut Légal Clima-Migrants",
    "Pacifique/Tuvalu — Submersion Totale, COP Pertes & Dommages Insuffisant, Diaspora Sans Nationalité",
    "Sahel/Afrique Subsaharienne — Désertification 216M Déplacés 2050, Conflits Eau-Terre & Zéro Cadre Légal",
  ],
  critical_alerts: [
    "Bangladesh: climate_displacement_severity",
    "Pacifique/Tuvalu: loss_damage_reparation_absence",
    "Sahel/Afrique Subsaharienne: climate_displacement_severity",
    "Asie du Sud-Est Côtière: legal_protection_climate_migrants_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_climate_forced_migration_rights_index: 6.16,
  data_sources: [
    "unhcr_climate_change_displacement_global_trends_report",
    "world_bank_groundswell_internal_climate_migration_report",
    "ipcc_ar6_impacts_adaptation_vulnerability_chapter_migration",
  ],
  entities: [
    { id: "CFM-001", name: "Bangladesh — 13M Déplacés Climatiques 2050, Cyclones & Montée Eaux, Zéro Statut Légal Clima-Migrants", country: "Bangladesh", sector: "Déplacement Climatique Côtier", composite_score: 93.45, climate_displacement_severity_score: 96.0, legal_protection_climate_migrants_gap_score: 94.0, adaptation_finance_access_exclusion_score: 91.0, loss_damage_reparation_absence_score: 92.0, risk_level: "critique", primary_pattern: "climate_displacement_severity", estimated_climate_forced_migration_rights_index: 9.35, last_updated: "2026-06-21" },
    { id: "CFM-002", name: "Pacifique/Tuvalu — Submersion Totale, COP Pertes & Dommages Insuffisant, Diaspora Sans Nationalité", country: "Tuvalu/Pacifique", sector: "Apatridie Climatique Insulaire", composite_score: 90.65, climate_displacement_severity_score: 93.0, legal_protection_climate_migrants_gap_score: 91.0, adaptation_finance_access_exclusion_score: 88.0, loss_damage_reparation_absence_score: 90.0, risk_level: "critique", primary_pattern: "loss_damage_reparation_absence", estimated_climate_forced_migration_rights_index: 9.07, last_updated: "2026-06-21" },
    { id: "CFM-003", name: "Sahel/Afrique Subsaharienne — Désertification 216M Déplacés 2050, Conflits Eau-Terre & Zéro Cadre Légal", country: "Sahel", sector: "Migration Climatique Continentale", composite_score: 88.2, climate_displacement_severity_score: 91.0, legal_protection_climate_migrants_gap_score: 88.0, adaptation_finance_access_exclusion_score: 86.0, loss_damage_reparation_absence_score: 87.0, risk_level: "critique", primary_pattern: "climate_displacement_severity", estimated_climate_forced_migration_rights_index: 8.82, last_updated: "2026-06-21" },
    { id: "CFM-004", name: "Asie du Sud-Est Côtière — Typhons, Deltas Inondés, Zéro Cadre Légal Migration Climatique", country: "Asie du Sud-Est", sector: "Déplacement Côtier Typhons", composite_score: 85.2, climate_displacement_severity_score: 88.0, legal_protection_climate_migrants_gap_score: 85.0, adaptation_finance_access_exclusion_score: 83.0, loss_damage_reparation_absence_score: 84.0, risk_level: "critique", primary_pattern: "legal_protection_climate_migrants_gap", estimated_climate_forced_migration_rights_index: 8.52, last_updated: "2026-06-21" },
    { id: "CFM-005", name: "Amérique Centrale — Sécheresse, Migrations Nord, Politiques Frontières Répressives & Droit Mobilité Nié", country: "Amérique Centrale", sector: "Migration Climatique Régionale", composite_score: 53.65, climate_displacement_severity_score: 56.0, legal_protection_climate_migrants_gap_score: 54.0, adaptation_finance_access_exclusion_score: 51.0, loss_damage_reparation_absence_score: 53.0, risk_level: "élevé", primary_pattern: "legal_protection_climate_migrants_gap", estimated_climate_forced_migration_rights_index: 5.37, last_updated: "2026-06-21" },
    { id: "CFM-006", name: "Méditerranée/MENA — Chaleur Extrême, Conflits Eau, Migration Forcée Non Reconnue Légalement", country: "MENA", sector: "Migration Climatique MENA", composite_score: 51.2, climate_displacement_severity_score: 54.0, legal_protection_climate_migrants_gap_score: 51.0, adaptation_finance_access_exclusion_score: 49.0, loss_damage_reparation_absence_score: 50.0, risk_level: "élevé", primary_pattern: "climate_displacement_severity", estimated_climate_forced_migration_rights_index: 5.12, last_updated: "2026-06-21" },
    { id: "CFM-007", name: "UNHCR/Climate Migrants Coalition — Plaidoyer Statut Clima-Migrants, Cadre Genève Insuffisant", country: "Global", sector: "Plaidoyer International", composite_score: 26.45, climate_displacement_severity_score: 27.0, legal_protection_climate_migrants_gap_score: 25.0, adaptation_finance_access_exclusion_score: 26.0, loss_damage_reparation_absence_score: 28.0, risk_level: "modéré", primary_pattern: "legal_protection_climate_migrants_gap", estimated_climate_forced_migration_rights_index: 2.65, last_updated: "2026-06-21" },
    { id: "CFM-008", name: "ONU/IPCC — Rapports AR6, Recommandations Adaptation & Accord Paris Article 8 Pertes & Dommages", country: "Global", sector: "Cadre Normatif International", composite_score: 4.1, climate_displacement_severity_score: 5.0, legal_protection_climate_migrants_gap_score: 4.0, adaptation_finance_access_exclusion_score: 4.0, loss_damage_reparation_absence_score: 3.0, risk_level: "faible", primary_pattern: "loss_damage_reparation_absence", estimated_climate_forced_migration_rights_index: 0.41, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/climate-forced-migration-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
