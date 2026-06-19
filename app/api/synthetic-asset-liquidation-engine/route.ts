import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_PORTFOLIOS = [
  // SAL-001 collateralized_derivative EMEA — critical collateral_cascade
  { portfolio_id:"SAL-001", asset_class:"collateralized_derivative", region:"EMEA",   collateral_health_ratio:0.12, liquidation_threshold_proximity:0.92, counterparty_default_risk:0.82, smart_contract_audit_score:0.35, protocol_liquidity_depth:0.22, oracle_manipulation_risk:0.55, slippage_exposure:0.65, impermanent_loss_risk:0.70, governance_attack_surface:0.60, cross_chain_bridge_risk:0.55, flash_loan_vulnerability:0.50, regulatory_seizure_risk:0.60, defi_protocol_concentration:0.75, synthetic_peg_stability:0.30, on_chain_transparency_score:0.28, insurance_coverage_ratio:0.10, exit_liquidity_score:0.18 },
  // SAL-002 yield_vault NAMER — low secured
  { portfolio_id:"SAL-002", asset_class:"yield_vault",               region:"NAMER",  collateral_health_ratio:0.92, liquidation_threshold_proximity:0.08, counterparty_default_risk:0.05, smart_contract_audit_score:0.95, protocol_liquidity_depth:0.90, oracle_manipulation_risk:0.06, slippage_exposure:0.05, impermanent_loss_risk:0.10, governance_attack_surface:0.08, cross_chain_bridge_risk:0.05, flash_loan_vulnerability:0.04, regulatory_seizure_risk:0.08, defi_protocol_concentration:0.10, synthetic_peg_stability:0.95, on_chain_transparency_score:0.92, insurance_coverage_ratio:0.85, exit_liquidity_score:0.92 },
  // SAL-003 synthetic_equity APAC — high oracle_attack
  { portfolio_id:"SAL-003", asset_class:"synthetic_equity",          region:"APAC",   collateral_health_ratio:0.52, liquidation_threshold_proximity:0.48, counterparty_default_risk:0.42, smart_contract_audit_score:0.40, protocol_liquidity_depth:0.55, oracle_manipulation_risk:0.78, slippage_exposure:0.45, impermanent_loss_risk:0.50, governance_attack_surface:0.55, cross_chain_bridge_risk:0.42, flash_loan_vulnerability:0.68, regulatory_seizure_risk:0.38, defi_protocol_concentration:0.48, synthetic_peg_stability:0.58, on_chain_transparency_score:0.50, insurance_coverage_ratio:0.30, exit_liquidity_score:0.48 },
  // SAL-004 tokenized_debt LATAM — low monitored
  { portfolio_id:"SAL-004", asset_class:"tokenized_debt",            region:"LATAM",  collateral_health_ratio:0.80, liquidation_threshold_proximity:0.15, counterparty_default_risk:0.18, smart_contract_audit_score:0.82, protocol_liquidity_depth:0.78, oracle_manipulation_risk:0.12, slippage_exposure:0.15, impermanent_loss_risk:0.20, governance_attack_surface:0.18, cross_chain_bridge_risk:0.20, flash_loan_vulnerability:0.15, regulatory_seizure_risk:0.22, defi_protocol_concentration:0.25, synthetic_peg_stability:0.88, on_chain_transparency_score:0.80, insurance_coverage_ratio:0.70, exit_liquidity_score:0.80 },
  // SAL-005 liquidity_pool EMEA — critical protocol_exploit
  { portfolio_id:"SAL-005", asset_class:"liquidity_pool",            region:"EMEA",   collateral_health_ratio:0.20, liquidation_threshold_proximity:0.82, counterparty_default_risk:0.72, smart_contract_audit_score:0.15, protocol_liquidity_depth:0.18, oracle_manipulation_risk:0.62, slippage_exposure:0.78, impermanent_loss_risk:0.85, governance_attack_surface:0.78, cross_chain_bridge_risk:0.68, flash_loan_vulnerability:0.72, regulatory_seizure_risk:0.65, defi_protocol_concentration:0.82, synthetic_peg_stability:0.25, on_chain_transparency_score:0.18, insurance_coverage_ratio:0.05, exit_liquidity_score:0.12 },
  // SAL-006 structured_product NAMER — moderate none
  { portfolio_id:"SAL-006", asset_class:"structured_product",        region:"NAMER",  collateral_health_ratio:0.65, liquidation_threshold_proximity:0.32, counterparty_default_risk:0.28, smart_contract_audit_score:0.62, protocol_liquidity_depth:0.58, oracle_manipulation_risk:0.28, slippage_exposure:0.32, impermanent_loss_risk:0.38, governance_attack_surface:0.35, cross_chain_bridge_risk:0.30, flash_loan_vulnerability:0.28, regulatory_seizure_risk:0.35, defi_protocol_concentration:0.42, synthetic_peg_stability:0.68, on_chain_transparency_score:0.62, insurance_coverage_ratio:0.48, exit_liquidity_score:0.60 },
  // SAL-007 cross_chain_bridge APAC — high liquidity_crunch
  { portfolio_id:"SAL-007", asset_class:"cross_chain_bridge",        region:"APAC",   collateral_health_ratio:0.42, liquidation_threshold_proximity:0.58, counterparty_default_risk:0.50, smart_contract_audit_score:0.48, protocol_liquidity_depth:0.18, oracle_manipulation_risk:0.42, slippage_exposure:0.72, impermanent_loss_risk:0.65, governance_attack_surface:0.55, cross_chain_bridge_risk:0.72, flash_loan_vulnerability:0.45, regulatory_seizure_risk:0.48, defi_protocol_concentration:0.60, synthetic_peg_stability:0.45, on_chain_transparency_score:0.42, insurance_coverage_ratio:0.22, exit_liquidity_score:0.20 },
  // SAL-008 algorithmic_stablecoin MEA — critical peg_destabilization
  { portfolio_id:"SAL-008", asset_class:"algorithmic_stablecoin",    region:"MEA",    collateral_health_ratio:0.15, liquidation_threshold_proximity:0.88, counterparty_default_risk:0.78, smart_contract_audit_score:0.22, protocol_liquidity_depth:0.12, oracle_manipulation_risk:0.70, slippage_exposure:0.82, impermanent_loss_risk:0.88, governance_attack_surface:0.82, cross_chain_bridge_risk:0.75, flash_loan_vulnerability:0.68, regulatory_seizure_risk:0.80, defi_protocol_concentration:0.88, synthetic_peg_stability:0.12, on_chain_transparency_score:0.15, insurance_coverage_ratio:0.05, exit_liquidity_score:0.08 },
];

type Portfolio = typeof MOCK_PORTFOLIOS[0];

function collateralScore(p: Portfolio): number {
  let s = 0;
  if      (p.collateral_health_ratio <= 0.20) s += 40; else if (p.collateral_health_ratio <= 0.40) s += 25; else if (p.collateral_health_ratio <= 0.60) s += 10;
  if      (p.liquidation_threshold_proximity >= 0.80) s += 35; else if (p.liquidation_threshold_proximity >= 0.60) s += 20; else if (p.liquidation_threshold_proximity >= 0.40) s += 8;
  if      (p.counterparty_default_risk >= 0.70) s += 25; else if (p.counterparty_default_risk >= 0.50) s += 14; else if (p.counterparty_default_risk >= 0.30) s += 5;
  return Math.min(s, 100);
}
function protocolScore(p: Portfolio): number {
  let s = 0;
  if      (p.smart_contract_audit_score <= 0.20) s += 40; else if (p.smart_contract_audit_score <= 0.45) s += 24; else if (p.smart_contract_audit_score <= 0.65) s += 10;
  if      (p.oracle_manipulation_risk >= 0.70) s += 35; else if (p.oracle_manipulation_risk >= 0.50) s += 20; else if (p.oracle_manipulation_risk >= 0.30) s += 8;
  if      (p.flash_loan_vulnerability >= 0.65) s += 25; else if (p.flash_loan_vulnerability >= 0.45) s += 14; else if (p.flash_loan_vulnerability >= 0.25) s += 5;
  return Math.min(s, 100);
}
function liquidityScore(p: Portfolio): number {
  let s = 0;
  if      (p.protocol_liquidity_depth <= 0.20) s += 40; else if (p.protocol_liquidity_depth <= 0.40) s += 25; else if (p.protocol_liquidity_depth <= 0.60) s += 10;
  if      (p.slippage_exposure >= 0.70) s += 35; else if (p.slippage_exposure >= 0.50) s += 20; else if (p.slippage_exposure >= 0.30) s += 8;
  if      (p.exit_liquidity_score <= 0.20) s += 25; else if (p.exit_liquidity_score <= 0.45) s += 14; else if (p.exit_liquidity_score <= 0.65) s += 5;
  return Math.min(s, 100);
}
function systemicScore(p: Portfolio): number {
  let s = 0;
  if      (p.defi_protocol_concentration >= 0.75) s += 40; else if (p.defi_protocol_concentration >= 0.55) s += 24; else if (p.defi_protocol_concentration >= 0.35) s += 10;
  if      (p.cross_chain_bridge_risk >= 0.70) s += 35; else if (p.cross_chain_bridge_risk >= 0.50) s += 20; else if (p.cross_chain_bridge_risk >= 0.30) s += 8;
  if      (p.regulatory_seizure_risk >= 0.65) s += 25; else if (p.regulatory_seizure_risk >= 0.45) s += 14; else if (p.regulatory_seizure_risk >= 0.25) s += 5;
  return Math.min(s, 100);
}
function composite(col: number, prot: number, liq: number, sys: number): number {
  return Math.min(Math.round((col * 0.30 + prot * 0.25 + liq * 0.25 + sys * 0.20) * 100) / 100, 100);
}
function liquidationPattern(p: Portfolio): string {
  if (p.collateral_health_ratio <= 0.25 && p.liquidation_threshold_proximity >= 0.70) return "collateral_cascade";
  if (p.oracle_manipulation_risk >= 0.65 || p.flash_loan_vulnerability >= 0.65) return "oracle_attack";
  if (p.protocol_liquidity_depth <= 0.25 && p.slippage_exposure >= 0.60) return "liquidity_crunch";
  if (p.smart_contract_audit_score <= 0.30) return "protocol_exploit";
  if (p.synthetic_peg_stability <= 0.30 && ["algorithmic_stablecoin","collateralized_derivative","structured_product"].includes(p.asset_class)) return "peg_destabilization";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "liquidating"; if (c >= 40) return "at_risk"; if (c >= 20) return "monitored"; return "secured"; }
function action(r: string, pat: string): string {
  if (r === "critical") {
    if (pat === "collateral_cascade") return "emergency_deleveraging";
    if (pat === "protocol_exploit")   return "protocol_pause";
    return "collateral_injection";
  }
  if (r === "high") {
    if (pat === "oracle_attack")    return "oracle_diversification";
    if (pat === "liquidity_crunch") return "liquidity_reinforcement";
    return "risk_rebalancing";
  }
  if (r === "moderate") return "defi_monitoring";
  return "no_action";
}
function signal(p: Portfolio, pat: string, comp: number): string {
  if (comp < 20) return "Portefeuille synthétique sécurisé — ratio collatéral sain, protocoles audités, liquidité DeFi suffisante";
  const labels: Record<string,string> = {
    collateral_cascade:  "Cascade de collatéral",
    oracle_attack:       "Attaque oracle",
    liquidity_crunch:    "Crise de liquidité",
    protocol_exploit:    "Exploit protocole",
    peg_destabilization: "Déstabilisation du peg",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — collatéral ${p.collateral_health_ratio.toFixed(2)} (seuil liq. ${p.liquidation_threshold_proximity.toFixed(2)}) — oracle risk ${p.oracle_manipulation_risk.toFixed(2)} — liquidité ${p.protocol_liquidity_depth.toFixed(2)} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const portfolios = MOCK_PORTFOLIOS.map(p => {
      const col = collateralScore(p), prot = protocolScore(p), liq = liquidityScore(p), sys = systemicScore(p);
      const comp = composite(col, prot, liq, sys), pat = liquidationPattern(p), r = risk(comp), sev = severity(comp), act = action(r, pat);
      return {
        portfolio_id: p.portfolio_id, asset_class: p.asset_class, region: p.region,
        liquidation_risk: r, liquidation_pattern: pat, liquidation_severity: sev, recommended_action: act,
        collateral_score: col, protocol_score: prot, liquidity_score: liq, systemic_score: sys,
        liquidation_composite: comp,
        is_liquidation_imminent: comp >= 60 || p.collateral_health_ratio <= 0.15 || p.liquidation_threshold_proximity >= 0.90,
        requires_collateral_top_up: comp >= 40 || p.collateral_health_ratio <= 0.35 || p.liquidation_threshold_proximity >= 0.65,
        estimated_liquidation_risk_index: Math.min(Math.round(comp/100*(1-p.insurance_coverage_ratio+0.01)*10*100)/100, 10.0),
        liquidation_signal: signal(p, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tcol=0,tprot=0,tliq=0,tsys=0,tcomp=0,tidx=0,imminentC=0,topupC=0;
    for (const port of portfolios) {
      rc[port.liquidation_risk]=(rc[port.liquidation_risk]||0)+1;
      pc[port.liquidation_pattern]=(pc[port.liquidation_pattern]||0)+1;
      sc[port.liquidation_severity]=(sc[port.liquidation_severity]||0)+1;
      ac[port.recommended_action]=(ac[port.recommended_action]||0)+1;
      tcol+=port.collateral_score; tprot+=port.protocol_score; tliq+=port.liquidity_score; tsys+=port.systemic_score;
      tcomp+=port.liquidation_composite; tidx+=port.estimated_liquidation_risk_index;
      if (port.is_liquidation_imminent) imminentC++;
      if (port.requires_collateral_top_up) topupC++;
    }
    const n = portfolios.length;
    return NextResponse.json({ portfolios, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_liquidation_composite: Math.round(tcomp/n*10)/10,
      liquidation_imminent_count: imminentC,
      collateral_top_up_count: topupC,
      avg_collateral_score: Math.round(tcol/n*10)/10,
      avg_protocol_score: Math.round(tprot/n*10)/10,
      avg_liquidity_score: Math.round(tliq/n*10)/10,
      avg_systemic_score: Math.round(tsys/n*10)/10,
      avg_estimated_liquidation_risk_index: Math.round(tidx/n*100)/100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/synthetic-asset-liquidation-engine`)).json());
}
