import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  { entity_id: "PCS-001", region: "EMEA",  pension_system_type: "defined_benefit",    demographic_dependency_ratio: 0.82, funding_gap_index: 0.55, investment_return_shortfall: 0.60, longevity_risk_exposure: 0.78, automation_contribution_erosion: 0.72, political_reform_paralysis: 0.60, intergenerational_fairness_gap: 0.55, pension_debt_to_gdp: 0.58, benefit_adequacy_erosion: 0.50, public_pension_trust_deficit: 0.55, private_pension_volatility: 0.60, informal_economy_coverage_gap: 0.45, migration_contribution_dependency: 0.50, early_retirement_pressure: 0.55, disability_benefit_strain: 0.50, pension_system_complexity_risk: 0.55, climate_transition_stranded_assets: 0.50 },
  { entity_id: "PCS-002", region: "APAC",  pension_system_type: "funded_system",       demographic_dependency_ratio: 0.20, funding_gap_index: 0.15, investment_return_shortfall: 0.20, longevity_risk_exposure: 0.22, automation_contribution_erosion: 0.18, political_reform_paralysis: 0.15, intergenerational_fairness_gap: 0.18, pension_debt_to_gdp: 0.12, benefit_adequacy_erosion: 0.15, public_pension_trust_deficit: 0.18, private_pension_volatility: 0.20, informal_economy_coverage_gap: 0.15, migration_contribution_dependency: 0.20, early_retirement_pressure: 0.15, disability_benefit_strain: 0.18, pension_system_complexity_risk: 0.15, climate_transition_stranded_assets: 0.12 },
  { entity_id: "PCS-003", region: "NOAM",  pension_system_type: "defined_contribution", demographic_dependency_ratio: 0.50, funding_gap_index: 0.48, investment_return_shortfall: 0.45, longevity_risk_exposure: 0.52, automation_contribution_erosion: 0.45, political_reform_paralysis: 0.75, intergenerational_fairness_gap: 0.50, pension_debt_to_gdp: 0.45, benefit_adequacy_erosion: 0.48, public_pension_trust_deficit: 0.68, private_pension_volatility: 0.50, informal_economy_coverage_gap: 0.45, migration_contribution_dependency: 0.40, early_retirement_pressure: 0.45, disability_benefit_strain: 0.42, pension_system_complexity_risk: 0.50, climate_transition_stranded_assets: 0.40 },
  { entity_id: "PCS-004", region: "LATAM", pension_system_type: "mixed_system",        demographic_dependency_ratio: 0.25, funding_gap_index: 0.22, investment_return_shortfall: 0.25, longevity_risk_exposure: 0.28, automation_contribution_erosion: 0.20, political_reform_paralysis: 0.25, intergenerational_fairness_gap: 0.22, pension_debt_to_gdp: 0.18, benefit_adequacy_erosion: 0.20, public_pension_trust_deficit: 0.25, private_pension_volatility: 0.28, informal_economy_coverage_gap: 0.22, migration_contribution_dependency: 0.25, early_retirement_pressure: 0.20, disability_benefit_strain: 0.22, pension_system_complexity_risk: 0.20, climate_transition_stranded_assets: 0.18 },
  { entity_id: "PCS-005", region: "EMEA",  pension_system_type: "pay_as_you_go",       demographic_dependency_ratio: 0.65, funding_gap_index: 0.82, investment_return_shortfall: 0.70, longevity_risk_exposure: 0.72, automation_contribution_erosion: 0.60, political_reform_paralysis: 0.65, intergenerational_fairness_gap: 0.60, pension_debt_to_gdp: 0.78, benefit_adequacy_erosion: 0.58, public_pension_trust_deficit: 0.62, private_pension_volatility: 0.65, informal_economy_coverage_gap: 0.55, migration_contribution_dependency: 0.60, early_retirement_pressure: 0.62, disability_benefit_strain: 0.58, pension_system_complexity_risk: 0.65, climate_transition_stranded_assets: 0.60 },
  { entity_id: "PCS-006", region: "APAC",  pension_system_type: "sovereign_fund",      demographic_dependency_ratio: 0.38, funding_gap_index: 0.32, investment_return_shortfall: 0.30, longevity_risk_exposure: 0.35, automation_contribution_erosion: 0.30, political_reform_paralysis: 0.28, intergenerational_fairness_gap: 0.32, pension_debt_to_gdp: 0.28, benefit_adequacy_erosion: 0.30, public_pension_trust_deficit: 0.32, private_pension_volatility: 0.35, informal_economy_coverage_gap: 0.30, migration_contribution_dependency: 0.28, early_retirement_pressure: 0.30, disability_benefit_strain: 0.28, pension_system_complexity_risk: 0.30, climate_transition_stranded_assets: 0.25 },
  { entity_id: "PCS-007", region: "NOAM",  pension_system_type: "corporate_pension",   demographic_dependency_ratio: 0.50, funding_gap_index: 0.48, investment_return_shortfall: 0.50, longevity_risk_exposure: 0.52, automation_contribution_erosion: 0.75, political_reform_paralysis: 0.50, intergenerational_fairness_gap: 0.48, pension_debt_to_gdp: 0.45, benefit_adequacy_erosion: 0.48, public_pension_trust_deficit: 0.50, private_pension_volatility: 0.55, informal_economy_coverage_gap: 0.68, migration_contribution_dependency: 0.45, early_retirement_pressure: 0.50, disability_benefit_strain: 0.45, pension_system_complexity_risk: 0.48, climate_transition_stranded_assets: 0.42 },
  { entity_id: "PCS-008", region: "MEA",   pension_system_type: "pay_as_you_go",       demographic_dependency_ratio: 0.65, funding_gap_index: 0.62, investment_return_shortfall: 0.65, longevity_risk_exposure: 0.70, automation_contribution_erosion: 0.60, political_reform_paralysis: 0.65, intergenerational_fairness_gap: 0.82, pension_debt_to_gdp: 0.60, benefit_adequacy_erosion: 0.75, public_pension_trust_deficit: 0.65, private_pension_volatility: 0.68, informal_economy_coverage_gap: 0.60, migration_contribution_dependency: 0.65, early_retirement_pressure: 0.62, disability_benefit_strain: 0.60, pension_system_complexity_risk: 0.65, climate_transition_stranded_assets: 0.58 },
];

type Entity = typeof MOCK_ENTITIES[0];

function demographicScore(i: Entity): number {
  return Math.round((i.demographic_dependency_ratio * 0.4 + i.longevity_risk_exposure * 0.35 + i.automation_contribution_erosion * 0.25) * 100 * 100) / 100;
}
function fundingScore(i: Entity): number {
  return Math.round((i.funding_gap_index * 0.4 + i.pension_debt_to_gdp * 0.35 + i.investment_return_shortfall * 0.25) * 100 * 100) / 100;
}
function socialScore(i: Entity): number {
  return Math.round((i.intergenerational_fairness_gap * 0.4 + i.benefit_adequacy_erosion * 0.35 + i.public_pension_trust_deficit * 0.25) * 100 * 100) / 100;
}
function structuralScore(i: Entity): number {
  return Math.round((i.political_reform_paralysis * 0.4 + i.informal_economy_coverage_gap * 0.35 + i.climate_transition_stranded_assets * 0.25) * 100 * 100) / 100;
}
function compositeScore(dem: number, fun: number, soc: number, str: number): number {
  return Math.round((dem * 0.30 + fun * 0.25 + soc * 0.25 + str * 0.20) * 100) / 100;
}
function pensionRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}
function pensionPattern(i: Entity): string {
  if (i.demographic_dependency_ratio >= 0.70 && i.automation_contribution_erosion >= 0.65) return "demographic_collapse";
  if (i.funding_gap_index >= 0.70 && i.pension_debt_to_gdp >= 0.65) return "pension_insolvency";
  if (i.intergenerational_fairness_gap >= 0.70 && i.benefit_adequacy_erosion >= 0.65) return "generational_war";
  if (i.political_reform_paralysis >= 0.70 && i.public_pension_trust_deficit >= 0.65) return "reform_paralysis";
  if (i.automation_contribution_erosion >= 0.70 && i.informal_economy_coverage_gap >= 0.65) return "automation_displacement";
  return "none";
}
function pensionSeverity(comp: number): string {
  if (comp >= 75) return "pension_emergency";
  if (comp >= 50) return "pension_crisis";
  if (comp >= 25) return "pension_stress";
  return "pension_sustainable";
}
function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "pension_emergency_restructuring";
  if (risk === "high" && pattern === "pension_insolvency") return "sovereign_pension_bailout";
  if (risk === "high") return "pension_reform_program";
  if (risk === "moderate") return "pension_monitoring";
  return "no_action";
}
function pensionSignal(i: Entity, risk: string, pattern: string): string {
  const signals: Record<string, string> = {
    critical: `⚠️ ALERTE CRITIQUE — Risque d'effondrement du système de retraite détecté (${i.region})`,
    high: `🔴 RISQUE ÉLEVÉ — Intervention urgente requise pour stabiliser le système de retraite (${i.region})`,
    moderate: `🟡 RISQUE MODÉRÉ — Surveillance renforcée du système de retraite recommandée (${i.region})`,
    low: `🟢 RISQUE FAIBLE — Système de retraite stable (${i.region})`,
  };
  const patternNotes: Record<string, string> = {
    demographic_collapse: " | Motif: Effondrement démographique imminent",
    pension_insolvency: " | Motif: Insolvabilité du fonds de retraite",
    generational_war: " | Motif: Conflit intergénérationnel critique",
    reform_paralysis: " | Motif: Paralysie des réformes structurelles",
    automation_displacement: " | Motif: Érosion des cotisations par l'automatisation",
    none: "",
  };
  return (signals[risk] || "") + (patternNotes[pattern] || "");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(i => {
      const dem  = demographicScore(i);
      const fun  = fundingScore(i);
      const soc  = socialScore(i);
      const str  = structuralScore(i);
      const comp = compositeScore(dem, fun, soc, str);
      const risk = pensionRisk(comp);
      const pattern = pensionPattern(i);
      const severity = pensionSeverity(comp);
      const action = recommendedAction(risk, pattern);
      return {
        entity_id: i.entity_id,
        region: i.region,
        pension_system_type: i.pension_system_type,
        pension_risk: risk,
        pension_pattern: pattern,
        pension_severity: severity,
        recommended_action: action,
        demographic_score: dem,
        funding_score: fun,
        social_score: soc,
        structural_score: str,
        pension_composite: comp,
        is_pension_crisis: comp >= 60,
        requires_pension_intervention: comp >= 40,
        pension_signal: pensionSignal(i, risk, pattern),
      };
    });

    const rc: Record<string, number> = {}, pc: Record<string, number> = {}, sc: Record<string, number> = {}, ac: Record<string, number> = {};
    let tDem = 0, tFun = 0, tSoc = 0, tStr = 0, tComp = 0, crisisCount = 0, interventionCount = 0;
    for (const e of entities) {
      rc[e.pension_risk] = (rc[e.pension_risk] || 0) + 1;
      pc[e.pension_pattern] = (pc[e.pension_pattern] || 0) + 1;
      sc[e.pension_severity] = (sc[e.pension_severity] || 0) + 1;
      ac[e.recommended_action] = (ac[e.recommended_action] || 0) + 1;
      tDem += e.demographic_score;
      tFun += e.funding_score;
      tSoc += e.social_score;
      tStr += e.structural_score;
      tComp += e.pension_composite;
      if (e.is_pension_crisis) crisisCount++;
      if (e.requires_pension_intervention) interventionCount++;
    }
    const n = entities.length;
    const avgComp = tComp / n;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        module: "Module 320 — Pension & Social Security System Collapse Intelligence Engine",
        total: n,
        risk_counts: rc,
        pattern_counts: pc,
        severity_counts: sc,
        action_counts: ac,
        avg_demographic_score: Math.round(tDem / n * 100) / 100,
        avg_funding_score: Math.round(tFun / n * 100) / 100,
        avg_social_score: Math.round(tSoc / n * 100) / 100,
        avg_structural_score: Math.round(tStr / n * 100) / 100,
        avg_pension_composite: Math.round(avgComp * 100) / 100,
        crisis_count: crisisCount,
        intervention_count: interventionCount,
        avg_estimated_pension_crisis_index: Math.round(avgComp / 100 * 10 * 100) / 100,
      },
    } as Record<string, unknown>));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/pension-collapse-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json() as Record<string, unknown>));
  } catch {
    return NextResponse.json(sealResponse({ error: "Upstream unavailable" } as Record<string, unknown>), { status: 502 });
  }
}
