import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // DTE-001 — EMEA, industrial_twin → critical, twin_divergence_crisis
  // physical_digital_sync_lag>=0.70 AND model_drift_rate>=0.65 → twin_divergence_crisis
  // composite >=60 → critical
  {
    id: "DTE-001", twin_category: "industrial_twin", region: "EMEA",
    simulation_accuracy: 0.15,
    physical_digital_sync_lag: 0.85,
    data_sovereignty_risk: 0.80,
    model_drift_rate: 0.80,
    twin_manipulation_risk: 0.68,
    predictive_fidelity: 0.18,
    real_time_latency: 0.72,
    sensor_coverage_gap: 0.78,
    adversarial_input_risk: 0.72,
    regulatory_compliance_gap: 0.72,
    economic_divergence_index: 0.75,
    twin_fragmentation_rate: 0.70,
    orchestration_complexity: 0.78,
    cybersecurity_exposure: 0.75,
    interoperability_deficit: 0.65,
    human_oversight_erosion: 0.75,
    twin_dependency_lock_in: 0.65,
  },
  // DTE-002 — APAC, urban_twin → low, none
  // composite < 20 → low; no pattern triggers
  {
    id: "DTE-002", twin_category: "urban_twin", region: "APAC",
    simulation_accuracy: 0.90,
    physical_digital_sync_lag: 0.10,
    data_sovereignty_risk: 0.12,
    model_drift_rate: 0.08,
    twin_manipulation_risk: 0.10,
    predictive_fidelity: 0.88,
    real_time_latency: 0.08,
    sensor_coverage_gap: 0.10,
    adversarial_input_risk: 0.10,
    regulatory_compliance_gap: 0.08,
    economic_divergence_index: 0.12,
    twin_fragmentation_rate: 0.08,
    orchestration_complexity: 0.15,
    cybersecurity_exposure: 0.10,
    interoperability_deficit: 0.12,
    human_oversight_erosion: 0.08,
    twin_dependency_lock_in: 0.10,
  },
  // DTE-003 — NOAM, financial_twin → high, adversarial_twin_attack
  // adversarial_input_risk>=0.70 AND cybersecurity_exposure>=0.65 → adversarial_twin_attack
  // composite 40-59 → high
  {
    id: "DTE-003", twin_category: "financial_twin", region: "NOAM",
    simulation_accuracy: 0.55,
    physical_digital_sync_lag: 0.48,
    data_sovereignty_risk: 0.52,
    model_drift_rate: 0.45,
    twin_manipulation_risk: 0.58,
    predictive_fidelity: 0.50,
    real_time_latency: 0.42,
    sensor_coverage_gap: 0.45,
    adversarial_input_risk: 0.78,
    regulatory_compliance_gap: 0.48,
    economic_divergence_index: 0.50,
    twin_fragmentation_rate: 0.40,
    orchestration_complexity: 0.52,
    cybersecurity_exposure: 0.72,
    interoperability_deficit: 0.45,
    human_oversight_erosion: 0.50,
    twin_dependency_lock_in: 0.45,
  },
  // DTE-004 — LATAM, urban_twin → low, none
  // composite < 20 → low; no pattern triggers
  {
    id: "DTE-004", twin_category: "urban_twin", region: "LATAM",
    simulation_accuracy: 0.88,
    physical_digital_sync_lag: 0.12,
    data_sovereignty_risk: 0.10,
    model_drift_rate: 0.10,
    twin_manipulation_risk: 0.12,
    predictive_fidelity: 0.85,
    real_time_latency: 0.10,
    sensor_coverage_gap: 0.12,
    adversarial_input_risk: 0.12,
    regulatory_compliance_gap: 0.10,
    economic_divergence_index: 0.15,
    twin_fragmentation_rate: 0.10,
    orchestration_complexity: 0.18,
    cybersecurity_exposure: 0.12,
    interoperability_deficit: 0.10,
    human_oversight_erosion: 0.10,
    twin_dependency_lock_in: 0.12,
  },
  // DTE-005 — MEA, supply_chain_twin → critical, digital_sovereignty_breach
  // data_sovereignty_risk>=0.70 AND regulatory_compliance_gap>=0.65 → digital_sovereignty_breach
  // composite >=60 → critical
  {
    id: "DTE-005", twin_category: "supply_chain_twin", region: "MEA",
    simulation_accuracy: 0.22,
    physical_digital_sync_lag: 0.65,
    data_sovereignty_risk: 0.82,
    model_drift_rate: 0.70,
    twin_manipulation_risk: 0.72,
    predictive_fidelity: 0.20,
    real_time_latency: 0.68,
    sensor_coverage_gap: 0.70,
    adversarial_input_risk: 0.65,
    regulatory_compliance_gap: 0.75,
    economic_divergence_index: 0.72,
    twin_fragmentation_rate: 0.65,
    orchestration_complexity: 0.72,
    cybersecurity_exposure: 0.70,
    interoperability_deficit: 0.62,
    human_oversight_erosion: 0.78,
    twin_dependency_lock_in: 0.65,
  },
  // DTE-006 — EMEA, logistics_twin → moderate, none
  // composite 20-39 → moderate; no pattern triggers
  {
    id: "DTE-006", twin_category: "logistics_twin", region: "EMEA",
    simulation_accuracy: 0.68,
    physical_digital_sync_lag: 0.32,
    data_sovereignty_risk: 0.30,
    model_drift_rate: 0.28,
    twin_manipulation_risk: 0.32,
    predictive_fidelity: 0.65,
    real_time_latency: 0.30,
    sensor_coverage_gap: 0.28,
    adversarial_input_risk: 0.30,
    regulatory_compliance_gap: 0.28,
    economic_divergence_index: 0.32,
    twin_fragmentation_rate: 0.28,
    orchestration_complexity: 0.35,
    cybersecurity_exposure: 0.30,
    interoperability_deficit: 0.30,
    human_oversight_erosion: 0.28,
    twin_dependency_lock_in: 0.30,
  },
  // DTE-007 — APAC, healthcare_twin → high, lock_in_monopoly
  // twin_dependency_lock_in>=0.70 AND interoperability_deficit>=0.65 → lock_in_monopoly
  // composite 40-59 → high
  {
    id: "DTE-007", twin_category: "healthcare_twin", region: "APAC",
    simulation_accuracy: 0.50,
    physical_digital_sync_lag: 0.50,
    data_sovereignty_risk: 0.52,
    model_drift_rate: 0.45,
    twin_manipulation_risk: 0.48,
    predictive_fidelity: 0.48,
    real_time_latency: 0.45,
    sensor_coverage_gap: 0.48,
    adversarial_input_risk: 0.50,
    regulatory_compliance_gap: 0.48,
    economic_divergence_index: 0.52,
    twin_fragmentation_rate: 0.45,
    orchestration_complexity: 0.55,
    cybersecurity_exposure: 0.50,
    interoperability_deficit: 0.72,
    human_oversight_erosion: 0.48,
    twin_dependency_lock_in: 0.80,
  },
  // DTE-008 — NOAM, military_twin → critical, predictive_failure_cascade
  // simulation_accuracy<=0.30 AND twin_fragmentation_rate>=0.60 → predictive_failure_cascade
  // composite >=60 → critical
  {
    id: "DTE-008", twin_category: "military_twin", region: "NOAM",
    simulation_accuracy: 0.20,
    physical_digital_sync_lag: 0.78,
    data_sovereignty_risk: 0.75,
    model_drift_rate: 0.78,
    twin_manipulation_risk: 0.72,
    predictive_fidelity: 0.18,
    real_time_latency: 0.75,
    sensor_coverage_gap: 0.72,
    adversarial_input_risk: 0.68,
    regulatory_compliance_gap: 0.70,
    economic_divergence_index: 0.72,
    twin_fragmentation_rate: 0.72,
    orchestration_complexity: 0.78,
    cybersecurity_exposure: 0.72,
    interoperability_deficit: 0.65,
    human_oversight_erosion: 0.70,
    twin_dependency_lock_in: 0.68,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function fidelityScore(e: Entity): number {
  const raw = (
    (1 - e.simulation_accuracy) * 0.4 +
    e.model_drift_rate * 0.35 +
    e.real_time_latency * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function syncScore(e: Entity): number {
  const raw = (
    e.physical_digital_sync_lag * 0.4 +
    e.sensor_coverage_gap * 0.35 +
    e.twin_fragmentation_rate * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function securityScore(e: Entity): number {
  const raw = (
    e.cybersecurity_exposure * 0.4 +
    e.adversarial_input_risk * 0.35 +
    e.twin_manipulation_risk * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function governanceScore(e: Entity): number {
  const raw = (
    e.data_sovereignty_risk * 0.4 +
    e.regulatory_compliance_gap * 0.35 +
    e.human_oversight_erosion * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function twinComposite(fid: number, syn: number, sec: number, gov: number): number {
  return Math.round((fid * 0.30 + syn * 0.25 + sec * 0.25 + gov * 0.20) * 100) / 100;
}

function twinPattern(e: Entity): string {
  if (e.physical_digital_sync_lag >= 0.70 && e.model_drift_rate >= 0.65)
    return "twin_divergence_crisis";
  if (e.data_sovereignty_risk >= 0.70 && e.regulatory_compliance_gap >= 0.65)
    return "digital_sovereignty_breach";
  if (e.adversarial_input_risk >= 0.70 && e.cybersecurity_exposure >= 0.65)
    return "adversarial_twin_attack";
  if (e.simulation_accuracy <= 0.30 && e.twin_fragmentation_rate >= 0.60)
    return "predictive_failure_cascade";
  if (e.twin_dependency_lock_in >= 0.70 && e.interoperability_deficit >= 0.65)
    return "lock_in_monopoly";
  return "none";
}

function twinRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function twinSeverity(comp: number): string {
  if (comp >= 75) return "twin_emergency";
  if (comp >= 50) return "critical_divergence";
  if (comp >= 25) return "twin_instability";
  return "twin_stable";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "twin_emergency_shutdown";
  if (risk === "high" && pattern === "adversarial_twin_attack") return "security_lockdown";
  if (risk === "high") return "twin_recalibration";
  if (risk === "moderate") return "sync_monitoring";
  return "no_action";
}

function twinSignal(e: Entity, risk: string, comp: number): string {
  if (risk === "critical") {
    return `Critique — synchronisation physique-numérique ${Math.round(e.physical_digital_sync_lag * 100)}% — dérive modèle ${Math.round(e.model_drift_rate * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "high") {
    return `Élevé — exposition cybersécurité ${Math.round(e.cybersecurity_exposure * 100)}% — risque données souveraines ${Math.round(e.data_sovereignty_risk * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "moderate") {
    return `Modéré — latence temps réel ${Math.round(e.real_time_latency * 100)}% — composite ${Math.round(comp)}`;
  }
  return "Jumeau numérique stable — fidélité optimale, synchronisation solide, gouvernance maîtrisée";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const fid = fidelityScore(e);
      const syn = syncScore(e);
      const sec = securityScore(e);
      const gov = governanceScore(e);
      const comp = twinComposite(fid, syn, sec, gov);
      const pat  = twinPattern(e);
      const risk = twinRisk(comp);
      const sev  = twinSeverity(comp);
      const act  = recommendedAction(risk, pat);
      const sig  = twinSignal(e, risk, comp);
      return {
        id:                    e.entity_id,
        region:                       e.region,
        twin_category:                e.twin_category,
        twin_risk:                    risk,
        twin_pattern:                 pat,
        twin_severity:                sev,
        recommended_action:           act,
        fidelity_score:               fid,
        sync_score:                   syn,
        security_score:               sec,
        governance_score:             gov,
        twin_composite:               comp,
        is_twin_crisis:               comp >= 60,
        requires_twin_intervention:   comp >= 40,
        twin_signal:                  sig,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tFid = 0, tSyn = 0, tSec = 0, tGov = 0, tComp = 0, crisisC = 0, interventionC = 0;

    for (const ent of entities) {
      rc[ent.twin_risk]          = (rc[ent.twin_risk]          || 0) + 1;
      pc[ent.twin_pattern]       = (pc[ent.twin_pattern]       || 0) + 1;
      sc[ent.twin_severity]      = (sc[ent.twin_severity]      || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tFid  += ent.fidelity_score;
      tSyn  += ent.sync_score;
      tSec  += ent.security_score;
      tGov  += ent.governance_score;
      tComp += ent.twin_composite;
      if (ent.is_twin_crisis)            crisisC++;
      if (ent.requires_twin_intervention) interventionC++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 10) / 10;
    const summary = {
      total:                          n,
      risk_counts:                    rc,
      pattern_counts:                 pc,
      severity_counts:                sc,
      action_counts:                  ac,
      avg_twin_composite:             avgComp,
      twin_crisis_count:              crisisC,
      twin_intervention_count:        interventionC,
      avg_fidelity_score:             Math.round(tFid / n * 10) / 10,
      avg_sync_score:                 Math.round(tSyn / n * 10) / 10,
      avg_security_score:             Math.round(tSec / n * 10) / 10,
      avg_governance_score:           Math.round(tGov / n * 10) / 10,
      avg_estimated_twin_risk_index:  Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "digital-twin-economy-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/digital-twin-economy-engine`);
    const data = await upstream.json();
    return NextResponse.json(sealResponse(data, "digital-twin-economy-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream digital twin economy engine unavailable" }, "digital-twin-economy-engine"),
      { status: 502 }
    );
  }
}
