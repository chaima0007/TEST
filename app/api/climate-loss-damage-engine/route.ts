import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[climate-loss-damage-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Climate Loss & Damage Engine Agent",
  domain: "climate_loss_damage",
  total_entities: 8,
  avg_composite: 59.67,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { cultural_territorial_loss: 2, economic_loss_scale: 2, compensation_mechanism_absence: 2, historical_emitter_impunity: 2 },
  top_risk_entities: [
    "Tuvalu/Kiribati — Submersion Territoriale, Identité Nationale Perdue & Déni Compensation Historique",
    "Bangladesh — Inondations 1/3 Territoire, 20M Déplacés Cyclones & Pertes Économiques Annuelles",
    "Sahel/Afrique — Désertification, Conflits Éleveurs-Agriculteurs & Famine Amplifiée Climat",
  ],
  critical_alerts: [
    "Tuvalu/Kiribati: cultural_territorial_loss",
    "Bangladesh: economic_loss_scale",
    "Sahel/Afrique: compensation_mechanism_absence",
    "AOSIS/Petits États Insulaires: cultural_territorial_loss",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_climate_loss_damage_index: 5.97,
  data_sources: [
    "loss_damage_collaboration_global_climate_vulnerability_report",
    "v20_vulnerable_twenty_group_climate_vulnerable_forum_annual_report",
    "unfccc_santiago_network_loss_damage_technical_assistance_report",
  ],
  entities: [
    { id: "LD-001", name: "Tuvalu/Kiribati — Submersion Territoriale, Identité Nationale Perdue & Déni Compensation Historique", country: "Océanie", composite_score: 89.65, economic_loss_scale_score: 88.0, cultural_territorial_loss_score: 95.0, compensation_mechanism_absence_score: 90.0, historical_emitter_impunity_score: 85.0, risk_level: "critique", primary_pattern: "cultural_territorial_loss", estimated_climate_loss_damage_index: 8.97, last_updated: "2026-06-20" },
    { id: "LD-002", name: "Bangladesh — Inondations 1/3 Territoire, 20M Déplacés Cyclones & Pertes Économiques Annuelles", country: "Asie du Sud", composite_score: 86.0, economic_loss_scale_score: 92.0, cultural_territorial_loss_score: 80.0, compensation_mechanism_absence_score: 88.0, historical_emitter_impunity_score: 82.0, risk_level: "critique", primary_pattern: "economic_loss_scale", estimated_climate_loss_damage_index: 8.6, last_updated: "2026-06-20" },
    { id: "LD-003", name: "Sahel/Afrique — Désertification, Conflits Éleveurs-Agriculteurs & Famine Amplifiée Climat", country: "Afrique Sub-Saharienne", composite_score: 84.0, economic_loss_scale_score: 85.0, cultural_territorial_loss_score: 82.0, compensation_mechanism_absence_score: 88.0, historical_emitter_impunity_score: 80.0, risk_level: "critique", primary_pattern: "compensation_mechanism_absence", estimated_climate_loss_damage_index: 8.4, last_updated: "2026-06-20" },
    { id: "LD-004", name: "AOSIS/Petits États Insulaires — Perte Souveraineté, Coraux Morts & Fonds L&D Insuffisant COP28", country: "Global/Océanie", composite_score: 82.0, economic_loss_scale_score: 78.0, cultural_territorial_loss_score: 90.0, compensation_mechanism_absence_score: 82.0, historical_emitter_impunity_score: 78.0, risk_level: "critique", primary_pattern: "cultural_territorial_loss", estimated_climate_loss_damage_index: 8.2, last_updated: "2026-06-20" },
    { id: "LD-005", name: "Amérique Latine/Glaciers — Disparition Glaciers Andes, Sécheresse Eau & Migrations Rurales", country: "Amérique Latine", composite_score: 53.85, economic_loss_scale_score: 52.0, cultural_territorial_loss_score: 55.0, compensation_mechanism_absence_score: 58.0, historical_emitter_impunity_score: 50.0, risk_level: "élevé", primary_pattern: "compensation_mechanism_absence", estimated_climate_loss_damage_index: 5.39, last_updated: "2026-06-20" },
    { id: "LD-006", name: "Asie du Sud-Est/Typhons — Dommages Cyclones Philippines/Vietnam & Reconstruction Sans Aide", country: "Asie du Sud-Est", composite_score: 51.35, economic_loss_scale_score: 50.0, cultural_territorial_loss_score: 52.0, compensation_mechanism_absence_score: 55.0, historical_emitter_impunity_score: 48.0, risk_level: "élevé", primary_pattern: "historical_emitter_impunity", estimated_climate_loss_damage_index: 5.14, last_updated: "2026-06-20" },
    { id: "LD-007", name: "COP27-28/Fonds L&D — Accord Sharm el-Sheikh, Fonds Mondial & Contributions Volontaires Insuffisantes", country: "Global", composite_score: 26.1, economic_loss_scale_score: 22.0, cultural_territorial_loss_score: 28.0, compensation_mechanism_absence_score: 30.0, historical_emitter_impunity_score: 25.0, risk_level: "modéré", primary_pattern: "economic_loss_scale", estimated_climate_loss_damage_index: 2.61, last_updated: "2026-06-20" },
    { id: "LD-008", name: "ONU/CCNUCC — Mécanisme Santiago, Article 8 Accord Paris & Réseau Knowledge Santiago", country: "Global", composite_score: 4.4, economic_loss_scale_score: 4.0, cultural_territorial_loss_score: 5.0, compensation_mechanism_absence_score: 3.0, historical_emitter_impunity_score: 6.0, risk_level: "faible", primary_pattern: "historical_emitter_impunity", estimated_climate_loss_damage_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/climate-loss-damage-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
