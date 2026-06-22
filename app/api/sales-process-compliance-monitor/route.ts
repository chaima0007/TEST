import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-process-compliance-monitor] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "deal_001", rep_id: "rep_003", rep_name: "Alice Martin", region: "NAMER",
    compliance_level: "full", methodology_adherence: "champion",
    compliance_risk: "low", compliance_action: "maintain",
    discovery_score: 100.0, qualification_score: 100.0,
    progression_score: 98.0, crm_hygiene_score: 98.8,
    compliance_composite: 99.5, missing_steps_count: 0,
    is_compliant: true, needs_process_coaching: false,
    key_gap: "none",
    deal_stage: "negotiation",
  },
  {
    deal_id: "deal_002", rep_id: "rep_001", rep_name: "Bruno Silva", region: "EMEA",
    compliance_level: "non_compliant", methodology_adherence: "at_risk",
    compliance_risk: "critical", compliance_action: "remediate",
    discovery_score: 10.0, qualification_score: 0.0,
    progression_score: 5.0, crm_hygiene_score: 12.0,
    compliance_composite: 6.7, missing_steps_count: 9,
    is_compliant: false, needs_process_coaching: true,
    key_gap: "champion not identified",
    deal_stage: "discovery",
  },
  {
    deal_id: "deal_003", rep_id: "rep_002", rep_name: "Clara Nguyen", region: "APAC",
    compliance_level: "partial", methodology_adherence: "solid",
    compliance_risk: "moderate", compliance_action: "coach_gaps",
    discovery_score: 75.0, qualification_score: 70.0,
    progression_score: 55.0, crm_hygiene_score: 62.5,
    compliance_composite: 66.3, missing_steps_count: 3,
    is_compliant: false, needs_process_coaching: false,
    key_gap: "business case not built",
    deal_stage: "proposal",
  },
  {
    deal_id: "deal_004", rep_id: "rep_005", rep_name: "Diego Ferreira", region: "LATAM",
    compliance_level: "minimal", methodology_adherence: "improvable",
    compliance_risk: "high", compliance_action: "process_review",
    discovery_score: 40.0, qualification_score: 25.0,
    progression_score: 30.0, crm_hygiene_score: 35.0,
    compliance_composite: 33.0, missing_steps_count: 6,
    is_compliant: false, needs_process_coaching: true,
    key_gap: "budget not confirmed",
    deal_stage: "qualification",
  },
  {
    deal_id: "deal_005", rep_id: "rep_007", rep_name: "Elena Kovacs", region: "EMEA",
    compliance_level: "full", methodology_adherence: "champion",
    compliance_risk: "low", compliance_action: "maintain",
    discovery_score: 90.0, qualification_score: 95.0,
    progression_score: 80.0, crm_hygiene_score: 87.5,
    compliance_composite: 88.3, missing_steps_count: 1,
    is_compliant: true, needs_process_coaching: false,
    key_gap: "legal review not started",
    deal_stage: "closing",
  },
  {
    deal_id: "deal_006", rep_id: "rep_004", rep_name: "Felix Okafor", region: "NAMER",
    compliance_level: "partial", methodology_adherence: "improvable",
    compliance_risk: "moderate", compliance_action: "coach_gaps",
    discovery_score: 60.0, qualification_score: 50.0,
    progression_score: 45.0, crm_hygiene_score: 55.0,
    compliance_composite: 53.0, missing_steps_count: 4,
    is_compliant: false, needs_process_coaching: true,
    key_gap: "decision process not mapped",
    deal_stage: "demo",
  },
  {
    deal_id: "deal_007", rep_id: "rep_006", rep_name: "Gabriela Torres", region: "LATAM",
    compliance_level: "full", methodology_adherence: "solid",
    compliance_risk: "low", compliance_action: "maintain",
    discovery_score: 85.0, qualification_score: 80.0,
    progression_score: 70.0, crm_hygiene_score: 75.0,
    compliance_composite: 78.5, missing_steps_count: 2,
    is_compliant: true, needs_process_coaching: false,
    key_gap: "weakest area: progression",
    deal_stage: "proposal",
  },
  {
    deal_id: "deal_008", rep_id: "rep_008", rep_name: "Hiro Tanaka", region: "APAC",
    compliance_level: "minimal", methodology_adherence: "at_risk",
    compliance_risk: "high", compliance_action: "process_review",
    discovery_score: 25.0, qualification_score: 20.0,
    progression_score: 15.0, crm_hygiene_score: 25.0,
    compliance_composite: 21.5, missing_steps_count: 7,
    is_compliant: false, needs_process_coaching: true,
    key_gap: "champion not identified",
    deal_stage: "discovery",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const level  = searchParams.get("level");
  const risk   = searchParams.get("risk");
  const region = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-process-compliance-monitor`);
      if (level)  url.searchParams.set("level", level);
      if (risk)   url.searchParams.set("risk", risk);
      if (region) url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let deals = [...mockDeals];
  if (level)  deals = deals.filter((d) => d.compliance_level === level);
  if (risk)   deals = deals.filter((d) => d.compliance_risk === risk);
  if (region) deals = deals.filter((d) => d.region === region);

  const level_counts:     Record<string, number> = {};
  const adherence_counts: Record<string, number> = {};
  const risk_counts:      Record<string, number> = {};
  const action_counts:    Record<string, number> = {};
  let total_comp = 0, total_disc = 0, total_qual = 0, total_prog = 0, total_crm = 0, total_miss = 0;

  for (const d of mockDeals) {
    level_counts[d.compliance_level]        = (level_counts[d.compliance_level] || 0) + 1;
    adherence_counts[d.methodology_adherence] = (adherence_counts[d.methodology_adherence] || 0) + 1;
    risk_counts[d.compliance_risk]          = (risk_counts[d.compliance_risk] || 0) + 1;
    action_counts[d.compliance_action]      = (action_counts[d.compliance_action] || 0) + 1;
    total_comp += d.compliance_composite;
    total_disc += d.discovery_score;
    total_qual += d.qualification_score;
    total_prog += d.progression_score;
    total_crm  += d.crm_hygiene_score;
    total_miss += d.missing_steps_count;
  }

  const n = mockDeals.length;

  return sealResponse(NextResponse.json({
    deals,
    summary: {
      total: n,
      compliance_level_counts:      level_counts,
      methodology_adherence_counts: adherence_counts,
      compliance_risk_counts:       risk_counts,
      action_counts,
      avg_compliance_composite:   Math.round((total_comp / n) * 10) / 10,
      fully_compliant_count:      mockDeals.filter((d) => d.is_compliant).length,
      coaching_needed_count:      mockDeals.filter((d) => d.needs_process_coaching).length,
      avg_discovery_score:        Math.round((total_disc / n) * 10) / 10,
      avg_qualification_score:    Math.round((total_qual / n) * 10) / 10,
      avg_progression_score:      Math.round((total_prog / n) * 10) / 10,
      avg_crm_hygiene_score:      Math.round((total_crm / n) * 10) / 10,
      avg_missing_steps:          Math.round((total_miss / n) * 10) / 10,
    },
  }));
}
