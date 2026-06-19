import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockCerts = [
  {
    cert_id: "ST-001", region: "North America",
    cert_risk: "low", cert_pattern: "none", cert_severity: "current",
    recommended_action: "no_action",
    expiry_score: 8.0, gap_score: 6.0, audit_score: 10.0, compliance_score: 8.0,
    cert_composite: 8.05, has_cert_risk: false, requires_immediate_action: false,
    estimated_compliance_gap_index: 0.24,
    cert_signal: "Certification posture current — all standards up-to-date and audit-ready",
  },
  {
    cert_id: "ST-002", region: "EMEA",
    cert_risk: "moderate", cert_pattern: "none", cert_severity: "due_soon",
    recommended_action: "renewal_scheduling",
    expiry_score: 22.0, gap_score: 14.0, audit_score: 15.0, compliance_score: 22.0,
    cert_composite: 18.35, has_cert_risk: false, requires_immediate_action: false,
    estimated_compliance_gap_index: 1.47,
    cert_signal: "Moderate — 165d to expiry — gap 32% — 1 audit findings — composite 18",
  },
  {
    cert_id: "ST-003", region: "APAC",
    cert_risk: "moderate", cert_pattern: "compliance_gap", cert_severity: "due_soon",
    recommended_action: "renewal_scheduling",
    expiry_score: 14.0, gap_score: 28.0, audit_score: 18.0, compliance_score: 20.0,
    cert_composite: 19.7, has_cert_risk: false, requires_immediate_action: false,
    estimated_compliance_gap_index: 2.17,
    cert_signal: "Moderate — 200d to expiry — gap 45% — 2 audit findings — composite 20",
  },
  {
    cert_id: "ST-004", region: "LATAM",
    cert_risk: "high", cert_pattern: "standard_obsolescence", cert_severity: "overdue",
    recommended_action: "standard_update",
    expiry_score: 44.0, gap_score: 48.0, audit_score: 30.0, compliance_score: 38.0,
    cert_composite: 40.7, has_cert_risk: true, requires_immediate_action: true,
    estimated_compliance_gap_index: 4.07,
    cert_signal: "High — 120d to expiry — gap 58% — 2 audit findings — composite 41",
  },
  {
    cert_id: "ST-005", region: "North America",
    cert_risk: "high", cert_pattern: "audit_failure", cert_severity: "overdue",
    recommended_action: "audit_preparation",
    expiry_score: 30.0, gap_score: 30.0, audit_score: 70.0, compliance_score: 28.0,
    cert_composite: 41.1, has_cert_risk: true, requires_immediate_action: true,
    estimated_compliance_gap_index: 4.52,
    cert_signal: "High — 150d to expiry — gap 50% — 4 audit findings — composite 41",
  },
  {
    cert_id: "ST-006", region: "EMEA",
    cert_risk: "high", cert_pattern: "new_requirement", cert_severity: "overdue",
    recommended_action: "regulatory_submission",
    expiry_score: 38.0, gap_score: 40.0, audit_score: 25.0, compliance_score: 44.0,
    cert_composite: 36.75, has_cert_risk: true, requires_immediate_action: false,
    estimated_compliance_gap_index: 3.68,
    cert_signal: "High — 95d to expiry — gap 55% — 1 audit findings — composite 37",
  },
  {
    cert_id: "ST-007", region: "APAC",
    cert_risk: "critical", cert_pattern: "certification_expiry", cert_severity: "expired",
    recommended_action: "emergency_recertification",
    expiry_score: 100.0, gap_score: 75.0, audit_score: 55.0, compliance_score: 60.0,
    cert_composite: 74.75, has_cert_risk: true, requires_immediate_action: true,
    estimated_compliance_gap_index: 8.96,
    cert_signal: "Critical — 15d to expiry — gap 80% — 5 audit findings — composite 75",
  },
  {
    cert_id: "ST-008", region: "LATAM",
    cert_risk: "critical", cert_pattern: "audit_failure", cert_severity: "expired",
    recommended_action: "emergency_recertification",
    expiry_score: 78.0, gap_score: 80.0, audit_score: 85.0, compliance_score: 70.0,
    cert_composite: 78.65, has_cert_risk: true, requires_immediate_action: true,
    estimated_compliance_gap_index: 9.44,
    cert_signal: "Critical — 5d to expiry — gap 75% — 6 audit findings — composite 79",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk     = searchParams.get("risk");
  const pattern  = searchParams.get("pattern");
  const severity = searchParams.get("severity");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/certification-standards-tracker-engine`);
      if (risk)     url.searchParams.set("risk",     risk);
      if (pattern)  url.searchParams.set("pattern",  pattern);
      if (severity) url.searchParams.set("severity", severity);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let certs = [...mockCerts];
  if (risk)     certs = certs.filter((c) => c.cert_risk === risk);
  if (pattern)  certs = certs.filter((c) => c.cert_pattern === pattern);
  if (severity) certs = certs.filter((c) => c.cert_severity === severity);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_exp = 0, total_gap = 0, total_aud = 0, total_cmp = 0, total_idx = 0;

  for (const c of mockCerts) {
    risk_counts[c.cert_risk]            = (risk_counts[c.cert_risk] || 0) + 1;
    pattern_counts[c.cert_pattern]      = (pattern_counts[c.cert_pattern] || 0) + 1;
    severity_counts[c.cert_severity]    = (severity_counts[c.cert_severity] || 0) + 1;
    action_counts[c.recommended_action] = (action_counts[c.recommended_action] || 0) + 1;
    total_comp += c.cert_composite;
    total_exp  += c.expiry_score;
    total_gap  += c.gap_score;
    total_aud  += c.audit_score;
    total_cmp  += c.compliance_score;
    total_idx  += c.estimated_compliance_gap_index;
  }

  const n = mockCerts.length;

  return NextResponse.json({
    certs,
    summary: {
      total:                                   n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_cert_composite:                      Math.round((total_comp / n) * 100) / 100,
      cert_risk_count:                         mockCerts.filter((c) => c.has_cert_risk).length,
      immediate_action_count:                  mockCerts.filter((c) => c.requires_immediate_action).length,
      avg_expiry_score:                        Math.round((total_exp / n) * 100) / 100,
      avg_gap_score:                           Math.round((total_gap / n) * 100) / 100,
      avg_audit_score:                         Math.round((total_aud / n) * 100) / 100,
      avg_compliance_score:                    Math.round((total_cmp / n) * 100) / 100,
      avg_estimated_compliance_gap_index:      Math.round((total_idx / n) * 100) / 100,
    },
  });
}
