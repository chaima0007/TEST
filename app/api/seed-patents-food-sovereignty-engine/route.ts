import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[seed-patents-food-sovereignty-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[seed-patents-food-sovereignty-engine] SWARM_API_URL is not set — falling back to mock data");
}

export const revalidate = 30;

const MOCK = {
  engine: "SPF_ENGINE",
  domain: "seed_patents_food_sovereignty",
  total_entities: 8,
  avg_composite: 59.99,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["wipo_patent_database", "grain_seed_sovereignty_report", "via_campesina_food_sovereignty"],
  entities: [
    { id: "SPF-001", name: "Monsanto/Bayer Seeds", country: "USA/Allemagne", composite_score: 91.2, risk_level: "critique", primary_pattern: "monopole_semences_ogm_brevets", estimated_seed_patents_food_sovereignty_index: 9.12, last_updated: "2026-06-22" },
    { id: "SPF-002", name: "Corteva Agriscience", country: "USA", composite_score: 86.5, risk_level: "critique", primary_pattern: "brevets_semences_restrictifs", estimated_seed_patents_food_sovereignty_index: 8.65, last_updated: "2026-06-22" },
    { id: "SPF-003", name: "Syngenta ChemChina", country: "Suisse/Chine", composite_score: 82.3, risk_level: "critique", primary_pattern: "contrôle_chaine_alimentaire", estimated_seed_patents_food_sovereignty_index: 8.23, last_updated: "2026-06-22" },
    { id: "SPF-004", name: "BASF Agriculture", country: "Allemagne", composite_score: 77.8, risk_level: "critique", primary_pattern: "semences_steriles_terminator", estimated_seed_patents_food_sovereignty_index: 7.78, last_updated: "2026-06-22" },
    { id: "SPF-005", name: "Pioneer DuPont", country: "USA", composite_score: 54.6, risk_level: "élevé", primary_pattern: "licences_restrictives_agriculteurs", estimated_seed_patents_food_sovereignty_index: 5.46, last_updated: "2026-06-22" },
    { id: "SPF-006", name: "Limagrain", country: "France", composite_score: 50.2, risk_level: "élevé", primary_pattern: "semi_ouvert_brevets_partiels", estimated_seed_patents_food_sovereignty_index: 5.02, last_updated: "2026-06-22" },
    { id: "SPF-007", name: "CGIAR Research", country: "Global", composite_score: 26.8, risk_level: "modéré", primary_pattern: "recherche_ouverte_partielle", estimated_seed_patents_food_sovereignty_index: 2.68, last_updated: "2026-06-22" },
    { id: "SPF-008", name: "La Via Campesina", country: "Global", composite_score: 10.5, risk_level: "faible", primary_pattern: "souveraineté_alimentaire_paysanne", estimated_seed_patents_food_sovereignty_index: 1.05, last_updated: "2026-06-22" },
  ],
};

export async function GET() {
  if (!SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${SWARM_API_URL}/api/seed-patents-food-sovereignty-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
