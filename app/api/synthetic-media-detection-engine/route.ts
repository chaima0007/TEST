import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // SMD-001 — critical, deepfake_epidemic
  { entity_id:"SMD-001", media_domain:"political_media", region:"EMEA",
    deepfake_prevalence:0.80, ai_content_saturation:0.72, detection_capability:0.22,
    authentication_gap:0.75, voice_clone_exposure:0.68, face_swap_sophistication:0.82,
    provenance_verification_rate:0.15, synthetic_identity_fraud_rate:0.55,
    content_authenticity_infrastructure:0.18, adversarial_evolution_speed:0.75,
    forensic_detection_lag:0.70, platform_content_moderation:0.20,
    public_trust_erosion:0.78, legal_framework_readiness:0.22,
    biometric_spoofing_risk:0.80, media_literacy_level:0.20,
    watermarking_adoption:0.15 },
  // SMD-002 — low, authentic_environment / none
  { entity_id:"SMD-002", media_domain:"corporate_comms", region:"APAC",
    deepfake_prevalence:0.10, ai_content_saturation:0.18, detection_capability:0.90,
    authentication_gap:0.12, voice_clone_exposure:0.10, face_swap_sophistication:0.08,
    provenance_verification_rate:0.88, synthetic_identity_fraud_rate:0.10,
    content_authenticity_infrastructure:0.88, adversarial_evolution_speed:0.12,
    forensic_detection_lag:0.10, platform_content_moderation:0.88,
    public_trust_erosion:0.10, legal_framework_readiness:0.90,
    biometric_spoofing_risk:0.08, media_literacy_level:0.88,
    watermarking_adoption:0.85 },
  // SMD-003 — high, identity_fraud_cascade
  { entity_id:"SMD-003", media_domain:"financial_media", region:"NOAM",
    deepfake_prevalence:0.50, ai_content_saturation:0.55, detection_capability:0.48,
    authentication_gap:0.68, voice_clone_exposure:0.60, face_swap_sophistication:0.55,
    provenance_verification_rate:0.38, synthetic_identity_fraud_rate:0.72,
    content_authenticity_infrastructure:0.40, adversarial_evolution_speed:0.50,
    forensic_detection_lag:0.48, platform_content_moderation:0.50,
    public_trust_erosion:0.52, legal_framework_readiness:0.45,
    biometric_spoofing_risk:0.60, media_literacy_level:0.45,
    watermarking_adoption:0.38 },
  // SMD-004 — low, authentic_environment / none
  { entity_id:"SMD-004", media_domain:"corporate_comms", region:"LATAM",
    deepfake_prevalence:0.12, ai_content_saturation:0.20, detection_capability:0.85,
    authentication_gap:0.15, voice_clone_exposure:0.12, face_swap_sophistication:0.10,
    provenance_verification_rate:0.82, synthetic_identity_fraud_rate:0.12,
    content_authenticity_infrastructure:0.82, adversarial_evolution_speed:0.15,
    forensic_detection_lag:0.12, platform_content_moderation:0.85,
    public_trust_erosion:0.12, legal_framework_readiness:0.85,
    biometric_spoofing_risk:0.10, media_literacy_level:0.82,
    watermarking_adoption:0.80 },
  // SMD-005 — critical, trust_collapse
  { entity_id:"SMD-005", media_domain:"political_media", region:"MEA",
    deepfake_prevalence:0.60, ai_content_saturation:0.70, detection_capability:0.30,
    authentication_gap:0.65, voice_clone_exposure:0.72, face_swap_sophistication:0.68,
    provenance_verification_rate:0.20, synthetic_identity_fraud_rate:0.60,
    content_authenticity_infrastructure:0.22, adversarial_evolution_speed:0.65,
    forensic_detection_lag:0.62, platform_content_moderation:0.28,
    public_trust_erosion:0.85, legal_framework_readiness:0.20,
    biometric_spoofing_risk:0.75, media_literacy_level:0.28,
    watermarking_adoption:0.18 },
  // SMD-006 — moderate, none
  { entity_id:"SMD-006", media_domain:"entertainment", region:"EMEA",
    deepfake_prevalence:0.32, ai_content_saturation:0.38, detection_capability:0.62,
    authentication_gap:0.35, voice_clone_exposure:0.30, face_swap_sophistication:0.38,
    provenance_verification_rate:0.55, synthetic_identity_fraud_rate:0.28,
    content_authenticity_infrastructure:0.55, adversarial_evolution_speed:0.35,
    forensic_detection_lag:0.32, platform_content_moderation:0.60,
    public_trust_erosion:0.38, legal_framework_readiness:0.55,
    biometric_spoofing_risk:0.30, media_literacy_level:0.55,
    watermarking_adoption:0.50 },
  // SMD-007 — high, governance_vacuum
  { entity_id:"SMD-007", media_domain:"financial_media", region:"APAC",
    deepfake_prevalence:0.48, ai_content_saturation:0.55, detection_capability:0.42,
    authentication_gap:0.52, voice_clone_exposure:0.48, face_swap_sophistication:0.50,
    provenance_verification_rate:0.40, synthetic_identity_fraud_rate:0.48,
    content_authenticity_infrastructure:0.38, adversarial_evolution_speed:0.55,
    forensic_detection_lag:0.50, platform_content_moderation:0.25,
    public_trust_erosion:0.50, legal_framework_readiness:0.22,
    biometric_spoofing_risk:0.52, media_literacy_level:0.45,
    watermarking_adoption:0.20 },
  // SMD-008 — critical, adversarial_arms_race
  // deepfake_prevalence <0.65 to avoid triggering deepfake_epidemic first;
  // adversarial_evolution_speed>=0.70 and forensic_detection_lag>=0.60 fires arms_race
  { entity_id:"SMD-008", media_domain:"political_media", region:"NOAM",
    deepfake_prevalence:0.55, ai_content_saturation:0.78, detection_capability:0.28,
    authentication_gap:0.58, voice_clone_exposure:0.80, face_swap_sophistication:0.85,
    provenance_verification_rate:0.22, synthetic_identity_fraud_rate:0.50,
    content_authenticity_infrastructure:0.20, adversarial_evolution_speed:0.88,
    forensic_detection_lag:0.78, platform_content_moderation:0.30,
    public_trust_erosion:0.62, legal_framework_readiness:0.32,
    biometric_spoofing_risk:0.82, media_literacy_level:0.35,
    watermarking_adoption:0.22 },
];

type Entity = typeof MOCK_ENTITIES[0];

function detectionScore(e: Entity): number {
  const raw = (1 - e.detection_capability) * 0.4
    + e.forensic_detection_lag * 0.35
    + e.adversarial_evolution_speed * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function authenticityScore(e: Entity): number {
  const raw = e.deepfake_prevalence * 0.4
    + e.authentication_gap * 0.35
    + (1 - e.provenance_verification_rate) * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function trustScore(e: Entity): number {
  const raw = e.public_trust_erosion * 0.4
    + e.synthetic_identity_fraud_rate * 0.35
    + (1 - e.media_literacy_level) * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function governanceScore(e: Entity): number {
  const raw = (1 - e.platform_content_moderation) * 0.4
    + (1 - e.legal_framework_readiness) * 0.35
    + (1 - e.watermarking_adoption) * 0.25;
  return Math.round(raw * 100 * 100) / 100;
}

function composite(det: number, auth: number, trust: number, gov: number): number {
  return Math.round((det * 0.30 + auth * 0.25 + trust * 0.25 + gov * 0.20) * 100) / 100;
}

function syntheticPattern(e: Entity): string {
  if (e.deepfake_prevalence >= 0.65 && (1 - e.detection_capability) >= 0.55) return "deepfake_epidemic";
  if (e.synthetic_identity_fraud_rate >= 0.65 && e.authentication_gap >= 0.55) return "identity_fraud_cascade";
  if (e.public_trust_erosion >= 0.70 && (1 - e.media_literacy_level) >= 0.60) return "trust_collapse";
  if ((1 - e.legal_framework_readiness) >= 0.70 && (1 - e.platform_content_moderation) >= 0.60) return "governance_vacuum";
  if (e.adversarial_evolution_speed >= 0.70 && e.forensic_detection_lag >= 0.60) return "adversarial_arms_race";
  return "none";
}

function syntheticRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function syntheticSeverity(comp: number): string {
  if (comp >= 75) return "synthetic_reality_crisis";
  if (comp >= 50) return "high_synthetic_threat";
  if (comp >= 25) return "developing_threat";
  return "authentic_environment";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "synthetic_media_emergency";
  if (risk === "high" && pattern === "trust_collapse") return "trust_restoration_protocol";
  if (risk === "high") return "detection_infrastructure";
  if (risk === "moderate") return "synthetic_monitoring";
  return "no_action";
}

function syntheticSignal(e: Entity, risk: string, comp: number): string {
  const dpPct  = Math.round(e.deepfake_prevalence * 100);
  const ptPct  = Math.round(e.public_trust_erosion * 100);
  const sifPct = Math.round(e.synthetic_identity_fraud_rate * 100);
  const dcPct  = Math.round(e.detection_capability * 100);
  const acsPct = Math.round(e.ai_content_saturation * 100);
  const compInt = Math.round(comp);
  if (risk === "critical") {
    return `Critique — prévalence deepfakes ${dpPct}% — érosion confiance ${ptPct}% — composite ${compInt}`;
  }
  if (risk === "high") {
    return `Élevé — fraude identité synthétique ${sifPct}% — capacité détection ${dcPct}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `Modéré — saturation contenu IA ${acsPct}% — composite ${compInt}`;
  }
  return "Environnement média authentique — détection robuste, confiance publique maintenue";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const det  = detectionScore(e);
      const auth = authenticityScore(e);
      const trust = trustScore(e);
      const gov  = governanceScore(e);
      const comp = composite(det, auth, trust, gov);
      const pat  = syntheticPattern(e);
      const risk = syntheticRisk(comp);
      const sev  = syntheticSeverity(comp);
      const act  = recommendedAction(risk, pat);
      return {
        entity_id:                        e.entity_id,
        region:                           e.region,
        media_domain:                     e.media_domain,
        synthetic_risk:                   risk,
        synthetic_pattern:                pat,
        synthetic_severity:               sev,
        recommended_action:               act,
        detection_score:                  det,
        authenticity_score:               auth,
        trust_score:                      trust,
        governance_score:                 gov,
        synthetic_composite:              comp,
        is_in_synthetic_crisis:           comp >= 60,
        requires_synthetic_intervention:  comp >= 40,
        synthetic_signal:                 syntheticSignal(e, risk, comp),
      };
    });

    const rc: Record<string,number> = {};
    const pc: Record<string,number> = {};
    const sc: Record<string,number> = {};
    const ac: Record<string,number> = {};
    let tDet=0, tAuth=0, tTrust=0, tGov=0, tComp=0, crisisC=0, interventionC=0;

    for (const ent of entities) {
      rc[ent.synthetic_risk]      = (rc[ent.synthetic_risk]      || 0) + 1;
      pc[ent.synthetic_pattern]   = (pc[ent.synthetic_pattern]   || 0) + 1;
      sc[ent.synthetic_severity]  = (sc[ent.synthetic_severity]  || 0) + 1;
      ac[ent.recommended_action]  = (ac[ent.recommended_action]  || 0) + 1;
      tDet   += ent.detection_score;
      tAuth  += ent.authenticity_score;
      tTrust += ent.trust_score;
      tGov   += ent.governance_score;
      tComp  += ent.synthetic_composite;
      if (ent.is_in_synthetic_crisis)          crisisC++;
      if (ent.requires_synthetic_intervention) interventionC++;
    }

    const n = entities.length;
    const avgComp = tComp / n;
    const summary = {
      total:                                  n,
      risk_counts:                            rc,
      pattern_counts:                         pc,
      severity_counts:                        sc,
      action_counts:                          ac,
      avg_synthetic_composite:                Math.round(avgComp * 10) / 10,
      synthetic_crisis_count:                 crisisC,
      synthetic_intervention_count:           interventionC,
      avg_detection_score:                    Math.round(tDet   / n * 10) / 10,
      avg_authenticity_score:                 Math.round(tAuth  / n * 10) / 10,
      avg_trust_score:                        Math.round(tTrust / n * 10) / 10,
      avg_governance_score:                   Math.round(tGov   / n * 10) / 10,
      avg_estimated_synthetic_threat_index:   Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary }, "synthetic-media-detection-engine")
    );
  }

  try {
    const upstream = await fetch(
      `${process.env.SWARM_API_URL}/synthetic-media-detection-engine`
    );
    const payload = await upstream.json();
    return NextResponse.json(
      sealResponse(payload, "synthetic-media-detection-engine")
    );
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream swarm unavailable" }, "synthetic-media-detection-engine"),
      { status: 502 }
    );
  }
}
