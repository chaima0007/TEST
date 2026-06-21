import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[pretrial-detention-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Pretrial Detention Engine Agent",
  domain: "pretrial_detention",
  total_entities: 8,
  avg_composite: 61.38,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { detention_duration_excess: 1, presumption_innocence_violation: 2, inhumane_conditions: 2, legal_access_denial: 3 },
  top_risk_entities: [
    "Philippines — Geôles 500%+ Surpeuplées, Détention Préventive 5 Ans Moy. & Torture Documentée",
    "RDC — Cachots Illégaux, 80%+ Prévenus Sans Jugement & Détention Arbitraire Systémique",
    "Haïti — Pénitencier National Effondré, Gangs Contrôlent Prisons & ONU 98% Prévenus",
  ],
  critical_alerts: [
    "Philippines: detention_duration_excess",
    "RDC: presumption_innocence_violation",
    "Haïti: inhumane_conditions",
    "Mexique: legal_access_denial",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_pretrial_detention_index: 6.14,
  data_sources: [
    "fair_trials_international_pretrial_detention_global_report",
    "penal_reform_international_global_prison_trends",
    "un_working_group_arbitrary_detention_annual_report",
  ],
  entities: [
    { entity_id: "PD-001", name: "Philippines — Geôles 500%+ Surpeuplées, Détention Préventive 5 Ans Moy. & Torture Documentée", country: "Asie du Sud-Est", composite_score: 93.25, detention_duration_excess_score: 95.0, inhumane_conditions_score: 95.0, legal_access_denial_score: 92.0, presumption_innocence_violation_score: 90.0, risk_level: "critique", primary_pattern: "detention_duration_excess", estimated_pretrial_detention_index: 9.33, last_updated: "2026-06-21" },
    { entity_id: "PD-002", name: "RDC — Cachots Illégaux, 80%+ Prévenus Sans Jugement & Détention Arbitraire Systémique", country: "Afrique Centrale", composite_score: 90.5, detention_duration_excess_score: 92.0, inhumane_conditions_score: 90.0, legal_access_denial_score: 88.0, presumption_innocence_violation_score: 92.0, risk_level: "critique", primary_pattern: "presumption_innocence_violation", estimated_pretrial_detention_index: 9.05, last_updated: "2026-06-21" },
    { entity_id: "PD-003", name: "Haïti — Pénitencier National Effondré, Gangs Contrôlent Prisons & ONU 98% Prévenus", country: "Caraïbes", composite_score: 88.25, detention_duration_excess_score: 88.0, inhumane_conditions_score: 92.0, legal_access_denial_score: 85.0, presumption_innocence_violation_score: 88.0, risk_level: "critique", primary_pattern: "inhumane_conditions", estimated_pretrial_detention_index: 8.83, last_updated: "2026-06-21" },
    { entity_id: "PD-004", name: "Mexique — Arraigo 80 Jours Légal, 40%+ Prévenus & Corruption Judiciaire Systémique", country: "Amérique Latine", composite_score: 85.0, detention_duration_excess_score: 85.0, inhumane_conditions_score: 82.0, legal_access_denial_score: 88.0, presumption_innocence_violation_score: 85.0, risk_level: "critique", primary_pattern: "legal_access_denial", estimated_pretrial_detention_index: 8.5, last_updated: "2026-06-21" },
    { entity_id: "PD-005", name: "USA — Rikers Island, Cash Bail Système Pauvres, Kalief Browder 3 Ans Rikers Mineur", country: "Amérique du Nord", composite_score: 54.25, detention_duration_excess_score: 52.0, inhumane_conditions_score: 55.0, legal_access_denial_score: 58.0, presumption_innocence_violation_score: 52.0, risk_level: "élevé", primary_pattern: "legal_access_denial", estimated_pretrial_detention_index: 5.43, last_updated: "2026-06-21" },
    { entity_id: "PD-006", name: "France — Détention Provisoire 30%+ Population Carcérale, MAJ Prolongés & Surpopulation", country: "Europe", composite_score: 49.5, detention_duration_excess_score: 48.0, inhumane_conditions_score: 52.0, legal_access_denial_score: 50.0, presumption_innocence_violation_score: 48.0, risk_level: "élevé", primary_pattern: "inhumane_conditions", estimated_pretrial_detention_index: 4.95, last_updated: "2026-06-21" },
    { entity_id: "PD-007", name: "Fair Trials International/Penal Reform — Monitoring Détention Préventive & Plaidoyer", country: "Global", composite_score: 25.85, detention_duration_excess_score: 22.0, inhumane_conditions_score: 25.0, legal_access_denial_score: 28.0, presumption_innocence_violation_score: 30.0, risk_level: "modéré", primary_pattern: "presumption_innocence_violation", estimated_pretrial_detention_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "PD-008", name: "ONU/CCPR — Art.9 PIDCP Liberté Personne, Groupe Travail Détention Arbitraire", country: "Global", composite_score: 4.4, detention_duration_excess_score: 4.0, inhumane_conditions_score: 5.0, legal_access_denial_score: 3.0, presumption_innocence_violation_score: 6.0, risk_level: "faible", primary_pattern: "legal_access_denial", estimated_pretrial_detention_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/pretrial-detention-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
