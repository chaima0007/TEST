import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"CW-001", region:"EMEA",  evaluation_period_id:"Q1-2026", competitive_deal_rate_pct:0.82, competitive_win_rate_pct:0.18, competitive_loss_rate_pct:0.72, single_competitor_loss_concentration_pct:0.68, competitor_identified_late_rate_pct:0.62, battle_card_usage_rate_pct:0.12, competitive_discovery_score:0.18, price_cited_as_loss_reason_pct:0.62, feature_gap_cited_as_loss_reason_pct:0.48, value_differentiation_score:0.15, competitive_pipeline_conversion_rate_pct:0.12, displacement_deal_win_rate_pct:0.10, incumbent_defense_win_rate_pct:0.28, multi_competitor_deal_rate_pct:0.55, competitive_intelligence_recency_score:0.12, proof_of_concept_win_rate_pct:0.22, executive_alignment_in_comp_deals_pct:0.18, total_competitive_deals:24, avg_deal_value_usd:98000 },
  { rep_id:"CW-002", region:"NAMER", evaluation_period_id:"Q1-2026", competitive_deal_rate_pct:0.45, competitive_win_rate_pct:0.72, competitive_loss_rate_pct:0.18, single_competitor_loss_concentration_pct:0.15, competitor_identified_late_rate_pct:0.12, battle_card_usage_rate_pct:0.88, competitive_discovery_score:0.85, price_cited_as_loss_reason_pct:0.12, feature_gap_cited_as_loss_reason_pct:0.10, value_differentiation_score:0.88, competitive_pipeline_conversion_rate_pct:0.68, displacement_deal_win_rate_pct:0.72, incumbent_defense_win_rate_pct:0.82, multi_competitor_deal_rate_pct:0.12, competitive_intelligence_recency_score:0.88, proof_of_concept_win_rate_pct:0.82, executive_alignment_in_comp_deals_pct:0.85, total_competitive_deals:32, avg_deal_value_usd:115000 },
  { rep_id:"CW-003", region:"APAC",  evaluation_period_id:"Q1-2026", competitive_deal_rate_pct:0.62, competitive_win_rate_pct:0.38, competitive_loss_rate_pct:0.48, single_competitor_loss_concentration_pct:0.42, competitor_identified_late_rate_pct:0.38, battle_card_usage_rate_pct:0.45, competitive_discovery_score:0.42, price_cited_as_loss_reason_pct:0.38, feature_gap_cited_as_loss_reason_pct:0.30, value_differentiation_score:0.48, competitive_pipeline_conversion_rate_pct:0.38, displacement_deal_win_rate_pct:0.35, incumbent_defense_win_rate_pct:0.55, multi_competitor_deal_rate_pct:0.32, competitive_intelligence_recency_score:0.48, proof_of_concept_win_rate_pct:0.48, executive_alignment_in_comp_deals_pct:0.42, total_competitive_deals:28, avg_deal_value_usd:82000 },
  { rep_id:"CW-004", region:"LATAM", evaluation_period_id:"Q1-2026", competitive_deal_rate_pct:0.35, competitive_win_rate_pct:0.88, competitive_loss_rate_pct:0.10, single_competitor_loss_concentration_pct:0.08, competitor_identified_late_rate_pct:0.08, battle_card_usage_rate_pct:0.92, competitive_discovery_score:0.90, price_cited_as_loss_reason_pct:0.08, feature_gap_cited_as_loss_reason_pct:0.06, value_differentiation_score:0.92, competitive_pipeline_conversion_rate_pct:0.80, displacement_deal_win_rate_pct:0.85, incumbent_defense_win_rate_pct:0.88, multi_competitor_deal_rate_pct:0.08, competitive_intelligence_recency_score:0.92, proof_of_concept_win_rate_pct:0.88, executive_alignment_in_comp_deals_pct:0.90, total_competitive_deals:18, avg_deal_value_usd:70000 },
  { rep_id:"CW-005", region:"EMEA",  evaluation_period_id:"Q1-2026", competitive_deal_rate_pct:0.78, competitive_win_rate_pct:0.22, competitive_loss_rate_pct:0.68, single_competitor_loss_concentration_pct:0.28, competitor_identified_late_rate_pct:0.55, battle_card_usage_rate_pct:0.22, competitive_discovery_score:0.25, price_cited_as_loss_reason_pct:0.58, feature_gap_cited_as_loss_reason_pct:0.45, value_differentiation_score:0.22, competitive_pipeline_conversion_rate_pct:0.18, displacement_deal_win_rate_pct:0.22, incumbent_defense_win_rate_pct:0.35, multi_competitor_deal_rate_pct:0.45, competitive_intelligence_recency_score:0.25, proof_of_concept_win_rate_pct:0.30, executive_alignment_in_comp_deals_pct:0.28, total_competitive_deals:38, avg_deal_value_usd:105000 },
  { rep_id:"CW-006", region:"MEA",   evaluation_period_id:"Q1-2026", competitive_deal_rate_pct:0.55, competitive_win_rate_pct:0.52, competitive_loss_rate_pct:0.35, single_competitor_loss_concentration_pct:0.22, competitor_identified_late_rate_pct:0.25, battle_card_usage_rate_pct:0.68, competitive_discovery_score:0.65, price_cited_as_loss_reason_pct:0.25, feature_gap_cited_as_loss_reason_pct:0.20, value_differentiation_score:0.68, competitive_pipeline_conversion_rate_pct:0.52, displacement_deal_win_rate_pct:0.55, incumbent_defense_win_rate_pct:0.68, multi_competitor_deal_rate_pct:0.22, competitive_intelligence_recency_score:0.65, proof_of_concept_win_rate_pct:0.62, executive_alignment_in_comp_deals_pct:0.65, total_competitive_deals:22, avg_deal_value_usd:88000 },
  { rep_id:"CW-007", region:"NAMER", evaluation_period_id:"Q1-2026", competitive_deal_rate_pct:0.90, competitive_win_rate_pct:0.15, competitive_loss_rate_pct:0.78, single_competitor_loss_concentration_pct:0.72, competitor_identified_late_rate_pct:0.72, battle_card_usage_rate_pct:0.08, competitive_discovery_score:0.10, price_cited_as_loss_reason_pct:0.68, feature_gap_cited_as_loss_reason_pct:0.55, value_differentiation_score:0.10, competitive_pipeline_conversion_rate_pct:0.08, displacement_deal_win_rate_pct:0.08, incumbent_defense_win_rate_pct:0.20, multi_competitor_deal_rate_pct:0.62, competitive_intelligence_recency_score:0.08, proof_of_concept_win_rate_pct:0.15, executive_alignment_in_comp_deals_pct:0.12, total_competitive_deals:42, avg_deal_value_usd:125000 },
  { rep_id:"CW-008", region:"APAC",  evaluation_period_id:"Q1-2026", competitive_deal_rate_pct:0.48, competitive_win_rate_pct:0.60, competitive_loss_rate_pct:0.28, single_competitor_loss_concentration_pct:0.18, competitor_identified_late_rate_pct:0.18, battle_card_usage_rate_pct:0.75, competitive_discovery_score:0.72, price_cited_as_loss_reason_pct:0.18, feature_gap_cited_as_loss_reason_pct:0.15, value_differentiation_score:0.75, competitive_pipeline_conversion_rate_pct:0.58, displacement_deal_win_rate_pct:0.62, incumbent_defense_win_rate_pct:0.72, multi_competitor_deal_rate_pct:0.18, competitive_intelligence_recency_score:0.72, proof_of_concept_win_rate_pct:0.72, executive_alignment_in_comp_deals_pct:0.75, total_competitive_deals:26, avg_deal_value_usd:92000 },
];

type Rep = typeof MOCK_REPS[0];

function exposureScore(i: Rep): number {
  let s = 0;
  if      (i.single_competitor_loss_concentration_pct >= 0.60) s += 40; else if (i.single_competitor_loss_concentration_pct >= 0.40) s += 22; else if (i.single_competitor_loss_concentration_pct >= 0.25) s += 8;
  if      (i.competitive_loss_rate_pct                >= 0.65) s += 35; else if (i.competitive_loss_rate_pct >= 0.45) s += 18; else if (i.competitive_loss_rate_pct >= 0.30) s += 8;
  if      (i.multi_competitor_deal_rate_pct           >= 0.50) s += 25; else if (i.multi_competitor_deal_rate_pct >= 0.30) s += 12;
  return Math.min(s, 100);
}
function positioningScore(i: Rep): number {
  let s = 0;
  if      (i.value_differentiation_score           <= 0.20) s += 45; else if (i.value_differentiation_score <= 0.45) s += 25; else if (i.value_differentiation_score <= 0.65) s += 10;
  if      (i.price_cited_as_loss_reason_pct        >= 0.55) s += 30; else if (i.price_cited_as_loss_reason_pct >= 0.35) s += 15;
  if      (i.feature_gap_cited_as_loss_reason_pct  >= 0.45) s += 25; else if (i.feature_gap_cited_as_loss_reason_pct >= 0.28) s += 12;
  return Math.min(s, 100);
}
function intelligenceScore(i: Rep): number {
  let s = 0;
  if      (i.competitor_identified_late_rate_pct     >= 0.55) s += 40; else if (i.competitor_identified_late_rate_pct >= 0.35) s += 22; else if (i.competitor_identified_late_rate_pct >= 0.20) s += 8;
  if      (i.competitive_intelligence_recency_score  <= 0.20) s += 35; else if (i.competitive_intelligence_recency_score <= 0.45) s += 18;
  if      (i.battle_card_usage_rate_pct              <= 0.25) s += 25; else if (i.battle_card_usage_rate_pct <= 0.55) s += 12;
  return Math.min(s, 100);
}
function conversionScore(i: Rep): number {
  let s = 0;
  if      (i.competitive_pipeline_conversion_rate_pct <= 0.15) s += 45; else if (i.competitive_pipeline_conversion_rate_pct <= 0.30) s += 25; else if (i.competitive_pipeline_conversion_rate_pct <= 0.45) s += 10;
  if      (i.displacement_deal_win_rate_pct           <= 0.20) s += 30; else if (i.displacement_deal_win_rate_pct <= 0.40) s += 15;
  if      (i.executive_alignment_in_comp_deals_pct    <= 0.25) s += 25; else if (i.executive_alignment_in_comp_deals_pct <= 0.50) s += 12;
  return Math.min(s, 100);
}
function composite(ex: number, po: number, in_: number, co: number): number {
  return Math.min(Math.round((ex * 0.30 + po * 0.25 + in_ * 0.25 + co * 0.20) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.single_competitor_loss_concentration_pct >= 0.55 && i.competitive_win_rate_pct <= 0.30) return "single_competitor_loser";
  if (i.price_cited_as_loss_reason_pct >= 0.50 && i.value_differentiation_score <= 0.30)        return "price_only_battle";
  if (i.feature_gap_cited_as_loss_reason_pct >= 0.40 && i.competitive_discovery_score <= 0.40)  return "feature_gap_surrender";
  if (i.competitor_identified_late_rate_pct >= 0.50 && i.battle_card_usage_rate_pct <= 0.30)    return "late_to_discover_comp";
  if (i.displacement_deal_win_rate_pct <= 0.15 && i.incumbent_defense_win_rate_pct >= 0.65)     return "displacement_target";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "losing"; if (c >= 40) return "slipping"; if (c >= 20) return "competing"; return "dominant"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "single_competitor_loser" || p === "price_only_battle") return "competitive_strategy_reset"; return "win_loss_review_intervention"; }
  if (r === "high") {
    if (p === "single_competitor_loser") return "battle_card_enforcement";
    if (p === "price_only_battle")       return "pricing_strategy_coaching";
    if (p === "feature_gap_surrender")   return "differentiation_coaching";
    if (p === "late_to_discover_comp")   return "discovery_depth_coaching";
    if (p === "displacement_target")     return "competitive_deal_desk_support";
    return "competitive_monitoring";
  }
  if (r === "moderate") return "competitive_monitoring";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Competitive performance strong — win rates, differentiation, and intel freshness within benchmark targets";
  const labels: Record<string,string> = { single_competitor_loser:"Single competitor loser", price_only_battle:"Price-only battle", feature_gap_surrender:"Feature gap surrender", late_to_discover_comp:"Late to discover competitor", displacement_target:"Displacement target" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(i.competitive_win_rate_pct*100)}% comp win rate — ${Math.round(i.price_cited_as_loss_reason_pct*100)}% price cited as loss — ${Math.round(i.competitor_identified_late_rate_pct*100)}% late discovery — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(i => {
      const ex = exposureScore(i), po = positioningScore(i), in_ = intelligenceScore(i), co = conversionScore(i);
      const comp = composite(ex, po, in_, co), pat = pattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      const lost = Math.round(i.total_competitive_deals * i.avg_deal_value_usd * i.competitive_loss_rate_pct * (comp/100) * 100) / 100;
      return {
        rep_id: i.rep_id, region: i.region,
        competitive_risk: r, competitive_pattern: pat, competitive_severity: sev, recommended_action: act,
        exposure_score: ex, positioning_score: po, intelligence_score: in_, conversion_score: co,
        competitive_composite: comp,
        has_competitive_gap: comp >= 40 || i.competitive_win_rate_pct <= 0.35 || i.single_competitor_loss_concentration_pct >= 0.40,
        requires_competitive_coaching: comp >= 25 || i.battle_card_usage_rate_pct <= 0.40 || i.value_differentiation_score <= 0.50,
        estimated_lost_revenue_usd: lost,
        competitive_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tex=0, tpo=0, tin=0, tco=0, tcomp=0, tlr=0, gc=0, cc=0;
    for (const r of reps) {
      rc[r.competitive_risk]=(rc[r.competitive_risk]||0)+1; pc[r.competitive_pattern]=(pc[r.competitive_pattern]||0)+1;
      sc[r.competitive_severity]=(sc[r.competitive_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      tex+=r.exposure_score; tpo+=r.positioning_score; tin+=r.intelligence_score; tco+=r.conversion_score;
      tcomp+=r.competitive_composite; tlr+=r.estimated_lost_revenue_usd;
      if (r.has_competitive_gap) gc++; if (r.requires_competitive_coaching) cc++;
    }
    const n = reps.length;
    return NextResponse.json(sealResponse({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_competitive_composite: Math.round(tcomp/n*10)/10,
      competitive_gap_count: gc, coaching_count: cc,
      avg_exposure_score: Math.round(tex/n*10)/10,
      avg_positioning_score: Math.round(tpo/n*10)/10,
      avg_intelligence_score: Math.round(tin/n*10)/10,
      avg_conversion_score: Math.round(tco/n*10)/10,
      total_estimated_lost_revenue_usd: Math.round(tlr*100)/100,
    }} as Record<string,unknown>));
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-competitive-win-loss-pattern-engine`)).json());
}
