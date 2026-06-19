import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_DOSSIERS = [
  { dossier_id:"DP-001", entity_type:"customer",  region:"EMEA",  consent_validity_score:0.10, consent_recency_days:420, data_minimization_score:0.20, purpose_limitation_score:0.15, access_request_pending_days:45, erasure_request_pending_days:38, portability_request_pending_days:40, breach_detection_days_since:5, breach_notification_delay_hours:96, encryption_at_rest_pct:0.20, encryption_in_transit_pct:0.30, vulnerability_exposure_score:0.88, cross_border_transfer_unprotected:8, standard_contractual_clauses_pct:0.10, retention_excess_days:200, retention_violation_count:6, dpia_completion_pct:0.10, third_party_processor_compliance:0.15 },
  { dossier_id:"DP-002", entity_type:"employee",  region:"NAMER", consent_validity_score:0.98, consent_recency_days:15,  data_minimization_score:0.95, purpose_limitation_score:0.97, access_request_pending_days:0,  erasure_request_pending_days:0,  portability_request_pending_days:0,  breach_detection_days_since:90, breach_notification_delay_hours:0,  encryption_at_rest_pct:0.99, encryption_in_transit_pct:0.99, vulnerability_exposure_score:0.02, cross_border_transfer_unprotected:0, standard_contractual_clauses_pct:0.99, retention_excess_days:0,   retention_violation_count:0, dpia_completion_pct:0.98, third_party_processor_compliance:0.97 },
  { dossier_id:"DP-003", entity_type:"partner",   region:"APAC",  consent_validity_score:0.55, consent_recency_days:120, data_minimization_score:0.60, purpose_limitation_score:0.58, access_request_pending_days:12, erasure_request_pending_days:8,  portability_request_pending_days:5,  breach_detection_days_since:30, breach_notification_delay_hours:30, encryption_at_rest_pct:0.72, encryption_in_transit_pct:0.68, vulnerability_exposure_score:0.40, cross_border_transfer_unprotected:2, standard_contractual_clauses_pct:0.60, retention_excess_days:45,  retention_violation_count:2, dpia_completion_pct:0.65, third_party_processor_compliance:0.60 },
  { dossier_id:"DP-004", entity_type:"prospect",  region:"LATAM", consent_validity_score:0.92, consent_recency_days:45,  data_minimization_score:0.90, purpose_limitation_score:0.88, access_request_pending_days:0,  erasure_request_pending_days:1,  portability_request_pending_days:0,  breach_detection_days_since:60, breach_notification_delay_hours:0,  encryption_at_rest_pct:0.95, encryption_in_transit_pct:0.94, vulnerability_exposure_score:0.08, cross_border_transfer_unprotected:0, standard_contractual_clauses_pct:0.92, retention_excess_days:0,   retention_violation_count:0, dpia_completion_pct:0.90, third_party_processor_compliance:0.92 },
  { dossier_id:"DP-005", entity_type:"customer",  region:"EMEA",  consent_validity_score:0.25, consent_recency_days:280, data_minimization_score:0.35, purpose_limitation_score:0.30, access_request_pending_days:25, erasure_request_pending_days:20, portability_request_pending_days:18, breach_detection_days_since:12, breach_notification_delay_hours:55, encryption_at_rest_pct:0.45, encryption_in_transit_pct:0.50, vulnerability_exposure_score:0.72, cross_border_transfer_unprotected:5, standard_contractual_clauses_pct:0.30, retention_excess_days:100, retention_violation_count:4, dpia_completion_pct:0.25, third_party_processor_compliance:0.30 },
  { dossier_id:"DP-006", entity_type:"employee",  region:"MEA",   consent_validity_score:0.80, consent_recency_days:60,  data_minimization_score:0.78, purpose_limitation_score:0.82, access_request_pending_days:2,  erasure_request_pending_days:0,  portability_request_pending_days:3,  breach_detection_days_since:45, breach_notification_delay_hours:5,  encryption_at_rest_pct:0.88, encryption_in_transit_pct:0.90, vulnerability_exposure_score:0.18, cross_border_transfer_unprotected:0, standard_contractual_clauses_pct:0.85, retention_excess_days:10,  retention_violation_count:0, dpia_completion_pct:0.80, third_party_processor_compliance:0.82 },
  { dossier_id:"DP-007", entity_type:"partner",   region:"NAMER", consent_validity_score:0.42, consent_recency_days:200, data_minimization_score:0.50, purpose_limitation_score:0.45, access_request_pending_days:16, erasure_request_pending_days:12, portability_request_pending_days:10, breach_detection_days_since:20, breach_notification_delay_hours:20, encryption_at_rest_pct:0.60, encryption_in_transit_pct:0.55, vulnerability_exposure_score:0.55, cross_border_transfer_unprotected:3, standard_contractual_clauses_pct:0.48, retention_excess_days:60,  retention_violation_count:3, dpia_completion_pct:0.45, third_party_processor_compliance:0.48 },
  { dossier_id:"DP-008", entity_type:"prospect",  region:"APAC",  consent_validity_score:0.05, consent_recency_days:380, data_minimization_score:0.10, purpose_limitation_score:0.08, access_request_pending_days:50, erasure_request_pending_days:42, portability_request_pending_days:35, breach_detection_days_since:2,  breach_notification_delay_hours:80, encryption_at_rest_pct:0.15, encryption_in_transit_pct:0.20, vulnerability_exposure_score:0.92, cross_border_transfer_unprotected:9, standard_contractual_clauses_pct:0.05, retention_excess_days:250, retention_violation_count:7, dpia_completion_pct:0.05, third_party_processor_compliance:0.08 },
];

type D = typeof MOCK_DOSSIERS[0];

function rgpdScore(i: D): number {
  let s = 0;
  if      (i.consent_validity_score  <= 0.40) s += 40; else if (i.consent_validity_score  <= 0.70) s += 22; else if (i.consent_validity_score  <= 0.90) s += 8;
  if      (i.consent_recency_days    >= 365)  s += 25; else if (i.consent_recency_days    >= 180)  s += 12; else if (i.consent_recency_days    >= 90)   s += 5;
  if      (i.data_minimization_score <= 0.40) s += 20; else if (i.data_minimization_score <= 0.70) s += 10; else if (i.data_minimization_score <= 0.85) s += 4;
  if      (i.purpose_limitation_score <= 0.40) s += 15; else if (i.purpose_limitation_score <= 0.70) s += 8;
  return Math.min(s, 100);
}
function rightsScore(i: D): number {
  let s = 0;
  if      (i.access_request_pending_days      >= 30) s += 40; else if (i.access_request_pending_days      >= 10) s += 22; else if (i.access_request_pending_days      >= 1) s += 8;
  if      (i.erasure_request_pending_days     >= 30) s += 35; else if (i.erasure_request_pending_days     >= 10) s += 18; else if (i.erasure_request_pending_days     >= 1) s += 6;
  if      (i.portability_request_pending_days >= 30) s += 25; else if (i.portability_request_pending_days >= 10) s += 12; else if (i.portability_request_pending_days >= 1) s += 4;
  return Math.min(s, 100);
}
function breachScore(i: D): number {
  let s = 0;
  if      (i.breach_notification_delay_hours  >= 72)   s += 40; else if (i.breach_notification_delay_hours  >= 24) s += 22; else if (i.breach_notification_delay_hours  >= 1) s += 8;
  if      (i.vulnerability_exposure_score     >= 0.70) s += 30; else if (i.vulnerability_exposure_score     >= 0.40) s += 16; else if (i.vulnerability_exposure_score     >= 0.15) s += 6;
  if      (i.encryption_at_rest_pct           <= 0.50) s += 20; else if (i.encryption_at_rest_pct           <= 0.80) s += 10;
  if      (i.encryption_in_transit_pct        <= 0.50) s += 10; else if (i.encryption_in_transit_pct        <= 0.80) s += 5;
  return Math.min(s, 100);
}
function transferScore(i: D): number {
  let s = 0;
  if      (i.cross_border_transfer_unprotected >= 5)    s += 45; else if (i.cross_border_transfer_unprotected >= 2) s += 25; else if (i.cross_border_transfer_unprotected >= 1) s += 10;
  if      (i.standard_contractual_clauses_pct  <= 0.40) s += 35; else if (i.standard_contractual_clauses_pct  <= 0.70) s += 18; else if (i.standard_contractual_clauses_pct  <= 0.90) s += 6;
  if      (i.retention_excess_days             >= 90)   s += 20; else if (i.retention_excess_days             >= 30)   s += 10;
  return Math.min(s, 100);
}
function composite(rg: number, ri: number, br: number, tr: number): number {
  return Math.min(Math.round((rg * 0.30 + ri * 0.25 + br * 0.25 + tr * 0.20) * 100) / 100, 100);
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "breached"; if (c >= 40) return "at_risk"; if (c >= 20) return "monitoring"; return "compliant"; }
function pattern(i: D): string {
  if (i.breach_notification_delay_hours >= 24 || i.vulnerability_exposure_score >= 0.60) return "data_breach";
  if (i.consent_validity_score <= 0.40 || i.purpose_limitation_score <= 0.40)             return "consent_violation";
  if (i.access_request_pending_days >= 15 || i.erasure_request_pending_days >= 15 || i.portability_request_pending_days >= 15) return "rights_denial";
  if (i.cross_border_transfer_unprotected >= 2 || i.standard_contractual_clauses_pct <= 0.50) return "cross_border_exposure";
  if (i.retention_excess_days >= 30 || i.retention_violation_count >= 2)                   return "retention_breach";
  return "none";
}
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "data_breach") return "emergency_data_lockdown";
    if (p === "cross_border_exposure") return "transfer_suspension";
    return "regulatory_filing";
  }
  if (r === "high") {
    if (p === "data_breach")           return "breach_notification";
    if (p === "consent_violation")     return "consent_remediation";
    if (p === "rights_denial")         return "rights_processing";
    if (p === "cross_border_exposure") return "dpia_required";
    if (p === "retention_breach")      return "regulatory_filing";
    return "compliance_monitoring";
  }
  if (r === "moderate") return "compliance_monitoring";
  return "no_action";
}
function fineRisk(i: D, comp: number): number {
  const aggr = 1 + (1 - i.dpia_completion_pct) * 0.5 + (1 - i.third_party_processor_compliance) * 0.3;
  return Math.round(Math.min(comp / 100 * aggr * 10, 10.0) * 100) / 100;
}
function signal(i: D, pat: string, comp: number): string {
  if (comp < 20) return "Protection des données conforme — consentement valide, droits respectés, aucune violation détectée";
  const labels: Record<string,string> = { consent_violation:"Violation de consentement", data_breach:"Violation de données", rights_denial:"Déni des droits RGPD", cross_border_exposure:"Transfert transfrontalier non sécurisé", retention_breach:"Violation de rétention" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — consentement ${Math.round(i.consent_validity_score*100)}% — accès en retard ${i.access_request_pending_days}j — effacement en retard ${i.erasure_request_pending_days}j — transferts non protégés ${i.cross_border_transfer_unprotected} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const dossiers = MOCK_DOSSIERS.map(i => {
      const rg = rgpdScore(i), ri = rightsScore(i), br = breachScore(i), tr = transferScore(i);
      const comp = composite(rg, ri, br, tr), pat = pattern(i), r = risk(comp), sev = severity(comp), act = action(r, pat);
      return {
        dossier_id: i.dossier_id, entity_type: i.entity_type, region: i.region,
        protection_risk: r, violation_pattern: pat, protection_severity: sev, recommended_action: act,
        rgpd_score: rg, rights_score: ri, breach_score: br, transfer_score: tr,
        protection_composite: comp,
        has_active_violation: comp >= 40 || i.breach_notification_delay_hours >= 24 || i.access_request_pending_days >= 15 || i.erasure_request_pending_days >= 15 || i.cross_border_transfer_unprotected >= 2,
        requires_dpa_notification: comp >= 25 || i.breach_notification_delay_hours >= 1 || i.vulnerability_exposure_score >= 0.60 || i.cross_border_transfer_unprotected >= 3,
        estimated_fine_risk_index: fineRisk(i, comp),
        protection_signal: signal(i, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let trg=0,tri=0,tbr=0,ttr=0,tcomp=0,tfine=0,av=0,dpa=0;
    for (const d of dossiers) {
      rc[d.protection_risk]=(rc[d.protection_risk]||0)+1; pc[d.violation_pattern]=(pc[d.violation_pattern]||0)+1;
      sc[d.protection_severity]=(sc[d.protection_severity]||0)+1; ac[d.recommended_action]=(ac[d.recommended_action]||0)+1;
      trg+=d.rgpd_score; tri+=d.rights_score; tbr+=d.breach_score; ttr+=d.transfer_score;
      tcomp+=d.protection_composite; tfine+=d.estimated_fine_risk_index;
      if (d.has_active_violation) av++; if (d.requires_dpa_notification) dpa++;
    }
    const n = dossiers.length;
    return NextResponse.json(sealResponse({ dossiers, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_protection_composite: Math.round(tcomp/n*10)/10,
      active_violation_count: av, dpa_notification_count: dpa,
      avg_rgpd_score: Math.round(trg/n*10)/10,
      avg_rights_score: Math.round(tri/n*10)/10,
      avg_breach_score: Math.round(tbr/n*10)/10,
      avg_transfer_score: Math.round(ttr/n*10)/10,
      avg_estimated_fine_risk_index: Math.round(tfine/n*100)/100,
    }} as Record<string,unknown>));
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/data-protection-engine`)).json());
}
