import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// ── Mock entities ──────────────────────────────────────────────────────────────
// Module 343 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// 8 entities covering all 5 wealth concentration patterns and all 4 risk levels.

const MOCK_ENTITIES = [
  // WCE-001 — Euro-Atlantic, Global_North → critical, plutocracy_lock_in
  // democratic_process_plutocratic_capture≥0.70 AND wealth_effect_political_power≥0.65 → plutocracy_lock_in
  // composite≥60 → critical
  {
    entity_id: "WCE-001", economic_zone: "Euro-Atlantic", region: "Global_North",
    gini_coefficient_extreme_level: 0.85,          billionaire_wealth_gdp_ratio: 0.78,
    top_1_percent_wealth_share: 0.68,              tax_evasion_elite_impunity: 0.72,
    offshore_wealth_accumulation_rate: 0.75,       democratic_process_plutocratic_capture: 0.82,
    inheritance_wealth_concentration: 0.78,        intergenerational_mobility_collapse: 0.68,
    social_elevator_destruction: 0.65,             luxury_asset_inflation_vs_wage_stagnation: 0.80,
    elite_network_exclusivity_index: 0.75,         meritocracy_narrative_collapse: 0.62,
    plutocratic_media_ownership: 0.65,             tax_haven_system_expansion: 0.68,
    wealth_effect_political_power: 0.78,           housing_wealth_extraction_rate: 0.72,
    financial_asset_class_monopoly: 0.70,
  },
  // WCE-002 — Oceania, Pacific_Rim → low, none
  // All values low → composite<20, no pattern triggered
  {
    entity_id: "WCE-002", economic_zone: "Oceania", region: "Pacific_Rim",
    gini_coefficient_extreme_level: 0.10,          billionaire_wealth_gdp_ratio: 0.08,
    top_1_percent_wealth_share: 0.10,              tax_evasion_elite_impunity: 0.08,
    offshore_wealth_accumulation_rate: 0.10,       democratic_process_plutocratic_capture: 0.08,
    inheritance_wealth_concentration: 0.10,        intergenerational_mobility_collapse: 0.08,
    social_elevator_destruction: 0.10,             luxury_asset_inflation_vs_wage_stagnation: 0.08,
    elite_network_exclusivity_index: 0.10,         meritocracy_narrative_collapse: 0.08,
    plutocratic_media_ownership: 0.10,             tax_haven_system_expansion: 0.08,
    wealth_effect_political_power: 0.10,           housing_wealth_extraction_rate: 0.08,
    financial_asset_class_monopoly: 0.10,
  },
  // WCE-003 — Anglo-Saxon, NOAM → high, wealth_singularity
  // top_1_percent_wealth_share≥0.70 AND billionaire_wealth_gdp_ratio≥0.65 → wealth_singularity
  // democratic_process_plutocratic_capture=0.55<0.70 → avoids plutocracy_lock_in
  // composite in [40,60) → high
  {
    entity_id: "WCE-003", economic_zone: "Anglo-Saxon", region: "NOAM",
    gini_coefficient_extreme_level: 0.62,          billionaire_wealth_gdp_ratio: 0.72,
    top_1_percent_wealth_share: 0.78,              tax_evasion_elite_impunity: 0.48,
    offshore_wealth_accumulation_rate: 0.55,       democratic_process_plutocratic_capture: 0.55,
    inheritance_wealth_concentration: 0.52,        intergenerational_mobility_collapse: 0.48,
    social_elevator_destruction: 0.45,             luxury_asset_inflation_vs_wage_stagnation: 0.55,
    elite_network_exclusivity_index: 0.58,         meritocracy_narrative_collapse: 0.45,
    plutocratic_media_ownership: 0.42,             tax_haven_system_expansion: 0.45,
    wealth_effect_political_power: 0.50,           housing_wealth_extraction_rate: 0.52,
    financial_asset_class_monopoly: 0.55,
  },
  // WCE-004 — Nordic, EMEA → low, none
  // All values low → composite<20, no pattern triggered
  {
    entity_id: "WCE-004", economic_zone: "Nordic", region: "EMEA",
    gini_coefficient_extreme_level: 0.08,          billionaire_wealth_gdp_ratio: 0.10,
    top_1_percent_wealth_share: 0.08,              tax_evasion_elite_impunity: 0.10,
    offshore_wealth_accumulation_rate: 0.08,       democratic_process_plutocratic_capture: 0.10,
    inheritance_wealth_concentration: 0.08,        intergenerational_mobility_collapse: 0.10,
    social_elevator_destruction: 0.08,             luxury_asset_inflation_vs_wage_stagnation: 0.10,
    elite_network_exclusivity_index: 0.08,         meritocracy_narrative_collapse: 0.10,
    plutocratic_media_ownership: 0.08,             tax_haven_system_expansion: 0.10,
    wealth_effect_political_power: 0.08,           housing_wealth_extraction_rate: 0.10,
    financial_asset_class_monopoly: 0.08,
  },
  // WCE-005 — Offshore_Finance, Global_South → critical, tax_impunity_regime
  // tax_evasion_elite_impunity≥0.70 AND tax_haven_system_expansion≥0.65 → tax_impunity_regime
  // democratic_process_plutocratic_capture=0.60<0.70 → avoids plutocracy_lock_in
  // top_1_percent_wealth_share=0.62<0.70 → avoids wealth_singularity
  // intergenerational_mobility_collapse=0.60<0.70 → avoids social_immobility_trap
  // composite≥60 → critical
  {
    entity_id: "WCE-005", economic_zone: "Offshore_Finance", region: "Global_South",
    gini_coefficient_extreme_level: 0.82,          billionaire_wealth_gdp_ratio: 0.75,
    top_1_percent_wealth_share: 0.62,              tax_evasion_elite_impunity: 0.85,
    offshore_wealth_accumulation_rate: 0.78,       democratic_process_plutocratic_capture: 0.60,
    inheritance_wealth_concentration: 0.72,        intergenerational_mobility_collapse: 0.60,
    social_elevator_destruction: 0.58,             luxury_asset_inflation_vs_wage_stagnation: 0.78,
    elite_network_exclusivity_index: 0.72,         meritocracy_narrative_collapse: 0.62,
    plutocratic_media_ownership: 0.60,             tax_haven_system_expansion: 0.82,
    wealth_effect_political_power: 0.62,           housing_wealth_extraction_rate: 0.70,
    financial_asset_class_monopoly: 0.68,
  },
  // WCE-006 — Emerging_Market, LATAM → moderate, none
  // Values below pattern thresholds → no pattern
  // composite in [20,40) → moderate
  {
    entity_id: "WCE-006", economic_zone: "Emerging_Market", region: "LATAM",
    gini_coefficient_extreme_level: 0.32,          billionaire_wealth_gdp_ratio: 0.28,
    top_1_percent_wealth_share: 0.30,              tax_evasion_elite_impunity: 0.28,
    offshore_wealth_accumulation_rate: 0.30,       democratic_process_plutocratic_capture: 0.30,
    inheritance_wealth_concentration: 0.28,        intergenerational_mobility_collapse: 0.30,
    social_elevator_destruction: 0.28,             luxury_asset_inflation_vs_wage_stagnation: 0.32,
    elite_network_exclusivity_index: 0.28,         meritocracy_narrative_collapse: 0.28,
    plutocratic_media_ownership: 0.30,             tax_haven_system_expansion: 0.28,
    wealth_effect_political_power: 0.30,           housing_wealth_extraction_rate: 0.28,
    financial_asset_class_monopoly: 0.30,
  },
  // WCE-007 — Post-Industrial, APAC → high, social_immobility_trap
  // intergenerational_mobility_collapse≥0.70 AND social_elevator_destruction≥0.65 → social_immobility_trap
  // democratic_process_plutocratic_capture=0.52<0.70 → avoids plutocracy_lock_in
  // top_1_percent_wealth_share=0.55<0.70 → avoids wealth_singularity
  // composite in [40,60) → high
  {
    entity_id: "WCE-007", economic_zone: "Post-Industrial", region: "APAC",
    gini_coefficient_extreme_level: 0.58,          billionaire_wealth_gdp_ratio: 0.52,
    top_1_percent_wealth_share: 0.55,              tax_evasion_elite_impunity: 0.48,
    offshore_wealth_accumulation_rate: 0.50,       democratic_process_plutocratic_capture: 0.52,
    inheritance_wealth_concentration: 0.55,        intergenerational_mobility_collapse: 0.78,
    social_elevator_destruction: 0.72,             luxury_asset_inflation_vs_wage_stagnation: 0.58,
    elite_network_exclusivity_index: 0.55,         meritocracy_narrative_collapse: 0.50,
    plutocratic_media_ownership: 0.45,             tax_haven_system_expansion: 0.42,
    wealth_effect_political_power: 0.48,           housing_wealth_extraction_rate: 0.52,
    financial_asset_class_monopoly: 0.50,
  },
  // WCE-008 — Oligarchic_Media, MEA → critical, media_plutocracy
  // plutocratic_media_ownership≥0.70 AND meritocracy_narrative_collapse≥0.65 → media_plutocracy
  // democratic_process_plutocratic_capture=0.60<0.70 → avoids plutocracy_lock_in
  // top_1_percent_wealth_share=0.62<0.70 → avoids wealth_singularity
  // intergenerational_mobility_collapse=0.60<0.70 → avoids social_immobility_trap
  // tax_evasion_elite_impunity=0.62<0.70 → avoids tax_impunity_regime
  // composite≥60 → critical
  {
    entity_id: "WCE-008", economic_zone: "Oligarchic_Media", region: "MEA",
    gini_coefficient_extreme_level: 0.80,          billionaire_wealth_gdp_ratio: 0.72,
    top_1_percent_wealth_share: 0.62,              tax_evasion_elite_impunity: 0.62,
    offshore_wealth_accumulation_rate: 0.70,       democratic_process_plutocratic_capture: 0.60,
    inheritance_wealth_concentration: 0.75,        intergenerational_mobility_collapse: 0.60,
    social_elevator_destruction: 0.62,             luxury_asset_inflation_vs_wage_stagnation: 0.78,
    elite_network_exclusivity_index: 0.72,         meritocracy_narrative_collapse: 0.78,
    plutocratic_media_ownership: 0.82,             tax_haven_system_expansion: 0.62,
    wealth_effect_political_power: 0.62,           housing_wealth_extraction_rate: 0.68,
    financial_asset_class_monopoly: 0.72,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

// ── Scoring functions (mirrors Python engine exactly) ──────────────────────────

function concentrationScore(e: Entity): number {
  return Math.round(
    (e.top_1_percent_wealth_share * 0.4
      + e.billionaire_wealth_gdp_ratio * 0.35
      + e.offshore_wealth_accumulation_rate * 0.25) * 100 * 100) / 100;
}

function mobilityScore(e: Entity): number {
  return Math.round(
    (e.intergenerational_mobility_collapse * 0.4
      + e.social_elevator_destruction * 0.35
      + e.meritocracy_narrative_collapse * 0.25) * 100 * 100) / 100;
}

function captureScore(e: Entity): number {
  return Math.round(
    (e.democratic_process_plutocratic_capture * 0.4
      + e.plutocratic_media_ownership * 0.35
      + e.wealth_effect_political_power * 0.25) * 100 * 100) / 100;
}

function systemicScore(e: Entity): number {
  return Math.round(
    (e.tax_evasion_elite_impunity * 0.4
      + e.tax_haven_system_expansion * 0.35
      + e.inheritance_wealth_concentration * 0.25) * 100 * 100) / 100;
}

function compositeScore(conc: number, mob: number, cap: number, sys: number): number {
  return Math.round((conc * 0.30 + mob * 0.25 + cap * 0.25 + sys * 0.20) * 100) / 100;
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function wealthPattern(e: Entity): string {
  if (e.democratic_process_plutocratic_capture >= 0.70 && e.wealth_effect_political_power >= 0.65)
    return "plutocracy_lock_in";
  if (e.top_1_percent_wealth_share >= 0.70 && e.billionaire_wealth_gdp_ratio >= 0.65)
    return "wealth_singularity";
  if (e.intergenerational_mobility_collapse >= 0.70 && e.social_elevator_destruction >= 0.65)
    return "social_immobility_trap";
  if (e.tax_evasion_elite_impunity >= 0.70 && e.tax_haven_system_expansion >= 0.65)
    return "tax_impunity_regime";
  if (e.plutocratic_media_ownership >= 0.70 && e.meritocracy_narrative_collapse >= 0.65)
    return "media_plutocracy";
  return "none";
}

function severity(risk: string): string {
  if (risk === "critical")  return "ploutocratie_systémique_avancée";
  if (risk === "high")      return "concentration_richesse_dangereuse";
  if (risk === "moderate")  return "inégalité_structurelle_active";
  return "inégalité_gérée";
}

function recommendedAction(risk: string): string {
  if (risk === "critical")  return "réforme_fiscale_urgente_ploutocratie";
  if (risk === "high")      return "démantèlement_capture_oligarchique";
  if (risk === "moderate")  return "renforcement_redistribution_systémique";
  return "veille_concentration_richesse";
}

function signal(risk: string): string {
  if (risk === "critical")  return "🔴 Ploutocratie systémique — démocratie économique compromise";
  if (risk === "high")      return "🟠 Concentration richesse dangereuse détectée";
  if (risk === "moderate")  return "🟡 Inégalité structurelle active — surveillance requise";
  return "🟢 Inégalité économique relativement gérée";
}

// ── GET handler ────────────────────────────────────────────────────────────────

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(
      sealResponse({ error: "SWARM_API_URL not configured" }, "wealth-concentration-engine") as Record<string, unknown>,
      { status: 502 }
    );
  }

  try {
    const entities = MOCK_ENTITIES.map(e => {
      const conc  = concentrationScore(e);
      const mob   = mobilityScore(e);
      const cap   = captureScore(e);
      const sys   = systemicScore(e);
      const comp  = compositeScore(conc, mob, cap, sys);
      const risk  = riskLevel(comp);
      const pat   = wealthPattern(e);
      const sev   = severity(risk);
      const act   = recommendedAction(risk);
      const sig   = signal(risk);

      return {
        entity_id:                              e.entity_id,
        economic_zone:                          e.economic_zone,
        region:                                 e.region,
        concentration_score:                    conc,
        mobility_score:                         mob,
        capture_score:                          cap,
        systemic_score:                         sys,
        composite_score:                        comp,
        risk_level:                             risk,
        wealth_pattern:                         pat,
        severity:                               sev,
        recommended_action:                     act,
        signal:                                 sig,
        top_1_percent_wealth_share:             e.top_1_percent_wealth_share,
        democratic_process_plutocratic_capture: e.democratic_process_plutocratic_capture,
      };
    });

    const patternDist: Record<string, number>  = {};
    const riskDist: Record<string, number>     = {};
    const severityDist: Record<string, number> = {};
    const actionDist: Record<string, number>   = {};

    let tConc = 0, tMob = 0, tCap = 0, tSys = 0, tComp = 0;

    for (const ent of entities) {
      patternDist[ent.wealth_pattern]    = (patternDist[ent.wealth_pattern]    || 0) + 1;
      riskDist[ent.risk_level]           = (riskDist[ent.risk_level]           || 0) + 1;
      severityDist[ent.severity]         = (severityDist[ent.severity]         || 0) + 1;
      actionDist[ent.recommended_action] = (actionDist[ent.recommended_action] || 0) + 1;
      tConc += ent.concentration_score;
      tMob  += ent.mobility_score;
      tCap  += ent.capture_score;
      tSys  += ent.systemic_score;
      tComp += ent.composite_score;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 100) / 100;

    const summary = {
      module_id:                     343,
      module_name:                   "Extreme Wealth Concentration & Plutocracy Intelligence Engine",
      total_entities:                n,
      critical_count:                riskDist["critical"]  || 0,
      high_count:                    riskDist["high"]      || 0,
      moderate_count:                riskDist["moderate"]  || 0,
      low_count:                     riskDist["low"]       || 0,
      avg_composite:                 avgComposite,
      pattern_distribution:          patternDist,
      risk_distribution:             riskDist,
      severity_distribution:         severityDist,
      action_distribution:           actionDist,
      avg_estimated_plutocracy_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
      avg_concentration_score:       Math.round(tConc / n * 100) / 100,
      avg_mobility_score:            Math.round(tMob  / n * 100) / 100,
      avg_capture_score:             Math.round(tCap  / n * 100) / 100,
      avg_systemic_score:            Math.round(tSys  / n * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary }, "wealth-concentration-engine") as Record<string, unknown>
    );
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Erreur moteur concentration richesse" }, "wealth-concentration-engine") as Record<string, unknown>,
      { status: 502 }
    );
  }
}
