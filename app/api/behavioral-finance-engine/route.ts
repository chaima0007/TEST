import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ── Helpers ───────────────────────────────────────────────────────────────────

function cognitiveScore(herd: number, overconf: number, anchoring: number) {
  return Math.round((herd * 0.4 + overconf * 0.35 + anchoring * 0.25) * 10000) / 100;
}
function emotionalScore(lossAv: number, panic: number, fomo: number) {
  return Math.round((lossAv * 0.4 + panic * 0.35 + fomo * 0.25) * 10000) / 100;
}
function narrativeScore(narrative: number, collDelusion: number, specBubble: number) {
  return Math.round((narrative * 0.4 + collDelusion * 0.35 + specBubble * 0.25) * 10000) / 100;
}
function systemicScore(cogDis: number, mentalAcc: number, wealthId: number) {
  return Math.round((cogDis * 0.4 + mentalAcc * 0.35 + wealthId * 0.25) * 10000) / 100;
}
function compositeScore(cog: number, emo: number, nar: number, sys: number) {
  return Math.round((cog * 0.30 + emo * 0.25 + nar * 0.25 + sys * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function behavioralPattern(p: {
  herd: number; panic: number; specBubble: number; collDelusion: number;
  narrative: number; cogDis: number; fomo: number; overconf: number;
  lossAv: number; sunkCost: number;
}): string {
  if (p.herd >= 0.70 && p.panic >= 0.65) return "mass_hysteria_crash";
  if (p.specBubble >= 0.70 && p.collDelusion >= 0.65) return "speculative_mania";
  if (p.narrative >= 0.70 && p.cogDis >= 0.65) return "narrative_collapse";
  if (p.fomo >= 0.70 && p.overconf >= 0.65) return "FOMO_spiral";
  if (p.lossAv >= 0.70 && p.sunkCost >= 0.65) return "cognitive_trap_cascade";
  return "none";
}
function severity(risk: string): string {
  const m: Record<string, string> = {
    critical: "krach_comportemental_systemique",
    high:     "instabilite_comportementale_majeure",
    moderate: "biais_structurels_actifs",
    low:      "comportement_rationnel_relatif",
  };
  return m[risk] ?? risk;
}
function recommendedAction(risk: string): string {
  const m: Record<string, string> = {
    critical: "circuit_breaker_comportemental_urgent",
    high:     "debiaisage_systemique_active",
    moderate: "surveillance_comportementale_renforcee",
    low:      "monitoring_biais_continu",
  };
  return m[risk] ?? risk;
}
function signal(risk: string): string {
  const m: Record<string, string> = {
    critical: "🔴 Krach comportemental imminent — biais systémiques critiques",
    high:     "🟠 Instabilité comportementale majeure détectée",
    moderate: "🟡 Biais actifs — surveillance requise",
    low:      "🟢 Comportement financier relativement rationnel",
  };
  return m[risk] ?? risk;
}

// ── Entity definitions (pre-computed) ────────────────────────────────────────

const mockEntities = (() => {
  // BFE-001: critical + mass_hysteria_crash (herd=0.85>=0.70, panic=0.75>=0.65)
  const e1 = (() => {
    const cog = cognitiveScore(0.85, 0.80, 0.75);
    const emo = emotionalScore(0.80, 0.75, 0.78);
    const nar = narrativeScore(0.78, 0.75, 0.78);
    const sys = systemicScore(0.78, 0.72, 0.72);
    const comp = compositeScore(cog, emo, nar, sys);
    const risk = riskLevel(comp);
    const pattern = behavioralPattern({ herd:0.85, panic:0.75, specBubble:0.78, collDelusion:0.75, narrative:0.78, cogDis:0.78, fomo:0.78, overconf:0.80, lossAv:0.80, sunkCost:0.68 });
    return { entity_id:"BFE-001", market_segment:"retail", region:"EMEA", cognitive_score:cog, emotional_score:emo, narrative_score:nar, systemic_score:sys, composite_score:comp, risk_level:risk, behavioral_pattern:pattern, severity:severity(risk), recommended_action:recommendedAction(risk), signal:signal(risk), speculative_bubble_formation_risk:0.78, collective_delusion_index:0.75 };
  })();

  // BFE-002: low risk, no pattern
  const e2 = (() => {
    const cog = cognitiveScore(0.12, 0.15, 0.12);
    const emo = emotionalScore(0.10, 0.10, 0.08);
    const nar = narrativeScore(0.10, 0.08, 0.10);
    const sys = systemicScore(0.12, 0.10, 0.08);
    const comp = compositeScore(cog, emo, nar, sys);
    const risk = riskLevel(comp);
    const pattern = behavioralPattern({ herd:0.12, panic:0.10, specBubble:0.10, collDelusion:0.08, narrative:0.10, cogDis:0.12, fomo:0.08, overconf:0.15, lossAv:0.10, sunkCost:0.10 });
    return { entity_id:"BFE-002", market_segment:"institutional", region:"NAMER", cognitive_score:cog, emotional_score:emo, narrative_score:nar, systemic_score:sys, composite_score:comp, risk_level:risk, behavioral_pattern:pattern, severity:severity(risk), recommended_action:recommendedAction(risk), signal:signal(risk), speculative_bubble_formation_risk:0.10, collective_delusion_index:0.08 };
  })();

  // BFE-003: high risk + speculative_mania (spec_bubble=0.75>=0.70, coll_del=0.70>=0.65)
  const e3 = (() => {
    const cog = cognitiveScore(0.58, 0.60, 0.50);
    const emo = emotionalScore(0.52, 0.50, 0.60);
    const nar = narrativeScore(0.65, 0.70, 0.75);
    const sys = systemicScore(0.55, 0.52, 0.52);
    const comp = compositeScore(cog, emo, nar, sys);
    const risk = riskLevel(comp);
    const pattern = behavioralPattern({ herd:0.58, panic:0.50, specBubble:0.75, collDelusion:0.70, narrative:0.65, cogDis:0.55, fomo:0.60, overconf:0.60, lossAv:0.52, sunkCost:0.50 });
    return { entity_id:"BFE-003", market_segment:"retail", region:"APAC", cognitive_score:cog, emotional_score:emo, narrative_score:nar, systemic_score:sys, composite_score:comp, risk_level:risk, behavioral_pattern:pattern, severity:severity(risk), recommended_action:recommendedAction(risk), signal:signal(risk), speculative_bubble_formation_risk:0.75, collective_delusion_index:0.70 };
  })();

  // BFE-004: low risk, no pattern
  const e4 = (() => {
    const cog = cognitiveScore(0.18, 0.20, 0.18);
    const emo = emotionalScore(0.15, 0.14, 0.12);
    const nar = narrativeScore(0.15, 0.12, 0.15);
    const sys = systemicScore(0.16, 0.14, 0.14);
    const comp = compositeScore(cog, emo, nar, sys);
    const risk = riskLevel(comp);
    const pattern = behavioralPattern({ herd:0.18, panic:0.14, specBubble:0.15, collDelusion:0.12, narrative:0.15, cogDis:0.16, fomo:0.12, overconf:0.20, lossAv:0.15, sunkCost:0.15 });
    return { entity_id:"BFE-004", market_segment:"b2b", region:"MEA", cognitive_score:cog, emotional_score:emo, narrative_score:nar, systemic_score:sys, composite_score:comp, risk_level:risk, behavioral_pattern:pattern, severity:severity(risk), recommended_action:recommendedAction(risk), signal:signal(risk), speculative_bubble_formation_risk:0.15, collective_delusion_index:0.12 };
  })();

  // BFE-005: critical + FOMO_spiral (fomo=0.85>=0.70, overconf=0.80>=0.65)
  // spec_bubble<0.70, coll_del<0.65, narrative_s<0.70 to avoid earlier patterns
  const e5 = (() => {
    const cog = cognitiveScore(0.60, 0.80, 0.68);
    const emo = emotionalScore(0.75, 0.58, 0.85);
    const nar = narrativeScore(0.65, 0.60, 0.65);
    const sys = systemicScore(0.68, 0.65, 0.70);
    const comp = compositeScore(cog, emo, nar, sys);
    const risk = riskLevel(comp);
    const pattern = behavioralPattern({ herd:0.60, panic:0.58, specBubble:0.65, collDelusion:0.60, narrative:0.65, cogDis:0.68, fomo:0.85, overconf:0.80, lossAv:0.75, sunkCost:0.55 });
    return { entity_id:"BFE-005", market_segment:"b2c", region:"LATAM", cognitive_score:cog, emotional_score:emo, narrative_score:nar, systemic_score:sys, composite_score:comp, risk_level:risk, behavioral_pattern:pattern, severity:severity(risk), recommended_action:recommendedAction(risk), signal:signal(risk), speculative_bubble_formation_risk:0.65, collective_delusion_index:0.60 };
  })();

  // BFE-006: moderate risk, no pattern
  const e6 = (() => {
    const cog = cognitiveScore(0.28, 0.30, 0.28);
    const emo = emotionalScore(0.26, 0.26, 0.24);
    const nar = narrativeScore(0.26, 0.24, 0.26);
    const sys = systemicScore(0.28, 0.26, 0.26);
    const comp = compositeScore(cog, emo, nar, sys);
    const risk = riskLevel(comp);
    const pattern = behavioralPattern({ herd:0.28, panic:0.26, specBubble:0.26, collDelusion:0.24, narrative:0.26, cogDis:0.28, fomo:0.24, overconf:0.30, lossAv:0.26, sunkCost:0.25 });
    return { entity_id:"BFE-006", market_segment:"partner", region:"EMEA", cognitive_score:cog, emotional_score:emo, narrative_score:nar, systemic_score:sys, composite_score:comp, risk_level:risk, behavioral_pattern:pattern, severity:severity(risk), recommended_action:recommendedAction(risk), signal:signal(risk), speculative_bubble_formation_risk:0.26, collective_delusion_index:0.24 };
  })();

  // BFE-007: high risk + narrative_collapse (narrative=0.78>=0.70, cog_dis=0.72>=0.65)
  // herd<0.70, spec_bubble<0.70, coll_del<0.65 to avoid earlier patterns
  const e7 = (() => {
    const cog = cognitiveScore(0.52, 0.55, 0.50);
    const emo = emotionalScore(0.55, 0.52, 0.55);
    const nar = narrativeScore(0.78, 0.52, 0.55);
    const sys = systemicScore(0.72, 0.60, 0.55);
    const comp = compositeScore(cog, emo, nar, sys);
    const risk = riskLevel(comp);
    const pattern = behavioralPattern({ herd:0.52, panic:0.52, specBubble:0.55, collDelusion:0.52, narrative:0.78, cogDis:0.72, fomo:0.55, overconf:0.55, lossAv:0.55, sunkCost:0.52 });
    return { entity_id:"BFE-007", market_segment:"institutional", region:"APAC", cognitive_score:cog, emotional_score:emo, narrative_score:nar, systemic_score:sys, composite_score:comp, risk_level:risk, behavioral_pattern:pattern, severity:severity(risk), recommended_action:recommendedAction(risk), signal:signal(risk), speculative_bubble_formation_risk:0.55, collective_delusion_index:0.52 };
  })();

  // BFE-008: critical + cognitive_trap_cascade (loss_av=0.85>=0.70, sunk_cost=0.80>=0.65)
  // herd<0.70 OR panic<0.65, spec_bubble<0.70, narrative_s<0.70, fomo<0.70 to avoid earlier patterns
  const e8 = (() => {
    const cog = cognitiveScore(0.68, 0.72, 0.70);
    const emo = emotionalScore(0.85, 0.62, 0.68);
    const nar = narrativeScore(0.65, 0.65, 0.65);
    const sys = systemicScore(0.78, 0.75, 0.72);
    const comp = compositeScore(cog, emo, nar, sys);
    const risk = riskLevel(comp);
    const pattern = behavioralPattern({ herd:0.68, panic:0.62, specBubble:0.65, collDelusion:0.65, narrative:0.65, cogDis:0.78, fomo:0.68, overconf:0.72, lossAv:0.85, sunkCost:0.80 });
    return { entity_id:"BFE-008", market_segment:"retail", region:"NAMER", cognitive_score:cog, emotional_score:emo, narrative_score:nar, systemic_score:sys, composite_score:comp, risk_level:risk, behavioral_pattern:pattern, severity:severity(risk), recommended_action:recommendedAction(risk), signal:signal(risk), speculative_bubble_formation_risk:0.65, collective_delusion_index:0.65 };
  })();

  return [e1, e2, e3, e4, e5, e6, e7, e8];
})();

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (!process.env.SWARM_API_URL) {
    let entities = [...mockEntities];
    if (risk)    entities = entities.filter((e) => e.risk_level === risk);
    if (pattern) entities = entities.filter((e) => e.behavioral_pattern === pattern);

    const risk_distribution:     Record<string, number> = {};
    const pattern_distribution:  Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution:   Record<string, number> = {};
    let total_comp = 0;
    let total_cog  = 0;

    for (const e of mockEntities) {
      risk_distribution[e.risk_level]         = (risk_distribution[e.risk_level] || 0) + 1;
      pattern_distribution[e.behavioral_pattern] = (pattern_distribution[e.behavioral_pattern] || 0) + 1;
      severity_distribution[e.severity]       = (severity_distribution[e.severity] || 0) + 1;
      action_distribution[e.recommended_action] = (action_distribution[e.recommended_action] || 0) + 1;
      total_comp += e.composite_score;
      total_cog  += e.cognitive_score;
    }

    const n = mockEntities.length;
    const avg_composite = Math.round((total_comp / n) * 100) / 100;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id:                           332,
        module_name:                         "Behavioral Finance & Wealth Psychology Intelligence Engine",
        total_entities:                      n,
        critical_count:                      mockEntities.filter((e) => e.risk_level === "critical").length,
        high_count:                          mockEntities.filter((e) => e.risk_level === "high").length,
        moderate_count:                      mockEntities.filter((e) => e.risk_level === "moderate").length,
        low_count:                           mockEntities.filter((e) => e.risk_level === "low").length,
        avg_composite,
        pattern_distribution,
        risk_distribution,
        severity_distribution,
        action_distribution,
        avg_estimated_behavioral_risk_index: Math.round((avg_composite / 100 * 10) * 100) / 100,
        avg_cognitive_score:                 Math.round((total_cog / n) * 100) / 100,
      },
    } as Record<string, unknown>));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/behavioral-finance-engine`);
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(await res.json());
  } catch { /* fall through to 502 */ }

  return NextResponse.json(
    sealResponse({ entities: [], summary: {} } as Record<string, unknown>),
    { status: 502 },
  );
}
