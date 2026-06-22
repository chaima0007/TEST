import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[space-weather-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  // SWE-001 — critical, carrington_level_event_risk (solar_exp>0.85, transformer_vuln>0.80)
  {
    id: "SWE-001", infrastructure_type: "power_grid", region: "NOAM",
    solar_activity_exposure: 0.92, grid_hardening_level: 0.10, transformer_vulnerability: 0.88,
    satellite_shielding: 0.50, gps_dependency: 0.80, communication_backup: 0.15,
    financial_system_exposure: 0.75, emergency_power_reserve: 0.12, early_warning_capability: 0.12,
    geomagnetic_latitude_risk: 0.88, critical_system_redundancy: 0.12, international_coordination: 0.15,
    public_awareness: 0.20, recovery_time_estimate: 0.85, data_center_protection: 0.18,
    aviation_vulnerability: 0.70, space_situational_awareness: 0.20,
  },
  // SWE-002 — critical, grid_infrastructure_collapse (geomag>0.85, grid_hardening<0.20)
  {
    id: "SWE-002", infrastructure_type: "electrical_distribution", region: "EMEA",
    solar_activity_exposure: 0.80, grid_hardening_level: 0.12, transformer_vulnerability: 0.78,
    satellite_shielding: 0.40, gps_dependency: 0.75, communication_backup: 0.20,
    financial_system_exposure: 0.68, emergency_power_reserve: 0.18, early_warning_capability: 0.15,
    geomagnetic_latitude_risk: 0.90, critical_system_redundancy: 0.18, international_coordination: 0.20,
    public_awareness: 0.22, recovery_time_estimate: 0.82, data_center_protection: 0.20,
    aviation_vulnerability: 0.65, space_situational_awareness: 0.25,
  },
  // SWE-003 — critical, satellite_constellation_disruption (sat_shielding<0.20, space_sit<0.20)
  {
    id: "SWE-003", infrastructure_type: "satellite_network", region: "APAC",
    solar_activity_exposure: 0.78, grid_hardening_level: 0.15, transformer_vulnerability: 0.72,
    satellite_shielding: 0.12, gps_dependency: 0.88, communication_backup: 0.15,
    financial_system_exposure: 0.70, emergency_power_reserve: 0.15, early_warning_capability: 0.18,
    geomagnetic_latitude_risk: 0.82, critical_system_redundancy: 0.15, international_coordination: 0.18,
    public_awareness: 0.20, recovery_time_estimate: 0.80, data_center_protection: 0.22,
    aviation_vulnerability: 0.72, space_situational_awareness: 0.15,
  },
  // SWE-004 — high, financial_system_blackout (fin_exp>0.80, data_center<0.25)
  {
    id: "SWE-004", infrastructure_type: "financial_infrastructure", region: "LATAM",
    solar_activity_exposure: 0.42, grid_hardening_level: 0.52, transformer_vulnerability: 0.40,
    satellite_shielding: 0.55, gps_dependency: 0.45, communication_backup: 0.58,
    financial_system_exposure: 0.85, emergency_power_reserve: 0.52, early_warning_capability: 0.55,
    geomagnetic_latitude_risk: 0.40, critical_system_redundancy: 0.55, international_coordination: 0.58,
    public_awareness: 0.52, recovery_time_estimate: 0.45, data_center_protection: 0.20,
    aviation_vulnerability: 0.42, space_situational_awareness: 0.55,
  },
  // SWE-005 — high, emergency_coordination_failure (emergency_power<0.20, intl_coord<0.20)
  {
    id: "SWE-005", infrastructure_type: "emergency_services", region: "SSA",
    solar_activity_exposure: 0.45, grid_hardening_level: 0.50, transformer_vulnerability: 0.42,
    satellite_shielding: 0.52, gps_dependency: 0.48, communication_backup: 0.55,
    financial_system_exposure: 0.45, emergency_power_reserve: 0.15, early_warning_capability: 0.52,
    geomagnetic_latitude_risk: 0.42, critical_system_redundancy: 0.52, international_coordination: 0.15,
    public_awareness: 0.50, recovery_time_estimate: 0.48, data_center_protection: 0.52,
    aviation_vulnerability: 0.40, space_situational_awareness: 0.50,
  },
  // SWE-006 — moderate, none
  {
    id: "SWE-006", infrastructure_type: "aviation_control", region: "NOAM",
    solar_activity_exposure: 0.30, grid_hardening_level: 0.55, transformer_vulnerability: 0.28,
    satellite_shielding: 0.55, gps_dependency: 0.35, communication_backup: 0.58,
    financial_system_exposure: 0.32, emergency_power_reserve: 0.55, early_warning_capability: 0.52,
    geomagnetic_latitude_risk: 0.32, critical_system_redundancy: 0.55, international_coordination: 0.52,
    public_awareness: 0.50, recovery_time_estimate: 0.35, data_center_protection: 0.55,
    aviation_vulnerability: 0.30, space_situational_awareness: 0.55,
  },
  // SWE-007 — low, none
  {
    id: "SWE-007", infrastructure_type: "telecommunications", region: "EMEA",
    solar_activity_exposure: 0.10, grid_hardening_level: 0.85, transformer_vulnerability: 0.10,
    satellite_shielding: 0.88, gps_dependency: 0.12, communication_backup: 0.88,
    financial_system_exposure: 0.10, emergency_power_reserve: 0.88, early_warning_capability: 0.88,
    geomagnetic_latitude_risk: 0.10, critical_system_redundancy: 0.88, international_coordination: 0.88,
    public_awareness: 0.85, recovery_time_estimate: 0.12, data_center_protection: 0.88,
    aviation_vulnerability: 0.10, space_situational_awareness: 0.88,
  },
  // SWE-008 — low, none
  {
    id: "SWE-008", infrastructure_type: "data_centers", region: "APAC",
    solar_activity_exposure: 0.08, grid_hardening_level: 0.88, transformer_vulnerability: 0.08,
    satellite_shielding: 0.90, gps_dependency: 0.10, communication_backup: 0.90,
    financial_system_exposure: 0.08, emergency_power_reserve: 0.90, early_warning_capability: 0.90,
    geomagnetic_latitude_risk: 0.08, critical_system_redundancy: 0.90, international_coordination: 0.90,
    public_awareness: 0.88, recovery_time_estimate: 0.10, data_center_protection: 0.90,
    aviation_vulnerability: 0.08, space_situational_awareness: 0.90,
  },
];

type SWEInput = typeof MOCK_ENTITIES[0];

function exposureScore(e: SWEInput): number {
  return Math.round((e.solar_activity_exposure * 0.4 + e.geomagnetic_latitude_risk * 0.35 + e.transformer_vulnerability * 0.25) * 100 * 100) / 100;
}
function resilienceScore(e: SWEInput): number {
  return Math.round(((1 - e.grid_hardening_level) * 0.4 + (1 - e.satellite_shielding) * 0.35 + (1 - e.critical_system_redundancy) * 0.25) * 100 * 100) / 100;
}
function preparednessScore(e: SWEInput): number {
  return Math.round(((1 - e.early_warning_capability) * 0.4 + (1 - e.emergency_power_reserve) * 0.35 + (1 - e.communication_backup) * 0.25) * 100 * 100) / 100;
}
function cascadeScore(e: SWEInput): number {
  return Math.round((e.financial_system_exposure * 0.4 + e.gps_dependency * 0.35 + e.aviation_vulnerability * 0.25) * 100 * 100) / 100;
}
function compositeScore(exp: number, res: number, pre: number, cas: number): number {
  return Math.round((exp * 0.30 + res * 0.25 + pre * 0.25 + cas * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function spaceWeatherPattern(e: SWEInput): string {
  if (e.solar_activity_exposure > 0.85 && e.transformer_vulnerability > 0.80) return "carrington_level_event_risk";
  if (e.geomagnetic_latitude_risk > 0.85 && e.grid_hardening_level < 0.20) return "grid_infrastructure_collapse";
  if (e.satellite_shielding < 0.20 && e.space_situational_awareness < 0.20) return "satellite_constellation_disruption";
  if (e.financial_system_exposure > 0.80 && e.data_center_protection < 0.25) return "financial_system_blackout";
  if (e.emergency_power_reserve < 0.20 && e.international_coordination < 0.20) return "emergency_coordination_failure";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_tempête_solaire_systémique";
  if (composite >= 40) return "crise_météo_spatiale_majeure";
  if (composite >= 20) return "perturbation_géomagnétique_structurelle";
  return "météo_spatiale_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_protection_infrastructures_critiques";
  if (risk === "high") return "renforcement_durcissement_systèmes_haute_priorité";
  if (risk === "moderate") return "amélioration_préparation_alerte_précoce";
  return "veille_météo_spatiale_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise tempête solaire systémique — infrastructures critiques en péril";
  if (risk === "high") return "🟠 Crise météo spatiale majeure détectée";
  if (risk === "moderate") return "🟡 Perturbation géomagnétique structurelle active";
  return "🟢 Météo spatiale sous surveillance";
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const exp  = exposureScore(e);
      const res  = resilienceScore(e);
      const pre  = preparednessScore(e);
      const cas  = cascadeScore(e);
      const comp = compositeScore(exp, res, pre, cas);
      const risk = riskLevel(comp);
      const pat  = spaceWeatherPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:                    e.entity_id,
        infrastructure_type:          e.infrastructure_type,
        region:                       e.region,
        exposure_score:               exp,
        resilience_score:             res,
        preparedness_score:           pre,
        cascade_score:                cas,
        composite_score:              comp,
        risk_level:                   risk,
        space_weather_pattern:        pat,
        severity:                     sev,
        recommended_action:           action,
        signal:                       sig,
        solar_activity_exposure:      e.solar_activity_exposure,
        geomagnetic_latitude_risk:    e.geomagnetic_latitude_risk,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]              = (risk_distribution[ent.risk_level]              || 0) + 1;
      pattern_distribution[ent.space_weather_pattern] = (pattern_distribution[ent.space_weather_pattern] || 0) + 1;
      severity_distribution[ent.severity]            = (severity_distribution[ent.severity]            || 0) + 1;
      action_distribution[ent.recommended_action]    = (action_distribution[ent.recommended_action]    || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                          407,
      module_name:                        "Météo Spatiale & Tempête Solaire Infrastructure Intelligence Engine",
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
      avg_estimated_space_weather_index:  Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>)));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/space-weather-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(sealResponse(await res.json())));
  } catch {}
  return sealResponse(NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 }));
}
