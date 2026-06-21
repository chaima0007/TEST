import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // PHA-001 — EMEA, cognitive_enhancement → critical, cognitive_arms_race
  { id: "PHA-001", augmentation_domain: "cognitive_enhancement", region: "EMEA",
    cognitive_enhancement_penetration: 0.82, genetic_modification_rate: 0.30,
    neural_interface_adoption: 0.70, longevity_extension_index: 0.35,
    augmentation_equity_gap: 0.60, regulatory_lag: 0.72, social_acceptance_rate: 0.38,
    enhancement_reversibility: 0.28, biological_integrity_risk: 0.55,
    cognitive_arms_race_intensity: 0.78, human_definition_instability: 0.50,
    post_human_transition_speed: 0.68, identity_dissolution_risk: 0.55,
    augmentation_dependency: 0.58, ethical_consensus_deficit: 0.65,
    competitiveness_divergence: 0.62, natural_human_obsolescence_risk: 0.70 },

  // PHA-002 — APAC, longevity → low, controlled_augmentation/none
  { id: "PHA-002", augmentation_domain: "longevity", region: "APAC",
    cognitive_enhancement_penetration: 0.12, genetic_modification_rate: 0.18,
    neural_interface_adoption: 0.10, longevity_extension_index: 0.55,
    augmentation_equity_gap: 0.10, regulatory_lag: 0.12, social_acceptance_rate: 0.85,
    enhancement_reversibility: 0.88, biological_integrity_risk: 0.12,
    cognitive_arms_race_intensity: 0.08, human_definition_instability: 0.10,
    post_human_transition_speed: 0.10, identity_dissolution_risk: 0.08,
    augmentation_dependency: 0.10, ethical_consensus_deficit: 0.12,
    competitiveness_divergence: 0.10, natural_human_obsolescence_risk: 0.08 },

  // PHA-003 — NOAM, neural_interface → high, identity_collapse
  { id: "PHA-003", augmentation_domain: "neural_interface", region: "NOAM",
    cognitive_enhancement_penetration: 0.55, genetic_modification_rate: 0.35,
    neural_interface_adoption: 0.62, longevity_extension_index: 0.40,
    augmentation_equity_gap: 0.50, regulatory_lag: 0.58, social_acceptance_rate: 0.45,
    enhancement_reversibility: 0.32, biological_integrity_risk: 0.55,
    cognitive_arms_race_intensity: 0.48, human_definition_instability: 0.62,
    post_human_transition_speed: 0.52, identity_dissolution_risk: 0.70,
    augmentation_dependency: 0.48, ethical_consensus_deficit: 0.55,
    competitiveness_divergence: 0.45, natural_human_obsolescence_risk: 0.52 },

  // PHA-004 — LATAM, longevity → low, controlled_augmentation/none
  { id: "PHA-004", augmentation_domain: "longevity", region: "LATAM",
    cognitive_enhancement_penetration: 0.10, genetic_modification_rate: 0.15,
    neural_interface_adoption: 0.08, longevity_extension_index: 0.30,
    augmentation_equity_gap: 0.15, regulatory_lag: 0.18, social_acceptance_rate: 0.80,
    enhancement_reversibility: 0.82, biological_integrity_risk: 0.10,
    cognitive_arms_race_intensity: 0.10, human_definition_instability: 0.12,
    post_human_transition_speed: 0.12, identity_dissolution_risk: 0.10,
    augmentation_dependency: 0.12, ethical_consensus_deficit: 0.15,
    competitiveness_divergence: 0.12, natural_human_obsolescence_risk: 0.10 },

  // PHA-005 — MEA, genetic_modification → critical, augmentation_divide
  { id: "PHA-005", augmentation_domain: "genetic_modification", region: "MEA",
    cognitive_enhancement_penetration: 0.65, genetic_modification_rate: 0.75,
    neural_interface_adoption: 0.45, longevity_extension_index: 0.50,
    augmentation_equity_gap: 0.82, regulatory_lag: 0.62, social_acceptance_rate: 0.30,
    enhancement_reversibility: 0.22, biological_integrity_risk: 0.60,
    cognitive_arms_race_intensity: 0.55, human_definition_instability: 0.48,
    post_human_transition_speed: 0.70, identity_dissolution_risk: 0.55,
    augmentation_dependency: 0.52, ethical_consensus_deficit: 0.68,
    competitiveness_divergence: 0.72, natural_human_obsolescence_risk: 0.75 },

  // PHA-006 — EMEA, neural_interface → moderate, none
  { id: "PHA-006", augmentation_domain: "neural_interface", region: "EMEA",
    cognitive_enhancement_penetration: 0.30, genetic_modification_rate: 0.25,
    neural_interface_adoption: 0.28, longevity_extension_index: 0.32,
    augmentation_equity_gap: 0.30, regulatory_lag: 0.32, social_acceptance_rate: 0.62,
    enhancement_reversibility: 0.58, biological_integrity_risk: 0.30,
    cognitive_arms_race_intensity: 0.28, human_definition_instability: 0.30,
    post_human_transition_speed: 0.28, identity_dissolution_risk: 0.30,
    augmentation_dependency: 0.28, ethical_consensus_deficit: 0.32,
    competitiveness_divergence: 0.30, natural_human_obsolescence_risk: 0.28 },

  // PHA-007 — APAC, cognitive_enhancement → high, regulatory_vacuum
  { id: "PHA-007", augmentation_domain: "cognitive_enhancement", region: "APAC",
    cognitive_enhancement_penetration: 0.58, genetic_modification_rate: 0.42,
    neural_interface_adoption: 0.50, longevity_extension_index: 0.45,
    augmentation_equity_gap: 0.55, regulatory_lag: 0.78, social_acceptance_rate: 0.40,
    enhancement_reversibility: 0.35, biological_integrity_risk: 0.50,
    cognitive_arms_race_intensity: 0.60, human_definition_instability: 0.48,
    post_human_transition_speed: 0.55, identity_dissolution_risk: 0.52,
    augmentation_dependency: 0.48, ethical_consensus_deficit: 0.72,
    competitiveness_divergence: 0.55, natural_human_obsolescence_risk: 0.58 },

  // PHA-008 — NOAM, genetic_modification → critical, biological_sovereignty_loss
  { id: "PHA-008", augmentation_domain: "genetic_modification", region: "NOAM",
    cognitive_enhancement_penetration: 0.70, genetic_modification_rate: 0.88,
    neural_interface_adoption: 0.55, longevity_extension_index: 0.60,
    augmentation_equity_gap: 0.65, regulatory_lag: 0.68, social_acceptance_rate: 0.28,
    enhancement_reversibility: 0.18, biological_integrity_risk: 0.78,
    cognitive_arms_race_intensity: 0.62, human_definition_instability: 0.52,
    post_human_transition_speed: 0.72, identity_dissolution_risk: 0.60,
    augmentation_dependency: 0.72, ethical_consensus_deficit: 0.70,
    competitiveness_divergence: 0.68, natural_human_obsolescence_risk: 0.80 },
];

type Entity = typeof MOCK_ENTITIES[0];

function adoptionScore(e: Entity): number {
  const raw =
    e.cognitive_enhancement_penetration * 0.35 +
    e.neural_interface_adoption * 0.35 +
    e.post_human_transition_speed * 0.30;
  return Math.round(raw * 100 * 100) / 100;
}

function equityScore(e: Entity): number {
  const raw =
    e.augmentation_equity_gap * 0.40 +
    e.competitiveness_divergence * 0.35 +
    e.natural_human_obsolescence_risk * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function integrityScore(e: Entity): number {
  const raw =
    e.biological_integrity_risk * 0.40 +
    e.identity_dissolution_risk * 0.35 +
    e.augmentation_dependency * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function transitionScore(e: Entity): number {
  const raw =
    e.regulatory_lag * 0.35 +
    e.ethical_consensus_deficit * 0.35 +
    (1 - e.social_acceptance_rate) * 0.30;
  return Math.round(raw * 100 * 100) / 100;
}

function compositeScore(
  adoption: number,
  equity: number,
  integrity: number,
  transition: number
): number {
  return Math.round((adoption * 0.30 + equity * 0.25 + integrity * 0.25 + transition * 0.20) * 100) / 100;
}

function augmentationRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function augmentationPattern(e: Entity): string {
  if (e.cognitive_arms_race_intensity >= 0.65 && e.cognitive_enhancement_penetration >= 0.60)
    return "cognitive_arms_race";
  if (e.identity_dissolution_risk >= 0.65 && e.human_definition_instability >= 0.55)
    return "identity_collapse";
  if (e.augmentation_equity_gap >= 0.70 && e.competitiveness_divergence >= 0.60)
    return "augmentation_divide";
  if (e.regulatory_lag >= 0.70 && e.ethical_consensus_deficit >= 0.60)
    return "regulatory_vacuum";
  if (e.biological_integrity_risk >= 0.65 && e.augmentation_dependency >= 0.60)
    return "biological_sovereignty_loss";
  return "none";
}

function augmentationSeverity(comp: number): string {
  if (comp >= 75) return "post_human_rupture";
  if (comp >= 50) return "high_transition_risk";
  if (comp >= 25) return "early_disruption";
  return "controlled_augmentation";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "augmentation_governance_emergency";
  if (risk === "high" && pattern === "identity_collapse") return "identity_preservation_protocol";
  if (risk === "high") return "transition_management";
  if (risk === "moderate") return "augmentation_monitoring";
  return "no_action";
}

function augmentationSignal(e: Entity, risk: string, comp: number): string {
  const compInt = Math.round(comp);
  if (risk === "critical") {
    return `Critique — course augmentation cognitive ${Math.round(e.cognitive_arms_race_intensity * 100)}% — dissolution identité ${Math.round(e.identity_dissolution_risk * 100)}% — composite ${compInt}`;
  }
  if (risk === "high") {
    return `Élevé — fracture augmentation ${Math.round(e.augmentation_equity_gap * 100)}% — retard réglementaire ${Math.round(e.regulatory_lag * 100)}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `Modéré — adoption augmentation ${Math.round(e.cognitive_enhancement_penetration * 100)}% — composite ${compInt}`;
  }
  return "Transition post-humaine maîtrisée — augmentation équitable, intégrité biologique préservée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const adoption   = adoptionScore(e);
      const equity     = equityScore(e);
      const integrity  = integrityScore(e);
      const transition = transitionScore(e);
      const comp       = compositeScore(adoption, equity, integrity, transition);
      const risk       = augmentationRisk(comp);
      const pattern    = augmentationPattern(e);
      const severity   = augmentationSeverity(comp);
      const action     = recommendedAction(risk, pattern);
      const sig        = augmentationSignal(e, risk, comp);

      return {
        id:                        e.entity_id,
        region:                           e.region,
        augmentation_domain:              e.augmentation_domain,
        augmentation_risk:                risk,
        augmentation_pattern:             pattern,
        augmentation_severity:            severity,
        recommended_action:               action,
        adoption_score:                   adoption,
        equity_score:                     equity,
        integrity_score:                  integrity,
        transition_score:                 transition,
        augmentation_composite:           comp,
        is_in_augmentation_crisis:        comp >= 60,
        requires_augmentation_intervention: comp >= 40,
        augmentation_signal:              sig,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tAdoption = 0, tEquity = 0, tIntegrity = 0, tTransition = 0, tComp = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.augmentation_risk]     = (rc[ent.augmentation_risk]     || 0) + 1;
      pc[ent.augmentation_pattern]  = (pc[ent.augmentation_pattern]  || 0) + 1;
      sc[ent.augmentation_severity] = (sc[ent.augmentation_severity] || 0) + 1;
      ac[ent.recommended_action]    = (ac[ent.recommended_action]    || 0) + 1;
      tAdoption   += ent.adoption_score;
      tEquity     += ent.equity_score;
      tIntegrity  += ent.integrity_score;
      tTransition += ent.transition_score;
      tComp       += ent.augmentation_composite;
      if (ent.is_in_augmentation_crisis)          crisisCount++;
      if (ent.requires_augmentation_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComposite = tComp / n;
    const summary = {
      total:                                       n,
      risk_counts:                                 rc,
      pattern_counts:                              pc,
      severity_counts:                             sc,
      action_counts:                               ac,
      avg_augmentation_composite:                  Math.round(avgComposite * 10) / 10,
      augmentation_crisis_count:                   crisisCount,
      augmentation_intervention_count:             interventionCount,
      avg_adoption_score:                          Math.round(tAdoption / n * 10) / 10,
      avg_equity_score:                            Math.round(tEquity / n * 10) / 10,
      avg_integrity_score:                         Math.round(tIntegrity / n * 10) / 10,
      avg_transition_score:                        Math.round(tTransition / n * 10) / 10,
      avg_estimated_augmentation_disruption_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary }, "post-human-augmentation-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/post-human-augmentation-engine`);
    const json = await upstream.json();
    return NextResponse.json(
      sealResponse(json, "post-human-augmentation-engine")
    );
  } catch {
    return NextResponse.json(
      sealResponse({ error: "upstream_unavailable" }, "post-human-augmentation-engine"),
      { status: 502 }
    );
  }
}
