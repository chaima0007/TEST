import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[legal-regulatory-watch-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockJurisdictions = [
  {
    jurisdiction_id: "LR-001", domain: "tax", region: "EMEA",
    legal_risk: "critical", regulatory_pattern: "litigation_risk",
    legal_severity: "critical", recommended_action: "emergency_compliance",
    compliance_score_out: 75, litigation_score: 83, licensing_score: 45, regulatory_score: 53,
    legal_composite: 66.5, has_legal_exposure: true,
    requires_immediate_counsel: true,
    estimated_legal_risk_index: 9.32,
    legal_signal: "Risque litige — conformité 15% — litiges 3 — expiration licence 0j — composite 67",
  },
  {
    jurisdiction_id: "LR-002", domain: "labor", region: "NAMER",
    legal_risk: "low", regulatory_pattern: "none",
    legal_severity: "compliant", recommended_action: "no_action",
    compliance_score_out: 0, litigation_score: 0, licensing_score: 0, regulatory_score: 0,
    legal_composite: 0.0, has_legal_exposure: false,
    requires_immediate_counsel: false,
    estimated_legal_risk_index: 0.01,
    legal_signal: "Conformité juridique solide — aucun litige, licences à jour, conformité réglementaire maintenue",
  },
  {
    jurisdiction_id: "LR-003", domain: "data_privacy", region: "APAC",
    legal_risk: "moderate", regulatory_pattern: "regulatory_change",
    legal_severity: "watch", recommended_action: "regulatory_monitoring",
    compliance_score_out: 53, litigation_score: 14, licensing_score: 6, regulatory_score: 82,
    legal_composite: 37.3, has_legal_exposure: true,
    requires_immediate_counsel: true,
    estimated_legal_risk_index: 2.06,
    legal_signal: "Changement réglementaire — conformité 55% — litiges 1 — expiration licence 120j — composite 37",
  },
  {
    jurisdiction_id: "LR-004", domain: "financial", region: "LATAM",
    legal_risk: "low", regulatory_pattern: "none",
    legal_severity: "compliant", recommended_action: "no_action",
    compliance_score_out: 0, litigation_score: 0, licensing_score: 0, regulatory_score: 6,
    legal_composite: 1.2, has_legal_exposure: false,
    requires_immediate_counsel: false,
    estimated_legal_risk_index: 0.01,
    legal_signal: "Conformité juridique solide — aucun litige, licences à jour, conformité réglementaire maintenue",
  },
  {
    jurisdiction_id: "LR-005", domain: "trade", region: "EMEA",
    legal_risk: "high", regulatory_pattern: "litigation_risk",
    legal_severity: "exposed", recommended_action: "litigation_response",
    compliance_score_out: 14, litigation_score: 55, licensing_score: 30, regulatory_score: 53,
    legal_composite: 38.45, has_legal_exposure: true,
    requires_immediate_counsel: true,
    estimated_legal_risk_index: 2.59,
    legal_signal: "Risque litige — conformité 60% — litiges 2 — expiration licence 90j — composite 38",
  },
  {
    jurisdiction_id: "LR-006", domain: "environmental", region: "NAMER",
    legal_risk: "low", regulatory_pattern: "none",
    legal_severity: "compliant", recommended_action: "no_action",
    compliance_score_out: 6, litigation_score: 6, licensing_score: 6, regulatory_score: 24,
    legal_composite: 10.35, has_legal_exposure: false,
    requires_immediate_counsel: false,
    estimated_legal_risk_index: 0.38,
    legal_signal: "Conformité juridique solide — aucun litige, licences à jour, conformité réglementaire maintenue",
  },
  {
    jurisdiction_id: "LR-007", domain: "healthcare", region: "APAC",
    legal_risk: "high", regulatory_pattern: "licensing_breach",
    legal_severity: "exposed", recommended_action: "licensing_remediation",
    compliance_score_out: 36, litigation_score: 20, licensing_score: 68, regulatory_score: 26,
    legal_composite: 38.7, has_legal_exposure: true,
    requires_immediate_counsel: true,
    estimated_legal_risk_index: 2.36,
    legal_signal: "Violation licence — conformité 68% — litiges 1 — expiration licence 15j — composite 39",
  },
  {
    jurisdiction_id: "LR-008", domain: "tax", region: "MEA",
    legal_risk: "critical", regulatory_pattern: "litigation_risk",
    legal_severity: "critical", recommended_action: "emergency_compliance",
    compliance_score_out: 75, litigation_score: 100, licensing_score: 28, regulatory_score: 53,
    legal_composite: 72.1, has_legal_exposure: true,
    requires_immediate_counsel: true,
    estimated_legal_risk_index: 6.93,
    legal_signal: "Risque litige — conformité 28% — litiges 7 — expiration licence 45j — composite 72",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");
  const region  = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/legal-regulatory-watch-engine`);
      if (risk)    url.searchParams.set("risk",    risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      if (region)  url.searchParams.set("region",  region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let jurisdictions = [...mockJurisdictions];
  if (risk)    jurisdictions = jurisdictions.filter((j) => j.legal_risk === risk);
  if (pattern) jurisdictions = jurisdictions.filter((j) => j.regulatory_pattern === pattern);
  if (region)  jurisdictions = jurisdictions.filter((j) => j.region === region);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_comp_s = 0, total_lit = 0, total_lic = 0,
      total_reg = 0, total_idx = 0;

  for (const j of mockJurisdictions) {
    risk_counts[j.legal_risk]           = (risk_counts[j.legal_risk] || 0) + 1;
    pattern_counts[j.regulatory_pattern] = (pattern_counts[j.regulatory_pattern] || 0) + 1;
    severity_counts[j.legal_severity]   = (severity_counts[j.legal_severity] || 0) + 1;
    action_counts[j.recommended_action] = (action_counts[j.recommended_action] || 0) + 1;
    total_comp   += j.legal_composite;
    total_comp_s += j.compliance_score_out;
    total_lit    += j.litigation_score;
    total_lic    += j.licensing_score;
    total_reg    += j.regulatory_score;
    total_idx    += j.estimated_legal_risk_index;
  }

  const n = mockJurisdictions.length;

  return sealResponse(NextResponse.json(sealResponse({
    jurisdictions,
    summary: {
      total:                          n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_legal_composite:            Math.round((total_comp / n) * 10) / 10,
      legal_exposure_count:           mockJurisdictions.filter((j) => j.has_legal_exposure).length,
      immediate_counsel_count:        mockJurisdictions.filter((j) => j.requires_immediate_counsel).length,
      avg_compliance_score:           Math.round((total_comp_s / n) * 10) / 10,
      avg_litigation_score:           Math.round((total_lit / n) * 10) / 10,
      avg_licensing_score:            Math.round((total_lic / n) * 10) / 10,
      avg_regulatory_score:           Math.round((total_reg / n) * 10) / 10,
      avg_estimated_legal_risk_index: Math.round((total_idx / n) * 100) / 100,
    },
  } as Record<string,unknown>)));
}
