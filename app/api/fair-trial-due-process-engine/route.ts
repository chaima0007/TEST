import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[fair-trial-due-process-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Fair Trial Due Process Engine Agent",
  domain: "fair_trial_due_process",
  total_entities: 8,
  avg_composite: 61.64,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { forced_confession_torture_evidence_severity: 2, secret_trial_mass_prosecution_scale: 2, legal_representation_denial_obstruction: 2, presumption_innocence_pretrial_violation_gap: 2 },
  top_risk_entities: [
    "Chine — Tribunaux Secrets Xinjiang, Avocats Droits Humains 709 Arrêtés, Aveux Télévisés Forcés & Taux Condamnation 99.9%",
    "Égypte/Sissi — Tribunaux Militaires Civils, 60 000 Prisonniers Politiques, Avocats Détenus & Audiences Mass 50+ Accusés",
    "Iran — Tribunaux Révolutionnaires, Exécutions Express Manifestants, Avocats Condamnés & Aveux Sous Torture Diffusés TV",
  ],
  critical_alerts: [
    "Chine: forced_confession_torture_evidence_severity",
    "Égypte/Sissi: secret_trial_mass_prosecution_scale",
    "Iran: forced_confession_torture_evidence_severity",
    "Arabie Saoudite: legal_representation_denial_obstruction",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_fair_trial_due_process_index: 6.16,
  data_sources: [
    "fair_trials_international_monitoring_report",
    "amnesty_international_torture_evidence_report",
    "icc_due_process_standards_review",
  ],
  entities: [
    { id: "FTD-001", name: "Chine — Tribunaux Secrets Xinjiang, Avocats Droits Humains 709 Arrêtés, Aveux Télévisés Forcés & Taux Condamnation 99.9%", country: "Chine", composite_score: 93.75, forced_confession_torture_evidence_severity_score: 96.0, secret_trial_mass_prosecution_scale_score: 94.0, legal_representation_denial_obstruction_score: 93.0, presumption_innocence_pretrial_violation_gap_score: 91.0, risk_level: "critique", primary_pattern: "forced_confession_torture_evidence_severity", estimated_fair_trial_due_process_index: 9.38, last_updated: "2026-06-21" },
    { id: "FTD-002", name: "Égypte/Sissi — Tribunaux Militaires Civils, 60 000 Prisonniers Politiques, Avocats Détenus & Audiences Mass 50+ Accusés", country: "Égypte", composite_score: 90.2, forced_confession_torture_evidence_severity_score: 92.0, secret_trial_mass_prosecution_scale_score: 91.0, legal_representation_denial_obstruction_score: 89.0, presumption_innocence_pretrial_violation_gap_score: 88.0, risk_level: "critique", primary_pattern: "secret_trial_mass_prosecution_scale", estimated_fair_trial_due_process_index: 9.02, last_updated: "2026-06-21" },
    { id: "FTD-003", name: "Iran — Tribunaux Révolutionnaires, Exécutions Express Manifestants, Avocats Condamnés & Aveux Sous Torture Diffusés TV", country: "Iran", composite_score: 87.25, forced_confession_torture_evidence_severity_score: 90.0, secret_trial_mass_prosecution_scale_score: 87.0, legal_representation_denial_obstruction_score: 86.0, presumption_innocence_pretrial_violation_gap_score: 85.0, risk_level: "critique", primary_pattern: "forced_confession_torture_evidence_severity", estimated_fair_trial_due_process_index: 8.73, last_updated: "2026-06-21" },
    { id: "FTD-004", name: "Arabie Saoudite — Tribunal Pénal Spécial Terrorisme, Militants Droits Humains, Femmes Activistes Jugées en Secret & Peine Mort Mineurs", country: "Arabie Saoudite", composite_score: 84.2, forced_confession_torture_evidence_severity_score: 86.0, secret_trial_mass_prosecution_scale_score: 85.0, legal_representation_denial_obstruction_score: 83.0, presumption_innocence_pretrial_violation_gap_score: 82.0, risk_level: "critique", primary_pattern: "legal_representation_denial_obstruction", estimated_fair_trial_due_process_index: 8.42, last_updated: "2026-06-21" },
    { id: "FTD-005", name: "Russie — Tribunaux Kangaroo Navalny/Kara-Murza, Avocats Défense Radiés, Audiences Pénitentiaires & Mass Procès Manifestants", country: "Russie", composite_score: 54.95, forced_confession_torture_evidence_severity_score: 57.0, secret_trial_mass_prosecution_scale_score: 55.0, legal_representation_denial_obstruction_score: 54.0, presumption_innocence_pretrial_violation_gap_score: 53.0, risk_level: "élevé", primary_pattern: "secret_trial_mass_prosecution_scale", estimated_fair_trial_due_process_index: 5.5, last_updated: "2026-06-21" },
    { id: "FTD-006", name: "USA — Guantanamo 20+ Ans Sans Procès, Plea Deals Coercitifs, Accusés Pauvres Défense Publique Débordée & Peine Mort Erreurs", country: "USA", composite_score: 52.15, forced_confession_torture_evidence_severity_score: 53.0, secret_trial_mass_prosecution_scale_score: 52.0, legal_representation_denial_obstruction_score: 53.0, presumption_innocence_pretrial_violation_gap_score: 50.0, risk_level: "élevé", primary_pattern: "presumption_innocence_pretrial_violation_gap", estimated_fair_trial_due_process_index: 5.22, last_updated: "2026-06-21" },
    { id: "FTD-007", name: "Fair Trials International/DPLF — Monitoring Procès, Standards Hambourg & Recours Individuels Droits Humains", country: "Global", composite_score: 26.65, forced_confession_torture_evidence_severity_score: 28.0, secret_trial_mass_prosecution_scale_score: 27.0, legal_representation_denial_obstruction_score: 26.0, presumption_innocence_pretrial_violation_gap_score: 25.0, risk_level: "modéré", primary_pattern: "legal_representation_denial_obstruction", estimated_fair_trial_due_process_index: 2.67, last_updated: "2026-06-21" },
    { id: "FTD-008", name: "ONU/CCPR Art.14 — Procès Équitable PIDCP, Présomption Innocence, Assistance Juridique Gratuite & SDG 16.3", country: "Global", composite_score: 4.0, forced_confession_torture_evidence_severity_score: 4.0, secret_trial_mass_prosecution_scale_score: 4.0, legal_representation_denial_obstruction_score: 4.0, presumption_innocence_pretrial_violation_gap_score: 4.0, risk_level: "faible", primary_pattern: "presumption_innocence_pretrial_violation_gap", estimated_fair_trial_due_process_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/fair-trial-due-process-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
