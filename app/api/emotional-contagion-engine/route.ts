import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // EC-001: EMEA, financial_panic → critical, panic_epidemic
  // panic_epidemic: contagion_velocity≥0.70, fear_cascade_intensity≥0.65
  // critical: composite≥60
  {
    entity_id: "EC-001", contagion_type: "financial_panic", region: "EMEA",
    contagion_velocity: 0.88, population_susceptibility: 0.80, emotional_amplification_rate: 0.82,
    social_network_density: 0.78, fear_cascade_intensity: 0.85, euphoria_bubble_risk: 0.20,
    rage_contagion_potential: 0.55, anxiety_baseline: 0.72, collective_resilience: 0.18,
    emotional_immune_response: 0.20, media_amplification_effect: 0.85, influencer_contagion_leverage: 0.75,
    institutional_trust_buffer: 0.22, cross_border_contagion: 0.80, recovery_velocity: 0.18,
    emotional_polarization_index: 0.60, contagion_mutation_rate: 0.55,
  },
  // EC-002: APAC, consumer_sentiment → low, emotional_equilibrium/none
  // low: composite<20; none pattern
  {
    entity_id: "EC-002", contagion_type: "consumer_sentiment", region: "APAC",
    contagion_velocity: 0.12, population_susceptibility: 0.15, emotional_amplification_rate: 0.14,
    social_network_density: 0.18, fear_cascade_intensity: 0.10, euphoria_bubble_risk: 0.12,
    rage_contagion_potential: 0.10, anxiety_baseline: 0.12, collective_resilience: 0.88,
    emotional_immune_response: 0.90, media_amplification_effect: 0.12, influencer_contagion_leverage: 0.10,
    institutional_trust_buffer: 0.90, cross_border_contagion: 0.10, recovery_velocity: 0.90,
    emotional_polarization_index: 0.10, contagion_mutation_rate: 0.08,
  },
  // EC-003: NOAM, social_media_rage → high, rage_wildfire
  // rage_wildfire: rage_contagion_potential≥0.70, social_network_density≥0.65
  // high: 40≤composite<60
  {
    entity_id: "EC-003", contagion_type: "social_media_rage", region: "NOAM",
    contagion_velocity: 0.55, population_susceptibility: 0.58, emotional_amplification_rate: 0.60,
    social_network_density: 0.72, fear_cascade_intensity: 0.42, euphoria_bubble_risk: 0.15,
    rage_contagion_potential: 0.78, anxiety_baseline: 0.50, collective_resilience: 0.42,
    emotional_immune_response: 0.45, media_amplification_effect: 0.60, influencer_contagion_leverage: 0.58,
    institutional_trust_buffer: 0.38, cross_border_contagion: 0.52, recovery_velocity: 0.42,
    emotional_polarization_index: 0.55, contagion_mutation_rate: 0.50,
  },
  // EC-004: LATAM, consumer_sentiment → low, emotional_equilibrium/none
  {
    entity_id: "EC-004", contagion_type: "consumer_sentiment", region: "LATAM",
    contagion_velocity: 0.10, population_susceptibility: 0.12, emotional_amplification_rate: 0.10,
    social_network_density: 0.15, fear_cascade_intensity: 0.08, euphoria_bubble_risk: 0.10,
    rage_contagion_potential: 0.08, anxiety_baseline: 0.10, collective_resilience: 0.90,
    emotional_immune_response: 0.88, media_amplification_effect: 0.10, influencer_contagion_leverage: 0.08,
    institutional_trust_buffer: 0.88, cross_border_contagion: 0.08, recovery_velocity: 0.92,
    emotional_polarization_index: 0.08, contagion_mutation_rate: 0.06,
  },
  // EC-005: MEA, political_rage → critical, polarization_spiral
  // polarization_spiral: emotional_polarization_index≥0.70, (1-institutional_trust_buffer)≥0.60
  // critical: composite≥60
  {
    entity_id: "EC-005", contagion_type: "political_rage", region: "MEA",
    contagion_velocity: 0.72, population_susceptibility: 0.68, emotional_amplification_rate: 0.70,
    social_network_density: 0.60, fear_cascade_intensity: 0.50, euphoria_bubble_risk: 0.18,
    rage_contagion_potential: 0.65, anxiety_baseline: 0.65, collective_resilience: 0.20,
    emotional_immune_response: 0.22, media_amplification_effect: 0.80, influencer_contagion_leverage: 0.72,
    institutional_trust_buffer: 0.25, cross_border_contagion: 0.75, recovery_velocity: 0.20,
    emotional_polarization_index: 0.82, contagion_mutation_rate: 0.68,
  },
  // EC-006: EMEA, market_euphoria → moderate, none
  // moderate: 20≤composite<40; none pattern
  {
    entity_id: "EC-006", contagion_type: "market_euphoria", region: "EMEA",
    contagion_velocity: 0.35, population_susceptibility: 0.38, emotional_amplification_rate: 0.40,
    social_network_density: 0.38, fear_cascade_intensity: 0.28, euphoria_bubble_risk: 0.55,
    rage_contagion_potential: 0.30, anxiety_baseline: 0.35, collective_resilience: 0.62,
    emotional_immune_response: 0.60, media_amplification_effect: 0.38, influencer_contagion_leverage: 0.35,
    institutional_trust_buffer: 0.58, cross_border_contagion: 0.35, recovery_velocity: 0.62,
    emotional_polarization_index: 0.32, contagion_mutation_rate: 0.30,
  },
  // EC-007: APAC, social_media_rage → high, anxiety_tsunami
  // anxiety_tsunami: anxiety_baseline≥0.70, population_susceptibility≥0.65
  // high: 40≤composite<60
  {
    entity_id: "EC-007", contagion_type: "social_media_rage", region: "APAC",
    contagion_velocity: 0.52, population_susceptibility: 0.72, emotional_amplification_rate: 0.55,
    social_network_density: 0.58, fear_cascade_intensity: 0.48, euphoria_bubble_risk: 0.12,
    rage_contagion_potential: 0.52, anxiety_baseline: 0.78, collective_resilience: 0.38,
    emotional_immune_response: 0.40, media_amplification_effect: 0.55, influencer_contagion_leverage: 0.52,
    institutional_trust_buffer: 0.42, cross_border_contagion: 0.50, recovery_velocity: 0.38,
    emotional_polarization_index: 0.48, contagion_mutation_rate: 0.45,
  },
  // EC-008: NOAM, financial_panic → critical, euphoria_mania
  // euphoria_mania: euphoria_bubble_risk≥0.70, emotional_amplification_rate≥0.60
  // critical: composite≥60
  {
    entity_id: "EC-008", contagion_type: "financial_panic", region: "NOAM",
    contagion_velocity: 0.75, population_susceptibility: 0.78, emotional_amplification_rate: 0.82,
    social_network_density: 0.72, fear_cascade_intensity: 0.55, euphoria_bubble_risk: 0.80,
    rage_contagion_potential: 0.58, anxiety_baseline: 0.65, collective_resilience: 0.20,
    emotional_immune_response: 0.18, media_amplification_effect: 0.80, influencer_contagion_leverage: 0.78,
    institutional_trust_buffer: 0.28, cross_border_contagion: 0.72, recovery_velocity: 0.20,
    emotional_polarization_index: 0.62, contagion_mutation_rate: 0.58,
  },
];

type Entity = (typeof MOCK_ENTITIES)[0];

function spreadScore(e: Entity): number {
  const raw = (e.contagion_velocity * 0.4 + e.social_network_density * 0.35 + e.population_susceptibility * 0.25) * 100;
  return Math.round(raw * 100) / 100;
}

function amplificationScore(e: Entity): number {
  const raw = (e.media_amplification_effect * 0.4 + e.emotional_amplification_rate * 0.35 + e.influencer_contagion_leverage * 0.25) * 100;
  return Math.round(raw * 100) / 100;
}

function resilienceScore(e: Entity): number {
  const raw = ((1 - e.collective_resilience) * 0.4 + (1 - e.emotional_immune_response) * 0.35 + (1 - e.recovery_velocity) * 0.25) * 100;
  return Math.round(raw * 100) / 100;
}

function polarizationScore(e: Entity): number {
  const raw = (e.emotional_polarization_index * 0.4 + e.rage_contagion_potential * 0.35 + e.contagion_mutation_rate * 0.25) * 100;
  return Math.round(raw * 100) / 100;
}

function contagionComposite(spread: number, amplification: number, resilience: number, polarization: number): number {
  return Math.round((spread * 0.30 + amplification * 0.25 + resilience * 0.25 + polarization * 0.20) * 100) / 100;
}

function contagionPattern(e: Entity): string {
  if (e.contagion_velocity >= 0.70 && e.fear_cascade_intensity >= 0.65) return "panic_epidemic";
  if (e.euphoria_bubble_risk >= 0.70 && e.emotional_amplification_rate >= 0.60) return "euphoria_mania";
  if (e.rage_contagion_potential >= 0.70 && e.social_network_density >= 0.65) return "rage_wildfire";
  if (e.anxiety_baseline >= 0.70 && e.population_susceptibility >= 0.65) return "anxiety_tsunami";
  if (e.emotional_polarization_index >= 0.70 && (1 - e.institutional_trust_buffer) >= 0.60) return "polarization_spiral";
  return "none";
}

function contagionRisk(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}

function contagionSeverity(composite: number): string {
  if (composite >= 75) return "contagion_emergency";
  if (composite >= 50) return "high_contagion";
  if (composite >= 25) return "contagion_developing";
  return "emotional_equilibrium";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "contagion_circuit_breaker";
  if (risk === "high" && pattern === "rage_wildfire") return "rage_de_escalation";
  if (risk === "high") return "emotional_containment";
  if (risk === "moderate") return "contagion_monitoring";
  return "no_action";
}

function contagionSignal(e: Entity, risk: string, composite: number): string {
  const comp = Math.round(composite);
  if (risk === "critical") {
    return `Critique — vélocité contagion ${Math.round(e.contagion_velocity * 100)}% — amplification médias ${Math.round(e.media_amplification_effect * 100)}% — composite ${comp}`;
  }
  if (risk === "high") {
    return `Élevé — polarisation émotionnelle ${Math.round(e.emotional_polarization_index * 100)}% — résilience collective ${Math.round(e.collective_resilience * 100)}% — composite ${comp}`;
  }
  if (risk === "moderate") {
    return `Modéré — susceptibilité population ${Math.round(e.population_susceptibility * 100)}% — composite ${comp}`;
  }
  return "Équilibre émotionnel — contagion contrôlée, résilience collective forte, polarisation faible";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map((e) => {
      const spread        = spreadScore(e);
      const amplification = amplificationScore(e);
      const resilience    = resilienceScore(e);
      const polarization  = polarizationScore(e);
      const composite     = contagionComposite(spread, amplification, resilience, polarization);
      const pattern       = contagionPattern(e);
      const risk          = contagionRisk(composite);
      const severity      = contagionSeverity(composite);
      const action        = recommendedAction(risk, pattern);
      const signal        = contagionSignal(e, risk, composite);

      return {
        entity_id:                       e.entity_id,
        region:                          e.region,
        contagion_type:                  e.contagion_type,
        contagion_risk:                  risk,
        contagion_pattern:               pattern,
        contagion_severity:              severity,
        recommended_action:              action,
        spread_score:                    spread,
        amplification_score:             amplification,
        resilience_score:                resilience,
        polarization_score:              polarization,
        contagion_composite:             composite,
        is_in_contagion_crisis:          composite >= 60,
        requires_contagion_intervention: composite >= 40,
        contagion_signal:                signal,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tSpread = 0, tAmplification = 0, tResilience = 0, tPolarization = 0, tComposite = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.contagion_risk]       = (rc[ent.contagion_risk]       || 0) + 1;
      pc[ent.contagion_pattern]    = (pc[ent.contagion_pattern]    || 0) + 1;
      sc[ent.contagion_severity]   = (sc[ent.contagion_severity]   || 0) + 1;
      ac[ent.recommended_action]   = (ac[ent.recommended_action]   || 0) + 1;
      tSpread        += ent.spread_score;
      tAmplification += ent.amplification_score;
      tResilience    += ent.resilience_score;
      tPolarization  += ent.polarization_score;
      tComposite     += ent.contagion_composite;
      if (ent.is_in_contagion_crisis)          crisisCount++;
      if (ent.requires_contagion_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComposite / n * 10) / 10;

    const summary = {
      total:                             n,
      risk_counts:                       rc,
      pattern_counts:                    pc,
      severity_counts:                   sc,
      action_counts:                     ac,
      avg_contagion_composite:           avgComposite,
      contagion_crisis_count:            crisisCount,
      contagion_intervention_count:      interventionCount,
      avg_spread_score:                  Math.round(tSpread / n * 10) / 10,
      avg_amplification_score:           Math.round(tAmplification / n * 10) / 10,
      avg_resilience_score:              Math.round(tResilience / n * 10) / 10,
      avg_polarization_score:            Math.round(tPolarization / n * 10) / 10,
      avg_estimated_contagion_index:     Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "emotional-contagion-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/emotional-contagion-engine`);
    if (!upstream.ok) throw new Error(`upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "emotional-contagion-engine"));
  } catch {
    return NextResponse.json(sealResponse({ error: "upstream unavailable" }, "emotional-contagion-engine"), { status: 502 });
  }
}
