import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // ICE-001 — critical, market_exit_uninsurability (uninsurability>0.85, market_exit>0.80)
  {
    id: "ICE-001", risk_category: "coastal_property", region: "NOAM",
    uninsurability_rate: 0.92, premium_increase_trajectory: 0.75,
    insurer_market_exit_rate: 0.88, government_backstop_dependence: 0.72,
    stranded_property_value: 0.70, flood_zone_exposure: 0.85,
    wildfire_risk_penetration: 0.65, storm_surge_vulnerability: 0.80,
    regulatory_solvency_risk: 0.68, reinsurance_withdrawal: 0.72,
    parametric_solution_gap: 0.65, low_income_exposure: 0.70,
    mortgage_market_contagion: 0.68, infrastructure_coverage_gap: 0.65,
    climate_model_uncertainty: 0.60, political_risk_influence: 0.62,
    innovation_solution_adoption: 0.30,
  },
  // ICE-002 — critical, premium_unaffordability_crisis (premium>0.85, low_income>0.80)
  {
    id: "ICE-002", risk_category: "wildfire_zone", region: "NOAM",
    uninsurability_rate: 0.72, premium_increase_trajectory: 0.90,
    insurer_market_exit_rate: 0.68, government_backstop_dependence: 0.75,
    stranded_property_value: 0.65, flood_zone_exposure: 0.58,
    wildfire_risk_penetration: 0.88, storm_surge_vulnerability: 0.50,
    regulatory_solvency_risk: 0.70, reinsurance_withdrawal: 0.68,
    parametric_solution_gap: 0.70, low_income_exposure: 0.85,
    mortgage_market_contagion: 0.65, infrastructure_coverage_gap: 0.68,
    climate_model_uncertainty: 0.62, political_risk_influence: 0.58,
    innovation_solution_adoption: 0.28,
  },
  // ICE-003 — critical, government_insurer_last_resort (gov_backstop>0.85, reg_solvency>0.80)
  {
    id: "ICE-003", risk_category: "flood_plain", region: "EMEA",
    uninsurability_rate: 0.78, premium_increase_trajectory: 0.72,
    insurer_market_exit_rate: 0.75, government_backstop_dependence: 0.90,
    stranded_property_value: 0.68, flood_zone_exposure: 0.82,
    wildfire_risk_penetration: 0.55, storm_surge_vulnerability: 0.75,
    regulatory_solvency_risk: 0.85, reinsurance_withdrawal: 0.72,
    parametric_solution_gap: 0.68, low_income_exposure: 0.70,
    mortgage_market_contagion: 0.65, infrastructure_coverage_gap: 0.62,
    climate_model_uncertainty: 0.65, political_risk_influence: 0.70,
    innovation_solution_adoption: 0.25,
  },
  // ICE-004 — high, stranded_asset_collapse (stranded>0.80, mortgage>0.75)
  {
    id: "ICE-004", risk_category: "coastal_urban", region: "APAC",
    uninsurability_rate: 0.55, premium_increase_trajectory: 0.52,
    insurer_market_exit_rate: 0.50, government_backstop_dependence: 0.55,
    stranded_property_value: 0.85, flood_zone_exposure: 0.58,
    wildfire_risk_penetration: 0.45, storm_surge_vulnerability: 0.60,
    regulatory_solvency_risk: 0.50, reinsurance_withdrawal: 0.52,
    parametric_solution_gap: 0.48, low_income_exposure: 0.52,
    mortgage_market_contagion: 0.80, infrastructure_coverage_gap: 0.50,
    climate_model_uncertainty: 0.52, political_risk_influence: 0.48,
    innovation_solution_adoption: 0.35,
  },
  // ICE-005 — high, systemic_financial_contagion (reinsurance>0.80, infra_gap>0.75)
  {
    id: "ICE-005", risk_category: "reinsurance_market", region: "EMEA",
    uninsurability_rate: 0.50, premium_increase_trajectory: 0.52,
    insurer_market_exit_rate: 0.48, government_backstop_dependence: 0.50,
    stranded_property_value: 0.52, flood_zone_exposure: 0.50,
    wildfire_risk_penetration: 0.48, storm_surge_vulnerability: 0.50,
    regulatory_solvency_risk: 0.55, reinsurance_withdrawal: 0.85,
    parametric_solution_gap: 0.52, low_income_exposure: 0.50,
    mortgage_market_contagion: 0.52, infrastructure_coverage_gap: 0.80,
    climate_model_uncertainty: 0.50, political_risk_influence: 0.48,
    innovation_solution_adoption: 0.32,
  },
  // ICE-006 — moderate, none
  {
    id: "ICE-006", risk_category: "agricultural", region: "LATAM",
    uninsurability_rate: 0.32, premium_increase_trajectory: 0.30,
    insurer_market_exit_rate: 0.28, government_backstop_dependence: 0.30,
    stranded_property_value: 0.28, flood_zone_exposure: 0.30,
    wildfire_risk_penetration: 0.32, storm_surge_vulnerability: 0.28,
    regulatory_solvency_risk: 0.30, reinsurance_withdrawal: 0.28,
    parametric_solution_gap: 0.32, low_income_exposure: 0.30,
    mortgage_market_contagion: 0.28, infrastructure_coverage_gap: 0.30,
    climate_model_uncertainty: 0.32, political_risk_influence: 0.28,
    innovation_solution_adoption: 0.50,
  },
  // ICE-007 — low, none
  {
    id: "ICE-007", risk_category: "inland_commercial", region: "EMEA",
    uninsurability_rate: 0.10, premium_increase_trajectory: 0.12,
    insurer_market_exit_rate: 0.10, government_backstop_dependence: 0.08,
    stranded_property_value: 0.10, flood_zone_exposure: 0.08,
    wildfire_risk_penetration: 0.10, storm_surge_vulnerability: 0.08,
    regulatory_solvency_risk: 0.10, reinsurance_withdrawal: 0.12,
    parametric_solution_gap: 0.10, low_income_exposure: 0.08,
    mortgage_market_contagion: 0.10, infrastructure_coverage_gap: 0.08,
    climate_model_uncertainty: 0.12, political_risk_influence: 0.10,
    innovation_solution_adoption: 0.75,
  },
  // ICE-008 — low, none
  {
    id: "ICE-008", risk_category: "municipal_infrastructure", region: "NOAM",
    uninsurability_rate: 0.12, premium_increase_trajectory: 0.10,
    insurer_market_exit_rate: 0.12, government_backstop_dependence: 0.10,
    stranded_property_value: 0.08, flood_zone_exposure: 0.10,
    wildfire_risk_penetration: 0.08, storm_surge_vulnerability: 0.10,
    regulatory_solvency_risk: 0.12, reinsurance_withdrawal: 0.10,
    parametric_solution_gap: 0.12, low_income_exposure: 0.10,
    mortgage_market_contagion: 0.08, infrastructure_coverage_gap: 0.10,
    climate_model_uncertainty: 0.10, political_risk_influence: 0.12,
    innovation_solution_adoption: 0.70,
  },
];

type ICEInput = typeof MOCK_ENTITIES[0];

function uninsurabilityScore(e: ICEInput): number {
  return Math.round((e.uninsurability_rate * 0.4 + e.insurer_market_exit_rate * 0.35 + e.flood_zone_exposure * 0.25) * 100 * 100) / 100;
}
function affordabilityScore(e: ICEInput): number {
  return Math.round((e.premium_increase_trajectory * 0.4 + e.low_income_exposure * 0.35 + e.parametric_solution_gap * 0.25) * 100 * 100) / 100;
}
function marketFailureScore(e: ICEInput): number {
  return Math.round((e.reinsurance_withdrawal * 0.4 + e.government_backstop_dependence * 0.35 + e.regulatory_solvency_risk * 0.25) * 100 * 100) / 100;
}
function systemicScore(e: ICEInput): number {
  return Math.round((e.mortgage_market_contagion * 0.4 + e.stranded_property_value * 0.35 + e.infrastructure_coverage_gap * 0.25) * 100 * 100) / 100;
}
function compositeScore(u: number, a: number, m: number, s: number): number {
  return Math.round((u * 0.30 + a * 0.25 + m * 0.25 + s * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function insurancePattern(e: ICEInput): string {
  if (e.uninsurability_rate > 0.85 && e.insurer_market_exit_rate > 0.80) return "market_exit_uninsurability";
  if (e.premium_increase_trajectory > 0.85 && e.low_income_exposure > 0.80) return "premium_unaffordability_crisis";
  if (e.government_backstop_dependence > 0.85 && e.regulatory_solvency_risk > 0.80) return "government_insurer_last_resort";
  if (e.stranded_property_value > 0.80 && e.mortgage_market_contagion > 0.75) return "stranded_asset_collapse";
  if (e.reinsurance_withdrawal > 0.80 && e.infrastructure_coverage_gap > 0.75) return "systemic_financial_contagion";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_assurance_climatique_systémique";
  if (composite >= 40) return "retrait_couverture_majeur_détecté";
  if (composite >= 20) return "stress_marché_assurance_structurel";
  return "surveillance_risque_assurance_active";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_retrait_couverture_critique";
  if (risk === "high") return "restructuration_marché_assurance_accélérée";
  if (risk === "moderate") return "renforcement_mécanismes_assurance_publique";
  return "veille_risque_assurance_climatique_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise assurance climatique systémique — retrait couverture en péril";
  if (risk === "high") return "🟠 Retrait couverture majeur détecté — marché en stress";
  if (risk === "moderate") return "🟡 Stress marché assurance structurel actif";
  return "🟢 Risque assurance climatique sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const u    = uninsurabilityScore(e);
      const a    = affordabilityScore(e);
      const m    = marketFailureScore(e);
      const s    = systemicScore(e);
      const comp = compositeScore(u, a, m, s);
      const risk = riskLevel(comp);
      const pat  = insurancePattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:               e.entity_id,
        risk_category:           e.risk_category,
        region:                  e.region,
        uninsurability_score:    u,
        affordability_score:     a,
        market_failure_score:    m,
        systemic_score:          s,
        composite_score:         comp,
        risk_level:              risk,
        insurance_pattern:       pat,
        severity:                sev,
        recommended_action:      action,
        signal:                  sig,
        uninsurability_rate:     e.uninsurability_rate,
        reinsurance_withdrawal:  e.reinsurance_withdrawal,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tU = 0, tA = 0, tM = 0, tS = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.insurance_pattern] = (pattern_distribution[ent.insurance_pattern] || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tU    += ent.uninsurability_score;
      tA    += ent.affordability_score;
      tM    += ent.market_failure_score;
      tS    += ent.systemic_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite       = Math.round(tComp / n * 10) / 10;
    const avgUninsurability  = Math.round(tU    / n * 10) / 10;

    const summary = {
      module_id:                                427,
      module_name:                              "Assurance Risque Climatique & Retrait Couverture Intelligence Engine",
      total:                                    n,
      critical:                                 criticalCount,
      high:                                     highCount,
      moderate:                                 moderateCount,
      low:                                      lowCount,
      avg_composite:                            avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_insurance_retreat_index:    Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, avg_uninsurability: avgUninsurability }, "insurance-climate-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/insurance-climate-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "insurance-climate-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "insurance-climate-engine"),
      { status: 502 }
    );
  }
}
