import { NextResponse } from "next/server";

const MOCK_ENTITIES = [
  { entity_id:"RC-001", entity_domain:"banking",       region:"EMEA",  policy_adherence_score:0.22, regulatory_deadline_compliance:0.28, internal_audit_score:0.25, external_audit_score:0.30, sanction_history_score:0.75, reporting_accuracy:0.32, documentation_completeness:0.28, training_completion_rate:0.30, whistleblower_incident_rate:0.68, data_governance_score:0.28, third_party_compliance_score:0.32, regulatory_change_adaptation_speed:0.25, ethics_committee_effectiveness:0.28, control_testing_coverage:0.30, risk_register_completeness:0.25, legal_counsel_access_score:0.35, compliance_culture_score:0.22 },
  { entity_id:"RC-002", entity_domain:"insurance",     region:"NAMER", policy_adherence_score:0.95, regulatory_deadline_compliance:0.94, internal_audit_score:0.92, external_audit_score:0.95, sanction_history_score:0.02, reporting_accuracy:0.96, documentation_completeness:0.95, training_completion_rate:0.96, whistleblower_incident_rate:0.02, data_governance_score:0.95, third_party_compliance_score:0.94, regulatory_change_adaptation_speed:0.92, ethics_committee_effectiveness:0.95, control_testing_coverage:0.94, risk_register_completeness:0.95, legal_counsel_access_score:0.96, compliance_culture_score:0.95 },
  { entity_id:"RC-003", entity_domain:"pharma",        region:"APAC",  policy_adherence_score:0.48, regulatory_deadline_compliance:0.42, internal_audit_score:0.38, external_audit_score:0.40, sanction_history_score:0.42, reporting_accuracy:0.55, documentation_completeness:0.50, training_completion_rate:0.55, whistleblower_incident_rate:0.35, data_governance_score:0.48, third_party_compliance_score:0.52, regulatory_change_adaptation_speed:0.48, ethics_committee_effectiveness:0.50, control_testing_coverage:0.42, risk_register_completeness:0.52, legal_counsel_access_score:0.55, compliance_culture_score:0.50 },
  { entity_id:"RC-004", entity_domain:"tech",          region:"NAMER", policy_adherence_score:0.85, regulatory_deadline_compliance:0.88, internal_audit_score:0.82, external_audit_score:0.85, sanction_history_score:0.08, reporting_accuracy:0.88, documentation_completeness:0.85, training_completion_rate:0.88, whistleblower_incident_rate:0.05, data_governance_score:0.88, third_party_compliance_score:0.85, regulatory_change_adaptation_speed:0.88, ethics_committee_effectiveness:0.85, control_testing_coverage:0.82, risk_register_completeness:0.88, legal_counsel_access_score:0.92, compliance_culture_score:0.88 },
  { entity_id:"RC-005", entity_domain:"energy",        region:"EMEA",  policy_adherence_score:0.30, regulatory_deadline_compliance:0.28, internal_audit_score:0.22, external_audit_score:0.25, sanction_history_score:0.62, reporting_accuracy:0.30, documentation_completeness:0.30, training_completion_rate:0.28, whistleblower_incident_rate:0.58, data_governance_score:0.25, third_party_compliance_score:0.30, regulatory_change_adaptation_speed:0.22, ethics_committee_effectiveness:0.25, control_testing_coverage:0.22, risk_register_completeness:0.20, legal_counsel_access_score:0.28, compliance_culture_score:0.20 },
  { entity_id:"RC-006", entity_domain:"retail",        region:"LATAM", policy_adherence_score:0.62, regulatory_deadline_compliance:0.60, internal_audit_score:0.65, external_audit_score:0.62, sanction_history_score:0.18, reporting_accuracy:0.68, documentation_completeness:0.65, training_completion_rate:0.65, whistleblower_incident_rate:0.15, data_governance_score:0.65, third_party_compliance_score:0.62, regulatory_change_adaptation_speed:0.65, ethics_committee_effectiveness:0.62, control_testing_coverage:0.65, risk_register_completeness:0.68, legal_counsel_access_score:0.65, compliance_culture_score:0.65 },
  { entity_id:"RC-007", entity_domain:"manufacturing", region:"APAC",  policy_adherence_score:0.40, regulatory_deadline_compliance:0.38, internal_audit_score:0.42, external_audit_score:0.38, sanction_history_score:0.48, reporting_accuracy:0.40, documentation_completeness:0.40, training_completion_rate:0.42, whistleblower_incident_rate:0.45, data_governance_score:0.38, third_party_compliance_score:0.42, regulatory_change_adaptation_speed:0.40, ethics_committee_effectiveness:0.40, control_testing_coverage:0.38, risk_register_completeness:0.42, legal_counsel_access_score:0.42, compliance_culture_score:0.38 },
  { entity_id:"RC-008", entity_domain:"government",    region:"MEA",   policy_adherence_score:0.72, regulatory_deadline_compliance:0.70, internal_audit_score:0.75, external_audit_score:0.72, sanction_history_score:0.12, reporting_accuracy:0.72, documentation_completeness:0.70, training_completion_rate:0.72, whistleblower_incident_rate:0.10, data_governance_score:0.75, third_party_compliance_score:0.70, regulatory_change_adaptation_speed:0.72, ethics_committee_effectiveness:0.75, control_testing_coverage:0.72, risk_register_completeness:0.75, legal_counsel_access_score:0.78, compliance_culture_score:0.72 },
];

type Entity = typeof MOCK_ENTITIES[0];

function policyScore(i: Entity): number {
  let s = 0;
  if      (i.policy_adherence_score <= 0.30) s += 40; else if (i.policy_adherence_score <= 0.55) s += 22; else if (i.policy_adherence_score <= 0.75) s += 8;
  if      (i.regulatory_deadline_compliance <= 0.30) s += 35; else if (i.regulatory_deadline_compliance <= 0.55) s += 18; else if (i.regulatory_deadline_compliance <= 0.75) s += 6;
  if      (i.documentation_completeness <= 0.30) s += 25; else if (i.documentation_completeness <= 0.55) s += 12;
  return Math.min(s, 100);
}
function auditScore(i: Entity): number {
  let s = 0;
  if      (i.internal_audit_score <= 0.30) s += 40; else if (i.internal_audit_score <= 0.55) s += 22; else if (i.internal_audit_score <= 0.75) s += 8;
  if      (i.external_audit_score <= 0.30) s += 35; else if (i.external_audit_score <= 0.55) s += 18; else if (i.external_audit_score <= 0.75) s += 6;
  if      (i.control_testing_coverage <= 0.30) s += 25; else if (i.control_testing_coverage <= 0.55) s += 12;
  return Math.min(s, 100);
}
function riskScore(i: Entity): number {
  let s = 0;
  if      (i.sanction_history_score >= 0.70) s += 40; else if (i.sanction_history_score >= 0.45) s += 22; else if (i.sanction_history_score >= 0.25) s += 8;
  if      (i.whistleblower_incident_rate >= 0.70) s += 35; else if (i.whistleblower_incident_rate >= 0.45) s += 18; else if (i.whistleblower_incident_rate >= 0.25) s += 6;
  if      (i.risk_register_completeness <= 0.30) s += 25; else if (i.risk_register_completeness <= 0.55) s += 12;
  return Math.min(s, 100);
}
function cultureScore(i: Entity): number {
  let s = 0;
  if      (i.compliance_culture_score <= 0.30) s += 40; else if (i.compliance_culture_score <= 0.55) s += 22; else if (i.compliance_culture_score <= 0.75) s += 8;
  if      (i.training_completion_rate <= 0.30) s += 35; else if (i.training_completion_rate <= 0.55) s += 18; else if (i.training_completion_rate <= 0.75) s += 6;
  if      (i.ethics_committee_effectiveness <= 0.30) s += 25; else if (i.ethics_committee_effectiveness <= 0.55) s += 12;
  return Math.min(s, 100);
}
function composite(pol: number, aud: number, rsk: number, cul: number): number {
  return Math.min(Math.round((pol * 0.30 + aud * 0.25 + rsk * 0.25 + cul * 0.20) * 100) / 100, 100);
}
function compliancePattern(i: Entity): string {
  if (i.policy_adherence_score <= 0.35 || i.regulatory_deadline_compliance <= 0.35) return "regulatory_breach";
  if (i.internal_audit_score <= 0.4 && i.external_audit_score <= 0.45)              return "audit_failure";
  if (i.sanction_history_score >= 0.5 || i.whistleblower_incident_rate >= 0.5)      return "sanction_risk";
  if (i.documentation_completeness <= 0.45 || i.control_testing_coverage <= 0.4)    return "policy_gap";
  if (i.reporting_accuracy <= 0.45 || i.data_governance_score <= 0.4)               return "reporting_violation";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "violated"; if (c >= 40) return "exposed"; if (c >= 20) return "monitored"; return "compliant"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "regulatory_breach") return "regulatory_shutdown";
    if (p === "sanction_risk")     return "emergency_compliance";
    return "sanction_response";
  }
  if (r === "high") {
    if (p === "audit_failure")       return "audit_remediation";
    if (p === "regulatory_breach")   return "emergency_compliance";
    if (p === "policy_gap")          return "policy_update";
    if (p === "reporting_violation") return "regulatory_dialogue";
    return "audit_remediation";
  }
  if (r === "moderate") return "compliance_monitoring";
  return "no_action";
}
function signal(i: Entity, pat: string, comp: number): string {
  if (comp < 20) return "Conformité réglementaire exemplaire — politiques respectées, audits réussis, culture compliance forte";
  const labels: Record<string,string> = {
    regulatory_breach:"Brèche réglementaire", audit_failure:"Défaillance audit",
    sanction_risk:"Risque sanction", policy_gap:"Lacune politique", reporting_violation:"Violation reporting",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — adhésion politiques ${Math.round(i.policy_adherence_score*100)}% — audits internes ${Math.round(i.internal_audit_score*100)}% — risque sanction ${Math.round(i.sanction_history_score*100)}% — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(i => {
      const pol = policyScore(i), aud = auditScore(i), rsk = riskScore(i), cul = cultureScore(i);
      const comp = composite(pol, aud, rsk, cul), pat = compliancePattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      return {
        entity_id: i.entity_id, region: i.region,
        compliance_risk: r, compliance_pattern: pat, compliance_severity: sev, recommended_action: act,
        policy_score: pol, audit_score: aud, risk_score: rsk, culture_score: cul,
        compliance_composite: comp,
        has_compliance_breach: comp >= 40 || i.sanction_history_score >= 0.4 || i.policy_adherence_score <= 0.4 || i.external_audit_score <= 0.4,
        requires_executive_action: comp >= 25 || i.whistleblower_incident_rate >= 0.4 || i.regulatory_deadline_compliance <= 0.35,
        estimated_sanction_risk_index: Math.min(Math.round(comp/100*(1-i.legal_counsel_access_score+0.01)*10*100)/100, 10.0),
        compliance_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tpol=0,taud=0,trsk=0,tcul=0,tcomp=0,tridx=0,breachC=0,execC=0;
    for (const e of entities) {
      rc[e.compliance_risk]=(rc[e.compliance_risk]||0)+1;
      pc[e.compliance_pattern]=(pc[e.compliance_pattern]||0)+1;
      sc[e.compliance_severity]=(sc[e.compliance_severity]||0)+1;
      ac[e.recommended_action]=(ac[e.recommended_action]||0)+1;
      tpol+=e.policy_score; taud+=e.audit_score; trsk+=e.risk_score; tcul+=e.culture_score;
      tcomp+=e.compliance_composite; tridx+=e.estimated_sanction_risk_index;
      if (e.has_compliance_breach)     breachC++;
      if (e.requires_executive_action) execC++;
    }
    const n = entities.length;
    return NextResponse.json({ entities, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_compliance_composite: Math.round(tcomp/n*10)/10,
      compliance_breach_count: breachC, executive_action_count: execC,
      avg_policy_score: Math.round(tpol/n*10)/10,
      avg_audit_score: Math.round(taud/n*10)/10,
      avg_risk_score: Math.round(trsk/n*10)/10,
      avg_culture_score: Math.round(tcul/n*10)/10,
      avg_estimated_sanction_risk_index: Math.round(tridx/n*100)/100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/regulatory-compliance-legal-engine`)).json());
}
