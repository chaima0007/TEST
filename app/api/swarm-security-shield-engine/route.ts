import { NextResponse } from "next/server";

const MOCK_AGENTS = [
  { agent_id:"AGT-001", agent_type:"sales_crm",           region:"EMEA",  hardcoded_secret_detected:0.92, env_var_exposure_risk:0.88, api_key_rotation_days_overdue:110, credential_in_plaintext_count:3, unauthorized_access_attempts:14, privilege_escalation_attempts:2, anomalous_access_pattern_score:0.85, inactive_user_access_count:4, prompt_injection_attempts:7, sql_injection_attempts:4, xss_attempt_count:3, input_validation_failure_rate:0.35, pii_exposure_risk_score:0.80, data_encryption_compliance_pct:0.35, gdpr_compliance_score:0.22, data_retention_violation_count:4, audit_log_completeness_pct:0.45, security_scan_days_overdue:115, open_vulnerability_count:11, mfa_enforcement_pct:0.18 },
  { agent_id:"AGT-002", agent_type:"finance_billing",      region:"NAMER", hardcoded_secret_detected:0.02, env_var_exposure_risk:0.05, api_key_rotation_days_overdue:10, credential_in_plaintext_count:0, unauthorized_access_attempts:0, privilege_escalation_attempts:0, anomalous_access_pattern_score:0.05, inactive_user_access_count:0, prompt_injection_attempts:0, sql_injection_attempts:0, xss_attempt_count:0, input_validation_failure_rate:0.01, pii_exposure_risk_score:0.05, data_encryption_compliance_pct:0.98, gdpr_compliance_score:0.98, data_retention_violation_count:0, audit_log_completeness_pct:0.99, security_scan_days_overdue:5, open_vulnerability_count:0, mfa_enforcement_pct:0.99 },
  { agent_id:"AGT-003", agent_type:"customer_service",     region:"APAC",  hardcoded_secret_detected:0.35, env_var_exposure_risk:0.40, api_key_rotation_days_overdue:45, credential_in_plaintext_count:1, unauthorized_access_attempts:5, privilege_escalation_attempts:0, anomalous_access_pattern_score:0.42, inactive_user_access_count:2, prompt_injection_attempts:2, sql_injection_attempts:1, xss_attempt_count:1, input_validation_failure_rate:0.12, pii_exposure_risk_score:0.30, data_encryption_compliance_pct:0.72, gdpr_compliance_score:0.68, data_retention_violation_count:2, audit_log_completeness_pct:0.78, security_scan_days_overdue:40, open_vulnerability_count:4, mfa_enforcement_pct:0.65 },
  { agent_id:"AGT-004", agent_type:"it_monitoring",        region:"LATAM", hardcoded_secret_detected:0.01, env_var_exposure_risk:0.02, api_key_rotation_days_overdue:8, credential_in_plaintext_count:0, unauthorized_access_attempts:1, privilege_escalation_attempts:0, anomalous_access_pattern_score:0.08, inactive_user_access_count:0, prompt_injection_attempts:0, sql_injection_attempts:0, xss_attempt_count:0, input_validation_failure_rate:0.02, pii_exposure_risk_score:0.04, data_encryption_compliance_pct:0.99, gdpr_compliance_score:0.97, data_retention_violation_count:0, audit_log_completeness_pct:0.99, security_scan_days_overdue:3, open_vulnerability_count:1, mfa_enforcement_pct:1.00 },
  { agent_id:"AGT-005", agent_type:"data_analytics",       region:"EMEA",  hardcoded_secret_detected:0.75, env_var_exposure_risk:0.70, api_key_rotation_days_overdue:95, credential_in_plaintext_count:2, unauthorized_access_attempts:12, privilege_escalation_attempts:2, anomalous_access_pattern_score:0.78, inactive_user_access_count:3, prompt_injection_attempts:5, sql_injection_attempts:3, xss_attempt_count:2, input_validation_failure_rate:0.28, pii_exposure_risk_score:0.65, data_encryption_compliance_pct:0.42, gdpr_compliance_score:0.38, data_retention_violation_count:3, audit_log_completeness_pct:0.55, security_scan_days_overdue:90, open_vulnerability_count:9, mfa_enforcement_pct:0.35 },
  { agent_id:"AGT-006", agent_type:"order_management",     region:"NAMER", hardcoded_secret_detected:0.10, env_var_exposure_risk:0.12, api_key_rotation_days_overdue:20, credential_in_plaintext_count:0, unauthorized_access_attempts:2, privilege_escalation_attempts:0, anomalous_access_pattern_score:0.18, inactive_user_access_count:1, prompt_injection_attempts:1, sql_injection_attempts:0, xss_attempt_count:0, input_validation_failure_rate:0.04, pii_exposure_risk_score:0.12, data_encryption_compliance_pct:0.90, gdpr_compliance_score:0.88, data_retention_violation_count:0, audit_log_completeness_pct:0.92, security_scan_days_overdue:18, open_vulnerability_count:2, mfa_enforcement_pct:0.88 },
  { agent_id:"AGT-007", agent_type:"marketing_leads",      region:"APAC",  hardcoded_secret_detected:0.55, env_var_exposure_risk:0.50, api_key_rotation_days_overdue:65, credential_in_plaintext_count:2, unauthorized_access_attempts:8, privilege_escalation_attempts:1, anomalous_access_pattern_score:0.60, inactive_user_access_count:2, prompt_injection_attempts:3, sql_injection_attempts:2, xss_attempt_count:2, input_validation_failure_rate:0.22, pii_exposure_risk_score:0.50, data_encryption_compliance_pct:0.55, gdpr_compliance_score:0.50, data_retention_violation_count:2, audit_log_completeness_pct:0.62, security_scan_days_overdue:60, open_vulnerability_count:7, mfa_enforcement_pct:0.50 },
  { agent_id:"AGT-008", agent_type:"recruitment",          region:"MEA",   hardcoded_secret_detected:0.08, env_var_exposure_risk:0.10, api_key_rotation_days_overdue:15, credential_in_plaintext_count:0, unauthorized_access_attempts:1, privilege_escalation_attempts:0, anomalous_access_pattern_score:0.12, inactive_user_access_count:0, prompt_injection_attempts:0, sql_injection_attempts:0, xss_attempt_count:0, input_validation_failure_rate:0.03, pii_exposure_risk_score:0.10, data_encryption_compliance_pct:0.93, gdpr_compliance_score:0.92, data_retention_violation_count:0, audit_log_completeness_pct:0.95, security_scan_days_overdue:12, open_vulnerability_count:1, mfa_enforcement_pct:0.92 },
];

type Agt = typeof MOCK_AGENTS[0];

function credentialScore(i: Agt): number {
  let s = 0;
  if      (i.hardcoded_secret_detected     >= 0.80) s += 40; else if (i.hardcoded_secret_detected >= 0.40) s += 22; else if (i.hardcoded_secret_detected >= 0.10) s += 8;
  if      (i.credential_in_plaintext_count >= 3)    s += 35; else if (i.credential_in_plaintext_count >= 1) s += 18;
  if      (i.api_key_rotation_days_overdue >= 90)   s += 25; else if (i.api_key_rotation_days_overdue >= 30) s += 12;
  return Math.min(s, 100);
}
function accessScore(i: Agt): number {
  let s = 0;
  if      (i.unauthorized_access_attempts   >= 10)   s += 40; else if (i.unauthorized_access_attempts >= 5) s += 22; else if (i.unauthorized_access_attempts >= 1) s += 8;
  if      (i.anomalous_access_pattern_score >= 0.70) s += 35; else if (i.anomalous_access_pattern_score >= 0.40) s += 18; else if (i.anomalous_access_pattern_score >= 0.15) s += 6;
  if      (i.privilege_escalation_attempts  >= 2)    s += 25; else if (i.privilege_escalation_attempts >= 1) s += 12;
  return Math.min(s, 100);
}
function injectionScore(i: Agt): number {
  let s = 0;
  if      (i.prompt_injection_attempts      >= 5)    s += 45; else if (i.prompt_injection_attempts >= 2) s += 25; else if (i.prompt_injection_attempts >= 1) s += 10;
  if      (i.sql_injection_attempts         >= 3)    s += 30; else if (i.sql_injection_attempts >= 1) s += 15;
  if      (i.input_validation_failure_rate  >= 0.20) s += 25; else if (i.input_validation_failure_rate >= 0.08) s += 12;
  return Math.min(s, 100);
}
function complianceScore(i: Agt): number {
  let s = 0;
  if      (i.gdpr_compliance_score     <= 0.60) s += 40; else if (i.gdpr_compliance_score <= 0.75) s += 22; else if (i.gdpr_compliance_score <= 0.90) s += 8;
  if      (i.pii_exposure_risk_score   >= 0.50) s += 35; else if (i.pii_exposure_risk_score >= 0.25) s += 18; else if (i.pii_exposure_risk_score >= 0.10) s += 6;
  if      (i.open_vulnerability_count  >= 8)    s += 25; else if (i.open_vulnerability_count >= 3) s += 12;
  return Math.min(s, 100);
}
function composite(cr: number, ac: number, inj: number, co: number): number {
  return Math.min(Math.round((cr * 0.30 + ac * 0.25 + inj * 0.25 + co * 0.20) * 100) / 100, 100);
}
function threatPattern(i: Agt): string {
  if (i.hardcoded_secret_detected >= 0.60 || i.credential_in_plaintext_count >= 2) return "credential_exposure";
  if (i.prompt_injection_attempts >= 3 || i.sql_injection_attempts >= 2)           return "injection_attempt";
  if (i.pii_exposure_risk_score >= 0.40 && i.data_encryption_compliance_pct <= 0.70) return "data_exfiltration";
  if (i.unauthorized_access_attempts >= 8 || i.privilege_escalation_attempts >= 1) return "access_anomaly";
  if (i.gdpr_compliance_score <= 0.70 && i.data_retention_violation_count >= 2)    return "compliance_violation";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "breached"; if (c >= 40) return "threatened"; if (c >= 20) return "monitoring"; return "secure"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "injection_attempt" || p === "data_exfiltration") return "emergency_lockdown";
    return "incident_containment";
  }
  if (r === "high") {
    if (p === "credential_exposure")  return "credential_rotation";
    if (p === "injection_attempt")    return "injection_block";
    if (p === "data_exfiltration")    return "data_quarantine";
    if (p === "access_anomaly")       return "access_review";
    if (p === "compliance_violation") return "compliance_audit";
    return "security_monitoring";
  }
  if (r === "moderate") return "security_monitoring";
  return "no_action";
}
function signal(i: Agt, pat: string, comp: number): string {
  if (comp < 20) return "Security posture strong — no credential exposure, injection attempts, access anomalies or compliance gaps detected";
  const labels: Record<string,string> = { credential_exposure:"Credential exposure", injection_attempt:"Injection attempt", data_exfiltration:"Data exfiltration risk", access_anomaly:"Access anomaly", compliance_violation:"Compliance violation" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${i.unauthorized_access_attempts} unauth access — ${i.prompt_injection_attempts} injection attempts — GDPR ${Math.round(i.gdpr_compliance_score*100)}% — ${i.open_vulnerability_count} open vulns — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const agents = MOCK_AGENTS.map(i => {
      const cr = credentialScore(i), ac = accessScore(i), inj = injectionScore(i), co = complianceScore(i);
      const comp = composite(cr, ac, inj, co), pat = threatPattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      return {
        agent_id: i.agent_id, agent_type: i.agent_type, region: i.region,
        security_risk: r, threat_pattern: pat, security_severity: sev, recommended_action: act,
        credential_score: cr, access_score: ac, injection_score: inj, compliance_score: co,
        security_composite: comp,
        has_active_threat: comp >= 40 || i.prompt_injection_attempts >= 1 || i.unauthorized_access_attempts >= 5 || i.credential_in_plaintext_count >= 1,
        requires_immediate_response: comp >= 25 || i.privilege_escalation_attempts >= 1 || i.hardcoded_secret_detected >= 0.40 || i.sql_injection_attempts >= 1,
        estimated_exposure_severity: Math.min(Math.round(comp / 100 * (1 - i.gdpr_compliance_score + 0.01) * 10 * 100) / 100, 10.0),
        security_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tcr=0,tac=0,tinj=0,tco=0,tcomp=0,texpos=0,gc=0,ec=0;
    for (const a of agents) {
      rc[a.security_risk]=(rc[a.security_risk]||0)+1; pc[a.threat_pattern]=(pc[a.threat_pattern]||0)+1;
      sc[a.security_severity]=(sc[a.security_severity]||0)+1; ac[a.recommended_action]=(ac[a.recommended_action]||0)+1;
      tcr+=a.credential_score; tac+=a.access_score; tinj+=a.injection_score; tco+=a.compliance_score;
      tcomp+=a.security_composite; texpos+=a.estimated_exposure_severity;
      if (a.has_active_threat) gc++; if (a.requires_immediate_response) ec++;
    }
    const n = agents.length;
    return NextResponse.json({ agents, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_security_composite: Math.round(tcomp/n*10)/10,
      active_threat_count: gc, immediate_response_count: ec,
      avg_credential_score: Math.round(tcr/n*10)/10,
      avg_access_score: Math.round(tac/n*10)/10,
      avg_injection_score: Math.round(tinj/n*10)/10,
      avg_compliance_score: Math.round(tco/n*10)/10,
      avg_estimated_exposure_severity: Math.round(texpos/n*100)/100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/swarm-security-shield-engine`)).json());
}
