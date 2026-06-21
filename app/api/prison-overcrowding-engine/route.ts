import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[prison-overcrowding-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Prison Overcrowding Engine Agent",
  domain: "prison_overcrowding",
  total_entities: 8,
  avg_composite: 59.71,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { occupancy_rate_excess: 2, violence_inmate_death: 2, health_sanitation_failure: 2, reform_political_will_gap: 2 },
  top_risk_entities: [
    "El Salvador — CECOT 800% Capacité, Gangs/MS13 Détenus en Masse & Droits Suspendus",
    "Philippines — BJMP 500% Capacité, Morts Liées à la Chaleur & Torture Banalisée",
    "Venezuela — Prisons DGCIM/Tocuyito, Bandas Armées Contrôlent Cellules & Épidémies",
  ],
  critical_alerts: [
    "El Salvador: occupancy_rate_excess",
    "Philippines: violence_inmate_death",
    "Venezuela: health_sanitation_failure",
    "Haïti: health_sanitation_failure",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_prison_overcrowding_index: 5.97,
  data_sources: [
    "world_prison_brief_icps_global_prison_population_database",
    "penal_reform_international_global_prison_trends_annual_report",
    "un_special_rapporteur_torture_places_of_deprivation_liberty_report",
  ],
  entities: [
    { id: "PO-001", name: "El Salvador — CECOT 800% Capacité, Gangs/MS13 Détenus en Masse & Droits Suspendus", country: "Amérique Centrale", composite_score: 90.0, occupancy_rate_excess_score: 95.0, health_sanitation_failure_score: 90.0, violence_inmate_death_score: 88.0, reform_political_will_gap_score: 85.0, risk_level: "critique", primary_pattern: "occupancy_rate_excess", estimated_prison_overcrowding_index: 9.0, last_updated: "2026-06-20" },
    { id: "PO-002", name: "Philippines — BJMP 500% Capacité, Morts Liées à la Chaleur & Torture Banalisée", country: "Asie du Sud-Est", composite_score: 86.05, occupancy_rate_excess_score: 88.0, health_sanitation_failure_score: 85.0, violence_inmate_death_score: 88.0, reform_political_will_gap_score: 82.0, risk_level: "critique", primary_pattern: "violence_inmate_death", estimated_prison_overcrowding_index: 8.61, last_updated: "2026-06-20" },
    { id: "PO-003", name: "Venezuela — Prisons DGCIM/Tocuyito, Bandas Armées Contrôlent Cellules & Épidémies", country: "Amérique Latine", composite_score: 84.75, occupancy_rate_excess_score: 85.0, health_sanitation_failure_score: 88.0, violence_inmate_death_score: 85.0, reform_political_will_gap_score: 80.0, risk_level: "critique", primary_pattern: "health_sanitation_failure", estimated_prison_overcrowding_index: 8.48, last_updated: "2026-06-20" },
    { id: "PO-004", name: "Haïti — Pénitencier National Port-au-Prince, 4000% Capacité & Gangs Infiltrés", country: "Caraïbes", composite_score: 81.35, occupancy_rate_excess_score: 80.0, health_sanitation_failure_score: 85.0, violence_inmate_death_score: 82.0, reform_political_will_gap_score: 78.0, risk_level: "critique", primary_pattern: "health_sanitation_failure", estimated_prison_overcrowding_index: 8.14, last_updated: "2026-06-20" },
    { id: "PO-005", name: "Thaïlande — 300% Capacité, Prisonniers Drogues Surreprésentés & Réforme Lente", country: "Asie du Sud-Est", composite_score: 53.85, occupancy_rate_excess_score: 52.0, health_sanitation_failure_score: 55.0, violence_inmate_death_score: 58.0, reform_political_will_gap_score: 50.0, risk_level: "élevé", primary_pattern: "reform_political_will_gap", estimated_prison_overcrowding_index: 5.39, last_updated: "2026-06-20" },
    { id: "PO-006", name: "Mexique — Prisons Fédérales Surpeuplées, Cartels & Corruption Pénitentiaire Systémique", country: "Amérique du Nord", composite_score: 51.15, occupancy_rate_excess_score: 48.0, health_sanitation_failure_score: 52.0, violence_inmate_death_score: 55.0, reform_political_will_gap_score: 50.0, risk_level: "élevé", primary_pattern: "reform_political_will_gap", estimated_prison_overcrowding_index: 5.12, last_updated: "2026-06-20" },
    { id: "PO-007", name: "UE/Pays-Bas — Fermeture Prisons, Alternatives Détention & Population Carcérale en Baisse", country: "Europe", composite_score: 26.1, occupancy_rate_excess_score: 22.0, health_sanitation_failure_score: 28.0, violence_inmate_death_score: 30.0, reform_political_will_gap_score: 25.0, risk_level: "modéré", primary_pattern: "occupancy_rate_excess", estimated_prison_overcrowding_index: 2.61, last_updated: "2026-06-20" },
    { id: "PO-008", name: "ONU/ONUDC — Règles Mandela, Standards Minima Traitement Détenus & Monitoring Global", country: "Global", composite_score: 4.4, occupancy_rate_excess_score: 4.0, health_sanitation_failure_score: 5.0, violence_inmate_death_score: 3.0, reform_political_will_gap_score: 6.0, risk_level: "faible", primary_pattern: "violence_inmate_death", estimated_prison_overcrowding_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/prison-overcrowding-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
