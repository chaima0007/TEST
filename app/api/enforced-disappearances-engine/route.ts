import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[enforced-disappearances-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Enforced Disappearances Engine Agent",
  domain: "enforced_disappearances",
  total_entities: 8,
  avg_composite: 61.63,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { state_perpetrated_disappearance_severity: 2, impunity_accountability_absence_scale: 2, family_right_to_truth_obstruction: 3, legal_framework_prevention_gap: 1 },
  top_risk_entities: [
    "Mexique — 100 000+ Disparus, Cartels+État Complicité, Registre RENPED & Fosses Communes 4 000+",
    "Syrie — 150 000+ Disparus Depuis 2011, Détention Assad Secrète, Torture & Zéro Responsabilité",
    "Corée du Nord — Disparitions Politiques Généralisées, Camps Kwanliso, Familles Sans Information",
  ],
  critical_alerts: [
    "Mexique: state_perpetrated_disappearance_severity",
    "Syrie: impunity_accountability_absence_scale",
    "Corée du Nord: family_right_to_truth_obstruction",
    "Chili/Argent Legacy: impunity_accountability_absence_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_enforced_disappearances_index: 6.16,
  data_sources: [
    "un_committee_on_enforced_disappearances_reports",
    "amnesty_international_enforced_disappearances_global",
    "fedefam_latin_america_missing_persons_database",
  ],
  entities: [
    { id: "EDE-001", name: "Mexique — 100 000+ Disparus, Cartels+État Complicité, Registre RENPED & Fosses Communes 4 000+", country: "Mexique", composite_score: 93.95, state_perpetrated_disappearance_severity_score: 96.0, impunity_accountability_absence_scale_score: 93.0, family_right_to_truth_obstruction_score: 94.0, legal_framework_prevention_gap_score: 92.0, risk_level: "critique", primary_pattern: "state_perpetrated_disappearance_severity", estimated_enforced_disappearances_index: 9.40, last_updated: "2026-06-21" },
    { id: "EDE-002", name: "Syrie — 150 000+ Disparus Depuis 2011, Détention Assad Secrète, Torture & Zéro Responsabilité", country: "Syrie", composite_score: 90.95, state_perpetrated_disappearance_severity_score: 93.0, impunity_accountability_absence_scale_score: 90.0, family_right_to_truth_obstruction_score: 91.0, legal_framework_prevention_gap_score: 89.0, risk_level: "critique", primary_pattern: "impunity_accountability_absence_scale", estimated_enforced_disappearances_index: 9.10, last_updated: "2026-06-21" },
    { id: "EDE-003", name: "Corée du Nord — Disparitions Politiques Généralisées, Camps Kwanliso, Familles Sans Information", country: "Corée du Nord", composite_score: 87.95, state_perpetrated_disappearance_severity_score: 90.0, impunity_accountability_absence_scale_score: 87.0, family_right_to_truth_obstruction_score: 88.0, legal_framework_prevention_gap_score: 86.0, risk_level: "critique", primary_pattern: "family_right_to_truth_obstruction", estimated_enforced_disappearances_index: 8.80, last_updated: "2026-06-21" },
    { id: "EDE-004", name: "Chili/Argent Legacy — 30 000 Argentins Disparus Dictature, Impunité Partielle & Bébés Volés", country: "Chili/Argentine", composite_score: 84.95, state_perpetrated_disappearance_severity_score: 87.0, impunity_accountability_absence_scale_score: 84.0, family_right_to_truth_obstruction_score: 85.0, legal_framework_prevention_gap_score: 83.0, risk_level: "critique", primary_pattern: "impunity_accountability_absence_scale", estimated_enforced_disappearances_index: 8.50, last_updated: "2026-06-21" },
    { id: "EDE-005", name: "Philippines — 1 200+ Disparus Guerre Drogues Duterte, Red-Tagging & Zéro Enquête", country: "Philippines", composite_score: 53.95, state_perpetrated_disappearance_severity_score: 56.0, impunity_accountability_absence_scale_score: 53.0, family_right_to_truth_obstruction_score: 54.0, legal_framework_prevention_gap_score: 52.0, risk_level: "élevé", primary_pattern: "state_perpetrated_disappearance_severity", estimated_enforced_disappearances_index: 5.40, last_updated: "2026-06-21" },
    { id: "EDE-006", name: "Sri Lanka/Birmanie — Post-Guerre LTTE 12 000 Disparus, Militaires Impunis & Familles Obstruction", country: "Sri Lanka/Myanmar", composite_score: 51.2, state_perpetrated_disappearance_severity_score: 53.0, impunity_accountability_absence_scale_score: 51.0, family_right_to_truth_obstruction_score: 51.0, legal_framework_prevention_gap_score: 49.0, risk_level: "élevé", primary_pattern: "family_right_to_truth_obstruction", estimated_enforced_disappearances_index: 5.12, last_updated: "2026-06-21" },
    { id: "EDE-007", name: "FEDEFAM/ICAED — Familles Disparus LATAM, Comité ONU CED & Mécanismes Vérité-Justice", country: "Global", composite_score: 26.1, state_perpetrated_disappearance_severity_score: 27.0, impunity_accountability_absence_scale_score: 26.0, family_right_to_truth_obstruction_score: 26.0, legal_framework_prevention_gap_score: 25.0, risk_level: "modéré", primary_pattern: "family_right_to_truth_obstruction", estimated_enforced_disappearances_index: 2.61, last_updated: "2026-06-21" },
    { id: "EDE-008", name: "ONU/Convention CED — Convention Disparitions Forcées 2006, Comité CED & SDG 16.3 Justice", country: "Global", composite_score: 4.0, state_perpetrated_disappearance_severity_score: 4.0, impunity_accountability_absence_scale_score: 4.0, family_right_to_truth_obstruction_score: 4.0, legal_framework_prevention_gap_score: 4.0, risk_level: "faible", primary_pattern: "legal_framework_prevention_gap", estimated_enforced_disappearances_index: 0.40, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/enforced-disappearances-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
