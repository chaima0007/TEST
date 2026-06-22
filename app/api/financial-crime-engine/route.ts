import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// ── Module 352 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// Anti-Money Laundering & Financial Crime Intelligence Engine
// 8 entities covering all 5 crime patterns and all 4 risk levels.

const MOCK_ENTITIES = [
  // FCE-001 — EMEA, offshore_banking → critical, systemic_laundering_network
  // money_laundering_volume_index≥0.70 AND shell_company_opacity_level≥0.65 → systemic_laundering_network
  // composite≥60 → critical
  {
    id: "FCE-001", financial_sector: "offshore_banking", region: "EMEA",
    money_laundering_volume_index: 0.85,           correspondent_banking_vulnerability: 0.78,
    shell_company_opacity_level: 0.82,             crypto_crime_laundering_integration: 0.60,
    trade_based_money_laundering_rate: 0.72,       real_estate_laundering_density: 0.75,
    beneficial_ownership_opacity: 0.80,            AML_enforcement_weakness_index: 0.72,
    financial_intelligence_gap: 0.68,              kleptocracy_asset_repatriation_failure: 0.60,
    state_sponsored_financial_crime_level: 0.55,   offshore_secrecy_exploitation: 0.70,
    sanction_evasion_sophistication: 0.65,         narco_financial_integration: 0.60,
    terrorist_financing_detection_gap: 0.58,       professional_enabler_complicity_rate: 0.60,
    regulatory_arbitrage_financial_crime: 0.72,
  },
  // FCE-002 — APAC, retail_banking → low, none
  // All low values → composite<20, no pattern triggered
  {
    id: "FCE-002", financial_sector: "retail_banking", region: "APAC",
    money_laundering_volume_index: 0.08,           correspondent_banking_vulnerability: 0.10,
    shell_company_opacity_level: 0.08,             crypto_crime_laundering_integration: 0.10,
    trade_based_money_laundering_rate: 0.08,       real_estate_laundering_density: 0.10,
    beneficial_ownership_opacity: 0.08,            AML_enforcement_weakness_index: 0.10,
    financial_intelligence_gap: 0.08,              kleptocracy_asset_repatriation_failure: 0.08,
    state_sponsored_financial_crime_level: 0.08,   offshore_secrecy_exploitation: 0.08,
    sanction_evasion_sophistication: 0.08,         narco_financial_integration: 0.08,
    terrorist_financing_detection_gap: 0.08,       professional_enabler_complicity_rate: 0.08,
    regulatory_arbitrage_financial_crime: 0.08,
  },
  // FCE-003 — MEA, correspondent_banking → high, sanction_evasion_empire
  // sanction_evasion_sophistication≥0.70 AND offshore_secrecy_exploitation≥0.65 → sanction_evasion_empire
  // money_laundering_volume_index=0.45<0.70 → avoids systemic_laundering_network
  // composite in [40,60) → high
  {
    id: "FCE-003", financial_sector: "correspondent_banking", region: "MEA",
    money_laundering_volume_index: 0.45,           correspondent_banking_vulnerability: 0.55,
    shell_company_opacity_level: 0.48,             crypto_crime_laundering_integration: 0.40,
    trade_based_money_laundering_rate: 0.42,       real_estate_laundering_density: 0.40,
    beneficial_ownership_opacity: 0.52,            AML_enforcement_weakness_index: 0.50,
    financial_intelligence_gap: 0.48,              kleptocracy_asset_repatriation_failure: 0.42,
    state_sponsored_financial_crime_level: 0.40,   offshore_secrecy_exploitation: 0.75,
    sanction_evasion_sophistication: 0.80,         narco_financial_integration: 0.38,
    terrorist_financing_detection_gap: 0.40,       professional_enabler_complicity_rate: 0.42,
    regulatory_arbitrage_financial_crime: 0.50,
  },
  // FCE-004 — LATAM, microfinance → low, none
  // All low values → composite<20, no pattern triggered
  {
    id: "FCE-004", financial_sector: "microfinance", region: "LATAM",
    money_laundering_volume_index: 0.10,           correspondent_banking_vulnerability: 0.08,
    shell_company_opacity_level: 0.08,             crypto_crime_laundering_integration: 0.10,
    trade_based_money_laundering_rate: 0.10,       real_estate_laundering_density: 0.08,
    beneficial_ownership_opacity: 0.10,            AML_enforcement_weakness_index: 0.08,
    financial_intelligence_gap: 0.10,              kleptocracy_asset_repatriation_failure: 0.08,
    state_sponsored_financial_crime_level: 0.08,   offshore_secrecy_exploitation: 0.10,
    sanction_evasion_sophistication: 0.08,         narco_financial_integration: 0.10,
    terrorist_financing_detection_gap: 0.08,       professional_enabler_complicity_rate: 0.10,
    regulatory_arbitrage_financial_crime: 0.08,
  },
  // FCE-005 — EMEA, state_finance → critical, kleptocracy_financial_system
  // kleptocracy_asset_repatriation_failure≥0.70 AND state_sponsored_financial_crime_level≥0.65 → kleptocracy_financial_system
  // money_laundering_volume_index=0.60<0.70 → avoids systemic_laundering_network
  // sanction_evasion_sophistication=0.55<0.70 → avoids sanction_evasion_empire
  // composite≥60 → critical
  {
    id: "FCE-005", financial_sector: "state_finance", region: "EMEA",
    money_laundering_volume_index: 0.60,           correspondent_banking_vulnerability: 0.72,
    shell_company_opacity_level: 0.65,             crypto_crime_laundering_integration: 0.55,
    trade_based_money_laundering_rate: 0.68,       real_estate_laundering_density: 0.70,
    beneficial_ownership_opacity: 0.75,            AML_enforcement_weakness_index: 0.78,
    financial_intelligence_gap: 0.72,              kleptocracy_asset_repatriation_failure: 0.85,
    state_sponsored_financial_crime_level: 0.80,   offshore_secrecy_exploitation: 0.60,
    sanction_evasion_sophistication: 0.55,         narco_financial_integration: 0.65,
    terrorist_financing_detection_gap: 0.60,       professional_enabler_complicity_rate: 0.58,
    regulatory_arbitrage_financial_crime: 0.70,
  },
  // FCE-006 — NOAM, insurance → moderate, none
  // composite in [20,40), no pattern triggered
  {
    id: "FCE-006", financial_sector: "insurance", region: "NOAM",
    money_laundering_volume_index: 0.28,           correspondent_banking_vulnerability: 0.30,
    shell_company_opacity_level: 0.25,             crypto_crime_laundering_integration: 0.22,
    trade_based_money_laundering_rate: 0.28,       real_estate_laundering_density: 0.25,
    beneficial_ownership_opacity: 0.30,            AML_enforcement_weakness_index: 0.28,
    financial_intelligence_gap: 0.25,              kleptocracy_asset_repatriation_failure: 0.22,
    state_sponsored_financial_crime_level: 0.20,   offshore_secrecy_exploitation: 0.25,
    sanction_evasion_sophistication: 0.28,         narco_financial_integration: 0.22,
    terrorist_financing_detection_gap: 0.25,       professional_enabler_complicity_rate: 0.28,
    regulatory_arbitrage_financial_crime: 0.25,
  },
  // FCE-007 — APAC, crypto_exchange → high, crypto_crime_integration
  // crypto_crime_laundering_integration≥0.70 AND AML_enforcement_weakness_index≥0.65 → crypto_crime_integration
  // money_laundering_volume_index=0.50<0.70 → avoids systemic_laundering_network
  // sanction_evasion_sophistication=0.48<0.70 → avoids sanction_evasion_empire
  // kleptocracy_asset_repatriation_failure=0.40<0.70 → avoids kleptocracy_financial_system
  // composite in [40,60) → high
  {
    id: "FCE-007", financial_sector: "crypto_exchange", region: "APAC",
    money_laundering_volume_index: 0.50,           correspondent_banking_vulnerability: 0.48,
    shell_company_opacity_level: 0.45,             crypto_crime_laundering_integration: 0.82,
    trade_based_money_laundering_rate: 0.45,       real_estate_laundering_density: 0.42,
    beneficial_ownership_opacity: 0.55,            AML_enforcement_weakness_index: 0.78,
    financial_intelligence_gap: 0.60,              kleptocracy_asset_repatriation_failure: 0.40,
    state_sponsored_financial_crime_level: 0.38,   offshore_secrecy_exploitation: 0.50,
    sanction_evasion_sophistication: 0.48,         narco_financial_integration: 0.40,
    terrorist_financing_detection_gap: 0.55,       professional_enabler_complicity_rate: 0.45,
    regulatory_arbitrage_financial_crime: 0.52,
  },
  // FCE-008 — LATAM, law_firm_trust → critical, professional_complicity_network
  // professional_enabler_complicity_rate≥0.70 AND beneficial_ownership_opacity≥0.65 → professional_complicity_network
  // money_laundering_volume_index=0.60<0.70 → avoids systemic_laundering_network
  // sanction_evasion_sophistication=0.55<0.70 → avoids sanction_evasion_empire
  // kleptocracy_asset_repatriation_failure=0.55<0.70 → avoids kleptocracy_financial_system
  // crypto_crime_laundering_integration=0.55<0.70 → avoids crypto_crime_integration
  // composite≥60 → critical
  {
    id: "FCE-008", financial_sector: "law_firm_trust", region: "LATAM",
    money_laundering_volume_index: 0.60,           correspondent_banking_vulnerability: 0.72,
    shell_company_opacity_level: 0.62,             crypto_crime_laundering_integration: 0.55,
    trade_based_money_laundering_rate: 0.70,       real_estate_laundering_density: 0.68,
    beneficial_ownership_opacity: 0.82,            AML_enforcement_weakness_index: 0.75,
    financial_intelligence_gap: 0.70,              kleptocracy_asset_repatriation_failure: 0.55,
    state_sponsored_financial_crime_level: 0.50,   offshore_secrecy_exploitation: 0.65,
    sanction_evasion_sophistication: 0.55,         narco_financial_integration: 0.72,
    terrorist_financing_detection_gap: 0.65,       professional_enabler_complicity_rate: 0.85,
    regulatory_arbitrage_financial_crime: 0.72,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

// ── Scoring functions (mirrors Python engine exactly) ──────────────────────────

function launderingScore(e: Entity): number {
  return Math.round((e.money_laundering_volume_index * 0.4 + e.shell_company_opacity_level * 0.35 + e.real_estate_laundering_density * 0.25) * 100 * 100) / 100;
}

function evasionScore(e: Entity): number {
  return Math.round((e.sanction_evasion_sophistication * 0.4 + e.offshore_secrecy_exploitation * 0.35 + e.regulatory_arbitrage_financial_crime * 0.25) * 100 * 100) / 100;
}

function opacityScore(e: Entity): number {
  return Math.round((e.beneficial_ownership_opacity * 0.4 + e.correspondent_banking_vulnerability * 0.35 + e.trade_based_money_laundering_rate * 0.25) * 100 * 100) / 100;
}

function governanceScore(e: Entity): number {
  return Math.round((e.AML_enforcement_weakness_index * 0.4 + e.financial_intelligence_gap * 0.35 + e.kleptocracy_asset_repatriation_failure * 0.25) * 100 * 100) / 100;
}

function compositeScore(lau: number, eva: number, opa: number, gov: number): number {
  return Math.round((lau * 0.30 + eva * 0.25 + opa * 0.25 + gov * 0.20) * 100) / 100;
}

function crimeRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function crimePattern(e: Entity): string {
  if (e.money_laundering_volume_index >= 0.70 && e.shell_company_opacity_level >= 0.65) return "systemic_laundering_network";
  if (e.sanction_evasion_sophistication >= 0.70 && e.offshore_secrecy_exploitation >= 0.65) return "sanction_evasion_empire";
  if (e.kleptocracy_asset_repatriation_failure >= 0.70 && e.state_sponsored_financial_crime_level >= 0.65) return "kleptocracy_financial_system";
  if (e.crypto_crime_laundering_integration >= 0.70 && e.AML_enforcement_weakness_index >= 0.65) return "crypto_crime_integration";
  if (e.professional_enabler_complicity_rate >= 0.70 && e.beneficial_ownership_opacity >= 0.65) return "professional_complicity_network";
  return "none";
}

function crimeSeverity(risk: string): string {
  if (risk === "critical") return "crime_financier_systémique";
  if (risk === "high")     return "réseau_criminel_financier_majeur";
  if (risk === "moderate") return "vulnérabilité_financière_structurelle";
  return "risque_crime_financier_contenu";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "intervention_AML_urgente";
  if (risk === "high")     return "démantèlement_réseau_financier_criminel";
  if (risk === "moderate") return "renforcement_compliance_AML_systémique";
  return "veille_crime_financier_continue";
}

function crimeSignal(risk: string): string {
  const signals: Record<string, string> = {
    critical: "🔴 Crime financier systémique — blanchiment à grande échelle",
    high:     "🟠 Réseau criminel financier majeur détecté",
    moderate: "🟡 Vulnérabilité financière structurelle active",
    low:      "🟢 Risque crime financier contenu et surveillé",
  };
  return signals[risk] ?? "Statut inconnu";
}

// ── GET handler ────────────────────────────────────────────────────────────────

export async function GET() {
  if (!process.env.SWARM_API_URL) {
  console.warn("[financial-crime-engine] SWARM_API_URL non défini — mode dégradé activé");
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

    return sealResponse(NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id:                          352,
        module_name:                        "Anti-Money Laundering & Financial Crime Intelligence Engine",
        total_entities:                     n,
        critical_count:                     rc["critical"]  || 0,
        high_count:                         rc["high"]      || 0,
        moderate_count:                     rc["moderate"]  || 0,
        low_count:                          rc["low"]       || 0,
        avg_composite:                      Math.round(avgComp * 100) / 100,
        pattern_distribution:               pc,
        risk_distribution:                  rc,
        severity_distribution:              sc,
        action_distribution:                ac,
        avg_estimated_financial_crime_index: Math.round(avgComp / 100 * 10 * 100) / 100,
      },
    } as Record<string, unknown>, "financial-crime-engine")));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/financial-crime-engine`, { next: { revalidate: 30 } });
    if (!upstream.ok) throw new Error(`Upstream ${upstream.status}`);
    return sealResponse(NextResponse.json(sealResponse(await upstream.json() as Record<string, unknown>, "financial-crime-engine")));
  } catch {
    return sealResponse(NextResponse.json(
      sealResponse({ error: "SWARM_API_URL upstream error" } as Record<string, unknown>, "financial-crime-engine"),
      { status: 502 }
    ));
  }
}
