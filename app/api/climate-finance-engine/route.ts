import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ─── Math (mirrors Python exactly) ───────────────────────────────────────────

interface CfeInput {
  entity_id: string;
  finance_domain: string;
  region: string;
  stranded_asset_exposure_rate: number;
  green_washing_prevalence_index: number;
  climate_finance_gap_severity: number;
  carbon_credit_integrity_risk: number;
  transition_risk_repricing_speed: number;
  physical_risk_underpricing_level: number;
  fossil_fuel_finance_lock_in: number;
  just_transition_funding_deficit: number;
  green_bond_market_fragility: number;
  climate_regulatory_arbitrage_risk: number;
  sovereign_climate_default_risk: number;
  climate_litigation_financial_risk: number;
  insurance_climate_retreat_rate: number;
  private_climate_finance_mobilization_gap: number;
  carbon_border_adjustment_shock: number;
  biodiversity_finance_gap: number;
  climate_finance_south_north_inequality: number;
}

function strandedScore(e: CfeInput): number {
  return Math.round((e.stranded_asset_exposure_rate * 0.4 + e.fossil_fuel_finance_lock_in * 0.35 + e.transition_risk_repricing_speed * 0.25) * 100 * 100) / 100;
}

function integrityScore(e: CfeInput): number {
  return Math.round((e.green_washing_prevalence_index * 0.4 + e.carbon_credit_integrity_risk * 0.35 + e.climate_regulatory_arbitrage_risk * 0.25) * 100 * 100) / 100;
}

function gapScore(e: CfeInput): number {
  return Math.round((e.climate_finance_gap_severity * 0.4 + e.just_transition_funding_deficit * 0.35 + e.private_climate_finance_mobilization_gap * 0.25) * 100 * 100) / 100;
}

function systemicScore(e: CfeInput): number {
  return Math.round((e.sovereign_climate_default_risk * 0.4 + e.insurance_climate_retreat_rate * 0.35 + e.climate_finance_south_north_inequality * 0.25) * 100 * 100) / 100;
}

function compositeScore(str: number, intg: number, gap: number, sys: number): number {
  return Math.round((str * 0.30 + intg * 0.25 + gap * 0.25 + sys * 0.20) * 100) / 100;
}

function climateFinancePattern(e: CfeInput): string {
  if (e.stranded_asset_exposure_rate >= 0.70 && e.fossil_fuel_finance_lock_in >= 0.65) return "stranded_asset_crisis";
  if (e.green_washing_prevalence_index >= 0.70 && e.carbon_credit_integrity_risk >= 0.65) return "green_washing_epidemic";
  if (e.climate_finance_gap_severity >= 0.70 && e.private_climate_finance_mobilization_gap >= 0.65) return "climate_finance_collapse";
  if (e.sovereign_climate_default_risk >= 0.70 && e.physical_risk_underpricing_level >= 0.65) return "sovereign_climate_default";
  if (e.insurance_climate_retreat_rate >= 0.70 && e.climate_finance_south_north_inequality >= 0.65) return "insurance_retreat_cascade";
  return "none";
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function severity(risk: string): string {
  const m: Record<string, string> = {
    critical: "crise_finance_climatique_systémique",
    high:     "risque_transition_verte_majeur",
    moderate: "fragilité_finance_climatique_structurelle",
    low:      "finance_climatique_sous_surveillance",
  };
  return m[risk] ?? risk;
}

function recommendedAction(risk: string): string {
  const m: Record<string, string> = {
    critical: "intervention_finance_climatique_urgente",
    high:     "réforme_finance_verte_accélérée",
    moderate: "renforcement_intégrité_finance_climatique",
    low:      "veille_finance_climatique_continue",
  };
  return m[risk] ?? risk;
}

function signal(risk: string): string {
  const m: Record<string, string> = {
    critical: "🔴 Crise finance climatique systémique — transition verte compromise",
    high:     "🟠 Risque transition verte majeur détecté",
    moderate: "🟡 Fragilité finance climatique structurelle active",
    low:      "🟢 Finance climatique sous surveillance",
  };
  return m[risk] ?? risk;
}

function analyzeEntity(e: CfeInput) {
  const str  = strandedScore(e);
  const intg = integrityScore(e);
  const gap  = gapScore(e);
  const sys  = systemicScore(e);
  const comp = compositeScore(str, intg, gap, sys);
  const pat  = climateFinancePattern(e);
  const risk = riskLevel(comp);
  const sev  = severity(risk);
  const action = recommendedAction(risk);
  const sig  = signal(risk);

  return {
    entity_id:                    e.entity_id,
    finance_domain:               e.finance_domain,
    region:                       e.region,
    stranded_score:               str,
    integrity_score:              intg,
    gap_score:                    gap,
    systemic_score:               sys,
    composite_score:              comp,
    risk_level:                   risk,
    climate_finance_pattern:      pat,
    severity:                     sev,
    recommended_action:           action,
    signal:                       sig,
    stranded_asset_exposure_rate: e.stranded_asset_exposure_rate,
    climate_finance_gap_severity: e.climate_finance_gap_severity,
  };
}

// ─── Mock entities ────────────────────────────────────────────────────────────

const mockEntities = (() => {
  // CFE-001: critical + stranded_asset_crisis
  // stranded=0.85>=0.70, fossil=0.80>=0.65 → stranded_asset_crisis
  // stranded_score=(0.85*0.4+0.80*0.35+0.78*0.25)*100=81.5
  // integrity=(0.75*0.4+0.70*0.35+0.68*0.25)*100=71.5
  // gap=(0.72*0.4+0.68*0.35+0.65*0.25)*100=68.85
  // systemic=(0.70*0.4+0.68*0.35+0.65*0.25)*100=68.05
  // composite=81.5*0.30+71.5*0.25+68.85*0.25+68.05*0.20=73.15 → critical
  const e1 = analyzeEntity({
    entity_id: "CFE-001", finance_domain: "fossil_fuel_banking", region: "EMEA",
    stranded_asset_exposure_rate: 0.85, fossil_fuel_finance_lock_in: 0.80,
    transition_risk_repricing_speed: 0.78, green_washing_prevalence_index: 0.75,
    carbon_credit_integrity_risk: 0.70, climate_regulatory_arbitrage_risk: 0.68,
    climate_finance_gap_severity: 0.72, just_transition_funding_deficit: 0.68,
    private_climate_finance_mobilization_gap: 0.65, sovereign_climate_default_risk: 0.70,
    insurance_climate_retreat_rate: 0.68, climate_finance_south_north_inequality: 0.65,
    physical_risk_underpricing_level: 0.72, green_bond_market_fragility: 0.68,
    climate_litigation_financial_risk: 0.65, carbon_border_adjustment_shock: 0.70,
    biodiversity_finance_gap: 0.68,
  });

  // CFE-002: low + none
  // all values ~0.10-0.20 → composite very low → low
  const e2 = analyzeEntity({
    entity_id: "CFE-002", finance_domain: "green_bonds", region: "NAMER",
    stranded_asset_exposure_rate: 0.10, fossil_fuel_finance_lock_in: 0.12,
    transition_risk_repricing_speed: 0.11, green_washing_prevalence_index: 0.10,
    carbon_credit_integrity_risk: 0.12, climate_regulatory_arbitrage_risk: 0.10,
    climate_finance_gap_severity: 0.11, just_transition_funding_deficit: 0.10,
    private_climate_finance_mobilization_gap: 0.12, sovereign_climate_default_risk: 0.10,
    insurance_climate_retreat_rate: 0.11, climate_finance_south_north_inequality: 0.10,
    physical_risk_underpricing_level: 0.10, green_bond_market_fragility: 0.12,
    climate_litigation_financial_risk: 0.10, carbon_border_adjustment_shock: 0.11,
    biodiversity_finance_gap: 0.10,
  });

  // CFE-003: high + green_washing_epidemic
  // green_wash=0.78>=0.70, carbon_credit=0.72>=0.65 → green_washing_epidemic
  // stranded<0.70 OR fossil<0.65 → no stranded_asset_crisis: stranded=0.48, fossil=0.45
  // Need composite 40-59 for "high"
  // stranded=(0.48*0.4+0.45*0.35+0.50*0.25)*100=46.45
  // integrity=(0.78*0.4+0.72*0.35+0.65*0.25)*100=73.7
  // gap=(0.52*0.4+0.48*0.35+0.50*0.25)*100=49.9
  // systemic=(0.48*0.4+0.50*0.35+0.48*0.25)*100=48.7
  // composite=46.45*0.30+73.7*0.25+49.9*0.25+48.7*0.20=13.935+18.425+12.475+9.74=54.575 → high
  const e3 = analyzeEntity({
    entity_id: "CFE-003", finance_domain: "esg_investment", region: "APAC",
    stranded_asset_exposure_rate: 0.48, fossil_fuel_finance_lock_in: 0.45,
    transition_risk_repricing_speed: 0.50, green_washing_prevalence_index: 0.78,
    carbon_credit_integrity_risk: 0.72, climate_regulatory_arbitrage_risk: 0.65,
    climate_finance_gap_severity: 0.52, just_transition_funding_deficit: 0.48,
    private_climate_finance_mobilization_gap: 0.50, sovereign_climate_default_risk: 0.48,
    insurance_climate_retreat_rate: 0.50, climate_finance_south_north_inequality: 0.48,
    physical_risk_underpricing_level: 0.50, green_bond_market_fragility: 0.55,
    climate_litigation_financial_risk: 0.52, carbon_border_adjustment_shock: 0.48,
    biodiversity_finance_gap: 0.50,
  });

  // CFE-004: low + none
  const e4 = analyzeEntity({
    entity_id: "CFE-004", finance_domain: "climate_insurance", region: "LATAM",
    stranded_asset_exposure_rate: 0.15, fossil_fuel_finance_lock_in: 0.18,
    transition_risk_repricing_speed: 0.14, green_washing_prevalence_index: 0.15,
    carbon_credit_integrity_risk: 0.12, climate_regulatory_arbitrage_risk: 0.14,
    climate_finance_gap_severity: 0.16, just_transition_funding_deficit: 0.14,
    private_climate_finance_mobilization_gap: 0.15, sovereign_climate_default_risk: 0.12,
    insurance_climate_retreat_rate: 0.14, climate_finance_south_north_inequality: 0.13,
    physical_risk_underpricing_level: 0.14, green_bond_market_fragility: 0.15,
    climate_litigation_financial_risk: 0.12, carbon_border_adjustment_shock: 0.14,
    biodiversity_finance_gap: 0.15,
  });

  // CFE-005: critical + climate_finance_collapse
  // gap=0.82>=0.70, private_mobilization=0.75>=0.65 → climate_finance_collapse
  // stranded<0.70 OR fossil<0.65: stranded=0.50, fossil=0.48
  // green_wash<0.70 OR carbon<0.65: green_wash=0.55, carbon=0.52
  // stranded=(0.50*0.4+0.48*0.35+0.65*0.25)*100=51.3
  // integrity=(0.55*0.4+0.52*0.35+0.58*0.25)*100=54.7
  // gap=(0.82*0.4+0.78*0.35+0.75*0.25)*100=79.55
  // systemic=(0.68*0.4+0.72*0.35+0.70*0.25)*100=70.2
  // composite=51.3*0.30+54.7*0.25+79.55*0.25+70.2*0.20=15.39+13.675+19.8875+14.04=62.99 → critical
  const e5 = analyzeEntity({
    entity_id: "CFE-005", finance_domain: "development_finance", region: "MEA",
    stranded_asset_exposure_rate: 0.50, fossil_fuel_finance_lock_in: 0.48,
    transition_risk_repricing_speed: 0.65, green_washing_prevalence_index: 0.55,
    carbon_credit_integrity_risk: 0.52, climate_regulatory_arbitrage_risk: 0.58,
    climate_finance_gap_severity: 0.82, just_transition_funding_deficit: 0.78,
    private_climate_finance_mobilization_gap: 0.75, sovereign_climate_default_risk: 0.68,
    insurance_climate_retreat_rate: 0.72, climate_finance_south_north_inequality: 0.70,
    physical_risk_underpricing_level: 0.62, green_bond_market_fragility: 0.68,
    climate_litigation_financial_risk: 0.60, carbon_border_adjustment_shock: 0.65,
    biodiversity_finance_gap: 0.70,
  });

  // CFE-006: moderate + none
  // all mid values 0.30-0.45, need composite 20-39
  // stranded=(0.32*0.4+0.30*0.35+0.35*0.25)*100=31.75
  // integrity=(0.35*0.4+0.32*0.35+0.30*0.25)*100=33.2
  // gap=(0.38*0.4+0.35*0.35+0.32*0.25)*100=35.45
  // systemic=(0.30*0.4+0.32*0.35+0.28*0.25)*100=30.2
  // composite=31.75*0.30+33.2*0.25+35.45*0.25+30.2*0.20=9.525+8.3+8.8625+6.04=32.73 → moderate
  const e6 = analyzeEntity({
    entity_id: "CFE-006", finance_domain: "sovereign_bonds", region: "EMEA",
    stranded_asset_exposure_rate: 0.32, fossil_fuel_finance_lock_in: 0.30,
    transition_risk_repricing_speed: 0.35, green_washing_prevalence_index: 0.35,
    carbon_credit_integrity_risk: 0.32, climate_regulatory_arbitrage_risk: 0.30,
    climate_finance_gap_severity: 0.38, just_transition_funding_deficit: 0.35,
    private_climate_finance_mobilization_gap: 0.32, sovereign_climate_default_risk: 0.30,
    insurance_climate_retreat_rate: 0.32, climate_finance_south_north_inequality: 0.28,
    physical_risk_underpricing_level: 0.30, green_bond_market_fragility: 0.35,
    climate_litigation_financial_risk: 0.30, carbon_border_adjustment_shock: 0.32,
    biodiversity_finance_gap: 0.35,
  });

  // CFE-007: high + sovereign_climate_default
  // sovereign=0.75>=0.70, physical=0.70>=0.65 → sovereign_climate_default
  // stranded<0.70 OR fossil<0.65: stranded=0.45, fossil=0.42
  // green_wash<0.70 OR carbon<0.65: green_wash=0.50, carbon=0.48
  // gap<0.70 OR private<0.65: gap=0.52, private=0.50
  // stranded=(0.45*0.4+0.42*0.35+0.50*0.25)*100=43.7
  // integrity=(0.50*0.4+0.48*0.35+0.50*0.25)*100=49.3
  // gap=(0.52*0.4+0.50*0.35+0.50*0.25)*100=50.3
  // systemic=(0.75*0.4+0.58*0.35+0.55*0.25)*100=64.05
  // composite=43.7*0.30+49.3*0.25+50.3*0.25+64.05*0.20=13.11+12.325+12.575+12.81=50.82 → high
  const e7 = analyzeEntity({
    entity_id: "CFE-007", finance_domain: "sovereign_climate_debt", region: "APAC",
    stranded_asset_exposure_rate: 0.45, fossil_fuel_finance_lock_in: 0.42,
    transition_risk_repricing_speed: 0.50, green_washing_prevalence_index: 0.50,
    carbon_credit_integrity_risk: 0.48, climate_regulatory_arbitrage_risk: 0.50,
    climate_finance_gap_severity: 0.52, just_transition_funding_deficit: 0.50,
    private_climate_finance_mobilization_gap: 0.50, sovereign_climate_default_risk: 0.75,
    insurance_climate_retreat_rate: 0.58, climate_finance_south_north_inequality: 0.55,
    physical_risk_underpricing_level: 0.70, green_bond_market_fragility: 0.55,
    climate_litigation_financial_risk: 0.60, carbon_border_adjustment_shock: 0.52,
    biodiversity_finance_gap: 0.55,
  });

  // CFE-008: critical + insurance_retreat_cascade
  // insurance=0.80>=0.70, south_north=0.72>=0.65 → insurance_retreat_cascade
  // stranded<0.70 OR fossil<0.65: stranded=0.65, fossil=0.60
  // green_wash<0.70 OR carbon<0.65: green_wash=0.65, carbon=0.62
  // gap<0.70 OR private<0.65: gap=0.65, private=0.62
  // sovereign<0.70 OR physical<0.65: sovereign=0.60, physical=0.58
  // stranded=(0.65*0.4+0.60*0.35+0.75*0.25)*100=65.75
  // integrity=(0.65*0.4+0.62*0.35+0.68*0.25)*100=64.70
  // gap=(0.65*0.4+0.68*0.35+0.62*0.25)*100=65.30
  // systemic=(0.60*0.4+0.80*0.35+0.72*0.25)*100=70.0
  // composite=65.75*0.30+64.70*0.25+65.30*0.25+70.0*0.20=19.725+16.175+16.325+14.0=66.22 → critical
  const e8 = analyzeEntity({
    entity_id: "CFE-008", finance_domain: "climate_insurance", region: "NOAM",
    stranded_asset_exposure_rate: 0.65, fossil_fuel_finance_lock_in: 0.60,
    transition_risk_repricing_speed: 0.75, green_washing_prevalence_index: 0.65,
    carbon_credit_integrity_risk: 0.62, climate_regulatory_arbitrage_risk: 0.68,
    climate_finance_gap_severity: 0.65, just_transition_funding_deficit: 0.68,
    private_climate_finance_mobilization_gap: 0.62, sovereign_climate_default_risk: 0.60,
    insurance_climate_retreat_rate: 0.80, climate_finance_south_north_inequality: 0.72,
    physical_risk_underpricing_level: 0.58, green_bond_market_fragility: 0.65,
    climate_litigation_financial_risk: 0.70, carbon_border_adjustment_shock: 0.65,
    biodiversity_finance_gap: 0.68,
  });

  return [e1, e2, e3, e4, e5, e6, e7, e8];
})();

// ─── Route handler ────────────────────────────────────────────────────────────

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (!SWARM_API_URL) {
    let entities = [...mockEntities];
    if (risk)    entities = entities.filter((e) => e.risk_level === risk);
    if (pattern) entities = entities.filter((e) => e.climate_finance_pattern === pattern);

    const risk_distribution:     Record<string, number> = {};
    const pattern_distribution:  Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution:   Record<string, number> = {};
    let total_comp     = 0;
    let total_stranded = 0;

    for (const e of mockEntities) {
      risk_distribution[e.risk_level]              = (risk_distribution[e.risk_level] || 0) + 1;
      pattern_distribution[e.climate_finance_pattern] = (pattern_distribution[e.climate_finance_pattern] || 0) + 1;
      severity_distribution[e.severity]            = (severity_distribution[e.severity] || 0) + 1;
      action_distribution[e.recommended_action]    = (action_distribution[e.recommended_action] || 0) + 1;
      total_comp     += e.composite_score;
      total_stranded += e.stranded_score;
    }

    const n = mockEntities.length;
    const avg_composite = Math.round((total_comp / n) * 100) / 100;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id:                              359,
        module_name:                            "Climate Finance & Green Transition Risk Intelligence Engine",
        total_entities:                         n,
        critical_count:                         mockEntities.filter((e) => e.risk_level === "critical").length,
        high_count:                             mockEntities.filter((e) => e.risk_level === "high").length,
        moderate_count:                         mockEntities.filter((e) => e.risk_level === "moderate").length,
        low_count:                              mockEntities.filter((e) => e.risk_level === "low").length,
        avg_composite,
        pattern_distribution,
        risk_distribution,
        severity_distribution,
        action_distribution,
        avg_estimated_climate_finance_index:    Math.round((avg_composite / 100 * 10) * 100) / 100,
      },
    } as Record<string, unknown>));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/climate-finance-engine`);
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(await res.json());
  } catch { /* fall through to 502 */ }

  return NextResponse.json(
    sealResponse({ entities: [], summary: {} } as Record<string, unknown>),
    { status: 502 },
  );
}
