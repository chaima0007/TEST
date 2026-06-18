import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", deal_name: "Apex Cloud Transformation", rep_id: "rep_003",
    drift_severity: "severe_drift", drift_pattern: "multi_drift",
    buyer_alignment: "disconnected", drift_action: "realign_now",
    level_drift_score: 88.0, function_drift_score: 100.0,
    exec_disengagement_score: 92.5, committee_dilution_score: 62.0,
    persona_drift_composite: 88.3, deal_misalignment_risk: 353200,
    realignment_probability: 4.0, is_drifted: true, needs_exec_reengagement: true,
    deal_value: 400000, target_persona_level: "C-suite", current_primary_contact_level: "Manager",
    target_persona_function: "business", current_primary_contact_function: "technical",
    region: "NAMER",
  },
  {
    deal_id: "deal_002", deal_name: "Solaris Data Platform", rep_id: "rep_001",
    drift_severity: "moderate_drift", drift_pattern: "sponsor_loss",
    buyer_alignment: "misaligned", drift_action: "re_engage_exec",
    level_drift_score: 35.0, function_drift_score: 20.0,
    exec_disengagement_score: 72.0, committee_dilution_score: 18.0,
    persona_drift_composite: 48.2, deal_misalignment_risk: 144600,
    realignment_probability: 28.5, is_drifted: true, needs_exec_reengagement: true,
    deal_value: 300000, target_persona_level: "VP", current_primary_contact_level: "Director",
    target_persona_function: "business", current_primary_contact_function: "business",
    region: "EMEA",
  },
  {
    deal_id: "deal_003", deal_name: "ZenithAI Scale-Up", rep_id: "rep_002",
    drift_severity: "aligned", drift_pattern: "no_drift",
    buyer_alignment: "strongly_aligned", drift_action: "maintain",
    level_drift_score: 0.0, function_drift_score: 0.0,
    exec_disengagement_score: 8.0, committee_dilution_score: 0.0,
    persona_drift_composite: 2.4, deal_misalignment_risk: 4800,
    realignment_probability: 96.0, is_drifted: false, needs_exec_reengagement: false,
    deal_value: 200000, target_persona_level: "C-suite", current_primary_contact_level: "C-suite",
    target_persona_function: "business", current_primary_contact_function: "business",
    region: "APAC",
  },
  {
    deal_id: "deal_004", deal_name: "Harbor Security Suite", rep_id: "rep_005",
    drift_severity: "severe_drift", drift_pattern: "level_downgrade",
    buyer_alignment: "disconnected", drift_action: "realign_now",
    level_drift_score: 90.0, function_drift_score: 20.0,
    exec_disengagement_score: 80.5, committee_dilution_score: 30.0,
    persona_drift_composite: 71.5, deal_misalignment_risk: 357500,
    realignment_probability: 10.5, is_drifted: true, needs_exec_reengagement: true,
    deal_value: 500000, target_persona_level: "C-suite", current_primary_contact_level: "Manager",
    target_persona_function: "finance", current_primary_contact_function: "finance",
    region: "NAMER",
  },
  {
    deal_id: "deal_005", deal_name: "PeakFlow Analytics", rep_id: "rep_007",
    drift_severity: "minor_drift", drift_pattern: "committee_dilution",
    buyer_alignment: "partially_aligned", drift_action: "requalify",
    level_drift_score: 8.0, function_drift_score: 20.0,
    exec_disengagement_score: 12.0, committee_dilution_score: 44.0,
    persona_drift_composite: 26.4, deal_misalignment_risk: 60720,
    realignment_probability: 68.0, is_drifted: false, needs_exec_reengagement: false,
    deal_value: 230000, target_persona_level: "VP", current_primary_contact_level: "VP",
    target_persona_function: "business", current_primary_contact_function: "business",
    region: "EMEA",
  },
  {
    deal_id: "deal_006", deal_name: "Orbit ERP Integration", rep_id: "rep_004",
    drift_severity: "minor_drift", drift_pattern: "function_shift",
    buyer_alignment: "partially_aligned", drift_action: "requalify",
    level_drift_score: 12.0, function_drift_score: 55.0,
    exec_disengagement_score: 14.0, committee_dilution_score: 8.0,
    persona_drift_composite: 21.3, deal_misalignment_risk: 38340,
    realignment_probability: 72.5, is_drifted: false, needs_exec_reengagement: false,
    deal_value: 180000, target_persona_level: "Director", current_primary_contact_level: "Director",
    target_persona_function: "business", current_primary_contact_function: "technical",
    region: "APAC",
  },
  {
    deal_id: "deal_007", deal_name: "Nexus Platform Expansion", rep_id: "rep_006",
    drift_severity: "moderate_drift", drift_pattern: "multi_drift",
    buyer_alignment: "misaligned", drift_action: "re_engage_exec",
    level_drift_score: 55.0, function_drift_score: 55.0,
    exec_disengagement_score: 48.0, committee_dilution_score: 22.0,
    persona_drift_composite: 51.9, deal_misalignment_risk: 93420,
    realignment_probability: 35.0, is_drifted: true, needs_exec_reengagement: false,
    deal_value: 180000, target_persona_level: "VP", current_primary_contact_level: "Manager",
    target_persona_function: "business", current_primary_contact_function: "technical",
    region: "LATAM",
  },
  {
    deal_id: "deal_008", deal_name: "Vertex CX Rollout", rep_id: "rep_008",
    drift_severity: "aligned", drift_pattern: "no_drift",
    buyer_alignment: "strongly_aligned", drift_action: "maintain",
    level_drift_score: 0.0, function_drift_score: 0.0,
    exec_disengagement_score: 5.0, committee_dilution_score: 0.0,
    persona_drift_composite: 1.5, deal_misalignment_risk: 2850,
    realignment_probability: 98.0, is_drifted: false, needs_exec_reengagement: false,
    deal_value: 190000, target_persona_level: "Director", current_primary_contact_level: "Director",
    target_persona_function: "technical", current_primary_contact_function: "technical",
    region: "NAMER",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const severity = searchParams.get("severity");
  const pattern  = searchParams.get("pattern");
  const region   = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/buyer-persona-drift`);
      if (severity) url.searchParams.set("severity", severity);
      if (pattern)  url.searchParams.set("pattern", pattern);
      if (region)   url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (severity) deals = deals.filter((d) => d.drift_severity === severity);
  if (pattern)  deals = deals.filter((d) => d.drift_pattern === pattern);
  if (region)   deals = deals.filter((d) => d.region === region);

  const severity_counts:  Record<string, number> = {};
  const pattern_counts:   Record<string, number> = {};
  const alignment_counts: Record<string, number> = {};
  const action_counts:    Record<string, number> = {};
  let total_comp = 0, total_lvl = 0, total_func = 0,
      total_exec = 0, total_real = 0, total_risk = 0;

  for (const d of mockDeals) {
    severity_counts[d.drift_severity]   = (severity_counts[d.drift_severity] || 0) + 1;
    pattern_counts[d.drift_pattern]     = (pattern_counts[d.drift_pattern] || 0) + 1;
    alignment_counts[d.buyer_alignment] = (alignment_counts[d.buyer_alignment] || 0) + 1;
    action_counts[d.drift_action]       = (action_counts[d.drift_action] || 0) + 1;
    total_comp += d.persona_drift_composite;
    total_lvl  += d.level_drift_score;
    total_func += d.function_drift_score;
    total_exec += d.exec_disengagement_score;
    total_real += d.realignment_probability;
    total_risk += d.deal_misalignment_risk;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      severity_counts,
      pattern_counts,
      alignment_counts,
      action_counts,
      avg_persona_drift_composite:  Math.round((total_comp / n) * 10) / 10,
      total_misalignment_risk:      Math.round(total_risk),
      drifted_count:                mockDeals.filter((d) => d.is_drifted).length,
      exec_reengagement_count:      mockDeals.filter((d) => d.needs_exec_reengagement).length,
      avg_level_drift_score:        Math.round((total_lvl / n) * 10) / 10,
      avg_function_drift_score:     Math.round((total_func / n) * 10) / 10,
      avg_exec_disengagement_score: Math.round((total_exec / n) * 10) / 10,
      avg_realignment_probability:  Math.round((total_real / n) * 10) / 10,
    },
  });
}
