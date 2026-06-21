import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[food-sovereignty-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Food Sovereignty Engine Agent",
  domain: "food_sovereignty",
  total_entities: 8,
  avg_composite: 59.05,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { seed_patent_monopoly: 2, agribusiness_market_control: 2, small_farmer_displacement: 2, traditional_knowledge_erasure: 2 },
  top_risk_entities: [
    "Inde/Asie du Sud — Brevets Semences Monsanto/Bayer, Suicides Agriculteurs & Dépendance GMO",
    "Afrique/Sahel — Alliance pour la Révolution Verte (AGRA), Semences Hybrides & Dépendance Intrants",
    "USA — Oligopole Semencier Bayer-Corteva-Syngenta, Lobbying TRIPS & Brevet Vivant",
  ],
  critical_alerts: [
    "Inde/Asie du Sud: seed_patent_monopoly",
    "Afrique/Sahel: agribusiness_market_control",
    "USA: agribusiness_market_control",
    "Brésil: small_farmer_displacement",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_food_sovereignty_index: 5.91,
  data_sources: [
    "grain_org_seed_patent_monopoly_corporate_control_food_report",
    "un_special_rapporteur_right_food_annual_report_seed_sovereignty",
    "itpgrfa_fao_treaty_plant_genetic_resources_food_agriculture",
  ],
  entities: [
    { id: "FS-001", name: "Inde/Asie du Sud — Brevets Semences Monsanto/Bayer, Suicides Agriculteurs & Dépendance GMO", country: "Asie du Sud", composite_score: 89.1, seed_patent_monopoly_score: 92.0, agribusiness_market_control_score: 88.0, small_farmer_displacement_score: 90.0, traditional_knowledge_erasure_score: 85.0, risk_level: "critique", primary_pattern: "seed_patent_monopoly", estimated_food_sovereignty_index: 8.91, last_updated: "2026-06-20" },
    { id: "FS-002", name: "Afrique/Sahel — Alliance pour la Révolution Verte (AGRA), Semences Hybrides & Dépendance Intrants", country: "Afrique Sub-Saharienne", composite_score: 86.4, seed_patent_monopoly_score: 85.0, agribusiness_market_control_score: 90.0, small_farmer_displacement_score: 88.0, traditional_knowledge_erasure_score: 82.0, risk_level: "critique", primary_pattern: "agribusiness_market_control", estimated_food_sovereignty_index: 8.64, last_updated: "2026-06-20" },
    { id: "FS-003", name: "USA — Oligopole Semencier Bayer-Corteva-Syngenta, Lobbying TRIPS & Brevet Vivant", country: "Amérique du Nord", composite_score: 83.9, seed_patent_monopoly_score: 88.0, agribusiness_market_control_score: 92.0, small_farmer_displacement_score: 78.0, traditional_knowledge_erasure_score: 75.0, risk_level: "critique", primary_pattern: "agribusiness_market_control", estimated_food_sovereignty_index: 8.39, last_updated: "2026-06-20" },
    { id: "FS-004", name: "Brésil — Déforestation Amazonie pour Soja, Latifundias & Criminalisation MST", country: "Amérique Latine", composite_score: 76.1, seed_patent_monopoly_score: 72.0, agribusiness_market_control_score: 80.0, small_farmer_displacement_score: 78.0, traditional_knowledge_erasure_score: 75.0, risk_level: "critique", primary_pattern: "small_farmer_displacement", estimated_food_sovereignty_index: 7.61, last_updated: "2026-06-20" },
    { id: "FS-005", name: "Europe/PAC — Subventions Agro-Industrielles, Baisse Exploitations Familiales & Normes GMO", country: "Europe", composite_score: 53.85, seed_patent_monopoly_score: 52.0, agribusiness_market_control_score: 55.0, small_farmer_displacement_score: 58.0, traditional_knowledge_erasure_score: 50.0, risk_level: "élevé", primary_pattern: "small_farmer_displacement", estimated_food_sovereignty_index: 5.39, last_updated: "2026-06-20" },
    { id: "FS-006", name: "Chine — Concentration Agraire, Disparition Variétés Locales & Contrôle Étatique Semences", country: "Asie du Nord-Est", composite_score: 51.15, seed_patent_monopoly_score: 48.0, agribusiness_market_control_score: 52.0, small_farmer_displacement_score: 55.0, traditional_knowledge_erasure_score: 50.0, risk_level: "élevé", primary_pattern: "traditional_knowledge_erasure", estimated_food_sovereignty_index: 5.12, last_updated: "2026-06-20" },
    { id: "FS-007", name: "Via Campesina/Nyéléni — Déclaration Souveraineté Alimentaire & Traité Semences FAO", country: "Global", composite_score: 27.5, seed_patent_monopoly_score: 22.0, agribusiness_market_control_score: 28.0, small_farmer_displacement_score: 30.0, traditional_knowledge_erasure_score: 32.0, risk_level: "modéré", primary_pattern: "seed_patent_monopoly", estimated_food_sovereignty_index: 2.75, last_updated: "2026-06-20" },
    { id: "FS-008", name: "ONU/FAO/TIRPAA — Traité International Ressources Phytogénétiques & Rapporteur Alimentation", country: "Global", composite_score: 4.4, seed_patent_monopoly_score: 4.0, agribusiness_market_control_score: 5.0, small_farmer_displacement_score: 3.0, traditional_knowledge_erasure_score: 6.0, risk_level: "faible", primary_pattern: "traditional_knowledge_erasure", estimated_food_sovereignty_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/food-sovereignty-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
