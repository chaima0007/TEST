import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", rep_id: "rep_001", deal_name: "Acme Corp Enterprise",
    threading_status: "well_threaded", threading_risk: "low",
    stakeholder_coverage: "comprehensive", threading_action: "maintain",
    coverage_score: 88.0, engagement_score: 82.0,
    executive_access_score: 90.0, resilience_score: 75.0,
    threading_composite: 84.3,
    is_single_threaded: false, needs_executive_access: false,
    estimated_risk_exposure_usd: 39750.0,
    primary_threading_gap: "weakest dimension: deal resilience",
    deal_value_usd: 250000.0, deal_stage: 2,
  },
  {
    deal_id: "deal_002", rep_id: "rep_002", deal_name: "Meridian Finance Q3",
    threading_status: "single_threaded", threading_risk: "critical",
    stakeholder_coverage: "poor", threading_action: "emergency_executive_outreach",
    coverage_score: 12.0, engagement_score: 8.0,
    executive_access_score: 0.0, resilience_score: 5.0,
    threading_composite: 6.5,
    is_single_threaded: true, needs_executive_access: true,
    estimated_risk_exposure_usd: 154350.0,
    primary_threading_gap: "no executive sponsor — critical blind spot at current stage",
    deal_value_usd: 165000.0, deal_stage: 2,
  },
  {
    deal_id: "deal_003", rep_id: "rep_001", deal_name: "Vertex Pharma Expansion",
    threading_status: "at_risk", threading_risk: "high",
    stakeholder_coverage: "partial", threading_action: "expand_stakeholder_map",
    coverage_score: 35.0, engagement_score: 28.0,
    executive_access_score: 22.0, resilience_score: 18.0,
    threading_composite: 26.8,
    is_single_threaded: false, needs_executive_access: true,
    estimated_risk_exposure_usd: 97552.0,
    primary_threading_gap: "no executive sponsor — critical blind spot at current stage",
    deal_value_usd: 133200.0, deal_stage: 1,
  },
  {
    deal_id: "deal_004", rep_id: "rep_003", deal_name: "Lumina Retail Platform",
    threading_status: "adequately_threaded", threading_risk: "moderate",
    stakeholder_coverage: "adequate", threading_action: "strengthen_existing",
    coverage_score: 58.0, engagement_score: 55.0,
    executive_access_score: 48.0, resilience_score: 50.0,
    threading_composite: 53.3,
    is_single_threaded: false, needs_executive_access: false,
    estimated_risk_exposure_usd: 87087.0,
    primary_threading_gap: "economic buyer not identified — procurement decision at risk",
    deal_value_usd: 186600.0, deal_stage: 1,
  },
  {
    deal_id: "deal_005", rep_id: "rep_004", deal_name: "TechCorp Global Renewal",
    threading_status: "well_threaded", threading_risk: "low",
    stakeholder_coverage: "comprehensive", threading_action: "maintain",
    coverage_score: 95.0, engagement_score: 90.0,
    executive_access_score: 92.0, resilience_score: 88.0,
    threading_composite: 91.8,
    is_single_threaded: false, needs_executive_access: false,
    estimated_risk_exposure_usd: 20492.0,
    primary_threading_gap: "weakest dimension: deal resilience",
    deal_value_usd: 250000.0, deal_stage: 2,
  },
  {
    deal_id: "deal_006", rep_id: "rep_002", deal_name: "Cascade Logistics EMEA",
    threading_status: "single_threaded", threading_risk: "critical",
    stakeholder_coverage: "poor", threading_action: "emergency_executive_outreach",
    coverage_score: 8.0, engagement_score: 5.0,
    executive_access_score: 0.0, resilience_score: 2.0,
    threading_composite: 4.0,
    is_single_threaded: true, needs_executive_access: true,
    estimated_risk_exposure_usd: 92160.0,
    primary_threading_gap: "no executive sponsor — critical blind spot at current stage",
    deal_value_usd: 96000.0, deal_stage: 1,
  },
  {
    deal_id: "deal_007", rep_id: "rep_003", deal_name: "Nexus Energy Cloud",
    threading_status: "adequately_threaded", threading_risk: "moderate",
    stakeholder_coverage: "adequate", threading_action: "strengthen_existing",
    coverage_score: 62.0, engagement_score: 58.0,
    executive_access_score: 55.0, resilience_score: 48.0,
    threading_composite: 56.8,
    is_single_threaded: false, needs_executive_access: false,
    estimated_risk_exposure_usd: 70884.0,
    primary_threading_gap: "no confirmed champion — deal lacks internal advocate",
    deal_value_usd: 164550.0, deal_stage: 1,
  },
  {
    deal_id: "deal_008", rep_id: "rep_004", deal_name: "Orion Healthcare Suite",
    threading_status: "at_risk", threading_risk: "high",
    stakeholder_coverage: "partial", threading_action: "expand_stakeholder_map",
    coverage_score: 30.0, engagement_score: 22.0,
    executive_access_score: 18.0, resilience_score: 15.0,
    threading_composite: 22.0,
    is_single_threaded: false, needs_executive_access: true,
    estimated_risk_exposure_usd: 172920.0,
    primary_threading_gap: "economic buyer not identified — procurement decision at risk",
    deal_value_usd: 221700.0, deal_stage: 2,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const status   = searchParams.get("status");
  const risk     = searchParams.get("risk");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/deal-multithreading-intelligence`);
      if (status) url.searchParams.set("status", status);
      if (risk)   url.searchParams.set("risk", risk);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (status) deals = deals.filter((d) => d.threading_status === status);
  if (risk)   deals = deals.filter((d) => d.threading_risk === risk);

  const status_counts: Record<string, number> = {};
  const risk_counts:   Record<string, number> = {};
  const cov_counts:    Record<string, number> = {};
  const act_counts:    Record<string, number> = {};
  let total_comp = 0, total_cov = 0, total_eng = 0, total_exec = 0, total_res = 0, total_pipe = 0;

  for (const d of mockDeals) {
    status_counts[d.threading_status]       = (status_counts[d.threading_status] || 0) + 1;
    risk_counts[d.threading_risk]           = (risk_counts[d.threading_risk] || 0) + 1;
    cov_counts[d.stakeholder_coverage]      = (cov_counts[d.stakeholder_coverage] || 0) + 1;
    act_counts[d.threading_action]          = (act_counts[d.threading_action] || 0) + 1;
    total_comp  += d.threading_composite;
    total_cov   += d.coverage_score;
    total_eng   += d.engagement_score;
    total_exec  += d.executive_access_score;
    total_res   += d.resilience_score;
    total_pipe  += d.estimated_risk_exposure_usd;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      threading_status_counts: status_counts,
      risk_counts,
      coverage_counts: cov_counts,
      action_counts: act_counts,
      avg_threading_composite:          Math.round((total_comp / n) * 10) / 10,
      single_threaded_count:            mockDeals.filter((d) => d.is_single_threaded).length,
      executive_access_needed_count:    mockDeals.filter((d) => d.needs_executive_access).length,
      avg_coverage_score:               Math.round((total_cov / n) * 10) / 10,
      avg_engagement_score:             Math.round((total_eng / n) * 10) / 10,
      avg_executive_access_score:       Math.round((total_exec / n) * 10) / 10,
      avg_resilience_score:             Math.round((total_res / n) * 10) / 10,
      total_at_risk_pipeline_usd:       Math.round(total_pipe * 100) / 100,
    },
  });
}
