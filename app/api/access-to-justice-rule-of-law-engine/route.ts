import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[access-to-justice-rule-of-law-engine] SWARM_API_URL not set — returning mock");
}

const MOCK = {
  agent: "Access to Justice & Rule of Law Engine Agent",
  domain: "access_to_justice_rule_of_law",
  total_entities: 8,
  avg_composite: 63.29,
  confidence_score: 0.87,
  avg_estimated_access_to_justice_rule_of_law_index: 6.33,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: { judicial_independence_capture: 3, political_prisoners_rule_of_law: 2, constitutional_erosion: 2, access_to_remedy_gaps: 1 },
  top_risk_entities: [
    "Érythrée/Afewerki — Zéro Tribunal Indépendant, Constitution Jamais Appliquée, Prisonniers Indéfinis Sans Procès",
    "Venezuela/Maduro — Justice Instrumentalisée, Opposants Emprisonnés, TSJ Capturé & Impunité FAES 5 000 Exécutions",
    "Biélorussie/Loukachenko — 1 000+ Prisonniers Politiques Post-2020, Juges Révoqués & Tribunaux Militaires Opposants",
  ],
  critical_alerts: [
    "Érythrée/Afewerki: constitutional_erosion",
    "Venezuela/Maduro: judicial_independence_capture",
    "Biélorussie/Loukachenko: political_prisoners_rule_of_law",
    "Nicaragua/Ortega: political_prisoners_rule_of_law",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  data_sources: [
    "world_justice_project_rule_of_law_2023",
    "freedom_house_rule_of_law_2023",
    "transparency_international_cpi_2023",
    "icj_judicial_independence_2022",
  ],
  entities: [
    { entity_id: "AJRL-001", name: "Venezuela/Maduro — Justice Instrumentalisée, Opposants Emprisonnés, TSJ Capturé & Impunité FAES 5 000 Exécutions", country: "Venezuela", judicial_independence_capture_score: 92.0, political_prisoners_rule_of_law_score: 91.0, constitutional_erosion_score: 90.0, access_to_remedy_gaps_score: 89.0, composite_score: 90.65, risk_level: "critique", primary_pattern: "judicial_independence_capture", estimated_access_to_justice_rule_of_law_index: 9.07, last_updated: "2026-06-21" },
    { entity_id: "AJRL-002", name: "Biélorussie/Loukachenko — 1 000+ Prisonniers Politiques Post-2020, Juges Révoqués & Tribunaux Militaires Opposants", country: "Biélorussie", judicial_independence_capture_score: 90.0, political_prisoners_rule_of_law_score: 94.0, constitutional_erosion_score: 88.0, access_to_remedy_gaps_score: 87.0, composite_score: 89.9, risk_level: "critique", primary_pattern: "political_prisoners_rule_of_law", estimated_access_to_justice_rule_of_law_index: 8.99, last_updated: "2026-06-21" },
    { entity_id: "AJRL-003", name: "Érythrée/Afewerki — Zéro Tribunal Indépendant, Constitution Jamais Appliquée, Prisonniers Indéfinis Sans Procès", country: "Érythrée", judicial_independence_capture_score: 95.0, political_prisoners_rule_of_law_score: 92.0, constitutional_erosion_score: 96.0, access_to_remedy_gaps_score: 93.0, composite_score: 94.1, risk_level: "critique", primary_pattern: "constitutional_erosion", estimated_access_to_justice_rule_of_law_index: 9.41, last_updated: "2026-06-21" },
    { entity_id: "AJRL-004", name: "Nicaragua/Ortega — Juges Révoqués, Opposants Dépouillés Nationalité, Mgr Rolando Álvarez 26 Ans Prison", country: "Nicaragua", judicial_independence_capture_score: 88.0, political_prisoners_rule_of_law_score: 90.0, constitutional_erosion_score: 87.0, access_to_remedy_gaps_score: 85.0, composite_score: 87.65, risk_level: "critique", primary_pattern: "political_prisoners_rule_of_law", estimated_access_to_justice_rule_of_law_index: 8.77, last_updated: "2026-06-21" },
    { entity_id: "AJRL-005", name: "Hongrie/Orbán — Réforme Judiciaire Anticonstitutionnelle, Conseil Judiciaire Capturé & Pression Médias", country: "Hongrie", judicial_independence_capture_score: 58.0, political_prisoners_rule_of_law_score: 48.0, constitutional_erosion_score: 62.0, access_to_remedy_gaps_score: 52.0, composite_score: 55.3, risk_level: "élevé", primary_pattern: "constitutional_erosion", estimated_access_to_justice_rule_of_law_index: 5.53, last_updated: "2026-06-21" },
    { entity_id: "AJRL-006", name: "Pologne/PiS — Réforme Cour Suprême Anticonstitutionnelle, CJUE Condamnations & Régression Indépendance", country: "Pologne", judicial_independence_capture_score: 55.0, political_prisoners_rule_of_law_score: 42.0, constitutional_erosion_score: 58.0, access_to_remedy_gaps_score: 48.0, composite_score: 51.1, risk_level: "élevé", primary_pattern: "judicial_independence_capture", estimated_access_to_justice_rule_of_law_index: 5.11, last_updated: "2026-06-21" },
    { entity_id: "AJRL-007", name: "Turquie/Erdoğan — Pression Judiciaire Post-2016, 150 000+ Arrestations Coup & Indépendance Partielle", country: "Turquie", judicial_independence_capture_score: 38.0, political_prisoners_rule_of_law_score: 35.0, constitutional_erosion_score: 32.0, access_to_remedy_gaps_score: 30.0, composite_score: 34.15, risk_level: "modéré", primary_pattern: "judicial_independence_capture", estimated_access_to_justice_rule_of_law_index: 3.42, last_updated: "2026-06-21" },
    { entity_id: "AJRL-008", name: "Danemark — État de Droit Exemplaire, Corruption Quasi-Nulle, Indépendance Judiciaire Constitutionnelle", country: "Danemark", judicial_independence_capture_score: 4.0, political_prisoners_rule_of_law_score: 3.0, constitutional_erosion_score: 3.0, access_to_remedy_gaps_score: 4.0, composite_score: 3.5, risk_level: "faible", primary_pattern: "access_to_remedy_gaps", estimated_access_to_justice_rule_of_law_index: 0.35, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/access-to-justice-rule-of-law-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data));
  } catch {
    return NextResponse.json(sealResponse(MOCK), { status: 502 });
  }
}
