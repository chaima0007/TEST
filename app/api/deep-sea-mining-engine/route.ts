import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // DSM-001 — Clarion-Clipperton, APAC → critical, deep_sea_ecosystem_destruction
  {
    entity_id: "DSM-001", mining_zone: "clarion_clipperton_zone", region: "APAC",
    ecological_destruction_scale: 0.92, polymetallic_nodule_competition: 0.80,
    ISA_governance_failure: 0.60, deep_sea_biodiversity_collapse: 0.88,
    sediment_plume_impact: 0.85, carbon_sequestration_disruption: 0.78,
    geopolitical_seabed_claim: 0.70, technological_mining_dominance: 0.75,
    small_island_state_exclusion: 0.65, treaty_violation_risk: 0.60,
    rare_mineral_seabed_value: 0.82, ocean_floor_sovereignty_dispute: 0.68,
    deep_sea_cable_risk: 0.55, military_seabed_use: 0.50,
    private_company_capture: 0.72, monitoring_enforcement_gap: 0.70,
    UNCLOS_framework_stress: 0.65,
  },
  // DSM-002 — Mid-Atlantic Ridge, EMEA → low, none
  {
    entity_id: "DSM-002", mining_zone: "mid_atlantic_ridge", region: "EMEA",
    ecological_destruction_scale: 0.18, polymetallic_nodule_competition: 0.15,
    ISA_governance_failure: 0.12, deep_sea_biodiversity_collapse: 0.20,
    sediment_plume_impact: 0.15, carbon_sequestration_disruption: 0.10,
    geopolitical_seabed_claim: 0.18, technological_mining_dominance: 0.12,
    small_island_state_exclusion: 0.10, treaty_violation_risk: 0.15,
    rare_mineral_seabed_value: 0.20, ocean_floor_sovereignty_dispute: 0.12,
    deep_sea_cable_risk: 0.08, military_seabed_use: 0.10,
    private_company_capture: 0.12, monitoring_enforcement_gap: 0.15,
    UNCLOS_framework_stress: 0.10,
  },
  // DSM-003 — South China Sea, APAC → critical, seabed_geopolitical_conflict
  {
    entity_id: "DSM-003", mining_zone: "south_china_sea_basin", region: "APAC",
    ecological_destruction_scale: 0.72, polymetallic_nodule_competition: 0.78,
    ISA_governance_failure: 0.65, deep_sea_biodiversity_collapse: 0.70,
    sediment_plume_impact: 0.68, carbon_sequestration_disruption: 0.62,
    geopolitical_seabed_claim: 0.90, technological_mining_dominance: 0.80,
    small_island_state_exclusion: 0.72, treaty_violation_risk: 0.75,
    rare_mineral_seabed_value: 0.78, ocean_floor_sovereignty_dispute: 0.85,
    deep_sea_cable_risk: 0.70, military_seabed_use: 0.82,
    private_company_capture: 0.65, monitoring_enforcement_gap: 0.70,
    UNCLOS_framework_stress: 0.78,
  },
  // DSM-004 — Indian Ocean Ridge, MEA → moderate, none
  {
    entity_id: "DSM-004", mining_zone: "indian_ocean_ridge", region: "MEA",
    ecological_destruction_scale: 0.38, polymetallic_nodule_competition: 0.42,
    ISA_governance_failure: 0.35, deep_sea_biodiversity_collapse: 0.40,
    sediment_plume_impact: 0.35, carbon_sequestration_disruption: 0.30,
    geopolitical_seabed_claim: 0.42, technological_mining_dominance: 0.38,
    small_island_state_exclusion: 0.35, treaty_violation_risk: 0.40,
    rare_mineral_seabed_value: 0.45, ocean_floor_sovereignty_dispute: 0.38,
    deep_sea_cable_risk: 0.30, military_seabed_use: 0.35,
    private_company_capture: 0.40, monitoring_enforcement_gap: 0.42,
    UNCLOS_framework_stress: 0.38,
  },
  // DSM-005 — Pacific ISA Zone, APAC → critical, ISA_governance_capture
  {
    entity_id: "DSM-005", mining_zone: "pacific_ISA_zone", region: "APAC",
    ecological_destruction_scale: 0.72, polymetallic_nodule_competition: 0.78,
    ISA_governance_failure: 0.88, deep_sea_biodiversity_collapse: 0.74,
    sediment_plume_impact: 0.70, carbon_sequestration_disruption: 0.65,
    geopolitical_seabed_claim: 0.68, technological_mining_dominance: 0.72,
    small_island_state_exclusion: 0.70, treaty_violation_risk: 0.75,
    rare_mineral_seabed_value: 0.80, ocean_floor_sovereignty_dispute: 0.65,
    deep_sea_cable_risk: 0.60, military_seabed_use: 0.58,
    private_company_capture: 0.85, monitoring_enforcement_gap: 0.78,
    UNCLOS_framework_stress: 0.72,
  },
  // DSM-006 — Cook Islands EEZ, PACIFIC → high, small_island_exclusion_crisis
  {
    entity_id: "DSM-006", mining_zone: "cook_islands_eez", region: "PACIFIC",
    ecological_destruction_scale: 0.62, polymetallic_nodule_competition: 0.68,
    ISA_governance_failure: 0.65, deep_sea_biodiversity_collapse: 0.60,
    sediment_plume_impact: 0.58, carbon_sequestration_disruption: 0.55,
    geopolitical_seabed_claim: 0.60, technological_mining_dominance: 0.65,
    small_island_state_exclusion: 0.85, treaty_violation_risk: 0.60,
    rare_mineral_seabed_value: 0.70, ocean_floor_sovereignty_dispute: 0.58,
    deep_sea_cable_risk: 0.48, military_seabed_use: 0.45,
    private_company_capture: 0.62, monitoring_enforcement_gap: 0.65,
    UNCLOS_framework_stress: 0.80,
  },
  // DSM-007 — Bismarck Sea, APAC → critical, mineral_rush_ecological_catastrophe
  {
    entity_id: "DSM-007", mining_zone: "bismarck_sea_basin", region: "APAC",
    ecological_destruction_scale: 0.75, polymetallic_nodule_competition: 0.80,
    ISA_governance_failure: 0.72, deep_sea_biodiversity_collapse: 0.78,
    sediment_plume_impact: 0.72, carbon_sequestration_disruption: 0.68,
    geopolitical_seabed_claim: 0.70, technological_mining_dominance: 0.75,
    small_island_state_exclusion: 0.72, treaty_violation_risk: 0.68,
    rare_mineral_seabed_value: 0.88, ocean_floor_sovereignty_dispute: 0.65,
    deep_sea_cable_risk: 0.60, military_seabed_use: 0.55,
    private_company_capture: 0.72, monitoring_enforcement_gap: 0.82,
    UNCLOS_framework_stress: 0.70,
  },
  // DSM-008 — Arctic Seabed, ARCTIC → high, none
  {
    entity_id: "DSM-008", mining_zone: "arctic_seabed_zone", region: "ARCTIC",
    ecological_destruction_scale: 0.58, polymetallic_nodule_competition: 0.62,
    ISA_governance_failure: 0.55, deep_sea_biodiversity_collapse: 0.52,
    sediment_plume_impact: 0.60, carbon_sequestration_disruption: 0.72,
    geopolitical_seabed_claim: 0.65, technological_mining_dominance: 0.60,
    small_island_state_exclusion: 0.30, treaty_violation_risk: 0.58,
    rare_mineral_seabed_value: 0.68, ocean_floor_sovereignty_dispute: 0.62,
    deep_sea_cable_risk: 0.55, military_seabed_use: 0.65,
    private_company_capture: 0.50, monitoring_enforcement_gap: 0.60,
    UNCLOS_framework_stress: 0.55,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function ecologicalScore(e: Entity): number {
  const raw = (
    e.ecological_destruction_scale * 0.4
    + e.deep_sea_biodiversity_collapse * 0.35
    + e.sediment_plume_impact * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function geopoliticalScore(e: Entity): number {
  const raw = (
    e.geopolitical_seabed_claim * 0.4
    + e.ocean_floor_sovereignty_dispute * 0.35
    + e.military_seabed_use * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function governanceScore(e: Entity): number {
  const raw = (
    e.ISA_governance_failure * 0.4
    + e.treaty_violation_risk * 0.35
    + e.UNCLOS_framework_stress * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function exploitationScore(e: Entity): number {
  const raw = (
    e.rare_mineral_seabed_value * 0.4
    + e.polymetallic_nodule_competition * 0.35
    + e.technological_mining_dominance * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(eco: number, geo: number, gov: number, exp: number): number {
  return Math.round((eco * 0.30 + geo * 0.25 + gov * 0.25 + exp * 0.20) * 100) / 100;
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function miningPattern(e: Entity): string {
  if (e.ecological_destruction_scale > 0.85 && e.deep_sea_biodiversity_collapse > 0.80) return "deep_sea_ecosystem_destruction";
  if (e.geopolitical_seabed_claim > 0.85 && e.ocean_floor_sovereignty_dispute > 0.80) return "seabed_geopolitical_conflict";
  if (e.ISA_governance_failure > 0.85 && e.private_company_capture > 0.80) return "ISA_governance_capture";
  if (e.small_island_state_exclusion > 0.80 && e.UNCLOS_framework_stress > 0.75) return "small_island_exclusion_crisis";
  if (e.rare_mineral_seabed_value > 0.80 && e.monitoring_enforcement_gap > 0.75) return "mineral_rush_ecological_catastrophe";
  return "none";
}

function severity(comp: number): string {
  if (comp >= 60) return "catastrophe_écologique_fond_marin_systémique";
  if (comp >= 40) return "crise_géopolitique_ressources_seabed_majeure";
  if (comp >= 20) return "tension_exploitation_fond_marin_active";
  return "surveillance_exploitation_minière_fond_marin";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_protection_écosystème_fond_marin";
  if (risk === "high")     return "renforcement_gouvernance_ISA_multilatérale";
  if (risk === "moderate") return "surveillance_renforcée_zones_extraction_seabed";
  return "veille_exploitation_minière_fond_marin_continue";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Catastrophe écologique fond marin systémique — destruction irréversible imminente";
  if (risk === "high")     return "🟠 Crise géopolitique ressources seabed majeure détectée";
  if (risk === "moderate") return "🟡 Tension exploitation fond marin active";
  return "🟢 Exploitation minière fond marin sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const eco  = ecologicalScore(e);
      const geo  = geopoliticalScore(e);
      const gov  = governanceScore(e);
      const exp  = exploitationScore(e);
      const comp = compositeScore(eco, geo, gov, exp);
      const risk = riskLevel(comp);
      const pat  = miningPattern(e);
      const sev  = severity(comp);
      const act  = recommendedAction(risk);
      const sig  = signal(risk);

      return {
        entity_id:                    e.entity_id,
        mining_zone:                  e.mining_zone,
        region:                       e.region,
        ecological_score:             eco,
        geopolitical_score:           geo,
        governance_score:             gov,
        exploitation_score:           exp,
        composite_score:              comp,
        risk_level:                   risk,
        mining_pattern:               pat,
        severity:                     sev,
        recommended_action:           act,
        signal:                       sig,
        ecological_destruction_scale: e.ecological_destruction_scale,
        geopolitical_seabed_claim:    e.geopolitical_seabed_claim,
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
      pc[ent.mining_pattern]     = (pc[ent.mining_pattern]     || 0) + 1;
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
      module_id:                        390,
      module_name:                      "Deep Sea Mining & Seabed Resource Geopolitics Intelligence Engine",
      total:                            n,
      critical:                         criticalCount,
      high:                             highCount,
      moderate:                         moderateCount,
      low:                              lowCount,
      avg_composite:                    avgComposite,
      distributions:                    { risk: rc, pattern: pc, severity: sc, action: ac },
      pattern_distribution:             pc,
      risk_distribution:                rc,
      severity_distribution:            sc,
      avg_estimated_seabed_risk_index:  Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "deep-sea-mining-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/deep-sea-mining-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "deep-sea-mining-engine"));
  } catch {
    return NextResponse.json(sealResponse({ error: "Upstream unavailable" }, "deep-sea-mining-engine"), { status: 502 });
  }
}
