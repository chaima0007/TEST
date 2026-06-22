import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // NC-001 — critical, narrative_hijacking
  {
    id: "NC-001", narrative_domain: "brand_narrative", region: "EMEA",
    narrative_coherence: 0.20, message_amplification_rate: 0.72, counter_narrative_exposure: 0.68,
    memetic_mutation_speed: 0.75, brand_narrative_integrity: 0.18, hostile_framing_intensity: 0.78,
    misinformation_penetration: 0.80, narrative_capture_risk: 0.82, audience_trust_level: 0.22,
    cultural_resonance_alignment: 0.20, emotional_narrative_charge: 0.85, viral_spread_coefficient: 0.72,
    institutional_narrative_support: 0.18, narrative_resilience: 0.20, sovereignty_gap: 0.78,
    strategic_communication_effectiveness: 0.18, memetic_immune_response: 0.15,
  },
  // NC-002 — low, narrative_sovereign/none
  {
    id: "NC-002", narrative_domain: "corporate_communications", region: "APAC",
    narrative_coherence: 0.92, message_amplification_rate: 0.20, counter_narrative_exposure: 0.12,
    memetic_mutation_speed: 0.10, brand_narrative_integrity: 0.90, hostile_framing_intensity: 0.10,
    misinformation_penetration: 0.08, narrative_capture_risk: 0.10, audience_trust_level: 0.92,
    cultural_resonance_alignment: 0.90, emotional_narrative_charge: 0.15, viral_spread_coefficient: 0.10,
    institutional_narrative_support: 0.90, narrative_resilience: 0.92, sovereignty_gap: 0.08,
    strategic_communication_effectiveness: 0.90, memetic_immune_response: 0.92,
  },
  // NC-003 — high, memetic_attack
  {
    id: "NC-003", narrative_domain: "strategic_messaging", region: "NOAM",
    narrative_coherence: 0.42, message_amplification_rate: 0.68, counter_narrative_exposure: 0.55,
    memetic_mutation_speed: 0.60, brand_narrative_integrity: 0.45, hostile_framing_intensity: 0.72,
    misinformation_penetration: 0.65, narrative_capture_risk: 0.55, audience_trust_level: 0.48,
    cultural_resonance_alignment: 0.45, emotional_narrative_charge: 0.70, viral_spread_coefficient: 0.60,
    institutional_narrative_support: 0.42, narrative_resilience: 0.40, sovereignty_gap: 0.52,
    strategic_communication_effectiveness: 0.42, memetic_immune_response: 0.38,
  },
  // NC-004 — low, narrative_sovereign/none
  {
    id: "NC-004", narrative_domain: "corporate_communications", region: "LATAM",
    narrative_coherence: 0.88, message_amplification_rate: 0.22, counter_narrative_exposure: 0.15,
    memetic_mutation_speed: 0.12, brand_narrative_integrity: 0.88, hostile_framing_intensity: 0.12,
    misinformation_penetration: 0.10, narrative_capture_risk: 0.12, audience_trust_level: 0.88,
    cultural_resonance_alignment: 0.85, emotional_narrative_charge: 0.18, viral_spread_coefficient: 0.12,
    institutional_narrative_support: 0.88, narrative_resilience: 0.88, sovereignty_gap: 0.10,
    strategic_communication_effectiveness: 0.88, memetic_immune_response: 0.88,
  },
  // NC-005 — critical, viral_narrative_collapse
  {
    id: "NC-005", narrative_domain: "brand_narrative", region: "MEA",
    narrative_coherence: 0.18, message_amplification_rate: 0.88, counter_narrative_exposure: 0.72,
    memetic_mutation_speed: 0.80, brand_narrative_integrity: 0.22, hostile_framing_intensity: 0.75,
    misinformation_penetration: 0.70, narrative_capture_risk: 0.60, audience_trust_level: 0.25,
    cultural_resonance_alignment: 0.22, emotional_narrative_charge: 0.90, viral_spread_coefficient: 0.85,
    institutional_narrative_support: 0.20, narrative_resilience: 0.18, sovereignty_gap: 0.72,
    strategic_communication_effectiveness: 0.20, memetic_immune_response: 0.18,
  },
  // NC-006 — moderate, none
  {
    id: "NC-006", narrative_domain: "public_affairs", region: "EMEA",
    narrative_coherence: 0.62, message_amplification_rate: 0.42, counter_narrative_exposure: 0.38,
    memetic_mutation_speed: 0.35, brand_narrative_integrity: 0.62, hostile_framing_intensity: 0.38,
    misinformation_penetration: 0.35, narrative_capture_risk: 0.38, audience_trust_level: 0.62,
    cultural_resonance_alignment: 0.60, emotional_narrative_charge: 0.40, viral_spread_coefficient: 0.38,
    institutional_narrative_support: 0.62, narrative_resilience: 0.62, sovereignty_gap: 0.35,
    strategic_communication_effectiveness: 0.62, memetic_immune_response: 0.60,
  },
  // NC-007 — high, audience_defection
  {
    id: "NC-007", narrative_domain: "strategic_messaging", region: "APAC",
    narrative_coherence: 0.45, message_amplification_rate: 0.65, counter_narrative_exposure: 0.68,
    memetic_mutation_speed: 0.58, brand_narrative_integrity: 0.50, hostile_framing_intensity: 0.55,
    misinformation_penetration: 0.52, narrative_capture_risk: 0.50, audience_trust_level: 0.22,
    cultural_resonance_alignment: 0.38, emotional_narrative_charge: 0.65, viral_spread_coefficient: 0.55,
    institutional_narrative_support: 0.40, narrative_resilience: 0.42, sovereignty_gap: 0.50,
    strategic_communication_effectiveness: 0.40, memetic_immune_response: 0.38,
  },
  // NC-008 — critical, sovereignty_erosion
  {
    id: "NC-008", narrative_domain: "brand_narrative", region: "NOAM",
    narrative_coherence: 0.22, message_amplification_rate: 0.80, counter_narrative_exposure: 0.45,
    memetic_mutation_speed: 0.72, brand_narrative_integrity: 0.28, hostile_framing_intensity: 0.62,
    misinformation_penetration: 0.60, narrative_capture_risk: 0.62, audience_trust_level: 0.28,
    cultural_resonance_alignment: 0.25, emotional_narrative_charge: 0.82, viral_spread_coefficient: 0.68,
    institutional_narrative_support: 0.22, narrative_resilience: 0.22, sovereignty_gap: 0.78,
    strategic_communication_effectiveness: 0.22, memetic_immune_response: 0.20,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function integrityScore(e: Entity): number {
  const raw =
    (1 - e.narrative_coherence) * 0.4 +
    (1 - e.brand_narrative_integrity) * 0.35 +
    (1 - e.audience_trust_level) * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function penetrationScore(e: Entity): number {
  const raw =
    e.misinformation_penetration * 0.4 +
    e.hostile_framing_intensity * 0.35 +
    e.counter_narrative_exposure * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function resilienceScore(e: Entity): number {
  const raw =
    (1 - e.narrative_resilience) * 0.4 +
    (1 - e.memetic_immune_response) * 0.35 +
    (1 - e.strategic_communication_effectiveness) * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function sovereigntyScore(e: Entity): number {
  const raw =
    e.sovereignty_gap * 0.4 +
    e.narrative_capture_risk * 0.35 +
    e.memetic_mutation_speed * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function compositeScore(
  integrity: number,
  penetration: number,
  resilience: number,
  sovereignty: number
): number {
  return Math.round(
    (integrity * 0.30 + penetration * 0.25 + resilience * 0.25 + sovereignty * 0.20) * 100
  ) / 100;
}

function narrativePattern(e: Entity): string {
  if (e.narrative_capture_risk >= 0.65 && (1 - e.brand_narrative_integrity) >= 0.55)
    return "narrative_hijacking";
  if (e.hostile_framing_intensity >= 0.65 && e.misinformation_penetration >= 0.55)
    return "memetic_attack";
  if (e.viral_spread_coefficient >= 0.70 && (1 - e.narrative_coherence) >= 0.55)
    return "viral_narrative_collapse";
  if ((1 - e.audience_trust_level) >= 0.70 && e.counter_narrative_exposure >= 0.60)
    return "audience_defection";
  if (e.sovereignty_gap >= 0.70 && (1 - e.narrative_resilience) >= 0.60)
    return "sovereignty_erosion";
  return "none";
}

function narrativeRisk(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}

function narrativeSeverity(composite: number): string {
  if (composite >= 75) return "narrative_collapse";
  if (composite >= 50) return "high_vulnerability";
  if (composite >= 25) return "developing_threat";
  return "narrative_sovereign";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "narrative_emergency_response";
  if (risk === "high" && pattern === "memetic_attack") return "counter_memetic_operation";
  if (risk === "high") return "narrative_reinforcement";
  if (risk === "moderate") return "narrative_monitoring";
  return "no_action";
}

function narrativeSignal(e: Entity, risk: string, composite: number): string {
  const compInt = Math.round(composite);
  if (risk === "critical") {
    return `Critique — intégrité narrative ${Math.round(e.narrative_coherence * 100)}% — pénétration désinformation ${Math.round(e.misinformation_penetration * 100)}% — composite ${compInt}`;
  }
  if (risk === "high") {
    return `Élevé — risque capture narrative ${Math.round(e.narrative_capture_risk * 100)}% — confiance audience ${Math.round(e.audience_trust_level * 100)}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `Modéré — exposition contre-narratives ${Math.round(e.counter_narrative_exposure * 100)}% — composite ${compInt}`;
  }
  return "Souveraineté narrative maintenue — cohérence des messages, résilience mémetique forte";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[narrative-control-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tIntegrity = 0, tPenetration = 0, tResilience = 0, tSovereignty = 0;
    let tComposite = 0, crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.narrative_risk]      = (rc[ent.narrative_risk]      || 0) + 1;
      pc[ent.narrative_pattern]   = (pc[ent.narrative_pattern]   || 0) + 1;
      sc[ent.narrative_severity]  = (sc[ent.narrative_severity]  || 0) + 1;
      ac[ent.recommended_action]  = (ac[ent.recommended_action]  || 0) + 1;
      tIntegrity   += ent.integrity_score;
      tPenetration += ent.penetration_score;
      tResilience  += ent.resilience_score;
      tSovereignty += ent.sovereignty_score;
      tComposite   += ent.narrative_composite;
      if (ent.is_in_narrative_crisis)          crisisCount++;
      if (ent.requires_narrative_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComposite = tComposite / n;

    const summary = {
      total:                                 n,
      risk_counts:                           rc,
      pattern_counts:                        pc,
      severity_counts:                       sc,
      action_counts:                         ac,
      avg_narrative_composite:               Math.round(avgComposite * 10) / 10,
      narrative_crisis_count:                crisisCount,
      narrative_intervention_count:          interventionCount,
      avg_integrity_score:                   Math.round(tIntegrity   / n * 10) / 10,
      avg_penetration_score:                 Math.round(tPenetration / n * 10) / 10,
      avg_resilience_score:                  Math.round(tResilience  / n * 10) / 10,
      avg_sovereignty_score:                 Math.round(tSovereignty / n * 10) / 10,
      avg_estimated_narrative_threat_index:  Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "narrative-control-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/narrative-control-engine`, { next: { revalidate: 30 } });
    return sealResponse(NextResponse.json(sealResponse(await upstream.json(), "narrative-control-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream narrative-control-engine unavailable" }, "narrative-control-engine"),
      { status: 502 }
    ));
  }
}
