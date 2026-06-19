import { NextResponse } from "next/server";

const MOCK_GAMES = [
  // GM-001 pricing_war EMEA — critical / zero_sum_destruction
  { game_id:"GM-001", game_type:"pricing_war",             region:"EMEA",  nash_equilibrium_stability:0.08, dominant_strategy_clarity:0.72, cooperative_surplus_potential:0.10, defection_temptation_index:0.88, information_asymmetry_score:0.75, commitment_credibility_score:0.12, payoff_matrix_volatility:0.85, iteration_learning_rate:0.20, coalition_stability_score:0.10, threat_credibility_score:0.75, outside_option_strength:0.30, time_pressure_index:0.80, reputation_effect_weight:0.15, zero_sum_intensity:0.90, signaling_effectiveness:0.18, punishment_mechanism_strength:0.70, bargaining_power_score:0.55 },
  // GM-002 merger_negotiation NAMER — low
  { game_id:"GM-002", game_type:"merger_negotiation",      region:"NAMER", nash_equilibrium_stability:0.88, dominant_strategy_clarity:0.82, cooperative_surplus_potential:0.85, defection_temptation_index:0.15, information_asymmetry_score:0.18, commitment_credibility_score:0.90, payoff_matrix_volatility:0.12, iteration_learning_rate:0.88, coalition_stability_score:0.85, threat_credibility_score:0.80, outside_option_strength:0.70, time_pressure_index:0.20, reputation_effect_weight:0.88, zero_sum_intensity:0.10, signaling_effectiveness:0.85, punishment_mechanism_strength:0.80, bargaining_power_score:0.75 },
  // GM-003 market_entry APAC — high / prisoners_dilemma_trap
  { game_id:"GM-003", game_type:"market_entry",            region:"APAC",  nash_equilibrium_stability:0.22, dominant_strategy_clarity:0.52, cooperative_surplus_potential:0.48, defection_temptation_index:0.72, information_asymmetry_score:0.55, commitment_credibility_score:0.40, payoff_matrix_volatility:0.55, iteration_learning_rate:0.48, coalition_stability_score:0.42, threat_credibility_score:0.55, outside_option_strength:0.55, time_pressure_index:0.55, reputation_effect_weight:0.45, zero_sum_intensity:0.52, signaling_effectiveness:0.44, punishment_mechanism_strength:0.52, bargaining_power_score:0.48 },
  // GM-004 supply_chain_contract LATAM — low
  { game_id:"GM-004", game_type:"supply_chain_contract",   region:"LATAM", nash_equilibrium_stability:0.80, dominant_strategy_clarity:0.78, cooperative_surplus_potential:0.80, defection_temptation_index:0.18, information_asymmetry_score:0.20, commitment_credibility_score:0.85, payoff_matrix_volatility:0.15, iteration_learning_rate:0.82, coalition_stability_score:0.78, threat_credibility_score:0.75, outside_option_strength:0.65, time_pressure_index:0.22, reputation_effect_weight:0.82, zero_sum_intensity:0.12, signaling_effectiveness:0.80, punishment_mechanism_strength:0.78, bargaining_power_score:0.70 },
  // GM-005 regulatory_negotiation EMEA — critical / nash_deadlock
  { game_id:"GM-005", game_type:"regulatory_negotiation",  region:"EMEA",  nash_equilibrium_stability:0.22, dominant_strategy_clarity:0.35, cooperative_surplus_potential:0.28, defection_temptation_index:0.65, information_asymmetry_score:0.72, commitment_credibility_score:0.20, payoff_matrix_volatility:0.80, iteration_learning_rate:0.22, coalition_stability_score:0.20, threat_credibility_score:0.40, outside_option_strength:0.38, time_pressure_index:0.75, reputation_effect_weight:0.22, zero_sum_intensity:0.68, signaling_effectiveness:0.20, punishment_mechanism_strength:0.30, bargaining_power_score:0.42 },
  // GM-006 alliance_formation MEA — moderate
  { game_id:"GM-006", game_type:"alliance_formation",      region:"MEA",   nash_equilibrium_stability:0.60, dominant_strategy_clarity:0.62, cooperative_surplus_potential:0.65, defection_temptation_index:0.38, information_asymmetry_score:0.38, commitment_credibility_score:0.65, payoff_matrix_volatility:0.32, iteration_learning_rate:0.62, coalition_stability_score:0.60, threat_credibility_score:0.62, outside_option_strength:0.52, time_pressure_index:0.35, reputation_effect_weight:0.62, zero_sum_intensity:0.30, signaling_effectiveness:0.58, punishment_mechanism_strength:0.60, bargaining_power_score:0.55 },
  // GM-007 talent_competition NAMER — high / defection_cascade
  { game_id:"GM-007", game_type:"talent_competition",      region:"NAMER", nash_equilibrium_stability:0.40, dominant_strategy_clarity:0.48, cooperative_surplus_potential:0.42, defection_temptation_index:0.68, information_asymmetry_score:0.52, commitment_credibility_score:0.42, payoff_matrix_volatility:0.55, iteration_learning_rate:0.45, coalition_stability_score:0.30, threat_credibility_score:0.50, outside_option_strength:0.62, time_pressure_index:0.60, reputation_effect_weight:0.42, zero_sum_intensity:0.55, signaling_effectiveness:0.42, punishment_mechanism_strength:0.45, bargaining_power_score:0.48 },
  // GM-008 ip_licensing APAC — low
  { game_id:"GM-008", game_type:"ip_licensing",            region:"APAC",  nash_equilibrium_stability:0.82, dominant_strategy_clarity:0.80, cooperative_surplus_potential:0.82, defection_temptation_index:0.12, information_asymmetry_score:0.15, commitment_credibility_score:0.88, payoff_matrix_volatility:0.10, iteration_learning_rate:0.85, coalition_stability_score:0.80, threat_credibility_score:0.78, outside_option_strength:0.72, time_pressure_index:0.18, reputation_effect_weight:0.85, zero_sum_intensity:0.08, signaling_effectiveness:0.82, punishment_mechanism_strength:0.80, bargaining_power_score:0.75 },
];

type Game = typeof MOCK_GAMES[0];

function stabilityScore(g: Game): number {
  const raw = (1 - g.nash_equilibrium_stability) * 100 * 0.40
    + g.payoff_matrix_volatility * 100 * 0.35
    + (1 - g.commitment_credibility_score) * 100 * 0.25;
  return Math.min(Math.round(raw * 100) / 100, 100);
}
function strategyScore(g: Game): number {
  const raw = (1 - g.dominant_strategy_clarity) * 100 * 0.40
    + (1 - g.threat_credibility_score) * 100 * 0.35
    + (1 - g.punishment_mechanism_strength) * 100 * 0.25;
  return Math.min(Math.round(raw * 100) / 100, 100);
}
function cooperationScore(g: Game): number {
  const raw = (1 - g.cooperative_surplus_potential) * 100 * 0.40
    + (1 - g.coalition_stability_score) * 100 * 0.35
    + (1 - g.reputation_effect_weight) * 100 * 0.25;
  return Math.min(Math.round(raw * 100) / 100, 100);
}
function informationScore(g: Game): number {
  const raw = g.information_asymmetry_score * 100 * 0.40
    + (1 - g.signaling_effectiveness) * 100 * 0.35
    + (1 - g.iteration_learning_rate) * 100 * 0.25;
  return Math.min(Math.round(raw * 100) / 100, 100);
}
function composite(stab: number, strat: number, coop: number, info: number): number {
  return Math.min(Math.round((stab * 0.30 + strat * 0.25 + coop * 0.25 + info * 0.20) * 100) / 100, 100);
}
function gameRisk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function gamePattern(g: Game): string {
  if (g.zero_sum_intensity >= 0.75 && g.cooperative_surplus_potential <= 0.25) return "zero_sum_destruction";
  if (g.nash_equilibrium_stability <= 0.25 && g.defection_temptation_index >= 0.70) return "prisoners_dilemma_trap";
  if (g.nash_equilibrium_stability <= 0.30 && g.commitment_credibility_score <= 0.30) return "nash_deadlock";
  if (g.defection_temptation_index >= 0.65 && g.coalition_stability_score <= 0.35) return "defection_cascade";
  if (g.information_asymmetry_score >= 0.65 && g.signaling_effectiveness <= 0.35) return "information_warfare";
  return "none";
}
function gameSeverity(c: number): string { if (c >= 60) return "destructive"; if (c >= 40) return "unstable"; if (c >= 20) return "negotiating"; return "optimal"; }
function gameAction(r: string): string {
  if (r === "critical") return "emergency_mediation";
  if (r === "high")     return "commitment_device";
  if (r === "moderate") return "strategy_monitoring";
  return "no_action";
}
function gameActionSecondary(r: string): string {
  if (r === "critical") return "game_reset";
  if (r === "high")     return "coalition_building";
  if (r === "moderate") return "strategy_monitoring";
  return "no_action";
}
function gameSignal(g: Game, pattern: string, comp: number): string {
  if (comp < 20) return "Équilibre de Nash optimal — stratégie dominante claire, coopération stable, information équilibrée";
  const labels: Record<string,string> = {
    prisoners_dilemma_trap: "Piège du dilemme du prisonnier",
    nash_deadlock:          "Blocage de Nash",
    defection_cascade:      "Cascade de défection",
    information_warfare:    "Guerre de l'information",
    zero_sum_destruction:   "Destruction somme nulle",
  };
  const label = labels[pattern] ?? pattern.replace(/_/g, " ");
  return `${label} — équilibre Nash ${g.nash_equilibrium_stability.toFixed(2)} — surplus coopératif ${g.cooperative_surplus_potential.toFixed(2)} — tentation défection ${g.defection_temptation_index.toFixed(2)} — composite ${Math.round(comp)}`;
}
function gameLossIndex(comp: number, nashStability: number): number {
  return Math.min(Math.round(comp / 100 * (1 - nashStability + 0.01) * 10 * 100) / 100, 10.0);
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const games = MOCK_GAMES.map(g => {
      const stab = stabilityScore(g), strat = strategyScore(g), coop = cooperationScore(g), info = informationScore(g);
      const comp = composite(stab, strat, coop, info);
      const risk = gameRisk(comp), pat = gamePattern(g), sev = gameSeverity(comp);
      const act = gameAction(risk), actSec = gameActionSecondary(risk);
      return {
        game_id: g.game_id, game_type: g.game_type, region: g.region,
        stability_score: stab, strategy_score: strat, cooperation_score: coop, information_score: info,
        game_composite: comp, game_risk: risk, game_pattern: pat, game_severity: sev,
        recommended_action: act, recommended_action_secondary: actSec,
        game_signal: gameSignal(g, pat, comp),
        estimated_game_loss_index: gameLossIndex(comp, g.nash_equilibrium_stability),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tStab=0, tStrat=0, tCoop=0, tInfo=0, tComp=0, tGli=0, destructiveC=0, mediationC=0;
    for (const g of games) {
      rc[g.game_risk]     = (rc[g.game_risk]     || 0) + 1;
      pc[g.game_pattern]  = (pc[g.game_pattern]  || 0) + 1;
      sc[g.game_severity] = (sc[g.game_severity] || 0) + 1;
      ac[g.recommended_action] = (ac[g.recommended_action] || 0) + 1;
      tStab += g.stability_score; tStrat += g.strategy_score;
      tCoop += g.cooperation_score; tInfo += g.information_score;
      tComp += g.game_composite; tGli += g.estimated_game_loss_index;
      if (g.game_severity === "destructive") destructiveC++;
      if (g.recommended_action === "emergency_mediation") mediationC++;
    }
    const n = games.length;
    return NextResponse.json({ games, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_game_composite: Math.round(tComp / n * 10) / 10,
      destructive_count: destructiveC, mediation_required_count: mediationC,
      avg_stability_score:    Math.round(tStab  / n * 10) / 10,
      avg_strategy_score:     Math.round(tStrat / n * 10) / 10,
      avg_cooperation_score:  Math.round(tCoop  / n * 10) / 10,
      avg_information_score:  Math.round(tInfo  / n * 10) / 10,
      avg_estimated_game_loss_index: Math.round(tGli / n * 100) / 100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/game-theory-decision-engine`)).json());
}
