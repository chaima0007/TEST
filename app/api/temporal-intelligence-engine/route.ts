import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_DECISIONS = [
  // DC-001 market_entry EMEA — critical window_collapse
  { decision_id:"DC-001", decision_type:"market_entry",      region:"EMEA",  timing_window_score:0.15, market_cycle_alignment:0.32, competitor_vulnerability_index:0.35, regulatory_window_score:0.22, seasonal_demand_fit:0.30, capital_market_receptivity:0.18, first_mover_advantage_score:0.18, execution_readiness_score:0.30, macro_momentum_alignment:0.20, stakeholder_availability_score:0.32, opportunity_decay_rate:0.85, counter_timing_risk:0.82, information_freshness_score:0.45, decision_urgency_index:0.78, resource_alignment_score:0.28, geopolitical_stability_window:0.25, timing_confidence_score:0.20 },
  // DC-002 product_launch NAMER — low
  { decision_id:"DC-002", decision_type:"product_launch",    region:"NAMER", timing_window_score:0.90, market_cycle_alignment:0.88, competitor_vulnerability_index:0.85, regulatory_window_score:0.92, seasonal_demand_fit:0.88, capital_market_receptivity:0.88, first_mover_advantage_score:0.85, execution_readiness_score:0.92, macro_momentum_alignment:0.90, stakeholder_availability_score:0.88, opportunity_decay_rate:0.08, counter_timing_risk:0.08, information_freshness_score:0.92, decision_urgency_index:0.10, resource_alignment_score:0.90, geopolitical_stability_window:0.92, timing_confidence_score:0.92 },
  // DC-003 acquisition APAC — high timing_miss
  { decision_id:"DC-003", decision_type:"acquisition",       region:"APAC",  timing_window_score:0.22, market_cycle_alignment:0.25, competitor_vulnerability_index:0.50, regulatory_window_score:0.58, seasonal_demand_fit:0.48, capital_market_receptivity:0.52, first_mover_advantage_score:0.50, execution_readiness_score:0.55, macro_momentum_alignment:0.55, stakeholder_availability_score:0.55, opportunity_decay_rate:0.62, counter_timing_risk:0.58, information_freshness_score:0.60, decision_urgency_index:0.55, resource_alignment_score:0.52, geopolitical_stability_window:0.55, timing_confidence_score:0.45 },
  // DC-004 regulatory_filing LATAM — low
  { decision_id:"DC-004", decision_type:"regulatory_filing", region:"LATAM", timing_window_score:0.82, market_cycle_alignment:0.80, competitor_vulnerability_index:0.75, regulatory_window_score:0.92, seasonal_demand_fit:0.80, capital_market_receptivity:0.82, first_mover_advantage_score:0.78, execution_readiness_score:0.85, macro_momentum_alignment:0.85, stakeholder_availability_score:0.82, opportunity_decay_rate:0.10, counter_timing_risk:0.10, information_freshness_score:0.88, decision_urgency_index:0.12, resource_alignment_score:0.82, geopolitical_stability_window:0.88, timing_confidence_score:0.90 },
  // DC-005 fundraising EMEA — critical delayed_response
  { decision_id:"DC-005", decision_type:"fundraising",       region:"EMEA",  timing_window_score:0.18, market_cycle_alignment:0.35, competitor_vulnerability_index:0.40, regulatory_window_score:0.25, seasonal_demand_fit:0.35, capital_market_receptivity:0.30, first_mover_advantage_score:0.22, execution_readiness_score:0.32, macro_momentum_alignment:0.28, stakeholder_availability_score:0.30, opportunity_decay_rate:0.68, counter_timing_risk:0.80, information_freshness_score:0.42, decision_urgency_index:0.88, resource_alignment_score:0.28, geopolitical_stability_window:0.22, timing_confidence_score:0.20 },
  // DC-006 talent_hiring MEA — moderate
  { decision_id:"DC-006", decision_type:"talent_hiring",     region:"MEA",   timing_window_score:0.65, market_cycle_alignment:0.62, competitor_vulnerability_index:0.60, regulatory_window_score:0.70, seasonal_demand_fit:0.62, capital_market_receptivity:0.65, first_mover_advantage_score:0.60, execution_readiness_score:0.68, macro_momentum_alignment:0.68, stakeholder_availability_score:0.65, opportunity_decay_rate:0.30, counter_timing_risk:0.28, information_freshness_score:0.68, decision_urgency_index:0.32, resource_alignment_score:0.65, geopolitical_stability_window:0.65, timing_confidence_score:0.65 },
  // DC-007 partnership NAMER — high timing_conflict
  { decision_id:"DC-007", decision_type:"partnership",       region:"NAMER", timing_window_score:0.65, market_cycle_alignment:0.55, competitor_vulnerability_index:0.45, regulatory_window_score:0.52, seasonal_demand_fit:0.55, capital_market_receptivity:0.48, first_mover_advantage_score:0.52, execution_readiness_score:0.55, macro_momentum_alignment:0.50, stakeholder_availability_score:0.55, opportunity_decay_rate:0.62, counter_timing_risk:0.72, information_freshness_score:0.58, decision_urgency_index:0.58, resource_alignment_score:0.52, geopolitical_stability_window:0.50, timing_confidence_score:0.48 },
  // DC-008 market_exit APAC — low
  { decision_id:"DC-008", decision_type:"market_exit",       region:"APAC",  timing_window_score:0.88, market_cycle_alignment:0.85, competitor_vulnerability_index:0.80, regulatory_window_score:0.82, seasonal_demand_fit:0.85, capital_market_receptivity:0.78, first_mover_advantage_score:0.82, execution_readiness_score:0.88, macro_momentum_alignment:0.82, stakeholder_availability_score:0.85, opportunity_decay_rate:0.10, counter_timing_risk:0.08, information_freshness_score:0.88, decision_urgency_index:0.12, resource_alignment_score:0.82, geopolitical_stability_window:0.88, timing_confidence_score:0.90 },
];

type Decision = typeof MOCK_DECISIONS[0];

// Sub-scores: higher = worse timing/readiness/alignment (inverted from raw 0-1 fields where 1=good)
function opportunityScore(d: Decision): number {
  return Math.min(((1 - d.timing_window_score) + (1 - d.market_cycle_alignment) + (1 - d.first_mover_advantage_score)) / 3 * 100, 100);
}
function readinessScore(d: Decision): number {
  return Math.min(((1 - d.execution_readiness_score) + (1 - d.resource_alignment_score) + (1 - d.stakeholder_availability_score)) / 3 * 100, 100);
}
function alignmentScore(d: Decision): number {
  return Math.min(((1 - d.regulatory_window_score) + (1 - d.macro_momentum_alignment) + (1 - d.capital_market_receptivity)) / 3 * 100, 100);
}
function riskScore(d: Decision): number {
  return Math.min((d.counter_timing_risk + d.opportunity_decay_rate + d.decision_urgency_index) / 3 * 100, 100);
}
function compositeScore(opp: number, read: number, alig: number, risk: number): number {
  return Math.min(Math.round((opp * 0.30 + read * 0.25 + alig * 0.25 + risk * 0.20) * 100) / 100, 100);
}
function timingPattern(d: Decision): string {
  if (d.timing_window_score < 0.30 && d.market_cycle_alignment < 0.30)                      return "timing_miss";
  if (d.opportunity_decay_rate > 0.70 && d.timing_window_score < 0.40)                       return "window_collapse";
  if (d.execution_readiness_score < 0.30 && d.timing_window_score > 0.70)                    return "premature_action";
  if (d.decision_urgency_index > 0.70 && d.timing_window_score < 0.30)                       return "delayed_response";
  if (d.counter_timing_risk > 0.60 && d.timing_window_score > 0.50)                          return "timing_conflict";
  return "none";
}
function temporalRisk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function timingSeverity(c: number): string { if (c >= 60) return "missed"; if (c >= 40) return "closing"; if (c >= 20) return "watch"; return "optimal"; }
function recommendedAction(r: string, pat: string): string {
  if (r === "critical") {
    if (pat === "window_collapse") return "emergency_acceleration";
    return "strategic_pause";
  }
  if (r === "high") {
    if (pat === "timing_miss") return "timing_recalibration";
    return "window_capture";
  }
  if (r === "moderate") return "timing_monitoring";
  return "no_action";
}
function missedWindow(d: Decision, comp: number): boolean {
  return comp >= 60 || (d.timing_window_score < 0.25 && d.opportunity_decay_rate > 0.60);
}
function accelerationRequired(d: Decision, comp: number): boolean {
  return comp >= 40 && d.decision_urgency_index > 0.60;
}
function estimatedTimingLossIndex(d: Decision, comp: number): number {
  return Math.min(Math.round(comp / 100 * (d.opportunity_decay_rate + d.counter_timing_risk) / 2 * 10 * 100) / 100, 10.0);
}
function timingSignal(d: Decision, pat: string, comp: number): string {
  if (comp < 20) return "Fenêtre temporelle optimale — timing parfait, alignement marché, préparation maximale";
  const labels: Record<string, string> = {
    timing_miss:       "Fenêtre manquée",
    window_collapse:   "Effondrement fenêtre",
    premature_action:  "Action prématurée",
    delayed_response:  "Réponse tardive",
    timing_conflict:   "Conflit temporel",
  };
  const label = labels[pat] ?? pat.replace(/_/g, " ");
  return `${label} — fenêtre ${d.timing_window_score.toFixed(2)} — decay ${d.opportunity_decay_rate.toFixed(2)} — préparation ${d.execution_readiness_score.toFixed(2)} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const decisions = MOCK_DECISIONS.map(d => {
      const opp = opportunityScore(d), read = readinessScore(d), alig = alignmentScore(d), risk = riskScore(d);
      const comp = compositeScore(opp, read, alig, risk);
      const pat = timingPattern(d), r = temporalRisk(comp), sev = timingSeverity(comp), act = recommendedAction(r, pat);
      return {
        decision_id:                    d.decision_id,
        decision_type:                  d.decision_type,
        region:                         d.region,
        temporal_risk:                  r,
        timing_pattern:                 pat,
        timing_severity:                sev,
        recommended_action:             act,
        opportunity_score:              opp,
        readiness_score:                read,
        alignment_score:                alig,
        risk_score:                     risk,
        temporal_composite:             comp,
        missed_window:                  missedWindow(d, comp),
        acceleration_required:          accelerationRequired(d, comp),
        estimated_timing_loss_index:    estimatedTimingLossIndex(d, comp),
        timing_signal:                  timingSignal(d, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let topp=0, tread=0, talig=0, trisk=0, tcomp=0, tloss=0, mwC=0, arC=0;
    for (const dec of decisions) {
      rc[dec.temporal_risk]    = (rc[dec.temporal_risk]    || 0) + 1;
      pc[dec.timing_pattern]   = (pc[dec.timing_pattern]   || 0) + 1;
      sc[dec.timing_severity]  = (sc[dec.timing_severity]  || 0) + 1;
      ac[dec.recommended_action] = (ac[dec.recommended_action] || 0) + 1;
      topp  += dec.opportunity_score;
      tread += dec.readiness_score;
      talig += dec.alignment_score;
      trisk += dec.risk_score;
      tcomp += dec.temporal_composite;
      tloss += dec.estimated_timing_loss_index;
      if (dec.missed_window)         mwC++;
      if (dec.acceleration_required) arC++;
    }
    const n = decisions.length;
    return NextResponse.json(sealResponse({ decisions, summary: {
      total:                            n,
      risk_counts:                      rc,
      pattern_counts:                   pc,
      severity_counts:                  sc,
      action_counts:                    ac,
      avg_temporal_composite:           Math.round(tcomp / n * 10) / 10,
      missed_window_count:              mwC,
      acceleration_required_count:      arC,
      avg_opportunity_score:            Math.round(topp  / n * 10) / 10,
      avg_readiness_score:              Math.round(tread / n * 10) / 10,
      avg_alignment_score:              Math.round(talig / n * 10) / 10,
      avg_risk_score:                   Math.round(trisk / n * 10) / 10,
      avg_estimated_timing_loss_index:  Math.round(tloss / n * 100) / 100,
    } as Record<string, unknown>}, "temporal-intelligence-engine") as Parameters<typeof NextResponse.json>[0]);
  }
  return NextResponse.json(sealResponse(await (await fetch(`${process.env.SWARM_API_URL}/temporal-intelligence-engine`)).json(), "temporal-intelligence-engine") as Parameters<typeof NextResponse.json>[0]);
}
