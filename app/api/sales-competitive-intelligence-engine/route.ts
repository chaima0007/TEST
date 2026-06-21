import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse({ error: "SWARM_API_URL not configured" } as Record<string,unknown>), { status: 502 });
  }
  return NextResponse.json(sealResponse({ reps: MOCK_REPS, summary: buildSummary(MOCK_REPS) } as Record<string,unknown>));
}

const MOCK_REPS = [
  { rep_id:"R001", region:"EMEA",  comp_risk:"critical",  comp_pattern:"price_surrender",        comp_severity:"losing",      recommended_action:"competitive_strategy_reset",      win_rate_score:90, positioning_score:88, battle_readiness_score:85, relationship_advantage_score:82, comp_composite:87.8, has_comp_gap:true,  requires_comp_coaching:true,  estimated_pipeline_at_risk_usd:320000, comp_signal:"Price surrender — 20% competitive win rate — 35% avg discount in comp deals — 50% late-stage losses — composite 88" },
  { rep_id:"R002", region:"APAC",  comp_risk:"critical",  comp_pattern:"feature_gap_concession", comp_severity:"losing",      recommended_action:"competitive_strategy_reset",      win_rate_score:75, positioning_score:80, battle_readiness_score:70, relationship_advantage_score:65, comp_composite:74.5, has_comp_gap:true,  requires_comp_coaching:true,  estimated_pipeline_at_risk_usd:280000, comp_signal:"Feature-gap concession — 28% competitive win rate — 28% avg discount — composite 75" },
  { rep_id:"R003", region:"NOAM",  comp_risk:"high",      comp_pattern:"late_entry_loss",        comp_severity:"challenged",  recommended_action:"competitive_escalation",          win_rate_score:55, positioning_score:48, battle_readiness_score:52, relationship_advantage_score:44, comp_composite:51.6, has_comp_gap:true,  requires_comp_coaching:true,  estimated_pipeline_at_risk_usd:195000, comp_signal:"Late-entry loss — 38% competitive win rate — composite 52" },
  { rep_id:"R004", region:"LATAM", comp_risk:"high",      comp_pattern:"relationship_deficit",   comp_severity:"challenged",  recommended_action:"competitive_escalation",          win_rate_score:48, positioning_score:42, battle_readiness_score:45, relationship_advantage_score:58, comp_composite:47.2, has_comp_gap:true,  requires_comp_coaching:true,  estimated_pipeline_at_risk_usd:165000, comp_signal:"Relationship deficit — 42% competitive win rate — composite 47" },
  { rep_id:"R005", region:"EMEA",  comp_risk:"moderate",  comp_pattern:"multi_vendor_spread",    comp_severity:"competitive", recommended_action:"competitive_monitoring",          win_rate_score:30, positioning_score:25, battle_readiness_score:28, relationship_advantage_score:22, comp_composite:27.0, has_comp_gap:true,  requires_comp_coaching:true,  estimated_pipeline_at_risk_usd:88000,  comp_signal:"Multi-vendor spread — 52% competitive win rate — composite 27" },
  { rep_id:"R006", region:"APAC",  comp_risk:"low",       comp_pattern:"none",                   comp_severity:"dominant",    recommended_action:"no_action",                       win_rate_score:8,  positioning_score:6,  battle_readiness_score:5,  relationship_advantage_score:4,  comp_composite:6.3,  has_comp_gap:false, requires_comp_coaching:false, estimated_pipeline_at_risk_usd:0,      comp_signal:"Competitive position strong — win rate, positioning, battle readiness, and executive alignment within benchmarks" },
  { rep_id:"R007", region:"NOAM",  comp_risk:"high",      comp_pattern:"price_surrender",        comp_severity:"challenged",  recommended_action:"value_differentiation_coaching",  win_rate_score:62, positioning_score:58, battle_readiness_score:55, relationship_advantage_score:48, comp_composite:58.2, has_comp_gap:true,  requires_comp_coaching:true,  estimated_pipeline_at_risk_usd:210000, comp_signal:"Price surrender — 32% competitive win rate — 24% avg discount — composite 58" },
  { rep_id:"R008", region:"LATAM", comp_risk:"low",       comp_pattern:"none",                   comp_severity:"dominant",    recommended_action:"no_action",                       win_rate_score:5,  positioning_score:4,  battle_readiness_score:6,  relationship_advantage_score:3,  comp_composite:4.8,  has_comp_gap:false, requires_comp_coaching:false, estimated_pipeline_at_risk_usd:0,      comp_signal:"Competitive position strong — win rate, positioning, battle readiness, and executive alignment within benchmarks" },
];

function buildSummary(reps: typeof MOCK_REPS) {
  const risk_counts:     Record<string,number> = {};
  const pattern_counts:  Record<string,number> = {};
  const severity_counts: Record<string,number> = {};
  const action_counts:   Record<string,number> = {};
  let comp=0, wr=0, po=0, br=0, ra=0, pr=0, gap=0, coach=0;
  for (const r of reps) {
    risk_counts[r.comp_risk]         = (risk_counts[r.comp_risk]||0)+1;
    pattern_counts[r.comp_pattern]   = (pattern_counts[r.comp_pattern]||0)+1;
    severity_counts[r.comp_severity] = (severity_counts[r.comp_severity]||0)+1;
    action_counts[r.recommended_action] = (action_counts[r.recommended_action]||0)+1;
    comp+=r.comp_composite; wr+=r.win_rate_score; po+=r.positioning_score;
    br+=r.battle_readiness_score; ra+=r.relationship_advantage_score;
    pr+=r.estimated_pipeline_at_risk_usd;
    if (r.has_comp_gap)          gap++;
    if (r.requires_comp_coaching) coach++;
  }
  const n = reps.length;
  return {
    total: n, risk_counts, pattern_counts, severity_counts, action_counts,
    avg_comp_composite:                     Math.round(comp/n*10)/10,
    comp_gap_count:                         gap,
    coaching_count:                         coach,
    avg_win_rate_score:                     Math.round(wr/n*10)/10,
    avg_positioning_score:                  Math.round(po/n*10)/10,
    avg_battle_readiness_score:             Math.round(br/n*10)/10,
    avg_relationship_advantage_score:       Math.round(ra/n*10)/10,
    total_estimated_pipeline_at_risk_usd:   Math.round(pr*100)/100,
  };
}
