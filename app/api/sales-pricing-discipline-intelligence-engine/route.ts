import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    pricing_risk: "low", pricing_pattern: "none",
    pricing_severity: "disciplined", recommended_action: "no_action",
    discount_depth_score: 0.0, discount_frequency_score: 0.0,
    margin_protection_score: 0.0, negotiation_discipline_score: 0.0,
    pricing_composite: 0.0,
    has_pricing_gap: false, requires_pricing_coaching: false,
    estimated_margin_loss_usd: 0.0,
    pricing_signal: "Pricing discipline strong — discount depth, frequency, and negotiation posture within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    pricing_risk: "low", pricing_pattern: "none",
    pricing_severity: "disciplined", recommended_action: "no_action",
    discount_depth_score: 4.0, discount_frequency_score: 3.0,
    margin_protection_score: 5.0, negotiation_discipline_score: 2.0,
    pricing_composite: 3.55,
    has_pricing_gap: false, requires_pricing_coaching: true,
    estimated_margin_loss_usd: 0.0,
    pricing_signal: "Pricing discipline strong — discount depth, frequency, and negotiation posture within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    pricing_risk: "moderate", pricing_pattern: "value_misaligner",
    pricing_severity: "managed", recommended_action: "discount_awareness_coaching",
    discount_depth_score: 20.0, discount_frequency_score: 22.0,
    margin_protection_score: 18.0, negotiation_discipline_score: 15.0,
    pricing_composite: 19.25,
    has_pricing_gap: true, requires_pricing_coaching: true,
    estimated_margin_loss_usd: 42000.0,
    pricing_signal: "Value misaligner — 12% avg discount — 42% deals discounted — 48% avg gross margin — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    pricing_risk: "moderate", pricing_pattern: "discount_reflex",
    pricing_severity: "managed", recommended_action: "discount_awareness_coaching",
    discount_depth_score: 22.0, discount_frequency_score: 28.0,
    margin_protection_score: 18.0, negotiation_discipline_score: 12.0,
    pricing_composite: 20.9,
    has_pricing_gap: true, requires_pricing_coaching: true,
    estimated_margin_loss_usd: 68000.0,
    pricing_signal: "Discount reflex — 14% avg discount — 45% deals discounted — 45% avg gross margin — composite 21",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    pricing_risk: "high", pricing_pattern: "late_stage_capitulator",
    pricing_severity: "aggressive", recommended_action: "negotiation_discipline_coaching",
    discount_depth_score: 40.0, discount_frequency_score: 38.0,
    margin_protection_score: 42.0, negotiation_discipline_score: 35.0,
    pricing_composite: 38.85,
    has_pricing_gap: true, requires_pricing_coaching: true,
    estimated_margin_loss_usd: 195000.0,
    pricing_signal: "Late-stage capitulator — 20% avg discount — 60% deals discounted — 38% avg gross margin — composite 39",
  },
  {
    rep_id: "rep_006", region: "West",
    pricing_risk: "high", pricing_pattern: "multi_discount_stacker",
    pricing_severity: "aggressive", recommended_action: "margin_recovery_coaching",
    discount_depth_score: 48.0, discount_frequency_score: 42.0,
    margin_protection_score: 40.0, negotiation_discipline_score: 50.0,
    pricing_composite: 44.9,
    has_pricing_gap: true, requires_pricing_coaching: true,
    estimated_margin_loss_usd: 364000.0,
    pricing_signal: "Multi-discount stacker — 22% avg discount — 68% deals discounted — 34% avg gross margin — composite 45",
  },
  {
    rep_id: "rep_007", region: "APAC",
    pricing_risk: "critical", pricing_pattern: "margin_eroder",
    pricing_severity: "uncontrolled", recommended_action: "pricing_intervention",
    discount_depth_score: 72.0, discount_frequency_score: 65.0,
    margin_protection_score: 68.0, negotiation_discipline_score: 70.0,
    pricing_composite: 69.05,
    has_pricing_gap: true, requires_pricing_coaching: true,
    estimated_margin_loss_usd: 966000.0,
    pricing_signal: "Margin eroder — 28% avg discount — 78% deals discounted — 28% avg gross margin — composite 69",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    pricing_risk: "critical", pricing_pattern: "discount_reflex",
    pricing_severity: "uncontrolled", recommended_action: "pricing_approval_requirement",
    discount_depth_score: 100.0, discount_frequency_score: 100.0,
    margin_protection_score: 100.0, negotiation_discipline_score: 100.0,
    pricing_composite: 100.0,
    has_pricing_gap: true, requires_pricing_coaching: true,
    estimated_margin_loss_usd: 2500000.0,
    pricing_signal: "Discount reflex — 35% avg discount — 88% deals discounted — 22% avg gross margin — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-pricing-discipline-intelligence-engine`);
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
  let total_comp = 0, tdd = 0, tdf = 0, tmp = 0, tnd = 0, total_margin = 0;

  for (const r of mockReps) {
    risk_counts[r.pricing_risk]           = (risk_counts[r.pricing_risk] || 0) + 1;
    pattern_counts[r.pricing_pattern]     = (pattern_counts[r.pricing_pattern] || 0) + 1;
    severity_counts[r.pricing_severity]   = (severity_counts[r.pricing_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp   += r.pricing_composite;
    tdd          += r.discount_depth_score;
    tdf          += r.discount_frequency_score;
    tmp          += r.margin_protection_score;
    tnd          += r.negotiation_discipline_score;
    total_margin += r.estimated_margin_loss_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                 n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_pricing_composite:                 Math.round((total_comp / n) * 10) / 10,
      pricing_gap_count:                     mockReps.filter((r) => r.has_pricing_gap).length,
      coaching_count:                        mockReps.filter((r) => r.requires_pricing_coaching).length,
      avg_discount_depth_score:              Math.round((tdd / n) * 10) / 10,
      avg_discount_frequency_score:          Math.round((tdf / n) * 10) / 10,
      avg_margin_protection_score:           Math.round((tmp / n) * 10) / 10,
      avg_negotiation_discipline_score:      Math.round((tnd / n) * 10) / 10,
      total_estimated_margin_loss_usd:       Math.round(total_margin * 100) / 100,
    },
  });
}
