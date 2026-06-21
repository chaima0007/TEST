import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // GDE-001 — critical, mass_extinction_cascade (extinction_drive>0.85, ecological_cascade>0.80)
  {
    id: "GDE-001", organism_type: "moustique_anopheles", region: "AFRIQUE_SUB_SAHARIENNE",
    extinction_drive_capability: 0.92, ecological_cascade_risk: 0.88,
    containment_failure_probability: 0.78, weaponization_risk: 0.72,
    regulatory_governance_gap: 0.80, accidental_release_risk: 0.75,
    gene_drive_proliferation: 0.85, species_targeting_precision: 0.68,
    cross_species_transfer: 0.72, irreversibility_level: 0.88,
    agricultural_disruption: 0.70, biodiversity_collapse_risk: 0.85,
    biosecurity_gap: 0.78, dual_use_intensity: 0.72,
    international_monitoring_failure: 0.78, natural_ecosystem_invasion: 0.82,
    democratic_consent_failure: 0.80,
  },
  // GDE-002 — low, none
  {
    id: "GDE-002", organism_type: "levure_laboratoire", region: "EMEA",
    extinction_drive_capability: 0.10, ecological_cascade_risk: 0.08,
    containment_failure_probability: 0.12, weaponization_risk: 0.10,
    regulatory_governance_gap: 0.08, accidental_release_risk: 0.10,
    gene_drive_proliferation: 0.12, species_targeting_precision: 0.15,
    cross_species_transfer: 0.08, irreversibility_level: 0.12,
    agricultural_disruption: 0.10, biodiversity_collapse_risk: 0.08,
    biosecurity_gap: 0.12, dual_use_intensity: 0.10,
    international_monitoring_failure: 0.08, natural_ecosystem_invasion: 0.10,
    democratic_consent_failure: 0.12,
  },
  // GDE-003 — critical, containment_breach_catastrophe (containment_failure>0.85, accidental_release>0.80)
  {
    id: "GDE-003", organism_type: "rongeur_sauvage", region: "APAC",
    extinction_drive_capability: 0.72, ecological_cascade_risk: 0.75,
    containment_failure_probability: 0.90, weaponization_risk: 0.68,
    regulatory_governance_gap: 0.78, accidental_release_risk: 0.88,
    gene_drive_proliferation: 0.80, species_targeting_precision: 0.60,
    cross_species_transfer: 0.82, irreversibility_level: 0.78,
    agricultural_disruption: 0.72, biodiversity_collapse_risk: 0.75,
    biosecurity_gap: 0.70, dual_use_intensity: 0.65,
    international_monitoring_failure: 0.72, natural_ecosystem_invasion: 0.78,
    democratic_consent_failure: 0.75,
  },
  // GDE-004 — moderate, none
  {
    id: "GDE-004", organism_type: "plante_cultivée", region: "NOAM",
    extinction_drive_capability: 0.28, ecological_cascade_risk: 0.30,
    containment_failure_probability: 0.32, weaponization_risk: 0.25,
    regulatory_governance_gap: 0.30, accidental_release_risk: 0.28,
    gene_drive_proliferation: 0.32, species_targeting_precision: 0.35,
    cross_species_transfer: 0.28, irreversibility_level: 0.30,
    agricultural_disruption: 0.32, biodiversity_collapse_risk: 0.28,
    biosecurity_gap: 0.30, dual_use_intensity: 0.25,
    international_monitoring_failure: 0.30, natural_ecosystem_invasion: 0.28,
    democratic_consent_failure: 0.32,
  },
  // GDE-005 — critical, gene_drive_bioweapon (weaponization>0.85, dual_use>0.80)
  {
    id: "GDE-005", organism_type: "insecte_ravageur", region: "MEA",
    extinction_drive_capability: 0.78, ecological_cascade_risk: 0.72,
    containment_failure_probability: 0.75, weaponization_risk: 0.92,
    regulatory_governance_gap: 0.80, accidental_release_risk: 0.72,
    gene_drive_proliferation: 0.85, species_targeting_precision: 0.70,
    cross_species_transfer: 0.75, irreversibility_level: 0.80,
    agricultural_disruption: 0.78, biodiversity_collapse_risk: 0.72,
    biosecurity_gap: 0.82, dual_use_intensity: 0.88,
    international_monitoring_failure: 0.78, natural_ecosystem_invasion: 0.72,
    democratic_consent_failure: 0.80,
  },
  // GDE-006 — high, governance_monitoring_void (regulatory_gap>0.80, int_monitoring>0.75)
  {
    id: "GDE-006", organism_type: "poisson_eau_douce", region: "LATAM",
    extinction_drive_capability: 0.52, ecological_cascade_risk: 0.55,
    containment_failure_probability: 0.50, weaponization_risk: 0.48,
    regulatory_governance_gap: 0.85, accidental_release_risk: 0.52,
    gene_drive_proliferation: 0.55, species_targeting_precision: 0.50,
    cross_species_transfer: 0.48, irreversibility_level: 0.60,
    agricultural_disruption: 0.52, biodiversity_collapse_risk: 0.55,
    biosecurity_gap: 0.50, dual_use_intensity: 0.48,
    international_monitoring_failure: 0.82, natural_ecosystem_invasion: 0.58,
    democratic_consent_failure: 0.55,
  },
  // GDE-007 — high, irreversible_ecosystem_invasion (irreversibility>0.80, natural_invasion>0.75)
  {
    id: "GDE-007", organism_type: "algue_marine", region: "APAC",
    extinction_drive_capability: 0.55, ecological_cascade_risk: 0.58,
    containment_failure_probability: 0.52, weaponization_risk: 0.45,
    regulatory_governance_gap: 0.60, accidental_release_risk: 0.55,
    gene_drive_proliferation: 0.58, species_targeting_precision: 0.45,
    cross_species_transfer: 0.60, irreversibility_level: 0.88,
    agricultural_disruption: 0.55, biodiversity_collapse_risk: 0.60,
    biosecurity_gap: 0.50, dual_use_intensity: 0.48,
    international_monitoring_failure: 0.58, natural_ecosystem_invasion: 0.82,
    democratic_consent_failure: 0.55,
  },
  // GDE-008 — critical, mass_extinction_cascade — second critical covering all risk levels
  {
    id: "GDE-008", organism_type: "mammifère_invasif", region: "EMEA",
    extinction_drive_capability: 0.88, ecological_cascade_risk: 0.85,
    containment_failure_probability: 0.82, weaponization_risk: 0.75,
    regulatory_governance_gap: 0.85, accidental_release_risk: 0.78,
    gene_drive_proliferation: 0.88, species_targeting_precision: 0.72,
    cross_species_transfer: 0.80, irreversibility_level: 0.90,
    agricultural_disruption: 0.80, biodiversity_collapse_risk: 0.88,
    biosecurity_gap: 0.82, dual_use_intensity: 0.78,
    international_monitoring_failure: 0.85, natural_ecosystem_invasion: 0.88,
    democratic_consent_failure: 0.82,
  },
];

type GDEInput = typeof MOCK_ENTITIES[0];

function extinctionScore(e: GDEInput): number {
  return Math.round((e.extinction_drive_capability * 0.40 + e.ecological_cascade_risk * 0.35 + e.biodiversity_collapse_risk * 0.25) * 100 * 100) / 100;
}
function containmentScore(e: GDEInput): number {
  return Math.round((e.containment_failure_probability * 0.40 + e.accidental_release_risk * 0.35 + e.cross_species_transfer * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: GDEInput): number {
  return Math.round((e.regulatory_governance_gap * 0.40 + e.international_monitoring_failure * 0.35 + e.democratic_consent_failure * 0.25) * 100 * 100) / 100;
}
function weaponizationScore(e: GDEInput): number {
  return Math.round((e.weaponization_risk * 0.40 + e.dual_use_intensity * 0.35 + e.biosecurity_gap * 0.25) * 100 * 100) / 100;
}
function compositeScore(ext: number, cont: number, gov: number, weap: number): number {
  return Math.round((ext * 0.30 + cont * 0.25 + gov * 0.25 + weap * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function geneDrivePattern(e: GDEInput): string {
  if (e.extinction_drive_capability > 0.85 && e.ecological_cascade_risk > 0.80) return "mass_extinction_cascade";
  if (e.containment_failure_probability > 0.85 && e.accidental_release_risk > 0.80) return "containment_breach_catastrophe";
  if (e.weaponization_risk > 0.85 && e.dual_use_intensity > 0.80) return "gene_drive_bioweapon";
  if (e.regulatory_governance_gap > 0.80 && e.international_monitoring_failure > 0.75) return "governance_monitoring_void";
  if (e.irreversibility_level > 0.80 && e.natural_ecosystem_invasion > 0.75) return "irreversible_ecosystem_invasion";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "extinction_écosystémique_catastrophique";
  if (composite >= 40) return "crise_gene_drive_majeure";
  if (composite >= 20) return "risque_gene_drive_structurel";
  return "gene_drive_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_extinction_urgence_mondiale";
  if (risk === "high") return "confinement_gene_drive_urgence";
  if (risk === "moderate") return "renforcement_gouvernance_gene_drive";
  return "veille_gene_drive_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Extinction systémique — technologie gene drive hors contrôle";
  if (risk === "high") return "🟠 Crise gene drive majeure — risque écosystémique élevé";
  if (risk === "moderate") return "🟡 Risque gene drive structurel — surveillance renforcée requise";
  return "🟢 Gene drive sous surveillance — confinement et gouvernance opérationnels";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const ext  = extinctionScore(e);
      const cont = containmentScore(e);
      const gov  = governanceScore(e);
      const weap = weaponizationScore(e);
      const comp = compositeScore(ext, cont, gov, weap);
      const risk = riskLevel(comp);
      const pat  = geneDrivePattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:                    e.entity_id,
        organism_type:                e.organism_type,
        region:                       e.region,
        extinction_score:             ext,
        containment_score:            cont,
        governance_score:             gov,
        weaponization_score:          weap,
        composite_score:              comp,
        risk_level:                   risk,
        gene_drive_pattern:           pat,
        severity:                     sev,
        recommended_action:           action,
        signal:                       sig,
        extinction_drive_capability:  e.extinction_drive_capability,
        ecological_cascade_risk:      e.ecological_cascade_risk,
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
      pattern_distribution[ent.gene_drive_pattern] = (pattern_distribution[ent.gene_drive_pattern] || 0) + 1;
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
      module_id:                              377,
      module_name:                            "Gene Drive & Extinction Technology Intelligence Engine",
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
      avg_estimated_gene_drive_risk_index:    Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "gene-drive-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/gene-drive-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "gene-drive-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "gene-drive-engine"),
      { status: 502 }
    );
  }
}
