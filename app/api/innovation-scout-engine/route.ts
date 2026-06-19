import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockSignals = [
  {
    signal_id: "IS-001", domain: "Generative AI", region: "NAMER",
    innovation_risk: "critical", innovation_pattern: "emerging_technology",
    innovation_severity: "critical_gap", recommended_action: "innovation_sprint",
    opportunity_score: 100, market_score: 98, capability_score: 95, timing_score: 100,
    innovation_composite: 98.5, has_opportunity_signal: true,
    requires_executive_attention: true,
    estimated_opportunity_value_index: 9.85,
    innovation_signal: "Emerging technology signal — 90% market whitespace — 82% disruption prob — 4mo window — composite 99",
  },
  {
    signal_id: "IS-002", domain: "Quantum Computing", region: "EMEA",
    innovation_risk: "high", innovation_pattern: "competitive_disruption",
    innovation_severity: "lagging", recommended_action: "competitive_response",
    opportunity_score: 72, market_score: 80, capability_score: 60, timing_score: 55,
    innovation_composite: 67.75, has_opportunity_signal: true,
    requires_executive_attention: true,
    estimated_opportunity_value_index: 5.42,
    innovation_signal: "Competitive disruption detected — 65% market whitespace — 68% disruption prob — 10mo window — composite 68",
  },
  {
    signal_id: "IS-003", domain: "Sustainable Energy", region: "APAC",
    innovation_risk: "high", innovation_pattern: "regulatory_opportunity",
    innovation_severity: "lagging", recommended_action: "regulatory_positioning",
    opportunity_score: 60, market_score: 55, capability_score: 50, timing_score: 65,
    innovation_composite: 57.25, has_opportunity_signal: true,
    requires_executive_attention: true,
    estimated_opportunity_value_index: 4.58,
    innovation_signal: "Regulatory tailwind identified — 60% market whitespace — 55% disruption prob — 14mo window — composite 57",
  },
  {
    signal_id: "IS-004", domain: "Healthcare Diagnostics", region: "NAMER",
    innovation_risk: "high", innovation_pattern: "market_whitespace",
    innovation_severity: "lagging", recommended_action: "market_entry_analysis",
    opportunity_score: 78, market_score: 50, capability_score: 55, timing_score: 48,
    innovation_composite: 59.1, has_opportunity_signal: true,
    requires_executive_attention: true,
    estimated_opportunity_value_index: 4.73,
    innovation_signal: "Market whitespace opportunity — 75% market whitespace — 50% disruption prob — 18mo window — composite 59",
  },
  {
    signal_id: "IS-005", domain: "Autonomous Logistics", region: "LATAM",
    innovation_risk: "moderate", innovation_pattern: "talent_shift",
    innovation_severity: "monitoring", recommended_action: "trend_monitoring",
    opportunity_score: 40, market_score: 35, capability_score: 42, timing_score: 30,
    innovation_composite: 37.15, has_opportunity_signal: false,
    requires_executive_attention: false,
    estimated_opportunity_value_index: 2.23,
    innovation_signal: "Talent shift underway — 45% market whitespace — 40% disruption prob — 20mo window — composite 37",
  },
  {
    signal_id: "IS-006", domain: "Fintech Payments", region: "EMEA",
    innovation_risk: "moderate", innovation_pattern: "none",
    innovation_severity: "monitoring", recommended_action: "trend_monitoring",
    opportunity_score: 35, market_score: 30, capability_score: 38, timing_score: 28,
    innovation_composite: 33.1, has_opportunity_signal: false,
    requires_executive_attention: false,
    estimated_opportunity_value_index: 1.99,
    innovation_signal: "Innovation landscape — 35% market whitespace — 38% disruption prob — 22mo window — composite 33",
  },
  {
    signal_id: "IS-007", domain: "EdTech Platforms", region: "APAC",
    innovation_risk: "low", innovation_pattern: "none",
    innovation_severity: "ahead", recommended_action: "no_action",
    opportunity_score: 12, market_score: 15, capability_score: 10, timing_score: 8,
    innovation_composite: 11.6, has_opportunity_signal: false,
    requires_executive_attention: false,
    estimated_opportunity_value_index: 0.70,
    innovation_signal: "Innovation landscape stable — no critical gaps or missed opportunities identified",
  },
  {
    signal_id: "IS-008", domain: "Cybersecurity AI", region: "NAMER",
    innovation_risk: "critical", innovation_pattern: "emerging_technology",
    innovation_severity: "critical_gap", recommended_action: "innovation_sprint",
    opportunity_score: 95, market_score: 92, capability_score: 88, timing_score: 96,
    innovation_composite: 93.05, has_opportunity_signal: true,
    requires_executive_attention: true,
    estimated_opportunity_value_index: 8.37,
    innovation_signal: "Emerging technology signal — 88% market whitespace — 78% disruption prob — 5mo window — composite 93",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");
  const region  = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/innovation-scout-engine`);
      if (risk)    url.searchParams.set("risk",    risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      if (region)  url.searchParams.set("region",  region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let signals = [...mockSignals];
  if (risk)    signals = signals.filter((s) => s.innovation_risk === risk);
  if (pattern) signals = signals.filter((s) => s.innovation_pattern === pattern);
  if (region)  signals = signals.filter((s) => s.region === region);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_opp = 0, total_mkt = 0, total_cap = 0,
      total_tim = 0, total_val = 0;

  for (const s of mockSignals) {
    risk_counts[s.innovation_risk]         = (risk_counts[s.innovation_risk] || 0) + 1;
    pattern_counts[s.innovation_pattern]   = (pattern_counts[s.innovation_pattern] || 0) + 1;
    severity_counts[s.innovation_severity] = (severity_counts[s.innovation_severity] || 0) + 1;
    action_counts[s.recommended_action]    = (action_counts[s.recommended_action] || 0) + 1;
    total_comp += s.innovation_composite;
    total_opp  += s.opportunity_score;
    total_mkt  += s.market_score;
    total_cap  += s.capability_score;
    total_tim  += s.timing_score;
    total_val  += s.estimated_opportunity_value_index;
  }

  const n = mockSignals.length;

  return NextResponse.json(sealResponse({
    signals,
    summary: {
      total:                                  n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_innovation_composite:               Math.round((total_comp / n) * 10) / 10,
      opportunity_signal_count:               mockSignals.filter((s) => s.has_opportunity_signal).length,
      executive_attention_count:              mockSignals.filter((s) => s.requires_executive_attention).length,
      avg_opportunity_score:                  Math.round((total_opp / n) * 10) / 10,
      avg_market_score:                       Math.round((total_mkt / n) * 10) / 10,
      avg_capability_score:                   Math.round((total_cap / n) * 10) / 10,
      avg_timing_score:                       Math.round((total_tim / n) * 10) / 10,
      avg_estimated_opportunity_value_index:  Math.round((total_val / n) * 100) / 100,
    },
  } as Record<string,unknown>));
}
