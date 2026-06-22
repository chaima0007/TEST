import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_INVOICES = [
  { invoice_id:"INV-001", client_id:"CL-042", region:"EMEA",  days_overdue:75, payment_delay_avg_days:55, late_payment_frequency_pct:0.72, partial_payment_count:3, dispute_history_count:4, billing_error_rate_pct:0.22, credit_note_frequency:4, invoice_rejection_count:3, invoice_amount_usd:48000, total_outstanding_usd:165000, credit_limit_utilization_pct:0.92, days_sales_outstanding:85, contract_value_usd:180000, client_tenure_months:14, account_health_score:0.15, payment_terms_days:30, last_contact_days_ago:3, promise_to_pay_broken_count:3, escalation_count:3 },
  { invoice_id:"INV-002", client_id:"CL-017", region:"NAMER", days_overdue:0,  payment_delay_avg_days:5,  late_payment_frequency_pct:0.05, partial_payment_count:0, dispute_history_count:0, billing_error_rate_pct:0.01, credit_note_frequency:0, invoice_rejection_count:0, invoice_amount_usd:22000, total_outstanding_usd:22000, credit_limit_utilization_pct:0.18, days_sales_outstanding:12, contract_value_usd:120000, client_tenure_months:36, account_health_score:0.95, payment_terms_days:30, last_contact_days_ago:0, promise_to_pay_broken_count:0, escalation_count:0 },
  { invoice_id:"INV-003", client_id:"CL-089", region:"APAC",  days_overdue:25, payment_delay_avg_days:28, late_payment_frequency_pct:0.38, partial_payment_count:1, dispute_history_count:1, billing_error_rate_pct:0.08, credit_note_frequency:1, invoice_rejection_count:1, invoice_amount_usd:35000, total_outstanding_usd:78000, credit_limit_utilization_pct:0.58, days_sales_outstanding:42, contract_value_usd:90000, client_tenure_months:8, account_health_score:0.55, payment_terms_days:30, last_contact_days_ago:5, promise_to_pay_broken_count:1, escalation_count:1 },
  { invoice_id:"INV-004", client_id:"CL-003", region:"LATAM", days_overdue:0,  payment_delay_avg_days:2,  late_payment_frequency_pct:0.02, partial_payment_count:0, dispute_history_count:0, billing_error_rate_pct:0.00, credit_note_frequency:0, invoice_rejection_count:0, invoice_amount_usd:85000, total_outstanding_usd:85000, credit_limit_utilization_pct:0.10, days_sales_outstanding:8, contract_value_usd:400000, client_tenure_months:48, account_health_score:0.98, payment_terms_days:45, last_contact_days_ago:0, promise_to_pay_broken_count:0, escalation_count:0 },
  { invoice_id:"INV-005", client_id:"CL-156", region:"EMEA",  days_overdue:95, payment_delay_avg_days:68, late_payment_frequency_pct:0.85, partial_payment_count:5, dispute_history_count:6, billing_error_rate_pct:0.32, credit_note_frequency:6, invoice_rejection_count:5, invoice_amount_usd:62000, total_outstanding_usd:220000, credit_limit_utilization_pct:0.97, days_sales_outstanding:110, contract_value_usd:250000, client_tenure_months:6, account_health_score:0.08, payment_terms_days:30, last_contact_days_ago:2, promise_to_pay_broken_count:5, escalation_count:5 },
  { invoice_id:"INV-006", client_id:"CL-071", region:"NAMER", days_overdue:12, payment_delay_avg_days:15, late_payment_frequency_pct:0.22, partial_payment_count:0, dispute_history_count:1, billing_error_rate_pct:0.05, credit_note_frequency:1, invoice_rejection_count:0, invoice_amount_usd:18000, total_outstanding_usd:38000, credit_limit_utilization_pct:0.35, days_sales_outstanding:22, contract_value_usd:80000, client_tenure_months:20, account_health_score:0.72, payment_terms_days:30, last_contact_days_ago:2, promise_to_pay_broken_count:0, escalation_count:0 },
  { invoice_id:"INV-007", client_id:"CL-204", region:"APAC",  days_overdue:48, payment_delay_avg_days:42, late_payment_frequency_pct:0.55, partial_payment_count:2, dispute_history_count:3, billing_error_rate_pct:0.16, credit_note_frequency:3, invoice_rejection_count:2, invoice_amount_usd:41000, total_outstanding_usd:128000, credit_limit_utilization_pct:0.82, days_sales_outstanding:65, contract_value_usd:145000, client_tenure_months:10, account_health_score:0.32, payment_terms_days:30, last_contact_days_ago:4, promise_to_pay_broken_count:2, escalation_count:2 },
  { invoice_id:"INV-008", client_id:"CL-058", region:"MEA",   days_overdue:5,  payment_delay_avg_days:10, late_payment_frequency_pct:0.12, partial_payment_count:0, dispute_history_count:0, billing_error_rate_pct:0.03, credit_note_frequency:1, invoice_rejection_count:0, invoice_amount_usd:29000, total_outstanding_usd:55000, credit_limit_utilization_pct:0.28, days_sales_outstanding:18, contract_value_usd:160000, client_tenure_months:24, account_health_score:0.82, payment_terms_days:30, last_contact_days_ago:1, promise_to_pay_broken_count:0, escalation_count:0 },
];

type Inv = typeof MOCK_INVOICES[0];

function overdueScore(i: Inv): number {
  let s = 0;
  if      (i.days_overdue >= 60)              s += 40; else if (i.days_overdue >= 30) s += 22; else if (i.days_overdue >= 10) s += 8;
  if      (i.payment_delay_avg_days >= 45)    s += 35; else if (i.payment_delay_avg_days >= 25) s += 18; else if (i.payment_delay_avg_days >= 10) s += 6;
  if      (i.promise_to_pay_broken_count >= 3) s += 25; else if (i.promise_to_pay_broken_count >= 1) s += 12;
  return Math.min(s, 100);
}
function disputeScore(i: Inv): number {
  let s = 0;
  if      (i.dispute_history_count  >= 4)    s += 40; else if (i.dispute_history_count >= 2) s += 22; else if (i.dispute_history_count >= 1) s += 8;
  if      (i.billing_error_rate_pct >= 0.20) s += 35; else if (i.billing_error_rate_pct >= 0.10) s += 18; else if (i.billing_error_rate_pct >= 0.05) s += 6;
  if      (i.invoice_rejection_count >= 3)   s += 25; else if (i.invoice_rejection_count >= 1) s += 12;
  return Math.min(s, 100);
}
function exposureScore(i: Inv): number {
  let s = 0;
  if      (i.credit_limit_utilization_pct >= 0.90) s += 40; else if (i.credit_limit_utilization_pct >= 0.70) s += 22; else if (i.credit_limit_utilization_pct >= 0.50) s += 8;
  if      (i.days_sales_outstanding >= 75)          s += 35; else if (i.days_sales_outstanding >= 50) s += 18; else if (i.days_sales_outstanding >= 30) s += 6;
  if      (i.escalation_count >= 3)                 s += 25; else if (i.escalation_count >= 1) s += 12;
  return Math.min(s, 100);
}
function behaviorScore(i: Inv): number {
  let s = 0;
  if      (i.late_payment_frequency_pct >= 0.60) s += 45; else if (i.late_payment_frequency_pct >= 0.35) s += 25; else if (i.late_payment_frequency_pct >= 0.15) s += 10;
  if      (i.partial_payment_count >= 3)          s += 30; else if (i.partial_payment_count >= 1) s += 15;
  if      (i.credit_note_frequency >= 4)          s += 25; else if (i.credit_note_frequency >= 2) s += 12;
  return Math.min(s, 100);
}
function composite(ov: number, di: number, ex: number, bh: number): number {
  return Math.min(Math.round((ov * 0.30 + di * 0.25 + ex * 0.25 + bh * 0.20) * 100) / 100, 100);
}
function pattern(i: Inv): string {
  if (i.late_payment_frequency_pct >= 0.50 && i.payment_delay_avg_days >= 30)      return "chronic_late_payer";
  if (i.dispute_history_count >= 3 && i.billing_error_rate_pct >= 0.10)            return "dispute_prone";
  if (i.partial_payment_count >= 2 && i.promise_to_pay_broken_count >= 1)          return "partial_payment";
  if (i.billing_error_rate_pct >= 0.15 && i.credit_note_frequency >= 3)            return "billing_anomaly";
  if (i.credit_limit_utilization_pct >= 0.80 && i.days_sales_outstanding >= 60)    return "revenue_leakage";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "at_risk"; if (c >= 20) return "watchlist"; return "healthy"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "chronic_late_payer" || p === "partial_payment") return "legal_review_trigger"; return "executive_escalation"; }
  if (r === "high") {
    if (p === "chronic_late_payer") return "formal_collection_notice";
    if (p === "dispute_prone")      return "dispute_resolution_call";
    if (p === "partial_payment")    return "payment_plan_negotiation";
    if (p === "billing_anomaly")    return "billing_correction";
    if (p === "revenue_leakage")    return "executive_escalation";
    return "payment_monitoring";
  }
  if (r === "moderate") return "gentle_reminder";
  return "no_action";
}
function signal(i: Inv, pat: string, comp: number): string {
  if (comp < 20) return "Invoice health normal — payment behaviour, dispute history and exposure within acceptable thresholds";
  const labels: Record<string,string> = { chronic_late_payer:"Chronic late payer", dispute_prone:"Dispute-prone", partial_payment:"Partial payment pattern", billing_anomaly:"Billing anomaly", revenue_leakage:"Revenue leakage" };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — ${i.days_overdue}d overdue — $${Math.round(i.invoice_amount_usd/1000)}k invoice — $${Math.round(i.total_outstanding_usd/1000)}k total AR — DSO ${Math.round(i.days_sales_outstanding)}d — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[invoice-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tov=0,tdi=0,tex=0,tbh=0,tcomp=0,tbd=0,gc=0,ec=0;
    for (const inv of invoices) {
      rc[inv.invoice_risk]=(rc[inv.invoice_risk]||0)+1; pc[inv.invoice_pattern]=(pc[inv.invoice_pattern]||0)+1;
      sc[inv.invoice_severity]=(sc[inv.invoice_severity]||0)+1; ac[inv.recommended_action]=(ac[inv.recommended_action]||0)+1;
      tov+=inv.overdue_score; tdi+=inv.dispute_score; tex+=inv.exposure_score; tbh+=inv.behavior_score;
      tcomp+=inv.invoice_composite; tbd+=inv.estimated_bad_debt_usd;
      if (inv.has_collection_signal) gc++; if (inv.requires_escalation) ec++;
    }
    const n = invoices.length;
    return sealResponse(NextResponse.json(sealResponse({ invoices, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_invoice_composite: Math.round(tcomp/n*10)/10,
      collection_signal_count: gc, escalation_count: ec,
      avg_overdue_score: Math.round(tov/n*10)/10,
      avg_dispute_score: Math.round(tdi/n*10)/10,
      avg_exposure_score: Math.round(tex/n*10)/10,
      avg_behavior_score: Math.round(tbh/n*10)/10,
      total_estimated_bad_debt_usd: Math.round(tbd*100)/100,
    }} as Record<string,unknown>)));
  }
  return sealResponse(NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/invoice-intelligence-engine`, { next: { revalidate: 30 } })).json()));
}
