import { NextResponse } from "next/server";

const MOCK_ASSETS = [
  // FO-001 real_estate_token EMEA — critical liquidity_freeze
  { asset_id:"FO-001", asset_category:"real_estate_token",   region:"EMEA",  liquidity_fragmentation_risk:0.88, ownership_concentration_index:0.55, governance_token_participation:0.22, revenue_distribution_efficiency:0.40, smart_contract_audit_score:0.45, fractional_valuation_accuracy:0.42, secondary_market_depth:0.12, holder_churn_rate:0.50, regulatory_tokenization_clarity:0.48, custody_risk_score:0.40, cross_border_transfer_friction:0.45, dividend_payment_reliability:0.38, oracle_price_accuracy:0.50, community_governance_health:0.35, exit_mechanism_robustness:0.30, fractional_liquidity_pool_depth:0.10, token_utility_score:0.35 },
  // FO-002 art_nft NAMER — low liquid
  { asset_id:"FO-002", asset_category:"art_nft",             region:"NAMER", liquidity_fragmentation_risk:0.10, ownership_concentration_index:0.12, governance_token_participation:0.88, revenue_distribution_efficiency:0.92, smart_contract_audit_score:0.95, fractional_valuation_accuracy:0.90, secondary_market_depth:0.92, holder_churn_rate:0.08, regulatory_tokenization_clarity:0.90, custody_risk_score:0.05, cross_border_transfer_friction:0.08, dividend_payment_reliability:0.95, oracle_price_accuracy:0.92, community_governance_health:0.90, exit_mechanism_robustness:0.92, fractional_liquidity_pool_depth:0.90, token_utility_score:0.90 },
  // FO-003 infrastructure_share APAC — high governance_capture
  { asset_id:"FO-003", asset_category:"infrastructure_share",region:"APAC",  liquidity_fragmentation_risk:0.45, ownership_concentration_index:0.78, governance_token_participation:0.18, revenue_distribution_efficiency:0.55, smart_contract_audit_score:0.62, fractional_valuation_accuracy:0.58, secondary_market_depth:0.45, holder_churn_rate:0.42, regulatory_tokenization_clarity:0.55, custody_risk_score:0.35, cross_border_transfer_friction:0.40, dividend_payment_reliability:0.50, oracle_price_accuracy:0.60, community_governance_health:0.22, exit_mechanism_robustness:0.48, fractional_liquidity_pool_depth:0.42, token_utility_score:0.50 },
  // FO-004 patent_royalty LATAM — low maturing
  { asset_id:"FO-004", asset_category:"patent_royalty",      region:"LATAM", liquidity_fragmentation_risk:0.22, ownership_concentration_index:0.20, governance_token_participation:0.75, revenue_distribution_efficiency:0.80, smart_contract_audit_score:0.82, fractional_valuation_accuracy:0.78, secondary_market_depth:0.72, holder_churn_rate:0.18, regulatory_tokenization_clarity:0.78, custody_risk_score:0.15, cross_border_transfer_friction:0.20, dividend_payment_reliability:0.85, oracle_price_accuracy:0.80, community_governance_health:0.75, exit_mechanism_robustness:0.80, fractional_liquidity_pool_depth:0.70, token_utility_score:0.75 },
  // FO-005 sports_contract MEA — critical oracle_manipulation
  { asset_id:"FO-005", asset_category:"sports_contract",     region:"MEA",   liquidity_fragmentation_risk:0.60, ownership_concentration_index:0.52, governance_token_participation:0.40, revenue_distribution_efficiency:0.28, smart_contract_audit_score:0.25, fractional_valuation_accuracy:0.18, secondary_market_depth:0.30, holder_churn_rate:0.55, regulatory_tokenization_clarity:0.45, custody_risk_score:0.65, cross_border_transfer_friction:0.50, dividend_payment_reliability:0.22, oracle_price_accuracy:0.12, community_governance_health:0.38, exit_mechanism_robustness:0.28, fractional_liquidity_pool_depth:0.25, token_utility_score:0.30 },
  // FO-006 music_rights NAMER — moderate none
  { asset_id:"FO-006", asset_category:"music_rights",        region:"NAMER", liquidity_fragmentation_risk:0.42, ownership_concentration_index:0.38, governance_token_participation:0.55, revenue_distribution_efficiency:0.60, smart_contract_audit_score:0.65, fractional_valuation_accuracy:0.62, secondary_market_depth:0.55, holder_churn_rate:0.38, regulatory_tokenization_clarity:0.60, custody_risk_score:0.35, cross_border_transfer_friction:0.42, dividend_payment_reliability:0.58, oracle_price_accuracy:0.62, community_governance_health:0.58, exit_mechanism_robustness:0.60, fractional_liquidity_pool_depth:0.52, token_utility_score:0.55 },
  // FO-007 carbon_credit EMEA — high regulatory_block
  { asset_id:"FO-007", asset_category:"carbon_credit",       region:"EMEA",  liquidity_fragmentation_risk:0.50, ownership_concentration_index:0.45, governance_token_participation:0.48, revenue_distribution_efficiency:0.42, smart_contract_audit_score:0.55, fractional_valuation_accuracy:0.50, secondary_market_depth:0.40, holder_churn_rate:0.48, regulatory_tokenization_clarity:0.15, custody_risk_score:0.45, cross_border_transfer_friction:0.78, dividend_payment_reliability:0.40, oracle_price_accuracy:0.55, community_governance_health:0.45, exit_mechanism_robustness:0.38, fractional_liquidity_pool_depth:0.38, token_utility_score:0.42 },
  // FO-008 data_cooperative APAC — critical holder_exodus
  { asset_id:"FO-008", asset_category:"data_cooperative",    region:"APAC",  liquidity_fragmentation_risk:0.62, ownership_concentration_index:0.50, governance_token_participation:0.28, revenue_distribution_efficiency:0.20, smart_contract_audit_score:0.40, fractional_valuation_accuracy:0.35, secondary_market_depth:0.18, holder_churn_rate:0.82, regulatory_tokenization_clarity:0.40, custody_risk_score:0.55, cross_border_transfer_friction:0.48, dividend_payment_reliability:0.18, oracle_price_accuracy:0.42, community_governance_health:0.25, exit_mechanism_robustness:0.22, fractional_liquidity_pool_depth:0.15, token_utility_score:0.25 },
];

type Asset = typeof MOCK_ASSETS[0];

function liquidityScore(a: Asset): number {
  const raw = a.liquidity_fragmentation_risk * 0.40
    + (1 - a.secondary_market_depth) * 0.35
    + (1 - a.fractional_liquidity_pool_depth) * 0.25;
  return Math.min(Math.round(raw * 100 * 100) / 100, 100);
}
function governanceScore(a: Asset): number {
  const raw = (1 - a.governance_token_participation) * 0.40
    + (1 - a.community_governance_health) * 0.35
    + a.ownership_concentration_index * 0.25;
  return Math.min(Math.round(raw * 100 * 100) / 100, 100);
}
function trustScore(a: Asset): number {
  const raw = (1 - a.smart_contract_audit_score) * 0.40
    + (1 - a.oracle_price_accuracy) * 0.35
    + a.custody_risk_score * 0.25;
  return Math.min(Math.round(raw * 100 * 100) / 100, 100);
}
function complianceScore(a: Asset): number {
  const raw = (1 - a.regulatory_tokenization_clarity) * 0.40
    + a.cross_border_transfer_friction * 0.35
    + (1 - a.exit_mechanism_robustness) * 0.25;
  return Math.min(Math.round(raw * 100 * 100) / 100, 100);
}
function composite(liq: number, gov: number, tru: number, comp: number): number {
  return Math.min(Math.round((liq * 0.30 + gov * 0.25 + tru * 0.25 + comp * 0.20) * 100) / 100, 100);
}
function ownershipPattern(a: Asset): string {
  if (a.liquidity_fragmentation_risk >= 0.70 && a.fractional_liquidity_pool_depth <= 0.30) return "liquidity_freeze";
  if (a.ownership_concentration_index >= 0.70 && a.governance_token_participation <= 0.30)  return "governance_capture";
  if (a.oracle_price_accuracy <= 0.30 && a.fractional_valuation_accuracy <= 0.35)           return "oracle_manipulation";
  if (a.regulatory_tokenization_clarity <= 0.30 || a.cross_border_transfer_friction >= 0.70) return "regulatory_block";
  if (a.holder_churn_rate >= 0.70 && a.secondary_market_depth <= 0.35)                       return "holder_exodus";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "frozen"; if (c >= 40) return "illiquid"; if (c >= 20) return "maturing"; return "liquid"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "liquidity_freeze" || p === "holder_exodus") return "emergency_liquidity";
    return "governance_reset";
  }
  if (r === "high") {
    if (p === "governance_capture") return "governance_reset";
    if (p === "regulatory_block")   return "compliance_sprint";
    return "market_deepening";
  }
  if (r === "moderate") return "token_monitoring";
  return "no_action";
}
function signal(a: Asset, pattern: string, comp: number): string {
  if (comp < 20) return "Actif fractionné en excellente santé — liquidité profonde, gouvernance décentralisée, conformité réglementaire assurée, oracles fiables";
  const labels: Record<string,string> = {
    liquidity_freeze:    "Gel de liquidité",
    governance_capture:  "Capture de gouvernance",
    oracle_manipulation: "Manipulation d'oracle",
    regulatory_block:    "Blocage réglementaire",
    holder_exodus:       "Exode des détenteurs",
  };
  const label = labels[pattern] ?? pattern.replace(/_/g," ");
  return `${label} — fragmentation liquidité ${a.liquidity_fragmentation_risk.toFixed(2)} — profondeur marché ${a.secondary_market_depth.toFixed(2)} — participation gouvernance ${a.governance_token_participation.toFixed(2)} — clarté réglementaire ${a.regulatory_tokenization_clarity.toFixed(2)} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const assets = MOCK_ASSETS.map(a => {
      const liq  = liquidityScore(a);
      const gov  = governanceScore(a);
      const tru  = trustScore(a);
      const comp = complianceScore(a);
      const c    = composite(liq, gov, tru, comp);
      const pat  = ownershipPattern(a);
      const r    = risk(c);
      const sev  = severity(c);
      const act  = action(r, pat);
      return {
        asset_id:                  a.asset_id,
        asset_category:            a.asset_category,
        region:                    a.region,
        ownership_risk:            r,
        ownership_pattern:         pat,
        ownership_severity:        sev,
        recommended_action:        act,
        liquidity_score:           liq,
        governance_score:          gov,
        trust_score:               tru,
        compliance_score:          comp,
        fractional_composite:      c,
        has_freeze_signal:         c >= 40 || a.liquidity_fragmentation_risk >= 0.60,
        estimated_illiquidity_index: Math.min(Math.round(c / 100 * (1 - a.fractional_liquidity_pool_depth + 0.01) * 10 * 100) / 100, 10.0),
        ownership_signal:          signal(a, pat, c),
      };
    });

    const rc: Record<string,number> = {}, pc: Record<string,number> = {}, sc: Record<string,number> = {}, ac: Record<string,number> = {};
    let tliq=0,tgov=0,ttru=0,tcomp=0,tcomposite=0,tilliq=0,freezeC=0,emergC=0;
    for (const asset of assets) {
      rc[asset.ownership_risk]      = (rc[asset.ownership_risk]      || 0) + 1;
      pc[asset.ownership_pattern]   = (pc[asset.ownership_pattern]   || 0) + 1;
      sc[asset.ownership_severity]  = (sc[asset.ownership_severity]  || 0) + 1;
      ac[asset.recommended_action]  = (ac[asset.recommended_action]  || 0) + 1;
      tliq       += asset.liquidity_score;
      tgov       += asset.governance_score;
      ttru       += asset.trust_score;
      tcomp      += asset.compliance_score;
      tcomposite += asset.fractional_composite;
      tilliq     += asset.estimated_illiquidity_index;
      if (asset.has_freeze_signal)                                                              freezeC++;
      if (asset.recommended_action === "emergency_liquidity" || asset.recommended_action === "governance_reset") emergC++;
    }
    const n = assets.length;
    return NextResponse.json({ assets, summary: {
      total:                           n,
      risk_counts:                     rc,
      pattern_counts:                  pc,
      severity_counts:                 sc,
      action_counts:                   ac,
      avg_fractional_composite:        Math.round(tcomposite / n * 10) / 10,
      freeze_signal_count:             freezeC,
      avg_liquidity_score:             Math.round(tliq / n * 10) / 10,
      avg_governance_score:            Math.round(tgov / n * 10) / 10,
      avg_trust_score:                 Math.round(ttru / n * 10) / 10,
      avg_compliance_score:            Math.round(tcomp / n * 10) / 10,
      avg_estimated_illiquidity_index: Math.round(tilliq / n * 100) / 100,
      emergency_action_count:          emergC,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/fractional-ownership-engine`)).json());
}
