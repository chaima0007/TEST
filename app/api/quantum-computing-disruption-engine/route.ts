import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── Mock entities ──────────────────────────────────────────────────────────────
// 8 entities covering all patterns and risk levels as specified in Module 307.

const MOCK_ENTITIES = [
  // QCD-001 — EMEA, financial_services → critical, cryptographic_apocalypse
  // cryptographic_vulnerability≥0.70 AND harvest_now_decrypt_later_risk≥0.65 → cryptographic_apocalypse
  // composite≥60 → critical
  {
    entity_id: "QCD-001", sector: "financial_services", region: "EMEA",
    cryptographic_vulnerability: 0.88,
    quantum_readiness_gap: 0.80,
    post_quantum_adoption_rate: 0.10,
    qubit_error_rate: 0.70,
    decoherence_susceptibility: 0.65,
    quantum_supremacy_exposure: 0.78,
    harvest_now_decrypt_later_risk: 0.82,
    quantum_key_distribution_adoption: 0.08,
    nist_pqc_compliance_gap: 0.85,
    supply_chain_quantum_risk: 0.70,
    financial_system_exposure: 0.75,
    critical_infrastructure_vulnerability: 0.65,
    quantum_arms_race_intensity: 0.60,
    talent_shortage_index: 0.62,
    standardization_lag: 0.78,
    adversarial_quantum_capability: 0.55,
    quantum_economic_disruption_index: 0.80,
  },
  // QCD-002 — APAC, healthcare → low, none
  // composite<20 → low; no pattern triggers
  {
    entity_id: "QCD-002", sector: "healthcare", region: "APAC",
    cryptographic_vulnerability: 0.08,
    quantum_readiness_gap: 0.10,
    post_quantum_adoption_rate: 0.90,
    qubit_error_rate: 0.10,
    decoherence_susceptibility: 0.08,
    quantum_supremacy_exposure: 0.10,
    harvest_now_decrypt_later_risk: 0.08,
    quantum_key_distribution_adoption: 0.88,
    nist_pqc_compliance_gap: 0.08,
    supply_chain_quantum_risk: 0.10,
    financial_system_exposure: 0.08,
    critical_infrastructure_vulnerability: 0.08,
    quantum_arms_race_intensity: 0.10,
    talent_shortage_index: 0.08,
    standardization_lag: 0.10,
    adversarial_quantum_capability: 0.08,
    quantum_economic_disruption_index: 0.08,
  },
  // QCD-003 — NOAM, defense → high, quantum_surprise_attack
  // adversarial_quantum_capability≥0.70 AND cryptographic_vulnerability≥0.60 → quantum_surprise_attack
  // cryptographic_vulnerability=0.62<0.70 OR harvest_now_decrypt_later_risk<0.65 → skip cryptographic_apocalypse
  // composite in [40,60) → high
  {
    entity_id: "QCD-003", sector: "defense", region: "NOAM",
    cryptographic_vulnerability: 0.62,
    quantum_readiness_gap: 0.50,
    post_quantum_adoption_rate: 0.42,
    qubit_error_rate: 0.48,
    decoherence_susceptibility: 0.45,
    quantum_supremacy_exposure: 0.58,
    harvest_now_decrypt_later_risk: 0.50,
    quantum_key_distribution_adoption: 0.38,
    nist_pqc_compliance_gap: 0.50,
    supply_chain_quantum_risk: 0.45,
    financial_system_exposure: 0.42,
    critical_infrastructure_vulnerability: 0.50,
    quantum_arms_race_intensity: 0.62,
    talent_shortage_index: 0.45,
    standardization_lag: 0.48,
    adversarial_quantum_capability: 0.78,
    quantum_economic_disruption_index: 0.52,
  },
  // QCD-004 — LATAM, telecommunications → low, none
  // composite<20 → low; no pattern triggers
  {
    entity_id: "QCD-004", sector: "telecommunications", region: "LATAM",
    cryptographic_vulnerability: 0.10,
    quantum_readiness_gap: 0.12,
    post_quantum_adoption_rate: 0.88,
    qubit_error_rate: 0.08,
    decoherence_susceptibility: 0.10,
    quantum_supremacy_exposure: 0.08,
    harvest_now_decrypt_later_risk: 0.10,
    quantum_key_distribution_adoption: 0.85,
    nist_pqc_compliance_gap: 0.10,
    supply_chain_quantum_risk: 0.08,
    financial_system_exposure: 0.10,
    critical_infrastructure_vulnerability: 0.10,
    quantum_arms_race_intensity: 0.08,
    talent_shortage_index: 0.10,
    standardization_lag: 0.08,
    adversarial_quantum_capability: 0.10,
    quantum_economic_disruption_index: 0.10,
  },
  // QCD-005 — MEA, energy_grid → critical, infrastructure_quantum_shock
  // critical_infrastructure_vulnerability≥0.70 AND quantum_readiness_gap≥0.65 → infrastructure_quantum_shock
  // cryptographic_vulnerability=0.55<0.70 → skip cryptographic_apocalypse
  // adversarial_quantum_capability=0.60<0.70 → skip quantum_surprise_attack
  // composite≥60 → critical
  {
    entity_id: "QCD-005", sector: "energy_grid", region: "MEA",
    cryptographic_vulnerability: 0.55,
    quantum_readiness_gap: 0.82,
    post_quantum_adoption_rate: 0.12,
    qubit_error_rate: 0.72,
    decoherence_susceptibility: 0.68,
    quantum_supremacy_exposure: 0.70,
    harvest_now_decrypt_later_risk: 0.55,
    quantum_key_distribution_adoption: 0.10,
    nist_pqc_compliance_gap: 0.78,
    supply_chain_quantum_risk: 0.72,
    financial_system_exposure: 0.65,
    critical_infrastructure_vulnerability: 0.88,
    quantum_arms_race_intensity: 0.65,
    talent_shortage_index: 0.60,
    standardization_lag: 0.75,
    adversarial_quantum_capability: 0.60,
    quantum_economic_disruption_index: 0.75,
  },
  // QCD-006 — EMEA, logistics → moderate, none
  // composite in [20,40) → moderate; no pattern triggers
  {
    entity_id: "QCD-006", sector: "logistics", region: "EMEA",
    cryptographic_vulnerability: 0.30,
    quantum_readiness_gap: 0.35,
    post_quantum_adoption_rate: 0.60,
    qubit_error_rate: 0.28,
    decoherence_susceptibility: 0.30,
    quantum_supremacy_exposure: 0.32,
    harvest_now_decrypt_later_risk: 0.28,
    quantum_key_distribution_adoption: 0.55,
    nist_pqc_compliance_gap: 0.30,
    supply_chain_quantum_risk: 0.32,
    financial_system_exposure: 0.28,
    critical_infrastructure_vulnerability: 0.30,
    quantum_arms_race_intensity: 0.28,
    talent_shortage_index: 0.30,
    standardization_lag: 0.32,
    adversarial_quantum_capability: 0.28,
    quantum_economic_disruption_index: 0.30,
  },
  // QCD-007 — APAC, banking → high, financial_system_collapse
  // financial_system_exposure≥0.70 AND nist_pqc_compliance_gap≥0.65 → financial_system_collapse
  // cryptographic_vulnerability=0.55<0.70 → skip cryptographic_apocalypse
  // adversarial_quantum_capability=0.48<0.70 → skip quantum_surprise_attack
  // critical_infrastructure_vulnerability=0.55<0.70 → skip infrastructure_quantum_shock
  // composite in [40,60) → high
  {
    entity_id: "QCD-007", sector: "banking", region: "APAC",
    cryptographic_vulnerability: 0.55,
    quantum_readiness_gap: 0.52,
    post_quantum_adoption_rate: 0.38,
    qubit_error_rate: 0.45,
    decoherence_susceptibility: 0.42,
    quantum_supremacy_exposure: 0.50,
    harvest_now_decrypt_later_risk: 0.52,
    quantum_key_distribution_adoption: 0.35,
    nist_pqc_compliance_gap: 0.72,
    supply_chain_quantum_risk: 0.45,
    financial_system_exposure: 0.78,
    critical_infrastructure_vulnerability: 0.55,
    quantum_arms_race_intensity: 0.42,
    talent_shortage_index: 0.45,
    standardization_lag: 0.50,
    adversarial_quantum_capability: 0.48,
    quantum_economic_disruption_index: 0.55,
  },
  // QCD-008 — NOAM, government → critical, talent_capability_gap
  // talent_shortage_index≥0.70 AND quantum_readiness_gap≥0.65 → talent_capability_gap
  // cryptographic_vulnerability=0.58<0.70 → skip cryptographic_apocalypse
  // adversarial_quantum_capability=0.55<0.70 → skip quantum_surprise_attack
  // critical_infrastructure_vulnerability=0.60<0.70 → skip infrastructure_quantum_shock
  // financial_system_exposure=0.55<0.70 → skip financial_system_collapse
  // composite≥60 → critical
  {
    entity_id: "QCD-008", sector: "government", region: "NOAM",
    cryptographic_vulnerability: 0.58,
    quantum_readiness_gap: 0.85,
    post_quantum_adoption_rate: 0.10,
    qubit_error_rate: 0.68,
    decoherence_susceptibility: 0.62,
    quantum_supremacy_exposure: 0.65,
    harvest_now_decrypt_later_risk: 0.58,
    quantum_key_distribution_adoption: 0.08,
    nist_pqc_compliance_gap: 0.80,
    supply_chain_quantum_risk: 0.68,
    financial_system_exposure: 0.55,
    critical_infrastructure_vulnerability: 0.60,
    quantum_arms_race_intensity: 0.68,
    talent_shortage_index: 0.82,
    standardization_lag: 0.80,
    adversarial_quantum_capability: 0.55,
    quantum_economic_disruption_index: 0.72,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

// ── Scoring functions (mirrors Python engine exactly) ──────────────────────────

function cryptographicScore(e: Entity): number {
  const raw = (
    e.cryptographic_vulnerability * 0.4
    + e.harvest_now_decrypt_later_risk * 0.35
    + e.nist_pqc_compliance_gap * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function readinessScore(e: Entity): number {
  const raw = (
    e.quantum_readiness_gap * 0.4
    + (1 - e.post_quantum_adoption_rate) * 0.35
    + e.standardization_lag * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function infrastructureScore(e: Entity): number {
  const raw = (
    e.critical_infrastructure_vulnerability * 0.4
    + e.financial_system_exposure * 0.35
    + e.supply_chain_quantum_risk * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function geopoliticalScore(e: Entity): number {
  const raw = (
    e.adversarial_quantum_capability * 0.4
    + e.quantum_arms_race_intensity * 0.35
    + e.talent_shortage_index * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function quantumComposite(crypto: number, readiness: number, infra: number, geo: number): number {
  return Math.round((crypto * 0.30 + readiness * 0.25 + infra * 0.25 + geo * 0.20) * 100) / 100;
}

function quantumRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function quantumPattern(e: Entity): string {
  if (e.cryptographic_vulnerability >= 0.70 && e.harvest_now_decrypt_later_risk >= 0.65)
    return "cryptographic_apocalypse";
  if (e.adversarial_quantum_capability >= 0.70 && e.cryptographic_vulnerability >= 0.60)
    return "quantum_surprise_attack";
  if (e.critical_infrastructure_vulnerability >= 0.70 && e.quantum_readiness_gap >= 0.65)
    return "infrastructure_quantum_shock";
  if (e.financial_system_exposure >= 0.70 && e.nist_pqc_compliance_gap >= 0.65)
    return "financial_system_collapse";
  if (e.talent_shortage_index >= 0.70 && e.quantum_readiness_gap >= 0.65)
    return "talent_capability_gap";
  return "none";
}

function quantumSeverity(comp: number): string {
  if (comp >= 75) return "quantum_emergency";
  if (comp >= 50) return "high_quantum_risk";
  if (comp >= 25) return "quantum_preparing";
  return "quantum_secure";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "quantum_emergency_migration";
  if (risk === "high" && pattern === "cryptographic_apocalypse") return "immediate_pqc_deployment";
  if (risk === "high") return "quantum_transition_plan";
  if (risk === "moderate") return "quantum_monitoring";
  return "no_action";
}

function quantumSignal(e: Entity, risk: string, comp: number): string {
  const compInt = Math.round(comp);
  if (risk === "critical") {
    return `Critique — vulnérabilité cryptographique ${Math.round(e.cryptographic_vulnerability * 100)}% — risque HNDL ${Math.round(e.harvest_now_decrypt_later_risk * 100)}% — composite ${compInt}`;
  }
  if (risk === "high") {
    return `Élevé — capacité adversaire quantique ${Math.round(e.adversarial_quantum_capability * 100)}% — écart préparation ${Math.round(e.quantum_readiness_gap * 100)}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `Modéré — retard standardisation ${Math.round(e.standardization_lag * 100)}% — composite ${compInt}`;
  }
  return "Infrastructure quantique sécurisée — conformité PQC NIST assurée, résilience cryptographique préservée";
}

// ── GET handler ────────────────────────────────────────────────────────────────

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const crypto  = cryptographicScore(e);
      const ready   = readinessScore(e);
      const infra   = infrastructureScore(e);
      const geo     = geopoliticalScore(e);
      const comp    = quantumComposite(crypto, ready, infra, geo);
      const risk    = quantumRisk(comp);
      const pat     = quantumPattern(e);
      const sev     = quantumSeverity(comp);
      const act     = recommendedAction(risk, pat);
      const sig     = quantumSignal(e, risk, comp);

      return {
        entity_id:                      e.entity_id,
        region:                         e.region,
        sector:                         e.sector,
        quantum_risk:                   risk,
        quantum_pattern:                pat,
        quantum_severity:               sev,
        recommended_action:             act,
        cryptographic_score:            crypto,
        readiness_score:                ready,
        infrastructure_score:           infra,
        geopolitical_score:             geo,
        quantum_composite:              comp,
        is_quantum_crisis:              comp >= 60,
        requires_quantum_intervention:  comp >= 40,
        quantum_signal:                 sig,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tCrypto = 0, tReady = 0, tInfra = 0, tGeo = 0, tComp = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.quantum_risk]       = (rc[ent.quantum_risk]       || 0) + 1;
      pc[ent.quantum_pattern]    = (pc[ent.quantum_pattern]    || 0) + 1;
      sc[ent.quantum_severity]   = (sc[ent.quantum_severity]   || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tCrypto += ent.cryptographic_score;
      tReady  += ent.readiness_score;
      tInfra  += ent.infrastructure_score;
      tGeo    += ent.geopolitical_score;
      tComp   += ent.quantum_composite;
      if (ent.is_quantum_crisis)             crisisCount++;
      if (ent.requires_quantum_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 10) / 10;

    const summary = {
      total:                                  n,
      risk_counts:                            rc,
      pattern_counts:                         pc,
      severity_counts:                        sc,
      action_counts:                          ac,
      avg_quantum_composite:                  avgComp,
      quantum_crisis_count:                   crisisCount,
      quantum_intervention_count:             interventionCount,
      avg_cryptographic_score:                Math.round(tCrypto / n * 10) / 10,
      avg_readiness_score:                    Math.round(tReady  / n * 10) / 10,
      avg_infrastructure_score:               Math.round(tInfra  / n * 10) / 10,
      avg_geopolitical_score:                 Math.round(tGeo    / n * 10) / 10,
      avg_estimated_quantum_disruption_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "quantum-computing-disruption-engine"));
  }

  try {
    const upstream = await fetch(`${SWARM_API_URL}/quantum-computing-disruption-engine`);
    const data = await upstream.json();
    return NextResponse.json(sealResponse(data, "quantum-computing-disruption-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream quantum computing disruption engine unavailable" }, "quantum-computing-disruption-engine"),
      { status: 502 }
    );
  }
}
