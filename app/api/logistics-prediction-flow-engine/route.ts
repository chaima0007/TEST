import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockFlows = [
  {
    flow_id: "LF-001", region: "EMEA",
    logistics_risk: "critical", flow_pattern: "supply_disruption", logistics_severity: "critical",
    recommended_action: "supply_chain_reset",
    delivery_score: 100.0, efficiency_score: 100.0, reliability_score: 75.0, resilience_score: 100.0,
    logistics_composite: 93.75, has_flow_alert: true, requires_strategic_review: true,
    estimated_supply_disruption_index: 7.59,
    logistics_signal: "Critical — livraisons à temps 50% — ruptures 45% — fiabilité fournisseurs 25% — composite 94",
  },
  {
    flow_id: "LF-005", region: "MEA",
    logistics_risk: "critical", flow_pattern: "supply_disruption", logistics_severity: "critical",
    recommended_action: "supply_chain_reset",
    delivery_score: 100.0, efficiency_score: 87.0, reliability_score: 80.0, resilience_score: 100.0,
    logistics_composite: 91.75, has_flow_alert: true, requires_strategic_review: true,
    estimated_supply_disruption_index: 7.25,
    logistics_signal: "Critical — livraisons à temps 45% — ruptures 42% — fiabilité fournisseurs 35% — composite 92",
  },
  {
    flow_id: "LF-007", region: "NAMER",
    logistics_risk: "critical", flow_pattern: "demand_surge", logistics_severity: "critical",
    recommended_action: "crisis_logistics",
    delivery_score: 100.0, efficiency_score: 45.0, reliability_score: 57.0, resilience_score: 45.0,
    logistics_composite: 64.5, has_flow_alert: true, requires_strategic_review: true,
    estimated_supply_disruption_index: 3.61,
    logistics_signal: "Critical — livraisons à temps 60% — ruptures 45% — fiabilité fournisseurs 60% — composite 64",
  },
  {
    flow_id: "LF-003", region: "APAC",
    logistics_risk: "moderate", flow_pattern: "last_mile_failure", logistics_severity: "constrained",
    recommended_action: "flow_monitoring",
    delivery_score: 52.0, efficiency_score: 34.0, reliability_score: 27.0, resilience_score: 34.0,
    logistics_composite: 37.65, has_flow_alert: true, requires_strategic_review: true,
    estimated_supply_disruption_index: 2.3,
    logistics_signal: "Moderate — livraisons à temps 65% — ruptures 20% — fiabilité fournisseurs 65% — composite 38",
  },
  {
    flow_id: "LF-006", region: "EMEA",
    logistics_risk: "moderate", flow_pattern: "none", logistics_severity: "constrained",
    recommended_action: "flow_monitoring",
    delivery_score: 45.0, efficiency_score: 16.0, reliability_score: 16.0, resilience_score: 21.0,
    logistics_composite: 25.7, has_flow_alert: false, requires_strategic_review: true,
    estimated_supply_disruption_index: 1.18,
    logistics_signal: "Moderate — livraisons à temps 72% — ruptures 18% — fiabilité fournisseurs 68% — composite 26",
  },
  {
    flow_id: "LF-004", region: "LATAM",
    logistics_risk: "moderate", flow_pattern: "inventory_imbalance", logistics_severity: "constrained",
    recommended_action: "flow_monitoring",
    delivery_score: 39.0, efficiency_score: 16.0, reliability_score: 16.0, resilience_score: 21.0,
    logistics_composite: 23.9, has_flow_alert: false, requires_strategic_review: false,
    estimated_supply_disruption_index: 1.1,
    logistics_signal: "Moderate — livraisons à temps 78% — ruptures 25% — fiabilité fournisseurs 72% — composite 24",
  },
  {
    flow_id: "LF-002", region: "NAMER",
    logistics_risk: "low", flow_pattern: "none", logistics_severity: "fluid",
    recommended_action: "no_action",
    delivery_score: 0.0, efficiency_score: 0.0, reliability_score: 0.0, resilience_score: 0.0,
    logistics_composite: 0.0, has_flow_alert: false, requires_strategic_review: false,
    estimated_supply_disruption_index: 0.0,
    logistics_signal: "Flux logistiques optimaux — livraisons fiables, stocks équilibrés, fournisseurs performants",
  },
  {
    flow_id: "LF-008", region: "APAC",
    logistics_risk: "low", flow_pattern: "none", logistics_severity: "fluid",
    recommended_action: "no_action",
    delivery_score: 0.0, efficiency_score: 0.0, reliability_score: 0.0, resilience_score: 0.0,
    logistics_composite: 0.0, has_flow_alert: false, requires_strategic_review: false,
    estimated_supply_disruption_index: 0.0,
    logistics_signal: "Flux logistiques optimaux — livraisons fiables, stocks équilibrés, fournisseurs performants",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (!process.env.SWARM_API_URL) {
    // mock computation path
    let flows = [...mockFlows];
    if (risk)    flows = flows.filter((f) => f.logistics_risk === risk);
    if (pattern) flows = flows.filter((f) => f.flow_pattern === pattern);

    const risk_counts:     Record<string, number> = {};
    const pattern_counts:  Record<string, number> = {};
    const severity_counts: Record<string, number> = {};
    const action_counts:   Record<string, number> = {};
    let total_comp = 0, total_deliv = 0, total_eff = 0, total_rel = 0, total_res = 0, total_idx = 0;

    for (const f of mockFlows) {
      risk_counts[f.logistics_risk]         = (risk_counts[f.logistics_risk] || 0) + 1;
      pattern_counts[f.flow_pattern]        = (pattern_counts[f.flow_pattern] || 0) + 1;
      severity_counts[f.logistics_severity] = (severity_counts[f.logistics_severity] || 0) + 1;
      action_counts[f.recommended_action]   = (action_counts[f.recommended_action] || 0) + 1;
      total_comp  += f.logistics_composite;
      total_deliv += f.delivery_score;
      total_eff   += f.efficiency_score;
      total_rel   += f.reliability_score;
      total_res   += f.resilience_score;
      total_idx   += f.estimated_supply_disruption_index;
    }

    const n = mockFlows.length;
    return NextResponse.json({
      flows,
      summary: {
        total:                                    n,
        risk_counts,
        pattern_counts,
        severity_counts,
        action_counts,
        avg_logistics_composite:                  Math.round((total_comp  / n) * 100) / 100,
        flow_alert_count:                         mockFlows.filter((f) => f.has_flow_alert).length,
        strategic_review_count:                   mockFlows.filter((f) => f.requires_strategic_review).length,
        avg_delivery_score:                       Math.round((total_deliv / n) * 100) / 100,
        avg_efficiency_score:                     Math.round((total_eff   / n) * 100) / 100,
        avg_reliability_score:                    Math.round((total_rel   / n) * 100) / 100,
        avg_resilience_score:                     Math.round((total_res   / n) * 100) / 100,
        avg_estimated_supply_disruption_index:    Math.round((total_idx   / n) * 100) / 100,
      },
    });
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/logistics-prediction-flow-engine`);
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(await res.json());
  } catch {}

  return NextResponse.json({ flows: [], summary: {} }, { status: 502 });
}
