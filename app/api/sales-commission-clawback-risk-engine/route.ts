import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", rep_id: "rep_001", rep_name: "Alice Chen", region: "West",
    deal_value_usd: 120000.0, commission_paid_usd: 9600.0,
    clawback_risk: "low", clawback_likelihood: "unlikely",
    primary_clawback_reason: "none", recommended_action: "no_action",
    payment_risk_score: 5.0, customer_stability_score: 8.0,
    deal_integrity_score: 3.0, rep_risk_score: 0.0,
    clawback_composite: 5.0, is_clawback_likely: false, requires_commission_hold: false,
    estimated_clawback_usd: 480.0,
    clawback_signal: "deal appears stable — low clawback risk",
  },
  {
    deal_id: "deal_002", rep_id: "rep_002", rep_name: "Marcus Hayes", region: "East",
    deal_value_usd: 250000.0, commission_paid_usd: 20000.0,
    clawback_risk: "moderate", clawback_likelihood: "possible",
    primary_clawback_reason: "payment_failure", recommended_action: "hold_commission",
    payment_risk_score: 47.0, customer_stability_score: 25.0,
    deal_integrity_score: 10.0, rep_risk_score: 15.0,
    clawback_composite: 29.8, is_clawback_likely: false, requires_commission_hold: true,
    estimated_clawback_usd: 5960.0,
    clawback_signal: "1 payment failure(s) — first payment not yet received — composite 30",
  },
  {
    deal_id: "deal_003", rep_id: "rep_003", rep_name: "Sofia Reyes", region: "Central",
    deal_value_usd: 85000.0, commission_paid_usd: 6800.0,
    clawback_risk: "moderate", clawback_likelihood: "possible",
    primary_clawback_reason: "deal_revision", recommended_action: "hold_commission",
    payment_risk_score: 20.0, customer_stability_score: 42.0,
    deal_integrity_score: 32.0, rep_risk_score: 0.0,
    clawback_composite: 26.5, is_clawback_likely: false, requires_commission_hold: false,
    estimated_clawback_usd: 1802.0,
    clawback_signal: "discount 22.0% vs avg 8.0% — deal may require revision — composite 27",
  },
  {
    deal_id: "deal_004", rep_id: "rep_004", rep_name: "Ryan Blackwell", region: "Southeast",
    deal_value_usd: 400000.0, commission_paid_usd: 32000.0,
    clawback_risk: "high", clawback_likelihood: "probable",
    primary_clawback_reason: "contract_dispute", recommended_action: "partial_clawback",
    payment_risk_score: 60.0, customer_stability_score: 55.0,
    deal_integrity_score: 70.0, rep_risk_score: 35.0,
    clawback_composite: 57.3, is_clawback_likely: true, requires_commission_hold: true,
    estimated_clawback_usd: 18336.0,
    clawback_signal: "legal hold or contract dispute — commission at risk — composite 57",
  },
  {
    deal_id: "deal_005", rep_id: "rep_005", rep_name: "Priya Nair", region: "Northeast",
    deal_value_usd: 650000.0, commission_paid_usd: 52000.0,
    clawback_risk: "critical", clawback_likelihood: "imminent",
    primary_clawback_reason: "early_cancellation", recommended_action: "full_clawback",
    payment_risk_score: 82.0, customer_stability_score: 88.0,
    deal_integrity_score: 75.0, rep_risk_score: 60.0,
    clawback_composite: 80.0, is_clawback_likely: true, requires_commission_hold: true,
    estimated_clawback_usd: 41600.0,
    clawback_signal: "cancellation request active — deal at high clawback risk — composite 80",
  },
  {
    deal_id: "deal_006", rep_id: "rep_006", rep_name: "Jordan Walsh", region: "Northwest",
    deal_value_usd: 75000.0, commission_paid_usd: 6000.0,
    clawback_risk: "low", clawback_likelihood: "unlikely",
    primary_clawback_reason: "none", recommended_action: "no_action",
    payment_risk_score: 4.0, customer_stability_score: 6.0,
    deal_integrity_score: 2.0, rep_risk_score: 0.0,
    clawback_composite: 3.8, is_clawback_likely: false, requires_commission_hold: false,
    estimated_clawback_usd: 228.0,
    clawback_signal: "deal appears stable — low clawback risk",
  },
  {
    deal_id: "deal_007", rep_id: "rep_007", rep_name: "Caleb Stone", region: "Southwest",
    deal_value_usd: 180000.0, commission_paid_usd: 14400.0,
    clawback_risk: "moderate", clawback_likelihood: "possible",
    primary_clawback_reason: "customer_bankruptcy", recommended_action: "hold_commission",
    payment_risk_score: 35.0, customer_stability_score: 68.0,
    deal_integrity_score: 15.0, rep_risk_score: 15.0,
    clawback_composite: 38.4, is_clawback_likely: false, requires_commission_hold: true,
    estimated_clawback_usd: 5530.0,
    clawback_signal: "customer health score 22/100 — high churn risk — composite 38",
  },
  {
    deal_id: "deal_008", rep_id: "rep_008", rep_name: "Nina Cross", region: "Central",
    deal_value_usd: 95000.0, commission_paid_usd: 7600.0,
    clawback_risk: "high", clawback_likelihood: "probable",
    primary_clawback_reason: "payment_failure", recommended_action: "partial_clawback",
    payment_risk_score: 71.0, customer_stability_score: 48.0,
    deal_integrity_score: 10.0, rep_risk_score: 35.0,
    clawback_composite: 52.8, is_clawback_likely: true, requires_commission_hold: true,
    estimated_clawback_usd: 4013.0,
    clawback_signal: "2 payment failure(s) — first payment not yet received — composite 53",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk       = searchParams.get("risk");
  const likelihood = searchParams.get("likelihood");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-commission-clawback-risk-engine`);
      if (risk)       url.searchParams.set("risk",       risk);
      if (likelihood) url.searchParams.set("likelihood", likelihood);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (risk)       deals = deals.filter((d) => d.clawback_risk        === risk);
  if (likelihood) deals = deals.filter((d) => d.clawback_likelihood  === likelihood);

  const risk_counts:       Record<string, number> = {};
  const likelihood_counts: Record<string, number> = {};
  const reason_counts:     Record<string, number> = {};
  const action_counts:     Record<string, number> = {};
  let total_comp = 0, total_pay = 0, total_stab = 0, total_int = 0, total_rep = 0, total_claw = 0;

  for (const d of mockDeals) {
    risk_counts[d.clawback_risk]              = (risk_counts[d.clawback_risk] || 0) + 1;
    likelihood_counts[d.clawback_likelihood]  = (likelihood_counts[d.clawback_likelihood] || 0) + 1;
    reason_counts[d.primary_clawback_reason]  = (reason_counts[d.primary_clawback_reason] || 0) + 1;
    action_counts[d.recommended_action]       = (action_counts[d.recommended_action] || 0) + 1;
    total_comp += d.clawback_composite;
    total_pay  += d.payment_risk_score;
    total_stab += d.customer_stability_score;
    total_int  += d.deal_integrity_score;
    total_rep  += d.rep_risk_score;
    total_claw += d.estimated_clawback_usd;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total:                          n,
      risk_counts,
      likelihood_counts,
      reason_counts,
      action_counts,
      avg_clawback_composite:         Math.round((total_comp / n) * 10) / 10,
      clawback_likely_count:          mockDeals.filter((d) => d.is_clawback_likely).length,
      commission_hold_count:          mockDeals.filter((d) => d.requires_commission_hold).length,
      avg_payment_risk_score:         Math.round((total_pay  / n) * 10) / 10,
      avg_customer_stability_score:   Math.round((total_stab / n) * 10) / 10,
      avg_deal_integrity_score:       Math.round((total_int  / n) * 10) / 10,
      avg_rep_risk_score:             Math.round((total_rep  / n) * 10) / 10,
      total_estimated_clawback_usd:   Math.round(total_claw),
    },
  });
}
