import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockSegments = [
  {
    segment_id: "EM-001", region: "EMEA",
    emotional_risk: "critical", behavior_pattern: "sentiment_collapse", emotional_severity: "chaotic",
    recommended_action: "emergency_sentiment_reset",
    sentiment_score: 100.0, rationality_score: 100.0, bias_score: 100.0, resilience_score: 100.0,
    emotional_composite: 100.0, has_emotional_crisis: true, requires_behavioral_intervention: true,
    estimated_sentiment_disruption_index: 8.3,
    emotional_signal: "Critical — sentiment 15% — confiance 18% — volatilité 80% — composite 100",
  },
  {
    segment_id: "EM-005", region: "MEA",
    emotional_risk: "critical", behavior_pattern: "sentiment_collapse", emotional_severity: "chaotic",
    recommended_action: "emergency_sentiment_reset",
    sentiment_score: 100.0, rationality_score: 83.0, bias_score: 66.0, resilience_score: 87.0,
    emotional_composite: 84.65, has_emotional_crisis: true, requires_behavioral_intervention: true,
    estimated_sentiment_disruption_index: 6.86,
    emotional_signal: "Critical — sentiment 22% — confiance 20% — volatilité 82% — composite 85",
  },
  {
    segment_id: "EM-003", region: "APAC",
    emotional_risk: "high", behavior_pattern: "panic_cascade", emotional_severity: "volatile",
    recommended_action: "behavior_circuit_breaker",
    sentiment_score: 65.0, rationality_score: 52.0, bias_score: 42.0, resilience_score: 52.0,
    emotional_composite: 53.4, has_emotional_crisis: true, requires_behavioral_intervention: true,
    estimated_sentiment_disruption_index: 3.36,
    emotional_signal: "High — sentiment 40% — confiance 38% — volatilité 75% — composite 53",
  },
  {
    segment_id: "EM-007", region: "NAMER",
    emotional_risk: "high", behavior_pattern: "cognitive_bias_surge", emotional_severity: "volatile",
    recommended_action: "bias_correction",
    sentiment_score: 52.0, rationality_score: 65.0, bias_score: 42.0, resilience_score: 41.0,
    emotional_composite: 50.55, has_emotional_crisis: true, requires_behavioral_intervention: true,
    estimated_sentiment_disruption_index: 3.08,
    emotional_signal: "High — sentiment 45% — confiance 42% — volatilité 55% — composite 51",
  },
  {
    segment_id: "EM-006", region: "EMEA",
    emotional_risk: "moderate", behavior_pattern: "cognitive_bias_surge", emotional_severity: "watchful",
    recommended_action: "sentiment_monitoring",
    sentiment_score: 32.0, rationality_score: 45.0, bias_score: 42.0, resilience_score: 34.0,
    emotional_composite: 38.15, has_emotional_crisis: false, requires_behavioral_intervention: true,
    estimated_sentiment_disruption_index: 1.95,
    emotional_signal: "Moderate — sentiment 52% — confiance 50% — volatilité 42% — composite 38",
  },
  {
    segment_id: "EM-004", region: "LATAM",
    emotional_risk: "moderate", behavior_pattern: "none", emotional_severity: "watchful",
    recommended_action: "sentiment_monitoring",
    sentiment_score: 21.0, rationality_score: 21.0, bias_score: 20.0, resilience_score: 21.0,
    emotional_composite: 20.75, has_emotional_crisis: false, requires_behavioral_intervention: false,
    estimated_sentiment_disruption_index: 0.95,
    emotional_signal: "Moderate — sentiment 58% — confiance 55% — volatilité 38% — composite 21",
  },
  {
    segment_id: "EM-002", region: "NAMER",
    emotional_risk: "low", behavior_pattern: "none", emotional_severity: "rational",
    recommended_action: "no_action",
    sentiment_score: 0.0, rationality_score: 0.0, bias_score: 0.0, resilience_score: 0.0,
    emotional_composite: 0.0, has_emotional_crisis: false, requires_behavioral_intervention: false,
    estimated_sentiment_disruption_index: 0.0,
    emotional_signal: "Comportement marché rationnel — sentiment positif, biais contenus, résilience émotionnelle forte",
  },
  {
    segment_id: "EM-008", region: "APAC",
    emotional_risk: "low", behavior_pattern: "none", emotional_severity: "rational",
    recommended_action: "no_action",
    sentiment_score: 0.0, rationality_score: 0.0, bias_score: 0.0, resilience_score: 0.0,
    emotional_composite: 0.0, has_emotional_crisis: false, requires_behavioral_intervention: false,
    estimated_sentiment_disruption_index: 0.0,
    emotional_signal: "Comportement marché rationnel — sentiment positif, biais contenus, résilience émotionnelle forte",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (!process.env.SWARM_API_URL) {
  console.warn("[emotional-intelligence-market-behavior-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    const pattern_counts:  Record<string, number> = {};
    const severity_counts: Record<string, number> = {};
    const action_counts:   Record<string, number> = {};
    let total_comp = 0, total_sent = 0, total_rat = 0, total_bias = 0, total_res = 0, total_idx = 0;

    for (const s of mockSegments) {
      risk_counts[s.emotional_risk]         = (risk_counts[s.emotional_risk] || 0) + 1;
      pattern_counts[s.behavior_pattern]    = (pattern_counts[s.behavior_pattern] || 0) + 1;
      severity_counts[s.emotional_severity] = (severity_counts[s.emotional_severity] || 0) + 1;
      action_counts[s.recommended_action]   = (action_counts[s.recommended_action] || 0) + 1;
      total_comp += s.emotional_composite;
      total_sent += s.sentiment_score;
      total_rat  += s.rationality_score;
      total_bias += s.bias_score;
      total_res  += s.resilience_score;
      total_idx  += s.estimated_sentiment_disruption_index;
    }

    const n = mockSegments.length;
    return sealResponse(NextResponse.json(sealResponse({
      segments,
      summary: {
        total:                                       n,
        risk_counts,
        pattern_counts,
        severity_counts,
        action_counts,
        avg_emotional_composite:                     Math.round((total_comp / n) * 100) / 100,
        emotional_crisis_count:                      mockSegments.filter((s) => s.has_emotional_crisis).length,
        behavioral_intervention_count:               mockSegments.filter((s) => s.requires_behavioral_intervention).length,
        avg_sentiment_score:                         Math.round((total_sent / n) * 100) / 100,
        avg_rationality_score:                       Math.round((total_rat  / n) * 100) / 100,
        avg_bias_score:                              Math.round((total_bias / n) * 100) / 100,
        avg_resilience_score:                        Math.round((total_res  / n) * 100) / 100,
        avg_estimated_sentiment_disruption_index:    Math.round((total_idx  / n) * 100) / 100,
      },
    } as Record<string,unknown>)));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/emotional-intelligence-market-behavior-engine`);
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(await res.json()));
  } catch {}

  return sealResponse(NextResponse.json(sealResponse({ segments: [], summary: {} } as Record<string,unknown>), { status: 502 }));
}
