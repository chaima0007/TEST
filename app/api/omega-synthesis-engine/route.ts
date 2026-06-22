import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// Module 300 — OMEGA SYNTHESIS: Meta-Intelligence Convergence Engine
// Caelum Partners — Propriété exclusive de Chaima Mhadbi, Fondatrice Caelum Partners, Bruxelles.

const MOCK_ENTITIES = [
  // OS-001 — EMEA, strategic_convergence — critical, omega_convergence_crisis
  { id:"OS-001", intelligence_domain:"strategic_convergence", region:"EMEA",
    financial_intelligence_signal:0.88, geopolitical_intelligence_signal:0.85, technological_intelligence_signal:0.60,
    social_intelligence_signal:0.55, environmental_intelligence_signal:0.50, cognitive_intelligence_signal:0.62,
    quantum_intelligence_signal:0.55, biological_intelligence_signal:0.50, civilizational_intelligence_signal:0.58,
    existential_intelligence_signal:0.82, narrative_intelligence_signal:0.65, economic_intelligence_signal:0.80,
    governance_intelligence_signal:0.78, spatial_intelligence_signal:0.52, temporal_intelligence_signal:0.55,
    consciousness_intelligence_signal:0.60, sovereignty_synthesis_index:0.18 },
  // OS-002 — APAC, technological_synthesis — low, omega_equilibrium / none
  { id:"OS-002", intelligence_domain:"technological_synthesis", region:"APAC",
    financial_intelligence_signal:0.12, geopolitical_intelligence_signal:0.10, technological_intelligence_signal:0.15,
    social_intelligence_signal:0.10, environmental_intelligence_signal:0.12, cognitive_intelligence_signal:0.10,
    quantum_intelligence_signal:0.12, biological_intelligence_signal:0.10, civilizational_intelligence_signal:0.10,
    existential_intelligence_signal:0.08, narrative_intelligence_signal:0.10, economic_intelligence_signal:0.12,
    governance_intelligence_signal:0.10, spatial_intelligence_signal:0.10, temporal_intelligence_signal:0.10,
    consciousness_intelligence_signal:0.08, sovereignty_synthesis_index:0.92 },
  // OS-003 — NOAM, civilizational_analysis — high, technological_singularity_approach
  { id:"OS-003", intelligence_domain:"civilizational_analysis", region:"NOAM",
    financial_intelligence_signal:0.55, geopolitical_intelligence_signal:0.50, technological_intelligence_signal:0.82,
    social_intelligence_signal:0.48, environmental_intelligence_signal:0.45, cognitive_intelligence_signal:0.50,
    quantum_intelligence_signal:0.78, biological_intelligence_signal:0.72, civilizational_intelligence_signal:0.52,
    existential_intelligence_signal:0.55, narrative_intelligence_signal:0.48, economic_intelligence_signal:0.52,
    governance_intelligence_signal:0.50, spatial_intelligence_signal:0.48, temporal_intelligence_signal:0.50,
    consciousness_intelligence_signal:0.55, sovereignty_synthesis_index:0.48 },
  // OS-004 — LATAM, technological_synthesis — low, omega_equilibrium / none
  { id:"OS-004", intelligence_domain:"technological_synthesis", region:"LATAM",
    financial_intelligence_signal:0.18, geopolitical_intelligence_signal:0.15, technological_intelligence_signal:0.20,
    social_intelligence_signal:0.15, environmental_intelligence_signal:0.18, cognitive_intelligence_signal:0.15,
    quantum_intelligence_signal:0.18, biological_intelligence_signal:0.15, civilizational_intelligence_signal:0.18,
    existential_intelligence_signal:0.12, narrative_intelligence_signal:0.15, economic_intelligence_signal:0.18,
    governance_intelligence_signal:0.15, spatial_intelligence_signal:0.15, temporal_intelligence_signal:0.15,
    consciousness_intelligence_signal:0.12, sovereignty_synthesis_index:0.88 },
  // OS-005 — MEA, strategic_convergence — critical, civilizational_inflection
  { id:"OS-005", intelligence_domain:"strategic_convergence", region:"MEA",
    financial_intelligence_signal:0.78, geopolitical_intelligence_signal:0.75, technological_intelligence_signal:0.65,
    social_intelligence_signal:0.60, environmental_intelligence_signal:0.58, cognitive_intelligence_signal:0.68,
    quantum_intelligence_signal:0.55, biological_intelligence_signal:0.52, civilizational_intelligence_signal:0.80,
    existential_intelligence_signal:0.72, narrative_intelligence_signal:0.62, economic_intelligence_signal:0.72,
    governance_intelligence_signal:0.70, spatial_intelligence_signal:0.60, temporal_intelligence_signal:0.78,
    consciousness_intelligence_signal:0.82, sovereignty_synthesis_index:0.22 },
  // OS-006 — EMEA, geopolitical_synthesis — moderate, none
  { id:"OS-006", intelligence_domain:"geopolitical_synthesis", region:"EMEA",
    financial_intelligence_signal:0.38, geopolitical_intelligence_signal:0.42, technological_intelligence_signal:0.35,
    social_intelligence_signal:0.30, environmental_intelligence_signal:0.32, cognitive_intelligence_signal:0.35,
    quantum_intelligence_signal:0.30, biological_intelligence_signal:0.28, civilizational_intelligence_signal:0.32,
    existential_intelligence_signal:0.30, narrative_intelligence_signal:0.28, economic_intelligence_signal:0.35,
    governance_intelligence_signal:0.38, spatial_intelligence_signal:0.30, temporal_intelligence_signal:0.32,
    consciousness_intelligence_signal:0.30, sovereignty_synthesis_index:0.62 },
  // OS-007 — APAC, civilizational_analysis — high, sovereignty_erosion_cascade
  { id:"OS-007", intelligence_domain:"civilizational_analysis", region:"APAC",
    financial_intelligence_signal:0.52, geopolitical_intelligence_signal:0.55, technological_intelligence_signal:0.48,
    social_intelligence_signal:0.50, environmental_intelligence_signal:0.45, cognitive_intelligence_signal:0.72,
    quantum_intelligence_signal:0.42, biological_intelligence_signal:0.45, civilizational_intelligence_signal:0.50,
    existential_intelligence_signal:0.58, narrative_intelligence_signal:0.68, economic_intelligence_signal:0.50,
    governance_intelligence_signal:0.52, spatial_intelligence_signal:0.45, temporal_intelligence_signal:0.48,
    consciousness_intelligence_signal:0.52, sovereignty_synthesis_index:0.28 },
  // OS-008 — NOAM, strategic_convergence — critical, strategic_intelligence_gap
  { id:"OS-008", intelligence_domain:"strategic_convergence", region:"NOAM",
    financial_intelligence_signal:0.82, geopolitical_intelligence_signal:0.78, technological_intelligence_signal:0.55,
    social_intelligence_signal:0.50, environmental_intelligence_signal:0.45, cognitive_intelligence_signal:0.58,
    quantum_intelligence_signal:0.48, biological_intelligence_signal:0.45, civilizational_intelligence_signal:0.52,
    existential_intelligence_signal:0.60, narrative_intelligence_signal:0.55, economic_intelligence_signal:0.75,
    governance_intelligence_signal:0.72, spatial_intelligence_signal:0.50, temporal_intelligence_signal:0.48,
    consciousness_intelligence_signal:0.52, sovereignty_synthesis_index:0.35 },
];

type RawEntity = typeof MOCK_ENTITIES[0];

function strategicScore(e: RawEntity): number {
  const raw = (
    e.financial_intelligence_signal * 0.25
    + e.geopolitical_intelligence_signal * 0.25
    + e.economic_intelligence_signal * 0.25
    + e.governance_intelligence_signal * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function convergenceScore(e: RawEntity): number {
  const raw = (
    e.technological_intelligence_signal * 0.3
    + e.quantum_intelligence_signal * 0.25
    + e.biological_intelligence_signal * 0.25
    + e.spatial_intelligence_signal * 0.2
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function resilienceScore(e: RawEntity): number {
  const raw = (
    e.social_intelligence_signal * 0.3
    + e.environmental_intelligence_signal * 0.3
    + e.civilizational_intelligence_signal * 0.2
    + e.temporal_intelligence_signal * 0.2
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function sovereigntyScore(e: RawEntity): number {
  const raw = (
    e.cognitive_intelligence_signal * 0.3
    + e.existential_intelligence_signal * 0.25
    + e.narrative_intelligence_signal * 0.25
    + (1 - e.sovereignty_synthesis_index) * 0.2
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function omegaComposite(strat: number, conv: number, resil: number, sov: number): number {
  return Math.round((strat * 0.30 + conv * 0.25 + resil * 0.25 + sov * 0.20) * 100) / 100;
}

function omegaRisk(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}

function omegaPattern(e: RawEntity): string {
  const fin = e.financial_intelligence_signal;
  const geo = e.geopolitical_intelligence_signal;
  const ext = e.existential_intelligence_signal;
  const tech = e.technological_intelligence_signal;
  const quantum = e.quantum_intelligence_signal;
  const bio = e.biological_intelligence_signal;
  const civ = e.civilizational_intelligence_signal;
  const con = e.consciousness_intelligence_signal;
  const temp = e.temporal_intelligence_signal;
  const sov = e.sovereignty_synthesis_index;
  const narr = e.narrative_intelligence_signal;

  if ((fin + geo + ext) / 3 >= 0.70) return "omega_convergence_crisis";
  if ((tech + quantum + bio) / 3 >= 0.70) return "technological_singularity_approach";
  if ((civ + con + temp) / 3 >= 0.65) return "civilizational_inflection";
  if ((1 - sov) >= 0.65 && narr >= 0.60) return "sovereignty_erosion_cascade";
  if ((fin + geo) / 2 >= 0.70 && (1 - sov) >= 0.55) return "strategic_intelligence_gap";
  return "none";
}

function omegaSeverity(composite: number): string {
  if (composite >= 75) return "omega_emergency";
  if (composite >= 50) return "high_convergence_risk";
  if (composite >= 25) return "strategic_tension";
  return "omega_equilibrium";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "omega_strategic_reset";
  if (risk === "high" && pattern === "omega_convergence_crisis") return "convergence_war_room";
  if (risk === "high") return "strategic_intelligence_amplification";
  if (risk === "moderate") return "omega_monitoring";
  return "no_action";
}

function omegaSignal(e: RawEntity, risk: string, composite: number): string {
  const finPct  = Math.round(e.financial_intelligence_signal * 100);
  const geoPct  = Math.round(e.geopolitical_intelligence_signal * 100);
  const sovPct  = Math.round(e.sovereignty_synthesis_index * 100);
  const techPct = Math.round(e.technological_intelligence_signal * 100);
  const extPct  = Math.round(e.existential_intelligence_signal * 100);
  const compInt = Math.round(composite);

  if (risk === "critical") {
    return `OMEGA CRITIQUE — convergence intelligence ${compInt}% — financier ${finPct}% — géopolitique ${geoPct}% — souveraineté ${sovPct}%`;
  }
  if (risk === "high") {
    return `OMEGA ÉLEVÉ — convergence technologique ${techPct}% — signal existentiel ${extPct}% — composite ${compInt}`;
  }
  if (risk === "moderate") {
    return `OMEGA MODÉRÉ — tensions stratégiques ${compInt}% — vigilance Caelum Partners activée`;
  }
  return "OMEGA ÉQUILIBRE — tous les signaux d'intelligence convergent favorablement — Caelum Partners en position de force souveraine";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[omega-synthesis-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string,number> = {};
    const pc: Record<string,number> = {};
    const sc: Record<string,number> = {};
    const ac: Record<string,number> = {};
    let tComp=0, tStrat=0, tConv=0, tResil=0, tSov=0, crisisC=0, interventionC=0;

    for (const ent of entities) {
      rc[ent.omega_risk]       = (rc[ent.omega_risk]       || 0) + 1;
      pc[ent.omega_pattern]    = (pc[ent.omega_pattern]    || 0) + 1;
      sc[ent.omega_severity]   = (sc[ent.omega_severity]   || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tComp  += ent.omega_composite;
      tStrat += ent.strategic_score;
      tConv  += ent.convergence_score;
      tResil += ent.resilience_score;
      tSov   += ent.sovereignty_score;
      if (ent.is_in_omega_crisis)          crisisC++;
      if (ent.requires_omega_intervention) interventionC++;
    }

    const n = entities.length;
    const avgComp = tComp / n;
    const summary = {
      total:                        n,
      risk_counts:                  rc,
      pattern_counts:               pc,
      severity_counts:              sc,
      action_counts:                ac,
      avg_omega_composite:          Math.round(avgComp * 10) / 10,
      omega_crisis_count:           crisisC,
      omega_intervention_count:     interventionC,
      avg_strategic_score:          Math.round(tStrat / n * 10) / 10,
      avg_convergence_score:        Math.round(tConv  / n * 10) / 10,
      avg_resilience_score:         Math.round(tResil / n * 10) / 10,
      avg_sovereignty_score:        Math.round(tSov   / n * 10) / 10,
      avg_estimated_omega_index:    Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "omega-synthesis-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/omega-synthesis-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return sealResponse(NextResponse.json(sealResponse(data, "omega-synthesis-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "upstream_unavailable", message: "Le moteur OMEGA SYNTHESIS est temporairement inaccessible." }, "omega-synthesis-engine"),
      { status: 502 }
    ));
  }
}
