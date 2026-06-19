import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ZONES = [
  // PI-001 coral_reef Pacific — critical/tipping_point_breach
  { zone_id:"PI-001", ecosystem_type:"coral_reef",          region:"Pacific",      planetary_boundary_breach_score:0.88, biodiversity_loss_rate:0.75, carbon_sequestration_capacity:0.18, tipping_point_proximity:0.90, ecosystem_service_value_score:0.20, climate_resilience_index:0.15, pollutant_concentration_risk:0.78, species_extinction_velocity:0.72, water_cycle_disruption_risk:0.65, soil_degradation_rate:0.55, natural_capital_depletion:0.82, ecosystem_connectivity_score:0.18, restoration_potential_score:0.22, indigenous_stewardship_quality:0.30, corporate_biodiversity_exposure:0.72, regulatory_nature_risk:0.68, nature_positive_trajectory:0.12 },
  // PI-002 forest_biome Nordic — low/thriving
  { zone_id:"PI-002", ecosystem_type:"forest_biome",        region:"Nordic",       planetary_boundary_breach_score:0.08, biodiversity_loss_rate:0.10, carbon_sequestration_capacity:0.92, tipping_point_proximity:0.08, ecosystem_service_value_score:0.90, climate_resilience_index:0.88, pollutant_concentration_risk:0.08, species_extinction_velocity:0.10, water_cycle_disruption_risk:0.08, soil_degradation_rate:0.10, natural_capital_depletion:0.08, ecosystem_connectivity_score:0.92, restoration_potential_score:0.88, indigenous_stewardship_quality:0.85, corporate_biodiversity_exposure:0.10, regulatory_nature_risk:0.08, nature_positive_trajectory:0.90 },
  // PI-003 ocean_system Indo-Pacific — high/biodiversity_collapse
  { zone_id:"PI-003", ecosystem_type:"ocean_system",        region:"Indo-Pacific", planetary_boundary_breach_score:0.62, biodiversity_loss_rate:0.78, carbon_sequestration_capacity:0.38, tipping_point_proximity:0.55, ecosystem_service_value_score:0.35, climate_resilience_index:0.30, pollutant_concentration_risk:0.72, species_extinction_velocity:0.80, water_cycle_disruption_risk:0.58, soil_degradation_rate:0.45, natural_capital_depletion:0.68, ecosystem_connectivity_score:0.28, restoration_potential_score:0.32, indigenous_stewardship_quality:0.42, corporate_biodiversity_exposure:0.65, regulatory_nature_risk:0.60, nature_positive_trajectory:0.22 },
  // PI-004 soil_microbiome Central Europe — low/degrading
  { zone_id:"PI-004", ecosystem_type:"soil_microbiome",     region:"Central Europe", planetary_boundary_breach_score:0.22, biodiversity_loss_rate:0.28, carbon_sequestration_capacity:0.70, tipping_point_proximity:0.18, ecosystem_service_value_score:0.68, climate_resilience_index:0.72, pollutant_concentration_risk:0.28, species_extinction_velocity:0.22, water_cycle_disruption_risk:0.25, soil_degradation_rate:0.32, natural_capital_depletion:0.25, ecosystem_connectivity_score:0.72, restoration_potential_score:0.75, indigenous_stewardship_quality:0.68, corporate_biodiversity_exposure:0.22, regulatory_nature_risk:0.20, nature_positive_trajectory:0.72 },
  // PI-005 atmospheric_layer Arctic — critical/carbon_crisis
  { zone_id:"PI-005", ecosystem_type:"atmospheric_layer",   region:"Arctic",       planetary_boundary_breach_score:0.82, biodiversity_loss_rate:0.62, carbon_sequestration_capacity:0.12, tipping_point_proximity:0.78, ecosystem_service_value_score:0.18, climate_resilience_index:0.12, pollutant_concentration_risk:0.85, species_extinction_velocity:0.58, water_cycle_disruption_risk:0.72, soil_degradation_rate:0.65, natural_capital_depletion:0.78, ecosystem_connectivity_score:0.22, restoration_potential_score:0.15, indigenous_stewardship_quality:0.28, corporate_biodiversity_exposure:0.80, regulatory_nature_risk:0.75, nature_positive_trajectory:0.10 },
  // PI-006 freshwater_basin Amazon — moderate/none
  { zone_id:"PI-006", ecosystem_type:"freshwater_basin",    region:"Amazon",       planetary_boundary_breach_score:0.42, biodiversity_loss_rate:0.38, carbon_sequestration_capacity:0.58, tipping_point_proximity:0.35, ecosystem_service_value_score:0.60, climate_resilience_index:0.55, pollutant_concentration_risk:0.40, species_extinction_velocity:0.35, water_cycle_disruption_risk:0.40, soil_degradation_rate:0.38, natural_capital_depletion:0.42, ecosystem_connectivity_score:0.58, restoration_potential_score:0.62, indigenous_stewardship_quality:0.55, corporate_biodiversity_exposure:0.38, regulatory_nature_risk:0.35, nature_positive_trajectory:0.52 },
  // PI-007 permafrost_zone Siberia — high/water_system_failure
  { zone_id:"PI-007", ecosystem_type:"permafrost_zone",     region:"Siberia",      planetary_boundary_breach_score:0.68, biodiversity_loss_rate:0.52, carbon_sequestration_capacity:0.28, tipping_point_proximity:0.62, ecosystem_service_value_score:0.30, climate_resilience_index:0.22, pollutant_concentration_risk:0.58, species_extinction_velocity:0.48, water_cycle_disruption_risk:0.78, soil_degradation_rate:0.72, natural_capital_depletion:0.65, ecosystem_connectivity_score:0.32, restoration_potential_score:0.28, indigenous_stewardship_quality:0.38, corporate_biodiversity_exposure:0.60, regulatory_nature_risk:0.55, nature_positive_trajectory:0.20 },
  // PI-008 urban_heat_island MENA — critical/ecosystem_fragmentation
  { zone_id:"PI-008", ecosystem_type:"urban_heat_island",   region:"MENA",         planetary_boundary_breach_score:0.75, biodiversity_loss_rate:0.68, carbon_sequestration_capacity:0.15, tipping_point_proximity:0.70, ecosystem_service_value_score:0.15, climate_resilience_index:0.18, pollutant_concentration_risk:0.88, species_extinction_velocity:0.55, water_cycle_disruption_risk:0.62, soil_degradation_rate:0.60, natural_capital_depletion:0.72, ecosystem_connectivity_score:0.12, restoration_potential_score:0.20, indigenous_stewardship_quality:0.18, corporate_biodiversity_exposure:0.78, regulatory_nature_risk:0.72, nature_positive_trajectory:0.12 },
];

type Zone = typeof MOCK_ZONES[0];

function boundaryScore(z: Zone): number {
  const avg = (z.planetary_boundary_breach_score + z.tipping_point_proximity + (1 - z.carbon_sequestration_capacity)) / 3;
  return Math.min(Math.round(avg * 100 * 100) / 100, 100);
}
function biodiversityScore(z: Zone): number {
  const avg = (z.biodiversity_loss_rate + z.species_extinction_velocity + (1 - z.ecosystem_connectivity_score)) / 3;
  return Math.min(Math.round(avg * 100 * 100) / 100, 100);
}
function degradationScore(z: Zone): number {
  const avg = (z.soil_degradation_rate + z.water_cycle_disruption_risk + z.natural_capital_depletion) / 3;
  return Math.min(Math.round(avg * 100 * 100) / 100, 100);
}
function exposureScore(z: Zone): number {
  const avg = (z.corporate_biodiversity_exposure + z.regulatory_nature_risk + (1 - z.nature_positive_trajectory)) / 3;
  return Math.min(Math.round(avg * 100 * 100) / 100, 100);
}
function composite(bnd: number, bio: number, deg: number, exp: number): number {
  return Math.min(Math.round((bnd * 0.30 + bio * 0.25 + deg * 0.25 + exp * 0.20) * 100) / 100, 100);
}
function ecosystemPattern(z: Zone): string {
  if (z.tipping_point_proximity >= 0.70 && z.planetary_boundary_breach_score >= 0.65) return "tipping_point_breach";
  if (z.biodiversity_loss_rate >= 0.65 && z.species_extinction_velocity >= 0.60)      return "biodiversity_collapse";
  if (z.carbon_sequestration_capacity <= 0.30 && z.planetary_boundary_breach_score >= 0.60) return "carbon_crisis";
  if (z.water_cycle_disruption_risk >= 0.65 && z.soil_degradation_rate >= 0.55)       return "water_system_failure";
  if (z.ecosystem_connectivity_score <= 0.30 && z.natural_capital_depletion >= 0.55)  return "ecosystem_fragmentation";
  return "none";
}
function planetaryRisk(c: number): string { if (c >= 60) return "critical"; if (c >= 40) return "high"; if (c >= 20) return "moderate"; return "low"; }
function severity(c: number): string { if (c >= 60) return "collapsed"; if (c >= 40) return "critical_stress"; if (c >= 20) return "degrading"; return "thriving"; }
function action(r: string, p: string): string {
  if (r === "critical") { if (p === "tipping_point_breach") return "ecosystem_emergency"; return "tipping_point_intervention"; }
  if (r === "high")     { if (p === "carbon_crisis") return "carbon_emergency"; return "nature_positive_program"; }
  if (r === "moderate") return "ecosystem_monitoring";
  return "no_action";
}
function signal(z: Zone, pat: string, comp: number): string {
  if (comp < 20) return "Écosystème en bonne santé — frontières planétaires respectées, biodiversité préservée, trajectoire nature-positive confirmée";
  const labels: Record<string,string> = {
    tipping_point_breach:    "Franchissement de point de bascule",
    biodiversity_collapse:   "Effondrement de la biodiversité",
    carbon_crisis:           "Crise carbone — séquestration critique",
    water_system_failure:    "Défaillance du cycle de l'eau",
    ecosystem_fragmentation: "Fragmentation écosystémique",
  };
  const label = labels[pat] ?? pat.replace(/_/g," ");
  return `${label} — transgression frontières ${z.planetary_boundary_breach_score.toFixed(2)} — proximité bascule ${z.tipping_point_proximity.toFixed(2)} — perte biodiversité ${z.biodiversity_loss_rate.toFixed(2)} — composite ${Math.round(comp)}`;
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const zones = MOCK_ZONES.map(z => {
      const bnd = boundaryScore(z), bio = biodiversityScore(z), deg = degradationScore(z), exp = exposureScore(z);
      const comp = composite(bnd, bio, deg, exp), pat = ecosystemPattern(z), r = planetaryRisk(comp), sev = severity(comp), act = action(r, pat);
      const isTipping = comp >= 60 || z.tipping_point_proximity >= 0.70;
      const requiresEmergency = act === "ecosystem_emergency" || act === "tipping_point_intervention";
      return {
        zone_id: z.zone_id, ecosystem_type: z.ecosystem_type, region: z.region,
        planetary_risk: r, ecosystem_pattern: pat, ecosystem_severity: sev, recommended_action: act,
        boundary_score: bnd, biodiversity_score: bio, degradation_score: deg, exposure_score: exp,
        planetary_risk_composite: comp,
        is_tipping_point_risk: isTipping,
        requires_emergency_intervention: requiresEmergency,
        estimated_planetary_risk_index: Math.round(Math.min(comp / 100 * (z.planetary_boundary_breach_score + z.tipping_point_proximity) / 2 * 10, 10.0) * 100) / 100,
        ecosystem_signal: signal(z, pat, comp),
      };
    });

    const rc: Record<string,number>={}, pc: Record<string,number>={}, sc: Record<string,number>={}, ac: Record<string,number>={};
    let tbnd=0, tbio=0, tdeg=0, texp=0, tcomp=0, tridx=0, tippingC=0, emergencyC=0;
    for (const zone of zones) {
      rc[zone.planetary_risk]       = (rc[zone.planetary_risk]       || 0) + 1;
      pc[zone.ecosystem_pattern]    = (pc[zone.ecosystem_pattern]    || 0) + 1;
      sc[zone.ecosystem_severity]   = (sc[zone.ecosystem_severity]   || 0) + 1;
      ac[zone.recommended_action]   = (ac[zone.recommended_action]   || 0) + 1;
      tbnd  += zone.boundary_score;
      tbio  += zone.biodiversity_score;
      tdeg  += zone.degradation_score;
      texp  += zone.exposure_score;
      tcomp += zone.planetary_risk_composite;
      tridx += zone.estimated_planetary_risk_index;
      if (zone.is_tipping_point_risk)           tippingC++;
      if (zone.requires_emergency_intervention) emergencyC++;
    }
    const n = zones.length;
    return NextResponse.json(sealResponse({ zones, summary: {
      total: n, risk_counts: rc, pattern_counts: pc, severity_counts: sc, action_counts: ac,
      avg_planetary_risk_composite:       Math.round(tcomp / n * 10) / 10,
      tipping_point_risk_count:           tippingC,
      emergency_intervention_count:       emergencyC,
      avg_boundary_score:                 Math.round(tbnd  / n * 10) / 10,
      avg_biodiversity_score:             Math.round(tbio  / n * 10) / 10,
      avg_degradation_score:              Math.round(tdeg  / n * 10) / 10,
      avg_exposure_score:                 Math.round(texp  / n * 10) / 10,
      avg_estimated_planetary_risk_index: Math.round(tridx / n * 100) / 100,
    } as Record<string, unknown>}, "planetary-intelligence-engine") as Parameters<typeof NextResponse.json>[0]);
  }
  return NextResponse.json(sealResponse(await (await fetch(`${process.env.SWARM_API_URL}/planetary-intelligence-engine`)).json(), "planetary-intelligence-engine") as Parameters<typeof NextResponse.json>[0]);
}
