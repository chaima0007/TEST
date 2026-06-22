import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[algorithmic-bias-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Algorithmic Bias Rights Engine Agent",
  domain: "algorithmic_bias_rights",
  total_entities: 8,
  avg_composite: 61.54,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { judicial_algorithmic_sentencing_gap: 2, predictive_policing_racial_bias_scale: 2, employment_housing_algorithmic_exclusion_severity: 2, algorithmic_transparency_right_explanation_absence: 2 },
  top_risk_entities: [
    "USA/COMPAS — Récidivisme Biaisé Justice, Crédit Score Racial & Algorithmes RH Discriminatoires",
    "Chine — Score Social Emploi Ethnique, Algorithmes Surveillance Citoyens & Notation Comportement",
    "UK — PredPol Police Prédictive, Algorithmes DWP Prestations & Windrush Biais Systémique",
  ],
  critical_alerts: [
    "USA/COMPAS: judicial_algorithmic_sentencing_gap",
    "Chine: predictive_policing_racial_bias_scale",
    "UK: employment_housing_algorithmic_exclusion_severity",
    "Pays en Développement: employment_housing_algorithmic_exclusion_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_algorithmic_bias_rights_index: 6.15,
  data_sources: [
    "algorithmic_justice_league_facial_recognition_bias_audit_report",
    "ai_now_institute_discriminatory_algorithms_employment_housing_study",
    "propublica_compas_recidivism_racial_bias_investigative_report",
  ],
  entities: [
    { id: "ABR-001", name: "USA/COMPAS — Récidivisme Biaisé Justice, Crédit Score Racial & Algorithmes RH Discriminatoires", country: "Amérique du Nord", composite_score: 92.9, employment_housing_algorithmic_exclusion_severity_score: 95.0, predictive_policing_racial_bias_scale_score: 92.0, judicial_algorithmic_sentencing_gap_score: 92.0, algorithmic_transparency_right_explanation_absence_score: 92.0, risk_level: "critique", primary_pattern: "judicial_algorithmic_sentencing_gap", estimated_algorithmic_bias_rights_index: 9.29, last_updated: "2026-06-21" },
    { id: "ABR-002", name: "Chine — Score Social Emploi Ethnique, Algorithmes Surveillance Citoyens & Notation Comportement", country: "Asie de l'Est", composite_score: 90.1, employment_housing_algorithmic_exclusion_severity_score: 90.0, predictive_policing_racial_bias_scale_score: 92.0, judicial_algorithmic_sentencing_gap_score: 90.0, algorithmic_transparency_right_explanation_absence_score: 88.0, risk_level: "critique", primary_pattern: "predictive_policing_racial_bias_scale", estimated_algorithmic_bias_rights_index: 9.01, last_updated: "2026-06-21" },
    { id: "ABR-003", name: "UK — PredPol Police Prédictive, Algorithmes DWP Prestations & Windrush Biais Systémique", country: "Europe", composite_score: 88.0, employment_housing_algorithmic_exclusion_severity_score: 88.0, predictive_policing_racial_bias_scale_score: 88.0, judicial_algorithmic_sentencing_gap_score: 88.0, algorithmic_transparency_right_explanation_absence_score: 88.0, risk_level: "critique", primary_pattern: "employment_housing_algorithmic_exclusion_severity", estimated_algorithmic_bias_rights_index: 8.8, last_updated: "2026-06-21" },
    { id: "ABR-004", name: "Pays en Développement — FinTech Exclusion Crédit Mobile, Score Sans Historique & Biais Genre", country: "Global Sud", composite_score: 85.75, employment_housing_algorithmic_exclusion_severity_score: 85.0, predictive_policing_racial_bias_scale_score: 85.0, judicial_algorithmic_sentencing_gap_score: 88.0, algorithmic_transparency_right_explanation_absence_score: 85.0, risk_level: "critique", primary_pattern: "employment_housing_algorithmic_exclusion_severity", estimated_algorithmic_bias_rights_index: 8.58, last_updated: "2026-06-21" },
    { id: "ABR-005", name: "UE — RGPD Art.22 Insuffisant, AI Act Lacunes Systèmes HRisk & Biais Recrutement Automatisé", country: "Europe", composite_score: 53.35, employment_housing_algorithmic_exclusion_severity_score: 52.0, predictive_policing_racial_bias_scale_score: 55.0, judicial_algorithmic_sentencing_gap_score: 52.0, algorithmic_transparency_right_explanation_absence_score: 55.0, risk_level: "élevé", primary_pattern: "algorithmic_transparency_right_explanation_absence", estimated_algorithmic_bias_rights_index: 5.34, last_updated: "2026-06-21" },
    { id: "ABR-006", name: "Amérique Latine — Algorithmes Police Prédictive, Score Pauvreté Géographique & Zéro Recours", country: "Amérique Latine", composite_score: 52.0, employment_housing_algorithmic_exclusion_severity_score: 50.0, predictive_policing_racial_bias_scale_score: 52.0, judicial_algorithmic_sentencing_gap_score: 52.0, algorithmic_transparency_right_explanation_absence_score: 55.0, risk_level: "élevé", primary_pattern: "predictive_policing_racial_bias_scale", estimated_algorithmic_bias_rights_index: 5.2, last_updated: "2026-06-21" },
    { id: "ABR-007", name: "Algorithmic Justice League/AI Now — Audit Biais, Fairness ML & Plaidoyer Réglementation IA", country: "Global", composite_score: 25.85, employment_housing_algorithmic_exclusion_severity_score: 22.0, predictive_policing_racial_bias_scale_score: 28.0, judicial_algorithmic_sentencing_gap_score: 25.0, algorithmic_transparency_right_explanation_absence_score: 30.0, risk_level: "modéré", primary_pattern: "algorithmic_transparency_right_explanation_absence", estimated_algorithmic_bias_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "ABR-008", name: "ONU/UNESCO — Recommandation IA 2021, RGPD Art.22, SDG 16 Justice & Droits Humains IA", country: "Global", composite_score: 4.4, employment_housing_algorithmic_exclusion_severity_score: 4.0, predictive_policing_racial_bias_scale_score: 5.0, judicial_algorithmic_sentencing_gap_score: 3.0, algorithmic_transparency_right_explanation_absence_score: 6.0, risk_level: "faible", primary_pattern: "judicial_algorithmic_sentencing_gap", estimated_algorithmic_bias_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/algorithmic-bias-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
