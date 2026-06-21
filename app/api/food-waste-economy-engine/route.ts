import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  // FWE-001 — critique — grande_distribution, Île-de-France
  // patterns: retail_overproduction_dump, cold_chain_collapse, date_label_confusion, consumer_behavioral_waste, policy_incentive_failure
  {
    id: "FWE-001", food_sector: "grande_distribution", region: "Île-de-France",
    retail_waste_rate: 80.0, production_surplus: 75.0, cold_chain_failure: 60.0,
    date_labeling_confusion: 70.0, consumer_waste_behavior: 65.0, redistribution_gap: 70.0,
    composting_infrastructure: 80.0, regulatory_compliance_gap: 70.0,
    supply_chain_inefficiency: 65.0, packaging_waste_impact: 70.0,
    food_bank_capacity: 20.0, corporate_responsibility_gap: 65.0,
    circular_economy_adoption: 75.0, economic_loss_per_capita: 1200.0,
    biodiversity_impact: 70.0, water_waste_embedded: 65.0, carbon_footprint_waste: 75.0,
  },
  // FWE-002 — critique — logistique_alimentaire, Auvergne-Rhône-Alpes
  // patterns: retail_overproduction_dump, cold_chain_collapse, date_label_confusion, consumer_behavioral_waste, policy_incentive_failure
  {
    id: "FWE-002", food_sector: "logistique_alimentaire", region: "Auvergne-Rhône-Alpes",
    retail_waste_rate: 65.0, production_surplus: 65.0, cold_chain_failure: 80.0,
    date_labeling_confusion: 55.0, consumer_waste_behavior: 60.0, redistribution_gap: 72.0,
    composting_infrastructure: 75.0, regulatory_compliance_gap: 60.0,
    supply_chain_inefficiency: 75.0, packaging_waste_impact: 70.0,
    food_bank_capacity: 25.0, corporate_responsibility_gap: 60.0,
    circular_economy_adoption: 80.0, economic_loss_per_capita: 1100.0,
    biodiversity_impact: 65.0, water_waste_embedded: 68.0, carbon_footprint_waste: 70.0,
  },
  // FWE-003 — critique — restauration_collective, Hauts-de-France
  // patterns: retail_overproduction_dump, date_label_confusion, consumer_behavioral_waste, policy_incentive_failure
  {
    id: "FWE-003", food_sector: "restauration_collective", region: "Hauts-de-France",
    retail_waste_rate: 70.0, production_surplus: 68.0, cold_chain_failure: 50.0,
    date_labeling_confusion: 55.0, consumer_waste_behavior: 80.0, redistribution_gap: 65.0,
    composting_infrastructure: 80.0, regulatory_compliance_gap: 65.0,
    supply_chain_inefficiency: 60.0, packaging_waste_impact: 62.0,
    food_bank_capacity: 30.0, corporate_responsibility_gap: 70.0,
    circular_economy_adoption: 78.0, economic_loss_per_capita: 950.0,
    biodiversity_impact: 68.0, water_waste_embedded: 58.0, carbon_footprint_waste: 72.0,
  },
  // FWE-004 — élevé — industrie_agroalimentaire, Bretagne
  // pattern: date_label_confusion
  {
    id: "FWE-004", food_sector: "industrie_agroalimentaire", region: "Bretagne",
    retail_waste_rate: 50.0, production_surplus: 48.0, cold_chain_failure: 45.0,
    date_labeling_confusion: 70.0, consumer_waste_behavior: 48.0, redistribution_gap: 52.0,
    composting_infrastructure: 60.0, regulatory_compliance_gap: 50.0,
    supply_chain_inefficiency: 50.0, packaging_waste_impact: 48.0,
    food_bank_capacity: 40.0, corporate_responsibility_gap: 48.0,
    circular_economy_adoption: 55.0, economic_loss_per_capita: 650.0,
    biodiversity_impact: 50.0, water_waste_embedded: 45.0, carbon_footprint_waste: 48.0,
  },
  // FWE-005 — élevé — coopérative_agricole, Nouvelle-Aquitaine
  // pattern: policy_incentive_failure
  {
    id: "FWE-005", food_sector: "coopérative_agricole", region: "Nouvelle-Aquitaine",
    retail_waste_rate: 52.0, production_surplus: 50.0, cold_chain_failure: 48.0,
    date_labeling_confusion: 50.0, consumer_waste_behavior: 50.0, redistribution_gap: 55.0,
    composting_infrastructure: 62.0, regulatory_compliance_gap: 70.0,
    supply_chain_inefficiency: 52.0, packaging_waste_impact: 50.0,
    food_bank_capacity: 35.0, corporate_responsibility_gap: 65.0,
    circular_economy_adoption: 58.0, economic_loss_per_capita: 700.0,
    biodiversity_impact: 52.0, water_waste_embedded: 48.0, carbon_footprint_waste: 50.0,
  },
  // FWE-006 — modéré — marché_de_proximité, Occitanie
  {
    id: "FWE-006", food_sector: "marché_de_proximité", region: "Occitanie",
    retail_waste_rate: 30.0, production_surplus: 28.0, cold_chain_failure: 25.0,
    date_labeling_confusion: 30.0, consumer_waste_behavior: 28.0, redistribution_gap: 32.0,
    composting_infrastructure: 55.0, regulatory_compliance_gap: 28.0,
    supply_chain_inefficiency: 30.0, packaging_waste_impact: 28.0,
    food_bank_capacity: 60.0, corporate_responsibility_gap: 30.0,
    circular_economy_adoption: 50.0, economic_loss_per_capita: 350.0,
    biodiversity_impact: 30.0, water_waste_embedded: 25.0, carbon_footprint_waste: 28.0,
  },
  // FWE-007 — faible — filière_biologique, Pays de la Loire
  {
    id: "FWE-007", food_sector: "filière_biologique", region: "Pays de la Loire",
    retail_waste_rate: 10.0, production_surplus: 12.0, cold_chain_failure: 10.0,
    date_labeling_confusion: 12.0, consumer_waste_behavior: 8.0, redistribution_gap: 10.0,
    composting_infrastructure: 20.0, regulatory_compliance_gap: 10.0,
    supply_chain_inefficiency: 12.0, packaging_waste_impact: 10.0,
    food_bank_capacity: 80.0, corporate_responsibility_gap: 12.0,
    circular_economy_adoption: 25.0, economic_loss_per_capita: 80.0,
    biodiversity_impact: 10.0, water_waste_embedded: 8.0, carbon_footprint_waste: 8.0,
  },
  // FWE-008 — faible — agriculture_raisonnée, Grand Est
  {
    id: "FWE-008", food_sector: "agriculture_raisonnée", region: "Grand Est",
    retail_waste_rate: 8.0, production_surplus: 10.0, cold_chain_failure: 8.0,
    date_labeling_confusion: 10.0, consumer_waste_behavior: 10.0, redistribution_gap: 8.0,
    composting_infrastructure: 15.0, regulatory_compliance_gap: 8.0,
    supply_chain_inefficiency: 10.0, packaging_waste_impact: 8.0,
    food_bank_capacity: 85.0, corporate_responsibility_gap: 10.0,
    circular_economy_adoption: 20.0, economic_loss_per_capita: 60.0,
    biodiversity_impact: 8.0, water_waste_embedded: 10.0, carbon_footprint_waste: 10.0,
  },
];

type FWEInput = (typeof MOCK_ENTITIES)[0];

function wasteScore(e: FWEInput): number {
  return Math.round(((e.retail_waste_rate + e.production_surplus + e.redistribution_gap + e.consumer_waste_behavior) / 4) * 100) / 100;
}
function supplyChainScore(e: FWEInput): number {
  return Math.round(((e.cold_chain_failure + e.supply_chain_inefficiency + e.packaging_waste_impact + e.water_waste_embedded) / 4) * 100) / 100;
}
function policyScore(e: FWEInput): number {
  return Math.round(((e.date_labeling_confusion + e.regulatory_compliance_gap + e.corporate_responsibility_gap + (100 - e.food_bank_capacity)) / 4) * 100) / 100;
}
function circularScore(e: FWEInput): number {
  return Math.round((((100 - e.composting_infrastructure) + (100 - e.circular_economy_adoption) + e.biodiversity_impact + e.carbon_footprint_waste) / 4) * 100) / 100;
}
function compositeScore(waste: number, supply: number, policy: number, circular: number): number {
  return Math.round((waste * 0.30 + supply * 0.25 + policy * 0.25 + circular * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function detectPatterns(e: FWEInput): string[] {
  const pats: string[] = [];
  if (e.retail_waste_rate > 60 || e.production_surplus > 60) pats.push("retail_overproduction_dump");
  if (e.cold_chain_failure > 55) pats.push("cold_chain_collapse");
  if (e.date_labeling_confusion > 50) pats.push("date_label_confusion");
  if (e.consumer_waste_behavior > 55) pats.push("consumer_behavioral_waste");
  if (e.regulatory_compliance_gap > 55 || e.corporate_responsibility_gap > 55) pats.push("policy_incentive_failure");
  return pats;
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const waste   = wasteScore(e);
      const supply  = supplyChainScore(e);
      const policy  = policyScore(e);
      const circ    = circularScore(e);
      const comp    = compositeScore(waste, supply, policy, circ);
      const risk    = riskLevel(comp);
      const pats    = detectPatterns(e);
      return {
        id:              e.entity_id,
        food_sector:            e.food_sector,
        region:                 e.region,
        waste_score:            waste,
        supply_chain_score:     supply,
        policy_score:           policy,
        circular_score:         circ,
        composite_score:        comp,
        risk_level:             risk,
        patterns:               pats,
        economic_loss_per_capita: e.economic_loss_per_capita,
        water_waste_embedded:   e.water_waste_embedded,
        carbon_footprint_waste: e.carbon_footprint_waste,
        biodiversity_impact:    e.biodiversity_impact,
        estimated_food_waste_index: Math.round(comp / 100 * 10 * 100) / 100,
      };
    });

    const risk_distribution: Record<string, number>    = {};
    const pattern_distribution: Record<string, number> = {};
    let tWaste = 0, tSupply = 0, tPolicy = 0, tCircular = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level] = (risk_distribution[ent.risk_level] || 0) + 1;
      for (const pat of ent.patterns) {
        pattern_distribution[pat] = (pattern_distribution[pat] || 0) + 1;
      }
      tWaste   += ent.waste_score;
      tSupply  += ent.supply_chain_score;
      tPolicy  += ent.policy_score;
      tCircular += ent.circular_score;
      tComp    += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgWaste    = Math.round(tWaste   / n * 10) / 10;
    const avgSupply   = Math.round(tSupply  / n * 10) / 10;
    const avgPolicy   = Math.round(tPolicy  / n * 10) / 10;
    const avgCircular = Math.round(tCircular / n * 10) / 10;
    const avgComposite = Math.round(tComp   / n * 10) / 10;

    const summary = {
      total_entities:                   n,
      critical_count:                   criticalCount,
      high_count:                       highCount,
      moderate_count:                   moderateCount,
      low_count:                        lowCount,
      avg_waste_score:                  avgWaste,
      avg_supply_chain_score:           avgSupply,
      avg_policy_score:                 avgPolicy,
      avg_circular_score:               avgCircular,
      avg_composite_score:              avgComposite,
      top_patterns:                     pattern_distribution,
      risk_distribution:                risk_distribution,
      avg_estimated_food_waste_index:   Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/food-waste-economy-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(sealResponse(await res.json()));
  } catch {}
  return NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 });
}
