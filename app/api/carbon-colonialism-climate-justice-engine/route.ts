import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[carbon-colonialism-climate-justice-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "carbon_colonialism_climate_justice_engine",
  domain: "carbon_colonialism_climate_justice",
  total_entities: 8,
  avg_composite: 61.97,
  confidence_score: 0.90,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    carbon_offset_land_grab: 3,
    climate_finance_inequity: 2,
    green_energy_displacement: 2,
    loss_damage_deficit: 1,
  },
  top_risk_entities: [
    { id: "CCJ-001", name: "République Démocratique du Congo — Accaparement Forêts Carbone, Expulsions Massives", score: 91.9, risk: "critique" },
    { id: "CCJ-003", name: "Mozambique — Projets Éoliens Déplacent Villageois, Bénéfices Exportés", score: 90.0, risk: "critique" },
    { id: "CCJ-002", name: "Bangladesh — 0.4% Émissions, 40M Réfugiés Climatiques, Zéro Réparation", score: 89.95, risk: "critique" },
  ],
  critical_alerts: [
    "CCJ-001: République Démocratique du Congo — Accaparement Forêts Carbone, Expulsions Massives — composite 91.9",
    "CCJ-002: Bangladesh — 0.4% Émissions, 40M Réfugiés Climatiques, Zéro Réparation — composite 89.95",
    "CCJ-003: Mozambique — Projets Éoliens Déplacent Villageois, Bénéfices Exportés — composite 90.0",
    "CCJ-004: Îles Marshall — Existence Menacée, Financement Climatique Bloqué par Conditionnalités — composite 86.65",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_carbon_colonialism_climate_justice_index: 6.2,
  data_sources: [
    "ipcc_ar6_climate_justice_2023",
    "un_fccc_loss_damage_fund_cop28_2023",
    "carbon_market_watch_redd_report_2024",
    "oxfam_climate_finance_inequality_2023",
  ],
  entities: [
    {
      id: "CCJ-001",
      name: "République Démocratique du Congo — Accaparement Forêts Carbone, Expulsions Massives",
      country: "RDC",
      carbon_offset_land_grab_score: 94.0,
      climate_finance_inequity_score: 91.0,
      green_energy_displacement_score: 89.0,
      loss_damage_reparations_deficit_score: 93.0,
      composite_score: 91.9,
      risk_level: "critique",
      primary_pattern: "5M hectares forêts cédés aux crédits carbone sans FPIC, 200k communautés déplacées, financement climatique 0.3% PIB reçu vs 8% promis",
      estimated_carbon_colonialism_climate_justice_index: 9.19,
      last_updated: "2026-06-21",
    },
    {
      id: "CCJ-002",
      name: "Bangladesh — 0.4% Émissions, 40M Réfugiés Climatiques, Zéro Réparation",
      country: "Bangladesh",
      carbon_offset_land_grab_score: 88.0,
      climate_finance_inequity_score: 93.0,
      green_energy_displacement_score: 86.0,
      loss_damage_reparations_deficit_score: 95.0,
      composite_score: 89.95,
      risk_level: "critique",
      primary_pattern: "Responsabilité historique nulle, 17% territoire submergé 2050, mécanisme perte-dommage COP28 insuffisant, fonds Green Climate reçu: 124M sur 1,3Md promis",
      estimated_carbon_colonialism_climate_justice_index: 9.0,
      last_updated: "2026-06-21",
    },
    {
      id: "CCJ-003",
      name: "Mozambique — Projets Éoliens Déplacent Villageois, Bénéfices Exportés",
      country: "Mozambique",
      carbon_offset_land_grab_score: 90.0,
      climate_finance_inequity_score: 87.0,
      green_energy_displacement_score: 92.0,
      loss_damage_reparations_deficit_score: 88.0,
      composite_score: 89.7,
      risk_level: "critique",
      primary_pattern: "Parcs éoliens Nacala déplacent 15k familles, électricité exportée vers Afrique du Sud, communautés sans accès 82% énergie renouvelable produite localement",
      estimated_carbon_colonialism_climate_justice_index: 8.97,
      last_updated: "2026-06-21",
    },
    {
      id: "CCJ-004",
      name: "Îles Marshall — Existence Menacée, Financement Climatique Bloqué par Conditionnalités",
      country: "Îles Marshall",
      carbon_offset_land_grab_score: 82.0,
      climate_finance_inequity_score: 89.0,
      green_energy_displacement_score: 84.0,
      loss_damage_reparations_deficit_score: 93.0,
      composite_score: 86.65,
      risk_level: "critique",
      primary_pattern: "Submersion 2050 certifiée, conditionnalités FMI bloquent accès fonds adaptation, 0 émissions historiques, perte souveraineté nationale programmée",
      estimated_carbon_colonialism_climate_justice_index: 8.67,
      last_updated: "2026-06-21",
    },
    {
      id: "CCJ-005",
      name: "Kenya — Marché Volontaire Carbone Frauduleux, REDD+ Détourné",
      country: "Kenya",
      carbon_offset_land_grab_score: 54.0,
      climate_finance_inequity_score: 52.0,
      green_energy_displacement_score: 50.0,
      loss_damage_reparations_deficit_score: 55.0,
      composite_score: 52.95,
      risk_level: "élevé",
      primary_pattern: "Projets REDD+ Kariba décertifiés fraude 2023, crédits carbone vendus sans bénéfice communautaire, 180k tonnes CO2 fictives compensées par multinationales",
      estimated_carbon_colonialism_climate_justice_index: 5.3,
      last_updated: "2026-06-21",
    },
    {
      id: "CCJ-006",
      name: "Brésil — Terres Autochtones Amazonie Sous Pression Carbone/Agrobusiness",
      country: "Brésil",
      carbon_offset_land_grab_score: 56.0,
      climate_finance_inequity_score: 50.0,
      green_energy_displacement_score: 53.0,
      loss_damage_reparations_deficit_score: 51.0,
      composite_score: 52.9,
      risk_level: "élevé",
      primary_pattern: "Déforestation Amazonie 11,568 km² 2022, crédits carbone mal attribués, peuples Yanomami victimes accaparement minier extractivisme climatique",
      estimated_carbon_colonialism_climate_justice_index: 5.29,
      last_updated: "2026-06-21",
    },
    {
      id: "CCJ-007",
      name: "Éthiopie — Barrage Grand Ethiopian Renaissance, Conflits Hydro-Climatiques",
      country: "Éthiopie",
      carbon_offset_land_grab_score: 28.0,
      climate_finance_inequity_score: 30.0,
      green_energy_displacement_score: 25.0,
      loss_damage_reparations_deficit_score: 27.0,
      composite_score: 27.65,
      risk_level: "modéré",
      primary_pattern: "Barrage GERD génère conflits régionaux eau, financement vert conditionné diplomatiquement, tensions climatiques Nil Bleu mal gérées",
      estimated_carbon_colonialism_climate_justice_index: 2.77,
      last_updated: "2026-06-21",
    },
    {
      id: "CCJ-008",
      name: "Danemark — Leader Financement Climatique, Fonds Perte-Dommage Pionnier",
      country: "Danemark",
      carbon_offset_land_grab_score: 5.0,
      climate_finance_inequity_score: 4.0,
      green_energy_displacement_score: 6.0,
      loss_damage_reparations_deficit_score: 5.0,
      composite_score: 5.0,
      risk_level: "faible",
      primary_pattern: "Premier pays fonds perte-dommage COP27, 100M€ engagés, transition juste exportée équitablement, modèle coopération climatique sud-sud",
      estimated_carbon_colonialism_climate_justice_index: 0.5,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/carbon-colonialism-climate-justice-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data.payload ?? data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }));
  }
}
