import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"PM-001", region:"EMEA",  evaluation_period_id:"Q2-2026", primary_contact_level_score:0.18, economic_buyer_contact_rate_pct:0.12, it_only_contact_rate_pct:0.72, business_unit_alignment_score:0.22, decision_maker_access_rate_pct:0.15, influencer_only_rate_pct:0.68, procurement_first_contact_rate_pct:0.55, avg_seniority_of_contacts:0.22, sponsor_identification_rate_pct:0.15, cross_functional_coverage_score:0.12, persona_to_use_case_fit_score:0.18, budget_authority_confirmed_rate_pct:0.10, vp_plus_engagement_rate_pct:0.12, champion_seniority_score:0.15, technical_blockers_rate_pct:0.62, wrong_entry_point_rate_pct:0.68, referral_to_right_person_rate_pct:0.12, lost_due_to_persona_mismatch_pct:0.42, total_deals_evaluated:8,  avg_deal_value_usd:95000 },
  { rep_id:"PM-002", region:"APAC",  evaluation_period_id:"Q2-2026", primary_contact_level_score:0.82, economic_buyer_contact_rate_pct:0.78, it_only_contact_rate_pct:0.12, business_unit_alignment_score:0.85, decision_maker_access_rate_pct:0.88, influencer_only_rate_pct:0.08, procurement_first_contact_rate_pct:0.08, avg_seniority_of_contacts:0.82, sponsor_identification_rate_pct:0.85, cross_functional_coverage_score:0.82, persona_to_use_case_fit_score:0.88, budget_authority_confirmed_rate_pct:0.85, vp_plus_engagement_rate_pct:0.82, champion_seniority_score:0.88, technical_blockers_rate_pct:0.08, wrong_entry_point_rate_pct:0.08, referral_to_right_person_rate_pct:0.88, lost_due_to_persona_mismatch_pct:0.05, total_deals_evaluated:15, avg_deal_value_usd:62000 },
  { rep_id:"PM-003", region:"NAMER", evaluation_period_id:"Q2-2026", primary_contact_level_score:0.45, economic_buyer_contact_rate_pct:0.45, it_only_contact_rate_pct:0.38, business_unit_alignment_score:0.52, decision_maker_access_rate_pct:0.52, influencer_only_rate_pct:0.32, procurement_first_contact_rate_pct:0.25, avg_seniority_of_contacts:0.52, sponsor_identification_rate_pct:0.55, cross_functional_coverage_score:0.48, persona_to_use_case_fit_score:0.55, budget_authority_confirmed_rate_pct:0.48, vp_plus_engagement_rate_pct:0.45, champion_seniority_score:0.52, technical_blockers_rate_pct:0.28, wrong_entry_point_rate_pct:0.32, referral_to_right_person_rate_pct:0.55, lost_due_to_persona_mismatch_pct:0.18, total_deals_evaluated:12, avg_deal_value_usd:75000 },
  { rep_id:"PM-004", region:"LATAM", evaluation_period_id:"Q2-2026", primary_contact_level_score:0.22, economic_buyer_contact_rate_pct:0.18, it_only_contact_rate_pct:0.62, business_unit_alignment_score:0.28, decision_maker_access_rate_pct:0.25, influencer_only_rate_pct:0.58, procurement_first_contact_rate_pct:0.42, avg_seniority_of_contacts:0.28, sponsor_identification_rate_pct:0.22, cross_functional_coverage_score:0.18, persona_to_use_case_fit_score:0.25, budget_authority_confirmed_rate_pct:0.15, vp_plus_engagement_rate_pct:0.18, champion_seniority_score:0.22, technical_blockers_rate_pct:0.52, wrong_entry_point_rate_pct:0.55, referral_to_right_person_rate_pct:0.18, lost_due_to_persona_mismatch_pct:0.35, total_deals_evaluated:9,  avg_deal_value_usd:82000 },
  { rep_id:"PM-005", region:"EMEA",  evaluation_period_id:"Q2-2026", primary_contact_level_score:0.12, economic_buyer_contact_rate_pct:0.08, it_only_contact_rate_pct:0.82, business_unit_alignment_score:0.15, decision_maker_access_rate_pct:0.10, influencer_only_rate_pct:0.75, procurement_first_contact_rate_pct:0.65, avg_seniority_of_contacts:0.12, sponsor_identification_rate_pct:0.08, cross_functional_coverage_score:0.08, persona_to_use_case_fit_score:0.12, budget_authority_confirmed_rate_pct:0.08, vp_plus_engagement_rate_pct:0.08, champion_seniority_score:0.10, technical_blockers_rate_pct:0.72, wrong_entry_point_rate_pct:0.75, referral_to_right_person_rate_pct:0.08, lost_due_to_persona_mismatch_pct:0.52, total_deals_evaluated:7,  avg_deal_value_usd:110000 },
  { rep_id:"PM-006", region:"MEA",   evaluation_period_id:"Q2-2026", primary_contact_level_score:0.68, economic_buyer_contact_rate_pct:0.65, it_only_contact_rate_pct:0.18, business_unit_alignment_score:0.72, decision_maker_access_rate_pct:0.72, influencer_only_rate_pct:0.15, procurement_first_contact_rate_pct:0.12, avg_seniority_of_contacts:0.68, sponsor_identification_rate_pct:0.72, cross_functional_coverage_score:0.68, persona_to_use_case_fit_score:0.75, budget_authority_confirmed_rate_pct:0.72, vp_plus_engagement_rate_pct:0.68, champion_seniority_score:0.72, technical_blockers_rate_pct:0.12, wrong_entry_point_rate_pct:0.15, referral_to_right_person_rate_pct:0.75, lost_due_to_persona_mismatch_pct:0.08, total_deals_evaluated:11, avg_deal_value_usd:58000 },
  { rep_id:"PM-007", region:"APAC",  evaluation_period_id:"Q2-2026", primary_contact_level_score:0.35, economic_buyer_contact_rate_pct:0.30, it_only_contact_rate_pct:0.52, business_unit_alignment_score:0.38, decision_maker_access_rate_pct:0.38, influencer_only_rate_pct:0.45, procurement_first_contact_rate_pct:0.32, avg_seniority_of_contacts:0.38, sponsor_identification_rate_pct:0.38, cross_functional_coverage_score:0.32, persona_to_use_case_fit_score:0.38, budget_authority_confirmed_rate_pct:0.32, vp_plus_engagement_rate_pct:0.32, champion_seniority_score:0.35, technical_blockers_rate_pct:0.38, wrong_entry_point_rate_pct:0.42, referral_to_right_person_rate_pct:0.38, lost_due_to_persona_mismatch_pct:0.25, total_deals_evaluated:10, avg_deal_value_usd:68000 },
  { rep_id:"PM-008", region:"NAMER", evaluation_period_id:"Q2-2026", primary_contact_level_score:0.72, economic_buyer_contact_rate_pct:0.68, it_only_contact_rate_pct:0.22, business_unit_alignment_score:0.75, decision_maker_access_rate_pct:0.78, influencer_only_rate_pct:0.12, procurement_first_contact_rate_pct:0.15, avg_seniority_of_contacts:0.72, sponsor_identification_rate_pct:0.75, cross_functional_coverage_score:0.72, persona_to_use_case_fit_score:0.78, budget_authority_confirmed_rate_pct:0.72, vp_plus_engagement_rate_pct:0.72, champion_seniority_score:0.75, technical_blockers_rate_pct:0.15, wrong_entry_point_rate_pct:0.12, referral_to_right_person_rate_pct:0.78, lost_due_to_persona_mismatch_pct:0.08, total_deals_evaluated:13, avg_deal_value_usd:72000 },
];

function acScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.decision_maker_access_rate_pct <= 0.30) s += 40;
  else if (inp.decision_maker_access_rate_pct <= 0.55) s += 22;
  else if (inp.decision_maker_access_rate_pct <= 0.75) s += 8;
  if      (inp.vp_plus_engagement_rate_pct   <= 0.20) s += 35;
  else if (inp.vp_plus_engagement_rate_pct   <= 0.45) s += 18;
  if      (inp.primary_contact_level_score   <= 0.25) s += 25;
  else if (inp.primary_contact_level_score   <= 0.50) s += 12;
  return Math.min(s, 100);
}
function alScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.persona_to_use_case_fit_score <= 0.30) s += 40;
  else if (inp.persona_to_use_case_fit_score <= 0.55) s += 22;
  else if (inp.persona_to_use_case_fit_score <= 0.75) s += 8;
  if      (inp.business_unit_alignment_score <= 0.30) s += 35;
  else if (inp.business_unit_alignment_score <= 0.55) s += 18;
  if      (inp.wrong_entry_point_rate_pct   >= 0.50) s += 25;
  else if (inp.wrong_entry_point_rate_pct   >= 0.30) s += 12;
  return Math.min(s, 100);
}
function auScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.economic_buyer_contact_rate_pct     <= 0.25) s += 40;
  else if (inp.economic_buyer_contact_rate_pct     <= 0.50) s += 22;
  else if (inp.economic_buyer_contact_rate_pct     <= 0.70) s += 8;
  if      (inp.budget_authority_confirmed_rate_pct <= 0.25) s += 35;
  else if (inp.budget_authority_confirmed_rate_pct <= 0.50) s += 18;
  if      (inp.influencer_only_rate_pct            >= 0.50) s += 25;
  else if (inp.influencer_only_rate_pct            >= 0.30) s += 12;
  return Math.min(s, 100);
}
function coScore(inp: typeof MOCK_REPS[0]): number {
  let s = 0;
  if      (inp.cross_functional_coverage_score     <= 0.25) s += 45;
  else if (inp.cross_functional_coverage_score     <= 0.50) s += 25;
  else if (inp.cross_functional_coverage_score     <= 0.70) s += 10;
  if      (inp.sponsor_identification_rate_pct     <= 0.30) s += 30;
  else if (inp.sponsor_identification_rate_pct     <= 0.55) s += 15;
  if      (inp.technical_blockers_rate_pct         >= 0.45) s += 25;
  else if (inp.technical_blockers_rate_pct         >= 0.25) s += 12;
  return Math.min(s, 100);
}
function composite(ac: number, al: number, au: number, co: number): number {
  return Math.min(Math.round((ac*0.30 + al*0.25 + au*0.30 + co*0.15)*100)/100, 100);
}
function pattern(inp: typeof MOCK_REPS[0]): string {
  if (inp.primary_contact_level_score <= 0.30 && inp.vp_plus_engagement_rate_pct <= 0.20) return "wrong_level";
  if (inp.business_unit_alignment_score <= 0.35 && inp.persona_to_use_case_fit_score <= 0.40) return "wrong_department";
  if (inp.influencer_only_rate_pct >= 0.50 && inp.decision_maker_access_rate_pct <= 0.35) return "influencer_only";
  if (inp.it_only_contact_rate_pct >= 0.55 && inp.technical_blockers_rate_pct >= 0.40) return "technical_gatekeeper";
  if (inp.economic_buyer_contact_rate_pct <= 0.25 && inp.budget_authority_confirmed_rate_pct <= 0.25) return "budget_blind";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "invisible"; if (c >= 40) return "disconnected"; if (c >= 20) return "misaligned"; return "aligned"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "wrong_level" || p === "influencer_only") return "deal_re_qualification"; return "persona_reset_intervention"; }
  if (r === "high") {
    if (p === "wrong_level" || p === "influencer_only") return "executive_access_coaching";
    if (p === "wrong_department") return "stakeholder_mapping_coaching";
    if (p === "technical_gatekeeper" || p === "budget_blind") return "budget_holder_introduction";
    return "stakeholder_mapping_coaching";
  }
  if (r === "moderate") return "persona_alignment_check";
  return "no_action";
}
function signal(inp: typeof MOCK_REPS[0], pat: string, comp: number): string {
  if (comp < 20) return "Buyer persona alignment strong — decision-maker access, budget authority, and cross-functional coverage within benchmarks";
  const labels: Record<string,string> = { wrong_level:"Wrong contact level", wrong_department:"Wrong department", influencer_only:"Influencer-only access", technical_gatekeeper:"Technical gatekeeper block", budget_blind:"Budget-blind engagement" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(inp.decision_maker_access_rate_pct*100)}% DM access — ${Math.round(inp.economic_buyer_contact_rate_pct*100)}% EB contact — ${Math.round(inp.vp_plus_engagement_rate_pct*100)}% VP+ engagement — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[sales-buyer-persona-mismatch-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const risk_counts: Record<string,number>={}, pattern_counts: Record<string,number>={};
    const severity_counts: Record<string,number>={}, action_counts: Record<string,number>={};
    let total_comp=0, total_ac=0, total_al=0, total_au=0, total_co=0, total_lv=0, gap=0, coach=0;
    for (const r of reps) {
      risk_counts[r.persona_risk]=(risk_counts[r.persona_risk]||0)+1;
      pattern_counts[r.persona_pattern]=(pattern_counts[r.persona_pattern]||0)+1;
      severity_counts[r.persona_severity]=(severity_counts[r.persona_severity]||0)+1;
      action_counts[r.recommended_action]=(action_counts[r.recommended_action]||0)+1;
      total_comp+=r.persona_composite; total_ac+=r.access_score; total_al+=r.alignment_score;
      total_au+=r.authority_score; total_co+=r.coverage_score; total_lv+=r.estimated_lost_deal_value_usd;
      if (r.has_persona_gap) gap++; if (r.requires_persona_coaching) coach++;
    }
    const n = reps.length;
    return sealResponse(NextResponse.json(sealResponse({ reps, summary: {
      total:n, risk_counts, pattern_counts, severity_counts, action_counts,
      avg_persona_composite: Math.round(total_comp/n*10)/10,
      persona_gap_count: gap, coaching_count: coach,
      avg_access_score: Math.round(total_ac/n*10)/10, avg_alignment_score: Math.round(total_al/n*10)/10,
      avg_authority_score: Math.round(total_au/n*10)/10, avg_coverage_score: Math.round(total_co/n*10)/10,
      total_estimated_lost_deal_value_usd: Math.round(total_lv*100)/100,
    }} as Record<string,unknown>)));
  }

  const res = await fetch(`${process.env.SWARM_API_URL}/sales-buyer-persona-mismatch-intelligence-engine`, { next: { revalidate: 30 } });
  return sealResponse(NextResponse.json(await res.json()));
}
