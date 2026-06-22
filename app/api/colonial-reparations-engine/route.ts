import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[colonial-reparations-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Colonial Reparations Engine Agent",
  domain: "colonial_reparations",
  total_entities: 8,
  avg_composite: 60.61,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { economic_extraction_scale: 2, cultural_artifact_restitution_gap: 2, structural_inequality_persistence: 2, political_acknowledgment_refusal: 2 },
  top_risk_entities: [
    "Congo/Belgique — Extraction Caoutchouc/Minéraux, 10M Morts & Déni Réparations Léopold II",
    "Inde/UK — Pillage East India Company, Famine Bengal & Refus Reconnaissance Dette Coloniale",
    "Caraïbes/France — Esclavage 250 Ans, Dette Haïti 1825 & Silence Officiel Réparations",
  ],
  critical_alerts: [
    "Congo/Belgique: economic_extraction_scale",
    "Inde/UK: cultural_artifact_restitution_gap",
    "Caraïbes/France: structural_inequality_persistence",
    "Afrique Ouest/France: structural_inequality_persistence",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_colonial_reparations_index: 6.06,
  data_sources: [
    "un_durban_declaration_programme_action_reparations_review",
    "caricom_reparations_commission_ten_point_plan_report",
    "colonial_crimes_accountability_coalition_global_audit",
  ],
  entities: [
    { id: "CR-001", name: "Congo/Belgique — Extraction Caoutchouc/Minéraux, 10M Morts & Déni Réparations Léopold II", country: "Afrique Centrale", composite_score: 91.5, economic_extraction_scale_score: 95.0, cultural_artifact_restitution_gap_score: 88.0, structural_inequality_persistence_score: 92.0, political_acknowledgment_refusal_score: 90.0, risk_level: "critique", primary_pattern: "economic_extraction_scale", estimated_colonial_reparations_index: 9.15, last_updated: "2026-06-21" },
    { id: "CR-002", name: "Inde/UK — Pillage East India Company, Famine Bengal & Refus Reconnaissance Dette Coloniale", country: "Asie du Sud", composite_score: 89.7, economic_extraction_scale_score: 92.0, cultural_artifact_restitution_gap_score: 90.0, structural_inequality_persistence_score: 88.0, political_acknowledgment_refusal_score: 88.0, risk_level: "critique", primary_pattern: "cultural_artifact_restitution_gap", estimated_colonial_reparations_index: 8.97, last_updated: "2026-06-21" },
    { id: "CR-003", name: "Caraïbes/France — Esclavage 250 Ans, Dette Haïti 1825 & Silence Officiel Réparations", country: "Caraïbes", composite_score: 86.4, economic_extraction_scale_score: 88.0, cultural_artifact_restitution_gap_score: 82.0, structural_inequality_persistence_score: 90.0, political_acknowledgment_refusal_score: 85.0, risk_level: "critique", primary_pattern: "structural_inequality_persistence", estimated_colonial_reparations_index: 8.64, last_updated: "2026-06-21" },
    { id: "CR-004", name: "Afrique Ouest/France — CFA Franc Néocolonial, Ressources Extractées & Ingérence Politique", country: "Afrique de l'Ouest", composite_score: 82.5, economic_extraction_scale_score: 82.0, cultural_artifact_restitution_gap_score: 78.0, structural_inequality_persistence_score: 88.0, political_acknowledgment_refusal_score: 82.0, risk_level: "critique", primary_pattern: "structural_inequality_persistence", estimated_colonial_reparations_index: 8.25, last_updated: "2026-06-21" },
    { id: "CR-005", name: "USA — Esclavage/Jim Crow, Réparations HR40 Bloquées & Inégalités Raciales Persistantes", country: "Amérique du Nord", composite_score: 53.6, economic_extraction_scale_score: 52.0, cultural_artifact_restitution_gap_score: 50.0, structural_inequality_persistence_score: 58.0, political_acknowledgment_refusal_score: 55.0, risk_level: "élevé", primary_pattern: "political_acknowledgment_refusal", estimated_colonial_reparations_index: 5.36, last_updated: "2026-06-21" },
    { id: "CR-006", name: "Allemagne/Namibie — Génocide Herero 1904, Accord 2021 Insuffisant & Descendants Exclus", country: "Afrique Australe", composite_score: 50.9, economic_extraction_scale_score: 48.0, cultural_artifact_restitution_gap_score: 52.0, structural_inequality_persistence_score: 50.0, political_acknowledgment_refusal_score: 55.0, risk_level: "élevé", primary_pattern: "political_acknowledgment_refusal", estimated_colonial_reparations_index: 5.09, last_updated: "2026-06-21" },
    { id: "CR-007", name: "CARICOM — Alliance 14 Nations, Plan Réparations 10 Points & Plaidoyer ONU", country: "Global", composite_score: 25.85, economic_extraction_scale_score: 22.0, cultural_artifact_restitution_gap_score: 28.0, structural_inequality_persistence_score: 25.0, political_acknowledgment_refusal_score: 30.0, risk_level: "modéré", primary_pattern: "economic_extraction_scale", estimated_colonial_reparations_index: 2.59, last_updated: "2026-06-21" },
    { id: "CR-008", name: "ONU/Déclaration Durban — Conférence Anti-Racisme 2001, Suivi & Mécanismes Révision", country: "Global", composite_score: 4.4, economic_extraction_scale_score: 4.0, cultural_artifact_restitution_gap_score: 5.0, structural_inequality_persistence_score: 3.0, political_acknowledgment_refusal_score: 6.0, risk_level: "faible", primary_pattern: "cultural_artifact_restitution_gap", estimated_colonial_reparations_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/colonial-reparations-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
