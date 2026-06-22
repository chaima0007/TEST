import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[digital-accessibility-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[digital-accessibility-rights-engine] SWARM_API_URL not set — running in offline mode");

const FALLBACK_PAYLOAD = {
  agent: "Digital Accessibility Rights Engine Agent",
  domain: "digital_accessibility_rights",
  total_entities: 8,
  avg_composite: 59.48,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  top_risk_entities: [
    "Afghanistan — Infrastructures numériques absentes, femmes exclues",
    "Niger — 5% connectivité, services publics inaccessibles en ligne",
    "Myanmar — Coupures internet & exclusion populations rurales",
  ],
  critical_alerts: [
    "Afghanistan: Near-total digital exclusion of women & rural populations",
    "Niger: 5% connectivity rate with zero accessible public digital services",
    "Myanmar: Internet shutdowns compounding digital accessibility barriers",
    "Bangladesh: WCAG compliance near-zero in public sector digital services",
  ],
  last_analysis: "2026-06-22",
  engine_version: "1.0.0",
  avg_estimated_digital_accessibility_rights_index: 5.95,
  entities: [
    {
      entity_id: "DAR-001",
      name: "Afghanistan — Infrastructures numériques absentes, femmes exclues",
      country: "Afghanistan",
      wcag_compliance_gap_score: 96.0,
      assistive_technology_exclusion_score: 94.0,
      public_service_digital_exclusion_score: 98.0,
      employment_digital_barrier_score: 97.0,
      composite_score: 96.25,
      risk_level: "critique",
      primary_pattern: "Near-total digital exclusion of women & rural populations",
      estimated_digital_accessibility_rights_index: 9.63,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DAR-002",
      name: "Niger — 5% connectivité, services publics inaccessibles en ligne",
      country: "Niger",
      wcag_compliance_gap_score: 92.0,
      assistive_technology_exclusion_score: 90.0,
      public_service_digital_exclusion_score: 95.0,
      employment_digital_barrier_score: 93.0,
      composite_score: 92.5,
      risk_level: "critique",
      primary_pattern: "5% connectivity rate with zero accessible public digital services",
      estimated_digital_accessibility_rights_index: 9.25,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DAR-003",
      name: "Myanmar — Coupures internet & exclusion populations rurales",
      country: "Myanmar",
      wcag_compliance_gap_score: 84.0,
      assistive_technology_exclusion_score: 80.0,
      public_service_digital_exclusion_score: 88.0,
      employment_digital_barrier_score: 85.0,
      composite_score: 84.45,
      risk_level: "critique",
      primary_pattern: "Internet shutdowns compounding digital accessibility barriers",
      estimated_digital_accessibility_rights_index: 8.45,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DAR-004",
      name: "Bangladesh — WCAG quasi-nul dans services publics numériques",
      country: "Bangladesh",
      wcag_compliance_gap_score: 76.0,
      assistive_technology_exclusion_score: 72.0,
      public_service_digital_exclusion_score: 78.0,
      employment_digital_barrier_score: 74.0,
      composite_score: 75.1,
      risk_level: "critique",
      primary_pattern: "WCAG compliance near-zero in public sector digital services",
      estimated_digital_accessibility_rights_index: 7.51,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DAR-005",
      name: "Inde — Accessibilité numérique fragmentée, lacunes handicap",
      country: "Inde",
      wcag_compliance_gap_score: 54.0,
      assistive_technology_exclusion_score: 50.0,
      public_service_digital_exclusion_score: 56.0,
      employment_digital_barrier_score: 52.0,
      composite_score: 53.1,
      risk_level: "élevé",
      primary_pattern: "Fragmented digital accessibility & disability inclusion gaps",
      estimated_digital_accessibility_rights_index: 5.31,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DAR-006",
      name: "USA — ADA numérique partiel, procès WCAG Section 508",
      country: "États-Unis",
      wcag_compliance_gap_score: 42.0,
      assistive_technology_exclusion_score: 38.0,
      public_service_digital_exclusion_score: 44.0,
      employment_digital_barrier_score: 40.0,
      composite_score: 41.1,
      risk_level: "élevé",
      primary_pattern: "Partial ADA digital coverage & ongoing Section 508 litigation",
      estimated_digital_accessibility_rights_index: 4.11,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DAR-007",
      name: "Brésil — LBI partielle, plateformes peu conformes WCAG",
      country: "Brésil",
      wcag_compliance_gap_score: 30.0,
      assistive_technology_exclusion_score: 26.0,
      public_service_digital_exclusion_score: 32.0,
      employment_digital_barrier_score: 28.0,
      composite_score: 29.1,
      risk_level: "modéré",
      primary_pattern: "Brazilian Inclusion Law partial implementation & WCAG non-compliance",
      estimated_digital_accessibility_rights_index: 2.91,
      last_updated: "2026-06-22",
    },
    {
      entity_id: "DAR-008",
      name: "UE — Directive Accessibilité Web, conformité WCAG 2.1 avancée",
      country: "Union Européenne",
      wcag_compliance_gap_score: 12.0,
      assistive_technology_exclusion_score: 10.0,
      public_service_digital_exclusion_score: 14.0,
      employment_digital_barrier_score: 12.0,
      composite_score: 12.0,
      risk_level: "faible",
      primary_pattern: "Web Accessibility Directive & advanced WCAG 2.1 compliance",
      estimated_digital_accessibility_rights_index: 1.20,
      last_updated: "2026-06-22",
    },
  ],
};

export async function GET() {
  if (!UPSTREAM) {
    return sealResponse(NextResponse.json({ payload: FALLBACK_PAYLOAD }));
  }
  try {
    const res = await fetch(`${UPSTREAM}/api/digital-accessibility-rights-engine`, {
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
