import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[noise-pollution-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const MOCK_ENTITIES = [
  // NPE-001 — critical, chronic_cardiovascular_noise_crisis (cardio>0.85, noise_db>0.80)
  {
    id: "NPE-001", urban_type: "métropole", region: "IDF",
    noise_level_db: 0.90, traffic_exposure: 0.88, aviation_exposure: 0.60, industrial_noise: 0.55,
    cardiovascular_risk: 0.88, sleep_disruption: 0.72, cognitive_impact: 0.70, mental_health_burden: 0.68,
    school_noise_exposure: 0.60, hospital_quiet_zone_compliance: 0.40,
    low_income_exposure: 0.65, racial_disparity: 0.60, regulatory_compliance: 0.30,
    green_barrier_coverage: 0.25, complaint_response_rate: 0.35, nighttime_violations: 0.70,
    tinnitus_prevalence: 0.62,
  },
  // NPE-002 — critical, sleep_deprivation_pandemic (sleep>0.85, nighttime>0.80)
  {
    id: "NPE-002", urban_type: "agglomération", region: "PACA",
    noise_level_db: 0.75, traffic_exposure: 0.78, aviation_exposure: 0.72, industrial_noise: 0.55,
    cardiovascular_risk: 0.72, sleep_disruption: 0.88, cognitive_impact: 0.68, mental_health_burden: 0.70,
    school_noise_exposure: 0.65, hospital_quiet_zone_compliance: 0.38,
    low_income_exposure: 0.68, racial_disparity: 0.62, regulatory_compliance: 0.28,
    green_barrier_coverage: 0.22, complaint_response_rate: 0.30, nighttime_violations: 0.85,
    tinnitus_prevalence: 0.68,
  },
  // NPE-003 — critical, childhood_cognitive_impairment (school>0.85, cogn>0.80)
  {
    id: "NPE-003", urban_type: "zone_industrielle", region: "HDF",
    noise_level_db: 0.82, traffic_exposure: 0.78, aviation_exposure: 0.50, industrial_noise: 0.88,
    cardiovascular_risk: 0.78, sleep_disruption: 0.75, cognitive_impact: 0.82, mental_health_burden: 0.72,
    school_noise_exposure: 0.88, hospital_quiet_zone_compliance: 0.35,
    low_income_exposure: 0.72, racial_disparity: 0.68, regulatory_compliance: 0.32,
    green_barrier_coverage: 0.20, complaint_response_rate: 0.32, nighttime_violations: 0.75,
    tinnitus_prevalence: 0.70,
  },
  // NPE-004 — high, noise_poverty_inequality_trap (low_income>0.85, racial>0.80)
  {
    id: "NPE-004", urban_type: "banlieue_dense", region: "IDF",
    noise_level_db: 0.42, traffic_exposure: 0.45, aviation_exposure: 0.35, industrial_noise: 0.30,
    cardiovascular_risk: 0.38, sleep_disruption: 0.40, cognitive_impact: 0.35, mental_health_burden: 0.38,
    school_noise_exposure: 0.50, hospital_quiet_zone_compliance: 0.55,
    low_income_exposure: 0.88, racial_disparity: 0.82, regulatory_compliance: 0.50,
    green_barrier_coverage: 0.45, complaint_response_rate: 0.48, nighttime_violations: 0.38,
    tinnitus_prevalence: 0.35,
  },
  // NPE-005 — high, regulatory_enforcement_collapse (reg_comp<0.20, complaint<0.20)
  {
    id: "NPE-005", urban_type: "port_industriel", region: "MED",
    noise_level_db: 0.45, traffic_exposure: 0.48, aviation_exposure: 0.38, industrial_noise: 0.50,
    cardiovascular_risk: 0.42, sleep_disruption: 0.45, cognitive_impact: 0.40, mental_health_burden: 0.42,
    school_noise_exposure: 0.45, hospital_quiet_zone_compliance: 0.45,
    low_income_exposure: 0.48, racial_disparity: 0.42, regulatory_compliance: 0.15,
    green_barrier_coverage: 0.40, complaint_response_rate: 0.18, nighttime_violations: 0.50,
    tinnitus_prevalence: 0.40,
  },
  // NPE-006 — moderate, none
  {
    id: "NPE-006", urban_type: "ville_moyenne", region: "ARA",
    noise_level_db: 0.35, traffic_exposure: 0.38, aviation_exposure: 0.25, industrial_noise: 0.28,
    cardiovascular_risk: 0.32, sleep_disruption: 0.35, cognitive_impact: 0.30, mental_health_burden: 0.28,
    school_noise_exposure: 0.32, hospital_quiet_zone_compliance: 0.60,
    low_income_exposure: 0.35, racial_disparity: 0.30, regulatory_compliance: 0.55,
    green_barrier_coverage: 0.45, complaint_response_rate: 0.55, nighttime_violations: 0.30,
    tinnitus_prevalence: 0.28,
  },
  // NPE-007 — low, none
  {
    id: "NPE-007", urban_type: "commune_rurale", region: "BZH",
    noise_level_db: 0.10, traffic_exposure: 0.12, aviation_exposure: 0.08, industrial_noise: 0.08,
    cardiovascular_risk: 0.10, sleep_disruption: 0.12, cognitive_impact: 0.10, mental_health_burden: 0.08,
    school_noise_exposure: 0.10, hospital_quiet_zone_compliance: 0.85,
    low_income_exposure: 0.12, racial_disparity: 0.10, regulatory_compliance: 0.88,
    green_barrier_coverage: 0.82, complaint_response_rate: 0.85, nighttime_violations: 0.08,
    tinnitus_prevalence: 0.10,
  },
  // NPE-008 — low, none
  {
    id: "NPE-008", urban_type: "parc_résidentiel", region: "OCC",
    noise_level_db: 0.12, traffic_exposure: 0.10, aviation_exposure: 0.08, industrial_noise: 0.06,
    cardiovascular_risk: 0.10, sleep_disruption: 0.10, cognitive_impact: 0.08, mental_health_burden: 0.10,
    school_noise_exposure: 0.08, hospital_quiet_zone_compliance: 0.90,
    low_income_exposure: 0.10, racial_disparity: 0.08, regulatory_compliance: 0.90,
    green_barrier_coverage: 0.88, complaint_response_rate: 0.88, nighttime_violations: 0.06,
    tinnitus_prevalence: 0.08,
  },
];

type NPEInput = typeof MOCK_ENTITIES[0];

function exposureScore(e: NPEInput): number {
  return Math.round((e.noise_level_db * 0.40 + e.traffic_exposure * 0.35 + e.aviation_exposure * 0.15 + e.industrial_noise * 0.10) * 100 * 100) / 100;
}
function healthImpactScore(e: NPEInput): number {
  return Math.round((e.cardiovascular_risk * 0.35 + e.sleep_disruption * 0.30 + e.cognitive_impact * 0.20 + e.mental_health_burden * 0.15) * 100 * 100) / 100;
}
function inequalityScore(e: NPEInput): number {
  return Math.round((e.low_income_exposure * 0.40 + e.racial_disparity * 0.35 + e.school_noise_exposure * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: NPEInput): number {
  return Math.round(((1 - e.regulatory_compliance) * 0.40 + e.nighttime_violations * 0.35 + (1 - e.complaint_response_rate) * 0.15 + (1 - e.green_barrier_coverage) * 0.10) * 100 * 100) / 100;
}
function compositeScore(exp: number, hlt: number, ineq: number, gov: number): number {
  return Math.round((exp * 0.30 + hlt * 0.25 + ineq * 0.25 + gov * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function noisePattern(e: NPEInput): string {
  if (e.cardiovascular_risk > 0.85 && e.noise_level_db > 0.80) return "chronic_cardiovascular_noise_crisis";
  if (e.sleep_disruption > 0.85 && e.nighttime_violations > 0.80) return "sleep_deprivation_pandemic";
  if (e.school_noise_exposure > 0.85 && e.cognitive_impact > 0.80) return "childhood_cognitive_impairment";
  if (e.low_income_exposure > 0.85 && e.racial_disparity > 0.80) return "noise_poverty_inequality_trap";
  if (e.regulatory_compliance < 0.20 && e.complaint_response_rate < 0.20) return "regulatory_enforcement_collapse";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_pollution_sonore_systémique";
  if (composite >= 40) return "crise_santé_urbaine_majeure";
  if (composite >= 20) return "nuisance_sonore_structurelle";
  return "environnement_sonore_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_pollution_sonore_critique";
  if (risk === "high") return "plan_réduction_bruit_accéléré_zones_vulnérables";
  if (risk === "moderate") return "renforcement_réglementation_acoustique_urbaine";
  return "veille_environnement_sonore_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise pollution sonore systémique — santé urbaine en péril";
  if (risk === "high") return "🟠 Crise santé urbaine majeure détectée";
  if (risk === "moderate") return "🟡 Nuisance sonore structurelle active";
  return "🟢 Environnement sonore sous surveillance";
}

const SWARM_API_URL = process.env.SWARM_API_URL;

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const exp  = exposureScore(e);
      const hlt  = healthImpactScore(e);
      const ineq = inequalityScore(e);
      const gov  = governanceScore(e);
      const comp = compositeScore(exp, hlt, ineq, gov);
      const risk = riskLevel(comp);
      const pat  = noisePattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:          e.entity_id,
        urban_type:         e.urban_type,
        region:             e.region,
        exposure_score:     exp,
        health_impact_score: hlt,
        inequality_score:   ineq,
        governance_score:   gov,
        composite_score:    comp,
        risk_level:         risk,
        noise_pattern:      pat,
        severity:           sev,
        recommended_action: action,
        signal:             sig,
        noise_level_db:     e.noise_level_db,
        sleep_disruption:   e.sleep_disruption,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.noise_pattern]      = (pattern_distribution[ent.noise_pattern]      || 0) + 1;
      severity_distribution[ent.severity]          = (severity_distribution[ent.severity]          || 0) + 1;
      action_distribution[ent.recommended_action]  = (action_distribution[ent.recommended_action]  || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                          398,
      module_name:                        "Pollution Sonore & Santé Urbaine Intelligence Engine",
      total:                              n,
      critical:                           criticalCount,
      high:                               highCount,
      moderate:                           moderateCount,
      low:                                lowCount,
      avg_composite:                      avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_noise_health_index:   Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>)));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/noise-pollution-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(sealResponse(await res.json())));
  } catch {}
  return sealResponse(NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 }));
}
