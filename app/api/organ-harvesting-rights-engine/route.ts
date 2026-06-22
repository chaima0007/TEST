import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[organ-harvesting-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Organ Harvesting Rights Engine Agent",
  domain: "organ_harvesting_rights",
  total_entities: 8,
  avg_composite: 60.81,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Chine — Prélèvements forcés sur prisonniers d'opinion (Falun Gong, Ouïghours)",
    "Corée du Nord — Organ harvesting sur détenus politiques",
    "Égypte — Trafic d'organes lié à la pauvreté & réfugiés",
  ],
  critical_alerts: [
    "Chine: State-sponsored forced organ extraction from prisoners of conscience",
    "Corée du Nord: Organ harvesting on political detainees without consent",
    "Égypte: Poverty-driven organ trafficking & refugee exploitation",
    "Inde: Kidney trade networks & coerced living donors",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_organ_harvesting_rights_index: 6.08,
  entities: [
    {
      entity_id: "OHR-001",
      name: "Chine — Prélèvements forcés sur prisonniers d'opinion (Falun Gong, Ouïghours)",
      country: "Chine",
      forced_organ_extraction_score: 99.0,
      prisoner_organ_trafficking_score: 98.0,
      consent_violation_medical_score: 97.0,
      accountability_impunity_score: 99.0,
      composite_score: 98.15,
      risk_level: "critique",
      primary_pattern: "State-sponsored forced organ extraction from prisoners of conscience",
      estimated_organ_harvesting_rights_index: 9.82,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "OHR-002",
      name: "Corée du Nord — Organ harvesting sur détenus politiques",
      country: "Corée du Nord",
      forced_organ_extraction_score: 90.0,
      prisoner_organ_trafficking_score: 88.0,
      consent_violation_medical_score: 92.0,
      accountability_impunity_score: 95.0,
      composite_score: 91.1,
      risk_level: "critique",
      primary_pattern: "Organ harvesting on political detainees without consent",
      estimated_organ_harvesting_rights_index: 9.11,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "OHR-003",
      name: "Égypte — Trafic d'organes lié à la pauvreté & réfugiés",
      country: "Égypte",
      forced_organ_extraction_score: 72.0,
      prisoner_organ_trafficking_score: 68.0,
      consent_violation_medical_score: 74.0,
      accountability_impunity_score: 70.0,
      composite_score: 71.15,
      risk_level: "critique",
      primary_pattern: "Poverty-driven organ trafficking & refugee exploitation",
      estimated_organ_harvesting_rights_index: 7.12,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "OHR-004",
      name: "Inde — Réseaux de trafic rénal & donneurs coercés",
      country: "Inde",
      forced_organ_extraction_score: 65.0,
      prisoner_organ_trafficking_score: 60.0,
      consent_violation_medical_score: 68.0,
      accountability_impunity_score: 62.0,
      composite_score: 63.75,
      risk_level: "critique",
      primary_pattern: "Kidney trade networks & coerced living donors",
      estimated_organ_harvesting_rights_index: 6.38,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "OHR-005",
      name: "Pakistan — Marché illégal de rein, donneurs ruraux exploités",
      country: "Pakistan",
      forced_organ_extraction_score: 55.0,
      prisoner_organ_trafficking_score: 48.0,
      consent_violation_medical_score: 52.0,
      accountability_impunity_score: 50.0,
      composite_score: 51.65,
      risk_level: "élevé",
      primary_pattern: "Illegal kidney market exploiting rural poor",
      estimated_organ_harvesting_rights_index: 5.17,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "OHR-006",
      name: "Philippines — Transplant tourism & impunité médicale",
      country: "Philippines",
      forced_organ_extraction_score: 44.0,
      prisoner_organ_trafficking_score: 40.0,
      consent_violation_medical_score: 46.0,
      accountability_impunity_score: 42.0,
      composite_score: 43.1,
      risk_level: "élevé",
      primary_pattern: "Transplant tourism hub & medical impunity",
      estimated_organ_harvesting_rights_index: 4.31,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "OHR-007",
      name: "Brésil — Trafic d'organes & liste d'attente contournée",
      country: "Brésil",
      forced_organ_extraction_score: 28.0,
      prisoner_organ_trafficking_score: 24.0,
      consent_violation_medical_score: 30.0,
      accountability_impunity_score: 26.0,
      composite_score: 27.1,
      risk_level: "modéré",
      primary_pattern: "Organ black market bypassing transplant waitlists",
      estimated_organ_harvesting_rights_index: 2.71,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "OHR-008",
      name: "Espagne — Système de don fort, opt-out, conformité internationale",
      country: "Espagne",
      forced_organ_extraction_score: 8.0,
      prisoner_organ_trafficking_score: 5.0,
      consent_violation_medical_score: 6.0,
      accountability_impunity_score: 7.0,
      composite_score: 6.55,
      risk_level: "faible",
      primary_pattern: "Strong opt-out donation system, international compliance",
      estimated_organ_harvesting_rights_index: 0.66,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/organ-harvesting-rights-engine`, {
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
