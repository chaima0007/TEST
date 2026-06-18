import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockProspects = [
  {
    prospect_id: "p_001", prospect_name: "Marie Dupont", company_name: "Acme Corp",
    rep_id: "rep_003", region: "EMEA",
    engagement_velocity: "accelerating", intent_level: "hot",
    engagement_risk: "low", engagement_action: "advance",
    email_engagement_score: 100.0, meeting_engagement_score: 100.0,
    digital_engagement_score: 100.0, velocity_trend_score: 95.0,
    engagement_composite: 98.5, days_to_re_engage: 1,
    is_high_intent: true, needs_reactivation: false,
    primary_signal: "pricing page visited — high buying intent",
  },
  {
    prospect_id: "p_002", prospect_name: "James Okafor", company_name: "BetaTech",
    rep_id: "rep_001", region: "NAMER",
    engagement_velocity: "cold", intent_level: "cold",
    engagement_risk: "critical", engagement_action: "disqualify",
    email_engagement_score: 5.0, meeting_engagement_score: 0.0,
    digital_engagement_score: 0.0, velocity_trend_score: 5.0,
    engagement_composite: 2.5, days_to_re_engage: 4,
    is_high_intent: false, needs_reactivation: true,
    primary_signal: "gone dark — reactivation required",
  },
  {
    prospect_id: "p_003", prospect_name: "Sofia Larsson", company_name: "CloudBase",
    rep_id: "rep_002", region: "EMEA",
    engagement_velocity: "steady", intent_level: "warm",
    engagement_risk: "moderate", engagement_action: "nurture",
    email_engagement_score: 60.0, meeting_engagement_score: 55.0,
    digital_engagement_score: 45.0, velocity_trend_score: 60.0,
    engagement_composite: 55.5, days_to_re_engage: 2,
    is_high_intent: false, needs_reactivation: false,
    primary_signal: "strongest signal: email engagement",
  },
  {
    prospect_id: "p_004", prospect_name: "Luca Moretti", company_name: "DeltaLink",
    rep_id: "rep_005", region: "LATAM",
    engagement_velocity: "stalled", intent_level: "lukewarm",
    engagement_risk: "high", engagement_action: "reactivate",
    email_engagement_score: 20.0, meeting_engagement_score: 8.0,
    digital_engagement_score: 15.0, velocity_trend_score: 15.0,
    engagement_composite: 15.0, days_to_re_engage: 5,
    is_high_intent: false, needs_reactivation: true,
    primary_signal: "multiple meetings ghosted — low engagement",
  },
  {
    prospect_id: "p_005", prospect_name: "Yuki Tanaka", company_name: "EcoTech",
    rep_id: "rep_007", region: "APAC",
    engagement_velocity: "accelerating", intent_level: "hot",
    engagement_risk: "low", engagement_action: "advance",
    email_engagement_score: 88.0, meeting_engagement_score: 90.0,
    digital_engagement_score: 85.0, velocity_trend_score: 90.0,
    engagement_composite: 88.5, days_to_re_engage: 1,
    is_high_intent: true, needs_reactivation: false,
    primary_signal: "demo requested — strong interest",
  },
  {
    prospect_id: "p_006", prospect_name: "Elena Vasquez", company_name: "Finova",
    rep_id: "rep_004", region: "LATAM",
    engagement_velocity: "decelerating", intent_level: "lukewarm",
    engagement_risk: "high", engagement_action: "reactivate",
    email_engagement_score: 35.0, meeting_engagement_score: 30.0,
    digital_engagement_score: 20.0, velocity_trend_score: 20.0,
    engagement_composite: 28.0, days_to_re_engage: 5,
    is_high_intent: false, needs_reactivation: true,
    primary_signal: "gone dark — reactivation required",
  },
  {
    prospect_id: "p_007", prospect_name: "Tom Krieger", company_name: "GlobalNet",
    rep_id: "rep_006", region: "NAMER",
    engagement_velocity: "steady", intent_level: "warm",
    engagement_risk: "low", engagement_action: "nurture",
    email_engagement_score: 70.0, meeting_engagement_score: 65.0,
    digital_engagement_score: 58.0, velocity_trend_score: 62.0,
    engagement_composite: 64.8, days_to_re_engage: 2,
    is_high_intent: false, needs_reactivation: false,
    primary_signal: "champion sharing content internally",
  },
  {
    prospect_id: "p_008", prospect_name: "Aisha Mensah", company_name: "HorizonAI",
    rep_id: "rep_008", region: "EMEA",
    engagement_velocity: "steady", intent_level: "warm",
    engagement_risk: "moderate", engagement_action: "nurture",
    email_engagement_score: 52.0, meeting_engagement_score: 48.0,
    digital_engagement_score: 42.0, velocity_trend_score: 55.0,
    engagement_composite: 49.3, days_to_re_engage: 3,
    is_high_intent: false, needs_reactivation: false,
    primary_signal: "strongest signal: email engagement",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const velocity = searchParams.get("velocity");
  const intent   = searchParams.get("intent");
  const region   = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/prospect-engagement-velocity`);
      if (velocity) url.searchParams.set("velocity", velocity);
      if (intent)   url.searchParams.set("intent", intent);
      if (region)   url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let prospects = [...mockProspects];
  if (velocity) prospects = prospects.filter((p) => p.engagement_velocity === velocity);
  if (intent)   prospects = prospects.filter((p) => p.intent_level === intent);
  if (region)   prospects = prospects.filter((p) => p.region === region);

  const v_counts: Record<string, number> = {};
  const i_counts: Record<string, number> = {};
  const r_counts: Record<string, number> = {};
  const a_counts: Record<string, number> = {};
  let total_comp = 0, total_email = 0, total_meet = 0, total_dig = 0, total_vel = 0, total_d2r = 0;

  for (const p of mockProspects) {
    v_counts[p.engagement_velocity] = (v_counts[p.engagement_velocity] || 0) + 1;
    i_counts[p.intent_level]        = (i_counts[p.intent_level] || 0) + 1;
    r_counts[p.engagement_risk]     = (r_counts[p.engagement_risk] || 0) + 1;
    a_counts[p.engagement_action]   = (a_counts[p.engagement_action] || 0) + 1;
    total_comp  += p.engagement_composite;
    total_email += p.email_engagement_score;
    total_meet  += p.meeting_engagement_score;
    total_dig   += p.digital_engagement_score;
    total_vel   += p.velocity_trend_score;
    total_d2r   += p.days_to_re_engage;
  }

  const n = mockProspects.length;

  return NextResponse.json({
    prospects,
    summary: {
      total: n,
      velocity_counts:               v_counts,
      intent_counts:                 i_counts,
      risk_counts:                   r_counts,
      action_counts:                 a_counts,
      avg_engagement_composite:      Math.round((total_comp / n) * 10) / 10,
      high_intent_count:             mockProspects.filter((p) => p.is_high_intent).length,
      reactivation_count:            mockProspects.filter((p) => p.needs_reactivation).length,
      avg_email_engagement_score:    Math.round((total_email / n) * 10) / 10,
      avg_meeting_engagement_score:  Math.round((total_meet / n) * 10) / 10,
      avg_digital_engagement_score:  Math.round((total_dig / n) * 10) / 10,
      avg_velocity_trend_score:      Math.round((total_vel / n) * 10) / 10,
      avg_days_to_re_engage:         Math.round((total_d2r / n) * 10) / 10,
    },
  });
}
