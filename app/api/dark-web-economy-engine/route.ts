import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// ── Module 384 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// Dark Web Economy & Underground Market Intelligence Engine
// 8 entities covering all 5 crime patterns and all 4 risk levels.

const MOCK_ENTITIES = [
  // DWE-001 — EMEA, ransomware_marketplace → critical, ransomware_industrial_complex
  // ransomware_ecosystem_scale>0.85 AND cybercrime_as_service>0.80 → ransomware_industrial_complex
  // composite≥60 → critical
  {
    id: "DWE-001", market_type: "ransomware_marketplace", region: "EMEA",
    ransomware_ecosystem_scale: 0.92,        drug_market_volume: 0.65,
    stolen_data_market_size: 0.78,           weapon_trafficking_intensity: 0.60,
    human_trafficking_digital: 0.55,         cybercrime_as_service: 0.88,
    crypto_laundering_volume: 0.72,          nation_state_marketplace: 0.65,
    darknet_market_resilience: 0.80,         exit_scam_frequency: 0.55,
    law_enforcement_effectiveness_gap: 0.75, AI_crime_automation: 0.70,
    zero_day_exploit_market: 0.68,           credential_market_saturation: 0.75,
    darkweb_to_mainstream_spillover: 0.72,   illicit_services_professionalization: 0.78,
    criminal_marketplace_consolidation: 0.70,
  },
  // DWE-002 — APAC, community_forum → low, none
  // All low values → composite<20, no pattern triggered
  {
    id: "DWE-002", market_type: "community_forum", region: "APAC",
    ransomware_ecosystem_scale: 0.08,        drug_market_volume: 0.10,
    stolen_data_market_size: 0.08,           weapon_trafficking_intensity: 0.08,
    human_trafficking_digital: 0.10,         cybercrime_as_service: 0.08,
    crypto_laundering_volume: 0.10,          nation_state_marketplace: 0.08,
    darknet_market_resilience: 0.08,         exit_scam_frequency: 0.10,
    law_enforcement_effectiveness_gap: 0.08, AI_crime_automation: 0.08,
    zero_day_exploit_market: 0.08,           credential_market_saturation: 0.08,
    darkweb_to_mainstream_spillover: 0.10,   illicit_services_professionalization: 0.08,
    criminal_marketplace_consolidation: 0.08,
  },
  // DWE-003 — MEA, state_sponsored_market → critical, nation_state_crime_market
  // nation_state_marketplace>0.85 AND zero_day_exploit_market>0.80 → nation_state_crime_market
  // ransomware_ecosystem_scale=0.60≤0.85 → avoids ransomware_industrial_complex
  // composite≥60 → critical
  {
    id: "DWE-003", market_type: "state_sponsored_market", region: "MEA",
    ransomware_ecosystem_scale: 0.60,        drug_market_volume: 0.55,
    stolen_data_market_size: 0.70,           weapon_trafficking_intensity: 0.65,
    human_trafficking_digital: 0.50,         cybercrime_as_service: 0.70,
    crypto_laundering_volume: 0.65,          nation_state_marketplace: 0.92,
    darknet_market_resilience: 0.75,         exit_scam_frequency: 0.50,
    law_enforcement_effectiveness_gap: 0.78, AI_crime_automation: 0.68,
    zero_day_exploit_market: 0.88,           credential_market_saturation: 0.70,
    darkweb_to_mainstream_spillover: 0.68,   illicit_services_professionalization: 0.72,
    criminal_marketplace_consolidation: 0.65,
  },
  // DWE-004 — LATAM, small_forum → low, none
  // All low values → composite<20, no pattern triggered
  {
    id: "DWE-004", market_type: "small_forum", region: "LATAM",
    ransomware_ecosystem_scale: 0.10,        drug_market_volume: 0.08,
    stolen_data_market_size: 0.10,           weapon_trafficking_intensity: 0.08,
    human_trafficking_digital: 0.10,         cybercrime_as_service: 0.08,
    crypto_laundering_volume: 0.10,          nation_state_marketplace: 0.08,
    darknet_market_resilience: 0.08,         exit_scam_frequency: 0.10,
    law_enforcement_effectiveness_gap: 0.08, AI_crime_automation: 0.10,
    zero_day_exploit_market: 0.08,           credential_market_saturation: 0.08,
    darkweb_to_mainstream_spillover: 0.08,   illicit_services_professionalization: 0.10,
    criminal_marketplace_consolidation: 0.08,
  },
  // DWE-005 — EMEA, consolidated_darknet → critical, criminal_marketplace_empire
  // criminal_marketplace_consolidation>0.85 AND illicit_services_professionalization>0.80 → criminal_marketplace_empire
  // ransomware_ecosystem_scale=0.65≤0.85 → avoids ransomware_industrial_complex
  // nation_state_marketplace=0.60≤0.85 → avoids nation_state_crime_market
  // composite≥60 → critical
  {
    id: "DWE-005", market_type: "consolidated_darknet", region: "EMEA",
    ransomware_ecosystem_scale: 0.65,        drug_market_volume: 0.70,
    stolen_data_market_size: 0.72,           weapon_trafficking_intensity: 0.68,
    human_trafficking_digital: 0.60,         cybercrime_as_service: 0.75,
    crypto_laundering_volume: 0.70,          nation_state_marketplace: 0.60,
    darknet_market_resilience: 0.80,         exit_scam_frequency: 0.62,
    law_enforcement_effectiveness_gap: 0.72, AI_crime_automation: 0.70,
    zero_day_exploit_market: 0.65,           credential_market_saturation: 0.72,
    darkweb_to_mainstream_spillover: 0.68,   illicit_services_professionalization: 0.88,
    criminal_marketplace_consolidation: 0.92,
  },
  // DWE-006 — NOAM, credential_shop → moderate, none
  // composite in [20,40), no pattern triggered
  {
    id: "DWE-006", market_type: "credential_shop", region: "NOAM",
    ransomware_ecosystem_scale: 0.28,        drug_market_volume: 0.30,
    stolen_data_market_size: 0.35,           weapon_trafficking_intensity: 0.22,
    human_trafficking_digital: 0.25,         cybercrime_as_service: 0.28,
    crypto_laundering_volume: 0.30,          nation_state_marketplace: 0.22,
    darknet_market_resilience: 0.28,         exit_scam_frequency: 0.25,
    law_enforcement_effectiveness_gap: 0.30, AI_crime_automation: 0.28,
    zero_day_exploit_market: 0.25,           credential_market_saturation: 0.35,
    darkweb_to_mainstream_spillover: 0.28,   illicit_services_professionalization: 0.25,
    criminal_marketplace_consolidation: 0.22,
  },
  // DWE-007 — APAC, ai_automation_hub → high, AI_crime_automation_crisis
  // AI_crime_automation>0.80 AND darkweb_to_mainstream_spillover>0.75 → AI_crime_automation_crisis
  // ransomware_ecosystem_scale=0.50≤0.85 → avoids ransomware_industrial_complex
  // nation_state_marketplace=0.45≤0.85 → avoids nation_state_crime_market
  // criminal_marketplace_consolidation=0.48≤0.85 → avoids criminal_marketplace_empire
  // composite in [40,60) → high
  {
    id: "DWE-007", market_type: "ai_automation_hub", region: "APAC",
    ransomware_ecosystem_scale: 0.50,        drug_market_volume: 0.42,
    stolen_data_market_size: 0.48,           weapon_trafficking_intensity: 0.40,
    human_trafficking_digital: 0.45,         cybercrime_as_service: 0.55,
    crypto_laundering_volume: 0.50,          nation_state_marketplace: 0.45,
    darknet_market_resilience: 0.52,         exit_scam_frequency: 0.42,
    law_enforcement_effectiveness_gap: 0.55, AI_crime_automation: 0.88,
    zero_day_exploit_market: 0.48,           credential_market_saturation: 0.50,
    darkweb_to_mainstream_spillover: 0.82,   illicit_services_professionalization: 0.60,
    criminal_marketplace_consolidation: 0.48,
  },
  // DWE-008 — LATAM, trafficking_network → critical, human_trafficking_digital_network
  // human_trafficking_digital>0.80 AND crypto_laundering_volume>0.75 → human_trafficking_digital_network
  // ransomware_ecosystem_scale=0.55≤0.85 → avoids ransomware_industrial_complex
  // nation_state_marketplace=0.50≤0.85 → avoids nation_state_crime_market
  // criminal_marketplace_consolidation=0.60≤0.85 → avoids criminal_marketplace_empire
  // AI_crime_automation=0.65≤0.80 → avoids AI_crime_automation_crisis
  // composite≥60 → critical
  {
    id: "DWE-008", market_type: "trafficking_network", region: "LATAM",
    ransomware_ecosystem_scale: 0.55,        drug_market_volume: 0.70,
    stolen_data_market_size: 0.65,           weapon_trafficking_intensity: 0.72,
    human_trafficking_digital: 0.88,         cybercrime_as_service: 0.68,
    crypto_laundering_volume: 0.82,          nation_state_marketplace: 0.50,
    darknet_market_resilience: 0.72,         exit_scam_frequency: 0.60,
    law_enforcement_effectiveness_gap: 0.78, AI_crime_automation: 0.65,
    zero_day_exploit_market: 0.55,           credential_market_saturation: 0.65,
    darkweb_to_mainstream_spillover: 0.70,   illicit_services_professionalization: 0.75,
    criminal_marketplace_consolidation: 0.60,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

// ── Scoring functions (mirrors Python engine exactly) ──────────────────────────

function crimeScaleScore(e: Entity): number {
  return Math.round((e.ransomware_ecosystem_scale * 0.40 + e.drug_market_volume * 0.35 + e.weapon_trafficking_intensity * 0.25) * 100 * 100) / 100;
}

function ecosystemScore(e: Entity): number {
  return Math.round((e.cybercrime_as_service * 0.40 + e.darknet_market_resilience * 0.35 + e.criminal_marketplace_consolidation * 0.25) * 100 * 100) / 100;
}

function enforcementGapScore(e: Entity): number {
  return Math.round((e.law_enforcement_effectiveness_gap * 0.40 + e.crypto_laundering_volume * 0.35 + e.exit_scam_frequency * 0.25) * 100 * 100) / 100;
}

function spilloverScore(e: Entity): number {
  return Math.round((e.darkweb_to_mainstream_spillover * 0.40 + e.AI_crime_automation * 0.35 + e.illicit_services_professionalization * 0.25) * 100 * 100) / 100;
}

function compositeScore(cs: number, eco: number, enf: number, sp: number): number {
  return Math.round((cs * 0.30 + eco * 0.25 + enf * 0.25 + sp * 0.20) * 100) / 100;
}

function darkwebRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function darkwebPattern(e: Entity): string {
  if (e.ransomware_ecosystem_scale > 0.85 && e.cybercrime_as_service > 0.80) return "ransomware_industrial_complex";
  if (e.nation_state_marketplace > 0.85 && e.zero_day_exploit_market > 0.80) return "nation_state_crime_market";
  if (e.criminal_marketplace_consolidation > 0.85 && e.illicit_services_professionalization > 0.80) return "criminal_marketplace_empire";
  if (e.AI_crime_automation > 0.80 && e.darkweb_to_mainstream_spillover > 0.75) return "AI_crime_automation_crisis";
  if (e.human_trafficking_digital > 0.80 && e.crypto_laundering_volume > 0.75) return "human_trafficking_digital_network";
  return "none";
}

function darkwebSeverity(risk: string): string {
  if (risk === "critical") return "économie_criminelle_systémique";
  if (risk === "high")     return "marché_souterrain_majeur";
  if (risk === "moderate") return "vulnérabilité_darkweb_structurelle";
  return "risque_darkweb_contenu";
}

function darkwebAction(risk: string): string {
  if (risk === "critical") return "démantèlement_urgence_darkweb";
  if (risk === "high")     return "neutralisation_réseau_souterrain";
  if (risk === "moderate") return "surveillance_renforcée_marchés_illicites";
  return "veille_darkweb_continue";
}

function darkwebSignal(risk: string): string {
  const signals: Record<string, string> = {
    critical: "🔴 Économie criminelle systémique — marché souterrain à grande échelle",
    high:     "🟠 Marché souterrain majeur détecté — intervention requise",
    moderate: "🟡 Vulnérabilité darkweb structurelle active",
    low:      "🟢 Risque darkweb contenu et surveillé",
  };
  return signals[risk] ?? "Statut inconnu";
}

// ── GET handler ────────────────────────────────────────────────────────────────

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const cs   = crimeScaleScore(e);
      const eco  = ecosystemScore(e);
      const enf  = enforcementGapScore(e);
      const sp   = spilloverScore(e);
      const comp = compositeScore(cs, eco, enf, sp);
      const risk = darkwebRisk(comp);
      const pat  = darkwebPattern(e);
      const sev  = darkwebSeverity(risk);
      const act  = darkwebAction(risk);
      const sig  = darkwebSignal(risk);
      return {
        id:                   e.entity_id,
        market_type:                 e.market_type,
        region:                      e.region,
        crime_scale_score:           cs,
        ecosystem_score:             eco,
        enforcement_gap_score:       enf,
        spillover_score:             sp,
        composite_score:             comp,
        risk_level:                  risk,
        crime_pattern:               pat,
        severity:                    sev,
        recommended_action:          act,
        signal:                      sig,
        ransomware_ecosystem_scale:  e.ransomware_ecosystem_scale,
        crypto_laundering_volume:    e.crypto_laundering_volume,
      };
    });

    const pc: Record<string, number> = {};
    const rc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tComp = 0;

    for (const ent of entities) {
      pc[ent.crime_pattern]      = (pc[ent.crime_pattern]      || 0) + 1;
      rc[ent.risk_level]         = (rc[ent.risk_level]         || 0) + 1;
      sc[ent.severity]           = (sc[ent.severity]           || 0) + 1;
      ac[ent.recommended_action] = (ac[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
    }

    const n = entities.length;
    const avgComp = tComp / n;

    return NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id:                        384,
        module_name:                      "Dark Web Economy & Underground Market Intelligence Engine",
        total:                            n,
        critical:                         rc["critical"]  || 0,
        high:                             rc["high"]      || 0,
        moderate:                         rc["moderate"]  || 0,
        low:                              rc["low"]       || 0,
        avg_composite:                    Math.round(avgComp * 100) / 100,
        pattern_distribution:             pc,
        risk_distribution:                rc,
        severity_distribution:            sc,
        action_distribution:              ac,
        avg_estimated_darkweb_risk_index: Math.round(avgComp / 100 * 10 * 100) / 100,
      },
    } as Record<string, unknown>, "dark-web-economy-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/dark-web-economy-engine`);
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return NextResponse.json(sealResponse(await upstream.json() as Record<string, unknown>, "dark-web-economy-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "SWARM_API_URL upstream error" } as Record<string, unknown>, "dark-web-economy-engine"),
      { status: 502 }
    );
  }
}
