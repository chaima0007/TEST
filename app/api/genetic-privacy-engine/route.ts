import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// 8 mock entities: ≥3 critical, ≥2 high, ≥1 moderate, ≥2 low; all 5 patterns covered
const MOCK_ENTITIES = [
  // GP-001 séquençage_génome NAMER — critical law_enforcement_dna_dragnet
  { entity_id: "GP-001", data_type: "séquençage_génome_complet", region: "NAMER", informed_consent_quality: 0.20, data_re_identification_risk: 0.90, third_party_sharing_opacity: 0.88, law_enforcement_access: 0.92, insurance_discrimination_risk: 0.75, employment_discrimination_risk: 0.70, family_cascade_exposure: 0.72, cross_border_data_flow: 0.80, security_breach_vulnerability: 0.85, biobank_commercial_exploitation: 0.65, indigenous_genetic_sovereignty: 0.55, minors_data_collection: 0.60, genetic_genealogy_use: 0.88, research_benefit_sharing: 0.20, regulatory_framework_strength: 0.22, opt_out_effectiveness: 0.18, right_to_deletion: 0.15 },
  // GP-002 données_adn_ancestral APAC — critical insurance_genetic_discrimination
  { entity_id: "GP-002", data_type: "données_adn_ancestral", region: "APAC", informed_consent_quality: 0.18, data_re_identification_risk: 0.85, third_party_sharing_opacity: 0.80, law_enforcement_access: 0.65, insurance_discrimination_risk: 0.92, employment_discrimination_risk: 0.88, family_cascade_exposure: 0.75, cross_border_data_flow: 0.72, security_breach_vulnerability: 0.80, biobank_commercial_exploitation: 0.70, indigenous_genetic_sovereignty: 0.60, minors_data_collection: 0.55, genetic_genealogy_use: 0.68, research_benefit_sharing: 0.15, regulatory_framework_strength: 0.18, opt_out_effectiveness: 0.20, right_to_deletion: 0.12 },
  // GP-003 biobanque_commerciale EMEA — critical corporate_biobank_exploitation
  { entity_id: "GP-003", data_type: "biobanque_commerciale", region: "EMEA", informed_consent_quality: 0.22, data_re_identification_risk: 0.82, third_party_sharing_opacity: 0.88, law_enforcement_access: 0.58, insurance_discrimination_risk: 0.70, employment_discrimination_risk: 0.65, family_cascade_exposure: 0.68, cross_border_data_flow: 0.78, security_breach_vulnerability: 0.85, biobank_commercial_exploitation: 0.90, indigenous_genetic_sovereignty: 0.55, minors_data_collection: 0.60, genetic_genealogy_use: 0.62, research_benefit_sharing: 0.12, regulatory_framework_strength: 0.20, opt_out_effectiveness: 0.15, right_to_deletion: 0.18 },
  // GP-004 données_pédiatriques LATAM — high family_member_privacy_violation
  { entity_id: "GP-004", data_type: "données_pédiatriques_génétiques", region: "LATAM", informed_consent_quality: 0.35, data_re_identification_risk: 0.65, third_party_sharing_opacity: 0.58, law_enforcement_access: 0.45, insurance_discrimination_risk: 0.55, employment_discrimination_risk: 0.48, family_cascade_exposure: 0.88, cross_border_data_flow: 0.62, security_breach_vulnerability: 0.60, biobank_commercial_exploitation: 0.55, indigenous_genetic_sovereignty: 0.50, minors_data_collection: 0.85, genetic_genealogy_use: 0.62, research_benefit_sharing: 0.30, regulatory_framework_strength: 0.38, opt_out_effectiveness: 0.32, right_to_deletion: 0.35 },
  // GP-005 extraction_coloniale MEA — high genetic_colonialism_extraction
  { entity_id: "GP-005", data_type: "extraction_génétique_populations", region: "MEA", informed_consent_quality: 0.52, data_re_identification_risk: 0.38, third_party_sharing_opacity: 0.38, law_enforcement_access: 0.28, insurance_discrimination_risk: 0.35, employment_discrimination_risk: 0.30, family_cascade_exposure: 0.38, cross_border_data_flow: 0.80, security_breach_vulnerability: 0.40, biobank_commercial_exploitation: 0.42, indigenous_genetic_sovereignty: 0.82, minors_data_collection: 0.35, genetic_genealogy_use: 0.42, research_benefit_sharing: 0.35, regulatory_framework_strength: 0.45, opt_out_effectiveness: 0.42, right_to_deletion: 0.40 },
  // GP-006 tests_prédictifs EMEA — moderate none
  { entity_id: "GP-006", data_type: "tests_génétiques_prédictifs", region: "EMEA", informed_consent_quality: 0.70, data_re_identification_risk: 0.28, third_party_sharing_opacity: 0.25, law_enforcement_access: 0.18, insurance_discrimination_risk: 0.25, employment_discrimination_risk: 0.22, family_cascade_exposure: 0.30, cross_border_data_flow: 0.25, security_breach_vulnerability: 0.28, biobank_commercial_exploitation: 0.25, indigenous_genetic_sovereignty: 0.22, minors_data_collection: 0.18, genetic_genealogy_use: 0.25, research_benefit_sharing: 0.65, regulatory_framework_strength: 0.68, opt_out_effectiveness: 0.65, right_to_deletion: 0.65 },
  // GP-007 recherche_académique NAMER — low none
  { entity_id: "GP-007", data_type: "recherche_académique_anonymisée", region: "NAMER", informed_consent_quality: 0.88, data_re_identification_risk: 0.12, third_party_sharing_opacity: 0.10, law_enforcement_access: 0.08, insurance_discrimination_risk: 0.10, employment_discrimination_risk: 0.08, family_cascade_exposure: 0.12, cross_border_data_flow: 0.15, security_breach_vulnerability: 0.12, biobank_commercial_exploitation: 0.10, indigenous_genetic_sovereignty: 0.12, minors_data_collection: 0.08, genetic_genealogy_use: 0.10, research_benefit_sharing: 0.90, regulatory_framework_strength: 0.88, opt_out_effectiveness: 0.90, right_to_deletion: 0.88 },
  // GP-008 données_cliniques APAC — low none
  { entity_id: "GP-008", data_type: "données_cliniques_génétiques", region: "APAC", informed_consent_quality: 0.82, data_re_identification_risk: 0.15, third_party_sharing_opacity: 0.12, law_enforcement_access: 0.10, insurance_discrimination_risk: 0.12, employment_discrimination_risk: 0.10, family_cascade_exposure: 0.15, cross_border_data_flow: 0.18, security_breach_vulnerability: 0.15, biobank_commercial_exploitation: 0.12, indigenous_genetic_sovereignty: 0.15, minors_data_collection: 0.10, genetic_genealogy_use: 0.12, research_benefit_sharing: 0.85, regulatory_framework_strength: 0.82, opt_out_effectiveness: 0.85, right_to_deletion: 0.82 },
];

type Entity = typeof MOCK_ENTITIES[0];

function consentScore(e: Entity): number {
  return Math.min(Math.round(((1 - e.informed_consent_quality) * 0.4 + e.third_party_sharing_opacity * 0.35 + (1 - e.opt_out_effectiveness) * 0.25) * 100 * 100) / 100, 100);
}

function dataSecurityScore(e: Entity): number {
  return Math.min(Math.round((e.data_re_identification_risk * 0.4 + e.security_breach_vulnerability * 0.35 + e.cross_border_data_flow * 0.25) * 100 * 100) / 100, 100);
}

function discriminationScore(e: Entity): number {
  return Math.min(Math.round((e.insurance_discrimination_risk * 0.4 + e.employment_discrimination_risk * 0.35 + e.law_enforcement_access * 0.25) * 100 * 100) / 100, 100);
}

function sovereigntyScore(e: Entity): number {
  return Math.min(Math.round((e.indigenous_genetic_sovereignty * 0.4 + e.biobank_commercial_exploitation * 0.35 + (1 - e.research_benefit_sharing) * 0.25) * 100 * 100) / 100, 100);
}

function compositeScore(cs: number, ds: number, dis: number, ss: number): number {
  return Math.min(Math.round((cs * 0.30 + ds * 0.25 + dis * 0.25 + ss * 0.20) * 100) / 100, 100);
}

function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}

function geneticPattern(e: Entity): string {
  if (e.law_enforcement_access > 0.85 && e.genetic_genealogy_use > 0.80) return "law_enforcement_dna_dragnet";
  if (e.insurance_discrimination_risk > 0.85 && e.employment_discrimination_risk > 0.80) return "insurance_genetic_discrimination";
  if (e.biobank_commercial_exploitation > 0.80 && e.third_party_sharing_opacity > 0.75) return "corporate_biobank_exploitation";
  if (e.family_cascade_exposure > 0.80 && e.minors_data_collection > 0.75) return "family_member_privacy_violation";
  if (e.indigenous_genetic_sovereignty > 0.80 && e.cross_border_data_flow > 0.75) return "genetic_colonialism_extraction";
  return "none";
}

function severity(composite: number): string {
  if (composite >= 60) return "crise_confidentialité_génétique_systémique";
  if (composite >= 40) return "violation_droits_génétiques_majeure";
  if (composite >= 20) return "risque_discrimination_génétique_structurel";
  return "confidentialité_génétique_sous_surveillance";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_protection_données_génétiques";
  if (risk === "high") return "audit_immédiat_banques_adn_et_consentement";
  if (risk === "moderate") return "renforcement_cadre_réglementaire_génétique";
  return "veille_confidentialité_génétique_continue";
}

function geneticSignal(risk: string, composite: number, pattern: string): string {
  if (composite < 20) return "Confidentialité génétique préservée — consentement éclairé fort, sécurité des données robuste, droits souverains respectés";
  const labels: Record<string, string> = {
    law_enforcement_dna_dragnet:      "Filet ADN forces de l'ordre",
    insurance_genetic_discrimination: "Discrimination génétique assurance",
    corporate_biobank_exploitation:   "Exploitation biobanque commerciale",
    family_member_privacy_violation:  "Violation vie privée familiale",
    genetic_colonialism_extraction:   "Extraction coloniale génétique",
  };
  const label = labels[pattern] ?? pattern.replace(/_/g, " ");
  return `${label} — composite ${Math.round(composite)} — risque ${risk}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map((e) => {
      const cs = consentScore(e);
      const ds = dataSecurityScore(e);
      const dis = discriminationScore(e);
      const ss = sovereigntyScore(e);
      const comp = compositeScore(cs, ds, dis, ss);
      const risk = riskLevel(comp);
      const pattern = geneticPattern(e);
      const sev = severity(comp);
      const action = recommendedAction(risk);
      const sig = geneticSignal(risk, comp, pattern);
      return {
        entity_id: e.entity_id,
        data_type: e.data_type,
        region: e.region,
        consent_score: cs,
        data_security_score: ds,
        discrimination_score: dis,
        sovereignty_score: ss,
        composite_score: comp,
        risk_level: risk,
        genetic_pattern: pattern,
        severity: sev,
        recommended_action: action,
        signal: sig,
        informed_consent_quality: e.informed_consent_quality,
        indigenous_genetic_sovereignty: e.indigenous_genetic_sovereignty,
      };
    });

    const riskDist: Record<string, number> = {};
    const patternDist: Record<string, number> = {};
    const severityDist: Record<string, number> = {};
    const actionDist: Record<string, number> = {};
    let totalComposite = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      riskDist[ent.risk_level]          = (riskDist[ent.risk_level]          || 0) + 1;
      patternDist[ent.genetic_pattern]  = (patternDist[ent.genetic_pattern]  || 0) + 1;
      severityDist[ent.severity]        = (severityDist[ent.severity]        || 0) + 1;
      actionDist[ent.recommended_action]= (actionDist[ent.recommended_action]|| 0) + 1;
      totalComposite += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round((totalComposite / n) * 10) / 10;

    const summary = {
      module_id: 431,
      module_name: "Confidentialité Génétique & Banques de Données ADN Intelligence Engine",
      total: n,
      critical: criticalCount,
      high: highCount,
      moderate: moderateCount,
      low: lowCount,
      avg_composite: avgComposite,
      pattern_distribution: patternDist,
      risk_distribution: riskDist,
      severity_distribution: severityDist,
      action_distribution: actionDist,
      avg_estimated_genetic_privacy_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>));
  }

  const upstream = await fetch(`${process.env.SWARM_API_URL}/api/genetic-privacy-engine`);
  if (!upstream.ok) {
    return NextResponse.json({ error: "Upstream error" }, { status: 502 });
  }
  return NextResponse.json(await upstream.json());
}
