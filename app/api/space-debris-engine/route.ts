import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // SDE-001 — critical, kessler_syndrome_onset (cascade_initiation_risk>0.85 AND debris_density>0.80)
  {
    entity_id: "SDE-001", orbital_shell: "LEO-550km", region: "Global",
    debris_density: 0.90, collision_probability: 0.88, cascade_initiation_risk: 0.92,
    mega_constellation_contribution: 0.55, mitigation_compliance_failure: 0.72,
    active_debris_removal_gap: 0.68, conjunction_event_rate: 0.78,
    weaponized_debris_risk: 0.42, LEO_saturation_level: 0.75,
    GEO_contamination_risk: 0.58, orbital_slot_exhaustion: 0.55,
    launch_cadence_impact: 0.60, international_governance_failure: 0.70,
    insurance_market_collapse: 0.62, space_weather_amplification: 0.58,
    debris_weaponization: 0.38, remediation_technology_lag: 0.72,
  },
  // SDE-002 — low, none
  {
    entity_id: "SDE-002", orbital_shell: "GEO-35786km", region: "EMEA",
    debris_density: 0.10, collision_probability: 0.08, cascade_initiation_risk: 0.10,
    mega_constellation_contribution: 0.12, mitigation_compliance_failure: 0.08,
    active_debris_removal_gap: 0.10, conjunction_event_rate: 0.08,
    weaponized_debris_risk: 0.10, LEO_saturation_level: 0.08,
    GEO_contamination_risk: 0.12, orbital_slot_exhaustion: 0.10,
    launch_cadence_impact: 0.08, international_governance_failure: 0.10,
    insurance_market_collapse: 0.08, space_weather_amplification: 0.12,
    debris_weaponization: 0.10, remediation_technology_lag: 0.08,
  },
  // SDE-003 — critical, mega_constellation_crisis (mega_constellation_contribution>0.85 AND LEO_saturation_level>0.80)
  {
    entity_id: "SDE-003", orbital_shell: "LEO-340km", region: "NOAM",
    debris_density: 0.72, collision_probability: 0.68, cascade_initiation_risk: 0.70,
    mega_constellation_contribution: 0.92, mitigation_compliance_failure: 0.75,
    active_debris_removal_gap: 0.68, conjunction_event_rate: 0.72,
    weaponized_debris_risk: 0.38, LEO_saturation_level: 0.88,
    GEO_contamination_risk: 0.55, orbital_slot_exhaustion: 0.60,
    launch_cadence_impact: 0.65, international_governance_failure: 0.72,
    insurance_market_collapse: 0.58, space_weather_amplification: 0.62,
    debris_weaponization: 0.35, remediation_technology_lag: 0.70,
  },
  // SDE-004 — moderate, none
  {
    entity_id: "SDE-004", orbital_shell: "MEO-20200km", region: "APAC",
    debris_density: 0.28, collision_probability: 0.30, cascade_initiation_risk: 0.28,
    mega_constellation_contribution: 0.30, mitigation_compliance_failure: 0.28,
    active_debris_removal_gap: 0.30, conjunction_event_rate: 0.28,
    weaponized_debris_risk: 0.30, LEO_saturation_level: 0.28,
    GEO_contamination_risk: 0.30, orbital_slot_exhaustion: 0.28,
    launch_cadence_impact: 0.30, international_governance_failure: 0.28,
    insurance_market_collapse: 0.30, space_weather_amplification: 0.28,
    debris_weaponization: 0.30, remediation_technology_lag: 0.28,
  },
  // SDE-005 — critical, debris_weaponization_cascade (weaponized_debris_risk>0.85 AND debris_weaponization>0.80)
  {
    entity_id: "SDE-005", orbital_shell: "LEO-800km", region: "MEA",
    debris_density: 0.70, collision_probability: 0.68, cascade_initiation_risk: 0.72,
    mega_constellation_contribution: 0.55, mitigation_compliance_failure: 0.78,
    active_debris_removal_gap: 0.70, conjunction_event_rate: 0.65,
    weaponized_debris_risk: 0.90, LEO_saturation_level: 0.65,
    GEO_contamination_risk: 0.60, orbital_slot_exhaustion: 0.58,
    launch_cadence_impact: 0.62, international_governance_failure: 0.75,
    insurance_market_collapse: 0.72, space_weather_amplification: 0.60,
    debris_weaponization: 0.88, remediation_technology_lag: 0.68,
  },
  // SDE-006 — high, governance_remediation_failure (international_governance_failure>0.80 AND active_debris_removal_gap>0.75)
  {
    entity_id: "SDE-006", orbital_shell: "SSO-600km", region: "LATAM",
    debris_density: 0.52, collision_probability: 0.48, cascade_initiation_risk: 0.50,
    mega_constellation_contribution: 0.48, mitigation_compliance_failure: 0.58,
    active_debris_removal_gap: 0.82, conjunction_event_rate: 0.50,
    weaponized_debris_risk: 0.45, LEO_saturation_level: 0.52,
    GEO_contamination_risk: 0.48, orbital_slot_exhaustion: 0.50,
    launch_cadence_impact: 0.48, international_governance_failure: 0.85,
    insurance_market_collapse: 0.50, space_weather_amplification: 0.48,
    debris_weaponization: 0.45, remediation_technology_lag: 0.55,
  },
  // SDE-007 — high, orbital_commons_collapse (orbital_slot_exhaustion>0.80 AND launch_cadence_impact>0.75)
  {
    entity_id: "SDE-007", orbital_shell: "GEO-35786km", region: "EMEA",
    debris_density: 0.55, collision_probability: 0.50, cascade_initiation_risk: 0.52,
    mega_constellation_contribution: 0.58, mitigation_compliance_failure: 0.55,
    active_debris_removal_gap: 0.60, conjunction_event_rate: 0.52,
    weaponized_debris_risk: 0.45, LEO_saturation_level: 0.55,
    GEO_contamination_risk: 0.60, orbital_slot_exhaustion: 0.88,
    launch_cadence_impact: 0.82, international_governance_failure: 0.60,
    insurance_market_collapse: 0.52, space_weather_amplification: 0.55,
    debris_weaponization: 0.42, remediation_technology_lag: 0.58,
  },
  // SDE-008 — critical, kessler_syndrome_onset (second instance, all scores elevated)
  {
    entity_id: "SDE-008", orbital_shell: "LEO-1200km", region: "APAC",
    debris_density: 0.88, collision_probability: 0.85, cascade_initiation_risk: 0.90,
    mega_constellation_contribution: 0.80, mitigation_compliance_failure: 0.82,
    active_debris_removal_gap: 0.78, conjunction_event_rate: 0.82,
    weaponized_debris_risk: 0.72, LEO_saturation_level: 0.80,
    GEO_contamination_risk: 0.75, orbital_slot_exhaustion: 0.78,
    launch_cadence_impact: 0.80, international_governance_failure: 0.85,
    insurance_market_collapse: 0.78, space_weather_amplification: 0.75,
    debris_weaponization: 0.68, remediation_technology_lag: 0.82,
  },
];

type SDEInput = typeof MOCK_ENTITIES[0];

function cascadeScore(e: SDEInput): number {
  return Math.round((e.cascade_initiation_risk * 0.4 + e.collision_probability * 0.35 + e.conjunction_event_rate * 0.25) * 100 * 100) / 100;
}
function densityScore(e: SDEInput): number {
  return Math.round((e.debris_density * 0.4 + e.LEO_saturation_level * 0.35 + e.GEO_contamination_risk * 0.25) * 100 * 100) / 100;
}
function governanceScore(e: SDEInput): number {
  return Math.round((e.international_governance_failure * 0.4 + e.mitigation_compliance_failure * 0.35 + e.remediation_technology_lag * 0.25) * 100 * 100) / 100;
}
function weaponizationScore(e: SDEInput): number {
  return Math.round((e.weaponized_debris_risk * 0.4 + e.debris_weaponization * 0.35 + e.insurance_market_collapse * 0.25) * 100 * 100) / 100;
}
function compositeScore(cas: number, den: number, gov: number, wep: number): number {
  return Math.round((cas * 0.30 + den * 0.25 + gov * 0.25 + wep * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function debrisPattern(e: SDEInput): string {
  if (e.cascade_initiation_risk > 0.85 && e.debris_density > 0.80) return "kessler_syndrome_onset";
  if (e.mega_constellation_contribution > 0.85 && e.LEO_saturation_level > 0.80) return "mega_constellation_crisis";
  if (e.weaponized_debris_risk > 0.85 && e.debris_weaponization > 0.80) return "debris_weaponization_cascade";
  if (e.international_governance_failure > 0.80 && e.active_debris_removal_gap > 0.75) return "governance_remediation_failure";
  if (e.orbital_slot_exhaustion > 0.80 && e.launch_cadence_impact > 0.75) return "orbital_commons_collapse";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "effondrement_orbital_systémique";
  if (composite >= 40) return "crise_débris_spatiaux_majeure";
  if (composite >= 20) return "saturation_orbitale_structurelle";
  return "débris_sous_surveillance";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_débris_urgence_mondiale";
  if (risk === "high") return "retrait_débris_actifs_urgence";
  if (risk === "moderate") return "renforcement_gouvernance_orbitale";
  return "veille_débris_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Syndrome Kessler imminent — effondrement orbital critique";
  if (risk === "high") return "🟠 Crise débris spatiaux majeure détectée";
  if (risk === "moderate") return "🟡 Saturation orbitale structurelle active";
  return "🟢 Débris spatiaux sous surveillance et contenus";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const cas  = cascadeScore(e);
      const den  = densityScore(e);
      const gov  = governanceScore(e);
      const wep  = weaponizationScore(e);
      const comp = compositeScore(cas, den, gov, wep);
      const risk = riskLevel(comp);
      const pat  = debrisPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        entity_id:             e.entity_id,
        orbital_shell:         e.orbital_shell,
        region:                e.region,
        cascade_score:         cas,
        density_score:         den,
        governance_score:      gov,
        weaponization_score:   wep,
        composite_score:       comp,
        risk_level:            risk,
        debris_pattern:        pat,
        severity:              sev,
        recommended_action:    action,
        signal:                sig,
        debris_density:        e.debris_density,
        collision_probability: e.collision_probability,
      };
    });

    const risk_distribution: Record<string, number>     = {};
    const pattern_distribution: Record<string, number>  = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number>   = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level]           = (risk_distribution[ent.risk_level]           || 0) + 1;
      pattern_distribution[ent.debris_pattern]    = (pattern_distribution[ent.debris_pattern]    || 0) + 1;
      severity_distribution[ent.severity]         = (severity_distribution[ent.severity]         || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;

    const summary = {
      module_id:                           370,
      module_name:                         "Space Debris & Kessler Syndrome Intelligence Engine",
      total:                               n,
      critical:                            criticalCount,
      high:                                highCount,
      moderate:                            moderateCount,
      low:                                 lowCount,
      avg_composite:                       avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_kessler_risk_index:    Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "space-debris-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/space-debris-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json(), "space-debris-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream unavailable", code: 502 }, "space-debris-engine"),
      { status: 502 }
    );
  }
}
