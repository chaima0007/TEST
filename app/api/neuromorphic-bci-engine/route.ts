import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// ── Mock Neuromorphic BCI Data ─────────────────────────────────────────────────
// Module 310 — Neuromorphic Computing & Brain-Computer Interface Intelligence Engine
// Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
//
// 17 numeric fields (0.0–1.0):
// neural_signal_fidelity (inverse: high=good), cognitive_privacy_risk,
// neural_manipulation_potential, bci_security_vulnerability,
// consciousness_data_extraction_risk, neurorights_violation_index,
// cognitive_enhancement_inequality, neural_surveillance_risk,
// brain_hacking_exposure, regulatory_gap_index, informed_consent_deficit,
// neural_data_monetization_risk, cognitive_dependency_risk,
// neural_interface_reliability (inverse: high=good), biosafety_concern_index,
// military_weaponization_risk, societal_acceptance_gap

const MOCK_ENTITIES = [
  // NBC-001: consumer_bci, EMEA → critical, neural_sovereignty_breach
  {
    id: "NBC-001", technology_type: "consumer_bci", region: "EMEA",
    neural_signal_fidelity: 0.20, cognitive_privacy_risk: 0.82, neural_manipulation_potential: 0.75,
    bci_security_vulnerability: 0.70, consciousness_data_extraction_risk: 0.78,
    neurorights_violation_index: 0.65, cognitive_enhancement_inequality: 0.65,
    neural_surveillance_risk: 0.72, brain_hacking_exposure: 0.60, regulatory_gap_index: 0.62,
    informed_consent_deficit: 0.68, neural_data_monetization_risk: 0.80,
    cognitive_dependency_risk: 0.65, neural_interface_reliability: 0.22,
    biosafety_concern_index: 0.58, military_weaponization_risk: 0.55, societal_acceptance_gap: 0.72,
  },
  // NBC-002: medical_implant, APAC → low, none
  {
    id: "NBC-002", technology_type: "medical_implant", region: "APAC",
    neural_signal_fidelity: 0.92, cognitive_privacy_risk: 0.08, neural_manipulation_potential: 0.10,
    bci_security_vulnerability: 0.10, consciousness_data_extraction_risk: 0.08,
    neurorights_violation_index: 0.10, cognitive_enhancement_inequality: 0.08,
    neural_surveillance_risk: 0.10, brain_hacking_exposure: 0.08, regulatory_gap_index: 0.12,
    informed_consent_deficit: 0.10, neural_data_monetization_risk: 0.08,
    cognitive_dependency_risk: 0.10, neural_interface_reliability: 0.92,
    biosafety_concern_index: 0.08, military_weaponization_risk: 0.05, societal_acceptance_gap: 0.12,
  },
  // NBC-003: military_bci, NOAM → high, military_neuroweapon
  {
    id: "NBC-003", technology_type: "military_bci", region: "NOAM",
    neural_signal_fidelity: 0.40, cognitive_privacy_risk: 0.52, neural_manipulation_potential: 0.72,
    bci_security_vulnerability: 0.55, consciousness_data_extraction_risk: 0.48,
    neurorights_violation_index: 0.55, cognitive_enhancement_inequality: 0.50,
    neural_surveillance_risk: 0.58, brain_hacking_exposure: 0.52, regulatory_gap_index: 0.55,
    informed_consent_deficit: 0.48, neural_data_monetization_risk: 0.45,
    cognitive_dependency_risk: 0.50, neural_interface_reliability: 0.40,
    biosafety_concern_index: 0.60, military_weaponization_risk: 0.78, societal_acceptance_gap: 0.60,
  },
  // NBC-004: medical_implant, LATAM → low, none
  {
    id: "NBC-004", technology_type: "medical_implant", region: "LATAM",
    neural_signal_fidelity: 0.88, cognitive_privacy_risk: 0.10, neural_manipulation_potential: 0.12,
    bci_security_vulnerability: 0.12, consciousness_data_extraction_risk: 0.10,
    neurorights_violation_index: 0.12, cognitive_enhancement_inequality: 0.10,
    neural_surveillance_risk: 0.12, brain_hacking_exposure: 0.10, regulatory_gap_index: 0.15,
    informed_consent_deficit: 0.12, neural_data_monetization_risk: 0.10,
    cognitive_dependency_risk: 0.12, neural_interface_reliability: 0.88,
    biosafety_concern_index: 0.10, military_weaponization_risk: 0.08, societal_acceptance_gap: 0.15,
  },
  // NBC-005: consumer_bci, MEA → critical, neurorights_violation
  {
    id: "NBC-005", technology_type: "consumer_bci", region: "MEA",
    neural_signal_fidelity: 0.22, cognitive_privacy_risk: 0.65, neural_manipulation_potential: 0.60,
    bci_security_vulnerability: 0.68, consciousness_data_extraction_risk: 0.62,
    neurorights_violation_index: 0.82, cognitive_enhancement_inequality: 0.65,
    neural_surveillance_risk: 0.75, brain_hacking_exposure: 0.60, regulatory_gap_index: 0.78,
    informed_consent_deficit: 0.72, neural_data_monetization_risk: 0.70,
    cognitive_dependency_risk: 0.68, neural_interface_reliability: 0.25,
    biosafety_concern_index: 0.55, military_weaponization_risk: 0.60, societal_acceptance_gap: 0.70,
  },
  // NBC-006: research_bci, EMEA → moderate, none
  {
    id: "NBC-006", technology_type: "research_bci", region: "EMEA",
    neural_signal_fidelity: 0.65, cognitive_privacy_risk: 0.28, neural_manipulation_potential: 0.30,
    bci_security_vulnerability: 0.30, consciousness_data_extraction_risk: 0.25,
    neurorights_violation_index: 0.30, cognitive_enhancement_inequality: 0.28,
    neural_surveillance_risk: 0.32, brain_hacking_exposure: 0.25, regulatory_gap_index: 0.35,
    informed_consent_deficit: 0.30, neural_data_monetization_risk: 0.28,
    cognitive_dependency_risk: 0.30, neural_interface_reliability: 0.65,
    biosafety_concern_index: 0.28, military_weaponization_risk: 0.25, societal_acceptance_gap: 0.35,
  },
  // NBC-007: consumer_bci, APAC → high, brain_hacking_attack
  {
    id: "NBC-007", technology_type: "consumer_bci", region: "APAC",
    neural_signal_fidelity: 0.35, cognitive_privacy_risk: 0.55, neural_manipulation_potential: 0.58,
    bci_security_vulnerability: 0.72, consciousness_data_extraction_risk: 0.52,
    neurorights_violation_index: 0.52, cognitive_enhancement_inequality: 0.55,
    neural_surveillance_risk: 0.60, brain_hacking_exposure: 0.78, regulatory_gap_index: 0.55,
    informed_consent_deficit: 0.50, neural_data_monetization_risk: 0.55,
    cognitive_dependency_risk: 0.52, neural_interface_reliability: 0.38,
    biosafety_concern_index: 0.48, military_weaponization_risk: 0.50, societal_acceptance_gap: 0.58,
  },
  // NBC-008: military_bci, NOAM → critical, cognitive_inequality_crisis
  {
    id: "NBC-008", technology_type: "military_bci", region: "NOAM",
    neural_signal_fidelity: 0.20, cognitive_privacy_risk: 0.65, neural_manipulation_potential: 0.68,
    bci_security_vulnerability: 0.70, consciousness_data_extraction_risk: 0.60,
    neurorights_violation_index: 0.65, cognitive_enhancement_inequality: 0.82,
    neural_surveillance_risk: 0.70, brain_hacking_exposure: 0.62, regulatory_gap_index: 0.65,
    informed_consent_deficit: 0.72, neural_data_monetization_risk: 0.70,
    cognitive_dependency_risk: 0.68, neural_interface_reliability: 0.22,
    biosafety_concern_index: 0.65, military_weaponization_risk: 0.68, societal_acceptance_gap: 0.75,
  },
];

type NBCEntity = typeof MOCK_ENTITIES[0];

// ── Sub-score helpers ──────────────────────────────────────────────────────────

function privacyScore(e: NBCEntity): number {
  return Math.min(
    Math.round(
      (e.cognitive_privacy_risk * 0.40
        + e.consciousness_data_extraction_risk * 0.35
        + e.neural_data_monetization_risk * 0.25) * 100 * 100
    ) / 100,
    100,
  );
}

function securityScore(e: NBCEntity): number {
  return Math.min(
    Math.round(
      (e.bci_security_vulnerability * 0.40
        + e.brain_hacking_exposure * 0.35
        + e.neural_manipulation_potential * 0.25) * 100 * 100
    ) / 100,
    100,
  );
}

function rightsScore(e: NBCEntity): number {
  return Math.min(
    Math.round(
      (e.neurorights_violation_index * 0.40
        + e.regulatory_gap_index * 0.35
        + e.informed_consent_deficit * 0.25) * 100 * 100
    ) / 100,
    100,
  );
}

function societalScore(e: NBCEntity): number {
  return Math.min(
    Math.round(
      (e.cognitive_enhancement_inequality * 0.40
        + e.military_weaponization_risk * 0.35
        + e.cognitive_dependency_risk * 0.25) * 100 * 100
    ) / 100,
    100,
  );
}

function composite(priv: number, sec: number, rights: number, soc: number): number {
  return Math.min(
    Math.round((priv * 0.30 + sec * 0.25 + rights * 0.25 + soc * 0.20) * 100) / 100,
    100,
  );
}

function neuralPattern(e: NBCEntity): string {
  if (e.cognitive_privacy_risk >= 0.70 && e.consciousness_data_extraction_risk >= 0.65)
    return "neural_sovereignty_breach";
  if (e.brain_hacking_exposure >= 0.70 && e.bci_security_vulnerability >= 0.65)
    return "brain_hacking_attack";
  if (e.neurorights_violation_index >= 0.70 && e.regulatory_gap_index >= 0.65)
    return "neurorights_violation";
  if (e.cognitive_enhancement_inequality >= 0.70 && e.informed_consent_deficit >= 0.60)
    return "cognitive_inequality_crisis";
  if (e.military_weaponization_risk >= 0.70 && e.neural_manipulation_potential >= 0.65)
    return "military_neuroweapon";
  return "none";
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function neuralSeverity(comp: number): string {
  if (comp >= 75) return "neural_emergency";
  if (comp >= 50) return "high_neural_risk";
  if (comp >= 25) return "neural_concern";
  return "neural_safe";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "neural_emergency_shutdown";
  if (risk === "high") {
    if (pattern === "brain_hacking_attack") return "neural_security_lockdown";
    return "neurorights_protection_program";
  }
  if (risk === "moderate") return "neural_monitoring";
  return "no_action";
}

function neuralSignal(e: NBCEntity, pattern: string, comp: number): string {
  if (comp < 20) {
    return (
      "Interface neuronale sécurisée — intégrité du signal neural confirmée, "
      + "droits neuraux respectés, aucune menace détectée"
    );
  }
  const labels: Record<string, string> = {
    neural_sovereignty_breach:   "Violation souveraineté neurale",
    brain_hacking_attack:        "Attaque de piratage cérébral",
    neurorights_violation:       "Violation des neurodroits",
    cognitive_inequality_crisis: "Crise d'inégalité cognitive",
    military_neuroweapon:        "Neuroarme militaire détectée",
    none:                        "Aucun pattern critique",
  };
  const label = labels[pattern] ?? pattern.replace(/_/g, " ");
  return (
    `${label} — vie privée neurale ${e.cognitive_privacy_risk.toFixed(2)}`
    + ` — vulnérabilité BCI ${e.bci_security_vulnerability.toFixed(2)}`
    + ` — index neurodroits ${e.neurorights_violation_index.toFixed(2)}`
    + ` — composite ${Math.round(comp)}`
  );
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[neuromorphic-bci-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tPriv = 0, tSec = 0, tRights = 0, tSoc = 0, tComp = 0;
    let crisisCount = 0, interventionCount = 0;

    for (const ent of entities) {
      rc[ent.neural_risk]        = (rc[ent.neural_risk] || 0)        + 1;
      pc[ent.neural_pattern]     = (pc[ent.neural_pattern] || 0)     + 1;
      sc[ent.neural_severity]    = (sc[ent.neural_severity] || 0)    + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tPriv   += ent.privacy_score;
      tSec    += ent.security_score;
      tRights += ent.rights_score;
      tSoc    += ent.societal_score;
      tComp   += ent.neural_composite;
      if (ent.is_neural_crisis)            crisisCount++;
      if (ent.requires_neural_intervention) interventionCount++;
    }

    const n = entities.length;
    const avgComp = tComp / n;

    const summary = {
      total:                           n,
      risk_counts:                     rc,
      pattern_counts:                  pc,
      severity_counts:                 sc,
      action_counts:                   ac,
      avg_neural_composite:            Math.round(avgComp * 10) / 10,
      neural_crisis_count:             crisisCount,
      neural_intervention_count:       interventionCount,
      avg_privacy_score:               Math.round(tPriv / n * 10) / 10,
      avg_security_score:              Math.round(tSec / n * 10) / 10,
      avg_rights_score:                Math.round(tRights / n * 10) / 10,
      avg_societal_score:              Math.round(tSoc / n * 10) / 10,
      avg_estimated_neural_risk_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary }, "neuromorphic-bci-engine") as Parameters<typeof NextResponse.json>[0],
    ));
  }

  return sealResponse(NextResponse.json(
    await (await fetch(`${process.env.SWARM_API_URL}/neuromorphic-bci-engine`, { next: { revalidate: 30 } })).json(),
  ));
}
