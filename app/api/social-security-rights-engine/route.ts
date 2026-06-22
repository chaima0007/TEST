import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[social-security-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[social-security-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "SocialSecurityRights Engine Agent",
  domain: "social_security_rights",
  total_entities: 8,
  avg_composite: 61.36,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Soudan du Sud — 0% couverture sociale, conflit, famine totale",
    "Haïti — Effondrement état, gangs, 80% économie informelle",
    "RDC — 90% travailleurs informels, caisses retraite insolvables",
  ],
  critical_alerts: [
    "Soudan du Sud: Total absence of social protection system",
    "Haïti: State collapse & near-total informal economy",
    "RDC: Insolvent pension funds & mass informal exclusion",
    "Bangladesh: Garment sector workers excluded from social protection",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_social_security_rights_index: 6.14,
  entities: [
    {
      entity_id: "SSR-001",
      name: "Soudan du Sud — 0% couverture sociale, conflit, famine totale",
      country: "Soudan du Sud",
      social_protection_gap_score: 98.0,
      unemployment_coverage_score: 99.0,
      pension_access_score: 99.0,
      informal_worker_exclusion_score: 98.0,
      composite_score: 98.5,
      risk_level: "critique",
      primary_pattern: "Total absence of social protection system",
      estimated_social_security_rights_index: 9.85,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SSR-002",
      name: "Haïti — Effondrement état, gangs, 80% économie informelle",
      country: "Haïti",
      social_protection_gap_score: 92.0,
      unemployment_coverage_score: 94.0,
      pension_access_score: 88.0,
      informal_worker_exclusion_score: 96.0,
      composite_score: 92.3,
      risk_level: "critique",
      primary_pattern: "State collapse & near-total informal economy",
      estimated_social_security_rights_index: 9.23,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SSR-003",
      name: "RDC — 90% travailleurs informels, caisses retraite insolvables",
      country: "République Démocratique du Congo",
      social_protection_gap_score: 86.0,
      unemployment_coverage_score: 84.0,
      pension_access_score: 88.0,
      informal_worker_exclusion_score: 90.0,
      composite_score: 86.8,
      risk_level: "critique",
      primary_pattern: "Insolvent pension funds & mass informal exclusion",
      estimated_social_security_rights_index: 8.68,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SSR-004",
      name: "Bangladesh — 85% informel, travailleurs textile sans protection",
      country: "Bangladesh",
      social_protection_gap_score: 78.0,
      unemployment_coverage_score: 76.0,
      pension_access_score: 74.0,
      informal_worker_exclusion_score: 84.0,
      composite_score: 77.7,
      risk_level: "critique",
      primary_pattern: "Garment sector workers excluded from social protection",
      estimated_social_security_rights_index: 7.77,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SSR-005",
      name: "Inde — MGNREGA insuffisant, 90% informels sans couverture EPFO",
      country: "Inde",
      social_protection_gap_score: 56.0,
      unemployment_coverage_score: 54.0,
      pension_access_score: 50.0,
      informal_worker_exclusion_score: 58.0,
      composite_score: 54.4,
      risk_level: "élevé",
      primary_pattern: "Massive informal workforce excluded from EPFO",
      estimated_social_security_rights_index: 5.44,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SSR-006",
      name: "Brésil — Bolsa Familia mais 38M informels sans INSS",
      country: "Brésil",
      social_protection_gap_score: 46.0,
      unemployment_coverage_score: 44.0,
      pension_access_score: 42.0,
      informal_worker_exclusion_score: 50.0,
      composite_score: 45.3,
      risk_level: "élevé",
      primary_pattern: "Dual system: formal coverage vs. large informal gap",
      estimated_social_security_rights_index: 4.53,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SSR-007",
      name: "USA — Gaps santé/chômage, pas de congé parental fédéral",
      country: "États-Unis",
      social_protection_gap_score: 32.0,
      unemployment_coverage_score: 30.0,
      pension_access_score: 26.0,
      informal_worker_exclusion_score: 28.0,
      composite_score: 29.2,
      risk_level: "modéré",
      primary_pattern: "Gaps in Medicaid & absence of universal parental leave",
      estimated_social_security_rights_index: 2.92,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "SSR-008",
      name: "Danemark/Allemagne — Bismarck/Beveridge, couverture 95%+",
      country: "Danemark/Allemagne",
      social_protection_gap_score: 8.0,
      unemployment_coverage_score: 6.0,
      pension_access_score: 7.0,
      informal_worker_exclusion_score: 5.0,
      composite_score: 6.65,
      risk_level: "faible",
      primary_pattern: "Universal social protection model, 95%+ coverage",
      estimated_social_security_rights_index: 0.67,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/social-security-rights-engine`, {
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
