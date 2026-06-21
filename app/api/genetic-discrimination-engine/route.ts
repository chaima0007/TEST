import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[genetic-discrimination-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Genetic Discrimination Engine Agent",
  domain: "genetic_discrimination",
  total_entities: 8,
  avg_composite: 61.52,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { predictive_data_consent_absence: 2, insurance_genetic_exclusion_severity: 2, legal_protection_genetic_privacy_gap: 2, employment_dna_testing_coercion_scale: 2 },
  top_risk_entities: [
    "Chine — Base ADN Ethnique Ouïghours, Biobanque Forcée & Prédiction Crimes Génétique",
    "USA — GINA Gaps Assurance Vie/Invalidité, 23andMe Data Breach & Employeurs ADN",
    "Inde — Tests ADN Castes Pureté, Assurances ADN Non Régulées & 0 Loi Génomique",
  ],
  critical_alerts: [
    "Chine: predictive_data_consent_absence",
    "USA: insurance_genetic_exclusion_severity",
    "Inde: legal_protection_genetic_privacy_gap",
    "UK/Europe: insurance_genetic_exclusion_severity",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_genetic_discrimination_index: 6.15,
  data_sources: [
    "aclu_genetic_discrimination_gina_gaps_insurance_employment_report",
    "unesco_human_genome_heritage_declaration_1997_bioethics_update",
    "nature_genetics_biobank_consent_privacy_discrimination_global_review",
  ],
  entities: [
    { id: "GDI-001", name: "Chine — Base ADN Ethnique Ouïghours, Biobanque Forcée & Prédiction Crimes Génétique", country: "Asie de l'Est", composite_score: 92.9, insurance_genetic_exclusion_severity_score: 88.0, employment_dna_testing_coercion_scale_score: 95.0, predictive_data_consent_absence_score: 95.0, legal_protection_genetic_privacy_gap_score: 95.0, risk_level: "critique", primary_pattern: "predictive_data_consent_absence", estimated_genetic_discrimination_index: 9.29, last_updated: "2026-06-21" },
    { id: "GDI-002", name: "USA — GINA Gaps Assurance Vie/Invalidité, 23andMe Data Breach & Employeurs ADN", country: "Amérique du Nord", composite_score: 89.7, insurance_genetic_exclusion_severity_score: 92.0, employment_dna_testing_coercion_scale_score: 88.0, predictive_data_consent_absence_score: 90.0, legal_protection_genetic_privacy_gap_score: 88.0, risk_level: "critique", primary_pattern: "insurance_genetic_exclusion_severity", estimated_genetic_discrimination_index: 8.97, last_updated: "2026-06-21" },
    { id: "GDI-003", name: "Inde — Tests ADN Castes Pureté, Assurances ADN Non Régulées & 0 Loi Génomique", country: "Asie du Sud", composite_score: 88.05, insurance_genetic_exclusion_severity_score: 88.0, employment_dna_testing_coercion_scale_score: 85.0, predictive_data_consent_absence_score: 88.0, legal_protection_genetic_privacy_gap_score: 92.0, risk_level: "critique", primary_pattern: "legal_protection_genetic_privacy_gap", estimated_genetic_discrimination_index: 8.81, last_updated: "2026-06-21" },
    { id: "GDI-004", name: "UK/Europe — Assureurs ADN BRCA1/BRCA2, Underwriting Génétique & Code Concordat Insuffisant", country: "Europe", composite_score: 85.15, insurance_genetic_exclusion_severity_score: 88.0, employment_dna_testing_coercion_scale_score: 82.0, predictive_data_consent_absence_score: 85.0, legal_protection_genetic_privacy_gap_score: 85.0, risk_level: "critique", primary_pattern: "insurance_genetic_exclusion_severity", estimated_genetic_discrimination_index: 8.52, last_updated: "2026-06-21" },
    { id: "GDI-005", name: "Australie — Pas de Loi Fédérale Discrimination Génétique, Assureurs Autorisés ADN", country: "Océanie", composite_score: 53.0, insurance_genetic_exclusion_severity_score: 55.0, employment_dna_testing_coercion_scale_score: 50.0, predictive_data_consent_absence_score: 52.0, legal_protection_genetic_privacy_gap_score: 55.0, risk_level: "élevé", primary_pattern: "legal_protection_genetic_privacy_gap", estimated_genetic_discrimination_index: 5.3, last_updated: "2026-06-21" },
    { id: "GDI-006", name: "Moyen-Orient/Gulf — Tests ADN Mariage Consanguinité, Refus Embauche & Zéro RGPD", country: "Moyen-Orient", composite_score: 53.1, insurance_genetic_exclusion_severity_score: 52.0, employment_dna_testing_coercion_scale_score: 55.0, predictive_data_consent_absence_score: 55.0, legal_protection_genetic_privacy_gap_score: 50.0, risk_level: "élevé", primary_pattern: "employment_dna_testing_coercion_scale", estimated_genetic_discrimination_index: 5.31, last_updated: "2026-06-21" },
    { id: "GDI-007", name: "Genome Privacy Alliance/ACLU — GINA Réforme, Consentement Génomique & Droits Biobanques", country: "Global", composite_score: 25.85, insurance_genetic_exclusion_severity_score: 22.0, employment_dna_testing_coercion_scale_score: 28.0, predictive_data_consent_absence_score: 25.0, legal_protection_genetic_privacy_gap_score: 30.0, risk_level: "modéré", primary_pattern: "predictive_data_consent_absence", estimated_genetic_discrimination_index: 2.59, last_updated: "2026-06-21" },
    { id: "GDI-008", name: "UNESCO — Déclaration Génome Humain Patrimoine Humanité 1997, OCDE Biobanques & OMS", country: "Global", composite_score: 4.4, insurance_genetic_exclusion_severity_score: 4.0, employment_dna_testing_coercion_scale_score: 5.0, predictive_data_consent_absence_score: 3.0, legal_protection_genetic_privacy_gap_score: 6.0, risk_level: "faible", primary_pattern: "employment_dna_testing_coercion_scale", estimated_genetic_discrimination_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/genetic-discrimination-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
