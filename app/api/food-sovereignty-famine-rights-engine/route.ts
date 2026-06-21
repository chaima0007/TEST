import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[food-sovereignty-famine-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Food Sovereignty Famine Rights Engine Agent",
  domain: "food_sovereignty_famine_rights",
  total_entities: 8,
  avg_composite: 61.75,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { famine_starvation_weaponization_severity: 4, land_grab_smallholder_displacement_scale: 2, seed_patent_corporate_monopoly: 2 },
  top_risk_entities: [
    "Yemen/Soudan — Famine Arme Guerre, Blocus Ports, 17M Insécurité Alimentaire Aiguë & Aid Workers Tués",
    "Éthiopie/Tigray — Récoltes Brûlées Systématiquement, Famine Weaponisée Conflits, Sièges Civils & Starvation Tactique",
    "Gaza/Palestine — Blocus 17 Ans, Famine Délibérée 2024 ONU Rapport, Destructions Terres Agricoles & Pêche Interdite",
  ],
  critical_alerts: [
    "Yemen/Soudan: famine_starvation_weaponization_severity",
    "Éthiopie/Tigray: famine_starvation_weaponization_severity",
    "Gaza/Palestine: famine_starvation_weaponization_severity",
    "RDC/Sahel: land_grab_smallholder_displacement_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_food_sovereignty_famine_rights_index: 6.18,
  data_sources: [
    "fao_world_food_insecurity_annual_report",
    "grain_land_grabbing_global_database",
    "la_via_campesina_food_sovereignty_violations_report",
  ],
  entities: [
    { entity_id: "FSF-001", name: "Yemen/Soudan — Famine Arme Guerre, Blocus Ports, 17M Insécurité Alimentaire Aiguë & Aid Workers Tués", country: "Yemen/Soudan", composite_score: 92.6, famine_starvation_weaponization_severity_score: 96.0, land_grab_smallholder_displacement_scale_score: 92.0, seed_patent_corporate_monopoly_score: 88.0, food_access_indigenous_sovereignty_deficit_gap_score: 94.0, risk_level: "critique", primary_pattern: "famine_starvation_weaponization_severity", estimated_food_sovereignty_famine_rights_index: 9.26, last_updated: "2026-06-21" },
    { entity_id: "FSF-002", name: "Éthiopie/Tigray — Récoltes Brûlées Systématiquement, Famine Weaponisée Conflits, Sièges Civils & Starvation Tactique", country: "Éthiopie", composite_score: 89.65, famine_starvation_weaponization_severity_score: 93.0, land_grab_smallholder_displacement_scale_score: 89.0, seed_patent_corporate_monopoly_score: 86.0, food_access_indigenous_sovereignty_deficit_gap_score: 90.0, risk_level: "critique", primary_pattern: "famine_starvation_weaponization_severity", estimated_food_sovereignty_famine_rights_index: 8.97, last_updated: "2026-06-21" },
    { entity_id: "FSF-003", name: "Gaza/Palestine — Blocus 17 Ans, Famine Délibérée 2024 ONU Rapport, Destructions Terres Agricoles & Pêche Interdite", country: "Palestine", composite_score: 87.15, famine_starvation_weaponization_severity_score: 90.0, land_grab_smallholder_displacement_scale_score: 88.0, seed_patent_corporate_monopoly_score: 83.0, food_access_indigenous_sovereignty_deficit_gap_score: 87.0, risk_level: "critique", primary_pattern: "famine_starvation_weaponization_severity", estimated_food_sovereignty_famine_rights_index: 8.72, last_updated: "2026-06-21" },
    { entity_id: "FSF-004", name: "RDC/Sahel — 27M Famine Aiguë, Climate Change Amplificateur, Terres Accaparées Multi-Nationales & Semences Brevetées", country: "RDC/Sahel", composite_score: 84.65, famine_starvation_weaponization_severity_score: 87.0, land_grab_smallholder_displacement_scale_score: 85.0, seed_patent_corporate_monopoly_score: 82.0, food_access_indigenous_sovereignty_deficit_gap_score: 84.0, risk_level: "critique", primary_pattern: "land_grab_smallholder_displacement_scale", estimated_food_sovereignty_famine_rights_index: 8.47, last_updated: "2026-06-21" },
    { entity_id: "FSF-005", name: "Inde/Bangladesh — Agriculteurs Dettes Suicides, Monsanto OGM Dépendance, Terres Firmes Chinoises & Prix Minimum", country: "Inde/Bangladesh", composite_score: 55.65, famine_starvation_weaponization_severity_score: 57.0, land_grab_smallholder_displacement_scale_score: 56.0, seed_patent_corporate_monopoly_score: 55.0, food_access_indigenous_sovereignty_deficit_gap_score: 54.0, risk_level: "élevé", primary_pattern: "seed_patent_corporate_monopoly", estimated_food_sovereignty_famine_rights_index: 5.57, last_updated: "2026-06-21" },
    { entity_id: "FSF-006", name: "USA/UE — Agrobusiness Subventions Distorsives, Monopole Semencier Bayer/Cargill, Dumpings Marchés Africains & Biofuels vs Food", country: "USA/UE", composite_score: 53.7, famine_starvation_weaponization_severity_score: 52.0, land_grab_smallholder_displacement_scale_score: 54.0, seed_patent_corporate_monopoly_score: 56.0, food_access_indigenous_sovereignty_deficit_gap_score: 53.0, risk_level: "élevé", primary_pattern: "seed_patent_corporate_monopoly", estimated_food_sovereignty_famine_rights_index: 5.37, last_updated: "2026-06-21" },
    { entity_id: "FSF-007", name: "La Via Campesina/FIAN — Mouvement Paysans Mondiaux, Déclaration ONU Droits Paysans 2018 & Monitoring Accaparement Terres", country: "Global", composite_score: 26.15, famine_starvation_weaponization_severity_score: 24.0, land_grab_smallholder_displacement_scale_score: 28.0, seed_patent_corporate_monopoly_score: 27.0, food_access_indigenous_sovereignty_deficit_gap_score: 26.0, risk_level: "modéré", primary_pattern: "land_grab_smallholder_displacement_scale", estimated_food_sovereignty_famine_rights_index: 2.62, last_updated: "2026-06-21" },
    { entity_id: "FSF-008", name: "ONU/Art.11 DESC — Droit Nourriture Adéquate, Rapporteur Spécial Alimentation & SDG 2 Faim Zéro", country: "Global", composite_score: 4.45, famine_starvation_weaponization_severity_score: 4.0, land_grab_smallholder_displacement_scale_score: 5.0, seed_patent_corporate_monopoly_score: 4.0, food_access_indigenous_sovereignty_deficit_gap_score: 5.0, risk_level: "faible", primary_pattern: "famine_starvation_weaponization_severity", estimated_food_sovereignty_famine_rights_index: 0.45, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/food-sovereignty-famine-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
