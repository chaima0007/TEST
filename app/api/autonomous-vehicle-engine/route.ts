import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[autonomous-vehicle-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  // AV-001 — critical, fatal_accident_liability_gap (accident_rate>0.85, liability_clarity>0.80)
  {
    id: "AV-001", vehicle_type: "robotaxi", region: "USA",
    safety_score_raw: 0.92, accident_rate: 0.92, regulatory_compliance: 0.90,
    liability_clarity: 0.88, insurance_coverage: 0.75, ethical_alignment: 0.70,
    data_privacy: 0.65, cybersecurity_resilience: 0.60, public_trust: 0.65,
    legislative_readiness: 0.88, bias_detection: 0.65, emergency_response: 0.72,
    manufacturer_accountability: 0.78, algorithmic_transparency: 0.65,
    mixed_traffic_safety: 0.88, pedestrian_protection: 0.85, weather_performance: 0.70,
  },
  // AV-002 — critical, regulatory_arbitrage_race (regulatory_compliance>0.85, legislative_readiness>0.80)
  {
    id: "AV-002", vehicle_type: "camion_autonome", region: "APAC",
    safety_score_raw: 0.88, accident_rate: 0.70, regulatory_compliance: 0.90,
    liability_clarity: 0.72, insurance_coverage: 0.70, ethical_alignment: 0.68,
    data_privacy: 0.65, cybersecurity_resilience: 0.60, public_trust: 0.60,
    legislative_readiness: 0.85, bias_detection: 0.62, emergency_response: 0.68,
    manufacturer_accountability: 0.72, algorithmic_transparency: 0.65,
    mixed_traffic_safety: 0.72, pedestrian_protection: 0.68, weather_performance: 0.65,
  },
  // AV-003 — critical, algorithmic_bias_discrimination (bias_detection>0.85, ethical_alignment>0.80)
  {
    id: "AV-003", vehicle_type: "navette_autonome", region: "UE",
    safety_score_raw: 0.80, accident_rate: 0.72, regulatory_compliance: 0.75,
    liability_clarity: 0.70, insurance_coverage: 0.68, ethical_alignment: 0.85,
    data_privacy: 0.65, cybersecurity_resilience: 0.62, public_trust: 0.58,
    legislative_readiness: 0.72, bias_detection: 0.88, emergency_response: 0.65,
    manufacturer_accountability: 0.70, algorithmic_transparency: 0.65,
    mixed_traffic_safety: 0.70, pedestrian_protection: 0.68, weather_performance: 0.62,
  },
  // AV-004 — high, insurance_market_collapse (insurance_coverage>0.80, manufacturer_accountability>0.75)
  {
    id: "AV-004", vehicle_type: "drone_livraison", region: "EMEA",
    safety_score_raw: 0.55, accident_rate: 0.48, regulatory_compliance: 0.52,
    liability_clarity: 0.50, insurance_coverage: 0.85, ethical_alignment: 0.48,
    data_privacy: 0.45, cybersecurity_resilience: 0.50, public_trust: 0.52,
    legislative_readiness: 0.50, bias_detection: 0.48, emergency_response: 0.52,
    manufacturer_accountability: 0.80, algorithmic_transparency: 0.48,
    mixed_traffic_safety: 0.50, pedestrian_protection: 0.48, weather_performance: 0.52,
  },
  // AV-005 — high, data_sovereignty_failure (data_privacy>0.80, cybersecurity_resilience>0.75)
  {
    id: "AV-005", vehicle_type: "véhicule_connecté", region: "LATAM",
    safety_score_raw: 0.50, accident_rate: 0.48, regulatory_compliance: 0.52,
    liability_clarity: 0.50, insurance_coverage: 0.48, ethical_alignment: 0.50,
    data_privacy: 0.85, cybersecurity_resilience: 0.80, public_trust: 0.50,
    legislative_readiness: 0.50, bias_detection: 0.48, emergency_response: 0.50,
    manufacturer_accountability: 0.50, algorithmic_transparency: 0.48,
    mixed_traffic_safety: 0.48, pedestrian_protection: 0.50, weather_performance: 0.52,
  },
  // AV-006 — moderate, none
  {
    id: "AV-006", vehicle_type: "véhicule_partagé", region: "NOAM",
    safety_score_raw: 0.32, accident_rate: 0.28, regulatory_compliance: 0.30,
    liability_clarity: 0.32, insurance_coverage: 0.28, ethical_alignment: 0.30,
    data_privacy: 0.28, cybersecurity_resilience: 0.30, public_trust: 0.32,
    legislative_readiness: 0.28, bias_detection: 0.30, emergency_response: 0.32,
    manufacturer_accountability: 0.28, algorithmic_transparency: 0.30,
    mixed_traffic_safety: 0.28, pedestrian_protection: 0.30, weather_performance: 0.28,
  },
  // AV-007 — low, none
  {
    id: "AV-007", vehicle_type: "bus_autonome", region: "UE",
    safety_score_raw: 0.10, accident_rate: 0.12, regulatory_compliance: 0.10,
    liability_clarity: 0.12, insurance_coverage: 0.10, ethical_alignment: 0.12,
    data_privacy: 0.10, cybersecurity_resilience: 0.12, public_trust: 0.15,
    legislative_readiness: 0.10, bias_detection: 0.12, emergency_response: 0.10,
    manufacturer_accountability: 0.12, algorithmic_transparency: 0.10,
    mixed_traffic_safety: 0.12, pedestrian_protection: 0.10, weather_performance: 0.12,
  },
  // AV-008 — low, none
  {
    id: "AV-008", vehicle_type: "taxi_autonome", region: "APAC",
    safety_score_raw: 0.08, accident_rate: 0.10, regulatory_compliance: 0.08,
    liability_clarity: 0.10, insurance_coverage: 0.08, ethical_alignment: 0.10,
    data_privacy: 0.08, cybersecurity_resilience: 0.10, public_trust: 0.12,
    legislative_readiness: 0.08, bias_detection: 0.10, emergency_response: 0.08,
    manufacturer_accountability: 0.10, algorithmic_transparency: 0.08,
    mixed_traffic_safety: 0.10, pedestrian_protection: 0.08, weather_performance: 0.10,
  },
];

type AVInput = typeof MOCK_ENTITIES[0];

function safetyScore(e: AVInput): number {
  return Math.round((e.accident_rate * 0.40 + e.mixed_traffic_safety * 0.35 + e.pedestrian_protection * 0.25) * 100 * 100) / 100;
}
function liabilityScore(e: AVInput): number {
  return Math.round((e.liability_clarity * 0.40 + e.manufacturer_accountability * 0.35 + e.insurance_coverage * 0.25) * 100 * 100) / 100;
}
function regulatoryScore(e: AVInput): number {
  return Math.round((e.regulatory_compliance * 0.40 + e.legislative_readiness * 0.35 + e.safety_score_raw * 0.25) * 100 * 100) / 100;
}
function ethicsScore(e: AVInput): number {
  return Math.round((e.ethical_alignment * 0.40 + e.algorithmic_transparency * 0.35 + e.bias_detection * 0.25) * 100 * 100) / 100;
}
function compositeScore(saf: number, lia: number, reg: number, eth: number): number {
  return Math.round((saf * 0.30 + lia * 0.25 + reg * 0.25 + eth * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function avPattern(e: AVInput): string {
  if (e.accident_rate > 0.85 && e.liability_clarity > 0.80) return "fatal_accident_liability_gap";
  if (e.regulatory_compliance > 0.85 && e.legislative_readiness > 0.80) return "regulatory_arbitrage_race";
  if (e.bias_detection > 0.85 && e.ethical_alignment > 0.80) return "algorithmic_bias_discrimination";
  if (e.insurance_coverage > 0.80 && e.manufacturer_accountability > 0.75) return "insurance_market_collapse";
  if (e.data_privacy > 0.80 && e.cybersecurity_resilience > 0.75) return "data_sovereignty_failure";
  return "none";
}
function severity(composite: number): string {
  if (composite >= 60) return "crise_responsabilité_véhicules_autonomes_systémique";
  if (composite >= 40) return "risque_juridique_majeur_véhicule_autonome";
  if (composite >= 20) return "vulnérabilité_réglementaire_structurelle";
  return "surveillance_sécurité_véhicules_autonomes";
}
function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_responsabilité_juridique_critique";
  if (risk === "high") return "révision_cadre_légal_véhicules_autonomes_accélérée";
  if (risk === "moderate") return "renforcement_protocoles_sécurité_réglementaires";
  return "veille_conformité_véhicules_autonomes_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Crise responsabilité juridique véhicules autonomes — intervention systémique requise";
  if (risk === "high") return "🟠 Risque juridique majeur détecté — révision légale urgente";
  if (risk === "moderate") return "🟡 Vulnérabilité réglementaire structurelle active";
  return "🟢 Sécurité véhicules autonomes sous surveillance";
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const saf  = safetyScore(e);
      const lia  = liabilityScore(e);
      const reg  = regulatoryScore(e);
      const eth  = ethicsScore(e);
      const comp = compositeScore(saf, lia, reg, eth);
      const risk = riskLevel(comp);
      const pat  = avPattern(e);
      const sev  = severity(comp);
      const action = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:               e.entity_id,
        vehicle_type:            e.vehicle_type,
        region:                  e.region,
        safety_score:            saf,
        liability_score:         lia,
        regulatory_score:        reg,
        ethics_score:            eth,
        composite_score:         comp,
        risk_level:              risk,
        av_pattern:              pat,
        severity:                sev,
        recommended_action:      action,
        signal:                  sig,
        accident_rate:           e.accident_rate,
        liability_clarity:       e.liability_clarity,
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
      pattern_distribution[ent.av_pattern]        = (pattern_distribution[ent.av_pattern]        || 0) + 1;
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
      module_id:                        394,
      module_name:                      "Véhicules Autonomes & Responsabilité Juridique Intelligence Engine",
      total:                            n,
      critical:                         criticalCount,
      high:                             highCount,
      moderate:                         moderateCount,
      low:                              lowCount,
      avg_composite:                    avgComposite,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_av_safety_index:    Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>)));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/autonomous-vehicle-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(sealResponse(await res.json())));
  } catch {}
  return sealResponse(NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 }));
}
