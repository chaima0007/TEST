import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[bottleneck-sniper-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── hardcoded entities ────────────────────────────────────────────────────────
// BNS-001: EMEA, manufacturing_system  → critical,  critical_path_failure
// BNS-002: APAC, digital_service       → low,       none
// BNS-003: NOAM, supply_chain          → high,      wip_catastrophe
// BNS-004: LATAM, service_operation    → low,       none
// BNS-005: MEA,  government_process   → critical,  policy_constraint_dominance
// BNS-006: EMEA, retail_operation      → moderate,  none
// BNS-007: APAC, healthcare_system     → high,      cascade_starvation
// BNS-008: NOAM, financial_process     → critical,  market_constraint_crisis

const MOCK_ENTITIES = [
  {
    id: "BNS-001", region: "EMEA", system_type: "manufacturing_system",
    throughput_reduction_rate: 0.82, constraint_utilization_excess: 0.78,
    queue_accumulation_rate: 0.70, resource_starvation_index: 0.65,
    batch_size_mismatch: 0.55, variability_amplification: 0.68,
    dependency_chain_fragility: 0.72, capacity_imbalance_index: 0.60,
    wip_explosion_risk: 0.75, policy_constraint_density: 0.55,
    market_constraint_severity: 0.45, inventory_buffer_gaps: 0.70,
    protective_capacity_deficit: 0.65, constraint_exploitation_gap: 0.60,
    subordination_failure_rate: 0.50, elevation_difficulty_index: 0.55,
    constraint_migration_velocity: 0.40,
  },
  {
    id: "BNS-002", region: "APAC", system_type: "digital_service",
    throughput_reduction_rate: 0.05, constraint_utilization_excess: 0.08,
    queue_accumulation_rate: 0.06, resource_starvation_index: 0.04,
    batch_size_mismatch: 0.10, variability_amplification: 0.08,
    dependency_chain_fragility: 0.07, capacity_imbalance_index: 0.06,
    wip_explosion_risk: 0.05, policy_constraint_density: 0.09,
    market_constraint_severity: 0.05, inventory_buffer_gaps: 0.06,
    protective_capacity_deficit: 0.07, constraint_exploitation_gap: 0.08,
    subordination_failure_rate: 0.05, elevation_difficulty_index: 0.10,
    constraint_migration_velocity: 0.85,
  },
  {
    id: "BNS-003", region: "NOAM", system_type: "supply_chain",
    throughput_reduction_rate: 0.50, constraint_utilization_excess: 0.45,
    queue_accumulation_rate: 0.72, resource_starvation_index: 0.40,
    batch_size_mismatch: 0.45, variability_amplification: 0.50,
    dependency_chain_fragility: 0.42, capacity_imbalance_index: 0.38,
    wip_explosion_risk: 0.78, policy_constraint_density: 0.35,
    market_constraint_severity: 0.30, inventory_buffer_gaps: 0.45,
    protective_capacity_deficit: 0.42, constraint_exploitation_gap: 0.40,
    subordination_failure_rate: 0.35, elevation_difficulty_index: 0.38,
    constraint_migration_velocity: 0.45,
  },
  {
    id: "BNS-004", region: "LATAM", system_type: "service_operation",
    throughput_reduction_rate: 0.12, constraint_utilization_excess: 0.15,
    queue_accumulation_rate: 0.10, resource_starvation_index: 0.08,
    batch_size_mismatch: 0.18, variability_amplification: 0.14,
    dependency_chain_fragility: 0.12, capacity_imbalance_index: 0.10,
    wip_explosion_risk: 0.11, policy_constraint_density: 0.16,
    market_constraint_severity: 0.10, inventory_buffer_gaps: 0.12,
    protective_capacity_deficit: 0.14, constraint_exploitation_gap: 0.15,
    subordination_failure_rate: 0.10, elevation_difficulty_index: 0.18,
    constraint_migration_velocity: 0.75,
  },
  {
    id: "BNS-005", region: "MEA", system_type: "government_process",
    throughput_reduction_rate: 0.60, constraint_utilization_excess: 0.55,
    queue_accumulation_rate: 0.65, resource_starvation_index: 0.58,
    batch_size_mismatch: 0.50, variability_amplification: 0.62,
    dependency_chain_fragility: 0.65, capacity_imbalance_index: 0.55,
    wip_explosion_risk: 0.60, policy_constraint_density: 0.78,
    market_constraint_severity: 0.45, inventory_buffer_gaps: 0.60,
    protective_capacity_deficit: 0.65, constraint_exploitation_gap: 0.55,
    subordination_failure_rate: 0.72, elevation_difficulty_index: 0.60,
    constraint_migration_velocity: 0.30,
  },
  {
    id: "BNS-006", region: "EMEA", system_type: "retail_operation",
    throughput_reduction_rate: 0.28, constraint_utilization_excess: 0.30,
    queue_accumulation_rate: 0.25, resource_starvation_index: 0.22,
    batch_size_mismatch: 0.30, variability_amplification: 0.28,
    dependency_chain_fragility: 0.25, capacity_imbalance_index: 0.22,
    wip_explosion_risk: 0.25, policy_constraint_density: 0.30,
    market_constraint_severity: 0.22, inventory_buffer_gaps: 0.28,
    protective_capacity_deficit: 0.30, constraint_exploitation_gap: 0.28,
    subordination_failure_rate: 0.25, elevation_difficulty_index: 0.30,
    constraint_migration_velocity: 0.62,
  },
  {
    id: "BNS-007", region: "APAC", system_type: "healthcare_system",
    throughput_reduction_rate: 0.48, constraint_utilization_excess: 0.42,
    queue_accumulation_rate: 0.55, resource_starvation_index: 0.75,
    batch_size_mismatch: 0.45, variability_amplification: 0.50,
    dependency_chain_fragility: 0.70, capacity_imbalance_index: 0.40,
    wip_explosion_risk: 0.52, policy_constraint_density: 0.38,
    market_constraint_severity: 0.32, inventory_buffer_gaps: 0.48,
    protective_capacity_deficit: 0.52, constraint_exploitation_gap: 0.42,
    subordination_failure_rate: 0.38, elevation_difficulty_index: 0.45,
    constraint_migration_velocity: 0.40,
  },
  {
    id: "BNS-008", region: "NOAM", system_type: "financial_process",
    throughput_reduction_rate: 0.65, constraint_utilization_excess: 0.60,
    queue_accumulation_rate: 0.62, resource_starvation_index: 0.55,
    batch_size_mismatch: 0.52, variability_amplification: 0.65,
    dependency_chain_fragility: 0.68, capacity_imbalance_index: 0.58,
    wip_explosion_risk: 0.62, policy_constraint_density: 0.58,
    market_constraint_severity: 0.75, inventory_buffer_gaps: 0.62,
    protective_capacity_deficit: 0.68, constraint_exploitation_gap: 0.72,
    subordination_failure_rate: 0.55, elevation_difficulty_index: 0.60,
    constraint_migration_velocity: 0.32,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

// ── scoring ───────────────────────────────────────────────────────────────────

function flowScore(e: Entity): number {
  return (e.throughput_reduction_rate * 0.40 + e.queue_accumulation_rate * 0.35 + e.wip_explosion_risk * 0.25) * 100;
}
function constraintScore(e: Entity): number {
  return (e.constraint_utilization_excess * 0.40 + e.constraint_exploitation_gap * 0.35 + e.capacity_imbalance_index * 0.25) * 100;
}
function systemScore(e: Entity): number {
  return (e.dependency_chain_fragility * 0.40 + e.variability_amplification * 0.35 + e.policy_constraint_density * 0.25) * 100;
}
function resilienceScore(e: Entity): number {
  return (e.protective_capacity_deficit * 0.40 + e.inventory_buffer_gaps * 0.35 + e.resource_starvation_index * 0.25) * 100;
}
function compositeScore(fl: number, co: number, sy: number, re: number): number {
  return fl * 0.30 + co * 0.25 + sy * 0.25 + re * 0.20;
}
function round2(v: number): number { return Math.round(v * 100) / 100; }

function constraintRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}
function constraintPattern(e: Entity): string {
  if (e.throughput_reduction_rate >= 0.70 && e.constraint_utilization_excess >= 0.65) return "critical_path_failure";
  if (e.policy_constraint_density >= 0.70 && e.subordination_failure_rate >= 0.65)    return "policy_constraint_dominance";
  if (e.market_constraint_severity >= 0.70 && e.constraint_exploitation_gap >= 0.65)  return "market_constraint_crisis";
  if (e.wip_explosion_risk >= 0.70 && e.queue_accumulation_rate >= 0.65)              return "wip_catastrophe";
  if (e.resource_starvation_index >= 0.70 && e.dependency_chain_fragility >= 0.65)    return "cascade_starvation";
  return "none";
}
function constraintSeverity(comp: number): string {
  if (comp >= 75) return "system_halt";
  if (comp >= 50) return "critical_constraint";
  if (comp >= 25) return "constraint_building";
  return "flow_optimal";
}
function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "emergency_constraint_bypass";
  if (risk === "high" && pattern === "policy_constraint_dominance") return "policy_redesign";
  if (risk === "high") return "constraint_exploitation_program";
  if (risk === "moderate") return "bottleneck_monitoring";
  return "no_action";
}
function constraintSignal(e: Entity, pattern: string, comp: number): string {
  if (comp < 20) return "Flux système optimal — contraintes bien gérées, débit préservé, aucune intervention requise";
  const labels: Record<string, string> = {
    critical_path_failure:       "Défaillance du chemin critique",
    policy_constraint_dominance: "Dominance des contraintes de politique",
    market_constraint_crisis:    "Crise de contrainte marché",
    wip_catastrophe:             "Catastrophe WIP en cours",
    cascade_starvation:          "Carence en cascade détectée",
  };
  const label = labels[pattern] ?? pattern.replace(/_/g, " ");
  return `${label} — débit réduit ${Math.round(e.throughput_reduction_rate * 100)}% — WIP explosion ${Math.round(e.wip_explosion_risk * 100)}% — file d'attente ${Math.round(e.queue_accumulation_rate * 100)}% — composite ${Math.round(comp)}`;
}

function processEntity(e: Entity) {
  const fl   = round2(flowScore(e));
  const co   = round2(constraintScore(e));
  const sy   = round2(systemScore(e));
  const re   = round2(resilienceScore(e));
  const comp = round2(compositeScore(fl, co, sy, re));
  const risk    = constraintRisk(comp);
  const pattern = constraintPattern(e);
  const severity = constraintSeverity(comp);
  const action   = recommendedAction(risk, pattern);
  return {
    id:                        e.entity_id,
    region:                           e.region,
    system_type:                      e.system_type,
    constraint_risk:                  risk,
    constraint_pattern:               pattern,
    constraint_severity:              severity,
    recommended_action:               action,
    flow_score:                       fl,
    constraint_score:                 co,
    system_score:                     sy,
    resilience_score:                 re,
    constraint_composite:             comp,
    is_constraint_crisis:             comp >= 60,
    requires_constraint_intervention: comp >= 40,
    constraint_signal:                constraintSignal(e, pattern, comp),
  };
}

export async function GET() {
  if (!SWARM_API_URL) {
    return sealResponse(NextResponse.json({ error: "SWARM_API_URL not configured" }, { status: 502 }));
  }

  const entities = MOCK_ENTITIES.map(processEntity);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let tfl = 0, tco = 0, tsy = 0, tre = 0, tcomp = 0;
  let crisis_count = 0, intervention_count = 0;

  for (const r of entities) {
    risk_counts[r.constraint_risk]         = (risk_counts[r.constraint_risk]         || 0) + 1;
    pattern_counts[r.constraint_pattern]   = (pattern_counts[r.constraint_pattern]   || 0) + 1;
    severity_counts[r.constraint_severity] = (severity_counts[r.constraint_severity] || 0) + 1;
    action_counts[r.recommended_action]    = (action_counts[r.recommended_action]    || 0) + 1;
    tfl   += r.flow_score;
    tco   += r.constraint_score;
    tsy   += r.system_score;
    tre   += r.resilience_score;
    tcomp += r.constraint_composite;
    if (r.is_constraint_crisis)             crisis_count++;
    if (r.requires_constraint_intervention) intervention_count++;
  }

  const n = entities.length;

  // Dominant pattern (most frequent non-none)
  let dominant_pattern = "none";
  let maxCount = 0;
  for (const [k, v] of Object.entries(pattern_counts)) {
    if (k !== "none" && v > maxCount) { maxCount = v; dominant_pattern = k; }
  }

  const avg_composite = round2(tcomp / n);

  const summary = {
    total_entities:                 n,
    critical_count:                 risk_counts["critical"]  || 0,
    high_count:                     risk_counts["high"]      || 0,
    moderate_count:                 risk_counts["moderate"]  || 0,
    low_count:                      risk_counts["low"]       || 0,
    crisis_entities:                crisis_count,
    intervention_required:          intervention_count,
    dominant_pattern,
    risk_counts,
    pattern_counts,
    severity_counts,
    action_counts,
    avg_flow_score:                 round2(tfl   / n),
    avg_constraint_score:           round2(tco   / n),
    avg_system_score:               round2(tsy   / n),
    avg_resilience_score:           round2(tre   / n),
    avg_constraint_composite:       avg_composite,
    avg_estimated_constraint_index: round2(avg_composite / 100 * 10),
  };

  return sealResponse(NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>)));
}
