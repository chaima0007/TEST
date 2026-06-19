import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ─── Types ────────────────────────────────────────────────────────────────────

interface MceInput {
  entity_id: string;
  methane_source: string;
  region: string;
  arctic_permafrost_methane_release_rate: number;
  submarine_methane_hydrate_destabilization: number;
  wetland_methane_emission_acceleration: number;
  agricultural_methane_uncontrolled_growth: number;
  fossil_fuel_methane_fugitive_emissions: number;
  urban_landfill_methane_saturation: number;
  atmospheric_methane_concentration_index: number;
  methane_warming_feedback_loop_intensity: number;
  permafrost_thaw_acceleration_rate: number;
  clathrate_gun_hypothesis_proximity: number;
  methane_monitoring_coverage_gap: number;
  methane_capture_technology_deployment: number;
  climate_policy_methane_neglect: number;
  arctic_amplification_rate: number;
  methane_vs_CO2_substitution_risk: number;
  deep_sea_methane_seep_activation: number;
  tundra_fire_methane_cascade: number;
}

// ─── Mock entities (8 entities covering all 5 patterns and all 4 risk levels) ──

const MOCK_ENTITIES: MceInput[] = [
  // MCE-001 — critical, permafrost_methane_bomb
  // arctic_permafrost>=0.70 AND clathrate_gun>=0.65 → permafrost_methane_bomb
  // composite≈75.3 → critical
  {
    entity_id: "MCE-001", methane_source: "arctic_permafrost", region: "ARCT",
    arctic_permafrost_methane_release_rate: 0.85,
    submarine_methane_hydrate_destabilization: 0.60,
    wetland_methane_emission_acceleration: 0.70,
    agricultural_methane_uncontrolled_growth: 0.65,
    fossil_fuel_methane_fugitive_emissions: 0.70,
    urban_landfill_methane_saturation: 0.55,
    atmospheric_methane_concentration_index: 0.78,
    methane_warming_feedback_loop_intensity: 0.72,
    permafrost_thaw_acceleration_rate: 0.80,
    clathrate_gun_hypothesis_proximity: 0.75,
    methane_monitoring_coverage_gap: 0.70,
    methane_capture_technology_deployment: 0.15,
    climate_policy_methane_neglect: 0.78,
    arctic_amplification_rate: 0.75,
    methane_vs_CO2_substitution_risk: 0.68,
    deep_sea_methane_seep_activation: 0.60,
    tundra_fire_methane_cascade: 0.65,
  },
  // MCE-002 — low, no pattern
  // All values low → composite≈9.0 → low, no pattern triggered
  {
    entity_id: "MCE-002", methane_source: "managed_wetland", region: "EMEA",
    arctic_permafrost_methane_release_rate: 0.08,
    submarine_methane_hydrate_destabilization: 0.10,
    wetland_methane_emission_acceleration: 0.08,
    agricultural_methane_uncontrolled_growth: 0.10,
    fossil_fuel_methane_fugitive_emissions: 0.08,
    urban_landfill_methane_saturation: 0.10,
    atmospheric_methane_concentration_index: 0.10,
    methane_warming_feedback_loop_intensity: 0.08,
    permafrost_thaw_acceleration_rate: 0.08,
    clathrate_gun_hypothesis_proximity: 0.10,
    methane_monitoring_coverage_gap: 0.10,
    methane_capture_technology_deployment: 0.85,
    climate_policy_methane_neglect: 0.08,
    arctic_amplification_rate: 0.08,
    methane_vs_CO2_substitution_risk: 0.10,
    deep_sea_methane_seep_activation: 0.08,
    tundra_fire_methane_cascade: 0.08,
  },
  // MCE-003 — high, agricultural_methane_crisis
  // agricultural>=0.70 AND policy>=0.65 → agricultural_methane_crisis
  // arctic<0.70 → avoids permafrost_methane_bomb
  // composite≈54.2 → high
  {
    entity_id: "MCE-003", methane_source: "livestock_agriculture", region: "LATAM",
    arctic_permafrost_methane_release_rate: 0.40,
    submarine_methane_hydrate_destabilization: 0.35,
    wetland_methane_emission_acceleration: 0.55,
    agricultural_methane_uncontrolled_growth: 0.80,
    fossil_fuel_methane_fugitive_emissions: 0.55,
    urban_landfill_methane_saturation: 0.60,
    atmospheric_methane_concentration_index: 0.60,
    methane_warming_feedback_loop_intensity: 0.50,
    permafrost_thaw_acceleration_rate: 0.38,
    clathrate_gun_hypothesis_proximity: 0.40,
    methane_monitoring_coverage_gap: 0.65,
    methane_capture_technology_deployment: 0.20,
    climate_policy_methane_neglect: 0.78,
    arctic_amplification_rate: 0.42,
    methane_vs_CO2_substitution_risk: 0.50,
    deep_sea_methane_seep_activation: 0.30,
    tundra_fire_methane_cascade: 0.40,
  },
  // MCE-004 — low, no pattern
  // All values low → composite≈10.9 → low, no pattern triggered
  {
    entity_id: "MCE-004", methane_source: "urban_landfill", region: "APAC",
    arctic_permafrost_methane_release_rate: 0.12,
    submarine_methane_hydrate_destabilization: 0.10,
    wetland_methane_emission_acceleration: 0.12,
    agricultural_methane_uncontrolled_growth: 0.10,
    fossil_fuel_methane_fugitive_emissions: 0.12,
    urban_landfill_methane_saturation: 0.08,
    atmospheric_methane_concentration_index: 0.10,
    methane_warming_feedback_loop_intensity: 0.10,
    permafrost_thaw_acceleration_rate: 0.10,
    clathrate_gun_hypothesis_proximity: 0.08,
    methane_monitoring_coverage_gap: 0.12,
    methane_capture_technology_deployment: 0.80,
    climate_policy_methane_neglect: 0.12,
    arctic_amplification_rate: 0.10,
    methane_vs_CO2_substitution_risk: 0.10,
    deep_sea_methane_seep_activation: 0.10,
    tundra_fire_methane_cascade: 0.08,
  },
  // MCE-005 — critical, clathrate_destabilization
  // submarine>=0.70 AND deep_sea>=0.65 → clathrate_destabilization
  // arctic<0.70 OR clathrate_gun<0.65 → avoids permafrost_methane_bomb
  // composite≈67.2 → critical
  {
    entity_id: "MCE-005", methane_source: "submarine_hydrate", region: "ARCT",
    arctic_permafrost_methane_release_rate: 0.60,
    submarine_methane_hydrate_destabilization: 0.82,
    wetland_methane_emission_acceleration: 0.70,
    agricultural_methane_uncontrolled_growth: 0.65,
    fossil_fuel_methane_fugitive_emissions: 0.72,
    urban_landfill_methane_saturation: 0.58,
    atmospheric_methane_concentration_index: 0.75,
    methane_warming_feedback_loop_intensity: 0.68,
    permafrost_thaw_acceleration_rate: 0.65,
    clathrate_gun_hypothesis_proximity: 0.60,
    methane_monitoring_coverage_gap: 0.72,
    methane_capture_technology_deployment: 0.18,
    climate_policy_methane_neglect: 0.72,
    arctic_amplification_rate: 0.62,
    methane_vs_CO2_substitution_risk: 0.65,
    deep_sea_methane_seep_activation: 0.78,
    tundra_fire_methane_cascade: 0.62,
  },
  // MCE-006 — moderate, no pattern
  // All values below pattern thresholds → no pattern, composite≈29.3 → moderate
  {
    entity_id: "MCE-006", methane_source: "natural_wetland", region: "NOAM",
    arctic_permafrost_methane_release_rate: 0.28,
    submarine_methane_hydrate_destabilization: 0.25,
    wetland_methane_emission_acceleration: 0.30,
    agricultural_methane_uncontrolled_growth: 0.28,
    fossil_fuel_methane_fugitive_emissions: 0.30,
    urban_landfill_methane_saturation: 0.25,
    atmospheric_methane_concentration_index: 0.32,
    methane_warming_feedback_loop_intensity: 0.28,
    permafrost_thaw_acceleration_rate: 0.25,
    clathrate_gun_hypothesis_proximity: 0.28,
    methane_monitoring_coverage_gap: 0.35,
    methane_capture_technology_deployment: 0.55,
    climate_policy_methane_neglect: 0.30,
    arctic_amplification_rate: 0.25,
    methane_vs_CO2_substitution_risk: 0.28,
    deep_sea_methane_seep_activation: 0.22,
    tundra_fire_methane_cascade: 0.25,
  },
  // MCE-007 — high, arctic_feedback_cascade
  // warming>=0.70 AND arctic_amplification>=0.65 → arctic_feedback_cascade
  // arctic<0.70 → avoids permafrost_methane_bomb
  // submarine<0.70 → avoids clathrate_destabilization
  // agricultural<0.70 → avoids agricultural_methane_crisis
  // composite≈56.2 → high
  {
    entity_id: "MCE-007", methane_source: "arctic_feedback", region: "ARCT",
    arctic_permafrost_methane_release_rate: 0.55,
    submarine_methane_hydrate_destabilization: 0.45,
    wetland_methane_emission_acceleration: 0.52,
    agricultural_methane_uncontrolled_growth: 0.50,
    fossil_fuel_methane_fugitive_emissions: 0.48,
    urban_landfill_methane_saturation: 0.45,
    atmospheric_methane_concentration_index: 0.52,
    methane_warming_feedback_loop_intensity: 0.78,
    permafrost_thaw_acceleration_rate: 0.48,
    clathrate_gun_hypothesis_proximity: 0.55,
    methane_monitoring_coverage_gap: 0.52,
    methane_capture_technology_deployment: 0.30,
    climate_policy_methane_neglect: 0.50,
    arctic_amplification_rate: 0.72,
    methane_vs_CO2_substitution_risk: 0.48,
    deep_sea_methane_seep_activation: 0.42,
    tundra_fire_methane_cascade: 0.45,
  },
  // MCE-008 — critical, tundra_methane_inferno
  // tundra_fire>=0.70 AND permafrost_thaw>=0.65 → tundra_methane_inferno
  // arctic<0.70 OR clathrate_gun<0.65 → avoids permafrost_methane_bomb
  // submarine<0.70 → avoids clathrate_destabilization
  // agricultural<0.70 OR policy<0.65 → avoids agricultural_methane_crisis
  // warming<0.70 → avoids arctic_feedback_cascade
  // composite≈69.6 → critical
  {
    entity_id: "MCE-008", methane_source: "tundra_wildfire", region: "ARCT",
    arctic_permafrost_methane_release_rate: 0.60,
    submarine_methane_hydrate_destabilization: 0.55,
    wetland_methane_emission_acceleration: 0.72,
    agricultural_methane_uncontrolled_growth: 0.65,
    fossil_fuel_methane_fugitive_emissions: 0.70,
    urban_landfill_methane_saturation: 0.60,
    atmospheric_methane_concentration_index: 0.72,
    methane_warming_feedback_loop_intensity: 0.68,
    permafrost_thaw_acceleration_rate: 0.78,
    clathrate_gun_hypothesis_proximity: 0.60,
    methane_monitoring_coverage_gap: 0.70,
    methane_capture_technology_deployment: 0.15,
    climate_policy_methane_neglect: 0.75,
    arctic_amplification_rate: 0.62,
    methane_vs_CO2_substitution_risk: 0.65,
    deep_sea_methane_seep_activation: 0.55,
    tundra_fire_methane_cascade: 0.82,
  },
];

// ─── Math (mirrors Python engine exactly) ─────────────────────────────────────

function arcticScore(e: MceInput): number {
  return Math.round(
    (e.arctic_permafrost_methane_release_rate * 0.4
      + e.permafrost_thaw_acceleration_rate * 0.35
      + e.arctic_amplification_rate * 0.25) * 100 * 100) / 100;
}

function emissionScore(e: MceInput): number {
  return Math.round(
    (e.atmospheric_methane_concentration_index * 0.4
      + e.agricultural_methane_uncontrolled_growth * 0.35
      + e.fossil_fuel_methane_fugitive_emissions * 0.25) * 100 * 100) / 100;
}

function feedbackScore(e: MceInput): number {
  return Math.round(
    (e.methane_warming_feedback_loop_intensity * 0.4
      + e.clathrate_gun_hypothesis_proximity * 0.35
      + e.tundra_fire_methane_cascade * 0.25) * 100 * 100) / 100;
}

function responseScore(e: MceInput): number {
  return Math.round(
    (e.climate_policy_methane_neglect * 0.4
      + e.methane_monitoring_coverage_gap * 0.35
      + (1 - e.methane_capture_technology_deployment) * 0.25) * 100 * 100) / 100;
}

function compositeScore(a: number, em: number, fb: number, rs: number): number {
  return Math.round((a * 0.30 + em * 0.25 + fb * 0.25 + rs * 0.20) * 100) / 100;
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function methanePattern(e: MceInput): string {
  if (e.arctic_permafrost_methane_release_rate >= 0.70 && e.clathrate_gun_hypothesis_proximity >= 0.65)
    return "permafrost_methane_bomb";
  if (e.submarine_methane_hydrate_destabilization >= 0.70 && e.deep_sea_methane_seep_activation >= 0.65)
    return "clathrate_destabilization";
  if (e.agricultural_methane_uncontrolled_growth >= 0.70 && e.climate_policy_methane_neglect >= 0.65)
    return "agricultural_methane_crisis";
  if (e.methane_warming_feedback_loop_intensity >= 0.70 && e.arctic_amplification_rate >= 0.65)
    return "arctic_feedback_cascade";
  if (e.tundra_fire_methane_cascade >= 0.70 && e.permafrost_thaw_acceleration_rate >= 0.65)
    return "tundra_methane_inferno";
  return "none";
}

function severity(comp: number): string {
  if (comp >= 60) return "bombe_méthane_imminente";
  if (comp >= 40) return "crise_méthane_accélérée";
  if (comp >= 20) return "accumulation_méthane_critique";
  return "émissions_méthane_surveillées";
}

function recommendedAction(risk: string): string {
  if (risk === "critical")  return "intervention_méthane_urgence_planétaire";
  if (risk === "high")      return "réduction_méthane_accélérée";
  if (risk === "moderate")  return "surveillance_méthane_renforcée";
  return "monitoring_méthane_continu";
}

function methaneSignal(risk: string): string {
  if (risk === "critical")  return "🔴 Bombe méthane imminente — emballement climatique irréversible";
  if (risk === "high")      return "🟠 Crise méthane accélérée détectée";
  if (risk === "moderate")  return "🟡 Accumulation méthane critique — vigilance";
  return "🟢 Émissions méthane sous surveillance";
}

function analyzeEntity(e: MceInput) {
  const a   = arcticScore(e);
  const em  = emissionScore(e);
  const fb  = feedbackScore(e);
  const rs  = responseScore(e);
  const comp = compositeScore(a, em, fb, rs);
  const risk  = riskLevel(comp);
  const pat   = methanePattern(e);
  const sev   = severity(comp);
  const act   = recommendedAction(risk);
  const sig   = methaneSignal(risk);

  return {
    entity_id:                               e.entity_id,
    methane_source:                          e.methane_source,
    region:                                  e.region,
    arctic_score:                            a,
    emission_score:                          em,
    feedback_score:                          fb,
    response_score:                          rs,
    composite_score:                         comp,
    risk_level:                              risk,
    methane_pattern:                         pat,
    severity:                                sev,
    recommended_action:                      act,
    signal:                                  sig,
    arctic_permafrost_methane_release_rate:  e.arctic_permafrost_methane_release_rate,
    methane_warming_feedback_loop_intensity: e.methane_warming_feedback_loop_intensity,
  };
}

// ─── GET handler ──────────────────────────────────────────────────────────────

export async function GET(request: Request) {
  if (!SWARM_API_URL) {
    return NextResponse.json(
      sealResponse({ error: "SWARM_API_URL non configuré — service indisponible" }, "methane-crisis-engine") as Record<string, unknown>,
      { status: 502 }
    );
  }

  const { searchParams } = new URL(request.url);
  const riskFilter    = searchParams.get("risk");
  const patternFilter = searchParams.get("pattern");

  try {
    const allResults = MOCK_ENTITIES.map(analyzeEntity);

    let entities = [...allResults];
    if (riskFilter)    entities = entities.filter((e) => e.risk_level      === riskFilter);
    if (patternFilter) entities = entities.filter((e) => e.methane_pattern === patternFilter);

    const patternDist:  Record<string, number> = {};
    const riskDist:     Record<string, number> = {};
    const severityDist: Record<string, number> = {};
    const actionDist:   Record<string, number> = {};
    let totalComp = 0, totalArctic = 0, totalEmission = 0, totalFeedback = 0, totalResponse = 0;

    for (const r of allResults) {
      patternDist[r.methane_pattern]    = (patternDist[r.methane_pattern]    || 0) + 1;
      riskDist[r.risk_level]            = (riskDist[r.risk_level]            || 0) + 1;
      severityDist[r.severity]          = (severityDist[r.severity]          || 0) + 1;
      actionDist[r.recommended_action]  = (actionDist[r.recommended_action]  || 0) + 1;
      totalComp     += r.composite_score;
      totalArctic   += r.arctic_score;
      totalEmission += r.emission_score;
      totalFeedback += r.feedback_score;
      totalResponse += r.response_score;
    }

    const n = allResults.length;
    const avgComposite = Math.round((totalComp / n) * 100) / 100;

    const summary = {
      module_id:                        345,
      module_name:                      "Methane Crisis & Arctic Methane Bomb Intelligence Engine",
      total_entities:                   n,
      critical_count:                   riskDist["critical"]  || 0,
      high_count:                       riskDist["high"]      || 0,
      moderate_count:                   riskDist["moderate"]  || 0,
      low_count:                        riskDist["low"]       || 0,
      avg_composite:                    avgComposite,
      pattern_distribution:             patternDist,
      risk_distribution:                riskDist,
      severity_distribution:            severityDist,
      action_distribution:              actionDist,
      avg_estimated_methane_risk_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
      avg_arctic_score:                 Math.round((totalArctic   / n) * 10) / 10,
      avg_emission_score:               Math.round((totalEmission / n) * 10) / 10,
      avg_feedback_score:               Math.round((totalFeedback / n) * 10) / 10,
      avg_response_score:               Math.round((totalResponse / n) * 10) / 10,
    };

    return NextResponse.json(
      sealResponse({ entities, summary }, "methane-crisis-engine") as Record<string, unknown>
    );
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Erreur moteur crise méthane" }, "methane-crisis-engine") as Record<string, unknown>,
      { status: 502 }
    );
  }
}
