import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // LBR-001 NMC_lithium_ion Afrique_Subsaharienne — critical toxic_battery_dumping_crisis
  { id:"LBR-001", battery_type:"NMC_lithium_ion", region:"Afrique_Subsaharienne", recovery_rate:0.12, lithium_recovery_efficiency:0.15, cobalt_recovery_gap:0.85, nickel_manganese_loss:0.78, toxic_chemical_leaching:0.88, groundwater_contamination_risk:0.82, transportation_hazard:0.75, recycling_facility_capacity:0.10, collection_infrastructure:0.12, informal_sector_proportion:0.88, second_life_deployment:0.05, producer_responsibility_compliance:0.08, carbon_cost_recycling:0.80, regulatory_framework_quality:0.10, innovation_investment:0.08, strategic_stockpile_recovery:0.10, circular_economy_score:0.06 },
  // LBR-002 LFP_lithium Asie_Sud — critical lithium_cobalt_scarcity_trap
  { id:"LBR-002", battery_type:"LFP_lithium", region:"Asie_Sud", recovery_rate:0.18, lithium_recovery_efficiency:0.20, cobalt_recovery_gap:0.88, nickel_manganese_loss:0.72, toxic_chemical_leaching:0.70, groundwater_contamination_risk:0.65, transportation_hazard:0.60, recycling_facility_capacity:0.20, collection_infrastructure:0.22, informal_sector_proportion:0.75, second_life_deployment:0.10, producer_responsibility_compliance:0.12, carbon_cost_recycling:0.72, regulatory_framework_quality:0.15, innovation_investment:0.12, strategic_stockpile_recovery:0.15, circular_economy_score:0.12 },
  // LBR-003 NCA_lithium Amérique_Latine — critical recycling_infrastructure_gap
  { id:"LBR-003", battery_type:"NCA_lithium", region:"Amérique_Latine", recovery_rate:0.20, lithium_recovery_efficiency:0.22, cobalt_recovery_gap:0.65, nickel_manganese_loss:0.60, toxic_chemical_leaching:0.72, groundwater_contamination_risk:0.68, transportation_hazard:0.62, recycling_facility_capacity:0.18, collection_infrastructure:0.20, informal_sector_proportion:0.70, second_life_deployment:0.08, producer_responsibility_compliance:0.15, carbon_cost_recycling:0.68, regulatory_framework_quality:0.18, innovation_investment:0.15, strategic_stockpile_recovery:0.18, circular_economy_score:0.10 },
  // LBR-004 LCO_lithium Moyen_Orient — high second_life_market_failure
  { id:"LBR-004", battery_type:"LCO_lithium", region:"Moyen_Orient", recovery_rate:0.35, lithium_recovery_efficiency:0.38, cobalt_recovery_gap:0.55, nickel_manganese_loss:0.50, toxic_chemical_leaching:0.48, groundwater_contamination_risk:0.45, transportation_hazard:0.42, recycling_facility_capacity:0.35, collection_infrastructure:0.38, informal_sector_proportion:0.50, second_life_deployment:0.15, producer_responsibility_compliance:0.30, carbon_cost_recycling:0.52, regulatory_framework_quality:0.35, innovation_investment:0.28, strategic_stockpile_recovery:0.32, circular_economy_score:0.18 },
  // LBR-005 NMC_lithium_ion Asie_Est — high extended_producer_responsibility_collapse
  { id:"LBR-005", battery_type:"NMC_lithium_ion", region:"Asie_Est", recovery_rate:0.40, lithium_recovery_efficiency:0.42, cobalt_recovery_gap:0.50, nickel_manganese_loss:0.45, toxic_chemical_leaching:0.42, groundwater_contamination_risk:0.40, transportation_hazard:0.38, recycling_facility_capacity:0.42, collection_infrastructure:0.40, informal_sector_proportion:0.45, second_life_deployment:0.22, producer_responsibility_compliance:0.18, carbon_cost_recycling:0.48, regulatory_framework_quality:0.20, innovation_investment:0.22, strategic_stockpile_recovery:0.38, circular_economy_score:0.25 },
  // LBR-006 LFP_lithium Europe_Est — moderate none
  { id:"LBR-006", battery_type:"LFP_lithium", region:"Europe_Est", recovery_rate:0.55, lithium_recovery_efficiency:0.58, cobalt_recovery_gap:0.38, nickel_manganese_loss:0.35, toxic_chemical_leaching:0.32, groundwater_contamination_risk:0.28, transportation_hazard:0.30, recycling_facility_capacity:0.58, collection_infrastructure:0.55, informal_sector_proportion:0.30, second_life_deployment:0.40, producer_responsibility_compliance:0.52, carbon_cost_recycling:0.38, regulatory_framework_quality:0.50, innovation_investment:0.45, strategic_stockpile_recovery:0.55, circular_economy_score:0.48 },
  // LBR-007 NCA_lithium Europe_Ouest — low none
  { id:"LBR-007", battery_type:"NCA_lithium", region:"Europe_Ouest", recovery_rate:0.82, lithium_recovery_efficiency:0.80, cobalt_recovery_gap:0.12, nickel_manganese_loss:0.10, toxic_chemical_leaching:0.08, groundwater_contamination_risk:0.06, transportation_hazard:0.10, recycling_facility_capacity:0.88, collection_infrastructure:0.85, informal_sector_proportion:0.05, second_life_deployment:0.78, producer_responsibility_compliance:0.88, carbon_cost_recycling:0.12, regulatory_framework_quality:0.90, innovation_investment:0.85, strategic_stockpile_recovery:0.82, circular_economy_score:0.88 },
  // LBR-008 LCO_lithium Amérique_Nord — low none
  { id:"LBR-008", battery_type:"LCO_lithium", region:"Amérique_Nord", recovery_rate:0.78, lithium_recovery_efficiency:0.75, cobalt_recovery_gap:0.15, nickel_manganese_loss:0.12, toxic_chemical_leaching:0.10, groundwater_contamination_risk:0.08, transportation_hazard:0.12, recycling_facility_capacity:0.82, collection_infrastructure:0.80, informal_sector_proportion:0.08, second_life_deployment:0.72, producer_responsibility_compliance:0.82, carbon_cost_recycling:0.15, regulatory_framework_quality:0.85, innovation_investment:0.80, strategic_stockpile_recovery:0.78, circular_economy_score:0.82 },
];

type Entity = typeof MOCK_ENTITIES[0];

function recoveryScore(e: Entity): number {
  const raw = (
    (1.0 - e.recovery_rate) * 0.4
    + (1.0 - e.lithium_recovery_efficiency) * 0.35
    + e.informal_sector_proportion * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function toxicityScore(e: Entity): number {
  const raw = (
    e.toxic_chemical_leaching * 0.4
    + e.groundwater_contamination_risk * 0.35
    + e.transportation_hazard * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function supplyScore(e: Entity): number {
  const raw = (
    e.cobalt_recovery_gap * 0.4
    + e.nickel_manganese_loss * 0.35
    + (1.0 - e.strategic_stockpile_recovery) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function governanceScore(e: Entity): number {
  const raw = (
    (1.0 - e.producer_responsibility_compliance) * 0.4
    + (1.0 - e.regulatory_framework_quality) * 0.35
    + (1.0 - e.innovation_investment) * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(rec: number, tox: number, sup: number, gov: number): number {
  return Math.round((rec * 0.30 + tox * 0.25 + sup * 0.25 + gov * 0.20) * 100) / 100;
}

function batteryPattern(e: Entity): string {
  if (e.toxic_chemical_leaching > 0.80 && e.groundwater_contamination_risk > 0.75) return "toxic_battery_dumping_crisis";
  if (e.cobalt_recovery_gap > 0.80 && e.lithium_recovery_efficiency < 0.25)         return "lithium_cobalt_scarcity_trap";
  if (e.recycling_facility_capacity < 0.25 && e.collection_infrastructure < 0.25)   return "recycling_infrastructure_gap";
  if (e.second_life_deployment < 0.20 && e.circular_economy_score < 0.25)           return "second_life_market_failure";
  if (e.producer_responsibility_compliance < 0.20 && e.regulatory_framework_quality < 0.25) return "extended_producer_responsibility_collapse";
  return "none";
}

function riskLevel(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }

function severity(c: number): string {
  if (c >= 60) return "crise_recyclage_lithium_systémique";
  if (c >= 40) return "crise_chaîne_valeur_batteries_majeure";
  if (c >= 20) return "déficit_infrastructure_recyclage_structurel";
  return "recyclage_batteries_sous_surveillance";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_décontamination_et_recyclage_critique";
  if (risk === "high")     return "renforcement_filière_recyclage_lithium_accéléré";
  if (risk === "moderate") return "optimisation_infrastructure_collecte_et_traitement";
  return "veille_économie_circulaire_batteries_continue";
}

function batterySignal(risk: string): string {
  if (risk === "critical") return "🔴 Crise recyclage batteries lithium systémique — économie circulaire en péril";
  if (risk === "high")     return "🟠 Crise chaîne valeur batteries majeure détectée";
  if (risk === "moderate") return "🟡 Déficit infrastructure recyclage structurel actif";
  return "🟢 Recyclage batteries lithium sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const rec = recoveryScore(e), tox = toxicityScore(e), sup = supplyScore(e), gov = governanceScore(e);
      const comp = compositeScore(rec, tox, sup, gov);
      const risk = riskLevel(comp);
      const pattern = batteryPattern(e);
      return {
        id: e.entity_id,
        battery_type: e.battery_type,
        region: e.region,
        recovery_score: rec,
        toxicity_score: tox,
        supply_score: sup,
        governance_score: gov,
        composite_score: comp,
        risk_level: risk,
        battery_pattern: pattern,
        severity: severity(comp),
        recommended_action: recommendedAction(risk),
        signal: batterySignal(risk),
        recycling_facility_capacity: e.recycling_facility_capacity,
        circular_economy_score: e.circular_economy_score,
      };
    });

    const rc: Record<string,number> = {}, pc: Record<string,number> = {}, sc: Record<string,number> = {}, ac: Record<string,number> = {};
    let trec=0, ttox=0, tsup=0, tgov=0, tcomp=0, tcircular=0;
    let critC=0, highC=0, modC=0, lowC=0;

    for (const e of entities) {
      rc[e.risk_level]          = (rc[e.risk_level]          || 0) + 1;
      pc[e.battery_pattern]     = (pc[e.battery_pattern]     || 0) + 1;
      sc[e.severity]            = (sc[e.severity]            || 0) + 1;
      ac[e.recommended_action]  = (ac[e.recommended_action]  || 0) + 1;
      trec  += e.recovery_score;
      ttox  += e.toxicity_score;
      tsup  += e.supply_score;
      tgov  += e.governance_score;
      tcomp += e.composite_score;
      tcircular += e.circular_economy_score;
      if      (e.risk_level === "critical") critC++;
      else if (e.risk_level === "high")     highC++;
      else if (e.risk_level === "moderate") modC++;
      else                                  lowC++;
    }

    const n = entities.length;
    const avg_composite = Math.round(tcomp / n * 10) / 10;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id: 425,
        module_name: "Recyclage Batteries Lithium & Économie Circulaire Intelligence Engine",
        total: n,
        critical: critC,
        high: highC,
        moderate: modC,
        low: lowC,
        avg_composite,
        pattern_distribution: pc,
        risk_distribution: rc,
        severity_distribution: sc,
        action_distribution: ac,
        avg_estimated_battery_circular_index: Math.round(avg_composite / 100 * 10 * 100) / 100,
      },
    } as Record<string,unknown>));
  }

  const upstream = await fetch(`${process.env.SWARM_API_URL}/api/lithium-battery-recycling-engine`);
  if (!upstream.ok) return NextResponse.json({ error: "Upstream error" }, { status: 502 });
  return NextResponse.json(await upstream.json());
}
