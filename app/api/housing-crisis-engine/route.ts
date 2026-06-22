import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // HCE-001 — critical, homelessness_crisis_explosion (homeless>0.85, eviction>0.80)
  {
    id: "HCE-001", market_type: "logement_social", region: "Île-de-France",
    price_to_income_ratio: 0.90, rent_burden_rate: 0.85,
    homelessness_prevalence: 0.92, speculative_investment_share: 0.72,
    vacancy_rate: 0.65, social_housing_stock: 0.75,
    construction_deficit: 0.70, eviction_rate: 0.88,
    landlord_monopolization: 0.68, first_buyer_exclusion: 0.82,
    geographic_segregation: 0.72, displacement_intensity: 0.70,
    zoning_restrictiveness: 0.68, tenant_protection_gap: 0.72,
    mortgage_debt_burden: 0.75, public_housing_waitlist: 0.80,
    financialization_intensity: 0.70,
  },
  // HCE-002 — critical, financialization_speculation_trap (financialization>0.85, speculative>0.80)
  {
    id: "HCE-002", market_type: "marché_locatif", region: "Grand Paris",
    price_to_income_ratio: 0.88, rent_burden_rate: 0.80,
    homelessness_prevalence: 0.68, speculative_investment_share: 0.85,
    vacancy_rate: 0.60, social_housing_stock: 0.65,
    construction_deficit: 0.72, eviction_rate: 0.68,
    landlord_monopolization: 0.78, first_buyer_exclusion: 0.80,
    geographic_segregation: 0.68, displacement_intensity: 0.72,
    zoning_restrictiveness: 0.70, tenant_protection_gap: 0.75,
    mortgage_debt_burden: 0.72, public_housing_waitlist: 0.70,
    financialization_intensity: 0.90,
  },
  // HCE-003 — critical, rental_market_collapse (tenant_protection>0.85, rent_burden>0.80)
  {
    id: "HCE-003", market_type: "résidentiel_privé", region: "Lyon Métropole",
    price_to_income_ratio: 0.82, rent_burden_rate: 0.88,
    homelessness_prevalence: 0.70, speculative_investment_share: 0.68,
    vacancy_rate: 0.60, social_housing_stock: 0.65,
    construction_deficit: 0.72, eviction_rate: 0.70,
    landlord_monopolization: 0.65, first_buyer_exclusion: 0.78,
    geographic_segregation: 0.65, displacement_intensity: 0.68,
    zoning_restrictiveness: 0.70, tenant_protection_gap: 0.88,
    mortgage_debt_burden: 0.72, public_housing_waitlist: 0.68,
    financialization_intensity: 0.65,
  },
  // HCE-004 — high, displacement_gentrification (displacement>0.80, geo_segregation>0.75)
  {
    id: "HCE-004", market_type: "réhabilitation_urbaine", region: "Marseille",
    price_to_income_ratio: 0.55, rent_burden_rate: 0.52,
    homelessness_prevalence: 0.50, speculative_investment_share: 0.48,
    vacancy_rate: 0.45, social_housing_stock: 0.50,
    construction_deficit: 0.48, eviction_rate: 0.50,
    landlord_monopolization: 0.48, first_buyer_exclusion: 0.52,
    geographic_segregation: 0.80, displacement_intensity: 0.85,
    zoning_restrictiveness: 0.50, tenant_protection_gap: 0.48,
    mortgage_debt_burden: 0.50, public_housing_waitlist: 0.52,
    financialization_intensity: 0.48,
  },
  // HCE-005 — high, social_housing_defunding (social_housing>0.80, waitlist>0.75)
  {
    id: "HCE-005", market_type: "habitat_social", region: "Bordeaux",
    price_to_income_ratio: 0.50, rent_burden_rate: 0.48,
    homelessness_prevalence: 0.52, speculative_investment_share: 0.48,
    vacancy_rate: 0.45, social_housing_stock: 0.85,
    construction_deficit: 0.50, eviction_rate: 0.48,
    landlord_monopolization: 0.45, first_buyer_exclusion: 0.50,
    geographic_segregation: 0.48, displacement_intensity: 0.50,
    zoning_restrictiveness: 0.48, tenant_protection_gap: 0.50,
    mortgage_debt_burden: 0.48, public_housing_waitlist: 0.82,
    financialization_intensity: 0.45,
  },
  // HCE-006 — moderate, none
  {
    id: "HCE-006", market_type: "péri_urbain", region: "Nantes",
    price_to_income_ratio: 0.30, rent_burden_rate: 0.28,
    homelessness_prevalence: 0.30, speculative_investment_share: 0.28,
    vacancy_rate: 0.25, social_housing_stock: 0.30,
    construction_deficit: 0.28, eviction_rate: 0.30,
    landlord_monopolization: 0.28, first_buyer_exclusion: 0.32,
    geographic_segregation: 0.28, displacement_intensity: 0.30,
    zoning_restrictiveness: 0.28, tenant_protection_gap: 0.30,
    mortgage_debt_burden: 0.28, public_housing_waitlist: 0.30,
    financialization_intensity: 0.28,
  },
  // HCE-007 — low, none
  {
    id: "HCE-007", market_type: "rural", region: "Bretagne",
    price_to_income_ratio: 0.10, rent_burden_rate: 0.12,
    homelessness_prevalence: 0.10, speculative_investment_share: 0.12,
    vacancy_rate: 0.10, social_housing_stock: 0.12,
    construction_deficit: 0.10, eviction_rate: 0.12,
    landlord_monopolization: 0.10, first_buyer_exclusion: 0.12,
    geographic_segregation: 0.10, displacement_intensity: 0.12,
    zoning_restrictiveness: 0.10, tenant_protection_gap: 0.12,
    mortgage_debt_burden: 0.10, public_housing_waitlist: 0.12,
    financialization_intensity: 0.10,
  },
  // HCE-008 — low, none
  {
    id: "HCE-008", market_type: "copropriété", region: "Alsace",
    price_to_income_ratio: 0.12, rent_burden_rate: 0.10,
    homelessness_prevalence: 0.12, speculative_investment_share: 0.10,
    vacancy_rate: 0.12, social_housing_stock: 0.10,
    construction_deficit: 0.12, eviction_rate: 0.10,
    landlord_monopolization: 0.12, first_buyer_exclusion: 0.10,
    geographic_segregation: 0.12, displacement_intensity: 0.10,
    zoning_restrictiveness: 0.12, tenant_protection_gap: 0.10,
    mortgage_debt_burden: 0.12, public_housing_waitlist: 0.10,
    financialization_intensity: 0.12,
  },
];

type HCEInput = typeof MOCK_ENTITIES[0];

function affordabilityScore(e: HCEInput): number {
  return Math.round((e.price_to_income_ratio * 0.4 + e.rent_burden_rate * 0.35 + e.first_buyer_exclusion * 0.25) * 100 * 100) / 100;
}
function speculationScore(e: HCEInput): number {
  return Math.round((e.speculative_investment_share * 0.4 + e.financialization_intensity * 0.35 + e.landlord_monopolization * 0.25) * 100 * 100) / 100;
}
function supplyScore(e: HCEInput): number {
  return Math.round((e.construction_deficit * 0.4 + e.zoning_restrictiveness * 0.35 + e.vacancy_rate * 0.25) * 100 * 100) / 100;
}
function homelessnessScore(e: HCEInput): number {
  return Math.round((e.homelessness_prevalence * 0.4 + e.eviction_rate * 0.35 + e.public_housing_waitlist * 0.25) * 100 * 100) / 100;
}
function compositeScore(aff: number, spe: number, sup: number, hom: number): number {
  return Math.round((aff * 0.30 + spe * 0.25 + sup * 0.25 + hom * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critique";
  if (composite >= 40) return "élevé";
  if (composite >= 20) return "modéré";
  return "faible";
}
function housingPattern(e: HCEInput): string {
  if (e.homelessness_prevalence > 0.85 && e.eviction_rate > 0.80) return "homelessness_crisis_explosion";
  if (e.financialization_intensity > 0.85 && e.speculative_investment_share > 0.80) return "financialization_speculation_trap";
  if (e.tenant_protection_gap > 0.85 && e.rent_burden_rate > 0.80) return "rental_market_collapse";
  if (e.displacement_intensity > 0.80 && e.geographic_segregation > 0.75) return "displacement_gentrification";
  if (e.social_housing_stock > 0.80 && e.public_housing_waitlist > 0.75) return "social_housing_defunding";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_logement_systémique_critique";
  if (composite >= 40) return "crise_accessibilité_immobilière_majeure";
  if (composite >= 20) return "tension_marché_immobilier_structurelle";
  return "marché_logement_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critique") return "intervention_urgente_crise_logement_systémique";
  if (risk === "élevé") return "régulation_marché_immobilier_accélérée";
  if (risk === "modéré") return "renforcement_politiques_accessibilité_logement";
  return "veille_marché_logement_continue";
}
function signal(risk: string): string {
  if (risk === "critique") return "🔴 Crise logement systémique — accessibilité immobilière en péril";
  if (risk === "élevé") return "🟠 Crise accessibilité immobilière majeure détectée";
  if (risk === "modéré") return "🟡 Tension marché immobilier structurelle active";
  return "🟢 Marché logement sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[housing-crisis-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tAff = 0, tSpe = 0, tSup = 0, tHom = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.housing_pattern]   = (pattern_distribution[ent.housing_pattern]   || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tAff  += ent.affordability_score;
      tSpe  += ent.speculation_score;
      tSup  += ent.supply_score;
      tHom  += ent.homelessness_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critique")       criticalCount++;
      else if (ent.risk_level === "élevé")     highCount++;
      else if (ent.risk_level === "modéré")    moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite        = Math.round(tComp / n * 10) / 10;
    const avgAffordability    = Math.round(tAff  / n * 10) / 10;

    const summary = {
      module_id:                                    422,
      module_name:                                  "Crise Logement & Accessibilité Immobilière Intelligence Engine",
      total:                                        n,
      critical:                                     criticalCount,
      high:                                         highCount,
      moderate:                                     moderateCount,
      low:                                          lowCount,
      avg_composite:                                avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_housing_affordability_index:    Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary, avg_affordability: avgAffordability }, "housing-crisis-engine")
    ));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/housing-crisis-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return sealResponse(NextResponse.json(sealResponse(await upstream.json(), "housing-crisis-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "housing-crisis-engine"),
      { status: 502 }
    ));
  }
}
