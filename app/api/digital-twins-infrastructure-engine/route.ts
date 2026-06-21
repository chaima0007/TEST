import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  // DTI-001 — critical / twin_divergence_catastrophe
  {
    id: "DTI-001", twin_domain: "smart_city", region: "EMEA",
    digital_physical_synchronization_gap: 0.85, twin_data_integrity_risk: 0.78,
    adversarial_twin_manipulation_risk: 0.72, twin_sovereignty_capture_index: 0.55,
    real_time_feedback_latency_risk: 0.80, twin_divergence_crisis_probability: 0.82,
    proprietary_lock_in_twin_vendor: 0.50, simulation_accuracy_degradation: 0.65,
    cascading_twin_failure_risk: 0.60, AI_decision_twin_autonomy_risk: 0.65,
    twin_cybersecurity_vulnerability: 0.68, physical_dependency_on_twin_decisions: 0.60,
    twin_data_monopoly_concentration: 0.45, regulatory_twin_gap: 0.60,
    twin_workforce_displacement: 0.45, cross_sector_twin_interdependency: 0.50,
    emergency_twin_override_capability: 0.55,
  },
  // DTI-002 — low / none
  {
    id: "DTI-002", twin_domain: "manufacturing", region: "NAMER",
    digital_physical_synchronization_gap: 0.10, twin_data_integrity_risk: 0.08,
    adversarial_twin_manipulation_risk: 0.12, twin_sovereignty_capture_index: 0.10,
    real_time_feedback_latency_risk: 0.08, twin_divergence_crisis_probability: 0.09,
    proprietary_lock_in_twin_vendor: 0.15, simulation_accuracy_degradation: 0.10,
    cascading_twin_failure_risk: 0.08, AI_decision_twin_autonomy_risk: 0.10,
    twin_cybersecurity_vulnerability: 0.12, physical_dependency_on_twin_decisions: 0.10,
    twin_data_monopoly_concentration: 0.08, regulatory_twin_gap: 0.12,
    twin_workforce_displacement: 0.10, cross_sector_twin_interdependency: 0.09,
    emergency_twin_override_capability: 0.90,
  },
  // DTI-003 — high / adversarial_twin_attack
  {
    id: "DTI-003", twin_domain: "energy_grid", region: "APAC",
    digital_physical_synchronization_gap: 0.42, twin_data_integrity_risk: 0.55,
    adversarial_twin_manipulation_risk: 0.78, twin_sovereignty_capture_index: 0.48,
    real_time_feedback_latency_risk: 0.40, twin_divergence_crisis_probability: 0.38,
    proprietary_lock_in_twin_vendor: 0.42, simulation_accuracy_degradation: 0.50,
    cascading_twin_failure_risk: 0.45, AI_decision_twin_autonomy_risk: 0.55,
    twin_cybersecurity_vulnerability: 0.72, physical_dependency_on_twin_decisions: 0.45,
    twin_data_monopoly_concentration: 0.40, regulatory_twin_gap: 0.50,
    twin_workforce_displacement: 0.35, cross_sector_twin_interdependency: 0.42,
    emergency_twin_override_capability: 0.60,
  },
  // DTI-004 — low / none
  {
    id: "DTI-004", twin_domain: "logistics", region: "LATAM",
    digital_physical_synchronization_gap: 0.12, twin_data_integrity_risk: 0.10,
    adversarial_twin_manipulation_risk: 0.08, twin_sovereignty_capture_index: 0.12,
    real_time_feedback_latency_risk: 0.10, twin_divergence_crisis_probability: 0.09,
    proprietary_lock_in_twin_vendor: 0.10, simulation_accuracy_degradation: 0.08,
    cascading_twin_failure_risk: 0.10, AI_decision_twin_autonomy_risk: 0.12,
    twin_cybersecurity_vulnerability: 0.10, physical_dependency_on_twin_decisions: 0.08,
    twin_data_monopoly_concentration: 0.10, regulatory_twin_gap: 0.15,
    twin_workforce_displacement: 0.12, cross_sector_twin_interdependency: 0.08,
    emergency_twin_override_capability: 0.88,
  },
  // DTI-005 — critical / cascading_twin_collapse
  {
    id: "DTI-005", twin_domain: "healthcare_infrastructure", region: "EMEA",
    digital_physical_synchronization_gap: 0.62, twin_data_integrity_risk: 0.70,
    adversarial_twin_manipulation_risk: 0.55, twin_sovereignty_capture_index: 0.60,
    real_time_feedback_latency_risk: 0.58, twin_divergence_crisis_probability: 0.60,
    proprietary_lock_in_twin_vendor: 0.58, simulation_accuracy_degradation: 0.65,
    cascading_twin_failure_risk: 0.82, AI_decision_twin_autonomy_risk: 0.60,
    twin_cybersecurity_vulnerability: 0.62, physical_dependency_on_twin_decisions: 0.65,
    twin_data_monopoly_concentration: 0.55, regulatory_twin_gap: 0.70,
    twin_workforce_displacement: 0.58, cross_sector_twin_interdependency: 0.78,
    emergency_twin_override_capability: 0.40,
  },
  // DTI-006 — moderate / none
  {
    id: "DTI-006", twin_domain: "transportation", region: "MEA",
    digital_physical_synchronization_gap: 0.32, twin_data_integrity_risk: 0.28,
    adversarial_twin_manipulation_risk: 0.30, twin_sovereignty_capture_index: 0.35,
    real_time_feedback_latency_risk: 0.28, twin_divergence_crisis_probability: 0.30,
    proprietary_lock_in_twin_vendor: 0.32, simulation_accuracy_degradation: 0.35,
    cascading_twin_failure_risk: 0.28, AI_decision_twin_autonomy_risk: 0.30,
    twin_cybersecurity_vulnerability: 0.32, physical_dependency_on_twin_decisions: 0.30,
    twin_data_monopoly_concentration: 0.28, regulatory_twin_gap: 0.35,
    twin_workforce_displacement: 0.30, cross_sector_twin_interdependency: 0.28,
    emergency_twin_override_capability: 0.68,
  },
  // DTI-007 — high / twin_vendor_monopoly
  {
    id: "DTI-007", twin_domain: "financial_markets", region: "NAMER",
    digital_physical_synchronization_gap: 0.45, twin_data_integrity_risk: 0.52,
    adversarial_twin_manipulation_risk: 0.42, twin_sovereignty_capture_index: 0.60,
    real_time_feedback_latency_risk: 0.40, twin_divergence_crisis_probability: 0.38,
    proprietary_lock_in_twin_vendor: 0.82, simulation_accuracy_degradation: 0.50,
    cascading_twin_failure_risk: 0.45, AI_decision_twin_autonomy_risk: 0.48,
    twin_cybersecurity_vulnerability: 0.42, physical_dependency_on_twin_decisions: 0.50,
    twin_data_monopoly_concentration: 0.75, regulatory_twin_gap: 0.58,
    twin_workforce_displacement: 0.50, cross_sector_twin_interdependency: 0.48,
    emergency_twin_override_capability: 0.55,
  },
  // DTI-008 — critical / physical_twin_lock
  {
    id: "DTI-008", twin_domain: "nuclear_facility", region: "EMEA",
    digital_physical_synchronization_gap: 0.58, twin_data_integrity_risk: 0.65,
    adversarial_twin_manipulation_risk: 0.60, twin_sovereignty_capture_index: 0.65,
    real_time_feedback_latency_risk: 0.62, twin_divergence_crisis_probability: 0.55,
    proprietary_lock_in_twin_vendor: 0.62, simulation_accuracy_degradation: 0.68,
    cascading_twin_failure_risk: 0.60, AI_decision_twin_autonomy_risk: 0.65,
    twin_cybersecurity_vulnerability: 0.62, physical_dependency_on_twin_decisions: 0.88,
    twin_data_monopoly_concentration: 0.58, regulatory_twin_gap: 0.70,
    twin_workforce_displacement: 0.60, cross_sector_twin_interdependency: 0.60,
    emergency_twin_override_capability: 0.18,
  },
];

type DTIEntity = typeof MOCK_ENTITIES[0];

function syncScore(e: DTIEntity): number {
  const v = (e.digital_physical_synchronization_gap * 0.40
    + e.twin_divergence_crisis_probability * 0.35
    + e.real_time_feedback_latency_risk * 0.25) * 100;
  return Math.min(Math.round(v * 100) / 100, 100);
}
function securityScore(e: DTIEntity): number {
  const v = (e.adversarial_twin_manipulation_risk * 0.40
    + e.twin_cybersecurity_vulnerability * 0.35
    + e.AI_decision_twin_autonomy_risk * 0.25) * 100;
  return Math.min(Math.round(v * 100) / 100, 100);
}
function dependencyScore(e: DTIEntity): number {
  const v = (e.physical_dependency_on_twin_decisions * 0.40
    + e.cascading_twin_failure_risk * 0.35
    + e.cross_sector_twin_interdependency * 0.25) * 100;
  return Math.min(Math.round(v * 100) / 100, 100);
}
function sovereigntyScore(e: DTIEntity): number {
  const v = (e.twin_sovereignty_capture_index * 0.40
    + e.proprietary_lock_in_twin_vendor * 0.35
    + e.twin_data_monopoly_concentration * 0.25) * 100;
  return Math.min(Math.round(v * 100) / 100, 100);
}
function compositeScore(sync: number, sec: number, dep: number, sov: number): number {
  return Math.min(Math.round((sync * 0.30 + sec * 0.25 + dep * 0.25 + sov * 0.20) * 100) / 100, 100);
}
function twinPattern(e: DTIEntity): string {
  if (e.digital_physical_synchronization_gap >= 0.70 && e.twin_divergence_crisis_probability >= 0.65)
    return "twin_divergence_catastrophe";
  if (e.adversarial_twin_manipulation_risk >= 0.70 && e.twin_cybersecurity_vulnerability >= 0.65)
    return "adversarial_twin_attack";
  if (e.physical_dependency_on_twin_decisions >= 0.70 && e.emergency_twin_override_capability <= 0.35)
    return "physical_twin_lock";
  if (e.proprietary_lock_in_twin_vendor >= 0.70 && e.twin_data_monopoly_concentration >= 0.65)
    return "twin_vendor_monopoly";
  if (e.cascading_twin_failure_risk >= 0.70 && e.cross_sector_twin_interdependency >= 0.65)
    return "cascading_twin_collapse";
  return "none";
}
function riskLevel(c: number): string {
  if (c >= 60) return "critical";
  if (c >= 40) return "high";
  if (c >= 20) return "moderate";
  return "low";
}
function severity(r: string): string {
  if (r === "critical")  return "effondrement_jumeau_numérique_critique";
  if (r === "high")      return "crise_infrastructure_jumeau_majeure";
  if (r === "moderate")  return "fragilité_jumeau_numérique_structurelle";
  return "jumeau_numérique_stable";
}
function recommendedAction(r: string): string {
  if (r === "critical")  return "intervention_urgente_résilience_jumeau";
  if (r === "high")      return "sécurisation_accélérée_infrastructure_jumeau";
  if (r === "moderate")  return "renforcement_indépendance_jumeau_numérique";
  return "veille_jumeau_numérique_continue";
}
function signal(r: string): string {
  if (r === "critical")  return "🔴 Effondrement jumeau numérique — infrastructure critique compromise";
  if (r === "high")      return "🟠 Crise infrastructure jumeau majeure détectée";
  if (r === "moderate")  return "🟡 Fragilité jumeau numérique structurelle active";
  return "🟢 Infrastructure jumeau numérique stable";
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const sync = syncScore(e), sec = securityScore(e);
      const dep = dependencyScore(e), sov = sovereigntyScore(e);
      const comp = compositeScore(sync, sec, dep, sov);
      const pat = twinPattern(e), r = riskLevel(comp);
      return {
        id: e.entity_id, twin_domain: e.twin_domain, region: e.region,
        sync_score: sync, security_score: sec,
        dependency_score: dep, sovereignty_score: sov,
        composite_score: comp, risk_level: r,
        twin_pattern: pat, severity: severity(r),
        recommended_action: recommendedAction(r),
        signal: signal(r),
        digital_physical_synchronization_gap: e.digital_physical_synchronization_gap,
        adversarial_twin_manipulation_risk: e.adversarial_twin_manipulation_risk,
      };
    });

    const patDist: Record<string, number> = {};
    const riskDist: Record<string, number> = {};
    const sevDist: Record<string, number> = {};
    const actDist: Record<string, number> = {};
    let totalComp = 0, critC = 0, highC = 0, modC = 0, lowC = 0;
    for (const ent of entities) {
      patDist[ent.twin_pattern]       = (patDist[ent.twin_pattern] || 0) + 1;
      riskDist[ent.risk_level]        = (riskDist[ent.risk_level] || 0) + 1;
      sevDist[ent.severity]           = (sevDist[ent.severity] || 0) + 1;
      actDist[ent.recommended_action] = (actDist[ent.recommended_action] || 0) + 1;
      totalComp += ent.composite_score;
      if (ent.risk_level === "critical")       critC++;
      else if (ent.risk_level === "high")      highC++;
      else if (ent.risk_level === "moderate")  modC++;
      else                                     lowC++;
    }
    const n = entities.length;
    const avgComp = Math.round((totalComp / n) * 10) / 10;

    const summaryData = {
      module_id: 353,
      module_name: "Digital Twins & Physical-Digital Infrastructure Intelligence Engine",
      total_entities: n,
      critical_count: critC,
      high_count: highC,
      moderate_count: modC,
      low_count: lowC,
      avg_composite: avgComp,
      pattern_distribution: patDist,
      risk_distribution: riskDist,
      severity_distribution: sevDist,
      action_distribution: actDist,
      avg_estimated_twin_risk_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary: summaryData as Record<string, unknown> }, "digital-twins-infrastructure-engine") as Parameters<typeof NextResponse.json>[0]
    );
  }

  try {
    const upstream = await fetch(`${SWARM_API_URL}/digital-twins-infrastructure-engine`);
    const data = await upstream.json();
    return NextResponse.json(
      sealResponse(data, "digital-twins-infrastructure-engine") as Parameters<typeof NextResponse.json>[0]
    );
  } catch {
    return NextResponse.json({ error: "upstream unavailable" }, { status: 502 });
  }
}
