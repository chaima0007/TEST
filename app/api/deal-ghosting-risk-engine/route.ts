import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", rep_id: "rep_001",
    ghosting_risk: "low", ghosting_pattern: "none",
    ghosting_severity: "active", recommended_action: "no_action",
    silence_score: 0.0, engagement_decay_score: 0.0,
    stakeholder_coverage_score: 0.0, deal_momentum_score: 0.0,
    ghosting_composite: 0.0, is_ghosted: false, requires_escalation: false,
    estimated_deal_recovery_pct: 100.0,
    ghosting_signal: "Deal engagement within healthy parameters",
  },
  {
    deal_id: "deal_002", rep_id: "rep_002",
    ghosting_risk: "low", ghosting_pattern: "silence_after_demo",
    ghosting_severity: "active", recommended_action: "follow_up_sequence",
    silence_score: 14.0, engagement_decay_score: 10.0,
    stakeholder_coverage_score: 10.0, deal_momentum_score: 5.0,
    ghosting_composite: 10.6, is_ghosted: false, requires_escalation: false,
    estimated_deal_recovery_pct: 89.4,
    ghosting_signal: "Demo 15d ago — 8d silence — composite 11",
  },
  {
    deal_id: "deal_003", rep_id: "rep_002",
    ghosting_risk: "moderate", ghosting_pattern: "proposal_drop_off",
    ghosting_severity: "cooling", recommended_action: "follow_up_sequence",
    silence_score: 22.0, engagement_decay_score: 38.0,
    stakeholder_coverage_score: 12.0, deal_momentum_score: 10.0,
    ghosting_composite: 22.1, is_ghosted: false, requires_escalation: false,
    estimated_deal_recovery_pct: 77.9,
    ghosting_signal: "Proposal sent 16d ago — no response — 3 attempts — composite 22",
  },
  {
    deal_id: "deal_004", rep_id: "rep_003",
    ghosting_risk: "moderate", ghosting_pattern: "champion_unresponsive",
    ghosting_severity: "cooling", recommended_action: "follow_up_sequence",
    silence_score: 28.0, engagement_decay_score: 20.0,
    stakeholder_coverage_score: 15.0, deal_momentum_score: 12.0,
    ghosting_composite: 20.7, is_ghosted: false, requires_escalation: true,
    estimated_deal_recovery_pct: 79.3,
    ghosting_signal: "Champion dark 15d — 3 unanswered outreach — composite 21",
  },
  {
    deal_id: "deal_005", rep_id: "rep_003",
    ghosting_risk: "high", ghosting_pattern: "multi_stakeholder_fade",
    ghosting_severity: "dark", recommended_action: "manager_re_engage",
    silence_score: 35.0, engagement_decay_score: 30.0,
    stakeholder_coverage_score: 48.0, deal_momentum_score: 20.0,
    ghosting_composite: 34.3, is_ghosted: false, requires_escalation: true,
    estimated_deal_recovery_pct: 65.7,
    ghosting_signal: "1/4 stakeholders responsive — composite 34",
  },
  {
    deal_id: "deal_006", rep_id: "rep_004",
    ghosting_risk: "high", ghosting_pattern: "champion_unresponsive",
    ghosting_severity: "dark", recommended_action: "manager_re_engage",
    silence_score: 45.0, engagement_decay_score: 38.0,
    stakeholder_coverage_score: 30.0, deal_momentum_score: 25.0,
    ghosting_composite: 36.3, is_ghosted: false, requires_escalation: true,
    estimated_deal_recovery_pct: 63.7,
    ghosting_signal: "Champion dark 18d — 5 unanswered outreach — composite 36",
  },
  {
    deal_id: "deal_007", rep_id: "rep_004",
    ghosting_risk: "critical", ghosting_pattern: "end_of_cycle_ghost",
    ghosting_severity: "lost", recommended_action: "exec_outreach",
    silence_score: 70.0, engagement_decay_score: 55.0,
    stakeholder_coverage_score: 50.0, deal_momentum_score: 65.0,
    ghosting_composite: 60.8, is_ghosted: true, requires_escalation: true,
    estimated_deal_recovery_pct: 39.2,
    ghosting_signal: "12d silence — 8d to close date — composite 61",
  },
  {
    deal_id: "deal_008", rep_id: "rep_005",
    ghosting_risk: "critical", ghosting_pattern: "end_of_cycle_ghost",
    ghosting_severity: "lost", recommended_action: "deal_disqualification",
    silence_score: 100.0, engagement_decay_score: 70.0,
    stakeholder_coverage_score: 80.0, deal_momentum_score: 75.0,
    ghosting_composite: 82.3, is_ghosted: true, requires_escalation: true,
    estimated_deal_recovery_pct: 17.7,
    ghosting_signal: "25d silence — 3d to close date — composite 82",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/deal-ghosting-risk-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (risk)    deals = deals.filter((d) => d.ghosting_risk    === risk);
  if (pattern) deals = deals.filter((d) => d.ghosting_pattern === pattern);

  const risk_counts:    Record<string, number> = {};
  const pattern_counts: Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:  Record<string, number> = {};
  let total_comp = 0, total_sil = 0, total_eng = 0, total_stk = 0, total_mom = 0, total_rec = 0;

  for (const d of mockDeals) {
    risk_counts[d.ghosting_risk]       = (risk_counts[d.ghosting_risk] || 0) + 1;
    pattern_counts[d.ghosting_pattern] = (pattern_counts[d.ghosting_pattern] || 0) + 1;
    severity_counts[d.ghosting_severity] = (severity_counts[d.ghosting_severity] || 0) + 1;
    action_counts[d.recommended_action] = (action_counts[d.recommended_action] || 0) + 1;
    total_comp += d.ghosting_composite;
    total_sil  += d.silence_score;
    total_eng  += d.engagement_decay_score;
    total_stk  += d.stakeholder_coverage_score;
    total_mom  += d.deal_momentum_score;
    total_rec  += d.estimated_deal_recovery_pct;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total:                           n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_ghosting_composite:          Math.round((total_comp / n) * 10) / 10,
      ghosted_count:                   mockDeals.filter((d) => d.is_ghosted).length,
      escalation_count:                mockDeals.filter((d) => d.requires_escalation).length,
      avg_silence_score:               Math.round((total_sil  / n) * 10) / 10,
      avg_engagement_decay_score:      Math.round((total_eng  / n) * 10) / 10,
      avg_stakeholder_coverage_score:  Math.round((total_stk  / n) * 10) / 10,
      avg_deal_momentum_score:         Math.round((total_mom  / n) * 10) / 10,
      avg_estimated_deal_recovery_pct: Math.round((total_rec  / n) * 10) / 10,
    },
  });
}
