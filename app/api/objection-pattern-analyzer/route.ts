import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", deal_name: "Acme Corp Enterprise", rep_id: "rep_003",
    primary_objection_type: "competitor", objection_severity: "minor",
    handling_readiness: "prepared", objection_action: "provide_proof",
    handling_effectiveness_score: 88.0, objection_density_score: 75.0,
    pattern_risk_score: 90.0, rep_preparedness_score: 95.0,
    objection_composite: 87.1, handle_rate: 100.0,
    late_stage_risk: true, is_objection_contained: true,
    needs_coaching: false, region: "NAMER",
  },
  {
    deal_id: "deal_002", deal_name: "BetaTech SaaS", rep_id: "rep_001",
    primary_objection_type: "price", objection_severity: "deal_breaker",
    handling_readiness: "unprepared", objection_action: "executive_call",
    handling_effectiveness_score: 8.0, objection_density_score: 15.0,
    pattern_risk_score: 20.0, rep_preparedness_score: 0.0,
    objection_composite: 11.5, handle_rate: 16.7,
    late_stage_risk: true, is_objection_contained: false,
    needs_coaching: true, region: "EMEA",
  },
  {
    deal_id: "deal_003", deal_name: "CloudBase Platform", rep_id: "rep_002",
    primary_objection_type: "status_quo", objection_severity: "moderate",
    handling_readiness: "needs_prep", objection_action: "reframe_value",
    handling_effectiveness_score: 55.0, objection_density_score: 55.0,
    pattern_risk_score: 72.0, rep_preparedness_score: 60.0,
    objection_composite: 61.1, handle_rate: 66.7,
    late_stage_risk: false, is_objection_contained: false,
    needs_coaching: false, region: "APAC",
  },
  {
    deal_id: "deal_004", deal_name: "Delta Networks", rep_id: "rep_005",
    primary_objection_type: "timing", objection_severity: "serious",
    handling_readiness: "reactive", objection_action: "reframe_value",
    handling_effectiveness_score: 22.0, objection_density_score: 35.0,
    pattern_risk_score: 50.0, rep_preparedness_score: 35.0,
    objection_composite: 35.3, handle_rate: 40.0,
    late_stage_risk: true, is_objection_contained: false,
    needs_coaching: true, region: "NAMER",
  },
  {
    deal_id: "deal_005", deal_name: "EcoTech Expansion", rep_id: "rep_007",
    primary_objection_type: "no_objection", objection_severity: "minor",
    handling_readiness: "prepared", objection_action: "none_needed",
    handling_effectiveness_score: 85.0, objection_density_score: 90.0,
    pattern_risk_score: 100.0, rep_preparedness_score: 95.0,
    objection_composite: 92.3, handle_rate: 100.0,
    late_stage_risk: false, is_objection_contained: true,
    needs_coaching: false, region: "EMEA",
  },
  {
    deal_id: "deal_006", deal_name: "Finova Capital", rep_id: "rep_004",
    primary_objection_type: "risk", objection_severity: "moderate",
    handling_readiness: "needs_prep", objection_action: "provide_proof",
    handling_effectiveness_score: 48.0, objection_density_score: 55.0,
    pattern_risk_score: 80.0, rep_preparedness_score: 55.0,
    objection_composite: 58.2, handle_rate: 75.0,
    late_stage_risk: false, is_objection_contained: false,
    needs_coaching: false, region: "APAC",
  },
  {
    deal_id: "deal_007", deal_name: "GlobalLink Corp", rep_id: "rep_006",
    primary_objection_type: "competitor", objection_severity: "minor",
    handling_readiness: "prepared", objection_action: "provide_proof",
    handling_effectiveness_score: 78.0, objection_density_score: 75.0,
    pattern_risk_score: 85.0, rep_preparedness_score: 80.0,
    objection_composite: 79.8, handle_rate: 100.0,
    late_stage_risk: false, is_objection_contained: true,
    needs_coaching: false, region: "LATAM",
  },
  {
    deal_id: "deal_008", deal_name: "HorizonAI Platform", rep_id: "rep_008",
    primary_objection_type: "price", objection_severity: "serious",
    handling_readiness: "reactive", objection_action: "reframe_value",
    handling_effectiveness_score: 18.0, objection_density_score: 15.0,
    pattern_risk_score: 55.0, rep_preparedness_score: 20.0,
    objection_composite: 27.8, handle_rate: 33.3,
    late_stage_risk: true, is_objection_contained: false,
    needs_coaching: true, region: "NAMER",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const objType  = searchParams.get("type");
  const severity = searchParams.get("severity");
  const region   = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/objection-pattern-analyzer`);
      if (objType)  url.searchParams.set("type", objType);
      if (severity) url.searchParams.set("severity", severity);
      if (region)   url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (objType)  deals = deals.filter((d) => d.primary_objection_type === objType);
  if (severity) deals = deals.filter((d) => d.objection_severity === severity);
  if (region)   deals = deals.filter((d) => d.region === region);

  const type_counts:     Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const readiness_counts:Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_hr = 0, total_hdl = 0,
      total_risk = 0, total_prep = 0, total_dens = 0;

  for (const d of mockDeals) {
    type_counts[d.primary_objection_type]  = (type_counts[d.primary_objection_type] || 0) + 1;
    severity_counts[d.objection_severity]  = (severity_counts[d.objection_severity] || 0) + 1;
    readiness_counts[d.handling_readiness] = (readiness_counts[d.handling_readiness] || 0) + 1;
    action_counts[d.objection_action]      = (action_counts[d.objection_action] || 0) + 1;
    total_comp += d.objection_composite;
    total_hr   += d.handle_rate;
    total_hdl  += d.handling_effectiveness_score;
    total_risk += d.pattern_risk_score;
    total_prep += d.rep_preparedness_score;
    total_dens += d.objection_density_score;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      objection_type_counts:            type_counts,
      severity_counts,
      readiness_counts,
      action_counts,
      avg_objection_composite:          Math.round((total_comp / n) * 10) / 10,
      avg_handle_rate:                  Math.round((total_hr / n) * 10) / 10,
      contained_count:                  mockDeals.filter((d) => d.is_objection_contained).length,
      coaching_count:                   mockDeals.filter((d) => d.needs_coaching).length,
      avg_handling_effectiveness_score: Math.round((total_hdl / n) * 10) / 10,
      avg_pattern_risk_score:           Math.round((total_risk / n) * 10) / 10,
      avg_rep_preparedness_score:       Math.round((total_prep / n) * 10) / 10,
      avg_objection_density_score:      Math.round((total_dens / n) * 10) / 10,
    },
  });
}
