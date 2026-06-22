import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[quota-fairness-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", rep_name: "Alice Martin", region: "NAMER",
    fairness_rating: "very_fair", fairness_risk: "low",
    bias_direction: "balanced", quota_action: "maintain",
    market_alignment_score: 88.0, experience_alignment_score: 92.0,
    peer_equity_score: 85.0, attainment_sustainability_score: 90.0,
    fairness_composite: 88.5, is_over_quoted: false, is_under_quoted: false,
    estimated_fair_quota_usd: 1150000.0,
    fairness_signal: "primary fairness gap: peer equity",
    annual_quota_usd: 1200000.0,
  },
  {
    rep_id: "rep_002", rep_name: "Bruno Silva", region: "EMEA",
    fairness_rating: "unfair", fairness_risk: "critical",
    bias_direction: "over_quoted", quota_action: "reduce_quota",
    market_alignment_score: 18.0, experience_alignment_score: 22.0,
    peer_equity_score: 15.0, attainment_sustainability_score: 12.0,
    fairness_composite: 17.3, is_over_quoted: true, is_under_quoted: false,
    estimated_fair_quota_usd: 680000.0,
    fairness_signal: "quota is 42% above peers in similar territories — review required",
    annual_quota_usd: 1400000.0,
  },
  {
    rep_id: "rep_003", rep_name: "Clara Nguyen", region: "APAC",
    fairness_rating: "very_fair", fairness_risk: "low",
    bias_direction: "balanced", quota_action: "maintain",
    market_alignment_score: 92.0, experience_alignment_score: 95.0,
    peer_equity_score: 88.0, attainment_sustainability_score: 94.0,
    fairness_composite: 92.0, is_over_quoted: false, is_under_quoted: false,
    estimated_fair_quota_usd: 1050000.0,
    fairness_signal: "primary fairness gap: peer equity",
    annual_quota_usd: 1000000.0,
  },
  {
    rep_id: "rep_004", rep_name: "Diego Ferreira", region: "LATAM",
    fairness_rating: "questionable", fairness_risk: "high",
    bias_direction: "over_quoted", quota_action: "reduce_quota",
    market_alignment_score: 32.0, experience_alignment_score: 28.0,
    peer_equity_score: 22.0, attainment_sustainability_score: 18.0,
    fairness_composite: 26.3, is_over_quoted: true, is_under_quoted: false,
    estimated_fair_quota_usd: 520000.0,
    fairness_signal: "quota increased 35% YoY while prior attainment was 48%",
    annual_quota_usd: 900000.0,
  },
  {
    rep_id: "rep_005", rep_name: "Elena Kovacs", region: "EMEA",
    fairness_rating: "fair", fairness_risk: "moderate",
    bias_direction: "balanced", quota_action: "recalibrate_territory",
    market_alignment_score: 58.0, experience_alignment_score: 62.0,
    peer_equity_score: 55.0, attainment_sustainability_score: 52.0,
    fairness_composite: 57.3, is_over_quoted: false, is_under_quoted: false,
    estimated_fair_quota_usd: 1100000.0,
    fairness_signal: "primary fairness gap: attainment sustainability",
    annual_quota_usd: 1100000.0,
  },
  {
    rep_id: "rep_006", rep_name: "Felix Okafor", region: "NAMER",
    fairness_rating: "unfair", fairness_risk: "critical",
    bias_direction: "under_quoted", quota_action: "increase_quota",
    market_alignment_score: 15.0, experience_alignment_score: 20.0,
    peer_equity_score: 12.0, attainment_sustainability_score: 8.0,
    fairness_composite: 14.3, is_over_quoted: false, is_under_quoted: true,
    estimated_fair_quota_usd: 1350000.0,
    fairness_signal: "quota is 30% below peers — potential under-assignment",
    annual_quota_usd: 700000.0,
  },
  {
    rep_id: "rep_007", rep_name: "Gabriela Torres", region: "LATAM",
    fairness_rating: "very_fair", fairness_risk: "low",
    bias_direction: "balanced", quota_action: "maintain",
    market_alignment_score: 80.0, experience_alignment_score: 78.0,
    peer_equity_score: 82.0, attainment_sustainability_score: 76.0,
    fairness_composite: 79.3, is_over_quoted: false, is_under_quoted: false,
    estimated_fair_quota_usd: 980000.0,
    fairness_signal: "primary fairness gap: experience alignment",
    annual_quota_usd: 950000.0,
  },
  {
    rep_id: "rep_008", rep_name: "Hiro Tanaka", region: "APAC",
    fairness_rating: "questionable", fairness_risk: "moderate",
    bias_direction: "balanced", quota_action: "recalibrate_territory",
    market_alignment_score: 42.0, experience_alignment_score: 48.0,
    peer_equity_score: 38.0, attainment_sustainability_score: 44.0,
    fairness_composite: 43.3, is_over_quoted: false, is_under_quoted: false,
    estimated_fair_quota_usd: 870000.0,
    fairness_signal: "team average attainment 55% — systemic over-quota across team",
    annual_quota_usd: 800000.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const rating = searchParams.get("rating");
  const risk   = searchParams.get("risk");
  const bias   = searchParams.get("bias");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/quota-fairness-engine`);
      if (rating) url.searchParams.set("rating", rating);
      if (risk)   url.searchParams.set("risk", risk);
      if (bias)   url.searchParams.set("bias", bias);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (rating) reps = reps.filter((r) => r.fairness_rating === rating);
  if (risk)   reps = reps.filter((r) => r.fairness_risk === risk);
  if (bias)   reps = reps.filter((r) => r.bias_direction === bias);

  const rating_counts: Record<string, number> = {};
  const risk_counts:   Record<string, number> = {};
  const bias_counts:   Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_comp = 0, total_mkt = 0, total_exp = 0, total_peer = 0, total_att = 0;

  for (const r of mockReps) {
    rating_counts[r.fairness_rating] = (rating_counts[r.fairness_rating] || 0) + 1;
    risk_counts[r.fairness_risk]     = (risk_counts[r.fairness_risk] || 0) + 1;
    bias_counts[r.bias_direction]    = (bias_counts[r.bias_direction] || 0) + 1;
    action_counts[r.quota_action]    = (action_counts[r.quota_action] || 0) + 1;
    total_comp  += r.fairness_composite;
    total_mkt   += r.market_alignment_score;
    total_exp   += r.experience_alignment_score;
    total_peer  += r.peer_equity_score;
    total_att   += r.attainment_sustainability_score;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total: n,
      fairness_counts: rating_counts,
      risk_counts,
      bias_counts,
      action_counts,
      avg_fairness_composite:             Math.round((total_comp / n) * 10) / 10,
      over_quoted_count:                  mockReps.filter((r) => r.is_over_quoted).length,
      under_quoted_count:                 mockReps.filter((r) => r.is_under_quoted).length,
      avg_market_alignment_score:         Math.round((total_mkt / n) * 10) / 10,
      avg_experience_alignment_score:     Math.round((total_exp / n) * 10) / 10,
      avg_peer_equity_score:              Math.round((total_peer / n) * 10) / 10,
      avg_attainment_sustainability_score: Math.round((total_att / n) * 10) / 10,
      total_quota_adjustment_opportunity_usd: Math.round(
        mockReps.filter((r) => r.is_over_quoted || r.is_under_quoted)
          .reduce((s, r) => s + Math.abs(r.estimated_fair_quota_usd - r.annual_quota_usd), 0)
      ),
    },
  }));
}
