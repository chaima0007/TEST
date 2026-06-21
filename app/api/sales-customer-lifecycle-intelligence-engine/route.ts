import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse({ error: "SWARM_API_URL not configured" } as Record<string,unknown>), { status: 502 });
  }
  return NextResponse.json(sealResponse({ reps: MOCK_REPS, summary: buildSummary(MOCK_REPS) } as Record<string,unknown>));
}

const MOCK_REPS = [
  { rep_id:"R001", region:"EMEA",  lifecycle_risk:"critical",  lifecycle_pattern:"churn_trajectory",  lifecycle_severity:"critical",  recommended_action:"emergency_save_intervention", adoption_score:88, engagement_score:90, renewal_readiness_score:85, expansion_potential_score:82, lifecycle_composite:86.8, has_lifecycle_gap:true,  requires_lifecycle_intervention:true,  estimated_churn_risk_usd:95000,  lifecycle_signal:"Churn trajectory — 20% adoption — 70d since last touch — 25d to renewal — composite 87" },
  { rep_id:"R002", region:"APAC",  lifecycle_risk:"high",      lifecycle_pattern:"expansion_stall",   lifecycle_severity:"declining",  recommended_action:"expansion_play",              adoption_score:55, engagement_score:52, renewal_readiness_score:48, expansion_potential_score:60, lifecycle_composite:53.4, has_lifecycle_gap:true,  requires_lifecycle_intervention:true,  estimated_churn_risk_usd:58000,  lifecycle_signal:"Expansion stall — 48% adoption — 35d since last touch — 95d to renewal — composite 53" },
  { rep_id:"R003", region:"NOAM",  lifecycle_risk:"high",      lifecycle_pattern:"adoption_lag",      lifecycle_severity:"declining",  recommended_action:"adoption_coaching",            adoption_score:62, engagement_score:44, renewal_readiness_score:38, expansion_potential_score:50, lifecycle_composite:49.6, has_lifecycle_gap:true,  requires_lifecycle_intervention:true,  estimated_churn_risk_usd:50000,  lifecycle_signal:"Adoption lag — 30% adoption — 20d since last touch — 120d to renewal — composite 50" },
  { rep_id:"R004", region:"LATAM", lifecycle_risk:"high",      lifecycle_pattern:"renewal_cliff",     lifecycle_severity:"declining",  recommended_action:"churn_prevention_outreach",    adoption_score:40, engagement_score:48, renewal_readiness_score:75, expansion_potential_score:35, lifecycle_composite:49.1, has_lifecycle_gap:true,  requires_lifecycle_intervention:true,  estimated_churn_risk_usd:42000,  lifecycle_signal:"Renewal cliff — 55% adoption — 28d since last touch — 38d to renewal — composite 49" },
  { rep_id:"R005", region:"EMEA",  lifecycle_risk:"moderate",  lifecycle_pattern:"dormant_account",   lifecycle_severity:"stable",     recommended_action:"health_monitoring",            adoption_score:25, engagement_score:38, renewal_readiness_score:20, expansion_potential_score:28, lifecycle_composite:27.4, has_lifecycle_gap:true,  requires_lifecycle_intervention:true,  estimated_churn_risk_usd:22000,  lifecycle_signal:"Dormant account — 60% adoption — 52d since last touch — 180d to renewal — composite 27" },
  { rep_id:"R006", region:"APAC",  lifecycle_risk:"low",       lifecycle_pattern:"none",              lifecycle_severity:"thriving",   recommended_action:"no_action",                   adoption_score:8,  engagement_score:6,  renewal_readiness_score:5,  expansion_potential_score:4,  lifecycle_composite:5.9,  has_lifecycle_gap:false, requires_lifecycle_intervention:false, estimated_churn_risk_usd:0,      lifecycle_signal:"Customer lifecycle healthy — strong adoption, engagement, renewal readiness, and expansion trajectory" },
  { rep_id:"R007", region:"NOAM",  lifecycle_risk:"critical",  lifecycle_pattern:"churn_trajectory",  lifecycle_severity:"critical",   recommended_action:"emergency_save_intervention",  adoption_score:82, engagement_score:78, renewal_readiness_score:80, expansion_potential_score:76, lifecycle_composite:79.7, has_lifecycle_gap:true,  requires_lifecycle_intervention:true,  estimated_churn_risk_usd:88000,  lifecycle_signal:"Churn trajectory — 15% adoption — 65d since last touch — 20d to renewal — composite 80" },
  { rep_id:"R008", region:"LATAM", lifecycle_risk:"low",       lifecycle_pattern:"none",              lifecycle_severity:"thriving",   recommended_action:"no_action",                   adoption_score:5,  engagement_score:4,  renewal_readiness_score:3,  expansion_potential_score:6,  lifecycle_composite:4.4,  has_lifecycle_gap:false, requires_lifecycle_intervention:false, estimated_churn_risk_usd:0,      lifecycle_signal:"Customer lifecycle healthy — strong adoption, engagement, renewal readiness, and expansion trajectory" },
];

function buildSummary(reps: typeof MOCK_REPS) {
  const risk_counts:     Record<string,number> = {};
  const pattern_counts:  Record<string,number> = {};
  const severity_counts: Record<string,number> = {};
  const action_counts:   Record<string,number> = {};
  let comp=0, ad=0, en=0, rr=0, ep=0, cr=0, gap=0, intv=0;
  for (const r of reps) {
    risk_counts[r.lifecycle_risk]         = (risk_counts[r.lifecycle_risk]||0)+1;
    pattern_counts[r.lifecycle_pattern]   = (pattern_counts[r.lifecycle_pattern]||0)+1;
    severity_counts[r.lifecycle_severity] = (severity_counts[r.lifecycle_severity]||0)+1;
    action_counts[r.recommended_action]   = (action_counts[r.recommended_action]||0)+1;
    comp+=r.lifecycle_composite; ad+=r.adoption_score; en+=r.engagement_score;
    rr+=r.renewal_readiness_score; ep+=r.expansion_potential_score;
    cr+=r.estimated_churn_risk_usd;
    if (r.has_lifecycle_gap)                gap++;
    if (r.requires_lifecycle_intervention)  intv++;
  }
  const n = reps.length;
  return {
    total: n, risk_counts, pattern_counts, severity_counts, action_counts,
    avg_lifecycle_composite:            Math.round(comp/n*10)/10,
    lifecycle_gap_count:                gap,
    intervention_count:                 intv,
    avg_adoption_score:                 Math.round(ad/n*10)/10,
    avg_engagement_score:               Math.round(en/n*10)/10,
    avg_renewal_readiness_score:        Math.round(rr/n*10)/10,
    avg_expansion_potential_score:      Math.round(ep/n*10)/10,
    total_estimated_churn_risk_usd:     Math.round(cr*100)/100,
  };
}
