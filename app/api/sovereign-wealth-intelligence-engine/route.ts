import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // SWI-001 — EMEA, sovereign_stabilization → critical, capital_misallocation
  {
    id: "SWI-001", fund_type: "sovereign_stabilization", region: "EMEA",
    mandate_alignment: 0.30, diversification_quality: 0.22, liquidity_buffer: 0.40,
    geopolitical_exposure: 0.62, currency_concentration: 0.72, return_on_mandate: 0.35,
    esg_compliance: 0.42, governance_maturity: 0.48, political_interference_risk: 0.58,
    rebalancing_agility: 0.32, alternative_asset_integration: 0.28,
    sovereign_debt_exposure: 0.55, concentration_risk: 0.78, duration_mismatch: 0.60,
    transparency_index: 0.38, intergenerational_equity: 0.35, shock_absorption_capacity: 0.38,
  },
  // SWI-002 — APAC, pension_sovereign → low, optimal_allocation/none
  {
    id: "SWI-002", fund_type: "pension_sovereign", region: "APAC",
    mandate_alignment: 0.92, diversification_quality: 0.90, liquidity_buffer: 0.88,
    geopolitical_exposure: 0.12, currency_concentration: 0.10, return_on_mandate: 0.90,
    esg_compliance: 0.88, governance_maturity: 0.92, political_interference_risk: 0.08,
    rebalancing_agility: 0.90, alternative_asset_integration: 0.85,
    sovereign_debt_exposure: 0.15, concentration_risk: 0.10, duration_mismatch: 0.10,
    transparency_index: 0.92, intergenerational_equity: 0.90, shock_absorption_capacity: 0.90,
  },
  // SWI-003 — NOAM, future_generations → high, political_capture
  {
    id: "SWI-003", fund_type: "future_generations", region: "NOAM",
    mandate_alignment: 0.52, diversification_quality: 0.58, liquidity_buffer: 0.55,
    geopolitical_exposure: 0.45, currency_concentration: 0.38, return_on_mandate: 0.50,
    esg_compliance: 0.60, governance_maturity: 0.30, political_interference_risk: 0.72,
    rebalancing_agility: 0.42, alternative_asset_integration: 0.40,
    sovereign_debt_exposure: 0.38, concentration_risk: 0.42, duration_mismatch: 0.45,
    transparency_index: 0.35, intergenerational_equity: 0.50, shock_absorption_capacity: 0.52,
  },
  // SWI-004 — LATAM, pension_sovereign → low, optimal_allocation/none
  {
    id: "SWI-004", fund_type: "pension_sovereign", region: "LATAM",
    mandate_alignment: 0.85, diversification_quality: 0.82, liquidity_buffer: 0.80,
    geopolitical_exposure: 0.18, currency_concentration: 0.15, return_on_mandate: 0.82,
    esg_compliance: 0.78, governance_maturity: 0.80, political_interference_risk: 0.12,
    rebalancing_agility: 0.80, alternative_asset_integration: 0.75,
    sovereign_debt_exposure: 0.20, concentration_risk: 0.15, duration_mismatch: 0.15,
    transparency_index: 0.82, intergenerational_equity: 0.82, shock_absorption_capacity: 0.82,
  },
  // SWI-005 — MEA, oil_stabilization → critical, liquidity_trap
  {
    id: "SWI-005", fund_type: "oil_stabilization", region: "MEA",
    mandate_alignment: 0.40, diversification_quality: 0.45, liquidity_buffer: 0.18,
    geopolitical_exposure: 0.65, currency_concentration: 0.60, return_on_mandate: 0.42,
    esg_compliance: 0.30, governance_maturity: 0.50, political_interference_risk: 0.55,
    rebalancing_agility: 0.28, alternative_asset_integration: 0.32,
    sovereign_debt_exposure: 0.58, concentration_risk: 0.55, duration_mismatch: 0.65,
    transparency_index: 0.42, intergenerational_equity: 0.38, shock_absorption_capacity: 0.22,
  },
  // SWI-006 — EMEA, development_fund → moderate, none
  {
    id: "SWI-006", fund_type: "development_fund", region: "EMEA",
    mandate_alignment: 0.62, diversification_quality: 0.60, liquidity_buffer: 0.62,
    geopolitical_exposure: 0.38, currency_concentration: 0.40, return_on_mandate: 0.58,
    esg_compliance: 0.65, governance_maturity: 0.62, political_interference_risk: 0.38,
    rebalancing_agility: 0.55, alternative_asset_integration: 0.50,
    sovereign_debt_exposure: 0.40, concentration_risk: 0.38, duration_mismatch: 0.40,
    transparency_index: 0.60, intergenerational_equity: 0.58, shock_absorption_capacity: 0.60,
  },
  // SWI-007 — APAC, future_generations → high, mandate_drift
  {
    id: "SWI-007", fund_type: "future_generations", region: "APAC",
    mandate_alignment: 0.22, diversification_quality: 0.55, liquidity_buffer: 0.58,
    geopolitical_exposure: 0.40, currency_concentration: 0.35, return_on_mandate: 0.28,
    esg_compliance: 0.52, governance_maturity: 0.60, political_interference_risk: 0.40,
    rebalancing_agility: 0.48, alternative_asset_integration: 0.45,
    sovereign_debt_exposure: 0.35, concentration_risk: 0.40, duration_mismatch: 0.42,
    transparency_index: 0.58, intergenerational_equity: 0.30, shock_absorption_capacity: 0.55,
  },
  // SWI-008 — NOAM, sovereign_stabilization → critical, geopolitical_overexposure
  {
    id: "SWI-008", fund_type: "sovereign_stabilization", region: "NOAM",
    mandate_alignment: 0.38, diversification_quality: 0.40, liquidity_buffer: 0.42,
    geopolitical_exposure: 0.82, currency_concentration: 0.65, return_on_mandate: 0.40,
    esg_compliance: 0.35, governance_maturity: 0.45, political_interference_risk: 0.60,
    rebalancing_agility: 0.30, alternative_asset_integration: 0.28,
    sovereign_debt_exposure: 0.72, concentration_risk: 0.58, duration_mismatch: 0.62,
    transparency_index: 0.40, intergenerational_equity: 0.35, shock_absorption_capacity: 0.38,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function allocationScore(e: Entity): number {
  const raw = (
    e.concentration_risk * 0.4
    + e.currency_concentration * 0.3
    + (1 - e.diversification_quality) * 0.3
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function governanceScore(e: Entity): number {
  const raw = (
    e.political_interference_risk * 0.4
    + (1 - e.governance_maturity) * 0.35
    + (1 - e.transparency_index) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function resilienceScore(e: Entity): number {
  const raw = (
    (1 - e.shock_absorption_capacity) * 0.4
    + (1 - e.liquidity_buffer) * 0.35
    + e.duration_mismatch * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function mandateScore(e: Entity): number {
  const raw = (
    (1 - e.mandate_alignment) * 0.4
    + (1 - e.return_on_mandate) * 0.35
    + (1 - e.intergenerational_equity) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function composite(alloc: number, gov: number, res: number, mand: number): number {
  return Math.round((alloc * 0.30 + gov * 0.25 + res * 0.25 + mand * 0.20) * 100) / 100;
}

function swPattern(e: Entity): string {
  if (e.concentration_risk >= 0.65 && (1 - e.diversification_quality) >= 0.55) return "capital_misallocation";
  if (e.political_interference_risk >= 0.65 && (1 - e.governance_maturity) >= 0.55) return "political_capture";
  if ((1 - e.liquidity_buffer) >= 0.65 && (1 - e.shock_absorption_capacity) >= 0.55) return "liquidity_trap";
  if ((1 - e.mandate_alignment) >= 0.65 && (1 - e.return_on_mandate) >= 0.55) return "mandate_drift";
  if (e.geopolitical_exposure >= 0.70 && e.sovereign_debt_exposure >= 0.60) return "geopolitical_overexposure";
  return "none";
}

function swRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function swSeverity(comp: number): string {
  if (comp >= 75) return "sovereign_crisis";
  if (comp >= 50) return "high_dysfunction";
  if (comp >= 25) return "capital_stress";
  return "optimal_allocation";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "sovereign_emergency_rebalancing";
  if (risk === "high" && pattern === "political_capture") return "governance_intervention";
  if (risk === "high") return "capital_reallocation";
  if (risk === "moderate") return "sw_monitoring";
  return "no_action";
}

function swSignal(e: Entity, risk: string, comp: number): string {
  const compInt = Math.round(comp);
  if (risk === "critical") {
    return `Critique — concentration risque ${Math.round(e.concentration_risk * 100)}% — interférence politique ${Math.round(e.political_interference_risk * 100)}% — composite ${compInt}`;
  }
  if (risk === "high") {
    return `Élevé — alignement mandat ${Math.round(e.mandate_alignment * 100)}% — buffer liquidité ${Math.round(e.liquidity_buffer * 100)}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `Modéré — qualité diversification ${Math.round(e.diversification_quality * 100)}% — composite ${compInt}`;
  }
  return "Fonds souverain optimal — allocation équilibrée, mandat respecté, gouvernance solide";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[sovereign-wealth-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number> = {}, pc: Record<string,number> = {},
          sc: Record<string,number> = {}, ac: Record<string,number> = {};
    let tComp = 0, tAlloc = 0, tGov = 0, tRes = 0, tMand = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.sw_risk]            = (rc[ent.sw_risk]            || 0) + 1;
      pc[ent.sw_pattern]         = (pc[ent.sw_pattern]         || 0) + 1;
      sc[ent.sw_severity]        = (sc[ent.sw_severity]        || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tComp  += ent.sw_composite;
      tAlloc += ent.allocation_score;
      tGov   += ent.governance_score;
      tRes   += ent.resilience_score;
      tMand  += ent.mandate_score;
      if (ent.is_in_sw_crisis)          crisisCount++;
      if (ent.requires_sw_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComp = tComp / n;
    const summary = {
      total:                           n,
      risk_counts:                     rc,
      pattern_counts:                  pc,
      severity_counts:                 sc,
      action_counts:                   ac,
      avg_sw_composite:                Math.round(avgComp * 10) / 10,
      sw_crisis_count:                 crisisCount,
      sw_intervention_count:           interventionCount,
      avg_allocation_score:            Math.round(tAlloc / n * 10) / 10,
      avg_governance_score:            Math.round(tGov   / n * 10) / 10,
      avg_resilience_score:            Math.round(tRes   / n * 10) / 10,
      avg_mandate_score:               Math.round(tMand  / n * 10) / 10,
      avg_estimated_capital_risk_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "sovereign-wealth-intelligence-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/sovereign-wealth-intelligence-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return sealResponse(NextResponse.json(sealResponse(data, "sovereign-wealth-intelligence-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream swarm unavailable" }, "sovereign-wealth-intelligence-engine"),
      { status: 502 }
    ));
  }
}
