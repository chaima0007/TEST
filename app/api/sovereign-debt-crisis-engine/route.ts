import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  { entity_id:"SDC-001", region:"EMEA",  sovereign_type:"emerging_market",  debt_to_gdp_ratio:0.85, fiscal_deficit_trajectory:0.80, foreign_currency_exposure:0.70, rollover_risk_index:0.80, interest_burden_rate:0.72, credit_rating_deterioration:0.68, primary_balance_gap:0.75, capital_flight_velocity:0.70, contagion_spillover_risk:0.65, imf_program_dependency:0.60, currency_crisis_coupling:0.55, banking_sector_exposure:0.60, political_fiscal_risk:0.65, market_confidence_erosion:0.72, debt_monetization_risk:0.70, external_financing_gap:0.75, demographic_fiscal_pressure:0.55 },
  { entity_id:"SDC-002", region:"APAC",  sovereign_type:"advanced_economy",  debt_to_gdp_ratio:0.15, fiscal_deficit_trajectory:0.10, foreign_currency_exposure:0.12, rollover_risk_index:0.12, interest_burden_rate:0.10, credit_rating_deterioration:0.12, primary_balance_gap:0.12, capital_flight_velocity:0.08, contagion_spillover_risk:0.10, imf_program_dependency:0.05, currency_crisis_coupling:0.08, banking_sector_exposure:0.08, political_fiscal_risk:0.10, market_confidence_erosion:0.15, debt_monetization_risk:0.10, external_financing_gap:0.10, demographic_fiscal_pressure:0.12 },
  { entity_id:"SDC-003", region:"NOAM",  sovereign_type:"frontier_market",   debt_to_gdp_ratio:0.45, fiscal_deficit_trajectory:0.50, foreign_currency_exposure:0.48, rollover_risk_index:0.75, interest_burden_rate:0.52, credit_rating_deterioration:0.45, primary_balance_gap:0.40, capital_flight_velocity:0.55, contagion_spillover_risk:0.35, imf_program_dependency:0.42, currency_crisis_coupling:0.40, banking_sector_exposure:0.30, political_fiscal_risk:0.40, market_confidence_erosion:0.48, debt_monetization_risk:0.44, external_financing_gap:0.70, demographic_fiscal_pressure:0.35 },
  { entity_id:"SDC-004", region:"LATAM", sovereign_type:"emerging_market",   debt_to_gdp_ratio:0.18, fiscal_deficit_trajectory:0.15, foreign_currency_exposure:0.20, rollover_risk_index:0.14, interest_burden_rate:0.12, credit_rating_deterioration:0.15, primary_balance_gap:0.14, capital_flight_velocity:0.10, contagion_spillover_risk:0.15, imf_program_dependency:0.10, currency_crisis_coupling:0.12, banking_sector_exposure:0.12, political_fiscal_risk:0.12, market_confidence_erosion:0.20, debt_monetization_risk:0.14, external_financing_gap:0.12, demographic_fiscal_pressure:0.15 },
  { entity_id:"SDC-005", region:"MEA",   sovereign_type:"frontier_market",   debt_to_gdp_ratio:0.80, fiscal_deficit_trajectory:0.55, foreign_currency_exposure:0.70, rollover_risk_index:0.60, interest_burden_rate:0.72, credit_rating_deterioration:0.70, primary_balance_gap:0.72, capital_flight_velocity:0.72, contagion_spillover_risk:0.82, imf_program_dependency:0.65, currency_crisis_coupling:0.70, banking_sector_exposure:0.78, political_fiscal_risk:0.65, market_confidence_erosion:0.75, debt_monetization_risk:0.68, external_financing_gap:0.65, demographic_fiscal_pressure:0.60 },
  { entity_id:"SDC-006", region:"EMEA",  sovereign_type:"advanced_economy",  debt_to_gdp_ratio:0.30, fiscal_deficit_trajectory:0.28, foreign_currency_exposure:0.25, rollover_risk_index:0.28, interest_burden_rate:0.26, credit_rating_deterioration:0.30, primary_balance_gap:0.25, capital_flight_velocity:0.25, contagion_spillover_risk:0.32, imf_program_dependency:0.20, currency_crisis_coupling:0.30, banking_sector_exposure:0.28, political_fiscal_risk:0.28, market_confidence_erosion:0.35, debt_monetization_risk:0.28, external_financing_gap:0.30, demographic_fiscal_pressure:0.30 },
  { entity_id:"SDC-007", region:"APAC",  sovereign_type:"emerging_market",   debt_to_gdp_ratio:0.52, fiscal_deficit_trajectory:0.48, foreign_currency_exposure:0.45, rollover_risk_index:0.42, interest_burden_rate:0.48, credit_rating_deterioration:0.68, primary_balance_gap:0.45, capital_flight_velocity:0.40, contagion_spillover_risk:0.38, imf_program_dependency:0.40, currency_crisis_coupling:0.35, banking_sector_exposure:0.42, political_fiscal_risk:0.60, market_confidence_erosion:0.75, debt_monetization_risk:0.45, external_financing_gap:0.45, demographic_fiscal_pressure:0.42 },
  { entity_id:"SDC-008", region:"LATAM", sovereign_type:"frontier_market",   debt_to_gdp_ratio:0.75, fiscal_deficit_trajectory:0.55, foreign_currency_exposure:0.78, rollover_risk_index:0.60, interest_burden_rate:0.68, credit_rating_deterioration:0.68, primary_balance_gap:0.70, capital_flight_velocity:0.65, contagion_spillover_risk:0.55, imf_program_dependency:0.70, currency_crisis_coupling:0.75, banking_sector_exposure:0.62, political_fiscal_risk:0.65, market_confidence_erosion:0.62, debt_monetization_risk:0.72, external_financing_gap:0.68, demographic_fiscal_pressure:0.65 },
];

type Entity = typeof MOCK_ENTITIES[0];

function solvencyScore(i: Entity): number {
  return (i.debt_to_gdp_ratio * 0.4 + i.fiscal_deficit_trajectory * 0.35 + i.primary_balance_gap * 0.25) * 100;
}
function liquidityScore(i: Entity): number {
  return (i.rollover_risk_index * 0.4 + i.external_financing_gap * 0.35 + i.capital_flight_velocity * 0.25) * 100;
}
function contagionScore(i: Entity): number {
  return (i.contagion_spillover_risk * 0.4 + i.banking_sector_exposure * 0.35 + i.currency_crisis_coupling * 0.25) * 100;
}
function confidenceScore(i: Entity): number {
  return (i.market_confidence_erosion * 0.4 + i.credit_rating_deterioration * 0.35 + i.political_fiscal_risk * 0.25) * 100;
}
function compositeScore(sol: number, liq: number, con: number, conf: number): number {
  return Math.round((sol * 0.30 + liq * 0.25 + con * 0.25 + conf * 0.20) * 100) / 100;
}
function debtRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}
function debtPattern(i: Entity): string {
  if (i.debt_to_gdp_ratio >= 0.70 && i.fiscal_deficit_trajectory >= 0.65) return "debt_spiral";
  if (i.rollover_risk_index >= 0.70 && i.external_financing_gap >= 0.65) return "liquidity_trap";
  if (i.contagion_spillover_risk >= 0.70 && i.banking_sector_exposure >= 0.65) return "contagion_cascade";
  if (i.market_confidence_erosion >= 0.70 && i.credit_rating_deterioration >= 0.65) return "confidence_collapse";
  if (i.currency_crisis_coupling >= 0.70 && i.foreign_currency_exposure >= 0.65) return "currency_debt_spiral";
  return "none";
}
function debtSeverity(comp: number): string {
  if (comp >= 75) return "fiscal_emergency";
  if (comp >= 50) return "high_fiscal_stress";
  if (comp >= 25) return "fiscal_tension";
  return "fiscal_stable";
}
function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "sovereign_debt_restructuring";
  if (risk === "high" && pattern === "contagion_cascade") return "contagion_firewall";
  if (risk === "high") return "fiscal_consolidation_program";
  if (risk === "moderate") return "fiscal_monitoring";
  return "no_action";
}
function debtSignal(i: Entity, pattern: string, comp: number): string {
  if (comp < 20) return "Stabilité fiscale souveraine — les indicateurs de solvabilité, liquidité, contagion et confiance restent dans les seuils de référence";
  const labels: Record<string, string> = {
    debt_spiral: "Spirale de la dette",
    liquidity_trap: "Trappe de liquidité",
    contagion_cascade: "Cascade de contagion",
    confidence_collapse: "Effondrement de la confiance",
    currency_debt_spiral: "Spirale dette-devises",
  };
  const label = labels[pattern] ?? pattern.replace(/_/g, " ");
  return `${label} — ratio dette/PIB ${Math.round(i.debt_to_gdp_ratio * 100)}% — déficit fiscal ${Math.round(i.fiscal_deficit_trajectory * 100)}% — risque de contagion ${Math.round(i.contagion_spillover_risk * 100)}% — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(i => {
      const sol = Math.round(solvencyScore(i) * 100) / 100;
      const liq = Math.round(liquidityScore(i) * 100) / 100;
      const con = Math.round(contagionScore(i) * 100) / 100;
      const conf = Math.round(confidenceScore(i) * 100) / 100;
      const comp = compositeScore(sol, liq, con, conf);
      const risk = debtRisk(comp);
      const pattern = debtPattern(i);
      const severity = debtSeverity(comp);
      const action = recommendedAction(risk, pattern);
      return {
        entity_id: i.entity_id,
        region: i.region,
        sovereign_type: i.sovereign_type,
        debt_risk: risk,
        debt_pattern: pattern,
        debt_severity: severity,
        recommended_action: action,
        solvency_score: sol,
        liquidity_score: liq,
        contagion_score: con,
        confidence_score: conf,
        debt_composite: comp,
        is_debt_crisis: comp >= 60,
        requires_debt_intervention: comp >= 40,
        debt_signal: debtSignal(i, pattern, comp),
      };
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tSol=0, tLiq=0, tCon=0, tConf=0, tComp=0, crisisCount=0, interventionCount=0;
    for (const e of entities) {
      rc[e.debt_risk]=(rc[e.debt_risk]||0)+1;
      pc[e.debt_pattern]=(pc[e.debt_pattern]||0)+1;
      sc[e.debt_severity]=(sc[e.debt_severity]||0)+1;
      ac[e.recommended_action]=(ac[e.recommended_action]||0)+1;
      tSol+=e.solvency_score; tLiq+=e.liquidity_score;
      tCon+=e.contagion_score; tConf+=e.confidence_score;
      tComp+=e.debt_composite;
      if (e.is_debt_crisis) crisisCount++;
      if (e.requires_debt_intervention) interventionCount++;
    }
    const n = entities.length;
    const avgComp = tComp / n;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        total: n,
        risk_counts: rc,
        pattern_counts: pc,
        severity_counts: sc,
        action_counts: ac,
        avg_solvency_score: Math.round(tSol/n*100)/100,
        avg_liquidity_score: Math.round(tLiq/n*100)/100,
        avg_contagion_score: Math.round(tCon/n*100)/100,
        avg_confidence_score: Math.round(tConf/n*100)/100,
        avg_debt_composite: Math.round(avgComp*100)/100,
        debt_crisis_count: crisisCount,
        debt_intervention_count: interventionCount,
        avg_estimated_fiscal_stress_index: Math.round(avgComp/100*10*100)/100,
      },
    } as Record<string,unknown>));
  }
  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/sovereign-debt-crisis-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json() as Record<string,unknown>));
  } catch {
    return NextResponse.json(sealResponse({ error: "Upstream unavailable" } as Record<string,unknown>), { status: 502 });
  }
}
