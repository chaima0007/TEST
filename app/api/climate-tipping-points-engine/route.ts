import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[climate-tipping-points-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

// ─── Math (mirrors Python exactly) ───────────────────────────────────────────

interface CtpInput {
  id: string;
  ecosystem_type: string;
  region: string;
  temperature_anomaly: number;
  ice_sheet_loss_rate: number;
  permafrost_thaw_index: number;
  ocean_acidification_level: number;
  methane_release_rate: number;
  coral_bleaching_intensity: number;
  arctic_sea_ice_decline: number;
  amazon_dieback_risk: number;
  jet_stream_disruption: number;
  monsoon_destabilization: number;
  sea_level_rise_velocity: number;
  biodiversity_collapse_rate: number;
  carbon_feedback_loop: number;
  tipping_cascade_risk: number;
  albedo_loss_factor: number;
  ecosystem_resilience: number;
  adaptation_capacity: number;
}

function thermalScore(e: CtpInput): number {
  return Math.round((e.temperature_anomaly * 0.4 + e.ice_sheet_loss_rate * 0.35 + e.permafrost_thaw_index * 0.25) * 100 * 100) / 100;
}

function ecosystemScore(e: CtpInput): number {
  return Math.round((e.coral_bleaching_intensity * 0.4 + e.amazon_dieback_risk * 0.35 + e.biodiversity_collapse_rate * 0.25) * 100 * 100) / 100;
}

function feedbackScore(e: CtpInput): number {
  return Math.round((e.carbon_feedback_loop * 0.4 + e.methane_release_rate * 0.35 + e.albedo_loss_factor * 0.25) * 100 * 100) / 100;
}

function vulnerabilityScore(e: CtpInput): number {
  return Math.round((e.tipping_cascade_risk * 0.4 + (1 - e.ecosystem_resilience) * 0.35 + (1 - e.adaptation_capacity) * 0.25) * 100 * 100) / 100;
}

function composite(t: number, ec: number, fb: number, vul: number): number {
  return Math.round((t * 0.30 + ec * 0.25 + fb * 0.25 + vul * 0.20) * 100) / 100;
}

function tippingPattern(e: CtpInput): string {
  if (e.temperature_anomaly >= 0.70 && e.carbon_feedback_loop >= 0.65) return "thermal_runaway";
  if (e.permafrost_thaw_index >= 0.70 && e.methane_release_rate >= 0.65) return "permafrost_collapse";
  if (e.ocean_acidification_level >= 0.70 && e.coral_bleaching_intensity >= 0.65) return "ocean_system_failure";
  if (e.amazon_dieback_risk >= 0.70 && e.biodiversity_collapse_rate >= 0.60) return "biosphere_cascade";
  if (e.arctic_sea_ice_decline >= 0.70 && e.albedo_loss_factor >= 0.65) return "arctic_tipping";
  return "none";
}

function tippingRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function tippingSeverity(comp: number): string {
  if (comp >= 75) return "planetary_emergency";
  if (comp >= 50) return "critical_tipping";
  if (comp >= 25) return "tipping_developing";
  return "ecosystem_stable";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "planetary_emergency_protocol";
  if (risk === "high" && pattern === "thermal_runaway") return "carbon_emergency_brake";
  if (risk === "high") return "ecosystem_crisis_response";
  if (risk === "moderate") return "tipping_monitoring";
  return "no_action";
}

function tippingSignal(e: CtpInput, risk: string, comp: number): string {
  if (risk === "critical") {
    return `Critique — anomalie thermique ${Math.round(e.temperature_anomaly * 100)}% — risque cascade basculement ${Math.round(e.tipping_cascade_risk * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "high") {
    return `Élevé — dégradation pergélisol ${Math.round(e.permafrost_thaw_index * 100)}% — résilience écosystème ${Math.round(e.ecosystem_resilience * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "moderate") {
    return `Modéré — acidification océan ${Math.round(e.ocean_acidification_level * 100)}% — composite ${Math.round(comp)}`;
  }
  return "Écosystème stable — résilience climatique solide, capacité d'adaptation optimale, aucun point de basculement imminent";
}

function analyzeEntity(e: CtpInput) {
  const t   = thermalScore(e);
  const ec  = ecosystemScore(e);
  const fb  = feedbackScore(e);
  const vul = vulnerabilityScore(e);
  const comp = composite(t, ec, fb, vul);
  const pat  = tippingPattern(e);
  const risk = tippingRisk(comp);
  const sev  = tippingSeverity(comp);
  const action = recommendedAction(risk, pat);
  const signal = tippingSignal(e, risk, comp);

  return {
    id: e.entity_id,
    region: e.region,
    ecosystem_type: e.ecosystem_type,
    tipping_risk: risk,
    tipping_pattern: pat,
    tipping_severity: sev,
    recommended_action: action,
    thermal_score: t,
    ecosystem_score: ec,
    feedback_score: fb,
    vulnerability_score: vul,
    tipping_composite: comp,
    is_tipping_crisis: comp >= 60,
    requires_tipping_intervention: comp >= 40,
    tipping_signal: signal,
  };
}

// ─── Mock entities ────────────────────────────────────────────────────────────

const mockEntities: CtpInput[] = [
  {
    id: "CTP-001", region: "EMEA", ecosystem_type: "arctic_ecosystem",
    temperature_anomaly: 0.88, ice_sheet_loss_rate: 0.82, permafrost_thaw_index: 0.75,
    ocean_acidification_level: 0.60, methane_release_rate: 0.72,
    coral_bleaching_intensity: 0.70, arctic_sea_ice_decline: 0.68,
    amazon_dieback_risk: 0.65, jet_stream_disruption: 0.62,
    monsoon_destabilization: 0.58, sea_level_rise_velocity: 0.65,
    biodiversity_collapse_rate: 0.68, carbon_feedback_loop: 0.80,
    tipping_cascade_risk: 0.78, albedo_loss_factor: 0.70,
    ecosystem_resilience: 0.18, adaptation_capacity: 0.20,
  },
  {
    id: "CTP-002", region: "APAC", ecosystem_type: "temperate_forest",
    temperature_anomaly: 0.12, ice_sheet_loss_rate: 0.10, permafrost_thaw_index: 0.11,
    ocean_acidification_level: 0.10, methane_release_rate: 0.11,
    coral_bleaching_intensity: 0.10, arctic_sea_ice_decline: 0.10,
    amazon_dieback_risk: 0.11, jet_stream_disruption: 0.10,
    monsoon_destabilization: 0.10, sea_level_rise_velocity: 0.10,
    biodiversity_collapse_rate: 0.10, carbon_feedback_loop: 0.12,
    tipping_cascade_risk: 0.12, albedo_loss_factor: 0.10,
    ecosystem_resilience: 0.92, adaptation_capacity: 0.88,
  },
  {
    id: "CTP-003", region: "NOAM", ecosystem_type: "boreal_forest",
    temperature_anomaly: 0.48, ice_sheet_loss_rate: 0.45, permafrost_thaw_index: 0.78,
    ocean_acidification_level: 0.30, methane_release_rate: 0.72,
    coral_bleaching_intensity: 0.35, arctic_sea_ice_decline: 0.38,
    amazon_dieback_risk: 0.30, jet_stream_disruption: 0.35,
    monsoon_destabilization: 0.28, sea_level_rise_velocity: 0.32,
    biodiversity_collapse_rate: 0.38, carbon_feedback_loop: 0.50,
    tipping_cascade_risk: 0.55, albedo_loss_factor: 0.42,
    ecosystem_resilience: 0.38, adaptation_capacity: 0.40,
  },
  {
    id: "CTP-004", region: "LATAM", ecosystem_type: "ocean_ecosystem",
    temperature_anomaly: 0.12, ice_sheet_loss_rate: 0.10, permafrost_thaw_index: 0.10,
    ocean_acidification_level: 0.11, methane_release_rate: 0.10,
    coral_bleaching_intensity: 0.11, arctic_sea_ice_decline: 0.10,
    amazon_dieback_risk: 0.10, jet_stream_disruption: 0.10,
    monsoon_destabilization: 0.10, sea_level_rise_velocity: 0.12,
    biodiversity_collapse_rate: 0.12, carbon_feedback_loop: 0.13,
    tipping_cascade_risk: 0.12, albedo_loss_factor: 0.11,
    ecosystem_resilience: 0.90, adaptation_capacity: 0.88,
  },
  {
    id: "CTP-005", region: "MEA", ecosystem_type: "tropical_rainforest",
    temperature_anomaly: 0.70, ice_sheet_loss_rate: 0.65, permafrost_thaw_index: 0.60,
    ocean_acidification_level: 0.58, methane_release_rate: 0.65,
    coral_bleaching_intensity: 0.65, arctic_sea_ice_decline: 0.50,
    amazon_dieback_risk: 0.82, jet_stream_disruption: 0.45,
    monsoon_destabilization: 0.55, sea_level_rise_velocity: 0.60,
    biodiversity_collapse_rate: 0.75, carbon_feedback_loop: 0.68,
    tipping_cascade_risk: 0.72, albedo_loss_factor: 0.62,
    ecosystem_resilience: 0.22, adaptation_capacity: 0.25,
  },
  {
    id: "CTP-006", region: "EMEA", ecosystem_type: "coastal_ecosystem",
    temperature_anomaly: 0.28, ice_sheet_loss_rate: 0.25, permafrost_thaw_index: 0.22,
    ocean_acidification_level: 0.22, methane_release_rate: 0.22,
    coral_bleaching_intensity: 0.25, arctic_sea_ice_decline: 0.20,
    amazon_dieback_risk: 0.20, jet_stream_disruption: 0.18,
    monsoon_destabilization: 0.15, sea_level_rise_velocity: 0.25,
    biodiversity_collapse_rate: 0.28, carbon_feedback_loop: 0.25,
    tipping_cascade_risk: 0.30, albedo_loss_factor: 0.20,
    ecosystem_resilience: 0.65, adaptation_capacity: 0.62,
  },
  {
    id: "CTP-007", region: "APAC", ecosystem_type: "coral_reef",
    temperature_anomaly: 0.48, ice_sheet_loss_rate: 0.40, permafrost_thaw_index: 0.35,
    ocean_acidification_level: 0.78, methane_release_rate: 0.42,
    coral_bleaching_intensity: 0.72, arctic_sea_ice_decline: 0.35,
    amazon_dieback_risk: 0.45, jet_stream_disruption: 0.30,
    monsoon_destabilization: 0.32, sea_level_rise_velocity: 0.48,
    biodiversity_collapse_rate: 0.50, carbon_feedback_loop: 0.45,
    tipping_cascade_risk: 0.52, albedo_loss_factor: 0.38,
    ecosystem_resilience: 0.40, adaptation_capacity: 0.42,
  },
  {
    id: "CTP-008", region: "NOAM", ecosystem_type: "arctic_ecosystem",
    temperature_anomaly: 0.72, ice_sheet_loss_rate: 0.75, permafrost_thaw_index: 0.68,
    ocean_acidification_level: 0.55, methane_release_rate: 0.62,
    coral_bleaching_intensity: 0.62, arctic_sea_ice_decline: 0.82,
    amazon_dieback_risk: 0.58, jet_stream_disruption: 0.60,
    monsoon_destabilization: 0.52, sea_level_rise_velocity: 0.68,
    biodiversity_collapse_rate: 0.65, carbon_feedback_loop: 0.65,
    tipping_cascade_risk: 0.70, albedo_loss_factor: 0.75,
    ecosystem_resilience: 0.22, adaptation_capacity: 0.25,
  },
];

// ─── Route handler ────────────────────────────────────────────────────────────

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  if (!SWARM_API_URL) {
    const allResults = mockEntities.map(analyzeEntity);
    let entities = [...allResults];
    if (risk)    entities = entities.filter((e) => e.tipping_risk === risk);
    if (pattern) entities = entities.filter((e) => e.tipping_pattern === pattern);

    const risk_counts:     Record<string, number> = {};
    const pattern_counts:  Record<string, number> = {};
    const severity_counts: Record<string, number> = {};
    const action_counts:   Record<string, number> = {};
    let total_comp = 0, total_thermal = 0, total_eco = 0, total_fb = 0, total_vul = 0;

    for (const r of allResults) {
      risk_counts[r.tipping_risk]       = (risk_counts[r.tipping_risk] || 0) + 1;
      pattern_counts[r.tipping_pattern] = (pattern_counts[r.tipping_pattern] || 0) + 1;
      severity_counts[r.tipping_severity] = (severity_counts[r.tipping_severity] || 0) + 1;
      action_counts[r.recommended_action] = (action_counts[r.recommended_action] || 0) + 1;
      total_comp    += r.tipping_composite;
      total_thermal += r.thermal_score;
      total_eco     += r.ecosystem_score;
      total_fb      += r.feedback_score;
      total_vul     += r.vulnerability_score;
    }

    const n = allResults.length;
    const avg_comp = Math.round((total_comp / n) * 10) / 10;

    return sealResponse(NextResponse.json(sealResponse({
      entities,
      summary: {
        total: n,
        risk_counts,
        pattern_counts,
        severity_counts,
        action_counts,
        avg_tipping_composite:       avg_comp,
        tipping_crisis_count:        allResults.filter((r) => r.is_tipping_crisis).length,
        tipping_intervention_count:  allResults.filter((r) => r.requires_tipping_intervention).length,
        avg_thermal_score:           Math.round((total_thermal / n) * 10) / 10,
        avg_ecosystem_score:         Math.round((total_eco     / n) * 10) / 10,
        avg_feedback_score:          Math.round((total_fb      / n) * 10) / 10,
        avg_vulnerability_score:     Math.round((total_vul     / n) * 10) / 10,
        avg_estimated_tipping_index: Math.round((avg_comp / 100 * 10) * 100) / 100,
      },
    } as Record<string, unknown>)));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/climate-tipping-points-engine`);
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(await res.json()));
  } catch {}

  return sealResponse(NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 }));
}
