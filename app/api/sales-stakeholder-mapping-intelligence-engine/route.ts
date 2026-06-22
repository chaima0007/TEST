import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-stakeholder-mapping-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "REP-001", region: "West",
    stakeholder_risk: "low", stakeholder_pattern: "none",
    stakeholder_severity: "mapped", recommended_action: "no_action",
    coverage_score: 5.0, champion_quality_score: 5.0,
    economic_alignment_score: 5.0, process_intelligence_score: 5.0,
    stakeholder_composite: 5.0,
    has_stakeholder_gap: false, requires_stakeholder_coaching: false,
    estimated_deal_risk_usd: 0.0,
    stakeholder_signal: "Stakeholder coverage strong — multi-threading, economic buyer access, and process intelligence within benchmarks",
  },
  {
    rep_id: "REP-002", region: "East",
    stakeholder_risk: "low", stakeholder_pattern: "none",
    stakeholder_severity: "mapped", recommended_action: "no_action",
    coverage_score: 8.0, champion_quality_score: 6.0,
    economic_alignment_score: 7.0, process_intelligence_score: 6.0,
    stakeholder_composite: 7.0,
    has_stakeholder_gap: false, requires_stakeholder_coaching: false,
    estimated_deal_risk_usd: 12000.0,
    stakeholder_signal: "Stakeholder coverage strong — multi-threading, economic buyer access, and process intelligence within benchmarks",
  },
  {
    rep_id: "REP-003", region: "Central",
    stakeholder_risk: "moderate", stakeholder_pattern: "none",
    stakeholder_severity: "developing", recommended_action: "stakeholder_tracking_coaching",
    coverage_score: 18.0, champion_quality_score: 15.0,
    economic_alignment_score: 12.0, process_intelligence_score: 20.0,
    stakeholder_composite: 15.75,
    has_stakeholder_gap: false, requires_stakeholder_coaching: true,
    estimated_deal_risk_usd: 28000.0,
    stakeholder_signal: "None — 45% economic buyer coverage — 60% multi-contact deals — 30% single-threaded — composite 16",
  },
  {
    rep_id: "REP-004", region: "Northeast",
    stakeholder_risk: "moderate", stakeholder_pattern: "champion_dependency",
    stakeholder_severity: "developing", recommended_action: "multi_thread_coaching",
    coverage_score: 22.0, champion_quality_score: 38.0,
    economic_alignment_score: 18.0, process_intelligence_score: 25.0,
    stakeholder_composite: 25.1,
    has_stakeholder_gap: false, requires_stakeholder_coaching: true,
    estimated_deal_risk_usd: 45000.0,
    stakeholder_signal: "Champion dependency — 50% economic buyer coverage — 55% multi-contact deals — 40% single-threaded — composite 25",
  },
  {
    rep_id: "REP-005", region: "Southeast",
    stakeholder_risk: "high", stakeholder_pattern: "economic_blind_spot",
    stakeholder_severity: "fragile", recommended_action: "economic_buyer_coaching",
    coverage_score: 35.0, champion_quality_score: 28.0,
    economic_alignment_score: 48.0, process_intelligence_score: 30.0,
    stakeholder_composite: 36.35,
    has_stakeholder_gap: true, requires_stakeholder_coaching: true,
    estimated_deal_risk_usd: 90000.0,
    stakeholder_signal: "Economic blind spot — 30% economic buyer coverage — 45% multi-contact deals — 55% single-threaded — composite 36",
  },
  {
    rep_id: "REP-006", region: "West",
    stakeholder_risk: "high", stakeholder_pattern: "single_threaded",
    stakeholder_severity: "fragile", recommended_action: "multi_thread_coaching",
    coverage_score: 48.0, champion_quality_score: 32.0,
    economic_alignment_score: 35.0, process_intelligence_score: 38.0,
    stakeholder_composite: 39.35,
    has_stakeholder_gap: true, requires_stakeholder_coaching: true,
    estimated_deal_risk_usd: 140000.0,
    stakeholder_signal: "Single threaded — 35% economic buyer coverage — 30% multi-contact deals — 70% single-threaded — composite 39",
  },
  {
    rep_id: "REP-007", region: "APAC",
    stakeholder_risk: "critical", stakeholder_pattern: "single_threaded",
    stakeholder_severity: "exposed", recommended_action: "executive_sponsor_escalation",
    coverage_score: 72.0, champion_quality_score: 55.0,
    economic_alignment_score: 60.0, process_intelligence_score: 58.0,
    stakeholder_composite: 62.65,
    has_stakeholder_gap: true, requires_stakeholder_coaching: true,
    estimated_deal_risk_usd: 380000.0,
    stakeholder_signal: "Single threaded — 20% economic buyer coverage — 20% multi-contact deals — 80% single-threaded — composite 63",
  },
  {
    rep_id: "REP-008", region: "EMEA",
    stakeholder_risk: "critical", stakeholder_pattern: "org_chart_gap",
    stakeholder_severity: "exposed", recommended_action: "deal_rescue_intervention",
    coverage_score: 80.0, champion_quality_score: 72.0,
    economic_alignment_score: 78.0, process_intelligence_score: 68.0,
    stakeholder_composite: 76.0,
    has_stakeholder_gap: true, requires_stakeholder_coaching: true,
    estimated_deal_risk_usd: 620000.0,
    stakeholder_signal: "Org chart gap — 15% economic buyer coverage — 15% multi-contact deals — 85% single-threaded — composite 76",
  },
];

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/api/sales-stakeholder-mapping-intelligence-engine`, { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_cov = 0, total_champ = 0, total_econ = 0, total_proc = 0, total_risk_usd = 0;

  for (const r of mockReps) {
    risk_counts[r.stakeholder_risk]       = (risk_counts[r.stakeholder_risk] || 0) + 1;
    pattern_counts[r.stakeholder_pattern] = (pattern_counts[r.stakeholder_pattern] || 0) + 1;
    severity_counts[r.stakeholder_severity] = (severity_counts[r.stakeholder_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp      += r.stakeholder_composite;
    total_cov       += r.coverage_score;
    total_champ     += r.champion_quality_score;
    total_econ      += r.economic_alignment_score;
    total_proc      += r.process_intelligence_score;
    total_risk_usd  += r.estimated_deal_risk_usd;
  }

  const n = mockReps.length;
  return sealResponse(NextResponse.json({
    reps: mockReps,
    summary: {
      total:                              n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_stakeholder_composite:          Math.round((total_comp / n) * 10) / 10,
      stakeholder_gap_count:              mockReps.filter((r) => r.has_stakeholder_gap).length,
      coaching_count:                     mockReps.filter((r) => r.requires_stakeholder_coaching).length,
      avg_coverage_score:                 Math.round((total_cov / n) * 10) / 10,
      avg_champion_quality_score:         Math.round((total_champ / n) * 10) / 10,
      avg_economic_alignment_score:       Math.round((total_econ / n) * 10) / 10,
      avg_process_intelligence_score:     Math.round((total_proc / n) * 10) / 10,
      total_estimated_deal_risk_usd:      Math.round(total_risk_usd * 100) / 100,
    },
  }));
}
