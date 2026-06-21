import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[statelessness-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Statelessness Engine Agent",
  domain: "statelessness",
  total_entities: 8,
  avg_composite: 59.17,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { population_scale_denial: 2, generational_transmission: 2, documentation_access_failure: 2, protection_legal_framework_gap: 2 },
  top_risk_entities: [
    "Myanmar/Rohingya — 1M Apatrides, Génocide & Déni Citoyenneté Depuis 1982",
    "Koweït/Bidun — 100K Apatrides, Interdits Éducation/Soins & Traitement Kafala Abusif",
    "Thaïlande — 480K Apatrides Collines, Enfants Sans Acte Naissance & Traite Favorisée",
  ],
  critical_alerts: [
    "Myanmar/Rohingya: population_scale_denial",
    "Koweït/Bidun: generational_transmission",
    "Thaïlande: documentation_access_failure",
    "Côte d'Ivoire: documentation_access_failure",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_statelessness_index: 5.92,
  data_sources: [
    "unhcr_ibelong_campaign_global_statelessness_report_2024",
    "institute_statelessness_inclusion_global_statelessness_report",
    "open_society_foundations_statelessness_documentation_access_study",
  ],
  entities: [
    { id: "SL-001", name: "Myanmar/Rohingya — 1M Apatrides, Génocide & Déni Citoyenneté Depuis 1982", country: "Asie du Sud-Est", composite_score: 91.6, population_scale_denial_score: 95.0, documentation_access_failure_score: 92.0, generational_transmission_score: 90.0, protection_legal_framework_gap_score: 88.0, risk_level: "critique", primary_pattern: "population_scale_denial", estimated_statelessness_index: 9.16, last_updated: "2026-06-20" },
    { id: "SL-002", name: "Koweït/Bidun — 100K Apatrides, Interdits Éducation/Soins & Traitement Kafala Abusif", country: "Moyen-Orient", composite_score: 86.65, population_scale_denial_score: 88.0, documentation_access_failure_score: 85.0, generational_transmission_score: 88.0, protection_legal_framework_gap_score: 85.0, risk_level: "critique", primary_pattern: "generational_transmission", estimated_statelessness_index: 8.67, last_updated: "2026-06-20" },
    { id: "SL-003", name: "Thaïlande — 480K Apatrides Collines, Enfants Sans Acte Naissance & Traite Favorisée", country: "Asie du Sud-Est", composite_score: 82.25, population_scale_denial_score: 82.0, documentation_access_failure_score: 85.0, generational_transmission_score: 80.0, protection_legal_framework_gap_score: 82.0, risk_level: "critique", primary_pattern: "documentation_access_failure", estimated_statelessness_index: 8.23, last_updated: "2026-06-20" },
    { id: "SL-004", name: "Côte d'Ivoire — 700K Apatrides Post-Guerre Civile, Enfants Migrants Sans Docs & Exclusion", country: "Afrique de l'Ouest", composite_score: 80.0, population_scale_denial_score: 80.0, documentation_access_failure_score: 82.0, generational_transmission_score: 78.0, protection_legal_framework_gap_score: 80.0, risk_level: "critique", primary_pattern: "documentation_access_failure", estimated_statelessness_index: 8.0, last_updated: "2026-06-20" },
    { id: "SL-005", name: "Europe/Ex-URSS — Apatrides Baltes Soviétiques, Russophones Latvia/Estonie & Naturalisation Restrictive", country: "Europe de l'Est", composite_score: 51.45, population_scale_denial_score: 52.0, documentation_access_failure_score: 50.0, generational_transmission_score: 55.0, protection_legal_framework_gap_score: 48.0, risk_level: "élevé", primary_pattern: "generational_transmission", estimated_statelessness_index: 5.15, last_updated: "2026-06-20" },
    { id: "SL-006", name: "République Dominicaine — Dénationalisation Haïtiens, Arrêt TC168/13 & Apatridie Générationnelle", country: "Caraïbes", composite_score: 51.15, population_scale_denial_score: 48.0, documentation_access_failure_score: 52.0, generational_transmission_score: 55.0, protection_legal_framework_gap_score: 50.0, risk_level: "élevé", primary_pattern: "protection_legal_framework_gap", estimated_statelessness_index: 5.12, last_updated: "2026-06-20" },
    { id: "SL-007", name: "HCR/#IBelong — Campagne Fin Apatridie 2024, Réformes Législatives & Enregistrements Naissances", country: "Global", composite_score: 25.85, population_scale_denial_score: 22.0, documentation_access_failure_score: 28.0, generational_transmission_score: 25.0, protection_legal_framework_gap_score: 30.0, risk_level: "modéré", primary_pattern: "population_scale_denial", estimated_statelessness_index: 2.59, last_updated: "2026-06-20" },
    { id: "SL-008", name: "ONU/Convention 1954-1961 — Statut Apatrides, Réduction Apatridie & Cadre Protection Global", country: "Global", composite_score: 4.4, population_scale_denial_score: 4.0, documentation_access_failure_score: 5.0, generational_transmission_score: 3.0, protection_legal_framework_gap_score: 6.0, risk_level: "faible", primary_pattern: "protection_legal_framework_gap", estimated_statelessness_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/statelessness-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
