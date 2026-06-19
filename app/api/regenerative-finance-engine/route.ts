import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_FUNDS = [
  // RF-001 carbon_market EMEA — critical greenwashing_exposure
  { fund_id:"RF-001", fund_type:"carbon_market",          region:"EMEA",   additionality_score:0.15, measurability_of_impact:0.20, greenwashing_risk:0.88, stakeholder_inclusion_depth:0.30, planetary_boundary_alignment:0.22, capital_recycling_efficiency:0.28, community_benefit_ratio:0.18, reporting_transparency_score:0.15, impact_reversibility_risk:0.75, blended_finance_leverage:0.20, sdg_alignment_score:0.22, indigenous_rights_respect:0.12, carbon_integrity_score:0.10, biodiversity_net_gain:0.18, social_return_on_investment:0.20, regenerative_multiplier:0.15, impact_verification_rigor:0.12 },
  // RF-002 biodiversity_credit APAC — low thriving
  { fund_id:"RF-002", fund_type:"biodiversity_credit",    region:"APAC",   additionality_score:0.92, measurability_of_impact:0.90, greenwashing_risk:0.05, stakeholder_inclusion_depth:0.92, planetary_boundary_alignment:0.95, capital_recycling_efficiency:0.88, community_benefit_ratio:0.90, reporting_transparency_score:0.92, impact_reversibility_risk:0.05, blended_finance_leverage:0.85, sdg_alignment_score:0.95, indigenous_rights_respect:0.92, carbon_integrity_score:0.90, biodiversity_net_gain:0.95, social_return_on_investment:0.88, regenerative_multiplier:0.92, impact_verification_rigor:0.90 },
  // RF-003 blended_finance NAMER — high impact_dilution
  { fund_id:"RF-003", fund_type:"blended_finance",        region:"NAMER",  additionality_score:0.50, measurability_of_impact:0.22, greenwashing_risk:0.42, stakeholder_inclusion_depth:0.55, planetary_boundary_alignment:0.48, capital_recycling_efficiency:0.50, community_benefit_ratio:0.45, reporting_transparency_score:0.48, impact_reversibility_risk:0.38, blended_finance_leverage:0.65, sdg_alignment_score:0.28, indigenous_rights_respect:0.50, carbon_integrity_score:0.52, biodiversity_net_gain:0.40, social_return_on_investment:0.45, regenerative_multiplier:0.48, impact_verification_rigor:0.45 },
  // RF-004 social_impact_fund LATAM — low regenerating
  { fund_id:"RF-004", fund_type:"social_impact_fund",     region:"LATAM",  additionality_score:0.78, measurability_of_impact:0.80, greenwashing_risk:0.12, stakeholder_inclusion_depth:0.82, planetary_boundary_alignment:0.75, capital_recycling_efficiency:0.78, community_benefit_ratio:0.85, reporting_transparency_score:0.80, impact_reversibility_risk:0.15, blended_finance_leverage:0.70, sdg_alignment_score:0.82, indigenous_rights_respect:0.75, carbon_integrity_score:0.78, biodiversity_net_gain:0.72, social_return_on_investment:0.85, regenerative_multiplier:0.78, impact_verification_rigor:0.80 },
  // RF-005 indigenous_land_trust APAC — critical exclusion_deficit
  { fund_id:"RF-005", fund_type:"indigenous_land_trust",  region:"APAC",   additionality_score:0.60, measurability_of_impact:0.55, greenwashing_risk:0.50, stakeholder_inclusion_depth:0.18, planetary_boundary_alignment:0.58, capital_recycling_efficiency:0.52, community_benefit_ratio:0.20, reporting_transparency_score:0.50, impact_reversibility_risk:0.62, blended_finance_leverage:0.40, sdg_alignment_score:0.55, indigenous_rights_respect:0.12, carbon_integrity_score:0.50, biodiversity_net_gain:0.42, social_return_on_investment:0.38, regenerative_multiplier:0.45, impact_verification_rigor:0.48 },
  // RF-006 circular_economy_fund MEA — moderate none
  { fund_id:"RF-006", fund_type:"circular_economy_fund",  region:"MEA",    additionality_score:0.62, measurability_of_impact:0.65, greenwashing_risk:0.28, stakeholder_inclusion_depth:0.62, planetary_boundary_alignment:0.65, capital_recycling_efficiency:0.70, community_benefit_ratio:0.62, reporting_transparency_score:0.60, impact_reversibility_risk:0.28, blended_finance_leverage:0.58, sdg_alignment_score:0.65, indigenous_rights_respect:0.60, carbon_integrity_score:0.65, biodiversity_net_gain:0.58, social_return_on_investment:0.62, regenerative_multiplier:0.60, impact_verification_rigor:0.62 },
  // RF-007 blue_economy EMEA — high measurement_gap
  { fund_id:"RF-007", fund_type:"blue_economy",           region:"EMEA",   additionality_score:0.55, measurability_of_impact:0.58, greenwashing_risk:0.38, stakeholder_inclusion_depth:0.52, planetary_boundary_alignment:0.55, capital_recycling_efficiency:0.48, community_benefit_ratio:0.50, reporting_transparency_score:0.22, impact_reversibility_risk:0.42, blended_finance_leverage:0.50, sdg_alignment_score:0.55, indigenous_rights_respect:0.55, carbon_integrity_score:0.52, biodiversity_net_gain:0.48, social_return_on_investment:0.50, regenerative_multiplier:0.52, impact_verification_rigor:0.18 },
  // RF-008 impact_bond NAMER — critical capital_misallocation
  { fund_id:"RF-008", fund_type:"impact_bond",            region:"NAMER",  additionality_score:0.45, measurability_of_impact:0.48, greenwashing_risk:0.55, stakeholder_inclusion_depth:0.42, planetary_boundary_alignment:0.40, capital_recycling_efficiency:0.12, community_benefit_ratio:0.38, reporting_transparency_score:0.42, impact_reversibility_risk:0.68, blended_finance_leverage:0.35, sdg_alignment_score:0.42, indigenous_rights_respect:0.40, carbon_integrity_score:0.45, biodiversity_net_gain:0.30, social_return_on_investment:0.35, regenerative_multiplier:0.15, impact_verification_rigor:0.40 },
];

type Fund = typeof MOCK_FUNDS[0];

function integrityScore(f: Fund): number {
  let s = 0;
  if      (f.greenwashing_risk >= 0.70) s += 40; else if (f.greenwashing_risk >= 0.45) s += 22; else if (f.greenwashing_risk >= 0.25) s += 8;
  if      (f.impact_reversibility_risk >= 0.65) s += 35; else if (f.impact_reversibility_risk >= 0.40) s += 18; else if (f.impact_reversibility_risk >= 0.20) s += 6;
  if      (f.additionality_score <= 0.30) s += 25; else if (f.additionality_score <= 0.55) s += 12;
  return Math.min(s, 100);
}
function impactScore(f: Fund): number {
  let s = 0;
  if      (f.measurability_of_impact <= 0.30) s += 40; else if (f.measurability_of_impact <= 0.55) s += 22; else if (f.measurability_of_impact <= 0.75) s += 8;
  if      (f.sdg_alignment_score <= 0.30) s += 35; else if (f.sdg_alignment_score <= 0.55) s += 18; else if (f.sdg_alignment_score <= 0.75) s += 6;
  if      (f.planetary_boundary_alignment <= 0.30) s += 25; else if (f.planetary_boundary_alignment <= 0.55) s += 12;
  return Math.min(s, 100);
}
function inclusionScore(f: Fund): number {
  let s = 0;
  if      (f.stakeholder_inclusion_depth <= 0.30) s += 40; else if (f.stakeholder_inclusion_depth <= 0.55) s += 22; else if (f.stakeholder_inclusion_depth <= 0.75) s += 8;
  if      (f.indigenous_rights_respect <= 0.30) s += 35; else if (f.indigenous_rights_respect <= 0.55) s += 18; else if (f.indigenous_rights_respect <= 0.75) s += 6;
  if      (f.community_benefit_ratio <= 0.30) s += 25; else if (f.community_benefit_ratio <= 0.55) s += 12;
  return Math.min(s, 100);
}
function verificationScore(f: Fund): number {
  let s = 0;
  if      (f.reporting_transparency_score <= 0.30) s += 40; else if (f.reporting_transparency_score <= 0.55) s += 22; else if (f.reporting_transparency_score <= 0.75) s += 8;
  if      (f.impact_verification_rigor <= 0.30) s += 35; else if (f.impact_verification_rigor <= 0.55) s += 18; else if (f.impact_verification_rigor <= 0.75) s += 6;
  if      (f.carbon_integrity_score <= 0.30) s += 25; else if (f.carbon_integrity_score <= 0.55) s += 12;
  return Math.min(s, 100);
}
function composite(integ: number, imp: number, incl: number, verif: number): number {
  return Math.min(Math.round((integ * 0.30 + imp * 0.25 + incl * 0.25 + verif * 0.20) * 100) / 100, 100);
}
function impactPattern(f: Fund): string {
  if (f.greenwashing_risk >= 0.65 && f.carbon_integrity_score <= 0.35) return "greenwashing_exposure";
  if (f.measurability_of_impact <= 0.30 && f.sdg_alignment_score <= 0.35) return "impact_dilution";
  if (f.indigenous_rights_respect <= 0.30 && f.stakeholder_inclusion_depth <= 0.35) return "exclusion_deficit";
  if (f.impact_verification_rigor <= 0.30 && f.reporting_transparency_score <= 0.35) return "measurement_gap";
  if (f.capital_recycling_efficiency <= 0.25 && f.regenerative_multiplier <= 0.30) return "capital_misallocation";
  return "none";
}
function riskLevel(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string  { if (c >= 60) return "extractive"; if (c >= 40) return "transitioning"; if (c >= 20) return "regenerating"; return "thriving"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "greenwashing_exposure") return "greenwashing_intervention"; return "impact_audit"; }
  if (r === "high") { if (p === "exclusion_deficit") return "stakeholder_realignment"; return "measurement_upgrade"; }
  if (r === "moderate") return "impact_monitoring";
  return "no_action";
}
function signal(f: Fund, pat: string, comp: number): string {
  if (comp < 20) return `Finance régénérative exemplaire — intégrité carbone certifiée, droits autochtones respectés, impact mesurable et vérifiable, multiplicateur régénératif ${f.regenerative_multiplier.toFixed(2)}`;
  const labels: Record<string,string> = {
    greenwashing_exposure:"Exposition au greenwashing", impact_dilution:"Dilution d'impact",
    exclusion_deficit:"Déficit d'inclusion", measurement_gap:"Lacune de mesure",
    capital_misallocation:"Mauvaise allocation du capital",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — risque greenwashing ${f.greenwashing_risk.toFixed(2)} — alignement SDG ${f.sdg_alignment_score.toFixed(2)} — droits autochtones ${f.indigenous_rights_respect.toFixed(2)} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const funds = MOCK_FUNDS.map(f => {
      const integ = integrityScore(f), imp = impactScore(f), incl = inclusionScore(f), verif = verificationScore(f);
      const comp = composite(integ, imp, incl, verif), pat = impactPattern(f), r = riskLevel(comp), sev = severity(comp), act = action(r, pat);
      return {
        fund_id: f.fund_id, fund_type: f.fund_type, region: f.region,
        regen_finance_risk: r, impact_pattern: pat, impact_severity: sev, recommended_action: act,
        integrity_score: integ, impact_score: imp, inclusion_score: incl, verification_score: verif,
        regen_finance_composite: comp,
        has_greenwashing_signal: comp >= 40 || f.greenwashing_risk >= 0.55 || f.carbon_integrity_score <= 0.35,
        requires_impact_audit: comp >= 25 || f.impact_verification_rigor <= 0.35 || f.additionality_score <= 0.30,
        estimated_impact_deficit_index: Math.min(Math.round(comp/100*(1-f.impact_verification_rigor+0.01)*10*100)/100, 10.0),
        regen_signal: signal(f, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tInteg=0, tImp=0, tIncl=0, tVerif=0, tComp=0, tDef=0, gwC=0, auditC=0;
    for (const fund of funds) {
      rc[fund.regen_finance_risk]=(rc[fund.regen_finance_risk]||0)+1;
      pc[fund.impact_pattern]=(pc[fund.impact_pattern]||0)+1;
      sc[fund.impact_severity]=(sc[fund.impact_severity]||0)+1;
      ac[fund.recommended_action]=(ac[fund.recommended_action]||0)+1;
      tInteg+=fund.integrity_score; tImp+=fund.impact_score; tIncl+=fund.inclusion_score; tVerif+=fund.verification_score;
      tComp+=fund.regen_finance_composite; tDef+=fund.estimated_impact_deficit_index;
      if (fund.has_greenwashing_signal) gwC++;
      if (fund.requires_impact_audit) auditC++;
    }
    const n = funds.length;
    const summary = {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_regen_finance_composite: Math.round(tComp/n*10)/10,
      greenwashing_signal_count: gwC,
      impact_audit_required_count: auditC,
      avg_integrity_score: Math.round(tInteg/n*10)/10,
      avg_impact_score: Math.round(tImp/n*10)/10,
      avg_inclusion_score: Math.round(tIncl/n*10)/10,
      avg_verification_score: Math.round(tVerif/n*10)/10,
      avg_estimated_impact_deficit_index: Math.round(tDef/n*100)/100,
    };
    return NextResponse.json(sealResponse({ funds, summary }, "regenerative-finance-engine") as Parameters<typeof NextResponse.json>[0]);
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/regenerative-finance-engine`)).json());
}
