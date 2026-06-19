import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockLearners = [
  {
    learner_id: "LP-001", region: "North America",
    learning_risk: "low", learning_pattern: "none", learning_severity: "thriving",
    recommended_action: "no_action",
    engagement_score_calc: 8.0, retention_score: 6.0, application_score: 10.0, alignment_score: 8.0,
    learning_composite: 8.05, has_learning_gap: false, requires_path_adjustment: false,
    estimated_learning_velocity_index: 0.08,
    learning_signal: "Learning engagement strong — completion, retention, application and alignment exceeding benchmarks",
  },
  {
    learner_id: "LP-002", region: "EMEA",
    learning_risk: "moderate", learning_pattern: "none", learning_severity: "progressing",
    recommended_action: "coaching_session",
    engagement_score_calc: 22.0, retention_score: 18.0, application_score: 20.0, alignment_score: 22.0,
    learning_composite: 20.65, has_learning_gap: false, requires_path_adjustment: true,
    estimated_learning_velocity_index: 1.24,
    learning_signal: "Moderate — 70% completion — retention 65% — 10d since last learning — composite 21",
  },
  {
    learner_id: "LP-003", region: "APAC",
    learning_risk: "moderate", learning_pattern: "learning_style_conflict", learning_severity: "progressing",
    recommended_action: "coaching_session",
    engagement_score_calc: 28.0, retention_score: 30.0, application_score: 40.0, alignment_score: 24.0,
    learning_composite: 30.1, has_learning_gap: false, requires_path_adjustment: true,
    estimated_learning_velocity_index: 1.81,
    learning_signal: "Moderate — 60% completion — retention 58% — 12d since last learning — composite 30",
  },
  {
    learner_id: "LP-004", region: "LATAM",
    learning_risk: "high", learning_pattern: "plateau_risk", learning_severity: "stalling",
    recommended_action: "content_refresh",
    engagement_score_calc: 48.0, retention_score: 62.0, application_score: 38.0, alignment_score: 40.0,
    learning_composite: 47.9, has_learning_gap: true, requires_path_adjustment: true,
    estimated_learning_velocity_index: 3.83,
    learning_signal: "High — 48% completion — retention 42% — 18d since last learning — composite 48",
  },
  {
    learner_id: "LP-005", region: "North America",
    learning_risk: "high", learning_pattern: "disengaged_learner", learning_severity: "stalling",
    recommended_action: "coaching_session",
    engagement_score_calc: 65.0, retention_score: 30.0, application_score: 28.0, alignment_score: 38.0,
    learning_composite: 41.7, has_learning_gap: true, requires_path_adjustment: true,
    estimated_learning_velocity_index: 4.17,
    learning_signal: "High — 40% completion — retention 55% — 25d since last learning — composite 42",
  },
  {
    learner_id: "LP-006", region: "EMEA",
    learning_risk: "high", learning_pattern: "high_potential_redirect", learning_severity: "stalling",
    recommended_action: "mentorship_match",
    engagement_score_calc: 8.0, retention_score: 8.0, application_score: 45.0, alignment_score: 65.0,
    learning_composite: 29.65, has_learning_gap: false, requires_path_adjustment: true,
    estimated_learning_velocity_index: 1.78,
    learning_signal: "High — 82% completion — retention 80% — 7d since last learning — composite 30",
  },
  {
    learner_id: "LP-007", region: "APAC",
    learning_risk: "critical", learning_pattern: "plateau_risk", learning_severity: "regressing",
    recommended_action: "intensive_bootcamp",
    engagement_score_calc: 80.0, retention_score: 80.0, application_score: 75.0, alignment_score: 65.0,
    learning_composite: 75.75, has_learning_gap: true, requires_path_adjustment: true,
    estimated_learning_velocity_index: 7.58,
    learning_signal: "Critical — 28% completion — retention 30% — 35d since last learning — composite 76",
  },
  {
    learner_id: "LP-008", region: "LATAM",
    learning_risk: "critical", learning_pattern: "disengaged_learner", learning_severity: "regressing",
    recommended_action: "intensive_bootcamp",
    engagement_score_calc: 88.0, retention_score: 72.0, application_score: 70.0, alignment_score: 68.0,
    learning_composite: 75.1, has_learning_gap: true, requires_path_adjustment: true,
    estimated_learning_velocity_index: 8.26,
    learning_signal: "Critical — 22% completion — retention 35% — 40d since last learning — composite 75",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk     = searchParams.get("risk");
  const pattern  = searchParams.get("pattern");
  const severity = searchParams.get("severity");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/personalized-learning-path-engine`);
      if (risk)     url.searchParams.set("risk",     risk);
      if (pattern)  url.searchParams.set("pattern",  pattern);
      if (severity) url.searchParams.set("severity", severity);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let learners = [...mockLearners];
  if (risk)     learners = learners.filter((l) => l.learning_risk === risk);
  if (pattern)  learners = learners.filter((l) => l.learning_pattern === pattern);
  if (severity) learners = learners.filter((l) => l.learning_severity === severity);

  const risk_counts:     Record<string, number> = {};
  const pattern_counts:  Record<string, number> = {};
  const severity_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_comp = 0, total_eng = 0, total_ret = 0, total_app = 0, total_aln = 0, total_vel = 0;

  for (const l of mockLearners) {
    risk_counts[l.learning_risk]        = (risk_counts[l.learning_risk] || 0) + 1;
    pattern_counts[l.learning_pattern]  = (pattern_counts[l.learning_pattern] || 0) + 1;
    severity_counts[l.learning_severity] = (severity_counts[l.learning_severity] || 0) + 1;
    action_counts[l.recommended_action] = (action_counts[l.recommended_action] || 0) + 1;
    total_comp += l.learning_composite;
    total_eng  += l.engagement_score_calc;
    total_ret  += l.retention_score;
    total_app  += l.application_score;
    total_aln  += l.alignment_score;
    total_vel  += l.estimated_learning_velocity_index;
  }

  const n = mockLearners.length;

  return NextResponse.json({
    learners,
    summary: {
      total:                                    n,
      risk_counts,
      pattern_counts,
      severity_counts,
      action_counts,
      avg_learning_composite:                   Math.round((total_comp / n) * 100) / 100,
      learning_gap_count:                       mockLearners.filter((l) => l.has_learning_gap).length,
      path_adjustment_count:                    mockLearners.filter((l) => l.requires_path_adjustment).length,
      avg_engagement_score_calc:                Math.round((total_eng / n) * 100) / 100,
      avg_retention_score:                      Math.round((total_ret / n) * 100) / 100,
      avg_application_score:                    Math.round((total_app / n) * 100) / 100,
      avg_alignment_score:                      Math.round((total_aln / n) * 100) / 100,
      avg_estimated_learning_velocity_index:    Math.round((total_vel / n) * 100) / 100,
    },
  });
}
