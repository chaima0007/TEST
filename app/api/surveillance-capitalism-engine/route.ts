import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // SCE-001 — Social_Media, USA → critical, behavioral_totalitarianism
  // behavioral_totalitarianism: behavioral_totalitarianism_risk>=0.70 AND autonomy_erosion_index>=0.65
  // composite >=60 → critical
  {
    id: "SCE-001", platform_type: "Social_Media", region: "USA",
    behavioral_surplus_extraction_rate: 0.90,
    prediction_product_invasiveness: 0.82,
    attention_capture_monopoly: 0.88,
    psychological_profiling_depth: 0.85,
    consent_manufacturing_level: 0.80,
    behavioral_modification_intensity: 0.87,
    data_broker_ecosystem_density: 0.78,
    third_party_surveillance_reach: 0.75,
    shadow_profiling_prevalence: 0.80,
    continuous_tracking_saturation: 0.88,
    intimate_data_commodification: 0.76,
    behavioral_futures_market_size: 0.84,
    autonomy_erosion_index: 0.88,
    prediction_weaponization_rate: 0.82,
    surveillance_competitive_advantage: 0.85,
    data_colonialism_index: 0.70,
    behavioral_totalitarianism_risk: 0.92,
  },
  // SCE-002 — E-Commerce, EU → low, none
  // composite < 20 → low; no pattern triggers
  {
    id: "SCE-002", platform_type: "E-Commerce", region: "EU",
    behavioral_surplus_extraction_rate: 0.12,
    prediction_product_invasiveness: 0.15,
    attention_capture_monopoly: 0.10,
    psychological_profiling_depth: 0.12,
    consent_manufacturing_level: 0.10,
    behavioral_modification_intensity: 0.11,
    data_broker_ecosystem_density: 0.13,
    third_party_surveillance_reach: 0.10,
    shadow_profiling_prevalence: 0.12,
    continuous_tracking_saturation: 0.14,
    intimate_data_commodification: 0.10,
    behavioral_futures_market_size: 0.11,
    autonomy_erosion_index: 0.12,
    prediction_weaponization_rate: 0.10,
    surveillance_competitive_advantage: 0.13,
    data_colonialism_index: 0.10,
    behavioral_totalitarianism_risk: 0.11,
  },
  // SCE-003 — AdTech, UK → high, prediction_product_hegemony
  // prediction_product_hegemony: prediction_product_invasiveness>=0.70 AND behavioral_futures_market_size>=0.65
  // behavioral_totalitarianism must NOT fire: behavioral_totalitarianism_risk<0.70 OR autonomy_erosion_index<0.65
  // composite >=40 and <60 → high
  {
    id: "SCE-003", platform_type: "AdTech", region: "UK",
    behavioral_surplus_extraction_rate: 0.62,
    prediction_product_invasiveness: 0.82,
    attention_capture_monopoly: 0.60,
    psychological_profiling_depth: 0.58,
    consent_manufacturing_level: 0.55,
    behavioral_modification_intensity: 0.60,
    data_broker_ecosystem_density: 0.65,
    third_party_surveillance_reach: 0.62,
    shadow_profiling_prevalence: 0.55,
    continuous_tracking_saturation: 0.60,
    intimate_data_commodification: 0.52,
    behavioral_futures_market_size: 0.78,
    autonomy_erosion_index: 0.55,
    prediction_weaponization_rate: 0.65,
    surveillance_competitive_advantage: 0.60,
    data_colonialism_index: 0.50,
    behavioral_totalitarianism_risk: 0.55,
  },
  // SCE-004 — HealthTech, Canada → low, none
  // composite < 20 → low; no pattern triggers
  {
    id: "SCE-004", platform_type: "HealthTech", region: "Canada",
    behavioral_surplus_extraction_rate: 0.15,
    prediction_product_invasiveness: 0.18,
    attention_capture_monopoly: 0.12,
    psychological_profiling_depth: 0.14,
    consent_manufacturing_level: 0.16,
    behavioral_modification_intensity: 0.13,
    data_broker_ecosystem_density: 0.15,
    third_party_surveillance_reach: 0.12,
    shadow_profiling_prevalence: 0.14,
    continuous_tracking_saturation: 0.16,
    intimate_data_commodification: 0.18,
    behavioral_futures_market_size: 0.13,
    autonomy_erosion_index: 0.14,
    prediction_weaponization_rate: 0.12,
    surveillance_competitive_advantage: 0.15,
    data_colonialism_index: 0.12,
    behavioral_totalitarianism_risk: 0.13,
  },
  // SCE-005 — Mobile_Apps, USA → critical, consent_manufacturing_crisis
  // consent_manufacturing_crisis: consent_manufacturing_level>=0.70 AND behavioral_modification_intensity>=0.65
  // behavioral_totalitarianism must NOT fire: behavioral_totalitarianism_risk<0.70 OR autonomy_erosion_index<0.65
  // prediction_product_hegemony must NOT fire
  // composite >=60 → critical
  {
    id: "SCE-005", platform_type: "Mobile_Apps", region: "USA",
    behavioral_surplus_extraction_rate: 0.82,
    prediction_product_invasiveness: 0.65,
    attention_capture_monopoly: 0.80,
    psychological_profiling_depth: 0.75,
    consent_manufacturing_level: 0.88,
    behavioral_modification_intensity: 0.85,
    data_broker_ecosystem_density: 0.78,
    third_party_surveillance_reach: 0.72,
    shadow_profiling_prevalence: 0.65,
    continuous_tracking_saturation: 0.80,
    intimate_data_commodification: 0.70,
    behavioral_futures_market_size: 0.62,
    autonomy_erosion_index: 0.60,
    prediction_weaponization_rate: 0.75,
    surveillance_competitive_advantage: 0.78,
    data_colonialism_index: 0.60,
    behavioral_totalitarianism_risk: 0.62,
  },
  // SCE-006 — IoT, Germany → moderate, none
  // composite >=20 and <40 → moderate; no pattern triggers
  {
    id: "SCE-006", platform_type: "IoT", region: "Germany",
    behavioral_surplus_extraction_rate: 0.35,
    prediction_product_invasiveness: 0.38,
    attention_capture_monopoly: 0.30,
    psychological_profiling_depth: 0.35,
    consent_manufacturing_level: 0.32,
    behavioral_modification_intensity: 0.30,
    data_broker_ecosystem_density: 0.38,
    third_party_surveillance_reach: 0.35,
    shadow_profiling_prevalence: 0.32,
    continuous_tracking_saturation: 0.40,
    intimate_data_commodification: 0.30,
    behavioral_futures_market_size: 0.35,
    autonomy_erosion_index: 0.38,
    prediction_weaponization_rate: 0.32,
    surveillance_competitive_advantage: 0.35,
    data_colonialism_index: 0.30,
    behavioral_totalitarianism_risk: 0.35,
  },
  // SCE-007 — DataBroker, USA → high, shadow_profiling_empire
  // shadow_profiling_empire: shadow_profiling_prevalence>=0.70 AND psychological_profiling_depth>=0.65
  // behavioral_totalitarianism must NOT fire, prediction_product_hegemony must NOT fire
  // consent_manufacturing_crisis must NOT fire
  // composite >=40 and <60 → high
  {
    id: "SCE-007", platform_type: "DataBroker", region: "USA",
    behavioral_surplus_extraction_rate: 0.62,
    prediction_product_invasiveness: 0.58,
    attention_capture_monopoly: 0.55,
    psychological_profiling_depth: 0.78,
    consent_manufacturing_level: 0.55,
    behavioral_modification_intensity: 0.58,
    data_broker_ecosystem_density: 0.72,
    third_party_surveillance_reach: 0.68,
    shadow_profiling_prevalence: 0.85,
    continuous_tracking_saturation: 0.65,
    intimate_data_commodification: 0.70,
    behavioral_futures_market_size: 0.60,
    autonomy_erosion_index: 0.55,
    prediction_weaponization_rate: 0.60,
    surveillance_competitive_advantage: 0.65,
    data_colonialism_index: 0.55,
    behavioral_totalitarianism_risk: 0.52,
  },
  // SCE-008 — BigTech, Global → critical, data_colonialism
  // data_colonialism: data_colonialism_index>=0.70 AND third_party_surveillance_reach>=0.65
  // behavioral_totalitarianism must NOT fire, prediction_product_hegemony must NOT fire
  // consent_manufacturing_crisis must NOT fire, shadow_profiling_empire must NOT fire
  // composite >=60 → critical
  {
    id: "SCE-008", platform_type: "BigTech", region: "Global",
    behavioral_surplus_extraction_rate: 0.88,
    prediction_product_invasiveness: 0.65,
    attention_capture_monopoly: 0.82,
    psychological_profiling_depth: 0.62,
    consent_manufacturing_level: 0.65,
    behavioral_modification_intensity: 0.62,
    data_broker_ecosystem_density: 0.80,
    third_party_surveillance_reach: 0.85,
    shadow_profiling_prevalence: 0.65,
    continuous_tracking_saturation: 0.85,
    intimate_data_commodification: 0.78,
    behavioral_futures_market_size: 0.80,
    autonomy_erosion_index: 0.60,
    prediction_weaponization_rate: 0.82,
    surveillance_competitive_advantage: 0.88,
    data_colonialism_index: 0.90,
    behavioral_totalitarianism_risk: 0.62,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function extractionScore(e: Entity): number {
  const raw = (
    e.behavioral_surplus_extraction_rate * 0.4 +
    e.behavioral_futures_market_size * 0.35 +
    e.data_broker_ecosystem_density * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function manipulationScore(e: Entity): number {
  const raw = (
    e.behavioral_modification_intensity * 0.4 +
    e.attention_capture_monopoly * 0.35 +
    e.consent_manufacturing_level * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function profilingScore(e: Entity): number {
  const raw = (
    e.psychological_profiling_depth * 0.4 +
    e.shadow_profiling_prevalence * 0.35 +
    e.intimate_data_commodification * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function autonomyScore(e: Entity): number {
  const raw = (
    e.autonomy_erosion_index * 0.4 +
    e.behavioral_totalitarianism_risk * 0.35 +
    e.data_colonialism_index * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(ext: number, man: number, pro: number, aut: number): number {
  return Math.round((ext * 0.30 + man * 0.25 + pro * 0.25 + aut * 0.20) * 100) / 100;
}

function surveillancePattern(e: Entity): string {
  if (e.behavioral_totalitarianism_risk >= 0.70 && e.autonomy_erosion_index >= 0.65)
    return "behavioral_totalitarianism";
  if (e.prediction_product_invasiveness >= 0.70 && e.behavioral_futures_market_size >= 0.65)
    return "prediction_product_hegemony";
  if (e.consent_manufacturing_level >= 0.70 && e.behavioral_modification_intensity >= 0.65)
    return "consent_manufacturing_crisis";
  if (e.shadow_profiling_prevalence >= 0.70 && e.psychological_profiling_depth >= 0.65)
    return "shadow_profiling_empire";
  if (e.data_colonialism_index >= 0.70 && e.third_party_surveillance_reach >= 0.65)
    return "data_colonialism";
  return "none";
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function severity(risk: string): string {
  if (risk === "critical") return "capitalisme_surveillance_total";
  if (risk === "high") return "extraction_comportementale_massive";
  if (risk === "moderate") return "surveillance_structurelle_active";
  return "surveillance_contenue";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "régulation_surveillance_urgente";
  if (risk === "high") return "démantèlement_extraction_comportementale";
  if (risk === "moderate") return "renforcement_consentement_éclairé";
  return "veille_surveillance_continue";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Capitalisme de surveillance total — extraction comportementale systémique";
  if (risk === "high") return "🟠 Extraction comportementale massive détectée";
  if (risk === "moderate") return "🟡 Surveillance structurelle active";
  return "🟢 Surveillance capitaliste contenue";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[surveillance-capitalism-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const patternDist: Record<string, number> = {};
    const riskDist: Record<string, number> = {};
    const severityDist: Record<string, number> = {};
    const actionDist: Record<string, number> = {};
    let totalComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      patternDist[ent.surveillance_pattern]  = (patternDist[ent.surveillance_pattern]  || 0) + 1;
      riskDist[ent.risk_level]               = (riskDist[ent.risk_level]               || 0) + 1;
      severityDist[ent.severity]             = (severityDist[ent.severity]             || 0) + 1;
      actionDist[ent.recommended_action]     = (actionDist[ent.recommended_action]     || 0) + 1;
      totalComp += ent.composite_score;
      if (ent.risk_level === "critical") criticalCount++;
      else if (ent.risk_level === "high") highCount++;
      else if (ent.risk_level === "moderate") moderateCount++;
      else lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(totalComp / n * 100) / 100;
    const summary = {
      module_id:                                    335,
      module_name:                                  "Surveillance Capitalism & Data Extraction Intelligence Engine",
      total_entities:                               n,
      critical_count:                               criticalCount,
      high_count:                                   highCount,
      moderate_count:                               moderateCount,
      low_count:                                    lowCount,
      avg_composite:                                avgComposite,
      pattern_distribution:                         patternDist,
      risk_distribution:                            riskDist,
      severity_distribution:                        severityDist,
      action_distribution:                          actionDist,
      avg_estimated_surveillance_capitalism_index:  Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "surveillance-capitalism-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/surveillance-capitalism-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return sealResponse(NextResponse.json(sealResponse(data, "surveillance-capitalism-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream surveillance capitalism engine unavailable" }, "surveillance-capitalism-engine"),
      { status: 502 }
    ));
  }
}
