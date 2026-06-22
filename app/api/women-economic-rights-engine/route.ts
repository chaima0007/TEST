import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[women-economic-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Women Economic Rights Engine Agent",
  domain: "women_economic_rights",
  total_entities: 8,
  avg_composite: 60.09,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Afghanistan — Taliban interdiction travail femmes, 100% emplois perdus 2021",
    "Yémen — Conflit détruit économie femmes, garde-chiourme, 80% emplois informels perdus",
    "Soudan/Sahel — Lois personnelles discriminatoires, héritage 1/2 part, banques interdites",
  ],
  critical_alerts: [
    "Afghanistan: legal_employment_barriers",
    "Yémen: financial_exclusion",
    "Soudan/Sahel: property_rights_gap",
    "Pakistan: property_rights_gap",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_women_economic_rights_index: 6.01,
  entities: [
    {
      entity_id: "WER-001",
      name: "Afghanistan — Taliban interdiction travail femmes, 100% emplois perdus 2021",
      country: "Afghanistan",
      property_rights_gap_score: 97.0,
      equal_pay_gap_score: 96.0,
      financial_exclusion_score: 98.0,
      legal_employment_barriers_score: 97.0,
      composite_score: 97.0,
      risk_level: "critique",
      primary_pattern: "legal_employment_barriers",
      estimated_women_economic_rights_index: 9.70,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "WER-002",
      name: "Yémen — Conflit détruit économie femmes, garde-chiourme, 80% emplois informels perdus",
      country: "Yémen",
      property_rights_gap_score: 90.0,
      equal_pay_gap_score: 88.0,
      financial_exclusion_score: 91.0,
      legal_employment_barriers_score: 89.0,
      composite_score: 89.75,
      risk_level: "critique",
      primary_pattern: "financial_exclusion",
      estimated_women_economic_rights_index: 8.98,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "WER-003",
      name: "Soudan/Sahel — Lois personnelles discriminatoires, héritage 1/2 part, banques interdites",
      country: "Soudan/Sahel",
      property_rights_gap_score: 84.0,
      equal_pay_gap_score: 82.0,
      financial_exclusion_score: 85.0,
      legal_employment_barriers_score: 80.0,
      composite_score: 82.95,
      risk_level: "critique",
      primary_pattern: "property_rights_gap",
      estimated_women_economic_rights_index: 8.30,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "WER-004",
      name: "Pakistan — Loi héritages islamiques, propriétaires foncières 3%, banque 7% femmes",
      country: "Pakistan",
      property_rights_gap_score: 76.0,
      equal_pay_gap_score: 74.0,
      financial_exclusion_score: 78.0,
      legal_employment_barriers_score: 72.0,
      composite_score: 75.1,
      risk_level: "critique",
      primary_pattern: "property_rights_gap",
      estimated_women_economic_rights_index: 7.51,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "WER-005",
      name: "Inde — Écart salaire 28%, successions rurales bafouées, accès microcrédit limité",
      country: "Inde",
      property_rights_gap_score: 57.0,
      equal_pay_gap_score: 58.0,
      financial_exclusion_score: 56.0,
      legal_employment_barriers_score: 56.0,
      composite_score: 56.95,
      risk_level: "élevé",
      primary_pattern: "equal_pay_gap",
      estimated_women_economic_rights_index: 5.70,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "WER-006",
      name: "Nigéria — Lois coutumières héritages, écart salaire 35%, secteur informel 90% femmes",
      country: "Nigéria",
      property_rights_gap_score: 46.0,
      equal_pay_gap_score: 48.0,
      financial_exclusion_score: 50.0,
      legal_employment_barriers_score: 44.0,
      composite_score: 47.2,
      risk_level: "élevé",
      primary_pattern: "equal_pay_gap",
      estimated_women_economic_rights_index: 4.72,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "WER-007",
      name: "USA — Écart salaire 18%, Glass ceiling Fortune 500, congé maternité non-fédéral",
      country: "USA",
      property_rights_gap_score: 26.0,
      equal_pay_gap_score: 30.0,
      financial_exclusion_score: 24.0,
      legal_employment_barriers_score: 22.0,
      composite_score: 25.9,
      risk_level: "modéré",
      primary_pattern: "equal_pay_gap",
      estimated_women_economic_rights_index: 2.59,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "WER-008",
      name: "Islande/Suède — Égalité salariale certifiée, parité CA 40%+, congé parental 50/50",
      country: "Islande/Suède",
      property_rights_gap_score: 6.0,
      equal_pay_gap_score: 7.0,
      financial_exclusion_score: 5.0,
      legal_employment_barriers_score: 8.0,
      composite_score: 6.45,
      risk_level: "faible",
      primary_pattern: "legal_employment_barriers",
      estimated_women_economic_rights_index: 0.65,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/women-economic-rights-engine`, {
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
