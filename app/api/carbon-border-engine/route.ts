import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // CBE-001 — critical, carbon_leakage_acceleration (carbon_leakage_risk>0.85, import_emission_intensity>0.80)
  {
    id: "CBE-001", sector_type: "acier", region: "EMEA",
    carbon_leakage_risk: 0.90, import_emission_intensity: 0.88,
    domestic_carbon_price: 0.70, border_price_equivalence: 0.72,
    compliance_verification_gap: 0.80, developing_country_impact: 0.60,
    wto_compatibility_risk: 0.65, industry_lobbying_capture: 0.80,
    measurement_accuracy: 0.78, data_availability: 0.75,
    third_country_retaliation: 0.60, green_industrial_policy_alignment: 0.70,
    renewable_transition_support: 0.55, supply_chain_decarbonization: 0.65,
    tariff_circumvention_risk: 0.75, political_stability: 0.50,
    administrative_capacity: 0.55,
  },
  // CBE-002 — critical, trade_war_escalation (third_country_retaliation>0.85, wto_compatibility_risk>0.80)
  {
    id: "CBE-002", sector_type: "ciment", region: "APAC",
    carbon_leakage_risk: 0.78, import_emission_intensity: 0.75,
    domestic_carbon_price: 0.65, border_price_equivalence: 0.68,
    compliance_verification_gap: 0.72, developing_country_impact: 0.70,
    wto_compatibility_risk: 0.85, industry_lobbying_capture: 0.78,
    measurement_accuracy: 0.70, data_availability: 0.68,
    third_country_retaliation: 0.90, green_industrial_policy_alignment: 0.72,
    renewable_transition_support: 0.60, supply_chain_decarbonization: 0.62,
    tariff_circumvention_risk: 0.70, political_stability: 0.45,
    administrative_capacity: 0.50,
  },
  // CBE-003 — critical, developing_country_exclusion (developing_country_impact>0.85, renewable_transition_support<0.20)
  {
    id: "CBE-003", sector_type: "aluminium", region: "SSA",
    carbon_leakage_risk: 0.80, import_emission_intensity: 0.78,
    domestic_carbon_price: 0.60, border_price_equivalence: 0.62,
    compliance_verification_gap: 0.75, developing_country_impact: 0.90,
    wto_compatibility_risk: 0.72, industry_lobbying_capture: 0.75,
    measurement_accuracy: 0.70, data_availability: 0.65,
    third_country_retaliation: 0.68, green_industrial_policy_alignment: 0.65,
    renewable_transition_support: 0.12, supply_chain_decarbonization: 0.60,
    tariff_circumvention_risk: 0.72, political_stability: 0.42,
    administrative_capacity: 0.48,
  },
  // CBE-004 — high, measurement_fraud_crisis (compliance_verification_gap>0.80, measurement_accuracy>0.75)
  {
    id: "CBE-004", sector_type: "engrais", region: "LATAM",
    carbon_leakage_risk: 0.48, import_emission_intensity: 0.45,
    domestic_carbon_price: 0.40, border_price_equivalence: 0.42,
    compliance_verification_gap: 0.85, developing_country_impact: 0.50,
    wto_compatibility_risk: 0.45, industry_lobbying_capture: 0.50,
    measurement_accuracy: 0.80, data_availability: 0.52,
    third_country_retaliation: 0.45, green_industrial_policy_alignment: 0.48,
    renewable_transition_support: 0.45, supply_chain_decarbonization: 0.48,
    tariff_circumvention_risk: 0.50, political_stability: 0.48,
    administrative_capacity: 0.50,
  },
  // CBE-005 — high, implementation_collapse (administrative_capacity>0.80, political_stability<0.20)
  {
    id: "CBE-005", sector_type: "électricité", region: "MENA",
    carbon_leakage_risk: 0.50, import_emission_intensity: 0.48,
    domestic_carbon_price: 0.42, border_price_equivalence: 0.44,
    compliance_verification_gap: 0.52, developing_country_impact: 0.55,
    wto_compatibility_risk: 0.50, industry_lobbying_capture: 0.55,
    measurement_accuracy: 0.50, data_availability: 0.48,
    third_country_retaliation: 0.52, green_industrial_policy_alignment: 0.50,
    renewable_transition_support: 0.48, supply_chain_decarbonization: 0.50,
    tariff_circumvention_risk: 0.48, political_stability: 0.15,
    administrative_capacity: 0.85,
  },
  // CBE-006 — moderate, none
  {
    id: "CBE-006", sector_type: "chimie", region: "NOAM",
    carbon_leakage_risk: 0.30, import_emission_intensity: 0.28,
    domestic_carbon_price: 0.25, border_price_equivalence: 0.28,
    compliance_verification_gap: 0.30, developing_country_impact: 0.28,
    wto_compatibility_risk: 0.28, industry_lobbying_capture: 0.30,
    measurement_accuracy: 0.28, data_availability: 0.30,
    third_country_retaliation: 0.28, green_industrial_policy_alignment: 0.30,
    renewable_transition_support: 0.28, supply_chain_decarbonization: 0.30,
    tariff_circumvention_risk: 0.28, political_stability: 0.70,
    administrative_capacity: 0.30,
  },
  // CBE-007 — low, none
  {
    id: "CBE-007", sector_type: "hydrogène", region: "EMEA",
    carbon_leakage_risk: 0.10, import_emission_intensity: 0.10,
    domestic_carbon_price: 0.08, border_price_equivalence: 0.10,
    compliance_verification_gap: 0.10, developing_country_impact: 0.10,
    wto_compatibility_risk: 0.10, industry_lobbying_capture: 0.10,
    measurement_accuracy: 0.10, data_availability: 0.12,
    third_country_retaliation: 0.10, green_industrial_policy_alignment: 0.12,
    renewable_transition_support: 0.90, supply_chain_decarbonization: 0.12,
    tariff_circumvention_risk: 0.10, political_stability: 0.90,
    administrative_capacity: 0.10,
  },
  // CBE-008 — low, none
  {
    id: "CBE-008", sector_type: "acier_recyclé", region: "APAC",
    carbon_leakage_risk: 0.12, import_emission_intensity: 0.12,
    domestic_carbon_price: 0.10, border_price_equivalence: 0.12,
    compliance_verification_gap: 0.12, developing_country_impact: 0.12,
    wto_compatibility_risk: 0.12, industry_lobbying_capture: 0.12,
    measurement_accuracy: 0.12, data_availability: 0.14,
    third_country_retaliation: 0.12, green_industrial_policy_alignment: 0.14,
    renewable_transition_support: 0.85, supply_chain_decarbonization: 0.14,
    tariff_circumvention_risk: 0.12, political_stability: 0.88,
    administrative_capacity: 0.12,
  },
];

type CBEInput = typeof MOCK_ENTITIES[0];

function leakageScore(e: CBEInput): number {
  return Math.round((e.carbon_leakage_risk * 0.40 + e.import_emission_intensity * 0.35 + e.tariff_circumvention_risk * 0.25) * 100 * 100) / 100;
}
function competitivenessScore(e: CBEInput): number {
  return Math.round((e.industry_lobbying_capture * 0.40 + e.green_industrial_policy_alignment * 0.35 + e.supply_chain_decarbonization * 0.25) * 100 * 100) / 100;
}
function complianceScore(e: CBEInput): number {
  return Math.round((e.compliance_verification_gap * 0.40 + e.measurement_accuracy * 0.35 + e.data_availability * 0.25) * 100 * 100) / 100;
}
function geopoliticalScore(e: CBEInput): number {
  return Math.round((e.third_country_retaliation * 0.40 + e.wto_compatibility_risk * 0.35 + e.developing_country_impact * 0.25) * 100 * 100) / 100;
}
function compositeScore(leak: number, comp: number, compl: number, geo: number): number {
  return Math.round((leak * 0.30 + comp * 0.25 + compl * 0.25 + geo * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function cbamPattern(e: CBEInput): string {
  if (e.carbon_leakage_risk > 0.85 && e.import_emission_intensity > 0.80) return "carbon_leakage_acceleration";
  if (e.third_country_retaliation > 0.85 && e.wto_compatibility_risk > 0.80) return "trade_war_escalation";
  if (e.developing_country_impact > 0.85 && e.renewable_transition_support < 0.20) return "developing_country_exclusion";
  if (e.compliance_verification_gap > 0.80 && e.measurement_accuracy > 0.75) return "measurement_fraud_crisis";
  if (e.administrative_capacity > 0.80 && e.political_stability < 0.20) return "implementation_collapse";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_mécanisme_carbone_frontière_systémique";
  if (composite >= 40) return "risque_fuite_carbone_majeur_détecté";
  if (composite >= 20) return "non_conformité_cbam_structurelle";
  return "ajustement_carbone_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_mécanisme_carbone_frontière_critique";
  if (risk === "high") return "renforcement_vérification_conformité_cbam_accélérée";
  if (risk === "moderate") return "mise_en_conformité_cbam_progressive";
  return "veille_ajustement_carbone_frontière_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise mécanisme ajustement carbone frontière — fuite carbone systémique";
  if (risk === "high") return "🟠 Risque fuite carbone majeur détecté — conformité CBAM compromise";
  if (risk === "moderate") return "🟡 Non-conformité CBAM structurelle — surveillance renforcée requise";
  return "🟢 Ajustement carbone frontière sous surveillance continue";
}

const SWARM_API_URL = process.env.SWARM_API_URL;

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const leak  = leakageScore(e);
      const comp  = competitivenessScore(e);
      const compl = complianceScore(e);
      const geo   = geopoliticalScore(e);
      const cmp   = compositeScore(leak, comp, compl, geo);
      const risk  = riskLevel(cmp);
      const pat   = cbamPattern(e);
      const sev   = severity(cmp);
      const action = recommendedAction(risk);
      const sig   = signal(risk);
      return {
        id:                      e.entity_id,
        sector_type:                    e.sector_type,
        region:                         e.region,
        leakage_score:                  leak,
        competitiveness_score:          comp,
        compliance_score:               compl,
        geopolitical_score:             geo,
        composite_score:                cmp,
        risk_level:                     risk,
        cbam_pattern:                   pat,
        severity:                       sev,
        recommended_action:             action,
        signal:                         sig,
        carbon_leakage_risk:            e.carbon_leakage_risk,
        compliance_verification_gap:    e.compliance_verification_gap,
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
      pattern_distribution[ent.cbam_pattern]      = (pattern_distribution[ent.cbam_pattern]      || 0) + 1;
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
      module_id:                               413,
      module_name:                             "Mécanisme Ajustement Carbone Frontière Intelligence Engine",
      total:                                   n,
      critical:                                criticalCount,
      high:                                    highCount,
      moderate:                                moderateCount,
      low:                                     lowCount,
      avg_composite:                           avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_cbam_effectiveness_index:  Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary } as Record<string, unknown>)
    );
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/carbon-border-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(sealResponse(await res.json()));
  } catch {}
  return NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 });
}
