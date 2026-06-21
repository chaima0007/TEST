import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse({ error: "SWARM_API_URL not configured" } as Record<string,unknown>), { status: 502 });
  }
  return NextResponse.json(sealResponse({ reps: MOCK_REPS, summary: buildSummary(MOCK_REPS) } as Record<string,unknown>));
}

const MOCK_REPS = [
  { rep_id:"R001", region:"EMEA",   hyg_risk:"critical",  hyg_pattern:"ghost_pipeline",   hyg_severity:"corrupted",  recommended_action:"crm_data_reset",           completeness_score:88, currency_score:85, accuracy_score:82, activity_capture_score:80, hyg_composite:85.2, has_hyg_gap:true,  requires_hyg_coaching:true,  estimated_forecast_error_usd:95000, hyg_signal:"Ghost pipeline — 45% deals missing contacts — stale rate 55% — composite 85" },
  { rep_id:"R002", region:"APAC",   hyg_risk:"high",      hyg_pattern:"field_skipper",    hyg_severity:"degraded",   recommended_action:"data_entry_coaching",       completeness_score:62, currency_score:55, accuracy_score:58, activity_capture_score:50, hyg_composite:57.4, has_hyg_gap:true,  requires_hyg_coaching:true,  estimated_forecast_error_usd:62000, hyg_signal:"Field skipper — low required-field completion — composite 57" },
  { rep_id:"R003", region:"NOAM",   hyg_risk:"high",      hyg_pattern:"stage_freezer",    hyg_severity:"degraded",   recommended_action:"stage_hygiene_coaching",    completeness_score:55, currency_score:48, accuracy_score:52, activity_capture_score:45, hyg_composite:51.8, has_hyg_gap:true,  requires_hyg_coaching:true,  estimated_forecast_error_usd:58000, hyg_signal:"Stage freezer — low stage advancement rate — composite 52" },
  { rep_id:"R004", region:"LATAM",  hyg_risk:"moderate",  hyg_pattern:"contact_orphaner", hyg_severity:"adequate",   recommended_action:"contact_linking_coaching",  completeness_score:38, currency_score:32, accuracy_score:35, activity_capture_score:30, hyg_composite:34.1, has_hyg_gap:true,  requires_hyg_coaching:true,  estimated_forecast_error_usd:38000, hyg_signal:"Contact orphaner — deals unlinked to contacts — composite 34" },
  { rep_id:"R005", region:"EMEA",   hyg_risk:"moderate",  hyg_pattern:"activity_shadow",  hyg_severity:"adequate",   recommended_action:"activity_logging_coaching", completeness_score:30, currency_score:25, accuracy_score:28, activity_capture_score:22, hyg_composite:26.8, has_hyg_gap:true,  requires_hyg_coaching:true,  estimated_forecast_error_usd:29000, hyg_signal:"Activity shadow — low activity log rate — composite 27" },
  { rep_id:"R006", region:"APAC",   hyg_risk:"low",       hyg_pattern:"none",             hyg_severity:"clean",      recommended_action:"no_action",                completeness_score:12, currency_score:10, accuracy_score:8,  activity_capture_score:6,  hyg_composite:9.8,  has_hyg_gap:false, requires_hyg_coaching:false, estimated_forecast_error_usd:0,     hyg_signal:"CRM data hygiene strong — all metrics within benchmarks" },
  { rep_id:"R007", region:"NOAM",   hyg_risk:"critical",  hyg_pattern:"ghost_pipeline",   hyg_severity:"corrupted",  recommended_action:"crm_audit_required",        completeness_score:82, currency_score:78, accuracy_score:75, activity_capture_score:70, hyg_composite:77.5, has_hyg_gap:true,  requires_hyg_coaching:true,  estimated_forecast_error_usd:88000, hyg_signal:"Ghost pipeline — missing contacts across 40% of deals — composite 78" },
  { rep_id:"R008", region:"LATAM",  hyg_risk:"low",       hyg_pattern:"none",             hyg_severity:"clean",      recommended_action:"no_action",                completeness_score:8,  currency_score:6,  accuracy_score:5,  activity_capture_score:4,  hyg_composite:6.4,  has_hyg_gap:false, requires_hyg_coaching:false, estimated_forecast_error_usd:0,     hyg_signal:"CRM data hygiene strong — all metrics within benchmarks" },
];

function buildSummary(reps: typeof MOCK_REPS) {
  const risk_counts: Record<string,number>    = {};
  const pattern_counts: Record<string,number> = {};
  const severity_counts: Record<string,number>= {};
  const action_counts: Record<string,number>  = {};
  let comp=0, cs=0, cu=0, ac=0, av=0, qr=0, gap=0, coach=0;
  for (const r of reps) {
    risk_counts[r.hyg_risk]             = (risk_counts[r.hyg_risk]||0)+1;
    pattern_counts[r.hyg_pattern]       = (pattern_counts[r.hyg_pattern]||0)+1;
    severity_counts[r.hyg_severity]     = (severity_counts[r.hyg_severity]||0)+1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action]||0)+1;
    comp+=r.hyg_composite; cs+=r.completeness_score; cu+=r.currency_score;
    ac+=r.accuracy_score;  av+=r.activity_capture_score;
    qr+=r.estimated_forecast_error_usd;
    if (r.has_hyg_gap)           gap++;
    if (r.requires_hyg_coaching) coach++;
  }
  const n = reps.length;
  return {
    total: n, risk_counts, pattern_counts, severity_counts, action_counts,
    avg_hyg_composite:                  Math.round(comp/n*10)/10,
    hyg_gap_count:                      gap,
    coaching_count:                     coach,
    avg_completeness_score:             Math.round(cs/n*10)/10,
    avg_currency_score:                 Math.round(cu/n*10)/10,
    avg_accuracy_score:                 Math.round(ac/n*10)/10,
    avg_activity_capture_score:         Math.round(av/n*10)/10,
    total_estimated_forecast_error_usd: Math.round(qr*100)/100,
  };
}
