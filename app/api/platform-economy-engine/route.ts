import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[platform-economy-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const MOCK_ENTITIES = [
  // PEE-001 — critical, algorithmic_wage_theft dominant
  {
    id: "PEE-001", platform_sector: "ride_hailing", region: "NOAM",
    wage_theft_index: 0.92, algorithmic_management_intensity: 0.88,
    benefit_denial_rate: 0.80, misclassification_prevalence: 0.78,
    platform_market_concentration: 0.70, worker_bargaining_power: 0.15,
    regulatory_compliance: 0.22, social_protection_gap: 0.75,
    income_volatility: 0.72, surveillance_score: 0.65,
    deactivation_risk: 0.70, minimum_earnings_gap: 0.68,
    union_access_barrier: 0.72, data_portability: 0.20,
    cross_platform_competition: 0.22, transparency_score: 0.18,
    legal_protection_effectiveness: 0.20,
  },
  // PEE-002 — critical, surveillance_control_dystopia (surveillance > 0.7)
  {
    id: "PEE-002", platform_sector: "food_delivery", region: "EMEA",
    wage_theft_index: 0.78, algorithmic_management_intensity: 0.72,
    benefit_denial_rate: 0.90, misclassification_prevalence: 0.82,
    platform_market_concentration: 0.68, worker_bargaining_power: 0.12,
    regulatory_compliance: 0.18, social_protection_gap: 0.88,
    income_volatility: 0.85, surveillance_score: 0.88,
    deactivation_risk: 0.82, minimum_earnings_gap: 0.80,
    union_access_barrier: 0.75, data_portability: 0.15,
    cross_platform_competition: 0.18, transparency_score: 0.12,
    legal_protection_effectiveness: 0.15,
  },
  // PEE-003 — critical, misclassification_fraud dominant
  {
    id: "PEE-003", platform_sector: "freelance_marketplace", region: "APAC",
    wage_theft_index: 0.75, algorithmic_management_intensity: 0.70,
    benefit_denial_rate: 0.72, misclassification_prevalence: 0.95,
    platform_market_concentration: 0.65, worker_bargaining_power: 0.10,
    regulatory_compliance: 0.08, social_protection_gap: 0.70,
    income_volatility: 0.68, surveillance_score: 0.60,
    deactivation_risk: 0.65, minimum_earnings_gap: 0.62,
    union_access_barrier: 0.68, data_portability: 0.25,
    cross_platform_competition: 0.20, transparency_score: 0.15,
    legal_protection_effectiveness: 0.10,
  },
  // PEE-004 — high, platform_monopoly_capture dominant
  {
    id: "PEE-004", platform_sector: "cloud_labor", region: "LATAM",
    wage_theft_index: 0.50, algorithmic_management_intensity: 0.48,
    benefit_denial_rate: 0.52, misclassification_prevalence: 0.50,
    platform_market_concentration: 0.65, worker_bargaining_power: 0.28,
    regulatory_compliance: 0.35, social_protection_gap: 0.50,
    income_volatility: 0.48, surveillance_score: 0.50,
    deactivation_risk: 0.45, minimum_earnings_gap: 0.48,
    union_access_barrier: 0.60, data_portability: 0.20,
    cross_platform_competition: 0.22, transparency_score: 0.28,
    legal_protection_effectiveness: 0.32,
  },
  // PEE-005 — high, surveillance_control_dystopia (surveillance > 0.7)
  {
    id: "PEE-005", platform_sector: "domestic_services", region: "SSA",
    wage_theft_index: 0.58, algorithmic_management_intensity: 0.55,
    benefit_denial_rate: 0.52, misclassification_prevalence: 0.50,
    platform_market_concentration: 0.48, worker_bargaining_power: 0.22,
    regulatory_compliance: 0.32, social_protection_gap: 0.50,
    income_volatility: 0.48, surveillance_score: 0.75,
    deactivation_risk: 0.45, minimum_earnings_gap: 0.48,
    union_access_barrier: 0.52, data_portability: 0.32,
    cross_platform_competition: 0.30, transparency_score: 0.28,
    legal_protection_effectiveness: 0.30,
  },
  // PEE-006 — moderate, benefits_denial_systematic dominant
  {
    id: "PEE-006", platform_sector: "microtask", region: "EMEA",
    wage_theft_index: 0.28, algorithmic_management_intensity: 0.25,
    benefit_denial_rate: 0.55, misclassification_prevalence: 0.28,
    platform_market_concentration: 0.30, worker_bargaining_power: 0.42,
    regulatory_compliance: 0.52, social_protection_gap: 0.50,
    income_volatility: 0.45, surveillance_score: 0.32,
    deactivation_risk: 0.38, minimum_earnings_gap: 0.40,
    union_access_barrier: 0.32, data_portability: 0.48,
    cross_platform_competition: 0.45, transparency_score: 0.42,
    legal_protection_effectiveness: 0.50,
  },
  // PEE-007 — low
  {
    id: "PEE-007", platform_sector: "professional_services", region: "NOAM",
    wage_theft_index: 0.10, algorithmic_management_intensity: 0.12,
    benefit_denial_rate: 0.12, misclassification_prevalence: 0.10,
    platform_market_concentration: 0.15, worker_bargaining_power: 0.75,
    regulatory_compliance: 0.80, social_protection_gap: 0.12,
    income_volatility: 0.10, surveillance_score: 0.15,
    deactivation_risk: 0.10, minimum_earnings_gap: 0.08,
    union_access_barrier: 0.12, data_portability: 0.82,
    cross_platform_competition: 0.78, transparency_score: 0.80,
    legal_protection_effectiveness: 0.82,
  },
  // PEE-008 — low
  {
    id: "PEE-008", platform_sector: "e_commerce_seller", region: "APAC",
    wage_theft_index: 0.08, algorithmic_management_intensity: 0.10,
    benefit_denial_rate: 0.10, misclassification_prevalence: 0.08,
    platform_market_concentration: 0.18, worker_bargaining_power: 0.70,
    regulatory_compliance: 0.75, social_protection_gap: 0.10,
    income_volatility: 0.12, surveillance_score: 0.12,
    deactivation_risk: 0.08, minimum_earnings_gap: 0.10,
    union_access_barrier: 0.10, data_portability: 0.78,
    cross_platform_competition: 0.72, transparency_score: 0.75,
    legal_protection_effectiveness: 0.78,
  },
];

type PEEInput = typeof MOCK_ENTITIES[0];

function exploitationScore(e: PEEInput): number {
  return Math.round((e.wage_theft_index + e.algorithmic_management_intensity) / 2 * 100 * 100) / 100;
}
function precarityScore(e: PEEInput): number {
  return Math.round(
    (e.benefit_denial_rate + e.social_protection_gap + e.income_volatility + e.deactivation_risk + e.minimum_earnings_gap) / 5 * 100 * 100
  ) / 100;
}
function monopolyScore(e: PEEInput): number {
  return Math.round(
    (e.platform_market_concentration + e.union_access_barrier + (1 - e.data_portability) + (1 - e.cross_platform_competition)) / 4 * 100 * 100
  ) / 100;
}
function misclassificationScore(e: PEEInput): number {
  return Math.round(
    (e.misclassification_prevalence + (1 - e.regulatory_compliance) + (1 - e.legal_protection_effectiveness)) / 3 * 100 * 100
  ) / 100;
}
function compositeScore(exp: number, pre: number, mon: number, mis: number): number {
  return Math.round((exp * 0.30 + pre * 0.25 + mon * 0.25 + mis * 0.20) * 100) / 100;
}
function riskLevel(composite: number): string {
  if (composite >= 60) return "critical";
  if (composite >= 40) return "high";
  if (composite >= 20) return "moderate";
  return "low";
}
function dominantPattern(e: PEEInput, exp: number, pre: number, mon: number, mis: number): string {
  if (e.surveillance_score > 0.7) return "surveillance_control_dystopia";
  const scores: Record<string, number> = {
    algorithmic_wage_theft: exp,
    benefits_denial_systematic: pre,
    platform_monopoly_capture: mon,
    misclassification_fraud: mis,
  };
  return Object.entries(scores).reduce((a, b) => (b[1] > a[1] ? b : a))[0];
}
function patternsDetected(e: PEEInput, exp: number, pre: number, mon: number, mis: number): string[] {
  const patterns: string[] = [];
  if (exp > 50) patterns.push("algorithmic_wage_theft");
  if (pre > 50) patterns.push("benefits_denial_systematic");
  if (mon > 50) patterns.push("platform_monopoly_capture");
  if (mis > 50) patterns.push("misclassification_fraud");
  if (e.surveillance_score > 0.7 && !patterns.includes("surveillance_control_dystopia")) {
    patterns.push("surveillance_control_dystopia");
  }
  return patterns;
}
function severity(composite: number): string {
  if (composite >= 60) return "critique";
  if (composite >= 40) return "élevée";
  if (composite >= 20) return "modérée";
  return "faible";
}
function action(risk: string): string {
  if (risk === "critical") return "intervention_urgente_droits_travailleurs_plateformes_critiques";
  if (risk === "high") return "renforcement_protection_sociale_gig_economy_accéléré";
  if (risk === "moderate") return "audit_conditions_travail_plateforme_et_reclassification";
  return "veille_économie_plateformes_continue";
}
function signal(risk: string): string {
  if (risk === "critical") return "🔴 Exploitation systémique travailleurs gig — droits fondamentaux en péril";
  if (risk === "high") return "🟠 Précarité structurelle majeure détectée — protection sociale insuffisante";
  if (risk === "moderate") return "🟡 Risque modéré économie plateforme — surveillance active requise";
  return "🟢 Économie plateforme sous surveillance — droits travailleurs stables";
}

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(e => {
      const exp = exploitationScore(e);
      const pre = precarityScore(e);
      const mon = monopolyScore(e);
      const mis = misclassificationScore(e);
      const comp = compositeScore(exp, pre, mon, mis);
      const risk = riskLevel(comp);
      const domPat = dominantPattern(e, exp, pre, mon, mis);
      const patterns = patternsDetected(e, exp, pre, mon, mis);
      const sev = severity(comp);
      const act = action(risk);
      const sig = signal(risk);
      return {
        id:              e.entity_id,
        platform_sector:        e.platform_sector,
        region:                 e.region,
        exploitation_score:     exp,
        precarity_score:        pre,
        monopoly_score:         mon,
        misclassification_score: mis,
        composite_score:        comp,
        risk_level:             risk,
        dominant_pattern:       domPat,
        patterns_detected:      patterns,
        severity:               sev,
        action:                 act,
        signal:                 sig,
        surveillance_score:     e.surveillance_score,
      };
    });

    const patternCounts: Record<string, number> = {};
    let tExp = 0, tPre = 0, tMon = 0, tMis = 0, tComp = 0;
    let criticalCount = 0, highCount = 0, moderateCount = 0, lowCount = 0;

    for (const ent of entities) {
      patternCounts[ent.dominant_pattern] = (patternCounts[ent.dominant_pattern] || 0) + 1;
      tExp  += ent.exploitation_score;
      tPre  += ent.precarity_score;
      tMon  += ent.monopoly_score;
      tMis  += ent.misclassification_score;
      tComp += ent.composite_score;
      if (ent.risk_level === "critical")       criticalCount++;
      else if (ent.risk_level === "high")      highCount++;
      else if (ent.risk_level === "moderate")  moderateCount++;
      else                                     lowCount++;
    }

    const n = entities.length;
    const avgComposite        = Math.round(tComp / n * 10) / 10;
    const avgExploitation     = Math.round(tExp  / n * 10) / 10;
    const avgPrecarity        = Math.round(tPre  / n * 10) / 10;
    const avgMonopoly         = Math.round(tMon  / n * 10) / 10;
    const avgMisclassification = Math.round(tMis / n * 10) / 10;
    const topPattern          = Object.entries(patternCounts).reduce((a, b) => (b[1] > a[1] ? b : a))[0];
    const entitiesAtRisk      = criticalCount + highCount;

    const summary = {
      total_entities:                 n,
      critical_count:                 criticalCount,
      high_count:                     highCount,
      moderate_count:                 moderateCount,
      low_count:                      lowCount,
      avg_exploitation:               avgExploitation,
      avg_precarity:                  avgPrecarity,
      avg_monopoly:                   avgMonopoly,
      avg_misclassification:          avgMisclassification,
      avg_composite:                  avgComposite,
      top_pattern:                    topPattern,
      entities_at_risk:               entitiesAtRisk,
      avg_estimated_gig_rights_index: Math.round(avgComposite / 100 * 10 * 100) / 100,
    };

    return sealResponse(NextResponse.json(
      sealResponse({ entities, summary } as Record<string, unknown>, "platform-economy-engine")
    ));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/platform-economy-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return sealResponse(NextResponse.json(sealResponse(await res.json() as Record<string, unknown>, "platform-economy-engine")));
  } catch {}
  return sealResponse(NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>, "platform-economy-engine"), { status: 502 }));
}
