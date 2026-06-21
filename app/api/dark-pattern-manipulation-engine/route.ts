import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // DPM-001: EMEA, social_media → critical risk, addiction_engineering pattern
  {
    id: "DPM-001", region: "EMEA", platform_type: "social_media",
    confirmshaming_intensity: 0.68,
    hidden_cost_deployment: 0.48,
    forced_continuity_risk: 0.52,
    roach_motel_severity: 0.58,
    misdirection_frequency: 0.62,
    disguised_ads_density: 0.55,
    trick_questions_rate: 0.48,
    bait_switch_index: 0.60,
    attention_capture_addiction_design: 0.92,
    dark_ux_pattern_density: 0.65,
    behavioral_manipulation_depth: 0.88,
    consent_erosion_index: 0.52,
    algorithmic_nudge_coercion: 0.82,
    scarcity_illusion_deployment: 0.70,
    social_proof_manipulation: 0.75,
    emotional_exploitation_index: 0.65,
    regulatory_dark_pattern_gap: 0.65,
  },
  // DPM-002: APAC, e_commerce → low risk, none pattern
  {
    id: "DPM-002", region: "APAC", platform_type: "e_commerce",
    confirmshaming_intensity: 0.10,
    hidden_cost_deployment: 0.12,
    forced_continuity_risk: 0.10,
    roach_motel_severity: 0.08,
    misdirection_frequency: 0.12,
    disguised_ads_density: 0.10,
    trick_questions_rate: 0.09,
    bait_switch_index: 0.10,
    attention_capture_addiction_design: 0.15,
    dark_ux_pattern_density: 0.12,
    behavioral_manipulation_depth: 0.10,
    consent_erosion_index: 0.08,
    algorithmic_nudge_coercion: 0.10,
    scarcity_illusion_deployment: 0.12,
    social_proof_manipulation: 0.10,
    emotional_exploitation_index: 0.08,
    regulatory_dark_pattern_gap: 0.10,
  },
  // DPM-003: NOAM, subscription_platform → high risk, consent_violation pattern
  {
    id: "DPM-003", region: "NOAM", platform_type: "subscription_platform",
    confirmshaming_intensity: 0.50,
    hidden_cost_deployment: 0.45,
    forced_continuity_risk: 0.75,
    roach_motel_severity: 0.55,
    misdirection_frequency: 0.45,
    disguised_ads_density: 0.40,
    trick_questions_rate: 0.42,
    bait_switch_index: 0.45,
    attention_capture_addiction_design: 0.40,
    dark_ux_pattern_density: 0.45,
    behavioral_manipulation_depth: 0.38,
    consent_erosion_index: 0.80,
    algorithmic_nudge_coercion: 0.40,
    scarcity_illusion_deployment: 0.42,
    social_proof_manipulation: 0.45,
    emotional_exploitation_index: 0.42,
    regulatory_dark_pattern_gap: 0.40,
  },
  // DPM-004: LATAM, gaming_platform → low risk, none pattern
  {
    id: "DPM-004", region: "LATAM", platform_type: "gaming_platform",
    confirmshaming_intensity: 0.15,
    hidden_cost_deployment: 0.10,
    forced_continuity_risk: 0.12,
    roach_motel_severity: 0.10,
    misdirection_frequency: 0.15,
    disguised_ads_density: 0.12,
    trick_questions_rate: 0.10,
    bait_switch_index: 0.12,
    attention_capture_addiction_design: 0.18,
    dark_ux_pattern_density: 0.15,
    behavioral_manipulation_depth: 0.12,
    consent_erosion_index: 0.10,
    algorithmic_nudge_coercion: 0.12,
    scarcity_illusion_deployment: 0.15,
    social_proof_manipulation: 0.12,
    emotional_exploitation_index: 0.10,
    regulatory_dark_pattern_gap: 0.12,
  },
  // DPM-005: MEA, social_media → critical risk, psychological_exploitation pattern
  {
    id: "DPM-005", region: "MEA", platform_type: "social_media",
    confirmshaming_intensity: 0.70,
    hidden_cost_deployment: 0.45,
    forced_continuity_risk: 0.50,
    roach_motel_severity: 0.55,
    misdirection_frequency: 0.70,
    disguised_ads_density: 0.60,
    trick_questions_rate: 0.50,
    bait_switch_index: 0.65,
    attention_capture_addiction_design: 0.60,
    dark_ux_pattern_density: 0.62,
    behavioral_manipulation_depth: 0.62,
    consent_erosion_index: 0.55,
    algorithmic_nudge_coercion: 0.82,
    scarcity_illusion_deployment: 0.75,
    social_proof_manipulation: 0.72,
    emotional_exploitation_index: 0.88,
    regulatory_dark_pattern_gap: 0.70,
  },
  // DPM-006: EMEA, news_platform → moderate risk, none pattern
  {
    id: "DPM-006", region: "EMEA", platform_type: "news_platform",
    confirmshaming_intensity: 0.30,
    hidden_cost_deployment: 0.35,
    forced_continuity_risk: 0.28,
    roach_motel_severity: 0.30,
    misdirection_frequency: 0.32,
    disguised_ads_density: 0.28,
    trick_questions_rate: 0.25,
    bait_switch_index: 0.30,
    attention_capture_addiction_design: 0.32,
    dark_ux_pattern_density: 0.30,
    behavioral_manipulation_depth: 0.28,
    consent_erosion_index: 0.25,
    algorithmic_nudge_coercion: 0.30,
    scarcity_illusion_deployment: 0.28,
    social_proof_manipulation: 0.30,
    emotional_exploitation_index: 0.28,
    regulatory_dark_pattern_gap: 0.30,
  },
  // DPM-007: APAC, fintech_app → high risk, systematic_deception pattern
  {
    id: "DPM-007", region: "APAC", platform_type: "fintech_app",
    confirmshaming_intensity: 0.55,
    hidden_cost_deployment: 0.82,
    forced_continuity_risk: 0.45,
    roach_motel_severity: 0.48,
    misdirection_frequency: 0.50,
    disguised_ads_density: 0.50,
    trick_questions_rate: 0.78,
    bait_switch_index: 0.55,
    attention_capture_addiction_design: 0.40,
    dark_ux_pattern_density: 0.45,
    behavioral_manipulation_depth: 0.38,
    consent_erosion_index: 0.42,
    algorithmic_nudge_coercion: 0.38,
    scarcity_illusion_deployment: 0.48,
    social_proof_manipulation: 0.42,
    emotional_exploitation_index: 0.40,
    regulatory_dark_pattern_gap: 0.42,
  },
  // DPM-008: NOAM, big_tech_platform → critical risk, regulatory_evasion pattern
  {
    id: "DPM-008", region: "NOAM", platform_type: "big_tech_platform",
    confirmshaming_intensity: 0.72,
    hidden_cost_deployment: 0.50,
    forced_continuity_risk: 0.55,
    roach_motel_severity: 0.60,
    misdirection_frequency: 0.75,
    disguised_ads_density: 0.65,
    trick_questions_rate: 0.50,
    bait_switch_index: 0.65,
    attention_capture_addiction_design: 0.58,
    dark_ux_pattern_density: 0.82,
    behavioral_manipulation_depth: 0.62,
    consent_erosion_index: 0.55,
    algorithmic_nudge_coercion: 0.62,
    scarcity_illusion_deployment: 0.72,
    social_proof_manipulation: 0.68,
    emotional_exploitation_index: 0.65,
    regulatory_dark_pattern_gap: 0.88,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function deceptionScore(e: Entity): number {
  const raw = e.hidden_cost_deployment * 0.4 + e.disguised_ads_density * 0.35 + e.trick_questions_rate * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function coercionScore(e: Entity): number {
  const raw = e.forced_continuity_risk * 0.4 + e.roach_motel_severity * 0.35 + e.consent_erosion_index * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function addictionScore(e: Entity): number {
  const raw = e.attention_capture_addiction_design * 0.4 + e.behavioral_manipulation_depth * 0.35 + e.algorithmic_nudge_coercion * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function exploitationScore(e: Entity): number {
  const raw = e.emotional_exploitation_index * 0.4 + e.social_proof_manipulation * 0.35 + e.regulatory_dark_pattern_gap * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function compositeScore(dec: number, coe: number, add: number, exp: number): number {
  return Math.round((dec * 0.30 + coe * 0.25 + add * 0.25 + exp * 0.20) * 100) / 100;
}

function manipulationRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function manipulationPattern(e: Entity): string {
  if (e.hidden_cost_deployment >= 0.70 && e.trick_questions_rate >= 0.65) return "systematic_deception";
  if (e.consent_erosion_index >= 0.70 && e.forced_continuity_risk >= 0.65) return "consent_violation";
  if (e.attention_capture_addiction_design >= 0.70 && e.behavioral_manipulation_depth >= 0.65) return "addiction_engineering";
  if (e.emotional_exploitation_index >= 0.70 && e.algorithmic_nudge_coercion >= 0.65) return "psychological_exploitation";
  if (e.regulatory_dark_pattern_gap >= 0.70 && e.dark_ux_pattern_density >= 0.65) return "regulatory_evasion";
  return "none";
}

function manipulationSeverity(comp: number): string {
  if (comp >= 75) return "manipulation_crisis";
  if (comp >= 50) return "high_manipulation";
  if (comp >= 25) return "pattern_accumulation";
  return "ethical_ux";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "dark_pattern_shutdown";
  if (risk === "high" && pattern === "consent_violation") return "regulatory_intervention";
  if (risk === "high") return "manipulation_audit";
  if (risk === "moderate") return "pattern_monitoring";
  return "no_action";
}

function manipulationSignal(e: Entity, pattern: string, comp: number, risk: string): string {
  const riskLabels: Record<string, string> = {
    critical: "risque critique", high: "risque élevé",
    moderate: "risque modéré", low: "risque faible",
  };
  const patternLabels: Record<string, string> = {
    systematic_deception: "déception systématique",
    consent_violation: "violation du consentement",
    addiction_engineering: "ingénierie de l'addiction",
    psychological_exploitation: "exploitation psychologique",
    regulatory_evasion: "évasion réglementaire",
    none: "aucun pattern détecté",
  };
  const riskFr = riskLabels[risk] ?? risk;
  const patternFr = patternLabels[pattern] ?? pattern.replace(/_/g, " ");
  const compStr = comp.toFixed(1);

  if (comp < 20) {
    return `Plateforme ${e.platform_type} (${e.region}) — UX éthique confirmé — aucune manipulation détectée — composite ${compStr} — conformité satisfaisante`;
  }
  return (
    `Alerte manipulation numérique — plateforme ${e.platform_type} (${e.region}) — ` +
    `${riskFr} — pattern: ${patternFr} — ` +
    `indice composite ${compStr} — ` +
    `déception ${Math.round(e.hidden_cost_deployment * 100)}% — ` +
    `coercition ${Math.round(e.forced_continuity_risk * 100)}% — ` +
    `exploitation émotionnelle ${Math.round(e.emotional_exploitation_index * 100)}%`
  );
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map((e) => {
      const dec = deceptionScore(e);
      const coe = coercionScore(e);
      const add = addictionScore(e);
      const exp = exploitationScore(e);
      const comp = compositeScore(dec, coe, add, exp);
      const risk = manipulationRisk(comp);
      const pattern = manipulationPattern(e);
      const severity = manipulationSeverity(comp);
      const action = recommendedAction(risk, pattern);
      return {
        id: e.entity_id,
        region: e.region,
        platform_type: e.platform_type,
        manipulation_risk: risk,
        manipulation_pattern: pattern,
        manipulation_severity: severity,
        recommended_action: action,
        deception_score: dec,
        coercion_score: coe,
        addiction_score: add,
        exploitation_score: exp,
        manipulation_composite: comp,
        is_manipulation_crisis: comp >= 60,
        requires_manipulation_intervention: comp >= 40,
        manipulation_signal: manipulationSignal(e, pattern, comp, risk),
      };
    });

    const patternFreq: Record<string, number> = {};
    let tDec = 0, tCoe = 0, tAdd = 0, tExp = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const r of entities) {
      if (r.manipulation_pattern !== "none") {
        patternFreq[r.manipulation_pattern] = (patternFreq[r.manipulation_pattern] || 0) + 1;
      }
      if (r.manipulation_risk === "critical") criticalCount++;
      else if (r.manipulation_risk === "high") highCount++;
      else if (r.manipulation_risk === "moderate") moderateCount++;
      else lowCount++;
      if (r.is_manipulation_crisis) crisisCount++;
      if (r.requires_manipulation_intervention) interventionCount++;
      tDec  += r.deception_score;
      tCoe  += r.coercion_score;
      tAdd  += r.addiction_score;
      tExp  += r.exploitation_score;
      tComp += r.manipulation_composite;
    }

    const n = entities.length;
    const dominantPattern = Object.keys(patternFreq).length > 0
      ? Object.keys(patternFreq).reduce((a, b) => patternFreq[a] >= patternFreq[b] ? a : b)
      : "none";

    const avgComposite = Math.round(tComp / n * 100) / 100;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        total_entities_analyzed: n,
        critical_manipulation_count: criticalCount,
        high_manipulation_count: highCount,
        moderate_manipulation_count: moderateCount,
        low_manipulation_count: lowCount,
        manipulation_crisis_count: crisisCount,
        requires_intervention_count: interventionCount,
        dominant_manipulation_pattern: dominantPattern,
        avg_deception_score: Math.round(tDec / n * 100) / 100,
        avg_coercion_score: Math.round(tCoe / n * 100) / 100,
        avg_addiction_score: Math.round(tAdd / n * 100) / 100,
        avg_exploitation_score: Math.round(tExp / n * 100) / 100,
        avg_estimated_manipulation_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
      },
    } as Record<string, unknown>, "dark-pattern-manipulation-engine") as Parameters<typeof NextResponse.json>[0]);
  }

  return NextResponse.json(sealResponse(
    await (await fetch(`${process.env.SWARM_API_URL}/dark-pattern-manipulation-engine`)).json(),
    "dark-pattern-manipulation-engine"
  ) as Parameters<typeof NextResponse.json>[0]);
}
