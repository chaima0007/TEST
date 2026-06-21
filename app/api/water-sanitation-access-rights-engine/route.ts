import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[water-sanitation-access-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Water Sanitation Access Rights Engine Agent",
  domain: "water_sanitation_access_rights",
  total_entities: 8,
  avg_composite: 61.56,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { safe_water_access_denial_severity: 3, sanitation_infrastructure_absence_scale: 3, water_privatization_commodification: 1, climate_water_stress_conflict_deficit_gap: 1 },
  top_risk_entities: ["Yemen — Guerre Civile Infrastructure Eau Détruite, Choléra 2.5M Cas, Puits Bombardés & Population Sans Eau Potable", "RDC/Kivu — Zones Conflit Sans Eau Traitée, Cholera Endémique, Femmes 6h/Jour Eau & Viols Puits Contamination Intentionnelle", "Inde/Assainissement — 500M Sans Toilettes 2020, Défécation Espace Ouvert, Dalits Puits Interdits & Fluorose Eaux Contaminées"],
  critical_alerts: ["Yemen: safe_water_access_denial_severity", "RDC/Kivu: sanitation_infrastructure_absence_scale", "Inde/Assainissement: sanitation_infrastructure_absence_scale", "Bolivie/Cochabamba: water_privatization_commodification"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_water_sanitation_access_rights_index: 6.16,
  data_sources: ["who_unicef_jmp_water_sanitation_report", "un_water_sdg6_progress_report", "human_rights_watch_water_conflict_report"],
  entities: [
    { id: "WAR-001", name: "Yemen — Guerre Civile Infrastructure Eau Détruite, Choléra 2.5M Cas, Puits Bombardés & Population Sans Eau Potable", country: "Yemen", composite_score: 93.3, safe_water_access_denial_severity_score: 95.0, sanitation_infrastructure_absence_scale_score: 93.0, water_privatization_commodification_score: 91.0, climate_water_stress_conflict_deficit_gap_score: 94.0, risk_level: "critique", primary_pattern: "safe_water_access_denial_severity", estimated_water_sanitation_access_rights_index: 9.33, last_updated: "2026-06-21" },
    { id: "WAR-002", name: "RDC/Kivu — Zones Conflit Sans Eau Traitée, Cholera Endémique, Femmes 6h/Jour Eau & Viols Puits Contamination Intentionnelle", country: "RDC", composite_score: 90.3, safe_water_access_denial_severity_score: 91.0, sanitation_infrastructure_absence_scale_score: 92.0, water_privatization_commodification_score: 88.0, climate_water_stress_conflict_deficit_gap_score: 90.0, risk_level: "critique", primary_pattern: "sanitation_infrastructure_absence_scale", estimated_water_sanitation_access_rights_index: 9.03, last_updated: "2026-06-21" },
    { id: "WAR-003", name: "Inde/Assainissement — 500M Sans Toilettes 2020, Défécation Espace Ouvert, Dalits Puits Interdits & Fluorose Eaux Contaminées", country: "Inde", composite_score: 87.3, safe_water_access_denial_severity_score: 88.0, sanitation_infrastructure_absence_scale_score: 89.0, water_privatization_commodification_score: 85.0, climate_water_stress_conflict_deficit_gap_score: 87.0, risk_level: "critique", primary_pattern: "sanitation_infrastructure_absence_scale", estimated_water_sanitation_access_rights_index: 8.73, last_updated: "2026-06-21" },
    { id: "WAR-004", name: "Bolivie/Cochabamba — Privatisation Eau Bechtel 1999, Guerre de l'Eau, Coupures Pauvres & Militarisation Distribution", country: "Bolivie", composite_score: 83.8, safe_water_access_denial_severity_score: 84.0, sanitation_infrastructure_absence_scale_score: 82.0, water_privatization_commodification_score: 86.0, climate_water_stress_conflict_deficit_gap_score: 83.0, risk_level: "critique", primary_pattern: "water_privatization_commodification", estimated_water_sanitation_access_rights_index: 8.38, last_updated: "2026-06-21" },
    { id: "WAR-005", name: "Pakistan/Inondations — Inondations 2022 33M Affectés, Eau Contaminée Post-Désastre, Infrastructure WASH Détruite & Diarrhée Mortelle", country: "Pakistan", composite_score: 54.65, safe_water_access_denial_severity_score: 56.0, sanitation_infrastructure_absence_scale_score: 54.0, water_privatization_commodification_score: 55.0, climate_water_stress_conflict_deficit_gap_score: 53.0, risk_level: "élevé", primary_pattern: "climate_water_stress_conflict_deficit_gap", estimated_water_sanitation_access_rights_index: 5.46, last_updated: "2026-06-21" },
    { id: "WAR-006", name: "Mexique/Pénurie — Mexico City Day Zero, Aquifères Sur-Exploités, Colonie Sans Eau Courante & Distribution Camion-Citerne Corruption", country: "Mexique", composite_score: 52.55, safe_water_access_denial_severity_score: 53.0, sanitation_infrastructure_absence_scale_score: 51.0, water_privatization_commodification_score: 54.0, climate_water_stress_conflict_deficit_gap_score: 52.0, risk_level: "élevé", primary_pattern: "safe_water_access_denial_severity", estimated_water_sanitation_access_rights_index: 5.25, last_updated: "2026-06-21" },
    { id: "WAR-007", name: "ONU/EAU — Résolution 64/292 Droit Eau 2010, WaterAid, WASH Monitoring & Reporting JMP", country: "Global", composite_score: 26.55, safe_water_access_denial_severity_score: 27.0, sanitation_infrastructure_absence_scale_score: 25.0, water_privatization_commodification_score: 28.0, climate_water_stress_conflict_deficit_gap_score: 26.0, risk_level: "modéré", primary_pattern: "sanitation_infrastructure_absence_scale", estimated_water_sanitation_access_rights_index: 2.66, last_updated: "2026-06-21" },
    { id: "WAR-008", name: "SDG6/OMS — ODD 6 Eau Potable 2030, OMS Standards Qualité, Rapport Progrès & Mécanismes Financement", country: "Global", composite_score: 4.0, safe_water_access_denial_severity_score: 4.0, sanitation_infrastructure_absence_scale_score: 4.0, water_privatization_commodification_score: 4.0, climate_water_stress_conflict_deficit_gap_score: 4.0, risk_level: "faible", primary_pattern: "safe_water_access_denial_severity", estimated_water_sanitation_access_rights_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/water-sanitation-access-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
