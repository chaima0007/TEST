import { NextResponse } from "next/server";

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json({ error: "SWARM_API_URL not configured" }, { status: 503 });
  }
  return NextResponse.json({ reps: MOCK_REPS, summary: buildSummary(MOCK_REPS) });
}

const MOCK_REPS = [
  { rep_id:"R001", region:"EMEA",  forecast_risk:"critical",  forecast_pattern:"chronic_overcommit", forecast_severity:"deceptive",   recommended_action:"forecast_audit",                   accuracy_score:90, consistency_score:88, pipeline_quality_score:85, calibration_score:82, forecast_composite:87.8, has_forecast_gap:true,  requires_forecast_coaching:true,  estimated_forecast_error_usd:480000, forecast_signal:"Chronic overcommit — 55% forecast accuracy — 40% avg commit variance — 50% late-quarter slip — composite 88" },
  { rep_id:"R002", region:"APAC",  forecast_risk:"critical",  forecast_pattern:"stage_inflate",      forecast_severity:"deceptive",   recommended_action:"forecast_audit",                   accuracy_score:75, consistency_score:70, pipeline_quality_score:80, calibration_score:72, forecast_composite:74.9, has_forecast_gap:true,  requires_forecast_coaching:true,  estimated_forecast_error_usd:350000, forecast_signal:"Stage inflate — 62% forecast accuracy — 30% commit variance — composite 75" },
  { rep_id:"R003", region:"NOAM",  forecast_risk:"high",      forecast_pattern:"volatile_caller",    forecast_severity:"unreliable",  recommended_action:"forecast_review_escalation",       accuracy_score:55, consistency_score:58, pipeline_quality_score:52, calibration_score:48, forecast_composite:53.9, has_forecast_gap:true,  requires_forecast_coaching:true,  estimated_forecast_error_usd:195000, forecast_signal:"Volatile caller — 72% forecast accuracy — 28% commit variance — composite 54" },
  { rep_id:"R004", region:"LATAM", forecast_risk:"high",      forecast_pattern:"late_quarter_crash", forecast_severity:"unreliable",  recommended_action:"forecast_review_escalation",       accuracy_score:48, consistency_score:52, pipeline_quality_score:45, calibration_score:40, forecast_composite:47.5, has_forecast_gap:true,  requires_forecast_coaching:true,  estimated_forecast_error_usd:160000, forecast_signal:"Late-quarter crash — 75% forecast accuracy — 22% commit variance — composite 48" },
  { rep_id:"R005", region:"EMEA",  forecast_risk:"moderate",  forecast_pattern:"sandbagger",         forecast_severity:"acceptable",  recommended_action:"forecast_calibration_coaching",     accuracy_score:28, consistency_score:25, pipeline_quality_score:22, calibration_score:20, forecast_composite:24.8, has_forecast_gap:true,  requires_forecast_coaching:true,  estimated_forecast_error_usd:68000,  forecast_signal:"Sandbagger — 87% forecast accuracy — 12% commit variance — composite 25" },
  { rep_id:"R006", region:"APAC",  forecast_risk:"low",       forecast_pattern:"none",               forecast_severity:"precise",     recommended_action:"no_action",                        accuracy_score:8,  consistency_score:6,  pipeline_quality_score:5,  calibration_score:4,  forecast_composite:6.3,  has_forecast_gap:false, requires_forecast_coaching:false, estimated_forecast_error_usd:0,      forecast_signal:"Forecast accuracy strong — commit variance, pipeline quality, stage accuracy, and calibration within benchmarks" },
  { rep_id:"R007", region:"NOAM",  forecast_risk:"high",      forecast_pattern:"chronic_overcommit", forecast_severity:"unreliable",  recommended_action:"forecast_discipline_coaching",     accuracy_score:62, consistency_score:58, pipeline_quality_score:55, calibration_score:50, forecast_composite:58.0, has_forecast_gap:true,  requires_forecast_coaching:true,  estimated_forecast_error_usd:240000, forecast_signal:"Chronic overcommit — 66% forecast accuracy — 22% commit variance — composite 58" },
  { rep_id:"R008", region:"LATAM", forecast_risk:"low",       forecast_pattern:"none",               forecast_severity:"precise",     recommended_action:"no_action",                        accuracy_score:5,  consistency_score:4,  pipeline_quality_score:6,  calibration_score:3,  forecast_composite:4.6,  has_forecast_gap:false, requires_forecast_coaching:false, estimated_forecast_error_usd:0,      forecast_signal:"Forecast accuracy strong — all metrics within benchmarks" },
];

function buildSummary(reps: typeof MOCK_REPS) {
  const risk_counts:     Record<string,number> = {};
  const pattern_counts:  Record<string,number> = {};
  const severity_counts: Record<string,number> = {};
  const action_counts:   Record<string,number> = {};
  let comp=0, ac=0, co=0, pq=0, ca=0, fe=0, gap=0, coach=0;
  for (const r of reps) {
    risk_counts[r.forecast_risk]         = (risk_counts[r.forecast_risk]||0)+1;
    pattern_counts[r.forecast_pattern]   = (pattern_counts[r.forecast_pattern]||0)+1;
    severity_counts[r.forecast_severity] = (severity_counts[r.forecast_severity]||0)+1;
    action_counts[r.recommended_action]  = (action_counts[r.recommended_action]||0)+1;
    comp+=r.forecast_composite; ac+=r.accuracy_score; co+=r.consistency_score;
    pq+=r.pipeline_quality_score; ca+=r.calibration_score;
    fe+=r.estimated_forecast_error_usd;
    if (r.has_forecast_gap)           gap++;
    if (r.requires_forecast_coaching) coach++;
  }
  const n = reps.length;
  return {
    total: n, risk_counts, pattern_counts, severity_counts, action_counts,
    avg_forecast_composite:                 Math.round(comp/n*10)/10,
    forecast_gap_count:                     gap,
    coaching_count:                         coach,
    avg_accuracy_score:                     Math.round(ac/n*10)/10,
    avg_consistency_score:                  Math.round(co/n*10)/10,
    avg_pipeline_quality_score:             Math.round(pq/n*10)/10,
    avg_calibration_score:                  Math.round(ca/n*10)/10,
    total_estimated_forecast_error_usd:     Math.round(fe*100)/100,
  };
}
