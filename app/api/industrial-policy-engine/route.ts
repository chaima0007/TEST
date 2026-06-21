import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  // SWARM_API_URL guard — will use mock data below
}

const MOCK_ENTITIES = [
  // IPE-001 — critical, pattern=strategic_dependency_crisis
  // strategic_dependency_crisis: strategic_dependency_exposure>0.85 AND semiconductor_dependency>0.80
  // composite >= 60 → critical
  {
    id: "IPE-001", industrial_sector: "semiconducteurs_electronique", region: "APAC",
    strategic_dependency_exposure: 0.90,
    reshoring_policy_effectiveness: 0.70,
    friend_shoring_progress: 0.55,
    industrial_subsidy_distortion: 0.65,
    supply_chain_resilience_gap: 0.75,
    semiconductor_dependency: 0.85,
    pharmaceutical_reshoring_lag: 0.70,
    green_tech_manufacturing_gap: 0.60,
    workforce_skills_mismatch: 0.65,
    regulatory_fragmentation: 0.62,
    protectionism_trade_war_risk: 0.65,
    IRA_like_subsidy_race: 0.60,
    strategic_autonomy_index: 0.65,
    de_risking_progress: 0.60,
    manufacturing_capacity_gap: 0.70,
    innovation_policy_effectiveness: 0.58,
    geopolitical_industrial_leverage: 0.70,
  },
  // IPE-002 — low, pattern=none
  // composite < 20 → low; no pattern triggers
  {
    id: "IPE-002", industrial_sector: "artisanat_local", region: "EMEA",
    strategic_dependency_exposure: 0.08,
    reshoring_policy_effectiveness: 0.10,
    friend_shoring_progress: 0.12,
    industrial_subsidy_distortion: 0.08,
    supply_chain_resilience_gap: 0.10,
    semiconductor_dependency: 0.08,
    pharmaceutical_reshoring_lag: 0.10,
    green_tech_manufacturing_gap: 0.10,
    workforce_skills_mismatch: 0.08,
    regulatory_fragmentation: 0.10,
    protectionism_trade_war_risk: 0.08,
    IRA_like_subsidy_race: 0.08,
    strategic_autonomy_index: 0.10,
    de_risking_progress: 0.10,
    manufacturing_capacity_gap: 0.08,
    innovation_policy_effectiveness: 0.12,
    geopolitical_industrial_leverage: 0.08,
  },
  // IPE-003 — high, pattern=subsidy_trade_war_escalation
  // subsidy_trade_war_escalation: IRA_like_subsidy_race>0.85 AND protectionism_trade_war_risk>0.80
  // strategic_dependency_crisis must NOT fire: strategic_dependency_exposure<=0.85 OR semiconductor_dependency<=0.80
  // composite >=40 and <60 → high
  {
    id: "IPE-003", industrial_sector: "acier_aluminium", region: "NOAM",
    strategic_dependency_exposure: 0.50,
    reshoring_policy_effectiveness: 0.50,
    friend_shoring_progress: 0.45,
    industrial_subsidy_distortion: 0.55,
    supply_chain_resilience_gap: 0.48,
    semiconductor_dependency: 0.48,
    pharmaceutical_reshoring_lag: 0.45,
    green_tech_manufacturing_gap: 0.48,
    workforce_skills_mismatch: 0.42,
    regulatory_fragmentation: 0.48,
    protectionism_trade_war_risk: 0.82,
    IRA_like_subsidy_race: 0.88,
    strategic_autonomy_index: 0.50,
    de_risking_progress: 0.48,
    manufacturing_capacity_gap: 0.45,
    innovation_policy_effectiveness: 0.42,
    geopolitical_industrial_leverage: 0.55,
  },
  // IPE-004 — moderate, pattern=none
  // composite >=20 and <40 → moderate; no pattern triggers
  {
    id: "IPE-004", industrial_sector: "chimie_materiaux", region: "LATAM",
    strategic_dependency_exposure: 0.28,
    reshoring_policy_effectiveness: 0.28,
    friend_shoring_progress: 0.30,
    industrial_subsidy_distortion: 0.28,
    supply_chain_resilience_gap: 0.28,
    semiconductor_dependency: 0.25,
    pharmaceutical_reshoring_lag: 0.30,
    green_tech_manufacturing_gap: 0.28,
    workforce_skills_mismatch: 0.28,
    regulatory_fragmentation: 0.30,
    protectionism_trade_war_risk: 0.25,
    IRA_like_subsidy_race: 0.25,
    strategic_autonomy_index: 0.28,
    de_risking_progress: 0.28,
    manufacturing_capacity_gap: 0.25,
    innovation_policy_effectiveness: 0.30,
    geopolitical_industrial_leverage: 0.30,
  },
  // IPE-005 — critical, pattern=reshoring_policy_failure
  // reshoring_policy_failure: reshoring_policy_effectiveness>0.85 AND workforce_skills_mismatch>0.80
  // strategic_dependency_crisis must NOT fire: strategic_dependency_exposure<=0.85 OR semiconductor_dependency<=0.80
  // subsidy_trade_war_escalation must NOT fire: IRA_like_subsidy_race<=0.85 OR protectionism_trade_war_risk<=0.80
  // composite >= 60 → critical
  {
    id: "IPE-005", industrial_sector: "construction_navale", region: "EMEA",
    strategic_dependency_exposure: 0.70,
    reshoring_policy_effectiveness: 0.88,
    friend_shoring_progress: 0.60,
    industrial_subsidy_distortion: 0.70,
    supply_chain_resilience_gap: 0.72,
    semiconductor_dependency: 0.65,
    pharmaceutical_reshoring_lag: 0.68,
    green_tech_manufacturing_gap: 0.65,
    workforce_skills_mismatch: 0.85,
    regulatory_fragmentation: 0.68,
    protectionism_trade_war_risk: 0.68,
    IRA_like_subsidy_race: 0.65,
    strategic_autonomy_index: 0.65,
    de_risking_progress: 0.65,
    manufacturing_capacity_gap: 0.68,
    innovation_policy_effectiveness: 0.62,
    geopolitical_industrial_leverage: 0.72,
  },
  // IPE-006 — high, pattern=pharmaceutical_supply_collapse
  // pharmaceutical_supply_collapse: pharmaceutical_reshoring_lag>0.80 AND supply_chain_resilience_gap>0.75
  // strategic_dependency_crisis must NOT fire: strategic_dependency_exposure<=0.85 OR semiconductor_dependency<=0.80
  // subsidy_trade_war_escalation must NOT fire: IRA_like_subsidy_race<=0.85 OR protectionism_trade_war_risk<=0.80
  // reshoring_policy_failure must NOT fire: reshoring_policy_effectiveness<=0.85 OR workforce_skills_mismatch<=0.80
  // composite >=40 and <60 → high
  {
    id: "IPE-006", industrial_sector: "pharmacie_biotechnologie", region: "MEA",
    strategic_dependency_exposure: 0.50,
    reshoring_policy_effectiveness: 0.50,
    friend_shoring_progress: 0.45,
    industrial_subsidy_distortion: 0.48,
    supply_chain_resilience_gap: 0.78,
    semiconductor_dependency: 0.45,
    pharmaceutical_reshoring_lag: 0.82,
    green_tech_manufacturing_gap: 0.45,
    workforce_skills_mismatch: 0.45,
    regulatory_fragmentation: 0.48,
    protectionism_trade_war_risk: 0.45,
    IRA_like_subsidy_race: 0.48,
    strategic_autonomy_index: 0.48,
    de_risking_progress: 0.45,
    manufacturing_capacity_gap: 0.48,
    innovation_policy_effectiveness: 0.42,
    geopolitical_industrial_leverage: 0.48,
  },
  // IPE-007 — critical, pattern=green_manufacturing_gap_crisis
  // green_manufacturing_gap_crisis: green_tech_manufacturing_gap>0.80 AND strategic_autonomy_index>0.75
  // all prior patterns must NOT fire
  // composite >= 60 → critical
  {
    id: "IPE-007", industrial_sector: "energies_renouvelables", region: "APAC",
    strategic_dependency_exposure: 0.70,
    reshoring_policy_effectiveness: 0.72,
    friend_shoring_progress: 0.62,
    industrial_subsidy_distortion: 0.68,
    supply_chain_resilience_gap: 0.72,
    semiconductor_dependency: 0.65,
    pharmaceutical_reshoring_lag: 0.68,
    green_tech_manufacturing_gap: 0.82,
    workforce_skills_mismatch: 0.65,
    regulatory_fragmentation: 0.68,
    protectionism_trade_war_risk: 0.70,
    IRA_like_subsidy_race: 0.68,
    strategic_autonomy_index: 0.78,
    de_risking_progress: 0.68,
    manufacturing_capacity_gap: 0.68,
    innovation_policy_effectiveness: 0.65,
    geopolitical_industrial_leverage: 0.75,
  },
  // IPE-008 — low, pattern=none
  // composite < 20 → low; no pattern triggers
  {
    id: "IPE-008", industrial_sector: "agriculture_agroalimentaire", region: "NOAM",
    strategic_dependency_exposure: 0.10,
    reshoring_policy_effectiveness: 0.08,
    friend_shoring_progress: 0.10,
    industrial_subsidy_distortion: 0.10,
    supply_chain_resilience_gap: 0.10,
    semiconductor_dependency: 0.10,
    pharmaceutical_reshoring_lag: 0.08,
    green_tech_manufacturing_gap: 0.10,
    workforce_skills_mismatch: 0.10,
    regulatory_fragmentation: 0.10,
    protectionism_trade_war_risk: 0.08,
    IRA_like_subsidy_race: 0.10,
    strategic_autonomy_index: 0.10,
    de_risking_progress: 0.08,
    manufacturing_capacity_gap: 0.08,
    innovation_policy_effectiveness: 0.12,
    geopolitical_industrial_leverage: 0.10,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function dependencyScore(e: Entity): number {
  const raw = (
    e.strategic_dependency_exposure * 0.4 +
    e.semiconductor_dependency * 0.35 +
    e.pharmaceutical_reshoring_lag * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function policyScore(e: Entity): number {
  const raw = (
    e.reshoring_policy_effectiveness * 0.4 +
    e.IRA_like_subsidy_race * 0.35 +
    e.industrial_subsidy_distortion * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function resilienceScore(e: Entity): number {
  const raw = (
    e.supply_chain_resilience_gap * 0.4 +
    e.manufacturing_capacity_gap * 0.35 +
    e.workforce_skills_mismatch * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function geopoliticalScore(e: Entity): number {
  const raw = (
    e.geopolitical_industrial_leverage * 0.4 +
    e.protectionism_trade_war_risk * 0.35 +
    e.de_risking_progress * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(dep: number, pol: number, res: number, geo: number): number {
  return Math.round((dep * 0.30 + pol * 0.25 + res * 0.25 + geo * 0.20) * 100) / 100;
}

function industrialPattern(e: Entity): string {
  if (e.strategic_dependency_exposure > 0.85 && e.semiconductor_dependency > 0.80)
    return "strategic_dependency_crisis";
  if (e.IRA_like_subsidy_race > 0.85 && e.protectionism_trade_war_risk > 0.80)
    return "subsidy_trade_war_escalation";
  if (e.reshoring_policy_effectiveness > 0.85 && e.workforce_skills_mismatch > 0.80)
    return "reshoring_policy_failure";
  if (e.pharmaceutical_reshoring_lag > 0.80 && e.supply_chain_resilience_gap > 0.75)
    return "pharmaceutical_supply_collapse";
  if (e.green_tech_manufacturing_gap > 0.80 && e.strategic_autonomy_index > 0.75)
    return "green_manufacturing_gap_crisis";
  return "none";
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function severity(comp: number): string {
  if (comp >= 60) return "crise_politique_industrielle_systémique";
  if (comp >= 40) return "disruption_industrielle_majeure";
  if (comp >= 20) return "restructuration_industrielle_active";
  return "politique_industrielle_gérée";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_politique_industrielle";
  if (risk === "high") return "renforcement_stratégie_relocalisation";
  if (risk === "moderate") return "surveillance_dépendances_industrielles";
  return "veille_politique_industrielle_continue";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise politique industrielle — dépendance stratégique systémique";
  if (risk === "high") return "🟠 Disruption industrielle majeure détectée";
  if (risk === "moderate") return "🟡 Restructuration industrielle active en cours";
  return "🟢 Politique industrielle gérée et surveillée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const dep = dependencyScore(e);
      const pol = policyScore(e);
      const res = resilienceScore(e);
      const geo = geopoliticalScore(e);
      const comp = compositeScore(dep, pol, res, geo);
      const pat  = industrialPattern(e);
      const risk = riskLevel(comp);
      const sev  = severity(comp);
      const act  = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:                       e.entity_id,
        industrial_sector:               e.industrial_sector,
        region:                          e.region,
        dependency_score:                dep,
        policy_score:                    pol,
        resilience_score:                res,
        geopolitical_score:              geo,
        composite_score:                 comp,
        risk_level:                      risk,
        industrial_pattern:              pat,
        severity:                        sev,
        recommended_action:              act,
        signal:                          sig,
        strategic_dependency_exposure:   e.strategic_dependency_exposure,
        semiconductor_dependency:        e.semiconductor_dependency,
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
      patDist[ent.industrial_pattern]  = (patDist[ent.industrial_pattern]  || 0) + 1;
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
      module_id:                         383,
      module_name:                       "Industrial Policy & Reshoring Intelligence Engine",
      total:                             n,
      critical:                          criticalCount,
      high:                              highCount,
      moderate:                          moderateCount,
      low:                               lowCount,
      avg_composite:                     avgComposite,
      risk_distribution:                 riskDist,
      pattern_distribution:              patDist,
      severity_distribution:             sevDist,
      action_distribution:               actDist,
      avg_estimated_reshoring_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "industrial-policy-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/industrial-policy-engine`);
    const data = await upstream.json();
    return NextResponse.json(sealResponse(data, "industrial-policy-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream industrial policy engine unavailable" }, "industrial-policy-engine"),
      { status: 502 }
    );
  }
}
