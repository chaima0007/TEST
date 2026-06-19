import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── Mock entities ──────────────────────────────────────────────────────────────
// 8 entities covering all patterns and risk levels as specified in Module 351.

const MOCK_ENTITIES = [
  // IRE-001 — critical, cascading_infrastructure_collapse
  // cascading_failure_interconnection_risk>=0.70 AND cross_sector_dependency_fragility>=0.65
  // composite >= 60 → critical
  {
    entity_id: "IRE-001", infrastructure_type: "power_grid", region: "NOAM",
    aging_infrastructure_deterioration_rate: 0.80,
    cascading_failure_interconnection_risk: 0.88,
    cyber_physical_attack_vulnerability: 0.72,
    climate_infrastructure_stress_index: 0.65,
    single_point_failure_density: 0.75,
    maintenance_investment_deficit: 0.78,
    emergency_response_capacity_gap: 0.70,
    backup_redundancy_inadequacy: 0.68,
    private_infrastructure_owner_underinvestment: 0.72,
    cross_sector_dependency_fragility: 0.82,
    extreme_weather_infrastructure_exposure: 0.65,
    infrastructure_workforce_shortage: 0.68,
    regulatory_enforcement_gap: 0.65,
    geopolitical_infrastructure_targeting_risk: 0.60,
    smart_infrastructure_vulnerability: 0.58,
    underground_infrastructure_neglect: 0.75,
    critical_node_attack_surface: 0.70,
  },
  // IRE-002 — low, no pattern (none)
  // composite < 20 → low
  {
    entity_id: "IRE-002", infrastructure_type: "water_treatment", region: "EMEA",
    aging_infrastructure_deterioration_rate: 0.10,
    cascading_failure_interconnection_risk: 0.08,
    cyber_physical_attack_vulnerability: 0.10,
    climate_infrastructure_stress_index: 0.08,
    single_point_failure_density: 0.10,
    maintenance_investment_deficit: 0.08,
    emergency_response_capacity_gap: 0.10,
    backup_redundancy_inadequacy: 0.08,
    private_infrastructure_owner_underinvestment: 0.10,
    cross_sector_dependency_fragility: 0.08,
    extreme_weather_infrastructure_exposure: 0.10,
    infrastructure_workforce_shortage: 0.08,
    regulatory_enforcement_gap: 0.10,
    geopolitical_infrastructure_targeting_risk: 0.08,
    smart_infrastructure_vulnerability: 0.10,
    underground_infrastructure_neglect: 0.08,
    critical_node_attack_surface: 0.10,
  },
  // IRE-003 — high, aging_critical_failure
  // aging_infrastructure_deterioration_rate>=0.70 AND maintenance_investment_deficit>=0.65
  // cascading pattern must NOT fire: cascading_failure_interconnection_risk<0.70 OR cross_sector_dependency_fragility<0.65
  // composite >= 40 and < 60 → high
  {
    entity_id: "IRE-003", infrastructure_type: "transport_network", region: "EMEA",
    aging_infrastructure_deterioration_rate: 0.82,
    cascading_failure_interconnection_risk: 0.50,
    cyber_physical_attack_vulnerability: 0.42,
    climate_infrastructure_stress_index: 0.45,
    single_point_failure_density: 0.48,
    maintenance_investment_deficit: 0.78,
    emergency_response_capacity_gap: 0.40,
    backup_redundancy_inadequacy: 0.38,
    private_infrastructure_owner_underinvestment: 0.45,
    cross_sector_dependency_fragility: 0.42,
    extreme_weather_infrastructure_exposure: 0.45,
    infrastructure_workforce_shortage: 0.40,
    regulatory_enforcement_gap: 0.42,
    geopolitical_infrastructure_targeting_risk: 0.38,
    smart_infrastructure_vulnerability: 0.40,
    underground_infrastructure_neglect: 0.72,
    critical_node_attack_surface: 0.45,
  },
  // IRE-004 — low, no pattern (none)
  // composite < 20 → low
  {
    entity_id: "IRE-004", infrastructure_type: "telecommunications", region: "APAC",
    aging_infrastructure_deterioration_rate: 0.12,
    cascading_failure_interconnection_risk: 0.10,
    cyber_physical_attack_vulnerability: 0.12,
    climate_infrastructure_stress_index: 0.10,
    single_point_failure_density: 0.12,
    maintenance_investment_deficit: 0.10,
    emergency_response_capacity_gap: 0.12,
    backup_redundancy_inadequacy: 0.10,
    private_infrastructure_owner_underinvestment: 0.12,
    cross_sector_dependency_fragility: 0.10,
    extreme_weather_infrastructure_exposure: 0.12,
    infrastructure_workforce_shortage: 0.10,
    regulatory_enforcement_gap: 0.12,
    geopolitical_infrastructure_targeting_risk: 0.10,
    smart_infrastructure_vulnerability: 0.12,
    underground_infrastructure_neglect: 0.10,
    critical_node_attack_surface: 0.12,
  },
  // IRE-005 — critical, cyber_physical_attack
  // cyber_physical_attack_vulnerability>=0.70 AND smart_infrastructure_vulnerability>=0.65
  // cascading pattern NOT fired: cascading_failure_interconnection_risk<0.70 OR cross_sector_dependency_fragility<0.65
  // aging pattern NOT fired: aging_infrastructure_deterioration_rate<0.70 OR maintenance_investment_deficit<0.65
  // composite >= 60 → critical
  {
    entity_id: "IRE-005", infrastructure_type: "smart_grid", region: "NOAM",
    aging_infrastructure_deterioration_rate: 0.55,
    cascading_failure_interconnection_risk: 0.60,
    cyber_physical_attack_vulnerability: 0.88,
    climate_infrastructure_stress_index: 0.55,
    single_point_failure_density: 0.65,
    maintenance_investment_deficit: 0.58,
    emergency_response_capacity_gap: 0.72,
    backup_redundancy_inadequacy: 0.68,
    private_infrastructure_owner_underinvestment: 0.65,
    cross_sector_dependency_fragility: 0.55,
    extreme_weather_infrastructure_exposure: 0.58,
    infrastructure_workforce_shortage: 0.65,
    regulatory_enforcement_gap: 0.70,
    geopolitical_infrastructure_targeting_risk: 0.78,
    smart_infrastructure_vulnerability: 0.82,
    underground_infrastructure_neglect: 0.55,
    critical_node_attack_surface: 0.80,
  },
  // IRE-006 — moderate, no pattern (none)
  // composite >= 20 and < 40 → moderate
  {
    entity_id: "IRE-006", infrastructure_type: "water_distribution", region: "LATAM",
    aging_infrastructure_deterioration_rate: 0.32,
    cascading_failure_interconnection_risk: 0.30,
    cyber_physical_attack_vulnerability: 0.32,
    climate_infrastructure_stress_index: 0.30,
    single_point_failure_density: 0.32,
    maintenance_investment_deficit: 0.28,
    emergency_response_capacity_gap: 0.32,
    backup_redundancy_inadequacy: 0.28,
    private_infrastructure_owner_underinvestment: 0.30,
    cross_sector_dependency_fragility: 0.28,
    extreme_weather_infrastructure_exposure: 0.32,
    infrastructure_workforce_shortage: 0.30,
    regulatory_enforcement_gap: 0.28,
    geopolitical_infrastructure_targeting_risk: 0.30,
    smart_infrastructure_vulnerability: 0.28,
    underground_infrastructure_neglect: 0.32,
    critical_node_attack_surface: 0.30,
  },
  // IRE-007 — high, climate_infrastructure_shock
  // climate_infrastructure_stress_index>=0.70 AND extreme_weather_infrastructure_exposure>=0.65
  // cascading pattern NOT fired: cascading_failure_interconnection_risk<0.70 OR cross_sector_dependency_fragility<0.65
  // aging pattern NOT fired: aging_infrastructure_deterioration_rate<0.70 OR maintenance_investment_deficit<0.65
  // cyber pattern NOT fired: cyber_physical_attack_vulnerability<0.70 OR smart_infrastructure_vulnerability<0.65
  // composite >= 40 and < 60 → high
  {
    entity_id: "IRE-007", infrastructure_type: "coastal_infrastructure", region: "APAC",
    aging_infrastructure_deterioration_rate: 0.50,
    cascading_failure_interconnection_risk: 0.48,
    cyber_physical_attack_vulnerability: 0.42,
    climate_infrastructure_stress_index: 0.82,
    single_point_failure_density: 0.50,
    maintenance_investment_deficit: 0.55,
    emergency_response_capacity_gap: 0.48,
    backup_redundancy_inadequacy: 0.42,
    private_infrastructure_owner_underinvestment: 0.50,
    cross_sector_dependency_fragility: 0.48,
    extreme_weather_infrastructure_exposure: 0.78,
    infrastructure_workforce_shortage: 0.45,
    regulatory_enforcement_gap: 0.48,
    geopolitical_infrastructure_targeting_risk: 0.42,
    smart_infrastructure_vulnerability: 0.40,
    underground_infrastructure_neglect: 0.48,
    critical_node_attack_surface: 0.45,
  },
  // IRE-008 — critical, resilience_vacuum
  // backup_redundancy_inadequacy>=0.70 AND emergency_response_capacity_gap>=0.65
  // cascading pattern NOT fired: cascading_failure_interconnection_risk<0.70 OR cross_sector_dependency_fragility<0.65
  // aging pattern NOT fired: aging_infrastructure_deterioration_rate<0.70 OR maintenance_investment_deficit<0.65
  // cyber pattern NOT fired: cyber_physical_attack_vulnerability<0.70 OR smart_infrastructure_vulnerability<0.65
  // climate pattern NOT fired: climate_infrastructure_stress_index<0.70 OR extreme_weather_infrastructure_exposure<0.65
  // composite >= 60 → critical
  {
    entity_id: "IRE-008", infrastructure_type: "emergency_systems", region: "MEA",
    aging_infrastructure_deterioration_rate: 0.60,
    cascading_failure_interconnection_risk: 0.58,
    cyber_physical_attack_vulnerability: 0.62,
    climate_infrastructure_stress_index: 0.60,
    single_point_failure_density: 0.72,
    maintenance_investment_deficit: 0.62,
    emergency_response_capacity_gap: 0.85,
    backup_redundancy_inadequacy: 0.88,
    private_infrastructure_owner_underinvestment: 0.75,
    cross_sector_dependency_fragility: 0.58,
    extreme_weather_infrastructure_exposure: 0.60,
    infrastructure_workforce_shortage: 0.78,
    regulatory_enforcement_gap: 0.65,
    geopolitical_infrastructure_targeting_risk: 0.62,
    smart_infrastructure_vulnerability: 0.60,
    underground_infrastructure_neglect: 0.68,
    critical_node_attack_surface: 0.72,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

// ── Scoring functions (mirrors Python engine exactly) ──────────────────────────

function physicalScore(e: Entity): number {
  const raw = (
    e.aging_infrastructure_deterioration_rate * 0.4
    + e.maintenance_investment_deficit * 0.35
    + e.underground_infrastructure_neglect * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function cascadeScore(e: Entity): number {
  const raw = (
    e.cascading_failure_interconnection_risk * 0.4
    + e.cross_sector_dependency_fragility * 0.35
    + e.single_point_failure_density * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function threatScore(e: Entity): number {
  const raw = (
    e.cyber_physical_attack_vulnerability * 0.4
    + e.geopolitical_infrastructure_targeting_risk * 0.35
    + e.smart_infrastructure_vulnerability * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function resilienceScore(e: Entity): number {
  const raw = (
    e.backup_redundancy_inadequacy * 0.4
    + e.emergency_response_capacity_gap * 0.35
    + e.infrastructure_workforce_shortage * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(phys: number, casc: number, thrt: number, resil: number): number {
  return Math.round((phys * 0.30 + casc * 0.25 + thrt * 0.25 + resil * 0.20) * 100) / 100;
}

function infraPattern(e: Entity): string {
  if (e.cascading_failure_interconnection_risk >= 0.70 && e.cross_sector_dependency_fragility >= 0.65)
    return "cascading_infrastructure_collapse";
  if (e.aging_infrastructure_deterioration_rate >= 0.70 && e.maintenance_investment_deficit >= 0.65)
    return "aging_critical_failure";
  if (e.cyber_physical_attack_vulnerability >= 0.70 && e.smart_infrastructure_vulnerability >= 0.65)
    return "cyber_physical_attack";
  if (e.climate_infrastructure_stress_index >= 0.70 && e.extreme_weather_infrastructure_exposure >= 0.65)
    return "climate_infrastructure_shock";
  if (e.backup_redundancy_inadequacy >= 0.70 && e.emergency_response_capacity_gap >= 0.65)
    return "resilience_vacuum";
  return "none";
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function severity(comp: number): string {
  if (comp >= 60) return "effondrement_infrastructure_critique";
  if (comp >= 40) return "crise_résilience_systémique";
  if (comp >= 20) return "fragilité_infrastructure_structurelle";
  return "infrastructure_sous_surveillance";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "réparation_urgente_infrastructure_critique";
  if (risk === "high") return "plan_résilience_infrastructure_accéléré";
  if (risk === "moderate") return "renforcement_redondance_systémique";
  return "veille_infrastructure_critique_continue";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Effondrement infrastructure critique — défaillance systémique imminente";
  if (risk === "high") return "🟠 Crise résilience systémique détectée";
  if (risk === "moderate") return "🟡 Fragilité infrastructure structurelle active";
  return "🟢 Infrastructure critique sous surveillance";
}

// ── GET handler ────────────────────────────────────────────────────────────────

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const phys  = physicalScore(e);
      const casc  = cascadeScore(e);
      const thrt  = threatScore(e);
      const resil = resilienceScore(e);
      const comp  = compositeScore(phys, casc, thrt, resil);
      const pat   = infraPattern(e);
      const risk  = riskLevel(comp);
      const sev   = severity(comp);
      const act   = recommendedAction(risk);
      const sig   = signal(risk);

      return {
        entity_id:                              e.entity_id,
        infrastructure_type:                    e.infrastructure_type,
        region:                                 e.region,
        physical_score:                         phys,
        cascade_score:                          casc,
        threat_score:                           thrt,
        resilience_score:                       resil,
        composite_score:                        comp,
        risk_level:                             risk,
        infra_pattern:                          pat,
        severity:                               sev,
        recommended_action:                     act,
        signal:                                 sig,
        aging_infrastructure_deterioration_rate: e.aging_infrastructure_deterioration_rate,
        cascading_failure_interconnection_risk:  e.cascading_failure_interconnection_risk,
      };
    });

    const riskDist: Record<string, number> = {};
    const patDist: Record<string, number> = {};
    const sevDist: Record<string, number> = {};
    const actDist: Record<string, number> = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      riskDist[ent.risk_level]        = (riskDist[ent.risk_level]        || 0) + 1;
      patDist[ent.infra_pattern]      = (patDist[ent.infra_pattern]      || 0) + 1;
      sevDist[ent.severity]           = (sevDist[ent.severity]           || 0) + 1;
      actDist[ent.recommended_action] = (actDist[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;
    const summary = {
      module_id:                     351,
      module_name:                   "Infrastructure Resilience & Critical System Failure Intelligence Engine",
      total_entities:                n,
      critical_count:                criticalCount,
      high_count:                    highCount,
      moderate_count:                moderateCount,
      low_count:                     lowCount,
      avg_composite:                 avgComposite,
      pattern_distribution:          patDist,
      risk_distribution:             riskDist,
      severity_distribution:         sevDist,
      action_distribution:           actDist,
      avg_estimated_infra_risk_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary }, "infrastructure-resilience-engine") as Record<string, unknown>
    );
  }

  try {
    const upstream = await fetch(`${SWARM_API_URL}/infrastructure-resilience-engine`);
    const data = await upstream.json();
    return NextResponse.json(
      sealResponse(data, "infrastructure-resilience-engine") as Record<string, unknown>
    );
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream infrastructure resilience engine unavailable" }, "infrastructure-resilience-engine") as Record<string, unknown>,
      { status: 502 }
    );
  }
}
