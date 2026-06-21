import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[racial-profiling-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Racial Profiling Engine Agent",
  domain: "racial_profiling",
  total_entities: 8,
  avg_composite: 61.04,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { stop_search_racial_disparity: 1, accountability_reform_absence: 3, criminal_justice_bias: 3, surveillance_targeting_race: 1 },
  top_risk_entities: [
    "USA — Stop & Frisk NYC, Noirs 3x Plus Arrêtés Drogues, Mass Incarceration & Ferguson",
    "France — Contrôles Faciès CNDS, Noirs/Arabes 6-8x Plus Contrôlés & IGPN Défaillante",
    "UK — Section 60 Stop&Search, Noirs 8x Plus Contrôlés & Metropolitan Police Casey Report",
  ],
  critical_alerts: [
    "USA: stop_search_racial_disparity",
    "France: accountability_reform_absence",
    "UK: criminal_justice_bias",
    "Australie: criminal_justice_bias",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_racial_profiling_index: 6.1,
  data_sources: [
    "open_society_justice_initiative_ethnic_profiling_europe_report",
    "ecri_council_europe_racial_profiling_recommendations",
    "mapping_police_violence_racial_disparity_database",
  ],
  entities: [
    { id: "RP-001", name: "USA — Stop & Frisk NYC, Noirs 3x Plus Arrêtés Drogues, Mass Incarceration & Ferguson", country: "Amérique du Nord", composite_score: 93.25, stop_search_racial_disparity_score: 95.0, criminal_justice_bias_score: 92.0, surveillance_targeting_race_score: 95.0, accountability_reform_absence_score: 90.0, risk_level: "critique", primary_pattern: "stop_search_racial_disparity", estimated_racial_profiling_index: 9.33, last_updated: "2026-06-21" },
    { id: "RP-002", name: "France — Contrôles Faciès CNDS, Noirs/Arabes 6-8x Plus Contrôlés & IGPN Défaillante", country: "Europe", composite_score: 89.3, stop_search_racial_disparity_score: 88.0, criminal_justice_bias_score: 88.0, surveillance_targeting_race_score: 90.0, accountability_reform_absence_score: 92.0, risk_level: "critique", primary_pattern: "accountability_reform_absence", estimated_racial_profiling_index: 8.93, last_updated: "2026-06-21" },
    { id: "RP-003", name: "UK — Section 60 Stop&Search, Noirs 8x Plus Contrôlés & Metropolitan Police Casey Report", country: "Europe", composite_score: 87.1, stop_search_racial_disparity_score: 85.0, criminal_justice_bias_score: 88.0, surveillance_targeting_race_score: 88.0, accountability_reform_absence_score: 88.0, risk_level: "critique", primary_pattern: "criminal_justice_bias", estimated_racial_profiling_index: 8.71, last_updated: "2026-06-21" },
    { id: "RP-004", name: "Australie — Aboriginal Surincarcération 27x, Profilage Racial Police & Deaths in Custody", country: "Océanie", composite_score: 84.6, stop_search_racial_disparity_score: 82.0, criminal_justice_bias_score: 90.0, surveillance_targeting_race_score: 82.0, accountability_reform_absence_score: 85.0, risk_level: "critique", primary_pattern: "criminal_justice_bias", estimated_racial_profiling_index: 8.46, last_updated: "2026-06-21" },
    { id: "RP-005", name: "Canada — Carding Toronto, Noirs/Autochtones Suiciblés, Rapport Waller & Réformes Lentes", country: "Amérique du Nord", composite_score: 53.95, stop_search_racial_disparity_score: 52.0, criminal_justice_bias_score: 55.0, surveillance_targeting_race_score: 52.0, accountability_reform_absence_score: 58.0, risk_level: "élevé", primary_pattern: "accountability_reform_absence", estimated_racial_profiling_index: 5.4, last_updated: "2026-06-21" },
    { id: "RP-006", name: "Espagne — Frontière Melilla Profilage Migrants, Refoulements Collectifs & Racisme Institutionnel", country: "Europe", composite_score: 49.9, stop_search_racial_disparity_score: 48.0, criminal_justice_bias_score: 52.0, surveillance_targeting_race_score: 50.0, accountability_reform_absence_score: 50.0, risk_level: "élevé", primary_pattern: "criminal_justice_bias", estimated_racial_profiling_index: 4.99, last_updated: "2026-06-21" },
    { id: "RP-007", name: "Open Society Justice Initiative/ECRI — Rapport Profilage Racial & Standards Européens", country: "Global", composite_score: 25.85, stop_search_racial_disparity_score: 22.0, criminal_justice_bias_score: 25.0, surveillance_targeting_race_score: 28.0, accountability_reform_absence_score: 30.0, risk_level: "modéré", primary_pattern: "accountability_reform_absence", estimated_racial_profiling_index: 2.59, last_updated: "2026-06-21" },
    { id: "RP-008", name: "ONU/CERD — Art.5 Non-Discrimination, Recommandation Générale XXXI Profilage Racial", country: "Global", composite_score: 4.4, stop_search_racial_disparity_score: 4.0, criminal_justice_bias_score: 5.0, surveillance_targeting_race_score: 3.0, accountability_reform_absence_score: 6.0, risk_level: "faible", primary_pattern: "surveillance_targeting_race", estimated_racial_profiling_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/racial-profiling-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
