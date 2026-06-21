import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[migrant-domestic-workers-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Migrant Domestic Workers Engine Agent",
  domain: "migrant_domestic_workers",
  total_entities: 8,
  avg_composite: 58.48,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { kafala_system: 3, labor_exploitation: 2, legal_protection_absence: 2, abuse_impunity: 1 },
  top_risk_entities: [
    "Arabie Saoudite/Golfe — 10M Travailleurs Domestiques, Kafala & Confiscation Passeports",
    "Liban — 250 000 Domestiques Bloquées, Crise Économique & Suicides Kafala",
    "Asie du Sud-Est/Hong Kong — Philippines/Indonésie & Exploitation Structurelle",
  ],
  critical_alerts: [
    "Arabie Saoudite/Golfe: kafala_system",
    "Liban: kafala_system",
    "Asie du Sud-Est/Hong Kong: labor_exploitation",
    "Afrique du Sud/Afrique: legal_protection_absence",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_migrant_domestic_workers_index: 5.85,
  data_sources: [
    "ilo_global_estimates_migrant_workers_report",
    "human_rights_watch_abuse_free_domestic_workers_investigations",
    "idwn_international_domestic_workers_network_annual_report",
  ],
  entities: [
    { id: "MDW-001", name: "Arabie Saoudite/Golfe — 10M Travailleurs Domestiques, Kafala & Confiscation Passeports", country: "Moyen-Orient", composite_score: 91.35, kafala_system_score: 92.0, labor_exploitation_score: 88.0, legal_protection_absence_score: 95.0, abuse_impunity_score: 90.0, risk_level: "critique", primary_pattern: "kafala_system", estimated_migrant_domestic_workers_index: 9.14, last_updated: "2026-06-20" },
    { id: "MDW-002", name: "Liban — 250 000 Domestiques Bloquées, Crise Économique & Suicides Kafala", country: "Moyen-Orient", composite_score: 88.25, kafala_system_score: 88.0, labor_exploitation_score: 85.0, legal_protection_absence_score: 92.0, abuse_impunity_score: 88.0, risk_level: "critique", primary_pattern: "kafala_system", estimated_migrant_domestic_workers_index: 8.83, last_updated: "2026-06-20" },
    { id: "MDW-003", name: "Asie du Sud-Est/Hong Kong — Philippines/Indonésie & Exploitation Structurelle", country: "Asie du Sud-Est", composite_score: 78.90, kafala_system_score: 78.0, labor_exploitation_score: 82.0, legal_protection_absence_score: 80.0, abuse_impunity_score: 75.0, risk_level: "critique", primary_pattern: "labor_exploitation", estimated_migrant_domestic_workers_index: 7.89, last_updated: "2026-06-20" },
    { id: "MDW-004", name: "Afrique du Sud/Afrique — Travail Domestique Non Régulé, Salaires Sous Minimum", country: "Afrique Sub-Saharienne", composite_score: 75.25, kafala_system_score: 70.0, labor_exploitation_score: 75.0, legal_protection_absence_score: 78.0, abuse_impunity_score: 80.0, risk_level: "critique", primary_pattern: "legal_protection_absence", estimated_migrant_domestic_workers_index: 7.53, last_updated: "2026-06-20" },
    { id: "MDW-005", name: "Europe/Travailleuses Sans-Papiers — Au Pair Exploitées & Domestiques Invisibles", country: "Europe", composite_score: 51.15, kafala_system_score: 48.0, labor_exploitation_score: 52.0, legal_protection_absence_score: 55.0, abuse_impunity_score: 50.0, risk_level: "élevé", primary_pattern: "labor_exploitation", estimated_migrant_domestic_workers_index: 5.12, last_updated: "2026-06-20" },
    { id: "MDW-006", name: "USA — 2M Travailleuses Domestiques, FLSA Exemptions & Discriminations Raciales", country: "Amérique du Nord", composite_score: 50.00, kafala_system_score: 45.0, labor_exploitation_score: 50.0, legal_protection_absence_score: 52.0, abuse_impunity_score: 55.0, risk_level: "élevé", primary_pattern: "abuse_impunity", estimated_migrant_domestic_workers_index: 5.00, last_updated: "2026-06-20" },
    { id: "MDW-007", name: "OIT/Convention 189 — Cadre Normatif, 35 Ratifications & IDWN Alliance", country: "Global", composite_score: 28.55, kafala_system_score: 28.0, labor_exploitation_score: 30.0, legal_protection_absence_score: 25.0, abuse_impunity_score: 32.0, risk_level: "modéré", primary_pattern: "legal_protection_absence", estimated_migrant_domestic_workers_index: 2.86, last_updated: "2026-06-20" },
    { id: "MDW-008", name: "ONU/CEDAW/Rapporteur — Travailleuses Domestiques Migrantes & Intersectionnalité", country: "Global", composite_score: 4.40, kafala_system_score: 4.0, labor_exploitation_score: 5.0, legal_protection_absence_score: 3.0, abuse_impunity_score: 6.0, risk_level: "faible", primary_pattern: "kafala_system", estimated_migrant_domestic_workers_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/migrant-domestic-workers-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
