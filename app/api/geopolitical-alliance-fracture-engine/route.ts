import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// ── Security guard ─────────────────────────────────────────────────────────────
if (!process.env.SWARM_API_URL) {
  // will be evaluated per-request below
}

// ── Mock entities ──────────────────────────────────────────────────────────────
// Module 312 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// 8 entities covering all fracture patterns and risk levels.

const MOCK_ENTITIES = [
  // GAF-001 — EMEA, nato_equivalent → critical, alliance_dissolution
  // internal_cohesion_erosion≥0.70 AND defection_incentive_strength≥0.65 → alliance_dissolution
  // composite≥60 → critical
  {
    entity_id: "GAF-001", alliance_type: "nato_equivalent", region: "EMEA",
    internal_cohesion_erosion: 0.85,            burden_sharing_imbalance: 0.75,
    strategic_interest_divergence: 0.80,        external_pressure_index: 0.72,
    defection_incentive_strength: 0.82,         alternative_alignment_attractiveness: 0.78,
    historical_grievance_activation: 0.70,      democratic_backsliding_within_alliance: 0.65,
    economic_decoupling_pressure: 0.70,         nuclear_deterrence_reliability: 0.15,
    intelligence_trust_deficit: 0.80,           sanctions_fatigue_index: 0.68,
    populist_alliance_skepticism: 0.68,         technology_rivalry_within_alliance: 0.62,
    leadership_legitimacy_crisis: 0.72,         treaty_obligation_strain: 0.75,
    multipolar_fragmentation_index: 0.80,
  },
  // GAF-002 — APAC, trade_bloc → low, none
  // All low values → composite<20, no pattern triggered
  {
    entity_id: "GAF-002", alliance_type: "trade_bloc", region: "APAC",
    internal_cohesion_erosion: 0.08,            burden_sharing_imbalance: 0.10,
    strategic_interest_divergence: 0.10,        external_pressure_index: 0.10,
    defection_incentive_strength: 0.08,         alternative_alignment_attractiveness: 0.08,
    historical_grievance_activation: 0.10,      democratic_backsliding_within_alliance: 0.08,
    economic_decoupling_pressure: 0.10,         nuclear_deterrence_reliability: 0.95,
    intelligence_trust_deficit: 0.08,           sanctions_fatigue_index: 0.08,
    populist_alliance_skepticism: 0.08,         technology_rivalry_within_alliance: 0.08,
    leadership_legitimacy_crisis: 0.08,         treaty_obligation_strain: 0.08,
    multipolar_fragmentation_index: 0.08,
  },
  // GAF-003 — NOAM, security_alliance → high, trust_collapse
  // intelligence_trust_deficit≥0.70 AND treaty_obligation_strain≥0.65 → trust_collapse
  // internal_cohesion_erosion=0.55<0.70 → avoids alliance_dissolution
  // alternative_alignment_attractiveness=0.45<0.70 → avoids strategic_pivot
  // composite in [40,60) → high
  {
    entity_id: "GAF-003", alliance_type: "security_alliance", region: "NOAM",
    internal_cohesion_erosion: 0.55,            burden_sharing_imbalance: 0.48,
    strategic_interest_divergence: 0.50,        external_pressure_index: 0.52,
    defection_incentive_strength: 0.48,         alternative_alignment_attractiveness: 0.45,
    historical_grievance_activation: 0.50,      democratic_backsliding_within_alliance: 0.38,
    economic_decoupling_pressure: 0.42,         nuclear_deterrence_reliability: 0.40,
    intelligence_trust_deficit: 0.78,           sanctions_fatigue_index: 0.45,
    populist_alliance_skepticism: 0.42,         technology_rivalry_within_alliance: 0.40,
    leadership_legitimacy_crisis: 0.45,         treaty_obligation_strain: 0.72,
    multipolar_fragmentation_index: 0.50,
  },
  // GAF-004 — LATAM, regional_bloc → low, none
  // All low values → composite<20, no pattern triggered
  {
    entity_id: "GAF-004", alliance_type: "regional_bloc", region: "LATAM",
    internal_cohesion_erosion: 0.10,            burden_sharing_imbalance: 0.12,
    strategic_interest_divergence: 0.12,        external_pressure_index: 0.10,
    defection_incentive_strength: 0.10,         alternative_alignment_attractiveness: 0.10,
    historical_grievance_activation: 0.12,      democratic_backsliding_within_alliance: 0.10,
    economic_decoupling_pressure: 0.12,         nuclear_deterrence_reliability: 0.92,
    intelligence_trust_deficit: 0.10,           sanctions_fatigue_index: 0.10,
    populist_alliance_skepticism: 0.10,         technology_rivalry_within_alliance: 0.10,
    leadership_legitimacy_crisis: 0.10,         treaty_obligation_strain: 0.10,
    multipolar_fragmentation_index: 0.10,
  },
  // GAF-005 — MEA, energy_alliance → critical, strategic_pivot
  // alternative_alignment_attractiveness≥0.70 AND strategic_interest_divergence≥0.65 → strategic_pivot
  // internal_cohesion_erosion=0.60<0.70 → avoids alliance_dissolution
  // defection_incentive_strength=0.60<0.65 → avoids alliance_dissolution trigger
  // composite≥60 → critical
  {
    entity_id: "GAF-005", alliance_type: "energy_alliance", region: "MEA",
    internal_cohesion_erosion: 0.60,            burden_sharing_imbalance: 0.78,
    strategic_interest_divergence: 0.82,        external_pressure_index: 0.75,
    defection_incentive_strength: 0.60,         alternative_alignment_attractiveness: 0.85,
    historical_grievance_activation: 0.72,      democratic_backsliding_within_alliance: 0.60,
    economic_decoupling_pressure: 0.75,         nuclear_deterrence_reliability: 0.30,
    intelligence_trust_deficit: 0.65,           sanctions_fatigue_index: 0.70,
    populist_alliance_skepticism: 0.65,         technology_rivalry_within_alliance: 0.60,
    leadership_legitimacy_crisis: 0.70,         treaty_obligation_strain: 0.60,
    multipolar_fragmentation_index: 0.82,
  },
  // GAF-006 — EMEA, economic_alliance → moderate, none
  // composite in [20,40), no pattern triggered
  // All fields below thresholds
  {
    entity_id: "GAF-006", alliance_type: "economic_alliance", region: "EMEA",
    internal_cohesion_erosion: 0.32,            burden_sharing_imbalance: 0.25,
    strategic_interest_divergence: 0.28,        external_pressure_index: 0.30,
    defection_incentive_strength: 0.28,         alternative_alignment_attractiveness: 0.25,
    historical_grievance_activation: 0.28,      democratic_backsliding_within_alliance: 0.25,
    economic_decoupling_pressure: 0.22,         nuclear_deterrence_reliability: 0.70,
    intelligence_trust_deficit: 0.30,           sanctions_fatigue_index: 0.28,
    populist_alliance_skepticism: 0.28,         technology_rivalry_within_alliance: 0.25,
    leadership_legitimacy_crisis: 0.30,         treaty_obligation_strain: 0.28,
    multipolar_fragmentation_index: 0.30,
  },
  // GAF-007 — APAC, security_alliance → high, populist_defection
  // populist_alliance_skepticism≥0.70 AND leadership_legitimacy_crisis≥0.65 → populist_defection
  // internal_cohesion_erosion=0.55<0.70 → avoids alliance_dissolution
  // alternative_alignment_attractiveness=0.55<0.70 → avoids strategic_pivot
  // intelligence_trust_deficit=0.55<0.70 → avoids trust_collapse
  // composite in [40,60) → high
  {
    entity_id: "GAF-007", alliance_type: "security_alliance", region: "APAC",
    internal_cohesion_erosion: 0.55,            burden_sharing_imbalance: 0.48,
    strategic_interest_divergence: 0.52,        external_pressure_index: 0.50,
    defection_incentive_strength: 0.50,         alternative_alignment_attractiveness: 0.55,
    historical_grievance_activation: 0.52,      democratic_backsliding_within_alliance: 0.70,
    economic_decoupling_pressure: 0.45,         nuclear_deterrence_reliability: 0.50,
    intelligence_trust_deficit: 0.55,           sanctions_fatigue_index: 0.48,
    populist_alliance_skepticism: 0.78,         technology_rivalry_within_alliance: 0.50,
    leadership_legitimacy_crisis: 0.80,         treaty_obligation_strain: 0.50,
    multipolar_fragmentation_index: 0.60,
  },
  // GAF-008 — NOAM, tech_alliance → critical, economic_fracture
  // economic_decoupling_pressure≥0.70 AND technology_rivalry_within_alliance≥0.65 → economic_fracture
  // internal_cohesion_erosion=0.60<0.70 → avoids alliance_dissolution
  // strategic_interest_divergence=0.62<0.65 → avoids strategic_pivot
  // intelligence_trust_deficit=0.55<0.70 → avoids trust_collapse
  // populist_alliance_skepticism=0.55<0.70 → avoids populist_defection
  // composite≥60 → critical
  {
    entity_id: "GAF-008", alliance_type: "tech_alliance", region: "NOAM",
    internal_cohesion_erosion: 0.60,            burden_sharing_imbalance: 0.55,
    strategic_interest_divergence: 0.62,        external_pressure_index: 0.68,
    defection_incentive_strength: 0.60,         alternative_alignment_attractiveness: 0.55,
    historical_grievance_activation: 0.60,      democratic_backsliding_within_alliance: 0.58,
    economic_decoupling_pressure: 0.85,         nuclear_deterrence_reliability: 0.30,
    intelligence_trust_deficit: 0.55,           sanctions_fatigue_index: 0.62,
    populist_alliance_skepticism: 0.55,         technology_rivalry_within_alliance: 0.75,
    leadership_legitimacy_crisis: 0.55,         treaty_obligation_strain: 0.58,
    multipolar_fragmentation_index: 0.78,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

// ── Scoring functions (mirrors Python engine exactly) ──────────────────────────

function cohesionScore(e: Entity): number {
  return Math.round(
    (e.internal_cohesion_erosion * 0.4
      + e.strategic_interest_divergence * 0.35
      + e.burden_sharing_imbalance * 0.25) * 100 * 100) / 100;
}

function defectionScore(e: Entity): number {
  return Math.round(
    (e.defection_incentive_strength * 0.4
      + e.alternative_alignment_attractiveness * 0.35
      + e.economic_decoupling_pressure * 0.25) * 100 * 100) / 100;
}

function trustScore(e: Entity): number {
  return Math.round(
    (e.intelligence_trust_deficit * 0.4
      + e.treaty_obligation_strain * 0.35
      + (1 - e.nuclear_deterrence_reliability) * 0.25) * 100 * 100) / 100;
}

function legitimacyScore(e: Entity): number {
  return Math.round(
    (e.leadership_legitimacy_crisis * 0.4
      + e.populist_alliance_skepticism * 0.35
      + e.democratic_backsliding_within_alliance * 0.25) * 100 * 100) / 100;
}

function fractureComposite(coh: number, def: number, tru: number, leg: number): number {
  return Math.round((coh * 0.30 + def * 0.25 + tru * 0.25 + leg * 0.20) * 100) / 100;
}

function fractureRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function fracturePattern(e: Entity): string {
  if (e.internal_cohesion_erosion >= 0.70 && e.defection_incentive_strength >= 0.65) return "alliance_dissolution";
  if (e.alternative_alignment_attractiveness >= 0.70 && e.strategic_interest_divergence >= 0.65) return "strategic_pivot";
  if (e.intelligence_trust_deficit >= 0.70 && e.treaty_obligation_strain >= 0.65) return "trust_collapse";
  if (e.populist_alliance_skepticism >= 0.70 && e.leadership_legitimacy_crisis >= 0.65) return "populist_defection";
  if (e.economic_decoupling_pressure >= 0.70 && e.technology_rivalry_within_alliance >= 0.65) return "economic_fracture";
  return "none";
}

function fractureSeverity(comp: number): string {
  if (comp >= 75) return "alliance_emergency";
  if (comp >= 50) return "high_fracture_risk";
  if (comp >= 25) return "fracture_developing";
  return "alliance_stable";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "alliance_emergency_summit";
  if (risk === "high") {
    if (pattern === "strategic_pivot") return "realignment_containment";
    return "cohesion_reinforcement";
  }
  if (risk === "moderate") return "alliance_monitoring";
  return "no_action";
}

function fractureSignal(e: Entity, pattern: string, comp: number): string {
  if (comp < 20) {
    return "Alliance stable — cohésion interne préservée, confiance mutuelle maintenue, risques de fracture maîtrisés";
  }
  if (comp >= 60) {
    return `Fracture critique détectée — cohésion ${e.internal_cohesion_erosion.toFixed(2)} — défection ${e.defection_incentive_strength.toFixed(2)} — confiance ${e.intelligence_trust_deficit.toFixed(2)} — composite ${Math.round(comp)}`;
  }
  if (comp >= 40) {
    const labels: Record<string, string> = {
      alliance_dissolution: "Dissolution d'alliance",
      strategic_pivot:      "Pivot stratégique",
      trust_collapse:       "Effondrement de confiance",
      populist_defection:   "Défection populiste",
      economic_fracture:    "Fracture économique",
    };
    const label = labels[pattern] ?? pattern.replace(/_/g, " ");
    return `Risque de fracture élevé — ${label} — cohésion ${e.internal_cohesion_erosion.toFixed(2)} — défection ${e.defection_incentive_strength.toFixed(2)} — composite ${Math.round(comp)}`;
  }
  return `Fracture en développement — tensions observées — fragmentation multipolaire ${e.multipolar_fragmentation_index.toFixed(2)} — composite ${Math.round(comp)}`;
}

// ── GET handler ────────────────────────────────────────────────────────────────

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(
      sealResponse({ error: "SWARM_API_URL non configuré — service indisponible" }, "geopolitical-alliance-fracture-engine") as Record<string, unknown>,
      { status: 503 }
    );
  }

  try {
    const entities = MOCK_ENTITIES.map(e => {
      const coh  = cohesionScore(e);
      const def  = defectionScore(e);
      const tru  = trustScore(e);
      const leg  = legitimacyScore(e);
      const comp = fractureComposite(coh, def, tru, leg);
      const risk = fractureRisk(comp);
      const pat  = fracturePattern(e);
      const sev  = fractureSeverity(comp);
      const act  = recommendedAction(risk, pat);
      const sig  = fractureSignal(e, pat, comp);

      return {
        entity_id:                        e.entity_id,
        region:                           e.region,
        alliance_type:                    e.alliance_type,
        fracture_risk:                    risk,
        fracture_pattern:                 pat,
        fracture_severity:                sev,
        recommended_action:               act,
        cohesion_score:                   coh,
        defection_score:                  def,
        trust_score:                      tru,
        legitimacy_score:                 leg,
        fracture_composite:               comp,
        is_fracture_crisis:               comp >= 60,
        requires_fracture_intervention:   comp >= 40,
        fracture_signal:                  sig,
      };
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tCoh = 0, tDef = 0, tTru = 0, tLeg = 0, tComp = 0;
    let crisisC = 0, interventionC = 0;

    for (const ent of entities) {
      rc[ent.fracture_risk]      = (rc[ent.fracture_risk]      || 0) + 1;
      pc[ent.fracture_pattern]   = (pc[ent.fracture_pattern]   || 0) + 1;
      sc[ent.fracture_severity]  = (sc[ent.fracture_severity]  || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tCoh   += ent.cohesion_score;
      tDef   += ent.defection_score;
      tTru   += ent.trust_score;
      tLeg   += ent.legitimacy_score;
      tComp  += ent.fracture_composite;
      if (ent.is_fracture_crisis)             crisisC++;
      if (ent.requires_fracture_intervention) interventionC++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 10) / 10;

    const fractureCrisisEntities = entities.filter(e => e.is_fracture_crisis).map(e => e.entity_id);
    const dominantFracturePattern = Object.entries(pc).sort((a, b) => b[1] - a[1])[0]?.[0] ?? "none";

    const summary = {
      module:                          "Module 312",
      engine:                          "Geopolitical Alliance Fracture & Multipolar Realignment Intelligence Engine",
      analyst:                         "Chaima Mhadbi",
      location:                        "Bruxelles",
      total_entities_analyzed:         n,
      critical_fractures:              rc["critical"]  || 0,
      high_fractures:                  rc["high"]      || 0,
      moderate_fractures:              rc["moderate"]  || 0,
      stable_alliances:                rc["low"]       || 0,
      avg_estimated_fracture_index:    Math.round(avgComp / 100 * 10 * 100) / 100,
      fracture_crisis_entities:        fractureCrisisEntities,
      dominant_fracture_pattern:       dominantFracturePattern,
      risk_counts:                     rc,
      pattern_counts:                  pc,
      severity_counts:                 sc,
      action_counts:                   ac,
      avg_cohesion_score:              Math.round(tCoh  / n * 10) / 10,
      avg_defection_score:             Math.round(tDef  / n * 10) / 10,
      avg_trust_score:                 Math.round(tTru  / n * 10) / 10,
      avg_legitimacy_score:            Math.round(tLeg  / n * 10) / 10,
      avg_fracture_composite:          avgComp,
      fracture_crisis_count:           crisisC,
      requires_intervention_count:     interventionC,
    };

    return NextResponse.json(
      sealResponse({ entities, summary }, "geopolitical-alliance-fracture-engine") as Record<string, unknown>
    );
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Erreur moteur fracture alliance géopolitique" }, "geopolitical-alliance-fracture-engine") as Record<string, unknown>,
      { status: 502 }
    );
  }
}
