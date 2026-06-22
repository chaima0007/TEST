import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[disability-rights-crpd-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[disability-rights-crpd-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Disability Rights CRPD Engine Agent",
  domain: "disability_rights_crpd",
  total_entities: 8,
  avg_composite: 60.15,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Russie — Internats psychiatriques 156 000 personnes, stérilisation forcée, CRPD non-respectée",
    "Indonésie — Pasung (chaînes), 57 000 personnes handicapées mentales enchaînées légalement",
    "Inde — Institutions résidentielles 800 000 personnes, tutelle totale sans recours",
  ],
  critical_alerts: [
    "Russie: institutional_segregation",
    "Indonésie: institutional_segregation",
    "Inde: legal_capacity_denial_crpd",
    "Afrique Sub-Saharienne: crpd_implementation_gap",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_disability_rights_crpd_index: 6.02,
  entities: [
    {
      entity_id: "DRC-001",
      name: "Russie — Internats psychiatriques 156 000 personnes, stérilisation forcée, CRPD non-respectée",
      country: "Russie",
      crpd_implementation_gap_score: 96.0,
      institutional_segregation_score: 95.0,
      employment_exclusion_score: 93.0,
      legal_capacity_denial_crpd_score: 94.0,
      composite_score: 94.7,
      risk_level: "critique",
      primary_pattern: "institutional_segregation",
      estimated_disability_rights_crpd_index: 9.47,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DRC-002",
      name: "Indonésie — Pasung (chaînes), 57 000 personnes handicapées mentales enchaînées légalement",
      country: "Indonésie",
      crpd_implementation_gap_score: 90.0,
      institutional_segregation_score: 92.0,
      employment_exclusion_score: 88.0,
      legal_capacity_denial_crpd_score: 89.0,
      composite_score: 89.9,
      risk_level: "critique",
      primary_pattern: "institutional_segregation",
      estimated_disability_rights_crpd_index: 8.99,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DRC-003",
      name: "Inde — Institutions résidentielles 800 000 personnes, tutelle totale sans recours",
      country: "Inde",
      crpd_implementation_gap_score: 84.0,
      institutional_segregation_score: 86.0,
      employment_exclusion_score: 82.0,
      legal_capacity_denial_crpd_score: 80.0,
      composite_score: 83.5,
      risk_level: "critique",
      primary_pattern: "legal_capacity_denial_crpd",
      estimated_disability_rights_crpd_index: 8.35,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DRC-004",
      name: "Afrique Sub-Saharienne — 0% CRPD appliqué, chasse sorcières albinos, exclusion totale",
      country: "Afrique Sub-Saharienne",
      crpd_implementation_gap_score: 76.0,
      institutional_segregation_score: 74.0,
      employment_exclusion_score: 78.0,
      legal_capacity_denial_crpd_score: 72.0,
      composite_score: 75.3,
      risk_level: "critique",
      primary_pattern: "crpd_implementation_gap",
      estimated_disability_rights_crpd_index: 7.53,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DRC-005",
      name: "USA — ADA partiel, 70% personnes handicapées sans emploi, Olmstead non-appliqué",
      country: "USA",
      crpd_implementation_gap_score: 57.0,
      institutional_segregation_score: 54.0,
      employment_exclusion_score: 60.0,
      legal_capacity_denial_crpd_score: 52.0,
      composite_score: 56.15,
      risk_level: "élevé",
      primary_pattern: "employment_exclusion",
      estimated_disability_rights_crpd_index: 5.62,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DRC-006",
      name: "Chine — CRPD ratifiée 2008, application zéro, 85M handicapés sans protection réelle",
      country: "Chine",
      crpd_implementation_gap_score: 48.0,
      institutional_segregation_score: 50.0,
      employment_exclusion_score: 46.0,
      legal_capacity_denial_crpd_score: 52.0,
      composite_score: 48.9,
      risk_level: "élevé",
      primary_pattern: "crpd_implementation_gap",
      estimated_disability_rights_crpd_index: 4.89,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DRC-007",
      name: "France — ESAT dérogation SMIC, accessibilité retardée 20 ans, CDAPH lenteur",
      country: "France",
      crpd_implementation_gap_score: 28.0,
      institutional_segregation_score: 26.0,
      employment_exclusion_score: 30.0,
      legal_capacity_denial_crpd_score: 24.0,
      composite_score: 27.1,
      risk_level: "modéré",
      primary_pattern: "employment_exclusion",
      estimated_disability_rights_crpd_index: 2.71,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DRC-008",
      name: "Suède/Finlande — CRPD pleinement appliqué, vie indépendante, emploi 60%+ handicapés",
      country: "Suède/Finlande",
      crpd_implementation_gap_score: 6.0,
      institutional_segregation_score: 7.0,
      employment_exclusion_score: 5.0,
      legal_capacity_denial_crpd_score: 8.0,
      composite_score: 6.45,
      risk_level: "faible",
      primary_pattern: "crpd_implementation_gap",
      estimated_disability_rights_crpd_index: 0.65,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/disability-rights-crpd-engine`, {
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
