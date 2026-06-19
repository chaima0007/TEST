import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  // SWARM_API_URL guard — will use mock data below
}

const MOCK_ENTITIES = [
  // GAE-001 — critical, pattern=creative_class_extinction
  // creative_class_extinction: AI_creative_displacement_rate>=0.70 AND creator_income_collapse_index>=0.65
  // composite >= 60 → critical
  {
    entity_id: "GAE-001", creative_sector: "illustration_design", region: "NOAM",
    AI_creative_displacement_rate: 0.85,
    copyright_training_data_exploitation: 0.60,
    creator_income_collapse_index: 0.80,
    AI_aesthetic_homogenization_risk: 0.65,
    generative_model_monopoly_concentration: 0.70,
    human_creativity_devaluation: 0.75,
    cultural_diversity_AI_erosion: 0.60,
    misinformation_synthetic_content_volume: 0.60,
    AI_plagiarism_undetectability: 0.55,
    creative_class_economic_collapse: 0.78,
    AI_gatekeeper_content_control: 0.65,
    authenticity_market_collapse: 0.50,
    AI_artistic_labor_substitution: 0.75,
    emotional_labor_AI_replacement_risk: 0.68,
    creative_IP_extraction_rate: 0.62,
    training_consent_violation_scale: 0.58,
    AI_cultural_production_homogeny: 0.55,
  },
  // GAE-002 — low, pattern=none
  // composite < 20 → low; no pattern triggers
  {
    entity_id: "GAE-002", creative_sector: "artisanal_craft", region: "EMEA",
    AI_creative_displacement_rate: 0.08,
    copyright_training_data_exploitation: 0.08,
    creator_income_collapse_index: 0.10,
    AI_aesthetic_homogenization_risk: 0.10,
    generative_model_monopoly_concentration: 0.10,
    human_creativity_devaluation: 0.08,
    cultural_diversity_AI_erosion: 0.08,
    misinformation_synthetic_content_volume: 0.10,
    AI_plagiarism_undetectability: 0.08,
    creative_class_economic_collapse: 0.08,
    AI_gatekeeper_content_control: 0.08,
    authenticity_market_collapse: 0.10,
    AI_artistic_labor_substitution: 0.08,
    emotional_labor_AI_replacement_risk: 0.08,
    creative_IP_extraction_rate: 0.08,
    training_consent_violation_scale: 0.08,
    AI_cultural_production_homogeny: 0.08,
  },
  // GAE-003 — high, pattern=generative_monopoly_capture
  // generative_monopoly_capture: generative_model_monopoly_concentration>=0.70 AND AI_gatekeeper_content_control>=0.65
  // creative_class_extinction must NOT fire: AI_creative_displacement_rate<0.70 OR creator_income_collapse_index<0.65
  // composite >=40 and <60 → high
  {
    entity_id: "GAE-003", creative_sector: "digital_media", region: "APAC",
    AI_creative_displacement_rate: 0.50,
    copyright_training_data_exploitation: 0.55,
    creator_income_collapse_index: 0.45,
    AI_aesthetic_homogenization_risk: 0.45,
    generative_model_monopoly_concentration: 0.80,
    human_creativity_devaluation: 0.48,
    cultural_diversity_AI_erosion: 0.42,
    misinformation_synthetic_content_volume: 0.42,
    AI_plagiarism_undetectability: 0.38,
    creative_class_economic_collapse: 0.45,
    AI_gatekeeper_content_control: 0.75,
    authenticity_market_collapse: 0.40,
    AI_artistic_labor_substitution: 0.48,
    emotional_labor_AI_replacement_risk: 0.42,
    creative_IP_extraction_rate: 0.50,
    training_consent_violation_scale: 0.45,
    AI_cultural_production_homogeny: 0.40,
  },
  // GAE-004 — low, pattern=none
  // composite < 20 → low; no pattern triggers
  {
    entity_id: "GAE-004", creative_sector: "folk_traditions", region: "LATAM",
    AI_creative_displacement_rate: 0.12,
    copyright_training_data_exploitation: 0.10,
    creator_income_collapse_index: 0.10,
    AI_aesthetic_homogenization_risk: 0.08,
    generative_model_monopoly_concentration: 0.12,
    human_creativity_devaluation: 0.10,
    cultural_diversity_AI_erosion: 0.10,
    misinformation_synthetic_content_volume: 0.10,
    AI_plagiarism_undetectability: 0.08,
    creative_class_economic_collapse: 0.10,
    AI_gatekeeper_content_control: 0.10,
    authenticity_market_collapse: 0.10,
    AI_artistic_labor_substitution: 0.10,
    emotional_labor_AI_replacement_risk: 0.08,
    creative_IP_extraction_rate: 0.10,
    training_consent_violation_scale: 0.08,
    AI_cultural_production_homogeny: 0.08,
  },
  // GAE-005 — critical, pattern=cultural_homogenization_crisis
  // cultural_homogenization_crisis: AI_aesthetic_homogenization_risk>=0.70 AND AI_cultural_production_homogeny>=0.65
  // creative_class_extinction must NOT fire: AI_creative_displacement_rate<0.70 OR creator_income_collapse_index<0.65
  // generative_monopoly_capture must NOT fire: generative_model_monopoly_concentration<0.70 OR AI_gatekeeper_content_control<0.65
  // composite >= 60 → critical
  {
    entity_id: "GAE-005", creative_sector: "music_production", region: "MEA",
    AI_creative_displacement_rate: 0.62,
    copyright_training_data_exploitation: 0.65,
    creator_income_collapse_index: 0.58,
    AI_aesthetic_homogenization_risk: 0.85,
    generative_model_monopoly_concentration: 0.62,
    human_creativity_devaluation: 0.70,
    cultural_diversity_AI_erosion: 0.78,
    misinformation_synthetic_content_volume: 0.68,
    AI_plagiarism_undetectability: 0.62,
    creative_class_economic_collapse: 0.65,
    AI_gatekeeper_content_control: 0.60,
    authenticity_market_collapse: 0.60,
    AI_artistic_labor_substitution: 0.60,
    emotional_labor_AI_replacement_risk: 0.62,
    creative_IP_extraction_rate: 0.65,
    training_consent_violation_scale: 0.60,
    AI_cultural_production_homogeny: 0.80,
  },
  // GAE-006 — moderate, pattern=none
  // composite >=20 and <40 → moderate; no pattern triggers
  {
    entity_id: "GAE-006", creative_sector: "indie_publishing", region: "EMEA",
    AI_creative_displacement_rate: 0.30,
    copyright_training_data_exploitation: 0.25,
    creator_income_collapse_index: 0.28,
    AI_aesthetic_homogenization_risk: 0.30,
    generative_model_monopoly_concentration: 0.32,
    human_creativity_devaluation: 0.28,
    cultural_diversity_AI_erosion: 0.28,
    misinformation_synthetic_content_volume: 0.28,
    AI_plagiarism_undetectability: 0.25,
    creative_class_economic_collapse: 0.28,
    AI_gatekeeper_content_control: 0.28,
    authenticity_market_collapse: 0.28,
    AI_artistic_labor_substitution: 0.28,
    emotional_labor_AI_replacement_risk: 0.25,
    creative_IP_extraction_rate: 0.28,
    training_consent_violation_scale: 0.25,
    AI_cultural_production_homogeny: 0.25,
  },
  // GAE-007 — high, pattern=IP_extraction_empire
  // IP_extraction_empire: copyright_training_data_exploitation>=0.70 AND training_consent_violation_scale>=0.65
  // creative_class_extinction must NOT fire: AI_creative_displacement_rate<0.70 OR creator_income_collapse_index<0.65
  // generative_monopoly_capture must NOT fire: generative_model_monopoly_concentration<0.70 OR AI_gatekeeper_content_control<0.65
  // cultural_homogenization_crisis must NOT fire: AI_aesthetic_homogenization_risk<0.70 OR AI_cultural_production_homogeny<0.65
  // composite >=40 and <60 → high
  {
    entity_id: "GAE-007", creative_sector: "stock_photography", region: "NOAM",
    AI_creative_displacement_rate: 0.50,
    copyright_training_data_exploitation: 0.82,
    creator_income_collapse_index: 0.48,
    AI_aesthetic_homogenization_risk: 0.52,
    generative_model_monopoly_concentration: 0.52,
    human_creativity_devaluation: 0.50,
    cultural_diversity_AI_erosion: 0.48,
    misinformation_synthetic_content_volume: 0.45,
    AI_plagiarism_undetectability: 0.42,
    creative_class_economic_collapse: 0.50,
    AI_gatekeeper_content_control: 0.48,
    authenticity_market_collapse: 0.40,
    AI_artistic_labor_substitution: 0.45,
    emotional_labor_AI_replacement_risk: 0.42,
    creative_IP_extraction_rate: 0.72,
    training_consent_violation_scale: 0.72,
    AI_cultural_production_homogeny: 0.45,
  },
  // GAE-008 — critical, pattern=synthetic_content_saturation
  // synthetic_content_saturation: misinformation_synthetic_content_volume>=0.70 AND AI_plagiarism_undetectability>=0.65
  // creative_class_extinction must NOT fire: AI_creative_displacement_rate<0.70 OR creator_income_collapse_index<0.65
  // generative_monopoly_capture must NOT fire: generative_model_monopoly_concentration<0.70 OR AI_gatekeeper_content_control<0.65
  // cultural_homogenization_crisis must NOT fire: AI_aesthetic_homogenization_risk<0.70 OR AI_cultural_production_homogeny<0.65
  // IP_extraction_empire must NOT fire: copyright_training_data_exploitation<0.70 OR training_consent_violation_scale<0.65
  // composite >= 60 → critical
  {
    entity_id: "GAE-008", creative_sector: "journalism_news", region: "APAC",
    AI_creative_displacement_rate: 0.65,
    copyright_training_data_exploitation: 0.65,
    creator_income_collapse_index: 0.60,
    AI_aesthetic_homogenization_risk: 0.62,
    generative_model_monopoly_concentration: 0.62,
    human_creativity_devaluation: 0.65,
    cultural_diversity_AI_erosion: 0.60,
    misinformation_synthetic_content_volume: 0.85,
    AI_plagiarism_undetectability: 0.80,
    creative_class_economic_collapse: 0.62,
    AI_gatekeeper_content_control: 0.58,
    authenticity_market_collapse: 0.75,
    AI_artistic_labor_substitution: 0.62,
    emotional_labor_AI_replacement_risk: 0.60,
    creative_IP_extraction_rate: 0.65,
    training_consent_violation_scale: 0.60,
    AI_cultural_production_homogeny: 0.55,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function displacementScore(e: Entity): number {
  const raw = (
    e.AI_creative_displacement_rate * 0.4 +
    e.creator_income_collapse_index * 0.35 +
    e.AI_artistic_labor_substitution * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function controlScore(e: Entity): number {
  const raw = (
    e.generative_model_monopoly_concentration * 0.4 +
    e.AI_gatekeeper_content_control * 0.35 +
    e.copyright_training_data_exploitation * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function cultureScore(e: Entity): number {
  const raw = (
    e.AI_aesthetic_homogenization_risk * 0.4 +
    e.cultural_diversity_AI_erosion * 0.35 +
    e.AI_cultural_production_homogeny * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function integrityScore(e: Entity): number {
  const raw = (
    e.misinformation_synthetic_content_volume * 0.4 +
    e.AI_plagiarism_undetectability * 0.35 +
    e.authenticity_market_collapse * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(disp: number, ctrl: number, cult: number, intg: number): number {
  return Math.round((disp * 0.30 + ctrl * 0.25 + cult * 0.25 + intg * 0.20) * 100) / 100;
}

function genaiPattern(e: Entity): string {
  if (e.AI_creative_displacement_rate >= 0.70 && e.creator_income_collapse_index >= 0.65)
    return "creative_class_extinction";
  if (e.generative_model_monopoly_concentration >= 0.70 && e.AI_gatekeeper_content_control >= 0.65)
    return "generative_monopoly_capture";
  if (e.AI_aesthetic_homogenization_risk >= 0.70 && e.AI_cultural_production_homogeny >= 0.65)
    return "cultural_homogenization_crisis";
  if (e.copyright_training_data_exploitation >= 0.70 && e.training_consent_violation_scale >= 0.65)
    return "IP_extraction_empire";
  if (e.misinformation_synthetic_content_volume >= 0.70 && e.AI_plagiarism_undetectability >= 0.65)
    return "synthetic_content_saturation";
  return "none";
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function severity(comp: number): string {
  if (comp >= 60) return "effondrement_économie_créative";
  if (comp >= 40) return "disruption_créative_majeure";
  if (comp >= 20) return "restructuration_créative_active";
  return "disruption_créative_gérée";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "protection_urgente_économie_créative";
  if (risk === "high") return "régulation_IA_générative_stricte";
  if (risk === "moderate") return "renforcement_droits_créateurs_IA";
  return "veille_disruption_créative_continue";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Effondrement économie créative — IA générative systémique";
  if (risk === "high") return "🟠 Disruption créative majeure détectée";
  if (risk === "moderate") return "🟡 Restructuration créative active en cours";
  return "🟢 Disruption créative gérée et surveillée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const disp = displacementScore(e);
      const ctrl = controlScore(e);
      const cult = cultureScore(e);
      const intg = integrityScore(e);
      const comp = compositeScore(disp, ctrl, cult, intg);
      const pat  = genaiPattern(e);
      const risk = riskLevel(comp);
      const sev  = severity(comp);
      const act  = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        entity_id:                              e.entity_id,
        creative_sector:                        e.creative_sector,
        region:                                 e.region,
        displacement_score:                     disp,
        control_score:                          ctrl,
        culture_score:                          cult,
        integrity_score:                        intg,
        composite_score:                        comp,
        risk_level:                             risk,
        genai_pattern:                          pat,
        severity:                               sev,
        recommended_action:                     act,
        signal:                                 sig,
        AI_creative_displacement_rate:          e.AI_creative_displacement_rate,
        generative_model_monopoly_concentration: e.generative_model_monopoly_concentration,
      };
    });

    const riskDist: Record<string, number> = {};
    const patDist: Record<string, number> = {};
    const sevDist: Record<string, number> = {};
    const actDist: Record<string, number> = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      riskDist[ent.risk_level]        = (riskDist[ent.risk_level]        || 0) + 1;
      patDist[ent.genai_pattern]      = (patDist[ent.genai_pattern]      || 0) + 1;
      sevDist[ent.severity]           = (sevDist[ent.severity]           || 0) + 1;
      actDist[ent.recommended_action] = (actDist[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;
    const summary = {
      module_id:                              350,
      module_name:                            "Generative AI & Creative Economy Disruption Intelligence Engine",
      total_entities:                         n,
      critical_count:                         criticalCount,
      high_count:                             highCount,
      moderate_count:                         moderateCount,
      low_count:                              lowCount,
      avg_composite:                          avgComposite,
      pattern_distribution:                   patDist,
      risk_distribution:                      riskDist,
      severity_distribution:                  sevDist,
      action_distribution:                    actDist,
      avg_estimated_creative_disruption_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "generative-ai-economy-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/generative-ai-economy-engine`);
    const data = await upstream.json();
    return NextResponse.json(sealResponse(data, "generative-ai-economy-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream generative AI economy engine unavailable" }, "generative-ai-economy-engine"),
      { status: 502 }
    );
  }
}
