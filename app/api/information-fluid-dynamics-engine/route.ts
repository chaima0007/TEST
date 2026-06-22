import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ─── Scoring helpers ──────────────────────────────────────────────────────────

function turbulenceScore(
  turbulence_coefficient: number,
  reynolds_number_analog: number,
  vortex_formation_risk: number,
): number {
  let s = 0;
  if      (turbulence_coefficient >= 0.70) s += 40;
  else if (turbulence_coefficient >= 0.50) s += 22;
  else if (turbulence_coefficient >= 0.30) s += 8;

  if      (reynolds_number_analog >= 0.75) s += 35;
  else if (reynolds_number_analog >= 0.55) s += 18;
  else if (reynolds_number_analog >= 0.35) s += 6;

  if      (vortex_formation_risk >= 0.65) s += 25;
  else if (vortex_formation_risk >= 0.45) s += 12;
  return Math.min(s, 100);
}

function entropyScore(
  entropy_level: number,
  fractal_dimension_risk: number,
  butterfly_effect_sensitivity: number,
): number {
  let s = 0;
  if      (entropy_level >= 0.70) s += 40;
  else if (entropy_level >= 0.50) s += 22;
  else if (entropy_level >= 0.30) s += 8;

  if      (fractal_dimension_risk >= 0.70) s += 35;
  else if (fractal_dimension_risk >= 0.50) s += 18;
  else if (fractal_dimension_risk >= 0.30) s += 6;

  if      (butterfly_effect_sensitivity >= 0.70) s += 25;
  else if (butterfly_effect_sensitivity >= 0.50) s += 12;
  return Math.min(s, 100);
}

function flowScore(
  information_viscosity: number,
  laminar_flow_efficiency: number,
  bifurcation_proximity: number,
): number {
  let s = 0;
  if      (information_viscosity >= 0.70) s += 40;
  else if (information_viscosity >= 0.50) s += 22;
  else if (information_viscosity >= 0.30) s += 8;

  const inv_lfe = 1.0 - laminar_flow_efficiency;
  if      (inv_lfe >= 0.70) s += 35;
  else if (inv_lfe >= 0.50) s += 18;
  else if (inv_lfe >= 0.30) s += 6;

  if      (bifurcation_proximity >= 0.70) s += 25;
  else if (bifurcation_proximity >= 0.50) s += 12;
  return Math.min(s, 100);
}

function resilienceScore(
  attractor_stability_score: number,
  resilience_basin_depth: number,
  chaos_recovery_speed: number,
): number {
  let s = 0;
  const inv_att = 1.0 - attractor_stability_score;
  if      (inv_att >= 0.70) s += 40;
  else if (inv_att >= 0.50) s += 22;
  else if (inv_att >= 0.30) s += 8;

  const inv_rbd = 1.0 - resilience_basin_depth;
  if      (inv_rbd >= 0.70) s += 35;
  else if (inv_rbd >= 0.50) s += 18;
  else if (inv_rbd >= 0.30) s += 6;

  const inv_crs = 1.0 - chaos_recovery_speed;
  if      (inv_crs >= 0.70) s += 25;
  else if (inv_crs >= 0.50) s += 12;
  return Math.min(s, 100);
}

function compositeScore(turb: number, entr: number, flow: number, res: number): number {
  return Math.min(Math.round((turb * 0.30 + entr * 0.25 + flow * 0.25 + res * 0.20) * 100) / 100, 100);
}

function chaosIndex(composite: number, attractor_stability_score: number): number {
  return Math.round(Math.min((composite / 100) * (1 - attractor_stability_score + 0.01) * 10, 10) * 100) / 100;
}

// ─── Mock systems ─────────────────────────────────────────────────────────────

const MOCK_SYSTEMS = [
  // IFD-001: company, EMEA → critical, turbulent_cascade
  {
    system_id: "IFD-001", system_type: "information_market", region: "EMEA",
    flow_velocity_index: 0.22, turbulence_coefficient: 0.88, entropy_level: 0.75,
    bifurcation_proximity: 0.70, information_viscosity: 0.80, attractor_stability_score: 0.10,
    vortex_formation_risk: 0.78, laminar_flow_efficiency: 0.12, reynolds_number_analog: 0.82,
    phase_transition_readiness: 0.45, dissipative_structure_score: 0.20, strange_attractor_detection: 0.55,
    fractal_dimension_risk: 0.72, butterfly_effect_sensitivity: 0.80, self_organization_capacity: 0.15,
    resilience_basin_depth: 0.10, chaos_recovery_speed: 0.08,
    chaos_risk: "critical", chaos_pattern: "turbulent_cascade", flow_severity: "chaotic",
    recommended_action: "chaos_containment",
  },
  // IFD-002: division, NAMER → low, laminar
  {
    system_id: "IFD-002", system_type: "organizational_network", region: "NAMER",
    flow_velocity_index: 0.90, turbulence_coefficient: 0.08, entropy_level: 0.10,
    bifurcation_proximity: 0.05, information_viscosity: 0.08, attractor_stability_score: 0.92,
    vortex_formation_risk: 0.06, laminar_flow_efficiency: 0.92, reynolds_number_analog: 0.07,
    phase_transition_readiness: 0.80, dissipative_structure_score: 0.88, strange_attractor_detection: 0.05,
    fractal_dimension_risk: 0.08, butterfly_effect_sensitivity: 0.07, self_organization_capacity: 0.90,
    resilience_basin_depth: 0.92, chaos_recovery_speed: 0.90,
    chaos_risk: "low", chaos_pattern: "none", flow_severity: "laminar",
    recommended_action: "no_action",
  },
  // IFD-003: subsidiary, APAC → high, entropy_collapse
  {
    system_id: "IFD-003", system_type: "supply_flow", region: "APAC",
    flow_velocity_index: 0.38, turbulence_coefficient: 0.52, entropy_level: 0.78,
    bifurcation_proximity: 0.55, information_viscosity: 0.60, attractor_stability_score: 0.30,
    vortex_formation_risk: 0.48, laminar_flow_efficiency: 0.35, reynolds_number_analog: 0.58,
    phase_transition_readiness: 0.55, dissipative_structure_score: 0.30, strange_attractor_detection: 0.42,
    fractal_dimension_risk: 0.72, butterfly_effect_sensitivity: 0.65, self_organization_capacity: 0.35,
    resilience_basin_depth: 0.28, chaos_recovery_speed: 0.30,
    chaos_risk: "high", chaos_pattern: "entropy_collapse", flow_severity: "turbulent",
    recommended_action: "entropy_reduction",
  },
  // IFD-004: jv, LATAM → low, transitional
  {
    system_id: "IFD-004", system_type: "capital_stream", region: "LATAM",
    flow_velocity_index: 0.72, turbulence_coefficient: 0.18, entropy_level: 0.22,
    bifurcation_proximity: 0.20, information_viscosity: 0.18, attractor_stability_score: 0.78,
    vortex_formation_risk: 0.15, laminar_flow_efficiency: 0.78, reynolds_number_analog: 0.15,
    phase_transition_readiness: 0.68, dissipative_structure_score: 0.72, strange_attractor_detection: 0.12,
    fractal_dimension_risk: 0.20, butterfly_effect_sensitivity: 0.18, self_organization_capacity: 0.75,
    resilience_basin_depth: 0.80, chaos_recovery_speed: 0.78,
    chaos_risk: "low", chaos_pattern: "none", flow_severity: "transitional",
    recommended_action: "no_action",
  },
  // IFD-005: company, EMEA → critical, bifurcation_crisis
  {
    system_id: "IFD-005", system_type: "social_cascade", region: "EMEA",
    flow_velocity_index: 0.30, turbulence_coefficient: 0.60, entropy_level: 0.68,
    bifurcation_proximity: 0.88, information_viscosity: 0.72, attractor_stability_score: 0.12,
    vortex_formation_risk: 0.58, laminar_flow_efficiency: 0.20, reynolds_number_analog: 0.65,
    phase_transition_readiness: 0.80, dissipative_structure_score: 0.22, strange_attractor_detection: 0.60,
    fractal_dimension_risk: 0.65, butterfly_effect_sensitivity: 0.70, self_organization_capacity: 0.20,
    resilience_basin_depth: 0.12, chaos_recovery_speed: 0.10,
    chaos_risk: "critical", chaos_pattern: "bifurcation_crisis", flow_severity: "chaotic",
    recommended_action: "flow_restructuring",
  },
  // IFD-006: division, NAMER → moderate, none
  {
    system_id: "IFD-006", system_type: "regulatory_pipeline", region: "NAMER",
    flow_velocity_index: 0.58, turbulence_coefficient: 0.32, entropy_level: 0.35,
    bifurcation_proximity: 0.28, information_viscosity: 0.32, attractor_stability_score: 0.62,
    vortex_formation_risk: 0.28, laminar_flow_efficiency: 0.62, reynolds_number_analog: 0.30,
    phase_transition_readiness: 0.55, dissipative_structure_score: 0.58, strange_attractor_detection: 0.25,
    fractal_dimension_risk: 0.32, butterfly_effect_sensitivity: 0.30, self_organization_capacity: 0.60,
    resilience_basin_depth: 0.60, chaos_recovery_speed: 0.62,
    chaos_risk: "moderate", chaos_pattern: "none", flow_severity: "transitional",
    recommended_action: "flow_monitoring",
  },
  // IFD-007: subsidiary, APAC → high, vortex_lock
  {
    system_id: "IFD-007", system_type: "innovation_diffusion", region: "APAC",
    flow_velocity_index: 0.35, turbulence_coefficient: 0.55, entropy_level: 0.55,
    bifurcation_proximity: 0.48, information_viscosity: 0.68, attractor_stability_score: 0.32,
    vortex_formation_risk: 0.78, laminar_flow_efficiency: 0.28, reynolds_number_analog: 0.55,
    phase_transition_readiness: 0.48, dissipative_structure_score: 0.35, strange_attractor_detection: 0.50,
    fractal_dimension_risk: 0.52, butterfly_effect_sensitivity: 0.55, self_organization_capacity: 0.30,
    resilience_basin_depth: 0.30, chaos_recovery_speed: 0.32,
    chaos_risk: "high", chaos_pattern: "vortex_lock", flow_severity: "turbulent",
    recommended_action: "attractor_stabilization",
  },
  // IFD-008: jv, MEA → critical, strange_attractor_trap
  {
    system_id: "IFD-008", system_type: "knowledge_vortex", region: "MEA",
    flow_velocity_index: 0.25, turbulence_coefficient: 0.72, entropy_level: 0.70,
    bifurcation_proximity: 0.75, information_viscosity: 0.75, attractor_stability_score: 0.08,
    vortex_formation_risk: 0.70, laminar_flow_efficiency: 0.15, reynolds_number_analog: 0.78,
    phase_transition_readiness: 0.70, dissipative_structure_score: 0.18, strange_attractor_detection: 0.80,
    fractal_dimension_risk: 0.75, butterfly_effect_sensitivity: 0.72, self_organization_capacity: 0.12,
    resilience_basin_depth: 0.08, chaos_recovery_speed: 0.10,
    chaos_risk: "critical", chaos_pattern: "strange_attractor_trap", flow_severity: "chaotic",
    recommended_action: "flow_restructuring",
  },
] as const;

type MockSystem = typeof MOCK_SYSTEMS[number];

function computeSystem(s: MockSystem) {
  const turb  = turbulenceScore(s.turbulence_coefficient, s.reynolds_number_analog, s.vortex_formation_risk);
  const entr  = entropyScore(s.entropy_level, s.fractal_dimension_risk, s.butterfly_effect_sensitivity);
  const flow  = flowScore(s.information_viscosity, s.laminar_flow_efficiency, s.bifurcation_proximity);
  const res   = resilienceScore(s.attractor_stability_score, s.resilience_basin_depth, s.chaos_recovery_speed);
  const comp  = compositeScore(turb, entr, flow, res);
  const cidx  = chaosIndex(comp, s.attractor_stability_score);
  const signal = (() => {
    if (comp < 20) return "Flux laminaire stable — dynamique fluide équilibrée, attracteurs stables, entropie maîtrisée";
    const LABELS: Record<string, string> = {
      turbulent_cascade:      "Cascade turbulente",
      entropy_collapse:        "Effondrement entropique",
      bifurcation_crisis:      "Crise de bifurcation",
      vortex_lock:             "Verrouillage vortex",
      strange_attractor_trap:  "Piège attracteur étrange",
    };
    const label = LABELS[s.chaos_pattern] ?? s.chaos_pattern;
    return `${label} — coefficient Reynolds ${s.reynolds_number_analog.toFixed(2)} — proximité bifurcation ${Math.round(s.bifurcation_proximity * 100)}% — entropie composite ${Math.round(comp)}`;
  })();

  return {
    system_id:              s.system_id,
    system_type:            s.system_type,
    region:                 s.region,
    chaos_risk:             s.chaos_risk,
    chaos_pattern:          s.chaos_pattern,
    flow_severity:          s.flow_severity,
    recommended_action:     s.recommended_action,
    turbulence_score:       turb,
    entropy_score:          entr,
    flow_score:             flow,
    resilience_score:       res,
    chaos_composite:        comp,
    has_chaos_signal:       (comp >= 40 || s.turbulence_coefficient >= 0.60 || s.bifurcation_proximity >= 0.65 || s.entropy_level >= 0.60),
    requires_restructuring: (comp >= 25 || s.reynolds_number_analog >= 0.65 || s.information_viscosity >= 0.65 || s.vortex_formation_risk >= 0.65),
    estimated_chaos_index:  cidx,
    chaos_signal:           signal,
  };
}

// ─── GET handler ──────────────────────────────────────────────────────────────

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (!process.env.SWARM_API_URL) {
  console.warn("[information-fluid-dynamics-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    const pattern_counts:  Record<string, number> = {};
    const severity_counts: Record<string, number> = {};
    const action_counts:   Record<string, number> = {};
    let total_comp = 0, total_turb = 0, total_entr = 0, total_flow = 0, total_res = 0, total_idx = 0;
    let chaos_signal_count = 0, restruct_count = 0;

    for (const s of allSystems) {
      risk_counts[s.chaos_risk]        = (risk_counts[s.chaos_risk] || 0) + 1;
      pattern_counts[s.chaos_pattern]  = (pattern_counts[s.chaos_pattern] || 0) + 1;
      severity_counts[s.flow_severity] = (severity_counts[s.flow_severity] || 0) + 1;
      action_counts[s.recommended_action] = (action_counts[s.recommended_action] || 0) + 1;
      total_comp += s.chaos_composite;
      total_turb += s.turbulence_score;
      total_entr += s.entropy_score;
      total_flow += s.flow_score;
      total_res  += s.resilience_score;
      total_idx  += s.estimated_chaos_index;
      if (s.has_chaos_signal)       chaos_signal_count++;
      if (s.requires_restructuring) restruct_count++;
    }

    const n = allSystems.length;

    return sealResponse(NextResponse.json(sealResponse({
      systems,
      summary: {
        total:                         n,
        risk_counts,
        pattern_counts,
        severity_counts,
        action_counts,
        avg_estimated_chaos_index:     Math.round((total_idx  / n) * 100) / 100,
        chaos_signal_count,
        restructuring_required_count:  restruct_count,
        avg_turbulence_score:          Math.round((total_turb / n) * 10) / 10,
        avg_entropy_score:             Math.round((total_entr / n) * 10) / 10,
        avg_flow_score:                Math.round((total_flow / n) * 10) / 10,
        avg_resilience_score:          Math.round((total_res  / n) * 10) / 10,
        avg_chaos_composite:           Math.round((total_comp / n) * 10) / 10,
      },
    } as Record<string, unknown>, "information-fluid-dynamics-engine") as Parameters<typeof NextResponse.json>[0]));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/information-fluid-dynamics-engine`);
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(sealResponse(await res.json(), "information-fluid-dynamics-engine") as Parameters<typeof NextResponse.json>[0]));
  } catch {}

  return sealResponse(NextResponse.json(sealResponse({ systems: [], summary: {} }, "information-fluid-dynamics-engine") as Parameters<typeof NextResponse.json>[0], { status: 502 }));
}
