import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"TI-001", region:"EMEA",  evaluation_period_id:"Q2-2026", accounts_per_rep_vs_benchmark:2.1, revenue_per_account_vs_benchmark:0.42, whitespace_accounts_untouched_pct:0.72, renewal_coverage_rate_pct:0.35, territory_quota_vs_capacity_ratio:1.72, active_accounts_pct:0.22, avg_travel_time_per_call_hours:3.5, geographic_concentration_score:0.28, icp_account_coverage_pct:0.18, new_logo_territory_penetration_pct:0.06, competitive_displacement_coverage:0.08, account_scoring_adoption_rate_pct:0.15, stale_account_rate_pct:0.62, multi_product_territory_pct:0.12, territory_nps_avg:-0.22, expansion_opportunity_capture_pct:0.12, rep_tenure_territory_months:6, total_accounts_in_territory:72, avg_arr_per_account_usd:88000 },
  { rep_id:"TI-002", region:"APAC",  evaluation_period_id:"Q2-2026", accounts_per_rep_vs_benchmark:0.85, revenue_per_account_vs_benchmark:1.22, whitespace_accounts_untouched_pct:0.18, renewal_coverage_rate_pct:0.92, territory_quota_vs_capacity_ratio:0.88, active_accounts_pct:0.88, avg_travel_time_per_call_hours:0.8, geographic_concentration_score:0.72, icp_account_coverage_pct:0.82, new_logo_territory_penetration_pct:0.32, competitive_displacement_coverage:0.42, account_scoring_adoption_rate_pct:0.88, stale_account_rate_pct:0.08, multi_product_territory_pct:0.62, territory_nps_avg:0.42, expansion_opportunity_capture_pct:0.72, rep_tenure_territory_months:24, total_accounts_in_territory:45, avg_arr_per_account_usd:115000 },
  { rep_id:"TI-003", region:"NAMER", evaluation_period_id:"Q2-2026", accounts_per_rep_vs_benchmark:1.25, revenue_per_account_vs_benchmark:0.78, whitespace_accounts_untouched_pct:0.42, renewal_coverage_rate_pct:0.68, territory_quota_vs_capacity_ratio:1.18, active_accounts_pct:0.58, avg_travel_time_per_call_hours:1.8, geographic_concentration_score:0.45, icp_account_coverage_pct:0.52, new_logo_territory_penetration_pct:0.18, competitive_displacement_coverage:0.22, account_scoring_adoption_rate_pct:0.55, stale_account_rate_pct:0.28, multi_product_territory_pct:0.38, territory_nps_avg:0.08, expansion_opportunity_capture_pct:0.42, rep_tenure_territory_months:14, total_accounts_in_territory:58, avg_arr_per_account_usd:96000 },
  { rep_id:"TI-004", region:"LATAM", evaluation_period_id:"Q2-2026", accounts_per_rep_vs_benchmark:0.38, revenue_per_account_vs_benchmark:0.35, whitespace_accounts_untouched_pct:0.68, renewal_coverage_rate_pct:0.28, territory_quota_vs_capacity_ratio:0.62, active_accounts_pct:0.32, avg_travel_time_per_call_hours:2.2, geographic_concentration_score:0.18, icp_account_coverage_pct:0.22, new_logo_territory_penetration_pct:0.08, competitive_displacement_coverage:0.05, account_scoring_adoption_rate_pct:0.18, stale_account_rate_pct:0.55, multi_product_territory_pct:0.08, territory_nps_avg:-0.12, expansion_opportunity_capture_pct:0.15, rep_tenure_territory_months:8, total_accounts_in_territory:28, avg_arr_per_account_usd:102000 },
  { rep_id:"TI-005", region:"EMEA",  evaluation_period_id:"Q2-2026", accounts_per_rep_vs_benchmark:1.0, revenue_per_account_vs_benchmark:1.05, whitespace_accounts_untouched_pct:0.22, renewal_coverage_rate_pct:0.88, territory_quota_vs_capacity_ratio:0.95, active_accounts_pct:0.82, avg_travel_time_per_call_hours:1.0, geographic_concentration_score:0.62, icp_account_coverage_pct:0.72, new_logo_territory_penetration_pct:0.28, competitive_displacement_coverage:0.35, account_scoring_adoption_rate_pct:0.78, stale_account_rate_pct:0.12, multi_product_territory_pct:0.55, territory_nps_avg:0.35, expansion_opportunity_capture_pct:0.62, rep_tenure_territory_months:20, total_accounts_in_territory:52, avg_arr_per_account_usd:108000 },
  { rep_id:"TI-006", region:"MEA",   evaluation_period_id:"Q2-2026", accounts_per_rep_vs_benchmark:2.45, revenue_per_account_vs_benchmark:0.28, whitespace_accounts_untouched_pct:0.78, renewal_coverage_rate_pct:0.22, territory_quota_vs_capacity_ratio:1.92, active_accounts_pct:0.15, avg_travel_time_per_call_hours:4.2, geographic_concentration_score:0.12, icp_account_coverage_pct:0.12, new_logo_territory_penetration_pct:0.04, competitive_displacement_coverage:0.04, account_scoring_adoption_rate_pct:0.08, stale_account_rate_pct:0.72, multi_product_territory_pct:0.06, territory_nps_avg:-0.38, expansion_opportunity_capture_pct:0.08, rep_tenure_territory_months:4, total_accounts_in_territory:88, avg_arr_per_account_usd:75000 },
  { rep_id:"TI-007", region:"APAC",  evaluation_period_id:"Q2-2026", accounts_per_rep_vs_benchmark:0.92, revenue_per_account_vs_benchmark:0.95, whitespace_accounts_untouched_pct:0.30, renewal_coverage_rate_pct:0.80, territory_quota_vs_capacity_ratio:0.98, active_accounts_pct:0.75, avg_travel_time_per_call_hours:1.2, geographic_concentration_score:0.55, icp_account_coverage_pct:0.65, new_logo_territory_penetration_pct:0.22, competitive_displacement_coverage:0.28, account_scoring_adoption_rate_pct:0.68, stale_account_rate_pct:0.18, multi_product_territory_pct:0.48, territory_nps_avg:0.22, expansion_opportunity_capture_pct:0.55, rep_tenure_territory_months:18, total_accounts_in_territory:48, avg_arr_per_account_usd:98000 },
  { rep_id:"TI-008", region:"NAMER", evaluation_period_id:"Q2-2026", accounts_per_rep_vs_benchmark:1.55, revenue_per_account_vs_benchmark:0.58, whitespace_accounts_untouched_pct:0.55, renewal_coverage_rate_pct:0.52, territory_quota_vs_capacity_ratio:1.38, active_accounts_pct:0.42, avg_travel_time_per_call_hours:2.5, geographic_concentration_score:0.32, icp_account_coverage_pct:0.38, new_logo_territory_penetration_pct:0.12, competitive_displacement_coverage:0.15, account_scoring_adoption_rate_pct:0.35, stale_account_rate_pct:0.42, multi_product_territory_pct:0.22, territory_nps_avg:-0.05, expansion_opportunity_capture_pct:0.28, rep_tenure_territory_months:10, total_accounts_in_territory:65, avg_arr_per_account_usd:92000 },
];

type Rep = typeof MOCK_REPS[0];

function loadScore(i: Rep): number {
  let s = 0;
  if      (i.territory_quota_vs_capacity_ratio >= 1.60) s += 40; else if (i.territory_quota_vs_capacity_ratio >= 1.30) s += 22; else if (i.territory_quota_vs_capacity_ratio >= 1.10) s += 8;
  if      (i.accounts_per_rep_vs_benchmark     >= 1.80) s += 35; else if (i.accounts_per_rep_vs_benchmark >= 1.40) s += 18;
  if      (i.avg_travel_time_per_call_hours    >= 3.0)  s += 25; else if (i.avg_travel_time_per_call_hours >= 1.5) s += 12;
  return Math.min(s, 100);
}
function coverageScore(i: Rep): number {
  let s = 0;
  if      (i.active_accounts_pct       <= 0.30) s += 45; else if (i.active_accounts_pct <= 0.55) s += 25; else if (i.active_accounts_pct <= 0.75) s += 10;
  if      (i.stale_account_rate_pct    >= 0.50) s += 30; else if (i.stale_account_rate_pct >= 0.28) s += 15;
  if      (i.renewal_coverage_rate_pct <= 0.50) s += 25; else if (i.renewal_coverage_rate_pct <= 0.75) s += 12;
  return Math.min(s, 100);
}
function penetrationScore(i: Rep): number {
  let s = 0;
  if      (i.whitespace_accounts_untouched_pct   >= 0.65) s += 40; else if (i.whitespace_accounts_untouched_pct >= 0.40) s += 22; else if (i.whitespace_accounts_untouched_pct >= 0.20) s += 8;
  if      (i.icp_account_coverage_pct            <= 0.25) s += 35; else if (i.icp_account_coverage_pct <= 0.50) s += 18;
  if      (i.new_logo_territory_penetration_pct  <= 0.10) s += 25; else if (i.new_logo_territory_penetration_pct <= 0.20) s += 12;
  return Math.min(s, 100);
}
function efficiencyScore(i: Rep): number {
  let s = 0;
  if      (i.revenue_per_account_vs_benchmark    <= 0.40) s += 45; else if (i.revenue_per_account_vs_benchmark <= 0.70) s += 25; else if (i.revenue_per_account_vs_benchmark <= 0.90) s += 10;
  if      (i.expansion_opportunity_capture_pct   <= 0.20) s += 30; else if (i.expansion_opportunity_capture_pct <= 0.45) s += 15;
  if      (i.account_scoring_adoption_rate_pct   <= 0.20) s += 25; else if (i.account_scoring_adoption_rate_pct <= 0.50) s += 12;
  return Math.min(s, 100);
}
function composite(lo: number, co: number, pe: number, ef: number): number {
  return Math.min(Math.round((lo * 0.25 + co * 0.30 + pe * 0.25 + ef * 0.20) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.territory_quota_vs_capacity_ratio >= 1.50 && i.accounts_per_rep_vs_benchmark >= 1.60) return "overloaded_rep";
  if (i.accounts_per_rep_vs_benchmark <= 0.50 && i.whitespace_accounts_untouched_pct >= 0.60) return "starved_territory";
  if (i.whitespace_accounts_untouched_pct >= 0.65 && i.icp_account_coverage_pct <= 0.25) return "whitespace_blind";
  if (i.active_accounts_pct <= 0.30 && i.stale_account_rate_pct >= 0.50) return "coverage_ghost";
  if (i.renewal_coverage_rate_pct <= 0.45 && i.expansion_opportunity_capture_pct <= 0.20) return "renewal_neglect";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "imbalanced"; if (c >= 20) return "drifting"; return "balanced"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "overloaded_rep" || p === "starved_territory") return "territory_redesign_escalation"; return "account_redistribution_review"; }
  if (r === "high") { if (p === "overloaded_rep") return "account_redistribution_review"; if (p === "starved_territory") return "coverage_model_reassignment"; if (p === "whitespace_blind") return "whitespace_activation_plan"; if (p === "coverage_ghost") return "account_redistribution_review"; if (p === "renewal_neglect") return "renewal_coverage_remediation"; return "territory_health_check"; }
  if (r === "moderate") return "territory_health_check";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Territory balance healthy — coverage, penetration, load, and efficiency within benchmark targets";
  const labels: Record<string,string> = { overloaded_rep:"Overloaded rep", starved_territory:"Starved territory", whitespace_blind:"Whitespace blind", coverage_ghost:"Coverage ghost", renewal_neglect:"Renewal neglect" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(i.active_accounts_pct*100)}% accounts active — ${Math.round(i.whitespace_accounts_untouched_pct*100)}% whitespace untouched — ${Math.round(i.renewal_coverage_rate_pct*100)}% renewal coverage — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[sales-territory-imbalance-coverage-gap-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tlo=0, tco=0, tpe=0, tef=0, tcomp=0, tur=0, gc=0, ic=0;
    for (const r of reps) {
      rc[r.territory_risk]=(rc[r.territory_risk]||0)+1; pc[r.territory_pattern]=(pc[r.territory_pattern]||0)+1;
      sc[r.territory_severity]=(sc[r.territory_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      tlo+=r.load_score; tco+=r.coverage_score; tpe+=r.penetration_score; tef+=r.efficiency_score;
      tcomp+=r.territory_composite; tur+=r.estimated_uncaptured_revenue_usd;
      if (r.has_territory_gap) gc++; if (r.requires_territory_intervention) ic++;
    }
    const n = reps.length;
    return sealResponse(NextResponse.json(sealResponse({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_territory_composite: Math.round(tcomp/n*10)/10,
      territory_gap_count: gc, intervention_count: ic,
      avg_load_score: Math.round(tlo/n*10)/10,
      avg_coverage_score: Math.round(tco/n*10)/10,
      avg_penetration_score: Math.round(tpe/n*10)/10,
      avg_efficiency_score: Math.round(tef/n*10)/10,
      total_estimated_uncaptured_revenue_usd: Math.round(tur*100)/100,
    }} as Record<string,unknown>)));
  }
  return sealResponse(NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-territory-imbalance-coverage-gap-engine`, { next: { revalidate: 30 } })).json()));
}
