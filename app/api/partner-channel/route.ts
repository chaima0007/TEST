import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[partner-channel] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockPartners = [
  {
    partner_id: "p_001",
    partner_name: "TechAlliance EMEA",
    partner_type: "co_sell",
    current_tier: "gold",
    recommended_tier: "gold",
    region: "EMEA",
    channel_health: "excellent",
    partner_action: "invest_and_grow",
    engagement_score: 82.5,
    performance_score: 78.3,
    pipeline_contribution: 150.0,
    win_rate: 0.75,
    certification_rate: 0.667,
    quota_attainment: 93.3,
    is_strategic: true,
    needs_intervention: false,
    closed_won_value: 280000,
    pipeline_value: 450000,
    deals_registered: 15,
    deals_closed_won: 9,
    joint_campaigns: 3,
    nps_score: 42,
    years_as_partner: 3.0,
  },
  {
    partner_id: "p_002",
    partner_name: "GlobalSI Partners",
    partner_type: "si",
    current_tier: "platinum",
    recommended_tier: "platinum",
    region: "Americas",
    channel_health: "excellent",
    partner_action: "invest_and_grow",
    engagement_score: 91.2,
    performance_score: 88.7,
    pipeline_contribution: 220.0,
    win_rate: 0.818,
    certification_rate: 0.9,
    quota_attainment: 115.0,
    is_strategic: true,
    needs_intervention: false,
    closed_won_value: 520000,
    pipeline_value: 660000,
    deals_registered: 22,
    deals_closed_won: 18,
    joint_campaigns: 5,
    nps_score: 68,
    years_as_partner: 5.5,
  },
  {
    partner_id: "p_003",
    partner_name: "MidMarket Resellers",
    partner_type: "reseller",
    current_tier: "silver",
    recommended_tier: "gold",
    region: "EMEA",
    channel_health: "healthy",
    partner_action: "joint_campaign",
    engagement_score: 63.8,
    performance_score: 61.4,
    pipeline_contribution: 95.0,
    win_rate: 0.556,
    certification_rate: 0.5,
    quota_attainment: 78.2,
    is_strategic: false,
    needs_intervention: false,
    closed_won_value: 150000,
    pipeline_value: 285000,
    deals_registered: 10,
    deals_closed_won: 5,
    joint_campaigns: 0,
    nps_score: 25,
    years_as_partner: 2.0,
  },
  {
    partner_id: "p_004",
    partner_name: "APAC Growth Network",
    partner_type: "referral",
    current_tier: "gold",
    recommended_tier: "silver",
    region: "APAC",
    channel_health: "needs_attention",
    partner_action: "enable_and_train",
    engagement_score: 38.2,
    performance_score: 42.1,
    pipeline_contribution: 55.0,
    win_rate: 0.4,
    certification_rate: 0.25,
    quota_attainment: 52.4,
    is_strategic: false,
    needs_intervention: false,
    closed_won_value: 95000,
    pipeline_value: 165000,
    deals_registered: 8,
    deals_closed_won: 4,
    joint_campaigns: 1,
    nps_score: -15,
    years_as_partner: 1.5,
  },
  {
    partner_id: "p_005",
    partner_name: "Legacy Distributor SA",
    partner_type: "distributor",
    current_tier: "silver",
    recommended_tier: "bronze",
    region: "EMEA",
    channel_health: "at_risk",
    partner_action: "review_and_reset",
    engagement_score: 22.5,
    performance_score: 28.9,
    pipeline_contribution: 30.0,
    win_rate: 0.25,
    certification_rate: 0.167,
    quota_attainment: 31.5,
    is_strategic: false,
    needs_intervention: true,
    closed_won_value: 42000,
    pipeline_value: 90000,
    deals_registered: 5,
    deals_closed_won: 2,
    joint_campaigns: 0,
    nps_score: -40,
    years_as_partner: 4.0,
  },
  {
    partner_id: "p_006",
    partner_name: "CloudTech Solutions",
    partner_type: "technology",
    current_tier: "gold",
    recommended_tier: "gold",
    region: "Americas",
    channel_health: "healthy",
    partner_action: "invest_and_grow",
    engagement_score: 72.0,
    performance_score: 69.5,
    pipeline_contribution: 108.0,
    win_rate: 0.636,
    certification_rate: 0.75,
    quota_attainment: 88.5,
    is_strategic: true,
    needs_intervention: false,
    closed_won_value: 195000,
    pipeline_value: 324000,
    deals_registered: 11,
    deals_closed_won: 7,
    joint_campaigns: 2,
    nps_score: 38,
    years_as_partner: 2.5,
  },
  {
    partner_id: "p_007",
    partner_name: "Dormant Partners Inc",
    partner_type: "reseller",
    current_tier: "bronze",
    recommended_tier: "prospect",
    region: "APAC",
    channel_health: "inactive",
    partner_action: "offboard",
    engagement_score: 5.0,
    performance_score: 8.3,
    pipeline_contribution: 0.0,
    win_rate: 0.0,
    certification_rate: 0.0,
    quota_attainment: 0.0,
    is_strategic: false,
    needs_intervention: true,
    closed_won_value: 0,
    pipeline_value: 0,
    deals_registered: 0,
    deals_closed_won: 0,
    joint_campaigns: 0,
    nps_score: -80,
    years_as_partner: 0.5,
  },
  {
    partner_id: "p_008",
    partner_name: "NewAge Referrals",
    partner_type: "referral",
    current_tier: "bronze",
    recommended_tier: "silver",
    region: "Americas",
    channel_health: "needs_attention",
    partner_action: "joint_campaign",
    engagement_score: 49.5,
    performance_score: 44.2,
    pipeline_contribution: 70.0,
    win_rate: 0.5,
    certification_rate: 0.333,
    quota_attainment: 65.8,
    is_strategic: false,
    needs_intervention: false,
    closed_won_value: 85000,
    pipeline_value: 210000,
    deals_registered: 7,
    deals_closed_won: 3,
    joint_campaigns: 0,
    nps_score: 10,
    years_as_partner: 0.8,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier    = searchParams.get("tier");
  const health  = searchParams.get("health");
  const region  = searchParams.get("region");
  const type    = searchParams.get("type");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/partner-channel`);
      if (tier)   url.searchParams.set("tier", tier);
      if (health) url.searchParams.set("health", health);
      if (region) url.searchParams.set("region", region);
      if (type)   url.searchParams.set("type", type);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let partners = [...mockPartners];
  if (tier)   partners = partners.filter((p) => p.current_tier === tier);
  if (health) partners = partners.filter((p) => p.channel_health === health);
  if (region) partners = partners.filter((p) => p.region === region);
  if (type)   partners = partners.filter((p) => p.partner_type === type);

  const tier_counts:   Record<string, number> = {};
  const type_counts:   Record<string, number> = {};
  const health_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_eng = 0, total_perf = 0, total_wr = 0, total_qa = 0;

  for (const p of mockPartners) {
    tier_counts[p.current_tier]      = (tier_counts[p.current_tier] || 0) + 1;
    type_counts[p.partner_type]      = (type_counts[p.partner_type] || 0) + 1;
    health_counts[p.channel_health]  = (health_counts[p.channel_health] || 0) + 1;
    action_counts[p.partner_action]  = (action_counts[p.partner_action] || 0) + 1;
    total_eng  += p.engagement_score;
    total_perf += p.performance_score;
    total_wr   += p.win_rate;
    total_qa   += p.quota_attainment;
  }

  const n = mockPartners.length;

  return sealResponse(NextResponse.json({
    partners,
    summary: {
      total:                    n,
      tier_counts,
      type_counts,
      health_counts,
      action_counts,
      avg_engagement_score:     Math.round((total_eng / n) * 10) / 10,
      avg_performance_score:    Math.round((total_perf / n) * 10) / 10,
      avg_win_rate:             Math.round((total_wr / n) * 1000) / 1000,
      avg_quota_attainment:     Math.round((total_qa / n) * 10) / 10,
      strategic_count:          mockPartners.filter((p) => p.is_strategic).length,
      at_risk_count:            mockPartners.filter((p) => ["at_risk", "inactive"].includes(p.channel_health)).length,
      top_performer_count:      mockPartners.filter((p) => ["excellent", "healthy"].includes(p.channel_health)).length,
      needs_intervention_count: mockPartners.filter((p) => p.needs_intervention).length,
    },
  }));
}
