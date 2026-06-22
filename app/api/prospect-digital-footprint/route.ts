import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[prospect-digital-footprint] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockProspects = [
  {
    prospect_id: "p001", company_name: "AcmeCorp", rep_id: "rep_003",
    intent_tier: "buying_now", footprint_pattern: "ready_to_buy",
    engagement_velocity: "surging", prospect_action: "immediate_sdr",
    website_intent_score: 100.0, content_engagement_score: 80.0,
    social_signal_score: 92.0, company_fit_score: 88.0,
    digital_footprint_composite: 90.5, lead_score: 100.0,
    days_to_outreach: 0, is_high_intent: true, needs_immediate_outreach: true,
    company_size_employees: 450, region: "NAMER",
  },
  {
    prospect_id: "p002", company_name: "BlueRidge Systems", rep_id: "rep_001",
    intent_tier: "hot", footprint_pattern: "intent_spiker",
    engagement_velocity: "growing", prospect_action: "warm_outreach",
    website_intent_score: 72.0, content_engagement_score: 48.0,
    social_signal_score: 42.0, company_fit_score: 72.0,
    digital_footprint_composite: 60.4, lead_score: 68.4,
    days_to_outreach: 2, is_high_intent: true, needs_immediate_outreach: false,
    company_size_employees: 280, region: "EMEA",
  },
  {
    prospect_id: "p003", company_name: "Orion Technologies", rep_id: "rep_002",
    intent_tier: "buying_now", footprint_pattern: "competitive_evaluator",
    engagement_velocity: "surging", prospect_action: "executive_touch",
    website_intent_score: 85.0, content_engagement_score: 62.0,
    social_signal_score: 88.0, company_fit_score: 90.0,
    digital_footprint_composite: 80.4, lead_score: 95.4,
    days_to_outreach: 0, is_high_intent: true, needs_immediate_outreach: true,
    company_size_employees: 2200, region: "APAC",
  },
  {
    prospect_id: "p004", company_name: "Sigma Analytics", rep_id: "rep_005",
    intent_tier: "warming", footprint_pattern: "active_researcher",
    engagement_velocity: "growing", prospect_action: "warm_outreach",
    website_intent_score: 32.0, content_engagement_score: 58.0,
    social_signal_score: 28.0, company_fit_score: 64.0,
    digital_footprint_composite: 42.8, lead_score: 50.8,
    days_to_outreach: 7, is_high_intent: false, needs_immediate_outreach: false,
    company_size_employees: 180, region: "NAMER",
  },
  {
    prospect_id: "p005", company_name: "Pinnacle Software", rep_id: "rep_007",
    intent_tier: "cold", footprint_pattern: "passive_lurker",
    engagement_velocity: "declining", prospect_action: "nurture",
    website_intent_score: 8.0, content_engagement_score: 12.0,
    social_signal_score: 5.0, company_fit_score: 48.0,
    digital_footprint_composite: 11.0, lead_score: 1.0,
    days_to_outreach: 21, is_high_intent: false, needs_immediate_outreach: false,
    company_size_employees: 90, region: "EMEA",
  },
  {
    prospect_id: "p006", company_name: "Vector Cloud", rep_id: "rep_004",
    intent_tier: "warming", footprint_pattern: "content_consumer",
    engagement_velocity: "flat", prospect_action: "nurture",
    website_intent_score: 18.0, content_engagement_score: 38.0,
    social_signal_score: 18.0, company_fit_score: 56.0,
    digital_footprint_composite: 27.5, lead_score: 27.5,
    days_to_outreach: 7, is_high_intent: false, needs_immediate_outreach: false,
    company_size_employees: 350, region: "LATAM",
  },
  {
    prospect_id: "p007", company_name: "Nexus Health", rep_id: "rep_006",
    intent_tier: "hot", footprint_pattern: "active_researcher",
    engagement_velocity: "growing", prospect_action: "warm_outreach",
    website_intent_score: 52.0, content_engagement_score: 60.0,
    social_signal_score: 38.0, company_fit_score: 78.0,
    digital_footprint_composite: 57.6, lead_score: 65.6,
    days_to_outreach: 2, is_high_intent: true, needs_immediate_outreach: false,
    company_size_employees: 620, region: "NAMER",
  },
  {
    prospect_id: "p008", company_name: "DataStream Inc", rep_id: "rep_008",
    intent_tier: "buying_now", footprint_pattern: "ready_to_buy",
    engagement_velocity: "surging", prospect_action: "executive_touch",
    website_intent_score: 95.0, content_engagement_score: 74.0,
    social_signal_score: 72.0, company_fit_score: 94.0,
    digital_footprint_composite: 85.8, lead_score: 100.0,
    days_to_outreach: 0, is_high_intent: true, needs_immediate_outreach: true,
    company_size_employees: 1500, region: "EMEA",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier    = searchParams.get("tier");
  const pattern = searchParams.get("pattern");
  const region  = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/prospect-digital-footprint`);
      if (tier)    url.searchParams.set("tier", tier);
      if (pattern) url.searchParams.set("pattern", pattern);
      if (region)  url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let prospects = [...mockProspects];
  if (tier)    prospects = prospects.filter((p) => p.intent_tier === tier);
  if (pattern) prospects = prospects.filter((p) => p.footprint_pattern === pattern);
  if (region)  prospects = prospects.filter((p) => p.region === region);

  const tier_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const velocity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_lead = 0, total_web = 0,
      total_cont = 0, total_soc = 0, total_fit = 0;

  for (const p of mockProspects) {
    tier_counts[p.intent_tier]          = (tier_counts[p.intent_tier] || 0) + 1;
    pattern_counts[p.footprint_pattern] = (pattern_counts[p.footprint_pattern] || 0) + 1;
    velocity_counts[p.engagement_velocity] = (velocity_counts[p.engagement_velocity] || 0) + 1;
    action_counts[p.prospect_action]    = (action_counts[p.prospect_action] || 0) + 1;
    total_comp += p.digital_footprint_composite;
    total_lead += p.lead_score;
    total_web  += p.website_intent_score;
    total_cont += p.content_engagement_score;
    total_soc  += p.social_signal_score;
    total_fit  += p.company_fit_score;
  }

  const n = mockProspects.length;

  return sealResponse(NextResponse.json({
    prospects,
    summary: {
      total: n,
      tier_counts,
      pattern_counts,
      velocity_counts,
      action_counts,
      avg_digital_footprint_composite: Math.round((total_comp / n) * 10) / 10,
      avg_lead_score:                  Math.round((total_lead / n) * 10) / 10,
      high_intent_count:               mockProspects.filter((p) => p.is_high_intent).length,
      immediate_outreach_count:        mockProspects.filter((p) => p.needs_immediate_outreach).length,
      avg_website_intent_score:        Math.round((total_web / n) * 10) / 10,
      avg_content_engagement_score:    Math.round((total_cont / n) * 10) / 10,
      avg_social_signal_score:         Math.round((total_soc / n) * 10) / 10,
      avg_company_fit_score:           Math.round((total_fit / n) * 10) / 10,
    },
  }));
}
