import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // FPA-001 EMEA incumbent_corporation — critical assumption_collapse
  { id:"FPA-001", domain_type:"incumbent_corporation", region:"EMEA",  assumption_density:0.85, conventional_wisdom_dependency:0.80, analogy_reasoning_reliance:0.75, first_order_thinking_dominance:0.80, mental_model_rigidity:0.75, epistemic_closure_risk:0.70, innovation_constraint_index:0.75, reasoning_from_authority_bias:0.80, complexity_masking_fundamentals:0.70, cost_estimation_accuracy:0.30, physics_constraint_violation_risk:0.65, path_dependency_lock_in:0.75, abstraction_layer_opacity:0.65, benchmark_anchoring_distortion:0.70, consensus_capture_risk:0.65, inversion_thinking_deficit:0.70, regenerative_capacity:0.25 },
  // FPA-002 APAC startup_ecosystem — low none
  { id:"FPA-002", domain_type:"startup_ecosystem",     region:"APAC",  assumption_density:0.20, conventional_wisdom_dependency:0.15, analogy_reasoning_reliance:0.25, first_order_thinking_dominance:0.20, mental_model_rigidity:0.15, epistemic_closure_risk:0.20, innovation_constraint_index:0.15, reasoning_from_authority_bias:0.10, complexity_masking_fundamentals:0.20, cost_estimation_accuracy:0.85, physics_constraint_violation_risk:0.15, path_dependency_lock_in:0.10, abstraction_layer_opacity:0.15, benchmark_anchoring_distortion:0.20, consensus_capture_risk:0.15, inversion_thinking_deficit:0.15, regenerative_capacity:0.90 },
  // FPA-003 NOAM government_agency — high epistemic_lock
  { id:"FPA-003", domain_type:"government_agency",     region:"NOAM",  assumption_density:0.55, conventional_wisdom_dependency:0.60, analogy_reasoning_reliance:0.50, first_order_thinking_dominance:0.60, mental_model_rigidity:0.75, epistemic_closure_risk:0.70, innovation_constraint_index:0.60, reasoning_from_authority_bias:0.65, complexity_masking_fundamentals:0.55, cost_estimation_accuracy:0.45, physics_constraint_violation_risk:0.50, path_dependency_lock_in:0.65, abstraction_layer_opacity:0.55, benchmark_anchoring_distortion:0.50, consensus_capture_risk:0.60, inversion_thinking_deficit:0.55, regenerative_capacity:0.40 },
  // FPA-004 LATAM sme_cluster — low none
  { id:"FPA-004", domain_type:"sme_cluster",           region:"LATAM", assumption_density:0.25, conventional_wisdom_dependency:0.20, analogy_reasoning_reliance:0.30, first_order_thinking_dominance:0.25, mental_model_rigidity:0.20, epistemic_closure_risk:0.25, innovation_constraint_index:0.20, reasoning_from_authority_bias:0.15, complexity_masking_fundamentals:0.25, cost_estimation_accuracy:0.80, physics_constraint_violation_risk:0.20, path_dependency_lock_in:0.15, abstraction_layer_opacity:0.20, benchmark_anchoring_distortion:0.25, consensus_capture_risk:0.20, inversion_thinking_deficit:0.20, regenerative_capacity:0.85 },
  // FPA-005 MEA legacy_industry — critical complexity_blindness
  { id:"FPA-005", domain_type:"legacy_industry",       region:"MEA",   assumption_density:0.80, conventional_wisdom_dependency:0.75, analogy_reasoning_reliance:0.70, first_order_thinking_dominance:0.75, mental_model_rigidity:0.70, epistemic_closure_risk:0.65, innovation_constraint_index:0.75, reasoning_from_authority_bias:0.70, complexity_masking_fundamentals:0.80, cost_estimation_accuracy:0.25, physics_constraint_violation_risk:0.70, path_dependency_lock_in:0.70, abstraction_layer_opacity:0.75, benchmark_anchoring_distortion:0.65, consensus_capture_risk:0.60, inversion_thinking_deficit:0.70, regenerative_capacity:0.20 },
  // FPA-006 EMEA academic_institution — moderate none
  { id:"FPA-006", domain_type:"academic_institution",  region:"EMEA",  assumption_density:0.35, conventional_wisdom_dependency:0.40, analogy_reasoning_reliance:0.35, first_order_thinking_dominance:0.35, mental_model_rigidity:0.40, epistemic_closure_risk:0.35, innovation_constraint_index:0.35, reasoning_from_authority_bias:0.45, complexity_masking_fundamentals:0.35, cost_estimation_accuracy:0.65, physics_constraint_violation_risk:0.30, path_dependency_lock_in:0.40, abstraction_layer_opacity:0.35, benchmark_anchoring_distortion:0.40, consensus_capture_risk:0.35, inversion_thinking_deficit:0.35, regenerative_capacity:0.65 },
  // FPA-007 APAC conglomerate — high benchmark_trap
  { id:"FPA-007", domain_type:"conglomerate",          region:"APAC",  assumption_density:0.55, conventional_wisdom_dependency:0.60, analogy_reasoning_reliance:0.55, first_order_thinking_dominance:0.55, mental_model_rigidity:0.55, epistemic_closure_risk:0.55, innovation_constraint_index:0.60, reasoning_from_authority_bias:0.55, complexity_masking_fundamentals:0.55, cost_estimation_accuracy:0.45, physics_constraint_violation_risk:0.50, path_dependency_lock_in:0.55, abstraction_layer_opacity:0.55, benchmark_anchoring_distortion:0.75, consensus_capture_risk:0.70, inversion_thinking_deficit:0.60, regenerative_capacity:0.40 },
  // FPA-008 NOAM regulatory_body — critical innovation_atrophy
  { id:"FPA-008", domain_type:"regulatory_body",       region:"NOAM",  assumption_density:0.80, conventional_wisdom_dependency:0.70, analogy_reasoning_reliance:0.65, first_order_thinking_dominance:0.75, mental_model_rigidity:0.75, epistemic_closure_risk:0.70, innovation_constraint_index:0.80, reasoning_from_authority_bias:0.75, complexity_masking_fundamentals:0.70, cost_estimation_accuracy:0.30, physics_constraint_violation_risk:0.60, path_dependency_lock_in:0.70, abstraction_layer_opacity:0.65, benchmark_anchoring_distortion:0.60, consensus_capture_risk:0.65, inversion_thinking_deficit:0.75, regenerative_capacity:0.25 },
];

type Entity = typeof MOCK_ENTITIES[0];

function assumptionScore(e: Entity): number {
  return Math.round((e.assumption_density * 0.4 + e.conventional_wisdom_dependency * 0.35 + e.analogy_reasoning_reliance * 0.25) * 100 * 100) / 100;
}
function rigidityScore(e: Entity): number {
  return Math.round((e.mental_model_rigidity * 0.4 + e.epistemic_closure_risk * 0.35 + e.path_dependency_lock_in * 0.25) * 100 * 100) / 100;
}
function blindspotScore(e: Entity): number {
  return Math.round((e.complexity_masking_fundamentals * 0.4 + e.abstraction_layer_opacity * 0.35 + e.benchmark_anchoring_distortion * 0.25) * 100 * 100) / 100;
}
function innovationScore(e: Entity): number {
  return Math.round((e.innovation_constraint_index * 0.4 + e.inversion_thinking_deficit * 0.35 + (1 - e.regenerative_capacity) * 0.25) * 100 * 100) / 100;
}
function composite(assumption: number, rigidity: number, blindspot: number, innovation: number): number {
  return Math.round((assumption * 0.30 + rigidity * 0.25 + blindspot * 0.25 + innovation * 0.20) * 100) / 100;
}
function principlesPattern(e: Entity): string {
  if (e.assumption_density >= 0.70 && e.conventional_wisdom_dependency >= 0.65) return "assumption_collapse";
  if (e.mental_model_rigidity >= 0.70 && e.epistemic_closure_risk >= 0.65)       return "epistemic_lock";
  if (e.complexity_masking_fundamentals >= 0.70 && e.abstraction_layer_opacity >= 0.65) return "complexity_blindness";
  if (e.innovation_constraint_index >= 0.70 && e.inversion_thinking_deficit >= 0.65)    return "innovation_atrophy";
  if (e.benchmark_anchoring_distortion >= 0.70 && e.consensus_capture_risk >= 0.65)     return "benchmark_trap";
  return "none";
}
function principlesRisk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function principlesSeverity(c: number): string { if (c >= 75) return "systemic_blindness_crisis"; if (c >= 50) return "high_assumption_risk"; if (c >= 25) return "assumption_accumulation"; return "first_principles_sound"; }
function recommendedAction(r: string, p: string): string {
  if (r === "critical") return "full_assumption_audit";
  if (r === "high" && p === "epistemic_lock") return "mindset_reconstruction";
  if (r === "high") return "first_principles_review";
  if (r === "moderate") return "assumption_mapping";
  return "no_action";
}
function principlesSignal(e: Entity, pat: string, comp: number): string {
  if (comp < 20) return "Premiers principes solides — densité d'hypothèses faible, modèles mentaux flexibles, angles morts limités, innovation active";
  const labels: Record<string,string> = {
    assumption_collapse:  "Effondrement d'hypothèses",
    epistemic_lock:       "Verrouillage épistémique",
    complexity_blindness: "Aveuglement par la complexité",
    innovation_atrophy:   "Atrophie de l'innovation",
    benchmark_trap:       "Piège du benchmark",
  };
  const label = labels[pat] ?? "Critique";
  return `${label} — densité d'hypothèses non vérifiées ${Math.round(e.assumption_density*100)}% — verrouillage épistémique — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const assumption = assumptionScore(e), rigidity = rigidityScore(e), blindspot = blindspotScore(e), innovation = innovationScore(e);
      const comp = composite(assumption, rigidity, blindspot, innovation);
      const pat  = principlesPattern(e), risk = principlesRisk(comp), sev = principlesSeverity(comp), act = recommendedAction(risk, pat);
      return {
        id: e.entity_id, region: e.region, domain_type: e.domain_type,
        principles_risk: risk, principles_pattern: pat, principles_severity: sev, recommended_action: act,
        assumption_score: assumption, rigidity_score: rigidity, blindspot_score: blindspot, innovation_score: innovation,
        principles_composite: comp,
        is_principles_crisis: comp >= 60,
        requires_principles_intervention: comp >= 40,
        principles_signal: principlesSignal(e, pat, comp),
      };
    });

    let tAssumption=0, tRigidity=0, tBlindspot=0, tInnovation=0, tComp=0;
    let criticalCount=0, highCount=0, moderateCount=0, lowCount=0, crisisCount=0, intervCount=0;
    for (const ent of entities) {
      if (ent.principles_risk === "critical")  criticalCount++;
      if (ent.principles_risk === "high")      highCount++;
      if (ent.principles_risk === "moderate")  moderateCount++;
      if (ent.principles_risk === "low")       lowCount++;
      if (ent.is_principles_crisis)            crisisCount++;
      if (ent.requires_principles_intervention) intervCount++;
      tAssumption += ent.assumption_score;
      tRigidity   += ent.rigidity_score;
      tBlindspot  += ent.blindspot_score;
      tInnovation += ent.innovation_score;
      tComp       += ent.principles_composite;
    }
    const n = entities.length;
    const avgComposite = tComp / n;

    return NextResponse.json(sealResponse({
      entity_results: entities,
      total_entities_analyzed:                 n,
      critical_principles_risk:                criticalCount,
      high_principles_risk:                    highCount,
      moderate_principles_risk:                moderateCount,
      low_principles_risk:                     lowCount,
      principles_crises_detected:              crisisCount,
      requires_intervention_count:             intervCount,
      avg_assumption_score:                    Math.round(tAssumption/n*10)/10,
      avg_rigidity_score:                      Math.round(tRigidity/n*10)/10,
      avg_blindspot_score:                     Math.round(tBlindspot/n*10)/10,
      avg_innovation_score:                    Math.round(tInnovation/n*10)/10,
      avg_estimated_principles_weakness_index: Math.round(avgComposite/100*10*100)/100,
    } as Record<string,unknown>));
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/first-principles-architecture-engine`)).json());
}
