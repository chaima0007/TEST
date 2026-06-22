import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[alternative-protein-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

if (!SWARM_API_URL) {
  console.warn("[alternative-protein-engine] SWARM_API_URL is not configured");
}

// ── Mock entity input data ────────────────────────────────────────────────────

const MOCK_ENTITIES = [
  // APE-001: cultivated_meat, LATAM → critical risk, livestock_disruption_crisis
  {
    id: "APE-001", protein_sector: "cultivated_meat", region: "LATAM",
    cultivated_meat_cost_parity_proximity: 0.82, plant_based_market_saturation_risk: 0.50,
    precision_fermentation_disruption: 0.75, traditional_livestock_industry_disruption_speed: 0.88,
    regulatory_approval_barrier_level: 0.55, consumer_acceptance_gap: 0.60,
    intellectual_property_concentration_risk: 0.68, biotech_monopoly_in_food_production: 0.72,
    nutritional_transition_risk: 0.58, supply_chain_protein_transition_fragility: 0.70,
    small_farmer_displacement_rate: 0.68, food_sovereignty_tech_capture: 0.65,
    allergen_safety_gap_in_novel_proteins: 0.60, carbon_emission_protein_transition_benefit: 0.45,
    protein_transition_inequality: 0.65, food_culture_disruption_index: 0.70,
    cellular_agriculture_biosafety_risk: 0.55,
  },
  // APE-002: plant_based, EMEA → low risk, none pattern
  {
    id: "APE-002", protein_sector: "plant_based", region: "EMEA",
    cultivated_meat_cost_parity_proximity: 0.15, plant_based_market_saturation_risk: 0.20,
    precision_fermentation_disruption: 0.12, traditional_livestock_industry_disruption_speed: 0.18,
    regulatory_approval_barrier_level: 0.20, consumer_acceptance_gap: 0.15,
    intellectual_property_concentration_risk: 0.16, biotech_monopoly_in_food_production: 0.14,
    nutritional_transition_risk: 0.15, supply_chain_protein_transition_fragility: 0.15,
    small_farmer_displacement_rate: 0.14, food_sovereignty_tech_capture: 0.12,
    allergen_safety_gap_in_novel_proteins: 0.12, carbon_emission_protein_transition_benefit: 0.80,
    protein_transition_inequality: 0.16, food_culture_disruption_index: 0.12,
    cellular_agriculture_biosafety_risk: 0.10,
  },
  // APE-003: precision_fermentation, NOAM → high risk, biotech_food_monopoly
  {
    id: "APE-003", protein_sector: "precision_fermentation", region: "NOAM",
    cultivated_meat_cost_parity_proximity: 0.48, plant_based_market_saturation_risk: 0.45,
    precision_fermentation_disruption: 0.45, traditional_livestock_industry_disruption_speed: 0.50,
    regulatory_approval_barrier_level: 0.52, consumer_acceptance_gap: 0.50,
    intellectual_property_concentration_risk: 0.75, biotech_monopoly_in_food_production: 0.82,
    nutritional_transition_risk: 0.45, supply_chain_protein_transition_fragility: 0.52,
    small_farmer_displacement_rate: 0.50, food_sovereignty_tech_capture: 0.55,
    allergen_safety_gap_in_novel_proteins: 0.45, carbon_emission_protein_transition_benefit: 0.45,
    protein_transition_inequality: 0.48, food_culture_disruption_index: 0.50,
    cellular_agriculture_biosafety_risk: 0.42,
  },
  // APE-004: insect_protein, APAC → low risk, none pattern
  {
    id: "APE-004", protein_sector: "insect_protein", region: "APAC",
    cultivated_meat_cost_parity_proximity: 0.12, plant_based_market_saturation_risk: 0.15,
    precision_fermentation_disruption: 0.10, traditional_livestock_industry_disruption_speed: 0.15,
    regulatory_approval_barrier_level: 0.22, consumer_acceptance_gap: 0.20,
    intellectual_property_concentration_risk: 0.15, biotech_monopoly_in_food_production: 0.18,
    nutritional_transition_risk: 0.15, supply_chain_protein_transition_fragility: 0.12,
    small_farmer_displacement_rate: 0.16, food_sovereignty_tech_capture: 0.10,
    allergen_safety_gap_in_novel_proteins: 0.10, carbon_emission_protein_transition_benefit: 0.85,
    protein_transition_inequality: 0.14, food_culture_disruption_index: 0.10,
    cellular_agriculture_biosafety_risk: 0.12,
  },
  // APE-005: cultivated_meat, APAC → critical risk, food_sovereignty_capture
  {
    id: "APE-005", protein_sector: "cultivated_meat", region: "APAC",
    cultivated_meat_cost_parity_proximity: 0.75, plant_based_market_saturation_risk: 0.55,
    precision_fermentation_disruption: 0.68, traditional_livestock_industry_disruption_speed: 0.72,
    regulatory_approval_barrier_level: 0.55, consumer_acceptance_gap: 0.60,
    intellectual_property_concentration_risk: 0.62, biotech_monopoly_in_food_production: 0.65,
    nutritional_transition_risk: 0.58, supply_chain_protein_transition_fragility: 0.68,
    small_farmer_displacement_rate: 0.80, food_sovereignty_tech_capture: 0.85,
    allergen_safety_gap_in_novel_proteins: 0.55, carbon_emission_protein_transition_benefit: 0.40,
    protein_transition_inequality: 0.72, food_culture_disruption_index: 0.75,
    cellular_agriculture_biosafety_risk: 0.50,
  },
  // APE-006: mycoprotein, MEA → moderate risk, none pattern
  {
    id: "APE-006", protein_sector: "mycoprotein", region: "MEA",
    cultivated_meat_cost_parity_proximity: 0.32, plant_based_market_saturation_risk: 0.30,
    precision_fermentation_disruption: 0.28, traditional_livestock_industry_disruption_speed: 0.35,
    regulatory_approval_barrier_level: 0.38, consumer_acceptance_gap: 0.35,
    intellectual_property_concentration_risk: 0.35, biotech_monopoly_in_food_production: 0.30,
    nutritional_transition_risk: 0.32, supply_chain_protein_transition_fragility: 0.32,
    small_farmer_displacement_rate: 0.30, food_sovereignty_tech_capture: 0.28,
    allergen_safety_gap_in_novel_proteins: 0.30, carbon_emission_protein_transition_benefit: 0.65,
    protein_transition_inequality: 0.28, food_culture_disruption_index: 0.32,
    cellular_agriculture_biosafety_risk: 0.28,
  },
  // APE-007: algae_protein, EMEA → high risk, transition_inequality_trap
  {
    id: "APE-007", protein_sector: "algae_protein", region: "EMEA",
    cultivated_meat_cost_parity_proximity: 0.50, plant_based_market_saturation_risk: 0.48,
    precision_fermentation_disruption: 0.45, traditional_livestock_industry_disruption_speed: 0.52,
    regulatory_approval_barrier_level: 0.52, consumer_acceptance_gap: 0.50,
    intellectual_property_concentration_risk: 0.50, biotech_monopoly_in_food_production: 0.48,
    nutritional_transition_risk: 0.45, supply_chain_protein_transition_fragility: 0.78,
    small_farmer_displacement_rate: 0.55, food_sovereignty_tech_capture: 0.45,
    allergen_safety_gap_in_novel_proteins: 0.42, carbon_emission_protein_transition_benefit: 0.40,
    protein_transition_inequality: 0.82, food_culture_disruption_index: 0.48,
    cellular_agriculture_biosafety_risk: 0.38,
  },
  // APE-008: cellular_agriculture, NOAM → critical risk, biosafety_novel_protein
  {
    id: "APE-008", protein_sector: "cellular_agriculture", region: "NOAM",
    cultivated_meat_cost_parity_proximity: 0.65, plant_based_market_saturation_risk: 0.55,
    precision_fermentation_disruption: 0.58, traditional_livestock_industry_disruption_speed: 0.60,
    regulatory_approval_barrier_level: 0.60, consumer_acceptance_gap: 0.65,
    intellectual_property_concentration_risk: 0.58, biotech_monopoly_in_food_production: 0.62,
    nutritional_transition_risk: 0.72, supply_chain_protein_transition_fragility: 0.60,
    small_farmer_displacement_rate: 0.58, food_sovereignty_tech_capture: 0.55,
    allergen_safety_gap_in_novel_proteins: 0.78, carbon_emission_protein_transition_benefit: 0.35,
    protein_transition_inequality: 0.62, food_culture_disruption_index: 0.65,
    cellular_agriculture_biosafety_risk: 0.85,
  },
];

export async function GET() {
  if (!SWARM_API_URL) {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "SWARM_API_URL not configured" } as Record<string, unknown>,
        "alternative-protein-engine"),
      { status: 502 }
    ));
  }

  try {
    const upstream = await fetch(`${SWARM_API_URL}/api/alternative-protein-engine`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(MOCK_ENTITIES),
      next: { revalidate: 30 },
    });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    const data = await upstream.json() as Record<string, unknown>;
    return sealResponse(NextResponse.json(sealResponse(data, "alternative-protein-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream unavailable" } as Record<string, unknown>,
        "alternative-protein-engine"),
      { status: 502 }
    ));
  }
}
