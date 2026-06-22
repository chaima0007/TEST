import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // CSE-001 — critical, grooming_network_proliferation (predator>0.85, grooming>0.80)
  {
    id: "CSE-001", platform_type: "réseau_social", region: "EMEA",
    predator_network_density: 0.92, grooming_incident_rate: 0.88,
    csam_detection_gap: 0.70, algorithmic_harm_amplification: 0.68,
    screen_addiction_severity: 0.65, cyberbullying_prevalence: 0.72,
    sextortion_risk_index: 0.68, age_verification_failure: 0.75,
    parental_control_gap: 0.65, dark_web_exposure: 0.70,
    mental_health_impact: 0.68, reporting_mechanism_gap: 0.65,
    law_enforcement_capacity: 0.62, cross_border_jurisdiction_gap: 0.70,
    digital_literacy_children: 0.60, platform_transparency_failure: 0.68,
    regulatory_enforcement_gap: 0.65,
  },
  // CSE-002 — critical, csam_distribution_infrastructure (csam>0.85, dark_web>0.80)
  {
    id: "CSE-002", platform_type: "messagerie_chiffrée", region: "APAC",
    predator_network_density: 0.72, grooming_incident_rate: 0.65,
    csam_detection_gap: 0.90, algorithmic_harm_amplification: 0.68,
    screen_addiction_severity: 0.62, cyberbullying_prevalence: 0.65,
    sextortion_risk_index: 0.70, age_verification_failure: 0.68,
    parental_control_gap: 0.65, dark_web_exposure: 0.85,
    mental_health_impact: 0.62, reporting_mechanism_gap: 0.68,
    law_enforcement_capacity: 0.70, cross_border_jurisdiction_gap: 0.72,
    digital_literacy_children: 0.60, platform_transparency_failure: 0.68,
    regulatory_enforcement_gap: 0.72,
  },
  // CSE-003 — critical, algorithmic_radicalization_youth (algo>0.85, screen>0.80)
  {
    id: "CSE-003", platform_type: "plateforme_vidéo", region: "NOAM",
    predator_network_density: 0.65, grooming_incident_rate: 0.62,
    csam_detection_gap: 0.68, algorithmic_harm_amplification: 0.88,
    screen_addiction_severity: 0.82, cyberbullying_prevalence: 0.70,
    sextortion_risk_index: 0.65, age_verification_failure: 0.72,
    parental_control_gap: 0.68, dark_web_exposure: 0.62,
    mental_health_impact: 0.75, reporting_mechanism_gap: 0.65,
    law_enforcement_capacity: 0.60, cross_border_jurisdiction_gap: 0.65,
    digital_literacy_children: 0.58, platform_transparency_failure: 0.70,
    regulatory_enforcement_gap: 0.65,
  },
  // CSE-004 — high, sextortion_epidemic (sextortion>0.80, cyberbullying>0.75)
  {
    id: "CSE-004", platform_type: "jeu_en_ligne", region: "LATAM",
    predator_network_density: 0.50, grooming_incident_rate: 0.48,
    csam_detection_gap: 0.50, algorithmic_harm_amplification: 0.52,
    screen_addiction_severity: 0.55, cyberbullying_prevalence: 0.78,
    sextortion_risk_index: 0.82, age_verification_failure: 0.50,
    parental_control_gap: 0.52, dark_web_exposure: 0.48,
    mental_health_impact: 0.55, reporting_mechanism_gap: 0.50,
    law_enforcement_capacity: 0.48, cross_border_jurisdiction_gap: 0.52,
    digital_literacy_children: 0.45, platform_transparency_failure: 0.50,
    regulatory_enforcement_gap: 0.52,
  },
  // CSE-005 — high, platform_moderation_failure (transp>0.80, reporting>0.75)
  {
    id: "CSE-005", platform_type: "forum_communautaire", region: "SSA",
    predator_network_density: 0.48, grooming_incident_rate: 0.45,
    csam_detection_gap: 0.50, algorithmic_harm_amplification: 0.48,
    screen_addiction_severity: 0.45, cyberbullying_prevalence: 0.50,
    sextortion_risk_index: 0.48, age_verification_failure: 0.52,
    parental_control_gap: 0.48, dark_web_exposure: 0.45,
    mental_health_impact: 0.50, reporting_mechanism_gap: 0.78,
    law_enforcement_capacity: 0.50, cross_border_jurisdiction_gap: 0.48,
    digital_literacy_children: 0.42, platform_transparency_failure: 0.82,
    regulatory_enforcement_gap: 0.50,
  },
  // CSE-006 — moderate, none
  {
    id: "CSE-006", platform_type: "application_éducative", region: "EMEA",
    predator_network_density: 0.28, grooming_incident_rate: 0.25,
    csam_detection_gap: 0.28, algorithmic_harm_amplification: 0.30,
    screen_addiction_severity: 0.28, cyberbullying_prevalence: 0.30,
    sextortion_risk_index: 0.25, age_verification_failure: 0.28,
    parental_control_gap: 0.30, dark_web_exposure: 0.25,
    mental_health_impact: 0.28, reporting_mechanism_gap: 0.30,
    law_enforcement_capacity: 0.28, cross_border_jurisdiction_gap: 0.30,
    digital_literacy_children: 0.72, platform_transparency_failure: 0.28,
    regulatory_enforcement_gap: 0.28,
  },
  // CSE-007 — low, none
  {
    id: "CSE-007", platform_type: "portail_parental", region: "NOAM",
    predator_network_density: 0.10, grooming_incident_rate: 0.08,
    csam_detection_gap: 0.10, algorithmic_harm_amplification: 0.10,
    screen_addiction_severity: 0.08, cyberbullying_prevalence: 0.10,
    sextortion_risk_index: 0.08, age_verification_failure: 0.10,
    parental_control_gap: 0.08, dark_web_exposure: 0.10,
    mental_health_impact: 0.08, reporting_mechanism_gap: 0.10,
    law_enforcement_capacity: 0.12, cross_border_jurisdiction_gap: 0.10,
    digital_literacy_children: 0.90, platform_transparency_failure: 0.10,
    regulatory_enforcement_gap: 0.10,
  },
  // CSE-008 — low, none
  {
    id: "CSE-008", platform_type: "service_streaming_famille", region: "APAC",
    predator_network_density: 0.12, grooming_incident_rate: 0.10,
    csam_detection_gap: 0.12, algorithmic_harm_amplification: 0.10,
    screen_addiction_severity: 0.12, cyberbullying_prevalence: 0.10,
    sextortion_risk_index: 0.10, age_verification_failure: 0.12,
    parental_control_gap: 0.10, dark_web_exposure: 0.12,
    mental_health_impact: 0.10, reporting_mechanism_gap: 0.12,
    law_enforcement_capacity: 0.10, cross_border_jurisdiction_gap: 0.12,
    digital_literacy_children: 0.88, platform_transparency_failure: 0.10,
    regulatory_enforcement_gap: 0.12,
  },
];

type CSEInput = typeof MOCK_ENTITIES[0];

function predationScore(e: CSEInput): number {
  return Math.round((e.predator_network_density * 0.4 + e.grooming_incident_rate * 0.35 + e.sextortion_risk_index * 0.25) * 100 * 100) / 100;
}
function contentScore(e: CSEInput): number {
  return Math.round((e.csam_detection_gap * 0.4 + e.dark_web_exposure * 0.35 + e.algorithmic_harm_amplification * 0.25) * 100 * 100) / 100;
}
function platformScore(e: CSEInput): number {
  return Math.round((e.age_verification_failure * 0.4 + e.platform_transparency_failure * 0.35 + e.parental_control_gap * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: CSEInput): number {
  return Math.round((e.regulatory_enforcement_gap * 0.4 + e.cross_border_jurisdiction_gap * 0.35 + e.law_enforcement_capacity * 0.25) * 100 * 100) / 100;
}
function compositeScore(pred: number, cont: number, plat: number, gov: number): number {
  return Math.round((pred * 0.30 + cont * 0.25 + plat * 0.25 + gov * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function safetyPattern(e: CSEInput): string {
  if (e.predator_network_density > 0.85 && e.grooming_incident_rate > 0.80) return "grooming_network_proliferation";
  if (e.csam_detection_gap > 0.85 && e.dark_web_exposure > 0.80) return "csam_distribution_infrastructure";
  if (e.algorithmic_harm_amplification > 0.85 && e.screen_addiction_severity > 0.80) return "algorithmic_radicalization_youth";
  if (e.sextortion_risk_index > 0.80 && e.cyberbullying_prevalence > 0.75) return "sextortion_epidemic";
  if (e.platform_transparency_failure > 0.80 && e.reporting_mechanism_gap > 0.75) return "platform_moderation_failure";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_protection_enfants_systémique";
  if (composite >= 40) return "crise_sécurité_numérique_majeure";
  if (composite >= 20) return "vulnérabilité_numérique_structurelle";
  return "surveillance_sécurité_enfants_active";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_protection_enfants_critique";
  if (risk === "high") return "renforcement_immédiat_modération_plateforme";
  if (risk === "moderate") return "amélioration_mécanismes_signalement_enfants";
  return "veille_sécurité_numérique_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise protection enfants systémique — intervention d'urgence requise";
  if (risk === "high") return "🟠 Crise sécurité numérique majeure détectée";
  if (risk === "moderate") return "🟡 Vulnérabilité numérique structurelle active";
  return "🟢 Sécurité enfants numérique sous surveillance";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[child-online-safety-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tPred = 0, tCont = 0, tPlat = 0, tGov = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.safety_pattern]    = (pattern_distribution[ent.safety_pattern]    || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tPred += ent.predation_score;
      tCont += ent.content_score;
      tPlat += ent.platform_score;
      tGov  += ent.governance_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;
    const avgPredation = Math.round(tPred / n * 10) / 10;

    const summary = {
      module_id:                                  436,
      module_name:                                "Sécurité Enfants Numérique & Préjudices en Ligne Intelligence Engine",
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
      avg_estimated_child_digital_safety_index:   Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary, avg_predation: avgPredation }, "child-online-safety-engine")
    ));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/child-online-safety-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return sealResponse(NextResponse.json(sealResponse(await upstream.json(), "child-online-safety-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "child-online-safety-engine"),
      { status: 502 }
    ));
  }
}
