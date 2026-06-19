import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ASSETS = [
  // AS-001 digital_twin EMEA — critical speculative_bubble
  { asset_id:"AS-001", asset_class:"digital_twin",          region:"EMEA",  scarcity_index:0.85, valuation_volatility:0.88, singularity_readiness_score:0.72, ai_creation_rate:0.78, network_effect_strength:0.60, token_liquidity_score:0.30, regulatory_uncertainty:0.75, post_rare_transition_score:0.65, value_store_resilience:0.20, market_manipulation_risk:0.80, consensus_legitimacy_score:0.15, speculative_premium_ratio:0.90, decentralization_score:0.22, sovereignty_alignment:0.30, quantum_security_level:0.25, adoption_velocity:0.82, paradigm_disruption_index:0.80 },
  // AS-002 synthetic_commodity NAMER — low stable
  { asset_id:"AS-002", asset_class:"synthetic_commodity",   region:"NAMER", scarcity_index:0.30, valuation_volatility:0.18, singularity_readiness_score:0.55, ai_creation_rate:0.22, network_effect_strength:0.80, token_liquidity_score:0.88, regulatory_uncertainty:0.15, post_rare_transition_score:0.70, value_store_resilience:0.85, market_manipulation_risk:0.12, consensus_legitimacy_score:0.90, speculative_premium_ratio:0.10, decentralization_score:0.78, sovereignty_alignment:0.85, quantum_security_level:0.80, adoption_velocity:0.45, paradigm_disruption_index:0.20 },
  // AS-003 attention_token APAC — high liquidity_crisis
  { asset_id:"AS-003", asset_class:"attention_token",       region:"APAC",  scarcity_index:0.55, valuation_volatility:0.62, singularity_readiness_score:0.48, ai_creation_rate:0.60, network_effect_strength:0.18, token_liquidity_score:0.20, regulatory_uncertainty:0.55, post_rare_transition_score:0.42, value_store_resilience:0.45, market_manipulation_risk:0.58, consensus_legitimacy_score:0.40, speculative_premium_ratio:0.55, decentralization_score:0.45, sovereignty_alignment:0.50, quantum_security_level:0.40, adoption_velocity:0.62, paradigm_disruption_index:0.55 },
  // AS-004 ai_generated_ip LATAM — low stable
  { asset_id:"AS-004", asset_class:"ai_generated_ip",       region:"LATAM", scarcity_index:0.20, valuation_volatility:0.15, singularity_readiness_score:0.65, ai_creation_rate:0.18, network_effect_strength:0.75, token_liquidity_score:0.82, regulatory_uncertainty:0.20, post_rare_transition_score:0.72, value_store_resilience:0.88, market_manipulation_risk:0.10, consensus_legitimacy_score:0.85, speculative_premium_ratio:0.08, decentralization_score:0.80, sovereignty_alignment:0.78, quantum_security_level:0.75, adoption_velocity:0.38, paradigm_disruption_index:0.18 },
  // AS-005 quantum_asset EMEA — critical regulatory_collapse
  { asset_id:"AS-005", asset_class:"quantum_asset",         region:"EMEA",  scarcity_index:0.78, valuation_volatility:0.80, singularity_readiness_score:0.85, ai_creation_rate:0.55, network_effect_strength:0.40, token_liquidity_score:0.35, regulatory_uncertainty:0.88, post_rare_transition_score:0.55, value_store_resilience:0.30, market_manipulation_risk:0.70, consensus_legitimacy_score:0.20, speculative_premium_ratio:0.72, decentralization_score:0.28, sovereignty_alignment:0.18, quantum_security_level:0.88, adoption_velocity:0.70, paradigm_disruption_index:0.72 },
  // AS-006 post_rare_material MEA — moderate speculative
  { asset_id:"AS-006", asset_class:"post_rare_material",    region:"MEA",   scarcity_index:0.50, valuation_volatility:0.45, singularity_readiness_score:0.38, ai_creation_rate:0.40, network_effect_strength:0.52, token_liquidity_score:0.55, regulatory_uncertainty:0.48, post_rare_transition_score:0.45, value_store_resilience:0.55, market_manipulation_risk:0.42, consensus_legitimacy_score:0.58, speculative_premium_ratio:0.40, decentralization_score:0.50, sovereignty_alignment:0.55, quantum_security_level:0.48, adoption_velocity:0.42, paradigm_disruption_index:0.38 },
  // AS-007 consciousness_token NAMER — high value_evaporation
  { asset_id:"AS-007", asset_class:"consciousness_token",   region:"NAMER", scarcity_index:0.70, valuation_volatility:0.72, singularity_readiness_score:0.60, ai_creation_rate:0.65, network_effect_strength:0.38, token_liquidity_score:0.40, regulatory_uncertainty:0.62, post_rare_transition_score:0.50, value_store_resilience:0.22, market_manipulation_risk:0.68, consensus_legitimacy_score:0.35, speculative_premium_ratio:0.65, decentralization_score:0.38, sovereignty_alignment:0.42, quantum_security_level:0.38, adoption_velocity:0.68, paradigm_disruption_index:0.62 },
  // AS-008 data_sovereignty APAC — low stable
  { asset_id:"AS-008", asset_class:"data_sovereignty",      region:"APAC",  scarcity_index:0.25, valuation_volatility:0.20, singularity_readiness_score:0.60, ai_creation_rate:0.25, network_effect_strength:0.72, token_liquidity_score:0.78, regulatory_uncertainty:0.18, post_rare_transition_score:0.68, value_store_resilience:0.82, market_manipulation_risk:0.15, consensus_legitimacy_score:0.88, speculative_premium_ratio:0.12, decentralization_score:0.75, sovereignty_alignment:0.90, quantum_security_level:0.70, adoption_velocity:0.40, paradigm_disruption_index:0.22 },
];

type Asset = typeof MOCK_ASSETS[0];

function valuationScore(i: Asset): number {
  let s = 0;
  if      (i.valuation_volatility >= 0.75) s += 40; else if (i.valuation_volatility >= 0.55) s += 22; else if (i.valuation_volatility >= 0.35) s += 8;
  if      (i.speculative_premium_ratio >= 0.70) s += 35; else if (i.speculative_premium_ratio >= 0.50) s += 18; else if (i.speculative_premium_ratio >= 0.30) s += 6;
  if      (i.scarcity_index >= 0.75) s += 25; else if (i.scarcity_index >= 0.50) s += 12;
  return Math.min(s, 100);
}
function marketScore(i: Asset): number {
  let s = 0;
  if      (i.market_manipulation_risk >= 0.70) s += 40; else if (i.market_manipulation_risk >= 0.50) s += 22; else if (i.market_manipulation_risk >= 0.30) s += 8;
  if      (i.regulatory_uncertainty >= 0.70) s += 35; else if (i.regulatory_uncertainty >= 0.50) s += 18; else if (i.regulatory_uncertainty >= 0.30) s += 6;
  if      (i.token_liquidity_score <= 0.25) s += 25; else if (i.token_liquidity_score <= 0.50) s += 12;
  return Math.min(s, 100);
}
function resilienceScore(i: Asset): number {
  let s = 0;
  if      (i.value_store_resilience <= 0.25) s += 40; else if (i.value_store_resilience <= 0.50) s += 22; else if (i.value_store_resilience <= 0.70) s += 8;
  if      (i.quantum_security_level <= 0.25) s += 35; else if (i.quantum_security_level <= 0.50) s += 18; else if (i.quantum_security_level <= 0.70) s += 6;
  if      (i.decentralization_score <= 0.25) s += 25; else if (i.decentralization_score <= 0.50) s += 12;
  return Math.min(s, 100);
}
function disruptionScore(i: Asset): number {
  let s = 0;
  if      (i.paradigm_disruption_index >= 0.75) s += 40; else if (i.paradigm_disruption_index >= 0.55) s += 22; else if (i.paradigm_disruption_index >= 0.35) s += 8;
  if      (i.ai_creation_rate >= 0.70) s += 35; else if (i.ai_creation_rate >= 0.50) s += 18; else if (i.ai_creation_rate >= 0.30) s += 6;
  if      (i.adoption_velocity >= 0.75) s += 25; else if (i.adoption_velocity >= 0.55) s += 12;
  return Math.min(s, 100);
}
function composite(val: number, mkt: number, res: number, dis: number): number {
  return Math.min(Math.round((val * 0.30 + mkt * 0.25 + res * 0.25 + dis * 0.20) * 100) / 100, 100);
}
function economyPattern(i: Asset): string {
  if (i.regulatory_uncertainty >= 0.70 && i.sovereignty_alignment < 0.30)          return "regulatory_collapse";
  if (i.speculative_premium_ratio >= 0.70 && i.consensus_legitimacy_score <= 0.35) return "speculative_bubble";
  if (i.token_liquidity_score <= 0.25 || i.network_effect_strength <= 0.20)        return "liquidity_crisis";
  if (i.value_store_resilience <= 0.25 && i.valuation_volatility >= 0.65)          return "value_evaporation";
  if (i.paradigm_disruption_index >= 0.75 && i.ai_creation_rate >= 0.65)           return "paradigm_displacement";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "bubble"; if (c >= 40) return "volatile"; if (c >= 20) return "speculative"; return "stable"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "speculative_bubble")  return "emergency_liquidation";
    if (p === "regulatory_collapse") return "regulatory_intervention";
    return "emergency_liquidation";
  }
  if (r === "high") {
    if (p === "liquidity_crisis")      return "portfolio_rebalancing";
    if (p === "value_evaporation")     return "risk_hedging";
    if (p === "paradigm_displacement") return "portfolio_rebalancing";
    return "risk_hedging";
  }
  if (r === "moderate") return "valuation_monitoring";
  return "no_action";
}
function signal(i: Asset, pat: string, comp: number): string {
  if (comp < 20) return "Actif post-rare stable — valorisation cohérente, marché liquide, résilience forte, singularité maîtrisée";
  const labels: Record<string,string> = {
    speculative_bubble:   "Bulle spéculative",
    regulatory_collapse:  "Effondrement réglementaire",
    liquidity_crisis:     "Crise de liquidité",
    value_evaporation:    "Évaporation de valeur",
    paradigm_displacement:"Déplacement paradigmatique",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — volatilité ${i.valuation_volatility.toFixed(2)} — manipulation ${i.market_manipulation_risk.toFixed(2)} — résilience ${i.value_store_resilience.toFixed(2)} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const assets = MOCK_ASSETS.map(i => {
      const val = valuationScore(i), mkt = marketScore(i), res = resilienceScore(i), dis = disruptionScore(i);
      const comp = composite(val, mkt, res, dis), pat = economyPattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      return {
        asset_id: i.asset_id, asset_class: i.asset_class, region: i.region,
        economy_risk: r, economy_pattern: pat, economy_severity: sev, recommended_action: act,
        valuation_score: val, market_score: mkt, resilience_score: res, disruption_score: dis,
        singularity_composite: comp,
        has_bubble_signal: comp >= 40 || i.speculative_premium_ratio >= 0.60 || i.market_manipulation_risk >= 0.65 || i.consensus_legitimacy_score <= 0.30,
        estimated_bubble_risk_index: Math.min(Math.round(comp/100*(1-i.consensus_legitimacy_score+0.01)*10*100)/100, 10.0),
        economy_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tval=0,tmkt=0,tres=0,tdis=0,tcomp=0,tbri=0,bubbleC=0,emergC=0;
    for (const a of assets) {
      rc[a.economy_risk]       = (rc[a.economy_risk]       || 0) + 1;
      pc[a.economy_pattern]    = (pc[a.economy_pattern]    || 0) + 1;
      sc[a.economy_severity]   = (sc[a.economy_severity]   || 0) + 1;
      ac[a.recommended_action] = (ac[a.recommended_action] || 0) + 1;
      tval += a.valuation_score; tmkt += a.market_score; tres += a.resilience_score; tdis += a.disruption_score;
      tcomp += a.singularity_composite; tbri += a.estimated_bubble_risk_index;
      if (a.has_bubble_signal) bubbleC++;
      if (a.recommended_action === "emergency_liquidation" || a.recommended_action === "regulatory_intervention") emergC++;
    }
    const n = assets.length;
    return NextResponse.json({ assets, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_singularity_composite: Math.round(tcomp/n*10)/10,
      bubble_alert_count: bubbleC,
      emergency_count: emergC,
      avg_valuation_score: Math.round(tval/n*10)/10,
      avg_market_score: Math.round(tmkt/n*10)/10,
      avg_resilience_score: Math.round(tres/n*10)/10,
      avg_disruption_score: Math.round(tdis/n*10)/10,
      avg_estimated_bubble_risk_index: Math.round(tbri/n*100)/100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/singularity-economy-engine`)).json());
}
