import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockTerritories = [
  {
    territory_id: "terr_001", territory_name: "NAMER West Tech", rep_id: "rep_003",
    whitespace_priority: "urgent", whitespace_type: "geo_expand",
    territory_health: "underpenetrated", whitespace_action: "immediate_focus",
    opportunity_density_score: 90.0, market_timing_score: 95.0,
    territory_coverage_score: 88.0, icp_alignment_score: 85.0,
    whitespace_composite: 89.5, estimated_whitespace_arr: 6800000,
    territory_penetration_pct: 11.0, is_high_potential_territory: true,
    needs_immediate_prospecting: true, region: "NAMER",
  },
  {
    territory_id: "terr_002", territory_name: "EMEA Financial Services", rep_id: "rep_001",
    whitespace_priority: "high", whitespace_type: "segment_expand",
    territory_health: "developing", whitespace_action: "prioritize",
    opportunity_density_score: 65.0, market_timing_score: 72.0,
    territory_coverage_score: 70.0, icp_alignment_score: 68.0,
    whitespace_composite: 68.7, estimated_whitespace_arr: 3200000,
    territory_penetration_pct: 24.0, is_high_potential_territory: true,
    needs_immediate_prospecting: false, region: "EMEA",
  },
  {
    territory_id: "terr_003", territory_name: "APAC SMB Growth", rep_id: "rep_002",
    whitespace_priority: "urgent", whitespace_type: "new_logo",
    territory_health: "underpenetrated", whitespace_action: "immediate_focus",
    opportunity_density_score: 85.0, market_timing_score: 85.0,
    territory_coverage_score: 92.0, icp_alignment_score: 78.0,
    whitespace_composite: 85.0, estimated_whitespace_arr: 4500000,
    territory_penetration_pct: 8.0, is_high_potential_territory: true,
    needs_immediate_prospecting: true, region: "APAC",
  },
  {
    territory_id: "terr_004", territory_name: "NAMER Mid-Market East", rep_id: "rep_005",
    whitespace_priority: "medium", whitespace_type: "product_expand",
    territory_health: "optimized", whitespace_action: "prospect",
    opportunity_density_score: 45.0, market_timing_score: 55.0,
    territory_coverage_score: 42.0, icp_alignment_score: 60.0,
    whitespace_composite: 49.8, estimated_whitespace_arr: 1800000,
    territory_penetration_pct: 42.0, is_high_potential_territory: false,
    needs_immediate_prospecting: false, region: "NAMER",
  },
  {
    territory_id: "terr_005", territory_name: "LATAM Enterprise", rep_id: "rep_007",
    whitespace_priority: "high", whitespace_type: "geo_expand",
    territory_health: "developing", whitespace_action: "prioritize",
    opportunity_density_score: 72.0, market_timing_score: 65.0,
    territory_coverage_score: 78.0, icp_alignment_score: 55.0,
    whitespace_composite: 68.1, estimated_whitespace_arr: 2900000,
    territory_penetration_pct: 18.0, is_high_potential_territory: true,
    needs_immediate_prospecting: false, region: "LATAM",
  },
  {
    territory_id: "terr_006", territory_name: "EMEA DACH Region", rep_id: "rep_004",
    whitespace_priority: "low", whitespace_type: "dormant_reactivate",
    territory_health: "saturated", whitespace_action: "nurture",
    opportunity_density_score: 22.0, market_timing_score: 40.0,
    territory_coverage_score: 18.0, icp_alignment_score: 45.0,
    whitespace_composite: 29.4, estimated_whitespace_arr: 620000,
    territory_penetration_pct: 75.0, is_high_potential_territory: false,
    needs_immediate_prospecting: false, region: "EMEA",
  },
  {
    territory_id: "terr_007", territory_name: "NAMER Federal Vertical", rep_id: "rep_006",
    whitespace_priority: "urgent", whitespace_type: "segment_expand",
    territory_health: "underpenetrated", whitespace_action: "immediate_focus",
    opportunity_density_score: 88.0, market_timing_score: 90.0,
    territory_coverage_score: 85.0, icp_alignment_score: 80.0,
    whitespace_composite: 86.1, estimated_whitespace_arr: 7200000,
    territory_penetration_pct: 6.0, is_high_potential_territory: true,
    needs_immediate_prospecting: true, region: "NAMER",
  },
  {
    territory_id: "terr_008", territory_name: "APAC Healthcare & Life Sciences", rep_id: "rep_008",
    whitespace_priority: "medium", whitespace_type: "product_expand",
    territory_health: "developing", whitespace_action: "prospect",
    opportunity_density_score: 50.0, market_timing_score: 60.0,
    territory_coverage_score: 48.0, icp_alignment_score: 58.0,
    whitespace_composite: 53.4, estimated_whitespace_arr: 2100000,
    territory_penetration_pct: 22.0, is_high_potential_territory: false,
    needs_immediate_prospecting: false, region: "APAC",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const priority = searchParams.get("priority");
  const type     = searchParams.get("type");
  const region   = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/territory-whitespace`);
      if (priority) url.searchParams.set("priority", priority);
      if (type)     url.searchParams.set("type", type);
      if (region)   url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let territories = [...mockTerritories];
  if (priority) territories = territories.filter((t) => t.whitespace_priority === priority);
  if (type)     territories = territories.filter((t) => t.whitespace_type === type);
  if (region)   territories = territories.filter((t) => t.region === region);

  const priority_counts: Record<string, number> = {};
  const type_counts:     Record<string, number> = {};
  const health_counts:   Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_opp = 0, total_timing = 0, total_cov = 0, total_icp = 0;
  let total_arr  = 0;

  for (const t of mockTerritories) {
    priority_counts[t.whitespace_priority] = (priority_counts[t.whitespace_priority] || 0) + 1;
    type_counts[t.whitespace_type]         = (type_counts[t.whitespace_type] || 0) + 1;
    health_counts[t.territory_health]      = (health_counts[t.territory_health] || 0) + 1;
    action_counts[t.whitespace_action]     = (action_counts[t.whitespace_action] || 0) + 1;
    total_comp   += t.whitespace_composite;
    total_opp    += t.opportunity_density_score;
    total_timing += t.market_timing_score;
    total_cov    += t.territory_coverage_score;
    total_icp    += t.icp_alignment_score;
    total_arr    += t.estimated_whitespace_arr;
  }

  const n = mockTerritories.length;

  return NextResponse.json({
    territories,
    summary: {
      total: n,
      priority_counts,
      type_counts,
      health_counts,
      action_counts,
      avg_whitespace_composite:       Math.round((total_comp / n) * 10) / 10,
      total_estimated_whitespace_arr: total_arr,
      high_potential_count:           mockTerritories.filter((t) => t.is_high_potential_territory).length,
      immediate_prospecting_count:    mockTerritories.filter((t) => t.needs_immediate_prospecting).length,
      avg_opportunity_density_score:  Math.round((total_opp / n) * 10) / 10,
      avg_market_timing_score:        Math.round((total_timing / n) * 10) / 10,
      avg_territory_coverage_score:   Math.round((total_cov / n) * 10) / 10,
      avg_icp_alignment_score:        Math.round((total_icp / n) * 10) / 10,
    },
  });
}
