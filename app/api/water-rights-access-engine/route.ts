import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[water-rights-access-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Water Rights Access Engine Agent",
  domain: "water_rights_access",
  total_entities: 8,
  avg_composite: 61.61,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { safe_water_access_deprivation_severity: 4, indigenous_water_rights_violation: 1, water_privatisation_corporate_capture_scale: 2, sanitation_hygiene_exclusion_gap: 1 },
  top_risk_entities: [
    "Afrique Sub-Saharienne — 400M Sans Eau Potable, Privatisation FMI & Femmes 6h/Jour Collecte",
    "Asie du Sud — Inde/Bangladesh Pollution Arsenic, 200M Privés Eau Sûre & Industries Sans Traitement",
    "MENA/Yemen — Guerre Eau, 18M Sans Accès Sûr, Puits Bombardés & Choléra",
  ],
  critical_alerts: [
    "Afrique Sub-Saharienne: safe_water_access_deprivation_severity",
    "Asie du Sud: safe_water_access_deprivation_severity",
    "MENA/Yemen: safe_water_access_deprivation_severity",
    "Amérique Latine/Communautés Autochtones: indigenous_water_rights_violation",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_water_rights_access_index: 6.16,
  data_sources: [
    "who_unicef_jmp_progress_drinking_water_sanitation_hygiene_report",
    "un_special_rapporteur_human_right_safe_drinking_water_sanitation_report",
    "foodandwaterwatch_water_privatisation_global_crisis_report",
  ],
  entities: [
    { id: "WAR-001", name: "Afrique Sub-Saharienne — 400M Sans Eau Potable, Privatisation FMI & Femmes 6h/Jour Collecte", country: "Afrique Sub-Saharienne", sector: "Accès Eau Rurale", composite_score: 93.2, safe_water_access_deprivation_severity_score: 96.0, water_privatisation_corporate_capture_scale_score: 93.0, indigenous_water_rights_violation_score: 91.0, sanitation_hygiene_exclusion_gap_score: 92.0, risk_level: "critique", primary_pattern: "safe_water_access_deprivation_severity", estimated_water_rights_access_index: 9.32, last_updated: "2026-06-21" },
    { id: "WAR-002", name: "Asie du Sud — Inde/Bangladesh Pollution Arsenic, 200M Privés Eau Sûre & Industries Sans Traitement", country: "Asie du Sud", sector: "Contamination Eau Industrielle", composite_score: 90.2, safe_water_access_deprivation_severity_score: 93.0, water_privatisation_corporate_capture_scale_score: 90.0, indigenous_water_rights_violation_score: 88.0, sanitation_hygiene_exclusion_gap_score: 89.0, risk_level: "critique", primary_pattern: "safe_water_access_deprivation_severity", estimated_water_rights_access_index: 9.02, last_updated: "2026-06-21" },
    { id: "WAR-003", name: "MENA/Yemen — Guerre Eau, 18M Sans Accès Sûr, Puits Bombardés & Choléra", country: "Yemen/MENA", sector: "Eau en Zones de Conflit", composite_score: 87.2, safe_water_access_deprivation_severity_score: 90.0, water_privatisation_corporate_capture_scale_score: 87.0, indigenous_water_rights_violation_score: 85.0, sanitation_hygiene_exclusion_gap_score: 86.0, risk_level: "critique", primary_pattern: "safe_water_access_deprivation_severity", estimated_water_rights_access_index: 8.72, last_updated: "2026-06-21" },
    { id: "WAR-004", name: "Amérique Latine/Communautés Autochtones — Barrages Hydro, Droits Autochtones Eau & Agro-Industrie", country: "Amérique Latine", sector: "Droits Eau Autochtones", composite_score: 86.2, safe_water_access_deprivation_severity_score: 87.0, water_privatisation_corporate_capture_scale_score: 84.0, indigenous_water_rights_violation_score: 90.0, sanitation_hygiene_exclusion_gap_score: 83.0, risk_level: "critique", primary_pattern: "indigenous_water_rights_violation", estimated_water_rights_access_index: 8.62, last_updated: "2026-06-21" },
    { id: "WAR-005", name: "USA/Flint/Frontline Communities — Contamination Plomb, Pollution PFAS Communautés Noires & Inaction État", country: "USA", sector: "Justice Eau Environnementale", composite_score: 54.2, safe_water_access_deprivation_severity_score: 57.0, water_privatisation_corporate_capture_scale_score: 54.0, indigenous_water_rights_violation_score: 52.0, sanitation_hygiene_exclusion_gap_score: 53.0, risk_level: "élevé", primary_pattern: "water_privatisation_corporate_capture_scale", estimated_water_rights_access_index: 5.42, last_updated: "2026-06-21" },
    { id: "WAR-006", name: "Europe de l'Est/Roms — Accès Eau Non Raccordés, Déconnexions Arbitraires & Discrimination", country: "Europe de l'Est", sector: "Exclusion Hydrique Roms", composite_score: 51.2, safe_water_access_deprivation_severity_score: 54.0, water_privatisation_corporate_capture_scale_score: 51.0, indigenous_water_rights_violation_score: 49.0, sanitation_hygiene_exclusion_gap_score: 50.0, risk_level: "élevé", primary_pattern: "sanitation_hygiene_exclusion_gap", estimated_water_rights_access_index: 5.12, last_updated: "2026-06-21" },
    { id: "WAR-007", name: "Coalition Eau Bien Commun/Oxfam — Plaidoyer Droit Eau ONU Rés 64/292 & Antiprivatisation", country: "Global", sector: "Plaidoyer Droit à l'Eau", composite_score: 26.55, safe_water_access_deprivation_severity_score: 28.0, water_privatisation_corporate_capture_scale_score: 25.0, indigenous_water_rights_violation_score: 26.0, sanitation_hygiene_exclusion_gap_score: 27.0, risk_level: "modéré", primary_pattern: "water_privatisation_corporate_capture_scale", estimated_water_rights_access_index: 2.66, last_updated: "2026-06-21" },
    { id: "WAR-008", name: "ONU/SDG 6 — Objectif Eau & Assainissement 2030, Rapporteur Spécial Eau & Cadre Normatif", country: "Global", sector: "Cadre Normatif International", composite_score: 4.1, safe_water_access_deprivation_severity_score: 5.0, water_privatisation_corporate_capture_scale_score: 4.0, indigenous_water_rights_violation_score: 4.0, sanitation_hygiene_exclusion_gap_score: 3.0, risk_level: "faible", primary_pattern: "safe_water_access_deprivation_severity", estimated_water_rights_access_index: 0.41, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/water-rights-access-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
