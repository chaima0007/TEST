import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[migration-asylum-seekers-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Migration Asylum Seekers Rights Engine Agent",
  domain: "migration_asylum_seekers_rights",
  total_entities: 8,
  avg_composite: 61.81,
  confidence_score: 0.87,
  risk_distribution: { "critique": 4, "élevé": 2, "modéré": 1, "faible": 1 },
  pattern_distribution: { "asylum_detention_pushback_severity": 4, "family_separation_unaccompanied_minors": 1, "refugee_determination_unfair_process_scale": 2, "statelessness_documentation_access_deficit_gap": 1 },
  top_risk_entities: ["Libye/Centres Détention Torture Migrants — Esclavage Documenté CNN 2017, Torture Rançonnage & Retours Forcés UE-Garde Côtes Libyenne", "UE/Grèce Pushbacks Mer Égée Morts — 27 000 Refoulements Documentés ECRE, Noyades Frontex Complicité & Violence Frontières Systémique", "USA/Politique Tolérance Zéro Séparation Familles — 5 500 Enfants Séparés Parents 2018, Cages Détention & Rétention ICE Conditions Dégradantes"],
  critical_alerts: ["Libye/Centres Détention Torture Migrants: asylum_detention_pushback_severity", "UE/Grèce Pushbacks Mer Égée Morts: asylum_detention_pushback_severity", "USA/Politique Tolérance Zéro Séparation Familles: family_separation_unaccompanied_minors", "Australie/Détention Offshore Manus Nauru: refugee_determination_unfair_process_scale"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_migration_asylum_seekers_rights_index: 6.18,
  data_sources: ["unhcr_global_trends_forced_displacement", "amnesty_international_asylum_seekers_report", "bordermonitoring_pushback_documentation"],
  entities: [
    {
      id: "MAS-001",
      name: "UE/Grèce Pushbacks Mer Égée Morts — 27 000 Refoulements Documentés ECRE, Noyades Frontex Complicité & Violence Frontières Systémique",
      country: "UE/Grèce",
      asylum_detention_pushback_severity_score: 94.0,
      refugee_determination_unfair_process_scale_score: 90.0,
      family_separation_unaccompanied_minors_score: 88.0,
      statelessness_documentation_access_deficit_gap_score: 86.0,
      composite_score: 89.9,
      risk_level: "critique",
      primary_pattern: "asylum_detention_pushback_severity",
      estimated_migration_asylum_seekers_rights_index: 8.99,
      last_updated: "2026-06-21",
    },
    {
      id: "MAS-002",
      name: "Libye/Centres Détention Torture Migrants — Esclavage Documenté CNN 2017, Torture Rançonnage & Retours Forcés UE-Garde Côtes Libyenne",
      country: "Libye",
      asylum_detention_pushback_severity_score: 93.0,
      refugee_determination_unfair_process_scale_score: 91.0,
      family_separation_unaccompanied_minors_score: 90.0,
      statelessness_documentation_access_deficit_gap_score: 89.0,
      composite_score: 90.95,
      risk_level: "critique",
      primary_pattern: "asylum_detention_pushback_severity",
      estimated_migration_asylum_seekers_rights_index: 9.09,
      last_updated: "2026-06-21",
    },
    {
      id: "MAS-003",
      name: "USA/Politique Tolérance Zéro Séparation Familles — 5 500 Enfants Séparés Parents 2018, Cages Détention & Rétention ICE Conditions Dégradantes",
      country: "USA",
      asylum_detention_pushback_severity_score: 89.0,
      refugee_determination_unfair_process_scale_score: 87.0,
      family_separation_unaccompanied_minors_score: 93.0,
      statelessness_documentation_access_deficit_gap_score: 84.0,
      composite_score: 88.5,
      risk_level: "critique",
      primary_pattern: "family_separation_unaccompanied_minors",
      estimated_migration_asylum_seekers_rights_index: 8.85,
      last_updated: "2026-06-21",
    },
    {
      id: "MAS-004",
      name: "Australie/Détention Offshore Manus Nauru — 12 Ans Détention Indéfinie, Suicides Documentés, Interdiction Réinstallation & Pacific Solution",
      country: "Australie",
      asylum_detention_pushback_severity_score: 87.0,
      refugee_determination_unfair_process_scale_score: 86.0,
      family_separation_unaccompanied_minors_score: 82.0,
      statelessness_documentation_access_deficit_gap_score: 85.0,
      composite_score: 85.1,
      risk_level: "critique",
      primary_pattern: "refugee_determination_unfair_process_scale",
      estimated_migration_asylum_seekers_rights_index: 8.51,
      last_updated: "2026-06-21",
    },
    {
      id: "MAS-005",
      name: "Biélorussie/Instrumentalisation Migrants Frontière Pologne — Arme Hybride Migration 2021, Migrants Piégés Forêts & Refoulements Violents Pologne",
      country: "Biélorussie",
      asylum_detention_pushback_severity_score: 57.0,
      refugee_determination_unfair_process_scale_score: 55.0,
      family_separation_unaccompanied_minors_score: 54.0,
      statelessness_documentation_access_deficit_gap_score: 56.0,
      composite_score: 55.55,
      risk_level: "élevé",
      primary_pattern: "asylum_detention_pushback_severity",
      estimated_migration_asylum_seekers_rights_index: 5.55,
      last_updated: "2026-06-21",
    },
    {
      id: "MAS-006",
      name: "Tunisie/Refoulements Désert Migrants Sub-Sahariens — Abandon Désert Documenté HRW, Violences Racistes & Complicité Tacite Accord UE-Tunisie",
      country: "Tunisie",
      asylum_detention_pushback_severity_score: 54.0,
      refugee_determination_unfair_process_scale_score: 52.0,
      family_separation_unaccompanied_minors_score: 50.0,
      statelessness_documentation_access_deficit_gap_score: 53.0,
      composite_score: 52.3,
      risk_level: "élevé",
      primary_pattern: "asylum_detention_pushback_severity",
      estimated_migration_asylum_seekers_rights_index: 5.23,
      last_updated: "2026-06-21",
    },
    {
      id: "MAS-007",
      name: "UNHCR/IOM Normes Protection Demandeurs Asile — Standards Détermination Statut Réfugié, Assistance Humanitaire & Plaidoyer Non-Refoulement",
      country: "Global",
      asylum_detention_pushback_severity_score: 28.0,
      refugee_determination_unfair_process_scale_score: 27.0,
      family_separation_unaccompanied_minors_score: 26.0,
      statelessness_documentation_access_deficit_gap_score: 25.0,
      composite_score: 26.65,
      risk_level: "modéré",
      primary_pattern: "refugee_determination_unfair_process_scale",
      estimated_migration_asylum_seekers_rights_index: 2.66,
      last_updated: "2026-06-21",
    },
    {
      id: "MAS-008",
      name: "ONU/Convention Réfugiés 1951 & Protocole 1967 — Droit Asile International, Non-Refoulement Principe & Cadre Normatif Protection Globale",
      country: "Global",
      asylum_detention_pushback_severity_score: 6.0,
      refugee_determination_unfair_process_scale_score: 5.0,
      family_separation_unaccompanied_minors_score: 5.0,
      statelessness_documentation_access_deficit_gap_score: 6.0,
      composite_score: 5.5,
      risk_level: "faible",
      primary_pattern: "statelessness_documentation_access_deficit_gap",
      estimated_migration_asylum_seekers_rights_index: 0.55,
      last_updated: "2026-06-21",
    }
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/migration-asylum-seekers-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
