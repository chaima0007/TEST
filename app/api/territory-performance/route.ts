import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockTerritories = [
  {
    territory_id: "t_001", territory_name: "EMEA West", rep_id: "r_001", region: "EMEA",
    territory_status: "on_target", territory_risk: "low",
    market_penetration: "low", territory_action: "expand",
    attainment_pct: 74.2, projected_attainment: 98.3,
    coverage_ratio: 1.0, penetration_pct: 22.0,
    account_health_score: 68.5, activity_score: 52.0, growth_score: 58.2,
    is_at_risk: false, needs_rebalancing: false,
    actual_revenue: 890000, target_revenue: 1200000,
  },
  {
    territory_id: "t_002", territory_name: "NAMER East", rep_id: "r_002", region: "NAMER",
    territory_status: "overperforming", territory_risk: "low",
    market_penetration: "medium", territory_action: "maintain",
    attainment_pct: 92.0, projected_attainment: 118.0,
    coverage_ratio: 1.52, penetration_pct: 38.0,
    account_health_score: 78.0, activity_score: 68.0, growth_score: 72.5,
    is_at_risk: false, needs_rebalancing: false,
    actual_revenue: 1104000, target_revenue: 1200000,
  },
  {
    territory_id: "t_003", territory_name: "APAC South", rep_id: "r_003", region: "APAC",
    territory_status: "underperforming", territory_risk: "high",
    market_penetration: "low", territory_action: "focus",
    attainment_pct: 52.0, projected_attainment: 72.0,
    coverage_ratio: 0.68, penetration_pct: 14.0,
    account_health_score: 42.0, activity_score: 32.0, growth_score: 35.8,
    is_at_risk: true, needs_rebalancing: false,
    actual_revenue: 520000, target_revenue: 1000000,
  },
  {
    territory_id: "t_004", territory_name: "LATAM North", rep_id: "r_004", region: "LATAM",
    territory_status: "critical", territory_risk: "critical",
    market_penetration: "untapped", territory_action: "urgent_intervention",
    attainment_pct: 28.0, projected_attainment: 42.0,
    coverage_ratio: 0.35, penetration_pct: 6.0,
    account_health_score: 22.0, activity_score: 15.0, growth_score: 18.4,
    is_at_risk: true, needs_rebalancing: false,
    actual_revenue: 280000, target_revenue: 1000000,
  },
  {
    territory_id: "t_005", territory_name: "EMEA Central", rep_id: "r_005", region: "EMEA",
    territory_status: "on_target", territory_risk: "medium",
    market_penetration: "medium", territory_action: "maintain",
    attainment_pct: 68.0, projected_attainment: 91.0,
    coverage_ratio: 0.88, penetration_pct: 28.0,
    account_health_score: 58.0, activity_score: 48.0, growth_score: 51.2,
    is_at_risk: false, needs_rebalancing: false,
    actual_revenue: 612000, target_revenue: 900000,
  },
  {
    territory_id: "t_006", territory_name: "NAMER West", rep_id: "r_006", region: "NAMER",
    territory_status: "overperforming", territory_risk: "low",
    market_penetration: "high", territory_action: "maintain",
    attainment_pct: 98.0, projected_attainment: 125.0,
    coverage_ratio: 1.82, penetration_pct: 54.0,
    account_health_score: 85.0, activity_score: 75.0, growth_score: 80.2,
    is_at_risk: false, needs_rebalancing: true,
    actual_revenue: 1176000, target_revenue: 1200000,
  },
  {
    territory_id: "t_007", territory_name: "MEA", rep_id: "r_007", region: "EMEA",
    territory_status: "underperforming", territory_risk: "high",
    market_penetration: "untapped", territory_action: "expand",
    attainment_pct: 38.0, projected_attainment: 76.0,
    coverage_ratio: 0.52, penetration_pct: 5.0,
    account_health_score: 35.0, activity_score: 28.0, growth_score: 30.5,
    is_at_risk: true, needs_rebalancing: false,
    actual_revenue: 342000, target_revenue: 900000,
  },
  {
    territory_id: "t_008", territory_name: "APAC North", rep_id: "r_008", region: "APAC",
    territory_status: "on_target", territory_risk: "medium",
    market_penetration: "medium", territory_action: "expand",
    attainment_pct: 72.0, projected_attainment: 94.0,
    coverage_ratio: 0.95, penetration_pct: 30.0,
    account_health_score: 62.0, activity_score: 55.0, growth_score: 58.8,
    is_at_risk: false, needs_rebalancing: false,
    actual_revenue: 720000, target_revenue: 1000000,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const status  = searchParams.get("status");
  const risk    = searchParams.get("risk");
  const region  = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/territory-performance`);
      if (status) url.searchParams.set("status", status);
      if (risk)   url.searchParams.set("risk", risk);
      if (region) url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let territories = [...mockTerritories];
  if (status) territories = territories.filter((t) => t.territory_status === status);
  if (risk)   territories = territories.filter((t) => t.territory_risk === risk);
  if (region) territories = territories.filter((t) => t.region === region);

  const status_counts:      Record<string, number> = {};
  const risk_counts:        Record<string, number> = {};
  const penetration_counts: Record<string, number> = {};
  const action_counts:      Record<string, number> = {};
  let total_attainment = 0, total_projected = 0, total_health = 0, total_growth = 0;

  for (const t of mockTerritories) {
    status_counts[t.territory_status]     = (status_counts[t.territory_status] || 0) + 1;
    risk_counts[t.territory_risk]         = (risk_counts[t.territory_risk] || 0) + 1;
    penetration_counts[t.market_penetration] = (penetration_counts[t.market_penetration] || 0) + 1;
    action_counts[t.territory_action]     = (action_counts[t.territory_action] || 0) + 1;
    total_attainment += t.attainment_pct;
    total_projected  += t.projected_attainment;
    total_health     += t.account_health_score;
    total_growth     += t.growth_score;
  }

  const n = mockTerritories.length;

  return NextResponse.json({
    territories,
    summary: {
      total:                    n,
      status_counts,
      risk_counts,
      penetration_counts,
      action_counts,
      avg_attainment_pct:       Math.round((total_attainment / n) * 10) / 10,
      avg_projected_attainment: Math.round((total_projected / n) * 10) / 10,
      total_revenue_gap:        mockTerritories.reduce((s, t) => s + Math.max(0, t.target_revenue - t.actual_revenue), 0),
      at_risk_count:            mockTerritories.filter((t) => t.is_at_risk).length,
      rebalancing_count:        mockTerritories.filter((t) => t.needs_rebalancing).length,
      avg_account_health:       Math.round((total_health / n) * 10) / 10,
      avg_growth_score:         Math.round((total_growth / n) * 10) / 10,
      high_performing_count:    mockTerritories.filter((t) =>
        t.territory_status === "overperforming" || t.territory_status === "on_target"
      ).length,
    },
  });
}
