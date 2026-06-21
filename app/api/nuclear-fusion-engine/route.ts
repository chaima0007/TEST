import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // NFE-001 — tokamak_program, APAC → critical, fusion_supremacy_race
  {
    id: "NFE-001", fusion_program: "tokamak_program", region: "APAC",
    technological_lead: 0.92, tritium_supply_control: 0.70,
    plasma_confinement_advantage: 0.88, fusion_patent_monopoly: 0.75,
    rare_material_access: 0.68, commercial_deployment_speed: 0.72,
    military_fusion_application: 0.60, geopolitical_leverage_gain: 0.78,
    ITER_dependency: 0.45, private_fusion_dominance: 0.55,
    IP_theft_vulnerability: 0.50, fusion_standards_capture: 0.72,
    energy_independence_threat: 0.80, proliferation_risk: 0.55,
    workforce_concentration: 0.70, supply_chain_dominance: 0.68,
    first_mover_advantage: 0.86,
  },
  // NFE-002 — inertial_confinement, LATAM → low, none
  {
    id: "NFE-002", fusion_program: "inertial_confinement", region: "LATAM",
    technological_lead: 0.18, tritium_supply_control: 0.15,
    plasma_confinement_advantage: 0.12, fusion_patent_monopoly: 0.10,
    rare_material_access: 0.14, commercial_deployment_speed: 0.12,
    military_fusion_application: 0.10, geopolitical_leverage_gain: 0.15,
    ITER_dependency: 0.80, private_fusion_dominance: 0.10,
    IP_theft_vulnerability: 0.12, fusion_standards_capture: 0.10,
    energy_independence_threat: 0.08, proliferation_risk: 0.12,
    workforce_concentration: 0.15, supply_chain_dominance: 0.10,
    first_mover_advantage: 0.12,
  },
  // NFE-003 — tritium_breeder_reactor, EMEA → high, tritium_geopolitical_weapon
  {
    id: "NFE-003", fusion_program: "tritium_breeder_reactor", region: "EMEA",
    technological_lead: 0.42, tritium_supply_control: 0.88,
    plasma_confinement_advantage: 0.38, fusion_patent_monopoly: 0.45,
    rare_material_access: 0.82, commercial_deployment_speed: 0.38,
    military_fusion_application: 0.35, geopolitical_leverage_gain: 0.50,
    ITER_dependency: 0.55, private_fusion_dominance: 0.35,
    IP_theft_vulnerability: 0.40, fusion_standards_capture: 0.48,
    energy_independence_threat: 0.52, proliferation_risk: 0.38,
    workforce_concentration: 0.42, supply_chain_dominance: 0.40,
    first_mover_advantage: 0.38,
  },
  // NFE-004 — stellarator_research, NOAM → low, none
  {
    id: "NFE-004", fusion_program: "stellarator_research", region: "NOAM",
    technological_lead: 0.20, tritium_supply_control: 0.18,
    plasma_confinement_advantage: 0.15, fusion_patent_monopoly: 0.12,
    rare_material_access: 0.16, commercial_deployment_speed: 0.14,
    military_fusion_application: 0.12, geopolitical_leverage_gain: 0.18,
    ITER_dependency: 0.75, private_fusion_dominance: 0.15,
    IP_theft_vulnerability: 0.14, fusion_standards_capture: 0.12,
    energy_independence_threat: 0.10, proliferation_risk: 0.14,
    workforce_concentration: 0.18, supply_chain_dominance: 0.12,
    first_mover_advantage: 0.14,
  },
  // NFE-005 — patent_portfolio_fusion, APAC → critical, fusion_IP_monopoly_capture
  {
    id: "NFE-005", fusion_program: "patent_portfolio_fusion", region: "APAC",
    technological_lead: 0.75, tritium_supply_control: 0.65,
    plasma_confinement_advantage: 0.70, fusion_patent_monopoly: 0.92,
    rare_material_access: 0.60, commercial_deployment_speed: 0.68,
    military_fusion_application: 0.55, geopolitical_leverage_gain: 0.75,
    ITER_dependency: 0.35, private_fusion_dominance: 0.65,
    IP_theft_vulnerability: 0.82, fusion_standards_capture: 0.78,
    energy_independence_threat: 0.70, proliferation_risk: 0.60,
    workforce_concentration: 0.72, supply_chain_dominance: 0.65,
    first_mover_advantage: 0.70,
  },
  // NFE-006 — private_commercial_fusion, NOAM → critical, private_fusion_disruption
  {
    id: "NFE-006", fusion_program: "private_commercial_fusion", region: "NOAM",
    technological_lead: 0.72, tritium_supply_control: 0.60,
    plasma_confinement_advantage: 0.68, fusion_patent_monopoly: 0.70,
    rare_material_access: 0.62, commercial_deployment_speed: 0.88,
    military_fusion_application: 0.50, geopolitical_leverage_gain: 0.70,
    ITER_dependency: 0.20, private_fusion_dominance: 0.85,
    IP_theft_vulnerability: 0.55, fusion_standards_capture: 0.72,
    energy_independence_threat: 0.75, proliferation_risk: 0.48,
    workforce_concentration: 0.65, supply_chain_dominance: 0.68,
    first_mover_advantage: 0.75,
  },
  // NFE-007 — military_fusion_program, MEA → moderate, none
  {
    id: "NFE-007", fusion_program: "military_fusion_program", region: "MEA",
    technological_lead: 0.38, tritium_supply_control: 0.35,
    plasma_confinement_advantage: 0.32, fusion_patent_monopoly: 0.30,
    rare_material_access: 0.38, commercial_deployment_speed: 0.28,
    military_fusion_application: 0.42, geopolitical_leverage_gain: 0.35,
    ITER_dependency: 0.60, private_fusion_dominance: 0.25,
    IP_theft_vulnerability: 0.30, fusion_standards_capture: 0.32,
    energy_independence_threat: 0.38, proliferation_risk: 0.40,
    workforce_concentration: 0.35, supply_chain_dominance: 0.30,
    first_mover_advantage: 0.28,
  },
  // NFE-008 — dual_use_fusion_weapons, EMEA → critical, fusion_proliferation_crisis
  {
    id: "NFE-008", fusion_program: "dual_use_fusion_weapons", region: "EMEA",
    technological_lead: 0.78, tritium_supply_control: 0.72,
    plasma_confinement_advantage: 0.75, fusion_patent_monopoly: 0.68,
    rare_material_access: 0.70, commercial_deployment_speed: 0.65,
    military_fusion_application: 0.88, geopolitical_leverage_gain: 0.80,
    ITER_dependency: 0.30, private_fusion_dominance: 0.60,
    IP_theft_vulnerability: 0.65, fusion_standards_capture: 0.75,
    energy_independence_threat: 0.72, proliferation_risk: 0.92,
    workforce_concentration: 0.68, supply_chain_dominance: 0.72,
    first_mover_advantage: 0.70,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function dominanceScore(e: Entity): number {
  const raw = (
    e.technological_lead * 0.40
    + e.plasma_confinement_advantage * 0.35
    + e.first_mover_advantage * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function supplyScore(e: Entity): number {
  const raw = (
    e.tritium_supply_control * 0.40
    + e.rare_material_access * 0.35
    + e.supply_chain_dominance * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function geopoliticalScore(e: Entity): number {
  const raw = (
    e.geopolitical_leverage_gain * 0.40
    + e.fusion_standards_capture * 0.35
    + e.energy_independence_threat * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function riskScore(e: Entity): number {
  const raw = (
    e.proliferation_risk * 0.40
    + e.IP_theft_vulnerability * 0.35
    + e.workforce_concentration * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(dom: number, sup: number, geo: number, risk: number): number {
  return Math.round((dom * 0.30 + sup * 0.25 + geo * 0.25 + risk * 0.20) * 100) / 100;
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function fusionPattern(e: Entity): string {
  if (e.technological_lead > 0.85 && e.first_mover_advantage > 0.80) return "fusion_supremacy_race";
  if (e.tritium_supply_control > 0.85 && e.rare_material_access > 0.80) return "tritium_geopolitical_weapon";
  if (e.fusion_patent_monopoly > 0.85 && e.IP_theft_vulnerability > 0.70) return "fusion_IP_monopoly_capture";
  if (e.private_fusion_dominance > 0.80 && e.commercial_deployment_speed > 0.75) return "private_fusion_disruption";
  if (e.proliferation_risk > 0.80 && e.military_fusion_application > 0.75) return "fusion_proliferation_crisis";
  return "none";
}

function severity(comp: number): string {
  if (comp >= 60) return "crise_fusion_géopolitique_systémique";
  if (comp >= 40) return "domination_fusion_stratégique_majeure";
  if (comp >= 20) return "tension_course_fusion_nucléaire";
  return "programme_fusion_sous_surveillance";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_course_fusion_nucléaire";
  if (risk === "high")     return "containment_stratégique_programme_fusion";
  if (risk === "moderate") return "surveillance_renforcée_géopolitique_fusion";
  return "veille_fusion_nucléaire_continue";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise fusion géopolitique systémique — domination technologique extrême";
  if (risk === "high")     return "🟠 Domination fusion stratégique majeure détectée";
  if (risk === "moderate") return "🟡 Tension course fusion nucléaire active";
  return "🟢 Programme fusion nucléaire sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const dom   = dominanceScore(e);
      const sup   = supplyScore(e);
      const geo   = geopoliticalScore(e);
      const risk  = riskScore(e);
      const comp  = compositeScore(dom, sup, geo, risk);
      const rl    = riskLevel(comp);
      const pat   = fusionPattern(e);
      const sev   = severity(comp);
      const act   = recommendedAction(rl);
      const sig   = signal(rl);

      return {
        id:               e.entity_id,
        fusion_program:          e.fusion_program,
        region:                  e.region,
        dominance_score:         dom,
        supply_score:            sup,
        geopolitical_score:      geo,
        risk_score:              risk,
        composite_score:         comp,
        risk_level:              rl,
        fusion_pattern:          pat,
        severity:                sev,
        recommended_action:      act,
        signal:                  sig,
        technological_lead:      e.technological_lead,
        proliferation_risk:      e.proliferation_risk,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      rc[ent.risk_level]        = (rc[ent.risk_level]        || 0) + 1;
      pc[ent.fusion_pattern]    = (pc[ent.fusion_pattern]    || 0) + 1;
      sc[ent.severity]          = (sc[ent.severity]          || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                            373,
      module_name:                          "Nuclear Fusion Energy Race & Geopolitics Intelligence Engine",
      total:                                n,
      critical:                             criticalCount,
      high:                                 highCount,
      moderate:                             moderateCount,
      low:                                  lowCount,
      avg_composite:                        avgComposite,
      pattern_distribution:                 pc,
      risk_distribution:                    rc,
      severity_distribution:                sc,
      action_distribution:                  ac,
      avg_estimated_fusion_dominance_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "nuclear-fusion-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/nuclear-fusion-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "nuclear-fusion-engine"));
  } catch {
    return NextResponse.json(sealResponse({ error: "Upstream unavailable" }, "nuclear-fusion-engine"), { status: 502 });
  }
}
