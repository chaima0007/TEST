import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[indigenous-data-sovereignty-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Indigenous Data Sovereignty Engine Agent",
  domain: "indigenous_data_sovereignty",
  total_entities: 8,
  avg_composite: 61.28,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { indigenous_data_extraction_commercialization_severity: 3, government_surveillance_indigenous_communities: 1, biometric_genomic_collection_without_consent_scale: 2, ocap_fpic_data_governance_exclusion_gap: 2 },
  top_risk_entities: [
    "USA — Havasupai Tribe Sang ADN Étude Maladie→Schizophrénie Sans Consentement, GenBank Données & NAGPRA Contournement",
    "Australie — Données Santé Communautés Autochtones Partagées Assureurs, Surveillance Drones NT & My Health Record Opt-Out Défaut",
    "Canada — FNPOC Données Mal Stockées, Visages Autochtones Algorithmie Policière & Base ADN GRC Surreprésentée",
  ],
  critical_alerts: [
    "USA: indigenous_data_extraction_commercialization_severity",
    "Australie: government_surveillance_indigenous_communities",
    "Canada: biometric_genomic_collection_without_consent_scale",
    "Brésil/Amazonie: ocap_fpic_data_governance_exclusion_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_indigenous_data_sovereignty_index: 6.13,
  data_sources: [
    "global_indigenous_data_alliance_care_principles",
    "first_nations_ocap_principles_report",
    "un_drip_cultural_data_rights_framework",
  ],
  entities: [
    { id: "IDS-001", name: "USA — Havasupai Tribe Sang ADN Étude Maladie→Schizophrénie Sans Consentement, GenBank Données & NAGPRA Contournement", country: "USA", composite_score: 92.65, indigenous_data_extraction_commercialization_severity_score: 95.0, biometric_genomic_collection_without_consent_scale_score: 93.0, government_surveillance_indigenous_communities_score: 90.0, ocap_fpic_data_governance_exclusion_gap_score: 92.0, risk_level: "critique", primary_pattern: "indigenous_data_extraction_commercialization_severity", estimated_indigenous_data_sovereignty_index: 9.27, last_updated: "2026-06-21" },
    { id: "IDS-002", name: "Australie — Données Santé Communautés Autochtones Partagées Assureurs, Surveillance Drones NT & My Health Record Opt-Out Défaut", country: "Australie", composite_score: 90.0, indigenous_data_extraction_commercialization_severity_score: 92.0, biometric_genomic_collection_without_consent_scale_score: 89.0, government_surveillance_indigenous_communities_score: 91.0, ocap_fpic_data_governance_exclusion_gap_score: 87.0, risk_level: "critique", primary_pattern: "government_surveillance_indigenous_communities", estimated_indigenous_data_sovereignty_index: 9.0, last_updated: "2026-06-21" },
    { id: "IDS-003", name: "Canada — FNPOC Données Mal Stockées, Visages Autochtones Algorithmie Policière & Base ADN GRC Surreprésentée", country: "Canada", composite_score: 86.65, indigenous_data_extraction_commercialization_severity_score: 88.0, biometric_genomic_collection_without_consent_scale_score: 87.0, government_surveillance_indigenous_communities_score: 86.0, ocap_fpic_data_governance_exclusion_gap_score: 85.0, risk_level: "critique", primary_pattern: "biometric_genomic_collection_without_consent_scale", estimated_indigenous_data_sovereignty_index: 8.67, last_updated: "2026-06-21" },
    { id: "IDS-004", name: "Brésil/Amazonie — Cartographie Satellite Terres Garimpos Sans Consultation, Données Yanomami Partagées Agro-Business & FUNAI Surveillance", country: "Brésil", composite_score: 83.65, indigenous_data_extraction_commercialization_severity_score: 85.0, biometric_genomic_collection_without_consent_scale_score: 83.0, government_surveillance_indigenous_communities_score: 84.0, ocap_fpic_data_governance_exclusion_gap_score: 82.0, risk_level: "critique", primary_pattern: "ocap_fpic_data_governance_exclusion_gap", estimated_indigenous_data_sovereignty_index: 8.37, last_updated: "2026-06-21" },
    { id: "IDS-005", name: "Nouvelle-Zélande Māori — Données Whakapapa Utilisées Recherche Académique Sans Retour Communauté & Data Colonialism Héritage", country: "Nouvelle-Zélande", composite_score: 54.6, indigenous_data_extraction_commercialization_severity_score: 57.0, biometric_genomic_collection_without_consent_scale_score: 54.0, government_surveillance_indigenous_communities_score: 52.0, ocap_fpic_data_governance_exclusion_gap_score: 55.0, risk_level: "élevé", primary_pattern: "indigenous_data_extraction_commercialization_severity", estimated_indigenous_data_sovereignty_index: 5.46, last_updated: "2026-06-21" },
    { id: "IDS-006", name: "Afrique Autochtones — Biopiraterie Données Génétiques San/Bushmen, Projets Génome Sans FPIC & Biotechs Brevets Traditionnels", country: "Afrique", composite_score: 52.15, indigenous_data_extraction_commercialization_severity_score: 54.0, biometric_genomic_collection_without_consent_scale_score: 53.0, government_surveillance_indigenous_communities_score: 50.0, ocap_fpic_data_governance_exclusion_gap_score: 51.0, risk_level: "élevé", primary_pattern: "biometric_genomic_collection_without_consent_scale", estimated_indigenous_data_sovereignty_index: 5.22, last_updated: "2026-06-21" },
    { id: "IDS-007", name: "FNPOC/GIDA — First Nations Principes OCAP, Global Indigenous Data Alliance, Standards CARE & Protocoles Gouvernance", country: "Global", composite_score: 26.55, indigenous_data_extraction_commercialization_severity_score: 28.0, biometric_genomic_collection_without_consent_scale_score: 26.0, government_surveillance_indigenous_communities_score: 25.0, ocap_fpic_data_governance_exclusion_gap_score: 27.0, risk_level: "modéré", primary_pattern: "ocap_fpic_data_governance_exclusion_gap", estimated_indigenous_data_sovereignty_index: 2.66, last_updated: "2026-06-21" },
    { id: "IDS-008", name: "ONU/DRIP Données — DRIP Art.11-13 Données Culturelles, CBD Nagoya Ressources Génétiques & SDG 17 Partenariat Données", country: "Global", composite_score: 4.0, indigenous_data_extraction_commercialization_severity_score: 4.0, biometric_genomic_collection_without_consent_scale_score: 4.0, government_surveillance_indigenous_communities_score: 4.0, ocap_fpic_data_governance_exclusion_gap_score: 4.0, risk_level: "faible", primary_pattern: "indigenous_data_extraction_commercialization_severity", estimated_indigenous_data_sovereignty_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/indigenous-data-sovereignty-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
