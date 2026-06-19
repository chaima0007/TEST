import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockCalls = [
  {
    call_id: "call_001", deal_id: "deal_001", rep_id: "rep_003",
    conversation_quality: "elite", conversation_pattern: "challenger",
    qualification_depth: "deeply_qualified", conversation_action: "share_as_example",
    discovery_score: 95.0, qualification_score: 100.0,
    communication_score: 90.0, value_articulation_score: 95.0,
    conversation_composite: 95.0, coaching_priority_score: 5.0,
    deal_advancement_score: 97.5, is_coachable_moment: false,
    is_exemplary_call: true, call_type: "discovery", region: "NAMER",
  },
  {
    call_id: "call_002", deal_id: "deal_002", rep_id: "rep_001",
    conversation_quality: "poor", conversation_pattern: "monologue",
    qualification_depth: "unqualified", conversation_action: "coach_immediately",
    discovery_score: 15.0, qualification_score: 0.0,
    communication_score: 40.0, value_articulation_score: 20.0,
    conversation_composite: 19.0, coaching_priority_score: 88.0,
    deal_advancement_score: 9.5, is_coachable_moment: true,
    is_exemplary_call: false, call_type: "discovery", region: "EMEA",
  },
  {
    call_id: "call_003", deal_id: "deal_003", rep_id: "rep_002",
    conversation_quality: "proficient", conversation_pattern: "consultative",
    qualification_depth: "moderately_qualified", conversation_action: "structured_coaching",
    discovery_score: 75.0, qualification_score: 60.0,
    communication_score: 78.0, value_articulation_score: 65.0,
    conversation_composite: 69.7, coaching_priority_score: 40.0,
    deal_advancement_score: 64.9, is_coachable_moment: false,
    is_exemplary_call: false, call_type: "demo", region: "APAC",
  },
  {
    call_id: "call_004", deal_id: "deal_004", rep_id: "rep_005",
    conversation_quality: "developing", conversation_pattern: "shallow_discovery",
    qualification_depth: "surface_level", conversation_action: "coach_immediately",
    discovery_score: 35.0, qualification_score: 20.0,
    communication_score: 60.0, value_articulation_score: 30.0,
    conversation_composite: 35.5, coaching_priority_score: 72.0,
    deal_advancement_score: 27.8, is_coachable_moment: true,
    is_exemplary_call: false, call_type: "followup", region: "NAMER",
  },
  {
    call_id: "call_005", deal_id: "deal_005", rep_id: "rep_007",
    conversation_quality: "elite", conversation_pattern: "consultative",
    qualification_depth: "deeply_qualified", conversation_action: "reinforce_strengths",
    discovery_score: 85.0, qualification_score: 80.0,
    communication_score: 85.0, value_articulation_score: 78.0,
    conversation_composite: 82.4, coaching_priority_score: 20.0,
    deal_advancement_score: 82.2, is_coachable_moment: false,
    is_exemplary_call: false, call_type: "demo", region: "EMEA",
  },
  {
    call_id: "call_006", deal_id: "deal_006", rep_id: "rep_004",
    conversation_quality: "developing", conversation_pattern: "feature_dump",
    qualification_depth: "unqualified", conversation_action: "coach_immediately",
    discovery_score: 22.0, qualification_score: 15.0,
    communication_score: 55.0, value_articulation_score: 45.0,
    conversation_composite: 33.0, coaching_priority_score: 80.0,
    deal_advancement_score: 16.5, is_coachable_moment: true,
    is_exemplary_call: false, call_type: "followup", region: "APAC",
  },
  {
    call_id: "call_007", deal_id: "deal_007", rep_id: "rep_006",
    conversation_quality: "proficient", conversation_pattern: "balanced_dialogue",
    qualification_depth: "moderately_qualified", conversation_action: "structured_coaching",
    discovery_score: 68.0, qualification_score: 60.0,
    communication_score: 72.0, value_articulation_score: 60.0,
    conversation_composite: 65.0, coaching_priority_score: 43.0,
    deal_advancement_score: 62.5, is_coachable_moment: false,
    is_exemplary_call: false, call_type: "negotiation", region: "LATAM",
  },
  {
    call_id: "call_008", deal_id: "deal_008", rep_id: "rep_008",
    conversation_quality: "poor", conversation_pattern: "shallow_discovery",
    qualification_depth: "unqualified", conversation_action: "coach_immediately",
    discovery_score: 20.0, qualification_score: 20.0,
    communication_score: 35.0, value_articulation_score: 10.0,
    conversation_composite: 22.0, coaching_priority_score: 90.0,
    deal_advancement_score: 11.0, is_coachable_moment: true,
    is_exemplary_call: false, call_type: "discovery", region: "NAMER",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const quality = searchParams.get("quality");
  const pattern = searchParams.get("pattern");
  const region  = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/conversation-intelligence`);
      if (quality) url.searchParams.set("quality", quality);
      if (pattern) url.searchParams.set("pattern", pattern);
      if (region)  url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let calls = [...mockCalls];
  if (quality) calls = calls.filter((c) => c.conversation_quality === quality);
  if (pattern) calls = calls.filter((c) => c.conversation_pattern === pattern);
  if (region)  calls = calls.filter((c) => c.region === region);

  const quality_counts:  Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const depth_counts:    Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_adv = 0, total_disc = 0,
      total_qual = 0, total_comm = 0, total_val = 0;

  for (const c of mockCalls) {
    quality_counts[c.conversation_quality]  = (quality_counts[c.conversation_quality] || 0) + 1;
    pattern_counts[c.conversation_pattern]  = (pattern_counts[c.conversation_pattern] || 0) + 1;
    depth_counts[c.qualification_depth]     = (depth_counts[c.qualification_depth] || 0) + 1;
    action_counts[c.conversation_action]    = (action_counts[c.conversation_action] || 0) + 1;
    total_comp += c.conversation_composite;
    total_adv  += c.deal_advancement_score;
    total_disc += c.discovery_score;
    total_qual += c.qualification_score;
    total_comm += c.communication_score;
    total_val  += c.value_articulation_score;
  }

  const n = mockCalls.length;

  return NextResponse.json(sealResponse({
    calls,
    summary: {
      total: n,
      quality_counts,
      pattern_counts,
      depth_counts,
      action_counts,
      avg_conversation_composite:   Math.round((total_comp / n) * 10) / 10,
      avg_deal_advancement_score:   Math.round((total_adv / n) * 10) / 10,
      coachable_count:              mockCalls.filter((c) => c.is_coachable_moment).length,
      exemplary_count:              mockCalls.filter((c) => c.is_exemplary_call).length,
      avg_discovery_score:          Math.round((total_disc / n) * 10) / 10,
      avg_qualification_score:      Math.round((total_qual / n) * 10) / 10,
      avg_communication_score:      Math.round((total_comm / n) * 10) / 10,
      avg_value_articulation_score: Math.round((total_val / n) * 10) / 10,
    },
  } as Record<string,unknown>));
}
