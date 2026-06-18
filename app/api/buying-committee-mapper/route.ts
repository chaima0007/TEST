import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", deal_name: "Acme Corp Enterprise", rep_id: "rep_003",
    committee_coverage: "full_coverage", committee_risk: "low",
    deal_complexity: "enterprise", committee_action: "maintain",
    role_coverage_score: 100.0, engagement_breadth_score: 98.0,
    blocker_management_score: 75.0, late_stage_alignment_score: 100.0,
    committee_composite: 93.9, coverage_ratio: 0.88,
    missing_role_count: 0, is_well_covered: true,
    needs_expansion: false, region: "NAMER",
  },
  {
    deal_id: "deal_002", deal_name: "BetaTech SaaS", rep_id: "rep_001",
    committee_coverage: "single_threaded", committee_risk: "critical",
    deal_complexity: "standard", committee_action: "expand_coverage",
    role_coverage_score: 15.0, engagement_breadth_score: 3.0,
    blocker_management_score: 0.0, late_stage_alignment_score: 0.0,
    committee_composite: 7.2, coverage_ratio: 0.25,
    missing_role_count: 3, is_well_covered: false,
    needs_expansion: true, region: "EMEA",
  },
  {
    deal_id: "deal_003", deal_name: "CloudBase Platform", rep_id: "rep_002",
    committee_coverage: "partial", committee_risk: "moderate",
    deal_complexity: "complex", committee_action: "expand_coverage",
    role_coverage_score: 62.0, engagement_breadth_score: 55.0,
    blocker_management_score: 75.0, late_stage_alignment_score: 48.0,
    committee_composite: 61.4, coverage_ratio: 0.6,
    missing_role_count: 1, is_well_covered: false,
    needs_expansion: false, region: "APAC",
  },
  {
    deal_id: "deal_004", deal_name: "Delta Networks", rep_id: "rep_005",
    committee_coverage: "thin", committee_risk: "high",
    deal_complexity: "standard", committee_action: "neutralize_blocker",
    role_coverage_score: 38.0, engagement_breadth_score: 28.0,
    blocker_management_score: 10.0, late_stage_alignment_score: 22.0,
    committee_composite: 27.6, coverage_ratio: 0.4,
    missing_role_count: 2, is_well_covered: false,
    needs_expansion: true, region: "NAMER",
  },
  {
    deal_id: "deal_005", deal_name: "EcoTech Expansion", rep_id: "rep_007",
    committee_coverage: "full_coverage", committee_risk: "low",
    deal_complexity: "enterprise", committee_action: "maintain",
    role_coverage_score: 88.0, engagement_breadth_score: 85.0,
    blocker_management_score: 80.0, late_stage_alignment_score: 90.0,
    committee_composite: 86.0, coverage_ratio: 0.82,
    missing_role_count: 0, is_well_covered: true,
    needs_expansion: false, region: "EMEA",
  },
  {
    deal_id: "deal_006", deal_name: "Finova Capital", rep_id: "rep_004",
    committee_coverage: "partial", committee_risk: "moderate",
    deal_complexity: "complex", committee_action: "executive_alignment",
    role_coverage_score: 52.0, engagement_breadth_score: 45.0,
    blocker_management_score: 75.0, late_stage_alignment_score: 35.0,
    committee_composite: 54.5, coverage_ratio: 0.55,
    missing_role_count: 1, is_well_covered: false,
    needs_expansion: false, region: "APAC",
  },
  {
    deal_id: "deal_007", deal_name: "GlobalLink Corp", rep_id: "rep_006",
    committee_coverage: "full_coverage", committee_risk: "low",
    deal_complexity: "complex", committee_action: "maintain",
    role_coverage_score: 78.0, engagement_breadth_score: 72.0,
    blocker_management_score: 75.0, late_stage_alignment_score: 68.0,
    committee_composite: 74.4, coverage_ratio: 0.75,
    missing_role_count: 0, is_well_covered: true,
    needs_expansion: false, region: "LATAM",
  },
  {
    deal_id: "deal_008", deal_name: "HorizonAI Platform", rep_id: "rep_008",
    committee_coverage: "thin", committee_risk: "high",
    deal_complexity: "standard", committee_action: "expand_coverage",
    role_coverage_score: 27.0, engagement_breadth_score: 16.0,
    blocker_management_score: 75.0, late_stage_alignment_score: 12.0,
    committee_composite: 32.8, coverage_ratio: 0.33,
    missing_role_count: 2, is_well_covered: false,
    needs_expansion: true, region: "NAMER",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const coverage   = searchParams.get("coverage");
  const risk       = searchParams.get("risk");
  const region     = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/buying-committee-mapper`);
      if (coverage) url.searchParams.set("coverage", coverage);
      if (risk)     url.searchParams.set("risk", risk);
      if (region)   url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (coverage) deals = deals.filter((d) => d.committee_coverage === coverage);
  if (risk)     deals = deals.filter((d) => d.committee_risk === risk);
  if (region)   deals = deals.filter((d) => d.region === region);

  const coverage_counts:   Record<string, number> = {};
  const risk_counts:       Record<string, number> = {};
  const complexity_counts: Record<string, number> = {};
  const action_counts:     Record<string, number> = {};
  let total_comp = 0, total_cov = 0, total_role = 0,
      total_brd = 0, total_blk = 0, total_lat = 0;

  for (const d of mockDeals) {
    coverage_counts[d.committee_coverage]   = (coverage_counts[d.committee_coverage] || 0) + 1;
    risk_counts[d.committee_risk]           = (risk_counts[d.committee_risk] || 0) + 1;
    complexity_counts[d.deal_complexity]    = (complexity_counts[d.deal_complexity] || 0) + 1;
    action_counts[d.committee_action]       = (action_counts[d.committee_action] || 0) + 1;
    total_comp += d.committee_composite;
    total_cov  += d.coverage_ratio;
    total_role += d.role_coverage_score;
    total_brd  += d.engagement_breadth_score;
    total_blk  += d.blocker_management_score;
    total_lat  += d.late_stage_alignment_score;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      coverage_counts,
      risk_counts,
      complexity_counts,
      action_counts,
      avg_committee_composite:        Math.round((total_comp / n) * 10) / 10,
      avg_coverage_ratio:             Math.round((total_cov / n) * 100) / 100,
      well_covered_count:             mockDeals.filter((d) => d.is_well_covered).length,
      expansion_needed_count:         mockDeals.filter((d) => d.needs_expansion).length,
      avg_role_coverage_score:        Math.round((total_role / n) * 10) / 10,
      avg_engagement_breadth_score:   Math.round((total_brd / n) * 10) / 10,
      avg_blocker_management_score:   Math.round((total_blk / n) * 10) / 10,
      avg_late_stage_alignment_score: Math.round((total_lat / n) * 10) / 10,
    },
  });
}
