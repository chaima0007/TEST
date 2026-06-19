import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"QR-001", region:"EMEA",      evaluation_period_id:"Q2-2026", quota_attainment_pct:1.28, forecast_accuracy_pct:0.38, commit_vs_actual_ratio:0.62, sandbagging_index:0.72, overcommit_frequency_pct:0.12, late_quarter_close_rate_pct:0.71, pipeline_to_quota_ratio:4.2, early_commit_accuracy_pct:0.28, mid_commit_accuracy_pct:0.41, late_commit_accuracy_pct:0.88, upside_conversion_rate_pct:0.72, commit_revision_frequency:2, pulled_in_deal_rate_pct:0.38, pushed_out_deal_rate_pct:0.08, quota_to_territory_fit_score:0.72, mgr_trust_in_forecast_score:0.28, peer_comparison_delta_pct:0.18, consecutive_miss_streak:0, voluntary_quota_increase_pct:0.05 },
  { rep_id:"QR-002", region:"APAC",      evaluation_period_id:"Q2-2026", quota_attainment_pct:0.71, forecast_accuracy_pct:0.28, commit_vs_actual_ratio:1.42, sandbagging_index:0.08, overcommit_frequency_pct:0.68, late_quarter_close_rate_pct:0.18, pipeline_to_quota_ratio:1.8, early_commit_accuracy_pct:0.38, mid_commit_accuracy_pct:0.31, late_commit_accuracy_pct:0.22, upside_conversion_rate_pct:0.12, commit_revision_frequency:3, pulled_in_deal_rate_pct:0.08, pushed_out_deal_rate_pct:0.32, quota_to_territory_fit_score:0.48, mgr_trust_in_forecast_score:0.22, peer_comparison_delta_pct:-0.28, consecutive_miss_streak:3, voluntary_quota_increase_pct:0.22 },
  { rep_id:"QR-003", region:"NAMER",     evaluation_period_id:"Q2-2026", quota_attainment_pct:0.98, forecast_accuracy_pct:0.88, commit_vs_actual_ratio:0.96, sandbagging_index:0.12, overcommit_frequency_pct:0.08, late_quarter_close_rate_pct:0.22, pipeline_to_quota_ratio:3.1, early_commit_accuracy_pct:0.85, mid_commit_accuracy_pct:0.88, late_commit_accuracy_pct:0.91, upside_conversion_rate_pct:0.62, commit_revision_frequency:1, pulled_in_deal_rate_pct:0.08, pushed_out_deal_rate_pct:0.06, quota_to_territory_fit_score:0.88, mgr_trust_in_forecast_score:0.91, peer_comparison_delta_pct:0.05, consecutive_miss_streak:0, voluntary_quota_increase_pct:0.08 },
  { rep_id:"QR-004", region:"LATAM",     evaluation_period_id:"Q2-2026", quota_attainment_pct:0.88, forecast_accuracy_pct:0.42, commit_vs_actual_ratio:0.88, sandbagging_index:0.35, overcommit_frequency_pct:0.28, late_quarter_close_rate_pct:0.58, pipeline_to_quota_ratio:2.8, early_commit_accuracy_pct:0.31, mid_commit_accuracy_pct:0.44, late_commit_accuracy_pct:0.71, upside_conversion_rate_pct:0.44, commit_revision_frequency:5, pulled_in_deal_rate_pct:0.22, pushed_out_deal_rate_pct:0.18, quota_to_territory_fit_score:0.58, mgr_trust_in_forecast_score:0.48, peer_comparison_delta_pct:-0.08, consecutive_miss_streak:1, voluntary_quota_increase_pct:0.04 },
  { rep_id:"QR-005", region:"EMEA",      evaluation_period_id:"Q2-2026", quota_attainment_pct:0.58, forecast_accuracy_pct:0.22, commit_vs_actual_ratio:1.58, sandbagging_index:0.05, overcommit_frequency_pct:0.82, late_quarter_close_rate_pct:0.12, pipeline_to_quota_ratio:1.4, early_commit_accuracy_pct:0.28, mid_commit_accuracy_pct:0.22, late_commit_accuracy_pct:0.18, upside_conversion_rate_pct:0.08, commit_revision_frequency:4, pulled_in_deal_rate_pct:0.12, pushed_out_deal_rate_pct:0.38, quota_to_territory_fit_score:0.38, mgr_trust_in_forecast_score:0.18, peer_comparison_delta_pct:-0.42, consecutive_miss_streak:4, voluntary_quota_increase_pct:0.28 },
  { rep_id:"QR-006", region:"MEA",       evaluation_period_id:"Q2-2026", quota_attainment_pct:1.08, forecast_accuracy_pct:0.52, commit_vs_actual_ratio:0.78, sandbagging_index:0.48, overcommit_frequency_pct:0.18, late_quarter_close_rate_pct:0.62, pipeline_to_quota_ratio:3.8, early_commit_accuracy_pct:0.22, mid_commit_accuracy_pct:0.55, late_commit_accuracy_pct:0.82, upside_conversion_rate_pct:0.58, commit_revision_frequency:3, pulled_in_deal_rate_pct:0.42, pushed_out_deal_rate_pct:0.11, quota_to_territory_fit_score:0.65, mgr_trust_in_forecast_score:0.42, peer_comparison_delta_pct:0.12, consecutive_miss_streak:0, voluntary_quota_increase_pct:0.02 },
  { rep_id:"QR-007", region:"APAC",      evaluation_period_id:"Q2-2026", quota_attainment_pct:0.82, forecast_accuracy_pct:0.48, commit_vs_actual_ratio:0.92, sandbagging_index:0.22, overcommit_frequency_pct:0.22, late_quarter_close_rate_pct:0.38, pipeline_to_quota_ratio:2.4, early_commit_accuracy_pct:0.55, mid_commit_accuracy_pct:0.51, late_commit_accuracy_pct:0.62, upside_conversion_rate_pct:0.38, commit_revision_frequency:6, pulled_in_deal_rate_pct:0.28, pushed_out_deal_rate_pct:0.28, quota_to_territory_fit_score:0.55, mgr_trust_in_forecast_score:0.55, peer_comparison_delta_pct:-0.05, consecutive_miss_streak:2, voluntary_quota_increase_pct:0.06 },
  { rep_id:"QR-008", region:"NAMER",     evaluation_period_id:"Q2-2026", quota_attainment_pct:1.18, forecast_accuracy_pct:0.72, commit_vs_actual_ratio:0.88, sandbagging_index:0.32, overcommit_frequency_pct:0.12, late_quarter_close_rate_pct:0.42, pipeline_to_quota_ratio:3.5, early_commit_accuracy_pct:0.68, mid_commit_accuracy_pct:0.72, late_commit_accuracy_pct:0.78, upside_conversion_rate_pct:0.55, commit_revision_frequency:2, pulled_in_deal_rate_pct:0.15, pushed_out_deal_rate_pct:0.08, quota_to_territory_fit_score:0.78, mgr_trust_in_forecast_score:0.75, peer_comparison_delta_pct:0.08, consecutive_miss_streak:0, voluntary_quota_increase_pct:0.10 },
];

function sbScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.sandbagging_index >= 0.65) s += 40;
  else if (inp.sandbagging_index >= 0.45) s += 22;
  else if (inp.sandbagging_index >= 0.25) s += 8;
  if      (inp.late_quarter_close_rate_pct >= 0.60) s += 35;
  else if (inp.late_quarter_close_rate_pct >= 0.40) s += 18;
  if      (inp.commit_vs_actual_ratio <= 0.70) s += 25;
  else if (inp.commit_vs_actual_ratio <= 0.85) s += 12;
  return Math.min(s, 100);
}
function ocScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.overcommit_frequency_pct >= 0.55) s += 40;
  else if (inp.overcommit_frequency_pct >= 0.35) s += 22;
  else if (inp.overcommit_frequency_pct >= 0.20) s += 8;
  if      (inp.consecutive_miss_streak >= 3) s += 35;
  else if (inp.consecutive_miss_streak >= 2) s += 18;
  if      (inp.mgr_trust_in_forecast_score <= 0.35) s += 25;
  else if (inp.mgr_trust_in_forecast_score <= 0.55) s += 12;
  return Math.min(s, 100);
}
function calScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.forecast_accuracy_pct <= 0.40) s += 40;
  else if (inp.forecast_accuracy_pct <= 0.60) s += 22;
  else if (inp.forecast_accuracy_pct <= 0.75) s += 8;
  if      (inp.early_commit_accuracy_pct <= 0.35) s += 30;
  else if (inp.early_commit_accuracy_pct <= 0.55) s += 15;
  if      (inp.mid_commit_accuracy_pct <= 0.50) s += 20;
  else if (inp.mid_commit_accuracy_pct <= 0.70) s += 10;
  if      (inp.late_commit_accuracy_pct <= 0.65) s += 10;
  return Math.min(s, 100);
}
function volScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.commit_revision_frequency >= 5) s += 40;
  else if (inp.commit_revision_frequency >= 3) s += 22;
  else if (inp.commit_revision_frequency >= 2) s += 8;
  if      (inp.pulled_in_deal_rate_pct >= 0.35) s += 35;
  else if (inp.pulled_in_deal_rate_pct >= 0.20) s += 18;
  if      (inp.pushed_out_deal_rate_pct >= 0.30) s += 25;
  else if (inp.pushed_out_deal_rate_pct >= 0.15) s += 12;
  return Math.min(s, 100);
}
function composite(sb: number, oc: number, cal: number, vol: number): number {
  return Math.min(Math.round((sb*0.30 + oc*0.25 + cal*0.30 + vol*0.15)*100)/100, 100);
}
function pattern(inp: typeof MOCK_REPS[0]): string {
  if (inp.sandbagging_index >= 0.50 && inp.late_quarter_close_rate_pct >= 0.45) return "sandbagging";
  if (inp.overcommit_frequency_pct >= 0.50 && inp.consecutive_miss_streak >= 2) return "overcommitting";
  if (inp.commit_revision_frequency >= 4 && inp.forecast_accuracy_pct <= 0.55) return "volatile_committor";
  if (inp.late_quarter_close_rate_pct >= 0.55 && inp.early_commit_accuracy_pct <= 0.40) return "late_surge";
  if (inp.pulled_in_deal_rate_pct >= 0.30 && inp.pushed_out_deal_rate_pct >= 0.25) return "forecast_manipulator";
  return "none";
}
function risk(c: number): string {
  if (c >= 60) return "critical";
  if (c >= 40) return "high";
  if (c >= 20) return "moderate";
  return "low";
}
function severity(c: number): string {
  if (c >= 60) return "manipulated";
  if (c >= 40) return "distorted";
  if (c >= 20) return "drifting";
  return "calibrated";
}
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "sandbagging" || p === "forecast_manipulator") return "executive_quota_escalation";
    return "quota_reset_intervention";
  }
  if (r === "high") {
    if (p === "sandbagging") return "manager_quota_review";
    if (p === "overcommitting") return "commit_accuracy_coaching";
    if (p === "volatile_committor") return "forecast_calibration_coaching";
    if (p === "late_surge") return "forecast_calibration_coaching";
    if (p === "forecast_manipulator") return "manager_quota_review";
    return "commit_accuracy_coaching";
  }
  if (r === "moderate") return "quota_check_in";
  return "no_action";
}
function signal(inp: typeof MOCK_REPS[0], pat: string, comp: number): string {
  if (comp < 20) return "Quota commitment well-calibrated — forecast accuracy, sandbagging index, and commit accuracy within benchmarks";
  const labels: Record<string,string> = {
    sandbagging: "Sandbagging", overcommitting: "Overcommitting",
    volatile_committor: "Volatile committor", late_surge: "Late surge", forecast_manipulator: "Forecast manipulator"
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(inp.forecast_accuracy_pct*100)}% forecast accuracy — sandbagging index ${inp.sandbagging_index.toFixed(2)} — ${inp.consecutive_miss_streak} miss streak — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(inp => {
      const sb  = sbScore(inp);
      const oc  = ocScore(inp);
      const cal = calScore(inp);
      const vol = volScore(inp);
      const comp = composite(sb, oc, cal, vol);
      const pat  = pattern(inp);
      const r    = risk(comp);
      const sev  = severity(comp);
      const act  = action(r, pat);
      const distortion = (comp/100) * Math.abs(1.0 - inp.commit_vs_actual_ratio) * inp.pipeline_to_quota_ratio * 100000;
      return {
        rep_id: inp.rep_id, region: inp.region,
        quota_risk: r, quota_pattern: pat, quota_severity: sev, recommended_action: act,
        sandbagging_score: sb, overcommit_score: oc, calibration_score: cal, volatility_score: vol,
        quota_composite: comp,
        has_quota_gap: comp >= 40 || inp.forecast_accuracy_pct <= 0.60 || inp.consecutive_miss_streak >= 2,
        requires_quota_intervention: comp >= 25 || inp.sandbagging_index >= 0.40 || inp.mgr_trust_in_forecast_score <= 0.50,
        estimated_quota_distortion_usd: Math.round(distortion * 100) / 100,
        quota_signal: signal(inp, pat, comp),
      };
    });

    const risk_counts: Record<string,number> = {};
    const pattern_counts: Record<string,number> = {};
    const severity_counts: Record<string,number> = {};
    const action_counts: Record<string,number> = {};
    let total_comp=0, total_sb=0, total_oc=0, total_cal=0, total_vol=0, total_dist=0;
    let gap_count=0, intervention_count=0;
    for (const r of reps) {
      risk_counts[r.quota_risk] = (risk_counts[r.quota_risk]||0)+1;
      pattern_counts[r.quota_pattern] = (pattern_counts[r.quota_pattern]||0)+1;
      severity_counts[r.quota_severity] = (severity_counts[r.quota_severity]||0)+1;
      action_counts[r.recommended_action] = (action_counts[r.recommended_action]||0)+1;
      total_comp += r.quota_composite;
      total_sb   += r.sandbagging_score;
      total_oc   += r.overcommit_score;
      total_cal  += r.calibration_score;
      total_vol  += r.volatility_score;
      total_dist += r.estimated_quota_distortion_usd;
      if (r.has_quota_gap) gap_count++;
      if (r.requires_quota_intervention) intervention_count++;
    }
    const n = reps.length;
    const summary = {
      total: n, risk_counts, pattern_counts, severity_counts, action_counts,
      avg_quota_composite: Math.round(total_comp/n*10)/10,
      quota_gap_count: gap_count, intervention_count,
      avg_sandbagging_score: Math.round(total_sb/n*10)/10,
      avg_overcommit_score: Math.round(total_oc/n*10)/10,
      avg_calibration_score: Math.round(total_cal/n*10)/10,
      avg_volatility_score: Math.round(total_vol/n*10)/10,
      total_estimated_quota_distortion_usd: Math.round(total_dist*100)/100,
    };
    return NextResponse.json(sealResponse({ reps, summary } as Record<string,unknown>));
  }

  const res = await fetch(`${process.env.SWARM_API_URL}/sales-quota-sandbag-overcommit-intelligence-engine`);
  const data = await res.json();
  return NextResponse.json(data);
}
