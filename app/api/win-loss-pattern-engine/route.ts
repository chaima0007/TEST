import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", deal_name: "Acme Corp Enterprise", rep_id: "rep_003",
    deal_outcome: "closed_won", loss_reason: "no_loss",
    rep_behavior_pattern: "exemplary", win_loss_action: "share_as_best_practice",
    process_quality_score: 95.0, execution_score: 98.0,
    relationship_score: 100.0, deal_health_score: 90.0,
    win_loss_composite: 95.8, win_probability_index: 90.0,
    replication_value: 100.0, is_best_practice: true,
    needs_coaching: false, region: "NAMER",
  },
  {
    deal_id: "deal_002", deal_name: "BetaTech SaaS", rep_id: "rep_001",
    deal_outcome: "closed_lost", loss_reason: "poor_process",
    rep_behavior_pattern: "high_risk", win_loss_action: "urgent_intervention",
    process_quality_score: 15.0, execution_score: 18.0,
    relationship_score: 10.0, deal_health_score: 20.0,
    win_loss_composite: 15.3, win_probability_index: 30.0,
    replication_value: 6.1, is_best_practice: false,
    needs_coaching: true, region: "EMEA",
  },
  {
    deal_id: "deal_003", deal_name: "CloudBase Platform", rep_id: "rep_002",
    deal_outcome: "closed_won", loss_reason: "no_loss",
    rep_behavior_pattern: "solid", win_loss_action: "replicate",
    process_quality_score: 68.0, execution_score: 72.0,
    relationship_score: 65.0, deal_health_score: 75.0,
    win_loss_composite: 70.0, win_probability_index: 68.0,
    replication_value: 77.0, is_best_practice: false,
    needs_coaching: false, region: "APAC",
  },
  {
    deal_id: "deal_004", deal_name: "Delta Networks", rep_id: "rep_005",
    deal_outcome: "closed_lost", loss_reason: "competitor",
    rep_behavior_pattern: "improvable", win_loss_action: "coach_and_improve",
    process_quality_score: 48.0, execution_score: 42.0,
    relationship_score: 35.0, deal_health_score: 22.0,
    win_loss_composite: 39.8, win_probability_index: 42.0,
    replication_value: 15.9, is_best_practice: false,
    needs_coaching: true, region: "NAMER",
  },
  {
    deal_id: "deal_005", deal_name: "EcoTech Expansion", rep_id: "rep_007",
    deal_outcome: "closed_won", loss_reason: "no_loss",
    rep_behavior_pattern: "exemplary", win_loss_action: "share_as_best_practice",
    process_quality_score: 88.0, execution_score: 92.0,
    relationship_score: 85.0, deal_health_score: 88.0,
    win_loss_composite: 88.5, win_probability_index: 88.0,
    replication_value: 97.4, is_best_practice: true,
    needs_coaching: false, region: "EMEA",
  },
  {
    deal_id: "deal_006", deal_name: "Finova Capital", rep_id: "rep_004",
    deal_outcome: "no_decision", loss_reason: "timing",
    rep_behavior_pattern: "improvable", win_loss_action: "coach_and_improve",
    process_quality_score: 55.0, execution_score: 50.0,
    relationship_score: 45.0, deal_health_score: 32.0,
    win_loss_composite: 49.3, win_probability_index: 50.0,
    replication_value: 19.7, is_best_practice: false,
    needs_coaching: true, region: "APAC",
  },
  {
    deal_id: "deal_007", deal_name: "GlobalLink Corp", rep_id: "rep_006",
    deal_outcome: "closed_won", loss_reason: "no_loss",
    rep_behavior_pattern: "exemplary", win_loss_action: "share_as_best_practice",
    process_quality_score: 82.0, execution_score: 85.0,
    relationship_score: 80.0, deal_health_score: 85.0,
    win_loss_composite: 83.3, win_probability_index: 82.0,
    replication_value: 91.6, is_best_practice: true,
    needs_coaching: false, region: "LATAM",
  },
  {
    deal_id: "deal_008", deal_name: "HorizonAI Platform", rep_id: "rep_008",
    deal_outcome: "closed_lost", loss_reason: "champion_loss",
    rep_behavior_pattern: "high_risk", win_loss_action: "urgent_intervention",
    process_quality_score: 28.0, execution_score: 22.0,
    relationship_score: 15.0, deal_health_score: 18.0,
    win_loss_composite: 22.0, win_probability_index: 25.0,
    replication_value: 8.8, is_best_practice: false,
    needs_coaching: true, region: "NAMER",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const outcome  = searchParams.get("outcome");
  const behavior = searchParams.get("behavior");
  const region   = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/win-loss-pattern-engine`);
      if (outcome)  url.searchParams.set("outcome", outcome);
      if (behavior) url.searchParams.set("behavior", behavior);
      if (region)   url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (outcome)  deals = deals.filter((d) => d.deal_outcome === outcome);
  if (behavior) deals = deals.filter((d) => d.rep_behavior_pattern === behavior);
  if (region)   deals = deals.filter((d) => d.region === region);

  const outcome_counts:   Record<string, number> = {};
  const loss_counts:      Record<string, number> = {};
  const behavior_counts:  Record<string, number> = {};
  const action_counts:    Record<string, number> = {};
  let total_comp = 0, total_proc = 0, total_exec = 0,
      total_rel = 0, total_repl = 0;

  for (const d of mockDeals) {
    outcome_counts[d.deal_outcome]          = (outcome_counts[d.deal_outcome] || 0) + 1;
    loss_counts[d.loss_reason]              = (loss_counts[d.loss_reason] || 0) + 1;
    behavior_counts[d.rep_behavior_pattern] = (behavior_counts[d.rep_behavior_pattern] || 0) + 1;
    action_counts[d.win_loss_action]        = (action_counts[d.win_loss_action] || 0) + 1;
    total_comp += d.win_loss_composite;
    total_proc += d.process_quality_score;
    total_exec += d.execution_score;
    total_rel  += d.relationship_score;
    total_repl += d.replication_value;
  }

  const n = mockDeals.length;
  const wonCount = mockDeals.filter((d) => d.deal_outcome === "closed_won").length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      outcome_counts,
      loss_reason_counts: loss_counts,
      behavior_counts,
      action_counts,
      avg_win_loss_composite:     Math.round((total_comp / n) * 10) / 10,
      win_rate:                   Math.round((wonCount / n) * 1000) / 10,
      best_practice_count:        mockDeals.filter((d) => d.is_best_practice).length,
      coaching_count:             mockDeals.filter((d) => d.needs_coaching).length,
      avg_process_quality_score:  Math.round((total_proc / n) * 10) / 10,
      avg_execution_score:        Math.round((total_exec / n) * 10) / 10,
      avg_relationship_score:     Math.round((total_rel / n) * 10) / 10,
      avg_replication_value:      Math.round((total_repl / n) * 10) / 10,
    },
  });
}
