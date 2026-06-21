import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  {
    id: "GEF-001", labor_sector: "ride_hailing", region: "LATAM",
    platform_worker_precarity_index: 0.82, social_protection_absence_rate: 0.78,
    income_volatility_severity: 0.75, algorithmic_management_oppression: 0.60,
    classification_misuse_rate: 0.55, collective_bargaining_erosion: 0.60,
    platform_monopoly_dependency: 0.58, health_insecurity_exposure: 0.72,
    housing_instability_cascade: 0.68, gig_poverty_trap_prevalence: 0.70,
    skills_atrophy_rate: 0.55, demographic_exploitation_index: 0.58,
    regulatory_arbitrage_exploitation: 0.60, platform_exit_barrier: 0.50,
    cross_platform_competition_race: 0.55, gig_economy_gdp_dependency: 0.48,
    labor_market_dualization_index: 0.52,
  },
  {
    id: "GEF-002", labor_sector: "freelance_creative", region: "APAC",
    platform_worker_precarity_index: 0.18, social_protection_absence_rate: 0.20,
    income_volatility_severity: 0.22, algorithmic_management_oppression: 0.15,
    classification_misuse_rate: 0.18, collective_bargaining_erosion: 0.15,
    platform_monopoly_dependency: 0.20, health_insecurity_exposure: 0.18,
    housing_instability_cascade: 0.15, gig_poverty_trap_prevalence: 0.12,
    skills_atrophy_rate: 0.15, demographic_exploitation_index: 0.18,
    regulatory_arbitrage_exploitation: 0.15, platform_exit_barrier: 0.20,
    cross_platform_competition_race: 0.18, gig_economy_gdp_dependency: 0.15,
    labor_market_dualization_index: 0.12,
  },
  {
    id: "GEF-003", labor_sector: "food_delivery", region: "EMEA",
    platform_worker_precarity_index: 0.58, social_protection_absence_rate: 0.55,
    income_volatility_severity: 0.52, algorithmic_management_oppression: 0.78,
    classification_misuse_rate: 0.60, collective_bargaining_erosion: 0.55,
    platform_monopoly_dependency: 0.72, health_insecurity_exposure: 0.58,
    housing_instability_cascade: 0.50, gig_poverty_trap_prevalence: 0.48,
    skills_atrophy_rate: 0.45, demographic_exploitation_index: 0.60,
    regulatory_arbitrage_exploitation: 0.55, platform_exit_barrier: 0.62,
    cross_platform_competition_race: 0.68, gig_economy_gdp_dependency: 0.48,
    labor_market_dualization_index: 0.50,
  },
  {
    id: "GEF-004", labor_sector: "micro_tasking", region: "NOAM",
    platform_worker_precarity_index: 0.12, social_protection_absence_rate: 0.15,
    income_volatility_severity: 0.10, algorithmic_management_oppression: 0.12,
    classification_misuse_rate: 0.10, collective_bargaining_erosion: 0.12,
    platform_monopoly_dependency: 0.15, health_insecurity_exposure: 0.12,
    housing_instability_cascade: 0.10, gig_poverty_trap_prevalence: 0.10,
    skills_atrophy_rate: 0.12, demographic_exploitation_index: 0.10,
    regulatory_arbitrage_exploitation: 0.12, platform_exit_barrier: 0.15,
    cross_platform_competition_race: 0.12, gig_economy_gdp_dependency: 0.10,
    labor_market_dualization_index: 0.08,
  },
  {
    id: "GEF-005", labor_sector: "domestic_care", region: "MEA",
    platform_worker_precarity_index: 0.62, social_protection_absence_rate: 0.58,
    income_volatility_severity: 0.60, algorithmic_management_oppression: 0.55,
    classification_misuse_rate: 0.78, collective_bargaining_erosion: 0.82,
    platform_monopoly_dependency: 0.58, health_insecurity_exposure: 0.72,
    housing_instability_cascade: 0.70, gig_poverty_trap_prevalence: 0.65,
    skills_atrophy_rate: 0.55, demographic_exploitation_index: 0.72,
    regulatory_arbitrage_exploitation: 0.68, platform_exit_barrier: 0.60,
    cross_platform_competition_race: 0.55, gig_economy_gdp_dependency: 0.50,
    labor_market_dualization_index: 0.58,
  },
  {
    id: "GEF-006", labor_sector: "logistics_last_mile", region: "APAC",
    platform_worker_precarity_index: 0.38, social_protection_absence_rate: 0.35,
    income_volatility_severity: 0.32, algorithmic_management_oppression: 0.40,
    classification_misuse_rate: 0.35, collective_bargaining_erosion: 0.38,
    platform_monopoly_dependency: 0.42, health_insecurity_exposure: 0.38,
    housing_instability_cascade: 0.30, gig_poverty_trap_prevalence: 0.32,
    skills_atrophy_rate: 0.28, demographic_exploitation_index: 0.35,
    regulatory_arbitrage_exploitation: 0.38, platform_exit_barrier: 0.40,
    cross_platform_competition_race: 0.42, gig_economy_gdp_dependency: 0.30,
    labor_market_dualization_index: 0.32,
  },
  {
    id: "GEF-007", labor_sector: "beauty_wellness", region: "LATAM",
    platform_worker_precarity_index: 0.58, social_protection_absence_rate: 0.55,
    income_volatility_severity: 0.72, algorithmic_management_oppression: 0.60,
    classification_misuse_rate: 0.58, collective_bargaining_erosion: 0.55,
    platform_monopoly_dependency: 0.52, health_insecurity_exposure: 0.58,
    housing_instability_cascade: 0.65, gig_poverty_trap_prevalence: 0.55,
    skills_atrophy_rate: 0.48, demographic_exploitation_index: 0.78,
    regulatory_arbitrage_exploitation: 0.55, platform_exit_barrier: 0.52,
    cross_platform_competition_race: 0.50, gig_economy_gdp_dependency: 0.45,
    labor_market_dualization_index: 0.52,
  },
  {
    id: "GEF-008", labor_sector: "platform_agriculture", region: "EMEA",
    platform_worker_precarity_index: 0.62, social_protection_absence_rate: 0.58,
    income_volatility_severity: 0.60, algorithmic_management_oppression: 0.58,
    classification_misuse_rate: 0.55, collective_bargaining_erosion: 0.62,
    platform_monopoly_dependency: 0.58, health_insecurity_exposure: 0.65,
    housing_instability_cascade: 0.72, gig_poverty_trap_prevalence: 0.68,
    skills_atrophy_rate: 0.60, demographic_exploitation_index: 0.62,
    regulatory_arbitrage_exploitation: 0.58, platform_exit_barrier: 0.55,
    cross_platform_competition_race: 0.52, gig_economy_gdp_dependency: 0.72,
    labor_market_dualization_index: 0.78,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function precarityScore(i: Entity): number {
  return Math.round((i.platform_worker_precarity_index * 0.4 + i.income_volatility_severity * 0.35 + i.gig_poverty_trap_prevalence * 0.25) * 100 * 100) / 100;
}
function rightsScore(i: Entity): number {
  return Math.round((i.social_protection_absence_rate * 0.4 + i.collective_bargaining_erosion * 0.35 + i.classification_misuse_rate * 0.25) * 100 * 100) / 100;
}
function exploitationScore(i: Entity): number {
  return Math.round((i.algorithmic_management_oppression * 0.4 + i.demographic_exploitation_index * 0.35 + i.regulatory_arbitrage_exploitation * 0.25) * 100 * 100) / 100;
}
function systemicScore(i: Entity): number {
  return Math.round((i.labor_market_dualization_index * 0.4 + i.platform_monopoly_dependency * 0.35 + i.gig_economy_gdp_dependency * 0.25) * 100 * 100) / 100;
}
function compositeScore(pre: number, rig: number, exp: number, sys: number): number {
  return Math.round((pre * 0.30 + rig * 0.25 + exp * 0.25 + sys * 0.20) * 100) / 100;
}
function gigRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}
function gigPattern(i: Entity): string {
  if (i.platform_worker_precarity_index >= 0.70 && i.social_protection_absence_rate >= 0.65) return "precariat_explosion";
  if (i.algorithmic_management_oppression >= 0.70 && i.platform_monopoly_dependency >= 0.65) return "algorithmic_serfdom";
  if (i.collective_bargaining_erosion >= 0.70 && i.classification_misuse_rate >= 0.65) return "rights_collapse";
  if (i.demographic_exploitation_index >= 0.70 && i.income_volatility_severity >= 0.65) return "demographic_exploitation";
  if (i.labor_market_dualization_index >= 0.70 && i.gig_economy_gdp_dependency >= 0.65) return "systemic_dualization";
  return "none";
}
function gigSeverity(comp: number): string {
  if (comp >= 60) return "effondrement_social_précariat";
  if (comp >= 40) return "crise_travail_platformisé";
  if (comp >= 20) return "précarisation_structurelle";
  return "tensions_gig_contenues";
}
function gigAction(risk: string): string {
  if (risk === "critical") return "intervention_sociale_urgente";
  if (risk === "high") return "régulation_plateforme_activée";
  if (risk === "moderate") return "renforcement_droits_travailleurs_gig";
  return "veille_précarité_continue";
}
function gigSignal(risk: string): string {
  const signals: Record<string, string> = {
    critical: "🔴 Effondrement social précariat — crise du travail critique",
    high: "🟠 Crise du travail platformisé détectée",
    moderate: "🟡 Précarisation structurelle en cours",
    low: "🟢 Économie gig relativement stable",
  };
  return signals[risk] || "";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(i => {
      const pre = precarityScore(i);
      const rig = rightsScore(i);
      const exp = exploitationScore(i);
      const sys = systemicScore(i);
      const comp = compositeScore(pre, rig, exp, sys);
      const risk = gigRisk(comp);
      const pattern = gigPattern(i);
      const severity = gigSeverity(comp);
      const action = gigAction(risk);
      return {
        id: i.entity_id,
        labor_sector: i.labor_sector,
        region: i.region,
        precarity_score: pre,
        rights_score: rig,
        exploitation_score: exp,
        systemic_score: sys,
        composite_score: comp,
        risk_level: risk,
        gig_pattern: pattern,
        severity,
        recommended_action: action,
        signal: gigSignal(risk),
        platform_worker_precarity_index: i.platform_worker_precarity_index,
        labor_market_dualization_index: i.labor_market_dualization_index,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tComp = 0;

    for (const e of entities) {
      rc[e.risk_level] = (rc[e.risk_level] || 0) + 1;
      pc[e.gig_pattern] = (pc[e.gig_pattern] || 0) + 1;
      sc[e.severity] = (sc[e.severity] || 0) + 1;
      ac[e.recommended_action] = (ac[e.recommended_action] || 0) + 1;
      tComp += e.composite_score;
    }
    const n = entities.length;
    const avgComp = tComp / n;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id: 334,
        module_name: "Gig Economy Fragility & Precariat Intelligence Engine",
        total_entities: n,
        critical_count: rc["critical"] || 0,
        high_count: rc["high"] || 0,
        moderate_count: rc["moderate"] || 0,
        low_count: rc["low"] || 0,
        avg_composite: Math.round(avgComp * 100) / 100,
        pattern_distribution: pc,
        risk_distribution: rc,
        severity_distribution: sc,
        action_distribution: ac,
        avg_estimated_precarity_index: Math.round(avgComp / 100 * 10 * 100) / 100,
      },
    } as Record<string, unknown>));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/gig-economy-fragility-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json() as Record<string, unknown>));
  } catch {
    return NextResponse.json(sealResponse({ error: "Upstream unavailable" } as Record<string, unknown>), { status: 502 });
  }
}
