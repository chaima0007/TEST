import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ACCOUNTS = [
  { account_id:"EX-001", region:"EMEA",  evaluation_period_id:"Q1-2026", license_utilization_pct:0.94, feature_depth_score_pct:0.82, api_call_growth_rate_pct:0.38, storage_utilization_pct:0.91, adjacent_product_fit_score:0.88, competitor_displacement_pct:0.58, integration_gap_count:6, feature_request_frequency:9, power_user_pct:0.48, nps_score:78.0, executive_engagement_score:0.82, expansion_conversation_initiated:0.8, champion_advocacy_score:0.88, stakeholder_growth_count:4, contract_renewal_months:7, upsell_budget_confirmed:0.85, current_arr_usd:220000, potential_expansion_arr_usd:180000, account_tenure_months:20 },
  { account_id:"EX-002", region:"NAMER", evaluation_period_id:"Q1-2026", license_utilization_pct:0.35, feature_depth_score_pct:0.28, api_call_growth_rate_pct:0.03, storage_utilization_pct:0.25, adjacent_product_fit_score:0.15, competitor_displacement_pct:0.10, integration_gap_count:0, feature_request_frequency:1, power_user_pct:0.06, nps_score:20.0, executive_engagement_score:0.18, expansion_conversation_initiated:0.0, champion_advocacy_score:0.15, stakeholder_growth_count:0, contract_renewal_months:14, upsell_budget_confirmed:0.05, current_arr_usd:95000, potential_expansion_arr_usd:20000, account_tenure_months:6 },
  { account_id:"EX-003", region:"APAC",  evaluation_period_id:"Q1-2026", license_utilization_pct:0.78, feature_depth_score_pct:0.60, api_call_growth_rate_pct:0.18, storage_utilization_pct:0.68, adjacent_product_fit_score:0.62, competitor_displacement_pct:0.35, integration_gap_count:3, feature_request_frequency:5, power_user_pct:0.28, nps_score:58.0, executive_engagement_score:0.55, expansion_conversation_initiated:0.5, champion_advocacy_score:0.60, stakeholder_growth_count:2, contract_renewal_months:5, upsell_budget_confirmed:0.55, current_arr_usd:140000, potential_expansion_arr_usd:85000, account_tenure_months:12 },
  { account_id:"EX-004", region:"LATAM", evaluation_period_id:"Q1-2026", license_utilization_pct:0.96, feature_depth_score_pct:0.90, api_call_growth_rate_pct:0.45, storage_utilization_pct:0.95, adjacent_product_fit_score:0.92, competitor_displacement_pct:0.65, integration_gap_count:8, feature_request_frequency:12, power_user_pct:0.55, nps_score:85.0, executive_engagement_score:0.90, expansion_conversation_initiated:0.95, champion_advocacy_score:0.92, stakeholder_growth_count:6, contract_renewal_months:6, upsell_budget_confirmed:0.92, current_arr_usd:310000, potential_expansion_arr_usd:250000, account_tenure_months:24 },
  { account_id:"EX-005", region:"EMEA",  evaluation_period_id:"Q1-2026", license_utilization_pct:0.52, feature_depth_score_pct:0.42, api_call_growth_rate_pct:0.08, storage_utilization_pct:0.45, adjacent_product_fit_score:0.38, competitor_displacement_pct:0.20, integration_gap_count:2, feature_request_frequency:3, power_user_pct:0.14, nps_score:42.0, executive_engagement_score:0.35, expansion_conversation_initiated:0.2, champion_advocacy_score:0.38, stakeholder_growth_count:1, contract_renewal_months:10, upsell_budget_confirmed:0.22, current_arr_usd:75000, potential_expansion_arr_usd:35000, account_tenure_months:9 },
  { account_id:"EX-006", region:"NAMER", evaluation_period_id:"Q1-2026", license_utilization_pct:0.88, feature_depth_score_pct:0.75, api_call_growth_rate_pct:0.25, storage_utilization_pct:0.80, adjacent_product_fit_score:0.78, competitor_displacement_pct:0.48, integration_gap_count:5, feature_request_frequency:7, power_user_pct:0.38, nps_score:68.0, executive_engagement_score:0.72, expansion_conversation_initiated:0.7, champion_advocacy_score:0.75, stakeholder_growth_count:3, contract_renewal_months:4, upsell_budget_confirmed:0.70, current_arr_usd:185000, potential_expansion_arr_usd:130000, account_tenure_months:16 },
  { account_id:"EX-007", region:"APAC",  evaluation_period_id:"Q1-2026", license_utilization_pct:0.62, feature_depth_score_pct:0.50, api_call_growth_rate_pct:0.12, storage_utilization_pct:0.58, adjacent_product_fit_score:0.48, competitor_displacement_pct:0.28, integration_gap_count:2, feature_request_frequency:4, power_user_pct:0.20, nps_score:50.0, executive_engagement_score:0.45, expansion_conversation_initiated:0.35, champion_advocacy_score:0.45, stakeholder_growth_count:1, contract_renewal_months:8, upsell_budget_confirmed:0.35, current_arr_usd:110000, potential_expansion_arr_usd:55000, account_tenure_months:10 },
  { account_id:"EX-008", region:"MEA",   evaluation_period_id:"Q1-2026", license_utilization_pct:0.82, feature_depth_score_pct:0.68, api_call_growth_rate_pct:0.22, storage_utilization_pct:0.75, adjacent_product_fit_score:0.70, competitor_displacement_pct:0.42, integration_gap_count:4, feature_request_frequency:6, power_user_pct:0.32, nps_score:62.0, executive_engagement_score:0.65, expansion_conversation_initiated:0.6, champion_advocacy_score:0.68, stakeholder_growth_count:2, contract_renewal_months:5, upsell_budget_confirmed:0.60, current_arr_usd:160000, potential_expansion_arr_usd:105000, account_tenure_months:14 },
];

type Acct = typeof MOCK_ACCOUNTS[0];

function usageCeilingScore(i: Acct): number {
  let s = 0;
  if      (i.license_utilization_pct  >= 0.90) s += 40; else if (i.license_utilization_pct >= 0.75) s += 22; else if (i.license_utilization_pct >= 0.60) s += 8;
  if      (i.api_call_growth_rate_pct >= 0.30) s += 35; else if (i.api_call_growth_rate_pct >= 0.15) s += 18; else if (i.api_call_growth_rate_pct >= 0.05) s += 6;
  if      (i.storage_utilization_pct  >= 0.85) s += 25; else if (i.storage_utilization_pct >= 0.65) s += 12;
  return Math.min(s, 100);
}
function productGapScore(i: Acct): number {
  let s = 0;
  if      (i.adjacent_product_fit_score  >= 0.80) s += 40; else if (i.adjacent_product_fit_score >= 0.60) s += 22; else if (i.adjacent_product_fit_score >= 0.40) s += 8;
  if      (i.integration_gap_count       >= 5)    s += 35; else if (i.integration_gap_count >= 3) s += 18; else if (i.integration_gap_count >= 1) s += 6;
  if      (i.competitor_displacement_pct >= 0.50) s += 25; else if (i.competitor_displacement_pct >= 0.30) s += 12;
  return Math.min(s, 100);
}
function engagementScore(i: Acct): number {
  let s = 0;
  if      (i.power_user_pct             >= 0.40) s += 45; else if (i.power_user_pct >= 0.25) s += 25; else if (i.power_user_pct >= 0.12) s += 10;
  if      (i.nps_score                  >= 70)   s += 30; else if (i.nps_score >= 50) s += 15;
  if      (i.executive_engagement_score >= 0.75) s += 25; else if (i.executive_engagement_score >= 0.50) s += 12;
  return Math.min(s, 100);
}
function relationshipScore(i: Acct): number {
  let s = 0;
  if      (i.champion_advocacy_score  >= 0.80) s += 40; else if (i.champion_advocacy_score >= 0.60) s += 22; else if (i.champion_advocacy_score >= 0.40) s += 8;
  if      (i.stakeholder_growth_count >= 4)    s += 35; else if (i.stakeholder_growth_count >= 2) s += 18; else if (i.stakeholder_growth_count >= 1) s += 6;
  if      (i.upsell_budget_confirmed  >= 0.80) s += 25; else if (i.upsell_budget_confirmed >= 0.50) s += 12;
  return Math.min(s, 100);
}
function composite(uc: number, pg: number, en: number, re: number): number {
  return Math.min(Math.round((uc * 0.30 + pg * 0.25 + en * 0.25 + re * 0.20) * 100) / 100, 100);
}
function pattern(i: Acct): string {
  if (i.license_utilization_pct >= 0.88 && i.api_call_growth_rate_pct >= 0.20)       return "usage_ceiling_breach";
  if (i.adjacent_product_fit_score >= 0.75 && i.integration_gap_count >= 3)           return "product_gap_signal";
  if (i.power_user_pct >= 0.35 && i.nps_score >= 65)                                  return "engagement_elevation";
  if (i.executive_engagement_score >= 0.70 && i.champion_advocacy_score >= 0.65)      return "executive_pull_through";
  if (i.competitor_displacement_pct >= 0.40 && i.feature_request_frequency >= 4)      return "contract_white_space";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "urgent"; if (c >= 40) return "active"; if (c >= 20) return "emerging"; return "dormant"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "executive_pull_through" || p === "usage_ceiling_breach") return "expansion_fast_track"; return "executive_expansion_briefing"; }
  if (r === "high") {
    if (p === "usage_ceiling_breach")   return "usage_ceiling_upsell";
    if (p === "product_gap_signal")     return "product_gap_discovery_call";
    if (p === "engagement_elevation")   return "qbr_expansion_pitch";
    if (p === "executive_pull_through") return "executive_expansion_briefing";
    if (p === "contract_white_space")   return "white_space_mapping_session";
    return "expansion_monitoring";
  }
  if (r === "moderate") return "cross_sell_campaign";
  return "no_action";
}
function signal(i: Acct, pat: string, comp: number): string {
  if (comp < 20) return "Expansion signals dormant — account usage, engagement and relationship indicators below expansion threshold";
  const labels: Record<string,string> = { usage_ceiling_breach:"Usage ceiling breach", product_gap_signal:"Product gap signal", engagement_elevation:"Engagement elevation", executive_pull_through:"Executive pull-through", contract_white_space:"Contract white space" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(i.license_utilization_pct*100)}% license utilization — ${Math.round(i.power_user_pct*100)}% power users — NPS ${Math.round(i.nps_score)} — $${Math.round(i.potential_expansion_arr_usd/1000)}k expansion potential — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[sales-expansion-revenue-signal-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tuc=0,tpg=0,ten=0,tre=0,tcomp=0,tarr=0,gc=0,ec=0;
    for (const a of accounts) {
      rc[a.expansion_risk]=(rc[a.expansion_risk]||0)+1; pc[a.expansion_pattern]=(pc[a.expansion_pattern]||0)+1;
      sc[a.expansion_severity]=(sc[a.expansion_severity]||0)+1; ac[a.recommended_action]=(ac[a.recommended_action]||0)+1;
      tuc+=a.usage_ceiling_score; tpg+=a.product_gap_score; ten+=a.engagement_score; tre+=a.relationship_score;
      tcomp+=a.expansion_composite; tarr+=a.estimated_expansion_arr_usd;
      if (a.has_expansion_signal) gc++; if (a.requires_executive_engagement) ec++;
    }
    const n = accounts.length;
    return sealResponse(NextResponse.json(sealResponse({ accounts, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_expansion_composite: Math.round(tcomp/n*10)/10,
      expansion_signal_count: gc, executive_engagement_count: ec,
      avg_usage_ceiling_score: Math.round(tuc/n*10)/10,
      avg_product_gap_score: Math.round(tpg/n*10)/10,
      avg_engagement_score: Math.round(ten/n*10)/10,
      avg_relationship_score: Math.round(tre/n*10)/10,
      total_estimated_expansion_arr_usd: Math.round(tarr*100)/100,
    }} as Record<string,unknown>)));
  }
  return sealResponse(NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-expansion-revenue-signal-engine`, { next: { revalidate: 30 } })).json()));
}
