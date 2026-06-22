import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// Mock entities for Module 295: Longevity Economy & Silver Intelligence Engine
// Designed to produce specific risk/pattern outcomes per entity spec.
const MOCK_ENTITIES = [
  // LE-001: EMEA, pension_management → critical, pension_collapse
  {
    id: "LE-001", longevity_segment: "pension_management", region: "EMEA",
    aging_population_rate: 0.80, longevity_biotech_adoption: 0.30, silver_spending_power: 0.30,
    intergenerational_wealth_transfer_rate: 0.40, pension_system_stress: 0.82,
    healthcare_cost_inflation: 0.60, productive_aging_index: 0.30,
    cognitive_decline_risk: 0.55, eldercare_infrastructure_gap: 0.55,
    longevity_financial_products_penetration: 0.30, age_discrimination_index: 0.50,
    social_isolation_risk: 0.55, multigenerational_workforce_integration: 0.30,
    longevity_insurance_penetration: 0.30, retirement_adequacy_gap: 0.75,
    silver_digital_inclusion: 0.40, geroscience_readiness: 0.25,
  },
  // LE-002: APAC, longevity_biotech → low, longevity_thriving / none
  {
    id: "LE-002", longevity_segment: "longevity_biotech", region: "APAC",
    aging_population_rate: 0.15, longevity_biotech_adoption: 0.88, silver_spending_power: 0.85,
    intergenerational_wealth_transfer_rate: 0.82, pension_system_stress: 0.12,
    healthcare_cost_inflation: 0.12, productive_aging_index: 0.88,
    cognitive_decline_risk: 0.12, eldercare_infrastructure_gap: 0.12,
    longevity_financial_products_penetration: 0.88, age_discrimination_index: 0.12,
    social_isolation_risk: 0.12, multigenerational_workforce_integration: 0.88,
    longevity_insurance_penetration: 0.88, retirement_adequacy_gap: 0.10,
    silver_digital_inclusion: 0.90, geroscience_readiness: 0.90,
  },
  // LE-003: NOAM, eldercare_services → high, healthcare_cost_spiral
  {
    id: "LE-003", longevity_segment: "eldercare_services", region: "NOAM",
    aging_population_rate: 0.55, longevity_biotech_adoption: 0.42, silver_spending_power: 0.50,
    intergenerational_wealth_transfer_rate: 0.50, pension_system_stress: 0.48,
    healthcare_cost_inflation: 0.75, productive_aging_index: 0.45,
    cognitive_decline_risk: 0.50, eldercare_infrastructure_gap: 0.68,
    longevity_financial_products_penetration: 0.48, age_discrimination_index: 0.40,
    social_isolation_risk: 0.45, multigenerational_workforce_integration: 0.45,
    longevity_insurance_penetration: 0.48, retirement_adequacy_gap: 0.50,
    silver_digital_inclusion: 0.55, geroscience_readiness: 0.40,
  },
  // LE-004: LATAM, longevity_biotech → low, longevity_thriving / none
  {
    id: "LE-004", longevity_segment: "longevity_biotech", region: "LATAM",
    aging_population_rate: 0.18, longevity_biotech_adoption: 0.80, silver_spending_power: 0.80,
    intergenerational_wealth_transfer_rate: 0.78, pension_system_stress: 0.15,
    healthcare_cost_inflation: 0.15, productive_aging_index: 0.82,
    cognitive_decline_risk: 0.15, eldercare_infrastructure_gap: 0.15,
    longevity_financial_products_penetration: 0.80, age_discrimination_index: 0.15,
    social_isolation_risk: 0.15, multigenerational_workforce_integration: 0.80,
    longevity_insurance_penetration: 0.82, retirement_adequacy_gap: 0.12,
    silver_digital_inclusion: 0.85, geroscience_readiness: 0.82,
  },
  // LE-005: MEA, pension_management → critical, silver_exclusion
  {
    id: "LE-005", longevity_segment: "pension_management", region: "MEA",
    aging_population_rate: 0.75, longevity_biotech_adoption: 0.20, silver_spending_power: 0.25,
    intergenerational_wealth_transfer_rate: 0.40, pension_system_stress: 0.60,
    healthcare_cost_inflation: 0.62, productive_aging_index: 0.22,
    cognitive_decline_risk: 0.58, eldercare_infrastructure_gap: 0.55,
    longevity_financial_products_penetration: 0.25, age_discrimination_index: 0.52,
    social_isolation_risk: 0.72, multigenerational_workforce_integration: 0.22,
    longevity_insurance_penetration: 0.28, retirement_adequacy_gap: 0.62,
    silver_digital_inclusion: 0.28, geroscience_readiness: 0.18,
  },
  // LE-006: EMEA, wealth_management → moderate, none
  {
    id: "LE-006", longevity_segment: "wealth_management", region: "EMEA",
    aging_population_rate: 0.38, longevity_biotech_adoption: 0.55, silver_spending_power: 0.60,
    intergenerational_wealth_transfer_rate: 0.55, pension_system_stress: 0.38,
    healthcare_cost_inflation: 0.38, productive_aging_index: 0.58,
    cognitive_decline_risk: 0.38, eldercare_infrastructure_gap: 0.38,
    longevity_financial_products_penetration: 0.55, age_discrimination_index: 0.38,
    social_isolation_risk: 0.38, multigenerational_workforce_integration: 0.55,
    longevity_insurance_penetration: 0.55, retirement_adequacy_gap: 0.38,
    silver_digital_inclusion: 0.60, geroscience_readiness: 0.55,
  },
  // LE-007: APAC, eldercare_services → high, intergenerational_wealth_lock
  {
    id: "LE-007", longevity_segment: "eldercare_services", region: "APAC",
    aging_population_rate: 0.60, longevity_biotech_adoption: 0.40, silver_spending_power: 0.48,
    intergenerational_wealth_transfer_rate: 0.28, pension_system_stress: 0.50,
    healthcare_cost_inflation: 0.55, productive_aging_index: 0.38,
    cognitive_decline_risk: 0.50, eldercare_infrastructure_gap: 0.52,
    longevity_financial_products_penetration: 0.45, age_discrimination_index: 0.62,
    social_isolation_risk: 0.50, multigenerational_workforce_integration: 0.38,
    longevity_insurance_penetration: 0.45, retirement_adequacy_gap: 0.52,
    silver_digital_inclusion: 0.52, geroscience_readiness: 0.38,
  },
  // LE-008: NOAM, pension_management → critical, longevity_insurance_gap
  {
    id: "LE-008", longevity_segment: "pension_management", region: "NOAM",
    aging_population_rate: 0.78, longevity_biotech_adoption: 0.22, silver_spending_power: 0.28,
    intergenerational_wealth_transfer_rate: 0.42, pension_system_stress: 0.65,
    healthcare_cost_inflation: 0.65, productive_aging_index: 0.25,
    cognitive_decline_risk: 0.62, eldercare_infrastructure_gap: 0.60,
    longevity_financial_products_penetration: 0.28, age_discrimination_index: 0.50,
    social_isolation_risk: 0.58, multigenerational_workforce_integration: 0.28,
    longevity_insurance_penetration: 0.22, retirement_adequacy_gap: 0.68,
    silver_digital_inclusion: 0.42, geroscience_readiness: 0.20,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function agingScore(e: Entity): number {
  return Math.round(
    (e.aging_population_rate * 0.4 + e.pension_system_stress * 0.35 + e.retirement_adequacy_gap * 0.25) * 100 * 100
  ) / 100;
}

function financialScore(e: Entity): number {
  return Math.round(
    ((1 - e.silver_spending_power) * 0.4 +
      (1 - e.longevity_financial_products_penetration) * 0.35 +
      (1 - e.longevity_insurance_penetration) * 0.25) *
      100 *
      100
  ) / 100;
}

function healthScore(e: Entity): number {
  return Math.round(
    (e.healthcare_cost_inflation * 0.4 + e.eldercare_infrastructure_gap * 0.35 + e.cognitive_decline_risk * 0.25) *
      100 *
      100
  ) / 100;
}

function inclusionScore(e: Entity): number {
  return Math.round(
    (e.social_isolation_risk * 0.4 + e.age_discrimination_index * 0.35 + (1 - e.silver_digital_inclusion) * 0.25) *
      100 *
      100
  ) / 100;
}

function longevityComposite(aging: number, financial: number, health: number, inclusion: number): number {
  return Math.round((aging * 0.30 + financial * 0.25 + health * 0.25 + inclusion * 0.20) * 100) / 100;
}

function longevityPattern(e: Entity): string {
  if (e.pension_system_stress >= 0.70 && e.retirement_adequacy_gap >= 0.65) return "pension_collapse";
  if (e.healthcare_cost_inflation >= 0.70 && e.eldercare_infrastructure_gap >= 0.60) return "healthcare_cost_spiral";
  if ((1 - e.silver_digital_inclusion) >= 0.65 && e.social_isolation_risk >= 0.60) return "silver_exclusion";
  if ((1 - e.intergenerational_wealth_transfer_rate) >= 0.65 && e.age_discrimination_index >= 0.55)
    return "intergenerational_wealth_lock";
  if ((1 - e.longevity_insurance_penetration) >= 0.70 && e.retirement_adequacy_gap >= 0.60)
    return "longevity_insurance_gap";
  return "none";
}

function longevityRisk(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}

function longevitySeverity(composite: number): string {
  if (composite >= 75) return "longevity_emergency";
  if (composite >= 50) return "high_longevity_risk";
  if (composite >= 25) return "silver_stress";
  return "longevity_thriving";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "longevity_emergency_program";
  if (risk === "high") {
    if (pattern === "pension_collapse") return "pension_rescue";
    return "silver_economy_stimulus";
  }
  if (risk === "moderate") return "longevity_monitoring";
  return "no_action";
}

function longevitySignal(e: Entity, risk: string, composite: number): string {
  if (risk === "critical") {
    return `Critique — stress système pension ${Math.round(e.pension_system_stress * 100)}% — inflation soins santé ${Math.round(e.healthcare_cost_inflation * 100)}% — composite ${Math.round(composite)}`;
  }
  if (risk === "high") {
    return `Élevé — isolation sociale seniors ${Math.round(e.social_isolation_risk * 100)}% — gap retraite ${Math.round(e.retirement_adequacy_gap * 100)}% — composite ${Math.round(composite)}`;
  }
  if (risk === "moderate") {
    return `Modéré — inclusion digitale silver ${Math.round(e.silver_digital_inclusion * 100)}% — composite ${Math.round(composite)}`;
  }
  return "Économie longévité florissante — silver power fort, systèmes de retraite robustes";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[longevity-economy-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tAging = 0, tFinancial = 0, tHealth = 0, tInclusion = 0, tComposite = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.longevity_risk] = (rc[ent.longevity_risk] || 0) + 1;
      pc[ent.longevity_pattern] = (pc[ent.longevity_pattern] || 0) + 1;
      sc[ent.longevity_severity] = (sc[ent.longevity_severity] || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tAging += ent.aging_score;
      tFinancial += ent.financial_score;
      tHealth += ent.health_score;
      tInclusion += ent.inclusion_score;
      tComposite += ent.longevity_composite;
      if (ent.is_in_longevity_crisis) crisisCount++;
      if (ent.requires_longevity_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round((tComposite / n) * 100) / 100;
    const summary = {
      total: n,
      risk_counts: rc,
      pattern_counts: pc,
      severity_counts: sc,
      action_counts: ac,
      avg_longevity_composite: avgComposite,
      longevity_crisis_count: crisisCount,
      longevity_intervention_count: interventionCount,
      avg_aging_score: Math.round((tAging / n) * 10) / 10,
      avg_financial_score: Math.round((tFinancial / n) * 10) / 10,
      avg_health_score: Math.round((tHealth / n) * 10) / 10,
      avg_inclusion_score: Math.round((tInclusion / n) * 10) / 10,
      avg_estimated_longevity_risk_index: Math.round((avgComposite / 100) * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "longevity-economy-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/longevity-economy-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    const data = await upstream.json();
    return sealResponse(NextResponse.json(sealResponse(data, "longevity-economy-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream longevity-economy-engine unavailable" }, "longevity-economy-engine"),
      { status: 502 }
    ));
  }
}
