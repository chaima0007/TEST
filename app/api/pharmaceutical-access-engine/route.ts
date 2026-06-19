import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // PAE-001 — critical, life_saving_drug_unaffordability (drug_price>0.85, out_of_pocket>0.80)
  {
    entity_id: "PAE-001", therapeutic_area: "oncologie", region: "SSA",
    drug_price_index: 0.92, patent_monopoly_duration: 0.70, generic_availability: 0.65,
    insurance_coverage_gap: 0.72, out_of_pocket_burden: 0.88, compulsory_license_use: 0.68,
    clinical_trial_inclusion: 0.65, off_label_access: 0.60, essential_medicine_gap: 0.72,
    black_market_penetration: 0.60, counterfeiting_risk: 0.65, research_neglected_diseases: 0.68,
    export_restriction: 0.65, regulatory_pathway_speed: 0.60, local_manufacturing: 0.62,
    treatment_adherence: 0.68, quality_assurance_gap: 0.60,
  },
  // PAE-002 — critical, patent_monopoly_abuse (patent_monopoly>0.85, export_restriction>0.80)
  {
    entity_id: "PAE-002", therapeutic_area: "maladies_rares", region: "APAC",
    drug_price_index: 0.62, patent_monopoly_duration: 0.90, generic_availability: 0.70,
    insurance_coverage_gap: 0.65, out_of_pocket_burden: 0.65, compulsory_license_use: 0.60,
    clinical_trial_inclusion: 0.62, off_label_access: 0.58, essential_medicine_gap: 0.65,
    black_market_penetration: 0.55, counterfeiting_risk: 0.60, research_neglected_diseases: 0.65,
    export_restriction: 0.85, regulatory_pathway_speed: 0.60, local_manufacturing: 0.55,
    treatment_adherence: 0.65, quality_assurance_gap: 0.62,
  },
  // PAE-003 — critical, generic_market_suppression (generic_availability>0.85, essential_medicine_gap>0.80)
  {
    entity_id: "PAE-003", therapeutic_area: "maladies_tropicales", region: "SSA",
    drug_price_index: 0.60, patent_monopoly_duration: 0.65, generic_availability: 0.88,
    insurance_coverage_gap: 0.70, out_of_pocket_burden: 0.65, compulsory_license_use: 0.60,
    clinical_trial_inclusion: 0.62, off_label_access: 0.55, essential_medicine_gap: 0.85,
    black_market_penetration: 0.60, counterfeiting_risk: 0.65, research_neglected_diseases: 0.68,
    export_restriction: 0.62, regulatory_pathway_speed: 0.55, local_manufacturing: 0.60,
    treatment_adherence: 0.65, quality_assurance_gap: 0.62,
  },
  // PAE-004 — high, clinical_trial_exclusion (clinical_trial_inclusion>0.80, research_neglected>0.75)
  {
    entity_id: "PAE-004", therapeutic_area: "pédiatrie", region: "EMEA",
    drug_price_index: 0.48, patent_monopoly_duration: 0.50, generic_availability: 0.45,
    insurance_coverage_gap: 0.50, out_of_pocket_burden: 0.48, compulsory_license_use: 0.45,
    clinical_trial_inclusion: 0.82, off_label_access: 0.50, essential_medicine_gap: 0.50,
    black_market_penetration: 0.45, counterfeiting_risk: 0.48, research_neglected_diseases: 0.78,
    export_restriction: 0.48, regulatory_pathway_speed: 0.50, local_manufacturing: 0.45,
    treatment_adherence: 0.50, quality_assurance_gap: 0.48,
  },
  // PAE-005 — high, counterfeit_drug_proliferation (counterfeiting_risk>0.80, black_market>0.75)
  {
    entity_id: "PAE-005", therapeutic_area: "anti-infectieux", region: "LATAM",
    drug_price_index: 0.45, patent_monopoly_duration: 0.50, generic_availability: 0.48,
    insurance_coverage_gap: 0.52, out_of_pocket_burden: 0.48, compulsory_license_use: 0.45,
    clinical_trial_inclusion: 0.48, off_label_access: 0.45, essential_medicine_gap: 0.50,
    black_market_penetration: 0.78, counterfeiting_risk: 0.85, research_neglected_diseases: 0.48,
    export_restriction: 0.50, regulatory_pathway_speed: 0.45, local_manufacturing: 0.48,
    treatment_adherence: 0.50, quality_assurance_gap: 0.50,
  },
  // PAE-006 — moderate, none
  {
    entity_id: "PAE-006", therapeutic_area: "cardiovasculaire", region: "NOAM",
    drug_price_index: 0.28, patent_monopoly_duration: 0.30, generic_availability: 0.28,
    insurance_coverage_gap: 0.30, out_of_pocket_burden: 0.28, compulsory_license_use: 0.25,
    clinical_trial_inclusion: 0.28, off_label_access: 0.30, essential_medicine_gap: 0.28,
    black_market_penetration: 0.25, counterfeiting_risk: 0.28, research_neglected_diseases: 0.30,
    export_restriction: 0.28, regulatory_pathway_speed: 0.30, local_manufacturing: 0.28,
    treatment_adherence: 0.30, quality_assurance_gap: 0.28,
  },
  // PAE-007 — low, none
  {
    entity_id: "PAE-007", therapeutic_area: "diabète", region: "NOAM",
    drug_price_index: 0.10, patent_monopoly_duration: 0.12, generic_availability: 0.10,
    insurance_coverage_gap: 0.12, out_of_pocket_burden: 0.10, compulsory_license_use: 0.08,
    clinical_trial_inclusion: 0.10, off_label_access: 0.12, essential_medicine_gap: 0.10,
    black_market_penetration: 0.08, counterfeiting_risk: 0.10, research_neglected_diseases: 0.12,
    export_restriction: 0.10, regulatory_pathway_speed: 0.12, local_manufacturing: 0.08,
    treatment_adherence: 0.10, quality_assurance_gap: 0.10,
  },
  // PAE-008 — low, none
  {
    entity_id: "PAE-008", therapeutic_area: "vaccination", region: "EMEA",
    drug_price_index: 0.12, patent_monopoly_duration: 0.10, generic_availability: 0.12,
    insurance_coverage_gap: 0.10, out_of_pocket_burden: 0.12, compulsory_license_use: 0.10,
    clinical_trial_inclusion: 0.12, off_label_access: 0.10, essential_medicine_gap: 0.12,
    black_market_penetration: 0.10, counterfeiting_risk: 0.12, research_neglected_diseases: 0.10,
    export_restriction: 0.12, regulatory_pathway_speed: 0.10, local_manufacturing: 0.10,
    treatment_adherence: 0.12, quality_assurance_gap: 0.10,
  },
];

type PAEInput = typeof MOCK_ENTITIES[0];

function affordabilityScore(e: PAEInput): number {
  return Math.round((e.drug_price_index * 0.4 + e.out_of_pocket_burden * 0.35 + e.insurance_coverage_gap * 0.25) * 100 * 100) / 100;
}
function monopolyScore(e: PAEInput): number {
  return Math.round((e.patent_monopoly_duration * 0.4 + e.export_restriction * 0.35 + e.compulsory_license_use * 0.25) * 100 * 100) / 100;
}
function availabilityScore(e: PAEInput): number {
  return Math.round((e.essential_medicine_gap * 0.4 + e.generic_availability * 0.35 + e.black_market_penetration * 0.25) * 100 * 100) / 100;
}
function innovationScore(e: PAEInput): number {
  return Math.round((e.research_neglected_diseases * 0.4 + e.clinical_trial_inclusion * 0.35 + e.quality_assurance_gap * 0.25) * 100 * 100) / 100;
}
function compositeScore(aff: number, mon: number, avl: number, inn: number): number {
  return Math.round((aff * 0.30 + mon * 0.25 + avl * 0.25 + inn * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function pharmaPattern(e: PAEInput): string {
  if (e.drug_price_index > 0.85 && e.out_of_pocket_burden > 0.80) return "life_saving_drug_unaffordability";
  if (e.patent_monopoly_duration > 0.85 && e.export_restriction > 0.80) return "patent_monopoly_abuse";
  if (e.generic_availability > 0.85 && e.essential_medicine_gap > 0.80) return "generic_market_suppression";
  if (e.clinical_trial_inclusion > 0.80 && e.research_neglected_diseases > 0.75) return "clinical_trial_exclusion";
  if (e.counterfeiting_risk > 0.80 && e.black_market_penetration > 0.75) return "counterfeit_drug_proliferation";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_accès_médicaments_systémique";
  if (composite >= 40) return "crise_prix_pharmaceutiques_majeure";
  if (composite >= 20) return "inégalité_accès_médicaments_structurelle";
  return "accès_pharmaceutique_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_accès_médicaments_essentiels";
  if (risk === "high") return "négociation_prix_licences_obligatoires_accélérée";
  if (risk === "moderate") return "renforcement_politiques_accès_génériques";
  return "veille_marché_pharmaceutique_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise accès médicaments systémique — santé publique en péril";
  if (risk === "high") return "🟠 Crise prix pharmaceutiques majeure détectée";
  if (risk === "moderate") return "🟡 Inégalité accès médicaments structurelle active";
  return "🟢 Accès pharmaceutique sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const aff  = affordabilityScore(e);
      const mon  = monopolyScore(e);
      const avl  = availabilityScore(e);
      const inn  = innovationScore(e);
      const comp = compositeScore(aff, mon, avl, inn);
      const risk = riskLevel(comp);
      const pat  = pharmaPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        entity_id:             e.entity_id,
        therapeutic_area:      e.therapeutic_area,
        region:                e.region,
        affordability_score:   aff,
        monopoly_score:        mon,
        availability_score:    avl,
        innovation_score:      inn,
        composite_score:       comp,
        risk_level:            risk,
        pharma_pattern:        pat,
        severity:              sev,
        recommended_action:    action,
        signal:                sig,
        drug_price_index:      e.drug_price_index,
        counterfeiting_risk:   e.counterfeiting_risk,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tAff = 0, tMon = 0, tAvl = 0, tInn = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.pharma_pattern]    = (pattern_distribution[ent.pharma_pattern]    || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tAff  += ent.affordability_score;
      tMon  += ent.monopoly_score;
      tAvl  += ent.availability_score;
      tInn  += ent.innovation_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite        = Math.round(tComp / n * 10) / 10;
    const avgAffordability    = Math.round(tAff  / n * 10) / 10;

    const summary = {
      module_id:                           411,
      module_name:                         "Accès Médicaments & Prix Pharmaceutiques Intelligence Engine",
      total:                               n,
      critical:                            criticalCount,
      high:                                highCount,
      moderate:                            moderateCount,
      low:                                 lowCount,
      avg_composite:                       avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_pharma_access_index:   Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, avg_affordability: avgAffordability }, "pharmaceutical-access-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/pharmaceutical-access-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "pharmaceutical-access-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "pharmaceutical-access-engine"),
      { status: 502 }
    );
  }
}
