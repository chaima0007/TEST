import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[forced-sterilization-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Forced Sterilization Rights Engine Agent",
  domain: "forced_sterilization_rights",
  total_entities: 8,
  avg_composite: 61.02,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Chine — Stérilisations forcées Ouïghours & minorités ethniques",
    "Inde — Camps de stérilisation massive & décès post-opératoires",
    "Ouzbékistan — Programme systématique de contrôle démographique",
  ],
  critical_alerts: [
    "Chine: Stérilisations forcées documentées sur les Ouïghours au Xinjiang",
    "Inde: Décès lors de camps de stérilisation de masse non consentie",
    "Ouzbékistan: Programme étatique ciblant les femmes rurales",
    "République tchèque: Stérilisations forcées Roms — cas CEDH non résolus",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_forced_sterilization_rights_index: 6.10,
  entities: [
    {
      entity_id: "FSR-001",
      name: "Chine — Stérilisations forcées Ouïghours & minorités ethniques",
      country: "Chine",
      coercive_sterilization_score: 97.0,
      consent_violation_score: 98.0,
      ethnic_targeting_score: 99.0,
      legal_accountability_gap_score: 96.0,
      composite_score: 97.45,
      risk_level: "critique",
      primary_pattern: "State-sponsored ethnic demographic control targeting Uyghurs",
      estimated_forced_sterilization_rights_index: 9.75,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "FSR-002",
      name: "Inde — Camps de stérilisation de masse & violations du consentement",
      country: "Inde",
      coercive_sterilization_score: 85.0,
      consent_violation_score: 88.0,
      ethnic_targeting_score: 75.0,
      legal_accountability_gap_score: 82.0,
      composite_score: 82.85,
      risk_level: "critique",
      primary_pattern: "Mass sterilisation camps with coercion & post-operative deaths",
      estimated_forced_sterilization_rights_index: 8.29,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "FSR-003",
      name: "Ouzbékistan — Programme étatique systématique de contrôle démographique",
      country: "Ouzbékistan",
      coercive_sterilization_score: 82.0,
      consent_violation_score: 85.0,
      ethnic_targeting_score: 70.0,
      legal_accountability_gap_score: 80.0,
      composite_score: 79.75,
      risk_level: "critique",
      primary_pattern: "Systematic state demographic control targeting rural women",
      estimated_forced_sterilization_rights_index: 7.98,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "FSR-004",
      name: "République tchèque — Stérilisations Roms, arrêts CEDH non exécutés",
      country: "République tchèque",
      coercive_sterilization_score: 78.0,
      consent_violation_score: 80.0,
      ethnic_targeting_score: 82.0,
      legal_accountability_gap_score: 75.0,
      composite_score: 78.85,
      risk_level: "critique",
      primary_pattern: "Forced sterilisation of Roma women, ECHR rulings not implemented",
      estimated_forced_sterilization_rights_index: 7.89,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "FSR-005",
      name: "Namibie — Stérilisations VIH+ sans consentement éclairé",
      country: "Namibie",
      coercive_sterilization_score: 58.0,
      consent_violation_score: 62.0,
      ethnic_targeting_score: 55.0,
      legal_accountability_gap_score: 60.0,
      composite_score: 58.65,
      risk_level: "élevé",
      primary_pattern: "Non-consensual sterilisation of HIV-positive women in public hospitals",
      estimated_forced_sterilization_rights_index: 5.87,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "FSR-006",
      name: "Pérou — Stérilisations forcées autochtones programme Fujimori",
      country: "Pérou",
      coercive_sterilization_score: 52.0,
      consent_violation_score: 55.0,
      ethnic_targeting_score: 60.0,
      legal_accountability_gap_score: 58.0,
      composite_score: 55.85,
      risk_level: "élevé",
      primary_pattern: "Fujimori-era mass sterilisation of Indigenous women, impunity persists",
      estimated_forced_sterilization_rights_index: 5.59,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "FSR-007",
      name: "Canada — Stérilisations autochtones récentes, enquête en cours",
      country: "Canada",
      coercive_sterilization_score: 28.0,
      consent_violation_score: 32.0,
      ethnic_targeting_score: 35.0,
      legal_accountability_gap_score: 30.0,
      composite_score: 31.0,
      risk_level: "modéré",
      primary_pattern: "Ongoing forced sterilisations of Indigenous women, Senate inquiry",
      estimated_forced_sterilization_rights_index: 3.1,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "FSR-008",
      name: "Pays-Bas — Cadre légal robuste, consentement éclairé protégé",
      country: "Pays-Bas",
      coercive_sterilization_score: 5.0,
      consent_violation_score: 4.0,
      ethnic_targeting_score: 3.0,
      legal_accountability_gap_score: 4.0,
      composite_score: 4.05,
      risk_level: "faible",
      primary_pattern: "Robust informed consent framework & accountability mechanisms",
      estimated_forced_sterilization_rights_index: 0.41,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/forced-sterilization-rights-engine`, {
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
