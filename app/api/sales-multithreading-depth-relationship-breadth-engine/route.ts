import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_REPS = [
  { rep_id:"MT-001", region:"EMEA",  evaluation_period_id:"Q1-2026", avg_contacts_per_account:1.4, single_threaded_account_rate_pct:0.72, avg_new_contacts_added_per_quarter:0.4, contact_attrition_rate_pct:0.45, economic_buyer_engaged_rate_pct:0.15, technical_buyer_engaged_rate_pct:0.65, end_user_engaged_rate_pct:0.22, champion_to_non_champion_ratio:8.0, avg_email_threads_per_contact:1.2, multi_contact_meeting_rate_pct:0.14, cross_functional_reach_score:0.16, referral_introduction_rate_pct:0.10, dormant_contact_rate_pct:0.58, contact_map_completeness_score:0.18, buying_committee_size_vs_avg:0.40, c_suite_engaged_rate_pct:0.10, vp_engaged_rate_pct:0.18, total_active_accounts:28, avg_deal_value_usd:95000 },
  { rep_id:"MT-002", region:"NAMER", evaluation_period_id:"Q1-2026", avg_contacts_per_account:5.8, single_threaded_account_rate_pct:0.08, avg_new_contacts_added_per_quarter:2.5, contact_attrition_rate_pct:0.10, economic_buyer_engaged_rate_pct:0.88, technical_buyer_engaged_rate_pct:0.85, end_user_engaged_rate_pct:0.82, champion_to_non_champion_ratio:1.5, avg_email_threads_per_contact:6.5, multi_contact_meeting_rate_pct:0.82, cross_functional_reach_score:0.88, referral_introduction_rate_pct:0.72, dormant_contact_rate_pct:0.10, contact_map_completeness_score:0.88, buying_committee_size_vs_avg:1.55, c_suite_engaged_rate_pct:0.78, vp_engaged_rate_pct:0.88, total_active_accounts:22, avg_deal_value_usd:118000 },
  { rep_id:"MT-003", region:"APAC",  evaluation_period_id:"Q1-2026", avg_contacts_per_account:2.8, single_threaded_account_rate_pct:0.42, avg_new_contacts_added_per_quarter:1.0, contact_attrition_rate_pct:0.28, economic_buyer_engaged_rate_pct:0.45, technical_buyer_engaged_rate_pct:0.70, end_user_engaged_rate_pct:0.48, champion_to_non_champion_ratio:3.5, avg_email_threads_per_contact:3.2, multi_contact_meeting_rate_pct:0.42, cross_functional_reach_score:0.48, referral_introduction_rate_pct:0.30, dormant_contact_rate_pct:0.35, contact_map_completeness_score:0.48, buying_committee_size_vs_avg:0.80, c_suite_engaged_rate_pct:0.35, vp_engaged_rate_pct:0.48, total_active_accounts:32, avg_deal_value_usd:82000 },
  { rep_id:"MT-004", region:"LATAM", evaluation_period_id:"Q1-2026", avg_contacts_per_account:7.2, single_threaded_account_rate_pct:0.04, avg_new_contacts_added_per_quarter:3.2, contact_attrition_rate_pct:0.06, economic_buyer_engaged_rate_pct:0.92, technical_buyer_engaged_rate_pct:0.90, end_user_engaged_rate_pct:0.88, champion_to_non_champion_ratio:1.2, avg_email_threads_per_contact:8.5, multi_contact_meeting_rate_pct:0.88, cross_functional_reach_score:0.92, referral_introduction_rate_pct:0.80, dormant_contact_rate_pct:0.06, contact_map_completeness_score:0.92, buying_committee_size_vs_avg:1.80, c_suite_engaged_rate_pct:0.85, vp_engaged_rate_pct:0.92, total_active_accounts:18, avg_deal_value_usd:68000 },
  { rep_id:"MT-005", region:"EMEA",  evaluation_period_id:"Q1-2026", avg_contacts_per_account:1.6, single_threaded_account_rate_pct:0.65, avg_new_contacts_added_per_quarter:0.3, contact_attrition_rate_pct:0.50, economic_buyer_engaged_rate_pct:0.12, technical_buyer_engaged_rate_pct:0.78, end_user_engaged_rate_pct:0.18, champion_to_non_champion_ratio:9.0, avg_email_threads_per_contact:1.5, multi_contact_meeting_rate_pct:0.16, cross_functional_reach_score:0.12, referral_introduction_rate_pct:0.08, dormant_contact_rate_pct:0.62, contact_map_completeness_score:0.15, buying_committee_size_vs_avg:0.35, c_suite_engaged_rate_pct:0.08, vp_engaged_rate_pct:0.12, total_active_accounts:35, avg_deal_value_usd:108000 },
  { rep_id:"MT-006", region:"MEA",   evaluation_period_id:"Q1-2026", avg_contacts_per_account:4.0, single_threaded_account_rate_pct:0.20, avg_new_contacts_added_per_quarter:1.8, contact_attrition_rate_pct:0.18, economic_buyer_engaged_rate_pct:0.70, technical_buyer_engaged_rate_pct:0.72, end_user_engaged_rate_pct:0.65, champion_to_non_champion_ratio:2.0, avg_email_threads_per_contact:4.8, multi_contact_meeting_rate_pct:0.65, cross_functional_reach_score:0.70, referral_introduction_rate_pct:0.55, dormant_contact_rate_pct:0.18, contact_map_completeness_score:0.72, buying_committee_size_vs_avg:1.20, c_suite_engaged_rate_pct:0.60, vp_engaged_rate_pct:0.72, total_active_accounts:25, avg_deal_value_usd:88000 },
  { rep_id:"MT-007", region:"NAMER", evaluation_period_id:"Q1-2026", avg_contacts_per_account:1.2, single_threaded_account_rate_pct:0.82, avg_new_contacts_added_per_quarter:0.2, contact_attrition_rate_pct:0.58, economic_buyer_engaged_rate_pct:0.08, technical_buyer_engaged_rate_pct:0.55, end_user_engaged_rate_pct:0.10, champion_to_non_champion_ratio:12.0, avg_email_threads_per_contact:0.8, multi_contact_meeting_rate_pct:0.10, cross_functional_reach_score:0.10, referral_introduction_rate_pct:0.05, dormant_contact_rate_pct:0.72, contact_map_completeness_score:0.10, buying_committee_size_vs_avg:0.25, c_suite_engaged_rate_pct:0.06, vp_engaged_rate_pct:0.10, total_active_accounts:40, avg_deal_value_usd:125000 },
  { rep_id:"MT-008", region:"APAC",  evaluation_period_id:"Q1-2026", avg_contacts_per_account:3.5, single_threaded_account_rate_pct:0.28, avg_new_contacts_added_per_quarter:1.4, contact_attrition_rate_pct:0.22, economic_buyer_engaged_rate_pct:0.58, technical_buyer_engaged_rate_pct:0.62, end_user_engaged_rate_pct:0.55, champion_to_non_champion_ratio:2.5, avg_email_threads_per_contact:4.0, multi_contact_meeting_rate_pct:0.55, cross_functional_reach_score:0.60, referral_introduction_rate_pct:0.42, dormant_contact_rate_pct:0.25, contact_map_completeness_score:0.60, buying_committee_size_vs_avg:1.00, c_suite_engaged_rate_pct:0.48, vp_engaged_rate_pct:0.60, total_active_accounts:30, avg_deal_value_usd:78000 },
];

type Rep = typeof MOCK_REPS[0];

function depthScore(i: Rep): number {
  let s = 0;
  if      (i.single_threaded_account_rate_pct   >= 0.60) s += 40; else if (i.single_threaded_account_rate_pct >= 0.40) s += 22; else if (i.single_threaded_account_rate_pct >= 0.22) s += 8;
  if      (i.avg_contacts_per_account           <= 1.5)  s += 35; else if (i.avg_contacts_per_account <= 2.5) s += 18; else if (i.avg_contacts_per_account <= 3.5) s += 6;
  if      (i.avg_new_contacts_added_per_quarter <= 0.5)  s += 25; else if (i.avg_new_contacts_added_per_quarter <= 1.2) s += 12;
  return Math.min(s, 100);
}
function coverageScore(i: Rep): number {
  let s = 0;
  if      (i.economic_buyer_engaged_rate_pct  <= 0.25) s += 45; else if (i.economic_buyer_engaged_rate_pct <= 0.50) s += 25; else if (i.economic_buyer_engaged_rate_pct <= 0.70) s += 10;
  if      (i.c_suite_engaged_rate_pct         <= 0.15) s += 30; else if (i.c_suite_engaged_rate_pct <= 0.35) s += 15;
  if      (i.contact_map_completeness_score   <= 0.25) s += 25; else if (i.contact_map_completeness_score <= 0.50) s += 12;
  return Math.min(s, 100);
}
function qualityScore(i: Rep): number {
  let s = 0;
  if      (i.multi_contact_meeting_rate_pct   <= 0.20) s += 40; else if (i.multi_contact_meeting_rate_pct <= 0.45) s += 22; else if (i.multi_contact_meeting_rate_pct <= 0.65) s += 8;
  if      (i.cross_functional_reach_score     <= 0.20) s += 35; else if (i.cross_functional_reach_score <= 0.45) s += 18;
  if      (i.referral_introduction_rate_pct   <= 0.15) s += 25; else if (i.referral_introduction_rate_pct <= 0.35) s += 12;
  return Math.min(s, 100);
}
function networkScore(i: Rep): number {
  let s = 0;
  if      (i.dormant_contact_rate_pct         >= 0.55) s += 45; else if (i.dormant_contact_rate_pct >= 0.35) s += 25; else if (i.dormant_contact_rate_pct >= 0.20) s += 10;
  if      (i.contact_attrition_rate_pct       >= 0.40) s += 30; else if (i.contact_attrition_rate_pct >= 0.22) s += 15;
  if      (i.buying_committee_size_vs_avg     <= 0.50) s += 25; else if (i.buying_committee_size_vs_avg <= 0.75) s += 12;
  return Math.min(s, 100);
}
function composite(de: number, co: number, qu: number, ne: number): number {
  return Math.min(Math.round((de * 0.30 + co * 0.25 + qu * 0.25 + ne * 0.20) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.single_threaded_account_rate_pct >= 0.55 && i.avg_contacts_per_account <= 1.8)                                   return "single_thread_dependency";
  if (i.c_suite_engaged_rate_pct <= 0.15 && i.vp_engaged_rate_pct <= 0.20 && i.technical_buyer_engaged_rate_pct >= 0.70)  return "it_bubble";
  if (i.c_suite_engaged_rate_pct >= 0.70 && i.end_user_engaged_rate_pct <= 0.20)                                          return "executive_bypass";
  if (i.vp_engaged_rate_pct >= 0.55 && i.economic_buyer_engaged_rate_pct <= 0.20)                                         return "vertical_tunnel";
  if (i.dormant_contact_rate_pct >= 0.50 && i.avg_new_contacts_added_per_quarter <= 0.8)                                  return "breadth_stall";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "isolated"; if (c >= 40) return "thin"; if (c >= 20) return "adequate"; return "networked"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "single_thread_dependency" || p === "breadth_stall") return "deal_restructure_escalation"; return "account_rescue_intervention"; }
  if (r === "high") {
    if (p === "single_thread_dependency") return "contact_expansion_coaching";
    if (p === "it_bubble")               return "it_champion_bridge_coaching";
    if (p === "executive_bypass")        return "exec_introduction_coaching";
    if (p === "vertical_tunnel")         return "stakeholder_mapping_workshop";
    if (p === "breadth_stall")           return "relationship_breadth_sprint";
    return "multithreading_monitoring";
  }
  if (r === "moderate") return "multithreading_monitoring";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Relationship breadth strong — multithreading depth, stakeholder coverage, and network health within benchmark targets";
  const labels: Record<string,string> = { single_thread_dependency:"Single-thread dependency", vertical_tunnel:"Vertical tunnel", it_bubble:"IT bubble", executive_bypass:"Executive bypass", breadth_stall:"Breadth stall" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${i.avg_contacts_per_account.toFixed(1)} avg contacts/account — ${Math.round(i.single_threaded_account_rate_pct*100)}% single-threaded — ${Math.round(i.economic_buyer_engaged_rate_pct*100)}% EB engaged — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(i => {
      const de = depthScore(i), co = coverageScore(i), qu = qualityScore(i), ne = networkScore(i);
      const comp = composite(de, co, qu, ne), pat = pattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      const vuln = Math.round(i.total_active_accounts * i.avg_deal_value_usd * i.single_threaded_account_rate_pct * (comp/100) * 100) / 100;
      return {
        rep_id: i.rep_id, region: i.region,
        multithread_risk: r, multithread_pattern: pat, multithread_severity: sev, recommended_action: act,
        depth_score: de, coverage_score: co, quality_score: qu, network_score: ne,
        multithread_composite: comp,
        has_multithread_gap: comp >= 40 || i.single_threaded_account_rate_pct >= 0.40 || i.economic_buyer_engaged_rate_pct <= 0.40,
        requires_expansion_coaching: comp >= 25 || i.avg_contacts_per_account <= 2.5 || i.multi_contact_meeting_rate_pct <= 0.40,
        estimated_vulnerable_pipeline_usd: vuln,
        multithread_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tde=0, tco=0, tqu=0, tne=0, tcomp=0, tvp=0, gc=0, ecc=0;
    for (const r of reps) {
      rc[r.multithread_risk]=(rc[r.multithread_risk]||0)+1; pc[r.multithread_pattern]=(pc[r.multithread_pattern]||0)+1;
      sc[r.multithread_severity]=(sc[r.multithread_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      tde+=r.depth_score; tco+=r.coverage_score; tqu+=r.quality_score; tne+=r.network_score;
      tcomp+=r.multithread_composite; tvp+=r.estimated_vulnerable_pipeline_usd;
      if (r.has_multithread_gap) gc++; if (r.requires_expansion_coaching) ecc++;
    }
    const n = reps.length;
    return NextResponse.json(sealResponse({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_multithread_composite: Math.round(tcomp/n*10)/10,
      multithread_gap_count: gc, expansion_coaching_count: ecc,
      avg_depth_score: Math.round(tde/n*10)/10,
      avg_coverage_score: Math.round(tco/n*10)/10,
      avg_quality_score: Math.round(tqu/n*10)/10,
      avg_network_score: Math.round(tne/n*10)/10,
      total_estimated_vulnerable_pipeline_usd: Math.round(tvp*100)/100,
    }} as Record<string,unknown>));
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-multithreading-depth-relationship-breadth-engine`)).json());
}
