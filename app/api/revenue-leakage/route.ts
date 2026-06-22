import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[revenue-leakage] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", rep_name: "Sophie Martin",
    region: "EMEA", segment: "enterprise",
    leakage_category: "moderate", leakage_risk: "high",
    leakage_pattern: "multiyear_miss", leakage_action: "deal_structuring",
    discount_leakage_score: 34.0, process_leakage_score: 28.5,
    champion_leakage_score: 42.3, expansion_leakage_score: 52.0,
    total_leakage_score: 37.4, estimated_lost_revenue: 401800,
    recovery_potential: 48.1,
    is_high_risk: true, needs_attention: false,
    total_deals: 40, avg_deal_size: 22000,
  },
  {
    rep_id: "rep_002", rep_name: "Marcus Johnson",
    region: "NAMER", segment: "enterprise",
    leakage_category: "critical", leakage_risk: "critical",
    leakage_pattern: "discount_heavy", leakage_action: "urgent_intervention",
    discount_leakage_score: 78.2, process_leakage_score: 55.4,
    champion_leakage_score: 38.6, expansion_leakage_score: 44.1,
    total_leakage_score: 58.9, estimated_lost_revenue: 724500,
    recovery_potential: 71.2,
    is_high_risk: true, needs_attention: true,
    total_deals: 52, avg_deal_size: 28000,
  },
  {
    rep_id: "rep_003", rep_name: "Priya Patel",
    region: "APAC", segment: "mid-market",
    leakage_category: "minimal", leakage_risk: "low",
    leakage_pattern: "mixed", leakage_action: "monitor",
    discount_leakage_score: 18.3, process_leakage_score: 14.2,
    champion_leakage_score: 12.8, expansion_leakage_score: 20.5,
    total_leakage_score: 15.8, estimated_lost_revenue: 68200,
    recovery_potential: 24.3,
    is_high_risk: false, needs_attention: false,
    total_deals: 38, avg_deal_size: 12000,
  },
  {
    rep_id: "rep_004", rep_name: "David Reyes",
    region: "LATAM", segment: "mid-market",
    leakage_category: "significant", leakage_risk: "high",
    leakage_pattern: "champion_deficit", leakage_action: "champion_coaching",
    discount_leakage_score: 28.4, process_leakage_score: 42.1,
    champion_leakage_score: 68.5, expansion_leakage_score: 35.6,
    total_leakage_score: 42.8, estimated_lost_revenue: 318600,
    recovery_potential: 55.8,
    is_high_risk: true, needs_attention: true,
    total_deals: 35, avg_deal_size: 16000,
  },
  {
    rep_id: "rep_005", rep_name: "Elena Vasquez",
    region: "EMEA", segment: "enterprise",
    leakage_category: "moderate", leakage_risk: "medium",
    leakage_pattern: "late_stage_loss", leakage_action: "deal_structuring",
    discount_leakage_score: 22.6, process_leakage_score: 48.3,
    champion_leakage_score: 24.7, expansion_leakage_score: 28.2,
    total_leakage_score: 32.1, estimated_lost_revenue: 242400,
    recovery_potential: 38.4,
    is_high_risk: false, needs_attention: false,
    total_deals: 44, avg_deal_size: 19000,
  },
  {
    rep_id: "rep_006", rep_name: "James Chen",
    region: "NAMER", segment: "smb",
    leakage_category: "minimal", leakage_risk: "low",
    leakage_pattern: "mixed", leakage_action: "monitor",
    discount_leakage_score: 12.1, process_leakage_score: 16.4,
    champion_leakage_score: 18.2, expansion_leakage_score: 14.8,
    total_leakage_score: 14.6, estimated_lost_revenue: 42800,
    recovery_potential: 18.6,
    is_high_risk: false, needs_attention: false,
    total_deals: 62, avg_deal_size: 6500,
  },
  {
    rep_id: "rep_007", rep_name: "Fatima Al-Hassan",
    region: "MEA", segment: "enterprise",
    leakage_category: "significant", leakage_risk: "high",
    leakage_pattern: "discount_heavy", leakage_action: "pricing_review",
    discount_leakage_score: 62.4, process_leakage_score: 28.6,
    champion_leakage_score: 32.1, expansion_leakage_score: 38.4,
    total_leakage_score: 40.2, estimated_lost_revenue: 298500,
    recovery_potential: 52.1,
    is_high_risk: true, needs_attention: true,
    total_deals: 28, avg_deal_size: 32000,
  },
  {
    rep_id: "rep_008", rep_name: "Lucas Müller",
    region: "EMEA", segment: "mid-market",
    leakage_category: "moderate", leakage_risk: "medium",
    leakage_pattern: "multiyear_miss", leakage_action: "deal_structuring",
    discount_leakage_score: 24.8, process_leakage_score: 22.3,
    champion_leakage_score: 28.6, expansion_leakage_score: 54.2,
    total_leakage_score: 29.7, estimated_lost_revenue: 186400,
    recovery_potential: 41.3,
    is_high_risk: false, needs_attention: false,
    total_deals: 45, avg_deal_size: 14000,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const category = searchParams.get("category");
  const risk     = searchParams.get("risk");
  const region   = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/revenue-leakage`);
      if (category) url.searchParams.set("category", category);
      if (risk)     url.searchParams.set("risk", risk);
      if (region)   url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (category) reps = reps.filter((r) => r.leakage_category === category);
  if (risk)     reps = reps.filter((r) => r.leakage_risk === risk);
  if (region)   reps = reps.filter((r) => r.region === region);

  const category_counts: Record<string, number> = {};
  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_discount = 0, total_score = 0, total_lost = 0,
      total_recovery = 0, total_process = 0;

  for (const r of mockReps) {
    category_counts[r.leakage_category] = (category_counts[r.leakage_category] || 0) + 1;
    risk_counts[r.leakage_risk]         = (risk_counts[r.leakage_risk] || 0) + 1;
    pattern_counts[r.leakage_pattern]   = (pattern_counts[r.leakage_pattern] || 0) + 1;
    action_counts[r.leakage_action]     = (action_counts[r.leakage_action] || 0) + 1;
    total_discount += r.discount_leakage_score;
    total_score    += r.total_leakage_score;
    total_lost     += r.estimated_lost_revenue;
    total_recovery += r.recovery_potential;
    total_process  += r.process_leakage_score;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total:                        n,
      category_counts,
      risk_counts,
      pattern_counts,
      action_counts,
      avg_discount_leakage_score:   Math.round((total_discount / n) * 10) / 10,
      avg_total_leakage_score:      Math.round((total_score / n) * 10) / 10,
      total_estimated_lost_revenue: Math.round(total_lost),
      high_risk_count:              mockReps.filter((r) => r.is_high_risk).length,
      coaching_count:               mockReps.filter((r) => r.needs_attention).length,
      avg_recovery_potential:       Math.round((total_recovery / n) * 10) / 10,
      total_pipeline_value_at_risk: Math.round(total_lost),
      avg_process_leakage_score:    Math.round((total_process / n) * 10) / 10,
    },
  }));
}
