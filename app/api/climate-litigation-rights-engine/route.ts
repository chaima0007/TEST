import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[climate-litigation-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Climate Litigation Rights Engine Agent",
  domain: "climate_litigation_rights",
  total_entities: 8,
  avg_composite: 61.58,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { corporate_climate_liability: 2, state_duty_climate_action: 2, environmental_right_recognition: 2, litigation_access_justice: 2 },
  top_risk_entities: [
    "Philippines — Commission Droits Humains, 50 Entreprises Fossiles & Premier Tribunal Climatique Mondial",
    "Pays-Bas/Urgenda — Cour Suprême 2019, État Condamné -25% GES & Modèle Litige Climatique Global",
    "Shell/La Haye — Cour District 2021, -45% Émissions 2030 Scope3 & Responsabilité Corporative",
  ],
  critical_alerts: [
    "Philippines: corporate_climate_liability",
    "Pays-Bas/Urgenda: state_duty_climate_action",
    "Shell/La Haye: corporate_climate_liability",
    "Colombie: environmental_right_recognition",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_climate_litigation_rights_index: 6.16,
  data_sources: [
    "sabin_center_climate_change_litigation_database",
    "un_hrc_resolution_48_13_right_healthy_environment",
    "clientearth_strategic_climate_litigation_report",
  ],
  entities: [
    { entity_id: "CL-001", name: "Philippines — Commission Droits Humains, 50 Entreprises Fossiles & Premier Tribunal Climatique Mondial", country: "Asie du Sud-Est", composite_score: 93.25, environmental_right_recognition_score: 95.0, state_duty_climate_action_score: 92.0, corporate_climate_liability_score: 95.0, litigation_access_justice_score: 90.0, risk_level: "critique", primary_pattern: "corporate_climate_liability", estimated_climate_litigation_rights_index: 9.33, last_updated: "2026-06-21" },
    { entity_id: "CL-002", name: "Pays-Bas/Urgenda — Cour Suprême 2019, État Condamné -25% GES & Modèle Litige Climatique Global", country: "Europe", composite_score: 91.75, environmental_right_recognition_score: 92.0, state_duty_climate_action_score: 95.0, corporate_climate_liability_score: 88.0, litigation_access_justice_score: 92.0, risk_level: "critique", primary_pattern: "state_duty_climate_action", estimated_climate_litigation_rights_index: 9.18, last_updated: "2026-06-21" },
    { entity_id: "CL-003", name: "Shell/La Haye — Cour District 2021, -45% Émissions 2030 Scope3 & Responsabilité Corporative", country: "Europe", composite_score: 88.25, environmental_right_recognition_score: 88.0, state_duty_climate_action_score: 85.0, corporate_climate_liability_score: 92.0, litigation_access_justice_score: 88.0, risk_level: "critique", primary_pattern: "corporate_climate_liability", estimated_climate_litigation_rights_index: 8.83, last_updated: "2026-06-21" },
    { entity_id: "CL-004", name: "Colombie — Cour Suprême Amazonie 2018, Droits Générations Futures & Déforestation Systémique", country: "Amérique Latine", composite_score: 85.75, environmental_right_recognition_score: 88.0, state_duty_climate_action_score: 85.0, corporate_climate_liability_score: 82.0, litigation_access_justice_score: 88.0, risk_level: "critique", primary_pattern: "environmental_right_recognition", estimated_climate_litigation_rights_index: 8.58, last_updated: "2026-06-21" },
    { entity_id: "CL-005", name: "Torres Strait/ONU — Peuples Autochtones Australie, CCPR Violations & Inaction État Condamnée", country: "Océanie", composite_score: 53.75, environmental_right_recognition_score: 55.0, state_duty_climate_action_score: 55.0, corporate_climate_liability_score: 50.0, litigation_access_justice_score: 55.0, risk_level: "élevé", primary_pattern: "litigation_access_justice", estimated_climate_litigation_rights_index: 5.38, last_updated: "2026-06-21" },
    { entity_id: "CL-006", name: "CEDH/Duarte Agostinho — Portugal & 32 États, Jeunes Requérants & Inaction Climatique Europe", country: "Europe", composite_score: 49.6, environmental_right_recognition_score: 50.0, state_duty_climate_action_score: 52.0, corporate_climate_liability_score: 48.0, litigation_access_justice_score: 48.0, risk_level: "élevé", primary_pattern: "state_duty_climate_action", estimated_climate_litigation_rights_index: 4.96, last_updated: "2026-06-21" },
    { entity_id: "CL-007", name: "Sabin Center/ClientEarth — 2000+ Cas Répertoriés, Base Données Mondiale & Stratégie Litige", country: "Global", composite_score: 25.85, environmental_right_recognition_score: 22.0, state_duty_climate_action_score: 28.0, corporate_climate_liability_score: 25.0, litigation_access_justice_score: 30.0, risk_level: "modéré", primary_pattern: "litigation_access_justice", estimated_climate_litigation_rights_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "CL-008", name: "ONU/HRC Res.48/13 — Droit Environnement Sain Reconnu 2021 & Rapporteur Spécial Nommé", country: "Global", composite_score: 4.4, environmental_right_recognition_score: 4.0, state_duty_climate_action_score: 5.0, corporate_climate_liability_score: 3.0, litigation_access_justice_score: 6.0, risk_level: "faible", primary_pattern: "environmental_right_recognition", estimated_climate_litigation_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/climate-litigation-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
