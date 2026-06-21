import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[environmental-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Environmental Rights Engine Agent",
  domain: "environmental_rights",
  total_entities: 8,
  avg_composite: 61.83,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { toxic_pollution_environmental_health_severity: 2, state_corporate_environmental_impunity_gap: 1, indigenous_environmental_destruction_scale: 2, environmental_defender_criminalisation: 3 },
  top_risk_entities: [
    "Nigeria/Delta Niger — Déversements Shell 40 Ans, 11M Habitants Pollution, Cancer/Mortalité & Zéro Décontamination",
    "Inde/Bhopal Legacy — 500 000 Exposés Union Carbide 1984, Eau Contaminée Encore 2024 & Impunité Dow Chemical",
    "Amazonie/Brésil — Mercure Garimpos Peuples Yanomami, Déforestation Légalisée Bolsonaro & Défenseurs Assassinés",
  ],
  critical_alerts: [
    "Nigeria/Delta Niger: toxic_pollution_environmental_health_severity",
    "Inde/Bhopal Legacy: state_corporate_environmental_impunity_gap",
    "Amazonie/Brésil: indigenous_environmental_destruction_scale",
    "Chine/Régions Industrielles: toxic_pollution_environmental_health_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_environmental_rights_index: 6.18,
  data_sources: [
    "global_witness_defenders_environmental_rights_report",
    "unep_state_of_environment_report",
    "amnesty_international_corporate_environmental_impunity",
  ],
  entities: [
    { id: "ENR-001", name: "Nigeria/Delta Niger — Déversements Shell 40 Ans, 11M Habitants Pollution, Cancer/Mortalité & Zéro Décontamination", country: "Nigeria", composite_score: 93.6, toxic_pollution_environmental_health_severity_score: 96.0, indigenous_environmental_destruction_scale_score: 93.0, environmental_defender_criminalisation_score: 91.0, state_corporate_environmental_impunity_gap_score: 94.0, risk_level: "critique", primary_pattern: "toxic_pollution_environmental_health_severity", estimated_environmental_rights_index: 9.36, last_updated: "2026-06-21" },
    { id: "ENR-002", name: "Inde/Bhopal Legacy — 500 000 Exposés Union Carbide 1984, Eau Contaminée Encore 2024 & Impunité Dow Chemical", country: "Inde", composite_score: 90.35, toxic_pollution_environmental_health_severity_score: 93.0, indigenous_environmental_destruction_scale_score: 89.0, environmental_defender_criminalisation_score: 88.0, state_corporate_environmental_impunity_gap_score: 91.0, risk_level: "critique", primary_pattern: "state_corporate_environmental_impunity_gap", estimated_environmental_rights_index: 9.04, last_updated: "2026-06-21" },
    { id: "ENR-003", name: "Amazonie/Brésil — Mercure Garimpos Peuples Yanomami, Déforestation Légalisée Bolsonaro & Défenseurs Assassinés", country: "Brésil", composite_score: 88.45, toxic_pollution_environmental_health_severity_score: 89.0, indigenous_environmental_destruction_scale_score: 92.0, environmental_defender_criminalisation_score: 87.0, state_corporate_environmental_impunity_gap_score: 85.0, risk_level: "critique", primary_pattern: "indigenous_environmental_destruction_scale", estimated_environmental_rights_index: 8.85, last_updated: "2026-06-21" },
    { id: "ENR-004", name: "Chine/Régions Industrielles — Smog PM2.5 Shanghai/Beijing, Villages Cancer Henan & Protestations Environnementales Réprimées", country: "Chine", composite_score: 84.65, toxic_pollution_environmental_health_severity_score: 87.0, indigenous_environmental_destruction_scale_score: 82.0, environmental_defender_criminalisation_score: 85.0, state_corporate_environmental_impunity_gap_score: 84.0, risk_level: "critique", primary_pattern: "toxic_pollution_environmental_health_severity", estimated_environmental_rights_index: 8.47, last_updated: "2026-06-21" },
    { id: "ENR-005", name: "Philippines — 800 Défenseurs Environnement Tués Depuis 2010, Mines Ouvertes & Lois Anti-Activisme", country: "Philippines", composite_score: 54.7, toxic_pollution_environmental_health_severity_score: 54.0, indigenous_environmental_destruction_scale_score: 56.0, environmental_defender_criminalisation_score: 58.0, state_corporate_environmental_impunity_gap_score: 50.0, risk_level: "élevé", primary_pattern: "environmental_defender_criminalisation", estimated_environmental_rights_index: 5.47, last_updated: "2026-06-21" },
    { id: "ENR-006", name: "Mexique/Amérique Centrale — Défenseurs Eau/Forêts Assassinés Cartels+État, Impunité 98% & Communautés Isolées", country: "Mexique", composite_score: 52.2, toxic_pollution_environmental_health_severity_score: 52.0, indigenous_environmental_destruction_scale_score: 53.0, environmental_defender_criminalisation_score: 55.0, state_corporate_environmental_impunity_gap_score: 48.0, risk_level: "élevé", primary_pattern: "environmental_defender_criminalisation", estimated_environmental_rights_index: 5.22, last_updated: "2026-06-21" },
    { id: "ENR-007", name: "Global Witness/AIDA — Rapport Défenseurs Environnement, Litiges Climatiques & Droit Environnement Sain ONU", country: "Global", composite_score: 26.45, toxic_pollution_environmental_health_severity_score: 26.0, indigenous_environmental_destruction_scale_score: 28.0, environmental_defender_criminalisation_score: 25.0, state_corporate_environmental_impunity_gap_score: 27.0, risk_level: "modéré", primary_pattern: "indigenous_environmental_destruction_scale", estimated_environmental_rights_index: 2.65, last_updated: "2026-06-21" },
    { id: "ENR-008", name: "ONU/Résolution 76/300 — Droit Environnement Sain Reconnaissance 2022, Rapporteur & SDG 15 Vie Terrestre", country: "Global", composite_score: 4.25, toxic_pollution_environmental_health_severity_score: 4.0, indigenous_environmental_destruction_scale_score: 4.0, environmental_defender_criminalisation_score: 5.0, state_corporate_environmental_impunity_gap_score: 4.0, risk_level: "faible", primary_pattern: "environmental_defender_criminalisation", estimated_environmental_rights_index: 0.43, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/environmental-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
