import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockCultures = [
  {
    microculture_id: "MC-001", cultural_cluster: "founding", region: "EMEA",
    cultural_risk: "low", cultural_pattern: "none",
    cultural_severity: "cohesive", recommended_action: "no_action",
    cohesion_score: 0, narrative_score: 0, ritual_score: 0, resilience_score: 0,
    cultural_composite: 0.0, has_fragmentation_alert: false, requires_intervention: false,
    estimated_culture_dissolution_index: 0.0,
    cultural_signal: "Micro-culture cohésive — narrations partagées, rituels vivants, générations alignées, identité forte",
  },
  {
    microculture_id: "MC-002", cultural_cluster: "legacy", region: "NAMER",
    cultural_risk: "critical", cultural_pattern: "tribal_fragmentation",
    cultural_severity: "dissolved", recommended_action: "emergency_culture_intervention",
    cohesion_score: 65, narrative_score: 65, ritual_score: 65, resilience_score: 100,
    cultural_composite: 72.0, has_fragmentation_alert: true, requires_intervention: true,
    estimated_culture_dissolution_index: 5.69,
    cultural_signal: "Fragmentation tribale — cohésion 38% — dérive valeurs 62% — tribalisme 68% — composite 72",
  },
  {
    microculture_id: "MC-003", cultural_cluster: "growth", region: "APAC",
    cultural_risk: "moderate", cultural_pattern: "none",
    cultural_severity: "drifting", recommended_action: "culture_pulse_monitoring",
    cohesion_score: 28, narrative_score: 40, ritual_score: 40, resilience_score: 14,
    cultural_composite: 31.2, has_fragmentation_alert: false, requires_intervention: true,
    estimated_culture_dissolution_index: 1.44,
    cultural_signal: "None — cohésion 55% — dérive valeurs 38% — tribalisme 42% — composite 31",
  },
  {
    microculture_id: "MC-004", cultural_cluster: "acquired", region: "LATAM",
    cultural_risk: "critical", cultural_pattern: "tribal_fragmentation",
    cultural_severity: "dissolved", recommended_action: "emergency_culture_intervention",
    cohesion_score: 100, narrative_score: 100, ritual_score: 82, resilience_score: 100,
    cultural_composite: 95.5, has_fragmentation_alert: true, requires_intervention: true,
    estimated_culture_dissolution_index: 8.21,
    cultural_signal: "Fragmentation tribale — cohésion 25% — dérive valeurs 80% — tribalisme 75% — composite 96",
  },
  {
    microculture_id: "MC-005", cultural_cluster: "remote", region: "MEA",
    cultural_risk: "high", cultural_pattern: "ritual_erosion",
    cultural_severity: "fragmented", recommended_action: "ritual_revival",
    cohesion_score: 52, narrative_score: 52, ritual_score: 52, resilience_score: 52,
    cultural_composite: 52.0, has_fragmentation_alert: true, requires_intervention: true,
    estimated_culture_dissolution_index: 3.17,
    cultural_signal: "Érosion rituelle — cohésion 45% — dérive valeurs 55% — tribalisme 50% — composite 52",
  },
  {
    microculture_id: "MC-006", cultural_cluster: "hybrid", region: "EMEA",
    cultural_risk: "low", cultural_pattern: "none",
    cultural_severity: "cohesive", recommended_action: "no_action",
    cohesion_score: 8, narrative_score: 14, ritual_score: 14, resilience_score: 8,
    cultural_composite: 11.0, has_fragmentation_alert: false, requires_intervention: false,
    estimated_culture_dissolution_index: 0.34,
    cultural_signal: "Micro-culture cohésive — narrations partagées, rituels vivants, générations alignées, identité forte",
  },
  {
    microculture_id: "MC-007", cultural_cluster: "generational_z", region: "NAMER",
    cultural_risk: "high", cultural_pattern: "generational_clash",
    cultural_severity: "fragmented", recommended_action: "generational_bridge_program",
    cohesion_score: 40, narrative_score: 52, ritual_score: 52, resilience_score: 52,
    cultural_composite: 48.4, has_fragmentation_alert: true, requires_intervention: true,
    estimated_culture_dissolution_index: 2.57,
    cultural_signal: "Choc générationnel — cohésion 48% — dérive valeurs 48% — tribalisme 45% — composite 48",
  },
  {
    microculture_id: "MC-008", cultural_cluster: "generational_x", region: "APAC",
    cultural_risk: "low", cultural_pattern: "none",
    cultural_severity: "cohesive", recommended_action: "no_action",
    cohesion_score: 0, narrative_score: 8, ritual_score: 6, resilience_score: 0,
    cultural_composite: 3.5, has_fragmentation_alert: false, requires_intervention: false,
    estimated_culture_dissolution_index: 0.08,
    cultural_signal: "Micro-culture cohésive — narrations partagées, rituels vivants, générations alignées, identité forte",
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (!process.env.SWARM_API_URL) {
  console.warn("[cultural-chronology-microculture-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    const pattern_counts:  Record<string, number> = {};
    const severity_counts: Record<string, number> = {};
    const action_counts:   Record<string, number> = {};
    let total_comp = 0, total_coh = 0, total_nar = 0, total_rit = 0,
        total_res = 0, total_diss = 0;

    for (const c of mockCultures) {
      risk_counts[c.cultural_risk]         = (risk_counts[c.cultural_risk] || 0) + 1;
      pattern_counts[c.cultural_pattern]   = (pattern_counts[c.cultural_pattern] || 0) + 1;
      severity_counts[c.cultural_severity] = (severity_counts[c.cultural_severity] || 0) + 1;
      action_counts[c.recommended_action]  = (action_counts[c.recommended_action] || 0) + 1;
      total_comp += c.cultural_composite;
      total_coh  += c.cohesion_score;
      total_nar  += c.narrative_score;
      total_rit  += c.ritual_score;
      total_res  += c.resilience_score;
      total_diss += c.estimated_culture_dissolution_index;
    }

    const n = mockCultures.length;

    return sealResponse(NextResponse.json(sealResponse({
      cultures,
      summary: {
        total:                                    n,
        risk_counts,
        pattern_counts,
        severity_counts,
        action_counts,
        avg_cultural_composite:                   Math.round((total_comp / n) * 10) / 10,
        fragmentation_alert_count:                mockCultures.filter((c) => c.has_fragmentation_alert).length,
        intervention_count:                       mockCultures.filter((c) => c.requires_intervention).length,
        avg_cohesion_score:                       Math.round((total_coh  / n) * 10) / 10,
        avg_narrative_score:                      Math.round((total_nar  / n) * 10) / 10,
        avg_ritual_score:                         Math.round((total_rit  / n) * 10) / 10,
        avg_resilience_score:                     Math.round((total_res  / n) * 10) / 10,
        avg_estimated_culture_dissolution_index:  Math.round((total_diss / n) * 100) / 100,
      },
    } as Record<string,unknown>)));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/cultural-chronology-microculture-engine`);
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(await res.json()));
  } catch {}

  return sealResponse(NextResponse.json(sealResponse({ cultures: [], summary: {} } as Record<string,unknown>)));
}
