import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // CRE-001 — critical, mass_bleaching_extinction_event (bf>0.85, ta>0.80)
  {
    id: "CRE-001", reef_type: "barrière_corallienne", region: "APAC",
    bleaching_frequency: 0.92, temperature_anomaly: 0.88,
    ocean_acidification_ph: 0.72, coral_cover_loss: 0.82,
    biodiversity_decline: 0.78, nutrient_pollution: 0.68,
    sedimentation_rate: 0.65, destructive_fishing_intensity: 0.70,
    crown_of_thorns_outbreak: 0.68, sunscreen_chemical_impact: 0.55,
    mpa_effectiveness: 0.45, restoration_investment: 0.35,
    climate_trajectory: 0.85, tourism_damage: 0.65,
    coastal_development_pressure: 0.68, recovery_time_estimate: 0.80,
    genetic_diversity_reserve: 0.25,
  },
  // CRE-002 — critical, ocean_acidification_dissolution (oa_ph>0.85, ccl>0.80)
  {
    id: "CRE-002", reef_type: "récif_frangeant", region: "CARIB",
    bleaching_frequency: 0.72, temperature_anomaly: 0.70,
    ocean_acidification_ph: 0.90, coral_cover_loss: 0.88,
    biodiversity_decline: 0.75, nutrient_pollution: 0.70,
    sedimentation_rate: 0.68, destructive_fishing_intensity: 0.65,
    crown_of_thorns_outbreak: 0.60, sunscreen_chemical_impact: 0.62,
    mpa_effectiveness: 0.50, restoration_investment: 0.40,
    climate_trajectory: 0.80, tourism_damage: 0.68,
    coastal_development_pressure: 0.72, recovery_time_estimate: 0.78,
    genetic_diversity_reserve: 0.28,
  },
  // CRE-003 — critical, nutrient_runoff_algae_takeover (np>0.85, sr>0.80)
  {
    id: "CRE-003", reef_type: "récif_patch", region: "EMEA",
    bleaching_frequency: 0.68, temperature_anomaly: 0.65,
    ocean_acidification_ph: 0.70, coral_cover_loss: 0.75,
    biodiversity_decline: 0.70, nutrient_pollution: 0.88,
    sedimentation_rate: 0.85, destructive_fishing_intensity: 0.65,
    crown_of_thorns_outbreak: 0.62, sunscreen_chemical_impact: 0.58,
    mpa_effectiveness: 0.45, restoration_investment: 0.38,
    climate_trajectory: 0.75, tourism_damage: 0.60,
    coastal_development_pressure: 0.65, recovery_time_estimate: 0.72,
    genetic_diversity_reserve: 0.30,
  },
  // CRE-004 — high, destructive_fishing_collapse (dfi>0.80, bd>0.75)
  {
    id: "CRE-004", reef_type: "récif_atoll", region: "PACIF",
    bleaching_frequency: 0.50, temperature_anomaly: 0.48,
    ocean_acidification_ph: 0.52, coral_cover_loss: 0.50,
    biodiversity_decline: 0.80, nutrient_pollution: 0.48,
    sedimentation_rate: 0.45, destructive_fishing_intensity: 0.85,
    crown_of_thorns_outbreak: 0.50, sunscreen_chemical_impact: 0.45,
    mpa_effectiveness: 0.48, restoration_investment: 0.42,
    climate_trajectory: 0.52, tourism_damage: 0.48,
    coastal_development_pressure: 0.50, recovery_time_estimate: 0.55,
    genetic_diversity_reserve: 0.40,
  },
  // CRE-005 — high, marine_protected_area_failure (mpa>0.80, ri>0.75)
  {
    id: "CRE-005", reef_type: "récif_profond", region: "LATAM",
    bleaching_frequency: 0.48, temperature_anomaly: 0.50,
    ocean_acidification_ph: 0.48, coral_cover_loss: 0.50,
    biodiversity_decline: 0.48, nutrient_pollution: 0.50,
    sedimentation_rate: 0.48, destructive_fishing_intensity: 0.52,
    crown_of_thorns_outbreak: 0.48, sunscreen_chemical_impact: 0.45,
    mpa_effectiveness: 0.85, restoration_investment: 0.80,
    climate_trajectory: 0.52, tourism_damage: 0.50,
    coastal_development_pressure: 0.48, recovery_time_estimate: 0.55,
    genetic_diversity_reserve: 0.38,
  },
  // CRE-006 — moderate, none
  {
    id: "CRE-006", reef_type: "récif_mesophotique", region: "NOAM",
    bleaching_frequency: 0.30, temperature_anomaly: 0.28,
    ocean_acidification_ph: 0.32, coral_cover_loss: 0.30,
    biodiversity_decline: 0.28, nutrient_pollution: 0.32,
    sedimentation_rate: 0.28, destructive_fishing_intensity: 0.30,
    crown_of_thorns_outbreak: 0.28, sunscreen_chemical_impact: 0.25,
    mpa_effectiveness: 0.30, restoration_investment: 0.28,
    climate_trajectory: 0.30, tourism_damage: 0.28,
    coastal_development_pressure: 0.30, recovery_time_estimate: 0.32,
    genetic_diversity_reserve: 0.60,
  },
  // CRE-007 — low, none
  {
    id: "CRE-007", reef_type: "récif_côtier", region: "APAC",
    bleaching_frequency: 0.10, temperature_anomaly: 0.12,
    ocean_acidification_ph: 0.10, coral_cover_loss: 0.12,
    biodiversity_decline: 0.10, nutrient_pollution: 0.12,
    sedimentation_rate: 0.10, destructive_fishing_intensity: 0.10,
    crown_of_thorns_outbreak: 0.12, sunscreen_chemical_impact: 0.08,
    mpa_effectiveness: 0.10, restoration_investment: 0.12,
    climate_trajectory: 0.10, tourism_damage: 0.10,
    coastal_development_pressure: 0.12, recovery_time_estimate: 0.10,
    genetic_diversity_reserve: 0.85,
  },
  // CRE-008 — low, none
  {
    id: "CRE-008", reef_type: "récif_corallien_isolé", region: "EMEA",
    bleaching_frequency: 0.12, temperature_anomaly: 0.10,
    ocean_acidification_ph: 0.12, coral_cover_loss: 0.10,
    biodiversity_decline: 0.12, nutrient_pollution: 0.10,
    sedimentation_rate: 0.12, destructive_fishing_intensity: 0.10,
    crown_of_thorns_outbreak: 0.10, sunscreen_chemical_impact: 0.10,
    mpa_effectiveness: 0.12, restoration_investment: 0.10,
    climate_trajectory: 0.12, tourism_damage: 0.10,
    coastal_development_pressure: 0.10, recovery_time_estimate: 0.12,
    genetic_diversity_reserve: 0.88,
  },
];

type CREInput = typeof MOCK_ENTITIES[0];

function bleachingScore(e: CREInput): number {
  return Math.round((e.bleaching_frequency * 0.4 + e.temperature_anomaly * 0.35 + e.ocean_acidification_ph * 0.25) * 100 * 100) / 100;
}
function pollutionScore(e: CREInput): number {
  return Math.round((e.nutrient_pollution * 0.4 + e.sedimentation_rate * 0.35 + e.sunscreen_chemical_impact * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: CREInput): number {
  return Math.round((e.destructive_fishing_intensity * 0.4 + e.tourism_damage * 0.35 + e.coastal_development_pressure * 0.25) * 100 * 100) / 100;
}
function recoveryScore(e: CREInput): number {
  return Math.round((e.coral_cover_loss * 0.4 + e.biodiversity_decline * 0.35 + e.crown_of_thorns_outbreak * 0.25) * 100 * 100) / 100;
}
function compositeScore(bl: number, po: number, go: number, re: number): number {
  return Math.round((bl * 0.30 + po * 0.25 + go * 0.25 + re * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function reefPattern(e: CREInput): string {
  if (e.bleaching_frequency > 0.85 && e.temperature_anomaly > 0.80) return "mass_bleaching_extinction_event";
  if (e.ocean_acidification_ph > 0.85 && e.coral_cover_loss > 0.80) return "ocean_acidification_dissolution";
  if (e.nutrient_pollution > 0.85 && e.sedimentation_rate > 0.80) return "nutrient_runoff_algae_takeover";
  if (e.destructive_fishing_intensity > 0.80 && e.biodiversity_decline > 0.75) return "destructive_fishing_collapse";
  if (e.mpa_effectiveness > 0.80 && e.restoration_investment > 0.75) return "marine_protected_area_failure";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "effondrement_récifal_systémique_critique";
  if (composite >= 40) return "dégradation_corallienne_majeure";
  if (composite >= 20) return "stress_écosystème_marin_modéré";
  return "récif_sous_surveillance_active";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_récif_effondrement_critique";
  if (risk === "high") return "restauration_corallienne_accélérée_zones_dégradées";
  if (risk === "moderate") return "renforcement_protection_marine_surveillance_continue";
  return "veille_santé_récifale_préventive";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Effondrement récifal systémique — extinction massive imminente";
  if (risk === "high") return "🟠 Dégradation corallienne majeure détectée";
  if (risk === "moderate") return "🟡 Stress écosystème marin modéré actif";
  return "🟢 Récif sous surveillance active";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const bl   = bleachingScore(e);
      const po   = pollutionScore(e);
      const go   = governanceScore(e);
      const re   = recoveryScore(e);
      const comp = compositeScore(bl, po, go, re);
      const risk = riskLevel(comp);
      const pat  = reefPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:            e.entity_id,
        reef_type:            e.reef_type,
        region:               e.region,
        bleaching_score:      bl,
        pollution_score:      po,
        governance_score:     go,
        recovery_score:       re,
        composite_score:      comp,
        risk_level:           risk,
        reef_pattern:         pat,
        severity:             sev,
        recommended_action:   action,
        signal:               sig,
        bleaching_frequency:  e.bleaching_frequency,
        coral_cover_loss:     e.coral_cover_loss,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tBl = 0, tPo = 0, tGo = 0, tRe = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.reef_pattern]      = (pattern_distribution[ent.reef_pattern]      || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tBl   += ent.bleaching_score;
      tPo   += ent.pollution_score;
      tGo   += ent.governance_score;
      tRe   += ent.recovery_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")      criticalCount++;
      else if (ent.risk_level === "high")     highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else                                    lowCount++;
    }

    const n = entities.length;
    const avgComposite  = Math.round(tComp / n * 10) / 10;
    const avgBleaching  = Math.round(tBl   / n * 10) / 10;

    const summary = {
      module_id:                          424,
      module_name:                        "Effondrement Récifs Coralliens & Écosystèmes Marins Intelligence Engine",
      total:                              n,
      critical:                           criticalCount,
      high:                               highCount,
      moderate:                           moderateCount,
      low:                                lowCount,
      avg_composite:                      avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_coral_health_index:   Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(
      sealResponse({ entities, summary, avg_bleaching: avgBleaching }, "coral-reef-engine")
    );
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/api/coral-reef-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "coral-reef-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "coral-reef-engine"),
      { status: 502 }
    );
  }
}
