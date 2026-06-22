import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK_ENTITIES = [
  // TFE-001 — EMEA, social_media_platform → critical, monopoly_feudalism
  // monopoly_feudalism: platform_market_capture>=0.70 AND gatekeeper_tax_burden>=0.65
  // composite >=60 → critical
  {
    id: "TFE-001", platform_domain: "social_media_platform", region: "EMEA",
    platform_market_capture: 0.88,
    cloud_rent_extraction_rate: 0.72,
    data_feudal_rent_index: 0.75,
    digital_labor_exploitation_rate: 0.60,
    api_dependency_lock_in: 0.70,
    algorithmic_sovereignty_erosion: 0.78,
    gatekeeper_tax_burden: 0.82,
    network_effect_moat_strength: 0.85,
    surveillance_capitalism_depth: 0.80,
    digital_commons_enclosure_rate: 0.65,
    platform_worker_precarity: 0.55,
    sovereign_cloud_dependency: 0.68,
    content_moderation_power: 0.90,
    antitrust_evasion_sophistication: 0.80,
    digital_exit_barrier_height: 0.72,
    small_business_platform_dependency: 0.75,
    innovation_tax_to_gatekeeper: 0.70,
  },
  // TFE-002 — APAC, local_marketplace → low, none
  // composite < 20 → low; no pattern triggers
  {
    id: "TFE-002", platform_domain: "local_marketplace", region: "APAC",
    platform_market_capture: 0.12,
    cloud_rent_extraction_rate: 0.08,
    data_feudal_rent_index: 0.10,
    digital_labor_exploitation_rate: 0.08,
    api_dependency_lock_in: 0.12,
    algorithmic_sovereignty_erosion: 0.10,
    gatekeeper_tax_burden: 0.10,
    network_effect_moat_strength: 0.15,
    surveillance_capitalism_depth: 0.10,
    digital_commons_enclosure_rate: 0.08,
    platform_worker_precarity: 0.10,
    sovereign_cloud_dependency: 0.10,
    content_moderation_power: 0.15,
    antitrust_evasion_sophistication: 0.08,
    digital_exit_barrier_height: 0.10,
    small_business_platform_dependency: 0.12,
    innovation_tax_to_gatekeeper: 0.08,
  },
  // TFE-003 — NOAM, cloud_platform → high, cloud_colonialism
  // cloud_colonialism: sovereign_cloud_dependency>=0.70 AND api_dependency_lock_in>=0.65
  // monopoly_feudalism must NOT fire: platform_market_capture<0.70 OR gatekeeper_tax_burden<0.65
  // data_serfdom must NOT fire: data_feudal_rent_index<0.70 OR surveillance_capitalism_depth<0.65
  // composite >=40 and <60 → high
  {
    id: "TFE-003", platform_domain: "cloud_platform", region: "NOAM",
    platform_market_capture: 0.50,
    cloud_rent_extraction_rate: 0.65,
    data_feudal_rent_index: 0.55,
    digital_labor_exploitation_rate: 0.40,
    api_dependency_lock_in: 0.78,
    algorithmic_sovereignty_erosion: 0.55,
    gatekeeper_tax_burden: 0.48,
    network_effect_moat_strength: 0.52,
    surveillance_capitalism_depth: 0.48,
    digital_commons_enclosure_rate: 0.45,
    platform_worker_precarity: 0.38,
    sovereign_cloud_dependency: 0.82,
    content_moderation_power: 0.42,
    antitrust_evasion_sophistication: 0.55,
    digital_exit_barrier_height: 0.60,
    small_business_platform_dependency: 0.58,
    innovation_tax_to_gatekeeper: 0.52,
  },
  // TFE-004 — LATAM, regional_platform → low, none
  // composite < 20 → low; no pattern triggers
  {
    id: "TFE-004", platform_domain: "regional_platform", region: "LATAM",
    platform_market_capture: 0.10,
    cloud_rent_extraction_rate: 0.10,
    data_feudal_rent_index: 0.08,
    digital_labor_exploitation_rate: 0.10,
    api_dependency_lock_in: 0.10,
    algorithmic_sovereignty_erosion: 0.08,
    gatekeeper_tax_burden: 0.08,
    network_effect_moat_strength: 0.12,
    surveillance_capitalism_depth: 0.08,
    digital_commons_enclosure_rate: 0.10,
    platform_worker_precarity: 0.08,
    sovereign_cloud_dependency: 0.12,
    content_moderation_power: 0.10,
    antitrust_evasion_sophistication: 0.08,
    digital_exit_barrier_height: 0.08,
    small_business_platform_dependency: 0.10,
    innovation_tax_to_gatekeeper: 0.10,
  },
  // TFE-005 — MEA, big_tech_ecosystem → critical, data_serfdom
  // data_serfdom: data_feudal_rent_index>=0.70 AND surveillance_capitalism_depth>=0.65
  // monopoly_feudalism must NOT fire: platform_market_capture<0.70 OR gatekeeper_tax_burden<0.65
  // composite >=60 → critical
  {
    id: "TFE-005", platform_domain: "big_tech_ecosystem", region: "MEA",
    platform_market_capture: 0.62,
    cloud_rent_extraction_rate: 0.70,
    data_feudal_rent_index: 0.85,
    digital_labor_exploitation_rate: 0.65,
    api_dependency_lock_in: 0.60,
    algorithmic_sovereignty_erosion: 0.75,
    gatekeeper_tax_burden: 0.60,
    network_effect_moat_strength: 0.68,
    surveillance_capitalism_depth: 0.88,
    digital_commons_enclosure_rate: 0.62,
    platform_worker_precarity: 0.55,
    sovereign_cloud_dependency: 0.65,
    content_moderation_power: 0.78,
    antitrust_evasion_sophistication: 0.72,
    digital_exit_barrier_height: 0.58,
    small_business_platform_dependency: 0.70,
    innovation_tax_to_gatekeeper: 0.68,
  },
  // TFE-006 — EMEA, digital_marketplace → moderate, none
  // composite >=20 and <40 → moderate; no pattern triggers
  {
    id: "TFE-006", platform_domain: "digital_marketplace", region: "EMEA",
    platform_market_capture: 0.35,
    cloud_rent_extraction_rate: 0.28,
    data_feudal_rent_index: 0.30,
    digital_labor_exploitation_rate: 0.32,
    api_dependency_lock_in: 0.30,
    algorithmic_sovereignty_erosion: 0.28,
    gatekeeper_tax_burden: 0.32,
    network_effect_moat_strength: 0.38,
    surveillance_capitalism_depth: 0.30,
    digital_commons_enclosure_rate: 0.28,
    platform_worker_precarity: 0.30,
    sovereign_cloud_dependency: 0.32,
    content_moderation_power: 0.35,
    antitrust_evasion_sophistication: 0.30,
    digital_exit_barrier_height: 0.28,
    small_business_platform_dependency: 0.35,
    innovation_tax_to_gatekeeper: 0.28,
  },
  // TFE-007 — APAC, gig_economy_platform → high, worker_feudalization
  // worker_feudalization: digital_labor_exploitation_rate>=0.70 AND platform_worker_precarity>=0.65
  // cloud_colonialism must NOT fire: sovereign_cloud_dependency<0.70 OR api_dependency_lock_in<0.65
  // digital_enclosure must NOT fire: digital_commons_enclosure_rate<0.70 OR digital_exit_barrier_height<0.65
  // monopoly_feudalism must NOT fire, data_serfdom must NOT fire
  // composite >=40 and <60 → high
  {
    id: "TFE-007", platform_domain: "gig_economy_platform", region: "APAC",
    platform_market_capture: 0.48,
    cloud_rent_extraction_rate: 0.40,
    data_feudal_rent_index: 0.42,
    digital_labor_exploitation_rate: 0.82,
    api_dependency_lock_in: 0.48,
    algorithmic_sovereignty_erosion: 0.50,
    gatekeeper_tax_burden: 0.45,
    network_effect_moat_strength: 0.52,
    surveillance_capitalism_depth: 0.55,
    digital_commons_enclosure_rate: 0.45,
    platform_worker_precarity: 0.78,
    sovereign_cloud_dependency: 0.42,
    content_moderation_power: 0.38,
    antitrust_evasion_sophistication: 0.45,
    digital_exit_barrier_height: 0.48,
    small_business_platform_dependency: 0.50,
    innovation_tax_to_gatekeeper: 0.42,
  },
  // TFE-008 — NOAM, platform_conglomerate → critical, digital_enclosure
  // digital_enclosure: digital_commons_enclosure_rate>=0.70 AND digital_exit_barrier_height>=0.65
  // cloud_colonialism must NOT fire: sovereign_cloud_dependency<0.70 OR api_dependency_lock_in<0.65
  // monopoly_feudalism must NOT fire, data_serfdom must NOT fire
  // composite >=60 → critical
  {
    id: "TFE-008", platform_domain: "platform_conglomerate", region: "NOAM",
    platform_market_capture: 0.65,
    cloud_rent_extraction_rate: 0.72,
    data_feudal_rent_index: 0.65,
    digital_labor_exploitation_rate: 0.60,
    api_dependency_lock_in: 0.60,
    algorithmic_sovereignty_erosion: 0.80,
    gatekeeper_tax_burden: 0.60,
    network_effect_moat_strength: 0.75,
    surveillance_capitalism_depth: 0.60,
    digital_commons_enclosure_rate: 0.82,
    platform_worker_precarity: 0.55,
    sovereign_cloud_dependency: 0.62,
    content_moderation_power: 0.78,
    antitrust_evasion_sophistication: 0.75,
    digital_exit_barrier_height: 0.80,
    small_business_platform_dependency: 0.78,
    innovation_tax_to_gatekeeper: 0.72,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function captureScore(e: Entity): number {
  const raw = (
    e.platform_market_capture * 0.4 +
    e.network_effect_moat_strength * 0.35 +
    e.gatekeeper_tax_burden * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function rentScore(e: Entity): number {
  const raw = (
    e.data_feudal_rent_index * 0.4 +
    e.cloud_rent_extraction_rate * 0.35 +
    e.innovation_tax_to_gatekeeper * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function dependencyScore(e: Entity): number {
  const raw = (
    e.api_dependency_lock_in * 0.4 +
    e.digital_exit_barrier_height * 0.35 +
    e.small_business_platform_dependency * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function sovereigntyScore(e: Entity): number {
  const raw = (
    e.algorithmic_sovereignty_erosion * 0.4 +
    e.sovereign_cloud_dependency * 0.35 +
    e.digital_commons_enclosure_rate * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function feudalComposite(cap: number, rent: number, dep: number, sov: number): number {
  return Math.round((cap * 0.30 + rent * 0.25 + dep * 0.25 + sov * 0.20) * 100) / 100;
}

function feudalPattern(e: Entity): string {
  if (e.platform_market_capture >= 0.70 && e.gatekeeper_tax_burden >= 0.65)
    return "monopoly_feudalism";
  if (e.data_feudal_rent_index >= 0.70 && e.surveillance_capitalism_depth >= 0.65)
    return "data_serfdom";
  if (e.sovereign_cloud_dependency >= 0.70 && e.api_dependency_lock_in >= 0.65)
    return "cloud_colonialism";
  if (e.digital_commons_enclosure_rate >= 0.70 && e.digital_exit_barrier_height >= 0.65)
    return "digital_enclosure";
  if (e.digital_labor_exploitation_rate >= 0.70 && e.platform_worker_precarity >= 0.65)
    return "worker_feudalization";
  return "none";
}

function feudalRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function feudalSeverity(comp: number): string {
  if (comp >= 75) return "feudal_emergency";
  if (comp >= 50) return "high_feudalization";
  if (comp >= 25) return "feudal_dynamics_emerging";
  return "digital_commons_healthy";
}

function recommendedAction(risk: string, pattern: string): string {
  if (risk === "critical") return "antitrust_emergency_action";
  if (risk === "high" && pattern === "cloud_colonialism") return "sovereign_cloud_program";
  if (risk === "high") return "platform_regulation";
  if (risk === "moderate") return "market_monitoring";
  return "no_action";
}

function feudalSignal(e: Entity, risk: string, comp: number): string {
  if (risk === "critical") {
    return `Critique — capture marché plateforme ${Math.round(e.platform_market_capture * 100)}% — rente féodale données ${Math.round(e.data_feudal_rent_index * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "high") {
    return `Élevé — dépendance cloud souverain ${Math.round(e.sovereign_cloud_dependency * 100)}% — verrouillage API ${Math.round(e.api_dependency_lock_in * 100)}% — composite ${Math.round(comp)}`;
  }
  if (risk === "moderate") {
    return `Modéré — enclosure communs numériques ${Math.round(e.digital_commons_enclosure_rate * 100)}% — composite ${Math.round(comp)}`;
  }
  return "Communs numériques florissants — concurrence saine, souveraineté préservée, plateformes équilibrées";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[techno-feudalism-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const rc: Record<string, number> = {};
    const pc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tCap = 0, tRent = 0, tDep = 0, tSov = 0, tComp = 0, crisisC = 0, interventionC = 0;

    for (const ent of entities) {
      rc[ent.feudal_risk]           = (rc[ent.feudal_risk]           || 0) + 1;
      pc[ent.feudal_pattern]        = (pc[ent.feudal_pattern]        || 0) + 1;
      sc[ent.feudal_severity]       = (sc[ent.feudal_severity]       || 0) + 1;
      ac[ent.recommended_action]    = (ac[ent.recommended_action]    || 0) + 1;
      tCap   += ent.capture_score;
      tRent  += ent.rent_score;
      tDep   += ent.dependency_score;
      tSov   += ent.sovereignty_score;
      tComp  += ent.feudal_composite;
      if (ent.is_feudal_crisis)             crisisC++;
      if (ent.requires_feudal_intervention) interventionC++;
    }

    const n = entities.length;
    const avgComp = Math.round(tComp / n * 10) / 10;
    const summary = {
      total:                              n,
      risk_counts:                        rc,
      pattern_counts:                     pc,
      severity_counts:                    sc,
      action_counts:                      ac,
      avg_feudal_composite:               avgComp,
      feudal_crisis_count:                crisisC,
      feudal_intervention_count:          interventionC,
      avg_capture_score:                  Math.round(tCap  / n * 10) / 10,
      avg_rent_score:                     Math.round(tRent / n * 10) / 10,
      avg_dependency_score:               Math.round(tDep  / n * 10) / 10,
      avg_sovereignty_score:              Math.round(tSov  / n * 10) / 10,
      avg_estimated_feudalization_index:  Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(sealResponse({ entities, summary }, "techno-feudalism-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/techno-feudalism-engine`, { next: { revalidate: 30 } });
    const data = await upstream.json();
    return sealResponse(NextResponse.json(sealResponse(data, "techno-feudalism-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "Upstream techno-feudalism engine unavailable" }, "techno-feudalism-engine"),
      { status: 502 }
    ));
  }
}
