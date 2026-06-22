import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[peasant-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Peasant Rights Engine Agent",
  domain: "peasant_rights",
  total_entities: 8,
  avg_composite: 58.66,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { land_dispossession: 2, corporate_agro_domination: 2, seed_criminalization: 2, legal_framework_absence: 2 },
  top_risk_entities: [
    "Honduras/Colombie/Guatemala — Syndicalistes Paysans Assassinés & Narco-Latifundisme",
    "Myanmar/Birmanie — Confiscation 5M Hectares, Junte Militaire & Entreprises Chinoises",
    "Inde — Lois Agricoles Libéralisation Forcée, Protestations Paysannes & MSP Menacé",
  ],
  critical_alerts: [
    "Honduras/Colombie/Guatemala: land_dispossession",
    "Myanmar/Birmanie: corporate_agro_domination",
    "Inde: seed_criminalization",
    "Afrique/Sahel: legal_framework_absence",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_peasant_rights_index: 5.87,
  data_sources: [
    "via_campesina_international_peasant_movement_annual_report",
    "grain_org_land_grabbing_corporate_food_regime_report",
    "un_special_rapporteur_right_food_peasants_undrop_implementation_review",
  ],
  entities: [
    { id: "PR-001", name: "Honduras/Colombie/Guatemala — Syndicalistes Paysans Assassinés & Narco-Latifundisme", country: "Amérique Latine", composite_score: 87.1, land_dispossession_score: 92.0, seed_criminalization_score: 82.0, legal_framework_absence_score: 88.0, corporate_agro_domination_score: 85.0, risk_level: "critique", primary_pattern: "land_dispossession", estimated_peasant_rights_index: 8.71, last_updated: "2026-06-20" },
    { id: "PR-002", name: "Myanmar/Birmanie — Confiscation 5M Hectares, Junte Militaire & Entreprises Chinoises", country: "Asie du Sud-Est", composite_score: 85.35, land_dispossession_score: 90.0, seed_criminalization_score: 78.0, legal_framework_absence_score: 85.0, corporate_agro_domination_score: 88.0, risk_level: "critique", primary_pattern: "corporate_agro_domination", estimated_peasant_rights_index: 8.54, last_updated: "2026-06-20" },
    { id: "PR-003", name: "Inde — Lois Agricoles Libéralisation Forcée, Protestations Paysannes & MSP Menacé", country: "Asie du Sud", composite_score: 80.9, land_dispossession_score: 78.0, seed_criminalization_score: 82.0, legal_framework_absence_score: 80.0, corporate_agro_domination_score: 85.0, risk_level: "critique", primary_pattern: "seed_criminalization", estimated_peasant_rights_index: 8.09, last_updated: "2026-06-20" },
    { id: "PR-004", name: "Afrique/Sahel — Accaparement Terres, Code Semencier UPOV & Paysans Sans Droits", country: "Afrique Sub-Saharienne", composite_score: 76.1, land_dispossession_score: 72.0, seed_criminalization_score: 80.0, legal_framework_absence_score: 78.0, corporate_agro_domination_score: 75.0, risk_level: "critique", primary_pattern: "legal_framework_absence", estimated_peasant_rights_index: 7.61, last_updated: "2026-06-20" },
    { id: "PR-005", name: "Brésil — Agrobusiness, Déforestation Amazonie & Mouvement Sans Terre MST Réprimé", country: "Amérique Latine", composite_score: 55.85, land_dispossession_score: 52.0, seed_criminalization_score: 55.0, legal_framework_absence_score: 58.0, corporate_agro_domination_score: 60.0, risk_level: "élevé", primary_pattern: "land_dispossession", estimated_peasant_rights_index: 5.59, last_updated: "2026-06-20" },
    { id: "PR-006", name: "Philippines — Réforme Agraire Inachevée, Haciendas & Paysans Assassinés Mindanao", country: "Asie du Sud-Est", composite_score: 51.15, land_dispossession_score: 50.0, seed_criminalization_score: 48.0, legal_framework_absence_score: 55.0, corporate_agro_domination_score: 52.0, risk_level: "élevé", primary_pattern: "legal_framework_absence", estimated_peasant_rights_index: 5.12, last_updated: "2026-06-20" },
    { id: "PR-007", name: "UE — PAC Lobby Agro-Industriel, Disparition Petites Exploitations & Semences Brevetées", country: "Europe", composite_score: 28.4, land_dispossession_score: 25.0, seed_criminalization_score: 30.0, legal_framework_absence_score: 28.0, corporate_agro_domination_score: 32.0, risk_level: "modéré", primary_pattern: "corporate_agro_domination", estimated_peasant_rights_index: 2.84, last_updated: "2026-06-20" },
    { id: "PR-008", name: "ONU/UNDROP/Via Campesina — Déclaration Droits Paysans 2018, FAO & Agroécologie", country: "Global", composite_score: 4.4, land_dispossession_score: 4.0, seed_criminalization_score: 5.0, legal_framework_absence_score: 3.0, corporate_agro_domination_score: 6.0, risk_level: "faible", primary_pattern: "seed_criminalization", estimated_peasant_rights_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/peasant-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
