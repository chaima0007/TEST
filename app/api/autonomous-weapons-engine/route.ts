import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  // AWE-001 — critical, accountability_vacuum_crisis (human_control_removal>0.85, legal_accountability_gap>0.80)
  {
    id: "AWE-001", system_type: "lethal_autonomous_drone", region: "MENA",
    human_control_removal: 0.92, legal_accountability_gap: 0.88,
    civilian_discrimination_failure: 0.72, proportionality_compliance: 0.18,
    targeting_algorithm_bias: 0.70, proliferation_risk: 0.68,
    treaty_compliance: 0.20, export_control_effectiveness: 0.25,
    arms_race_intensity: 0.70, ngo_oversight_access: 0.15,
    incident_transparency: 0.18, review_mechanism_quality: 0.20,
    international_law_compliance: 0.18, dual_use_risk: 0.72,
    small_state_deployment: 0.65, non_state_actor_access: 0.68,
    autonomous_escalation_risk: 0.75,
  },
  // AWE-002 — critical, civilian_harm_discrimination_failure (civ_discrim>0.85, 1-prop_compliance>0.80)
  {
    id: "AWE-002", system_type: "autonomous_targeting_system", region: "SSA",
    human_control_removal: 0.75, legal_accountability_gap: 0.78,
    civilian_discrimination_failure: 0.90, proportionality_compliance: 0.12,
    targeting_algorithm_bias: 0.82, proliferation_risk: 0.70,
    treaty_compliance: 0.22, export_control_effectiveness: 0.28,
    arms_race_intensity: 0.72, ngo_oversight_access: 0.18,
    incident_transparency: 0.20, review_mechanism_quality: 0.22,
    international_law_compliance: 0.20, dual_use_risk: 0.68,
    small_state_deployment: 0.70, non_state_actor_access: 0.65,
    autonomous_escalation_risk: 0.78,
  },
  // AWE-003 — critical, arms_race_proliferation (prolif_risk>0.85, non_state_actor_access>0.80)
  {
    id: "AWE-003", system_type: "swarm_weapons_system", region: "APAC",
    human_control_removal: 0.70, legal_accountability_gap: 0.65,
    civilian_discrimination_failure: 0.68, proportionality_compliance: 0.22,
    targeting_algorithm_bias: 0.68, proliferation_risk: 0.90,
    treaty_compliance: 0.25, export_control_effectiveness: 0.20,
    arms_race_intensity: 0.85, ngo_oversight_access: 0.20,
    incident_transparency: 0.22, review_mechanism_quality: 0.18,
    international_law_compliance: 0.22, dual_use_risk: 0.80,
    small_state_deployment: 0.75, non_state_actor_access: 0.85,
    autonomous_escalation_risk: 0.80,
  },
  // AWE-004 — high, treaty_governance_collapse (1-treaty_compliance>0.80, 1-intl_law>0.75)
  {
    id: "AWE-004", system_type: "robotic_combat_vehicle", region: "EMEA",
    human_control_removal: 0.55, legal_accountability_gap: 0.52,
    civilian_discrimination_failure: 0.50, proportionality_compliance: 0.45,
    targeting_algorithm_bias: 0.50, proliferation_risk: 0.52,
    treaty_compliance: 0.15, export_control_effectiveness: 0.45,
    arms_race_intensity: 0.52, ngo_oversight_access: 0.45,
    incident_transparency: 0.48, review_mechanism_quality: 0.45,
    international_law_compliance: 0.20, dual_use_risk: 0.52,
    small_state_deployment: 0.50, non_state_actor_access: 0.48,
    autonomous_escalation_risk: 0.52,
  },
  // AWE-005 — high, algorithmic_bias_targeting (targeting_bias>0.80, escalation_risk>0.75)
  {
    id: "AWE-005", system_type: "ai_surveillance_strike_system", region: "LATAM",
    human_control_removal: 0.50, legal_accountability_gap: 0.52,
    civilian_discrimination_failure: 0.55, proportionality_compliance: 0.42,
    targeting_algorithm_bias: 0.85, proliferation_risk: 0.48,
    treaty_compliance: 0.40, export_control_effectiveness: 0.42,
    arms_race_intensity: 0.48, ngo_oversight_access: 0.40,
    incident_transparency: 0.42, review_mechanism_quality: 0.40,
    international_law_compliance: 0.42, dual_use_risk: 0.48,
    small_state_deployment: 0.45, non_state_actor_access: 0.42,
    autonomous_escalation_risk: 0.80,
  },
  // AWE-006 — moderate, none
  {
    id: "AWE-006", system_type: "semi_autonomous_patrol_drone", region: "NOAM",
    human_control_removal: 0.28, legal_accountability_gap: 0.30,
    civilian_discrimination_failure: 0.30, proportionality_compliance: 0.68,
    targeting_algorithm_bias: 0.30, proliferation_risk: 0.28,
    treaty_compliance: 0.68, export_control_effectiveness: 0.65,
    arms_race_intensity: 0.28, ngo_oversight_access: 0.62,
    incident_transparency: 0.60, review_mechanism_quality: 0.65,
    international_law_compliance: 0.65, dual_use_risk: 0.28,
    small_state_deployment: 0.25, non_state_actor_access: 0.28,
    autonomous_escalation_risk: 0.30,
  },
  // AWE-007 — low, none
  {
    id: "AWE-007", system_type: "remote_controlled_bomb_disposal", region: "EMEA",
    human_control_removal: 0.08, legal_accountability_gap: 0.10,
    civilian_discrimination_failure: 0.10, proportionality_compliance: 0.92,
    targeting_algorithm_bias: 0.10, proliferation_risk: 0.08,
    treaty_compliance: 0.90, export_control_effectiveness: 0.88,
    arms_race_intensity: 0.08, ngo_oversight_access: 0.85,
    incident_transparency: 0.88, review_mechanism_quality: 0.90,
    international_law_compliance: 0.90, dual_use_risk: 0.10,
    small_state_deployment: 0.08, non_state_actor_access: 0.08,
    autonomous_escalation_risk: 0.08,
  },
  // AWE-008 — low, none
  {
    id: "AWE-008", system_type: "supervised_border_surveillance", region: "NOAM",
    human_control_removal: 0.10, legal_accountability_gap: 0.12,
    civilian_discrimination_failure: 0.12, proportionality_compliance: 0.88,
    targeting_algorithm_bias: 0.12, proliferation_risk: 0.10,
    treaty_compliance: 0.88, export_control_effectiveness: 0.85,
    arms_race_intensity: 0.10, ngo_oversight_access: 0.82,
    incident_transparency: 0.85, review_mechanism_quality: 0.88,
    international_law_compliance: 0.88, dual_use_risk: 0.12,
    small_state_deployment: 0.10, non_state_actor_access: 0.10,
    autonomous_escalation_risk: 0.10,
  },
];

type AWEInput = typeof MOCK_ENTITIES[0];

function accountabilityScore(e: AWEInput): number {
  return Math.round((e.human_control_removal * 0.5 + e.legal_accountability_gap * 0.5) * 100 * 100) / 100;
}
function legalScore(e: AWEInput): number {
  return Math.round((
    e.civilian_discrimination_failure * 0.35
    + (1 - e.proportionality_compliance) * 0.25
    + (1 - e.international_law_compliance) * 0.25
    + (1 - e.treaty_compliance) * 0.15
  ) * 100 * 100) / 100;
}
function proliferationScore(e: AWEInput): number {
  return Math.round((
    e.proliferation_risk * 0.25
    + e.arms_race_intensity * 0.20
    + e.dual_use_risk * 0.20
    + e.small_state_deployment * 0.15
    + e.non_state_actor_access * 0.15
    + (1 - e.export_control_effectiveness) * 0.05
  ) * 100 * 100) / 100;
}
function biasScore(e: AWEInput): number {
  return Math.round((
    e.targeting_algorithm_bias * 0.40
    + e.autonomous_escalation_risk * 0.30
    + (1 - e.ngo_oversight_access) * 0.15
    + (1 - e.incident_transparency) * 0.10
    + (1 - e.review_mechanism_quality) * 0.05
  ) * 100 * 100) / 100;
}
function compositeScore(acc: number, leg: number, pro: number, bia: number): number {
  return Math.round((acc * 0.30 + leg * 0.25 + pro * 0.25 + bia * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function weaponsPattern(e: AWEInput): string {
  if (e.human_control_removal > 0.85 && e.legal_accountability_gap > 0.80) return "accountability_vacuum_crisis";
  if (e.civilian_discrimination_failure > 0.85 && (1 - e.proportionality_compliance) > 0.80) return "civilian_harm_discrimination_failure";
  if (e.proliferation_risk > 0.85 && e.non_state_actor_access > 0.80) return "arms_race_proliferation";
  if ((1 - e.treaty_compliance) > 0.80 && (1 - e.international_law_compliance) > 0.75) return "treaty_governance_collapse";
  if (e.targeting_algorithm_bias > 0.80 && e.autonomous_escalation_risk > 0.75) return "algorithmic_bias_targeting";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_gouvernance_létale_systémique";
  if (composite >= 40) return "crise_prolifération_armes_autonomes_majeure";
  if (composite >= 20) return "risque_biais_algorithmique_structurel";
  return "surveillance_gouvernance_armes_ia";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_contrôle_armes_létales_ia";
  if (risk === "high") return "renforcement_traités_non_prolifération_systèmes_autonomes";
  if (risk === "moderate") return "révision_mécanismes_supervision_humaine_ia";
  return "veille_gouvernance_armes_autonomes_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise gouvernance létale systémique — contrôle humain en péril";
  if (risk === "high") return "🟠 Crise prolifération armes autonomes majeure détectée";
  if (risk === "moderate") return "🟡 Risque biais algorithmique structurel actif";
  return "🟢 Surveillance gouvernance armes IA continue";
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const acc  = accountabilityScore(e);
      const leg  = legalScore(e);
      const pro  = proliferationScore(e);
      const bia  = biasScore(e);
      const comp = compositeScore(acc, leg, pro, bia);
      const risk = riskLevel(comp);
      const pat  = weaponsPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:              e.entity_id,
        system_type:            e.system_type,
        region:                 e.region,
        accountability_score:   acc,
        legal_score:            leg,
        proliferation_score:    pro,
        bias_score:             bia,
        composite_score:        comp,
        risk_level:             risk,
        weapons_pattern:        pat,
        severity:               sev,
        recommended_action:     action,
        signal:                 sig,
        human_control_removal:  e.human_control_removal,
        proliferation_risk:     e.proliferation_risk,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tAcc = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.weapons_pattern]   = (pattern_distribution[ent.weapons_pattern]   || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tAcc  += ent.accountability_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;
    const avgAccountability = Math.round(tAcc / n * 10) / 10;

    const summary = {
      module_id:                                406,
      module_name:                              "Autonomous Weapons & Lethal AI Governance Intelligence Engine",
      total:                                    n,
      critical:                                 criticalCount,
      high:                                     highCount,
      moderate:                                 moderateCount,
      low:                                      lowCount,
      avg_composite:                            avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_lethal_ai_governance_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, avg_accountability: avgAccountability } as Record<string, unknown>)
    );
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/autonomous-weapons-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(sealResponse(await res.json()));
  } catch {}
  return NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 });
}
