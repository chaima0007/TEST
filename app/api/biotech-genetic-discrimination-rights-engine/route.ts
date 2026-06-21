import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[biotech-genetic-discrimination-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "biotech_genetic_discrimination_rights_engine",
  domain: "biotech_genetic_discrimination",
  total_entities: 8,
  avg_composite: 62.02,
  confidence_score: 0.91,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    corporate_genetic_exploitation: 3,
    state_genomic_surveillance: 2,
    insurance_discrimination: 2,
    consent_violation: 1,
  },
  top_risk_entities: [
    { id: "BGD-002", name: "Chine — Base Données ADN Obligatoire, Surveillance Génétique Ethnique", score: 94.2, risk: "critique" },
    { id: "BGD-001", name: "États-Unis — Compagnies Assurances Génotype, GINA Non Appliquée", score: 89.95, risk: "critique" },
    { id: "BGD-003", name: "Inde — Discrimination Génétique Castes, Entreprises Sans Régulation", score: 87.05, risk: "critique" },
  ],
  critical_alerts: [
    "BGD-001: États-Unis — Compagnies Assurances Génotype, GINA Non Appliquée — composite 89.95",
    "BGD-002: Chine — Base Données ADN Obligatoire, Surveillance Génétique Ethnique — composite 94.2",
    "BGD-003: Inde — Discrimination Génétique Castes, Entreprises Sans Régulation — composite 87.05",
    "BGD-004: Brésil — Biopiraterie Génétique Peuples Autochtones, Données Vendues — composite 86.3",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_biotech_genetic_discrimination_index: 6.2,
  data_sources: [
    "who_human_genome_mapping_project_2023",
    "ohchr_genetic_discrimination_report_2024",
    "un_biotechnology_rights_framework_2023",
    "gina_enforcement_eeoc_report_2024",
  ],
  entities: [
    {
      id: "BGD-001",
      name: "États-Unis — Compagnies Assurances Génotype, GINA Non Appliquée",
      country: "États-Unis",
      genetic_data_exploitation_corporate_score: 92.0,
      discrimination_employment_insurance_score: 90.0,
      consent_privacy_genomic_database_score: 88.0,
      regulatory_framework_protection_score: 85.0,
      composite_score: 89.95,
      risk_level: "critique",
      primary_pattern: "Exploitation données génomiques 23andMe/AncestryDNA, discrimination assurance santé GINA contournée, 26M profils génétiques exposés",
      estimated_biotech_genetic_discrimination_index: 9.0,
      last_updated: "2026-06-21",
    },
    {
      id: "BGD-002",
      name: "Chine — Base Données ADN Obligatoire, Surveillance Génétique Ethnique",
      country: "Chine",
      genetic_data_exploitation_corporate_score: 95.0,
      discrimination_employment_insurance_score: 91.0,
      consent_privacy_genomic_database_score: 96.0,
      regulatory_framework_protection_score: 94.0,
      composite_score: 94.2,
      risk_level: "critique",
      primary_pattern: "Base ADN 80M citoyens Xinjiang, séquençage ethnique Ouïghours, discrimination génétique systémique par l'État",
      estimated_biotech_genetic_discrimination_index: 9.42,
      last_updated: "2026-06-21",
    },
    {
      id: "BGD-003",
      name: "Inde — Discrimination Génétique Castes, Entreprises Sans Régulation",
      country: "Inde",
      genetic_data_exploitation_corporate_score: 88.0,
      discrimination_employment_insurance_score: 87.0,
      consent_privacy_genomic_database_score: 85.0,
      regulatory_framework_protection_score: 89.0,
      composite_score: 87.05,
      risk_level: "critique",
      primary_pattern: "Corrélation génotype-caste utilisée par employeurs, absence loi protection ADN, 600k profils collectés sans consentement",
      estimated_biotech_genetic_discrimination_index: 8.71,
      last_updated: "2026-06-21",
    },
    {
      id: "BGD-004",
      name: "Brésil — Biopiraterie Génétique Peuples Autochtones, Données Vendues",
      country: "Brésil",
      genetic_data_exploitation_corporate_score: 86.0,
      discrimination_employment_insurance_score: 84.0,
      consent_privacy_genomic_database_score: 90.0,
      regulatory_framework_protection_score: 83.0,
      composite_score: 86.3,
      risk_level: "critique",
      primary_pattern: "Exploitation données génétiques Amazonie sans consentement FPIC, biopiraterie Big Pharma, discrimination assurance vie 34% plus élevée",
      estimated_biotech_genetic_discrimination_index: 8.63,
      last_updated: "2026-06-21",
    },
    {
      id: "BGD-005",
      name: "Royaume-Uni — NHS Génomique, Accès Assureurs aux Prédispositions",
      country: "Royaume-Uni",
      genetic_data_exploitation_corporate_score: 52.0,
      discrimination_employment_insurance_score: 55.0,
      consent_privacy_genomic_database_score: 48.0,
      regulatory_framework_protection_score: 50.0,
      composite_score: 51.45,
      risk_level: "élevé",
      primary_pattern: "NHS 100K Genomes Project, assureurs demandent résultats BRCA1/2, moratoire volontaire insuffisant, gaps réglementaires ICO",
      estimated_biotech_genetic_discrimination_index: 5.15,
      last_updated: "2026-06-21",
    },
    {
      id: "BGD-006",
      name: "Australie — Discrimination Assurance-Vie Génétique Légale",
      country: "Australie",
      genetic_data_exploitation_corporate_score: 54.0,
      discrimination_employment_insurance_score: 58.0,
      consent_privacy_genomic_database_score: 50.0,
      regulatory_framework_protection_score: 52.0,
      composite_score: 53.7,
      risk_level: "élevé",
      primary_pattern: "Discrimination génétique assurance-vie légalement autorisée jusqu'en 2023, résidus pratiques, 4% Australiens refusés couverture",
      estimated_biotech_genetic_discrimination_index: 5.37,
      last_updated: "2026-06-21",
    },
    {
      id: "BGD-007",
      name: "Mexique — Banques Génétiques Privées Non Régulées, Frontière ADN",
      country: "Mexique",
      genetic_data_exploitation_corporate_score: 28.0,
      discrimination_employment_insurance_score: 25.0,
      consent_privacy_genomic_database_score: 30.0,
      regulatory_framework_protection_score: 26.0,
      composite_score: 27.45,
      risk_level: "modéré",
      primary_pattern: "Cliniques génétiques privées sans cadre légal, données partagées avec partenaires US, protection constitutionnelle insuffisante",
      estimated_biotech_genetic_discrimination_index: 2.75,
      last_updated: "2026-06-21",
    },
    {
      id: "BGD-008",
      name: "France — Loi Bioéthique 2021, Protection CNIL Génomique",
      country: "France",
      genetic_data_exploitation_corporate_score: 8.0,
      discrimination_employment_insurance_score: 7.0,
      consent_privacy_genomic_database_score: 9.0,
      regulatory_framework_protection_score: 6.0,
      composite_score: 7.75,
      risk_level: "faible",
      primary_pattern: "Loi bioéthique 2021 protège données génétiques, CNIL supervision stricte, interdiction discrimination génétique emploi/assurance",
      estimated_biotech_genetic_discrimination_index: 0.78,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/biotech-genetic-discrimination-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data.payload ?? data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }));
  }
}
