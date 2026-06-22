import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[space-mining-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[space-mining-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

export const revalidate = 30;

const MOCK = {
  engine: "SMR_ENGINE",
  domain: "space_mining_rights",
  total_entities: 8,
  avg_composite: 61.0,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["copuos_un_space_committee", "space_law_journal", "nasa_artemis_program_docs"],
  entities: [
    { id: "SMR-001", name: "SpaceX Asteroid Mining", country: "USA", composite_score: 92.3, risk_level: "critique", primary_pattern: "monopole_ressources_spatiales", estimated_space_mining_rights_index: 9.23, last_updated: "2026-06-22" },
    { id: "SMR-002", name: "Planetary Resources", country: "USA", composite_score: 85.6, risk_level: "critique", primary_pattern: "exploitation_asteroïdes_non_regulee", estimated_space_mining_rights_index: 8.56, last_updated: "2026-06-22" },
    { id: "SMR-003", name: "Deep Space Industries", country: "USA", composite_score: 81.1, risk_level: "critique", primary_pattern: "extraction_mineraux_espace_droit", estimated_space_mining_rights_index: 8.11, last_updated: "2026-06-22" },
    { id: "SMR-004", name: "ispace Japan", country: "Japon", composite_score: 75.1, risk_level: "critique", primary_pattern: "droits_propriete_ressources_lune", estimated_space_mining_rights_index: 7.51, last_updated: "2026-06-22" },
    { id: "SMR-005", name: "NASA Artemis Program", country: "USA", composite_score: 56.0, risk_level: "élevé", primary_pattern: "governance_partielle_ressources", estimated_space_mining_rights_index: 5.60, last_updated: "2026-06-22" },
    { id: "SMR-006", name: "ESA Space Resources", country: "Europe", composite_score: 53.95, risk_level: "élevé", primary_pattern: "cooperation_insuffisante_onu", estimated_space_mining_rights_index: 5.40, last_updated: "2026-06-22" },
    { id: "SMR-007", name: "COPUOS UN Space", country: "Global", composite_score: 30.3, risk_level: "modéré", primary_pattern: "regulation_partielle_espace", estimated_space_mining_rights_index: 3.03, last_updated: "2026-06-22" },
    { id: "SMR-008", name: "Space Law Institute", country: "Global", composite_score: 13.3, risk_level: "faible", primary_pattern: "défense_traité_espace_1967", estimated_space_mining_rights_index: 1.33, last_updated: "2026-06-22" },
  ],
};

export async function GET() {
  if (!SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${SWARM_API_URL}/api/space-mining-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
