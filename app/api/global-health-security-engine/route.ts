import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // GHS-001 — critical, pandemic_preparedness_collapse (preparedness_gap>0.85, surveillance>0.80)
  {
    entity_id: "GHS-001", health_system_type: "système_fragile_pandémique", region: "AFRIQUE_SSA",
    pandemic_preparedness_gap: 0.92, surveillance_system_weakness: 0.88,
    healthcare_system_resilience: 0.75, international_coordination_failure: 0.72,
    WHO_funding_adequacy: 0.68, vaccine_manufacturing_capacity: 0.70,
    supply_chain_health_vulnerability: 0.78, health_worker_shortage: 0.80,
    IHR_compliance_failure: 0.82, diagnostic_capacity_gap: 0.85,
    PHEIC_response_speed: 0.78, cross_border_health_cooperation: 0.65,
    health_financing_gap: 0.80, antimicrobial_resistance_burden: 0.72,
    zoonotic_spillover_risk: 0.70, climate_health_nexus: 0.75,
    health_inequality_structural: 0.82,
  },
  // GHS-002 — low, none
  {
    entity_id: "GHS-002", health_system_type: "système_résilient_avancé", region: "EUROPE_NORD",
    pandemic_preparedness_gap: 0.10, surveillance_system_weakness: 0.08,
    healthcare_system_resilience: 0.12, international_coordination_failure: 0.10,
    WHO_funding_adequacy: 0.08, vaccine_manufacturing_capacity: 0.10,
    supply_chain_health_vulnerability: 0.12, health_worker_shortage: 0.08,
    IHR_compliance_failure: 0.10, diagnostic_capacity_gap: 0.12,
    PHEIC_response_speed: 0.08, cross_border_health_cooperation: 0.10,
    health_financing_gap: 0.08, antimicrobial_resistance_burden: 0.12,
    zoonotic_spillover_risk: 0.10, climate_health_nexus: 0.08,
    health_inequality_structural: 0.10,
  },
  // GHS-003 — critical, international_health_governance_failure (WHO_funding>0.85, coord_failure>0.80)
  {
    entity_id: "GHS-003", health_system_type: "défaillance_gouvernance_mondiale", region: "MOYEN_ORIENT",
    pandemic_preparedness_gap: 0.72, surveillance_system_weakness: 0.70,
    healthcare_system_resilience: 0.68, international_coordination_failure: 0.88,
    WHO_funding_adequacy: 0.90, vaccine_manufacturing_capacity: 0.72,
    supply_chain_health_vulnerability: 0.75, health_worker_shortage: 0.68,
    IHR_compliance_failure: 0.80, diagnostic_capacity_gap: 0.70,
    PHEIC_response_speed: 0.78, cross_border_health_cooperation: 0.72,
    health_financing_gap: 0.70, antimicrobial_resistance_burden: 0.65,
    zoonotic_spillover_risk: 0.68, climate_health_nexus: 0.72,
    health_inequality_structural: 0.75,
  },
  // GHS-004 — moderate, none
  {
    entity_id: "GHS-004", health_system_type: "système_en_développement", region: "ASIE_SUD",
    pandemic_preparedness_gap: 0.32, surveillance_system_weakness: 0.30,
    healthcare_system_resilience: 0.28, international_coordination_failure: 0.30,
    WHO_funding_adequacy: 0.32, vaccine_manufacturing_capacity: 0.28,
    supply_chain_health_vulnerability: 0.30, health_worker_shortage: 0.32,
    IHR_compliance_failure: 0.28, diagnostic_capacity_gap: 0.30,
    PHEIC_response_speed: 0.32, cross_border_health_cooperation: 0.28,
    health_financing_gap: 0.30, antimicrobial_resistance_burden: 0.32,
    zoonotic_spillover_risk: 0.28, climate_health_nexus: 0.30,
    health_inequality_structural: 0.32,
  },
  // GHS-005 — critical, health_supply_chain_crisis (supply_chain>0.85, vaccine_manuf>0.80)
  {
    entity_id: "GHS-005", health_system_type: "crise_chaîne_approvisionnement", region: "AMERIQUE_LATINE",
    pandemic_preparedness_gap: 0.70, surveillance_system_weakness: 0.68,
    healthcare_system_resilience: 0.72, international_coordination_failure: 0.68,
    WHO_funding_adequacy: 0.70, vaccine_manufacturing_capacity: 0.88,
    supply_chain_health_vulnerability: 0.92, health_worker_shortage: 0.72,
    IHR_compliance_failure: 0.75, diagnostic_capacity_gap: 0.68,
    PHEIC_response_speed: 0.80, cross_border_health_cooperation: 0.65,
    health_financing_gap: 0.72, antimicrobial_resistance_burden: 0.68,
    zoonotic_spillover_risk: 0.70, climate_health_nexus: 0.72,
    health_inequality_structural: 0.78,
  },
  // GHS-006 — high, health_system_resilience_collapse (resilience>0.80, worker_shortage>0.75)
  {
    entity_id: "GHS-006", health_system_type: "effondrement_résilience_sanitaire", region: "EUROPE_EST",
    pandemic_preparedness_gap: 0.50, surveillance_system_weakness: 0.48,
    healthcare_system_resilience: 0.85, international_coordination_failure: 0.50,
    WHO_funding_adequacy: 0.48, vaccine_manufacturing_capacity: 0.52,
    supply_chain_health_vulnerability: 0.50, health_worker_shortage: 0.82,
    IHR_compliance_failure: 0.52, diagnostic_capacity_gap: 0.48,
    PHEIC_response_speed: 0.50, cross_border_health_cooperation: 0.52,
    health_financing_gap: 0.50, antimicrobial_resistance_burden: 0.48,
    zoonotic_spillover_risk: 0.52, climate_health_nexus: 0.50,
    health_inequality_structural: 0.52,
  },
  // GHS-007 — high, climate_zoonotic_health_nexus (climate>0.80, zoonotic>0.75)
  {
    entity_id: "GHS-007", health_system_type: "nexus_climatique_zoonotique", region: "ASIE_PACIFIQUE",
    pandemic_preparedness_gap: 0.55, surveillance_system_weakness: 0.52,
    healthcare_system_resilience: 0.50, international_coordination_failure: 0.55,
    WHO_funding_adequacy: 0.52, vaccine_manufacturing_capacity: 0.50,
    supply_chain_health_vulnerability: 0.55, health_worker_shortage: 0.52,
    IHR_compliance_failure: 0.50, diagnostic_capacity_gap: 0.55,
    PHEIC_response_speed: 0.52, cross_border_health_cooperation: 0.50,
    health_financing_gap: 0.55, antimicrobial_resistance_burden: 0.52,
    zoonotic_spillover_risk: 0.82, climate_health_nexus: 0.88,
    health_inequality_structural: 0.52,
  },
  // GHS-008 — moderate, none
  {
    entity_id: "GHS-008", health_system_type: "système_émergent_renforcé", region: "AFRIQUE_NORD",
    pandemic_preparedness_gap: 0.25, surveillance_system_weakness: 0.28,
    healthcare_system_resilience: 0.22, international_coordination_failure: 0.28,
    WHO_funding_adequacy: 0.25, vaccine_manufacturing_capacity: 0.22,
    supply_chain_health_vulnerability: 0.28, health_worker_shortage: 0.25,
    IHR_compliance_failure: 0.22, diagnostic_capacity_gap: 0.28,
    PHEIC_response_speed: 0.25, cross_border_health_cooperation: 0.22,
    health_financing_gap: 0.28, antimicrobial_resistance_burden: 0.25,
    zoonotic_spillover_risk: 0.22, climate_health_nexus: 0.28,
    health_inequality_structural: 0.25,
  },
];

type GHSInput = typeof MOCK_ENTITIES[0];

function preparednessScore(e: GHSInput): number {
  return Math.round((e.pandemic_preparedness_gap * 0.4 + e.surveillance_system_weakness * 0.35 + e.diagnostic_capacity_gap * 0.25) * 100 * 100) / 100;
}
function responseScore(e: GHSInput): number {
  return Math.round((e.PHEIC_response_speed * 0.4 + e.supply_chain_health_vulnerability * 0.35 + e.vaccine_manufacturing_capacity * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: GHSInput): number {
  return Math.round((e.IHR_compliance_failure * 0.4 + e.international_coordination_failure * 0.35 + e.WHO_funding_adequacy * 0.25) * 100 * 100) / 100;
}
function equityScore(e: GHSInput): number {
  return Math.round((e.health_inequality_structural * 0.4 + e.health_financing_gap * 0.35 + e.health_worker_shortage * 0.25) * 100 * 100) / 100;
}
function compositeScore(prep: number, resp: number, gov: number, eq: number): number {
  return Math.round((prep * 0.30 + resp * 0.25 + gov * 0.25 + eq * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function ghsPattern(e: GHSInput): string {
  if (e.pandemic_preparedness_gap > 0.85 && e.surveillance_system_weakness > 0.80) return "pandemic_preparedness_collapse";
  if (e.WHO_funding_adequacy > 0.85 && e.international_coordination_failure > 0.80) return "international_health_governance_failure";
  if (e.supply_chain_health_vulnerability > 0.85 && e.vaccine_manufacturing_capacity > 0.80) return "health_supply_chain_crisis";
  if (e.healthcare_system_resilience > 0.80 && e.health_worker_shortage > 0.75) return "health_system_resilience_collapse";
  if (e.climate_health_nexus > 0.80 && e.zoonotic_spillover_risk > 0.75) return "climate_zoonotic_health_nexus";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "effondrement_sécurité_sanitaire_mondiale";
  if (composite >= 40) return "crise_sécurité_sanitaire_majeure";
  if (composite >= 20) return "vulnérabilité_sanitaire_structurelle";
  return "sécurité_sanitaire_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgence_sanitaire_mondiale";
  if (risk === "high") return "renforcement_architecture_sanitaire_urgence";
  if (risk === "moderate") return "consolidation_systèmes_santé_structurelle";
  return "veille_sécurité_sanitaire_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Effondrement sécurité sanitaire — architecture mondiale critique";
  if (risk === "high") return "🟠 Crise sécurité sanitaire mondiale majeure détectée";
  if (risk === "moderate") return "🟡 Vulnérabilité sanitaire structurelle active";
  return "🟢 Sécurité sanitaire sous surveillance et contenue";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const prep = preparednessScore(e);
      const resp = responseScore(e);
      const gov  = governanceScore(e);
      const eq   = equityScore(e);
      const comp = compositeScore(prep, resp, gov, eq);
      const risk = riskLevel(comp);
      const pat  = ghsPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        entity_id:                  e.entity_id,
        health_system_type:         e.health_system_type,
        region:                     e.region,
        preparedness_score:         prep,
        response_score:             resp,
        governance_score:           gov,
        equity_score:               eq,
        composite_score:            comp,
        risk_level:                 risk,
        ghs_pattern:                pat,
        severity:                   sev,
        recommended_action:         action,
        signal:                     sig,
        pandemic_preparedness_gap:  e.pandemic_preparedness_gap,
        IHR_compliance_failure:     e.IHR_compliance_failure,
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
      pattern_distribution[ent.ghs_pattern]       = (pattern_distribution[ent.ghs_pattern]       || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                             382,
      module_name:                           "Global Health Security Architecture Intelligence Engine",
      total:                                 n,
      critical:                              criticalCount,
      high:                                  highCount,
      moderate:                              moderateCount,
      low:                                   lowCount,
      avg_composite:                         avgComposite,
      risk_distribution,
      pattern_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_health_security_index:   Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "global-health-security-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/global-health-security-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "global-health-security-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "global-health-security-engine"),
      { status: 502 }
    );
  }
}
