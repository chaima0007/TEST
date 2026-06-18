import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", deal_name: "TechCorp ELA", rep_id: "rep_001",
    contamination_level: "clean", contamination_risk: "low",
    primary_contamination_type: "none", contamination_action: "proceed",
    ethics_score: 0.0, compliance_score: 5.0, financial_integrity_score: 6.3, audit_quality_score: 4.8,
    contamination_composite: 3.6, requires_legal_review: false, requires_escalation: false,
    estimated_compliance_exposure_usd: 0.0,
    contamination_signal: "deal clean — no contamination signals detected",
    deal_value_usd: 450000.0,
  },
  {
    deal_id: "deal_002", deal_name: "Meridian Finance Platform", rep_id: "rep_002",
    contamination_level: "blocked", contamination_risk: "critical",
    primary_contamination_type: "conflict_of_interest", contamination_action: "halt_deal",
    ethics_score: 70.0, compliance_score: 55.0, financial_integrity_score: 62.0, audit_quality_score: 48.0,
    contamination_composite: 60.7, requires_legal_review: true, requires_escalation: true,
    estimated_compliance_exposure_usd: 273150.0,
    contamination_signal: "conflict of interest flag raised — deal requires ethics board review",
    deal_value_usd: 900000.0,
  },
  {
    deal_id: "deal_003", deal_name: "Apex Cloud Migration", rep_id: "rep_003",
    contamination_level: "clean", contamination_risk: "low",
    primary_contamination_type: "none", contamination_action: "proceed",
    ethics_score: 0.0, compliance_score: 3.0, financial_integrity_score: 2.5, audit_quality_score: 2.0,
    contamination_composite: 1.9, requires_legal_review: false, requires_escalation: false,
    estimated_compliance_exposure_usd: 0.0,
    contamination_signal: "deal clean — no contamination signals detected",
    deal_value_usd: 280000.0,
  },
  {
    deal_id: "deal_004", deal_name: "Orion Healthcare Data Platform", rep_id: "rep_001",
    contamination_level: "review_required", contamination_risk: "high",
    primary_contamination_type: "compliance_gap", contamination_action: "legal_review",
    ethics_score: 10.0, compliance_score: 55.0, financial_integrity_score: 38.0, audit_quality_score: 42.0,
    contamination_composite: 36.3, requires_legal_review: true, requires_escalation: true,
    estimated_compliance_exposure_usd: 81675.0,
    contamination_signal: "compliance review not completed — deal cannot progress without it",
    deal_value_usd: 450000.0,
  },
  {
    deal_id: "deal_005", deal_name: "Lumina Retail Expansion", rep_id: "rep_002",
    contamination_level: "advisory", contamination_risk: "moderate",
    primary_contamination_type: "financial_irregularity", contamination_action: "escalate_to_manager",
    ethics_score: 5.0, compliance_score: 8.0, financial_integrity_score: 45.0, audit_quality_score: 28.0,
    contamination_composite: 18.7, requires_legal_review: false, requires_escalation: true,
    estimated_compliance_exposure_usd: 14025.0,
    contamination_signal: "25% discount above policy — revenue recognition risk",
    deal_value_usd: 150000.0,
  },
  {
    deal_id: "deal_006", deal_name: "Cascade Logistics Integration", rep_id: "rep_004",
    contamination_level: "review_required", contamination_risk: "high",
    primary_contamination_type: "channel_conflict", contamination_action: "escalate_to_manager",
    ethics_score: 8.0, compliance_score: 35.0, financial_integrity_score: 28.0, audit_quality_score: 55.0,
    contamination_composite: 30.8, requires_legal_review: false, requires_escalation: true,
    estimated_compliance_exposure_usd: 46200.0,
    contamination_signal: "channel conflict detected — partner agreement may be violated",
    deal_value_usd: 300000.0,
  },
  {
    deal_id: "deal_007", deal_name: "Nexus Energy Analytics", rep_id: "rep_003",
    contamination_level: "clean", contamination_risk: "low",
    primary_contamination_type: "none", contamination_action: "proceed",
    ethics_score: 0.0, compliance_score: 6.5, financial_integrity_score: 7.8, audit_quality_score: 5.2,
    contamination_composite: 4.3, requires_legal_review: false, requires_escalation: false,
    estimated_compliance_exposure_usd: 0.0,
    contamination_signal: "deal clean — no contamination signals detected",
    deal_value_usd: 220000.0,
  },
  {
    deal_id: "deal_008", deal_name: "Vertex Pharma Research Suite", rep_id: "rep_001",
    contamination_level: "blocked", contamination_risk: "critical",
    primary_contamination_type: "conflict_of_interest", contamination_action: "halt_deal",
    ethics_score: 60.0, compliance_score: 68.0, financial_integrity_score: 55.0, audit_quality_score: 35.0,
    contamination_composite: 60.0, requires_legal_review: true, requires_escalation: true,
    estimated_compliance_exposure_usd: 390000.0,
    contamination_signal: "related party involvement detected — independent review mandatory",
    deal_value_usd: 1300000.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const level = searchParams.get("level");
  const risk  = searchParams.get("risk");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/deal-contamination-risk-engine`);
      if (level) url.searchParams.set("level", level);
      if (risk)  url.searchParams.set("risk", risk);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (level) deals = deals.filter((d) => d.contamination_level === level);
  if (risk)  deals = deals.filter((d) => d.contamination_risk === risk);

  const level_counts:  Record<string, number> = {};
  const risk_counts:   Record<string, number> = {};
  const type_counts:   Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_comp = 0, total_eth = 0, total_comp_sc = 0, total_fin = 0, total_aud = 0, total_exp = 0;

  for (const d of mockDeals) {
    level_counts[d.contamination_level]           = (level_counts[d.contamination_level] || 0) + 1;
    risk_counts[d.contamination_risk]             = (risk_counts[d.contamination_risk] || 0) + 1;
    type_counts[d.primary_contamination_type]     = (type_counts[d.primary_contamination_type] || 0) + 1;
    action_counts[d.contamination_action]         = (action_counts[d.contamination_action] || 0) + 1;
    total_comp    += d.contamination_composite;
    total_eth     += d.ethics_score;
    total_comp_sc += d.compliance_score;
    total_fin     += d.financial_integrity_score;
    total_aud     += d.audit_quality_score;
    total_exp     += d.estimated_compliance_exposure_usd;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      level_counts,
      risk_counts,
      type_counts,
      action_counts,
      avg_contamination_composite:     Math.round((total_comp / n) * 10) / 10,
      legal_review_required_count:     mockDeals.filter((d) => d.requires_legal_review).length,
      escalation_required_count:       mockDeals.filter((d) => d.requires_escalation).length,
      avg_ethics_score:                Math.round((total_eth / n) * 10) / 10,
      avg_compliance_score:            Math.round((total_comp_sc / n) * 10) / 10,
      avg_financial_integrity_score:   Math.round((total_fin / n) * 10) / 10,
      avg_audit_quality_score:         Math.round((total_aud / n) * 10) / 10,
      total_compliance_exposure_usd:   Math.round(total_exp),
    },
  });
}
