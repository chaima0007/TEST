import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[corporate-accountability-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Corporate Accountability Rights Engine Agent",
  domain: "corporate_accountability_rights",
  total_entities: 8,
  avg_composite: 62.07,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { corporate_human_rights_abuse_impunity_severity: 2, supply_chain_forced_labor_exploitation_scale: 2, environmental_corporate_destruction_impunity: 1, remedy_access_corporate_victims_gap: 3 },
  top_risk_entities: [
    "Shell/Total/ENI Afrique — Niger Delta 40 Ans Déversements, Congo Contamination & Zéro Remédiation Victimes",
    "Apple/Samsung/Foxconn — Suicides Usines Chine, Cobalt Mines Enfants RDC & Travail Forcé Ouïghours Supply Chain",
    "Chevron/Texaco Amazonie — Pollution Équateur 18Mds Jugement Refusé, 30 000 Victimes & Impunité Totale",
  ],
  critical_alerts: [
    "Shell/Total/ENI Afrique: corporate_human_rights_abuse_impunity_severity",
    "Apple/Samsung/Foxconn: supply_chain_forced_labor_exploitation_scale",
    "Chevron/Texaco Amazonie: environmental_corporate_destruction_impunity",
    "Fast Fashion/H&M/Zara: supply_chain_forced_labor_exploitation_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_corporate_accountability_rights_index: 6.21,
  data_sources: [
    "ohchr_business_human_rights_ruggie_principles",
    "global_witness_corporate_impunity_report",
    "amnesty_international_supply_chain_forced_labor",
  ],
  entities: [
    { id: "CAR-001", name: "Shell/Total/ENI Afrique — Niger Delta 40 Ans Déversements, Congo Contamination & Zéro Remédiation Victimes", country: "Nigeria", composite_score: 94.15, corporate_human_rights_abuse_impunity_severity_score: 96.0, supply_chain_forced_labor_exploitation_scale_score: 93.0, environmental_corporate_destruction_impunity_score: 94.0, remedy_access_corporate_victims_gap_score: 93.0, risk_level: "critique", primary_pattern: "corporate_human_rights_abuse_impunity_severity", estimated_corporate_accountability_rights_index: 9.42, last_updated: "2026-06-21" },
    { id: "CAR-002", name: "Apple/Samsung/Foxconn — Suicides Usines Chine, Cobalt Mines Enfants RDC & Travail Forcé Ouïghours Supply Chain", country: "Global", composite_score: 91.1, corporate_human_rights_abuse_impunity_severity_score: 92.0, supply_chain_forced_labor_exploitation_scale_score: 93.0, environmental_corporate_destruction_impunity_score: 89.0, remedy_access_corporate_victims_gap_score: 90.0, risk_level: "critique", primary_pattern: "supply_chain_forced_labor_exploitation_scale", estimated_corporate_accountability_rights_index: 9.11, last_updated: "2026-06-21" },
    { id: "CAR-003", name: "Chevron/Texaco Amazonie — Pollution Équateur 18Mds Jugement Refusé, 30 000 Victimes & Impunité Totale", country: "Équateur", composite_score: 88.1, corporate_human_rights_abuse_impunity_severity_score: 89.0, supply_chain_forced_labor_exploitation_scale_score: 85.0, environmental_corporate_destruction_impunity_score: 91.0, remedy_access_corporate_victims_gap_score: 87.0, risk_level: "critique", primary_pattern: "environmental_corporate_destruction_impunity", estimated_corporate_accountability_rights_index: 8.81, last_updated: "2026-06-21" },
    { id: "CAR-004", name: "Fast Fashion/H&M/Zara — Rana Plaza 1134 Morts Bangladesh, Travail Forcé Ouïghours Coton & Greenwashing", country: "Bangladesh", composite_score: 85.1, corporate_human_rights_abuse_impunity_severity_score: 86.0, supply_chain_forced_labor_exploitation_scale_score: 87.0, environmental_corporate_destruction_impunity_score: 83.0, remedy_access_corporate_victims_gap_score: 84.0, risk_level: "critique", primary_pattern: "supply_chain_forced_labor_exploitation_scale", estimated_corporate_accountability_rights_index: 8.51, last_updated: "2026-06-21" },
    { id: "CAR-005", name: "Big Pharma GSK/Pfizer — Essais Afrique Sans Consentement, Prix Médicaments Prohibitifs & Accès Vaccins Inégal", country: "Global", composite_score: 54.95, corporate_human_rights_abuse_impunity_severity_score: 57.0, supply_chain_forced_labor_exploitation_scale_score: 53.0, environmental_corporate_destruction_impunity_score: 52.0, remedy_access_corporate_victims_gap_score: 58.0, risk_level: "élevé", primary_pattern: "corporate_human_rights_abuse_impunity_severity", estimated_corporate_accountability_rights_index: 5.5, last_updated: "2026-06-21" },
    { id: "CAR-006", name: "Google/Meta Surveillance — Données Personnelles Sans Consentement, Profilage Minorités & Algorithmes Discriminatoires", country: "Global", composite_score: 52.05, corporate_human_rights_abuse_impunity_severity_score: 53.0, supply_chain_forced_labor_exploitation_scale_score: 50.0, environmental_corporate_destruction_impunity_score: 49.0, remedy_access_corporate_victims_gap_score: 57.0, risk_level: "élevé", primary_pattern: "remedy_access_corporate_victims_gap", estimated_corporate_accountability_rights_index: 5.21, last_updated: "2026-06-21" },
    { id: "CAR-007", name: "OHCHR/UN Working Group BHR — Principes Ruggie 2011, Devoir de Vigilance & Mécanismes Plainte OCDE", country: "Global", composite_score: 26.95, corporate_human_rights_abuse_impunity_severity_score: 28.0, supply_chain_forced_labor_exploitation_scale_score: 26.0, environmental_corporate_destruction_impunity_score: 25.0, remedy_access_corporate_victims_gap_score: 29.0, risk_level: "modéré", primary_pattern: "remedy_access_corporate_victims_gap", estimated_corporate_accountability_rights_index: 2.7, last_updated: "2026-06-21" },
    { id: "CAR-008", name: "ONU/Traité Entreprises & DH — Négociations Instrument Contraignant BHR, Draft Treaty 2023 & SDG 17 Partenariats", country: "Global", composite_score: 4.2, corporate_human_rights_abuse_impunity_severity_score: 4.0, supply_chain_forced_labor_exploitation_scale_score: 4.0, environmental_corporate_destruction_impunity_score: 4.0, remedy_access_corporate_victims_gap_score: 5.0, risk_level: "faible", primary_pattern: "remedy_access_corporate_victims_gap", estimated_corporate_accountability_rights_index: 0.42, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/corporate-accountability-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
