import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // MBM-001: critical, metamorphic_stall
  { entity_id:"MBM-001", transformation_stage:"identity_dissolution", region:"EMEA",
    transformation_velocity:0.22, identity_coherence_score:0.25, legacy_anchor_risk:0.75,
    new_capability_readiness:0.22, revenue_model_clarity:0.20, stakeholder_change_tolerance:0.55,
    cultural_transformation_depth:0.18, innovation_pipeline_richness:0.22, organizational_grief_processing:0.28,
    transformation_leadership_strength:0.22, change_momentum_score:0.22, resistance_to_change_index:0.72,
    ecosystem_partner_alignment:0.55, customer_migration_readiness:0.55, financial_runway_adequacy:0.22,
    metamorphic_vision_clarity:0.20, post_transformation_market_fit:0.15 },
  // MBM-002: low, metamorphosed, none
  { entity_id:"MBM-002", transformation_stage:"culture_metamorphosis", region:"NAMER",
    transformation_velocity:0.90, identity_coherence_score:0.90, legacy_anchor_risk:0.15,
    new_capability_readiness:0.90, revenue_model_clarity:0.92, stakeholder_change_tolerance:0.90,
    cultural_transformation_depth:0.88, innovation_pipeline_richness:0.90, organizational_grief_processing:0.85,
    transformation_leadership_strength:0.90, change_momentum_score:0.90, resistance_to_change_index:0.15,
    ecosystem_partner_alignment:0.90, customer_migration_readiness:0.90, financial_runway_adequacy:0.90,
    metamorphic_vision_clarity:0.92, post_transformation_market_fit:0.88 },
  // MBM-003: high, identity_crisis
  { entity_id:"MBM-003", transformation_stage:"chrysalis_phase", region:"APAC",
    transformation_velocity:0.35, identity_coherence_score:0.22, legacy_anchor_risk:0.55,
    new_capability_readiness:0.35, revenue_model_clarity:0.40, stakeholder_change_tolerance:0.35,
    cultural_transformation_depth:0.32, innovation_pipeline_richness:0.35, organizational_grief_processing:0.38,
    transformation_leadership_strength:0.35, change_momentum_score:0.35, resistance_to_change_index:0.55,
    ecosystem_partner_alignment:0.35, customer_migration_readiness:0.35, financial_runway_adequacy:0.35,
    metamorphic_vision_clarity:0.40, post_transformation_market_fit:0.30 },
  // MBM-004: low, metamorphosed, none
  { entity_id:"MBM-004", transformation_stage:"capability_reconfiguration", region:"LATAM",
    transformation_velocity:0.70, identity_coherence_score:0.72, legacy_anchor_risk:0.28,
    new_capability_readiness:0.70, revenue_model_clarity:0.68, stakeholder_change_tolerance:0.72,
    cultural_transformation_depth:0.65, innovation_pipeline_richness:0.70, organizational_grief_processing:0.68,
    transformation_leadership_strength:0.70, change_momentum_score:0.72, resistance_to_change_index:0.28,
    ecosystem_partner_alignment:0.70, customer_migration_readiness:0.70, financial_runway_adequacy:0.70,
    metamorphic_vision_clarity:0.72, post_transformation_market_fit:0.68 },
  // MBM-005: critical, capability_gap
  { entity_id:"MBM-005", transformation_stage:"revenue_model_pivot", region:"EMEA",
    transformation_velocity:0.22, identity_coherence_score:0.55, legacy_anchor_risk:0.60,
    new_capability_readiness:0.22, revenue_model_clarity:0.18, stakeholder_change_tolerance:0.55,
    cultural_transformation_depth:0.20, innovation_pipeline_richness:0.22, organizational_grief_processing:0.25,
    transformation_leadership_strength:0.22, change_momentum_score:0.22, resistance_to_change_index:0.60,
    ecosystem_partner_alignment:0.55, customer_migration_readiness:0.55, financial_runway_adequacy:0.22,
    metamorphic_vision_clarity:0.30, post_transformation_market_fit:0.20 },
  // MBM-006: moderate, none
  { entity_id:"MBM-006", transformation_stage:"ecosystem_reposition", region:"NAMER",
    transformation_velocity:0.55, identity_coherence_score:0.55, legacy_anchor_risk:0.52,
    new_capability_readiness:0.55, revenue_model_clarity:0.58, stakeholder_change_tolerance:0.55,
    cultural_transformation_depth:0.52, innovation_pipeline_richness:0.55, organizational_grief_processing:0.50,
    transformation_leadership_strength:0.55, change_momentum_score:0.55, resistance_to_change_index:0.52,
    ecosystem_partner_alignment:0.55, customer_migration_readiness:0.55, financial_runway_adequacy:0.55,
    metamorphic_vision_clarity:0.55, post_transformation_market_fit:0.52 },
  // MBM-007: high, ecosystem_rejection
  { entity_id:"MBM-007", transformation_stage:"value_proposition_reinvention", region:"APAC",
    transformation_velocity:0.40, identity_coherence_score:0.55, legacy_anchor_risk:0.55,
    new_capability_readiness:0.40, revenue_model_clarity:0.45, stakeholder_change_tolerance:0.55,
    cultural_transformation_depth:0.38, innovation_pipeline_richness:0.40, organizational_grief_processing:0.42,
    transformation_leadership_strength:0.40, change_momentum_score:0.40, resistance_to_change_index:0.55,
    ecosystem_partner_alignment:0.22, customer_migration_readiness:0.28, financial_runway_adequacy:0.40,
    metamorphic_vision_clarity:0.45, post_transformation_market_fit:0.35 },
  // MBM-008: critical, vision_collapse
  { entity_id:"MBM-008", transformation_stage:"stakeholder_realignment", region:"MEA",
    transformation_velocity:0.22, identity_coherence_score:0.55, legacy_anchor_risk:0.72,
    new_capability_readiness:0.22, revenue_model_clarity:0.18, stakeholder_change_tolerance:0.45,
    cultural_transformation_depth:0.20, innovation_pipeline_richness:0.55, organizational_grief_processing:0.25,
    transformation_leadership_strength:0.22, change_momentum_score:0.40, resistance_to_change_index:0.60,
    ecosystem_partner_alignment:0.45, customer_migration_readiness:0.45, financial_runway_adequacy:0.22,
    metamorphic_vision_clarity:0.22, post_transformation_market_fit:0.18 },
];

type Entity = typeof MOCK_ENTITIES[0];

function stagnationScore(e: Entity): number {
  let s = 0;
  if      (e.legacy_anchor_risk >= 0.70) s += 40; else if (e.legacy_anchor_risk >= 0.50) s += 22; else if (e.legacy_anchor_risk >= 0.35) s += 8;
  if      (e.resistance_to_change_index >= 0.70) s += 35; else if (e.resistance_to_change_index >= 0.50) s += 18; else if (e.resistance_to_change_index >= 0.35) s += 6;
  if      (e.identity_coherence_score <= 0.30) s += 25; else if (e.identity_coherence_score <= 0.50) s += 12;
  return Math.min(s, 100);
}

function readinessScore(e: Entity): number {
  let s = 0;
  if      (e.new_capability_readiness <= 0.30) s += 40; else if (e.new_capability_readiness <= 0.50) s += 22; else if (e.new_capability_readiness <= 0.65) s += 8;
  if      (e.transformation_leadership_strength <= 0.30) s += 35; else if (e.transformation_leadership_strength <= 0.50) s += 18; else if (e.transformation_leadership_strength <= 0.65) s += 6;
  if      (e.financial_runway_adequacy <= 0.30) s += 25; else if (e.financial_runway_adequacy <= 0.50) s += 12;
  return Math.min(s, 100);
}

function momentumScore(e: Entity): number {
  let s = 0;
  if      (e.change_momentum_score <= 0.30) s += 40; else if (e.change_momentum_score <= 0.50) s += 22; else if (e.change_momentum_score <= 0.65) s += 8;
  if      (e.transformation_velocity <= 0.30) s += 35; else if (e.transformation_velocity <= 0.50) s += 18; else if (e.transformation_velocity <= 0.65) s += 6;
  if      (e.innovation_pipeline_richness <= 0.30) s += 25; else if (e.innovation_pipeline_richness <= 0.50) s += 12;
  return Math.min(s, 100);
}

function alignmentScore(e: Entity): number {
  let s = 0;
  if      (e.ecosystem_partner_alignment <= 0.30) s += 40; else if (e.ecosystem_partner_alignment <= 0.50) s += 22; else if (e.ecosystem_partner_alignment <= 0.65) s += 8;
  if      (e.customer_migration_readiness <= 0.30) s += 35; else if (e.customer_migration_readiness <= 0.50) s += 18; else if (e.customer_migration_readiness <= 0.65) s += 6;
  if      (e.stakeholder_change_tolerance <= 0.30) s += 25; else if (e.stakeholder_change_tolerance <= 0.50) s += 12;
  return Math.min(s, 100);
}

function composite(stag: number, read: number, mom: number, align: number): number {
  return Math.min(Math.round((stag * 0.30 + read * 0.25 + mom * 0.25 + align * 0.20) * 100) / 100, 100);
}

function metamorphicPattern(e: Entity): string {
  if (e.legacy_anchor_risk >= 0.65 && e.change_momentum_score <= 0.35) return "metamorphic_stall";
  if (e.identity_coherence_score <= 0.30 || (e.resistance_to_change_index >= 0.65 && e.metamorphic_vision_clarity <= 0.35)) return "identity_crisis";
  if (e.new_capability_readiness <= 0.30 && e.innovation_pipeline_richness <= 0.35) return "capability_gap";
  if (e.ecosystem_partner_alignment <= 0.30 && e.customer_migration_readiness <= 0.35) return "ecosystem_rejection";
  if (e.metamorphic_vision_clarity <= 0.25 && e.transformation_leadership_strength <= 0.35) return "vision_collapse";
  return "none";
}

function transformationRisk(c: number): string {
  if (c >= 60) return "critical";
  if (c >= 40) return "high";
  if (c >= 20) return "moderate";
  return "low";
}

function transformationSeverity(c: number): string {
  if (c >= 60) return "fossilized";
  if (c >= 40) return "transitioning";
  if (c >= 20) return "morphing";
  return "metamorphosed";
}

function recommendedAction(r: string, p: string): string {
  if (r === "critical") {
    if (p === "metamorphic_stall") return "transformation_emergency";
    return "identity_reconstruction";
  }
  if (r === "high") {
    if (p === "capability_gap") return "capability_sprint";
    return "ecosystem_rebuild";
  }
  if (r === "moderate") return "transformation_monitoring";
  return "no_action";
}

function transformationSignal(e: Entity, pat: string, comp: number): string {
  if (comp < 20) return "Métamorphose accomplie — modèle d'affaires réinventé, transformation intégrée, alignement écosystémique confirmé";
  const labels: Record<string, string> = {
    metamorphic_stall: "Stagnation métamorphique",
    identity_crisis: "Crise identitaire",
    capability_gap: "Déficit capacitaire",
    ecosystem_rejection: "Rejet écosystémique",
    vision_collapse: "Effondrement visionnaire",
    none: "Transformation en cours",
  };
  const label = labels[pat] ?? pat.replace(/_/g, " ");
  return `${label} — vélocité ${e.transformation_velocity.toFixed(2)} — vision ${Math.round(e.metamorphic_vision_clarity * 100)}% — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const stag = stagnationScore(e), read = readinessScore(e), mom = momentumScore(e), align = alignmentScore(e);
      const comp = composite(stag, read, mom, align);
      const pat = metamorphicPattern(e), risk = transformationRisk(comp), sev = transformationSeverity(comp), act = recommendedAction(risk, pat);
      return {
        entity_id: e.entity_id, region: e.region, transformation_stage: e.transformation_stage,
        transformation_risk: risk, metamorphic_pattern: pat, transformation_severity: sev, recommended_action: act,
        stagnation_score: stag, readiness_score: read, momentum_score: mom, alignment_score: align,
        transformation_composite: comp,
        is_in_metamorphic_crisis: comp >= 40 || e.legacy_anchor_risk >= 0.60 || e.resistance_to_change_index >= 0.60 || e.metamorphic_vision_clarity <= 0.25,
        requires_immediate_intervention: comp >= 25 || e.transformation_leadership_strength <= 0.30 || e.financial_runway_adequacy <= 0.30 || e.post_transformation_market_fit <= 0.25,
        transformation_signal: transformationSignal(e, pat, comp),
      };
    });
    const rc: Record<string, number> = {}, pc: Record<string, number> = {}, sc: Record<string, number> = {}, ac: Record<string, number> = {};
    let tcomp = 0, tstag = 0, tread = 0, tmom = 0, talign = 0, tridx = 0, crisisC = 0, interventionC = 0;
    for (const ent of entities) {
      rc[ent.transformation_risk] = (rc[ent.transformation_risk] || 0) + 1;
      pc[ent.metamorphic_pattern] = (pc[ent.metamorphic_pattern] || 0) + 1;
      sc[ent.transformation_severity] = (sc[ent.transformation_severity] || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tcomp += ent.transformation_composite; tstag += ent.stagnation_score; tread += ent.readiness_score;
      tmom += ent.momentum_score; talign += ent.alignment_score;
      if (ent.is_in_metamorphic_crisis) crisisC++;
      if (ent.requires_immediate_intervention) interventionC++;
    }
    for (const [idx, ent] of entities.entries()) {
      const pmf = MOCK_ENTITIES[idx].post_transformation_market_fit;
      tridx += Math.min(Math.round(ent.transformation_composite / 100 * (1 - pmf + 0.01) * 10 * 100) / 100, 10.0);
    }
    const n = entities.length;
    return NextResponse.json(sealResponse({
      entities,
      summary: {
        total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
        avg_transformation_composite: Math.round(tcomp / n * 10) / 10,
        metamorphic_crisis_count: crisisC,
        immediate_intervention_count: interventionC,
        avg_stagnation_score: Math.round(tstag / n * 10) / 10,
        avg_readiness_score: Math.round(tread / n * 10) / 10,
        avg_momentum_score: Math.round(tmom / n * 10) / 10,
        avg_alignment_score: Math.round(talign / n * 10) / 10,
        avg_estimated_transformation_risk_index: Math.round(tridx / n * 100) / 100,
      },
    }, "metamorphic-business-model-engine"));
  }
  return NextResponse.json(sealResponse(
    await (await fetch(`${process.env.SWARM_API_URL}/metamorphic-business-model-engine`)).json(),
    "metamorphic-business-model-engine"
  ));
}
