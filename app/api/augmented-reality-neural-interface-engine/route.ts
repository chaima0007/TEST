import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// ── Mock AR/XR Neural Interface Data ──────────────────────────────────────────
// Each interface has 17 numeric fields (0.0–1.0).
// Fields: neural_latency_risk, spatial_accuracy_score, cognitive_immersion_depth,
//         biometric_privacy_exposure, neural_signal_integrity, sensory_coherence_score,
//         eye_tracking_precision, haptic_fidelity_score, reality_anchoring_stability,
//         motion_sickness_risk, neural_fatigue_accumulation, bci_safety_compliance,
//         data_sovereignty_of_neural_data, immersive_addiction_risk,
//         cross_platform_interoperability, environmental_mapping_accuracy,
//         neural_adaptation_speed

const MOCK_INTERFACES = [
  // ARNI-001: brain_computer_interface, EMEA → critical, neural_overload
  {
    interface_id: "ARNI-001", interface_type: "brain_computer_interface", region: "EMEA",
    neural_latency_risk: 0.88, spatial_accuracy_score: 0.22, cognitive_immersion_depth: 0.35,
    biometric_privacy_exposure: 0.80, neural_signal_integrity: 0.20, sensory_coherence_score: 0.18,
    eye_tracking_precision: 0.25, haptic_fidelity_score: 0.22, reality_anchoring_stability: 0.20,
    motion_sickness_risk: 0.78, neural_fatigue_accumulation: 0.82, bci_safety_compliance: 0.15,
    data_sovereignty_of_neural_data: 0.85, immersive_addiction_risk: 0.72, cross_platform_interoperability: 0.18,
    environmental_mapping_accuracy: 0.20, neural_adaptation_speed: 0.18,
  },
  // ARNI-002: spatial_computing, NAMER → low, immersive
  {
    interface_id: "ARNI-002", interface_type: "spatial_computing", region: "NAMER",
    neural_latency_risk: 0.08, spatial_accuracy_score: 0.92, cognitive_immersion_depth: 0.90,
    biometric_privacy_exposure: 0.10, neural_signal_integrity: 0.95, sensory_coherence_score: 0.92,
    eye_tracking_precision: 0.90, haptic_fidelity_score: 0.88, reality_anchoring_stability: 0.94,
    motion_sickness_risk: 0.05, neural_fatigue_accumulation: 0.08, bci_safety_compliance: 0.96,
    data_sovereignty_of_neural_data: 0.08, immersive_addiction_risk: 0.10, cross_platform_interoperability: 0.90,
    environmental_mapping_accuracy: 0.92, neural_adaptation_speed: 0.88,
  },
  // ARNI-003: holographic_overlay, APAC → high, reality_dissociation
  {
    interface_id: "ARNI-003", interface_type: "holographic_overlay", region: "APAC",
    neural_latency_risk: 0.55, spatial_accuracy_score: 0.48, cognitive_immersion_depth: 0.52,
    biometric_privacy_exposure: 0.52, neural_signal_integrity: 0.50, sensory_coherence_score: 0.20,
    eye_tracking_precision: 0.45, haptic_fidelity_score: 0.42, reality_anchoring_stability: 0.18,
    motion_sickness_risk: 0.62, neural_fatigue_accumulation: 0.58, bci_safety_compliance: 0.50,
    data_sovereignty_of_neural_data: 0.58, immersive_addiction_risk: 0.55, cross_platform_interoperability: 0.42,
    environmental_mapping_accuracy: 0.38, neural_adaptation_speed: 0.40,
  },
  // ARNI-004: haptic_neural, LATAM → low, calibrating
  {
    interface_id: "ARNI-004", interface_type: "haptic_neural", region: "LATAM",
    neural_latency_risk: 0.15, spatial_accuracy_score: 0.80, cognitive_immersion_depth: 0.78,
    biometric_privacy_exposure: 0.18, neural_signal_integrity: 0.82, sensory_coherence_score: 0.80,
    eye_tracking_precision: 0.75, haptic_fidelity_score: 0.85, reality_anchoring_stability: 0.78,
    motion_sickness_risk: 0.12, neural_fatigue_accumulation: 0.18, bci_safety_compliance: 0.85,
    data_sovereignty_of_neural_data: 0.15, immersive_addiction_risk: 0.20, cross_platform_interoperability: 0.78,
    environmental_mapping_accuracy: 0.80, neural_adaptation_speed: 0.75,
  },
  // ARNI-005: retinal_projection, EMEA → critical, biometric_breach
  {
    interface_id: "ARNI-005", interface_type: "retinal_projection", region: "EMEA",
    neural_latency_risk: 0.72, spatial_accuracy_score: 0.28, cognitive_immersion_depth: 0.30,
    biometric_privacy_exposure: 0.90, neural_signal_integrity: 0.28, sensory_coherence_score: 0.32,
    eye_tracking_precision: 0.22, haptic_fidelity_score: 0.28, reality_anchoring_stability: 0.30,
    motion_sickness_risk: 0.70, neural_fatigue_accumulation: 0.75, bci_safety_compliance: 0.20,
    data_sovereignty_of_neural_data: 0.88, immersive_addiction_risk: 0.68, cross_platform_interoperability: 0.22,
    environmental_mapping_accuracy: 0.25, neural_adaptation_speed: 0.20,
  },
  // ARNI-006: mixed_reality_mesh, NAMER → moderate, none
  {
    interface_id: "ARNI-006", interface_type: "mixed_reality_mesh", region: "NAMER",
    neural_latency_risk: 0.35, spatial_accuracy_score: 0.62, cognitive_immersion_depth: 0.65,
    biometric_privacy_exposure: 0.38, neural_signal_integrity: 0.60, sensory_coherence_score: 0.62,
    eye_tracking_precision: 0.58, haptic_fidelity_score: 0.60, reality_anchoring_stability: 0.62,
    motion_sickness_risk: 0.32, neural_fatigue_accumulation: 0.38, bci_safety_compliance: 0.65,
    data_sovereignty_of_neural_data: 0.35, immersive_addiction_risk: 0.38, cross_platform_interoperability: 0.60,
    environmental_mapping_accuracy: 0.62, neural_adaptation_speed: 0.58,
  },
  // ARNI-007: neural_feedback_loop, APAC → high, bci_failure
  {
    interface_id: "ARNI-007", interface_type: "neural_feedback_loop", region: "APAC",
    neural_latency_risk: 0.62, spatial_accuracy_score: 0.38, cognitive_immersion_depth: 0.42,
    biometric_privacy_exposure: 0.60, neural_signal_integrity: 0.20, sensory_coherence_score: 0.42,
    eye_tracking_precision: 0.35, haptic_fidelity_score: 0.38, reality_anchoring_stability: 0.40,
    motion_sickness_risk: 0.58, neural_fatigue_accumulation: 0.62, bci_safety_compliance: 0.18,
    data_sovereignty_of_neural_data: 0.65, immersive_addiction_risk: 0.58, cross_platform_interoperability: 0.32,
    environmental_mapping_accuracy: 0.35, neural_adaptation_speed: 0.30,
  },
  // ARNI-008: embodied_ai_avatar, MEA → critical, sensory_collapse
  {
    interface_id: "ARNI-008", interface_type: "embodied_ai_avatar", region: "MEA",
    neural_latency_risk: 0.80, spatial_accuracy_score: 0.18, cognitive_immersion_depth: 0.22,
    biometric_privacy_exposure: 0.78, neural_signal_integrity: 0.22, sensory_coherence_score: 0.28,
    eye_tracking_precision: 0.20, haptic_fidelity_score: 0.25, reality_anchoring_stability: 0.22,
    motion_sickness_risk: 0.82, neural_fatigue_accumulation: 0.78, bci_safety_compliance: 0.18,
    data_sovereignty_of_neural_data: 0.82, immersive_addiction_risk: 0.75, cross_platform_interoperability: 0.15,
    environmental_mapping_accuracy: 0.18, neural_adaptation_speed: 0.15,
  },
];

type ARInterface = typeof MOCK_INTERFACES[0];

// ── Sub-score helpers ──────────────────────────────────────────────────────────

function neuralRiskScore(i: ARInterface): number {
  return (
    i.neural_latency_risk * 0.333
    + i.neural_fatigue_accumulation * 0.333
    + (1.0 - i.bci_safety_compliance) * 0.334
  );
}

function immersionScore(i: ARInterface): number {
  return (
    (1.0 - i.cognitive_immersion_depth) * 0.333
    + (1.0 - i.sensory_coherence_score) * 0.333
    + (1.0 - i.reality_anchoring_stability) * 0.334
  );
}

function safetyScore(i: ARInterface): number {
  return (
    i.biometric_privacy_exposure * 0.333
    + i.motion_sickness_risk * 0.333
    + i.immersive_addiction_risk * 0.334
  );
}

function integrityScore(i: ARInterface): number {
  return (
    (1.0 - i.neural_signal_integrity) * 0.333
    + i.data_sovereignty_of_neural_data * 0.333
    + (1.0 - i.spatial_accuracy_score) * 0.334
  );
}

function composite(nr: number, im: number, sa: number, ig: number): number {
  return Math.min(
    Math.round((nr * 0.30 + im * 0.25 + sa * 0.25 + ig * 0.20) * 10000) / 10000,
    1.0,
  );
}

function neuralPattern(i: ARInterface): string {
  if (i.neural_latency_risk >= 0.75 && i.neural_fatigue_accumulation >= 0.70) return "neural_overload";
  if (i.reality_anchoring_stability <= 0.25 || i.sensory_coherence_score <= 0.25) return "reality_dissociation";
  if (i.biometric_privacy_exposure >= 0.75 || i.data_sovereignty_of_neural_data >= 0.75) return "biometric_breach";
  if (i.bci_safety_compliance <= 0.25 || i.neural_signal_integrity <= 0.25) return "bci_failure";
  if (i.sensory_coherence_score <= 0.35 && i.haptic_fidelity_score <= 0.35) return "sensory_collapse";
  return "none";
}

function riskLevel(comp: number): string {
  if (comp >= 0.60) return "critical";
  if (comp >= 0.40) return "high";
  if (comp >= 0.20) return "moderate";
  return "low";
}

function severity(comp: number): string {
  if (comp >= 0.60) return "critical_neural";
  if (comp >= 0.40) return "unstable";
  if (comp >= 0.20) return "calibrating";
  return "immersive";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") {
    if (pattern === "neural_overload" || pattern === "bci_failure") return "neural_emergency_disconnect";
    return "bci_safety_lockdown";
  }
  if (risk === "high") {
    if (pattern === "reality_dissociation" || pattern === "sensory_collapse") return "immersion_recalibration";
    return "privacy_shield";
  }
  if (risk === "moderate") return "neural_monitoring";
  return "no_action";
}

function neuralSignal(i: ARInterface, pattern: string, comp: number): string {
  const latencyMs = Math.round(i.neural_latency_risk * 500 * 10) / 10;
  const immersionPct = Math.round(i.cognitive_immersion_depth * 100 * 10) / 10;
  const integrityPct = Math.round(i.neural_signal_integrity * 100 * 10) / 10;
  if (comp < 0.20) {
    return `Interface neuronale stable — latence ${latencyMs}ms — immersion ${immersionPct}% — intégrité signal ${integrityPct}%`;
  }
  const labels: Record<string, string> = {
    neural_overload:      "Surcharge neuronale",
    reality_dissociation: "Dissociation réalité",
    biometric_breach:     "Violation biométrique",
    bci_failure:          "Défaillance BCI",
    sensory_collapse:     "Effondrement sensoriel",
    none:                 "Aucun pattern critique",
  };
  const label = labels[pattern] ?? pattern.replace(/_/g, " ");
  return `${label} — latence ${latencyMs}ms — immersion ${immersionPct}% — intégrité signal ${integrityPct}% — risque composite ${Math.round(comp * 100 * 10) / 10}%`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const interfaces = MOCK_INTERFACES.map(i => {
      const nr = neuralRiskScore(i);
      const im = immersionScore(i);
      const sa = safetyScore(i);
      const ig = integrityScore(i);
      const comp = composite(nr, im, sa, ig);
      const pattern = neuralPattern(i);
      const risk = riskLevel(comp);
      const sev = severity(comp);
      const act = recommendedAction(risk, pattern);
      return {
        interface_id: i.interface_id,
        interface_type: i.interface_type,
        region: i.region,
        neural_risk: risk,
        neural_pattern: pattern,
        neural_severity: sev,
        recommended_action: act,
        neural_risk_score: Math.round(nr * 100 * 100) / 100,
        immersion_score: Math.round(im * 100 * 100) / 100,
        safety_score: Math.round(sa * 100 * 100) / 100,
        integrity_score: Math.round(ig * 100 * 100) / 100,
        neural_risk_composite: Math.round(comp * 100 * 100) / 100,
        has_critical_signal:
          comp >= 0.40 || i.neural_latency_risk >= 0.70 || i.bci_safety_compliance <= 0.30,
        requires_disconnect:
          comp >= 0.25 || i.neural_fatigue_accumulation >= 0.65 || i.biometric_privacy_exposure >= 0.70,
        estimated_neural_risk_index:
          Math.min(
            Math.round(comp * (1 - i.neural_signal_integrity + 0.01) * 10 * 100) / 100,
            10.0,
          ),
        neural_signal: neuralSignal(i, pattern, comp),
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tNr = 0, tIm = 0, tSa = 0, tIg = 0, tComp = 0, tIdx = 0;
    let critC = 0, discC = 0;

    for (const iface of interfaces) {
      rc[iface.neural_risk] = (rc[iface.neural_risk] || 0) + 1;
      pc[iface.neural_pattern] = (pc[iface.neural_pattern] || 0) + 1;
      sc[iface.neural_severity] = (sc[iface.neural_severity] || 0) + 1;
      ac[iface.recommended_action] = (ac[iface.recommended_action] || 0) + 1;
      tNr += iface.neural_risk_score;
      tIm += iface.immersion_score;
      tSa += iface.safety_score;
      tIg += iface.integrity_score;
      tComp += iface.neural_risk_composite;
      tIdx += iface.estimated_neural_risk_index;
      if (iface.has_critical_signal) critC++;
      if (iface.requires_disconnect) discC++;
    }

    const n = interfaces.length;
    const summary = {
      total: n,
      risk_counts: rc,
      pattern_counts: pc,
      severity_counts: sc,
      action_counts: ac,
      avg_neural_risk_composite: Math.round(tComp / n * 10) / 10,
      critical_signal_count: critC,
      disconnect_required_count: discC,
      avg_neural_risk_score: Math.round(tNr / n * 10) / 10,
      avg_immersion_score: Math.round(tIm / n * 10) / 10,
      avg_safety_score: Math.round(tSa / n * 10) / 10,
      avg_integrity_score: Math.round(tIg / n * 10) / 10,
      avg_estimated_neural_risk_index: Math.round(tIdx / n * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ interfaces, summary }, "augmented-reality-neural-interface-engine") as Parameters<typeof NextResponse.json>[0],
    );
  }

  return NextResponse.json(
    await (await fetch(`${process.env.SWARM_API_URL}/augmented-reality-neural-interface-engine`)).json(),
  );
}
