import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-social-selling-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    social_selling_risk: "low", social_selling_pattern: "none",
    social_selling_severity: "active", recommended_action: "no_action",
    profile_presence_score: 0.0, content_effectiveness_score: 0.0,
    prospect_engagement_score: 0.0, social_pipeline_score: 0.0,
    social_selling_composite: 0.0,
    has_social_gap: false, requires_social_coaching: false,
    estimated_pipeline_loss_usd: 0.0,
    social_selling_signal: "Social selling performance healthy — prospect engagement, content reach, and pipeline generation within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    social_selling_risk: "low", social_selling_pattern: "none",
    social_selling_severity: "active", recommended_action: "no_action",
    profile_presence_score: 4.0, content_effectiveness_score: 3.0,
    prospect_engagement_score: 5.0, social_pipeline_score: 2.0,
    social_selling_composite: 3.55,
    has_social_gap: false, requires_social_coaching: false,
    estimated_pipeline_loss_usd: 0.0,
    social_selling_signal: "Social selling performance healthy — prospect engagement, content reach, and pipeline generation within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    social_selling_risk: "moderate", social_selling_pattern: "content_inconsistency",
    social_selling_severity: "developing", recommended_action: "social_presence_coaching",
    profile_presence_score: 15.0, content_effectiveness_score: 30.0,
    prospect_engagement_score: 18.0, social_pipeline_score: 20.0,
    social_selling_composite: 20.9,
    has_social_gap: false, requires_social_coaching: true,
    estimated_pipeline_loss_usd: 7560.0,
    social_selling_signal: "Content inconsistency — SSI 42 — 2 posts/mo — 1 social meetings — composite 21",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    social_selling_risk: "moderate", social_selling_pattern: "low_prospect_engagement",
    social_selling_severity: "developing", recommended_action: "social_presence_coaching",
    profile_presence_score: 20.0, content_effectiveness_score: 22.0,
    prospect_engagement_score: 38.0, social_pipeline_score: 15.0,
    social_selling_composite: 24.45,
    has_social_gap: false, requires_social_coaching: true,
    estimated_pipeline_loss_usd: 10584.0,
    social_selling_signal: "Low prospect engagement — SSI 38 — 3 posts/mo — 1 social meetings — composite 24",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    social_selling_risk: "high", social_selling_pattern: "inmail_abuse",
    social_selling_severity: "passive", recommended_action: "inmail_optimization",
    profile_presence_score: 35.0, content_effectiveness_score: 28.0,
    prospect_engagement_score: 45.0, social_pipeline_score: 40.0,
    social_selling_composite: 37.5,
    has_social_gap: true, requires_social_coaching: true,
    estimated_pipeline_loss_usd: 34020.0,
    social_selling_signal: "Inmail abuse — SSI 28 — 1 posts/mo — 0 social meetings — composite 38",
  },
  {
    rep_id: "rep_006", region: "West",
    social_selling_risk: "high", social_selling_pattern: "competitor_following",
    social_selling_severity: "passive", recommended_action: "social_presence_coaching",
    profile_presence_score: 42.0, content_effectiveness_score: 38.0,
    prospect_engagement_score: 35.0, social_pipeline_score: 48.0,
    social_selling_composite: 40.8,
    has_social_gap: true, requires_social_coaching: true,
    estimated_pipeline_loss_usd: 45360.0,
    social_selling_signal: "Competitor following — SSI 22 — 0 posts/mo — 0 social meetings — composite 41",
  },
  {
    rep_id: "rep_007", region: "APAC",
    social_selling_risk: "critical", social_selling_pattern: "invisible_online",
    social_selling_severity: "invisible", recommended_action: "brand_building_program",
    profile_presence_score: 70.0, content_effectiveness_score: 65.0,
    prospect_engagement_score: 72.0, social_pipeline_score: 75.0,
    social_selling_composite: 70.7,
    has_social_gap: true, requires_social_coaching: true,
    estimated_pipeline_loss_usd: 22680.0,
    social_selling_signal: "Invisible online — SSI 18 — 0 posts/mo — 0 social meetings — composite 71",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    social_selling_risk: "critical", social_selling_pattern: "invisible_online",
    social_selling_severity: "invisible", recommended_action: "brand_building_program",
    profile_presence_score: 100.0, content_effectiveness_score: 100.0,
    prospect_engagement_score: 100.0, social_pipeline_score: 100.0,
    social_selling_composite: 100.0,
    has_social_gap: true, requires_social_coaching: true,
    estimated_pipeline_loss_usd: 22680.0,
    social_selling_signal: "Invisible online — SSI 10 — 0 posts/mo — 0 social meetings — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-social-selling-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.social_selling_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.social_selling_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_pres = 0, total_cont = 0, total_pros = 0, total_pipe = 0, total_impact = 0;

  for (const r of mockReps) {
    risk_counts[r.social_selling_risk]       = (risk_counts[r.social_selling_risk] || 0) + 1;
    pattern_counts[r.social_selling_pattern] = (pattern_counts[r.social_selling_pattern] || 0) + 1;
    severity_counts[r.social_selling_severity] = (severity_counts[r.social_selling_severity] || 0) + 1;
    action_counts[r.recommended_action]      = (action_counts[r.recommended_action] || 0) + 1;
    total_comp   += r.social_selling_composite;
    total_pres   += r.profile_presence_score;
    total_cont   += r.content_effectiveness_score;
    total_pros   += r.prospect_engagement_score;
    total_pipe   += r.social_pipeline_score;
    total_impact += r.estimated_pipeline_loss_usd;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_social_selling_composite:             Math.round((total_comp / n) * 10) / 10,
      social_gap_count:                         mockReps.filter((r) => r.has_social_gap).length,
      coaching_count:                           mockReps.filter((r) => r.requires_social_coaching).length,
      avg_profile_presence_score:               Math.round((total_pres / n) * 10) / 10,
      avg_content_effectiveness_score:          Math.round((total_cont / n) * 10) / 10,
      avg_prospect_engagement_score:            Math.round((total_pros / n) * 10) / 10,
      avg_social_pipeline_score:                Math.round((total_pipe / n) * 10) / 10,
      total_estimated_pipeline_loss_usd:        Math.round(total_impact * 100) / 100,
    },
  }));
}
