import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockIncidents = [
  {
    incident_id: "CR-001", brand_entity: "AcmeCorp", region: "NAMER",
    crisis_risk: "critical", crisis_pattern: "social_media_storm",
    crisis_severity: "emergency", recommended_action: "crisis_war_room",
    media_score: 100, social_score: 100, legal_score: 98, reputation_score: 100,
    crisis_composite: 99.5, has_active_crisis: true,
    requires_executive_response: true,
    estimated_reputation_damage_score: 9.45,
    crisis_signal: "Social media storm forming — 78% negative — 15.0M reach — trust 8% — composite 100",
  },
  {
    incident_id: "CR-002", brand_entity: "BetaBrand", region: "EMEA",
    crisis_risk: "critical", crisis_pattern: "reputational_attack",
    crisis_severity: "emergency", recommended_action: "executive_response",
    media_score: 80, social_score: 75, legal_score: 70, reputation_score: 85,
    crisis_composite: 77.25, has_active_crisis: true,
    requires_executive_response: true,
    estimated_reputation_damage_score: 6.95,
    crisis_signal: "Reputational attack detected — 65% negative — 12.0M reach — trust 15% — composite 77",
  },
  {
    incident_id: "CR-003", brand_entity: "CloudCo", region: "APAC",
    crisis_risk: "high", crisis_pattern: "regulatory_scrutiny",
    crisis_severity: "crisis", recommended_action: "legal_hold",
    media_score: 55, social_score: 45, legal_score: 72, reputation_score: 50,
    crisis_composite: 55.4, has_active_crisis: true,
    requires_executive_response: true,
    estimated_reputation_damage_score: 4.43,
    crisis_signal: "Regulatory scrutiny elevated — 45% negative — 8.5M reach — trust 35% — composite 55",
  },
  {
    incident_id: "CR-004", brand_entity: "DeltaGroup", region: "NAMER",
    crisis_risk: "high", crisis_pattern: "executive_misconduct",
    crisis_severity: "crisis", recommended_action: "executive_response",
    media_score: 60, social_score: 50, legal_score: 65, reputation_score: 55,
    crisis_composite: 57.75, has_active_crisis: true,
    requires_executive_response: true,
    estimated_reputation_damage_score: 4.62,
    crisis_signal: "Executive misconduct signal — 55% negative — 6.0M reach — trust 30% — composite 58",
  },
  {
    incident_id: "CR-005", brand_entity: "EchoMedia", region: "LATAM",
    crisis_risk: "high", crisis_pattern: "media_escalation",
    crisis_severity: "crisis", recommended_action: "executive_response",
    media_score: 70, social_score: 40, legal_score: 35, reputation_score: 48,
    crisis_composite: 49.35, has_active_crisis: true,
    requires_executive_response: true,
    estimated_reputation_damage_score: 3.45,
    crisis_signal: "Media escalation in progress — 42% negative — 9.0M reach — trust 40% — composite 49",
  },
  {
    incident_id: "CR-006", brand_entity: "FusionRetail", region: "EMEA",
    crisis_risk: "moderate", crisis_pattern: "none",
    crisis_severity: "elevated", recommended_action: "proactive_statement",
    media_score: 30, social_score: 28, legal_score: 22, reputation_score: 35,
    crisis_composite: 28.45, has_active_crisis: false,
    requires_executive_response: false,
    estimated_reputation_damage_score: 1.42,
    crisis_signal: "Nominal — 25% negative — 2.5M reach — trust 62% — composite 28",
  },
  {
    incident_id: "CR-007", brand_entity: "GlobeTech", region: "APAC",
    crisis_risk: "moderate", crisis_pattern: "none",
    crisis_severity: "elevated", recommended_action: "proactive_statement",
    media_score: 25, social_score: 22, legal_score: 18, reputation_score: 30,
    crisis_composite: 23.6, has_active_crisis: false,
    requires_executive_response: false,
    estimated_reputation_damage_score: 1.18,
    crisis_signal: "Nominal — 22% negative — 1.8M reach — trust 68% — composite 24",
  },
  {
    incident_id: "CR-008", brand_entity: "HarborBrands", region: "NAMER",
    crisis_risk: "low", crisis_pattern: "none",
    crisis_severity: "nominal", recommended_action: "no_action",
    media_score: 8, social_score: 10, legal_score: 5, reputation_score: 6,
    crisis_composite: 7.4, has_active_crisis: false,
    requires_executive_response: false,
    estimated_reputation_damage_score: 0.07,
    crisis_signal: "Brand reputation stable — media, social and legal indicators within normal parameters",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");
  const region  = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/pr-crisis-management-engine`);
      if (risk)    url.searchParams.set("risk",    risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      if (region)  url.searchParams.set("region",  region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let incidents = [...mockIncidents];
  if (risk)    incidents = incidents.filter((c) => c.crisis_risk === risk);
  if (pattern) incidents = incidents.filter((c) => c.crisis_pattern === pattern);
  if (region)  incidents = incidents.filter((c) => c.region === region);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_med = 0, total_soc = 0, total_leg = 0,
      total_rep = 0, total_dmg = 0;

  for (const c of mockIncidents) {
    risk_counts[c.crisis_risk]         = (risk_counts[c.crisis_risk] || 0) + 1;
    pattern_counts[c.crisis_pattern]   = (pattern_counts[c.crisis_pattern] || 0) + 1;
    severity_counts[c.crisis_severity] = (severity_counts[c.crisis_severity] || 0) + 1;
    action_counts[c.recommended_action] = (action_counts[c.recommended_action] || 0) + 1;
    total_comp += c.crisis_composite;
    total_med  += c.media_score;
    total_soc  += c.social_score;
    total_leg  += c.legal_score;
    total_rep  += c.reputation_score;
    total_dmg  += c.estimated_reputation_damage_score;
  }

  const n = mockIncidents.length;

  return NextResponse.json({
    incidents,
    summary: {
      total:                                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_crisis_composite:                     Math.round((total_comp / n) * 10) / 10,
      active_crisis_count:                      mockIncidents.filter((c) => c.has_active_crisis).length,
      executive_response_count:                 mockIncidents.filter((c) => c.requires_executive_response).length,
      avg_media_score:                          Math.round((total_med / n) * 10) / 10,
      avg_social_score:                         Math.round((total_soc / n) * 10) / 10,
      avg_legal_score:                          Math.round((total_leg / n) * 10) / 10,
      avg_reputation_score:                     Math.round((total_rep / n) * 10) / 10,
      avg_estimated_reputation_damage_score:    Math.round((total_dmg / n) * 100) / 100,
    },
  });
}
