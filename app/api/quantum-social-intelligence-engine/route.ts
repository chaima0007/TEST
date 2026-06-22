import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // QSI-001 hive_mind EMEA — critical herd_collapse
  { id:"QSI-001", collective_type:"hive_mind",          region:"EMEA",  collective_coherence_score:0.15, information_cascade_velocity:0.82, social_proof_amplification:0.78, tribal_polarization_risk:0.45, herd_behavior_intensity:0.90, contrarian_signal_strength:0.08, network_centrality_concentration:0.72, emotional_contagion_rate:0.85, collective_intelligence_efficiency:0.18, echo_chamber_density:0.55, behavioral_synchrony_index:0.20, wisdom_crowd_accuracy:0.22, social_resilience_score:0.12, influence_diversity_index:0.15, opinion_volatility:0.60, coordination_failure_risk:0.80, emergence_pattern_clarity:0.88 },
  // QSI-002 crowd_wisdom NAMER — low harmonious
  { id:"QSI-002", collective_type:"crowd_wisdom",       region:"NAMER", collective_coherence_score:0.90, information_cascade_velocity:0.15, social_proof_amplification:0.20, tribal_polarization_risk:0.10, herd_behavior_intensity:0.18, contrarian_signal_strength:0.80, network_centrality_concentration:0.22, emotional_contagion_rate:0.12, collective_intelligence_efficiency:0.92, echo_chamber_density:0.08, behavioral_synchrony_index:0.88, wisdom_crowd_accuracy:0.92, social_resilience_score:0.90, influence_diversity_index:0.88, opinion_volatility:0.10, coordination_failure_risk:0.08, emergence_pattern_clarity:0.12 },
  // QSI-003 social_contagion APAC — high echo_cascade
  { id:"QSI-003", collective_type:"social_contagion",   region:"APAC",  collective_coherence_score:0.42, information_cascade_velocity:0.72, social_proof_amplification:0.68, tribal_polarization_risk:0.52, herd_behavior_intensity:0.55, contrarian_signal_strength:0.28, network_centrality_concentration:0.58, emotional_contagion_rate:0.75, collective_intelligence_efficiency:0.38, echo_chamber_density:0.80, behavioral_synchrony_index:0.45, wisdom_crowd_accuracy:0.40, social_resilience_score:0.35, influence_diversity_index:0.30, opinion_volatility:0.62, coordination_failure_risk:0.48, emergence_pattern_clarity:0.70 },
  // QSI-004 emergent_consensus LATAM — low emerging
  { id:"QSI-004", collective_type:"emergent_consensus", region:"LATAM", collective_coherence_score:0.72, information_cascade_velocity:0.28, social_proof_amplification:0.32, tribal_polarization_risk:0.22, herd_behavior_intensity:0.25, contrarian_signal_strength:0.65, network_centrality_concentration:0.30, emotional_contagion_rate:0.20, collective_intelligence_efficiency:0.75, echo_chamber_density:0.20, behavioral_synchrony_index:0.70, wisdom_crowd_accuracy:0.78, social_resilience_score:0.80, influence_diversity_index:0.72, opinion_volatility:0.18, coordination_failure_risk:0.15, emergence_pattern_clarity:0.35 },
  // QSI-005 tribal_dynamics EMEA — critical tribal_fragmentation
  { id:"QSI-005", collective_type:"tribal_dynamics",    region:"EMEA",  collective_coherence_score:0.18, information_cascade_velocity:0.55, social_proof_amplification:0.50, tribal_polarization_risk:0.88, herd_behavior_intensity:0.42, contrarian_signal_strength:0.15, network_centrality_concentration:0.48, emotional_contagion_rate:0.72, collective_intelligence_efficiency:0.20, echo_chamber_density:0.60, behavioral_synchrony_index:0.22, wisdom_crowd_accuracy:0.25, social_resilience_score:0.15, influence_diversity_index:0.12, opinion_volatility:0.85, coordination_failure_risk:0.75, emergence_pattern_clarity:0.82 },
  // QSI-006 market_psychology NAMER — moderate none
  { id:"QSI-006", collective_type:"market_psychology",  region:"NAMER", collective_coherence_score:0.58, information_cascade_velocity:0.40, social_proof_amplification:0.45, tribal_polarization_risk:0.38, herd_behavior_intensity:0.42, contrarian_signal_strength:0.50, network_centrality_concentration:0.40, emotional_contagion_rate:0.38, collective_intelligence_efficiency:0.55, echo_chamber_density:0.35, behavioral_synchrony_index:0.55, wisdom_crowd_accuracy:0.58, social_resilience_score:0.55, influence_diversity_index:0.52, opinion_volatility:0.38, coordination_failure_risk:0.35, emergence_pattern_clarity:0.42 },
  // QSI-007 network_cascade APAC — high wisdom_failure
  { id:"QSI-007", collective_type:"network_cascade",    region:"APAC",  collective_coherence_score:0.35, information_cascade_velocity:0.65, social_proof_amplification:0.58, tribal_polarization_risk:0.55, herd_behavior_intensity:0.50, contrarian_signal_strength:0.22, network_centrality_concentration:0.62, emotional_contagion_rate:0.60, collective_intelligence_efficiency:0.22, echo_chamber_density:0.48, behavioral_synchrony_index:0.38, wisdom_crowd_accuracy:0.18, social_resilience_score:0.30, influence_diversity_index:0.28, opinion_volatility:0.58, coordination_failure_risk:0.55, emergence_pattern_clarity:0.65 },
  // QSI-008 viral_tipping MEA — critical mass_coordination
  { id:"QSI-008", collective_type:"viral_tipping",      region:"MEA",   collective_coherence_score:0.25, information_cascade_velocity:0.88, social_proof_amplification:0.85, tribal_polarization_risk:0.52, herd_behavior_intensity:0.78, contrarian_signal_strength:0.12, network_centrality_concentration:0.92, emotional_contagion_rate:0.80, collective_intelligence_efficiency:0.28, echo_chamber_density:0.58, behavioral_synchrony_index:0.85, wisdom_crowd_accuracy:0.30, social_resilience_score:0.18, influence_diversity_index:0.15, opinion_volatility:0.65, coordination_failure_risk:0.72, emergence_pattern_clarity:0.90 },
];

type Entity = typeof MOCK_ENTITIES[0];

function coherenceScore(e: Entity): number {
  const raw =
    (1 - e.collective_coherence_score)   * 40 +
    (1 - e.behavioral_synchrony_index)   * 35 +
    e.coordination_failure_risk          * 25;
  return Math.min(Math.round(raw * 10) / 10, 100);
}
function contagionScore(e: Entity): number {
  const raw =
    e.emotional_contagion_rate           * 40 +
    e.information_cascade_velocity       * 35 +
    e.social_proof_amplification         * 25;
  return Math.min(Math.round(raw * 100 * 10) / 10, 100);
}
function polarizationScore(e: Entity): number {
  const raw =
    e.tribal_polarization_risk           * 40 +
    e.echo_chamber_density               * 35 +
    e.opinion_volatility                 * 25;
  return Math.min(Math.round(raw * 100 * 10) / 10, 100);
}
function resilienceScore(e: Entity): number {
  const raw =
    (1 - e.social_resilience_score)      * 40 +
    (1 - e.wisdom_crowd_accuracy)        * 35 +
    (1 - e.influence_diversity_index)    * 25;
  return Math.min(Math.round(raw * 100 * 10) / 10, 100);
}
function composite(coh: number, con: number, pol: number, res: number): number {
  return Math.min(Math.round((coh * 0.30 + con * 0.25 + pol * 0.25 + res * 0.20) * 100) / 100, 100);
}
function emergencePattern(e: Entity): string {
  if (e.herd_behavior_intensity >= 0.70 && e.contrarian_signal_strength <= 0.30) return "herd_collapse";
  if (e.echo_chamber_density >= 0.65 && e.information_cascade_velocity >= 0.60)  return "echo_cascade";
  if (e.tribal_polarization_risk >= 0.65 && e.opinion_volatility >= 0.55)        return "tribal_fragmentation";
  if (e.wisdom_crowd_accuracy <= 0.35 && e.collective_intelligence_efficiency <= 0.40) return "wisdom_failure";
  if (e.network_centrality_concentration >= 0.70 && e.behavioral_synchrony_index >= 0.65) return "mass_coordination";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "chaotic"; if (c >= 40) return "volatile"; if (c >= 20) return "emerging"; return "harmonious"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "herd_collapse" || p === "mass_coordination") return "collective_reset";
    return "cascade_containment";
  }
  if (r === "high") {
    if (p === "echo_cascade" || p === "tribal_fragmentation") return "behavioral_intervention";
    return "diversity_injection";
  }
  if (r === "moderate") return "social_monitoring";
  return "no_action";
}
function signal(e: Entity, pat: string, comp: number): string {
  if (comp < 20) return "Intelligence collective forte — cohésion sociale optimale, sagesse de la foule active, résilience élevée";
  const labels: Record<string,string> = {
    herd_collapse:        "Effondrement comportement grégaire",
    echo_cascade:         "Cascade chambre d'écho",
    tribal_fragmentation: "Fragmentation tribale",
    wisdom_failure:       "Échec sagesse collective",
    mass_coordination:    "Coordination de masse",
    none:                 "Dynamique sociale stable",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — contagion émotionnelle ${e.emotional_contagion_rate.toFixed(2)} — polarisation tribale ${e.tribal_polarization_risk.toFixed(2)} — résilience sociale ${e.social_resilience_score.toFixed(2)} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[quantum-social-intelligence-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tcoh=0, tcon=0, tpol=0, tres=0, tcomp=0, tidx=0, cascC=0, intervC=0;
    for (const ent of entities) {
      rc[ent.social_risk]=(rc[ent.social_risk]||0)+1;
      pc[ent.emergence_pattern]=(pc[ent.emergence_pattern]||0)+1;
      sc[ent.collective_severity]=(sc[ent.collective_severity]||0)+1;
      ac[ent.recommended_action]=(ac[ent.recommended_action]||0)+1;
      tcoh+=ent.coherence_score; tcon+=ent.contagion_score; tpol+=ent.polarization_score; tres+=ent.resilience_score;
      tcomp+=ent.social_composite; tidx+=ent.estimated_collective_risk_index;
      if (ent.has_cascade_signal) cascC++;
      if (ent.requires_collective_intervention) intervC++;
    }
    const n = entities.length;
    return sealResponse(NextResponse.json(sealResponse({ entities, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_social_composite: Math.round(tcomp/n*10)/10,
      cascade_signal_count: cascC, collective_intervention_count: intervC,
      avg_coherence_score: Math.round(tcoh/n*10)/10,
      avg_contagion_score: Math.round(tcon/n*10)/10,
      avg_polarization_score: Math.round(tpol/n*10)/10,
      avg_resilience_score: Math.round(tres/n*10)/10,
      avg_estimated_collective_risk_index: Math.round(tidx/n*100)/100,
    }} as Record<string,unknown>)));
  }
  return sealResponse(NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/quantum-social-intelligence-engine`, { next: { revalidate: 30 } })).json()));
}
