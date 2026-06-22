import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // ER-001 — critical, existential_cascade
  { id:"ER-001", risk_category:"civilizational_collapse", region:"GLOBAL",
    existential_exposure_score:0.92, continuity_plan_robustness:0.12, black_swan_preparedness:0.10,
    cascade_failure_vulnerability:0.88, civilizational_resilience_score:0.10, institutional_trust_erosion_rate:0.82,
    strategic_optionality_reserve:0.08, antifragility_score:0.09, early_warning_system_quality:0.08,
    societal_cohesion_index:0.10, technological_dependency_risk:0.85, resource_sovereignty_score:0.12,
    emergency_governance_readiness:0.08, knowledge_preservation_score:0.15, regenerative_recovery_capacity:0.10,
    strategic_redundancy_depth:0.08, existential_hedge_ratio:0.05 },
  // ER-002 — low, resilient
  { id:"ER-002", risk_category:"climate_tipping", region:"NAMER",
    existential_exposure_score:0.12, continuity_plan_robustness:0.92, black_swan_preparedness:0.90,
    cascade_failure_vulnerability:0.10, civilizational_resilience_score:0.92, institutional_trust_erosion_rate:0.08,
    strategic_optionality_reserve:0.90, antifragility_score:0.88, early_warning_system_quality:0.92,
    societal_cohesion_index:0.90, technological_dependency_risk:0.10, resource_sovereignty_score:0.92,
    emergency_governance_readiness:0.92, knowledge_preservation_score:0.90, regenerative_recovery_capacity:0.92,
    strategic_redundancy_depth:0.88, existential_hedge_ratio:0.90 },
  // ER-003 — high, institutional_collapse
  { id:"ER-003", risk_category:"democratic_erosion", region:"EMEA",
    existential_exposure_score:0.72, continuity_plan_robustness:0.30, black_swan_preparedness:0.35,
    cascade_failure_vulnerability:0.60, civilizational_resilience_score:0.32, institutional_trust_erosion_rate:0.78,
    strategic_optionality_reserve:0.28, antifragility_score:0.30, early_warning_system_quality:0.38,
    societal_cohesion_index:0.18, technological_dependency_risk:0.65, resource_sovereignty_score:0.30,
    emergency_governance_readiness:0.28, knowledge_preservation_score:0.38, regenerative_recovery_capacity:0.30,
    strategic_redundancy_depth:0.28, existential_hedge_ratio:0.22 },
  // ER-004 — low, high_alert (moderate composite but low risk label)
  { id:"ER-004", risk_category:"pandemics_biosecurity", region:"APAC",
    existential_exposure_score:0.20, continuity_plan_robustness:0.75, black_swan_preparedness:0.72,
    cascade_failure_vulnerability:0.18, civilizational_resilience_score:0.78, institutional_trust_erosion_rate:0.20,
    strategic_optionality_reserve:0.75, antifragility_score:0.72, early_warning_system_quality:0.78,
    societal_cohesion_index:0.75, technological_dependency_risk:0.20, resource_sovereignty_score:0.78,
    emergency_governance_readiness:0.80, knowledge_preservation_score:0.75, regenerative_recovery_capacity:0.78,
    strategic_redundancy_depth:0.70, existential_hedge_ratio:0.72 },
  // ER-005 — critical, black_swan_blindspot
  { id:"ER-005", risk_category:"ai_misalignment", region:"GLOBAL",
    existential_exposure_score:0.85, continuity_plan_robustness:0.20, black_swan_preparedness:0.08,
    cascade_failure_vulnerability:0.78, civilizational_resilience_score:0.22, institutional_trust_erosion_rate:0.62,
    strategic_optionality_reserve:0.18, antifragility_score:0.20, early_warning_system_quality:0.12,
    societal_cohesion_index:0.32, technological_dependency_risk:0.88, resource_sovereignty_score:0.18,
    emergency_governance_readiness:0.15, knowledge_preservation_score:0.28, regenerative_recovery_capacity:0.20,
    strategic_redundancy_depth:0.18, existential_hedge_ratio:0.10 },
  // ER-006 — moderate, none
  { id:"ER-006", risk_category:"financial_system_failure", region:"LATAM",
    existential_exposure_score:0.48, continuity_plan_robustness:0.55, black_swan_preparedness:0.52,
    cascade_failure_vulnerability:0.42, civilizational_resilience_score:0.52, institutional_trust_erosion_rate:0.42,
    strategic_optionality_reserve:0.50, antifragility_score:0.48, early_warning_system_quality:0.55,
    societal_cohesion_index:0.52, technological_dependency_risk:0.45, resource_sovereignty_score:0.52,
    emergency_governance_readiness:0.55, knowledge_preservation_score:0.52, regenerative_recovery_capacity:0.50,
    strategic_redundancy_depth:0.48, existential_hedge_ratio:0.50 },
  // ER-007 — high, civilizational_drift
  { id:"ER-007", risk_category:"technology_singularity", region:"EMEA",
    existential_exposure_score:0.68, continuity_plan_robustness:0.35, black_swan_preparedness:0.40,
    cascade_failure_vulnerability:0.58, civilizational_resilience_score:0.38, institutional_trust_erosion_rate:0.62,
    strategic_optionality_reserve:0.32, antifragility_score:0.35, early_warning_system_quality:0.42,
    societal_cohesion_index:0.35, technological_dependency_risk:0.72, resource_sovereignty_score:0.32,
    emergency_governance_readiness:0.38, knowledge_preservation_score:0.40, regenerative_recovery_capacity:0.35,
    strategic_redundancy_depth:0.32, existential_hedge_ratio:0.28 },
  // ER-008 — critical, continuity_failure
  { id:"ER-008", risk_category:"nuclear_risk", region:"MEA",
    existential_exposure_score:0.88, continuity_plan_robustness:0.08, black_swan_preparedness:0.18,
    cascade_failure_vulnerability:0.82, civilizational_resilience_score:0.15, institutional_trust_erosion_rate:0.72,
    strategic_optionality_reserve:0.10, antifragility_score:0.12, early_warning_system_quality:0.20,
    societal_cohesion_index:0.22, technological_dependency_risk:0.80, resource_sovereignty_score:0.12,
    emergency_governance_readiness:0.12, knowledge_preservation_score:0.10, regenerative_recovery_capacity:0.12,
    strategic_redundancy_depth:0.08, existential_hedge_ratio:0.08 },
];

type Entity = typeof MOCK_ENTITIES[0];

function exposureScore(e: Entity): number {
  const raw = (e.existential_exposure_score + e.cascade_failure_vulnerability + e.technological_dependency_risk) / 3.0;
  return Math.round(raw * 100 * 100) / 100;
}
function preparednessScore(e: Entity): number {
  const raw = ((1 - e.black_swan_preparedness) + (1 - e.early_warning_system_quality) + (1 - e.emergency_governance_readiness)) / 3.0;
  return Math.round(raw * 100 * 100) / 100;
}
function resilienceScore(e: Entity): number {
  const raw = ((1 - e.civilizational_resilience_score) + (1 - e.antifragility_score) + (1 - e.regenerative_recovery_capacity)) / 3.0;
  return Math.round(raw * 100 * 100) / 100;
}
function continuityScore(e: Entity): number {
  const raw = ((1 - e.continuity_plan_robustness) + (1 - e.strategic_redundancy_depth) + (1 - e.knowledge_preservation_score)) / 3.0;
  return Math.round(raw * 100 * 100) / 100;
}
function composite(exp: number, prep: number, res: number, cont: number): number {
  return Math.round((exp * 0.30 + prep * 0.25 + res * 0.25 + cont * 0.20) * 100) / 100;
}
function existentialPattern(e: Entity): string {
  if (e.existential_exposure_score >= 0.75 && e.cascade_failure_vulnerability >= 0.70) return "existential_cascade";
  if (e.institutional_trust_erosion_rate >= 0.70 && e.societal_cohesion_index <= 0.30) return "institutional_collapse";
  if (e.institutional_trust_erosion_rate >= 0.50 && e.societal_cohesion_index <= 0.50) return "civilizational_drift";
  if (e.black_swan_preparedness <= 0.25 && e.early_warning_system_quality <= 0.30) return "black_swan_blindspot";
  if (e.continuity_plan_robustness <= 0.25 && e.strategic_redundancy_depth <= 0.30) return "continuity_failure";
  return "none";
}
function riskLevel(comp: number): string {
  if (comp >= 65) return "critical";
  if (comp >= 45) return "high";
  if (comp >= 25) return "moderate";
  return "low";
}
function severity(comp: number): string {
  if (comp >= 65) return "existential";
  if (comp >= 45) return "critical_systemic";
  if (comp >= 25) return "high_alert";
  return "resilient";
}
function protocol(risk: string, pattern: string): string {
  if (risk === "critical") {
    if (pattern === "existential_cascade" || pattern === "black_swan_blindspot") return "existential_continuity_protocol";
    return "civilizational_hedge";
  }
  if (risk === "high") {
    if (pattern === "institutional_collapse" || pattern === "civilizational_drift") return "resilience_reinforcement";
    return "cascade_prevention";
  }
  if (risk === "moderate") return "existential_monitoring";
  return "no_action";
}
function signal(e: Entity, pattern: string, comp: number): string {
  const resilPct   = Math.round(e.civilizational_resilience_score * 100);
  const antifPct   = Math.round(e.antifragility_score * 100);
  const contPct    = Math.round(e.continuity_plan_robustness * 100);
  if (comp < 25) {
    return `Risque existentiel maîtrisé — résilience civilisationnelle ${resilPct}% — antifragilité ${antifPct}% — continuité stratégique ${contPct}%`;
  }
  const labels: Record<string,string> = {
    existential_cascade:    "Cascade existentielle",
    institutional_collapse: "Effondrement institutionnel",
    civilizational_drift:   "Dérive civilisationnelle",
    black_swan_blindspot:   "Angle mort cygne noir",
    continuity_failure:     "Défaillance continuité",
  };
  const label = labels[pattern] ?? pattern.replace(/_/g," ");
  return `${label} — exposition ${Math.round(e.existential_exposure_score*100)}% — vulnérabilité cascade ${Math.round(e.cascade_failure_vulnerability*100)}% — résilience ${resilPct}% — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[existential-risk-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tExp=0, tPrep=0, tRes=0, tCont=0, tComp=0, tEri=0, cascadeC=0, contC=0;
    for (const ent of entities) {
      rc[ent.existential_risk_level]  = (rc[ent.existential_risk_level]  || 0) + 1;
      pc[ent.existential_pattern]     = (pc[ent.existential_pattern]     || 0) + 1;
      sc[ent.systemic_severity]       = (sc[ent.systemic_severity]       || 0) + 1;
      ac[ent.recommended_protocol]    = (ac[ent.recommended_protocol]    || 0) + 1;
      tExp  += ent.exposure_score;
      tPrep += ent.preparedness_score;
      tRes  += ent.resilience_score;
      tCont += ent.continuity_score;
      tComp += ent.existential_composite;
      tEri  += ent.estimated_existential_risk_index;
      if (ent.has_cascade_signal)           cascadeC++;
      if (ent.requires_continuity_protocol) contC++;
    }
    const n = entities.length;
    const summary = {
      total:                                    n,
      risk_counts:                              rc,
      pattern_counts:                           pc,
      severity_counts:                          sc,
      protocol_counts:                          ac,
      avg_existential_composite:                Math.round(tComp / n * 10) / 10,
      cascade_signal_count:                     cascadeC,
      continuity_protocol_required_count:       contC,
      avg_exposure_score:                       Math.round(tExp / n * 10) / 10,
      avg_preparedness_score:                   Math.round(tPrep / n * 10) / 10,
      avg_resilience_score:                     Math.round(tRes / n * 10) / 10,
      avg_continuity_score:                     Math.round(tCont / n * 10) / 10,
      avg_estimated_existential_risk_index:     Math.round(tEri / n * 100) / 100,
    };
    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "existential-risk-engine")));
  }
  return sealResponse(NextResponse.json(sealResponse(
    await (await fetch(`${process.env.SWARM_API_URL}/existential-risk-engine`, { next: { revalidate: 30 } })).json(),
    "existential-risk-engine"
  )));
}
