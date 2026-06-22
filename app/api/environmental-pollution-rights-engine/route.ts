import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[environmental-pollution-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[environmental-pollution-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Environmental Pollution Rights Engine Agent",
  domain: "environmental_pollution_rights",
  total_entities: 8,
  avg_composite: 60.48,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Bangladesh — Pollution Textile Dhaka Rivières, 99% Eau Contaminée & 280 000 Morts/An Pollution Air",
    "Pakistan — Lahore Ville la Plus Polluée Monde 2024, Smog Paralysant & Crise Eau Souterraine",
    "Inde — Delhi Smog Mortel, 1,67 Million Morts Pollution Air/An & Fleuves Sacrés Toxiques",
  ],
  critical_alerts: [
    "Bangladesh: water_contamination_score",
    "Pakistan: air_pollution_mortality_score",
    "Inde: air_pollution_mortality_score",
    "Nigeria: toxic_waste_exposure_score",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_environmental_pollution_rights_index: 6.05,
  entities: [
    {
      entity_id: "EPR-001",
      name: "Bangladesh — Pollution Textile Dhaka Rivières, 99% Eau Contaminée & 280 000 Morts/An Pollution Air",
      country: "Bangladesh",
      air_pollution_mortality_score: 89.0,
      water_contamination_score: 91.0,
      toxic_waste_exposure_score: 88.0,
      environmental_justice_gap_score: 90.0,
      composite_score: 89.45,
      risk_level: "critique",
      primary_pattern: "water_contamination_score",
      estimated_environmental_pollution_rights_index: 8.95,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "EPR-002",
      name: "Pakistan — Lahore Ville la Plus Polluée Monde 2024, Smog Paralysant & Crise Eau Souterraine",
      country: "Pakistan",
      air_pollution_mortality_score: 88.0,
      water_contamination_score: 86.0,
      toxic_waste_exposure_score: 85.0,
      environmental_justice_gap_score: 87.0,
      composite_score: 86.55,
      risk_level: "critique",
      primary_pattern: "air_pollution_mortality_score",
      estimated_environmental_pollution_rights_index: 8.66,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "EPR-003",
      name: "Inde — Delhi Smog Mortel, 1,67 Million Morts Pollution Air/An & Fleuves Sacrés Toxiques",
      country: "Inde",
      air_pollution_mortality_score: 86.0,
      water_contamination_score: 84.0,
      toxic_waste_exposure_score: 83.0,
      environmental_justice_gap_score: 85.0,
      composite_score: 84.55,
      risk_level: "critique",
      primary_pattern: "air_pollution_mortality_score",
      estimated_environmental_pollution_rights_index: 8.46,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "EPR-004",
      name: "Nigeria — Pollution Delta Niger 60 Ans Shell & Eni, Sols Détruits & Communautés Sans Recours Juridique",
      country: "Nigeria",
      air_pollution_mortality_score: 82.0,
      water_contamination_score: 85.0,
      toxic_waste_exposure_score: 87.0,
      environmental_justice_gap_score: 84.0,
      composite_score: 84.4,
      risk_level: "critique",
      primary_pattern: "toxic_waste_exposure_score",
      estimated_environmental_pollution_rights_index: 8.44,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "EPR-005",
      name: "Chine — Rivières Toxiques Métaux Lourds Industrie, Zones Cancers & Villages Empoisonnés Invisibilisés",
      country: "Chine",
      air_pollution_mortality_score: 54.0,
      water_contamination_score: 56.0,
      toxic_waste_exposure_score: 57.0,
      environmental_justice_gap_score: 55.0,
      composite_score: 55.45,
      risk_level: "élevé",
      primary_pattern: "toxic_waste_exposure_score",
      estimated_environmental_pollution_rights_index: 5.55,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "EPR-006",
      name: "USA — Flint Water Crisis, Cancer Alley Louisiane & Justice Environnementale Raciale Défaillante",
      country: "USA",
      air_pollution_mortality_score: 43.0,
      water_contamination_score: 45.0,
      toxic_waste_exposure_score: 47.0,
      environmental_justice_gap_score: 50.0,
      composite_score: 45.9,
      risk_level: "élevé",
      primary_pattern: "environmental_justice_gap_score",
      estimated_environmental_pollution_rights_index: 4.59,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "EPR-007",
      name: "Pologne — Smog Charbon Hivernal, Maladies Respiratoires Chroniques & Résistance Transition Énergétique",
      country: "Pologne",
      air_pollution_mortality_score: 30.0,
      water_contamination_score: 26.0,
      toxic_waste_exposure_score: 28.0,
      environmental_justice_gap_score: 27.0,
      composite_score: 27.9,
      risk_level: "modéré",
      primary_pattern: "air_pollution_mortality_score",
      estimated_environmental_pollution_rights_index: 2.79,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "EPR-008",
      name: "Finlande — Air le Plus Pur EU, Eau Potable Universelle & Droits Environnementaux Constitutionnels",
      country: "Finlande",
      air_pollution_mortality_score: 11.0,
      water_contamination_score: 9.0,
      toxic_waste_exposure_score: 10.0,
      environmental_justice_gap_score: 8.0,
      composite_score: 9.65,
      risk_level: "faible",
      primary_pattern: "air_pollution_mortality_score",
      estimated_environmental_pollution_rights_index: 0.97,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/environmental-pollution-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return sealResponse(
      NextResponse.json({ payload: FALLBACK_PAYLOAD }, { status: 502 })
    );
  }
}
