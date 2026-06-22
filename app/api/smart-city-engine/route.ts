import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_CITIES = [
  // SCE-001: total_surveillance_city + authoritarian_smart_city_export (critical)
  { id:"SCE-001", city_type:"autoritaire_intégré",   region:"APAC",
    camera_surveillance_density:0.92, facial_recognition_deployment:0.90, movement_tracking_intensity:0.88,
    predictive_policing_bias:0.82, IoT_data_vulnerability:0.70, smart_grid_cyber_exposure:0.68,
    digital_twin_city_control:0.85, behavioral_nudging_scale:0.80, private_tech_city_capture:0.75,
    citizen_data_monetization:0.72, democratic_accountability_gap:0.90, algorithmic_urban_discrimination:0.78,
    fiveG_surveillance_integration:0.88, CCP_smart_city_export:0.92, dissent_suppression_capacity:0.88,
    urban_data_sovereignty_loss:0.85, smart_home_surveillance_integration:0.82 },
  // SCE-002: private_tech_city_capture_pattern (critical)
  { id:"SCE-002", city_type:"capture_tech_privée",   region:"NAMER",
    camera_surveillance_density:0.78, facial_recognition_deployment:0.72, movement_tracking_intensity:0.75,
    predictive_policing_bias:0.70, IoT_data_vulnerability:0.65, smart_grid_cyber_exposure:0.62,
    digital_twin_city_control:0.80, behavioral_nudging_scale:0.78, private_tech_city_capture:0.90,
    citizen_data_monetization:0.88, democratic_accountability_gap:0.82, algorithmic_urban_discrimination:0.70,
    fiveG_surveillance_integration:0.75, CCP_smart_city_export:0.40, dissent_suppression_capacity:0.45,
    urban_data_sovereignty_loss:0.80, smart_home_surveillance_integration:0.72 },
  // SCE-003: predictive_policing_dystopia (high)
  { id:"SCE-003", city_type:"policing_prédictif",    region:"NAMER",
    camera_surveillance_density:0.72, facial_recognition_deployment:0.68, movement_tracking_intensity:0.70,
    predictive_policing_bias:0.85, IoT_data_vulnerability:0.55, smart_grid_cyber_exposure:0.52,
    digital_twin_city_control:0.65, behavioral_nudging_scale:0.60, private_tech_city_capture:0.62,
    citizen_data_monetization:0.58, democratic_accountability_gap:0.72, algorithmic_urban_discrimination:0.80,
    fiveG_surveillance_integration:0.65, CCP_smart_city_export:0.30, dissent_suppression_capacity:0.42,
    urban_data_sovereignty_loss:0.65, smart_home_surveillance_integration:0.60 },
  // SCE-004: IoT_city_cyber_catastrophe (high)
  { id:"SCE-004", city_type:"infrastructure_IoT",    region:"EMEA",
    camera_surveillance_density:0.65, facial_recognition_deployment:0.58, movement_tracking_intensity:0.62,
    predictive_policing_bias:0.55, IoT_data_vulnerability:0.88, smart_grid_cyber_exposure:0.82,
    digital_twin_city_control:0.60, behavioral_nudging_scale:0.55, private_tech_city_capture:0.58,
    citizen_data_monetization:0.52, democratic_accountability_gap:0.62, algorithmic_urban_discrimination:0.58,
    fiveG_surveillance_integration:0.62, CCP_smart_city_export:0.25, dissent_suppression_capacity:0.35,
    urban_data_sovereignty_loss:0.60, smart_home_surveillance_integration:0.55 },
  // SCE-005: total_surveillance_city (high)
  { id:"SCE-005", city_type:"surveillance_dense",    region:"APAC",
    camera_surveillance_density:0.90, facial_recognition_deployment:0.85, movement_tracking_intensity:0.78,
    predictive_policing_bias:0.62, IoT_data_vulnerability:0.58, smart_grid_cyber_exposure:0.55,
    digital_twin_city_control:0.60, behavioral_nudging_scale:0.55, private_tech_city_capture:0.52,
    citizen_data_monetization:0.48, democratic_accountability_gap:0.65, algorithmic_urban_discrimination:0.55,
    fiveG_surveillance_integration:0.70, CCP_smart_city_export:0.45, dissent_suppression_capacity:0.50,
    urban_data_sovereignty_loss:0.55, smart_home_surveillance_integration:0.60 },
  // SCE-006: no patterns (moderate)
  { id:"SCE-006", city_type:"mixte_régulé",          region:"EMEA",
    camera_surveillance_density:0.52, facial_recognition_deployment:0.45, movement_tracking_intensity:0.48,
    predictive_policing_bias:0.42, IoT_data_vulnerability:0.50, smart_grid_cyber_exposure:0.45,
    digital_twin_city_control:0.48, behavioral_nudging_scale:0.40, private_tech_city_capture:0.45,
    citizen_data_monetization:0.42, democratic_accountability_gap:0.50, algorithmic_urban_discrimination:0.45,
    fiveG_surveillance_integration:0.48, CCP_smart_city_export:0.18, dissent_suppression_capacity:0.22,
    urban_data_sovereignty_loss:0.45, smart_home_surveillance_integration:0.42 },
  // SCE-007: no patterns (moderate)
  { id:"SCE-007", city_type:"semi_connecté",         region:"LATAM",
    camera_surveillance_density:0.40, facial_recognition_deployment:0.35, movement_tracking_intensity:0.38,
    predictive_policing_bias:0.32, IoT_data_vulnerability:0.42, smart_grid_cyber_exposure:0.38,
    digital_twin_city_control:0.35, behavioral_nudging_scale:0.30, private_tech_city_capture:0.38,
    citizen_data_monetization:0.35, democratic_accountability_gap:0.40, algorithmic_urban_discrimination:0.35,
    fiveG_surveillance_integration:0.38, CCP_smart_city_export:0.12, dissent_suppression_capacity:0.18,
    urban_data_sovereignty_loss:0.38, smart_home_surveillance_integration:0.32 },
  // SCE-008: no patterns (low)
  { id:"SCE-008", city_type:"démocratique_ouvert",   region:"EMEA",
    camera_surveillance_density:0.18, facial_recognition_deployment:0.12, movement_tracking_intensity:0.15,
    predictive_policing_bias:0.10, IoT_data_vulnerability:0.20, smart_grid_cyber_exposure:0.18,
    digital_twin_city_control:0.12, behavioral_nudging_scale:0.10, private_tech_city_capture:0.15,
    citizen_data_monetization:0.12, democratic_accountability_gap:0.15, algorithmic_urban_discrimination:0.10,
    fiveG_surveillance_integration:0.15, CCP_smart_city_export:0.05, dissent_suppression_capacity:0.08,
    urban_data_sovereignty_loss:0.12, smart_home_surveillance_integration:0.10 },
];

type City = typeof MOCK_CITIES[0];

function surveillanceScore(c: City): number {
  const avg = (c.camera_surveillance_density + c.facial_recognition_deployment + c.movement_tracking_intensity + c.fiveG_surveillance_integration + c.smart_home_surveillance_integration) / 5;
  return Math.min(Math.round(avg * 100 * 100) / 100, 100);
}
function controlScore(c: City): number {
  const avg = (c.predictive_policing_bias + c.digital_twin_city_control + c.behavioral_nudging_scale + c.CCP_smart_city_export + c.dissent_suppression_capacity) / 5;
  return Math.min(Math.round(avg * 100 * 100) / 100, 100);
}
function vulnerabilityScore(c: City): number {
  const avg = (c.IoT_data_vulnerability + c.smart_grid_cyber_exposure + c.algorithmic_urban_discrimination) / 3;
  return Math.min(Math.round(avg * 100 * 100) / 100, 100);
}
function sovereigntyScore(c: City): number {
  const avg = (c.private_tech_city_capture + c.citizen_data_monetization + c.democratic_accountability_gap + c.urban_data_sovereignty_loss) / 4;
  return Math.min(Math.round(avg * 100 * 100) / 100, 100);
}
function compositeScore(surv: number, ctrl: number, vuln: number, sov: number): number {
  return Math.min(Math.round((surv * 0.30 + ctrl * 0.25 + vuln * 0.25 + sov * 0.20) * 100) / 100, 100);
}
function riskLevel(comp: number): string {
  if (comp >= 60) return "critical"; if (comp >= 40) return "high"; if (comp >= 20) return "moderate"; return "low";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[smart-city-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    let tSurv = 0, tCtrl = 0, tVuln = 0, tComp = 0;
    let critical = 0, high = 0, moderate = 0, low = 0;
    const dist: Record<string, number> = {};
    for (const city of cities) {
      tSurv += city.surveillance_score; tCtrl += city.control_score;
      tVuln += city.vulnerability_score; tComp += city.composite_score;
      dist[city.risk_level] = (dist[city.risk_level] || 0) + 1;
      if (city.risk_level === "critical")      critical++;
      else if (city.risk_level === "high")     high++;
      else if (city.risk_level === "moderate") moderate++;
      else                                     low++;
    }
    const n = cities.length;
    const avg_composite = Math.round(tComp / n * 100) / 100;
    return sealResponse(NextResponse.json(sealResponse({ cities, summary: {
      module_id: 388,
      module_name: "Smart City & Urban Surveillance Intelligence Engine",
      total: n,
      critical, high, moderate, low,
      avg_composite,
      distributions: dist,
      avg_estimated_smart_city_surveillance_index: Math.round(avg_composite / 100 * 10 * 100) / 100,
      avg_surveillance_score: Math.round(tSurv / n * 100) / 100,
      avg_control_score:      Math.round(tCtrl / n * 100) / 100,
      avg_vulnerability_score: Math.round(tVuln / n * 100) / 100,
    } as Record<string, unknown>}, "smart-city-engine") as Parameters<typeof NextResponse.json>[0]));
  }
  return sealResponse(NextResponse.json(sealResponse(await (await fetch(`${process.env.SWARM_API_URL}/smart-city-engine`, { next: { revalidate: 30 } })).json(), "smart-city-engine") as Parameters<typeof NextResponse.json>[0]));
}
