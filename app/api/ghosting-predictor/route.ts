import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", deal_name: "Apex Cloud Platform", rep_id: "rep_003",
    ghosting_risk: "critical", ghosting_pattern: "full_ghost",
    buyer_momentum: "stalled", ghosting_action: "last_resort",
    silence_score: 90.0, engagement_decay_score: 85.0,
    behavioral_risk_score: 75.0, deal_urgency_score: 78.0,
    ghosting_composite: 83.8, predicted_ghost_days: 0,
    recovery_probability: 12.0, is_at_risk_of_ghosting: true,
    needs_escalation: true, deal_value: 350000, region: "NAMER",
  },
  {
    deal_id: "deal_002", deal_name: "Solaris Data Platform", rep_id: "rep_001",
    ghosting_risk: "moderate", ghosting_pattern: "cooling_off",
    buyer_momentum: "decelerating", ghosting_action: "re_engage",
    silence_score: 35.0, engagement_decay_score: 30.0,
    behavioral_risk_score: 25.0, deal_urgency_score: 40.0,
    ghosting_composite: 32.3, predicted_ghost_days: 10,
    recovery_probability: 65.0, is_at_risk_of_ghosting: false,
    needs_escalation: false, deal_value: 280000, region: "EMEA",
  },
  {
    deal_id: "deal_003", deal_name: "ZenithAI Scale-Up", rep_id: "rep_002",
    ghosting_risk: "low", ghosting_pattern: "engaged",
    buyer_momentum: "accelerating", ghosting_action: "maintain",
    silence_score: 8.0, engagement_decay_score: 5.0,
    behavioral_risk_score: 10.0, deal_urgency_score: 25.0,
    ghosting_composite: 11.3, predicted_ghost_days: 30,
    recovery_probability: 92.0, is_at_risk_of_ghosting: false,
    needs_escalation: false, deal_value: 200000, region: "APAC",
  },
  {
    deal_id: "deal_004", deal_name: "Harbor Security Suite", rep_id: "rep_005",
    ghosting_risk: "high", ghosting_pattern: "partial_ghost",
    buyer_momentum: "stalled", ghosting_action: "escalate_path",
    silence_score: 65.0, engagement_decay_score: 60.0,
    behavioral_risk_score: 55.0, deal_urgency_score: 55.0,
    ghosting_composite: 59.8, predicted_ghost_days: 5,
    recovery_probability: 35.0, is_at_risk_of_ghosting: true,
    needs_escalation: true, deal_value: 500000, region: "NAMER",
  },
  {
    deal_id: "deal_005", deal_name: "PeakFlow Analytics", rep_id: "rep_007",
    ghosting_risk: "high", ghosting_pattern: "champion_exit",
    buyer_momentum: "stalled", ghosting_action: "last_resort",
    silence_score: 70.0, engagement_decay_score: 65.0,
    behavioral_risk_score: 68.0, deal_urgency_score: 60.0,
    ghosting_composite: 66.3, predicted_ghost_days: 0,
    recovery_probability: 20.0, is_at_risk_of_ghosting: true,
    needs_escalation: true, deal_value: 230000, region: "EMEA",
  },
  {
    deal_id: "deal_006", deal_name: "Orbit ERP Integration", rep_id: "rep_004",
    ghosting_risk: "moderate", ghosting_pattern: "slow_fade",
    buyer_momentum: "decelerating", ghosting_action: "re_engage",
    silence_score: 40.0, engagement_decay_score: 38.0,
    behavioral_risk_score: 32.0, deal_urgency_score: 30.0,
    ghosting_composite: 36.5, predicted_ghost_days: 12,
    recovery_probability: 58.0, is_at_risk_of_ghosting: false,
    needs_escalation: false, deal_value: 180000, region: "APAC",
  },
  {
    deal_id: "deal_007", deal_name: "Nexus Platform Expansion", rep_id: "rep_006",
    ghosting_risk: "low", ghosting_pattern: "engaged",
    buyer_momentum: "stable", ghosting_action: "maintain",
    silence_score: 12.0, engagement_decay_score: 8.0,
    behavioral_risk_score: 6.0, deal_urgency_score: 18.0,
    ghosting_composite: 10.9, predicted_ghost_days: 30,
    recovery_probability: 88.0, is_at_risk_of_ghosting: false,
    needs_escalation: false, deal_value: 180000, region: "LATAM",
  },
  {
    deal_id: "deal_008", deal_name: "Vertex CX Rollout", rep_id: "rep_008",
    ghosting_risk: "critical", ghosting_pattern: "full_ghost",
    buyer_momentum: "stalled", ghosting_action: "last_resort",
    silence_score: 85.0, engagement_decay_score: 80.0,
    behavioral_risk_score: 72.0, deal_urgency_score: 65.0,
    ghosting_composite: 78.4, predicted_ghost_days: 0,
    recovery_probability: 18.0, is_at_risk_of_ghosting: true,
    needs_escalation: true, deal_value: 420000, region: "NAMER",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");
  const region  = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/ghosting-predictor`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      if (region)  url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (risk)    deals = deals.filter((d) => d.ghosting_risk === risk);
  if (pattern) deals = deals.filter((d) => d.ghosting_pattern === pattern);
  if (region)  deals = deals.filter((d) => d.region === region);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const momentum_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_rec = 0, total_sil = 0,
      total_dec = 0, total_beh = 0, total_urg = 0;

  for (const d of mockDeals) {
    risk_counts[d.ghosting_risk]       = (risk_counts[d.ghosting_risk] || 0) + 1;
    pattern_counts[d.ghosting_pattern] = (pattern_counts[d.ghosting_pattern] || 0) + 1;
    momentum_counts[d.buyer_momentum]  = (momentum_counts[d.buyer_momentum] || 0) + 1;
    action_counts[d.ghosting_action]   = (action_counts[d.ghosting_action] || 0) + 1;
    total_comp += d.ghosting_composite;
    total_rec  += d.recovery_probability;
    total_sil  += d.silence_score;
    total_dec  += d.engagement_decay_score;
    total_beh  += d.behavioral_risk_score;
    total_urg  += d.deal_urgency_score;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      risk_counts,
      pattern_counts,
      momentum_counts,
      action_counts,
      avg_ghosting_composite:       Math.round((total_comp / n) * 10) / 10,
      avg_recovery_probability:     Math.round((total_rec / n) * 10) / 10,
      at_risk_count:                mockDeals.filter((d) => d.is_at_risk_of_ghosting).length,
      escalation_count:             mockDeals.filter((d) => d.needs_escalation).length,
      avg_silence_score:            Math.round((total_sil / n) * 10) / 10,
      avg_engagement_decay_score:   Math.round((total_dec / n) * 10) / 10,
      avg_behavioral_risk_score:    Math.round((total_beh / n) * 10) / 10,
      avg_deal_urgency_score:       Math.round((total_urg / n) * 10) / 10,
    },
  });
}
