import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", deal_name: "Acme Corp Enterprise", rep_id: "rep_003",
    champion_status: "active_advocate", champion_risk: "low",
    influence_level: "high_influence", champion_action: "maintain",
    engagement_score: 98.0, influence_score: 100.0,
    stability_score: 100.0, deal_protection_score: 100.0,
    champion_composite: 99.5, departure_probability: 0.0,
    deal_at_risk_score: 0.5, is_champion_stable: true,
    needs_backup_champion: false, region: "NAMER",
  },
  {
    deal_id: "deal_002", deal_name: "BetaTech SaaS", rep_id: "rep_001",
    champion_status: "departed", champion_risk: "critical",
    influence_level: "high_influence", champion_action: "escalate_exec",
    engagement_score: 12.0, influence_score: 58.0,
    stability_score: 10.0, deal_protection_score: 35.0,
    champion_composite: 26.5, departure_probability: 90.0,
    deal_at_risk_score: 95.0, is_champion_stable: false,
    needs_backup_champion: true, region: "EMEA",
  },
  {
    deal_id: "deal_003", deal_name: "CloudBase Platform", rep_id: "rep_002",
    champion_status: "engaged", champion_risk: "low",
    influence_level: "moderate_influence", champion_action: "maintain",
    engagement_score: 65.0, influence_score: 52.0,
    stability_score: 72.0, deal_protection_score: 60.0,
    champion_composite: 63.8, departure_probability: 5.0,
    deal_at_risk_score: 36.2, is_champion_stable: true,
    needs_backup_champion: false, region: "APAC",
  },
  {
    deal_id: "deal_004", deal_name: "Delta Networks", rep_id: "rep_005",
    champion_status: "cooling", champion_risk: "high",
    influence_level: "moderate_influence", champion_action: "re_engage",
    engagement_score: 22.0, influence_score: 40.0,
    stability_score: 45.0, deal_protection_score: 28.0,
    champion_composite: 32.8, departure_probability: 25.0,
    deal_at_risk_score: 67.2, is_champion_stable: false,
    needs_backup_champion: true, region: "NAMER",
  },
  {
    deal_id: "deal_005", deal_name: "EcoTech Expansion", rep_id: "rep_007",
    champion_status: "active_advocate", champion_risk: "low",
    influence_level: "high_influence", champion_action: "maintain",
    engagement_score: 88.0, influence_score: 82.0,
    stability_score: 85.0, deal_protection_score: 78.0,
    champion_composite: 84.4, departure_probability: 0.0,
    deal_at_risk_score: 15.6, is_champion_stable: true,
    needs_backup_champion: false, region: "EMEA",
  },
  {
    deal_id: "deal_006", deal_name: "Finova Capital", rep_id: "rep_004",
    champion_status: "cooling", champion_risk: "moderate",
    influence_level: "low_influence", champion_action: "find_backup",
    engagement_score: 38.0, influence_score: 22.0,
    stability_score: 55.0, deal_protection_score: 32.0,
    champion_composite: 38.4, departure_probability: 18.0,
    deal_at_risk_score: 61.6, is_champion_stable: false,
    needs_backup_champion: true, region: "APAC",
  },
  {
    deal_id: "deal_007", deal_name: "GlobalLink Corp", rep_id: "rep_006",
    champion_status: "engaged", champion_risk: "low",
    influence_level: "high_influence", champion_action: "maintain",
    engagement_score: 72.0, influence_score: 76.0,
    stability_score: 80.0, deal_protection_score: 70.0,
    champion_composite: 74.5, departure_probability: 3.0,
    deal_at_risk_score: 25.5, is_champion_stable: true,
    needs_backup_champion: false, region: "LATAM",
  },
  {
    deal_id: "deal_008", deal_name: "HorizonAI Platform", rep_id: "rep_008",
    champion_status: "silent", champion_risk: "critical",
    influence_level: "unknown", champion_action: "escalate_exec",
    engagement_score: 5.0, influence_score: 10.0,
    stability_score: 18.0, deal_protection_score: 8.0,
    champion_composite: 10.2, departure_probability: 38.0,
    deal_at_risk_score: 89.8, is_champion_stable: false,
    needs_backup_champion: true, region: "NAMER",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const status = searchParams.get("status");
  const risk   = searchParams.get("risk");
  const region = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/champion-risk-monitor`);
      if (status) url.searchParams.set("status", status);
      if (risk)   url.searchParams.set("risk", risk);
      if (region) url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (status) deals = deals.filter((d) => d.champion_status === status);
  if (risk)   deals = deals.filter((d) => d.champion_risk === risk);
  if (region) deals = deals.filter((d) => d.region === region);

  const status_counts:   Record<string, number> = {};
  const risk_counts:     Record<string, number> = {};
  const infl_counts:     Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_dep = 0, total_eng = 0,
      total_inf = 0, total_sta = 0, total_dar = 0;

  for (const d of mockDeals) {
    status_counts[d.champion_status]   = (status_counts[d.champion_status] || 0) + 1;
    risk_counts[d.champion_risk]       = (risk_counts[d.champion_risk] || 0) + 1;
    infl_counts[d.influence_level]     = (infl_counts[d.influence_level] || 0) + 1;
    action_counts[d.champion_action]   = (action_counts[d.champion_action] || 0) + 1;
    total_comp += d.champion_composite;
    total_dep  += d.departure_probability;
    total_eng  += d.engagement_score;
    total_inf  += d.influence_score;
    total_sta  += d.stability_score;
    total_dar  += d.deal_at_risk_score;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      status_counts,
      risk_counts,
      influence_counts: infl_counts,
      action_counts,
      avg_champion_composite:     Math.round((total_comp / n) * 10) / 10,
      avg_departure_probability:  Math.round((total_dep / n) * 10) / 10,
      stable_count:               mockDeals.filter((d) => d.is_champion_stable).length,
      backup_needed_count:        mockDeals.filter((d) => d.needs_backup_champion).length,
      avg_engagement_score:       Math.round((total_eng / n) * 10) / 10,
      avg_influence_score:        Math.round((total_inf / n) * 10) / 10,
      avg_stability_score:        Math.round((total_sta / n) * 10) / 10,
      avg_deal_at_risk_score:     Math.round((total_dar / n) * 10) / 10,
    },
  });
}
