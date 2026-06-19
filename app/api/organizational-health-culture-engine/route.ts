import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockUnits = [
  {
    unit_id: "OH-001", department: "sales", region: "EMEA",
    health_risk: "critical", culture_pattern: "toxic_culture",
    health_severity: "critical", recommended_action: "executive_intervention",
    engagement_score: 100, leadership_score: 52, culture_score: 82, wellbeing_score: 83,
    health_composite: 80.1, has_culture_alert: true, requires_executive_intervention: true,
    estimated_culture_risk_index: 5.69,
    health_signal: "Culture toxique — engagement 15% — turnover 35% — manager eff. 55% — composite 80",
  },
  {
    unit_id: "OH-002", department: "engineering", region: "NAMER",
    health_risk: "low", culture_pattern: "none",
    health_severity: "thriving", recommended_action: "no_action",
    engagement_score: 0, leadership_score: 0, culture_score: 0, wellbeing_score: 0,
    health_composite: 0.0, has_culture_alert: false, requires_executive_intervention: false,
    estimated_culture_risk_index: 0.0,
    health_signal: "Culture organisationnelle saine — engagement fort, leadership solide, bien-être optimal",
  },
  {
    unit_id: "OH-003", department: "ops", region: "APAC",
    health_risk: "critical", culture_pattern: "disengagement_spiral",
    health_severity: "critical", recommended_action: "organizational_restructuring",
    engagement_score: 87, leadership_score: 52, culture_score: 52, wellbeing_score: 70,
    health_composite: 66.1, has_culture_alert: true, requires_executive_intervention: true,
    estimated_culture_risk_index: 3.37,
    health_signal: "Spirale de désengagement — engagement 38% — turnover 28% — manager eff. 55% — composite 66",
  },
  {
    unit_id: "OH-004", department: "finance", region: "LATAM",
    health_risk: "low", culture_pattern: "none",
    health_severity: "thriving", recommended_action: "no_action",
    engagement_score: 0, leadership_score: 0, culture_score: 0, wellbeing_score: 6,
    health_composite: 1.2, has_culture_alert: false, requires_executive_intervention: false,
    estimated_culture_risk_index: 0.02,
    health_signal: "Culture organisationnelle saine — engagement fort, leadership solide, bien-être optimal",
  },
  {
    unit_id: "OH-005", department: "marketing", region: "EMEA",
    health_risk: "critical", culture_pattern: "leadership_void",
    health_severity: "critical", recommended_action: "culture_transformation",
    engagement_score: 70, leadership_score: 100, culture_score: 52, wellbeing_score: 83,
    health_composite: 75.6, has_culture_alert: true, requires_executive_intervention: true,
    estimated_culture_risk_index: 4.99,
    health_signal: "Vide de leadership — engagement 38% — turnover 18% — manager eff. 22% — composite 76",
  },
  {
    unit_id: "OH-006", department: "HR", region: "NAMER",
    health_risk: "moderate", culture_pattern: "change_resistance",
    health_severity: "stable", recommended_action: "culture_monitoring",
    engagement_score: 28, leadership_score: 39, culture_score: 28, wellbeing_score: 26,
    health_composite: 30.35, has_culture_alert: false, requires_executive_intervention: true,
    estimated_culture_risk_index: 1.4,
    health_signal: "Résistance au changement — engagement 58% — turnover 12% — manager eff. 65% — composite 30",
  },
  {
    unit_id: "OH-007", department: "product", region: "APAC",
    health_risk: "high", culture_pattern: "diversity_gap",
    health_severity: "concerning", recommended_action: "diversity_inclusion_program",
    engagement_score: 52, leadership_score: 69, culture_score: 52, wellbeing_score: 40,
    health_composite: 53.85, has_culture_alert: true, requires_executive_intervention: true,
    estimated_culture_risk_index: 2.48,
    health_signal: "Écart de diversité — engagement 55% — turnover 20% — manager eff. 60% — composite 54",
  },
  {
    unit_id: "OH-008", department: "logistics", region: "MEA",
    health_risk: "critical", culture_pattern: "disengagement_spiral",
    health_severity: "critical", recommended_action: "organizational_restructuring",
    engagement_score: 100, leadership_score: 100, culture_score: 100, wellbeing_score: 100,
    health_composite: 100.0, has_culture_alert: true, requires_executive_intervention: true,
    estimated_culture_risk_index: 7.6,
    health_signal: "Spirale de désengagement — engagement 12% — turnover 40% — manager eff. 40% — composite 100",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/organizational-health-culture-engine`);
      if (risk)    url.searchParams.set("risk",    risk);
      if (pattern) url.searchParams.set("pattern", pattern);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let units = [...mockUnits];
  if (risk)    units = units.filter((u) => u.health_risk === risk);
  if (pattern) units = units.filter((u) => u.culture_pattern === pattern);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_eng = 0, total_lead = 0, total_cult = 0,
      total_well = 0, total_risk_idx = 0;

  for (const u of mockUnits) {
    risk_counts[u.health_risk]           = (risk_counts[u.health_risk] || 0) + 1;
    pattern_counts[u.culture_pattern]    = (pattern_counts[u.culture_pattern] || 0) + 1;
    severity_counts[u.health_severity]   = (severity_counts[u.health_severity] || 0) + 1;
    action_counts[u.recommended_action]  = (action_counts[u.recommended_action] || 0) + 1;
    total_comp      += u.health_composite;
    total_eng       += u.engagement_score;
    total_lead      += u.leadership_score;
    total_cult      += u.culture_score;
    total_well      += u.wellbeing_score;
    total_risk_idx  += u.estimated_culture_risk_index;
  }

  const n = mockUnits.length;

  return NextResponse.json(sealResponse({
    units,
    summary: {
      total:                              n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_health_composite:               Math.round((total_comp     / n) * 10) / 10,
      culture_alert_count:                mockUnits.filter((u) => u.has_culture_alert).length,
      executive_intervention_count:       mockUnits.filter((u) => u.requires_executive_intervention).length,
      avg_engagement_score:               Math.round((total_eng      / n) * 10) / 10,
      avg_leadership_score:               Math.round((total_lead     / n) * 10) / 10,
      avg_culture_score:                  Math.round((total_cult     / n) * 10) / 10,
      avg_wellbeing_score:                Math.round((total_well     / n) * 10) / 10,
      avg_estimated_culture_risk_index:   Math.round((total_risk_idx / n) * 100) / 100,
    },
  } as Record<string,unknown>));
}
