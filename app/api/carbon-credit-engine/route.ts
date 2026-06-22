import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

// ─── Math (mirrors Python exactly) ───────────────────────────────────────────

interface CceInput {
  id: string;
  market_type: string;
  region: string;
  fraud_prevalence: number;
  additionality_failure: number;
  permanence_risk: number;
  double_counting_rate: number;
  verification_opacity: number;
  greenwashing_integration: number;
  REDD_collapse_risk: number;
  voluntary_market_manipulation: number;
  corporate_offset_abuse: number;
  regulatory_arbitrage: number;
  biodiversity_credit_fraud: number;
  social_impact_fabrication: number;
  methodology_gaming: number;
  registry_manipulation: number;
  carbon_washing_intensity: number;
  market_concentration: number;
  standard_capture: number;
}

function fraudScore(e: CceInput): number {
  return Math.round((e.fraud_prevalence * 0.40 + e.double_counting_rate * 0.35 + e.additionality_failure * 0.25) * 100 * 100) / 100;
}

function greenwashScore(e: CceInput): number {
  return Math.round((e.greenwashing_integration * 0.40 + e.corporate_offset_abuse * 0.35 + e.carbon_washing_intensity * 0.25) * 100 * 100) / 100;
}

function systemicScore(e: CceInput): number {
  return Math.round((e.REDD_collapse_risk * 0.40 + e.permanence_risk * 0.35 + e.biodiversity_credit_fraud * 0.25) * 100 * 100) / 100;
}

function manipulationScore(e: CceInput): number {
  return Math.round((e.voluntary_market_manipulation * 0.40 + e.market_concentration * 0.35 + e.registry_manipulation * 0.25) * 100 * 100) / 100;
}

function compositeScore(fr: number, gw: number, sy: number, mn: number): number {
  return Math.round((fr * 0.30 + gw * 0.25 + sy * 0.25 + mn * 0.20) * 100) / 100;
}

function carbonCreditPattern(e: CceInput): string {
  if (e.fraud_prevalence > 0.85 && e.double_counting_rate > 0.80) return "systematic_carbon_fraud";
  if (e.REDD_collapse_risk > 0.85 && e.additionality_failure > 0.80) return "REDD_ecosystem_collapse";
  if (e.greenwashing_integration > 0.85 && e.corporate_offset_abuse > 0.80) return "corporate_greenwashing_empire";
  if (e.voluntary_market_manipulation > 0.80 && e.market_concentration > 0.75) return "market_manipulation_capture";
  if (e.standard_capture > 0.80 && e.registry_manipulation > 0.75) return "standard_regulatory_capture";
  return "none";
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function severity(risk: string): string {
  const m: Record<string, string> = {
    critical: "crise_fraude_carbone_systémique",
    high:     "risque_manipulation_marché_carbone_majeur",
    moderate: "fragilité_intégrité_crédit_carbone_structurelle",
    low:      "marché_carbone_sous_surveillance",
  };
  return m[risk] ?? risk;
}

function recommendedAction(risk: string): string {
  const m: Record<string, string> = {
    critical: "intervention_fraude_carbone_urgente",
    high:     "audit_marché_carbone_accéléré",
    moderate: "renforcement_vérification_crédit_carbone",
    low:      "veille_marché_carbone_continue",
  };
  return m[risk] ?? risk;
}

function signal(risk: string): string {
  const m: Record<string, string> = {
    critical: "🔴 Crise fraude carbone systémique — intégrité marchés climatiques compromise",
    high:     "🟠 Risque manipulation marché carbone majeur détecté",
    moderate: "🟡 Fragilité intégrité crédit carbone structurelle active",
    low:      "🟢 Marché carbone sous surveillance",
  };
  return m[risk] ?? risk;
}

function analyzeEntity(e: CceInput) {
  const fr  = fraudScore(e);
  const gw  = greenwashScore(e);
  const sy  = systemicScore(e);
  const mn  = manipulationScore(e);
  const comp = compositeScore(fr, gw, sy, mn);
  const pat  = carbonCreditPattern(e);
  const risk = riskLevel(comp);
  const sev  = severity(risk);
  const action = recommendedAction(risk);
  const sig  = signal(risk);

  return {
    id:                e.entity_id,
    market_type:              e.market_type,
    region:                   e.region,
    fraud_score:              fr,
    greenwash_score:          gw,
    systemic_score:           sy,
    manipulation_score:       mn,
    composite_score:          comp,
    risk_level:               risk,
    carbon_credit_pattern:    pat,
    severity:                 sev,
    recommended_action:       action,
    signal:                   sig,
    fraud_prevalence:         e.fraud_prevalence,
    greenwashing_integration: e.greenwashing_integration,
  };
}

// ─── Mock entities ────────────────────────────────────────────────────────────

const mockEntities = (() => {
  // CCE-001: critical + systematic_carbon_fraud
  // fraud_prevalence=0.90>0.85, double_counting_rate=0.85>0.80 → systematic_carbon_fraud
  // fraud=(0.90*0.4+0.85*0.35+0.80*0.25)*100=85.75
  // greenwash=(0.80*0.4+0.78*0.35+0.75*0.25)*100=78.05
  // systemic=(0.75*0.4+0.72*0.35+0.70*0.25)*100=72.70
  // manipulation=(0.72*0.4+0.70*0.35+0.68*0.25)*100=70.30
  // composite=85.75*0.30+78.05*0.25+72.70*0.25+70.30*0.20=25.725+19.5125+18.175+14.06=77.47 → critical
  const e1 = analyzeEntity({
    id: "CCE-001", market_type: "voluntary_carbon_market", region: "GLOBAL",
    fraud_prevalence: 0.90, additionality_failure: 0.80, permanence_risk: 0.72,
    double_counting_rate: 0.85, verification_opacity: 0.82, greenwashing_integration: 0.80,
    REDD_collapse_risk: 0.75, voluntary_market_manipulation: 0.72, corporate_offset_abuse: 0.78,
    regulatory_arbitrage: 0.70, biodiversity_credit_fraud: 0.70, social_impact_fabrication: 0.68,
    methodology_gaming: 0.75, registry_manipulation: 0.68, carbon_washing_intensity: 0.75,
    market_concentration: 0.70, standard_capture: 0.72,
  });

  // CCE-002: low + none
  // All values ~0.10-0.15 → composite ~12 → low
  const e2 = analyzeEntity({
    id: "CCE-002", market_type: "compliance_market", region: "EU",
    fraud_prevalence: 0.10, additionality_failure: 0.12, permanence_risk: 0.11,
    double_counting_rate: 0.10, verification_opacity: 0.12, greenwashing_integration: 0.10,
    REDD_collapse_risk: 0.11, voluntary_market_manipulation: 0.10, corporate_offset_abuse: 0.12,
    regulatory_arbitrage: 0.10, biodiversity_credit_fraud: 0.11, social_impact_fabrication: 0.10,
    methodology_gaming: 0.12, registry_manipulation: 0.10, carbon_washing_intensity: 0.11,
    market_concentration: 0.10, standard_capture: 0.11,
  });

  // CCE-003: critical + REDD_ecosystem_collapse
  // REDD_collapse_risk=0.90>0.85, additionality_failure=0.85>0.80 → REDD_ecosystem_collapse
  // fraud_prevalence=0.70≤0.85 → no pattern 1
  // fraud=(0.70*0.4+0.65*0.35+0.85*0.25)*100=72.00
  // greenwash=(0.72*0.4+0.70*0.35+0.68*0.25)*100=70.30
  // systemic=(0.90*0.4+0.80*0.35+0.75*0.25)*100=82.75
  // manipulation=(0.68*0.4+0.65*0.35+0.62*0.25)*100=65.45
  // composite=72.00*0.30+70.30*0.25+82.75*0.25+65.45*0.20=21.60+17.575+20.6875+13.09=72.95 → critical
  const e3 = analyzeEntity({
    id: "CCE-003", market_type: "REDD_plus", region: "AMAZONIA",
    fraud_prevalence: 0.70, additionality_failure: 0.85, permanence_risk: 0.80,
    double_counting_rate: 0.65, verification_opacity: 0.78, greenwashing_integration: 0.72,
    REDD_collapse_risk: 0.90, voluntary_market_manipulation: 0.68, corporate_offset_abuse: 0.70,
    regulatory_arbitrage: 0.65, biodiversity_credit_fraud: 0.75, social_impact_fabrication: 0.72,
    methodology_gaming: 0.70, registry_manipulation: 0.62, carbon_washing_intensity: 0.68,
    market_concentration: 0.65, standard_capture: 0.60,
  });

  // CCE-004: high + corporate_greenwashing_empire
  // greenwashing_integration=0.90>0.85, corporate_offset_abuse=0.85>0.80 → corporate_greenwashing_empire
  // fraud_prevalence=0.50≤0.85, REDD_collapse_risk=0.50≤0.85 → no patterns 1-2
  // fraud=(0.50*0.4+0.45*0.35+0.45*0.25)*100=47.00
  // greenwash=(0.90*0.4+0.85*0.35+0.72*0.25)*100=83.75
  // systemic=(0.50*0.4+0.48*0.35+0.48*0.25)*100=48.80
  // manipulation=(0.50*0.4+0.48*0.35+0.45*0.25)*100=48.05
  // composite=47.00*0.30+83.75*0.25+48.80*0.25+48.05*0.20=14.10+20.9375+12.20+9.61=56.85 → high
  const e4 = analyzeEntity({
    id: "CCE-004", market_type: "corporate_offset", region: "NAMER",
    fraud_prevalence: 0.50, additionality_failure: 0.45, permanence_risk: 0.48,
    double_counting_rate: 0.45, verification_opacity: 0.52, greenwashing_integration: 0.90,
    REDD_collapse_risk: 0.50, voluntary_market_manipulation: 0.50, corporate_offset_abuse: 0.85,
    regulatory_arbitrage: 0.52, biodiversity_credit_fraud: 0.48, social_impact_fabrication: 0.50,
    methodology_gaming: 0.55, registry_manipulation: 0.45, carbon_washing_intensity: 0.72,
    market_concentration: 0.48, standard_capture: 0.50,
  });

  // CCE-005: critical + market_manipulation_capture
  // voluntary_market_manipulation=0.85>0.80, market_concentration=0.80>0.75 → market_manipulation_capture
  // fraud_prev=0.55≤0.85, REDD=0.55≤0.85, greenwash_int=0.60≤0.85 → no patterns 1-3
  // fraud=(0.55*0.4+0.50*0.35+0.45*0.25)*100=50.75
  // greenwash=(0.60*0.4+0.55*0.35+0.60*0.25)*100=58.25
  // systemic=(0.55*0.4+0.62*0.35+0.58*0.25)*100=58.20
  // manipulation=(0.85*0.4+0.80*0.35+0.70*0.25)*100=79.50
  // composite=50.75*0.30+58.25*0.25+58.20*0.25+79.50*0.20=15.225+14.5625+14.55+15.90=60.24 → critical
  const e5 = analyzeEntity({
    id: "CCE-005", market_type: "voluntary_carbon_market", region: "APAC",
    fraud_prevalence: 0.55, additionality_failure: 0.45, permanence_risk: 0.62,
    double_counting_rate: 0.50, verification_opacity: 0.58, greenwashing_integration: 0.60,
    REDD_collapse_risk: 0.55, voluntary_market_manipulation: 0.85, corporate_offset_abuse: 0.55,
    regulatory_arbitrage: 0.68, biodiversity_credit_fraud: 0.58, social_impact_fabrication: 0.55,
    methodology_gaming: 0.60, registry_manipulation: 0.70, carbon_washing_intensity: 0.60,
    market_concentration: 0.80, standard_capture: 0.65,
  });

  // CCE-006: moderate + none
  // All mid values 0.28-0.38, composite ~31 → moderate
  // fraud=(0.30*0.4+0.28*0.35+0.32*0.25)*100=29.8
  // greenwash=(0.35*0.4+0.32*0.35+0.30*0.25)*100=32.7
  // systemic=(0.32*0.4+0.30*0.35+0.28*0.25)*100=30.5
  // manipulation=(0.35*0.4+0.32*0.35+0.28*0.25)*100=32.2
  // composite=29.8*0.30+32.7*0.25+30.5*0.25+32.2*0.20=8.94+8.175+7.625+6.44=31.18 → moderate
  const e6 = analyzeEntity({
    id: "CCE-006", market_type: "biodiversity_credit", region: "EMEA",
    fraud_prevalence: 0.30, additionality_failure: 0.32, permanence_risk: 0.30,
    double_counting_rate: 0.28, verification_opacity: 0.35, greenwashing_integration: 0.35,
    REDD_collapse_risk: 0.32, voluntary_market_manipulation: 0.35, corporate_offset_abuse: 0.32,
    regulatory_arbitrage: 0.30, biodiversity_credit_fraud: 0.28, social_impact_fabrication: 0.30,
    methodology_gaming: 0.32, registry_manipulation: 0.28, carbon_washing_intensity: 0.30,
    market_concentration: 0.32, standard_capture: 0.30,
  });

  // CCE-007: high + standard_regulatory_capture
  // standard_capture=0.85>0.80, registry_manipulation=0.80>0.75 → standard_regulatory_capture
  // fraud_prev=0.45≤0.85, REDD=0.45≤0.85, greenwash=0.50≤0.85, vol_manip=0.50≤0.80 → no patterns 1-4
  // fraud=(0.45*0.4+0.40*0.35+0.42*0.25)*100=42.50
  // greenwash=(0.50*0.4+0.45*0.35+0.48*0.25)*100=47.75
  // systemic=(0.45*0.4+0.50*0.35+0.48*0.25)*100=47.50
  // manipulation=(0.50*0.4+0.48*0.35+0.80*0.25)*100=56.80
  // composite=42.50*0.30+47.75*0.25+47.50*0.25+56.80*0.20=12.75+11.9375+11.875+11.36=47.92 → high
  const e7 = analyzeEntity({
    id: "CCE-007", market_type: "compliance_market", region: "LATAM",
    fraud_prevalence: 0.45, additionality_failure: 0.42, permanence_risk: 0.50,
    double_counting_rate: 0.40, verification_opacity: 0.48, greenwashing_integration: 0.50,
    REDD_collapse_risk: 0.45, voluntary_market_manipulation: 0.50, corporate_offset_abuse: 0.45,
    regulatory_arbitrage: 0.55, biodiversity_credit_fraud: 0.48, social_impact_fabrication: 0.45,
    methodology_gaming: 0.52, registry_manipulation: 0.80, carbon_washing_intensity: 0.48,
    market_concentration: 0.48, standard_capture: 0.85,
  });

  // CCE-008: low + none
  // All values ~0.12-0.18 → composite ~14 → low
  const e8 = analyzeEntity({
    id: "CCE-008", market_type: "sovereign_carbon", region: "MEA",
    fraud_prevalence: 0.14, additionality_failure: 0.16, permanence_risk: 0.12,
    double_counting_rate: 0.13, verification_opacity: 0.15, greenwashing_integration: 0.14,
    REDD_collapse_risk: 0.12, voluntary_market_manipulation: 0.15, corporate_offset_abuse: 0.13,
    regulatory_arbitrage: 0.14, biodiversity_credit_fraud: 0.12, social_impact_fabrication: 0.13,
    methodology_gaming: 0.15, registry_manipulation: 0.13, carbon_washing_intensity: 0.14,
    market_concentration: 0.12, standard_capture: 0.14,
  });

  return [e1, e2, e3, e4, e5, e6, e7, e8];
})();

// ─── Route handler ────────────────────────────────────────────────────────────

export async function GET(request: Request) {
  if (!process.env.SWARM_API_URL) {
  console.warn("[carbon-credit-engine] SWARM_API_URL non défini — mode dégradé activé");
} = new URL(request.url);
    const risk    = searchParams.get("risk");
    const pattern = searchParams.get("pattern");

    let entities = [...mockEntities];
    if (risk)    entities = entities.filter((e) => e.risk_level === risk);
    if (pattern) entities = entities.filter((e) => e.carbon_credit_pattern === pattern);

    const risk_distribution:     Record<string, number> = {};
    const pattern_distribution:  Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution:   Record<string, number> = {};
    let total_comp        = 0;
    let total_fraud_prev  = 0;

    for (const e of mockEntities) {
      risk_distribution[e.risk_level]             = (risk_distribution[e.risk_level] || 0) + 1;
      pattern_distribution[e.carbon_credit_pattern] = (pattern_distribution[e.carbon_credit_pattern] || 0) + 1;
      severity_distribution[e.severity]           = (severity_distribution[e.severity] || 0) + 1;
      action_distribution[e.recommended_action]   = (action_distribution[e.recommended_action] || 0) + 1;
      total_comp       += e.composite_score;
      total_fraud_prev += e.fraud_prevalence;
    }

    const n = mockEntities.length;
    const avg_composite = Math.round((total_comp / n) * 100) / 100;

    return sealResponse(NextResponse.json(sealResponse({
      entities,
      summary: {
        module_id:                        369,
        module_name:                      "Carbon Credit Market & Climate Finance Fraud Intelligence Engine",
        total:                            n,
        critical:                         mockEntities.filter((e) => e.risk_level === "critical").length,
        high:                             mockEntities.filter((e) => e.risk_level === "high").length,
        moderate:                         mockEntities.filter((e) => e.risk_level === "moderate").length,
        low:                              mockEntities.filter((e) => e.risk_level === "low").length,
        avg_composite,
        distributions:                    pattern_distribution,
        avg_estimated_carbon_fraud_index: Math.round((avg_composite / 100 * 10) * 100) / 100,
        risk_distribution,
        severity_distribution,
        action_distribution,
      },
    } as Record<string, unknown>)));
  }

  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const pattern = searchParams.get("pattern");

  try {
    const url = new URL(`${SWARM_API_URL}/api/carbon-credit-engine`);
    if (risk)    url.searchParams.set("risk",    risk);
    if (pattern) url.searchParams.set("pattern", pattern);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(await res.json()));
  } catch { /* fall through to 502 */ }

  return sealResponse(NextResponse.json(
    sealResponse({ entities: [], summary: {} } as Record<string, unknown>),
    { status: 502 },
  ));
}
