import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// ── Mock entities ──────────────────────────────────────────────────────────────
// Module 326 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// 8 entities covering all nuclear risk patterns and risk levels.

const MOCK_ENTITIES = [
  // NUC-001 — MEA, weapons_program → critical, proliferation_cascade
  // proliferation_momentum≥0.70 AND new_entrant_proliferation_risk≥0.65 → proliferation_cascade
  // composite≥60 → critical
  {
    entity_id: "NUC-001", nuclear_domain: "weapons_program", region: "MEA",
    proliferation_momentum: 0.85,          arms_control_erosion_rate: 0.78,
    nuclear_doctrine_shift: 0.72,          tactical_nuclear_deployment_risk: 0.75,
    cyber_nuclear_vulnerability: 0.68,     nuclear_terrorism_risk: 0.62,
    command_control_integrity: 0.20,       deterrence_stability_erosion: 0.70,
    second_strike_vulnerability: 0.65,     miscalculation_risk: 0.68,
    fissile_material_security_gap: 0.65,   nuclear_state_fragility_risk: 0.72,
    dual_use_technology_diffusion: 0.75,   nuclear_taboo_erosion: 0.68,
    new_entrant_proliferation_risk: 0.82,  nuclear_winter_probability_driver: 0.60,
    diplomatic_framework_collapse: 0.72,
  },
  // NUC-002 — EMEA, civilian_nuclear → low, none
  // All low values → composite<20, no pattern triggered
  {
    entity_id: "NUC-002", nuclear_domain: "civilian_nuclear", region: "EMEA",
    proliferation_momentum: 0.08,          arms_control_erosion_rate: 0.10,
    nuclear_doctrine_shift: 0.10,          tactical_nuclear_deployment_risk: 0.08,
    cyber_nuclear_vulnerability: 0.10,     nuclear_terrorism_risk: 0.08,
    command_control_integrity: 0.90,       deterrence_stability_erosion: 0.08,
    second_strike_vulnerability: 0.10,     miscalculation_risk: 0.08,
    fissile_material_security_gap: 0.10,   nuclear_state_fragility_risk: 0.08,
    dual_use_technology_diffusion: 0.10,   nuclear_taboo_erosion: 0.08,
    new_entrant_proliferation_risk: 0.08,  nuclear_winter_probability_driver: 0.05,
    diplomatic_framework_collapse: 0.08,
  },
  // NUC-003 — APAC, deterrence_posture → high, deterrence_breakdown
  // deterrence_stability_erosion≥0.70 AND miscalculation_risk≥0.65 → deterrence_breakdown
  // proliferation_momentum=0.45<0.70 → avoids proliferation_cascade
  // composite in [40,60) → high
  {
    entity_id: "NUC-003", nuclear_domain: "deterrence_posture", region: "APAC",
    proliferation_momentum: 0.45,          arms_control_erosion_rate: 0.52,
    nuclear_doctrine_shift: 0.48,          tactical_nuclear_deployment_risk: 0.55,
    cyber_nuclear_vulnerability: 0.50,     nuclear_terrorism_risk: 0.42,
    command_control_integrity: 0.45,       deterrence_stability_erosion: 0.78,
    second_strike_vulnerability: 0.55,     miscalculation_risk: 0.72,
    fissile_material_security_gap: 0.38,   nuclear_state_fragility_risk: 0.45,
    dual_use_technology_diffusion: 0.40,   nuclear_taboo_erosion: 0.42,
    new_entrant_proliferation_risk: 0.40,  nuclear_winter_probability_driver: 0.45,
    diplomatic_framework_collapse: 0.48,
  },
  // NUC-004 — LATAM, research_reactor → low, none
  // All low values → composite<20, no pattern triggered
  {
    entity_id: "NUC-004", nuclear_domain: "research_reactor", region: "LATAM",
    proliferation_momentum: 0.10,          arms_control_erosion_rate: 0.12,
    nuclear_doctrine_shift: 0.10,          tactical_nuclear_deployment_risk: 0.08,
    cyber_nuclear_vulnerability: 0.10,     nuclear_terrorism_risk: 0.10,
    command_control_integrity: 0.88,       deterrence_stability_erosion: 0.10,
    second_strike_vulnerability: 0.08,     miscalculation_risk: 0.10,
    fissile_material_security_gap: 0.08,   nuclear_state_fragility_risk: 0.10,
    dual_use_technology_diffusion: 0.08,   nuclear_taboo_erosion: 0.10,
    new_entrant_proliferation_risk: 0.08,  nuclear_winter_probability_driver: 0.05,
    diplomatic_framework_collapse: 0.10,
  },
  // NUC-005 — NOAM, global_arsenal → critical, arms_control_collapse
  // arms_control_erosion_rate≥0.70 AND diplomatic_framework_collapse≥0.65 → arms_control_collapse
  // proliferation_momentum=0.60<0.70 → avoids proliferation_cascade
  // deterrence_stability_erosion=0.60<0.70 → avoids deterrence_breakdown
  // nuclear_terrorism_risk=0.58<0.70 → avoids nuclear_terrorism_event
  // nuclear_doctrine_shift=0.60<0.70 → avoids doctrine_escalation
  // composite≥60 → critical
  {
    entity_id: "NUC-005", nuclear_domain: "global_arsenal", region: "NOAM",
    proliferation_momentum: 0.60,          arms_control_erosion_rate: 0.82,
    nuclear_doctrine_shift: 0.60,          tactical_nuclear_deployment_risk: 0.72,
    cyber_nuclear_vulnerability: 0.68,     nuclear_terrorism_risk: 0.58,
    command_control_integrity: 0.22,       deterrence_stability_erosion: 0.60,
    second_strike_vulnerability: 0.65,     miscalculation_risk: 0.62,
    fissile_material_security_gap: 0.62,   nuclear_state_fragility_risk: 0.58,
    dual_use_technology_diffusion: 0.65,   nuclear_taboo_erosion: 0.62,
    new_entrant_proliferation_risk: 0.58,  nuclear_winter_probability_driver: 0.68,
    diplomatic_framework_collapse: 0.78,
  },
  // NUC-006 — EMEA, arms_control → moderate, none
  // All values below pattern thresholds → no pattern
  // composite in [20,40) → moderate
  {
    entity_id: "NUC-006", nuclear_domain: "arms_control", region: "EMEA",
    proliferation_momentum: 0.28,          arms_control_erosion_rate: 0.30,
    nuclear_doctrine_shift: 0.28,          tactical_nuclear_deployment_risk: 0.25,
    cyber_nuclear_vulnerability: 0.28,     nuclear_terrorism_risk: 0.25,
    command_control_integrity: 0.68,       deterrence_stability_erosion: 0.30,
    second_strike_vulnerability: 0.25,     miscalculation_risk: 0.28,
    fissile_material_security_gap: 0.25,   nuclear_state_fragility_risk: 0.28,
    dual_use_technology_diffusion: 0.28,   nuclear_taboo_erosion: 0.25,
    new_entrant_proliferation_risk: 0.25,  nuclear_winter_probability_driver: 0.22,
    diplomatic_framework_collapse: 0.28,
  },
  // NUC-007 — MEA, failed_state_nuclear → high, nuclear_terrorism_event
  // nuclear_terrorism_risk≥0.70 AND fissile_material_security_gap≥0.65 → nuclear_terrorism_event
  // proliferation_momentum=0.55<0.70 → avoids proliferation_cascade
  // deterrence_stability_erosion=0.55<0.70 → avoids deterrence_breakdown
  // composite in [40,60) → high
  {
    entity_id: "NUC-007", nuclear_domain: "failed_state_nuclear", region: "MEA",
    proliferation_momentum: 0.55,          arms_control_erosion_rate: 0.52,
    nuclear_doctrine_shift: 0.48,          tactical_nuclear_deployment_risk: 0.55,
    cyber_nuclear_vulnerability: 0.58,     nuclear_terrorism_risk: 0.80,
    command_control_integrity: 0.35,       deterrence_stability_erosion: 0.55,
    second_strike_vulnerability: 0.50,     miscalculation_risk: 0.55,
    fissile_material_security_gap: 0.75,   nuclear_state_fragility_risk: 0.72,
    dual_use_technology_diffusion: 0.48,   nuclear_taboo_erosion: 0.45,
    new_entrant_proliferation_risk: 0.50,  nuclear_winter_probability_driver: 0.52,
    diplomatic_framework_collapse: 0.48,
  },
  // NUC-008 — APAC, regional_competition → critical, doctrine_escalation
  // nuclear_doctrine_shift≥0.70 AND nuclear_taboo_erosion≥0.65 → doctrine_escalation
  // proliferation_momentum=0.60<0.70 → avoids proliferation_cascade
  // deterrence_stability_erosion=0.60<0.70 → avoids deterrence_breakdown
  // nuclear_terrorism_risk=0.58<0.70 → avoids nuclear_terrorism_event
  // composite≥60 → critical
  {
    entity_id: "NUC-008", nuclear_domain: "regional_competition", region: "APAC",
    proliferation_momentum: 0.60,          arms_control_erosion_rate: 0.62,
    nuclear_doctrine_shift: 0.82,          tactical_nuclear_deployment_risk: 0.72,
    cyber_nuclear_vulnerability: 0.65,     nuclear_terrorism_risk: 0.58,
    command_control_integrity: 0.20,       deterrence_stability_erosion: 0.60,
    second_strike_vulnerability: 0.65,     miscalculation_risk: 0.60,
    fissile_material_security_gap: 0.62,   nuclear_state_fragility_risk: 0.65,
    dual_use_technology_diffusion: 0.62,   nuclear_taboo_erosion: 0.78,
    new_entrant_proliferation_risk: 0.60,  nuclear_winter_probability_driver: 0.65,
    diplomatic_framework_collapse: 0.68,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

// ── Scoring functions (mirrors Python engine exactly) ──────────────────────────

function proliferationScore(e: Entity): number {
  return Math.round(
    (e.proliferation_momentum * 0.4
      + e.new_entrant_proliferation_risk * 0.35
      + e.dual_use_technology_diffusion * 0.25) * 100 * 100) / 100;
}

function stabilityScore(e: Entity): number {
  return Math.round(
    (e.deterrence_stability_erosion * 0.4
      + e.miscalculation_risk * 0.35
      + e.arms_control_erosion_rate * 0.25) * 100 * 100) / 100;
}

function securityScore(e: Entity): number {
  return Math.round(
    (e.fissile_material_security_gap * 0.4
      + e.nuclear_terrorism_risk * 0.35
      + (1 - e.command_control_integrity) * 0.25) * 100 * 100) / 100;
}

function doctrineScore(e: Entity): number {
  return Math.round(
    (e.nuclear_doctrine_shift * 0.4
      + e.nuclear_taboo_erosion * 0.35
      + e.diplomatic_framework_collapse * 0.25) * 100 * 100) / 100;
}

function nuclearComposite(prolif: number, stability: number, security: number, doctrine: number): number {
  return Math.round((prolif * 0.30 + stability * 0.25 + security * 0.25 + doctrine * 0.20) * 100) / 100;
}

function nuclearRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function nuclearPattern(e: Entity): string {
  if (e.proliferation_momentum >= 0.70 && e.new_entrant_proliferation_risk >= 0.65)
    return "proliferation_cascade";
  if (e.deterrence_stability_erosion >= 0.70 && e.miscalculation_risk >= 0.65)
    return "deterrence_breakdown";
  if (e.nuclear_terrorism_risk >= 0.70 && e.fissile_material_security_gap >= 0.65)
    return "nuclear_terrorism_event";
  if (e.nuclear_doctrine_shift >= 0.70 && e.nuclear_taboo_erosion >= 0.65)
    return "doctrine_escalation";
  if (e.arms_control_erosion_rate >= 0.70 && e.diplomatic_framework_collapse >= 0.65)
    return "arms_control_collapse";
  return "none";
}

function nuclearSeverity(comp: number): string {
  if (comp >= 75) return "existential_threat";
  if (comp >= 50) return "high_nuclear_risk";
  if (comp >= 25) return "nuclear_tension";
  return "nuclear_stable";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "existential_risk_protocol";
  if (risk === "high") {
    if (pattern === "nuclear_terrorism_event") return "nuclear_security_emergency";
    return "nonproliferation_activation";
  }
  if (risk === "moderate") return "nuclear_monitoring";
  return "no_action";
}

function nuclearSignal(e: Entity, pattern: string, comp: number): string {
  if (comp < 20) {
    return "Domaine nucléaire stable — prolifération maîtrisée, dissuasion stable, sécurité des matières fissiles assurée, aucun risque existentiel détecté";
  }
  if (comp >= 60) {
    const critLabels: Record<string, string> = {
      proliferation_cascade:   "Cascade de prolifération nucléaire",
      deterrence_breakdown:    "Effondrement de la dissuasion",
      nuclear_terrorism_event: "Événement terroriste nucléaire imminent",
      doctrine_escalation:     "Escalade doctrinale nucléaire",
      arms_control_collapse:   "Effondrement du contrôle des armements",
      none:                    "Défaillance nucléaire composite",
    };
    const label = critLabels[pattern] ?? pattern.replace(/_/g, " ");
    return `Critique — risque existentiel nucléaire — ${label} — prolifération ${e.proliferation_momentum.toFixed(2)} — composite ${Math.round(comp)}`;
  }
  if (comp >= 40) {
    const highLabels: Record<string, string> = {
      proliferation_cascade:   "Dynamique de prolifération en accélération",
      deterrence_breakdown:    "Fragilisation de la dissuasion",
      nuclear_terrorism_event: "Risque terroriste nucléaire élevé",
      doctrine_escalation:     "Dérive doctrinale nucléaire",
      arms_control_collapse:   "Érosion du cadre de contrôle armements",
      none:                    "Tension nucléaire diffuse",
    };
    const label = highLabels[pattern] ?? pattern.replace(/_/g, " ");
    return `Risque nucléaire élevé — ${label} — érosion dissuasion ${e.deterrence_stability_erosion.toFixed(2)} — risque calcul erroné ${e.miscalculation_risk.toFixed(2)} — composite ${Math.round(comp)}`;
  }
  return `Tension nucléaire modérée — surveillance requise — érosion contrôle armements ${e.arms_control_erosion_rate.toFixed(2)} — diffusion double usage ${e.dual_use_technology_diffusion.toFixed(2)} — composite ${Math.round(comp)}`;
}

// ── GET handler ────────────────────────────────────────────────────────────────

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(
      sealResponse({ error: "SWARM_API_URL non configuré — service indisponible" }, "nuclear-risk-engine") as Record<string, unknown>,
      { status: 503 }
    );
  }

  try {
    const entities = MOCK_ENTITIES.map(e => {
      const prolif   = proliferationScore(e);
      const stab     = stabilityScore(e);
      const sec      = securityScore(e);
      const doc      = doctrineScore(e);
      const comp     = nuclearComposite(prolif, stab, sec, doc);
      const risk     = nuclearRisk(comp);
      const pat      = nuclearPattern(e);
      const sev      = nuclearSeverity(comp);
      const act      = recommendedAction(risk, pat);
      const sig      = nuclearSignal(e, pat, comp);

      return {
        entity_id:                     e.entity_id,
        region:                        e.region,
        nuclear_domain:                e.nuclear_domain,
        nuclear_risk:                  risk,
        nuclear_pattern:               pat,
        nuclear_severity:              sev,
        recommended_action:            act,
        proliferation_score:           prolif,
        stability_score:               stab,
        security_score:                sec,
        doctrine_score:                doc,
        nuclear_composite:             comp,
        is_nuclear_crisis:             comp >= 60,
        requires_nuclear_intervention: comp >= 40,
        nuclear_signal:                sig,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tProlif = 0, tStab = 0, tSec = 0, tDoc = 0, tComp = 0;
    let crisisC = 0, interventionC = 0;

    for (const ent of entities) {
      rc[ent.nuclear_risk]       = (rc[ent.nuclear_risk]       || 0) + 1;
      pc[ent.nuclear_pattern]    = (pc[ent.nuclear_pattern]    || 0) + 1;
      sc[ent.nuclear_severity]   = (sc[ent.nuclear_severity]   || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tProlif += ent.proliferation_score;
      tStab   += ent.stability_score;
      tSec    += ent.security_score;
      tDoc    += ent.doctrine_score;
      tComp   += ent.nuclear_composite;
      if (ent.is_nuclear_crisis)             crisisC++;
      if (ent.requires_nuclear_intervention) interventionC++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 100) / 100;

    const summary = {
      total_entities:                     n,
      critical_entities:                  rc["critical"]  || 0,
      high_entities:                      rc["high"]      || 0,
      moderate_entities:                  rc["moderate"]  || 0,
      low_entities:                       rc["low"]       || 0,
      crisis_entities:                    crisisC,
      intervention_required:              interventionC,
      avg_proliferation_score:            Math.round(tProlif / n * 100) / 100,
      avg_stability_score:                Math.round(tStab   / n * 100) / 100,
      avg_security_score:                 Math.round(tSec    / n * 100) / 100,
      avg_doctrine_score:                 Math.round(tDoc    / n * 100) / 100,
      avg_nuclear_composite:              avgComp,
      avg_estimated_nuclear_threat_index: Math.round(avgComp / 100 * 10 * 100) / 100,
      risk_counts:                        rc,
      pattern_counts:                     pc,
      severity_counts:                    sc,
      action_counts:                      ac,
    };

    return NextResponse.json(
      sealResponse({ entities, summary }, "nuclear-risk-engine") as Record<string, unknown>
    );
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Erreur moteur risque nucléaire" }, "nuclear-risk-engine") as Record<string, unknown>,
      { status: 502 }
    );
  }
}
