import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// ── Module 386 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// Crypto Exchange & Digital Asset Regulation Intelligence Engine
// 8 entities covering all 5 crypto patterns and all 4 risk levels.

const MOCK_ENTITIES = [
  // CRE-001 — EMEA, centralized_exchange → critical, exchange_collapse_cascade
  // exchange_collapse_risk>0.85 AND contagion_from_collapse>0.80 → exchange_collapse_cascade
  // composite≥60 → critical
  {
    id: "CRE-001", exchange_type: "centralized_exchange", region: "EMEA",
    exchange_collapse_risk: 0.92,          fractional_reserve_crypto: 0.78,
    regulatory_arbitrage_intensity: 0.72,  custody_failure_risk: 0.80,
    market_manipulation_scale: 0.65,       insider_trading_prevalence: 0.60,
    stablecoin_depegging_risk: 0.70,       CBDC_competitive_threat: 0.55,
    AML_compliance_failure: 0.75,          exchange_concentration_risk: 0.68,
    retail_investor_harm: 0.78,            geopolitical_ban_risk: 0.60,
    proof_of_reserve_failure: 0.72,        contagion_from_collapse: 0.88,
    regulatory_fragmentation_global: 0.65, consumer_protection_gap: 0.70,
    crypto_oligopoly_formation: 0.62,
  },
  // CRE-002 — APAC, decentralized_protocol → low, none
  // All low values → composite<20, no pattern triggered
  {
    id: "CRE-002", exchange_type: "decentralized_protocol", region: "APAC",
    exchange_collapse_risk: 0.08,          fractional_reserve_crypto: 0.10,
    regulatory_arbitrage_intensity: 0.08,  custody_failure_risk: 0.10,
    market_manipulation_scale: 0.08,       insider_trading_prevalence: 0.10,
    stablecoin_depegging_risk: 0.08,       CBDC_competitive_threat: 0.10,
    AML_compliance_failure: 0.08,          exchange_concentration_risk: 0.10,
    retail_investor_harm: 0.08,            geopolitical_ban_risk: 0.08,
    proof_of_reserve_failure: 0.08,        contagion_from_collapse: 0.10,
    regulatory_fragmentation_global: 0.08, consumer_protection_gap: 0.08,
    crypto_oligopoly_formation: 0.08,
  },
  // CRE-003 — NOAM, stablecoin_issuer → critical, fractional_reserve_crisis
  // fractional_reserve_crypto>0.85 AND proof_of_reserve_failure>0.80 → fractional_reserve_crisis
  // exchange_collapse_risk=0.60≤0.85 → avoids exchange_collapse_cascade
  // composite≥60 → critical
  {
    id: "CRE-003", exchange_type: "stablecoin_issuer", region: "NOAM",
    exchange_collapse_risk: 0.60,          fractional_reserve_crypto: 0.90,
    regulatory_arbitrage_intensity: 0.75,  custody_failure_risk: 0.72,
    market_manipulation_scale: 0.62,       insider_trading_prevalence: 0.58,
    stablecoin_depegging_risk: 0.82,       CBDC_competitive_threat: 0.65,
    AML_compliance_failure: 0.70,          exchange_concentration_risk: 0.65,
    retail_investor_harm: 0.75,            geopolitical_ban_risk: 0.55,
    proof_of_reserve_failure: 0.86,        contagion_from_collapse: 0.68,
    regulatory_fragmentation_global: 0.62, consumer_protection_gap: 0.68,
    crypto_oligopoly_formation: 0.55,
  },
  // CRE-004 — LATAM, retail_crypto_app → moderate, none
  // composite in [20,40), no pattern triggered
  {
    id: "CRE-004", exchange_type: "retail_crypto_app", region: "LATAM",
    exchange_collapse_risk: 0.28,          fractional_reserve_crypto: 0.25,
    regulatory_arbitrage_intensity: 0.30,  custody_failure_risk: 0.22,
    market_manipulation_scale: 0.28,       insider_trading_prevalence: 0.25,
    stablecoin_depegging_risk: 0.22,       CBDC_competitive_threat: 0.28,
    AML_compliance_failure: 0.30,          exchange_concentration_risk: 0.25,
    retail_investor_harm: 0.28,            geopolitical_ban_risk: 0.22,
    proof_of_reserve_failure: 0.25,        contagion_from_collapse: 0.28,
    regulatory_fragmentation_global: 0.25, consumer_protection_gap: 0.30,
    crypto_oligopoly_formation: 0.22,
  },
  // CRE-005 — MEA, crypto_derivatives_platform → high, market_manipulation_empire
  // market_manipulation_scale>0.85 AND insider_trading_prevalence>0.80 → market_manipulation_empire
  // exchange_collapse_risk=0.55≤0.85 → avoids exchange_collapse_cascade
  // fractional_reserve_crypto=0.50≤0.85 → avoids fractional_reserve_crisis
  // composite in [40,60) → high
  {
    id: "CRE-005", exchange_type: "crypto_derivatives_platform", region: "MEA",
    exchange_collapse_risk: 0.55,          fractional_reserve_crypto: 0.50,
    regulatory_arbitrage_intensity: 0.48,  custody_failure_risk: 0.45,
    market_manipulation_scale: 0.88,       insider_trading_prevalence: 0.84,
    stablecoin_depegging_risk: 0.40,       CBDC_competitive_threat: 0.38,
    AML_compliance_failure: 0.45,          exchange_concentration_risk: 0.42,
    retail_investor_harm: 0.55,            geopolitical_ban_risk: 0.38,
    proof_of_reserve_failure: 0.40,        contagion_from_collapse: 0.50,
    regulatory_fragmentation_global: 0.42, consumer_protection_gap: 0.48,
    crypto_oligopoly_formation: 0.40,
  },
  // CRE-006 — APAC, crypto_lending_platform → low, none
  // All low values → composite<20, no pattern triggered
  {
    id: "CRE-006", exchange_type: "crypto_lending_platform", region: "APAC",
    exchange_collapse_risk: 0.10,          fractional_reserve_crypto: 0.08,
    regulatory_arbitrage_intensity: 0.10,  custody_failure_risk: 0.08,
    market_manipulation_scale: 0.10,       insider_trading_prevalence: 0.08,
    stablecoin_depegging_risk: 0.10,       CBDC_competitive_threat: 0.08,
    AML_compliance_failure: 0.10,          exchange_concentration_risk: 0.08,
    retail_investor_harm: 0.10,            geopolitical_ban_risk: 0.10,
    proof_of_reserve_failure: 0.08,        contagion_from_collapse: 0.10,
    regulatory_fragmentation_global: 0.10, consumer_protection_gap: 0.08,
    crypto_oligopoly_formation: 0.10,
  },
  // CRE-007 — EMEA, crypto_mining_conglomerate → high, regulatory_ban_extermination
  // geopolitical_ban_risk>0.80 AND regulatory_fragmentation_global>0.75 → regulatory_ban_extermination
  // exchange_collapse_risk=0.45≤0.85 → avoids exchange_collapse_cascade
  // fractional_reserve_crypto=0.42≤0.85 → avoids fractional_reserve_crisis
  // market_manipulation_scale=0.50≤0.85 → avoids market_manipulation_empire
  // composite in [40,60) → high
  {
    id: "CRE-007", exchange_type: "crypto_mining_conglomerate", region: "EMEA",
    exchange_collapse_risk: 0.45,          fractional_reserve_crypto: 0.42,
    regulatory_arbitrage_intensity: 0.65,  custody_failure_risk: 0.42,
    market_manipulation_scale: 0.50,       insider_trading_prevalence: 0.45,
    stablecoin_depegging_risk: 0.38,       CBDC_competitive_threat: 0.42,
    AML_compliance_failure: 0.55,          exchange_concentration_risk: 0.60,
    retail_investor_harm: 0.50,            geopolitical_ban_risk: 0.85,
    proof_of_reserve_failure: 0.40,        contagion_from_collapse: 0.48,
    regulatory_fragmentation_global: 0.80, consumer_protection_gap: 0.55,
    crypto_oligopoly_formation: 0.58,
  },
  // CRE-008 — NOAM, crypto_market_maker → critical, crypto_oligopoly_capture
  // crypto_oligopoly_formation>0.80 AND exchange_concentration_risk>0.75 → crypto_oligopoly_capture
  // exchange_collapse_risk=0.62≤0.85 → avoids exchange_collapse_cascade
  // fractional_reserve_crypto=0.58≤0.85 → avoids fractional_reserve_crisis
  // market_manipulation_scale=0.60≤0.85 → avoids market_manipulation_empire
  // geopolitical_ban_risk=0.55≤0.80 → avoids regulatory_ban_extermination
  // composite≥60 → critical
  {
    id: "CRE-008", exchange_type: "crypto_market_maker", region: "NOAM",
    exchange_collapse_risk: 0.62,          fractional_reserve_crypto: 0.58,
    regulatory_arbitrage_intensity: 0.70,  custody_failure_risk: 0.65,
    market_manipulation_scale: 0.60,       insider_trading_prevalence: 0.55,
    stablecoin_depegging_risk: 0.50,       CBDC_competitive_threat: 0.55,
    AML_compliance_failure: 0.72,          exchange_concentration_risk: 0.80,
    retail_investor_harm: 0.72,            geopolitical_ban_risk: 0.55,
    proof_of_reserve_failure: 0.60,        contagion_from_collapse: 0.65,
    regulatory_fragmentation_global: 0.68, consumer_protection_gap: 0.75,
    crypto_oligopoly_formation: 0.84,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

// ── Scoring functions (mirrors Python engine exactly) ──────────────────────────

function collapseScore(e: Entity): number {
  return Math.round((e.exchange_collapse_risk * 0.40 + e.fractional_reserve_crypto * 0.35 + e.custody_failure_risk * 0.25) * 100 * 100) / 100;
}

function manipulationScore(e: Entity): number {
  return Math.round((e.market_manipulation_scale * 0.40 + e.insider_trading_prevalence * 0.35 + e.retail_investor_harm * 0.25) * 100 * 100) / 100;
}

function regulatoryScore(e: Entity): number {
  return Math.round((e.AML_compliance_failure * 0.40 + e.regulatory_arbitrage_intensity * 0.35 + e.regulatory_fragmentation_global * 0.25) * 100 * 100) / 100;
}

function concentrationScore(e: Entity): number {
  return Math.round((e.exchange_concentration_risk * 0.40 + e.crypto_oligopoly_formation * 0.35 + e.consumer_protection_gap * 0.25) * 100 * 100) / 100;
}

function compositeScore(col: number, man: number, reg: number, con: number): number {
  return Math.round((col * 0.30 + man * 0.25 + reg * 0.25 + con * 0.20) * 100) / 100;
}

function cryptoRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function cryptoPattern(e: Entity): string {
  if (e.exchange_collapse_risk > 0.85 && e.contagion_from_collapse > 0.80)            return "exchange_collapse_cascade";
  if (e.fractional_reserve_crypto > 0.85 && e.proof_of_reserve_failure > 0.80)        return "fractional_reserve_crisis";
  if (e.market_manipulation_scale > 0.85 && e.insider_trading_prevalence > 0.80)      return "market_manipulation_empire";
  if (e.geopolitical_ban_risk > 0.80 && e.regulatory_fragmentation_global > 0.75)     return "regulatory_ban_extermination";
  if (e.crypto_oligopoly_formation > 0.80 && e.exchange_concentration_risk > 0.75)    return "crypto_oligopoly_capture";
  return "none";
}

function cryptoSeverity(risk: string): string {
  if (risk === "critical") return "effondrement_crypto_systémique";
  if (risk === "high")     return "crise_réglementaire_crypto_majeure";
  if (risk === "moderate") return "vulnérabilité_structurelle_crypto";
  return "risque_crypto_contenu";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_réglementaire_urgente_crypto";
  if (risk === "high")     return "supervision_renforcée_exchange_crypto";
  if (risk === "moderate") return "audit_conformité_actifs_numériques";
  return "veille_réglementaire_crypto_continue";
}

function cryptoSignal(risk: string): string {
  const signals: Record<string, string> = {
    critical: "🔴 Effondrement crypto systémique — risque contagion majeur",
    high:     "🟠 Crise réglementaire crypto majeure détectée",
    moderate: "🟡 Vulnérabilité structurelle crypto active",
    low:      "🟢 Risque crypto contenu et surveillé",
  };
  return signals[risk] ?? "Statut inconnu";
}

// ── GET handler ────────────────────────────────────────────────────────────────

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[crypto-regulation-engine] SWARM_API_URL non défini — mode dégradé activé");
};
    });

    const pc: Record<string, number> = {};
    const rc: Record<string, number> = {};
    const sc: Record<string, number> = {};
    const ac: Record<string, number> = {};
    let tComp = 0, tCol = 0, tMan = 0, tReg = 0;

    for (const ent of entities) {
      pc[ent.crypto_pattern]      = (pc[ent.crypto_pattern]      || 0) + 1;
      rc[ent.risk_level]          = (rc[ent.risk_level]          || 0) + 1;
      sc[ent.severity]            = (sc[ent.severity]            || 0) + 1;
      ac[ent.recommended_action]  = (ac[ent.recommended_action]  || 0) + 1;
      tComp += ent.composite_score;
      tCol  += ent.collapse_score;
      tMan  += ent.manipulation_score;
      tReg  += ent.regulatory_score;
    }

    const n = entities.length;
    const avgComp = tComp / n;
    const avgCol  = tCol  / n;
    const avgMan  = tMan  / n;
    const avgReg  = tReg  / n;

    return sealResponse(NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id:                             386,
        module_name:                           "Crypto Exchange & Digital Asset Regulation Intelligence Engine",
        total:                                 n,
        critical:                              rc["critical"]  || 0,
        high:                                  rc["high"]      || 0,
        moderate:                              rc["moderate"]  || 0,
        low:                                   rc["low"]       || 0,
        avg_composite:                         Math.round(avgComp * 100) / 100,
        distributions: {
          pattern:   pc,
          risk:      rc,
          severity:  sc,
          action:    ac,
        },
        avg_estimated_crypto_regulatory_index: Math.round(avgComp / 100 * 10 * 100) / 100,
        avg_collapse_score:                    Math.round(avgCol  * 100) / 100,
        avg_manipulation_score:                Math.round(avgMan  * 100) / 100,
        avg_regulatory_score:                  Math.round(avgReg  * 100) / 100,
      },
    } as Record<string, unknown>, "crypto-regulation-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/crypto-regulation-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return sealResponse(NextResponse.json(sealResponse(await upstream.json() as Record<string, unknown>, "crypto-regulation-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "SWARM_API_URL upstream error" } as Record<string, unknown>, "crypto-regulation-engine"),
      { status: 502 }
    ));
  }
}
