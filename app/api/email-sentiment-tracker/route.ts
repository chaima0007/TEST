import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[email-sentiment-tracker] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockThreads = [
  {
    thread_id: "thr_001", deal_id: "deal_001", rep_id: "rep_003",
    thread_sentiment: "enthusiastic", sentiment_trajectory: "improving",
    buyer_engagement_signal: "highly_engaged", email_action: "keep_momentum",
    reply_quality_score: 90.0, engagement_depth_score: 95.0,
    sentiment_momentum_score: 88.0, urgency_alignment_score: 92.0,
    email_composite: 91.5, predicted_open_probability: 87.0,
    thread_health_index: 96.5, is_thread_healthy: true,
    needs_intervention: false, region: "NAMER",
  },
  {
    thread_id: "thr_002", deal_id: "deal_002", rep_id: "rep_001",
    thread_sentiment: "negative", sentiment_trajectory: "flatlined",
    buyer_engagement_signal: "disengaged", email_action: "escalate_send",
    reply_quality_score: 5.0, engagement_depth_score: 8.0,
    sentiment_momentum_score: 20.0, urgency_alignment_score: 5.0,
    email_composite: 9.8, predicted_open_probability: 5.0,
    thread_health_index: 9.8, is_thread_healthy: false,
    needs_intervention: true, region: "EMEA",
  },
  {
    thread_id: "thr_003", deal_id: "deal_003", rep_id: "rep_002",
    thread_sentiment: "positive", sentiment_trajectory: "stable",
    buyer_engagement_signal: "engaged", email_action: "keep_momentum",
    reply_quality_score: 65.0, engagement_depth_score: 60.0,
    sentiment_momentum_score: 68.0, urgency_alignment_score: 55.0,
    email_composite: 63.1, predicted_open_probability: 57.0,
    thread_health_index: 68.1, is_thread_healthy: true,
    needs_intervention: false, region: "APAC",
  },
  {
    thread_id: "thr_004", deal_id: "deal_004", rep_id: "rep_005",
    thread_sentiment: "cooling", sentiment_trajectory: "declining",
    buyer_engagement_signal: "disengaging", email_action: "pattern_break",
    reply_quality_score: 30.0, engagement_depth_score: 22.0,
    sentiment_momentum_score: 32.0, urgency_alignment_score: 18.0,
    email_composite: 26.7, predicted_open_probability: 16.0,
    thread_health_index: 26.7, is_thread_healthy: false,
    needs_intervention: true, region: "NAMER",
  },
  {
    thread_id: "thr_005", deal_id: "deal_005", rep_id: "rep_007",
    thread_sentiment: "positive", sentiment_trajectory: "improving",
    buyer_engagement_signal: "engaged", email_action: "keep_momentum",
    reply_quality_score: 70.0, engagement_depth_score: 72.0,
    sentiment_momentum_score: 75.0, urgency_alignment_score: 65.0,
    email_composite: 71.3, predicted_open_probability: 63.0,
    thread_health_index: 76.3, is_thread_healthy: true,
    needs_intervention: false, region: "EMEA",
  },
  {
    thread_id: "thr_006", deal_id: "deal_006", rep_id: "rep_004",
    thread_sentiment: "neutral", sentiment_trajectory: "volatile",
    buyer_engagement_signal: "passively_engaged", email_action: "reframe",
    reply_quality_score: 42.0, engagement_depth_score: 38.0,
    sentiment_momentum_score: 50.0, urgency_alignment_score: 28.0,
    email_composite: 40.9, predicted_open_probability: 24.0,
    thread_health_index: 40.9, is_thread_healthy: false,
    needs_intervention: false, region: "APAC",
  },
  {
    thread_id: "thr_007", deal_id: "deal_007", rep_id: "rep_006",
    thread_sentiment: "enthusiastic", sentiment_trajectory: "stable",
    buyer_engagement_signal: "highly_engaged", email_action: "keep_momentum",
    reply_quality_score: 82.0, engagement_depth_score: 88.0,
    sentiment_momentum_score: 80.0, urgency_alignment_score: 85.0,
    email_composite: 83.9, predicted_open_probability: 80.0,
    thread_health_index: 88.9, is_thread_healthy: true,
    needs_intervention: false, region: "LATAM",
  },
  {
    thread_id: "thr_008", deal_id: "deal_008", rep_id: "rep_008",
    thread_sentiment: "cooling", sentiment_trajectory: "declining",
    buyer_engagement_signal: "disengaging", email_action: "pattern_break",
    reply_quality_score: 18.0, engagement_depth_score: 12.0,
    sentiment_momentum_score: 28.0, urgency_alignment_score: 10.0,
    email_composite: 18.0, predicted_open_probability: 11.0,
    thread_health_index: 18.0, is_thread_healthy: false,
    needs_intervention: true, region: "NAMER",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const sentiment  = searchParams.get("sentiment");
  const trajectory = searchParams.get("trajectory");
  const region     = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/email-sentiment-tracker`);
      if (sentiment)  url.searchParams.set("sentiment", sentiment);
      if (trajectory) url.searchParams.set("trajectory", trajectory);
      if (region)     url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let threads = [...mockThreads];
  if (sentiment)  threads = threads.filter((t) => t.thread_sentiment === sentiment);
  if (trajectory) threads = threads.filter((t) => t.sentiment_trajectory === trajectory);
  if (region)     threads = threads.filter((t) => t.region === region);

  const sentiment_counts:  Record<string, number> = {};
  const trajectory_counts: Record<string, number> = {};
  const engagement_counts: Record<string, number> = {};
  const action_counts:     Record<string, number> = {};
  let total_comp = 0, total_health = 0, total_reply = 0,
      total_depth = 0, total_mom = 0, total_urg = 0;

  for (const t of mockThreads) {
    sentiment_counts[t.thread_sentiment]       = (sentiment_counts[t.thread_sentiment] || 0) + 1;
    trajectory_counts[t.sentiment_trajectory]  = (trajectory_counts[t.sentiment_trajectory] || 0) + 1;
    engagement_counts[t.buyer_engagement_signal] = (engagement_counts[t.buyer_engagement_signal] || 0) + 1;
    action_counts[t.email_action]              = (action_counts[t.email_action] || 0) + 1;
    total_comp   += t.email_composite;
    total_health += t.thread_health_index;
    total_reply  += t.reply_quality_score;
    total_depth  += t.engagement_depth_score;
    total_mom    += t.sentiment_momentum_score;
    total_urg    += t.urgency_alignment_score;
  }

  const n = mockThreads.length;

  return sealResponse(NextResponse.json({
    threads,
    summary: {
      total: n,
      sentiment_counts,
      trajectory_counts,
      engagement_counts,
      action_counts,
      avg_email_composite:            Math.round((total_comp / n) * 10) / 10,
      avg_thread_health_index:        Math.round((total_health / n) * 10) / 10,
      healthy_count:                  mockThreads.filter((t) => t.is_thread_healthy).length,
      intervention_count:             mockThreads.filter((t) => t.needs_intervention).length,
      avg_reply_quality_score:        Math.round((total_reply / n) * 10) / 10,
      avg_engagement_depth_score:     Math.round((total_depth / n) * 10) / 10,
      avg_sentiment_momentum_score:   Math.round((total_mom / n) * 10) / 10,
      avg_urgency_alignment_score:    Math.round((total_urg / n) * 10) / 10,
    },
  }));
}
