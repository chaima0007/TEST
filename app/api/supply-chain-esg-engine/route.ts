import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[supply-chain-esg-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const MOCK_ENTITIES = [
  // SCE-001 — critical, forced_labor_opacity (forced_labor_risk>0.85, child_labor_exposure>0.80)
  {
    id: "SCE-001", industry_type: "textile", region: "APAC",
    supply_visibility: 0.85, forced_labor_risk: 0.90, child_labor_exposure: 0.85,
    carbon_footprint: 0.75, deforestation_link: 0.70, water_pollution: 0.70,
    conflict_mineral_use: 0.50, audit_independence: 0.75, reporting_quality: 0.70,
    certification_credibility: 0.70, subcontractor_risk: 0.80, living_wage_compliance: 0.80,
    gender_equality: 0.60, biodiversity_impact: 0.60, data_integrity: 0.80,
    regulatory_compliance: 0.65, third_party_verification: 0.65,
  },
  // SCE-002 — critical, greenwashing_deception (carbon_footprint>0.85, reporting_quality<0.20)
  {
    id: "SCE-002", industry_type: "energie_fossile", region: "NOAM",
    supply_visibility: 0.80, forced_labor_risk: 0.72, child_labor_exposure: 0.68,
    carbon_footprint: 0.90, deforestation_link: 0.72, water_pollution: 0.75,
    conflict_mineral_use: 0.50, audit_independence: 0.80, reporting_quality: 0.10,
    certification_credibility: 0.70, subcontractor_risk: 0.78, living_wage_compliance: 0.70,
    gender_equality: 0.55, biodiversity_impact: 0.65, data_integrity: 0.80,
    regulatory_compliance: 0.60, third_party_verification: 0.50,
  },
  // SCE-003 — critical, conflict_mineral_complicity (conflict_mineral_use>0.85, supply_visibility<0.20)
  {
    id: "SCE-003", industry_type: "electronique", region: "SSA",
    supply_visibility: 0.10, forced_labor_risk: 0.75, child_labor_exposure: 0.70,
    carbon_footprint: 0.78, deforestation_link: 0.72, water_pollution: 0.70,
    conflict_mineral_use: 0.90, audit_independence: 0.78, reporting_quality: 0.70,
    certification_credibility: 0.72, subcontractor_risk: 0.80, living_wage_compliance: 0.72,
    gender_equality: 0.55, biodiversity_impact: 0.60, data_integrity: 0.75,
    regulatory_compliance: 0.62, third_party_verification: 0.55,
  },
  // SCE-004 — high, carbon_laundering_scheme (carbon_footprint>0.80, deforestation_link>0.75)
  {
    id: "SCE-004", industry_type: "agroalimentaire", region: "LATAM",
    supply_visibility: 0.48, forced_labor_risk: 0.40, child_labor_exposure: 0.38,
    carbon_footprint: 0.82, deforestation_link: 0.78, water_pollution: 0.50,
    conflict_mineral_use: 0.30, audit_independence: 0.42, reporting_quality: 0.40,
    certification_credibility: 0.44, subcontractor_risk: 0.45, living_wage_compliance: 0.42,
    gender_equality: 0.40, biodiversity_impact: 0.50, data_integrity: 0.50,
    regulatory_compliance: 0.42, third_party_verification: 0.38,
  },
  // SCE-005 — high, supplier_audit_capture (audit_independence>0.80, certification_credibility>0.75)
  {
    id: "SCE-005", industry_type: "chimie_industrielle", region: "EMEA",
    supply_visibility: 0.50, forced_labor_risk: 0.42, child_labor_exposure: 0.40,
    carbon_footprint: 0.45, deforestation_link: 0.42, water_pollution: 0.40,
    conflict_mineral_use: 0.35, audit_independence: 0.85, reporting_quality: 0.70,
    certification_credibility: 0.80, subcontractor_risk: 0.48, living_wage_compliance: 0.45,
    gender_equality: 0.42, biodiversity_impact: 0.38, data_integrity: 0.52,
    regulatory_compliance: 0.48, third_party_verification: 0.40,
  },
  // SCE-006 — moderate, none
  {
    id: "SCE-006", industry_type: "logistique", region: "EMEA",
    supply_visibility: 0.32, forced_labor_risk: 0.28, child_labor_exposure: 0.25,
    carbon_footprint: 0.32, deforestation_link: 0.28, water_pollution: 0.30,
    conflict_mineral_use: 0.20, audit_independence: 0.30, reporting_quality: 0.28,
    certification_credibility: 0.32, subcontractor_risk: 0.28, living_wage_compliance: 0.30,
    gender_equality: 0.32, biodiversity_impact: 0.28, data_integrity: 0.30,
    regulatory_compliance: 0.30, third_party_verification: 0.28,
  },
  // SCE-007 — low, none
  {
    id: "SCE-007", industry_type: "pharmaceutique", region: "NOAM",
    supply_visibility: 0.12, forced_labor_risk: 0.10, child_labor_exposure: 0.08,
    carbon_footprint: 0.12, deforestation_link: 0.10, water_pollution: 0.10,
    conflict_mineral_use: 0.08, audit_independence: 0.10, reporting_quality: 0.12,
    certification_credibility: 0.10, subcontractor_risk: 0.10, living_wage_compliance: 0.12,
    gender_equality: 0.14, biodiversity_impact: 0.10, data_integrity: 0.12,
    regulatory_compliance: 0.14, third_party_verification: 0.12,
  },
  // SCE-008 — low, none
  {
    id: "SCE-008", industry_type: "technologie", region: "APAC",
    supply_visibility: 0.14, forced_labor_risk: 0.12, child_labor_exposure: 0.10,
    carbon_footprint: 0.10, deforestation_link: 0.12, water_pollution: 0.12,
    conflict_mineral_use: 0.10, audit_independence: 0.12, reporting_quality: 0.14,
    certification_credibility: 0.12, subcontractor_risk: 0.12, living_wage_compliance: 0.14,
    gender_equality: 0.16, biodiversity_impact: 0.12, data_integrity: 0.14,
    regulatory_compliance: 0.16, third_party_verification: 0.14,
  },
];

type SCEInput = typeof MOCK_ENTITIES[0];

function visibilityScore(e: SCEInput): number {
  return Math.round((e.supply_visibility * 0.40 + e.subcontractor_risk * 0.35 + e.data_integrity * 0.25) * 100 * 100) / 100;
}
function laborScore(e: SCEInput): number {
  return Math.round((e.forced_labor_risk * 0.40 + e.child_labor_exposure * 0.35 + e.living_wage_compliance * 0.25) * 100 * 100) / 100;
}
function environmentalScore(e: SCEInput): number {
  return Math.round((e.carbon_footprint * 0.40 + e.deforestation_link * 0.35 + e.water_pollution * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: SCEInput): number {
  return Math.round((e.audit_independence * 0.40 + e.reporting_quality * 0.35 + e.certification_credibility * 0.25) * 100 * 100) / 100;
}
function compositeScore(vis: number, lab: number, env: number, gov: number): number {
  return Math.round((vis * 0.30 + lab * 0.25 + env * 0.25 + gov * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function esgPattern(e: SCEInput): string {
  if (e.forced_labor_risk > 0.85 && e.child_labor_exposure > 0.80) return "forced_labor_opacity";
  if (e.carbon_footprint > 0.85 && e.reporting_quality < 0.20) return "greenwashing_deception";
  if (e.conflict_mineral_use > 0.85 && e.supply_visibility < 0.20) return "conflict_mineral_complicity";
  if (e.carbon_footprint > 0.80 && e.deforestation_link > 0.75) return "carbon_laundering_scheme";
  if (e.audit_independence > 0.80 && e.certification_credibility > 0.75) return "supplier_audit_capture";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_opacité_chaîne_approvisionnement_critique";
  if (composite >= 40) return "risque_esg_majeur_détecté";
  if (composite >= 20) return "non_conformité_esg_structurelle";
  return "transparence_esg_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "audit_urgence_chaîne_approvisionnement_intégrale";
  if (risk === "high") return "renforcement_contrôle_fournisseurs_tier2_tier3";
  if (risk === "moderate") return "mise_en_conformité_esg_progressive";
  return "veille_transparence_chaîne_approvisionnement";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise opacité chaîne d'approvisionnement — violation ESG systémique";
  if (risk === "high") return "🟠 Risque ESG majeur détecté dans la chaîne fournisseurs";
  if (risk === "moderate") return "🟡 Non-conformité ESG structurelle — surveillance renforcée requise";
  return "🟢 Transparence ESG sous surveillance continue";
}

const SWARM_API_URL = process.env.SWARM_API_URL;

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const vis  = visibilityScore(e);
      const lab  = laborScore(e);
      const env  = environmentalScore(e);
      const gov  = governanceScore(e);
      const comp = compositeScore(vis, lab, env, gov);
      const risk = riskLevel(comp);
      const pat  = esgPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:             e.entity_id,
        industry_type:         e.industry_type,
        region:                e.region,
        visibility_score:      vis,
        labor_score:           lab,
        environmental_score:   env,
        governance_score:      gov,
        composite_score:       comp,
        risk_level:            risk,
        esg_pattern:           pat,
        severity:              sev,
        recommended_action:    action,
        signal:                sig,
        supply_visibility:     e.supply_visibility,
        forced_labor_risk:     e.forced_labor_risk,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.esg_pattern]       = (pattern_distribution[ent.esg_pattern]       || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                              397,
      module_name:                            "Transparence Chaîne d'Approvisionnement ESG Intelligence Engine",
      total:                                  n,
      critical:                               criticalCount,
      high:                                   highCount,
      moderate:                               moderateCount,
      low:                                    lowCount,
      avg_composite:                          avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_esg_transparency_index:   Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary } as Record<string, unknown>)
    ));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/supply-chain-esg-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(sealResponse(await res.json())));
  } catch {}
  return sealResponse(NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 }));
}
