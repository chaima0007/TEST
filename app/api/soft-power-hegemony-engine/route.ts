import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // SPH-001: NOAM, tech_entertainment_hegemon → critical, cultural_monopoly
  { id:"SPH-001", power_domain:"tech_entertainment_hegemon", region:"NOAM",
    cultural_export_dominance:0.88, language_hegemony_index:0.82, media_narrative_control:0.78,
    educational_model_projection:0.75, diaspora_influence_leverage:0.72, brand_ideology_penetration:0.85,
    entertainment_culture_capture:0.90, algorithmic_culture_shaping:0.80, religious_soft_power:0.45,
    normative_framework_dominance:0.70, sports_diplomacy_reach:0.65, tech_standard_setting_power:0.88,
    cultural_autonomy_erosion:0.78, linguistic_diversity_threat:0.72, value_system_colonization:0.68,
    counter_hegemony_capacity:0.20, soft_power_weaponization_index:0.75 },
  // SPH-002: LATAM, local_culture_economy → low, none
  { id:"SPH-002", power_domain:"local_culture_economy", region:"LATAM",
    cultural_export_dominance:0.18, language_hegemony_index:0.22, media_narrative_control:0.20,
    educational_model_projection:0.25, diaspora_influence_leverage:0.28, brand_ideology_penetration:0.15,
    entertainment_culture_capture:0.20, algorithmic_culture_shaping:0.18, religious_soft_power:0.35,
    normative_framework_dominance:0.22, sports_diplomacy_reach:0.30, tech_standard_setting_power:0.15,
    cultural_autonomy_erosion:0.18, linguistic_diversity_threat:0.20, value_system_colonization:0.15,
    counter_hegemony_capacity:0.80, soft_power_weaponization_index:0.10 },
  // SPH-003: EMEA, media_platform → high, narrative_hegemony
  { id:"SPH-003", power_domain:"media_platform", region:"EMEA",
    cultural_export_dominance:0.55, language_hegemony_index:0.60, media_narrative_control:0.78,
    educational_model_projection:0.50, diaspora_influence_leverage:0.48, brand_ideology_penetration:0.52,
    entertainment_culture_capture:0.58, algorithmic_culture_shaping:0.72, religious_soft_power:0.40,
    normative_framework_dominance:0.55, sports_diplomacy_reach:0.45, tech_standard_setting_power:0.50,
    cultural_autonomy_erosion:0.55, linguistic_diversity_threat:0.58, value_system_colonization:0.48,
    counter_hegemony_capacity:0.45, soft_power_weaponization_index:0.52 },
  // SPH-004: APAC, regional_power → low, none
  { id:"SPH-004", power_domain:"regional_power", region:"APAC",
    cultural_export_dominance:0.25, language_hegemony_index:0.28, media_narrative_control:0.22,
    educational_model_projection:0.30, diaspora_influence_leverage:0.32, brand_ideology_penetration:0.20,
    entertainment_culture_capture:0.25, algorithmic_culture_shaping:0.20, religious_soft_power:0.42,
    normative_framework_dominance:0.25, sports_diplomacy_reach:0.35, tech_standard_setting_power:0.28,
    cultural_autonomy_erosion:0.22, linguistic_diversity_threat:0.25, value_system_colonization:0.20,
    counter_hegemony_capacity:0.72, soft_power_weaponization_index:0.18 },
  // SPH-005: NOAM, global_institution → critical, normative_colonization
  { id:"SPH-005", power_domain:"global_institution", region:"NOAM",
    cultural_export_dominance:0.65, language_hegemony_index:0.70, media_narrative_control:0.68,
    educational_model_projection:0.82, diaspora_influence_leverage:0.65, brand_ideology_penetration:0.60,
    entertainment_culture_capture:0.58, algorithmic_culture_shaping:0.62, religious_soft_power:0.50,
    normative_framework_dominance:0.85, sports_diplomacy_reach:0.55, tech_standard_setting_power:0.72,
    cultural_autonomy_erosion:0.70, linguistic_diversity_threat:0.65, value_system_colonization:0.78,
    counter_hegemony_capacity:0.22, soft_power_weaponization_index:0.68 },
  // SPH-006: EMEA, multilateral_org → moderate, none
  { id:"SPH-006", power_domain:"multilateral_org", region:"EMEA",
    cultural_export_dominance:0.38, language_hegemony_index:0.42, media_narrative_control:0.35,
    educational_model_projection:0.40, diaspora_influence_leverage:0.38, brand_ideology_penetration:0.32,
    entertainment_culture_capture:0.35, algorithmic_culture_shaping:0.30, religious_soft_power:0.28,
    normative_framework_dominance:0.45, sports_diplomacy_reach:0.40, tech_standard_setting_power:0.35,
    cultural_autonomy_erosion:0.38, linguistic_diversity_threat:0.35, value_system_colonization:0.32,
    counter_hegemony_capacity:0.60, soft_power_weaponization_index:0.28 },
  // SPH-007: APAC, emerging_hegemon → high, soft_power_weaponization
  { id:"SPH-007", power_domain:"emerging_hegemon", region:"APAC",
    cultural_export_dominance:0.58, language_hegemony_index:0.55, media_narrative_control:0.60,
    educational_model_projection:0.62, diaspora_influence_leverage:0.65, brand_ideology_penetration:0.55,
    entertainment_culture_capture:0.52, algorithmic_culture_shaping:0.58, religious_soft_power:0.48,
    normative_framework_dominance:0.55, sports_diplomacy_reach:0.62, tech_standard_setting_power:0.68,
    cultural_autonomy_erosion:0.72, linguistic_diversity_threat:0.58, value_system_colonization:0.55,
    counter_hegemony_capacity:0.38, soft_power_weaponization_index:0.78 },
  // SPH-008: NOAM, language_institution → critical, linguistic_homogenization
  { id:"SPH-008", power_domain:"language_institution", region:"NOAM",
    cultural_export_dominance:0.72, language_hegemony_index:0.88, media_narrative_control:0.75,
    educational_model_projection:0.80, diaspora_influence_leverage:0.70, brand_ideology_penetration:0.65,
    entertainment_culture_capture:0.68, algorithmic_culture_shaping:0.72, religious_soft_power:0.42,
    normative_framework_dominance:0.68, sports_diplomacy_reach:0.50, tech_standard_setting_power:0.65,
    cultural_autonomy_erosion:0.70, linguistic_diversity_threat:0.82, value_system_colonization:0.65,
    counter_hegemony_capacity:0.18, soft_power_weaponization_index:0.62 },
];

type Entity = typeof MOCK_ENTITIES[0];

function culturalScore(e: Entity): number {
  const raw = (
    e.cultural_export_dominance * 0.4
    + e.entertainment_culture_capture * 0.35
    + e.brand_ideology_penetration * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}
function informationScore(e: Entity): number {
  const raw = (
    e.media_narrative_control * 0.4
    + e.algorithmic_culture_shaping * 0.35
    + e.language_hegemony_index * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}
function normativeScore(e: Entity): number {
  const raw = (
    e.normative_framework_dominance * 0.4
    + e.educational_model_projection * 0.35
    + e.value_system_colonization * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}
function powerScore(e: Entity): number {
  const raw = (
    e.tech_standard_setting_power * 0.4
    + e.diaspora_influence_leverage * 0.35
    + e.soft_power_weaponization_index * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}
function composite(cult: number, info: number, norm: number, pow: number): number {
  return Math.round((cult * 0.30 + info * 0.25 + norm * 0.25 + pow * 0.20) * 100) / 100;
}
function hegemonyPattern(e: Entity): string {
  if (e.cultural_export_dominance >= 0.70 && e.entertainment_culture_capture >= 0.65) return "cultural_monopoly";
  if (e.media_narrative_control >= 0.70 && e.algorithmic_culture_shaping >= 0.65) return "narrative_hegemony";
  if (e.normative_framework_dominance >= 0.70 && e.value_system_colonization >= 0.65) return "normative_colonization";
  if (e.language_hegemony_index >= 0.70 && e.linguistic_diversity_threat >= 0.65) return "linguistic_homogenization";
  if (e.soft_power_weaponization_index >= 0.70 && e.cultural_autonomy_erosion >= 0.65) return "soft_power_weaponization";
  return "none";
}
function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}
function severity(comp: number): string {
  if (comp >= 75) return "hegemony_emergency";
  if (comp >= 50) return "high_hegemony_risk";
  if (comp >= 25) return "hegemony_developing";
  return "cultural_sovereignty_maintained";
}
function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "cultural_sovereignty_emergency";
  if (risk === "high" && pattern === "narrative_hegemony") return "counter_narrative_program";
  if (risk === "high") return "cultural_resilience_framework";
  if (risk === "moderate") return "cultural_monitoring";
  return "no_action";
}
function hegemonySignal(e: Entity, risk: string, comp: number): string {
  if (risk === "critical") {
    return `Critique — domination exportations culturelles ${Math.round(e.cultural_export_dominance * 100)}% — contrôle narratif médias ${Math.round(e.media_narrative_control * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "high") {
    return `Élevé — hégémonie linguistique ${Math.round(e.language_hegemony_index * 100)}% — cadrage normatif ${Math.round(e.normative_framework_dominance * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "moderate") {
    return `Modéré — capture culture divertissement ${Math.round(e.entertainment_culture_capture * 100)}% — composite ${Math.round(comp)}`;
  }
  return "Souveraineté culturelle préservée — pluralisme linguistique intact, autonomie normative maintenue";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[soft-power-hegemony-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tComp=0, tCult=0, tInfo=0, tNorm=0, tPow=0, crisisC=0, interventionC=0;
    for (const ent of entities) {
      rc[ent.hegemony_risk]        = (rc[ent.hegemony_risk]        || 0) + 1;
      pc[ent.hegemony_pattern]     = (pc[ent.hegemony_pattern]     || 0) + 1;
      sc[ent.hegemony_severity]    = (sc[ent.hegemony_severity]    || 0) + 1;
      ac[ent.recommended_action]   = (ac[ent.recommended_action]   || 0) + 1;
      tComp += ent.hegemony_composite;
      tCult += ent.cultural_score;
      tInfo += ent.information_score;
      tNorm += ent.normative_score;
      tPow  += ent.power_score;
      if (ent.is_hegemony_crisis)             crisisC++;
      if (ent.requires_hegemony_intervention) interventionC++;
    }
    const n = entities.length;
    const avgComp = tComp / n;
    const summary = {
      total:                          n,
      risk_counts:                    rc,
      pattern_counts:                 pc,
      severity_counts:                sc,
      action_counts:                  ac,
      avg_hegemony_composite:         Math.round(avgComp * 10) / 10,
      hegemony_crisis_count:          crisisC,
      hegemony_intervention_count:    interventionC,
      avg_cultural_score:             Math.round(tCult / n * 10) / 10,
      avg_information_score:          Math.round(tInfo / n * 10) / 10,
      avg_normative_score:            Math.round(tNorm / n * 10) / 10,
      avg_power_score:                Math.round(tPow  / n * 10) / 10,
      avg_estimated_hegemony_index:   Math.round(avgComp / 100 * 10 * 100) / 100,
    };
    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "soft-power-hegemony-engine")));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/soft-power-hegemony-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    return sealResponse(NextResponse.json(sealResponse(await res.json(), "soft-power-hegemony-engine")));
  } catch {
    return sealResponse(NextResponse.json(sealResponse({ error: "upstream unavailable" }, "soft-power-hegemony-engine"), { status: 502 }));
  }
}
