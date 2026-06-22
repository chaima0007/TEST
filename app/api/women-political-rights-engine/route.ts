import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[women-political-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Women Political Rights Engine Agent",
  domain: "women_political_rights",
  total_entities: 8,
  avg_composite: 61.57,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Afghanistan — Femmes exclues de tout rôle politique sous les Taliban",
    "Arabie Saoudite — Système de tutelle masculine & participation politique limitée",
    "Iran — Répression des militantes politiques & discriminations légales",
  ],
  critical_alerts: [
    "Afghanistan: Interdiction totale des femmes en politique sous les Taliban",
    "Arabie Saoudite: Système de tutelle masculine bloque participation politique",
    "Iran: Candidates rejetées & militantes emprisonnées",
    "Yémen: Violence électorale ciblant les femmes candidates",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_women_political_rights_index: 6.16,
  entities: [
    {
      entity_id: "WPR-001",
      name: "Afghanistan — Femmes exclues de tout rôle politique sous les Taliban",
      country: "Afghanistan",
      political_exclusion_score: 99.0,
      electoral_violence_score: 95.0,
      legal_barriers_participation_score: 98.0,
      institutional_discrimination_score: 97.0,
      composite_score: 97.25,
      risk_level: "critique",
      primary_pattern: "Total exclusion of women from all political roles",
      estimated_women_political_rights_index: 9.73,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "WPR-002",
      name: "Arabie Saoudite — Système de tutelle masculine & participation politique limitée",
      country: "Arabie Saoudite",
      political_exclusion_score: 88.0,
      electoral_violence_score: 72.0,
      legal_barriers_participation_score: 90.0,
      institutional_discrimination_score: 85.0,
      composite_score: 84.65,
      risk_level: "critique",
      primary_pattern: "Male guardianship system blocking political participation",
      estimated_women_political_rights_index: 8.47,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "WPR-003",
      name: "Iran — Répression des militantes politiques & discriminations légales",
      country: "Iran",
      political_exclusion_score: 85.0,
      electoral_violence_score: 80.0,
      legal_barriers_participation_score: 87.0,
      institutional_discrimination_score: 83.0,
      composite_score: 83.75,
      risk_level: "critique",
      primary_pattern: "Systematic rejection of female candidates & imprisonment of activists",
      estimated_women_political_rights_index: 8.38,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "WPR-004",
      name: "Yémen — Violence électorale ciblant les femmes candidates",
      country: "Yémen",
      political_exclusion_score: 80.0,
      electoral_violence_score: 85.0,
      legal_barriers_participation_score: 78.0,
      institutional_discrimination_score: 79.0,
      composite_score: 80.45,
      risk_level: "critique",
      primary_pattern: "Electoral violence targeting women in conflict zones",
      estimated_women_political_rights_index: 8.05,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "WPR-005",
      name: "Nigeria — Quotas non appliqués & intimidation des candidates",
      country: "Nigeria",
      political_exclusion_score: 58.0,
      electoral_violence_score: 62.0,
      legal_barriers_participation_score: 50.0,
      institutional_discrimination_score: 55.0,
      composite_score: 56.65,
      risk_level: "élevé",
      primary_pattern: "Unenforced gender quotas & intimidation of female candidates",
      estimated_women_political_rights_index: 5.67,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "WPR-006",
      name: "Pakistan — Barrières culturelles & violence politique contre les femmes",
      country: "Pakistan",
      political_exclusion_score: 52.0,
      electoral_violence_score: 55.0,
      legal_barriers_participation_score: 48.0,
      institutional_discrimination_score: 50.0,
      composite_score: 51.35,
      risk_level: "élevé",
      primary_pattern: "Cultural barriers & political violence limiting women leadership",
      estimated_women_political_rights_index: 5.14,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "WPR-007",
      name: "Brésil — Harcèlement politique des élues & sous-représentation",
      country: "Brésil",
      political_exclusion_score: 30.0,
      electoral_violence_score: 28.0,
      legal_barriers_participation_score: 25.0,
      institutional_discrimination_score: 27.0,
      composite_score: 27.6,
      risk_level: "modéré",
      primary_pattern: "Political harassment of elected women & structural underrepresentation",
      estimated_women_political_rights_index: 2.76,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "WPR-008",
      name: "Islande — Parité atteinte, lois anti-discrimination robustes",
      country: "Islande",
      political_exclusion_score: 6.0,
      electoral_violence_score: 5.0,
      legal_barriers_participation_score: 4.0,
      institutional_discrimination_score: 5.0,
      composite_score: 5.05,
      risk_level: "faible",
      primary_pattern: "Gender parity achieved, robust anti-discrimination laws",
      estimated_women_political_rights_index: 0.51,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/women-political-rights-engine`, {
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
