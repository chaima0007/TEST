import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[call-tone-analyzer] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockCalls = [
  {
    call_id: "call_001", deal_name: "Apex Cloud Transformation", rep_id: "rep_003",
    tone_sentiment: "positive", dominant_tone: "enthusiastic",
    conversation_control: "balanced", tone_action: "reinforce",
    rep_confidence_score: 88.0, buyer_engagement_score: 82.0,
    objection_handling_score: 90.0, conversation_quality_score: 78.0,
    call_tone_composite: 85.5, deal_advancement_probability: 98.0,
    call_coaching_priority: 8.0, is_positive_call: true, needs_immediate_coaching: false,
    call_duration_minutes: 48, region: "NAMER",
  },
  {
    call_id: "call_002", deal_name: "Solaris Data Platform", rep_id: "rep_001",
    tone_sentiment: "negative", dominant_tone: "panic_signal",
    conversation_control: "fragmented", tone_action: "intervene",
    rep_confidence_score: 22.0, buyer_engagement_score: 18.0,
    objection_handling_score: 12.0, conversation_quality_score: 15.0,
    call_tone_composite: 18.4, deal_advancement_probability: 4.0,
    call_coaching_priority: 95.0, is_positive_call: false, needs_immediate_coaching: true,
    call_duration_minutes: 12, region: "EMEA",
  },
  {
    call_id: "call_003", deal_name: "ZenithAI Scale-Up", rep_id: "rep_002",
    tone_sentiment: "positive", dominant_tone: "authoritative",
    conversation_control: "balanced", tone_action: "reinforce",
    rep_confidence_score: 78.0, buyer_engagement_score: 72.0,
    objection_handling_score: 88.0, conversation_quality_score: 68.0,
    call_tone_composite: 76.8, deal_advancement_probability: 92.0,
    call_coaching_priority: 20.0, is_positive_call: true, needs_immediate_coaching: false,
    call_duration_minutes: 55, region: "APAC",
  },
  {
    call_id: "call_004", deal_name: "Harbor Security Suite", rep_id: "rep_005",
    tone_sentiment: "cautious", dominant_tone: "hesitant",
    conversation_control: "buyer_led", tone_action: "reframe",
    rep_confidence_score: 35.0, buyer_engagement_score: 55.0,
    objection_handling_score: 42.0, conversation_quality_score: 38.0,
    call_tone_composite: 42.8, deal_advancement_probability: 38.0,
    call_coaching_priority: 68.0, is_positive_call: false, needs_immediate_coaching: true,
    call_duration_minutes: 32, region: "NAMER",
  },
  {
    call_id: "call_005", deal_name: "PeakFlow Analytics", rep_id: "rep_007",
    tone_sentiment: "neutral", dominant_tone: "authoritative",
    conversation_control: "rep_led", tone_action: "nurture",
    rep_confidence_score: 65.0, buyer_engagement_score: 42.0,
    objection_handling_score: 70.0, conversation_quality_score: 52.0,
    call_tone_composite: 58.2, deal_advancement_probability: 62.0,
    call_coaching_priority: 40.0, is_positive_call: false, needs_immediate_coaching: false,
    call_duration_minutes: 40, region: "EMEA",
  },
  {
    call_id: "call_006", deal_name: "Orbit ERP Integration", rep_id: "rep_004",
    tone_sentiment: "cautious", dominant_tone: "evasive",
    conversation_control: "buyer_led", tone_action: "reframe",
    rep_confidence_score: 28.0, buyer_engagement_score: 25.0,
    objection_handling_score: 30.0, conversation_quality_score: 22.0,
    call_tone_composite: 27.0, deal_advancement_probability: 18.0,
    call_coaching_priority: 82.0, is_positive_call: false, needs_immediate_coaching: true,
    call_duration_minutes: 22, region: "APAC",
  },
  {
    call_id: "call_007", deal_name: "Nexus Platform Expansion", rep_id: "rep_006",
    tone_sentiment: "positive", dominant_tone: "enthusiastic",
    conversation_control: "balanced", tone_action: "reinforce",
    rep_confidence_score: 72.0, buyer_engagement_score: 78.0,
    objection_handling_score: 82.0, conversation_quality_score: 65.0,
    call_tone_composite: 74.8, deal_advancement_probability: 88.0,
    call_coaching_priority: 22.0, is_positive_call: true, needs_immediate_coaching: false,
    call_duration_minutes: 50, region: "LATAM",
  },
  {
    call_id: "call_008", deal_name: "Vertex CX Rollout", rep_id: "rep_008",
    tone_sentiment: "neutral", dominant_tone: "resistant",
    conversation_control: "buyer_led", tone_action: "nurture",
    rep_confidence_score: 55.0, buyer_engagement_score: 38.0,
    objection_handling_score: 48.0, conversation_quality_score: 44.0,
    call_tone_composite: 47.2, deal_advancement_probability: 42.0,
    call_coaching_priority: 52.0, is_positive_call: false, needs_immediate_coaching: false,
    call_duration_minutes: 35, region: "NAMER",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const sentiment = searchParams.get("sentiment");
  const tone      = searchParams.get("tone");
  const region    = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/call-tone-analyzer`);
      if (sentiment) url.searchParams.set("sentiment", sentiment);
      if (tone)      url.searchParams.set("tone", tone);
      if (region)    url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let calls = [...mockCalls];
  if (sentiment) calls = calls.filter((c) => c.tone_sentiment === sentiment);
  if (tone)      calls = calls.filter((c) => c.dominant_tone === tone);
  if (region)    calls = calls.filter((c) => c.region === region);

  const sentiment_counts: Record<string, number> = {};
  const tone_counts:      Record<string, number> = {};
  const control_counts:   Record<string, number> = {};
  const action_counts:    Record<string, number> = {};
  let total_comp = 0, total_conf = 0, total_eng = 0,
      total_obj = 0, total_adv = 0, total_coach = 0;

  for (const c of mockCalls) {
    sentiment_counts[c.tone_sentiment]       = (sentiment_counts[c.tone_sentiment] || 0) + 1;
    tone_counts[c.dominant_tone]             = (tone_counts[c.dominant_tone] || 0) + 1;
    control_counts[c.conversation_control]   = (control_counts[c.conversation_control] || 0) + 1;
    action_counts[c.tone_action]             = (action_counts[c.tone_action] || 0) + 1;
    total_comp  += c.call_tone_composite;
    total_conf  += c.rep_confidence_score;
    total_eng   += c.buyer_engagement_score;
    total_obj   += c.objection_handling_score;
    total_adv   += c.deal_advancement_probability;
    total_coach += c.call_coaching_priority;
  }

  const n = mockCalls.length;

  return sealResponse(NextResponse.json({
    calls,
    summary: {
      total: n,
      sentiment_counts,
      tone_counts,
      control_counts,
      action_counts,
      avg_call_tone_composite:          Math.round((total_comp / n) * 10) / 10,
      positive_call_count:              mockCalls.filter((c) => c.is_positive_call).length,
      coaching_needed_count:            mockCalls.filter((c) => c.needs_immediate_coaching).length,
      avg_rep_confidence_score:         Math.round((total_conf / n) * 10) / 10,
      avg_buyer_engagement_score:       Math.round((total_eng / n) * 10) / 10,
      avg_objection_handling_score:     Math.round((total_obj / n) * 10) / 10,
      avg_deal_advancement_probability: Math.round((total_adv / n) * 10) / 10,
      avg_coaching_priority:            Math.round((total_coach / n) * 10) / 10,
    },
  }));
}
