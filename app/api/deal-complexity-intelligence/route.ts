import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[deal-complexity-intelligence] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", rep_id: "rep_001", deal_name: "Acme Enterprise Suite",
    complexity_tier: "enterprise", complexity_risk: "critical",
    primary_complexity_dimension: "technology", complexity_action: "dedicated_deal_team",
    people_complexity_score: 82.0, process_complexity_score: 88.0,
    technology_complexity_score: 90.0, legal_complexity_score: 80.0,
    complexity_composite: 85.0,
    requires_deal_desk: true, needs_executive_sponsor: true,
    estimated_win_probability_impact_pct: -30.0,
    complexity_summary: "primary: technology — custom legal, security review, 12-month implementation",
    deal_value_usd: 750000.0,
  },
  {
    deal_id: "deal_002", rep_id: "rep_002", deal_name: "Meridian SMB Starter",
    complexity_tier: "simple", complexity_risk: "low",
    primary_complexity_dimension: "process", complexity_action: "standard_process",
    people_complexity_score: 5.0, process_complexity_score: 6.0,
    technology_complexity_score: 8.0, legal_complexity_score: 2.0,
    complexity_composite: 5.3,
    requires_deal_desk: false, needs_executive_sponsor: false,
    estimated_win_probability_impact_pct: -5.0,
    complexity_summary: "primary complexity driver: process (6/100)",
    deal_value_usd: 12000.0,
  },
  {
    deal_id: "deal_003", rep_id: "rep_001", deal_name: "Vertex Pharma Compliance",
    complexity_tier: "complex", complexity_risk: "high",
    primary_complexity_dimension: "legal", complexity_action: "executive_sponsor_required",
    people_complexity_score: 45.0, process_complexity_score: 52.0,
    technology_complexity_score: 48.0, legal_complexity_score: 72.0,
    complexity_composite: 54.3,
    requires_deal_desk: true, needs_executive_sponsor: false,
    estimated_win_probability_impact_pct: -20.0,
    complexity_summary: "primary: legal — custom legal, security review, multi-region",
    deal_value_usd: 320000.0,
  },
  {
    deal_id: "deal_004", rep_id: "rep_003", deal_name: "Lumina Retail Standard",
    complexity_tier: "standard", complexity_risk: "moderate",
    primary_complexity_dimension: "technology", complexity_action: "assign_solution_engineer",
    people_complexity_score: 22.0, process_complexity_score: 28.0,
    technology_complexity_score: 38.0, legal_complexity_score: 15.0,
    complexity_composite: 25.8,
    requires_deal_desk: false, needs_executive_sponsor: false,
    estimated_win_probability_impact_pct: -12.0,
    complexity_summary: "primary complexity driver: technology (38/100)",
    deal_value_usd: 95000.0,
  },
  {
    deal_id: "deal_005", rep_id: "rep_004", deal_name: "TechCorp Global Platform",
    complexity_tier: "enterprise", complexity_risk: "critical",
    primary_complexity_dimension: "people", complexity_action: "dedicated_deal_team",
    people_complexity_score: 95.0, process_complexity_score: 85.0,
    technology_complexity_score: 78.0, legal_complexity_score: 88.0,
    complexity_composite: 86.5,
    requires_deal_desk: true, needs_executive_sponsor: true,
    estimated_win_probability_impact_pct: -30.0,
    complexity_summary: "primary: people — custom legal, security review, POC required, 18-month implementation",
    deal_value_usd: 1200000.0,
  },
  {
    deal_id: "deal_006", rep_id: "rep_002", deal_name: "Cascade Logistics Ops",
    complexity_tier: "standard", complexity_risk: "moderate",
    primary_complexity_dimension: "process", complexity_action: "assign_solution_engineer",
    people_complexity_score: 18.0, process_complexity_score: 35.0,
    technology_complexity_score: 28.0, legal_complexity_score: 20.0,
    complexity_composite: 25.3,
    requires_deal_desk: false, needs_executive_sponsor: false,
    estimated_win_probability_impact_pct: -12.0,
    complexity_summary: "primary complexity driver: process (35/100)",
    deal_value_usd: 68000.0,
  },
  {
    deal_id: "deal_007", rep_id: "rep_003", deal_name: "Nexus Energy Cloud",
    complexity_tier: "complex", complexity_risk: "high",
    primary_complexity_dimension: "technology", complexity_action: "executive_sponsor_required",
    people_complexity_score: 38.0, process_complexity_score: 60.0,
    technology_complexity_score: 65.0, legal_complexity_score: 42.0,
    complexity_composite: 51.3,
    requires_deal_desk: false, needs_executive_sponsor: false,
    estimated_win_probability_impact_pct: -20.0,
    complexity_summary: "primary: technology — security review, POC required, 9-month implementation",
    deal_value_usd: 225000.0,
  },
  {
    deal_id: "deal_008", rep_id: "rep_004", deal_name: "Orion Healthcare Suite",
    complexity_tier: "enterprise", complexity_risk: "critical",
    primary_complexity_dimension: "legal", complexity_action: "dedicated_deal_team",
    people_complexity_score: 62.0, process_complexity_score: 70.0,
    technology_complexity_score: 55.0, legal_complexity_score: 95.0,
    complexity_composite: 70.5,
    requires_deal_desk: true, needs_executive_sponsor: true,
    estimated_win_probability_impact_pct: -30.0,
    complexity_summary: "primary: legal — custom legal, security review, multi-region",
    deal_value_usd: 480000.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier = searchParams.get("tier");
  const risk = searchParams.get("risk");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/deal-complexity-intelligence`);
      if (tier) url.searchParams.set("tier", tier);
      if (risk) url.searchParams.set("risk", risk);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let deals = [...mockDeals];
  if (tier) deals = deals.filter((d) => d.complexity_tier === tier);
  if (risk) deals = deals.filter((d) => d.complexity_risk === risk);

  const tier_counts: Record<string,number> = {};
  const risk_counts: Record<string,number> = {};
  const dim_counts:  Record<string,number> = {};
  const act_counts:  Record<string,number> = {};
  let total_comp=0, total_p=0, total_pr=0, total_t=0, total_l=0, high_pipe=0;

  for (const d of mockDeals) {
    tier_counts[d.complexity_tier]                     = (tier_counts[d.complexity_tier] || 0) + 1;
    risk_counts[d.complexity_risk]                     = (risk_counts[d.complexity_risk] || 0) + 1;
    dim_counts[d.primary_complexity_dimension]         = (dim_counts[d.primary_complexity_dimension] || 0) + 1;
    act_counts[d.complexity_action]                    = (act_counts[d.complexity_action] || 0) + 1;
    total_comp += d.complexity_composite;
    total_p    += d.people_complexity_score;
    total_pr   += d.process_complexity_score;
    total_t    += d.technology_complexity_score;
    total_l    += d.legal_complexity_score;
    if (d.complexity_composite >= 50) high_pipe += d.deal_value_usd;
  }

  const n = mockDeals.length;

  return sealResponse(NextResponse.json(sealResponse({
    deals,
    summary: {
      total: n,
      tier_counts,
      risk_counts,
      dimension_counts: dim_counts,
      action_counts: act_counts,
      avg_complexity_composite:       Math.round((total_comp / n) * 10) / 10,
      deal_desk_required_count:       mockDeals.filter((d) => d.requires_deal_desk).length,
      executive_sponsor_needed_count: mockDeals.filter((d) => d.needs_executive_sponsor).length,
      avg_people_score:               Math.round((total_p / n) * 10) / 10,
      avg_process_score:              Math.round((total_pr / n) * 10) / 10,
      avg_technology_score:           Math.round((total_t / n) * 10) / 10,
      avg_legal_score:                Math.round((total_l / n) * 10) / 10,
      high_complexity_pipeline_usd:   Math.round(high_pipe * 100) / 100,
    },
  } as Record<string,unknown>)));
}
