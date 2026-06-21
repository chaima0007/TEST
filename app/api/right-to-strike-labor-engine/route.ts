import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[right-to-strike-labor-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Right to Strike Labor Engine Agent",
  domain: "right_to_strike_labor",
  total_entities: 8,
  avg_composite: 61.44,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { strike_prohibition_criminalization_severity: 3, union_busting_retaliation_workers: 2, essential_services_overclassification_scope_scale: 2, precarious_workers_strike_exclusion_gap: 1 },
  top_risk_entities: [
    "Chine/Vietnam — Grèves Illégales Officiellement, 300+ Grèves/An Réprimées Foxconn/Nike, Syndicalistes Arrêtés & ACFTU Contrôlé État",
    "Arabie Saoudite/Qatar — Grèves Totalement Interdites, Travailleurs Migrants Deportés si Grève, Kafala & Syndicats Criminalisés",
    "Bangladesh/Rana Plaza Aftermath — Grèves Réprimées Usines Vêtements, Licenciements Organisateurs, Police Anti-Grève & Peur Représailles",
  ],
  critical_alerts: [
    "Chine/Vietnam: strike_prohibition_criminalization_severity",
    "Arabie Saoudite/Qatar: strike_prohibition_criminalization_severity",
    "Bangladesh/Rana Plaza Aftermath: union_busting_retaliation_workers",
    "Colombie/Amérique Latine: union_busting_retaliation_workers",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_right_to_strike_labor_index: 6.14,
  data_sources: [
    "ituc_global_rights_index_annual_report",
    "ilo_convention_87_98_compliance_monitoring",
    "human_rights_watch_labor_rights_global_survey",
  ],
  entities: [
    { id: "RSL-001", name: "Chine/Vietnam — Grèves Illégales Officiellement, 300+ Grèves/An Réprimées Foxconn/Nike, Syndicalistes Arrêtés & ACFTU Contrôlé État", country: "Chine/Vietnam", composite_score: 92.95, strike_prohibition_criminalization_severity_score: 95.0, essential_services_overclassification_scope_scale_score: 93.0, union_busting_retaliation_workers_score: 92.0, precarious_workers_strike_exclusion_gap_score: 91.0, risk_level: "critique", primary_pattern: "strike_prohibition_criminalization_severity", estimated_right_to_strike_labor_index: 9.30, last_updated: "2026-06-21" },
    { id: "RSL-002", name: "Arabie Saoudite/Qatar — Grèves Totalement Interdites, Travailleurs Migrants Deportés si Grève, Kafala & Syndicats Criminalisés", country: "Arabie Saoudite/Qatar", composite_score: 89.85, strike_prohibition_criminalization_severity_score: 92.0, essential_services_overclassification_scope_scale_score: 89.0, union_busting_retaliation_workers_score: 88.0, precarious_workers_strike_exclusion_gap_score: 90.0, risk_level: "critique", primary_pattern: "strike_prohibition_criminalization_severity", estimated_right_to_strike_labor_index: 8.99, last_updated: "2026-06-21" },
    { id: "RSL-003", name: "Bangladesh/Rana Plaza Aftermath — Grèves Réprimées Usines Vêtements, Licenciements Organisateurs, Police Anti-Grève & Peur Représailles", country: "Bangladesh", composite_score: 86.90, strike_prohibition_criminalization_severity_score: 89.0, essential_services_overclassification_scope_scale_score: 86.0, union_busting_retaliation_workers_score: 86.0, precarious_workers_strike_exclusion_gap_score: 86.0, risk_level: "critique", primary_pattern: "union_busting_retaliation_workers", estimated_right_to_strike_labor_index: 8.69, last_updated: "2026-06-21" },
    { id: "RSL-004", name: "Colombie/Amérique Latine — 3 000 Syndicalistes Assassinés 1986-2023, Grèves Minières Réprimées Armée & Impunité Tueurs", country: "Colombie", composite_score: 83.85, strike_prohibition_criminalization_severity_score: 86.0, essential_services_overclassification_scope_scale_score: 83.0, union_busting_retaliation_workers_score: 82.0, precarious_workers_strike_exclusion_gap_score: 84.0, risk_level: "critique", primary_pattern: "union_busting_retaliation_workers", estimated_right_to_strike_labor_index: 8.39, last_updated: "2026-06-21" },
    { id: "RSL-005", name: "UK Post-2023 — Strikes Act 2023 Minimum Service Levels, Transport/Santé Grèves Restreintes & Sanctions Anti-Grévistes", country: "Royaume-Uni", composite_score: 54.85, strike_prohibition_criminalization_severity_score: 57.0, essential_services_overclassification_scope_scale_score: 54.0, union_busting_retaliation_workers_score: 53.0, precarious_workers_strike_exclusion_gap_score: 55.0, risk_level: "élevé", primary_pattern: "essential_services_overclassification_scope_scale", estimated_right_to_strike_labor_index: 5.49, last_updated: "2026-06-21" },
    { id: "RSL-006", name: "USA — Taft-Hartley Interdictions Syndicats, Amazon/Starbucks Union Busting, Grévistes Remplacés Permanents & Gig Workers Exclus", country: "USA", composite_score: 51.85, strike_prohibition_criminalization_severity_score: 54.0, essential_services_overclassification_scope_scale_score: 51.0, union_busting_retaliation_workers_score: 50.0, precarious_workers_strike_exclusion_gap_score: 52.0, risk_level: "élevé", primary_pattern: "precarious_workers_strike_exclusion_gap", estimated_right_to_strike_labor_index: 5.19, last_updated: "2026-06-21" },
    { id: "RSL-007", name: "ITUC/CSI — Indice Mondial Droits Syndicaux, Cas Violations & Plaidoyer ILO Convention 87/98", country: "Global", composite_score: 27.05, strike_prohibition_criminalization_severity_score: 28.0, essential_services_overclassification_scope_scale_score: 26.0, union_busting_retaliation_workers_score: 27.0, precarious_workers_strike_exclusion_gap_score: 27.0, risk_level: "modéré", primary_pattern: "strike_prohibition_criminalization_severity", estimated_right_to_strike_labor_index: 2.71, last_updated: "2026-06-21" },
    { id: "RSL-008", name: "OIT/C087-C098 — Convention Liberté Syndicale 87, Droit Organisation Collective 98 & SDG 8.8 Droits Travail", country: "Global", composite_score: 4.25, strike_prohibition_criminalization_severity_score: 4.0, essential_services_overclassification_scope_scale_score: 4.0, union_busting_retaliation_workers_score: 5.0, precarious_workers_strike_exclusion_gap_score: 4.0, risk_level: "faible", primary_pattern: "essential_services_overclassification_scope_scale", estimated_right_to_strike_labor_index: 0.43, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/right-to-strike-labor-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
