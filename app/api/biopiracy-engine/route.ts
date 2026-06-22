import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[biopiracy-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(sealResponse(getMockData(), "Biopiracy Agent")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/biopiracy-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(sealResponse(data, "Biopiracy Agent")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse(getMockData(), "Biopiracy Agent"),
      { status: 502 }
    ));
  }
}

function getMockData() {
  const entities = [
    {
      id: "BIO-001",
      name: "PharmaCorp Amazonia",
      country: "Brésil",
      sector: "Pharmaceutique",
      composite_score: 86.65,
      genetic_appropriation_score: 90.0,
      traditional_knowledge_score: 85.0,
      patent_abuse_score: 88.0,
      commercial_extraction_score: 82.0,
      risk_level: "critique",
      primary_pattern: "Appropriation de Ressource Génétique",
      key_signals: ["Appropriation génétique: 90/100", "Violation savoirs traditionnels: 85/100", "Abus brevet biodiversité: 88/100"],
      estimated_biopiracy_index: 8.67,
      last_updated: "2026-06-18",
    },
    {
      id: "BIO-002",
      name: "BioGen Asia Pacific",
      country: "Inde",
      sector: "Biotechnologie",
      composite_score: 82.9,
      genetic_appropriation_score: 88.0,
      traditional_knowledge_score: 80.0,
      patent_abuse_score: 78.0,
      commercial_extraction_score: 85.0,
      risk_level: "critique",
      primary_pattern: "Appropriation de Ressource Génétique",
      key_signals: ["Appropriation génétique: 88/100", "Violation savoirs traditionnels: 80/100", "Extraction commerciale: 85/100"],
      estimated_biopiracy_index: 8.29,
      last_updated: "2026-06-17",
    },
    {
      id: "BIO-003",
      name: "Savane Resources Corp",
      country: "Afrique du Sud",
      sector: "Cosmétique & Herboristerie",
      composite_score: 76.9,
      genetic_appropriation_score: 78.0,
      traditional_knowledge_score: 82.0,
      patent_abuse_score: 72.0,
      commercial_extraction_score: 75.0,
      risk_level: "critique",
      primary_pattern: "Violation de Savoir Traditionnel",
      key_signals: ["Violation savoirs traditionnels: 82/100", "Appropriation génétique: 78/100", "Score composite biopiraterie: 76.9/100"],
      estimated_biopiracy_index: 7.69,
      last_updated: "2026-06-16",
    },
    {
      id: "BIO-004",
      name: "Équateur Biodiversité SA",
      country: "Équateur",
      sector: "Extraction Végétale",
      composite_score: 63.9,
      genetic_appropriation_score: 68.0,
      traditional_knowledge_score: 60.0,
      patent_abuse_score: 70.0,
      commercial_extraction_score: 55.0,
      risk_level: "critique",
      primary_pattern: "Brevet Illégitime sur Biodiversité",
      key_signals: ["Abus brevet biodiversité: 70/100", "Appropriation génétique: 68/100", "Extraction commerciale: 55/100"],
      estimated_biopiracy_index: 6.39,
      last_updated: "2026-06-15",
    },
    {
      id: "BIO-005",
      name: "Forêt Médicinale Myanmar",
      country: "Myanmar",
      sector: "Médecine Traditionnelle",
      composite_score: 49.85,
      genetic_appropriation_score: 55.0,
      traditional_knowledge_score: 50.0,
      patent_abuse_score: 45.0,
      commercial_extraction_score: 48.0,
      risk_level: "élevé",
      primary_pattern: "Surveillance Protocole de Nagoya",
      key_signals: ["Score composite biopiraterie: 49.85/100", "Score composite biopiraterie: 49.85/100", "Score composite biopiraterie: 49.85/100"],
      estimated_biopiracy_index: 4.99,
      last_updated: "2026-06-14",
    },
    {
      id: "BIO-006",
      name: "Ethnobot Kenya Ltd",
      country: "Kenya",
      sector: "Ethnobotanique Commerciale",
      composite_score: 42.5,
      genetic_appropriation_score: 48.0,
      traditional_knowledge_score: 42.0,
      patent_abuse_score: 40.0,
      commercial_extraction_score: 38.0,
      risk_level: "élevé",
      primary_pattern: "Surveillance Protocole de Nagoya",
      key_signals: ["Score composite biopiraterie: 42.5/100", "Score composite biopiraterie: 42.5/100", "Score composite biopiraterie: 42.5/100"],
      estimated_biopiracy_index: 4.25,
      last_updated: "2026-06-13",
    },
    {
      id: "BIO-007",
      name: "Institut Plantes Médicinales Pérou",
      country: "Pérou",
      sector: "Recherche Académique",
      composite_score: 26.55,
      genetic_appropriation_score: 28.0,
      traditional_knowledge_score: 25.0,
      patent_abuse_score: 30.0,
      commercial_extraction_score: 22.0,
      risk_level: "modéré",
      primary_pattern: "Surveillance Protocole de Nagoya",
      key_signals: ["Score composite biopiraterie: 26.55/100", "Score composite biopiraterie: 26.55/100", "Score composite biopiraterie: 26.55/100"],
      estimated_biopiracy_index: 2.66,
      last_updated: "2026-06-12",
    },
    {
      id: "BIO-008",
      name: "Conservation ONG Costa Rica",
      country: "Costa Rica",
      sector: "Conservation & ONG",
      composite_score: 11.0,
      genetic_appropriation_score: 10.0,
      traditional_knowledge_score: 8.0,
      patent_abuse_score: 12.0,
      commercial_extraction_score: 15.0,
      risk_level: "faible",
      primary_pattern: "Surveillance Protocole de Nagoya",
      key_signals: ["Score composite biopiraterie: 11/100", "Score composite biopiraterie: 11/100", "Score composite biopiraterie: 11/100"],
      estimated_biopiracy_index: 1.1,
      last_updated: "2026-06-11",
    },
  ];

  const summary = {
    total_entities: 8,
    avg_composite: 55.03,
    risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
    pattern_distribution: {
      "Appropriation de Ressource Génétique": 2,
      "Violation de Savoir Traditionnel": 1,
      "Brevet Illégitime sur Biodiversité": 1,
      "Extraction Commerciale Non-Autorisée": 0,
      "Surveillance Protocole de Nagoya": 4,
    },
    top_risk_entities: ["PharmaCorp Amazonia", "BioGen Asia Pacific", "Savane Resources Corp"],
    critical_alerts: 4,
    last_analysis: "2026-06-20",
    engine_version: "2.1.0",
    domain: "biopiracy",
    confidence_score: 84.6,
    data_sources: ["OMPI", "CBD-Nagoya Protocol", "IUCN", "WHO", "Indigenous Rights Watch"],
    entities,
    avg_estimated_biopiracy_index: 5.5,
  };

  return { entities, summary };
}
