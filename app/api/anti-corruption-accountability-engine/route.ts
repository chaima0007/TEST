import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[anti-corruption-accountability-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "anti_corruption_accountability_engine",
  domain: "anti_corruption_accountability",
  total_entities: 8,
  avg_composite: 61.33,
  confidence_score: 0.90,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    state_capture: 3,
    judicial_bribery: 2,
    kleptocracy_procurement: 2,
    whistleblower_deficit: 1,
  },
  top_risk_entities: [
    { id: "ACA-001", name: "Somalie/Yémen — IPC 8-10/100 & État Capturé", score: 93.25, risk: "critique" },
    { id: "ACA-002", name: "Venezuela/Nicaragua — PDVSA Pillé & Kleptocrates", score: 90.2, risk: "critique" },
    { id: "ACA-003", name: "Russie/Poutine — Oligarques Kremlin & Navalny", score: 87.2, risk: "critique" },
  ],
  critical_alerts: [
    "ACA-001: Somalie/Yémen — IPC 8-10/100 & État Capturé — composite 93.25",
    "ACA-002: Venezuela/Nicaragua — PDVSA Pillé & Kleptocrates — composite 90.2",
    "ACA-003: Russie/Poutine — Oligarques Kremlin & Navalny — composite 87.2",
    "ACA-004: Chine — Anti-Corruption Xi Sélective & CCDI — composite 84.2",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_anti_corruption_accountability_index: 6.13,
  data_sources: [
    "transparency_international_cpi_annual_report",
    "fatf_money_laundering_corruption_assessment",
    "global_witness_state_capture_kleptocracy_report",
  ],
  entities: [
    {
      entity_id: "ACA-001",
      name: "Somalie/Yémen — IPC 8-10/100 & État Capturé",
      country: "Somalie",
      grand_corruption_state_capture_severity_score: 95.0,
      judicial_police_bribery_impunity_scale_score: 92.0,
      public_procurement_kleptocracy_scale_score: 93.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 91.0,
      composite_score: 93.25,
      risk_level: "critique",
      primary_pattern: "État Capturé Clans, Fonctionnaires Jamais Payés & Aid Détournée",
      estimated_anti_corruption_accountability_index: 9.33,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ACA-002",
      name: "Venezuela/Nicaragua — PDVSA Pillé & Kleptocrates",
      country: "Venezuela",
      grand_corruption_state_capture_severity_score: 92.0,
      judicial_police_bribery_impunity_scale_score: 89.0,
      public_procurement_kleptocracy_scale_score: 90.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 88.0,
      composite_score: 90.2,
      risk_level: "critique",
      primary_pattern: "Pétrole PDVSA Pillé, Maduro Kleptocrates & Opposition Emprisonnée",
      estimated_anti_corruption_accountability_index: 9.02,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ACA-003",
      name: "Russie/Poutine — Oligarques Kremlin & Navalny",
      country: "Russie",
      grand_corruption_state_capture_severity_score: 89.0,
      judicial_police_bribery_impunity_scale_score: 86.0,
      public_procurement_kleptocracy_scale_score: 87.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 85.0,
      composite_score: 87.2,
      risk_level: "critique",
      primary_pattern: "Oligarques Proches Kremlin, Marchés Opaque & FBK Liquidé",
      estimated_anti_corruption_accountability_index: 8.72,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ACA-004",
      name: "Chine — Anti-Corruption Xi Sélective & CCDI",
      country: "Chine",
      grand_corruption_state_capture_severity_score: 86.0,
      judicial_police_bribery_impunity_scale_score: 83.0,
      public_procurement_kleptocracy_scale_score: 83.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 84.0,
      composite_score: 84.2,
      risk_level: "critique",
      primary_pattern: "5M Fonctionnaires Punis, Whistleblowers Disparus & CCDI Parti Contrôle",
      estimated_anti_corruption_accountability_index: 8.42,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ACA-005",
      name: "Brésil/Nigeria — Lava Jato Stoppé & Odebrecht",
      country: "Brésil",
      grand_corruption_state_capture_severity_score: 57.0,
      judicial_police_bribery_impunity_scale_score: 54.0,
      public_procurement_kleptocracy_scale_score: 55.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 53.0,
      composite_score: 55.1,
      risk_level: "élevé",
      primary_pattern: "Lava Jato Stoppé Politique, Odebrecht 12 Pays & EFCC Sélectif",
      estimated_anti_corruption_accountability_index: 5.51,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ACA-006",
      name: "Europe/USA — Panama Papers & Lobbying Légalisé",
      country: "Europe/USA",
      grand_corruption_state_capture_severity_score: 53.0,
      judicial_police_bribery_impunity_scale_score: 51.0,
      public_procurement_kleptocracy_scale_score: 52.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 51.0,
      composite_score: 52.0,
      risk_level: "élevé",
      primary_pattern: "Panama Papers Sans Suite, Enablers Immunisés & Revolving Door",
      estimated_anti_corruption_accountability_index: 5.2,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ACA-007",
      name: "Transparency International/GRECO — CPI & Standards OCDE",
      country: "International",
      grand_corruption_state_capture_severity_score: 27.0,
      judicial_police_bribery_impunity_scale_score: 25.0,
      public_procurement_kleptocracy_scale_score: 26.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 25.0,
      composite_score: 25.9,
      risk_level: "modéré",
      primary_pattern: "Mécanisme Évaluation CoE & Recommandations Anti-Corruption",
      estimated_anti_corruption_accountability_index: 2.59,
      last_updated: "2026-06-21",
    },
    {
      entity_id: "ACA-008",
      name: "ONU/UNCAC — Convention 2003 & SDG 16.6",
      country: "International",
      grand_corruption_state_capture_severity_score: 4.0,
      judicial_police_bribery_impunity_scale_score: 4.0,
      public_procurement_kleptocracy_scale_score: 4.0,
      whistleblower_anticorruption_protection_deficit_gap_score: 4.0,
      composite_score: 4.0,
      risk_level: "faible",
      primary_pattern: "Convention Nations Unies Contre Corruption 2003 & GAFI Blanchiment",
      estimated_anti_corruption_accountability_index: 0.4,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/anti-corruption-accountability-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
