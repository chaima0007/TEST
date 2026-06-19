import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"DL-001", region:"EMEA",  evaluation_period_id:"Q2-2026", avg_discount_depth_pct:0.32, discount_frequency_pct:0.72, unauthorized_discount_rate_pct:0.42, early_discount_offer_rate_pct:0.55, discount_as_first_response_pct:0.62, gross_margin_vs_target_pct:-0.18, price_objection_concession_rate_pct:0.58, multi_level_discount_rate_pct:0.48, discount_to_close_conversion_pct:0.38, competitor_price_match_rate_pct:0.62, list_price_win_rate_pct:0.05, end_of_quarter_spike_rate_pct:0.68, approval_request_bypass_count:5, avg_deal_cycle_with_discount_days:72, value_objection_to_discount_pct:0.72, deal_size_after_discount_shrink_pct:0.28, repeat_discount_same_customer_pct:0.55, total_closed_deals:9,  avg_deal_value_usd:85000 },
  { rep_id:"DL-002", region:"APAC",  evaluation_period_id:"Q2-2026", avg_discount_depth_pct:0.06, discount_frequency_pct:0.18, unauthorized_discount_rate_pct:0.02, early_discount_offer_rate_pct:0.08, discount_as_first_response_pct:0.05, gross_margin_vs_target_pct:0.12, price_objection_concession_rate_pct:0.10, multi_level_discount_rate_pct:0.05, discount_to_close_conversion_pct:0.82, competitor_price_match_rate_pct:0.10, list_price_win_rate_pct:0.62, end_of_quarter_spike_rate_pct:0.08, approval_request_bypass_count:0, avg_deal_cycle_with_discount_days:28, value_objection_to_discount_pct:0.08, deal_size_after_discount_shrink_pct:0.02, repeat_discount_same_customer_pct:0.05, total_closed_deals:14, avg_deal_value_usd:62000 },
  { rep_id:"DL-003", region:"NAMER", evaluation_period_id:"Q2-2026", avg_discount_depth_pct:0.15, discount_frequency_pct:0.42, unauthorized_discount_rate_pct:0.12, early_discount_offer_rate_pct:0.22, discount_as_first_response_pct:0.22, gross_margin_vs_target_pct:-0.03, price_objection_concession_rate_pct:0.28, multi_level_discount_rate_pct:0.18, discount_to_close_conversion_pct:0.62, competitor_price_match_rate_pct:0.32, list_price_win_rate_pct:0.38, end_of_quarter_spike_rate_pct:0.25, approval_request_bypass_count:1, avg_deal_cycle_with_discount_days:42, value_objection_to_discount_pct:0.32, deal_size_after_discount_shrink_pct:0.08, repeat_discount_same_customer_pct:0.22, total_closed_deals:12, avg_deal_value_usd:72000 },
  { rep_id:"DL-004", region:"LATAM", evaluation_period_id:"Q2-2026", avg_discount_depth_pct:0.24, discount_frequency_pct:0.62, unauthorized_discount_rate_pct:0.32, early_discount_offer_rate_pct:0.48, discount_as_first_response_pct:0.52, gross_margin_vs_target_pct:-0.12, price_objection_concession_rate_pct:0.48, multi_level_discount_rate_pct:0.38, discount_to_close_conversion_pct:0.42, competitor_price_match_rate_pct:0.52, list_price_win_rate_pct:0.12, end_of_quarter_spike_rate_pct:0.52, approval_request_bypass_count:3, avg_deal_cycle_with_discount_days:58, value_objection_to_discount_pct:0.58, deal_size_after_discount_shrink_pct:0.18, repeat_discount_same_customer_pct:0.42, total_closed_deals:8,  avg_deal_value_usd:78000 },
  { rep_id:"DL-005", region:"EMEA",  evaluation_period_id:"Q2-2026", avg_discount_depth_pct:0.38, discount_frequency_pct:0.78, unauthorized_discount_rate_pct:0.48, early_discount_offer_rate_pct:0.62, discount_as_first_response_pct:0.68, gross_margin_vs_target_pct:-0.22, price_objection_concession_rate_pct:0.65, multi_level_discount_rate_pct:0.52, discount_to_close_conversion_pct:0.28, competitor_price_match_rate_pct:0.68, list_price_win_rate_pct:0.02, end_of_quarter_spike_rate_pct:0.72, approval_request_bypass_count:6, avg_deal_cycle_with_discount_days:82, value_objection_to_discount_pct:0.78, deal_size_after_discount_shrink_pct:0.32, repeat_discount_same_customer_pct:0.62, total_closed_deals:7,  avg_deal_value_usd:110000 },
  { rep_id:"DL-006", region:"MEA",   evaluation_period_id:"Q2-2026", avg_discount_depth_pct:0.09, discount_frequency_pct:0.25, unauthorized_discount_rate_pct:0.04, early_discount_offer_rate_pct:0.12, discount_as_first_response_pct:0.08, gross_margin_vs_target_pct:0.08, price_objection_concession_rate_pct:0.15, multi_level_discount_rate_pct:0.08, discount_to_close_conversion_pct:0.78, competitor_price_match_rate_pct:0.15, list_price_win_rate_pct:0.55, end_of_quarter_spike_rate_pct:0.12, approval_request_bypass_count:0, avg_deal_cycle_with_discount_days:32, value_objection_to_discount_pct:0.12, deal_size_after_discount_shrink_pct:0.04, repeat_discount_same_customer_pct:0.08, total_closed_deals:11, avg_deal_value_usd:55000 },
  { rep_id:"DL-007", region:"APAC",  evaluation_period_id:"Q2-2026", avg_discount_depth_pct:0.19, discount_frequency_pct:0.52, unauthorized_discount_rate_pct:0.18, early_discount_offer_rate_pct:0.32, discount_as_first_response_pct:0.32, gross_margin_vs_target_pct:-0.06, price_objection_concession_rate_pct:0.35, multi_level_discount_rate_pct:0.25, discount_to_close_conversion_pct:0.52, competitor_price_match_rate_pct:0.38, list_price_win_rate_pct:0.28, end_of_quarter_spike_rate_pct:0.35, approval_request_bypass_count:2, avg_deal_cycle_with_discount_days:48, value_objection_to_discount_pct:0.42, deal_size_after_discount_shrink_pct:0.12, repeat_discount_same_customer_pct:0.28, total_closed_deals:10, avg_deal_value_usd:68000 },
  { rep_id:"DL-008", region:"NAMER", evaluation_period_id:"Q2-2026", avg_discount_depth_pct:0.08, discount_frequency_pct:0.22, unauthorized_discount_rate_pct:0.03, early_discount_offer_rate_pct:0.10, discount_as_first_response_pct:0.08, gross_margin_vs_target_pct:0.05, price_objection_concession_rate_pct:0.12, multi_level_discount_rate_pct:0.06, discount_to_close_conversion_pct:0.85, competitor_price_match_rate_pct:0.12, list_price_win_rate_pct:0.58, end_of_quarter_spike_rate_pct:0.10, approval_request_bypass_count:0, avg_deal_cycle_with_discount_days:25, value_objection_to_discount_pct:0.10, deal_size_after_discount_shrink_pct:0.03, repeat_discount_same_customer_pct:0.06, total_closed_deals:13, avg_deal_value_usd:72000 },
];

function frScore(i: typeof MOCK_REPS[0]): number {
  let s=0;
  if      (i.discount_frequency_pct        >= 0.70) s+=40; else if (i.discount_frequency_pct >= 0.50) s+=22; else if (i.discount_frequency_pct >= 0.35) s+=8;
  if      (i.multi_level_discount_rate_pct >= 0.45) s+=35; else if (i.multi_level_discount_rate_pct >= 0.25) s+=18;
  if      (i.end_of_quarter_spike_rate_pct >= 0.55) s+=25; else if (i.end_of_quarter_spike_rate_pct >= 0.35) s+=12;
  return Math.min(s,100);
}
function deScore(i: typeof MOCK_REPS[0]): number {
  let s=0;
  if      (i.avg_discount_depth_pct             >= 0.30) s+=40; else if (i.avg_discount_depth_pct >= 0.18) s+=22; else if (i.avg_discount_depth_pct >= 0.10) s+=8;
  if      (i.deal_size_after_discount_shrink_pct>= 0.25) s+=35; else if (i.deal_size_after_discount_shrink_pct >= 0.12) s+=18;
  if      (i.gross_margin_vs_target_pct         <=-0.15) s+=25; else if (i.gross_margin_vs_target_pct <= -0.05) s+=12;
  return Math.min(s,100);
}
function diScore(i: typeof MOCK_REPS[0]): number {
  let s=0;
  if      (i.unauthorized_discount_rate_pct  >= 0.40) s+=40; else if (i.unauthorized_discount_rate_pct >= 0.20) s+=22; else if (i.unauthorized_discount_rate_pct >= 0.08) s+=8;
  if      (i.early_discount_offer_rate_pct   >= 0.50) s+=35; else if (i.early_discount_offer_rate_pct >= 0.28) s+=18;
  if      (i.approval_request_bypass_count   >= 4)    s+=25; else if (i.approval_request_bypass_count >= 2) s+=12;
  return Math.min(s,100);
}
function vdScore(i: typeof MOCK_REPS[0]): number {
  let s=0;
  if      (i.discount_as_first_response_pct         >= 0.55) s+=45; else if (i.discount_as_first_response_pct >= 0.30) s+=25; else if (i.discount_as_first_response_pct >= 0.15) s+=10;
  if      (i.price_objection_concession_rate_pct    >= 0.55) s+=30; else if (i.price_objection_concession_rate_pct >= 0.30) s+=15;
  if      (i.list_price_win_rate_pct                <= 0.10) s+=25; else if (i.list_price_win_rate_pct <= 0.25) s+=12;
  return Math.min(s,100);
}
function composite(fr:number,de:number,di:number,vd:number): number { return Math.min(Math.round((fr*0.25+de*0.30+di*0.25+vd*0.20)*100)/100,100); }
function pattern(i: typeof MOCK_REPS[0]): string {
  if (i.end_of_quarter_spike_rate_pct >= 0.45 && i.avg_discount_depth_pct >= 0.20) return "panic_discounter";
  if (i.repeat_discount_same_customer_pct >= 0.50 && i.list_price_win_rate_pct <= 0.15) return "relationship_briber";
  if (i.early_discount_offer_rate_pct >= 0.45 && i.discount_as_first_response_pct >= 0.40) return "price_first_seller";
  if (i.unauthorized_discount_rate_pct >= 0.30 && i.approval_request_bypass_count >= 3) return "approval_bypasser";
  if (i.discount_frequency_pct >= 0.60 && i.multi_level_discount_rate_pct >= 0.35) return "chronic_leaker";
  return "none";
}
function risk(c:number): string { if(c>=60)return"critical";if(c>=40)return"high";if(c>=20)return"moderate";return"low"; }
function severity(c:number): string { if(c>=60)return"eroding";if(c>=40)return"leaking";if(c>=20)return"drifting";return"disciplined"; }
function action(r:string,p:string): string {
  if(r==="critical"){if(p==="approval_bypasser"||p==="chronic_leaker")return"pricing_authority_reset";return"deal_desk_review";}
  if(r==="high"){if(p==="panic_discounter"||p==="price_first_seller")return"value_selling_coaching";if(p==="relationship_briber")return"pricing_discipline_coaching";if(p==="approval_bypasser")return"approval_process_enforcement";if(p==="chronic_leaker")return"deal_desk_review";return"pricing_discipline_coaching";}
  if(r==="moderate")return"discount_monitoring";return"no_action";
}
function signal(i: typeof MOCK_REPS[0],pat:string,comp:number): string {
  if(comp<20)return"Discount discipline healthy — frequency, depth, authorization, and value defense within benchmarks";
  const labels: Record<string,string>={panic_discounter:"Panic discounter",relationship_briber:"Relationship briber",price_first_seller:"Price-first seller",approval_bypasser:"Approval bypasser",chronic_leaker:"Chronic leaker"};
  const label=labels[pat]??pat.replace(/_/g," ");
  return`${label} — ${Math.round(i.discount_frequency_pct*100)}% deals discounted — avg depth ${Math.round(i.avg_discount_depth_pct*100)}% — ${Math.round(i.unauthorized_discount_rate_pct*100)}% unauthorized — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(i => {
      const fr=frScore(i),de=deScore(i),di=diScore(i),vd=vdScore(i);
      const comp=composite(fr,de,di,vd),pat=pattern(i),r=risk(comp),sev=severity(comp),act=action(r,pat);
      const me=i.total_closed_deals*i.avg_deal_value_usd*i.avg_discount_depth_pct*i.discount_frequency_pct*(comp/100);
      return { rep_id:i.rep_id,region:i.region, discount_risk:r,discount_pattern:pat,discount_severity:sev,recommended_action:act,
        frequency_score:fr,depth_score:de,discipline_score:di,value_defense_score:vd,discount_composite:comp,
        has_discount_gap:comp>=40||i.avg_discount_depth_pct>=0.20||i.unauthorized_discount_rate_pct>=0.15,
        requires_discount_intervention:comp>=25||i.discount_frequency_pct>=0.50||i.gross_margin_vs_target_pct<=-0.08,
        estimated_margin_erosion_usd:Math.round(me*100)/100,
        discount_signal:signal(i,pat,comp) };
    });
    const rc: Record<string,number>={},pc: Record<string,number>={},sc: Record<string,number>={},ac: Record<string,number>={};
    let tc=0,tf=0,td=0,tdi=0,tv=0,tm=0,gc=0,ic=0;
    for(const r of reps){rc[r.discount_risk]=(rc[r.discount_risk]||0)+1;pc[r.discount_pattern]=(pc[r.discount_pattern]||0)+1;sc[r.discount_severity]=(sc[r.discount_severity]||0)+1;ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;tc+=r.discount_composite;tf+=r.frequency_score;td+=r.depth_score;tdi+=r.discipline_score;tv+=r.value_defense_score;tm+=r.estimated_margin_erosion_usd;if(r.has_discount_gap)gc++;if(r.requires_discount_intervention)ic++;}
    const n=reps.length;
    return NextResponse.json(sealResponse({reps,summary:{total:n,risk_counts:rc,pattern_counts:pc,severity_counts:sc,action_counts:ac,avg_discount_composite:Math.round(tc/n*10)/10,discount_gap_count:gc,intervention_count:ic,avg_frequency_score:Math.round(tf/n*10)/10,avg_depth_score:Math.round(td/n*10)/10,avg_discipline_score:Math.round(tdi/n*10)/10,avg_value_defense_score:Math.round(tv/n*10)/10,total_estimated_margin_erosion_usd:Math.round(tm*100)/100}} as Record<string,unknown>));
  }
  return NextResponse.json(await(await fetch(`${process.env.SWARM_API_URL}/sales-discount-leakage-margin-erosion-intelligence-engine`)).json());
}
