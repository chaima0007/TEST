import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // DCE-001: critical, platform_imperial_capture (pdr>0.85 AND eve>0.80)
  { entity_id:"DCE-001", tech_domain:"platform_monopoly", region:"AFRIQUE",
    platform_dependency_ratio:0.92, data_extraction_intensity:0.78,
    algorithmic_bias_export:0.70, digital_infrastructure_control:0.75,
    content_moderation_dominance:0.80, payment_system_capture:0.72,
    cloud_sovereignty_erosion:0.75, AI_dependency_trap:0.78,
    surveillance_export_risk:0.65, economic_value_extraction:0.88,
    local_industry_displacement:0.82, regulatory_capture_risk:0.74,
    digital_divide_amplification:0.70, language_digital_exclusion:0.68,
    tech_debt_accumulation:0.72, data_localization_failure:0.70,
    geopolitical_tech_leverage:0.78 },

  // DCE-002: low, none
  { entity_id:"DCE-002", tech_domain:"souveraineté_numérique", region:"EUROPE",
    platform_dependency_ratio:0.12, data_extraction_intensity:0.10,
    algorithmic_bias_export:0.08, digital_infrastructure_control:0.15,
    content_moderation_dominance:0.12, payment_system_capture:0.10,
    cloud_sovereignty_erosion:0.12, AI_dependency_trap:0.10,
    surveillance_export_risk:0.08, economic_value_extraction:0.10,
    local_industry_displacement:0.12, regulatory_capture_risk:0.10,
    digital_divide_amplification:0.10, language_digital_exclusion:0.08,
    tech_debt_accumulation:0.10, data_localization_failure:0.12,
    geopolitical_tech_leverage:0.10 },

  // DCE-003: critical, data_extraction_empire (dei>0.85 AND dlf>0.80)
  { entity_id:"DCE-003", tech_domain:"extraction_données_massives", region:"ASIE_SUD",
    platform_dependency_ratio:0.72, data_extraction_intensity:0.90,
    algorithmic_bias_export:0.74, digital_infrastructure_control:0.70,
    content_moderation_dominance:0.68, payment_system_capture:0.72,
    cloud_sovereignty_erosion:0.75, AI_dependency_trap:0.70,
    surveillance_export_risk:0.68, economic_value_extraction:0.74,
    local_industry_displacement:0.76, regulatory_capture_risk:0.70,
    digital_divide_amplification:0.68, language_digital_exclusion:0.65,
    tech_debt_accumulation:0.70, data_localization_failure:0.86,
    geopolitical_tech_leverage:0.72 },

  // DCE-004: moderate, none
  { entity_id:"DCE-004", tech_domain:"infrastructure_cloud", region:"LATAM",
    platform_dependency_ratio:0.32, data_extraction_intensity:0.28,
    algorithmic_bias_export:0.25, digital_infrastructure_control:0.30,
    content_moderation_dominance:0.28, payment_system_capture:0.30,
    cloud_sovereignty_erosion:0.35, AI_dependency_trap:0.28,
    surveillance_export_risk:0.25, economic_value_extraction:0.30,
    local_industry_displacement:0.28, regulatory_capture_risk:0.32,
    digital_divide_amplification:0.30, language_digital_exclusion:0.28,
    tech_debt_accumulation:0.30, data_localization_failure:0.28,
    geopolitical_tech_leverage:0.32 },

  // DCE-005: critical, AI_dependency_trap_system (adt>0.85 AND cse>0.80)
  { entity_id:"DCE-005", tech_domain:"dépendance_IA_cloud", region:"AFRIQUE_SUB",
    platform_dependency_ratio:0.75, data_extraction_intensity:0.72,
    algorithmic_bias_export:0.70, digital_infrastructure_control:0.78,
    content_moderation_dominance:0.72, payment_system_capture:0.68,
    cloud_sovereignty_erosion:0.88, AI_dependency_trap:0.92,
    surveillance_export_risk:0.68, economic_value_extraction:0.74,
    local_industry_displacement:0.72, regulatory_capture_risk:0.70,
    digital_divide_amplification:0.68, language_digital_exclusion:0.65,
    tech_debt_accumulation:0.70, data_localization_failure:0.72,
    geopolitical_tech_leverage:0.75 },

  // DCE-006: high, surveillance_export_colonialism (ser>0.80 AND abe>0.75; pdr<=0.85, dei<=0.85, adt<=0.85)
  { entity_id:"DCE-006", tech_domain:"exportation_surveillance", region:"MOYEN_ORIENT",
    platform_dependency_ratio:0.55, data_extraction_intensity:0.52,
    algorithmic_bias_export:0.80, digital_infrastructure_control:0.55,
    content_moderation_dominance:0.58, payment_system_capture:0.50,
    cloud_sovereignty_erosion:0.55, AI_dependency_trap:0.52,
    surveillance_export_risk:0.85, economic_value_extraction:0.55,
    local_industry_displacement:0.52, regulatory_capture_risk:0.55,
    digital_divide_amplification:0.50, language_digital_exclusion:0.48,
    tech_debt_accumulation:0.52, data_localization_failure:0.50,
    geopolitical_tech_leverage:0.60 },

  // DCE-007: high, digital_divide_structural (dda>0.80 AND lde>0.75; pdr<=0.85, dei<=0.85, adt<=0.85, ser<=0.80)
  { entity_id:"DCE-007", tech_domain:"fracture_numérique_structurelle", region:"ASIE_CENTRALE",
    platform_dependency_ratio:0.48, data_extraction_intensity:0.45,
    algorithmic_bias_export:0.42, digital_infrastructure_control:0.50,
    content_moderation_dominance:0.45, payment_system_capture:0.48,
    cloud_sovereignty_erosion:0.50, AI_dependency_trap:0.45,
    surveillance_export_risk:0.42, economic_value_extraction:0.48,
    local_industry_displacement:0.50, regulatory_capture_risk:0.45,
    digital_divide_amplification:0.85, language_digital_exclusion:0.82,
    tech_debt_accumulation:0.48, data_localization_failure:0.45,
    geopolitical_tech_leverage:0.48 },

  // DCE-008: low, none
  { entity_id:"DCE-008", tech_domain:"résilience_tech_locale", region:"NAMER",
    platform_dependency_ratio:0.08, data_extraction_intensity:0.10,
    algorithmic_bias_export:0.12, digital_infrastructure_control:0.10,
    content_moderation_dominance:0.08, payment_system_capture:0.12,
    cloud_sovereignty_erosion:0.10, AI_dependency_trap:0.08,
    surveillance_export_risk:0.10, economic_value_extraction:0.08,
    local_industry_displacement:0.10, regulatory_capture_risk:0.12,
    digital_divide_amplification:0.10, language_digital_exclusion:0.08,
    tech_debt_accumulation:0.10, data_localization_failure:0.08,
    geopolitical_tech_leverage:0.10 },
];

type DCEEntity = typeof MOCK_ENTITIES[0];

function dependencyScore(e: DCEEntity): number {
  const v = e.platform_dependency_ratio * 0.40
          + e.AI_dependency_trap * 0.35
          + e.payment_system_capture * 0.25;
  return Math.min(Math.round(v * 10000) / 100, 100);
}
function extractionScore(e: DCEEntity): number {
  const v = e.data_extraction_intensity * 0.40
          + e.economic_value_extraction * 0.35
          + e.local_industry_displacement * 0.25;
  return Math.min(Math.round(v * 10000) / 100, 100);
}
function sovereigntyScore(e: DCEEntity): number {
  const v = e.cloud_sovereignty_erosion * 0.40
          + e.digital_infrastructure_control * 0.35
          + e.regulatory_capture_risk * 0.25;
  return Math.min(Math.round(v * 10000) / 100, 100);
}
function exclusionScore(e: DCEEntity): number {
  const v = e.digital_divide_amplification * 0.40
          + e.language_digital_exclusion * 0.35
          + e.tech_debt_accumulation * 0.25;
  return Math.min(Math.round(v * 10000) / 100, 100);
}
function compositeScore(dep: number, ext: number, sov: number, exc: number): number {
  return Math.min(Math.round((dep * 0.30 + ext * 0.25 + sov * 0.25 + exc * 0.20) * 100) / 100, 100);
}
function colonialPattern(e: DCEEntity): string {
  if (e.platform_dependency_ratio > 0.85 && e.economic_value_extraction > 0.80)  return "platform_imperial_capture";
  if (e.data_extraction_intensity > 0.85 && e.data_localization_failure > 0.80)  return "data_extraction_empire";
  if (e.AI_dependency_trap > 0.85 && e.cloud_sovereignty_erosion > 0.80)         return "AI_dependency_trap_system";
  if (e.surveillance_export_risk > 0.80 && e.algorithmic_bias_export > 0.75)     return "surveillance_export_colonialism";
  if (e.digital_divide_amplification > 0.80 && e.language_digital_exclusion > 0.75) return "digital_divide_structural";
  return "none";
}
function riskLevel(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string {
  if (c >= 60) return "colonialisme_numérique_systémique";
  if (c >= 40) return "crise_souveraineté_tech_majeure";
  if (c >= 20) return "erosion_autonomie_numérique";
  return "souveraineté_tech_relative";
}
function recommendedAction(c: number): string {
  if (c >= 60) return "intervention_décolonisation_numérique_urgente";
  if (c >= 40) return "stratégie_souveraineté_tech_accélérée";
  if (c >= 20) return "renforcement_industrie_numérique_locale";
  return "veille_souveraineté_numérique_continue";
}
function signal(c: number): string {
  if (c >= 60) return "🔴 Colonialisme numérique systémique — souveraineté tech compromise";
  if (c >= 40) return "🟠 Crise souveraineté technologique majeure détectée";
  if (c >= 20) return "🟡 Érosion autonomie numérique active";
  return "🟢 Souveraineté tech relativement maintenue";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const dep = dependencyScore(e), ext = extractionScore(e), sov = sovereigntyScore(e), exc = exclusionScore(e);
      const comp = compositeScore(dep, ext, sov, exc);
      const pat = colonialPattern(e), risk = riskLevel(comp);
      return {
        entity_id: e.entity_id,
        tech_domain: e.tech_domain,
        region: e.region,
        dependency_score: dep,
        extraction_score: ext,
        sovereignty_score: sov,
        exclusion_score: exc,
        composite_score: comp,
        risk_level: risk,
        colonial_pattern: pat,
        severity: severity(comp),
        recommended_action: recommendedAction(comp),
        signal: signal(comp),
        platform_dependency_ratio: e.platform_dependency_ratio,
        data_localization_failure: e.data_localization_failure,
      };
    });

    const patDist:  Record<string,number> = {};
    const riskDist: Record<string,number> = {};
    const sevDist:  Record<string,number> = {};
    const actDist:  Record<string,number> = {};
    let totalComp = 0, critical = 0, high = 0, moderate = 0, low = 0;
    for (const en of entities) {
      patDist[en.colonial_pattern]      = (patDist[en.colonial_pattern]      || 0) + 1;
      riskDist[en.risk_level]           = (riskDist[en.risk_level]           || 0) + 1;
      sevDist[en.severity]              = (sevDist[en.severity]              || 0) + 1;
      actDist[en.recommended_action]    = (actDist[en.recommended_action]    || 0) + 1;
      totalComp += en.composite_score;
      if (en.risk_level === "critical")       critical++;
      else if (en.risk_level === "high")      high++;
      else if (en.risk_level === "moderate")  moderate++;
      else                                    low++;
    }
    const n = entities.length;
    const avgComposite = Math.round(totalComp / n * 10) / 10;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id: 371,
        module_name: "Digital Colonialism & Tech Sovereignty Intelligence Engine",
        total: n,
        critical,
        high,
        moderate,
        low,
        avg_composite: avgComposite,
        pattern_distribution: patDist,
        risk_distribution: riskDist,
        severity_distribution: sevDist,
        action_distribution: actDist,
        avg_estimated_digital_colonial_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
      } as Record<string, unknown>,
    } as Record<string, unknown>, "digital-colonialism-engine") as Parameters<typeof NextResponse.json>[0]);
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/digital-colonialism-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json() as Record<string, unknown>, "digital-colonialism-engine") as Parameters<typeof NextResponse.json>[0]);
  } catch {
    return NextResponse.json(
      sealResponse({ error: "upstream_unavailable" } as Record<string, unknown>, "digital-colonialism-engine") as Parameters<typeof NextResponse.json>[0],
      { status: 502 }
    );
  }
}
