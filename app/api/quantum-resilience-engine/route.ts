import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[quantum-resilience-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── Mock entities ──────────────────────────────────────────────────────────────
// 8 entities covering all patterns and risk levels as specified in Module 280.

const MOCK_ENTITIES = [
  // QR-001 — EMEA, quantum_core → critical, quantum_decoherence
  // decoherence_risk≥0.65, (1-quantum_coherence)≥0.50 → quantum_decoherence
  // Need composite≥60 → critical
  {
    id: "QR-001", region: "EMEA", defense_layer: "quantum_core",
    quantum_coherence: 0.10, adaptive_capacity: 0.30, threat_neutralization: 0.30,
    system_redundancy: 0.30, attack_surface_reduction: 0.30, recovery_velocity: 0.30,
    cross_layer_synchrony: 0.30, anomaly_detection: 0.30, self_healing_rate: 0.30,
    defensive_posture: 0.30, resilience_depth: 0.30, entropy_management: 0.30,
    cascade_prevention: 0.30, adaptive_immunity: 0.30, quantum_entanglement_index: 0.30,
    decoherence_risk: 0.88, vulnerability_exposure: 0.82,
  },
  // QR-002 — APAC, perimeter → low, resilient/none
  // All good values → composite<20
  {
    id: "QR-002", region: "APAC", defense_layer: "perimeter",
    quantum_coherence: 0.92, adaptive_capacity: 0.90, threat_neutralization: 0.92,
    system_redundancy: 0.90, attack_surface_reduction: 0.92, recovery_velocity: 0.90,
    cross_layer_synchrony: 0.92, anomaly_detection: 0.90, self_healing_rate: 0.92,
    defensive_posture: 0.90, resilience_depth: 0.92, entropy_management: 0.90,
    cascade_prevention: 0.92, adaptive_immunity: 0.90, quantum_entanglement_index: 0.92,
    decoherence_risk: 0.08, vulnerability_exposure: 0.08,
  },
  // QR-003 — NOAM, adaptive_mesh → high, adaptive_failure
  // (1-adaptive_capacity)≥0.60 and (1-self_healing_rate)≥0.55 → adaptive_failure
  // composite in [40,60) → high
  {
    id: "QR-003", region: "NOAM", defense_layer: "adaptive_mesh",
    quantum_coherence: 0.65, adaptive_capacity: 0.30, threat_neutralization: 0.60,
    system_redundancy: 0.60, attack_surface_reduction: 0.60, recovery_velocity: 0.60,
    cross_layer_synchrony: 0.65, anomaly_detection: 0.60, self_healing_rate: 0.35,
    defensive_posture: 0.60, resilience_depth: 0.60, entropy_management: 0.65,
    cascade_prevention: 0.65, adaptive_immunity: 0.58, quantum_entanglement_index: 0.60,
    decoherence_risk: 0.30, vulnerability_exposure: 0.35,
  },
  // QR-004 — LATAM, perimeter → low, resilient/none
  {
    id: "QR-004", region: "LATAM", defense_layer: "perimeter",
    quantum_coherence: 0.88, adaptive_capacity: 0.85, threat_neutralization: 0.88,
    system_redundancy: 0.85, attack_surface_reduction: 0.88, recovery_velocity: 0.85,
    cross_layer_synchrony: 0.88, anomaly_detection: 0.85, self_healing_rate: 0.88,
    defensive_posture: 0.85, resilience_depth: 0.88, entropy_management: 0.85,
    cascade_prevention: 0.88, adaptive_immunity: 0.85, quantum_entanglement_index: 0.88,
    decoherence_risk: 0.10, vulnerability_exposure: 0.10,
  },
  // QR-005 — MEA, quantum_core → critical, cascade_collapse
  // (1-cascade_prevention)≥0.65 and (1-cross_layer_synchrony)≥0.55 → cascade_collapse
  // But decoherence_risk<0.65 to avoid quantum_decoherence taking priority
  // composite≥60 → critical
  {
    id: "QR-005", region: "MEA", defense_layer: "quantum_core",
    quantum_coherence: 0.20, adaptive_capacity: 0.25, threat_neutralization: 0.25,
    system_redundancy: 0.25, attack_surface_reduction: 0.25, recovery_velocity: 0.25,
    cross_layer_synchrony: 0.35, anomaly_detection: 0.25, self_healing_rate: 0.50,
    defensive_posture: 0.25, resilience_depth: 0.25, entropy_management: 0.25,
    cascade_prevention: 0.28, adaptive_immunity: 0.50, quantum_entanglement_index: 0.25,
    decoherence_risk: 0.60, vulnerability_exposure: 0.80,
  },
  // QR-006 — EMEA, adaptive_mesh → moderate, none
  // composite in [20,40), no pattern triggered
  {
    id: "QR-006", region: "EMEA", defense_layer: "adaptive_mesh",
    quantum_coherence: 0.72, adaptive_capacity: 0.68, threat_neutralization: 0.72,
    system_redundancy: 0.70, attack_surface_reduction: 0.70, recovery_velocity: 0.70,
    cross_layer_synchrony: 0.72, anomaly_detection: 0.70, self_healing_rate: 0.72,
    defensive_posture: 0.70, resilience_depth: 0.70, entropy_management: 0.70,
    cascade_prevention: 0.72, adaptive_immunity: 0.70, quantum_entanglement_index: 0.70,
    decoherence_risk: 0.22, vulnerability_exposure: 0.22,
  },
  // QR-007 — APAC, response_layer → high, vulnerability_breach
  // vulnerability_exposure≥0.65 and (1-threat_neutralization)≥0.55 → vulnerability_breach
  // decoherence_risk<0.65 to skip quantum_decoherence
  // (1-adaptive_capacity)<0.60 or (1-self_healing_rate)<0.55 to skip adaptive_failure
  // composite in [40,60) → high
  {
    id: "QR-007", region: "APAC", defense_layer: "response_layer",
    quantum_coherence: 0.62, adaptive_capacity: 0.50, threat_neutralization: 0.30,
    system_redundancy: 0.50, attack_surface_reduction: 0.50, recovery_velocity: 0.50,
    cross_layer_synchrony: 0.55, anomaly_detection: 0.45, self_healing_rate: 0.55,
    defensive_posture: 0.50, resilience_depth: 0.50, entropy_management: 0.55,
    cascade_prevention: 0.55, adaptive_immunity: 0.50, quantum_entanglement_index: 0.50,
    decoherence_risk: 0.40, vulnerability_exposure: 0.75,
  },
  // QR-008 — NOAM, quantum_core → critical, immune_breakdown
  // (1-adaptive_immunity)=0.78≥0.65 → immune_breakdown
  // decoherence_risk=0.60<0.65 → skip quantum_decoherence
  // (1-adaptive_capacity)=0.50<0.60 → skip adaptive_failure
  // (1-cascade_prevention)=0.60<0.65 → skip cascade_collapse
  // vulnerability_exposure=0.55<0.65 → skip vulnerability_breach
  // composite≥60 → critical
  {
    id: "QR-008", region: "NOAM", defense_layer: "quantum_core",
    quantum_coherence: 0.15, adaptive_capacity: 0.50, threat_neutralization: 0.20,
    system_redundancy: 0.20, attack_surface_reduction: 0.20, recovery_velocity: 0.20,
    cross_layer_synchrony: 0.25, anomaly_detection: 0.20, self_healing_rate: 0.55,
    defensive_posture: 0.20, resilience_depth: 0.20, entropy_management: 0.20,
    cascade_prevention: 0.40, adaptive_immunity: 0.22, quantum_entanglement_index: 0.20,
    decoherence_risk: 0.60, vulnerability_exposure: 0.55,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

// ── Scoring functions (mirrors Python engine exactly) ──────────────────────────

function coherenceScore(e: Entity): number {
  return (
    e.decoherence_risk * 0.4
    + e.vulnerability_exposure * 0.3
    + (1 - e.quantum_coherence) * 0.3
  ) * 100;
}

function adaptationScore(e: Entity): number {
  return (
    (1 - e.adaptive_capacity) * 0.35
    + (1 - e.adaptive_immunity) * 0.35
    + (1 - e.self_healing_rate) * 0.30
  ) * 100;
}

function neutralizationScore(e: Entity): number {
  return (
    (1 - e.threat_neutralization) * 0.4
    + (1 - e.anomaly_detection) * 0.3
    + (1 - e.attack_surface_reduction) * 0.3
  ) * 100;
}

function synchronyScore(e: Entity): number {
  return (
    (1 - e.cross_layer_synchrony) * 0.4
    + (1 - e.cascade_prevention) * 0.35
    + (1 - e.entropy_management) * 0.25
  ) * 100;
}

function resilienceComposite(coh: number, ada: number, neu: number, syn: number): number {
  return Math.round((coh * 0.30 + ada * 0.25 + neu * 0.25 + syn * 0.20) * 100) / 100;
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function resiliencePattern(e: Entity): string {
  if (e.decoherence_risk >= 0.65 && (1 - e.quantum_coherence) >= 0.50) return "quantum_decoherence";
  if ((1 - e.adaptive_capacity) >= 0.60 && (1 - e.self_healing_rate) >= 0.55) return "adaptive_failure";
  if ((1 - e.cascade_prevention) >= 0.65 && (1 - e.cross_layer_synchrony) >= 0.55) return "cascade_collapse";
  if (e.vulnerability_exposure >= 0.65 && (1 - e.threat_neutralization) >= 0.55) return "vulnerability_breach";
  if ((1 - e.adaptive_immunity) >= 0.65) return "immune_breakdown";
  return "none";
}

function resilienceSeverity(comp: number): string {
  if (comp >= 75) return "collapsed";
  if (comp >= 50) return "critical_stress";
  if (comp >= 25) return "degrading";
  return "resilient";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "quantum_reinforcement_emergency";
  if (risk === "high") {
    if (pattern === "quantum_decoherence") return "decoherence_correction";
    return "adaptive_defense_protocol";
  }
  if (risk === "moderate") return "resilience_monitoring";
  return "no_action";
}

function resilienceSignal(
  e: Entity,
  risk: string,
  coh: number,
  ada: number,
  syn: number,
  comp: number,
): string {
  if (risk === "critical") {
    return `Critique — cohérence quantique ${100 - Math.floor(coh)}% — immunité adaptative ${100 - Math.floor(ada)}% — composite ${Math.floor(comp)}`;
  }
  if (risk === "high") {
    return `Élevé — vulnérabilité ${Math.floor(e.vulnerability_exposure * 100)}% — synchronie ${100 - Math.floor(syn)}% — composite ${Math.floor(comp)}`;
  }
  if (risk === "moderate") {
    return `Modéré — capacité adaptative ${Math.floor(e.adaptive_capacity * 100)}% — résilience composite ${Math.floor(comp)}`;
  }
  return "Résilience quantique optimale — défenses adaptatives stables, cohérence maintenue";
}

// ── GET handler ────────────────────────────────────────────────────────────────

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const coh  = coherenceScore(e);
      const ada  = adaptationScore(e);
      const neu  = neutralizationScore(e);
      const syn  = synchronyScore(e);
      const comp = resilienceComposite(coh, ada, neu, syn);
      const risk = riskLevel(comp);
      const pat  = resiliencePattern(e);
      const sev  = resilienceSeverity(comp);
      const act  = recommendedAction(risk, pat);
      const sig  = resilienceSignal(e, risk, coh, ada, syn, comp);

      return {
        id:                        e.entity_id,
        region:                           e.region,
        defense_layer:                    e.defense_layer,
        resilience_risk:                  risk,
        resilience_pattern:               pat,
        resilience_severity:              sev,
        recommended_action:               act,
        coherence_score:                  Math.round(coh * 100) / 100,
        adaptation_score:                 Math.round(ada * 100) / 100,
        neutralization_score:             Math.round(neu * 100) / 100,
        synchrony_score:                  Math.round(syn * 100) / 100,
        resilience_composite:             comp,
        is_in_resilience_crisis:          comp >= 60,
        requires_immediate_reinforcement: comp >= 40,
        resilience_signal:                sig,
      };
    });

    const rc: Record<string,number> = {};
    const pc: Record<string,number> = {};
    const sc: Record<string,number> = {};
    const ac: Record<string,number> = {};
    let tComp=0, tCoh=0, tAda=0, tNeu=0, tSyn=0, crisisC=0, reinfC=0;

    for (const ent of entities) {
      rc[ent.resilience_risk]    = (rc[ent.resilience_risk]    || 0) + 1;
      pc[ent.resilience_pattern] = (pc[ent.resilience_pattern] || 0) + 1;
      sc[ent.resilience_severity] = (sc[ent.resilience_severity] || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tComp += ent.resilience_composite;
      tCoh  += ent.coherence_score;
      tAda  += ent.adaptation_score;
      tNeu  += ent.neutralization_score;
      tSyn  += ent.synchrony_score;
      if (ent.is_in_resilience_crisis)          crisisC++;
      if (ent.requires_immediate_reinforcement) reinfC++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 10) / 10;

    const summary = {
      total:                          n,
      risk_counts:                    rc,
      pattern_counts:                 pc,
      severity_counts:                sc,
      action_counts:                  ac,
      avg_resilience_composite:       avgComp,
      resilience_crisis_count:        crisisC,
      immediate_reinforcement_count:  reinfC,
      avg_coherence_score:            Math.round(tCoh / n * 10) / 10,
      avg_adaptation_score:           Math.round(tAda / n * 10) / 10,
      avg_neutralization_score:       Math.round(tNeu / n * 10) / 10,
      avg_synchrony_score:            Math.round(tSyn / n * 10) / 10,
      avg_estimated_resilience_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary }, "quantum-resilience-engine") as Record<string, unknown>
    ));
  }

  try {
    const upstream = await fetch(`${SWARM_API_URL}/api/quantum-resilience-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return sealResponse(NextResponse.json(
      sealResponse(data, "quantum-resilience-engine") as Record<string, unknown>
    ));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream swarm API unavailable" }, "quantum-resilience-engine") as Record<string, unknown>,
      { status: 502 }
    ));
  }
}
