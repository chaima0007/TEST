import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";
const SWARM_API_URL = process.env.SWARM_API_URL;
if (!SWARM_API_URL) console.warn("[healthcare-access-rights-engine] SWARM_API_URL not set");

const FALLBACK = {
  agent: "Healthcare Access Rights Engine",
  domain: "healthcare_access_rights",
  avg_composite: 60.01,
  confidence_score: 0.88,
  total_entities: 8,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  critical_alerts: [
    "Somalia:universal_coverage_gap",
    "CAR:healthcare_infrastructure_collapse",
    "Chad:medical_personnel_shortage",
    "Sierra Leone:essential_medicines_access",
  ],
  data_sources: [
    "who_universal_health_coverage_index_2024",
    "world_bank_health_expenditure_2024",
    "unicef_maternal_mortality_2024",
    "msf_access_medicines_report",
  ],
  estimated_healthcare_access_rights_index: 6.00,
  entities: [
    { id: "HAR-001", name: "Somalia — 1 Médecin/100 000 Hab, Infrastructure Effondrée", country: "Somalie", composite_score: 91.20, risk_level: "critique", primary_pattern: "universal_coverage_gap", estimated_healthcare_access_rights_index: 9.12 },
    { id: "HAR-002", name: "Central African Republic — 3 Médecins/100k, Mortalité 829/100k", country: "Centrafrique", composite_score: 86.70, risk_level: "critique", primary_pattern: "healthcare_infrastructure_collapse", estimated_healthcare_access_rights_index: 8.67 },
    { id: "HAR-003", name: "Chad — 0.4 Médecins/1 000, Déserts Médicaux 80% Territoire", country: "Tchad", composite_score: 83.70, risk_level: "critique", primary_pattern: "medical_personnel_shortage", estimated_healthcare_access_rights_index: 8.37 },
    { id: "HAR-004", name: "Sierra Leone — Mortalité Maternelle 443/100k, Ebola Legacy", country: "Sierra Leone", composite_score: 77.70, risk_level: "critique", primary_pattern: "essential_medicines_access", estimated_healthcare_access_rights_index: 7.77 },
    { id: "HAR-005", name: "Haiti — Hôpitaux Détruits, Choléra Retour, Ariel Henry", country: "Haïti", composite_score: 53.20, risk_level: "élevé", primary_pattern: "healthcare_infrastructure_collapse", estimated_healthcare_access_rights_index: 5.32 },
    { id: "HAR-006", name: "Indonesia — JKN Coverage Gaps, Spécialistes Concentrés Urbains", country: "Indonésie", composite_score: 48.55, risk_level: "élevé", primary_pattern: "universal_coverage_gap", estimated_healthcare_access_rights_index: 4.86 },
    { id: "HAR-007", name: "Brazil — SUS Sous-Financé, Inégalités Régionales Nord/Sud", country: "Brésil", composite_score: 29.20, risk_level: "modéré", primary_pattern: "universal_coverage_gap", estimated_healthcare_access_rights_index: 2.92 },
    { id: "HAR-008", name: "Thailand — UHC 2002 Meilleure Pratique Mondiale OMS", country: "Thaïlande", composite_score: 9.80, risk_level: "faible", primary_pattern: "universal_coverage_gap", estimated_healthcare_access_rights_index: 0.98 },
  ],
};

export async function GET() {
  try {
    const upstream = await fetch(`${SWARM_API_URL}/healthcare-access-rights-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(FALLBACK), { status: 502 });
  }
}
