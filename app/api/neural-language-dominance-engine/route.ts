import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // NLD-001 tech_platform NAMER — critical / AI_language_hegemony
  { id:"NLD-001", language_domain:"tech_platform",      region:"NAMER", english_AI_training_bias:0.85, linguistic_minority_exclusion_rate:0.72, LLM_monolingual_dominance:0.60, language_death_acceleration_index:0.65, cognitive_framework_homogenization:0.60, translation_sovereignty_risk:0.68, AI_language_gatekeeping_power:0.78, cultural_concept_untranslatability_loss:0.65, indigenous_language_AI_gap:0.65, narrative_framing_linguistic_lock:0.70, multilingual_AI_access_inequality:0.68, syntactic_worldview_erosion:0.65, linguistic_decolonization_resistance:0.70, semantic_manipulation_via_language:0.60, LLM_cultural_bias_propagation:0.55, language_as_power_concentration:0.75, cognitive_sovereignty_erosion_index:0.72 },
  // NLD-002 minority_language EMEA — low / none
  { id:"NLD-002", language_domain:"minority_language",  region:"EMEA",  english_AI_training_bias:0.12, linguistic_minority_exclusion_rate:0.10, LLM_monolingual_dominance:0.10, language_death_acceleration_index:0.08, cognitive_framework_homogenization:0.10, translation_sovereignty_risk:0.12, AI_language_gatekeeping_power:0.08, cultural_concept_untranslatability_loss:0.12, indigenous_language_AI_gap:0.08, narrative_framing_linguistic_lock:0.10, multilingual_AI_access_inequality:0.12, syntactic_worldview_erosion:0.10, linguistic_decolonization_resistance:0.08, semantic_manipulation_via_language:0.10, LLM_cultural_bias_propagation:0.08, language_as_power_concentration:0.12, cognitive_sovereignty_erosion_index:0.10 },
  // NLD-003 social_media APAC — high / linguistic_monoculture_collapse
  { id:"NLD-003", language_domain:"social_media",       region:"APAC",  english_AI_training_bias:0.40, linguistic_minority_exclusion_rate:0.38, LLM_monolingual_dominance:0.72, language_death_acceleration_index:0.68, cognitive_framework_homogenization:0.42, translation_sovereignty_risk:0.38, AI_language_gatekeeping_power:0.38, cultural_concept_untranslatability_loss:0.40, indigenous_language_AI_gap:0.30, narrative_framing_linguistic_lock:0.42, multilingual_AI_access_inequality:0.35, syntactic_worldview_erosion:0.38, linguistic_decolonization_resistance:0.35, semantic_manipulation_via_language:0.35, LLM_cultural_bias_propagation:0.32, language_as_power_concentration:0.35, cognitive_sovereignty_erosion_index:0.38 },
  // NLD-004 indigenous_community LATAM — low / none
  { id:"NLD-004", language_domain:"indigenous_community", region:"LATAM", english_AI_training_bias:0.08, linguistic_minority_exclusion_rate:0.12, LLM_monolingual_dominance:0.12, language_death_acceleration_index:0.10, cognitive_framework_homogenization:0.08, translation_sovereignty_risk:0.10, AI_language_gatekeeping_power:0.10, cultural_concept_untranslatability_loss:0.12, indigenous_language_AI_gap:0.10, narrative_framing_linguistic_lock:0.08, multilingual_AI_access_inequality:0.08, syntactic_worldview_erosion:0.12, linguistic_decolonization_resistance:0.12, semantic_manipulation_via_language:0.08, LLM_cultural_bias_propagation:0.10, language_as_power_concentration:0.08, cognitive_sovereignty_erosion_index:0.10 },
  // NLD-005 ai_foundation_model GLOBAL — critical / cognitive_colonization
  { id:"NLD-005", language_domain:"ai_foundation_model", region:"GLOBAL", english_AI_training_bias:0.75, linguistic_minority_exclusion_rate:0.68, LLM_monolingual_dominance:0.60, language_death_acceleration_index:0.72, cognitive_framework_homogenization:0.78, translation_sovereignty_risk:0.70, AI_language_gatekeeping_power:0.70, cultural_concept_untranslatability_loss:0.70, indigenous_language_AI_gap:0.65, narrative_framing_linguistic_lock:0.70, multilingual_AI_access_inequality:0.70, syntactic_worldview_erosion:0.68, linguistic_decolonization_resistance:0.75, semantic_manipulation_via_language:0.60, LLM_cultural_bias_propagation:0.55, language_as_power_concentration:0.72, cognitive_sovereignty_erosion_index:0.80 },
  // NLD-006 translation_service MEA — moderate / none
  { id:"NLD-006", language_domain:"translation_service", region:"MEA",  english_AI_training_bias:0.28, linguistic_minority_exclusion_rate:0.30, LLM_monolingual_dominance:0.30, language_death_acceleration_index:0.28, cognitive_framework_homogenization:0.32, translation_sovereignty_risk:0.28, AI_language_gatekeeping_power:0.25, cultural_concept_untranslatability_loss:0.25, indigenous_language_AI_gap:0.22, narrative_framing_linguistic_lock:0.28, multilingual_AI_access_inequality:0.28, syntactic_worldview_erosion:0.25, linguistic_decolonization_resistance:0.28, semantic_manipulation_via_language:0.25, LLM_cultural_bias_propagation:0.22, language_as_power_concentration:0.30, cognitive_sovereignty_erosion_index:0.30 },
  // NLD-007 education_platform SSA — high / indigenous_extinction
  { id:"NLD-007", language_domain:"education_platform", region:"SSA",   english_AI_training_bias:0.38, linguistic_minority_exclusion_rate:0.68, LLM_monolingual_dominance:0.40, language_death_acceleration_index:0.42, cognitive_framework_homogenization:0.40, translation_sovereignty_risk:0.38, AI_language_gatekeeping_power:0.35, cultural_concept_untranslatability_loss:0.38, indigenous_language_AI_gap:0.72, narrative_framing_linguistic_lock:0.40, multilingual_AI_access_inequality:0.42, syntactic_worldview_erosion:0.38, linguistic_decolonization_resistance:0.38, semantic_manipulation_via_language:0.35, LLM_cultural_bias_propagation:0.32, language_as_power_concentration:0.40, cognitive_sovereignty_erosion_index:0.42 },
  // NLD-008 media_narrative GLOBAL — critical / semantic_manipulation_crisis
  { id:"NLD-008", language_domain:"media_narrative",    region:"GLOBAL", english_AI_training_bias:0.65, linguistic_minority_exclusion_rate:0.62, LLM_monolingual_dominance:0.60, language_death_acceleration_index:0.65, cognitive_framework_homogenization:0.68, translation_sovereignty_risk:0.65, AI_language_gatekeeping_power:0.60, cultural_concept_untranslatability_loss:0.65, indigenous_language_AI_gap:0.60, narrative_framing_linguistic_lock:0.72, multilingual_AI_access_inequality:0.65, syntactic_worldview_erosion:0.65, linguistic_decolonization_resistance:0.70, semantic_manipulation_via_language:0.78, LLM_cultural_bias_propagation:0.72, language_as_power_concentration:0.68, cognitive_sovereignty_erosion_index:0.72 },
];

type Entity = typeof MOCK_ENTITIES[0];

function dominanceScore(e: Entity): number {
  return Math.round((e.english_AI_training_bias * 0.40 + e.LLM_monolingual_dominance * 0.35 + e.AI_language_gatekeeping_power * 0.25) * 10000) / 100;
}
function exclusionScore(e: Entity): number {
  return Math.round((e.linguistic_minority_exclusion_rate * 0.40 + e.multilingual_AI_access_inequality * 0.35 + e.indigenous_language_AI_gap * 0.25) * 10000) / 100;
}
function homogenizationScore(e: Entity): number {
  return Math.round((e.cognitive_framework_homogenization * 0.40 + e.language_death_acceleration_index * 0.35 + e.cultural_concept_untranslatability_loss * 0.25) * 10000) / 100;
}
function sovereigntyScore(e: Entity): number {
  return Math.round((e.cognitive_sovereignty_erosion_index * 0.40 + e.linguistic_decolonization_resistance * 0.35 + e.language_as_power_concentration * 0.25) * 10000) / 100;
}
function compositeScore(d: number, ex: number, h: number, s: number): number {
  return Math.round((d * 0.30 + ex * 0.25 + h * 0.25 + s * 0.20) * 100) / 100;
}
function languagePattern(e: Entity): string {
  if (e.LLM_monolingual_dominance >= 0.70 && e.language_death_acceleration_index >= 0.65) return "linguistic_monoculture_collapse";
  if (e.cognitive_framework_homogenization >= 0.70 && e.cognitive_sovereignty_erosion_index >= 0.65) return "cognitive_colonization";
  if (e.english_AI_training_bias >= 0.70 && e.AI_language_gatekeeping_power >= 0.65) return "AI_language_hegemony";
  if (e.indigenous_language_AI_gap >= 0.70 && e.linguistic_minority_exclusion_rate >= 0.65) return "indigenous_extinction";
  if (e.semantic_manipulation_via_language >= 0.70 && e.LLM_cultural_bias_propagation >= 0.65) return "semantic_manipulation_crisis";
  return "none";
}
function riskLevel(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string {
  if (c >= 60) return "hégémonie_linguistique_totale";
  if (c >= 40) return "domination_linguistique_avancée";
  if (c >= 20) return "homogénéisation_active";
  return "diversité_linguistique_relative";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "souveraineté_linguistique_urgente";
  if (risk === "high")     return "décolonisation_linguistique_IA";
  if (risk === "moderate") return "renforcement_multilinguisme_IA";
  return "veille_diversité_linguistique";
}
function signal(c: number): string {
  if (c >= 60) return "🔴 Hégémonie linguistique totale — colonisation cognitive via IA";
  if (c >= 40) return "🟠 Domination linguistique avancée détectée";
  if (c >= 20) return "🟡 Homogénéisation linguistique en cours";
  return "🟢 Diversité linguistique relativement préservée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[neural-language-dominance-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string, number> = {}, pc: Record<string, number> = {}, sc: Record<string, number> = {}, ac: Record<string, number> = {};
    let tDom = 0, tExc = 0, tHom = 0, tSov = 0, tComp = 0;
    for (const ent of entities) {
      rc[ent.risk_level]        = (rc[ent.risk_level]        || 0) + 1;
      pc[ent.language_pattern]  = (pc[ent.language_pattern]  || 0) + 1;
      sc[ent.severity]          = (sc[ent.severity]          || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tDom  += ent.dominance_score;
      tExc  += ent.exclusion_score;
      tHom  += ent.homogenization_score;
      tSov  += ent.sovereignty_score;
      tComp += ent.composite_score;
    }
    const n = entities.length;
    const avgComp = Math.round(tComp / n * 100) / 100;

    return sealResponse(NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id:                                336,
        module_name:                              "Neural Language Dominance & Linguistic Intelligence Engine",
        total_entities:                           n,
        critical_count:                           rc["critical"] ?? 0,
        high_count:                               rc["high"]     ?? 0,
        moderate_count:                           rc["moderate"] ?? 0,
        low_count:                                rc["low"]      ?? 0,
        avg_composite:                            avgComp,
        pattern_distribution:                     pc,
        risk_distribution:                        rc,
        severity_distribution:                    sc,
        action_distribution:                      ac,
        avg_estimated_linguistic_dominance_index: Math.round(avgComp / 100 * 10 * 100) / 100,
        avg_dominance_score:                      Math.round(tDom  / n * 10) / 10,
        avg_exclusion_score:                      Math.round(tExc  / n * 10) / 10,
        avg_homogenization_score:                 Math.round(tHom  / n * 10) / 10,
        avg_sovereignty_score:                    Math.round(tSov  / n * 10) / 10,
      },
    } as Record<string, unknown>)));
  }

  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/neural-language-dominance-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    return sealResponse(NextResponse.json(sealResponse(await res.json() as Record<string, unknown>)));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 } as Record<string, unknown>),
      { status: 502 },
    ));
  }
}
