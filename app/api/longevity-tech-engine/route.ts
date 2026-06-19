import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── Mock entities ──────────────────────────────────────────────────────────────
// 8 entities covering all patterns and risk levels as specified in Module 324.

const MOCK_ENTITIES = [
  // LTE-001 — NOAM, biotech_cluster → critical, immortality_apartheid
  // senolytic_therapy_access_inequality≥0.70 AND longevity_wealth_concentration≥0.65 → immortality_apartheid
  // composite≥60 → critical
  {
    entity_id: "LTE-001", longevity_sector: "biotech_cluster", region: "NOAM",
    senolytic_therapy_access_inequality: 0.85,
    epigenetic_reprogramming_risk: 0.75,
    longevity_wealth_concentration: 0.80,
    healthcare_system_disruption_rate: 0.70,
    pension_system_longevity_shock: 0.65,
    intergenerational_resource_conflict: 0.60,
    immortality_elite_emergence_risk: 0.78,
    regulatory_approval_gap: 0.55,
    bioethics_framework_deficit: 0.50,
    longevity_data_sovereignty_risk: 0.60,
    anti_aging_inequality_index: 0.82,
    youth_labor_market_displacement: 0.55,
    democratic_longevity_governance_gap: 0.50,
    biotech_monopoly_formation: 0.65,
    longevity_economy_transition_speed: 0.70,
    social_cohesion_longevity_tension: 0.65,
    longevity_misinformation_exposure: 0.55,
  },
  // LTE-002 — APAC, traditional_medicine → low, none
  // values all 0.15–0.25 range
  {
    entity_id: "LTE-002", longevity_sector: "traditional_medicine", region: "APAC",
    senolytic_therapy_access_inequality: 0.18,
    epigenetic_reprogramming_risk: 0.20,
    longevity_wealth_concentration: 0.15,
    healthcare_system_disruption_rate: 0.18,
    pension_system_longevity_shock: 0.20,
    intergenerational_resource_conflict: 0.15,
    immortality_elite_emergence_risk: 0.18,
    regulatory_approval_gap: 0.20,
    bioethics_framework_deficit: 0.15,
    longevity_data_sovereignty_risk: 0.18,
    anti_aging_inequality_index: 0.20,
    youth_labor_market_displacement: 0.15,
    democratic_longevity_governance_gap: 0.18,
    biotech_monopoly_formation: 0.20,
    longevity_economy_transition_speed: 0.15,
    social_cohesion_longevity_tension: 0.18,
    longevity_misinformation_exposure: 0.22,
  },
  // LTE-003 — EMEA, pharmaceutical_sector → high, governance_vacuum
  // regulatory_approval_gap≥0.70 AND bioethics_framework_deficit≥0.65 → governance_vacuum
  // composite in [40,60) → high
  {
    entity_id: "LTE-003", longevity_sector: "pharmaceutical_sector", region: "EMEA",
    senolytic_therapy_access_inequality: 0.50,
    epigenetic_reprogramming_risk: 0.48,
    longevity_wealth_concentration: 0.45,
    healthcare_system_disruption_rate: 0.52,
    pension_system_longevity_shock: 0.48,
    intergenerational_resource_conflict: 0.45,
    immortality_elite_emergence_risk: 0.50,
    regulatory_approval_gap: 0.75,
    bioethics_framework_deficit: 0.70,
    longevity_data_sovereignty_risk: 0.48,
    anti_aging_inequality_index: 0.52,
    youth_labor_market_displacement: 0.45,
    democratic_longevity_governance_gap: 0.50,
    biotech_monopoly_formation: 0.48,
    longevity_economy_transition_speed: 0.45,
    social_cohesion_longevity_tension: 0.50,
    longevity_misinformation_exposure: 0.48,
  },
  // LTE-004 — LATAM, public_health → low, none
  // values all 0.15–0.25 range
  {
    entity_id: "LTE-004", longevity_sector: "public_health", region: "LATAM",
    senolytic_therapy_access_inequality: 0.20,
    epigenetic_reprogramming_risk: 0.18,
    longevity_wealth_concentration: 0.22,
    healthcare_system_disruption_rate: 0.15,
    pension_system_longevity_shock: 0.20,
    intergenerational_resource_conflict: 0.18,
    immortality_elite_emergence_risk: 0.15,
    regulatory_approval_gap: 0.20,
    bioethics_framework_deficit: 0.18,
    longevity_data_sovereignty_risk: 0.15,
    anti_aging_inequality_index: 0.20,
    youth_labor_market_displacement: 0.18,
    democratic_longevity_governance_gap: 0.22,
    biotech_monopoly_formation: 0.15,
    longevity_economy_transition_speed: 0.20,
    social_cohesion_longevity_tension: 0.18,
    longevity_misinformation_exposure: 0.15,
  },
  // LTE-005 — NOAM, silicon_valley_longevity → critical, biotech_monopoly
  // biotech_monopoly_formation≥0.70 AND longevity_data_sovereignty_risk≥0.65 → biotech_monopoly
  // composite≥60 → critical
  {
    entity_id: "LTE-005", longevity_sector: "silicon_valley_longevity", region: "NOAM",
    senolytic_therapy_access_inequality: 0.72,
    epigenetic_reprogramming_risk: 0.78,
    longevity_wealth_concentration: 0.75,
    healthcare_system_disruption_rate: 0.70,
    pension_system_longevity_shock: 0.72,
    intergenerational_resource_conflict: 0.68,
    immortality_elite_emergence_risk: 0.80,
    regulatory_approval_gap: 0.70,
    bioethics_framework_deficit: 0.72,
    longevity_data_sovereignty_risk: 0.78,
    anti_aging_inequality_index: 0.75,
    youth_labor_market_displacement: 0.70,
    democratic_longevity_governance_gap: 0.72,
    biotech_monopoly_formation: 0.82,
    longevity_economy_transition_speed: 0.75,
    social_cohesion_longevity_tension: 0.70,
    longevity_misinformation_exposure: 0.68,
  },
  // LTE-006 — EMEA, research_institution → moderate, none
  // values around 0.25–0.35 range
  {
    entity_id: "LTE-006", longevity_sector: "research_institution", region: "EMEA",
    senolytic_therapy_access_inequality: 0.30,
    epigenetic_reprogramming_risk: 0.28,
    longevity_wealth_concentration: 0.32,
    healthcare_system_disruption_rate: 0.28,
    pension_system_longevity_shock: 0.30,
    intergenerational_resource_conflict: 0.25,
    immortality_elite_emergence_risk: 0.30,
    regulatory_approval_gap: 0.32,
    bioethics_framework_deficit: 0.28,
    longevity_data_sovereignty_risk: 0.30,
    anti_aging_inequality_index: 0.28,
    youth_labor_market_displacement: 0.25,
    democratic_longevity_governance_gap: 0.30,
    biotech_monopoly_formation: 0.28,
    longevity_economy_transition_speed: 0.32,
    social_cohesion_longevity_tension: 0.28,
    longevity_misinformation_exposure: 0.30,
  },
  // LTE-007 — APAC, aging_society → high, system_collapse_shock
  // healthcare_system_disruption_rate≥0.70 AND pension_system_longevity_shock≥0.65 → system_collapse_shock
  // composite in [40,60) → high
  {
    entity_id: "LTE-007", longevity_sector: "aging_society", region: "APAC",
    senolytic_therapy_access_inequality: 0.55,
    epigenetic_reprogramming_risk: 0.50,
    longevity_wealth_concentration: 0.48,
    healthcare_system_disruption_rate: 0.75,
    pension_system_longevity_shock: 0.72,
    intergenerational_resource_conflict: 0.52,
    immortality_elite_emergence_risk: 0.50,
    regulatory_approval_gap: 0.48,
    bioethics_framework_deficit: 0.45,
    longevity_data_sovereignty_risk: 0.52,
    anti_aging_inequality_index: 0.55,
    youth_labor_market_displacement: 0.50,
    democratic_longevity_governance_gap: 0.48,
    biotech_monopoly_formation: 0.45,
    longevity_economy_transition_speed: 0.55,
    social_cohesion_longevity_tension: 0.52,
    longevity_misinformation_exposure: 0.48,
  },
  // LTE-008 — MEA, longevity_economy → critical, intergenerational_war
  // intergenerational_resource_conflict≥0.70 AND youth_labor_market_displacement≥0.65 → intergenerational_war
  // composite≥60 → critical
  {
    entity_id: "LTE-008", longevity_sector: "longevity_economy", region: "MEA",
    senolytic_therapy_access_inequality: 0.72,
    epigenetic_reprogramming_risk: 0.68,
    longevity_wealth_concentration: 0.70,
    healthcare_system_disruption_rate: 0.68,
    pension_system_longevity_shock: 0.65,
    intergenerational_resource_conflict: 0.78,
    immortality_elite_emergence_risk: 0.70,
    regulatory_approval_gap: 0.65,
    bioethics_framework_deficit: 0.68,
    longevity_data_sovereignty_risk: 0.65,
    anti_aging_inequality_index: 0.72,
    youth_labor_market_displacement: 0.72,
    democratic_longevity_governance_gap: 0.68,
    biotech_monopoly_formation: 0.65,
    longevity_economy_transition_speed: 0.70,
    social_cohesion_longevity_tension: 0.72,
    longevity_misinformation_exposure: 0.68,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

// ── Scoring functions (mirrors Python engine exactly) ──────────────────────────

function accessScore(e: Entity): number {
  const raw = (
    e.senolytic_therapy_access_inequality * 0.4
    + e.anti_aging_inequality_index * 0.35
    + e.longevity_wealth_concentration * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function disruptionScore(e: Entity): number {
  const raw = (
    e.healthcare_system_disruption_rate * 0.4
    + e.pension_system_longevity_shock * 0.35
    + e.longevity_economy_transition_speed * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function governanceScore(e: Entity): number {
  const raw = (
    e.regulatory_approval_gap * 0.4
    + e.bioethics_framework_deficit * 0.35
    + e.democratic_longevity_governance_gap * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function societalScore(e: Entity): number {
  const raw = (
    e.immortality_elite_emergence_risk * 0.4
    + e.intergenerational_resource_conflict * 0.35
    + e.social_cohesion_longevity_tension * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function longevityComposite(access: number, disruption: number, governance: number, societal: number): number {
  return Math.round((access * 0.30 + disruption * 0.25 + governance * 0.25 + societal * 0.20) * 100) / 100;
}

function longevityRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function longevityPattern(e: Entity): string {
  if (e.senolytic_therapy_access_inequality >= 0.70 && e.longevity_wealth_concentration >= 0.65)
    return "immortality_apartheid";
  if (e.healthcare_system_disruption_rate >= 0.70 && e.pension_system_longevity_shock >= 0.65)
    return "system_collapse_shock";
  if (e.biotech_monopoly_formation >= 0.70 && e.longevity_data_sovereignty_risk >= 0.65)
    return "biotech_monopoly";
  if (e.regulatory_approval_gap >= 0.70 && e.bioethics_framework_deficit >= 0.65)
    return "governance_vacuum";
  if (e.intergenerational_resource_conflict >= 0.70 && e.youth_labor_market_displacement >= 0.65)
    return "intergenerational_war";
  return "none";
}

function longevitySeverity(comp: number): string {
  if (comp >= 75) return "longevity_emergency";
  if (comp >= 50) return "high_longevity_disruption";
  if (comp >= 25) return "longevity_tension";
  return "longevity_managed";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "longevity_emergency_governance";
  if (risk === "high" && pattern === "immortality_apartheid") return "universal_longevity_access";
  if (risk === "high") return "longevity_transition_framework";
  if (risk === "moderate") return "longevity_monitoring";
  return "no_action";
}

function longevitySignal(e: Entity, risk: string, comp: number, access: number): string {
  if (risk === "critical") {
    return `Critique — apartheid de l'immortalité émergent — inégalité d'accès ${Math.round(access)}% — composite ${comp.toFixed(1)}`;
  }
  if (risk === "high") {
    return `Élevé — disruption système longévité ${Math.round(e.healthcare_system_disruption_rate * 100)}% — lacune gouvernance ${Math.round(e.regulatory_approval_gap * 100)}% — composite ${comp.toFixed(1)}`;
  }
  if (risk === "moderate") {
    return `Modéré — tension sociale longévité ${Math.round(e.social_cohesion_longevity_tension * 100)}% — composite ${comp.toFixed(1)}`;
  }
  return "Technologie longévité gérée — accès équitable, gouvernance solide, cohésion sociale préservée";
}

// ── GET handler ────────────────────────────────────────────────────────────────

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const access     = accessScore(e);
      const disruption = disruptionScore(e);
      const governance = governanceScore(e);
      const societal   = societalScore(e);
      const comp       = longevityComposite(access, disruption, governance, societal);
      const risk       = longevityRisk(comp);
      const pat        = longevityPattern(e);
      const sev        = longevitySeverity(comp);
      const act        = recommendedAction(risk, pat);
      const sig        = longevitySignal(e, risk, comp, access);

      return {
        entity_id:                          e.entity_id,
        region:                             e.region,
        longevity_sector:                   e.longevity_sector,
        longevity_risk:                     risk,
        longevity_pattern:                  pat,
        longevity_severity:                 sev,
        recommended_action:                 act,
        access_score:                       access,
        disruption_score:                   disruption,
        governance_score:                   governance,
        societal_score:                     societal,
        longevity_composite:                comp,
        is_longevity_crisis:                comp >= 60,
        requires_longevity_intervention:    comp >= 40,
        longevity_signal:                   sig,
      };
    });

    let tAccess = 0, tDisruption = 0, tGovernance = 0, tSocietal = 0, tComp = 0;
    let crisisCount = 0, interventionCount = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      tAccess     += ent.access_score;
      tDisruption += ent.disruption_score;
      tGovernance += ent.governance_score;
      tSocietal   += ent.societal_score;
      tComp       += ent.longevity_composite;
      if (ent.is_longevity_crisis)              crisisCount++;
      if (ent.requires_longevity_intervention)  interventionCount++;
      if (ent.longevity_risk === "critical")    criticalCount++;
      if (ent.longevity_risk === "high")        highCount++;
      if (ent.longevity_risk === "moderate")    moderateCount++;
      if (ent.longevity_risk === "low")         lowCount++;
    }

    const n = entities.length;
    const avgComp = Math.round((tComp / n) * 100) / 100;

    const summary = {
      total_entities:                           n,
      critical_entities:                        criticalCount,
      high_entities:                            highCount,
      moderate_entities:                        moderateCount,
      low_entities:                             lowCount,
      entities_requiring_intervention:          interventionCount,
      longevity_crisis_entities:                crisisCount,
      avg_access_score:                         Math.round((tAccess     / n) * 100) / 100,
      avg_disruption_score:                     Math.round((tDisruption / n) * 100) / 100,
      avg_governance_score:                     Math.round((tGovernance / n) * 100) / 100,
      avg_societal_score:                       Math.round((tSocietal   / n) * 100) / 100,
      avg_longevity_composite:                  avgComp,
      avg_estimated_longevity_disruption_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "longevity-tech-engine"));
  }

  try {
    const upstream = await fetch(`${SWARM_API_URL}/longevity-tech-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    const data = await upstream.json();
    return NextResponse.json(sealResponse(data, "longevity-tech-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream longevity-tech-engine unavailable" }, "longevity-tech-engine"),
      { status: 502 }
    );
  }
}
