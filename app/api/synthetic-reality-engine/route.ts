import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // SRE-001 — EMEA, digital_media → critical, reality_consensus_collapse
  // reality_consensus_erosion>0.85 AND reality_verification_collapse>0.80
  {
    entity_id: "SRE-001", media_domain: "digital_media", region: "EMEA",
    deepfake_saturation_level: 0.82,
    reality_consensus_erosion: 0.88,
    political_deepfake_weaponization: 0.60,
    financial_fraud_deepfake: 0.55,
    identity_theft_synthetic: 0.60,
    consent_violation_synthetic_media: 0.78,
    detection_technology_gap: 0.70,
    celebrity_non_consent: 0.72,
    synthetic_evidence_falsification: 0.55,
    emotional_manipulation_capacity: 0.70,
    reality_verification_collapse: 0.85,
    AI_media_monopoly: 0.60,
    deepfake_criminalization_failure: 0.60,
    synthetic_pornography_harm: 0.70,
    geopolitical_deepfake_incidents: 0.55,
    economic_deepfake_fraud_scale: 0.50,
    social_trust_erosion: 0.80,
  },
  // SRE-002 — APAC, community_tv → low, none
  // composite < 20 → low; no pattern triggers
  {
    entity_id: "SRE-002", media_domain: "community_tv", region: "APAC",
    deepfake_saturation_level: 0.08,
    reality_consensus_erosion: 0.10,
    political_deepfake_weaponization: 0.08,
    financial_fraud_deepfake: 0.10,
    identity_theft_synthetic: 0.08,
    consent_violation_synthetic_media: 0.10,
    detection_technology_gap: 0.10,
    celebrity_non_consent: 0.08,
    synthetic_evidence_falsification: 0.08,
    emotional_manipulation_capacity: 0.10,
    reality_verification_collapse: 0.08,
    AI_media_monopoly: 0.10,
    deepfake_criminalization_failure: 0.08,
    synthetic_pornography_harm: 0.08,
    geopolitical_deepfake_incidents: 0.08,
    economic_deepfake_fraud_scale: 0.10,
    social_trust_erosion: 0.10,
  },
  // SRE-003 — MEA, state_media → critical, political_deepfake_crisis
  // political_deepfake_weaponization>0.85 AND geopolitical_deepfake_incidents>0.80
  // reality_consensus_erosion<=0.85 to prevent pattern 1 firing
  {
    entity_id: "SRE-003", media_domain: "state_media", region: "MEA",
    deepfake_saturation_level: 0.75,
    reality_consensus_erosion: 0.70,
    political_deepfake_weaponization: 0.88,
    financial_fraud_deepfake: 0.55,
    identity_theft_synthetic: 0.60,
    consent_violation_synthetic_media: 0.70,
    detection_technology_gap: 0.65,
    celebrity_non_consent: 0.68,
    synthetic_evidence_falsification: 0.60,
    emotional_manipulation_capacity: 0.75,
    reality_verification_collapse: 0.65,
    AI_media_monopoly: 0.60,
    deepfake_criminalization_failure: 0.60,
    synthetic_pornography_harm: 0.65,
    geopolitical_deepfake_incidents: 0.85,
    economic_deepfake_fraud_scale: 0.50,
    social_trust_erosion: 0.75,
  },
  // SRE-004 — NOAM, financial_media → critical, synthetic_fraud_epidemic
  // financial_fraud_deepfake>0.85 AND economic_deepfake_fraud_scale>0.80
  // patterns 1-2 must NOT fire
  {
    entity_id: "SRE-004", media_domain: "financial_media", region: "NOAM",
    deepfake_saturation_level: 0.70,
    reality_consensus_erosion: 0.65,
    political_deepfake_weaponization: 0.60,
    financial_fraud_deepfake: 0.88,
    identity_theft_synthetic: 0.78,
    consent_violation_synthetic_media: 0.65,
    detection_technology_gap: 0.70,
    celebrity_non_consent: 0.60,
    synthetic_evidence_falsification: 0.60,
    emotional_manipulation_capacity: 0.70,
    reality_verification_collapse: 0.65,
    AI_media_monopoly: 0.65,
    deepfake_criminalization_failure: 0.60,
    synthetic_pornography_harm: 0.65,
    geopolitical_deepfake_incidents: 0.50,
    economic_deepfake_fraud_scale: 0.85,
    social_trust_erosion: 0.72,
  },
  // SRE-005 — LATAM, legal_media → high, synthetic_evidence_crisis
  // synthetic_evidence_falsification>0.80 AND deepfake_criminalization_failure>0.75
  // patterns 1-3 must NOT fire; composite 40-59
  {
    entity_id: "SRE-005", media_domain: "legal_media", region: "LATAM",
    deepfake_saturation_level: 0.52,
    reality_consensus_erosion: 0.55,
    political_deepfake_weaponization: 0.50,
    financial_fraud_deepfake: 0.55,
    identity_theft_synthetic: 0.55,
    consent_violation_synthetic_media: 0.50,
    detection_technology_gap: 0.65,
    celebrity_non_consent: 0.48,
    synthetic_evidence_falsification: 0.82,
    emotional_manipulation_capacity: 0.55,
    reality_verification_collapse: 0.55,
    AI_media_monopoly: 0.60,
    deepfake_criminalization_failure: 0.78,
    synthetic_pornography_harm: 0.52,
    geopolitical_deepfake_incidents: 0.45,
    economic_deepfake_fraud_scale: 0.48,
    social_trust_erosion: 0.55,
  },
  // SRE-006 — EMEA, broadcast_media → moderate, none
  // composite 20-39; no pattern triggers
  {
    entity_id: "SRE-006", media_domain: "broadcast_media", region: "EMEA",
    deepfake_saturation_level: 0.28,
    reality_consensus_erosion: 0.30,
    political_deepfake_weaponization: 0.28,
    financial_fraud_deepfake: 0.30,
    identity_theft_synthetic: 0.28,
    consent_violation_synthetic_media: 0.30,
    detection_technology_gap: 0.30,
    celebrity_non_consent: 0.28,
    synthetic_evidence_falsification: 0.28,
    emotional_manipulation_capacity: 0.30,
    reality_verification_collapse: 0.28,
    AI_media_monopoly: 0.30,
    deepfake_criminalization_failure: 0.28,
    synthetic_pornography_harm: 0.28,
    geopolitical_deepfake_incidents: 0.28,
    economic_deepfake_fraud_scale: 0.30,
    social_trust_erosion: 0.30,
  },
  // SRE-007 — APAC, tech_platform → high, AI_media_monopoly_capture
  // AI_media_monopoly>0.80 AND detection_technology_gap>0.75
  // patterns 1-4 must NOT fire; composite 40-59
  {
    entity_id: "SRE-007", media_domain: "tech_platform", region: "APAC",
    deepfake_saturation_level: 0.60,
    reality_consensus_erosion: 0.55,
    political_deepfake_weaponization: 0.50,
    financial_fraud_deepfake: 0.50,
    identity_theft_synthetic: 0.55,
    consent_violation_synthetic_media: 0.58,
    detection_technology_gap: 0.80,
    celebrity_non_consent: 0.55,
    synthetic_evidence_falsification: 0.60,
    emotional_manipulation_capacity: 0.60,
    reality_verification_collapse: 0.55,
    AI_media_monopoly: 0.85,
    deepfake_criminalization_failure: 0.55,
    synthetic_pornography_harm: 0.55,
    geopolitical_deepfake_incidents: 0.45,
    economic_deepfake_fraud_scale: 0.48,
    social_trust_erosion: 0.58,
  },
  // SRE-008 — NOAM, print_media → low, none
  // composite < 20 → low; no pattern triggers
  {
    entity_id: "SRE-008", media_domain: "print_media", region: "NOAM",
    deepfake_saturation_level: 0.10,
    reality_consensus_erosion: 0.12,
    political_deepfake_weaponization: 0.10,
    financial_fraud_deepfake: 0.12,
    identity_theft_synthetic: 0.10,
    consent_violation_synthetic_media: 0.10,
    detection_technology_gap: 0.12,
    celebrity_non_consent: 0.10,
    synthetic_evidence_falsification: 0.10,
    emotional_manipulation_capacity: 0.12,
    reality_verification_collapse: 0.10,
    AI_media_monopoly: 0.12,
    deepfake_criminalization_failure: 0.10,
    synthetic_pornography_harm: 0.10,
    geopolitical_deepfake_incidents: 0.10,
    economic_deepfake_fraud_scale: 0.12,
    social_trust_erosion: 0.12,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function saturationScore(e: Entity): number {
  const raw = (
    e.deepfake_saturation_level * 0.40 +
    e.consent_violation_synthetic_media * 0.35 +
    e.celebrity_non_consent * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function trustScore(e: Entity): number {
  const raw = (
    e.social_trust_erosion * 0.40 +
    e.reality_consensus_erosion * 0.35 +
    e.reality_verification_collapse * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function fraudScore(e: Entity): number {
  const raw = (
    e.financial_fraud_deepfake * 0.40 +
    e.identity_theft_synthetic * 0.35 +
    e.economic_deepfake_fraud_scale * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function weaponizationScore(e: Entity): number {
  const raw = (
    e.political_deepfake_weaponization * 0.40 +
    e.geopolitical_deepfake_incidents * 0.35 +
    e.synthetic_evidence_falsification * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(sat: number, trust: number, fraud: number, weap: number): number {
  return Math.round((sat * 0.30 + trust * 0.25 + fraud * 0.25 + weap * 0.20) * 100) / 100;
}

function syntheticPattern(e: Entity): string {
  if (e.reality_consensus_erosion > 0.85 && e.reality_verification_collapse > 0.80)
    return "reality_consensus_collapse";
  if (e.political_deepfake_weaponization > 0.85 && e.geopolitical_deepfake_incidents > 0.80)
    return "political_deepfake_crisis";
  if (e.financial_fraud_deepfake > 0.85 && e.economic_deepfake_fraud_scale > 0.80)
    return "synthetic_fraud_epidemic";
  if (e.synthetic_evidence_falsification > 0.80 && e.deepfake_criminalization_failure > 0.75)
    return "synthetic_evidence_crisis";
  if (e.AI_media_monopoly > 0.80 && e.detection_technology_gap > 0.75)
    return "AI_media_monopoly_capture";
  return "none";
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function severity(comp: number): string {
  if (comp >= 60) return "effondrement_réalité_systémique";
  if (comp >= 40) return "crise_deepfake_majeure";
  if (comp >= 20) return "économie_synthétique_active";
  return "réalité_synthétique_contenue";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_réalité_urgente";
  if (risk === "high") return "contre-mesures_deepfake_activées";
  if (risk === "moderate") return "renforcement_détection_synthétique";
  return "veille_réalité_synthétique_continue";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Effondrement réalité systémique — deepfake critique";
  if (risk === "high") return "🟠 Crise deepfake majeure détectée";
  if (risk === "moderate") return "🟡 Économie synthétique active";
  return "🟢 Réalité synthétique relativement contenue";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const sat  = saturationScore(e);
      const trus = trustScore(e);
      const frau = fraudScore(e);
      const weap = weaponizationScore(e);
      const comp = compositeScore(sat, trus, frau, weap);
      const pat  = syntheticPattern(e);
      const risk = riskLevel(comp);
      const sev  = severity(comp);
      const act  = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        entity_id:                        e.entity_id,
        media_domain:                     e.media_domain,
        region:                           e.region,
        saturation_score:                 sat,
        trust_score:                      trus,
        fraud_score:                      frau,
        weaponization_score:              weap,
        composite_score:                  comp,
        risk_level:                       risk,
        synthetic_pattern:                pat,
        severity:                         sev,
        recommended_action:               act,
        signal:                           sig,
        deepfake_saturation_level:        e.deepfake_saturation_level,
        social_trust_erosion:             e.social_trust_erosion,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      rc[ent.risk_level]          = (rc[ent.risk_level]          || 0) + 1;
      pc[ent.synthetic_pattern]   = (pc[ent.synthetic_pattern]   || 0) + 1;
      sc[ent.severity]            = (sc[ent.severity]            || 0) + 1;
      ac[ent.recommended_action]  = (ac[ent.recommended_action]  || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 10) / 10;
    const summary = {
      module_id:                              378,
      module_name:                            "Synthetic Reality & Deepfake Economy Intelligence Engine",
      total:                                  n,
      critical:                               criticalCount,
      high:                                   highCount,
      moderate:                               moderateCount,
      low:                                    lowCount,
      avg_composite:                          avgComp,
      risk_distribution:                      rc,
      pattern_distribution:                   pc,
      severity_distribution:                  sc,
      action_distribution:                    ac,
      avg_estimated_synthetic_reality_index:  Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "synthetic-reality-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/synthetic-reality-engine`);
    const data = await upstream.json();
    return NextResponse.json(sealResponse(data, "synthetic-reality-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream synthetic reality engine unavailable" }, "synthetic-reality-engine"),
      { status: 502 }
    );
  }
}
