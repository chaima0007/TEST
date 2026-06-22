import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // AFE-001 — critical, liquidity_vacuum
  { id: "AFE-001", ecosystem_type: "defi_protocol", region: "EMEA",
    autonomous_liquidity_depth: 0.10, algorithmic_governance_maturity: 0.20, self_regulation_effectiveness: 0.15,
    market_maker_concentration: 0.75, flash_crash_susceptibility: 0.70, liquidity_fragmentation: 0.80,
    order_flow_toxicity: 0.65, price_discovery_efficiency: 0.25, systemic_correlation: 0.72,
    circuit_breaker_effectiveness: 0.18, dark_pool_opacity: 0.70, hft_dominance: 0.55,
    regulatory_arbitrage_exposure: 0.68, cross_market_contagion: 0.65, autonomous_agent_conflict_rate: 0.75,
    market_microstructure_stress: 0.62, information_latency_risk: 0.70 },
  // AFE-002 — low, none
  { id: "AFE-002", ecosystem_type: "traditional_exchange", region: "APAC",
    autonomous_liquidity_depth: 0.88, algorithmic_governance_maturity: 0.85, self_regulation_effectiveness: 0.90,
    market_maker_concentration: 0.12, flash_crash_susceptibility: 0.10, liquidity_fragmentation: 0.12,
    order_flow_toxicity: 0.10, price_discovery_efficiency: 0.90, systemic_correlation: 0.15,
    circuit_breaker_effectiveness: 0.92, dark_pool_opacity: 0.12, hft_dominance: 0.15,
    regulatory_arbitrage_exposure: 0.10, cross_market_contagion: 0.12, autonomous_agent_conflict_rate: 0.10,
    market_microstructure_stress: 0.12, information_latency_risk: 0.10 },
  // AFE-003 — high, flash_crash_cascade
  { id: "AFE-003", ecosystem_type: "algo_market", region: "NOAM",
    autonomous_liquidity_depth: 0.42, algorithmic_governance_maturity: 0.38, self_regulation_effectiveness: 0.40,
    market_maker_concentration: 0.55, flash_crash_susceptibility: 0.72, liquidity_fragmentation: 0.50,
    order_flow_toxicity: 0.58, price_discovery_efficiency: 0.45, systemic_correlation: 0.55,
    circuit_breaker_effectiveness: 0.40, dark_pool_opacity: 0.50, hft_dominance: 0.60,
    regulatory_arbitrage_exposure: 0.45, cross_market_contagion: 0.50, autonomous_agent_conflict_rate: 0.55,
    market_microstructure_stress: 0.65, information_latency_risk: 0.55 },
  // AFE-004 — low, none
  { id: "AFE-004", ecosystem_type: "traditional_exchange", region: "LATAM",
    autonomous_liquidity_depth: 0.82, algorithmic_governance_maturity: 0.78, self_regulation_effectiveness: 0.85,
    market_maker_concentration: 0.18, flash_crash_susceptibility: 0.15, liquidity_fragmentation: 0.18,
    order_flow_toxicity: 0.15, price_discovery_efficiency: 0.85, systemic_correlation: 0.20,
    circuit_breaker_effectiveness: 0.88, dark_pool_opacity: 0.15, hft_dominance: 0.20,
    regulatory_arbitrage_exposure: 0.15, cross_market_contagion: 0.18, autonomous_agent_conflict_rate: 0.15,
    market_microstructure_stress: 0.18, information_latency_risk: 0.15 },
  // AFE-005 — critical, governance_failure
  { id: "AFE-005", ecosystem_type: "defi_protocol", region: "MEA",
    autonomous_liquidity_depth: 0.25, algorithmic_governance_maturity: 0.12, self_regulation_effectiveness: 0.10,
    market_maker_concentration: 0.65, flash_crash_susceptibility: 0.58, liquidity_fragmentation: 0.55,
    order_flow_toxicity: 0.62, price_discovery_efficiency: 0.20, systemic_correlation: 0.68,
    circuit_breaker_effectiveness: 0.15, dark_pool_opacity: 0.72, hft_dominance: 0.55,
    regulatory_arbitrage_exposure: 0.78, cross_market_contagion: 0.55, autonomous_agent_conflict_rate: 0.70,
    market_microstructure_stress: 0.60, information_latency_risk: 0.72 },
  // AFE-006 — moderate, none
  { id: "AFE-006", ecosystem_type: "dark_pool", region: "EMEA",
    autonomous_liquidity_depth: 0.62, algorithmic_governance_maturity: 0.60, self_regulation_effectiveness: 0.62,
    market_maker_concentration: 0.30, flash_crash_susceptibility: 0.28, liquidity_fragmentation: 0.30,
    order_flow_toxicity: 0.30, price_discovery_efficiency: 0.60, systemic_correlation: 0.32,
    circuit_breaker_effectiveness: 0.65, dark_pool_opacity: 0.58, hft_dominance: 0.35,
    regulatory_arbitrage_exposure: 0.28, cross_market_contagion: 0.30, autonomous_agent_conflict_rate: 0.32,
    market_microstructure_stress: 0.28, information_latency_risk: 0.32 },
  // AFE-007 — high, contagion_spiral
  { id: "AFE-007", ecosystem_type: "algo_market", region: "APAC",
    autonomous_liquidity_depth: 0.40, algorithmic_governance_maturity: 0.42, self_regulation_effectiveness: 0.45,
    market_maker_concentration: 0.52, flash_crash_susceptibility: 0.50, liquidity_fragmentation: 0.45,
    order_flow_toxicity: 0.48, price_discovery_efficiency: 0.42, systemic_correlation: 0.75,
    circuit_breaker_effectiveness: 0.38, dark_pool_opacity: 0.48, hft_dominance: 0.52,
    regulatory_arbitrage_exposure: 0.42, cross_market_contagion: 0.68, autonomous_agent_conflict_rate: 0.55,
    market_microstructure_stress: 0.48, information_latency_risk: 0.52 },
  // AFE-008 — critical, hft_predation
  { id: "AFE-008", ecosystem_type: "hft_venue", region: "NOAM",
    autonomous_liquidity_depth: 0.22, algorithmic_governance_maturity: 0.25, self_regulation_effectiveness: 0.40,
    market_maker_concentration: 0.72, flash_crash_susceptibility: 0.60, liquidity_fragmentation: 0.55,
    order_flow_toxicity: 0.85, price_discovery_efficiency: 0.22, systemic_correlation: 0.62,
    circuit_breaker_effectiveness: 0.22, dark_pool_opacity: 0.60, hft_dominance: 0.90,
    regulatory_arbitrage_exposure: 0.50, cross_market_contagion: 0.55, autonomous_agent_conflict_rate: 0.75,
    market_microstructure_stress: 0.70, information_latency_risk: 0.78 },
];

type Entity = typeof MOCK_ENTITIES[0];

function liquidityScore(e: Entity): number {
  const raw = (
    e.liquidity_fragmentation * 0.4
    + (1 - e.autonomous_liquidity_depth) * 0.3
    + e.market_maker_concentration * 0.3
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function governanceScore(e: Entity): number {
  const raw = (
    (1 - e.self_regulation_effectiveness) * 0.4
    + (1 - e.algorithmic_governance_maturity) * 0.35
    + e.regulatory_arbitrage_exposure * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function microstructureScore(e: Entity): number {
  const raw = (
    e.flash_crash_susceptibility * 0.35
    + e.order_flow_toxicity * 0.35
    + e.market_microstructure_stress * 0.30
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function contagionScore(e: Entity): number {
  const raw = (
    e.systemic_correlation * 0.4
    + e.cross_market_contagion * 0.35
    + (1 - e.circuit_breaker_effectiveness) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function ecosystemComposite(liq: number, gov: number, micro: number, cont: number): number {
  return Math.round((liq * 0.30 + gov * 0.25 + micro * 0.25 + cont * 0.20) * 100) / 100;
}

function ecosystemRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function ecosystemPattern(e: Entity): string {
  if (e.liquidity_fragmentation >= 0.65 && (1 - e.autonomous_liquidity_depth) >= 0.55) return "liquidity_vacuum";
  if (e.flash_crash_susceptibility >= 0.65 && e.market_microstructure_stress >= 0.55) return "flash_crash_cascade";
  if ((1 - e.self_regulation_effectiveness) >= 0.65 && e.regulatory_arbitrage_exposure >= 0.55) return "governance_failure";
  if (e.systemic_correlation >= 0.70 && e.cross_market_contagion >= 0.60) return "contagion_spiral";
  if (e.hft_dominance >= 0.70 && e.order_flow_toxicity >= 0.60) return "hft_predation";
  return "none";
}

function ecosystemSeverity(comp: number): string {
  if (comp >= 75) return "systemic_collapse";
  if (comp >= 50) return "high_dysfunction";
  if (comp >= 25) return "market_stress";
  return "autonomous_equilibrium";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "market_circuit_breaker_emergency";
  if (risk === "high") {
    if (pattern === "contagion_spiral") return "contagion_quarantine";
    return "ecosystem_stabilization";
  }
  if (risk === "moderate") return "market_monitoring";
  return "no_action";
}

function ecosystemSignal(e: Entity, risk: string, comp: number, gov: number): string {
  if (risk === "critical") {
    return `Critique — fragmentation liquidité ${Math.floor(e.liquidity_fragmentation * 100)}% — corrélation systémique ${Math.floor(e.systemic_correlation * 100)}% — composite ${Math.floor(comp)}`;
  }
  if (risk === "high") {
    return `Élevé — flash crash susceptibilité ${Math.floor(e.flash_crash_susceptibility * 100)}% — gouvernance ${100 - Math.floor(gov)}% — composite ${Math.floor(comp)}`;
  }
  if (risk === "moderate") {
    return `Modéré — toxicité flux ordres ${Math.floor(e.order_flow_toxicity * 100)}% — composite ${Math.floor(comp)}`;
  }
  return "Écosystème financier autonome stable — liquidité équilibrée, gouvernance algorithmique efficace";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[autonomous-financial-ecosystem-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number> = {}, pc: Record<string,number> = {},
          sc: Record<string,number> = {}, ac: Record<string,number> = {};
    let tComp = 0, tLiq = 0, tGov = 0, tMicro = 0, tCont = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.ecosystem_risk]      = (rc[ent.ecosystem_risk]      || 0) + 1;
      pc[ent.ecosystem_pattern]   = (pc[ent.ecosystem_pattern]   || 0) + 1;
      sc[ent.ecosystem_severity]  = (sc[ent.ecosystem_severity]  || 0) + 1;
      ac[ent.recommended_action]  = (ac[ent.recommended_action]  || 0) + 1;
      tComp  += ent.ecosystem_composite;
      tLiq   += ent.liquidity_score;
      tGov   += ent.governance_score;
      tMicro += ent.microstructure_score;
      tCont  += ent.contagion_score;
      if (ent.is_in_ecosystem_crisis)          crisisCount++;
      if (ent.requires_ecosystem_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 10) / 10;
    const summary = {
      total:                                n,
      risk_counts:                          rc,
      pattern_counts:                       pc,
      severity_counts:                      sc,
      action_counts:                        ac,
      avg_ecosystem_composite:              avgComp,
      ecosystem_crisis_count:               crisisCount,
      ecosystem_intervention_count:         interventionCount,
      avg_liquidity_score:                  Math.round(tLiq   / n * 10) / 10,
      avg_governance_score:                 Math.round(tGov   / n * 10) / 10,
      avg_microstructure_score:             Math.round(tMicro / n * 10) / 10,
      avg_contagion_score:                  Math.round(tCont  / n * 10) / 10,
      avg_estimated_ecosystem_stress_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "autonomous-financial-ecosystem-engine")));
  }

  return sealResponse(NextResponse.json(sealResponse(
    await (await fetch(`${process.env.SWARM_API_URL}/autonomous-financial-ecosystem-engine`, { next: { revalidate: 30 } })).json(),
    "autonomous-financial-ecosystem-engine"
  )));
}
