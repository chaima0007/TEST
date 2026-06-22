import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[economic-sanctions-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Economic Sanctions Rights Engine Agent",
  domain: "economic_sanctions_rights",
  total_entities: 8,
  avg_composite: 60.27,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Iran — Sanctions médicales bloquant accès aux médicaments vitaux",
    "Venezuela — Effondrement humanitaire sous embargo économique",
    "Cuba — 60 ans de blocus & pénuries alimentaires chroniques",
  ],
  critical_alerts: [
    "Iran: Medical sanctions blocking cancer treatment & insulin access",
    "Venezuela: Economic collapse & humanitarian crisis under US sanctions",
    "Cuba: 60-year embargo causing chronic food & medicine shortages",
    "Syrie: Sanctions exacerbating civilian suffering in conflict zones",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_economic_sanctions_rights_index: 6.03,
  entities: [
    {
      entity_id: "ESR-001",
      name: "Iran — Sanctions médicales bloquant traitements vitaux",
      country: "Iran",
      civilian_harm_score: 92.0,
      humanitarian_exception_failure_score: 94.0,
      medical_access_denial_score: 96.0,
      food_security_impact_score: 78.0,
      composite_score: 90.35,
      risk_level: "critique",
      primary_pattern: "Medical sanctions blocking cancer & insulin access",
      estimated_economic_sanctions_rights_index: 9.04,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ESR-002",
      name: "Venezuela — Effondrement économique & crise humanitaire",
      country: "Venezuela",
      civilian_harm_score: 89.0,
      humanitarian_exception_failure_score: 86.0,
      medical_access_denial_score: 88.0,
      food_security_impact_score: 92.0,
      composite_score: 88.6,
      risk_level: "critique",
      primary_pattern: "Economic collapse amplified by sectoral sanctions",
      estimated_economic_sanctions_rights_index: 8.86,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ESR-003",
      name: "Cuba — 60 ans de blocus & pénuries structurelles",
      country: "Cuba",
      civilian_harm_score: 82.0,
      humanitarian_exception_failure_score: 80.0,
      medical_access_denial_score: 84.0,
      food_security_impact_score: 85.0,
      composite_score: 82.55,
      risk_level: "critique",
      primary_pattern: "60-year embargo with chronic food & medicine shortages",
      estimated_economic_sanctions_rights_index: 8.26,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ESR-004",
      name: "Syrie — Sanctions aggravant souffrances civiles en zone de conflit",
      country: "Syrie",
      civilian_harm_score: 85.0,
      humanitarian_exception_failure_score: 82.0,
      medical_access_denial_score: 80.0,
      food_security_impact_score: 87.0,
      composite_score: 83.65,
      risk_level: "critique",
      primary_pattern: "Sanctions exacerbating civilian suffering in war zones",
      estimated_economic_sanctions_rights_index: 8.37,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ESR-005",
      name: "Myanmar — Sanctions post-coup & impact populations rurales",
      country: "Myanmar",
      civilian_harm_score: 55.0,
      humanitarian_exception_failure_score: 52.0,
      medical_access_denial_score: 50.0,
      food_security_impact_score: 58.0,
      composite_score: 53.85,
      risk_level: "élevé",
      primary_pattern: "Post-coup sanctions with rural population collateral impact",
      estimated_economic_sanctions_rights_index: 5.39,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ESR-006",
      name: "Russie — Sanctions sectorielles & accès aux biens essentiels",
      country: "Russie",
      civilian_harm_score: 46.0,
      humanitarian_exception_failure_score: 44.0,
      medical_access_denial_score: 42.0,
      food_security_impact_score: 48.0,
      composite_score: 44.9,
      risk_level: "élevé",
      primary_pattern: "Sectoral sanctions with civilian goods access restrictions",
      estimated_economic_sanctions_rights_index: 4.49,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ESR-007",
      name: "Corée du Nord — Sanctions totales & famine structurelle",
      country: "Corée du Nord",
      civilian_harm_score: 30.0,
      humanitarian_exception_failure_score: 28.0,
      medical_access_denial_score: 26.0,
      food_security_impact_score: 32.0,
      composite_score: 28.9,
      risk_level: "modéré",
      primary_pattern: "Total sanctions with regime-managed humanitarian access",
      estimated_economic_sanctions_rights_index: 2.89,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "ESR-008",
      name: "UE — Régime de sanctions ciblées avec exemptions humanitaires",
      country: "Union Européenne",
      civilian_harm_score: 10.0,
      humanitarian_exception_failure_score: 8.0,
      medical_access_denial_score: 6.0,
      food_security_impact_score: 9.0,
      composite_score: 8.35,
      risk_level: "faible",
      primary_pattern: "Targeted sanctions with robust humanitarian carve-outs",
      estimated_economic_sanctions_rights_index: 0.84,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/economic-sanctions-rights-engine`, {
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
