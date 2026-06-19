import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // BGE-001 — lithium, APAC → critical, lithium_supply_crisis
  {
    entity_id: "BGE-001", mineral_type: "lithium", region: "APAC",
    lithium_supply_concentration: 0.92, cobalt_congo_dependency: 0.55, nickel_supply_risk: 0.62,
    manganese_geopolitical_control: 0.58, battery_manufacturing_monopoly: 0.88,
    EV_supply_chain_vulnerability: 0.70, Chinese_battery_dominance: 0.78,
    recycling_infrastructure_gap: 0.72, artisanal_mining_risk: 0.60, child_labor_exposure: 0.52,
    environmental_mining_destruction: 0.58, strategic_stockpile_inadequacy: 0.65,
    processing_chokepoint: 0.70, battery_technology_lock_in: 0.75,
    energy_storage_sovereignty: 0.68, mineral_nationalism_risk: 0.62,
    green_tech_supply_weaponization: 0.60,
  },
  // BGE-002 — battery_cells, APAC → critical, Chinese_battery_capture
  {
    entity_id: "BGE-002", mineral_type: "battery_cells", region: "APAC",
    lithium_supply_concentration: 0.70, cobalt_congo_dependency: 0.60, nickel_supply_risk: 0.68,
    manganese_geopolitical_control: 0.72, battery_manufacturing_monopoly: 0.78,
    EV_supply_chain_vulnerability: 0.65, Chinese_battery_dominance: 0.90,
    recycling_infrastructure_gap: 0.58, artisanal_mining_risk: 0.50, child_labor_exposure: 0.45,
    environmental_mining_destruction: 0.52, strategic_stockpile_inadequacy: 0.60,
    processing_chokepoint: 0.85, battery_technology_lock_in: 0.80,
    energy_storage_sovereignty: 0.75, mineral_nationalism_risk: 0.65,
    green_tech_supply_weaponization: 0.62,
  },
  // BGE-003 — cobalt, MEA → critical, cobalt_humanitarian_crisis
  {
    entity_id: "BGE-003", mineral_type: "cobalt", region: "MEA",
    lithium_supply_concentration: 0.60, cobalt_congo_dependency: 0.90, nickel_supply_risk: 0.55,
    manganese_geopolitical_control: 0.50, battery_manufacturing_monopoly: 0.58,
    EV_supply_chain_vulnerability: 0.62, Chinese_battery_dominance: 0.65,
    recycling_infrastructure_gap: 0.70, artisanal_mining_risk: 0.82, child_labor_exposure: 0.88,
    environmental_mining_destruction: 0.78, strategic_stockpile_inadequacy: 0.60,
    processing_chokepoint: 0.55, battery_technology_lock_in: 0.62,
    energy_storage_sovereignty: 0.58, mineral_nationalism_risk: 0.55,
    green_tech_supply_weaponization: 0.50,
  },
  // BGE-004 — critical_minerals, EMEA → critical, green_tech_weaponization
  {
    entity_id: "BGE-004", mineral_type: "critical_minerals", region: "EMEA",
    lithium_supply_concentration: 0.65, cobalt_congo_dependency: 0.58, nickel_supply_risk: 0.60,
    manganese_geopolitical_control: 0.72, battery_manufacturing_monopoly: 0.68,
    EV_supply_chain_vulnerability: 0.70, Chinese_battery_dominance: 0.75,
    recycling_infrastructure_gap: 0.62, artisanal_mining_risk: 0.55, child_labor_exposure: 0.48,
    environmental_mining_destruction: 0.60, strategic_stockpile_inadequacy: 0.65,
    processing_chokepoint: 0.60, battery_technology_lock_in: 0.72,
    energy_storage_sovereignty: 0.78, mineral_nationalism_risk: 0.82,
    green_tech_supply_weaponization: 0.85,
  },
  // BGE-005 — EV_batteries, NOAM → critical, EV_supply_chain_collapse
  {
    entity_id: "BGE-005", mineral_type: "EV_batteries", region: "NOAM",
    lithium_supply_concentration: 0.68, cobalt_congo_dependency: 0.62, nickel_supply_risk: 0.70,
    manganese_geopolitical_control: 0.65, battery_manufacturing_monopoly: 0.72,
    EV_supply_chain_vulnerability: 0.88, Chinese_battery_dominance: 0.75,
    recycling_infrastructure_gap: 0.80, artisanal_mining_risk: 0.58, child_labor_exposure: 0.50,
    environmental_mining_destruction: 0.55, strategic_stockpile_inadequacy: 0.82,
    processing_chokepoint: 0.68, battery_technology_lock_in: 0.78,
    energy_storage_sovereignty: 0.82, mineral_nationalism_risk: 0.70,
    green_tech_supply_weaponization: 0.65,
  },
  // BGE-006 — nickel, APAC → high, none
  {
    entity_id: "BGE-006", mineral_type: "nickel", region: "APAC",
    lithium_supply_concentration: 0.55, cobalt_congo_dependency: 0.48, nickel_supply_risk: 0.72,
    manganese_geopolitical_control: 0.60, battery_manufacturing_monopoly: 0.55,
    EV_supply_chain_vulnerability: 0.58, Chinese_battery_dominance: 0.62,
    recycling_infrastructure_gap: 0.50, artisanal_mining_risk: 0.45, child_labor_exposure: 0.40,
    environmental_mining_destruction: 0.52, strategic_stockpile_inadequacy: 0.55,
    processing_chokepoint: 0.48, battery_technology_lock_in: 0.58,
    energy_storage_sovereignty: 0.52, mineral_nationalism_risk: 0.50,
    green_tech_supply_weaponization: 0.45,
  },
  // BGE-007 — manganese, LATAM → moderate, none
  {
    entity_id: "BGE-007", mineral_type: "manganese", region: "LATAM",
    lithium_supply_concentration: 0.30, cobalt_congo_dependency: 0.28, nickel_supply_risk: 0.32,
    manganese_geopolitical_control: 0.45, battery_manufacturing_monopoly: 0.35,
    EV_supply_chain_vulnerability: 0.38, Chinese_battery_dominance: 0.40,
    recycling_infrastructure_gap: 0.32, artisanal_mining_risk: 0.28, child_labor_exposure: 0.25,
    environmental_mining_destruction: 0.30, strategic_stockpile_inadequacy: 0.35,
    processing_chokepoint: 0.28, battery_technology_lock_in: 0.38,
    energy_storage_sovereignty: 0.35, mineral_nationalism_risk: 0.30,
    green_tech_supply_weaponization: 0.28,
  },
  // BGE-008 — recycled_materials, EMEA → low, none
  {
    entity_id: "BGE-008", mineral_type: "recycled_materials", region: "EMEA",
    lithium_supply_concentration: 0.12, cobalt_congo_dependency: 0.10, nickel_supply_risk: 0.15,
    manganese_geopolitical_control: 0.18, battery_manufacturing_monopoly: 0.14,
    EV_supply_chain_vulnerability: 0.16, Chinese_battery_dominance: 0.20,
    recycling_infrastructure_gap: 0.12, artisanal_mining_risk: 0.10, child_labor_exposure: 0.08,
    environmental_mining_destruction: 0.12, strategic_stockpile_inadequacy: 0.14,
    processing_chokepoint: 0.10, battery_technology_lock_in: 0.16,
    energy_storage_sovereignty: 0.14, mineral_nationalism_risk: 0.12,
    green_tech_supply_weaponization: 0.10,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function supplyScore(e: Entity): number {
  const raw = (
    e.lithium_supply_concentration * 0.4
    + e.cobalt_congo_dependency * 0.35
    + e.nickel_supply_risk * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function geopoliticalScore(e: Entity): number {
  const raw = (
    e.Chinese_battery_dominance * 0.4
    + e.battery_manufacturing_monopoly * 0.35
    + e.manganese_geopolitical_control * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function humanitarianScore(e: Entity): number {
  const raw = (
    e.artisanal_mining_risk * 0.4
    + e.child_labor_exposure * 0.35
    + e.environmental_mining_destruction * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function sovereigntyScore(e: Entity): number {
  const raw = (
    e.energy_storage_sovereignty * 0.4
    + e.battery_technology_lock_in * 0.35
    + e.recycling_infrastructure_gap * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(supply: number, geo: number, humanitarian: number, sovereignty: number): number {
  return Math.round((supply * 0.30 + geo * 0.25 + humanitarian * 0.25 + sovereignty * 0.20) * 100) / 100;
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function batteryPattern(e: Entity): string {
  if (e.lithium_supply_concentration > 0.85 && e.battery_manufacturing_monopoly > 0.80) return "lithium_supply_crisis";
  if (e.Chinese_battery_dominance > 0.85 && e.processing_chokepoint > 0.80)             return "Chinese_battery_capture";
  if (e.cobalt_congo_dependency > 0.85 && e.child_labor_exposure > 0.80)                return "cobalt_humanitarian_crisis";
  if (e.green_tech_supply_weaponization > 0.80 && e.mineral_nationalism_risk > 0.75)    return "green_tech_weaponization";
  if (e.EV_supply_chain_vulnerability > 0.80 && e.strategic_stockpile_inadequacy > 0.75) return "EV_supply_chain_collapse";
  return "none";
}

function severity(comp: number): string {
  if (comp >= 60) return "crise_géopolitique_batteries_systémique";
  if (comp >= 40) return "tension_approvisionnement_minéraux_majeure";
  if (comp >= 20) return "risque_chaîne_batteries_modéré";
  return "surveillance_minéraux_transition_verte";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "sécurisation_urgente_minéraux_batteries_critiques";
  if (risk === "high")     return "diversification_approvisionnement_batteries_accélérée";
  if (risk === "moderate") return "renforcement_résilience_chaîne_valeur_batteries";
  return "veille_géopolitique_minéraux_transition_continue";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise géopolitique batteries systémique — dépendance minéraux extrême";
  if (risk === "high")     return "🟠 Tension approvisionnement minéraux batteries majeure détectée";
  if (risk === "moderate") return "🟡 Risque chaîne valeur batteries modéré actif";
  return "🟢 Surveillance minéraux transition verte en cours";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const supply      = supplyScore(e);
      const geo         = geopoliticalScore(e);
      const humanitarian = humanitarianScore(e);
      const sovereignty  = sovereigntyScore(e);
      const comp         = compositeScore(supply, geo, humanitarian, sovereignty);
      const risk         = riskLevel(comp);
      const pattern      = batteryPattern(e);
      const sev          = severity(comp);
      const action       = recommendedAction(risk);
      const sig          = signal(risk);

      return {
        entity_id:                     e.entity_id,
        mineral_type:                  e.mineral_type,
        region:                        e.region,
        supply_score:                  supply,
        geopolitical_score:            geo,
        humanitarian_score:            humanitarian,
        sovereignty_score:             sovereignty,
        composite_score:               comp,
        risk_level:                    risk,
        battery_pattern:               pattern,
        severity:                      sev,
        recommended_action:            action,
        signal:                        sig,
        lithium_supply_concentration:  e.lithium_supply_concentration,
        green_tech_supply_weaponization: e.green_tech_supply_weaponization,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      rc[ent.risk_level]         = (rc[ent.risk_level]         || 0) + 1;
      pc[ent.battery_pattern]    = (pc[ent.battery_pattern]    || 0) + 1;
      sc[ent.severity]           = (sc[ent.severity]           || 0) + 1;
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
      module_id:                            380,
      module_name:                          "Battery Geopolitics & Critical Minerals for Clean Energy Intelligence Engine",
      total:                                n,
      critical:                             criticalCount,
      high:                                 highCount,
      moderate:                             moderateCount,
      low:                                  lowCount,
      avg_composite:                        avgComposite,
      risk_distribution:                    rc,
      pattern_distribution:                 pc,
      severity_distribution:                sc,
      action_distribution:                  ac,
      avg_estimated_battery_geopolitics_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "battery-geopolitics-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/battery-geopolitics-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "battery-geopolitics-engine"));
  } catch {
    return NextResponse.json(sealResponse({ error: "Upstream unavailable" }, "battery-geopolitics-engine"), { status: 502 });
  }
}
