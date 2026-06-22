import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[revenue-leak-detector] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "acc_001", account_name: "Apex Corp", csm_id: "csm_003",
    leak_severity: "critical", leak_pattern: "multi_leak",
    retention_outlook: "critical", leak_action: "executive_save",
    discount_risk_score: 80.0, renewal_risk_score: 85.0,
    expansion_health_score: 15.0, relationship_score: 10.0,
    leak_composite: 89.3, estimated_arr_at_risk: 160740.0,
    arr_expansion_potential: 55800.0, is_leaking: true,
    needs_executive_save: true, current_arr: 180000, region: "NAMER",
  },
  {
    account_id: "acc_002", account_name: "Solaris Financial", csm_id: "csm_001",
    leak_severity: "contained", leak_pattern: "healthy",
    retention_outlook: "secure", leak_action: "monitor",
    discount_risk_score: 5.0, renewal_risk_score: 8.0,
    expansion_health_score: 90.0, relationship_score: 92.0,
    leak_composite: 10.6, estimated_arr_at_risk: 31800.0,
    arr_expansion_potential: 42000.0, is_leaking: false,
    needs_executive_save: false, current_arr: 300000, region: "EMEA",
  },
  {
    account_id: "acc_003", account_name: "ZenithAI Platform", csm_id: "csm_002",
    leak_severity: "significant", leak_pattern: "renewal_risk",
    retention_outlook: "at_risk", leak_action: "retention_play",
    discount_risk_score: 25.0, renewal_risk_score: 60.0,
    expansion_health_score: 55.0, relationship_score: 60.0,
    leak_composite: 50.3, estimated_arr_at_risk: 100600.0,
    arr_expansion_potential: 48000.0, is_leaking: true,
    needs_executive_save: false, current_arr: 200000, region: "APAC",
  },
  {
    account_id: "acc_004", account_name: "Harbor Tech Solutions", csm_id: "csm_005",
    leak_severity: "moderate", leak_pattern: "expansion_stall",
    retention_outlook: "watchlist", leak_action: "protect_expansion",
    discount_risk_score: 10.0, renewal_risk_score: 28.0,
    expansion_health_score: 25.0, relationship_score: 72.0,
    leak_composite: 36.7, estimated_arr_at_risk: 183500.0,
    arr_expansion_potential: 175000.0, is_leaking: false,
    needs_executive_save: false, current_arr: 500000, region: "NAMER",
  },
  {
    account_id: "acc_005", account_name: "PeakFlow Labs", csm_id: "csm_007",
    leak_severity: "critical", leak_pattern: "champion_erosion",
    retention_outlook: "critical", leak_action: "executive_save",
    discount_risk_score: 30.0, renewal_risk_score: 55.0,
    expansion_health_score: 40.0, relationship_score: 20.0,
    leak_composite: 66.5, estimated_arr_at_risk: 153190.0,
    arr_expansion_potential: 62100.0, is_leaking: true,
    needs_executive_save: true, current_arr: 230000, region: "EMEA",
  },
  {
    account_id: "acc_006", account_name: "Orbit Retail Group", csm_id: "csm_004",
    leak_severity: "moderate", leak_pattern: "discount_creep",
    retention_outlook: "watchlist", leak_action: "protect_expansion",
    discount_risk_score: 55.0, renewal_risk_score: 18.0,
    expansion_health_score: 68.0, relationship_score: 75.0,
    leak_composite: 30.1, estimated_arr_at_risk: 54180.0,
    arr_expansion_potential: 31500.0, is_leaking: false,
    needs_executive_save: false, current_arr: 180000, region: "APAC",
  },
  {
    account_id: "acc_007", account_name: "Nexus Consulting", csm_id: "csm_006",
    leak_severity: "contained", leak_pattern: "healthy",
    retention_outlook: "secure", leak_action: "monitor",
    discount_risk_score: 0.0, renewal_risk_score: 5.0,
    expansion_health_score: 95.0, relationship_score: 98.0,
    leak_composite: 3.8, estimated_arr_at_risk: 6840.0,
    arr_expansion_potential: 54000.0, is_leaking: false,
    needs_executive_save: false, current_arr: 180000, region: "LATAM",
  },
  {
    account_id: "acc_008", account_name: "Vertex Manufacturing", csm_id: "csm_008",
    leak_severity: "significant", leak_pattern: "multi_leak",
    retention_outlook: "at_risk", leak_action: "retention_play",
    discount_risk_score: 45.0, renewal_risk_score: 45.0,
    expansion_health_score: 30.0, relationship_score: 40.0,
    leak_composite: 56.8, estimated_arr_at_risk: 107920.0,
    arr_expansion_potential: 72200.0, is_leaking: true,
    needs_executive_save: false, current_arr: 190000, region: "NAMER",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const severity = searchParams.get("severity");
  const pattern  = searchParams.get("pattern");
  const region   = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/revenue-leak-detector`);
      if (severity) url.searchParams.set("severity", severity);
      if (pattern)  url.searchParams.set("pattern", pattern);
      if (region)   url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (severity) accounts = accounts.filter((a) => a.leak_severity === severity);
  if (pattern)  accounts = accounts.filter((a) => a.leak_pattern === pattern);
  if (region)   accounts = accounts.filter((a) => a.region === region);

  const severity_counts: Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const outlook_counts:  Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_disc = 0, total_renew = 0,
      total_exp = 0, total_rel = 0, total_arr_risk = 0;

  for (const a of mockAccounts) {
    severity_counts[a.leak_severity]    = (severity_counts[a.leak_severity] || 0) + 1;
    pattern_counts[a.leak_pattern]      = (pattern_counts[a.leak_pattern] || 0) + 1;
    outlook_counts[a.retention_outlook] = (outlook_counts[a.retention_outlook] || 0) + 1;
    action_counts[a.leak_action]        = (action_counts[a.leak_action] || 0) + 1;
    total_comp  += a.leak_composite;
    total_disc  += a.discount_risk_score;
    total_renew += a.renewal_risk_score;
    total_exp   += a.expansion_health_score;
    total_rel   += a.relationship_score;
    total_arr_risk += a.estimated_arr_at_risk;
  }

  const n = mockAccounts.length;

  return sealResponse(NextResponse.json({
    accounts,
    summary: {
      total: n,
      severity_counts,
      pattern_counts,
      outlook_counts,
      action_counts,
      avg_leak_composite:           Math.round((total_comp / n) * 10) / 10,
      total_arr_at_risk:            total_arr_risk,
      leaking_count:                mockAccounts.filter((a) => a.is_leaking).length,
      executive_save_count:         mockAccounts.filter((a) => a.needs_executive_save).length,
      avg_discount_risk_score:      Math.round((total_disc / n) * 10) / 10,
      avg_renewal_risk_score:       Math.round((total_renew / n) * 10) / 10,
      avg_expansion_health_score:   Math.round((total_exp / n) * 10) / 10,
      avg_relationship_score:       Math.round((total_rel / n) * 10) / 10,
    },
  }));
}
