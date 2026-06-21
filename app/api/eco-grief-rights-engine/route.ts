import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[eco-grief-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Eco Grief Rights Engine Agent",
  domain: "eco_grief_rights",
  total_entities: 8,
  avg_composite: 61.56,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { climate_displacement_trauma_severity: 2, ecological_loss_grief_recognition_gap: 2, mental_health_climate_support_absence: 2, indigenous_land_loss_cultural_trauma: 2 },
  top_risk_entities: [
    "Kiribati/Tuvalu/Pacifique — Submersion Totale, Deuil Territoire & Zéro Soutien Psychologique",
    "Bangladesh — 30M Déplacés Climatiques 2050, Trauma Terres Inondées & Zéro Cadre Légal",
    "Australie/Bushfires — Solastalgie Documentée, Éco-Anxiété & Effondrement Grande Barrière Corail",
  ],
  critical_alerts: [
    "Kiribati/Tuvalu/Pacifique: climate_displacement_trauma_severity",
    "Bangladesh: ecological_loss_grief_recognition_gap",
    "Australie/Bushfires: mental_health_climate_support_absence",
    "Peuples Autochtones Amazonie/Arctique: indigenous_land_loss_cultural_trauma",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_eco_grief_rights_index: 6.16,
  data_sources: [
    "lancet_countdown_climate_change_mental_health_report_2023",
    "american_psychological_association_eco_anxiety_climate_distress_report",
    "unhcr_climate_displacement_psychological_trauma_global_review",
  ],
  entities: [
    { entity_id: "EGR-001", name: "Kiribati/Tuvalu/Pacifique — Submersion Totale, Deuil Territoire & Zéro Soutien Psychologique", country: "Océanie", composite_score: 93.65, climate_displacement_trauma_severity_score: 95.0, ecological_loss_grief_recognition_gap_score: 92.0, mental_health_climate_support_absence_score: 95.0, indigenous_land_loss_cultural_trauma_score: 92.0, risk_level: "critique", primary_pattern: "climate_displacement_trauma_severity", estimated_eco_grief_rights_index: 9.37, last_updated: "2026-06-21" },
    { entity_id: "EGR-002", name: "Bangladesh — 30M Déplacés Climatiques 2050, Trauma Terres Inondées & Zéro Cadre Légal", country: "Asie du Sud", composite_score: 89.6, climate_displacement_trauma_severity_score: 90.0, ecological_loss_grief_recognition_gap_score: 92.0, mental_health_climate_support_absence_score: 88.0, indigenous_land_loss_cultural_trauma_score: 88.0, risk_level: "critique", primary_pattern: "ecological_loss_grief_recognition_gap", estimated_eco_grief_rights_index: 8.96, last_updated: "2026-06-21" },
    { entity_id: "EGR-003", name: "Australie/Bushfires — Solastalgie Documentée, Éco-Anxiété & Effondrement Grande Barrière Corail", country: "Océanie", composite_score: 88.0, climate_displacement_trauma_severity_score: 88.0, ecological_loss_grief_recognition_gap_score: 88.0, mental_health_climate_support_absence_score: 88.0, indigenous_land_loss_cultural_trauma_score: 88.0, risk_level: "critique", primary_pattern: "mental_health_climate_support_absence", estimated_eco_grief_rights_index: 8.8, last_updated: "2026-06-21" },
    { entity_id: "EGR-004", name: "Peuples Autochtones Amazonie/Arctique — Déforestation, Fonte Glaces & Destruction Culture-Nature", country: "Global", composite_score: 86.75, climate_displacement_trauma_severity_score: 85.0, ecological_loss_grief_recognition_gap_score: 88.0, mental_health_climate_support_absence_score: 85.0, indigenous_land_loss_cultural_trauma_score: 90.0, risk_level: "critique", primary_pattern: "indigenous_land_loss_cultural_trauma", estimated_eco_grief_rights_index: 8.68, last_updated: "2026-06-21" },
    { entity_id: "EGR-005", name: "Sahel/Afrique — Sécheresse Permanente, Éco-Chagrin Non Reconnu & Zéro Soutien Psychosocial", country: "Afrique", composite_score: 53.25, climate_displacement_trauma_severity_score: 55.0, ecological_loss_grief_recognition_gap_score: 52.0, mental_health_climate_support_absence_score: 55.0, indigenous_land_loss_cultural_trauma_score: 50.0, risk_level: "élevé", primary_pattern: "climate_displacement_trauma_severity", estimated_eco_grief_rights_index: 5.33, last_updated: "2026-06-21" },
    { entity_id: "EGR-006", name: "Europe/Jeunesse — Éco-Anxiété 68% Jeunes 16-25, Burnout Activistes & Manque Prise en Charge", country: "Europe", composite_score: 51.0, climate_displacement_trauma_severity_score: 50.0, ecological_loss_grief_recognition_gap_score: 52.0, mental_health_climate_support_absence_score: 52.0, indigenous_land_loss_cultural_trauma_score: 50.0, risk_level: "élevé", primary_pattern: "ecological_loss_grief_recognition_gap", estimated_eco_grief_rights_index: 5.1, last_updated: "2026-06-21" },
    { entity_id: "EGR-007", name: "APA/Lancet Countdown — Reconnaissance Éco-Anxiété, Protocoles Thérapie Climat & Plaidoyer", country: "Global", composite_score: 25.85, climate_displacement_trauma_severity_score: 22.0, ecological_loss_grief_recognition_gap_score: 28.0, mental_health_climate_support_absence_score: 25.0, indigenous_land_loss_cultural_trauma_score: 30.0, risk_level: "modéré", primary_pattern: "mental_health_climate_support_absence", estimated_eco_grief_rights_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "EGR-008", name: "ONU/OHCHR — Droit Environnement Sain Résolution 2021, SDG 13 Climat & Soutien Trauma", country: "Global", composite_score: 4.4, climate_displacement_trauma_severity_score: 4.0, ecological_loss_grief_recognition_gap_score: 5.0, mental_health_climate_support_absence_score: 3.0, indigenous_land_loss_cultural_trauma_score: 6.0, risk_level: "faible", primary_pattern: "indigenous_land_loss_cultural_trauma", estimated_eco_grief_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/eco-grief-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
