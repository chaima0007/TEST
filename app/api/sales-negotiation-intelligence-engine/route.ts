import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001", region: "West",
    negotiation_risk: "low", negotiation_pattern: "none",
    negotiation_severity: "disciplined", recommended_action: "no_action",
    concession_discipline_score: 0.0, negotiation_process_score: 0.0,
    negotiation_urgency_score: 0.0, value_articulation_score: 0.0,
    negotiation_composite: 0.0,
    has_negotiation_gap: false, requires_negotiation_coaching: false,
    estimated_margin_erosion_usd: 0.0,
    negotiation_signal: "Negotiation discipline healthy — concession management, value anchoring, and urgency creation within benchmarks",
  },
  {
    rep_id: "rep_002", region: "East",
    negotiation_risk: "low", negotiation_pattern: "none",
    negotiation_severity: "disciplined", recommended_action: "no_action",
    concession_discipline_score: 3.0, negotiation_process_score: 4.0,
    negotiation_urgency_score: 2.0, value_articulation_score: 5.0,
    negotiation_composite: 3.45,
    has_negotiation_gap: false, requires_negotiation_coaching: false,
    estimated_margin_erosion_usd: 0.0,
    negotiation_signal: "Negotiation discipline healthy — concession management, value anchoring, and urgency creation within benchmarks",
  },
  {
    rep_id: "rep_003", region: "Central",
    negotiation_risk: "moderate", negotiation_pattern: "urgency_creation_gap",
    negotiation_severity: "developing", recommended_action: "negotiation_skills_coaching",
    concession_discipline_score: 18.0, negotiation_process_score: 12.0,
    negotiation_urgency_score: 28.0, value_articulation_score: 15.0,
    negotiation_composite: 18.75,
    has_negotiation_gap: false, requires_negotiation_coaching: false,
    estimated_margin_erosion_usd: 12600.0,
    negotiation_signal: "Urgency creation gap — 30% give first concession immediately — 28% deals won without discount — 1.8 avg rounds — composite 19",
  },
  {
    rep_id: "rep_004", region: "Northeast",
    negotiation_risk: "moderate", negotiation_pattern: "price_anchoring_failure",
    negotiation_severity: "developing", recommended_action: "negotiation_skills_coaching",
    concession_discipline_score: 22.0, negotiation_process_score: 18.0,
    negotiation_urgency_score: 20.0, value_articulation_score: 32.0,
    negotiation_composite: 22.3,
    has_negotiation_gap: false, requires_negotiation_coaching: true,
    estimated_margin_erosion_usd: 28800.0,
    negotiation_signal: "Price anchoring failure — 45% give first concession immediately — 22% deals won without discount — 2.1 avg rounds — composite 22",
  },
  {
    rep_id: "rep_005", region: "Southeast",
    negotiation_risk: "high", negotiation_pattern: "concession_cascade",
    negotiation_severity: "reactive", recommended_action: "concession_management_review",
    concession_discipline_score: 45.0, negotiation_process_score: 32.0,
    negotiation_urgency_score: 28.0, value_articulation_score: 30.0,
    negotiation_composite: 36.65,
    has_negotiation_gap: false, requires_negotiation_coaching: true,
    estimated_margin_erosion_usd: 72000.0,
    negotiation_signal: "Concession cascade — 62% give first concession immediately — 18% deals won without discount — 3.2 avg rounds — composite 37",
  },
  {
    rep_id: "rep_006", region: "West",
    negotiation_risk: "high", negotiation_pattern: "early_capitulation",
    negotiation_severity: "reactive", recommended_action: "negotiation_skills_coaching",
    concession_discipline_score: 58.0, negotiation_process_score: 35.0,
    negotiation_urgency_score: 30.0, value_articulation_score: 28.0,
    negotiation_composite: 42.0,
    has_negotiation_gap: true, requires_negotiation_coaching: true,
    estimated_margin_erosion_usd: 108000.0,
    negotiation_signal: "Early capitulation — 78% give first concession immediately — 12% deals won without discount — 2.8 avg rounds — composite 42",
  },
  {
    rep_id: "rep_007", region: "APAC",
    negotiation_risk: "critical", negotiation_pattern: "manager_escalation_dependency",
    negotiation_severity: "erosive", recommended_action: "manager_escalation_reduction",
    concession_discipline_score: 65.0, negotiation_process_score: 78.0,
    negotiation_urgency_score: 55.0, value_articulation_score: 60.0,
    negotiation_composite: 66.5,
    has_negotiation_gap: true, requires_negotiation_coaching: true,
    estimated_margin_erosion_usd: 224000.0,
    negotiation_signal: "Manager escalation dependency — 85% give first concession immediately — 8% deals won without discount — 4.0 avg rounds — composite 67",
  },
  {
    rep_id: "rep_008", region: "EMEA",
    negotiation_risk: "critical", negotiation_pattern: "early_capitulation",
    negotiation_severity: "erosive", recommended_action: "concession_management_review",
    concession_discipline_score: 100.0, negotiation_process_score: 100.0,
    negotiation_urgency_score: 100.0, value_articulation_score: 100.0,
    negotiation_composite: 100.0,
    has_negotiation_gap: true, requires_negotiation_coaching: true,
    estimated_margin_erosion_usd: 350000.0,
    negotiation_signal: "Early capitulation — 95% give first concession immediately — 5% deals won without discount — 5.0 avg rounds — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-negotiation-intelligence-engine`);
      if (risk)    url.searchParams.set("risk", risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (risk)    reps = reps.filter((r) => r.negotiation_risk    === risk);
  if (pattern) reps = reps.filter((r) => r.negotiation_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_con = 0, total_pro = 0, total_urg = 0, total_val = 0, total_erosion = 0;

  for (const r of mockReps) {
    risk_counts[r.negotiation_risk]       = (risk_counts[r.negotiation_risk] || 0) + 1;
    pattern_counts[r.negotiation_pattern] = (pattern_counts[r.negotiation_pattern] || 0) + 1;
    severity_counts[r.negotiation_severity] = (severity_counts[r.negotiation_severity] || 0) + 1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action] || 0) + 1;
    total_comp    += r.negotiation_composite;
    total_con     += r.concession_discipline_score;
    total_pro     += r.negotiation_process_score;
    total_urg     += r.negotiation_urgency_score;
    total_val     += r.value_articulation_score;
    total_erosion += r.estimated_margin_erosion_usd;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total:                                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_negotiation_composite:                Math.round((total_comp / n) * 10) / 10,
      negotiation_gap_count:                    mockReps.filter((r) => r.has_negotiation_gap).length,
      coaching_count:                           mockReps.filter((r) => r.requires_negotiation_coaching).length,
      avg_concession_discipline_score:          Math.round((total_con / n) * 10) / 10,
      avg_negotiation_process_score:            Math.round((total_pro / n) * 10) / 10,
      avg_negotiation_urgency_score:            Math.round((total_urg / n) * 10) / 10,
      avg_value_articulation_score:             Math.round((total_val / n) * 10) / 10,
      total_estimated_margin_erosion_usd:       Math.round(total_erosion * 100) / 100,
    },
  });
}
