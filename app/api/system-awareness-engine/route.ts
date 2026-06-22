import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// ── Mock entities ──────────────────────────────────────────────────────────────
// Module 316 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// 8 entities covering all system awareness patterns and risk levels.

const MOCK_ENTITIES = [
  // SAW-001 — EMEA, financial_system → critical, runaway_reinforcing_loop
  // reinforcing_loop_dominance≥0.70 AND balancing_loop_weakness≥0.65 → runaway_reinforcing_loop
  // composite≥75 → system_chaos severity, composite≥60 → critical
  {
    id: "SAW-001", system_category: "financial_system", region: "EMEA",
    reinforcing_loop_dominance: 0.85,  balancing_loop_weakness: 0.80,
    delay_accumulation_risk: 0.78,     stock_flow_misalignment: 0.70,
    emergence_unpredictability: 0.75,  systemic_leverage_blindness: 0.72,
    feedback_signal_noise_ratio: 0.15, archetype_trap_exposure: 0.68,
    policy_resistance_index: 0.72,     complexity_escalation_rate: 0.72,
    nonlinear_response_risk: 0.70,     tipping_point_proximity: 0.68,
    intervention_side_effect_risk: 0.65, systemic_inertia_index: 0.68,
    oscillation_instability: 0.75,     goal_seeking_drift: 0.60,
    system_boundary_permeability: 0.65,
  },
  // SAW-002 — APAC, small_enterprise → low, none
  // All low values → composite<20, no pattern triggered
  {
    id: "SAW-002", system_category: "small_enterprise", region: "APAC",
    reinforcing_loop_dominance: 0.08,  balancing_loop_weakness: 0.10,
    delay_accumulation_risk: 0.10,     stock_flow_misalignment: 0.08,
    emergence_unpredictability: 0.10,  systemic_leverage_blindness: 0.08,
    feedback_signal_noise_ratio: 0.88, archetype_trap_exposure: 0.08,
    policy_resistance_index: 0.10,     complexity_escalation_rate: 0.10,
    nonlinear_response_risk: 0.08,     tipping_point_proximity: 0.10,
    intervention_side_effect_risk: 0.10, systemic_inertia_index: 0.10,
    oscillation_instability: 0.08,     goal_seeking_drift: 0.08,
    system_boundary_permeability: 0.10,
  },
  // SAW-003 — NOAM, healthcare_system → high, delay_catastrophe
  // delay_accumulation_risk≥0.70 AND policy_resistance_index≥0.65 → delay_catastrophe
  // reinforcing_loop_dominance=0.50<0.70 → avoids runaway_reinforcing_loop
  // composite in [40,60) → high
  {
    id: "SAW-003", system_category: "healthcare_system", region: "NOAM",
    reinforcing_loop_dominance: 0.50,  balancing_loop_weakness: 0.48,
    delay_accumulation_risk: 0.78,     stock_flow_misalignment: 0.50,
    emergence_unpredictability: 0.45,  systemic_leverage_blindness: 0.38,
    feedback_signal_noise_ratio: 0.25, archetype_trap_exposure: 0.35,
    policy_resistance_index: 0.72,     complexity_escalation_rate: 0.48,
    nonlinear_response_risk: 0.42,     tipping_point_proximity: 0.40,
    intervention_side_effect_risk: 0.40, systemic_inertia_index: 0.45,
    oscillation_instability: 0.45,     goal_seeking_drift: 0.40,
    system_boundary_permeability: 0.42,
  },
  // SAW-004 — LATAM, local_economy → low, none
  // All low values → composite<20, no pattern triggered
  {
    id: "SAW-004", system_category: "local_economy", region: "LATAM",
    reinforcing_loop_dominance: 0.10,  balancing_loop_weakness: 0.12,
    delay_accumulation_risk: 0.12,     stock_flow_misalignment: 0.10,
    emergence_unpredictability: 0.12,  systemic_leverage_blindness: 0.10,
    feedback_signal_noise_ratio: 0.85, archetype_trap_exposure: 0.10,
    policy_resistance_index: 0.10,     complexity_escalation_rate: 0.12,
    nonlinear_response_risk: 0.10,     tipping_point_proximity: 0.10,
    intervention_side_effect_risk: 0.12, systemic_inertia_index: 0.10,
    oscillation_instability: 0.10,     goal_seeking_drift: 0.10,
    system_boundary_permeability: 0.12,
  },
  // SAW-005 — MEA, political_system → critical, tipping_point_cascade
  // tipping_point_proximity≥0.70 AND nonlinear_response_risk≥0.65 → tipping_point_cascade
  // reinforcing_loop_dominance=0.60<0.70 → avoids runaway_reinforcing_loop
  // delay_accumulation_risk=0.60<0.70 → avoids delay_catastrophe
  // composite≥60 → critical
  {
    id: "SAW-005", system_category: "political_system", region: "MEA",
    reinforcing_loop_dominance: 0.60,  balancing_loop_weakness: 0.55,
    delay_accumulation_risk: 0.60,     stock_flow_misalignment: 0.70,
    emergence_unpredictability: 0.80,  systemic_leverage_blindness: 0.60,
    feedback_signal_noise_ratio: 0.15, archetype_trap_exposure: 0.55,
    policy_resistance_index: 0.55,     complexity_escalation_rate: 0.72,
    nonlinear_response_risk: 0.78,     tipping_point_proximity: 0.82,
    intervention_side_effect_risk: 0.65, systemic_inertia_index: 0.68,
    oscillation_instability: 0.65,     goal_seeking_drift: 0.60,
    system_boundary_permeability: 0.65,
  },
  // SAW-006 — EMEA, corporate_org → moderate, none
  // All values below pattern thresholds → no pattern
  // composite in [20,40) → moderate
  {
    id: "SAW-006", system_category: "corporate_org", region: "EMEA",
    reinforcing_loop_dominance: 0.28,  balancing_loop_weakness: 0.25,
    delay_accumulation_risk: 0.28,     stock_flow_misalignment: 0.28,
    emergence_unpredictability: 0.28,  systemic_leverage_blindness: 0.22,
    feedback_signal_noise_ratio: 0.65, archetype_trap_exposure: 0.20,
    policy_resistance_index: 0.25,     complexity_escalation_rate: 0.25,
    nonlinear_response_risk: 0.22,     tipping_point_proximity: 0.25,
    intervention_side_effect_risk: 0.25, systemic_inertia_index: 0.28,
    oscillation_instability: 0.22,     goal_seeking_drift: 0.22,
    system_boundary_permeability: 0.28,
  },
  // SAW-007 — APAC, supply_network → high, archetype_trap
  // archetype_trap_exposure≥0.70 AND systemic_leverage_blindness≥0.65 → archetype_trap
  // reinforcing_loop_dominance=0.50<0.70 → avoids runaway_reinforcing_loop
  // delay_accumulation_risk=0.55<0.70 → avoids delay_catastrophe
  // tipping_point_proximity=0.40<0.70 → avoids tipping_point_cascade
  // composite in [40,60) → high
  {
    id: "SAW-007", system_category: "supply_network", region: "APAC",
    reinforcing_loop_dominance: 0.50,  balancing_loop_weakness: 0.48,
    delay_accumulation_risk: 0.55,     stock_flow_misalignment: 0.48,
    emergence_unpredictability: 0.48,  systemic_leverage_blindness: 0.75,
    feedback_signal_noise_ratio: 0.40, archetype_trap_exposure: 0.78,
    policy_resistance_index: 0.50,     complexity_escalation_rate: 0.50,
    nonlinear_response_risk: 0.45,     tipping_point_proximity: 0.40,
    intervention_side_effect_risk: 0.55, systemic_inertia_index: 0.45,
    oscillation_instability: 0.45,     goal_seeking_drift: 0.42,
    system_boundary_permeability: 0.48,
  },
  // SAW-008 — NOAM, social_system → critical, oscillation_death_spiral
  // oscillation_instability≥0.70 AND goal_seeking_drift≥0.65 → oscillation_death_spiral
  // reinforcing_loop_dominance=0.55<0.70 → avoids runaway_reinforcing_loop
  // delay_accumulation_risk=0.55<0.70 → avoids delay_catastrophe
  // tipping_point_proximity=0.55<0.70 → avoids tipping_point_cascade
  // archetype_trap_exposure=0.55<0.70 → avoids archetype_trap
  // composite≥60 → critical
  {
    id: "SAW-008", system_category: "social_system", region: "NOAM",
    reinforcing_loop_dominance: 0.55,  balancing_loop_weakness: 0.50,
    delay_accumulation_risk: 0.55,     stock_flow_misalignment: 0.65,
    emergence_unpredictability: 0.70,  systemic_leverage_blindness: 0.55,
    feedback_signal_noise_ratio: 0.15, archetype_trap_exposure: 0.55,
    policy_resistance_index: 0.50,     complexity_escalation_rate: 0.68,
    nonlinear_response_risk: 0.55,     tipping_point_proximity: 0.55,
    intervention_side_effect_risk: 0.65, systemic_inertia_index: 0.62,
    oscillation_instability: 0.85,     goal_seeking_drift: 0.78,
    system_boundary_permeability: 0.60,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

// ── Scoring functions (mirrors Python engine exactly) ──────────────────────────

function loopScore(e: Entity): number {
  return Math.round(
    (e.reinforcing_loop_dominance * 0.4
      + e.balancing_loop_weakness * 0.35
      + e.oscillation_instability * 0.25) * 100 * 100) / 100;
}

function delayScore(e: Entity): number {
  return Math.round(
    (e.delay_accumulation_risk * 0.4
      + (1 - e.feedback_signal_noise_ratio) * 0.35
      + e.policy_resistance_index * 0.25) * 100 * 100) / 100;
}

function emergenceScore(e: Entity): number {
  return Math.round(
    (e.emergence_unpredictability * 0.4
      + e.nonlinear_response_risk * 0.35
      + e.tipping_point_proximity * 0.25) * 100 * 100) / 100;
}

function blindspotScore(e: Entity): number {
  return Math.round(
    (e.systemic_leverage_blindness * 0.4
      + e.archetype_trap_exposure * 0.35
      + e.intervention_side_effect_risk * 0.25) * 100 * 100) / 100;
}

function awarenessComposite(loop: number, delay: number, emergence: number, blindspot: number): number {
  return Math.round((loop * 0.30 + delay * 0.25 + emergence * 0.25 + blindspot * 0.20) * 100) / 100;
}

function awarenessRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function awarenessPattern(e: Entity): string {
  if (e.reinforcing_loop_dominance >= 0.70 && e.balancing_loop_weakness >= 0.65)
    return "runaway_reinforcing_loop";
  if (e.delay_accumulation_risk >= 0.70 && e.policy_resistance_index >= 0.65)
    return "delay_catastrophe";
  if (e.tipping_point_proximity >= 0.70 && e.nonlinear_response_risk >= 0.65)
    return "tipping_point_cascade";
  if (e.archetype_trap_exposure >= 0.70 && e.systemic_leverage_blindness >= 0.65)
    return "archetype_trap";
  if (e.oscillation_instability >= 0.70 && e.goal_seeking_drift >= 0.65)
    return "oscillation_death_spiral";
  return "none";
}

function awarenessSeverity(comp: number): string {
  if (comp >= 75) return "system_chaos";
  if (comp >= 50) return "high_systemic_risk";
  if (comp >= 25) return "systemic_instability";
  return "system_balanced";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "systemic_emergency_redesign";
  if (risk === "high") {
    if (pattern === "runaway_reinforcing_loop") return "loop_dampening";
    return "leverage_point_intervention";
  }
  if (risk === "moderate") return "system_monitoring";
  return "no_action";
}

function systemSignal(e: Entity, pattern: string, comp: number): string {
  if (comp < 20) {
    return "Système équilibré — boucles de rétroaction stables, dynamiques de délai maîtrisées, aucun comportement émergent critique détecté";
  }
  if (comp >= 60) {
    const critLabels: Record<string, string> = {
      runaway_reinforcing_loop: "Boucle de renforcement incontrôlée",
      delay_catastrophe:        "Catastrophe par accumulation de délais",
      tipping_point_cascade:    "Cascade vers point de basculement",
      archetype_trap:           "Piège d'archétype systémique",
      oscillation_death_spiral: "Spirale d'oscillation fatale",
      none:                     "Défaillance systémique composite",
    };
    const label = critLabels[pattern] ?? pattern.replace(/_/g, " ");
    return `Crise systémique critique — ${label} — boucles renforçantes ${e.reinforcing_loop_dominance.toFixed(2)} — proximité basculement ${e.tipping_point_proximity.toFixed(2)} — composite ${Math.round(comp)}`;
  }
  if (comp >= 40) {
    const highLabels: Record<string, string> = {
      runaway_reinforcing_loop: "Boucle de renforcement en fuite",
      delay_catastrophe:        "Accumulation critique de délais",
      tipping_point_cascade:    "Risque de basculement non-linéaire",
      archetype_trap:           "Exposition aux archétypes pathologiques",
      oscillation_death_spiral: "Instabilité oscillatoire croissante",
      none:                     "Déséquilibre systémique",
    };
    const label = highLabels[pattern] ?? pattern.replace(/_/g, " ");
    return `Risque systémique élevé — ${label} — résistance politique ${e.policy_resistance_index.toFixed(2)} — imprévisibilité émergente ${e.emergence_unpredictability.toFixed(2)} — composite ${Math.round(comp)}`;
  }
  return `Instabilité systémique modérée — tensions observées — inertie systémique ${e.systemic_inertia_index.toFixed(2)} — perméabilité frontières ${e.system_boundary_permeability.toFixed(2)} — composite ${Math.round(comp)}`;
}

// ── GET handler ────────────────────────────────────────────────────────────────

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[system-awareness-engine] SWARM_API_URL non défini — mode dégradé activé");
}, "system-awareness-engine") as Record<string, unknown>,
      { status: 502 }
    );
  }

  try {
    const entities = MOCK_ENTITIES.map(e => {
      const loop      = loopScore(e);
      const delay     = delayScore(e);
      const emergence = emergenceScore(e);
      const blindspot = blindspotScore(e);
      const comp      = awarenessComposite(loop, delay, emergence, blindspot);
      const risk      = awarenessRisk(comp);
      const pat       = awarenessPattern(e);
      const sev       = awarenessSeverity(comp);
      const act       = recommendedAction(risk, pat);
      const sig       = systemSignal(e, pat, comp);

      return {
        id:                      e.entity_id,
        region:                         e.region,
        system_category:                e.system_category,
        awareness_risk:                 risk,
        awareness_pattern:              pat,
        awareness_severity:             sev,
        recommended_action:             act,
        loop_score:                     loop,
        delay_score:                    delay,
        emergence_score:                emergence,
        blindspot_score:                blindspot,
        awareness_composite:            comp,
        is_system_crisis:               comp >= 60,
        requires_system_intervention:   comp >= 40,
        system_signal:                  sig,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tLoop = 0, tDelay = 0, tEmergence = 0, tBlindspot = 0, tComp = 0;
    let crisisC = 0, interventionC = 0;

    for (const ent of entities) {
      rc[ent.awareness_risk]      = (rc[ent.awareness_risk]      || 0) + 1;
      pc[ent.awareness_pattern]   = (pc[ent.awareness_pattern]   || 0) + 1;
      sc[ent.awareness_severity]  = (sc[ent.awareness_severity]  || 0) + 1;
      ac[ent.recommended_action]  = (ac[ent.recommended_action]  || 0) + 1;
      tLoop      += ent.loop_score;
      tDelay     += ent.delay_score;
      tEmergence += ent.emergence_score;
      tBlindspot += ent.blindspot_score;
      tComp      += ent.awareness_composite;
      if (ent.is_system_crisis)             crisisC++;
      if (ent.requires_system_intervention) interventionC++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 100) / 100;

    const summary = {
      total_entities_analyzed:         n,
      critical_count:                  rc["critical"]  || 0,
      high_count:                      rc["high"]      || 0,
      moderate_count:                  rc["moderate"]  || 0,
      low_count:                       rc["low"]       || 0,
      crisis_count:                    crisisC,
      intervention_required_count:     interventionC,
      avg_loop_score:                  Math.round(tLoop      / n * 100) / 100,
      avg_delay_score:                 Math.round(tDelay     / n * 100) / 100,
      avg_emergence_score:             Math.round(tEmergence / n * 100) / 100,
      avg_blindspot_score:             Math.round(tBlindspot / n * 100) / 100,
      avg_awareness_composite:         avgComp,
      avg_estimated_system_risk_index: Math.round(avgComp / 100 * 10 * 100) / 100,
      risk_counts:                     rc,
      pattern_counts:                  pc,
      severity_counts:                 sc,
      action_counts:                   ac,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary }, "system-awareness-engine") as Record<string, unknown>
    ));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Erreur moteur conscience systémique" }, "system-awareness-engine") as Record<string, unknown>,
      { status: 502 }
    ));
  }
}
