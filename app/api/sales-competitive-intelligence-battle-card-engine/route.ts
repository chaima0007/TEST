import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"CI-001", region:"EMEA",  evaluation_period_id:"Q2-2026", competitive_win_rate_pct:0.18, competitive_loss_rate_pct:0.72, battle_card_usage_rate_pct:0.12, competitive_mention_early_rate_pct:0.15, price_concession_vs_competitor_pct:0.62, feature_comparison_loss_rate_pct:0.52, competitive_deal_cycle_delta_days:28, no_competitive_intel_rate_pct:0.52, competitive_stakeholder_loss_pct:0.58, single_competitor_thread_rate_pct:0.65, late_competitor_discovery_rate_pct:0.58, displacement_win_rate_pct:0.12, proof_of_concept_win_rate_pct:0.18, reference_customer_usage_pct:0.10, total_competitive_deals:11, avg_deal_value_usd:92000, competitive_intensity_score:0.78, head_to_head_calls_per_deal:0.2, post_loss_debrief_rate_pct:0.12, total_deals_evaluated:14 },
  { rep_id:"CI-002", region:"APAC",  evaluation_period_id:"Q2-2026", competitive_win_rate_pct:0.72, competitive_loss_rate_pct:0.18, battle_card_usage_rate_pct:0.88, competitive_mention_early_rate_pct:0.78, price_concession_vs_competitor_pct:0.10, feature_comparison_loss_rate_pct:0.08, competitive_deal_cycle_delta_days:5, no_competitive_intel_rate_pct:0.05, competitive_stakeholder_loss_pct:0.10, single_competitor_thread_rate_pct:0.12, late_competitor_discovery_rate_pct:0.05, displacement_win_rate_pct:0.65, proof_of_concept_win_rate_pct:0.72, reference_customer_usage_pct:0.68, total_competitive_deals:14, avg_deal_value_usd:75000, competitive_intensity_score:0.72, head_to_head_calls_per_deal:2.8, post_loss_debrief_rate_pct:0.88, total_deals_evaluated:18 },
  { rep_id:"CI-003", region:"NAMER", evaluation_period_id:"Q2-2026", competitive_win_rate_pct:0.38, competitive_loss_rate_pct:0.45, battle_card_usage_rate_pct:0.52, competitive_mention_early_rate_pct:0.45, price_concession_vs_competitor_pct:0.32, feature_comparison_loss_rate_pct:0.28, competitive_deal_cycle_delta_days:14, no_competitive_intel_rate_pct:0.22, competitive_stakeholder_loss_pct:0.35, single_competitor_thread_rate_pct:0.38, late_competitor_discovery_rate_pct:0.28, displacement_win_rate_pct:0.38, proof_of_concept_win_rate_pct:0.42, reference_customer_usage_pct:0.38, total_competitive_deals:12, avg_deal_value_usd:68000, competitive_intensity_score:0.65, head_to_head_calls_per_deal:1.2, post_loss_debrief_rate_pct:0.48, total_deals_evaluated:15 },
  { rep_id:"CI-004", region:"LATAM", evaluation_period_id:"Q2-2026", competitive_win_rate_pct:0.22, competitive_loss_rate_pct:0.65, battle_card_usage_rate_pct:0.22, competitive_mention_early_rate_pct:0.18, price_concession_vs_competitor_pct:0.58, feature_comparison_loss_rate_pct:0.48, competitive_deal_cycle_delta_days:22, no_competitive_intel_rate_pct:0.45, competitive_stakeholder_loss_pct:0.52, single_competitor_thread_rate_pct:0.62, late_competitor_discovery_rate_pct:0.48, displacement_win_rate_pct:0.15, proof_of_concept_win_rate_pct:0.22, reference_customer_usage_pct:0.12, total_competitive_deals:9, avg_deal_value_usd:82000, competitive_intensity_score:0.72, head_to_head_calls_per_deal:0.3, post_loss_debrief_rate_pct:0.18, total_deals_evaluated:12 },
  { rep_id:"CI-005", region:"EMEA",  evaluation_period_id:"Q2-2026", competitive_win_rate_pct:0.58, competitive_loss_rate_pct:0.28, battle_card_usage_rate_pct:0.75, competitive_mention_early_rate_pct:0.65, price_concession_vs_competitor_pct:0.18, feature_comparison_loss_rate_pct:0.15, competitive_deal_cycle_delta_days:8, no_competitive_intel_rate_pct:0.10, competitive_stakeholder_loss_pct:0.18, single_competitor_thread_rate_pct:0.22, late_competitor_discovery_rate_pct:0.12, displacement_win_rate_pct:0.52, proof_of_concept_win_rate_pct:0.62, reference_customer_usage_pct:0.55, total_competitive_deals:13, avg_deal_value_usd:88000, competitive_intensity_score:0.68, head_to_head_calls_per_deal:2.2, post_loss_debrief_rate_pct:0.75, total_deals_evaluated:17 },
  { rep_id:"CI-006", region:"MEA",   evaluation_period_id:"Q2-2026", competitive_win_rate_pct:0.12, competitive_loss_rate_pct:0.78, battle_card_usage_rate_pct:0.08, competitive_mention_early_rate_pct:0.10, price_concession_vs_competitor_pct:0.68, feature_comparison_loss_rate_pct:0.58, competitive_deal_cycle_delta_days:32, no_competitive_intel_rate_pct:0.58, competitive_stakeholder_loss_pct:0.65, single_competitor_thread_rate_pct:0.72, late_competitor_discovery_rate_pct:0.65, displacement_win_rate_pct:0.08, proof_of_concept_win_rate_pct:0.12, reference_customer_usage_pct:0.06, total_competitive_deals:10, avg_deal_value_usd:62000, competitive_intensity_score:0.82, head_to_head_calls_per_deal:0.1, post_loss_debrief_rate_pct:0.08, total_deals_evaluated:13 },
  { rep_id:"CI-007", region:"APAC",  evaluation_period_id:"Q2-2026", competitive_win_rate_pct:0.48, competitive_loss_rate_pct:0.35, battle_card_usage_rate_pct:0.62, competitive_mention_early_rate_pct:0.55, price_concession_vs_competitor_pct:0.25, feature_comparison_loss_rate_pct:0.22, competitive_deal_cycle_delta_days:11, no_competitive_intel_rate_pct:0.15, competitive_stakeholder_loss_pct:0.25, single_competitor_thread_rate_pct:0.32, late_competitor_discovery_rate_pct:0.18, displacement_win_rate_pct:0.45, proof_of_concept_win_rate_pct:0.52, reference_customer_usage_pct:0.45, total_competitive_deals:11, avg_deal_value_usd:72000, competitive_intensity_score:0.62, head_to_head_calls_per_deal:1.8, post_loss_debrief_rate_pct:0.62, total_deals_evaluated:14 },
  { rep_id:"CI-008", region:"NAMER", evaluation_period_id:"Q2-2026", competitive_win_rate_pct:0.28, competitive_loss_rate_pct:0.55, battle_card_usage_rate_pct:0.35, competitive_mention_early_rate_pct:0.32, price_concession_vs_competitor_pct:0.45, feature_comparison_loss_rate_pct:0.38, competitive_deal_cycle_delta_days:18, no_competitive_intel_rate_pct:0.32, competitive_stakeholder_loss_pct:0.42, single_competitor_thread_rate_pct:0.48, late_competitor_discovery_rate_pct:0.35, displacement_win_rate_pct:0.25, proof_of_concept_win_rate_pct:0.32, reference_customer_usage_pct:0.25, total_competitive_deals:10, avg_deal_value_usd:78000, competitive_intensity_score:0.70, head_to_head_calls_per_deal:0.8, post_loss_debrief_rate_pct:0.35, total_deals_evaluated:13 },
];

type Rep = typeof MOCK_REPS[0];

function preparednessScore(i: Rep): number {
  let s = 0;
  if      (i.battle_card_usage_rate_pct    <= 0.25) s += 40; else if (i.battle_card_usage_rate_pct <= 0.50) s += 22; else if (i.battle_card_usage_rate_pct <= 0.70) s += 8;
  if      (i.no_competitive_intel_rate_pct >= 0.40) s += 35; else if (i.no_competitive_intel_rate_pct >= 0.22) s += 18;
  if      (i.post_loss_debrief_rate_pct    <= 0.20) s += 25; else if (i.post_loss_debrief_rate_pct <= 0.45) s += 12;
  return Math.min(s, 100);
}
function executionScore(i: Rep): number {
  let s = 0;
  if      (i.competitive_win_rate_pct          <= 0.25) s += 45; else if (i.competitive_win_rate_pct <= 0.45) s += 25; else if (i.competitive_win_rate_pct <= 0.60) s += 10;
  if      (i.price_concession_vs_competitor_pct >= 0.50) s += 30; else if (i.price_concession_vs_competitor_pct >= 0.28) s += 15;
  if      (i.competitive_deal_cycle_delta_days  >= 25) s += 25; else if (i.competitive_deal_cycle_delta_days >= 12) s += 12;
  return Math.min(s, 100);
}
function intelligenceScore(i: Rep): number {
  let s = 0;
  if      (i.late_competitor_discovery_rate_pct >= 0.45) s += 40; else if (i.late_competitor_discovery_rate_pct >= 0.25) s += 22; else if (i.late_competitor_discovery_rate_pct >= 0.12) s += 8;
  if      (i.competitive_mention_early_rate_pct <= 0.25) s += 35; else if (i.competitive_mention_early_rate_pct <= 0.50) s += 18;
  if      (i.head_to_head_calls_per_deal        <= 0.5) s += 25; else if (i.head_to_head_calls_per_deal <= 1.2) s += 12;
  return Math.min(s, 100);
}
function positioningScore(i: Rep): number {
  let s = 0;
  if      (i.feature_comparison_loss_rate_pct  >= 0.45) s += 40; else if (i.feature_comparison_loss_rate_pct >= 0.25) s += 22; else if (i.feature_comparison_loss_rate_pct >= 0.12) s += 8;
  if      (i.single_competitor_thread_rate_pct >= 0.60) s += 35; else if (i.single_competitor_thread_rate_pct >= 0.35) s += 18;
  if      (i.reference_customer_usage_pct      <= 0.15) s += 25; else if (i.reference_customer_usage_pct <= 0.35) s += 12;
  return Math.min(s, 100);
}
function composite(pr: number, ex: number, int_: number, po: number): number {
  return Math.min(Math.round((pr * 0.25 + ex * 0.35 + int_ * 0.20 + po * 0.20) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.battle_card_usage_rate_pct <= 0.20 && i.no_competitive_intel_rate_pct >= 0.40) return "unprepared_seller";
  if (i.feature_comparison_loss_rate_pct >= 0.45 && i.price_concession_vs_competitor_pct <= 0.20) return "feature_fighter";
  if (i.price_concession_vs_competitor_pct >= 0.55 && i.competitive_win_rate_pct <= 0.30) return "price_surrenderer";
  if (i.late_competitor_discovery_rate_pct >= 0.45 && i.competitive_mention_early_rate_pct <= 0.20) return "late_discovery";
  if (i.single_competitor_thread_rate_pct >= 0.60 && i.competitive_stakeholder_loss_pct >= 0.45) return "single_thread_loser";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "losing"; if (c >= 40) return "struggling"; if (c >= 20) return "competing"; return "dominant"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "unprepared_seller" || p === "price_surrenderer") return "executive_competitive_escalation"; return "competitive_deal_review"; }
  if (r === "high") { if (p === "unprepared_seller") return "battle_card_refresh_coaching"; if (p === "feature_fighter") return "value_differentiation_coaching"; if (p === "price_surrenderer") return "value_differentiation_coaching"; if (p === "late_discovery") return "competitive_awareness_coaching"; if (p === "single_thread_loser") return "multi_thread_coaching"; return "battle_card_refresh_coaching"; }
  if (r === "moderate") return "competitive_awareness_coaching";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Competitive execution healthy — win rate, battle card usage, and intel discovery within benchmarks";
  const labels: Record<string,string> = { unprepared_seller:"Unprepared seller", feature_fighter:"Feature fighter", price_surrenderer:"Price surrenderer", late_discovery:"Late discovery", single_thread_loser:"Single-thread loser" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(i.competitive_win_rate_pct*100)}% comp win rate — ${Math.round(i.battle_card_usage_rate_pct*100)}% battle card usage — ${Math.round(i.late_competitor_discovery_rate_pct*100)}% late discovery — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(i => {
      const pr = preparednessScore(i), ex = executionScore(i), int_ = intelligenceScore(i), po = positioningScore(i);
      const comp = composite(pr, ex, int_, po), pat = pattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      const lr = Math.round(i.total_competitive_deals * i.avg_deal_value_usd * i.competitive_loss_rate_pct * (comp/100) * 100) / 100;
      return {
        rep_id: i.rep_id, region: i.region,
        competitive_risk: r, competitive_pattern: pat, competitive_severity: sev, recommended_action: act,
        preparedness_score: pr, execution_score: ex, intelligence_score: int_, positioning_score: po,
        competitive_composite: comp,
        has_competitive_gap: comp >= 40 || i.competitive_win_rate_pct <= 0.40 || i.battle_card_usage_rate_pct <= 0.50,
        requires_competitive_coaching: comp >= 25 || i.no_competitive_intel_rate_pct >= 0.30 || i.late_competitor_discovery_rate_pct >= 0.25,
        estimated_lost_revenue_usd: lr,
        competitive_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tpr=0, tex=0, tin=0, tpo=0, tcomp=0, tlr=0, gc=0, cc=0;
    for (const r of reps) {
      rc[r.competitive_risk]=(rc[r.competitive_risk]||0)+1; pc[r.competitive_pattern]=(pc[r.competitive_pattern]||0)+1;
      sc[r.competitive_severity]=(sc[r.competitive_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      tpr+=r.preparedness_score; tex+=r.execution_score; tin+=r.intelligence_score; tpo+=r.positioning_score;
      tcomp+=r.competitive_composite; tlr+=r.estimated_lost_revenue_usd;
      if (r.has_competitive_gap) gc++; if (r.requires_competitive_coaching) cc++;
    }
    const n = reps.length;
    return NextResponse.json(sealResponse({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_competitive_composite: Math.round(tcomp/n*10)/10,
      competitive_gap_count: gc, coaching_count: cc,
      avg_preparedness_score: Math.round(tpr/n*10)/10,
      avg_execution_score: Math.round(tex/n*10)/10,
      avg_intelligence_score: Math.round(tin/n*10)/10,
      avg_positioning_score: Math.round(tpo/n*10)/10,
      total_estimated_lost_revenue_usd: Math.round(tlr*100)/100,
    }} as Record<string,unknown>));
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-competitive-intelligence-battle-card-engine`)).json());
}
