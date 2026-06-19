import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // UME-001 — critical, toxic_ewaste_dumping_crisis (toxic_chem>0.85, heavy_metal>0.80)
  {
    entity_id: "UME-001", electronics_sector: "décharge_informelle", region: "SSA",
    ewaste_volume_growth: 0.88, informal_recycling_rate: 0.80,
    toxic_chemical_exposure: 0.90, heavy_metal_leaching: 0.85,
    gold_silver_recovery_rate: 0.70, rare_earth_extraction: 0.68,
    battery_recycling_gap: 0.82, circular_economy_adoption: 0.20,
    producer_take_back_compliance: 0.18, child_labor_exposure: 0.75,
    cross_border_illegal_shipment: 0.80, consumer_awareness: 0.15,
    repair_right_access: 0.20, collection_infrastructure: 0.18,
    data_destruction_security: 0.22, recycling_technology_gap: 0.78,
    regulatory_enforcement: 0.15,
  },
  // UME-002 — critical, critical_metal_supply_gap (gold_silver>0.85, rare_earth>0.80)
  {
    entity_id: "UME-002", electronics_sector: "extraction_métaux_précieux", region: "APAC",
    ewaste_volume_growth: 0.85, informal_recycling_rate: 0.72,
    toxic_chemical_exposure: 0.70, heavy_metal_leaching: 0.68,
    gold_silver_recovery_rate: 0.90, rare_earth_extraction: 0.85,
    battery_recycling_gap: 0.80, circular_economy_adoption: 0.22,
    producer_take_back_compliance: 0.20, child_labor_exposure: 0.65,
    cross_border_illegal_shipment: 0.75, consumer_awareness: 0.18,
    repair_right_access: 0.22, collection_infrastructure: 0.20,
    data_destruction_security: 0.18, recycling_technology_gap: 0.72,
    regulatory_enforcement: 0.18,
  },
  // UME-003 — critical, informal_sector_health_catastrophe (informal>0.85, child_labor>0.80)
  {
    entity_id: "UME-003", electronics_sector: "recyclage_artisanal", region: "AFRIQUE_OUEST",
    ewaste_volume_growth: 0.90, informal_recycling_rate: 0.90,
    toxic_chemical_exposure: 0.78, heavy_metal_leaching: 0.72,
    gold_silver_recovery_rate: 0.82, rare_earth_extraction: 0.80,
    battery_recycling_gap: 0.88, circular_economy_adoption: 0.15,
    producer_take_back_compliance: 0.12, child_labor_exposure: 0.85,
    cross_border_illegal_shipment: 0.82, consumer_awareness: 0.10,
    repair_right_access: 0.15, collection_infrastructure: 0.12,
    data_destruction_security: 0.12, recycling_technology_gap: 0.85,
    regulatory_enforcement: 0.10,
  },
  // UME-004 — high, extended_producer_responsibility_failure (producer>0.80, regulatory>0.75)
  {
    entity_id: "UME-004", electronics_sector: "fabricant_électronique", region: "EMEA",
    ewaste_volume_growth: 0.55, informal_recycling_rate: 0.45,
    toxic_chemical_exposure: 0.48, heavy_metal_leaching: 0.45,
    gold_silver_recovery_rate: 0.50, rare_earth_extraction: 0.48,
    battery_recycling_gap: 0.52, circular_economy_adoption: 0.42,
    producer_take_back_compliance: 0.85, child_labor_exposure: 0.35,
    cross_border_illegal_shipment: 0.48, consumer_awareness: 0.45,
    repair_right_access: 0.42, collection_infrastructure: 0.45,
    data_destruction_security: 0.48, recycling_technology_gap: 0.50,
    regulatory_enforcement: 0.80,
  },
  // UME-005 — high, planned_obsolescence_acceleration (ewaste>0.80, recycling_tech>0.75)
  {
    entity_id: "UME-005", electronics_sector: "grande_consommation", region: "NOAM",
    ewaste_volume_growth: 0.85, informal_recycling_rate: 0.40,
    toxic_chemical_exposure: 0.42, heavy_metal_leaching: 0.40,
    gold_silver_recovery_rate: 0.45, rare_earth_extraction: 0.42,
    battery_recycling_gap: 0.55, circular_economy_adoption: 0.38,
    producer_take_back_compliance: 0.40, child_labor_exposure: 0.25,
    cross_border_illegal_shipment: 0.45, consumer_awareness: 0.42,
    repair_right_access: 0.40, collection_infrastructure: 0.42,
    data_destruction_security: 0.45, recycling_technology_gap: 0.80,
    regulatory_enforcement: 0.38,
  },
  // UME-006 — moderate, none
  {
    entity_id: "UME-006", electronics_sector: "collecte_municipale", region: "LATAM",
    ewaste_volume_growth: 0.30, informal_recycling_rate: 0.28,
    toxic_chemical_exposure: 0.30, heavy_metal_leaching: 0.28,
    gold_silver_recovery_rate: 0.30, rare_earth_extraction: 0.28,
    battery_recycling_gap: 0.32, circular_economy_adoption: 0.30,
    producer_take_back_compliance: 0.28, child_labor_exposure: 0.18,
    cross_border_illegal_shipment: 0.25, consumer_awareness: 0.32,
    repair_right_access: 0.30, collection_infrastructure: 0.28,
    data_destruction_security: 0.30, recycling_technology_gap: 0.30,
    regulatory_enforcement: 0.28,
  },
  // UME-007 — low, none
  {
    entity_id: "UME-007", electronics_sector: "recyclage_certifié", region: "EMEA",
    ewaste_volume_growth: 0.10, informal_recycling_rate: 0.08,
    toxic_chemical_exposure: 0.10, heavy_metal_leaching: 0.08,
    gold_silver_recovery_rate: 0.10, rare_earth_extraction: 0.08,
    battery_recycling_gap: 0.10, circular_economy_adoption: 0.12,
    producer_take_back_compliance: 0.10, child_labor_exposure: 0.05,
    cross_border_illegal_shipment: 0.08, consumer_awareness: 0.12,
    repair_right_access: 0.10, collection_infrastructure: 0.12,
    data_destruction_security: 0.10, recycling_technology_gap: 0.08,
    regulatory_enforcement: 0.12,
  },
  // UME-008 — low, none
  {
    entity_id: "UME-008", electronics_sector: "réparation_reconditionnement", region: "NOAM",
    ewaste_volume_growth: 0.08, informal_recycling_rate: 0.10,
    toxic_chemical_exposure: 0.08, heavy_metal_leaching: 0.10,
    gold_silver_recovery_rate: 0.08, rare_earth_extraction: 0.10,
    battery_recycling_gap: 0.08, circular_economy_adoption: 0.10,
    producer_take_back_compliance: 0.12, child_labor_exposure: 0.04,
    cross_border_illegal_shipment: 0.06, consumer_awareness: 0.10,
    repair_right_access: 0.12, collection_infrastructure: 0.10,
    data_destruction_security: 0.08, recycling_technology_gap: 0.10,
    regulatory_enforcement: 0.10,
  },
];

type UMEInput = (typeof MOCK_ENTITIES)[0];

function ewasteScore(e: UMEInput): number {
  return Math.round((e.ewaste_volume_growth * 0.4 + e.battery_recycling_gap * 0.35 + e.cross_border_illegal_shipment * 0.25) * 100 * 100) / 100;
}
function recoveryScore(e: UMEInput): number {
  return Math.round((e.gold_silver_recovery_rate * 0.4 + e.rare_earth_extraction * 0.35 + e.circular_economy_adoption * 0.25) * 100 * 100) / 100;
}
function toxicityScore(e: UMEInput): number {
  return Math.round((e.toxic_chemical_exposure * 0.4 + e.heavy_metal_leaching * 0.35 + e.child_labor_exposure * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: UMEInput): number {
  return Math.round((e.regulatory_enforcement * 0.4 + e.producer_take_back_compliance * 0.35 + e.collection_infrastructure * 0.25) * 100 * 100) / 100;
}
function compositeScore(ew: number, rec: number, tox: number, gov: number): number {
  return Math.round((ew * 0.30 + rec * 0.25 + tox * 0.25 + gov * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function miningPattern(e: UMEInput): string {
  if (e.toxic_chemical_exposure > 0.85 && e.heavy_metal_leaching > 0.80) return "toxic_ewaste_dumping_crisis";
  if (e.gold_silver_recovery_rate > 0.85 && e.rare_earth_extraction > 0.80) return "critical_metal_supply_gap";
  if (e.informal_recycling_rate > 0.85 && e.child_labor_exposure > 0.80) return "informal_sector_health_catastrophe";
  if (e.producer_take_back_compliance > 0.80 && e.regulatory_enforcement > 0.75) return "extended_producer_responsibility_failure";
  if (e.ewaste_volume_growth > 0.80 && e.recycling_technology_gap > 0.75) return "planned_obsolescence_acceleration";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_minage_urbain_systémique";
  if (composite >= 40) return "crise_recyclage_déchets_électroniques_majeure";
  if (composite >= 20) return "déficit_économie_circulaire_structurel";
  return "surveillance_filière_déchets_électroniques";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_minage_urbain_critique";
  if (risk === "high") return "renforcement_filière_recyclage_électronique_accéléré";
  if (risk === "moderate") return "amélioration_collecte_et_traçabilité_déchets";
  return "veille_minage_urbain_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise minage urbain systémique — recyclage déchets électroniques en péril";
  if (risk === "high") return "🟠 Crise recyclage déchets électroniques majeure détectée";
  if (risk === "moderate") return "🟡 Déficit économie circulaire structurel actif";
  return "🟢 Filière déchets électroniques sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const ew   = ewasteScore(e);
      const rec  = recoveryScore(e);
      const tox  = toxicityScore(e);
      const gov  = governanceScore(e);
      const comp = compositeScore(ew, rec, tox, gov);
      const risk = riskLevel(comp);
      const pat  = miningPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        entity_id:                    e.entity_id,
        electronics_sector:           e.electronics_sector,
        region:                       e.region,
        ewaste_score:                 ew,
        recovery_score:               rec,
        toxicity_score:               tox,
        governance_score:             gov,
        composite_score:              comp,
        risk_level:                   risk,
        mining_pattern:               pat,
        severity:                     sev,
        recommended_action:           action,
        signal:                       sig,
        ewaste_volume_growth:         e.ewaste_volume_growth,
        informal_recycling_rate:      e.informal_recycling_rate,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tEw = 0, tRec = 0, tTox = 0, tGov = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.mining_pattern]    = (pattern_distribution[ent.mining_pattern]    || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tEw   += ent.ewaste_score;
      tRec  += ent.recovery_score;
      tTox  += ent.toxicity_score;
      tGov  += ent.governance_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;
    const avgEwaste    = Math.round(tEw   / n * 10) / 10;

    const summary = {
      module_id:                            410,
      module_name:                          "Minage Urbain & Recyclage Déchets Électroniques Intelligence Engine",
      total:                                n,
      critical:                             criticalCount,
      high:                                 highCount,
      moderate:                             moderateCount,
      low:                                  lowCount,
      avg_composite:                        avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_urban_mining_index:     Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, avg_ewaste: avgEwaste }, "urban-mining-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/urban-mining-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "urban-mining-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "urban-mining-engine"),
      { status: 502 }
    );
  }
}
