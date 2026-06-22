import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[ethics-compliance-sentinel-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAgents = [
  {
    agent_id: "EC-001", region: "EU-West", agent_type: "recommendation_engine",
    compliance_risk: "low", compliance_pattern: "none",
    compliance_severity: "compliant", recommended_action: "no_action",
    bias_score: 4.0, privacy_score: 2.0, ethics_score: 3.0, regulatory_score: 1.0,
    compliance_composite: 2.8,
    has_compliance_flag: false, requires_immediate_review: false,
    estimated_liability_index: 0.03,
    compliance_signal: "Compliance posture strong — bias, privacy, ethics and regulatory indicators within acceptable thresholds",
  },
  {
    agent_id: "EC-002", region: "APAC", agent_type: "content_classifier",
    compliance_risk: "moderate", compliance_pattern: "transparency_failure",
    compliance_severity: "watchlist", recommended_action: "compliance_monitoring",
    bias_score: 14.0, privacy_score: 8.0, ethics_score: 18.0, regulatory_score: 10.0,
    compliance_composite: 12.9,
    has_compliance_flag: false, requires_immediate_review: false,
    estimated_liability_index: 0.15,
    compliance_signal: "moderate — bias 18% — consent 92% — lag 12d — composite 13",
  },
  {
    agent_id: "EC-003", region: "NA-East", agent_type: "decision_support_agent",
    compliance_risk: "moderate", compliance_pattern: "regulatory_gap",
    compliance_severity: "watchlist", recommended_action: "compliance_monitoring",
    bias_score: 22.0, privacy_score: 8.0, ethics_score: 12.0, regulatory_score: 40.0,
    compliance_composite: 20.2,
    has_compliance_flag: false, requires_immediate_review: true,
    estimated_liability_index: 0.28,
    compliance_signal: "moderate — bias 22% — consent 90% — lag 48d — composite 20",
  },
  {
    agent_id: "EC-004", region: "EU-Central", agent_type: "data_pipeline_agent",
    compliance_risk: "high", compliance_pattern: "gdpr_violation",
    compliance_severity: "non_compliant", recommended_action: "gdpr_remediation",
    bias_score: 8.0, privacy_score: 75.0, ethics_score: 10.0, regulatory_score: 18.0,
    compliance_composite: 29.4,
    has_compliance_flag: false, requires_immediate_review: true,
    estimated_liability_index: 0.56,
    compliance_signal: "high — bias 12% — consent 68% — lag 20d — composite 29",
  },
  {
    agent_id: "EC-005", region: "LATAM", agent_type: "hiring_screener",
    compliance_risk: "high", compliance_pattern: "bias_detection",
    compliance_severity: "non_compliant", recommended_action: "bias_review",
    bias_score: 75.0, privacy_score: 22.0, ethics_score: 15.0, regulatory_score: 12.0,
    compliance_composite: 37.2,
    has_compliance_flag: true, requires_immediate_review: true,
    estimated_liability_index: 1.12,
    compliance_signal: "high — bias 58% — consent 84% — lag 18d — composite 37",
  },
  {
    agent_id: "EC-006", region: "MEA", agent_type: "credit_scoring_agent",
    compliance_risk: "high", compliance_pattern: "ethical_breach",
    compliance_severity: "non_compliant", recommended_action: "ethical_committee_review",
    bias_score: 30.0, privacy_score: 18.0, ethics_score: 80.0, regulatory_score: 22.0,
    compliance_composite: 38.6,
    has_compliance_flag: true, requires_immediate_review: true,
    estimated_liability_index: 0.95,
    compliance_signal: "high — bias 28% — consent 88% — lag 32d — composite 39",
  },
  {
    agent_id: "EC-007", region: "NA-West", agent_type: "medical_diagnosis_agent",
    compliance_risk: "critical", compliance_pattern: "bias_detection",
    compliance_severity: "breach", recommended_action: "legal_escalation",
    bias_score: 100.0, privacy_score: 55.0, ethics_score: 70.0, regulatory_score: 60.0,
    compliance_composite: 74.0,
    has_compliance_flag: true, requires_immediate_review: true,
    estimated_liability_index: 4.22,
    compliance_signal: "critical — bias 72% — consent 71% — lag 65d — composite 74",
  },
  {
    agent_id: "EC-008", region: "EU-North", agent_type: "financial_advisor_agent",
    compliance_risk: "critical", compliance_pattern: "gdpr_violation",
    compliance_severity: "breach", recommended_action: "legal_escalation",
    bias_score: 60.0, privacy_score: 100.0, ethics_score: 100.0, regulatory_score: 100.0,
    compliance_composite: 89.0,
    has_compliance_flag: true, requires_immediate_review: true,
    estimated_liability_index: 9.01,
    compliance_signal: "critical — bias 65% — consent 62% — lag 75d — composite 89",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/ethics-compliance-sentinel-engine`);
      if (risk)    url.searchParams.set("risk",    risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let agents = [...mockAgents];
  if (risk)    agents = agents.filter((a) => a.compliance_risk    === risk);
  if (pattern) agents = agents.filter((a) => a.compliance_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_bias = 0, total_priv = 0, total_eth = 0, total_reg = 0, total_liab = 0;

  for (const a of mockAgents) {
    risk_counts[a.compliance_risk]       = (risk_counts[a.compliance_risk] || 0) + 1;
    pattern_counts[a.compliance_pattern] = (pattern_counts[a.compliance_pattern] || 0) + 1;
    severity_counts[a.compliance_severity] = (severity_counts[a.compliance_severity] || 0) + 1;
    action_counts[a.recommended_action]  = (action_counts[a.recommended_action] || 0) + 1;
    total_comp += a.compliance_composite;
    total_bias += a.bias_score;
    total_priv += a.privacy_score;
    total_eth  += a.ethics_score;
    total_reg  += a.regulatory_score;
    total_liab += a.estimated_liability_index;
  }

  const n = mockAgents.length;

  return sealResponse(NextResponse.json(sealResponse({
    agents,
    summary: {
      total:                          n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_compliance_composite:       Math.round((total_comp / n) * 10) / 10,
      compliance_flag_count:          mockAgents.filter((a) => a.has_compliance_flag).length,
      immediate_review_count:         mockAgents.filter((a) => a.requires_immediate_review).length,
      avg_bias_score:                 Math.round((total_bias / n) * 10) / 10,
      avg_privacy_score:              Math.round((total_priv / n) * 10) / 10,
      avg_ethics_score:               Math.round((total_eth  / n) * 10) / 10,
      avg_regulatory_score:           Math.round((total_reg  / n) * 10) / 10,
      avg_estimated_liability_index:  Math.round((total_liab / n) * 100) / 100,
    },
  } as Record<string,unknown>)));
}
