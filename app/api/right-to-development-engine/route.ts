import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[right-to-development-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Right to Development Engine Agent",
  domain: "right_to_development",
  total_entities: 8,
  avg_composite: 61.31,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { development_finance_neocolonial_conditionality: 3, debt_trap_sovereignty_undermining: 2, technology_knowledge_transfer_exclusion_scale: 2, sdg_implementation_inequality_gap: 1 },
  top_risk_entities: [
    "Afrique Sub-Saharienne/FMI — Conditionnalités Austérité Coupes Santé/Éducation, Dette 70% PIB & Souveraineté Économique Réduite",
    "Sri Lanka/Zambie — Surendettement Ceinture Route Chine, Ports Loués 99 Ans & Défaut Paiement Sans Restructuration",
    "Haïti — Ingérence FMI/Banque Mondiale 30 Ans, Corruption Induite Aide & Dépendance Structurelle Humanitaire",
  ],
  critical_alerts: [
    "Afrique Sub-Saharienne/FMI: development_finance_neocolonial_conditionality",
    "Sri Lanka/Zambie: debt_trap_sovereignty_undermining",
    "Haïti: development_finance_neocolonial_conditionality",
    "Sahel: development_finance_neocolonial_conditionality",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_right_to_development_index: 6.13,
  data_sources: [
    "un_declaration_right_to_development_1986_resolution_41_128",
    "unctad_trade_development_report",
    "oxfam_imf_austerity_conditionality_report",
  ],
  entities: [
    { id: "RTD-001", name: "Afrique Sub-Saharienne/FMI — Conditionnalités Austérité Coupes Santé/Éducation, Dette 70% PIB & Souveraineté Économique Réduite", country: "Afrique Sub-Saharienne", composite_score: 93.6, development_finance_neocolonial_conditionality_score: 96.0, technology_knowledge_transfer_exclusion_scale_score: 91.0, debt_trap_sovereignty_undermining_score: 93.0, sdg_implementation_inequality_gap_score: 94.0, risk_level: "critique", primary_pattern: "development_finance_neocolonial_conditionality", estimated_right_to_development_index: 9.36, last_updated: "2026-06-21" },
    { id: "RTD-002", name: "Sri Lanka/Zambie — Surendettement Ceinture Route Chine, Ports Loués 99 Ans & Défaut Paiement Sans Restructuration", country: "Sri Lanka/Zambie", composite_score: 90.7, development_finance_neocolonial_conditionality_score: 92.0, technology_knowledge_transfer_exclusion_scale_score: 87.0, debt_trap_sovereignty_undermining_score: 95.0, sdg_implementation_inequality_gap_score: 88.0, risk_level: "critique", primary_pattern: "debt_trap_sovereignty_undermining", estimated_right_to_development_index: 9.07, last_updated: "2026-06-21" },
    { id: "RTD-003", name: "Haïti — Ingérence FMI/Banque Mondiale 30 Ans, Corruption Induite Aide & Dépendance Structurelle Humanitaire", country: "Haïti", composite_score: 87.1, development_finance_neocolonial_conditionality_score: 89.0, technology_knowledge_transfer_exclusion_scale_score: 85.0, debt_trap_sovereignty_undermining_score: 87.0, sdg_implementation_inequality_gap_score: 87.0, risk_level: "critique", primary_pattern: "development_finance_neocolonial_conditionality", estimated_right_to_development_index: 8.71, last_updated: "2026-06-21" },
    { id: "RTD-004", name: "Sahel — Accords EPA UE Bloquant Industrialisation, Dumping Agricole & Marché Fermé Produits Locaux", country: "Sahel", composite_score: 84.05, development_finance_neocolonial_conditionality_score: 86.0, technology_knowledge_transfer_exclusion_scale_score: 83.0, debt_trap_sovereignty_undermining_score: 82.0, sdg_implementation_inequality_gap_score: 85.0, risk_level: "critique", primary_pattern: "development_finance_neocolonial_conditionality", estimated_right_to_development_index: 8.41, last_updated: "2026-06-21" },
    { id: "RTD-005", name: "Asie du Sud/Bangladesh — Propriété Intellectuelle TRIPS Médicaments Génériques, Semences Brevets & Transfert Technologie Refusé", country: "Asie du Sud", composite_score: 53.4, development_finance_neocolonial_conditionality_score: 52.0, technology_knowledge_transfer_exclusion_scale_score: 58.0, debt_trap_sovereignty_undermining_score: 50.0, sdg_implementation_inequality_gap_score: 54.0, risk_level: "élevé", primary_pattern: "technology_knowledge_transfer_exclusion_scale", estimated_right_to_development_index: 5.34, last_updated: "2026-06-21" },
    { id: "RTD-006", name: "Amérique Latine — Traités Investissement ISDS vs Politiques Publiques, Nationalisations Pénalisées & Souveraineté Normative", country: "Amérique Latine", composite_score: 51.15, development_finance_neocolonial_conditionality_score: 50.0, technology_knowledge_transfer_exclusion_scale_score: 48.0, debt_trap_sovereignty_undermining_score: 55.0, sdg_implementation_inequality_gap_score: 52.0, risk_level: "élevé", primary_pattern: "debt_trap_sovereignty_undermining", estimated_right_to_development_index: 5.12, last_updated: "2026-06-21" },
    { id: "RTD-007", name: "G77/UNCTAD — Coalition Sud Global, Commerce Équitable, Réforme Institutions Bretton Woods & Standards NIEO", country: "Global", composite_score: 26.25, development_finance_neocolonial_conditionality_score: 26.0, technology_knowledge_transfer_exclusion_scale_score: 28.0, debt_trap_sovereignty_undermining_score: 25.0, sdg_implementation_inequality_gap_score: 26.0, risk_level: "modéré", primary_pattern: "technology_knowledge_transfer_exclusion_scale", estimated_right_to_development_index: 2.63, last_updated: "2026-06-21" },
    { id: "RTD-008", name: "ONU/Déclaration 1986 — Déclaration Droit Développement, Résolution 41/128 & SDG 17 Partenariats", country: "Global", composite_score: 4.2, development_finance_neocolonial_conditionality_score: 4.0, technology_knowledge_transfer_exclusion_scale_score: 4.0, debt_trap_sovereignty_undermining_score: 4.0, sdg_implementation_inequality_gap_score: 5.0, risk_level: "faible", primary_pattern: "sdg_implementation_inequality_gap", estimated_right_to_development_index: 0.42, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/right-to-development-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
