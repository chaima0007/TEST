import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse({ error: "SWARM_API_URL not configured" } as Record<string,unknown>), { status: 502 });
  }
  return NextResponse.json(sealResponse({ reps: MOCK_REPS, summary: buildSummary(MOCK_REPS) } as Record<string,unknown>));
}

const MOCK_REPS = [
  { rep_id:"R001", region:"EMEA",  territory_risk:"critical",  territory_pattern:"whitespace_neglect",  territory_severity:"neglected",    recommended_action:"territory_strategy_reset",           coverage_score:88, prospecting_score:85, efficiency_score:80, segmentation_score:82, territory_composite:84.8, has_territory_gap:true,  requires_territory_coaching:true,  estimated_missed_revenue_usd:420000, territory_signal:"Whitespace neglect — 25% accounts touched — 8% whitespace coverage — 55% inactive — composite 85" },
  { rep_id:"R002", region:"APAC",  territory_risk:"critical",  territory_pattern:"density_imbalance",   territory_severity:"neglected",    recommended_action:"territory_rebalancing",              coverage_score:75, prospecting_score:70, efficiency_score:72, segmentation_score:68, territory_composite:72.4, has_territory_gap:true,  requires_territory_coaching:true,  estimated_missed_revenue_usd:350000, territory_signal:"Density imbalance — 30% accounts touched — 12% whitespace — composite 72" },
  { rep_id:"R003", region:"NOAM",  territory_risk:"high",      territory_pattern:"travel_inefficiency", territory_severity:"underserved",  recommended_action:"route_optimization_coaching",        coverage_score:52, prospecting_score:48, efficiency_score:58, segmentation_score:45, territory_composite:50.8, has_territory_gap:true,  requires_territory_coaching:true,  estimated_missed_revenue_usd:240000, territory_signal:"Travel inefficiency — 45% accounts touched — 20% whitespace — composite 51" },
  { rep_id:"R004", region:"LATAM", territory_risk:"high",      territory_pattern:"vertical_blind_spot", territory_severity:"underserved",  recommended_action:"vertical_expansion_coaching",        coverage_score:45, prospecting_score:42, efficiency_score:38, segmentation_score:52, territory_composite:44.3, has_territory_gap:true,  requires_territory_coaching:true,  estimated_missed_revenue_usd:195000, territory_signal:"Vertical blind spot — 50% accounts touched — 18% whitespace — composite 44" },
  { rep_id:"R005", region:"EMEA",  territory_risk:"moderate",  territory_pattern:"renewal_anchoring",   territory_severity:"adequate",    recommended_action:"territory_monitoring",               coverage_score:28, prospecting_score:32, efficiency_score:22, segmentation_score:25, territory_composite:26.9, has_territory_gap:true,  requires_territory_coaching:true,  estimated_missed_revenue_usd:88000,  territory_signal:"Renewal anchoring — 65% accounts touched — 22% whitespace — composite 27" },
  { rep_id:"R006", region:"APAC",  territory_risk:"low",       territory_pattern:"none",                territory_severity:"optimal",     recommended_action:"no_action",                          coverage_score:8,  prospecting_score:6,  efficiency_score:5,  segmentation_score:7,  territory_composite:6.6,  has_territory_gap:false, requires_territory_coaching:false, estimated_missed_revenue_usd:0,      territory_signal:"Territory coverage optimal — accounts touched, whitespace prospecting, travel efficiency, and segmentation within benchmarks" },
  { rep_id:"R007", region:"NOAM",  territory_risk:"high",      territory_pattern:"whitespace_neglect",  territory_severity:"underserved",  recommended_action:"whitespace_prospecting_coaching",    coverage_score:60, prospecting_score:55, efficiency_score:48, segmentation_score:52, territory_composite:55.3, has_territory_gap:true,  requires_territory_coaching:true,  estimated_missed_revenue_usd:280000, territory_signal:"Whitespace neglect — 38% accounts touched — 10% whitespace — composite 55" },
  { rep_id:"R008", region:"LATAM", territory_risk:"low",       territory_pattern:"none",                territory_severity:"optimal",     recommended_action:"no_action",                          coverage_score:5,  prospecting_score:4,  efficiency_score:6,  segmentation_score:5,  territory_composite:5.0,  has_territory_gap:false, requires_territory_coaching:false, estimated_missed_revenue_usd:0,      territory_signal:"Territory coverage optimal — all metrics within benchmarks" },
];

function buildSummary(reps: typeof MOCK_REPS) {
  const risk_counts:     Record<string,number> = {};
  const pattern_counts:  Record<string,number> = {};
  const severity_counts: Record<string,number> = {};
  const action_counts:   Record<string,number> = {};
  let comp=0, co=0, pr=0, ef=0, se=0, mr=0, gap=0, coach=0;
  for (const r of reps) {
    risk_counts[r.territory_risk]         = (risk_counts[r.territory_risk]||0)+1;
    pattern_counts[r.territory_pattern]   = (pattern_counts[r.territory_pattern]||0)+1;
    severity_counts[r.territory_severity] = (severity_counts[r.territory_severity]||0)+1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action]||0)+1;
    comp+=r.territory_composite; co+=r.coverage_score; pr+=r.prospecting_score;
    ef+=r.efficiency_score; se+=r.segmentation_score;
    mr+=r.estimated_missed_revenue_usd;
    if (r.has_territory_gap)           gap++;
    if (r.requires_territory_coaching) coach++;
  }
  const n = reps.length;
  return {
    total: n, risk_counts, pattern_counts, severity_counts, action_counts,
    avg_territory_composite:                Math.round(comp/n*10)/10,
    territory_gap_count:                    gap,
    coaching_count:                         coach,
    avg_coverage_score:                     Math.round(co/n*10)/10,
    avg_prospecting_score:                  Math.round(pr/n*10)/10,
    avg_efficiency_score:                   Math.round(ef/n*10)/10,
    avg_segmentation_score:                 Math.round(se/n*10)/10,
    total_estimated_missed_revenue_usd:     Math.round(mr*100)/100,
  };
}
