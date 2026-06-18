import { NextResponse } from "next/server";

const MOCK_REPS = [
  { rep_id:"NL-001", region:"EMEA",  evaluation_period_id:"Q2-2026", first_concession_without_ask_pct:0.72, avg_concession_rounds_per_deal:4.2, price_anchor_usage_rate_pct:0.12, concession_size_avg_pct:0.22, deal_closed_below_floor_price_pct:0.38, multi_element_trade_rate_pct:0.08, deadline_pressure_concession_pct:0.68, bundle_unbundling_rate_pct:0.52, legal_hold_up_capitulation_pct:0.62, negotiation_preparation_score:0.22, walk_away_rate_pct:0.01, final_price_vs_list_pct:0.68, value_selling_score:0.18, competitor_price_match_rate_pct:0.72, procurement_win_rate_pct:0.18, multi_year_deal_rate_pct:0.12, payment_terms_concession_pct:0.55, total_closed_deals:32, avg_deal_value_usd:88000 },
  { rep_id:"NL-002", region:"APAC",  evaluation_period_id:"Q2-2026", first_concession_without_ask_pct:0.18, avg_concession_rounds_per_deal:1.2, price_anchor_usage_rate_pct:0.82, concession_size_avg_pct:0.06, deal_closed_below_floor_price_pct:0.05, multi_element_trade_rate_pct:0.72, deadline_pressure_concession_pct:0.12, bundle_unbundling_rate_pct:0.10, legal_hold_up_capitulation_pct:0.08, negotiation_preparation_score:0.88, walk_away_rate_pct:0.14, final_price_vs_list_pct:0.94, value_selling_score:0.88, competitor_price_match_rate_pct:0.12, procurement_win_rate_pct:0.72, multi_year_deal_rate_pct:0.62, payment_terms_concession_pct:0.08, total_closed_deals:28, avg_deal_value_usd:112000 },
  { rep_id:"NL-003", region:"NAMER", evaluation_period_id:"Q2-2026", first_concession_without_ask_pct:0.42, avg_concession_rounds_per_deal:2.8, price_anchor_usage_rate_pct:0.45, concession_size_avg_pct:0.14, deal_closed_below_floor_price_pct:0.18, multi_element_trade_rate_pct:0.38, deadline_pressure_concession_pct:0.35, bundle_unbundling_rate_pct:0.28, legal_hold_up_capitulation_pct:0.32, negotiation_preparation_score:0.55, walk_away_rate_pct:0.05, final_price_vs_list_pct:0.82, value_selling_score:0.52, competitor_price_match_rate_pct:0.38, procurement_win_rate_pct:0.48, multi_year_deal_rate_pct:0.35, payment_terms_concession_pct:0.28, total_closed_deals:41, avg_deal_value_usd:95000 },
  { rep_id:"NL-004", region:"LATAM", evaluation_period_id:"Q2-2026", first_concession_without_ask_pct:0.62, avg_concession_rounds_per_deal:4.8, price_anchor_usage_rate_pct:0.08, concession_size_avg_pct:0.28, deal_closed_below_floor_price_pct:0.42, multi_element_trade_rate_pct:0.05, deadline_pressure_concession_pct:0.72, bundle_unbundling_rate_pct:0.58, legal_hold_up_capitulation_pct:0.58, negotiation_preparation_score:0.18, walk_away_rate_pct:0.005, final_price_vs_list_pct:0.62, value_selling_score:0.12, competitor_price_match_rate_pct:0.82, procurement_win_rate_pct:0.12, multi_year_deal_rate_pct:0.08, payment_terms_concession_pct:0.68, total_closed_deals:22, avg_deal_value_usd:78000 },
  { rep_id:"NL-005", region:"EMEA",  evaluation_period_id:"Q2-2026", first_concession_without_ask_pct:0.22, avg_concession_rounds_per_deal:1.5, price_anchor_usage_rate_pct:0.72, concession_size_avg_pct:0.08, deal_closed_below_floor_price_pct:0.08, multi_element_trade_rate_pct:0.62, deadline_pressure_concession_pct:0.18, bundle_unbundling_rate_pct:0.12, legal_hold_up_capitulation_pct:0.12, negotiation_preparation_score:0.78, walk_away_rate_pct:0.10, final_price_vs_list_pct:0.91, value_selling_score:0.78, competitor_price_match_rate_pct:0.18, procurement_win_rate_pct:0.65, multi_year_deal_rate_pct:0.52, payment_terms_concession_pct:0.12, total_closed_deals:35, avg_deal_value_usd:102000 },
  { rep_id:"NL-006", region:"MEA",   evaluation_period_id:"Q2-2026", first_concession_without_ask_pct:0.82, avg_concession_rounds_per_deal:5.5, price_anchor_usage_rate_pct:0.05, concession_size_avg_pct:0.32, deal_closed_below_floor_price_pct:0.52, multi_element_trade_rate_pct:0.04, deadline_pressure_concession_pct:0.78, bundle_unbundling_rate_pct:0.65, legal_hold_up_capitulation_pct:0.72, negotiation_preparation_score:0.12, walk_away_rate_pct:0.005, final_price_vs_list_pct:0.55, value_selling_score:0.08, competitor_price_match_rate_pct:0.88, procurement_win_rate_pct:0.08, multi_year_deal_rate_pct:0.05, payment_terms_concession_pct:0.78, total_closed_deals:18, avg_deal_value_usd:72000 },
  { rep_id:"NL-007", region:"APAC",  evaluation_period_id:"Q2-2026", first_concession_without_ask_pct:0.35, avg_concession_rounds_per_deal:2.2, price_anchor_usage_rate_pct:0.58, concession_size_avg_pct:0.10, deal_closed_below_floor_price_pct:0.12, multi_element_trade_rate_pct:0.52, deadline_pressure_concession_pct:0.25, bundle_unbundling_rate_pct:0.18, legal_hold_up_capitulation_pct:0.22, negotiation_preparation_score:0.68, walk_away_rate_pct:0.07, final_price_vs_list_pct:0.87, value_selling_score:0.65, competitor_price_match_rate_pct:0.28, procurement_win_rate_pct:0.58, multi_year_deal_rate_pct:0.42, payment_terms_concession_pct:0.18, total_closed_deals:38, avg_deal_value_usd:98000 },
  { rep_id:"NL-008", region:"NAMER", evaluation_period_id:"Q2-2026", first_concession_without_ask_pct:0.58, avg_concession_rounds_per_deal:3.5, price_anchor_usage_rate_pct:0.25, concession_size_avg_pct:0.18, deal_closed_below_floor_price_pct:0.28, multi_element_trade_rate_pct:0.15, deadline_pressure_concession_pct:0.52, bundle_unbundling_rate_pct:0.42, legal_hold_up_capitulation_pct:0.45, negotiation_preparation_score:0.38, walk_away_rate_pct:0.02, final_price_vs_list_pct:0.76, value_selling_score:0.35, competitor_price_match_rate_pct:0.55, procurement_win_rate_pct:0.32, multi_year_deal_rate_pct:0.22, payment_terms_concession_pct:0.42, total_closed_deals:29, avg_deal_value_usd:91000 },
];

type Rep = typeof MOCK_REPS[0];

function disciplineScore(i: Rep): number {
  let s = 0;
  if      (i.first_concession_without_ask_pct  >= 0.55) s += 40; else if (i.first_concession_without_ask_pct >= 0.32) s += 22; else if (i.first_concession_without_ask_pct >= 0.15) s += 8;
  if      (i.deal_closed_below_floor_price_pct >= 0.30) s += 35; else if (i.deal_closed_below_floor_price_pct >= 0.15) s += 18;
  if      (i.multi_element_trade_rate_pct      <= 0.20) s += 25; else if (i.multi_element_trade_rate_pct <= 0.45) s += 12;
  return Math.min(s, 100);
}
function leverageScore(i: Rep): number {
  let s = 0;
  if      (i.avg_concession_rounds_per_deal    >= 4.0) s += 45; else if (i.avg_concession_rounds_per_deal >= 2.5) s += 25; else if (i.avg_concession_rounds_per_deal >= 1.5) s += 10;
  if      (i.deadline_pressure_concession_pct  >= 0.55) s += 30; else if (i.deadline_pressure_concession_pct >= 0.30) s += 15;
  if      (i.procurement_win_rate_pct          <= 0.25) s += 25; else if (i.procurement_win_rate_pct <= 0.50) s += 12;
  return Math.min(s, 100);
}
function preparationScore(i: Rep): number {
  let s = 0;
  if      (i.negotiation_preparation_score     <= 0.25) s += 40; else if (i.negotiation_preparation_score <= 0.50) s += 22; else if (i.negotiation_preparation_score <= 0.70) s += 8;
  if      (i.walk_away_rate_pct                <= 0.02) s += 35; else if (i.walk_away_rate_pct <= 0.06) s += 18;
  if      (i.legal_hold_up_capitulation_pct    >= 0.55) s += 25; else if (i.legal_hold_up_capitulation_pct >= 0.30) s += 12;
  return Math.min(s, 100);
}
function valueAnchoringScore(i: Rep): number {
  let s = 0;
  if      (i.price_anchor_usage_rate_pct       <= 0.20) s += 45; else if (i.price_anchor_usage_rate_pct <= 0.45) s += 25; else if (i.price_anchor_usage_rate_pct <= 0.65) s += 10;
  if      (i.competitor_price_match_rate_pct   >= 0.55) s += 30; else if (i.competitor_price_match_rate_pct >= 0.30) s += 15;
  if      (i.value_selling_score               <= 0.25) s += 25; else if (i.value_selling_score <= 0.55) s += 12;
  return Math.min(s, 100);
}
function composite(di: number, le: number, pr: number, va: number): number {
  return Math.min(Math.round((di * 0.30 + le * 0.25 + pr * 0.25 + va * 0.20) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.first_concession_without_ask_pct >= 0.55 && i.price_anchor_usage_rate_pct <= 0.20) return "first_mover_conceder";
  if (i.price_anchor_usage_rate_pct <= 0.15 && i.final_price_vs_list_pct <= 0.75) return "anchor_avoider";
  if (i.avg_concession_rounds_per_deal >= 4.0 && i.concession_size_avg_pct >= 0.15) return "multi_round_eroder";
  if (i.deadline_pressure_concession_pct >= 0.60 && i.deal_closed_below_floor_price_pct >= 0.20) return "deadline_capitulator";
  if (i.bundle_unbundling_rate_pct >= 0.45 && i.multi_element_trade_rate_pct <= 0.15) return "bundler_destroyer";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "collapsing"; if (c >= 40) return "eroding"; if (c >= 20) return "softening"; return "disciplined"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "first_mover_conceder" || p === "anchor_avoider") return "executive_negotiation_reset"; return "deal_desk_negotiation_support"; }
  if (r === "high") {
    if (p === "first_mover_conceder") return "concession_discipline_coaching";
    if (p === "anchor_avoider")       return "anchor_technique_coaching";
    if (p === "multi_round_eroder")   return "deal_desk_negotiation_support";
    if (p === "deadline_capitulator") return "value_framing_coaching";
    if (p === "bundler_destroyer")    return "concession_discipline_coaching";
    return "negotiation_awareness_coaching";
  }
  if (r === "moderate") return "negotiation_awareness_coaching";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Negotiation discipline strong — pricing, concessions, and leverage within benchmark targets";
  const labels: Record<string,string> = { first_mover_conceder:"First mover conceder", anchor_avoider:"Anchor avoider", multi_round_eroder:"Multi-round eroder", deadline_capitulator:"Deadline capitulator", bundler_destroyer:"Bundler destroyer" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(i.first_concession_without_ask_pct*100)}% concede without ask — ${(i.avg_concession_rounds_per_deal).toFixed(1)} rounds avg — ${Math.round(i.final_price_vs_list_pct*100)}% final vs list — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(i => {
      const di = disciplineScore(i), le = leverageScore(i), pr = preparationScore(i), va = valueAnchoringScore(i);
      const comp = composite(di, le, pr, va), pat = pattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      const margin = Math.round(i.total_closed_deals * i.avg_deal_value_usd * Math.min(i.concession_size_avg_pct * i.avg_concession_rounds_per_deal, 0.5) * (comp/100) * 100) / 100;
      return {
        rep_id: i.rep_id, region: i.region,
        negotiation_risk: r, negotiation_pattern: pat, negotiation_severity: sev, recommended_action: act,
        discipline_score: di, leverage_score: le, preparation_score: pr, value_anchoring_score: va,
        negotiation_composite: comp,
        has_negotiation_gap: comp >= 40 || i.final_price_vs_list_pct <= 0.80 || i.first_concession_without_ask_pct >= 0.30,
        requires_negotiation_coaching: comp >= 25 || i.price_anchor_usage_rate_pct <= 0.45 || i.deal_closed_below_floor_price_pct >= 0.10,
        estimated_margin_left_usd: margin,
        negotiation_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tdi=0, tle=0, tpr=0, tva=0, tcomp=0, tmar=0, gc=0, cc=0;
    for (const r of reps) {
      rc[r.negotiation_risk]=(rc[r.negotiation_risk]||0)+1; pc[r.negotiation_pattern]=(pc[r.negotiation_pattern]||0)+1;
      sc[r.negotiation_severity]=(sc[r.negotiation_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      tdi+=r.discipline_score; tle+=r.leverage_score; tpr+=r.preparation_score; tva+=r.value_anchoring_score;
      tcomp+=r.negotiation_composite; tmar+=r.estimated_margin_left_usd;
      if (r.has_negotiation_gap) gc++; if (r.requires_negotiation_coaching) cc++;
    }
    const n = reps.length;
    return NextResponse.json({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_negotiation_composite: Math.round(tcomp/n*10)/10,
      negotiation_gap_count: gc, coaching_count: cc,
      avg_discipline_score: Math.round(tdi/n*10)/10,
      avg_leverage_score: Math.round(tle/n*10)/10,
      avg_preparation_score: Math.round(tpr/n*10)/10,
      avg_value_anchoring_score: Math.round(tva/n*10)/10,
      total_estimated_margin_left_usd: Math.round(tmar*100)/100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-price-sensitivity-negotiation-leverage-engine`)).json());
}
