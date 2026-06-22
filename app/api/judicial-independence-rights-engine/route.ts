import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[judicial-independence-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Judicial Independence Rights Engine Agent",
  domain: "judicial_independence_rights",
  total_entities: 8,
  avg_composite: 61.93,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { executive_judiciary_capture_severity: 5, judge_persecution_harassment_risk: 1, court_packing_restructuring_abuse_gap: 2 },
  top_risk_entities: [
    "Hongrie/Orbán — Réforme Constitutionnelle 2011-19, Cour Suprême Vidée, Procureur Général Allié & Juges Fidèles Nommés",
    "Turquie Post-2016 — 4 000 Juges Destitués Coup d'État, Tribunaux Spéciaux Terrorisme, Erdoğan Contrôle Judiciaire",
    "Venezuela/Maduro — CSJ Peuplée Chavistes, 100% Acquittements Demandés Exécutif, Juges Exil & Prisonniers Politiques",
  ],
  critical_alerts: [
    "Hongrie/Orbán: executive_judiciary_capture_severity",
    "Turquie Post-2016: judge_persecution_harassment_risk",
    "Venezuela/Maduro: executive_judiciary_capture_severity",
    "Pologne/PiS 2015-23: court_packing_restructuring_abuse_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_judicial_independence_rights_index: 6.19,
  data_sources: [
    "venice_commission_rule_of_law_reports",
    "icj_judicial_independence_standards",
    "amnesty_international_judicial_persecution_report",
  ],
  entities: [
    { id: "JIR-001", name: "Hongrie/Orbán — Réforme Constitutionnelle 2011-19, Cour Suprême Vidée, Procureur Général Allié & Juges Fidèles Nommés", country: "Hongrie", composite_score: 93.65, executive_judiciary_capture_severity_score: 96.0, judicial_appointment_politicization_scale_score: 94.0, judge_persecution_harassment_risk_score: 91.0, court_packing_restructuring_abuse_gap_score: 93.0, risk_level: "critique", primary_pattern: "executive_judiciary_capture_severity", estimated_judicial_independence_rights_index: 9.37, last_updated: "2026-06-21" },
    { id: "JIR-002", name: "Turquie Post-2016 — 4 000 Juges Destitués Coup d'État, Tribunaux Spéciaux Terrorisme, Erdoğan Contrôle Judiciaire", country: "Turquie", composite_score: 91.25, executive_judiciary_capture_severity_score: 93.0, judicial_appointment_politicization_scale_score: 91.0, judge_persecution_harassment_risk_score: 92.0, court_packing_restructuring_abuse_gap_score: 88.0, risk_level: "critique", primary_pattern: "judge_persecution_harassment_risk", estimated_judicial_independence_rights_index: 9.13, last_updated: "2026-06-21" },
    { id: "JIR-003", name: "Venezuela/Maduro — CSJ Peuplée Chavistes, 100% Acquittements Demandés Exécutif, Juges Exil & Prisonniers Politiques", country: "Venezuela", composite_score: 88.0, executive_judiciary_capture_severity_score: 91.0, judicial_appointment_politicization_scale_score: 89.0, judge_persecution_harassment_risk_score: 85.0, court_packing_restructuring_abuse_gap_score: 86.0, risk_level: "critique", primary_pattern: "executive_judiciary_capture_severity", estimated_judicial_independence_rights_index: 8.8, last_updated: "2026-06-21" },
    { id: "JIR-004", name: "Pologne/PiS 2015-23 — Tribunal Constitutionnel Paralysé, KRS Politisé, Sanctions EU Infringement & Réforme Réversée", country: "Pologne", composite_score: 84.9, executive_judiciary_capture_severity_score: 87.0, judicial_appointment_politicization_scale_score: 86.0, judge_persecution_harassment_risk_score: 82.0, court_packing_restructuring_abuse_gap_score: 84.0, risk_level: "critique", primary_pattern: "court_packing_restructuring_abuse_gap", estimated_judicial_independence_rights_index: 8.49, last_updated: "2026-06-21" },
    { id: "JIR-005", name: "Pakistan/Bangladesh — ISI Pression Magistrats, Arrêts Politiques Opportuns, Blasphème Poursuites & Avocats Attaqués", country: "Pakistan", composite_score: 54.75, executive_judiciary_capture_severity_score: 57.0, judicial_appointment_politicization_scale_score: 55.0, judge_persecution_harassment_risk_score: 54.0, court_packing_restructuring_abuse_gap_score: 52.0, risk_level: "élevé", primary_pattern: "executive_judiciary_capture_severity", estimated_judicial_independence_rights_index: 5.48, last_updated: "2026-06-21" },
    { id: "JIR-006", name: "USA/Trump 2025 — Tentatives Influence SCOTUS, Purge FBI/DOJ, Procureurs Spéciaux Révoqués & Juges Fédéraux Intimidés", country: "USA", composite_score: 52.2, executive_judiciary_capture_severity_score: 54.0, judicial_appointment_politicization_scale_score: 53.0, judge_persecution_harassment_risk_score: 51.0, court_packing_restructuring_abuse_gap_score: 50.0, risk_level: "élevé", primary_pattern: "executive_judiciary_capture_severity", estimated_judicial_independence_rights_index: 5.22, last_updated: "2026-06-21" },
    { id: "JIR-007", name: "ICJ/Venice Commission — Avis Conformité État de Droit, Indépendance Standards & Rapports Commission Venise", country: "Global", composite_score: 26.65, executive_judiciary_capture_severity_score: 28.0, judicial_appointment_politicization_scale_score: 27.0, judge_persecution_harassment_risk_score: 26.0, court_packing_restructuring_abuse_gap_score: 25.0, risk_level: "modéré", primary_pattern: "court_packing_restructuring_abuse_gap", estimated_judicial_independence_rights_index: 2.67, last_updated: "2026-06-21" },
    { id: "JIR-008", name: "ONU/CCPR — Principe Indépendance Judiciaire 1985, CCPR Art.14 Procès Équitable & SDG 16.3 Accès Justice", country: "Global", composite_score: 4.0, executive_judiciary_capture_severity_score: 4.0, judicial_appointment_politicization_scale_score: 4.0, judge_persecution_harassment_risk_score: 4.0, court_packing_restructuring_abuse_gap_score: 4.0, risk_level: "faible", primary_pattern: "executive_judiciary_capture_severity", estimated_judicial_independence_rights_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/judicial-independence-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
