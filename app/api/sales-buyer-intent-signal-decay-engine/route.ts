import { NextResponse } from "next/server";

const MOCK_REPS = [
  { rep_id:"BI-001", region:"EMEA",  evaluation_period_id:"Q1-2026", website_visit_decay_rate_pct:0.68, email_open_rate_decay_pct:0.62, content_download_decay_rate_pct:0.58, avg_days_since_last_digital_touch:28.0, demo_no_show_rate_pct:0.62, demo_follow_up_response_rate_pct:0.18, evaluation_activity_score:0.15, trial_feature_adoption_rate_pct:0.12, champion_response_latency_days:16.0, champion_meeting_acceptance_rate_pct:0.18, champion_internal_forward_rate_pct:0.08, intent_score_trend:-0.72, buying_committee_engagement_score:0.16, multi_contact_engagement_rate_pct:0.12, days_since_last_positive_signal:52.0, intent_data_coverage_score:0.18, deals_with_intent_decay:12, avg_deal_value_usd:92000 },
  { rep_id:"BI-002", region:"NAMER", evaluation_period_id:"Q1-2026", website_visit_decay_rate_pct:0.10, email_open_rate_decay_pct:0.08, content_download_decay_rate_pct:0.10, avg_days_since_last_digital_touch:3.0, demo_no_show_rate_pct:0.08, demo_follow_up_response_rate_pct:0.88, evaluation_activity_score:0.88, trial_feature_adoption_rate_pct:0.82, champion_response_latency_days:1.2, champion_meeting_acceptance_rate_pct:0.88, champion_internal_forward_rate_pct:0.72, intent_score_trend:0.72, buying_committee_engagement_score:0.88, multi_contact_engagement_rate_pct:0.82, days_since_last_positive_signal:2.0, intent_data_coverage_score:0.88, deals_with_intent_decay:2, avg_deal_value_usd:115000 },
  { rep_id:"BI-003", region:"APAC",  evaluation_period_id:"Q1-2026", website_visit_decay_rate_pct:0.42, email_open_rate_decay_pct:0.38, content_download_decay_rate_pct:0.35, avg_days_since_last_digital_touch:16.0, demo_no_show_rate_pct:0.35, demo_follow_up_response_rate_pct:0.48, evaluation_activity_score:0.48, trial_feature_adoption_rate_pct:0.42, champion_response_latency_days:7.5, champion_meeting_acceptance_rate_pct:0.48, champion_internal_forward_rate_pct:0.28, intent_score_trend:-0.35, buying_committee_engagement_score:0.45, multi_contact_engagement_rate_pct:0.38, days_since_last_positive_signal:22.0, intent_data_coverage_score:0.48, deals_with_intent_decay:8, avg_deal_value_usd:78000 },
  { rep_id:"BI-004", region:"LATAM", evaluation_period_id:"Q1-2026", website_visit_decay_rate_pct:0.05, email_open_rate_decay_pct:0.05, content_download_decay_rate_pct:0.05, avg_days_since_last_digital_touch:1.5, demo_no_show_rate_pct:0.05, demo_follow_up_response_rate_pct:0.92, evaluation_activity_score:0.92, trial_feature_adoption_rate_pct:0.88, champion_response_latency_days:0.8, champion_meeting_acceptance_rate_pct:0.92, champion_internal_forward_rate_pct:0.80, intent_score_trend:0.85, buying_committee_engagement_score:0.92, multi_contact_engagement_rate_pct:0.88, days_since_last_positive_signal:1.0, intent_data_coverage_score:0.92, deals_with_intent_decay:1, avg_deal_value_usd:65000 },
  { rep_id:"BI-005", region:"EMEA",  evaluation_period_id:"Q1-2026", website_visit_decay_rate_pct:0.58, email_open_rate_decay_pct:0.55, content_download_decay_rate_pct:0.52, avg_days_since_last_digital_touch:32.0, demo_no_show_rate_pct:0.55, demo_follow_up_response_rate_pct:0.20, evaluation_activity_score:0.18, trial_feature_adoption_rate_pct:0.15, champion_response_latency_days:12.0, champion_meeting_acceptance_rate_pct:0.22, champion_internal_forward_rate_pct:0.10, intent_score_trend:-0.65, buying_committee_engagement_score:0.20, multi_contact_engagement_rate_pct:0.15, days_since_last_positive_signal:48.0, intent_data_coverage_score:0.22, deals_with_intent_decay:15, avg_deal_value_usd:108000 },
  { rep_id:"BI-006", region:"NAMER", evaluation_period_id:"Q1-2026", website_visit_decay_rate_pct:0.28, email_open_rate_decay_pct:0.25, content_download_decay_rate_pct:0.22, avg_days_since_last_digital_touch:10.0, demo_no_show_rate_pct:0.22, demo_follow_up_response_rate_pct:0.65, evaluation_activity_score:0.65, trial_feature_adoption_rate_pct:0.60, champion_response_latency_days:4.5, champion_meeting_acceptance_rate_pct:0.65, champion_internal_forward_rate_pct:0.48, intent_score_trend:-0.18, buying_committee_engagement_score:0.62, multi_contact_engagement_rate_pct:0.58, days_since_last_positive_signal:12.0, intent_data_coverage_score:0.65, deals_with_intent_decay:4, avg_deal_value_usd:88000 },
  { rep_id:"BI-007", region:"APAC",  evaluation_period_id:"Q1-2026", website_visit_decay_rate_pct:0.78, email_open_rate_decay_pct:0.72, content_download_decay_rate_pct:0.68, avg_days_since_last_digital_touch:42.0, demo_no_show_rate_pct:0.72, demo_follow_up_response_rate_pct:0.12, evaluation_activity_score:0.10, trial_feature_adoption_rate_pct:0.08, champion_response_latency_days:22.0, champion_meeting_acceptance_rate_pct:0.12, champion_internal_forward_rate_pct:0.05, intent_score_trend:-0.85, buying_committee_engagement_score:0.10, multi_contact_engagement_rate_pct:0.08, days_since_last_positive_signal:65.0, intent_data_coverage_score:0.12, deals_with_intent_decay:18, avg_deal_value_usd:125000 },
  { rep_id:"BI-008", region:"MEA",   evaluation_period_id:"Q1-2026", website_visit_decay_rate_pct:0.35, email_open_rate_decay_pct:0.32, content_download_decay_rate_pct:0.28, avg_days_since_last_digital_touch:14.0, demo_no_show_rate_pct:0.28, demo_follow_up_response_rate_pct:0.55, evaluation_activity_score:0.55, trial_feature_adoption_rate_pct:0.50, champion_response_latency_days:6.0, champion_meeting_acceptance_rate_pct:0.55, champion_internal_forward_rate_pct:0.35, intent_score_trend:-0.25, buying_committee_engagement_score:0.52, multi_contact_engagement_rate_pct:0.48, days_since_last_positive_signal:18.0, intent_data_coverage_score:0.55, deals_with_intent_decay:6, avg_deal_value_usd:72000 },
];

type Rep = typeof MOCK_REPS[0];

function engagementScore(i: Rep): number {
  let s = 0;
  if      (i.website_visit_decay_rate_pct         >= 0.60) s += 40; else if (i.website_visit_decay_rate_pct >= 0.35) s += 22; else if (i.website_visit_decay_rate_pct >= 0.18) s += 8;
  if      (i.email_open_rate_decay_pct            >= 0.55) s += 35; else if (i.email_open_rate_decay_pct >= 0.30) s += 18;
  if      (i.avg_days_since_last_digital_touch    >= 30)   s += 25; else if (i.avg_days_since_last_digital_touch >= 14) s += 12;
  return Math.min(s, 100);
}
function signalScore(i: Rep): number {
  let s = 0;
  if      (i.intent_score_trend                    <= -0.60) s += 45; else if (i.intent_score_trend <= -0.30) s += 25; else if (i.intent_score_trend <= -0.10) s += 10;
  if      (i.buying_committee_engagement_score     <= 0.20) s += 30; else if (i.buying_committee_engagement_score <= 0.45) s += 15;
  if      (i.multi_contact_engagement_rate_pct     <= 0.15) s += 25; else if (i.multi_contact_engagement_rate_pct <= 0.35) s += 12;
  return Math.min(s, 100);
}
function championScore(i: Rep): number {
  let s = 0;
  if      (i.champion_response_latency_days        >= 14.0) s += 40; else if (i.champion_response_latency_days >= 7.0) s += 22; else if (i.champion_response_latency_days >= 3.5) s += 8;
  if      (i.champion_meeting_acceptance_rate_pct  <= 0.20) s += 35; else if (i.champion_meeting_acceptance_rate_pct <= 0.45) s += 18;
  if      (i.champion_internal_forward_rate_pct    <= 0.10) s += 25; else if (i.champion_internal_forward_rate_pct <= 0.25) s += 12;
  return Math.min(s, 100);
}
function freshnessScore(i: Rep): number {
  let s = 0;
  if      (i.days_since_last_positive_signal       >= 45)  s += 45; else if (i.days_since_last_positive_signal >= 21) s += 25; else if (i.days_since_last_positive_signal >= 10) s += 10;
  if      (i.content_download_decay_rate_pct       >= 0.55) s += 30; else if (i.content_download_decay_rate_pct >= 0.30) s += 15;
  if      (i.intent_data_coverage_score            <= 0.20) s += 25; else if (i.intent_data_coverage_score <= 0.45) s += 12;
  return Math.min(s, 100);
}
function composite(en: number, si: number, ch: number, fr: number): number {
  return Math.min(Math.round((en * 0.30 + si * 0.25 + ch * 0.25 + fr * 0.20) * 100) / 100, 100);
}
function pattern(i: Rep): string {
  if (i.website_visit_decay_rate_pct >= 0.55 && i.avg_days_since_last_digital_touch >= 21)       return "digital_ghost";
  if (i.content_download_decay_rate_pct >= 0.50 && i.buying_committee_engagement_score <= 0.25)   return "content_disengagement";
  if (i.demo_no_show_rate_pct >= 0.50 && i.demo_follow_up_response_rate_pct <= 0.25)              return "demo_dropout";
  if (i.champion_response_latency_days >= 10.0 && i.champion_meeting_acceptance_rate_pct <= 0.25) return "champion_signal_fade";
  if (i.evaluation_activity_score <= 0.20 && i.trial_feature_adoption_rate_pct <= 0.20)           return "evaluation_abandonment";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "cold"; if (c >= 40) return "cooling"; if (c >= 20) return "warming"; return "engaged"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "digital_ghost" || p === "evaluation_abandonment") return "pipeline_purge_recommendation";
    if (p === "champion_signal_fade") return "executive_reconnect_protocol";
    return "deal_rescue_intervention";
  }
  if (r === "high") {
    if (p === "digital_ghost")           return "re_engagement_outreach";
    if (p === "content_disengagement")   return "content_nurture_activation";
    if (p === "demo_dropout")            return "demo_reactivation_campaign";
    if (p === "champion_signal_fade")    return "champion_reactivation_call";
    if (p === "evaluation_abandonment")  return "deal_rescue_intervention";
    return "intent_monitoring";
  }
  if (r === "moderate") return "intent_monitoring";
  return "no_action";
}
function signal(i: Rep, pat: string, comp: number): string {
  if (comp < 20) return "Buyer intent signals healthy — digital engagement, champion activity, and signal freshness within benchmark targets";
  const labels: Record<string,string> = { digital_ghost:"Digital ghost", content_disengagement:"Content disengagement", demo_dropout:"Demo dropout", champion_signal_fade:"Champion signal fade", evaluation_abandonment:"Evaluation abandonment" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${Math.round(i.website_visit_decay_rate_pct*100)}% web visit decay — ${Math.round(i.days_since_last_positive_signal)} days since positive signal — ${i.champion_response_latency_days.toFixed(1)}d champion latency — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const reps = MOCK_REPS.map(i => {
      const en = engagementScore(i), si = signalScore(i), ch = championScore(i), fr = freshnessScore(i);
      const comp = composite(en, si, ch, fr), pat = pattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      const cold = Math.round(i.deals_with_intent_decay * i.avg_deal_value_usd * (1 - Math.max(i.buying_committee_engagement_score, 0.05)) * (comp/100) * 100) / 100;
      return {
        rep_id: i.rep_id, region: i.region,
        intent_risk: r, intent_pattern: pat, intent_severity: sev, recommended_action: act,
        engagement_score: en, signal_score: si, champion_score: ch, freshness_score: fr,
        intent_composite: comp,
        has_intent_gap: comp >= 40 || i.days_since_last_positive_signal >= 21 || i.buying_committee_engagement_score <= 0.35,
        requires_reengagement: comp >= 25 || i.champion_response_latency_days >= 7.0 || i.website_visit_decay_rate_pct >= 0.30,
        estimated_cold_pipeline_usd: cold,
        intent_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let ten=0, tsi=0, tch=0, tfr=0, tcomp=0, tcp=0, gc=0, re=0;
    for (const r of reps) {
      rc[r.intent_risk]=(rc[r.intent_risk]||0)+1; pc[r.intent_pattern]=(pc[r.intent_pattern]||0)+1;
      sc[r.intent_severity]=(sc[r.intent_severity]||0)+1; ac[r.recommended_action]=(ac[r.recommended_action]||0)+1;
      ten+=r.engagement_score; tsi+=r.signal_score; tch+=r.champion_score; tfr+=r.freshness_score;
      tcomp+=r.intent_composite; tcp+=r.estimated_cold_pipeline_usd;
      if (r.has_intent_gap) gc++; if (r.requires_reengagement) re++;
    }
    const n = reps.length;
    return NextResponse.json({ reps, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_intent_composite: Math.round(tcomp/n*10)/10,
      intent_gap_count: gc, reengagement_count: re,
      avg_engagement_score: Math.round(ten/n*10)/10,
      avg_signal_score: Math.round(tsi/n*10)/10,
      avg_champion_score: Math.round(tch/n*10)/10,
      avg_freshness_score: Math.round(tfr/n*10)/10,
      total_estimated_cold_pipeline_usd: Math.round(tcp*100)/100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/sales-buyer-intent-signal-decay-engine`)).json());
}
