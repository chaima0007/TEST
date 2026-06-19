import { NextResponse } from "next/server";

const MOCK_TERRITORIES = [
  // GT-001 sanctions_zone EMEA — critical/sanctions_cascade
  { territory_id:"GT-001", territory_type:"sanctions_zone",     region:"EMEA",  political_stability_score:0.18, sanctions_exposure_risk:0.88, diplomatic_relationship_quality:0.12, trade_agreement_coverage:0.10, regulatory_alignment_score:0.15, conflict_proximity_index:0.55, supply_chain_geopolitical_risk:0.82, currency_sovereignty_risk:0.75, institutional_quality_score:0.20, anti_corruption_score:0.18, press_freedom_index:0.15, rule_of_law_score:0.20, foreign_investment_protection:0.15, bilateral_tension_index:0.80, technology_decoupling_risk:0.72, energy_dependency_risk:0.65, democratic_resilience_score:0.15 },
  // GT-002 regulatory_union NAMER — low/stable
  { territory_id:"GT-002", territory_type:"regulatory_union",   region:"NAMER", political_stability_score:0.88, sanctions_exposure_risk:0.05, diplomatic_relationship_quality:0.92, trade_agreement_coverage:0.90, regulatory_alignment_score:0.92, conflict_proximity_index:0.05, supply_chain_geopolitical_risk:0.08, currency_sovereignty_risk:0.10, institutional_quality_score:0.90, anti_corruption_score:0.88, press_freedom_index:0.92, rule_of_law_score:0.90, foreign_investment_protection:0.92, bilateral_tension_index:0.08, technology_decoupling_risk:0.05, energy_dependency_risk:0.10, democratic_resilience_score:0.90 },
  // GT-003 emerging_market APAC — high/regulatory_decoupling
  { territory_id:"GT-003", territory_type:"emerging_market",    region:"APAC",  political_stability_score:0.48, sanctions_exposure_risk:0.40, diplomatic_relationship_quality:0.45, trade_agreement_coverage:0.52, regulatory_alignment_score:0.28, conflict_proximity_index:0.35, supply_chain_geopolitical_risk:0.55, currency_sovereignty_risk:0.48, institutional_quality_score:0.45, anti_corruption_score:0.42, press_freedom_index:0.40, rule_of_law_score:0.45, foreign_investment_protection:0.40, bilateral_tension_index:0.52, technology_decoupling_risk:0.62, energy_dependency_risk:0.50, democratic_resilience_score:0.45 },
  // GT-004 diplomatic_hub LATAM — low/stable
  { territory_id:"GT-004", territory_type:"diplomatic_hub",     region:"LATAM", political_stability_score:0.78, sanctions_exposure_risk:0.08, diplomatic_relationship_quality:0.85, trade_agreement_coverage:0.80, regulatory_alignment_score:0.78, conflict_proximity_index:0.10, supply_chain_geopolitical_risk:0.15, currency_sovereignty_risk:0.22, institutional_quality_score:0.75, anti_corruption_score:0.70, press_freedom_index:0.78, rule_of_law_score:0.75, foreign_investment_protection:0.80, bilateral_tension_index:0.12, technology_decoupling_risk:0.12, energy_dependency_risk:0.20, democratic_resilience_score:0.80 },
  // GT-005 conflict_adjacent EMEA — critical/conflict_spillover
  { territory_id:"GT-005", territory_type:"conflict_adjacent",  region:"EMEA",  political_stability_score:0.22, sanctions_exposure_risk:0.58, diplomatic_relationship_quality:0.25, trade_agreement_coverage:0.30, regulatory_alignment_score:0.32, conflict_proximity_index:0.82, supply_chain_geopolitical_risk:0.78, currency_sovereignty_risk:0.68, institutional_quality_score:0.30, anti_corruption_score:0.28, press_freedom_index:0.25, rule_of_law_score:0.28, foreign_investment_protection:0.25, bilateral_tension_index:0.62, technology_decoupling_risk:0.55, energy_dependency_risk:0.72, democratic_resilience_score:0.22 },
  // GT-006 bilateral_trade MEA — moderate
  { territory_id:"GT-006", territory_type:"bilateral_trade",    region:"MEA",   political_stability_score:0.65, sanctions_exposure_risk:0.28, diplomatic_relationship_quality:0.62, trade_agreement_coverage:0.60, regulatory_alignment_score:0.58, conflict_proximity_index:0.28, supply_chain_geopolitical_risk:0.35, currency_sovereignty_risk:0.38, institutional_quality_score:0.68, anti_corruption_score:0.65, press_freedom_index:0.62, rule_of_law_score:0.65, foreign_investment_protection:0.68, bilateral_tension_index:0.28, technology_decoupling_risk:0.38, energy_dependency_risk:0.38, democratic_resilience_score:0.62 },
  // GT-007 strategic_corridor NAMER — high/diplomatic_rupture
  { territory_id:"GT-007", territory_type:"strategic_corridor", region:"NAMER", political_stability_score:0.45, sanctions_exposure_risk:0.42, diplomatic_relationship_quality:0.22, trade_agreement_coverage:0.48, regulatory_alignment_score:0.45, conflict_proximity_index:0.40, supply_chain_geopolitical_risk:0.55, currency_sovereignty_risk:0.38, institutional_quality_score:0.48, anti_corruption_score:0.50, press_freedom_index:0.55, rule_of_law_score:0.48, foreign_investment_protection:0.45, bilateral_tension_index:0.72, technology_decoupling_risk:0.48, energy_dependency_risk:0.35, democratic_resilience_score:0.50 },
  // GT-008 multilateral_bloc APAC — low/stable
  { territory_id:"GT-008", territory_type:"multilateral_bloc",  region:"APAC",  political_stability_score:0.82, sanctions_exposure_risk:0.08, diplomatic_relationship_quality:0.88, trade_agreement_coverage:0.85, regulatory_alignment_score:0.85, conflict_proximity_index:0.08, supply_chain_geopolitical_risk:0.10, currency_sovereignty_risk:0.12, institutional_quality_score:0.85, anti_corruption_score:0.82, press_freedom_index:0.80, rule_of_law_score:0.85, foreign_investment_protection:0.88, bilateral_tension_index:0.10, technology_decoupling_risk:0.10, energy_dependency_risk:0.15, democratic_resilience_score:0.85 },
];

type Territory = typeof MOCK_TERRITORIES[0];

function stabilityScore(t: Territory): number {
  const avg = (t.political_stability_score + t.rule_of_law_score + t.democratic_resilience_score) / 3;
  return Math.min(Math.round((1 - avg) * 100 * 100) / 100, 100);
}
function exposureScore(t: Territory): number {
  const avg = (t.sanctions_exposure_risk + t.conflict_proximity_index + t.bilateral_tension_index) / 3;
  return Math.min(Math.round(avg * 100 * 100) / 100, 100);
}
function governanceScore(t: Territory): number {
  const avg = (t.institutional_quality_score + t.anti_corruption_score + t.foreign_investment_protection) / 3;
  return Math.min(Math.round((1 - avg) * 100 * 100) / 100, 100);
}
function sovereigntyScore(t: Territory): number {
  const avg = (t.technology_decoupling_risk + t.energy_dependency_risk + (1 - t.regulatory_alignment_score)) / 3;
  return Math.min(Math.round(avg * 100 * 100) / 100, 100);
}
function composite(stab: number, exp: number, gov: number, sov: number): number {
  return Math.min(Math.round((stab * 0.30 + exp * 0.25 + gov * 0.25 + sov * 0.20) * 100) / 100, 100);
}
function geopoliticalPattern(t: Territory): string {
  if (t.sanctions_exposure_risk >= 0.65) return "sanctions_cascade";
  if (t.conflict_proximity_index >= 0.60) return "conflict_spillover";
  if (t.bilateral_tension_index >= 0.65 && t.diplomatic_relationship_quality <= 0.35) return "diplomatic_rupture";
  if (t.regulatory_alignment_score <= 0.35 && t.technology_decoupling_risk >= 0.55) return "regulatory_decoupling";
  if (t.energy_dependency_risk >= 0.60 && t.currency_sovereignty_risk >= 0.55) return "sovereignty_erosion";
  return "none";
}
function risk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "hostile"; if (c >= 40) return "tense"; if (c >= 20) return "cautious"; return "stable"; }
function action(r: string, p: string): string {
  if (r === "critical") {
    if (p === "sanctions_cascade") return "market_exit_plan";
    return "emergency_hedging";
  }
  if (r === "high") {
    if (p === "diplomatic_rupture" || p === "conflict_spillover") return "diplomatic_engagement";
    return "exposure_reduction";
  }
  if (r === "moderate") return "geopolitical_monitoring";
  return "no_action";
}
function signal(t: Territory, pat: string, comp: number): string {
  if (comp < 20) return "Zone géopolitique stable — relations diplomatiques solides, souveraineté préservée, risques maîtrisés";
  const labels: Record<string, string> = {
    sanctions_cascade:     "Cascade de sanctions",
    diplomatic_rupture:    "Rupture diplomatique",
    regulatory_decoupling: "Découplage réglementaire",
    conflict_spillover:    "Débordement conflictuel",
    sovereignty_erosion:   "Érosion souveraineté",
  };
  const label = labels[pat] ?? pat.replace(/_/g, " ");
  return `${label} — exposition sanctions ${t.sanctions_exposure_risk.toFixed(2)} — stabilité politique ${t.political_stability_score.toFixed(2)} — tension bilatérale ${t.bilateral_tension_index.toFixed(2)} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const territories = MOCK_TERRITORIES.map(t => {
      const stab = stabilityScore(t), exp = exposureScore(t), gov = governanceScore(t), sov = sovereigntyScore(t);
      const comp = composite(stab, exp, gov, sov), pat = geopoliticalPattern(t), r = risk(comp), sev = severity(comp), act = action(r, pat);
      const isHostile = comp >= 60;
      const exitPlan  = act === "market_exit_plan";
      return {
        territory_id: t.territory_id, territory_type: t.territory_type, region: t.region,
        geopolitical_risk: r, geopolitical_pattern: pat, geopolitical_severity: sev, recommended_action: act,
        stability_score: stab, exposure_score: exp, governance_score: gov, sovereignty_score: sov,
        geopolitical_composite: comp,
        is_hostile_territory: isHostile,
        requires_exit_plan: exitPlan,
        estimated_geopolitical_risk_index: Math.round(Math.min(comp / 100 * (t.sanctions_exposure_risk + t.conflict_proximity_index) / 2 * 10, 10.0) * 100) / 100,
        geopolitical_signal: signal(t, pat, comp),
      };
    });
    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tstab=0, texp=0, tgov=0, tsov=0, tcomp=0, tridx=0, hostileC=0, exitC=0;
    for (const ter of territories) {
      rc[ter.geopolitical_risk]     = (rc[ter.geopolitical_risk]     || 0) + 1;
      pc[ter.geopolitical_pattern]  = (pc[ter.geopolitical_pattern]  || 0) + 1;
      sc[ter.geopolitical_severity] = (sc[ter.geopolitical_severity] || 0) + 1;
      ac[ter.recommended_action]    = (ac[ter.recommended_action]    || 0) + 1;
      tstab += ter.stability_score; texp += ter.exposure_score; tgov += ter.governance_score; tsov += ter.sovereignty_score;
      tcomp += ter.geopolitical_composite; tridx += ter.estimated_geopolitical_risk_index;
      if (ter.is_hostile_territory) hostileC++;
      if (ter.requires_exit_plan)   exitC++;
    }
    const n = territories.length;
    return NextResponse.json({ territories, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_geopolitical_composite: Math.round(tcomp / n * 10) / 10,
      hostile_count: hostileC, exit_plan_count: exitC,
      avg_stability_score:   Math.round(tstab / n * 10) / 10,
      avg_exposure_score:    Math.round(texp  / n * 10) / 10,
      avg_governance_score:  Math.round(tgov  / n * 10) / 10,
      avg_sovereignty_score: Math.round(tsov  / n * 10) / 10,
      avg_estimated_geopolitical_risk_index: Math.round(tridx / n * 100) / 100,
    }});
  }
  return NextResponse.json(await (await fetch(`${process.env.SWARM_API_URL}/geopolitical-resilience-engine`)).json());
}
