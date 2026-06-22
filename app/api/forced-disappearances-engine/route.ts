import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[forced-disappearances-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Forced Disappearances Engine Agent",
  domain: "forced_disappearances",
  total_entities: 8,
  avg_composite: 60.3,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { state_perpetration_scale: 2, body_concealment_impunity: 2, family_search_obstruction: 2, truth_justice_mechanism_gap: 2 },
  top_risk_entities: [
    "Syrie — 100K+ Disparus Régime Assad, Prisons Secrètes Saydnaya & Fosses Communes",
    "Mexique — 110K Disparus Cartels/État, Fossés Communs & FNAILEP Sans Résultats",
    "Égypte — Disparitions Post-2013, Sisi Opposants/Journalistes & Déni Détentions Secrètes",
  ],
  critical_alerts: [
    "Syrie: state_perpetration_scale",
    "Mexique: body_concealment_impunity",
    "Égypte: family_search_obstruction",
    "Argentine/Mémoire: truth_justice_mechanism_gap",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_forced_disappearances_index: 6.03,
  data_sources: [
    "icmp_international_commission_missing_persons_annual_report",
    "amnesty_international_enforced_disappearances_global_report",
    "un_committee_ced_enforced_disappearances_session_reports",
  ],
  entities: [
    { id: "FD-001", name: "Syrie — 100K+ Disparus Régime Assad, Prisons Secrètes Saydnaya & Fosses Communes", country: "Moyen-Orient", composite_score: 92.4, state_perpetration_scale_score: 95.0, body_concealment_impunity_score: 92.0, family_search_obstruction_score: 90.0, truth_justice_mechanism_gap_score: 92.0, risk_level: "critique", primary_pattern: "state_perpetration_scale", estimated_forced_disappearances_index: 9.24, last_updated: "2026-06-20" },
    { id: "FD-002", name: "Mexique — 110K Disparus Cartels/État, Fossés Communs & FNAILEP Sans Résultats", country: "Amérique du Nord", composite_score: 87.75, state_perpetration_scale_score: 88.0, body_concealment_impunity_score: 90.0, family_search_obstruction_score: 85.0, truth_justice_mechanism_gap_score: 88.0, risk_level: "critique", primary_pattern: "body_concealment_impunity", estimated_forced_disappearances_index: 8.78, last_updated: "2026-06-20" },
    { id: "FD-003", name: "Égypte — Disparitions Post-2013, Sisi Opposants/Journalistes & Déni Détentions Secrètes", country: "Afrique du Nord", composite_score: 85.0, state_perpetration_scale_score: 85.0, body_concealment_impunity_score: 82.0, family_search_obstruction_score: 88.0, truth_justice_mechanism_gap_score: 85.0, risk_level: "critique", primary_pattern: "family_search_obstruction", estimated_forced_disappearances_index: 8.5, last_updated: "2026-06-20" },
    { id: "FD-004", name: "Argentine/Mémoire — 30K Disparus Dictature 1976-83, ESMA & Lucha Abuelas Plaza Mayo", country: "Amérique Latine", composite_score: 81.1, state_perpetration_scale_score: 82.0, body_concealment_impunity_score: 78.0, family_search_obstruction_score: 80.0, truth_justice_mechanism_gap_score: 85.0, risk_level: "critique", primary_pattern: "truth_justice_mechanism_gap", estimated_forced_disappearances_index: 8.11, last_updated: "2026-06-20" },
    { id: "FD-005", name: "Chine/Xinjiang — Disparitions Ouïghours, Détentions Secrètes Camps & Familles Sans Nouvelles", country: "Asie du Nord-Est", composite_score: 55.0, state_perpetration_scale_score: 55.0, body_concealment_impunity_score: 52.0, family_search_obstruction_score: 58.0, truth_justice_mechanism_gap_score: 55.0, risk_level: "élevé", primary_pattern: "family_search_obstruction", estimated_forced_disappearances_index: 5.5, last_updated: "2026-06-20" },
    { id: "FD-006", name: "Colombie — Paramilitaires/FARC Disparus, Unité Recherche Personnes Desaparecidas & Paix Partielle", country: "Amérique Latine", composite_score: 50.9, state_perpetration_scale_score: 48.0, body_concealment_impunity_score: 52.0, family_search_obstruction_score: 50.0, truth_justice_mechanism_gap_score: 55.0, risk_level: "élevé", primary_pattern: "truth_justice_mechanism_gap", estimated_forced_disappearances_index: 5.09, last_updated: "2026-06-20" },
    { id: "FD-007", name: "FEDEFAM/ICMP — Fédération Familles Disparus, Identification ADN & Plaidoyer International", country: "Global", composite_score: 25.85, state_perpetration_scale_score: 22.0, body_concealment_impunity_score: 25.0, family_search_obstruction_score: 28.0, truth_justice_mechanism_gap_score: 30.0, risk_level: "modéré", primary_pattern: "state_perpetration_scale", estimated_forced_disappearances_index: 2.59, last_updated: "2026-06-20" },
    { id: "FD-008", name: "ONU/Convention 2006 — Déclaration Disparitions Forcées, Comité CED & Rapports Périodiques", country: "Global", composite_score: 4.4, state_perpetration_scale_score: 4.0, body_concealment_impunity_score: 5.0, family_search_obstruction_score: 3.0, truth_justice_mechanism_gap_score: 6.0, risk_level: "faible", primary_pattern: "body_concealment_impunity", estimated_forced_disappearances_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/forced-disappearances-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
