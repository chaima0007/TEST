import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  // SWARM_API_URL guard — will use mock data below
}

const MOCK_ENTITIES = [
  // CPE-001 — critical, pattern=regulatory_capture_complete
  // regulatory_capture_complete: regulatory_capture_depth>=0.70 AND agency_capture_prevalence>=0.65
  // composite >=60 → critical
  {
    id: "CPE-001", industry_sector: "financial_services", region: "NOAM",
    regulatory_capture_depth: 0.88,
    lobbying_expenditure_ratio: 0.72,
    revolving_door_intensity: 0.65,
    market_concentration_index: 0.60,
    antitrust_enforcement_weakness: 0.58,
    tax_arbitrage_sophistication: 0.70,
    regulatory_arbitrage_exploitation: 0.68,
    corporate_sovereignty_over_state: 0.62,
    standard_setting_capture: 0.55,
    judicial_capture_risk: 0.65,
    legislative_capture_index: 0.75,
    agency_capture_prevalence: 0.82,
    dark_money_political_influence: 0.60,
    patent_system_weaponization: 0.55,
    regulatory_complexity_weaponization: 0.58,
    state_aid_capture_mechanism: 0.60,
    private_enforcement_substitution: 0.52,
  },
  // CPE-002 — low, pattern=none
  // composite < 20 → low; no pattern triggers
  {
    id: "CPE-002", industry_sector: "local_retail", region: "EMEA",
    regulatory_capture_depth: 0.10,
    lobbying_expenditure_ratio: 0.08,
    revolving_door_intensity: 0.10,
    market_concentration_index: 0.12,
    antitrust_enforcement_weakness: 0.10,
    tax_arbitrage_sophistication: 0.08,
    regulatory_arbitrage_exploitation: 0.10,
    corporate_sovereignty_over_state: 0.08,
    standard_setting_capture: 0.10,
    judicial_capture_risk: 0.08,
    legislative_capture_index: 0.10,
    agency_capture_prevalence: 0.10,
    dark_money_political_influence: 0.08,
    patent_system_weaponization: 0.10,
    regulatory_complexity_weaponization: 0.08,
    state_aid_capture_mechanism: 0.10,
    private_enforcement_substitution: 0.08,
  },
  // CPE-003 — high, pattern=antitrust_collapse
  // antitrust_collapse: market_concentration_index>=0.70 AND antitrust_enforcement_weakness>=0.65
  // regulatory_capture_complete must NOT fire: regulatory_capture_depth<0.70 OR agency_capture_prevalence<0.65
  // composite >=40 and <60 → high
  {
    id: "CPE-003", industry_sector: "big_tech", region: "APAC",
    regulatory_capture_depth: 0.50,
    lobbying_expenditure_ratio: 0.55,
    revolving_door_intensity: 0.48,
    market_concentration_index: 0.82,
    antitrust_enforcement_weakness: 0.78,
    tax_arbitrage_sophistication: 0.45,
    regulatory_arbitrage_exploitation: 0.42,
    corporate_sovereignty_over_state: 0.40,
    standard_setting_capture: 0.45,
    judicial_capture_risk: 0.48,
    legislative_capture_index: 0.42,
    agency_capture_prevalence: 0.45,
    dark_money_political_influence: 0.38,
    patent_system_weaponization: 0.55,
    regulatory_complexity_weaponization: 0.40,
    state_aid_capture_mechanism: 0.38,
    private_enforcement_substitution: 0.42,
  },
  // CPE-004 — low, pattern=none
  // composite < 20 → low; no pattern triggers
  {
    id: "CPE-004", industry_sector: "cooperative_farming", region: "LATAM",
    regulatory_capture_depth: 0.12,
    lobbying_expenditure_ratio: 0.10,
    revolving_door_intensity: 0.08,
    market_concentration_index: 0.10,
    antitrust_enforcement_weakness: 0.10,
    tax_arbitrage_sophistication: 0.08,
    regulatory_arbitrage_exploitation: 0.10,
    corporate_sovereignty_over_state: 0.08,
    standard_setting_capture: 0.10,
    judicial_capture_risk: 0.10,
    legislative_capture_index: 0.08,
    agency_capture_prevalence: 0.10,
    dark_money_political_influence: 0.10,
    patent_system_weaponization: 0.08,
    regulatory_complexity_weaponization: 0.10,
    state_aid_capture_mechanism: 0.08,
    private_enforcement_substitution: 0.10,
  },
  // CPE-005 — critical, pattern=dark_money_dominance
  // dark_money_dominance: dark_money_political_influence>=0.70 AND lobbying_expenditure_ratio>=0.65
  // regulatory_capture_complete must NOT fire: regulatory_capture_depth<0.70 OR agency_capture_prevalence<0.65
  // antitrust_collapse must NOT fire: market_concentration_index<0.70 OR antitrust_enforcement_weakness<0.65
  // composite >=60 → critical
  {
    id: "CPE-005", industry_sector: "fossil_fuels", region: "MEA",
    regulatory_capture_depth: 0.62,
    lobbying_expenditure_ratio: 0.85,
    revolving_door_intensity: 0.72,
    market_concentration_index: 0.58,
    antitrust_enforcement_weakness: 0.60,
    tax_arbitrage_sophistication: 0.78,
    regulatory_arbitrage_exploitation: 0.75,
    corporate_sovereignty_over_state: 0.68,
    standard_setting_capture: 0.55,
    judicial_capture_risk: 0.72,
    legislative_capture_index: 0.70,
    agency_capture_prevalence: 0.60,
    dark_money_political_influence: 0.88,
    patent_system_weaponization: 0.50,
    regulatory_complexity_weaponization: 0.52,
    state_aid_capture_mechanism: 0.70,
    private_enforcement_substitution: 0.60,
  },
  // CPE-006 — moderate, pattern=none
  // composite >=20 and <40 → moderate; no pattern triggers
  {
    id: "CPE-006", industry_sector: "regional_utilities", region: "EMEA",
    regulatory_capture_depth: 0.32,
    lobbying_expenditure_ratio: 0.28,
    revolving_door_intensity: 0.30,
    market_concentration_index: 0.35,
    antitrust_enforcement_weakness: 0.30,
    tax_arbitrage_sophistication: 0.28,
    regulatory_arbitrage_exploitation: 0.32,
    corporate_sovereignty_over_state: 0.28,
    standard_setting_capture: 0.30,
    judicial_capture_risk: 0.28,
    legislative_capture_index: 0.32,
    agency_capture_prevalence: 0.30,
    dark_money_political_influence: 0.28,
    patent_system_weaponization: 0.30,
    regulatory_complexity_weaponization: 0.28,
    state_aid_capture_mechanism: 0.30,
    private_enforcement_substitution: 0.28,
  },
  // CPE-007 — high, pattern=corporate_sovereignty
  // corporate_sovereignty: corporate_sovereignty_over_state>=0.70 AND tax_arbitrage_sophistication>=0.65
  // regulatory_capture_complete must NOT fire, antitrust_collapse must NOT fire, dark_money_dominance must NOT fire
  // composite >=40 and <60 → high
  {
    id: "CPE-007", industry_sector: "multinational_pharma", region: "NOAM",
    regulatory_capture_depth: 0.50,
    lobbying_expenditure_ratio: 0.55,
    revolving_door_intensity: 0.48,
    market_concentration_index: 0.55,
    antitrust_enforcement_weakness: 0.52,
    tax_arbitrage_sophistication: 0.82,
    regulatory_arbitrage_exploitation: 0.78,
    corporate_sovereignty_over_state: 0.85,
    standard_setting_capture: 0.45,
    judicial_capture_risk: 0.50,
    legislative_capture_index: 0.48,
    agency_capture_prevalence: 0.45,
    dark_money_political_influence: 0.52,
    patent_system_weaponization: 0.60,
    regulatory_complexity_weaponization: 0.50,
    state_aid_capture_mechanism: 0.55,
    private_enforcement_substitution: 0.48,
  },
  // CPE-008 — critical, pattern=standard_capture_hegemony
  // standard_capture_hegemony: standard_setting_capture>=0.70 AND regulatory_complexity_weaponization>=0.65
  // regulatory_capture_complete must NOT fire, antitrust_collapse must NOT fire,
  // dark_money_dominance must NOT fire, corporate_sovereignty must NOT fire
  // composite >=60 → critical
  {
    id: "CPE-008", industry_sector: "defense_aerospace", region: "NOAM",
    regulatory_capture_depth: 0.65,
    lobbying_expenditure_ratio: 0.62,
    revolving_door_intensity: 0.70,
    market_concentration_index: 0.60,
    antitrust_enforcement_weakness: 0.58,
    tax_arbitrage_sophistication: 0.60,
    regulatory_arbitrage_exploitation: 0.65,
    corporate_sovereignty_over_state: 0.62,
    standard_setting_capture: 0.85,
    judicial_capture_risk: 0.78,
    legislative_capture_index: 0.72,
    agency_capture_prevalence: 0.60,
    dark_money_political_influence: 0.60,
    patent_system_weaponization: 0.68,
    regulatory_complexity_weaponization: 0.82,
    state_aid_capture_mechanism: 0.78,
    private_enforcement_substitution: 0.70,
  },
];

type Entity = typeof MOCK_ENTITIES[0];

function captureScore(e: Entity): number {
  const raw = (
    e.regulatory_capture_depth * 0.4 +
    e.agency_capture_prevalence * 0.35 +
    e.legislative_capture_index * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function marketScore(e: Entity): number {
  const raw = (
    e.market_concentration_index * 0.4 +
    e.antitrust_enforcement_weakness * 0.35 +
    e.patent_system_weaponization * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function influenceScore(e: Entity): number {
  const raw = (
    e.lobbying_expenditure_ratio * 0.4 +
    e.dark_money_political_influence * 0.35 +
    e.revolving_door_intensity * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function sovereigntyScore(e: Entity): number {
  const raw = (
    e.corporate_sovereignty_over_state * 0.4 +
    e.tax_arbitrage_sophistication * 0.35 +
    e.regulatory_arbitrage_exploitation * 0.25
  ) * 100;
  return Math.round(raw * 100) / 100;
}

function compositeScore(cap: number, mkt: number, inf: number, sov: number): number {
  return Math.round((cap * 0.30 + mkt * 0.25 + inf * 0.25 + sov * 0.20) * 100) / 100;
}

function capturePattern(e: Entity): string {
  if (e.regulatory_capture_depth >= 0.70 && e.agency_capture_prevalence >= 0.65)
    return "regulatory_capture_complete";
  if (e.market_concentration_index >= 0.70 && e.antitrust_enforcement_weakness >= 0.65)
    return "antitrust_collapse";
  if (e.dark_money_political_influence >= 0.70 && e.lobbying_expenditure_ratio >= 0.65)
    return "dark_money_dominance";
  if (e.corporate_sovereignty_over_state >= 0.70 && e.tax_arbitrage_sophistication >= 0.65)
    return "corporate_sovereignty";
  if (e.standard_setting_capture >= 0.70 && e.regulatory_complexity_weaponization >= 0.65)
    return "standard_capture_hegemony";
  return "none";
}

function riskLevel(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function severity(comp: number): string {
  if (comp >= 60) return "capture_corporative_systémique";
  if (comp >= 40) return "pouvoir_corporatif_dominant";
  if (comp >= 20) return "dérive_corporative_structurelle";
  return "équilibre_régulateur_relatif";
}

function recommendedAction(risk: string): string {
  if (risk === "critical") return "restauration_souveraineté_régulatrice_urgente";
  if (risk === "high") return "démantèlement_capture_corporative";
  if (risk === "moderate") return "renforcement_antitrust_systémique";
  return "veille_pouvoir_corporatif";
}

function signal(risk: string): string {
  if (risk === "critical") return "🔴 Capture corporative systémique — État sous contrôle privé";
  if (risk === "high") return "🟠 Pouvoir corporatif dominant détecté";
  if (risk === "moderate") return "🟡 Dérive corporative structurelle active";
  return "🟢 Équilibre régulateur relatif maintenu";
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const cap  = captureScore(e);
      const mkt  = marketScore(e);
      const inf  = influenceScore(e);
      const sov  = sovereigntyScore(e);
      const comp = compositeScore(cap, mkt, inf, sov);
      const pat  = capturePattern(e);
      const risk = riskLevel(comp);
      const sev  = severity(comp);
      const act  = recommendedAction(risk);
      const sig  = signal(risk);
      return {
        id:                        e.entity_id,
        industry_sector:                  e.industry_sector,
        region:                           e.region,
        capture_score:                    cap,
        market_score:                     mkt,
        influence_score:                  inf,
        sovereignty_score:                sov,
        composite_score:                  comp,
        risk_level:                       risk,
        capture_pattern:                  pat,
        severity:                         sev,
        recommended_action:               act,
        signal:                           sig,
        regulatory_capture_depth:         e.regulatory_capture_depth,
        corporate_sovereignty_over_state: e.corporate_sovereignty_over_state,
      };
    });

    const riskDist: Record<string, number> = {};
    const patDist: Record<string, number> = {};
    const sevDist: Record<string, number> = {};
    const actDist: Record<string, number> = {};
    let tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      riskDist[ent.risk_level]          = (riskDist[ent.risk_level]          || 0) + 1;
      patDist[ent.capture_pattern]      = (patDist[ent.capture_pattern]      || 0) + 1;
      sevDist[ent.severity]             = (sevDist[ent.severity]             || 0) + 1;
      actDist[ent.recommended_action]   = (actDist[ent.recommended_action]   || 0) + 1;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite = Math.round(tComp / n * 10) / 10;
    const summary = {
      module_id:                    339,
      module_name:                  "Corporate Power Capture & Regulatory Arbitrage Intelligence Engine",
      total_entities:               n,
      critical_count:               criticalCount,
      high_count:                   highCount,
      moderate_count:               moderateCount,
      low_count:                    lowCount,
      avg_composite:                avgComposite,
      pattern_distribution:         patDist,
      risk_distribution:            riskDist,
      severity_distribution:        sevDist,
      action_distribution:          actDist,
      avg_estimated_capture_index:  Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary }, "corporate-capture-engine"));
  }

  try {
    const upstream = await fetch(`${process.env.SWARM_API_URL}/corporate-capture-engine`);
    const data = await upstream.json();
    return NextResponse.json(sealResponse(data, "corporate-capture-engine"));
  } catch {
    return NextResponse.json(
      sealResponse({ error: "Upstream corporate capture engine unavailable" }, "corporate-capture-engine"),
      { status: 502 }
    );
  }
}
