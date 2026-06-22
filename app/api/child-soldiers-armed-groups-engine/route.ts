import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[child-soldiers-armed-groups-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[child-soldiers-armed-groups-engine] SWARM_API_URL is not set — falling back to mock data");
}

export const revalidate = 30;

const MOCK = {
  engine: "CSA_ENGINE",
  domain: "child_soldiers_armed_groups",
  total_entities: 8,
  avg_composite: 61.4,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["unicef_child_protection_database", "un_secretary_general_children_conflict", "human_rights_watch_children_report"],
  entities: [
    { id: "CSA-001", name: "Lord's Resistance Army", country: "Ouganda/RDC", composite_score: 92.3, risk_level: "critique", primary_pattern: "recrutement_enfants_force_ouganda", estimated_child_soldiers_armed_groups_index: 9.23, last_updated: "2026-06-22" },
    { id: "CSA-002", name: "Al-Shabaab Somalia", country: "Somalie", composite_score: 88.4, risk_level: "critique", primary_pattern: "enfants_soldats_terrorisme", estimated_child_soldiers_armed_groups_index: 8.84, last_updated: "2026-06-22" },
    { id: "CSA-003", name: "Boko Haram Nigeria", country: "Nigeria", composite_score: 84.1, risk_level: "critique", primary_pattern: "enlèvement_enfants_masse", estimated_child_soldiers_armed_groups_index: 8.41, last_updated: "2026-06-22" },
    { id: "CSA-004", name: "FDLR Congo", country: "RDC", composite_score: 78.6, risk_level: "critique", primary_pattern: "enfants_soldats_minerais_conflit", estimated_child_soldiers_armed_groups_index: 7.86, last_updated: "2026-06-22" },
    { id: "CSA-005", name: "Milices Sahel", country: "Sahel", composite_score: 56.2, risk_level: "élevé", primary_pattern: "recrutement_mineur_conflits", estimated_child_soldiers_armed_groups_index: 5.62, last_updated: "2026-06-22" },
    { id: "CSA-006", name: "Paramilitaires Myanmar", country: "Myanmar", composite_score: 52.8, risk_level: "élevé", primary_pattern: "travail_force_enfants", estimated_child_soldiers_armed_groups_index: 5.28, last_updated: "2026-06-22" },
    { id: "CSA-007", name: "Armée Nationale Chad", country: "Tchad", composite_score: 27.4, risk_level: "modéré", primary_pattern: "engagement_rehabilitation_partiel", estimated_child_soldiers_armed_groups_index: 2.74, last_updated: "2026-06-22" },
    { id: "CSA-008", name: "UNICEF Child Protection", country: "Global", composite_score: 11.6, risk_level: "faible", primary_pattern: "programme_protection_enfance", estimated_child_soldiers_armed_groups_index: 1.16, last_updated: "2026-06-22" },
  ],
};

export async function GET() {
  if (!SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${SWARM_API_URL}/api/child-soldiers-armed-groups-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
