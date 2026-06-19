import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockScenarios = [
  {
    scenario_id: "FS-001", region: "EMEA",
    foresight_risk: "critical", scenario_pattern: "black_swan", foresight_severity: "blind_spot",
    recommended_action: "emergency_replan",
    signal_score: 100.0, readiness_score: 100.0, simulation_score: 100.0, exposure_score: 100.0,
    foresight_composite: 100.0, has_blind_spot_risk: true, requires_immediate_simulation: true,
    estimated_scenario_risk_index: 9.6,
    foresight_signal: "Critical — détection signaux 5% — préparation 5% — résilience 5% — composite 100",
  },
  {
    scenario_id: "FS-008", region: "MEA",
    foresight_risk: "critical", scenario_pattern: "black_swan", foresight_severity: "blind_spot",
    recommended_action: "emergency_replan",
    signal_score: 100.0, readiness_score: 100.0, simulation_score: 100.0, exposure_score: 100.0,
    foresight_composite: 100.0, has_blind_spot_risk: true, requires_immediate_simulation: true,
    estimated_scenario_risk_index: 7.9,
    foresight_signal: "Critical — détection signaux 22% — préparation 18% — résilience 20% — composite 100",
  },
  {
    scenario_id: "FS-005", region: "EMEA",
    foresight_risk: "critical", scenario_pattern: "black_swan", foresight_severity: "blind_spot",
    recommended_action: "emergency_replan",
    signal_score: 100.0, readiness_score: 100.0, simulation_score: 100.0, exposure_score: 68.0,
    foresight_composite: 93.6, has_blind_spot_risk: true, requires_immediate_simulation: true,
    estimated_scenario_risk_index: 7.11,
    foresight_signal: "Critical — détection signaux 20% — préparation 20% — résilience 20% — composite 94",
  },
  {
    scenario_id: "FS-007", region: "APAC",
    foresight_risk: "critical", scenario_pattern: "none", foresight_severity: "blind_spot",
    recommended_action: "crisis_simulation",
    signal_score: 53.0, readiness_score: 69.0, simulation_score: 70.0, exposure_score: 52.0,
    foresight_composite: 61.05, has_blind_spot_risk: true, requires_immediate_simulation: true,
    estimated_scenario_risk_index: 3.72,
    foresight_signal: "Critical — détection signaux 40% — préparation 40% — résilience 35% — composite 61",
  },
  {
    scenario_id: "FS-003", region: "APAC",
    foresight_risk: "high", scenario_pattern: "none", foresight_severity: "vulnerable",
    recommended_action: "contingency_activation",
    signal_score: 53.0, readiness_score: 52.0, simulation_score: 40.0, exposure_score: 38.0,
    foresight_composite: 46.5, has_blind_spot_risk: true, requires_immediate_simulation: true,
    estimated_scenario_risk_index: 3.07,
    foresight_signal: "High — détection signaux 35% — préparation 35% — résilience 30% — composite 46",
  },
  {
    scenario_id: "FS-006", region: "NAMER",
    foresight_risk: "moderate", scenario_pattern: "none", foresight_severity: "monitoring",
    recommended_action: "strategic_hedge",
    signal_score: 32.0, readiness_score: 21.0, simulation_score: 34.0, exposure_score: 27.0,
    foresight_composite: 28.75, has_blind_spot_risk: false, requires_immediate_simulation: true,
    estimated_scenario_risk_index: 1.32,
    foresight_signal: "Moderate — détection signaux 55% — préparation 52% — résilience 50% — composite 29",
  },
  {
    scenario_id: "FS-004", region: "LATAM",
    foresight_risk: "low", scenario_pattern: "none", foresight_severity: "prepared",
    recommended_action: "no_action",
    signal_score: 7.0, readiness_score: 12.0, simulation_score: 9.0, exposure_score: 0.0,
    foresight_composite: 7.35, has_blind_spot_risk: false, requires_immediate_simulation: false,
    estimated_scenario_risk_index: 0.23,
    foresight_signal: "Anticipation stratégique robuste — signaux bien captés, scénarios maîtrisés, capacité adaptative forte",
  },
  {
    scenario_id: "FS-002", region: "NAMER",
    foresight_risk: "low", scenario_pattern: "black_swan", foresight_severity: "prepared",
    recommended_action: "no_action",
    signal_score: 0.0, readiness_score: 0.0, simulation_score: 25.0, exposure_score: 0.0,
    foresight_composite: 6.25, has_blind_spot_risk: true, requires_immediate_simulation: false,
    estimated_scenario_risk_index: 0.1,
    foresight_signal: "Anticipation stratégique robuste — signaux bien captés, scénarios maîtrisés, capacité adaptative forte",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (!process.env.SWARM_API_URL) {
    // mock computation path
    let scenarios = [...mockScenarios];
    if (risk)    scenarios = scenarios.filter((s) => s.foresight_risk === risk);
    if (pattern) scenarios = scenarios.filter((s) => s.scenario_pattern === pattern);

    const risk_counts:     Record<string, number> = {};
    const pattern_counts:  Record<string, number> = {};
    const severity_counts: Record<string, number> = {};
    const action_counts:   Record<string, number> = {};
    let total_comp = 0, total_sig = 0, total_read = 0, total_sim = 0, total_exp = 0, total_idx = 0;

    for (const s of mockScenarios) {
      risk_counts[s.foresight_risk]         = (risk_counts[s.foresight_risk] || 0) + 1;
      pattern_counts[s.scenario_pattern]    = (pattern_counts[s.scenario_pattern] || 0) + 1;
      severity_counts[s.foresight_severity] = (severity_counts[s.foresight_severity] || 0) + 1;
      action_counts[s.recommended_action]   = (action_counts[s.recommended_action] || 0) + 1;
      total_comp += s.foresight_composite;
      total_sig  += s.signal_score;
      total_read += s.readiness_score;
      total_sim  += s.simulation_score;
      total_exp  += s.exposure_score;
      total_idx  += s.estimated_scenario_risk_index;
    }

    const n = mockScenarios.length;
    return NextResponse.json({
      scenarios,
      summary: {
        total:                              n,
        risk_counts,
        pattern_counts,
        severity_counts,
        action_counts,
        avg_foresight_composite:            Math.round((total_comp / n) * 100) / 100,
        blind_spot_risk_count:              mockScenarios.filter((s) => s.has_blind_spot_risk).length,
        immediate_simulation_count:         mockScenarios.filter((s) => s.requires_immediate_simulation).length,
        avg_signal_score:                   Math.round((total_sig  / n) * 100) / 100,
        avg_readiness_score:                Math.round((total_read / n) * 100) / 100,
        avg_simulation_score:               Math.round((total_sim  / n) * 100) / 100,
        avg_exposure_score:                 Math.round((total_exp  / n) * 100) / 100,
        avg_estimated_scenario_risk_index:  Math.round((total_idx  / n) * 100) / 100,
      },
    });
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/strategic-foresight-simulation-engine`);
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(await res.json());
  } catch {}

  return NextResponse.json({ scenarios: [], summary: {} }, { status: 502 });
}
