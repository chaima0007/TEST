import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[gender-based-violence-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[gender-based-violence-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Gender Based Violence Rights Engine Agent",
  domain: "gender_based_violence_rights",
  total_entities: 8,
  avg_composite: 60.81,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Honduras — Taux Féminicide Parmi les Plus Élevés Monde, Impunité 95% & Gangs MS-13",
    "RD Congo — Viols de Guerre Systématiques, Arme de Guerre Documentée ONU & Impunité Totale",
    "Afghanistan — Abolition Droits Femmes Talibans, Violences Domestiques Légalisées & Zéro Recours",
  ],
  critical_alerts: [
    "Honduras: femicide_score",
    "RD Congo: domestic_violence_impunity_score",
    "Afghanistan: institutional_revictimization_score",
    "Mexique: femicide_score",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_gender_based_violence_rights_index: 6.08,
  entities: [
    {
      entity_id: "GBV-001",
      name: "Honduras — Taux Féminicide Parmi les Plus Élevés Monde, Impunité 95% & Gangs MS-13",
      country: "Honduras",
      femicide_score: 90.0,
      domestic_violence_impunity_score: 88.0,
      institutional_revictimization_score: 87.0,
      access_protection_gap_score: 86.0,
      composite_score: 88.05,
      risk_level: "critique",
      primary_pattern: "femicide_score",
      estimated_gender_based_violence_rights_index: 8.81,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "GBV-002",
      name: "RD Congo — Viols de Guerre Systématiques, Arme de Guerre Documentée ONU & Impunité Totale",
      country: "RD Congo",
      femicide_score: 88.0,
      domestic_violence_impunity_score: 86.0,
      institutional_revictimization_score: 85.0,
      access_protection_gap_score: 84.0,
      composite_score: 86.05,
      risk_level: "critique",
      primary_pattern: "domestic_violence_impunity_score",
      estimated_gender_based_violence_rights_index: 8.61,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "GBV-003",
      name: "Afghanistan — Abolition Droits Femmes Talibans, Violences Domestiques Légalisées & Zéro Recours",
      country: "Afghanistan",
      femicide_score: 87.0,
      domestic_violence_impunity_score: 85.0,
      institutional_revictimization_score: 88.0,
      access_protection_gap_score: 86.0,
      composite_score: 86.65,
      risk_level: "critique",
      primary_pattern: "institutional_revictimization_score",
      estimated_gender_based_violence_rights_index: 8.67,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "GBV-004",
      name: "Mexique — 10 Femicides/Jour, Alerte Genre 21 États & Défaillance Systémique Ministerio Público",
      country: "Mexique",
      femicide_score: 82.0,
      domestic_violence_impunity_score: 80.0,
      institutional_revictimization_score: 78.0,
      access_protection_gap_score: 77.0,
      composite_score: 79.65,
      risk_level: "critique",
      primary_pattern: "femicide_score",
      estimated_gender_based_violence_rights_index: 7.97,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "GBV-005",
      name: "Inde — Violence Conjugale 30% Femmes, Barrières Culturelles Dépôt Plainte & Justice Lente",
      country: "Inde",
      femicide_score: 55.0,
      domestic_violence_impunity_score: 57.0,
      institutional_revictimization_score: 53.0,
      access_protection_gap_score: 56.0,
      composite_score: 55.2,
      risk_level: "élevé",
      primary_pattern: "domestic_violence_impunity_score",
      estimated_gender_based_violence_rights_index: 5.52,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "GBV-006",
      name: "Turquie — Retrait Convention Istanbul 2021, Hausse Féminicides & Résistances Institutionnelles",
      country: "Turquie",
      femicide_score: 49.0,
      domestic_violence_impunity_score: 51.0,
      institutional_revictimization_score: 50.0,
      access_protection_gap_score: 48.0,
      composite_score: 49.7,
      risk_level: "élevé",
      primary_pattern: "institutional_revictimization_score",
      estimated_gender_based_violence_rights_index: 4.97,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "GBV-007",
      name: "Brésil — Loi Maria da Penha Partiellement Appliquée, Lacunes Refuges & Violences Rurales",
      country: "Brésil",
      femicide_score: 32.0,
      domestic_violence_impunity_score: 30.0,
      institutional_revictimization_score: 28.0,
      access_protection_gap_score: 31.0,
      composite_score: 30.35,
      risk_level: "modéré",
      primary_pattern: "access_protection_gap_score",
      estimated_gender_based_violence_rights_index: 3.04,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "GBV-008",
      name: "Islande — Cadre Légal Fort Convention Istanbul, Réseau Refuges Complet & Taux Condamnation Élevé",
      country: "Islande",
      femicide_score: 12.0,
      domestic_violence_impunity_score: 11.0,
      institutional_revictimization_score: 10.0,
      access_protection_gap_score: 13.0,
      composite_score: 11.55,
      risk_level: "faible",
      primary_pattern: "access_protection_gap_score",
      estimated_gender_based_violence_rights_index: 1.16,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/gender-based-violence-rights-engine`, {
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
