import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[climate-change-human-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Climate Change Human Rights Engine Agent",
  domain: "climate_change_human_rights",
  total_entities: 8,
  avg_composite: 62.24,
  confidence_score: 0.87,
  risk_distribution: { "critique": 4, "élevé": 2, "modéré": 1, "faible": 1 },
  pattern_distribution: { "climate_displacement_refugee_rights_severity": 3, "extreme_weather_livelihood_destruction_scale": 2, "fossil_fuel_community_health_impact": 1, "climate_justice_loss_damage_deficit_gap": 2 },
  top_risk_entities: ["Tuvalu/Îles Pacifique — Submersion Territoriale Totale, 11 000 Citoyens Apatrides Futurs, Coraux Blanchis & Eau Douce Salinisée", "Bangladesh/Delta du Gange — 20M Réfugiés Climatiques 2050, Cyclones Amplifiés, Inondations Annuelles & Salinisation Terres Agricoles", "Sahel/Afrique — Désertification 6M km², Conflits Éleveurs-Agriculteurs Eau, Famines Récurrentes & 1M+ Déplacés Annuels"],
  critical_alerts: ["Tuvalu/Îles Pacifique: climate_displacement_refugee_rights_severity", "Bangladesh/Delta du Gange: climate_displacement_refugee_rights_severity", "Sahel/Afrique: extreme_weather_livelihood_destruction_scale", "Amazonie/Brésil: fossil_fuel_community_health_impact"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_climate_change_human_rights_index: 6.22,
  data_sources: ["ipcc_climate_vulnerability_human_rights_report", "unhrc_climate_change_rights_resolution", "loss_damage_finance_accountability_report"],
  entities: [
    {
,      entity_id: "CCH-001"
      name: "Tuvalu/Îles Pacifique — Submersion Territoriale Totale, 11 000 Citoyens Apatrides Futurs, Coraux Blanchis & Eau Douce Salinisée"
      country: "Tuvalu/Pacifique"
      climate_displacement_refugee_rights_severity_score: 97.0
      extreme_weather_livelihood_destruction_scale_score: 95.0
      fossil_fuel_community_health_impact_score: 93.0
      climate_justice_loss_damage_deficit_gap_score: 96.0
      composite_score: 95.3
      risk_level: "critique"
      primary_pattern: "climate_displacement_refugee_rights_severity"
      estimated_climate_change_human_rights_index: 9.53
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "CCH-002"
      name: "Bangladesh/Delta du Gange — 20M Réfugiés Climatiques 2050, Cyclones Amplifiés, Inondations Annuelles & Salinisation Terres Agricoles"
      country: "Bangladesh"
      climate_displacement_refugee_rights_severity_score: 94.0
      extreme_weather_livelihood_destruction_scale_score: 92.0
      fossil_fuel_community_health_impact_score: 90.0
      climate_justice_loss_damage_deficit_gap_score: 93.0
      composite_score: 92.3
      risk_level: "critique"
      primary_pattern: "climate_displacement_refugee_rights_severity"
      estimated_climate_change_human_rights_index: 9.23
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "CCH-003"
      name: "Sahel/Afrique — Désertification 6M km², Conflits Éleveurs-Agriculteurs Eau, Famines Récurrentes & 1M+ Déplacés Annuels"
      country: "Sahel/Afrique"
      climate_displacement_refugee_rights_severity_score: 91.0
      extreme_weather_livelihood_destruction_scale_score: 89.0
      fossil_fuel_community_health_impact_score: 88.0
      climate_justice_loss_damage_deficit_gap_score: 90.0
      composite_score: 89.55
      risk_level: "critique"
      primary_pattern: "extreme_weather_livelihood_destruction_scale"
      estimated_climate_change_human_rights_index: 8.96
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "CCH-004"
      name: "Amazonie/Brésil — Déforestation 20% Biome, Communautés Autochtones Chassées, Sécheresses Record & Droits Territoriaux Violés"
      country: "Brésil/Amazonie"
      climate_displacement_refugee_rights_severity_score: 82.0
      extreme_weather_livelihood_destruction_scale_score: 80.0
      fossil_fuel_community_health_impact_score: 83.0
      climate_justice_loss_damage_deficit_gap_score: 81.0
      composite_score: 81.55
      risk_level: "critique"
      primary_pattern: "fossil_fuel_community_health_impact"
      estimated_climate_change_human_rights_index: 8.15
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "CCH-005"
      name: "Australie/Bushfires 2019-2020 — 3 Milliards Animaux Tués, Communautés Rurales Détruites, Fumée=Santé Publique & Peuples Premiers Terres Brûlées"
      country: "Australie"
      climate_displacement_refugee_rights_severity_score: 57.0
      extreme_weather_livelihood_destruction_scale_score: 55.0
      fossil_fuel_community_health_impact_score: 54.0
      climate_justice_loss_damage_deficit_gap_score: 56.0
      composite_score: 55.55
      risk_level: "élevé"
      primary_pattern: "extreme_weather_livelihood_destruction_scale"
      estimated_climate_change_human_rights_index: 5.55
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "CCH-006"
      name: "USA/Porto Rico Ouragan Maria — Infrastructure Détruite 6 Mois, 3 000 Morts Non-Reconnus, Diaspora Forcée & Abandon Fédéral Documenté"
      country: "USA/Porto Rico"
      climate_displacement_refugee_rights_severity_score: 54.0
      extreme_weather_livelihood_destruction_scale_score: 52.0
      fossil_fuel_community_health_impact_score: 51.0
      climate_justice_loss_damage_deficit_gap_score: 53.0
      composite_score: 52.55
      risk_level: "élevé"
      primary_pattern: "climate_displacement_refugee_rights_severity"
      estimated_climate_change_human_rights_index: 5.25
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "CCH-007"
      name: "IPCC/UNHRC — Rapport Changement Climatique Droits Humains 2022, Résolution ONU Droit Environnement Sain & Rapporteur Spécial Créé"
      country: "Global"
      climate_displacement_refugee_rights_severity_score: 28.0
      extreme_weather_livelihood_destruction_scale_score: 27.0
      fossil_fuel_community_health_impact_score: 26.0
      climate_justice_loss_damage_deficit_gap_score: 25.0
      composite_score: 26.65
      risk_level: "modéré"
      primary_pattern: "climate_justice_loss_damage_deficit_gap"
      estimated_climate_change_human_rights_index: 2.66
      last_updated: "2026-06-21"
    },
    {
,      entity_id: "CCH-008"
      name: "ONU/Accord Paris — COP28 Fonds Loss & Damage 700M$, NDC Insuffisantes 2.7°C Trajectoire & Mécanisme Compensation Climatique Partiel"
      country: "Global"
      climate_displacement_refugee_rights_severity_score: 5.0
      extreme_weather_livelihood_destruction_scale_score: 4.0
      fossil_fuel_community_health_impact_score: 4.0
      climate_justice_loss_damage_deficit_gap_score: 5.0
      composite_score: 4.5
      risk_level: "faible"
      primary_pattern: "climate_justice_loss_damage_deficit_gap"
      estimated_climate_change_human_rights_index: 0.45
      last_updated: "2026-06-21"
    }
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/climate-change-human-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
