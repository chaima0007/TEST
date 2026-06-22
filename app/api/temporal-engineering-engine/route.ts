import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_HORIZONS = [
  // TE-001: macro_structural, EMEA → critical, timeline_bifurcation
  {
    horizon_id: "TE-001", temporal_domain: "macro_structural", region: "EMEA",
    timeline_divergence_risk: 0.88, chronological_coherence_score: 0.22, anticipation_horizon_depth: 0.30,
    temporal_blind_spot_ratio: 0.55, multi_scale_synchronization: 0.28, intervention_window_precision: 0.32,
    causal_loop_detection_score: 0.45, future_optionality_score: 0.38, temporal_leverage_index: 0.25,
    chronological_risk_concentration: 0.72, scenario_branching_factor: 0.80, retroactive_impact_sensitivity: 0.58,
    temporal_resilience_score: 0.20, clock_speed_mismatch_risk: 0.60, anticipation_accuracy_score: 0.30,
    decision_timing_optimality: 0.28, temporal_arbitrage_potential: 0.35,
  },
  // TE-002: meso_strategic, NAMER → low, temporally_mastered
  {
    horizon_id: "TE-002", temporal_domain: "meso_strategic", region: "NAMER",
    timeline_divergence_risk: 0.08, chronological_coherence_score: 0.92, anticipation_horizon_depth: 0.88,
    temporal_blind_spot_ratio: 0.10, multi_scale_synchronization: 0.90, intervention_window_precision: 0.92,
    causal_loop_detection_score: 0.12, future_optionality_score: 0.88, temporal_leverage_index: 0.85,
    chronological_risk_concentration: 0.08, scenario_branching_factor: 0.10, retroactive_impact_sensitivity: 0.12,
    temporal_resilience_score: 0.92, clock_speed_mismatch_risk: 0.08, anticipation_accuracy_score: 0.90,
    decision_timing_optimality: 0.92, temporal_arbitrage_potential: 0.88,
  },
  // TE-003: meta_civilizational, APAC → high, temporal_blind_spot
  {
    horizon_id: "TE-003", temporal_domain: "meta_civilizational", region: "APAC",
    timeline_divergence_risk: 0.42, chronological_coherence_score: 0.48, anticipation_horizon_depth: 0.55,
    temporal_blind_spot_ratio: 0.72, multi_scale_synchronization: 0.50, intervention_window_precision: 0.45,
    causal_loop_detection_score: 0.38, future_optionality_score: 0.52, temporal_leverage_index: 0.48,
    chronological_risk_concentration: 0.50, scenario_branching_factor: 0.42, retroactive_impact_sensitivity: 0.48,
    temporal_resilience_score: 0.45, clock_speed_mismatch_risk: 0.50, anticipation_accuracy_score: 0.28,
    decision_timing_optimality: 0.40, temporal_arbitrage_potential: 0.50,
  },
  // TE-004: micro_tactical, LATAM → low, anticipating
  {
    horizon_id: "TE-004", temporal_domain: "micro_tactical", region: "LATAM",
    timeline_divergence_risk: 0.15, chronological_coherence_score: 0.80, anticipation_horizon_depth: 0.78,
    temporal_blind_spot_ratio: 0.18, multi_scale_synchronization: 0.78, intervention_window_precision: 0.82,
    causal_loop_detection_score: 0.20, future_optionality_score: 0.75, temporal_leverage_index: 0.72,
    chronological_risk_concentration: 0.15, scenario_branching_factor: 0.18, retroactive_impact_sensitivity: 0.22,
    temporal_resilience_score: 0.80, clock_speed_mismatch_risk: 0.15, anticipation_accuracy_score: 0.78,
    decision_timing_optimality: 0.80, temporal_arbitrage_potential: 0.75,
  },
  // TE-005: quantum_temporal, EMEA → critical, causal_loop_trap
  {
    horizon_id: "TE-005", temporal_domain: "quantum_temporal", region: "EMEA",
    timeline_divergence_risk: 0.75, chronological_coherence_score: 0.18, anticipation_horizon_depth: 0.22,
    temporal_blind_spot_ratio: 0.60, multi_scale_synchronization: 0.20, intervention_window_precision: 0.18,
    causal_loop_detection_score: 0.85, future_optionality_score: 0.20, temporal_leverage_index: 0.15,
    chronological_risk_concentration: 0.78, scenario_branching_factor: 0.70, retroactive_impact_sensitivity: 0.80,
    temporal_resilience_score: 0.12, clock_speed_mismatch_risk: 0.75, anticipation_accuracy_score: 0.18,
    decision_timing_optimality: 0.15, temporal_arbitrage_potential: 0.22,
  },
  // TE-006: cyclical_historical, NAMER → moderate, none
  {
    horizon_id: "TE-006", temporal_domain: "cyclical_historical", region: "NAMER",
    timeline_divergence_risk: 0.30, chronological_coherence_score: 0.65, anticipation_horizon_depth: 0.60,
    temporal_blind_spot_ratio: 0.32, multi_scale_synchronization: 0.62, intervention_window_precision: 0.65,
    causal_loop_detection_score: 0.28, future_optionality_score: 0.60, temporal_leverage_index: 0.58,
    chronological_risk_concentration: 0.32, scenario_branching_factor: 0.30, retroactive_impact_sensitivity: 0.35,
    temporal_resilience_score: 0.62, clock_speed_mismatch_risk: 0.35, anticipation_accuracy_score: 0.62,
    decision_timing_optimality: 0.65, temporal_arbitrage_potential: 0.58,
  },
  // TE-007: emergent_futures, APAC → high, chronological_desync
  {
    horizon_id: "TE-007", temporal_domain: "emergent_futures", region: "APAC",
    timeline_divergence_risk: 0.48, chronological_coherence_score: 0.35, anticipation_horizon_depth: 0.45,
    temporal_blind_spot_ratio: 0.45, multi_scale_synchronization: 0.28, intervention_window_precision: 0.42,
    causal_loop_detection_score: 0.40, future_optionality_score: 0.55, temporal_leverage_index: 0.40,
    chronological_risk_concentration: 0.52, scenario_branching_factor: 0.48, retroactive_impact_sensitivity: 0.50,
    temporal_resilience_score: 0.38, clock_speed_mismatch_risk: 0.72, anticipation_accuracy_score: 0.42,
    decision_timing_optimality: 0.38, temporal_arbitrage_potential: 0.45,
  },
  // TE-008: retroactive_causality, MEA → critical, future_optionality_collapse
  {
    horizon_id: "TE-008", temporal_domain: "retroactive_causality", region: "MEA",
    timeline_divergence_risk: 0.80, chronological_coherence_score: 0.15, anticipation_horizon_depth: 0.18,
    temporal_blind_spot_ratio: 0.65, multi_scale_synchronization: 0.15, intervention_window_precision: 0.12,
    causal_loop_detection_score: 0.55, future_optionality_score: 0.15, temporal_leverage_index: 0.12,
    chronological_risk_concentration: 0.80, scenario_branching_factor: 0.18, retroactive_impact_sensitivity: 0.85,
    temporal_resilience_score: 0.10, clock_speed_mismatch_risk: 0.78, anticipation_accuracy_score: 0.15,
    decision_timing_optimality: 0.12, temporal_arbitrage_potential: 0.18,
  },
];

type Horizon = typeof MOCK_HORIZONS[0];

function divergenceScore(h: Horizon): number {
  return Math.min(1.0, Math.max(0.0,
    h.timeline_divergence_risk * 0.40
    + h.scenario_branching_factor * 0.35
    + h.chronological_risk_concentration * 0.25
  ));
}
function anticipationScore(h: Horizon): number {
  return Math.min(1.0, Math.max(0.0,
    h.temporal_blind_spot_ratio * 0.40
    + (1.0 - h.anticipation_accuracy_score) * 0.35
    + (1.0 - h.intervention_window_precision) * 0.25
  ));
}
function synchronizationScore(h: Horizon): number {
  return Math.min(1.0, Math.max(0.0,
    h.clock_speed_mismatch_risk * 0.40
    + (1.0 - h.multi_scale_synchronization) * 0.35
    + (1.0 - h.chronological_coherence_score) * 0.25
  ));
}
function resilienceScore(h: Horizon): number {
  return Math.min(1.0, Math.max(0.0,
    (1.0 - h.temporal_resilience_score) * 0.40
    + h.retroactive_impact_sensitivity * 0.35
    + h.causal_loop_detection_score * 0.25
  ));
}
function composite(div: number, ant: number, syn: number, res: number): number {
  return Math.min(Math.round((div * 0.30 + ant * 0.25 + syn * 0.25 + res * 0.20) * 100 * 100) / 100, 100);
}
function temporalPattern(h: Horizon): string {
  if (h.timeline_divergence_risk >= 0.70 && h.scenario_branching_factor >= 0.65) return "timeline_bifurcation";
  if (h.temporal_blind_spot_ratio >= 0.65 && h.anticipation_accuracy_score <= 0.35) return "temporal_blind_spot";
  if (h.clock_speed_mismatch_risk >= 0.65 && h.multi_scale_synchronization <= 0.40) return "chronological_desync";
  if (h.causal_loop_detection_score >= 0.70) return "causal_loop_trap";
  if (h.future_optionality_score <= 0.25 && h.scenario_branching_factor <= 0.25) return "future_optionality_collapse";
  return "none";
}
function risk(comp: number): string { if (comp >= 60) return "critical"; if (comp >= 40) return "high"; if (comp >= 20) return "moderate"; return "low"; }
function severity(comp: number): string { if (comp >= 60) return "temporally_lost"; if (comp >= 40) return "desynchronized"; if (comp >= 20) return "anticipating"; return "temporally_mastered"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (["timeline_bifurcation","causal_loop_trap","future_optionality_collapse"].includes(p)) return "temporal_emergency_realignment";
    return "timeline_convergence_protocol";
  }
  if (r === "high") {
    if (p === "chronological_desync") return "chronological_resync";
    return "anticipation_upgrade";
  }
  if (r === "moderate") return "temporal_monitoring";
  return "no_action";
}
function signal(h: Horizon, pat: string, comp: number): string {
  const cohPct = Math.round(h.chronological_coherence_score * 100);
  const winPct = Math.round(h.intervention_window_precision * 100);
  const arb    = h.temporal_arbitrage_potential.toFixed(2);
  if (comp < 20) {
    return `Maîtrise temporelle multi-chronologique — cohérence ${cohPct}% — fenêtre intervention ${winPct}% — arbitrage temporel ${arb}`;
  }
  const labels: Record<string,string> = {
    timeline_bifurcation: "Bifurcation temporelle détectée",
    temporal_blind_spot:  "Zone aveugle temporelle critique",
    chronological_desync: "Désynchronisation chronologique active",
    causal_loop_trap:     "Piège boucle causale identifiée",
    future_optionality_collapse: "Effondrement optionnalité future",
    none: "Anomalie temporelle diffuse",
  };
  const label    = labels[pat] ?? pat.replace(/_/g," ");
  const divPct   = Math.round(h.timeline_divergence_risk * 100);
  const blindPct = Math.round(h.temporal_blind_spot_ratio * 100);
  return `${label} — divergence timeline ${divPct}% — zone aveugle ${blindPct}% — cohérence ${cohPct}% — fenêtre intervention ${winPct}% — arbitrage temporel ${arb} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[temporal-engineering-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tDiv=0,tAnt=0,tSyn=0,tRes=0,tComp=0,tIdx=0,bifC=0,realC=0;
    for (const hz of horizons) {
      rc[hz.temporal_risk]=(rc[hz.temporal_risk]||0)+1;
      pc[hz.temporal_pattern]=(pc[hz.temporal_pattern]||0)+1;
      sc[hz.temporal_severity]=(sc[hz.temporal_severity]||0)+1;
      ac[hz.recommended_action]=(ac[hz.recommended_action]||0)+1;
      tDiv+=hz.divergence_score; tAnt+=hz.anticipation_score; tSyn+=hz.synchronization_score; tRes+=hz.resilience_score;
      tComp+=hz.temporal_composite; tIdx+=hz.estimated_temporal_risk_index;
      if (hz.has_bifurcation_signal) bifC++;
      if (hz.requires_realignment) realC++;
    }
    const n = horizons.length;
    const summary = {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_temporal_composite: Math.round(tComp/n*10)/10,
      bifurcation_signal_count: bifC, realignment_required_count: realC,
      avg_divergence_score:      Math.round(tDiv/n*10)/10,
      avg_anticipation_score:    Math.round(tAnt/n*10)/10,
      avg_synchronization_score: Math.round(tSyn/n*10)/10,
      avg_resilience_score:      Math.round(tRes/n*10)/10,
      avg_estimated_temporal_risk_index: Math.round(tIdx/n*100)/100,
    };

    return sealResponse(NextResponse.json(sealResponse({ horizons, summary }, "temporal-engineering-engine")));
  }
  return sealResponse(NextResponse.json(sealResponse(
    await (await fetch(`${process.env.SWARM_API_URL}/temporal-engineering-engine`, { next: { revalidate: 30 } })).json(),
    "temporal-engineering-engine"
  )));
}
