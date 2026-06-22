import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[right-to-education-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[right-to-education-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "RightToEducationRights Engine Agent",
  domain: "right_to_education_rights",
  total_entities: 8,
  avg_composite: 60.53,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Niger — 45% scolarisation, 3M hors école, Boko Haram 800 écoles",
    "Afghanistan — 1.4M filles exclues lycées, enseignantes congédiées",
    "Mali — 800+ écoles fermées, 400k enfants déscolarisés",
  ],
  critical_alerts: [
    "Niger: Jihadist school closures & extreme gender exclusion",
    "Afghanistan: Taliban gender apartheid in education system",
    "Mali: Armed group attacks on schools & teachers",
    "Yémen: Conflict-destroyed education infrastructure",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_right_to_education_rights_index: 6.05,
  entities: [
    {
      entity_id: "RTE-001",
      name: "Niger — 45% scolarisation, 3M hors école, Boko Haram 800 écoles",
      country: "Niger",
      out_of_school_score: 97.0,
      gender_education_gap_score: 95.0,
      education_quality_gap_score: 94.0,
      attacks_on_education_score: 96.0,
      composite_score: 95.55,
      risk_level: "critique",
      primary_pattern: "Jihadist school closures & extreme gender exclusion",
      estimated_right_to_education_rights_index: 9.56,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTE-002",
      name: "Afghanistan — 1.4M filles exclues lycées, enseignantes congédiées",
      country: "Afghanistan",
      out_of_school_score: 90.0,
      gender_education_gap_score: 98.0,
      education_quality_gap_score: 82.0,
      attacks_on_education_score: 88.0,
      composite_score: 89.6,
      risk_level: "critique",
      primary_pattern: "Taliban gender apartheid in education system",
      estimated_right_to_education_rights_index: 8.96,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTE-003",
      name: "Mali — 800+ écoles fermées, 400k enfants déscolarisés",
      country: "Mali",
      out_of_school_score: 84.0,
      gender_education_gap_score: 80.0,
      education_quality_gap_score: 78.0,
      attacks_on_education_score: 92.0,
      composite_score: 83.1,
      risk_level: "critique",
      primary_pattern: "Armed group attacks on schools & teachers",
      estimated_right_to_education_rights_index: 8.31,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTE-004",
      name: "Yémen — 2M déscolarisés, 2 500 écoles détruites, enseignants non payés",
      country: "Yémen",
      out_of_school_score: 80.0,
      gender_education_gap_score: 74.0,
      education_quality_gap_score: 76.0,
      attacks_on_education_score: 88.0,
      composite_score: 79.1,
      risk_level: "critique",
      primary_pattern: "Conflict-destroyed education infrastructure",
      estimated_right_to_education_rights_index: 7.91,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTE-005",
      name: "Pakistan — 22M hors école, madrasas insuffisantes, inégalités urbain/rural",
      country: "Pakistan",
      out_of_school_score: 58.0,
      gender_education_gap_score: 60.0,
      education_quality_gap_score: 52.0,
      attacks_on_education_score: 46.0,
      composite_score: 54.6,
      risk_level: "élevé",
      primary_pattern: "Massive out-of-school crisis with gender gap",
      estimated_right_to_education_rights_index: 5.46,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTE-006",
      name: "Nigeria — 10M déscolarisés #1 Afrique, Boko Haram 1 500 écoles",
      country: "Nigeria",
      out_of_school_score: 50.0,
      gender_education_gap_score: 46.0,
      education_quality_gap_score: 44.0,
      attacks_on_education_score: 52.0,
      composite_score: 47.9,
      risk_level: "élevé",
      primary_pattern: "Boko Haram attacks & North-South education divide",
      estimated_right_to_education_rights_index: 4.79,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTE-007",
      name: "Inde — RTE Act lacunes, 35M OOS, discrimination castes",
      country: "Inde",
      out_of_school_score: 32.0,
      gender_education_gap_score: 30.0,
      education_quality_gap_score: 34.0,
      attacks_on_education_score: 22.0,
      composite_score: 30.0,
      risk_level: "modéré",
      primary_pattern: "Caste discrimination & quality gap in public education",
      estimated_right_to_education_rights_index: 3.0,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "RTE-008",
      name: "Finlande/Corée du Sud — PISA top, éducation gratuite universelle",
      country: "Finlande/Corée du Sud",
      out_of_school_score: 5.0,
      gender_education_gap_score: 6.0,
      education_quality_gap_score: 4.0,
      attacks_on_education_score: 2.0,
      composite_score: 4.4,
      risk_level: "faible",
      primary_pattern: "Universal free education, teacher excellence model",
      estimated_right_to_education_rights_index: 0.44,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/right-to-education-rights-engine`, {
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
