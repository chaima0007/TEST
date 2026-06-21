import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[economic-sanctions-human-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Economic Sanctions Human Rights Engine Agent",
  domain: "economic_sanctions_human_rights",
  total_entities: 8,
  avg_composite: 59.14,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { medicine_food_access_denial: 2, civilian_suffering_scale: 2, sanctions_impunity_perpetrators: 2, democratic_governance_erosion: 2 },
  top_risk_entities: [
    "Iran — Sanctions OFAC, Pénurie Médicaments Oncologie & Effondrement Rial Populations",
    "Venezuela — Sanctions USA/UE, Hyperinflation, Fuite 7M Réfugiés & Crise Humanitaire",
    "Cuba — Blocus 60 Ans, Pénuries Chroniques & Embargo Unilatéral Condamné ONU",
  ],
  critical_alerts: [
    "Iran: medicine_food_access_denial",
    "Venezuela: civilian_suffering_scale",
    "Cuba: medicine_food_access_denial",
    "Corée du Nord: sanctions_impunity_perpetrators",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_economic_sanctions_human_rights_index: 5.91,
  data_sources: [
    "human_rights_watch_sanctions_civilian_impact_annual_report",
    "oxfam_unintended_consequences_sanctions_humanitarian_crisis_report",
    "un_special_rapporteur_unilateral_coercive_measures_human_rights_annual",
  ],
  entities: [
    { id: "ES-001", name: "Iran — Sanctions OFAC, Pénurie Médicaments Oncologie & Effondrement Rial Populations", country: "Moyen-Orient", composite_score: 88.35, civilian_suffering_scale_score: 92.0, medicine_food_access_denial_score: 95.0, democratic_governance_erosion_score: 80.0, sanctions_impunity_perpetrators_score: 85.0, risk_level: "critique", primary_pattern: "medicine_food_access_denial", estimated_economic_sanctions_human_rights_index: 8.84, last_updated: "2026-06-20" },
    { id: "ES-002", name: "Venezuela — Sanctions USA/UE, Hyperinflation, Fuite 7M Réfugiés & Crise Humanitaire", country: "Amérique Latine", composite_score: 86.55, civilian_suffering_scale_score: 88.0, medicine_food_access_denial_score: 90.0, democratic_governance_erosion_score: 85.0, sanctions_impunity_perpetrators_score: 82.0, risk_level: "critique", primary_pattern: "civilian_suffering_scale", estimated_economic_sanctions_human_rights_index: 8.66, last_updated: "2026-06-20" },
    { id: "ES-003", name: "Cuba — Blocus 60 Ans, Pénuries Chroniques & Embargo Unilatéral Condamné ONU", country: "Caraïbes", composite_score: 81.15, civilian_suffering_scale_score: 80.0, medicine_food_access_denial_score: 85.0, democratic_governance_erosion_score: 78.0, sanctions_impunity_perpetrators_score: 82.0, risk_level: "critique", primary_pattern: "medicine_food_access_denial", estimated_economic_sanctions_human_rights_index: 8.12, last_updated: "2026-06-20" },
    { id: "ES-004", name: "Corée du Nord — Sanctions CSNU, Famines Endémiques & Régime Enrichi sous Blocus", country: "Asie du Nord-Est", composite_score: 80.6, civilian_suffering_scale_score: 82.0, medicine_food_access_denial_score: 80.0, democratic_governance_erosion_score: 72.0, sanctions_impunity_perpetrators_score: 90.0, risk_level: "critique", primary_pattern: "sanctions_impunity_perpetrators", estimated_economic_sanctions_human_rights_index: 8.06, last_updated: "2026-06-20" },
    { id: "ES-005", name: "Russie/Ukraine — Sanctions G7, Réponse Agression & Double Standard vs Alliés Autoritaires", country: "Europe de l'Est", composite_score: 52.95, civilian_suffering_scale_score: 52.0, medicine_food_access_denial_score: 48.0, democratic_governance_erosion_score: 55.0, sanctions_impunity_perpetrators_score: 58.0, risk_level: "élevé", primary_pattern: "democratic_governance_erosion", estimated_economic_sanctions_human_rights_index: 5.3, last_updated: "2026-06-20" },
    { id: "ES-006", name: "Syrie/Yémen — Sanctions & Guerre, Caesar Act, Blocus Houthis & Aide Humanitaire Bloquée", country: "Moyen-Orient", composite_score: 51.6, civilian_suffering_scale_score: 55.0, medicine_food_access_denial_score: 52.0, democratic_governance_erosion_score: 50.0, sanctions_impunity_perpetrators_score: 48.0, risk_level: "élevé", primary_pattern: "civilian_suffering_scale", estimated_economic_sanctions_human_rights_index: 5.16, last_updated: "2026-06-20" },
    { id: "ES-007", name: "UE/USA — Sanctions Ciblées GAFI, Gel Avoirs & Exemptions Humanitaires Insuffisantes", country: "Global", composite_score: 27.5, civilian_suffering_scale_score: 22.0, medicine_food_access_denial_score: 28.0, democratic_governance_erosion_score: 30.0, sanctions_impunity_perpetrators_score: 32.0, risk_level: "modéré", primary_pattern: "democratic_governance_erosion", estimated_economic_sanctions_human_rights_index: 2.75, last_updated: "2026-06-20" },
    { id: "ES-008", name: "ONU/CSNU — Régime Sanctions Multilatérales, Comités & Mécanisme Suivi Humanitaire", country: "Global", composite_score: 4.4, civilian_suffering_scale_score: 4.0, medicine_food_access_denial_score: 5.0, democratic_governance_erosion_score: 3.0, sanctions_impunity_perpetrators_score: 6.0, risk_level: "faible", primary_pattern: "sanctions_impunity_perpetrators", estimated_economic_sanctions_human_rights_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/economic-sanctions-human-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
