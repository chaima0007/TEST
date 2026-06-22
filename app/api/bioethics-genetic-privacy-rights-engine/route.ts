import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[bioethics-genetic-privacy-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Bioethics Genetic Privacy Rights Engine Agent",
  domain: "bioethics_genetic_privacy_rights",
  total_entities: 8,
  avg_composite: 61.34,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { genome_editing_embryo_ethics_severity: 3, genetic_database_state_surveillance_scale: 2, informed_consent_biobank_research_deficit_gap: 2, insurance_employment_genetic_discrimination: 1 },
  top_risk_entities: ["Chine/CRISPR — He Jiankui Bébés OGM 2018, ADN Uyghurs Police Collecté, Biobank 10M Génomes État & CRISPR Non-Réglementé", "USA/GINA Gaps — GenBank Données Partagées Sans Consentement, Assurances Vie Exemption GINA, Ancestrie ADN Police & DTC Testing Mineurs", "UE/GDPR Tensions — Biobanques UK Reconsent Post-Brexit, 23andMe Faillite Données 14M, GDPR Exemptions Recherche & Profilage Ethnique"],
  critical_alerts: ["Chine/CRISPR: genome_editing_embryo_ethics_severity", "USA/GINA Gaps: genetic_database_state_surveillance_scale", "UE/GDPR Tensions: informed_consent_biobank_research_deficit_gap", "Inde/Biodata: insurance_employment_genetic_discrimination"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_bioethics_genetic_privacy_rights_index: 6.13,
  data_sources: ["un_human_genome_declaration_report", "isscr_stem_cell_ethics_guidelines", "amnesty_international_genetic_surveillance_report"],
  entities: [
    { id: "BGR-001", name: "Chine/CRISPR — He Jiankui Bébés OGM 2018, ADN Uyghurs Police Collecté, Biobank 10M Génomes État & CRISPR Non-Réglementé", country: "Chine", composite_score: 93.55, genome_editing_embryo_ethics_severity_score: 95.0, genetic_database_state_surveillance_scale_score: 93.0, insurance_employment_genetic_discrimination_score: 92.0, informed_consent_biobank_research_deficit_gap_score: 94.0, risk_level: "critique", primary_pattern: "genome_editing_embryo_ethics_severity", estimated_bioethics_genetic_privacy_rights_index: 9.36, last_updated: "2026-06-21" },
    { id: "BGR-002", name: "USA/GINA Gaps — GenBank Données Partagées Sans Consentement, Assurances Vie Exemption GINA, Ancestrie ADN Police & DTC Testing Mineurs", country: "USA", composite_score: 89.65, genome_editing_embryo_ethics_severity_score: 91.0, genetic_database_state_surveillance_scale_score: 89.0, insurance_employment_genetic_discrimination_score: 90.0, informed_consent_biobank_research_deficit_gap_score: 88.0, risk_level: "critique", primary_pattern: "genetic_database_state_surveillance_scale", estimated_bioethics_genetic_privacy_rights_index: 8.96, last_updated: "2026-06-21" },
    { id: "BGR-003", name: "UE/GDPR Tensions — Biobanques UK Reconsent Post-Brexit, 23andMe Faillite Données 14M, GDPR Exemptions Recherche & Profilage Ethnique", country: "Europe", composite_score: 86.45, genome_editing_embryo_ethics_severity_score: 87.0, genetic_database_state_surveillance_scale_score: 86.0, insurance_employment_genetic_discrimination_score: 85.0, informed_consent_biobank_research_deficit_gap_score: 88.0, risk_level: "critique", primary_pattern: "informed_consent_biobank_research_deficit_gap", estimated_bioethics_genetic_privacy_rights_index: 8.64, last_updated: "2026-06-21" },
    { id: "BGR-004", name: "Inde/Biodata — UIDAI Aadhaar ADN Proposition, Programme Génome Humain National, Absence Loi Génétique & Pharma Tests Essais Pauvres", country: "Inde", composite_score: 82.6, genome_editing_embryo_ethics_severity_score: 83.0, genetic_database_state_surveillance_scale_score: 82.0, insurance_employment_genetic_discrimination_score: 84.0, informed_consent_biobank_research_deficit_gap_score: 81.0, risk_level: "critique", primary_pattern: "insurance_employment_genetic_discrimination", estimated_bioethics_genetic_privacy_rights_index: 8.26, last_updated: "2026-06-21" },
    { id: "BGR-005", name: "Australie/Police ADN — Base ADN Police 1M, Innocent Inclus, Prédiction Phénotype & Familial Searching Non-Régulé", country: "Australie", composite_score: 55.45, genome_editing_embryo_ethics_severity_score: 56.0, genetic_database_state_surveillance_scale_score: 54.0, insurance_employment_genetic_discrimination_score: 55.0, informed_consent_biobank_research_deficit_gap_score: 57.0, risk_level: "élevé", primary_pattern: "genetic_database_state_surveillance_scale", estimated_bioethics_genetic_privacy_rights_index: 5.54, last_updated: "2026-06-21" },
    { id: "BGR-006", name: "Israël/Génome — État Registre Génétique 2019, Kohanim ADN Discrimination, Comités IVF Non-Indépendants & Surrogacy Exploitation", country: "Israël", composite_score: 52.45, genome_editing_embryo_ethics_severity_score: 52.0, genetic_database_state_surveillance_scale_score: 51.0, insurance_employment_genetic_discrimination_score: 54.0, informed_consent_biobank_research_deficit_gap_score: 53.0, risk_level: "élevé", primary_pattern: "genome_editing_embryo_ethics_severity", estimated_bioethics_genetic_privacy_rights_index: 5.25, last_updated: "2026-06-21" },
    { id: "BGR-007", name: "UNESCO/ISSCR — Déclaration Universelle Génome Humain 1997, ISSCR Guidelines Cellules Souches 2021, Global Observatory & Bioethics Comités", country: "Global", composite_score: 26.55, genome_editing_embryo_ethics_severity_score: 27.0, genetic_database_state_surveillance_scale_score: 25.0, insurance_employment_genetic_discrimination_score: 28.0, informed_consent_biobank_research_deficit_gap_score: 26.0, risk_level: "modéré", primary_pattern: "informed_consent_biobank_research_deficit_gap", estimated_bioethics_genetic_privacy_rights_index: 2.66, last_updated: "2026-06-21" },
    { id: "BGR-008", name: "ONU/Oviedo — Convention Oviedo Biomédecine 1997, PIDESC Art.15 Science, Déclaration Helsinki & Belmont Report Standards", country: "Global", composite_score: 4.0, genome_editing_embryo_ethics_severity_score: 4.0, genetic_database_state_surveillance_scale_score: 4.0, insurance_employment_genetic_discrimination_score: 4.0, informed_consent_biobank_research_deficit_gap_score: 4.0, risk_level: "faible", primary_pattern: "genome_editing_embryo_ethics_severity", estimated_bioethics_genetic_privacy_rights_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/bioethics-genetic-privacy-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
