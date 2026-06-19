import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"ME-001", region:"EMEA",  evaluation_period_id:"Q1-2026", avg_discount_pct:0.32, max_discount_pct:0.52, deals_discounted_above_approval_pct:0.48, unauthorized_discount_rate_pct:0.35, deal_desk_bypass_rate_pct:0.45, approval_cycle_shortcut_rate_pct:0.38, post_approval_discount_increase_rate_pct:0.28, avg_gross_margin_pct:0.22, deals_below_floor_margin_pct:0.32, quarter_end_discount_spike_ratio:2.8, list_price_adherence_rate_pct:0.28, discount_justification_rate_pct:0.30, multi_year_discount_front_loading_pct:0.52, bundled_discount_rate_pct:0.18, competitive_discount_rate_pct:0.65, total_deals_closed:28, avg_deal_value_usd:95000 },
  { rep_id:"ME-002", region:"NAMER", evaluation_period_id:"Q1-2026", avg_discount_pct:0.06, max_discount_pct:0.15, deals_discounted_above_approval_pct:0.04, unauthorized_discount_rate_pct:0.02, deal_desk_bypass_rate_pct:0.03, approval_cycle_shortcut_rate_pct:0.02, post_approval_discount_increase_rate_pct:0.02, avg_gross_margin_pct:0.58, deals_below_floor_margin_pct:0.02, quarter_end_discount_spike_ratio:1.1, list_price_adherence_rate_pct:0.88, discount_justification_rate_pct:0.92, multi_year_discount_front_loading_pct:0.08, bundled_discount_rate_pct:0.72, competitive_discount_rate_pct:0.15, total_deals_closed:35, avg_deal_value_usd:120000 },
  { rep_id:"ME-003", region:"APAC",  evaluation_period_id:"Q1-2026", avg_discount_pct:0.20, max_discount_pct:0.38, deals_discounted_above_approval_pct:0.28, unauthorized_discount_rate_pct:0.18, deal_desk_bypass_rate_pct:0.25, approval_cycle_shortcut_rate_pct:0.22, post_approval_discount_increase_rate_pct:0.16, avg_gross_margin_pct:0.38, deals_below_floor_margin_pct:0.18, quarter_end_discount_spike_ratio:1.9, list_price_adherence_rate_pct:0.52, discount_justification_rate_pct:0.55, multi_year_discount_front_loading_pct:0.30, bundled_discount_rate_pct:0.38, competitive_discount_rate_pct:0.42, total_deals_closed:22, avg_deal_value_usd:82000 },
  { rep_id:"ME-004", region:"LATAM", evaluation_period_id:"Q1-2026", avg_discount_pct:0.03, max_discount_pct:0.10, deals_discounted_above_approval_pct:0.02, unauthorized_discount_rate_pct:0.01, deal_desk_bypass_rate_pct:0.01, approval_cycle_shortcut_rate_pct:0.01, post_approval_discount_increase_rate_pct:0.01, avg_gross_margin_pct:0.65, deals_below_floor_margin_pct:0.01, quarter_end_discount_spike_ratio:1.0, list_price_adherence_rate_pct:0.95, discount_justification_rate_pct:0.98, multi_year_discount_front_loading_pct:0.04, bundled_discount_rate_pct:0.82, competitive_discount_rate_pct:0.08, total_deals_closed:18, avg_deal_value_usd:65000 },
  { rep_id:"ME-005", region:"EMEA",  evaluation_period_id:"Q1-2026", avg_discount_pct:0.38, max_discount_pct:0.58, deals_discounted_above_approval_pct:0.55, unauthorized_discount_rate_pct:0.42, deal_desk_bypass_rate_pct:0.52, approval_cycle_shortcut_rate_pct:0.48, post_approval_discount_increase_rate_pct:0.35, avg_gross_margin_pct:0.16, deals_below_floor_margin_pct:0.42, quarter_end_discount_spike_ratio:3.2, list_price_adherence_rate_pct:0.20, discount_justification_rate_pct:0.22, multi_year_discount_front_loading_pct:0.62, bundled_discount_rate_pct:0.12, competitive_discount_rate_pct:0.75, total_deals_closed:40, avg_deal_value_usd:115000 },
  { rep_id:"ME-006", region:"NAMER", evaluation_period_id:"Q1-2026", avg_discount_pct:0.12, max_discount_pct:0.22, deals_discounted_above_approval_pct:0.10, unauthorized_discount_rate_pct:0.06, deal_desk_bypass_rate_pct:0.08, approval_cycle_shortcut_rate_pct:0.06, post_approval_discount_increase_rate_pct:0.05, avg_gross_margin_pct:0.50, deals_below_floor_margin_pct:0.06, quarter_end_discount_spike_ratio:1.4, list_price_adherence_rate_pct:0.78, discount_justification_rate_pct:0.80, multi_year_discount_front_loading_pct:0.14, bundled_discount_rate_pct:0.60, competitive_discount_rate_pct:0.25, total_deals_closed:30, avg_deal_value_usd:92000 },
  { rep_id:"ME-007", region:"APAC",  evaluation_period_id:"Q1-2026", avg_discount_pct:0.45, max_discount_pct:0.70, deals_discounted_above_approval_pct:0.65, unauthorized_discount_rate_pct:0.52, deal_desk_bypass_rate_pct:0.60, approval_cycle_shortcut_rate_pct:0.55, post_approval_discount_increase_rate_pct:0.42, avg_gross_margin_pct:0.10, deals_below_floor_margin_pct:0.55, quarter_end_discount_spike_ratio:4.0, list_price_adherence_rate_pct:0.12, discount_justification_rate_pct:0.15, multi_year_discount_front_loading_pct:0.72, bundled_discount_rate_pct:0.08, competitive_discount_rate_pct:0.85, total_deals_closed:48, avg_deal_value_usd:130000 },
  { rep_id:"ME-008", region:"MEA",   evaluation_period_id:"Q1-2026", avg_discount_pct:0.16, max_discount_pct:0.28, deals_discounted_above_approval_pct:0.15, unauthorized_discount_rate_pct:0.10, deal_desk_bypass_rate_pct:0.12, approval_cycle_shortcut_rate_pct:0.10, post_approval_discount_increase_rate_pct:0.08, avg_gross_margin_pct:0.44, deals_below_floor_margin_pct:0.10, quarter_end_discount_spike_ratio:1.6, list_price_adherence_rate_pct:0.68, discount_justification_rate_pct:0.70, multi_year_discount_front_loading_pct:0.20, bundled_discount_rate_pct:0.52, competitive_discount_rate_pct:0.32, total_deals_closed:25, avg_deal_value_usd:75000 },
];

type Rep = typeof MOCK_REPS[0];

function disciplineScore(i: Rep): number {
  let s = 0;
  if      (i.avg_discount_pct                    >= 0.30) s += 40; else if (i.avg_discount_pct >= 0.18) s += 22; else if (i.avg_discount_pct >= 0.10) s += 8;
  if      (i.max_discount_pct                    >= 0.50) s += 35; else if (i.max_discount_pct >= 0.35) s += 18;
  if      (i.deals_discounted_above_approval_pct >= 0.40) s += 25; else if (i.deals_discounted_above_approval_pct >= 0.22) s += 12;
  return Math.min(s, 100);
}
function processScore(i: Rep): number {
  let s = 0;
  if      (i.deal_desk_bypass_rate_pct               >= 0.40) s += 45; else if (i.deal_desk_bypass_rate_pct >= 0.22) s += 25; else if (i.deal_desk_bypass_rate_pct >= 0.10) s += 10;
  if      (i.unauthorized_discount_rate_pct          >= 0.30) s += 30; else if (i.unauthorized_discount_rate_pct >= 0.15) s += 15;
  if      (i.post_approval_discount_increase_rate_pct >= 0.25) s += 25; else if (i.post_approval_discount_increase_rate_pct >= 0.12) s += 12;
  return Math.min(s, 100);
}
function outcomeScore(i: Rep): number {
  let s = 0;
  if      (i.deals_below_floor_margin_pct        >= 0.30) s += 40; else if (i.deals_below_floor_margin_pct >= 0.15) s += 22; else if (i.deals_below_floor_margin_pct >= 0.07) s += 8;
  if      (i.avg_gross_margin_pct                <= 0.20) s += 35; else if (i.avg_gross_margin_pct <= 0.35) s += 18;
  if      (i.quarter_end_discount_spike_ratio    >= 2.5)  s += 25; else if (i.quarter_end_discount_spike_ratio >= 1.8) s += 12;
  return Math.min(s, 100);
}
function valueScore(i: Rep): number {
  let s = 0;
  if      (i.list_price_adherence_rate_pct       <= 0.30) s += 45; else if (i.list_price_adherence_rate_pct <= 0.55) s += 25; else if (i.list_price_adherence_rate_pct <= 0.75) s += 10;
  if      (i.discount_justification_rate_pct     <= 0.35) s += 30; else if (i.discount_justification_rate_pct <= 0.60) s += 15;
  if      (i.bundled_discount_rate_pct           <= 0.20) s += 25; else if (i.bundled_discount_rate_pct <= 0.40) s += 12;
  return Math.min(s, 100);
}
function composite(di: number, pr: number, ou: number, va: number): number {
  return Math.min(Math.round((di * 0.30 + pr * 0.25 + ou * 0.25 + va * 0.20) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.deal_desk_bypass_rate_pct >= 0.35 && i.unauthorized_discount_rate_pct >= 0.25)     return "approval_bypasser";
  if (i.avg_discount_pct >= 0.25 && i.list_price_adherence_rate_pct <= 0.35)               return "list_price_ignorer";
  if (i.quarter_end_discount_spike_ratio >= 2.2 && i.deals_below_floor_margin_pct >= 0.20) return "quarter_end_dumper";
  if (i.max_discount_pct >= 0.45 && i.competitive_discount_rate_pct >= 0.60)               return "panic_discounter";
  if (i.multi_year_discount_front_loading_pct >= 0.45 && i.avg_gross_margin_pct <= 0.30)   return "margin_creep_enabler";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "collapsing"; if (c >= 40) return "eroding"; if (c >= 20) return "drifting"; return "disciplined"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "approval_bypasser" || p === "list_price_ignorer") return "executive_pricing_escalation"; return "margin_rescue_intervention"; }
  if (r === "high") {
    if (p === "approval_bypasser")    return "approval_workflow_audit";
    if (p === "panic_discounter")     return "value_selling_coaching";
    if (p === "margin_creep_enabler") return "pricing_strategy_reset";
    if (p === "list_price_ignorer")   return "deal_desk_enforcement";
    if (p === "quarter_end_dumper")   return "discount_hygiene_coaching";
    return "margin_monitoring";
  }
  if (r === "moderate") return "margin_monitoring";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Discount discipline strong — approval compliance, margin outcomes, and value selling within benchmark targets";
  const labels: Record<string,string> = { approval_bypasser:"Approval bypasser", panic_discounter:"Panic discounter", margin_creep_enabler:"Margin creep enabler", list_price_ignorer:"List price ignorer", quarter_end_dumper:"Quarter-end dumper" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(i.avg_discount_pct*100)}% avg discount — ${Math.round(i.deal_desk_bypass_rate_pct*100)}% deal desk bypass — ${Math.round(i.deals_below_floor_margin_pct*100)}% below floor — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(i => {
      const di = disciplineScore(i), pr = processScore(i), ou = outcomeScore(i), va = valueScore(i);
      const comp = composite(di, pr, ou, va), pat = pattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      const erosion = Math.round(i.total_deals_closed * i.avg_deal_value_usd * i.avg_discount_pct * (comp/100) * 100) / 100;
      return {
        rep_id: i.rep_id, region: i.region,
        margin_risk: r, margin_pattern: pat, margin_severity: sev, recommended_action: act,
        discipline_score: di, process_score: pr, outcome_score: ou, value_score: va,
        margin_composite: comp,
        has_margin_gap: comp >= 40 || i.avg_gross_margin_pct <= 0.35 || i.deals_below_floor_margin_pct >= 0.15,
        requires_intervention: comp >= 25 || i.deal_desk_bypass_rate_pct >= 0.20 || i.avg_discount_pct >= 0.15,
        estimated_margin_erosion_usd: erosion,
        margin_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tdi=0, tpr=0, tou=0, tva=0, tcomp=0, tme=0, gc=0, ic=0;
    for (const r of reps) {
      rc[r.margin_risk]=(rc[r.margin_risk]||0)+1; pc[r.margin_pattern]=(pc[r.margin_pattern]||0)+1;
      sc[r.margin_severity]=(sc[r.margin_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      tdi+=r.discipline_score; tpr+=r.process_score; tou+=r.outcome_score; tva+=r.value_score;
      tcomp+=r.margin_composite; tme+=r.estimated_margin_erosion_usd;
      if (r.has_margin_gap) gc++; if (r.requires_intervention) ic++;
    }
    const n = reps.length;
    return NextResponse.json(sealResponse({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_margin_composite: Math.round(tcomp/n*10)/10,
      margin_gap_count: gc, intervention_count: ic,
      avg_discipline_score: Math.round(tdi/n*10)/10,
      avg_process_score: Math.round(tpr/n*10)/10,
      avg_outcome_score: Math.round(tou/n*10)/10,
      avg_value_score: Math.round(tva/n*10)/10,
      total_estimated_margin_erosion_usd: Math.round(tme*100)/100,
    }} as Record<string,unknown>));
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-discount-approval-abuse-margin-erosion-engine`)).json());
}
