import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // NDE-001 — critical, treaty_collapse_cascade (treaty_withdrawal>0.85, verification>0.80)
  {
    entity_id: "NDE-001", actor_type: "état_nucléaire", region: "EMEA",
    npt_compliance_gap: 0.88, arsenal_modernization_rate: 0.82,
    first_strike_doctrine_risk: 0.78, tactical_weapons_proliferation: 0.75,
    verification_mechanism_failure: 0.84, treaty_withdrawal_risk: 0.90,
    nuclear_sharing_arrangement_risk: 0.72, cyber_vulnerability_command: 0.68,
    miscalculation_risk: 0.72, civilian_population_exposure: 0.76,
    nuclear_winter_contribution: 0.74, iaea_safeguard_gap: 0.78,
    disarmament_commitment_gap: 0.80, dual_use_technology_spread: 0.70,
    space_nuclear_weapon_risk: 0.65, radiological_terrorism_risk: 0.68,
    nuclear_energy_weapon_nexus: 0.72,
  },
  // NDE-002 — critical, nuclear_state_proliferation (npt_gap>0.85, tactical>0.80)
  {
    entity_id: "NDE-002", actor_type: "puissance_émergente", region: "APAC",
    npt_compliance_gap: 0.92, arsenal_modernization_rate: 0.88,
    first_strike_doctrine_risk: 0.72, tactical_weapons_proliferation: 0.86,
    verification_mechanism_failure: 0.70, treaty_withdrawal_risk: 0.75,
    nuclear_sharing_arrangement_risk: 0.68, cyber_vulnerability_command: 0.65,
    miscalculation_risk: 0.70, civilian_population_exposure: 0.74,
    nuclear_winter_contribution: 0.72, iaea_safeguard_gap: 0.80,
    disarmament_commitment_gap: 0.76, dual_use_technology_spread: 0.72,
    space_nuclear_weapon_risk: 0.60, radiological_terrorism_risk: 0.65,
    nuclear_energy_weapon_nexus: 0.68,
  },
  // NDE-003 — critical, tactical_weapon_doctrine_shift (first_strike>0.85, nuclear_sharing>0.80)
  {
    entity_id: "NDE-003", actor_type: "alliance_militaire", region: "NOAM",
    npt_compliance_gap: 0.78, arsenal_modernization_rate: 0.85,
    first_strike_doctrine_risk: 0.90, tactical_weapons_proliferation: 0.78,
    verification_mechanism_failure: 0.75, treaty_withdrawal_risk: 0.72,
    nuclear_sharing_arrangement_risk: 0.84, cyber_vulnerability_command: 0.70,
    miscalculation_risk: 0.74, civilian_population_exposure: 0.76,
    nuclear_winter_contribution: 0.72, iaea_safeguard_gap: 0.70,
    disarmament_commitment_gap: 0.74, dual_use_technology_spread: 0.68,
    space_nuclear_weapon_risk: 0.65, radiological_terrorism_risk: 0.62,
    nuclear_energy_weapon_nexus: 0.70,
  },
  // NDE-004 — high, cyber_nuclear_command_risk (cyber>0.80, miscalculation>0.75)
  {
    entity_id: "NDE-004", actor_type: "état_nucléaire", region: "LATAM",
    npt_compliance_gap: 0.52, arsenal_modernization_rate: 0.50,
    first_strike_doctrine_risk: 0.48, tactical_weapons_proliferation: 0.52,
    verification_mechanism_failure: 0.50, treaty_withdrawal_risk: 0.48,
    nuclear_sharing_arrangement_risk: 0.50, cyber_vulnerability_command: 0.84,
    miscalculation_risk: 0.80, civilian_population_exposure: 0.52,
    nuclear_winter_contribution: 0.50, iaea_safeguard_gap: 0.48,
    disarmament_commitment_gap: 0.50, dual_use_technology_spread: 0.48,
    space_nuclear_weapon_risk: 0.45, radiological_terrorism_risk: 0.50,
    nuclear_energy_weapon_nexus: 0.48,
  },
  // NDE-005 — high, humanitarian_impact_denial (civilian>0.80, nuclear_winter>0.75)
  {
    entity_id: "NDE-005", actor_type: "puissance_régionale", region: "MENA",
    npt_compliance_gap: 0.50, arsenal_modernization_rate: 0.48,
    first_strike_doctrine_risk: 0.52, tactical_weapons_proliferation: 0.48,
    verification_mechanism_failure: 0.50, treaty_withdrawal_risk: 0.52,
    nuclear_sharing_arrangement_risk: 0.48, cyber_vulnerability_command: 0.52,
    miscalculation_risk: 0.50, civilian_population_exposure: 0.85,
    nuclear_winter_contribution: 0.80, iaea_safeguard_gap: 0.50,
    disarmament_commitment_gap: 0.48, dual_use_technology_spread: 0.50,
    space_nuclear_weapon_risk: 0.45, radiological_terrorism_risk: 0.52,
    nuclear_energy_weapon_nexus: 0.50,
  },
  // NDE-006 — moderate, none
  {
    entity_id: "NDE-006", actor_type: "organisation_internationale", region: "EMEA",
    npt_compliance_gap: 0.28, arsenal_modernization_rate: 0.30,
    first_strike_doctrine_risk: 0.28, tactical_weapons_proliferation: 0.30,
    verification_mechanism_failure: 0.32, treaty_withdrawal_risk: 0.28,
    nuclear_sharing_arrangement_risk: 0.30, cyber_vulnerability_command: 0.28,
    miscalculation_risk: 0.30, civilian_population_exposure: 0.28,
    nuclear_winter_contribution: 0.30, iaea_safeguard_gap: 0.32,
    disarmament_commitment_gap: 0.28, dual_use_technology_spread: 0.30,
    space_nuclear_weapon_risk: 0.25, radiological_terrorism_risk: 0.28,
    nuclear_energy_weapon_nexus: 0.30,
  },
  // NDE-007 — low, none
  {
    entity_id: "NDE-007", actor_type: "état_non_nucléaire", region: "APAC",
    npt_compliance_gap: 0.10, arsenal_modernization_rate: 0.08,
    first_strike_doctrine_risk: 0.10, tactical_weapons_proliferation: 0.08,
    verification_mechanism_failure: 0.10, treaty_withdrawal_risk: 0.08,
    nuclear_sharing_arrangement_risk: 0.10, cyber_vulnerability_command: 0.08,
    miscalculation_risk: 0.10, civilian_population_exposure: 0.08,
    nuclear_winter_contribution: 0.10, iaea_safeguard_gap: 0.08,
    disarmament_commitment_gap: 0.10, dual_use_technology_spread: 0.08,
    space_nuclear_weapon_risk: 0.08, radiological_terrorism_risk: 0.10,
    nuclear_energy_weapon_nexus: 0.08,
  },
  // NDE-008 — low, none
  {
    entity_id: "NDE-008", actor_type: "état_non_nucléaire", region: "SSA",
    npt_compliance_gap: 0.12, arsenal_modernization_rate: 0.10,
    first_strike_doctrine_risk: 0.08, tactical_weapons_proliferation: 0.10,
    verification_mechanism_failure: 0.12, treaty_withdrawal_risk: 0.10,
    nuclear_sharing_arrangement_risk: 0.08, cyber_vulnerability_command: 0.10,
    miscalculation_risk: 0.12, civilian_population_exposure: 0.10,
    nuclear_winter_contribution: 0.08, iaea_safeguard_gap: 0.12,
    disarmament_commitment_gap: 0.10, dual_use_technology_spread: 0.08,
    space_nuclear_weapon_risk: 0.10, radiological_terrorism_risk: 0.08,
    nuclear_energy_weapon_nexus: 0.10,
  },
];

type NDEInput = typeof MOCK_ENTITIES[0];

function proliferationScore(e: NDEInput): number {
  return Math.round((e.npt_compliance_gap * 0.4 + e.tactical_weapons_proliferation * 0.35 + e.dual_use_technology_spread * 0.25) * 100 * 100) / 100;
}
function treatyScore(e: NDEInput): number {
  return Math.round((e.treaty_withdrawal_risk * 0.4 + e.verification_mechanism_failure * 0.35 + e.disarmament_commitment_gap * 0.25) * 100 * 100) / 100;
}
function deterrenceScore(e: NDEInput): number {
  return Math.round((e.first_strike_doctrine_risk * 0.4 + e.miscalculation_risk * 0.35 + e.cyber_vulnerability_command * 0.25) * 100 * 100) / 100;
}
function humanitarianScore(e: NDEInput): number {
  return Math.round((e.civilian_population_exposure * 0.4 + e.nuclear_winter_contribution * 0.35 + e.radiological_terrorism_risk * 0.25) * 100 * 100) / 100;
}
function compositeScore(pro: number, tre: number, det: number, hum: number): number {
  return Math.round((pro * 0.30 + tre * 0.25 + det * 0.25 + hum * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function nuclearPattern(e: NDEInput): string {
  if (e.treaty_withdrawal_risk > 0.85 && e.verification_mechanism_failure > 0.80) return "treaty_collapse_cascade";
  if (e.npt_compliance_gap > 0.85 && e.tactical_weapons_proliferation > 0.80) return "nuclear_state_proliferation";
  if (e.first_strike_doctrine_risk > 0.85 && e.nuclear_sharing_arrangement_risk > 0.80) return "tactical_weapon_doctrine_shift";
  if (e.cyber_vulnerability_command > 0.80 && e.miscalculation_risk > 0.75) return "cyber_nuclear_command_risk";
  if (e.civilian_population_exposure > 0.80 && e.nuclear_winter_contribution > 0.75) return "humanitarian_impact_denial";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_nucleaire_systemique_critique";
  if (composite >= 40) return "risque_proliferation_majeur";
  if (composite >= 20) return "tension_desarmement_structurelle";
  return "surveillance_controle_armements";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_desarmement_nucleaire";
  if (risk === "high") return "renforcement_traites_verification_acceleree";
  if (risk === "moderate") return "dialogue_controle_armements_renforce";
  return "veille_nucleaire_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise nucléaire systémique — désarmement en péril immédiat";
  if (risk === "high") return "🟠 Risque de prolifération majeur détecté";
  if (risk === "moderate") return "🟡 Tension structurelle contrôle des armements active";
  return "🟢 Contrôle armements sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const pro  = proliferationScore(e);
      const tre  = treatyScore(e);
      const det  = deterrenceScore(e);
      const hum  = humanitarianScore(e);
      const comp = compositeScore(pro, tre, det, hum);
      const risk = riskLevel(comp);
      const pat  = nuclearPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        entity_id:                    e.entity_id,
        actor_type:                   e.actor_type,
        region:                       e.region,
        proliferation_score:          pro,
        treaty_score:                 tre,
        deterrence_score:             det,
        humanitarian_score:           hum,
        composite_score:              comp,
        risk_level:                   risk,
        nuclear_pattern:              pat,
        severity:                     sev,
        recommended_action:           action,
        signal:                       sig,
        npt_compliance_gap:           e.npt_compliance_gap,
        iaea_safeguard_gap:           e.iaea_safeguard_gap,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tPro = 0, tTre = 0, tDet = 0, tHum = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.nuclear_pattern]   = (pattern_distribution[ent.nuclear_pattern]   || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tPro  += ent.proliferation_score;
      tTre  += ent.treaty_score;
      tDet  += ent.deterrence_score;
      tHum  += ent.humanitarian_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite       = Math.round(tComp / n * 10) / 10;
    const avgProliferation   = Math.round(tPro  / n * 10) / 10;

    const summary = {
      module_id:                             438,
      module_name:                           "Désarmement Nucléaire & Contrôle des Armements Intelligence Engine",
      total:                                 n,
      critical:                              criticalCount,
      high:                                  highCount,
      moderate:                              moderateCount,
      low:                                   lowCount,
      avg_composite:                         avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_nuclear_risk_index:      Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, avg_proliferation: avgProliferation }, "nuclear-disarmament-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/nuclear-disarmament-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "nuclear-disarmament-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream indisponible", code: 502 }, "nuclear-disarmament-engine"),
      { status: 502 }
    );
  }
}
