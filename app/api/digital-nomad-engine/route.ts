import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // DNE-001 — critical, housing_gentrification_explosion (housing_spike>0.85, displacement>0.80)
  {
    id: "DNE-001", destination_type: "ville_côtière", region: "EMEA",
    housing_price_spike: 0.92, local_displacement_rate: 0.88,
    rental_market_distortion: 0.82, tax_contribution_gap: 0.70,
    visa_fee_revenue: 0.65, local_wage_disparity: 0.72,
    cultural_commodification: 0.68, service_sector_overload: 0.65,
    co_working_space_monopoly: 0.70, brain_gain_local_benefit: 0.68,
    digital_infrastructure_strain: 0.72, social_cohesion_impact: 0.65,
    regulatory_clarity: 0.60, income_inequality_amplification: 0.68,
    seasonal_volatility: 0.62, environmental_footprint: 0.65,
    integration_quality: 0.60,
  },
  // DNE-002 — critical, tax_base_erosion_crisis (tax_gap>0.85, visa_fee>0.80)
  {
    id: "DNE-002", destination_type: "hub_numérique", region: "APAC",
    housing_price_spike: 0.62, local_displacement_rate: 0.60,
    rental_market_distortion: 0.65, tax_contribution_gap: 0.90,
    visa_fee_revenue: 0.85, local_wage_disparity: 0.72,
    cultural_commodification: 0.68, service_sector_overload: 0.65,
    co_working_space_monopoly: 0.70, brain_gain_local_benefit: 0.75,
    digital_infrastructure_strain: 0.72, social_cohesion_impact: 0.68,
    regulatory_clarity: 0.65, income_inequality_amplification: 0.70,
    seasonal_volatility: 0.65, environmental_footprint: 0.68,
    integration_quality: 0.62,
  },
  // DNE-003 — critical, cultural_displacement_trap (cultural_com>0.85, service_overload>0.80)
  {
    id: "DNE-003", destination_type: "île_tropicale", region: "LATAM",
    housing_price_spike: 0.72, local_displacement_rate: 0.68,
    rental_market_distortion: 0.70, tax_contribution_gap: 0.65,
    visa_fee_revenue: 0.60, local_wage_disparity: 0.68,
    cultural_commodification: 0.90, service_sector_overload: 0.85,
    co_working_space_monopoly: 0.72, brain_gain_local_benefit: 0.65,
    digital_infrastructure_strain: 0.68, social_cohesion_impact: 0.72,
    regulatory_clarity: 0.60, income_inequality_amplification: 0.65,
    seasonal_volatility: 0.62, environmental_footprint: 0.68,
    integration_quality: 0.60,
  },
  // DNE-004 — high, two_tier_economy_formation (wage_disparity>0.80, income_ineq>0.75)
  {
    id: "DNE-004", destination_type: "zone_économique_spéciale", region: "SSA",
    housing_price_spike: 0.48, local_displacement_rate: 0.45,
    rental_market_distortion: 0.50, tax_contribution_gap: 0.52,
    visa_fee_revenue: 0.48, local_wage_disparity: 0.85,
    cultural_commodification: 0.50, service_sector_overload: 0.48,
    co_working_space_monopoly: 0.52, brain_gain_local_benefit: 0.50,
    digital_infrastructure_strain: 0.48, social_cohesion_impact: 0.52,
    regulatory_clarity: 0.48, income_inequality_amplification: 0.80,
    seasonal_volatility: 0.48, environmental_footprint: 0.50,
    integration_quality: 0.48,
  },
  // DNE-005 — high, regulatory_arbitrage_race (reg_clarity>0.80, seasonal_vol>0.75)
  {
    id: "DNE-005", destination_type: "ville_universitaire", region: "NOAM",
    housing_price_spike: 0.45, local_displacement_rate: 0.42,
    rental_market_distortion: 0.48, tax_contribution_gap: 0.50,
    visa_fee_revenue: 0.45, local_wage_disparity: 0.48,
    cultural_commodification: 0.50, service_sector_overload: 0.45,
    co_working_space_monopoly: 0.48, brain_gain_local_benefit: 0.50,
    digital_infrastructure_strain: 0.48, social_cohesion_impact: 0.45,
    regulatory_clarity: 0.85, income_inequality_amplification: 0.50,
    seasonal_volatility: 0.80, environmental_footprint: 0.48,
    integration_quality: 0.45,
  },
  // DNE-006 — moderate, none
  {
    id: "DNE-006", destination_type: "village_rural", region: "EMEA",
    housing_price_spike: 0.30, local_displacement_rate: 0.28,
    rental_market_distortion: 0.30, tax_contribution_gap: 0.32,
    visa_fee_revenue: 0.28, local_wage_disparity: 0.30,
    cultural_commodification: 0.32, service_sector_overload: 0.28,
    co_working_space_monopoly: 0.30, brain_gain_local_benefit: 0.32,
    digital_infrastructure_strain: 0.28, social_cohesion_impact: 0.30,
    regulatory_clarity: 0.32, income_inequality_amplification: 0.28,
    seasonal_volatility: 0.30, environmental_footprint: 0.28,
    integration_quality: 0.30,
  },
  // DNE-007 — low, none
  {
    id: "DNE-007", destination_type: "métropole_diversifiée", region: "NOAM",
    housing_price_spike: 0.10, local_displacement_rate: 0.08,
    rental_market_distortion: 0.10, tax_contribution_gap: 0.12,
    visa_fee_revenue: 0.08, local_wage_disparity: 0.10,
    cultural_commodification: 0.12, service_sector_overload: 0.08,
    co_working_space_monopoly: 0.10, brain_gain_local_benefit: 0.12,
    digital_infrastructure_strain: 0.08, social_cohesion_impact: 0.10,
    regulatory_clarity: 0.12, income_inequality_amplification: 0.08,
    seasonal_volatility: 0.10, environmental_footprint: 0.08,
    integration_quality: 0.10,
  },
  // DNE-008 — low, none
  {
    id: "DNE-008", destination_type: "ville_intermédiaire", region: "APAC",
    housing_price_spike: 0.12, local_displacement_rate: 0.10,
    rental_market_distortion: 0.12, tax_contribution_gap: 0.10,
    visa_fee_revenue: 0.12, local_wage_disparity: 0.10,
    cultural_commodification: 0.10, service_sector_overload: 0.12,
    co_working_space_monopoly: 0.10, brain_gain_local_benefit: 0.10,
    digital_infrastructure_strain: 0.12, social_cohesion_impact: 0.10,
    regulatory_clarity: 0.08, income_inequality_amplification: 0.10,
    seasonal_volatility: 0.12, environmental_footprint: 0.10,
    integration_quality: 0.12,
  },
];

type DNEInput = typeof MOCK_ENTITIES[0];

function gentrificationScore(e: DNEInput): number {
  return Math.round((e.housing_price_spike * 0.4 + e.local_displacement_rate * 0.35 + e.rental_market_distortion * 0.25) * 100 * 100) / 100;
}
function taxEvasionScore(e: DNEInput): number {
  return Math.round((e.tax_contribution_gap * 0.4 + e.visa_fee_revenue * 0.35 + e.local_wage_disparity * 0.25) * 100 * 100) / 100;
}
function inequalityScore(e: DNEInput): number {
  return Math.round((e.cultural_commodification * 0.4 + e.service_sector_overload * 0.35 + e.co_working_space_monopoly * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: DNEInput): number {
  return Math.round((e.brain_gain_local_benefit * 0.4 + e.digital_infrastructure_strain * 0.35 + e.social_cohesion_impact * 0.25) * 100 * 100) / 100;
}
function compositeScore(gen: number, tax: number, ineq: number, gov: number): number {
  return Math.round((gen * 0.30 + tax * 0.25 + ineq * 0.25 + gov * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function nomadPattern(e: DNEInput): string {
  if (e.housing_price_spike > 0.85 && e.local_displacement_rate > 0.80) return "housing_gentrification_explosion";
  if (e.tax_contribution_gap > 0.85 && e.visa_fee_revenue > 0.80) return "tax_base_erosion_crisis";
  if (e.cultural_commodification > 0.85 && e.service_sector_overload > 0.80) return "cultural_displacement_trap";
  if (e.local_wage_disparity > 0.80 && e.income_inequality_amplification > 0.75) return "two_tier_economy_formation";
  if (e.regulatory_clarity > 0.80 && e.seasonal_volatility > 0.75) return "regulatory_arbitrage_race";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_gentrification_nomade_systémique";
  if (composite >= 40) return "crise_impact_local_majeure";
  if (composite >= 20) return "inégalité_économique_structurelle";
  return "impact_nomade_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_protection_résidents_locaux";
  if (risk === "high") return "régulation_accélérée_marché_immobilier_nomade";
  if (risk === "moderate") return "renforcement_politiques_intégration_économique";
  return "veille_impact_nomade_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise gentrification nomade systémique — impact local en péril";
  if (risk === "high") return "🟠 Crise impact local majeure détectée";
  if (risk === "moderate") return "🟡 Inégalité économique structurelle active";
  return "🟢 Impact nomade sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const gen  = gentrificationScore(e);
      const tax  = taxEvasionScore(e);
      const ineq = inequalityScore(e);
      const gov  = governanceScore(e);
      const comp = compositeScore(gen, tax, ineq, gov);
      const risk = riskLevel(comp);
      const pat  = nomadPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:                  e.entity_id,
        destination_type:           e.destination_type,
        region:                     e.region,
        gentrification_score:       gen,
        tax_evasion_score:          tax,
        inequality_score:           ineq,
        governance_score:           gov,
        composite_score:            comp,
        risk_level:                 risk,
        nomad_pattern:              pat,
        severity:                   sev,
        recommended_action:         action,
        signal:                     sig,
        housing_price_spike:        e.housing_price_spike,
        local_displacement_rate:    e.local_displacement_rate,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tGen = 0, tTax = 0, tIneq = 0, tGov = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.nomad_pattern]     = (pattern_distribution[ent.nomad_pattern]     || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tGen  += ent.gentrification_score;
      tTax  += ent.tax_evasion_score;
      tIneq += ent.inequality_score;
      tGov  += ent.governance_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;
    const avgGentrification = Math.round(tGen / n * 10) / 10;

    const summary = {
      module_id:                           430,
      module_name:                         "Économie Nomades Numériques & Impact Local Intelligence Engine",
      total:                               n,
      critical:                            criticalCount,
      high:                                highCount,
      moderate:                            moderateCount,
      low:                                 lowCount,
      avg_composite:                       avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_nomad_impact_index:    Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, avg_gentrification: avgGentrification }, "digital-nomad-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/digital-nomad-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "digital-nomad-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "digital-nomad-engine"),
      { status: 502 }
    );
  }
}
