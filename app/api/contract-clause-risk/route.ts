import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[contract-clause-risk] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockContracts = [
  {
    contract_id: "c001", deal_name: "Apex Cloud Platform MSA", rep_id: "rep_003",
    clause_risk_level: "critical", risky_clause_pattern: "multi_clause_risk",
    negotiation_stance: "escalate_legal", contract_action: "block_signing",
    liability_risk_score: 100.0, ip_risk_score: 100.0,
    renewal_trap_score: 90.0, termination_risk_score: 74.0,
    clause_risk_composite: 94.5, estimated_financial_exposure: 1000000,
    clause_negotiability_score: 0.0, is_high_risk_contract: true, needs_legal_escalation: true,
    contract_value: 500000, contract_term_months: 36, region: "NAMER",
  },
  {
    contract_id: "c002", deal_name: "Solaris Data SaaS Agreement", rep_id: "rep_001",
    clause_risk_level: "high", risky_clause_pattern: "liability_exposure",
    negotiation_stance: "negotiate_hard", contract_action: "redline",
    liability_risk_score: 75.0, ip_risk_score: 15.0,
    renewal_trap_score: 10.0, termination_risk_score: 28.0,
    clause_risk_composite: 46.8, estimated_financial_exposure: 140400,
    clause_negotiability_score: 48.0, is_high_risk_contract: false, needs_legal_escalation: false,
    contract_value: 300000, contract_term_months: 24, region: "EMEA",
  },
  {
    contract_id: "c003", deal_name: "ZenithAI Partnership Agreement", rep_id: "rep_002",
    clause_risk_level: "low", risky_clause_pattern: "clean",
    negotiation_stance: "accept", contract_action: "proceed",
    liability_risk_score: 5.0, ip_risk_score: 0.0,
    renewal_trap_score: 0.0, termination_risk_score: 8.0,
    clause_risk_composite: 3.3, estimated_financial_exposure: 6600,
    clause_negotiability_score: 93.0, is_high_risk_contract: false, needs_legal_escalation: false,
    contract_value: 200000, contract_term_months: 12, region: "APAC",
  },
  {
    contract_id: "c004", deal_name: "Harbor Security Services MSA", rep_id: "rep_005",
    clause_risk_level: "critical", risky_clause_pattern: "ip_conflict",
    negotiation_stance: "escalate_legal", contract_action: "block_signing",
    liability_risk_score: 20.0, ip_risk_score: 85.0,
    renewal_trap_score: 25.0, termination_risk_score: 43.0,
    clause_risk_composite: 46.8, estimated_financial_exposure: 500000,
    clause_negotiability_score: 35.0, is_high_risk_contract: true, needs_legal_escalation: true,
    contract_value: 500000, contract_term_months: 36, region: "NAMER",
  },
  {
    contract_id: "c005", deal_name: "PeakFlow Analytics Subscription", rep_id: "rep_007",
    clause_risk_level: "moderate", risky_clause_pattern: "renewal_trap",
    negotiation_stance: "minor_revision", contract_action: "flag_for_review",
    liability_risk_score: 15.0, ip_risk_score: 0.0,
    renewal_trap_score: 65.0, termination_risk_score: 18.0,
    clause_risk_composite: 32.0, estimated_financial_exposure: 73600,
    clause_negotiability_score: 63.0, is_high_risk_contract: false, needs_legal_escalation: false,
    contract_value: 230000, contract_term_months: 24, region: "EMEA",
  },
  {
    contract_id: "c006", deal_name: "Orbit ERP Integration License", rep_id: "rep_004",
    clause_risk_level: "moderate", risky_clause_pattern: "termination_risk",
    negotiation_stance: "minor_revision", contract_action: "flag_for_review",
    liability_risk_score: 10.0, ip_risk_score: 0.0,
    renewal_trap_score: 5.0, termination_risk_score: 68.0,
    clause_risk_composite: 30.1, estimated_financial_exposure: 54180,
    clause_negotiability_score: 55.0, is_high_risk_contract: false, needs_legal_escalation: false,
    contract_value: 180000, contract_term_months: 36, region: "APAC",
  },
  {
    contract_id: "c007", deal_name: "Nexus Platform Enterprise", rep_id: "rep_006",
    clause_risk_level: "high", risky_clause_pattern: "multi_clause_risk",
    negotiation_stance: "negotiate_hard", contract_action: "redline",
    liability_risk_score: 55.0, ip_risk_score: 50.0,
    renewal_trap_score: 45.0, termination_risk_score: 30.0,
    clause_risk_composite: 47.0, estimated_financial_exposure: 84600,
    clause_negotiability_score: 28.0, is_high_risk_contract: false, needs_legal_escalation: false,
    contract_value: 180000, contract_term_months: 24, region: "LATAM",
  },
  {
    contract_id: "c008", deal_name: "Vertex CX SaaS Subscription", rep_id: "rep_008",
    clause_risk_level: "low", risky_clause_pattern: "clean",
    negotiation_stance: "accept", contract_action: "proceed",
    liability_risk_score: 10.0, ip_risk_score: 0.0,
    renewal_trap_score: 10.0, termination_risk_score: 5.0,
    clause_risk_composite: 5.5, estimated_financial_exposure: 10450,
    clause_negotiability_score: 90.0, is_high_risk_contract: false, needs_legal_escalation: false,
    contract_value: 190000, contract_term_months: 12, region: "NAMER",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");
  const region  = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/contract-clause-risk`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      if (region)  url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let contracts = [...mockContracts];
  if (risk)    contracts = contracts.filter((c) => c.clause_risk_level === risk);
  if (pattern) contracts = contracts.filter((c) => c.risky_clause_pattern === pattern);
  if (region)  contracts = contracts.filter((c) => c.region === region);

  const risk_counts:    Record<string, number> = {};
  const pattern_counts: Record<string, number> = {};
  const stance_counts:  Record<string, number> = {};
  const action_counts:  Record<string, number> = {};
  let total_comp = 0, total_liab = 0, total_ip = 0, total_ren = 0,
      total_neg = 0, total_exp = 0;

  for (const c of mockContracts) {
    risk_counts[c.clause_risk_level]       = (risk_counts[c.clause_risk_level] || 0) + 1;
    pattern_counts[c.risky_clause_pattern] = (pattern_counts[c.risky_clause_pattern] || 0) + 1;
    stance_counts[c.negotiation_stance]    = (stance_counts[c.negotiation_stance] || 0) + 1;
    action_counts[c.contract_action]       = (action_counts[c.contract_action] || 0) + 1;
    total_comp += c.clause_risk_composite;
    total_liab += c.liability_risk_score;
    total_ip   += c.ip_risk_score;
    total_ren  += c.renewal_trap_score;
    total_neg  += c.clause_negotiability_score;
    total_exp  += c.estimated_financial_exposure;
  }

  const n = mockContracts.length;

  return sealResponse(NextResponse.json({
    contracts,
    summary: {
      total: n,
      risk_counts,
      pattern_counts,
      stance_counts,
      action_counts,
      avg_clause_risk_composite:  Math.round((total_comp / n) * 10) / 10,
      total_financial_exposure:   Math.round(total_exp),
      high_risk_count:            mockContracts.filter((c) => c.is_high_risk_contract).length,
      legal_escalation_count:     mockContracts.filter((c) => c.needs_legal_escalation).length,
      avg_liability_risk_score:   Math.round((total_liab / n) * 10) / 10,
      avg_ip_risk_score:          Math.round((total_ip / n) * 10) / 10,
      avg_renewal_trap_score:     Math.round((total_ren / n) * 10) / 10,
      avg_negotiability_score:    Math.round((total_neg / n) * 10) / 10,
    },
  }));
}
