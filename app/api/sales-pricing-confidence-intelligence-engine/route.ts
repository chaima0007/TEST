import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    pricing_risk: "low", pricing_pattern: "none",
    pricing_severity: "confident", recommended_action: "no_action",
    confidence_score: 0.0, value_score: 0.0,
    discipline_score: 0.0, competitive_score: 0.0,
    pricing_composite: 0.0,
    has_pricing_gap: false, requires_pricing_coaching: false,
    estimated_margin_erosion_usd: 0.0,
    pricing_signal: "Pricing confidence healthy — discount discipline, value articulation, and competitive positioning within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    pricing_risk: "low", pricing_pattern: "none",
    pricing_severity: "confident", recommended_action: "no_action",
    confidence_score: 4.0, value_score: 3.0,
    discipline_score: 5.0, competitive_score: 2.0,
    pricing_composite: 3.65,
    has_pricing_gap: false, requires_pricing_coaching: false,
    estimated_margin_erosion_usd: 0.0,
    pricing_signal: "Pricing confidence healthy — discount discipline, value articulation, and competitive positioning within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    pricing_risk: "moderate", pricing_pattern: "value_articulation_gap",
    pricing_severity: "cautious", recommended_action: "value_selling_coaching",
    confidence_score: 18.0, value_score: 28.0,
    discipline_score: 15.0, competitive_score: 12.0,
    pricing_composite: 19.15,
    has_pricing_gap: false, requires_pricing_coaching: true,
    estimated_margin_erosion_usd: 52000.0,
    pricing_signal: "Value articulation gap — 12% avg final discount — 28% preemptive discounting — 18% full-price closes — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    pricing_risk: "moderate", pricing_pattern: "anchor_too_low",
    pricing_severity: "cautious", recommended_action: "value_selling_coaching",
    confidence_score: 22.0, value_score: 20.0,
    discipline_score: 25.0, competitive_score: 18.0,
    pricing_composite: 21.7,
    has_pricing_gap: false, requires_pricing_coaching: true,
    estimated_margin_erosion_usd: 108000.0,
    pricing_signal: "Anchor too low — 15% avg final discount — 32% preemptive discounting — 20% full-price closes — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    pricing_risk: "high", pricing_pattern: "preemptive_discounting",
    pricing_severity: "hesitant", recommended_action: "negotiation_confidence_coaching",
    confidence_score: 45.0, value_score: 38.0,
    discipline_score: 40.0, competitive_score: 30.0,
    pricing_composite: 39.35,
    has_pricing_gap: false, requires_pricing_coaching: true,
    estimated_margin_erosion_usd: 264000.0,
    pricing_signal: "Preemptive discounting — 18% avg final discount — 55% preemptive discounting — 10% full-price closes — composite 39",
  },
  {
    rep_id: "rep_006", region: "West",
    pricing_risk: "high", pricing_pattern: "competitor_price_panic",
    pricing_severity: "hesitant", recommended_action: "negotiation_confidence_coaching",
    confidence_score: 52.0, value_score: 42.0,
    discipline_score: 48.0, competitive_score: 55.0,
    pricing_composite: 49.35,
    has_pricing_gap: true, requires_pricing_coaching: true,
    estimated_margin_erosion_usd: 480000.0,
    pricing_signal: "Competitor price panic — 22% avg final discount — 48% preemptive discounting — 8% full-price closes — composite 49",
  },
  {
    rep_id: "rep_007", region: "APAC",
    pricing_risk: "critical", pricing_pattern: "approval_escalation_dependency",
    pricing_severity: "capitulating", recommended_action: "approval_process_coaching",
    confidence_score: 70.0, value_score: 65.0,
    discipline_score: 68.0, competitive_score: 72.0,
    pricing_composite: 68.7,
    has_pricing_gap: true, requires_pricing_coaching: true,
    estimated_margin_erosion_usd: 1200000.0,
    pricing_signal: "Approval escalation dependency — 30% avg final discount — 65% preemptive discounting — 5% full-price closes — composite 69",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    pricing_risk: "critical", pricing_pattern: "approval_escalation_dependency",
    pricing_severity: "capitulating", recommended_action: "approval_process_coaching",
    confidence_score: 100.0, value_score: 100.0,
    discipline_score: 100.0, competitive_score: 100.0,
    pricing_composite: 100.0,
    has_pricing_gap: true, requires_pricing_coaching: true,
    estimated_margin_erosion_usd: 5500000.0,
    pricing_signal: "Approval escalation dependency — 35% avg final discount — 70% preemptive discounting — 3% full-price closes — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-pricing-confidence-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.pricing_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.pricing_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_con = 0, total_val = 0, total_dis = 0, total_com = 0, total_loss = 0;

  for (const r of mockReps) {
    risk_counts[r.pricing_risk]       = (risk_counts[r.pricing_risk] || 0) + 1;
    pattern_counts[r.pricing_pattern] = (pattern_counts[r.pricing_pattern] || 0) + 1;
    severity_counts[r.pricing_severity] = (severity_counts[r.pricing_severity] || 0) + 1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
    total_comp += r.pricing_composite;
    total_con  += r.confidence_score;
    total_val  += r.value_score;
    total_dis  += r.discipline_score;
    total_com  += r.competitive_score;
    total_loss += r.estimated_margin_erosion_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_pricing_composite:                Math.round((total_comp / n) * 10) / 10,
      pricing_gap_count:                    mockReps.filter((r) => r.has_pricing_gap).length,
      coaching_count:                       mockReps.filter((r) => r.requires_pricing_coaching).length,
      avg_confidence_score:                 Math.round((total_con / n) * 10) / 10,
      avg_value_score:                      Math.round((total_val / n) * 10) / 10,
      avg_discipline_score:                 Math.round((total_dis / n) * 10) / 10,
      avg_competitive_score:                Math.round((total_com / n) * 10) / 10,
      total_estimated_margin_erosion_usd:   Math.round(total_loss * 100) / 100,
    },
  });
}
