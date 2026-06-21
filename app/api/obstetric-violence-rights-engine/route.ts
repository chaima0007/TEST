import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[obstetric-violence-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Obstetric Violence Rights Engine Agent",
  domain: "obstetric_violence_rights",
  total_entities: 8,
  avg_composite: 61.9,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { physical_obstetric_abuse_severity: 2, informed_consent_violation_scale: 2, legal_accountability_gap: 2, institutional_denial_minimization_pattern: 2 },
  top_risk_entities: [
    "Venezuela/Amérique Latine — Stérilisations Forcées, Épisiotomies Non Consenties & Zéro Recours",
    "Inde — 45% Accouchements Sans Consentement, Humiliations Publiques & Discrimination Caste Maternité",
    "Afrique Sub-Sah. — Mortalité Maternelle 542/100K, Violences Obstétriques Documentées OMS",
  ],
  critical_alerts: [
    "Venezuela/Amérique Latine: physical_obstetric_abuse_severity",
    "Inde: informed_consent_violation_scale",
    "Afrique Sub-Sah.: physical_obstetric_abuse_severity",
    "Mexique/Brésil: legal_accountability_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_obstetric_violence_rights_index: 6.19,
  data_sources: [
    "who_figo_prevention_elimination_disrespect_abuse_childbirth_report",
    "ohchr_special_rapporteur_torture_healthcare_obstetric_violence_review",
    "human_rights_watch_obstetric_violence_latin_america_india_report",
  ],
  entities: [
    { entity_id: "OVR-001", name: "Venezuela/Amérique Latine — Stérilisations Forcées, Épisiotomies Non Consenties & Zéro Recours", country: "Amérique Latine", composite_score: 93.65, physical_obstetric_abuse_severity_score: 95.0, informed_consent_violation_scale_score: 92.0, legal_accountability_gap_score: 95.0, institutional_denial_minimization_pattern_score: 92.0, risk_level: "critique", primary_pattern: "physical_obstetric_abuse_severity", estimated_obstetric_violence_rights_index: 9.37, last_updated: "2026-06-21" },
    { entity_id: "OVR-002", name: "Inde — 45% Accouchements Sans Consentement, Humiliations Publiques & Discrimination Caste Maternité", country: "Asie du Sud", composite_score: 90.35, physical_obstetric_abuse_severity_score: 90.0, informed_consent_violation_scale_score: 95.0, legal_accountability_gap_score: 88.0, institutional_denial_minimization_pattern_score: 88.0, risk_level: "critique", primary_pattern: "informed_consent_violation_scale", estimated_obstetric_violence_rights_index: 9.04, last_updated: "2026-06-21" },
    { entity_id: "OVR-003", name: "Afrique Sub-Sah. — Mortalité Maternelle 542/100K, Violences Obstétriques Documentées OMS", country: "Afrique", composite_score: 88.6, physical_obstetric_abuse_severity_score: 92.0, informed_consent_violation_scale_score: 88.0, legal_accountability_gap_score: 88.0, institutional_denial_minimization_pattern_score: 85.0, risk_level: "critique", primary_pattern: "physical_obstetric_abuse_severity", estimated_obstetric_violence_rights_index: 8.86, last_updated: "2026-06-21" },
    { entity_id: "OVR-004", name: "Mexique/Brésil — Terme Légal 'Violence Obstétricale' 2007, 90% Cas Non Poursuivis", country: "Amérique Latine", composite_score: 86.85, physical_obstetric_abuse_severity_score: 85.0, informed_consent_violation_scale_score: 85.0, legal_accountability_gap_score: 90.0, institutional_denial_minimization_pattern_score: 88.0, risk_level: "critique", primary_pattern: "legal_accountability_gap", estimated_obstetric_violence_rights_index: 8.69, last_updated: "2026-06-21" },
    { entity_id: "OVR-005", name: "USA — 1/6 Femmes Reportent Maltraitance Maternité, Mortalité Noires 3x Plus & Silence Médical", country: "Amérique du Nord", composite_score: 53.5, physical_obstetric_abuse_severity_score: 52.0, informed_consent_violation_scale_score: 55.0, legal_accountability_gap_score: 55.0, institutional_denial_minimization_pattern_score: 52.0, risk_level: "élevé", primary_pattern: "informed_consent_violation_scale", estimated_obstetric_violence_rights_index: 5.35, last_updated: "2026-06-21" },
    { entity_id: "OVR-006", name: "France — 1 Femme/5 Victime Maltraitance Maternité (Rapport HCE 2018), Déni Institutionnel", country: "Europe", composite_score: 52.0, physical_obstetric_abuse_severity_score: 50.0, informed_consent_violation_scale_score: 52.0, legal_accountability_gap_score: 52.0, institutional_denial_minimization_pattern_score: 55.0, risk_level: "élevé", primary_pattern: "institutional_denial_minimization_pattern", estimated_obstetric_violence_rights_index: 5.2, last_updated: "2026-06-21" },
    { entity_id: "OVR-007", name: "FIGO/OMS — Déclaration Prévention Violence Obstétricale 2019, Standards Consentement", country: "Global", composite_score: 25.85, physical_obstetric_abuse_severity_score: 22.0, informed_consent_violation_scale_score: 28.0, legal_accountability_gap_score: 25.0, institutional_denial_minimization_pattern_score: 30.0, risk_level: "modéré", primary_pattern: "legal_accountability_gap", estimated_obstetric_violence_rights_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "OVR-008", name: "ONU/OHCHR — Rapport Spécial Torture Soins Santé, CEDAW Art.12 Santé Reproductive", country: "Global", composite_score: 4.4, physical_obstetric_abuse_severity_score: 4.0, informed_consent_violation_scale_score: 5.0, legal_accountability_gap_score: 3.0, institutional_denial_minimization_pattern_score: 6.0, risk_level: "faible", primary_pattern: "institutional_denial_minimization_pattern", estimated_obstetric_violence_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/obstetric-violence-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
