import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) {
  console.warn("[surveillance-capitalism-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

export const revalidate = 30;

const MOCK = {
  engine: "SCR_ENGINE",
  domain: "surveillance_capitalism_rights",
  total_entities: 8,
  avg_composite: 60.96,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: ["gdpr_enforcement_tracker", "privacy_international_report", "electronic_frontier_foundation"],
  entities: [
    { id: "SCR-001", name: "Meta Platforms", country: "USA", composite_score: 92.3, risk_level: "critique", primary_pattern: "surveillance_comportementale_massive", estimated_surveillance_capitalism_rights_index: 9.23, last_updated: "2026-06-22" },
    { id: "SCR-002", name: "Google/Alphabet", country: "USA", composite_score: 88.3, risk_level: "critique", primary_pattern: "monetisation_donnees_personnelles", estimated_surveillance_capitalism_rights_index: 8.83, last_updated: "2026-06-22" },
    { id: "SCR-003", name: "TikTok/ByteDance", country: "Chine/USA", composite_score: 83.6, risk_level: "critique", primary_pattern: "algorithme_manipulation_psychologique", estimated_surveillance_capitalism_rights_index: 8.36, last_updated: "2026-06-22" },
    { id: "SCR-004", name: "Amazon Surveillance", country: "USA", composite_score: 75.1, risk_level: "critique", primary_pattern: "tracking_omnipresent_consommateurs", estimated_surveillance_capitalism_rights_index: 7.51, last_updated: "2026-06-22" },
    { id: "SCR-005", name: "Apple Data", country: "USA", composite_score: 56.0, risk_level: "élevé", primary_pattern: "consentement_insuffisant_publicite", estimated_surveillance_capitalism_rights_index: 5.60, last_updated: "2026-06-22" },
    { id: "SCR-006", name: "Microsoft Azure AI", country: "USA", composite_score: 52.75, risk_level: "élevé", primary_pattern: "surveillance_workplace_numérique", estimated_surveillance_capitalism_rights_index: 5.28, last_updated: "2026-06-22" },
    { id: "SCR-007", name: "Twitter/X Corp", country: "USA", composite_score: 30.3, risk_level: "modéré", primary_pattern: "données_publiques_exploitation", estimated_surveillance_capitalism_rights_index: 3.03, last_updated: "2026-06-22" },
    { id: "SCR-008", name: "Signal Foundation", country: "USA", composite_score: 9.3, risk_level: "faible", primary_pattern: "protection_données_exemplaire", estimated_surveillance_capitalism_rights_index: 0.93, last_updated: "2026-06-22" },
  ],
};

export async function GET() {
  if (!SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${SWARM_API_URL}/api/surveillance-capitalism-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
