import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // RDE-001 — critical, orphan_drug_pricing_crisis (orphan_drug_price_index>0.85, insurance_coverage_gap>0.80)
  {
    entity_id: "RDE-001", disease_category: "maladies_métaboliques_rares", region: "NOAM",
    diagnostic_delay_years: 0.70, misdiagnosis_rate: 0.68,
    treatment_availability_gap: 0.88, orphan_drug_price_index: 0.92,
    research_investment_gap: 0.72, clinical_trial_access: 0.78,
    regulatory_approval_delay: 0.70, patient_registry_gap: 0.68,
    off_label_use_risk: 0.65, compassionate_use_barrier: 0.72,
    insurance_coverage_gap: 0.85, biobank_access_restriction: 0.68,
    patient_group_funding_capture: 0.60, cross_border_access_barrier: 0.65,
    genetic_test_availability: 0.70, newborn_screening_gap: 0.62,
    specialist_density_gap: 0.80,
  },
  // RDE-002 — critical, diagnostic_odyssey_barrier (diagnostic_delay_years>0.85, misdiagnosis_rate>0.80)
  {
    entity_id: "RDE-002", disease_category: "maladies_neurologiques_rares", region: "EMEA",
    diagnostic_delay_years: 0.90, misdiagnosis_rate: 0.86,
    treatment_availability_gap: 0.72, orphan_drug_price_index: 0.68,
    research_investment_gap: 0.75, clinical_trial_access: 0.70,
    regulatory_approval_delay: 0.68, patient_registry_gap: 0.72,
    off_label_use_risk: 0.70, compassionate_use_barrier: 0.65,
    insurance_coverage_gap: 0.68, biobank_access_restriction: 0.70,
    patient_group_funding_capture: 0.62, cross_border_access_barrier: 0.65,
    genetic_test_availability: 0.68, newborn_screening_gap: 0.70,
    specialist_density_gap: 0.82,
  },
  // RDE-003 — critical, research_funding_desert (research_investment_gap>0.85, patient_registry_gap>0.80)
  {
    entity_id: "RDE-003", disease_category: "maladies_génétiques_ultra_rares", region: "SSA",
    diagnostic_delay_years: 0.68, misdiagnosis_rate: 0.65,
    treatment_availability_gap: 0.80, orphan_drug_price_index: 0.72,
    research_investment_gap: 0.90, clinical_trial_access: 0.75,
    regulatory_approval_delay: 0.72, patient_registry_gap: 0.85,
    off_label_use_risk: 0.68, compassionate_use_barrier: 0.70,
    insurance_coverage_gap: 0.72, biobank_access_restriction: 0.78,
    patient_group_funding_capture: 0.65, cross_border_access_barrier: 0.68,
    genetic_test_availability: 0.82, newborn_screening_gap: 0.75,
    specialist_density_gap: 0.78,
  },
  // RDE-004 — high, regulatory_pathway_blockade (regulatory_approval_delay>0.80, cross_border_access_barrier>0.75)
  {
    entity_id: "RDE-004", disease_category: "maladies_auto_immunes_rares", region: "APAC",
    diagnostic_delay_years: 0.48, misdiagnosis_rate: 0.45,
    treatment_availability_gap: 0.50, orphan_drug_price_index: 0.52,
    research_investment_gap: 0.48, clinical_trial_access: 0.50,
    regulatory_approval_delay: 0.85, patient_registry_gap: 0.48,
    off_label_use_risk: 0.52, compassionate_use_barrier: 0.50,
    insurance_coverage_gap: 0.48, biobank_access_restriction: 0.50,
    patient_group_funding_capture: 0.45, cross_border_access_barrier: 0.80,
    genetic_test_availability: 0.48, newborn_screening_gap: 0.45,
    specialist_density_gap: 0.50,
  },
  // RDE-005 — high, patient_advocacy_capture (patient_group_funding_capture>0.80, newborn_screening_gap>0.75)
  {
    entity_id: "RDE-005", disease_category: "maladies_lysosomales", region: "LATAM",
    diagnostic_delay_years: 0.45, misdiagnosis_rate: 0.48,
    treatment_availability_gap: 0.52, orphan_drug_price_index: 0.48,
    research_investment_gap: 0.50, clinical_trial_access: 0.45,
    regulatory_approval_delay: 0.48, patient_registry_gap: 0.50,
    off_label_use_risk: 0.48, compassionate_use_barrier: 0.52,
    insurance_coverage_gap: 0.48, biobank_access_restriction: 0.45,
    patient_group_funding_capture: 0.85, cross_border_access_barrier: 0.48,
    genetic_test_availability: 0.50, newborn_screening_gap: 0.80,
    specialist_density_gap: 0.48,
  },
  // RDE-006 — moderate, none
  {
    entity_id: "RDE-006", disease_category: "maladies_hématologiques_rares", region: "EMEA",
    diagnostic_delay_years: 0.28, misdiagnosis_rate: 0.30,
    treatment_availability_gap: 0.32, orphan_drug_price_index: 0.28,
    research_investment_gap: 0.30, clinical_trial_access: 0.28,
    regulatory_approval_delay: 0.30, patient_registry_gap: 0.28,
    off_label_use_risk: 0.32, compassionate_use_barrier: 0.28,
    insurance_coverage_gap: 0.30, biobank_access_restriction: 0.28,
    patient_group_funding_capture: 0.25, cross_border_access_barrier: 0.30,
    genetic_test_availability: 0.28, newborn_screening_gap: 0.25,
    specialist_density_gap: 0.30,
  },
  // RDE-007 — low, none
  {
    entity_id: "RDE-007", disease_category: "maladies_mitochondriales", region: "NOAM",
    diagnostic_delay_years: 0.10, misdiagnosis_rate: 0.12,
    treatment_availability_gap: 0.10, orphan_drug_price_index: 0.12,
    research_investment_gap: 0.10, clinical_trial_access: 0.12,
    regulatory_approval_delay: 0.10, patient_registry_gap: 0.08,
    off_label_use_risk: 0.12, compassionate_use_barrier: 0.10,
    insurance_coverage_gap: 0.12, biobank_access_restriction: 0.10,
    patient_group_funding_capture: 0.08, cross_border_access_barrier: 0.10,
    genetic_test_availability: 0.12, newborn_screening_gap: 0.08,
    specialist_density_gap: 0.10,
  },
  // RDE-008 — low, none
  {
    entity_id: "RDE-008", disease_category: "maladies_dermatologiques_rares", region: "APAC",
    diagnostic_delay_years: 0.12, misdiagnosis_rate: 0.10,
    treatment_availability_gap: 0.12, orphan_drug_price_index: 0.10,
    research_investment_gap: 0.12, clinical_trial_access: 0.10,
    regulatory_approval_delay: 0.12, patient_registry_gap: 0.10,
    off_label_use_risk: 0.10, compassionate_use_barrier: 0.12,
    insurance_coverage_gap: 0.10, biobank_access_restriction: 0.12,
    patient_group_funding_capture: 0.10, cross_border_access_barrier: 0.12,
    genetic_test_availability: 0.10, newborn_screening_gap: 0.10,
    specialist_density_gap: 0.12,
  },
];

type RDEInput = typeof MOCK_ENTITIES[0];

function accessScore(e: RDEInput): number {
  return Math.round((e.treatment_availability_gap * 0.4 + e.specialist_density_gap * 0.35 + e.clinical_trial_access * 0.25) * 100 * 100) / 100;
}
function researchScore(e: RDEInput): number {
  return Math.round((e.research_investment_gap * 0.4 + e.biobank_access_restriction * 0.35 + e.patient_registry_gap * 0.25) * 100 * 100) / 100;
}
function affordabilityScore(e: RDEInput): number {
  return Math.round((e.orphan_drug_price_index * 0.4 + e.insurance_coverage_gap * 0.35 + e.compassionate_use_barrier * 0.25) * 100 * 100) / 100;
}
function regulatoryScore(e: RDEInput): number {
  return Math.round((e.regulatory_approval_delay * 0.4 + e.cross_border_access_barrier * 0.35 + e.off_label_use_risk * 0.25) * 100 * 100) / 100;
}
function compositeScore(acc: number, res: number, aff: number, reg: number): number {
  return Math.round((acc * 0.30 + res * 0.25 + aff * 0.25 + reg * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function rareDiseasePattern(e: RDEInput): string {
  if (e.orphan_drug_price_index > 0.85 && e.insurance_coverage_gap > 0.80) return "orphan_drug_pricing_crisis";
  if (e.diagnostic_delay_years > 0.85 && e.misdiagnosis_rate > 0.80) return "diagnostic_odyssey_barrier";
  if (e.research_investment_gap > 0.85 && e.patient_registry_gap > 0.80) return "research_funding_desert";
  if (e.regulatory_approval_delay > 0.80 && e.cross_border_access_barrier > 0.75) return "regulatory_pathway_blockade";
  if (e.patient_group_funding_capture > 0.80 && e.newborn_screening_gap > 0.75) return "patient_advocacy_capture";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_accès_médicaments_orphelins_systémique";
  if (composite >= 40) return "crise_recherche_maladies_rares_majeure";
  if (composite >= 20) return "inégalité_accès_thérapeutique_structurelle";
  return "surveillance_maladies_rares_active";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_accès_médicaments_orphelins";
  if (risk === "high") return "renforcement_parcours_diagnostic_et_recherche";
  if (risk === "moderate") return "amélioration_politiques_accès_thérapeutique";
  return "veille_maladies_rares_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise accès médicaments orphelins systémique — patients en danger";
  if (risk === "high") return "🟠 Crise recherche maladies rares majeure détectée";
  if (risk === "moderate") return "🟡 Inégalité accès thérapeutique structurelle active";
  return "🟢 Surveillance maladies rares active";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const acc  = accessScore(e);
      const res  = researchScore(e);
      const aff  = affordabilityScore(e);
      const reg  = regulatoryScore(e);
      const comp = compositeScore(acc, res, aff, reg);
      const risk = riskLevel(comp);
      const pat  = rareDiseasePattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        entity_id:                  e.entity_id,
        disease_category:           e.disease_category,
        region:                     e.region,
        access_score:               acc,
        research_score:             res,
        affordability_score:        aff,
        regulatory_score:           reg,
        composite_score:            comp,
        risk_level:                 risk,
        rare_disease_pattern:       pat,
        severity:                   sev,
        recommended_action:         action,
        signal:                     sig,
        orphan_drug_price_index:    e.orphan_drug_price_index,
        diagnostic_delay_years:     e.diagnostic_delay_years,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tAcc = 0, tRes = 0, tAff = 0, tReg = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.rare_disease_pattern] = (pattern_distribution[ent.rare_disease_pattern] || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tAcc  += ent.access_score;
      tRes  += ent.research_score;
      tAff  += ent.affordability_score;
      tReg  += ent.regulatory_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;
    const avgAccess    = Math.round(tAcc  / n * 10) / 10;

    const summary = {
      module_id:                                  435,
      module_name:                                "Maladies Rares & Médicaments Orphelins Intelligence Engine",
      total:                                      n,
      critical:                                   criticalCount,
      high:                                       highCount,
      moderate:                                   moderateCount,
      low:                                        lowCount,
      avg_composite:                              avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_rare_disease_access_index:    Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, avg_access: avgAccess }, "rare-disease-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/rare-disease-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "rare-disease-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "rare-disease-engine"),
      { status: 502 }
    );
  }
}
