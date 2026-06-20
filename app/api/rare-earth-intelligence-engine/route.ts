import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // REI-001 — rare_earth_elements, APAC → critical, rare_earth_monopoly_crisis
  {
    entity_id: "REI-001", material_category: "rare_earth_elements", region: "APAC",
    supply_concentration_monopoly_risk: 0.88, critical_material_import_dependency: 0.80,
    mining_geopolitical_leverage: 0.72, processing_chokepoint_control: 0.82,
    strategic_reserve_depletion_rate: 0.70, conflict_mineral_sourcing_risk: 0.45,
    green_tech_material_demand_surge: 0.75, recycling_capacity_inadequacy: 0.78,
    substitute_material_unavailability: 0.60, export_restriction_weaponization_risk: 0.65,
    environmental_mining_collapse_risk: 0.58, labor_rights_mining_violation: 0.50,
    material_scarcity_technology_lock: 0.72, critical_material_price_volatility: 0.68,
    supply_chain_single_point_failure: 0.60, allied_mining_diversification_gap: 0.75,
    deep_sea_mining_regulatory_vacuum: 0.55,
  },
  // REI-002 — lithium, LATAM → low, none
  {
    entity_id: "REI-002", material_category: "lithium", region: "LATAM",
    supply_concentration_monopoly_risk: 0.18, critical_material_import_dependency: 0.15,
    mining_geopolitical_leverage: 0.20, processing_chokepoint_control: 0.12,
    strategic_reserve_depletion_rate: 0.10, conflict_mineral_sourcing_risk: 0.12,
    green_tech_material_demand_surge: 0.22, recycling_capacity_inadequacy: 0.18,
    substitute_material_unavailability: 0.15, export_restriction_weaponization_risk: 0.10,
    environmental_mining_collapse_risk: 0.12, labor_rights_mining_violation: 0.10,
    material_scarcity_technology_lock: 0.15, critical_material_price_volatility: 0.20,
    supply_chain_single_point_failure: 0.12, allied_mining_diversification_gap: 0.18,
    deep_sea_mining_regulatory_vacuum: 0.08,
  },
  // REI-003 — rare_earth_elements, EMEA → high, export_weapon_deployment
  {
    entity_id: "REI-003", material_category: "rare_earth_elements", region: "EMEA",
    supply_concentration_monopoly_risk: 0.55, critical_material_import_dependency: 0.62,
    mining_geopolitical_leverage: 0.72, processing_chokepoint_control: 0.48,
    strategic_reserve_depletion_rate: 0.50, conflict_mineral_sourcing_risk: 0.45,
    green_tech_material_demand_surge: 0.55, recycling_capacity_inadequacy: 0.52,
    substitute_material_unavailability: 0.48, export_restriction_weaponization_risk: 0.78,
    environmental_mining_collapse_risk: 0.40, labor_rights_mining_violation: 0.38,
    material_scarcity_technology_lock: 0.50, critical_material_price_volatility: 0.55,
    supply_chain_single_point_failure: 0.45, allied_mining_diversification_gap: 0.58,
    deep_sea_mining_regulatory_vacuum: 0.35,
  },
  // REI-004 — cobalt, NOAM → low, none
  {
    entity_id: "REI-004", material_category: "cobalt", region: "NOAM",
    supply_concentration_monopoly_risk: 0.15, critical_material_import_dependency: 0.20,
    mining_geopolitical_leverage: 0.18, processing_chokepoint_control: 0.10,
    strategic_reserve_depletion_rate: 0.12, conflict_mineral_sourcing_risk: 0.08,
    green_tech_material_demand_surge: 0.25, recycling_capacity_inadequacy: 0.20,
    substitute_material_unavailability: 0.18, export_restriction_weaponization_risk: 0.12,
    environmental_mining_collapse_risk: 0.10, labor_rights_mining_violation: 0.08,
    material_scarcity_technology_lock: 0.18, critical_material_price_volatility: 0.22,
    supply_chain_single_point_failure: 0.15, allied_mining_diversification_gap: 0.20,
    deep_sea_mining_regulatory_vacuum: 0.10,
  },
  // REI-005 — lithium, APAC → critical, green_tech_material_crunch
  {
    entity_id: "REI-005", material_category: "lithium", region: "APAC",
    supply_concentration_monopoly_risk: 0.65, critical_material_import_dependency: 0.70,
    mining_geopolitical_leverage: 0.60, processing_chokepoint_control: 0.58,
    strategic_reserve_depletion_rate: 0.72, conflict_mineral_sourcing_risk: 0.48,
    green_tech_material_demand_surge: 0.82, recycling_capacity_inadequacy: 0.72,
    substitute_material_unavailability: 0.75, export_restriction_weaponization_risk: 0.58,
    environmental_mining_collapse_risk: 0.55, labor_rights_mining_violation: 0.42,
    material_scarcity_technology_lock: 0.78, critical_material_price_volatility: 0.75,
    supply_chain_single_point_failure: 0.62, allied_mining_diversification_gap: 0.68,
    deep_sea_mining_regulatory_vacuum: 0.50,
  },
  // REI-006 — copper, MEA → moderate, none
  {
    entity_id: "REI-006", material_category: "copper", region: "MEA",
    supply_concentration_monopoly_risk: 0.40, critical_material_import_dependency: 0.38,
    mining_geopolitical_leverage: 0.42, processing_chokepoint_control: 0.35,
    strategic_reserve_depletion_rate: 0.30, conflict_mineral_sourcing_risk: 0.38,
    green_tech_material_demand_surge: 0.42, recycling_capacity_inadequacy: 0.35,
    substitute_material_unavailability: 0.30, export_restriction_weaponization_risk: 0.38,
    environmental_mining_collapse_risk: 0.42, labor_rights_mining_violation: 0.35,
    material_scarcity_technology_lock: 0.38, critical_material_price_volatility: 0.40,
    supply_chain_single_point_failure: 0.32, allied_mining_diversification_gap: 0.40,
    deep_sea_mining_regulatory_vacuum: 0.28,
  },
  // REI-007 — cobalt, EMEA → high, conflict_mineral_cascade
  {
    entity_id: "REI-007", material_category: "cobalt", region: "EMEA",
    supply_concentration_monopoly_risk: 0.58, critical_material_import_dependency: 0.65,
    mining_geopolitical_leverage: 0.60, processing_chokepoint_control: 0.52,
    strategic_reserve_depletion_rate: 0.55, conflict_mineral_sourcing_risk: 0.78,
    green_tech_material_demand_surge: 0.50, recycling_capacity_inadequacy: 0.58,
    substitute_material_unavailability: 0.45, export_restriction_weaponization_risk: 0.55,
    environmental_mining_collapse_risk: 0.60, labor_rights_mining_violation: 0.72,
    material_scarcity_technology_lock: 0.52, critical_material_price_volatility: 0.60,
    supply_chain_single_point_failure: 0.50, allied_mining_diversification_gap: 0.62,
    deep_sea_mining_regulatory_vacuum: 0.40,
  },
  // REI-008 — semiconductor_minerals, NOAM → critical, supply_chain_collapse
  {
    entity_id: "REI-008", material_category: "semiconductor_minerals", region: "NOAM",
    supply_concentration_monopoly_risk: 0.70, critical_material_import_dependency: 0.78,
    mining_geopolitical_leverage: 0.68, processing_chokepoint_control: 0.60,
    strategic_reserve_depletion_rate: 0.75, conflict_mineral_sourcing_risk: 0.50,
    green_tech_material_demand_surge: 0.68, recycling_capacity_inadequacy: 0.72,
    substitute_material_unavailability: 0.62, export_restriction_weaponization_risk: 0.60,
    environmental_mining_collapse_risk: 0.55, labor_rights_mining_violation: 0.45,
    material_scarcity_technology_lock: 0.70, critical_material_price_volatility: 0.72,
    supply_chain_single_point_failure: 0.82, allied_mining_diversification_gap: 0.75,
    deep_sea_mining_regulatory_vacuum: 0.60,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function supplyScore(e: Entity): number {
  const raw = (
    e.supply_concentration_monopoly_risk * 0.4
    + e.critical_material_import_dependency * 0.35
    + e.processing_chokepoint_control * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function geopoliticalScore(e: Entity): number {
  const raw = (
    e.mining_geopolitical_leverage * 0.4
    + e.export_restriction_weaponization_risk * 0.35
    + e.conflict_mineral_sourcing_risk * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function demandScore(e: Entity): number {
  const raw = (
    e.green_tech_material_demand_surge * 0.4
    + e.material_scarcity_technology_lock * 0.35
    + e.substitute_material_unavailability * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function resilienceScore(e: Entity): number {
  const raw = (
    e.recycling_capacity_inadequacy * 0.4
    + e.supply_chain_single_point_failure * 0.35
    + e.allied_mining_diversification_gap * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(supply: number, geo: number, demand: number, resilience: number): number {
  return Math.round((supply * 0.30 + geo * 0.25 + demand * 0.25 + resilience * 0.20) * 100) / 100;
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critique";
  if (comp >= 40) return "élevé";
  if (comp >= 20) return "modéré";
  return "faible";
}

function materialPattern(e: Entity): string {
  if (e.supply_concentration_monopoly_risk >= 0.70 && e.processing_chokepoint_control >= 0.65) return "rare_earth_monopoly_crisis";
  if (e.export_restriction_weaponization_risk >= 0.70 && e.mining_geopolitical_leverage >= 0.65) return "export_weapon_deployment";
  if (e.green_tech_material_demand_surge >= 0.70 && e.substitute_material_unavailability >= 0.65) return "green_tech_material_crunch";
  if (e.conflict_mineral_sourcing_risk >= 0.70 && e.labor_rights_mining_violation >= 0.65) return "conflict_mineral_cascade";
  if (e.supply_chain_single_point_failure >= 0.70 && e.critical_material_import_dependency >= 0.65) return "supply_chain_collapse";
  return "none";
}

function severity(comp: number): string {
  if (comp >= 60) return "crise_matières_critiques_systémique";
  if (comp >= 40) return "pénurie_stratégique_majeure";
  if (comp >= 20) return "tension_approvisionnement_critique";
  return "approvisionnement_sous_surveillance";
}

function recommendedAction(risk: string): string {
  if (risk === "critique") return "sécurisation_urgente_approvisionnements_critiques";
  if (risk === "élevé")    return "diversification_stratégique_accélérée";
  if (risk === "modéré")  return "renforcement_résilience_chaînes_approvisionnement";
  return "veille_matières_critiques_continue";
}

function signal(risk: string): string {
  if (risk === "critique") return "🔴 Crise matières critiques systémique — dépendance stratégique extrême";
  if (risk === "élevé")    return "🟠 Pénurie stratégique majeure détectée";
  if (risk === "modéré")  return "🟡 Tension approvisionnement critique active";
  return "🟢 Approvisionnement matières critiques sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const supply      = supplyScore(e);
      const geo         = geopoliticalScore(e);
      const demand      = demandScore(e);
      const resilience  = resilienceScore(e);
      const comp        = compositeScore(supply, geo, demand, resilience);
      const risk        = riskLevel(comp);
      const pattern     = materialPattern(e);
      const sev         = severity(comp);
      const action      = recommendedAction(risk);
      const sig         = signal(risk);

      return {
        entity_id:                            e.entity_id,
        material_category:                    e.material_category,
        region:                               e.region,
        supply_score:                         supply,
        geopolitical_score:                   geo,
        demand_score:                         demand,
        resilience_score:                     resilience,
        composite_score:                      comp,
        risk_level:                           risk,
        material_pattern:                     pattern,
        severity:                             sev,
        recommended_action:                   action,
        signal:                               sig,
        supply_concentration_monopoly_risk:   e.supply_concentration_monopoly_risk,
        export_restriction_weaponization_risk: e.export_restriction_weaponization_risk,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      rc[ent.risk_level]          = (rc[ent.risk_level]          || 0) + 1;
      pc[ent.material_pattern]    = (pc[ent.material_pattern]    || 0) + 1;
      sc[ent.severity]            = (sc[ent.severity]            || 0) + 1;
      ac[ent.recommended_action]  = (ac[ent.recommended_action]  || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critique")     criticalCount++;
      else if (ent.risk_level === "élevé")    highCount++;
      else if (ent.risk_level === "modéré")  moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                         347,
      module_name:                       "Rare Earth & Critical Materials Geopolitics Intelligence Engine",
      total_entities:                    n,
      critical_count:                    criticalCount,
      high_count:                        highCount,
      moderate_count:                    moderateCount,
      low_count:                         lowCount,
      avg_composite:                     avgComposite,
      pattern_distribution:              pc,
      risk_distribution:                 rc,
      severity_distribution:             sc,
      action_distribution:               ac,
      avg_estimated_material_risk_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "rare-earth-intelligence-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/rare-earth-intelligence-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "rare-earth-intelligence-engine"));
  } catch {
    return NextResponse.json(sealResponse({ error: "Upstream unavailable" }, "rare-earth-intelligence-engine"), { status: 502 });
  }
}
