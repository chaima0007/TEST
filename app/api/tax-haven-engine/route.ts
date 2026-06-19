import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

// ── Module 405 — Caelum Partners — Chaima Mhadbi, Fondatrice, Bruxelles
// Paradis Fiscaux & Centres Financiers Offshore Intelligence Engine
// 8 entities covering all 5 patterns and all 4 risk levels.

const SWARM_API_URL = process.env.SWARM_API_URL;

interface TheInput {
  entity_id: string;
  haven_type: string;
  region: string;
  secrecy_score: number;
  corporate_tax_rate: number;
  beneficial_ownership_opacity: number;
  treaty_network_abuse: number;
  profit_shifting_intensity: number;
  illicit_flow_volume: number;
  regulatory_compliance: number;
  automatic_info_exchange: number;
  beneficial_ownership_register: number;
  politically_exposed_persons: number;
  real_estate_opacity: number;
  trust_structure_opacity: number;
  shell_company_ease: number;
  enforcement_effectiveness: number;
  civil_society_access: number;
  multilateral_cooperation: number;
  domestic_tax_erosion: number;
}

const MOCK_ENTITIES: TheInput[] = [
  // THE-001 — EMEA, juridiction_offshore → critical, sovereign_wealth_capture
  // beneficial_ownership_opacity>0.85 AND politically_exposed_persons>0.80 → sovereign_wealth_capture
  // composite≥60 → critical
  {
    entity_id: "THE-001", haven_type: "juridiction_offshore", region: "EMEA",
    secrecy_score: 0.90,
    corporate_tax_rate: 0.05,
    beneficial_ownership_opacity: 0.92,
    treaty_network_abuse: 0.75,
    profit_shifting_intensity: 0.70,
    illicit_flow_volume: 0.78,
    regulatory_compliance: 0.15,
    automatic_info_exchange: 0.12,
    beneficial_ownership_register: 0.10,
    politically_exposed_persons: 0.88,
    real_estate_opacity: 0.80,
    trust_structure_opacity: 0.85,
    shell_company_ease: 0.78,
    enforcement_effectiveness: 0.10,
    civil_society_access: 0.15,
    multilateral_cooperation: 0.12,
    domestic_tax_erosion: 0.82,
  },
  // THE-002 — APAC, centre_financier_offshore → critical, corporate_profit_shifting
  // profit_shifting_intensity>0.85 AND treaty_network_abuse>0.80
  // beneficial_ownership_opacity=0.72 → avoids sovereign_wealth_capture
  // composite≥60 → critical
  {
    entity_id: "THE-002", haven_type: "centre_financier_offshore", region: "APAC",
    secrecy_score: 0.85,
    corporate_tax_rate: 0.02,
    beneficial_ownership_opacity: 0.72,
    treaty_network_abuse: 0.88,
    profit_shifting_intensity: 0.90,
    illicit_flow_volume: 0.68,
    regulatory_compliance: 0.18,
    automatic_info_exchange: 0.15,
    beneficial_ownership_register: 0.20,
    politically_exposed_persons: 0.70,
    real_estate_opacity: 0.72,
    trust_structure_opacity: 0.80,
    shell_company_ease: 0.75,
    enforcement_effectiveness: 0.12,
    civil_society_access: 0.18,
    multilateral_cooperation: 0.15,
    domestic_tax_erosion: 0.78,
  },
  // THE-003 — LATAM, paradis_fiscal_insulaire → critical, illicit_financial_flows
  // illicit_flow_volume>0.85 AND shell_company_ease>0.80
  // beneficial_ownership_opacity=0.78, profit_shifting_intensity=0.75 → avoids earlier patterns
  // composite≥60 → critical
  {
    entity_id: "THE-003", haven_type: "paradis_fiscal_insulaire", region: "LATAM",
    secrecy_score: 0.88,
    corporate_tax_rate: 0.00,
    beneficial_ownership_opacity: 0.78,
    treaty_network_abuse: 0.72,
    profit_shifting_intensity: 0.75,
    illicit_flow_volume: 0.92,
    regulatory_compliance: 0.12,
    automatic_info_exchange: 0.10,
    beneficial_ownership_register: 0.08,
    politically_exposed_persons: 0.75,
    real_estate_opacity: 0.78,
    trust_structure_opacity: 0.82,
    shell_company_ease: 0.88,
    enforcement_effectiveness: 0.08,
    civil_society_access: 0.12,
    multilateral_cooperation: 0.10,
    domestic_tax_erosion: 0.80,
  },
  // THE-004 — NOAM, zone_franche_financière → high, regulatory_arbitrage_network
  // secrecy_score>0.80 AND regulatory_compliance<0.25
  // beneficial_ownership_opacity=0.55, profit_shifting=0.42, illicit=0.45 → avoids earlier patterns
  // composite≈51.8 → high [40,60)
  {
    entity_id: "THE-004", haven_type: "zone_franche_financière", region: "NOAM",
    secrecy_score: 0.82,
    corporate_tax_rate: 0.08,
    beneficial_ownership_opacity: 0.55,
    treaty_network_abuse: 0.45,
    profit_shifting_intensity: 0.42,
    illicit_flow_volume: 0.45,
    regulatory_compliance: 0.22,
    automatic_info_exchange: 0.45,
    beneficial_ownership_register: 0.40,
    politically_exposed_persons: 0.45,
    real_estate_opacity: 0.48,
    trust_structure_opacity: 0.52,
    shell_company_ease: 0.45,
    enforcement_effectiveness: 0.60,
    civil_society_access: 0.48,
    multilateral_cooperation: 0.42,
    domestic_tax_erosion: 0.40,
  },
  // THE-005 — MEA, juridiction_secrète → high, democratic_fiscal_erosion
  // domestic_tax_erosion>0.80 AND civil_society_access<0.25
  // secrecy_score=0.60 → avoids regulatory_arbitrage_network
  // composite≈50.9 → high [40,60)
  {
    entity_id: "THE-005", haven_type: "juridiction_secrète", region: "MEA",
    secrecy_score: 0.60,
    corporate_tax_rate: 0.10,
    beneficial_ownership_opacity: 0.52,
    treaty_network_abuse: 0.48,
    profit_shifting_intensity: 0.45,
    illicit_flow_volume: 0.42,
    regulatory_compliance: 0.40,
    automatic_info_exchange: 0.52,
    beneficial_ownership_register: 0.48,
    politically_exposed_persons: 0.50,
    real_estate_opacity: 0.45,
    trust_structure_opacity: 0.50,
    shell_company_ease: 0.42,
    enforcement_effectiveness: 0.55,
    civil_society_access: 0.18,
    multilateral_cooperation: 0.42,
    domestic_tax_erosion: 0.82,
  },
  // THE-006 — EMEA, territoire_autonome_fiscal → moderate, none
  // composite≈35.5 → moderate [20,40)
  {
    entity_id: "THE-006", haven_type: "territoire_autonome_fiscal", region: "EMEA",
    secrecy_score: 0.38,
    corporate_tax_rate: 0.15,
    beneficial_ownership_opacity: 0.35,
    treaty_network_abuse: 0.30,
    profit_shifting_intensity: 0.32,
    illicit_flow_volume: 0.28,
    regulatory_compliance: 0.55,
    automatic_info_exchange: 0.52,
    beneficial_ownership_register: 0.50,
    politically_exposed_persons: 0.28,
    real_estate_opacity: 0.32,
    trust_structure_opacity: 0.35,
    shell_company_ease: 0.30,
    enforcement_effectiveness: 0.55,
    civil_society_access: 0.58,
    multilateral_cooperation: 0.52,
    domestic_tax_erosion: 0.30,
  },
  // THE-007 — APAC, microjuridiction_offshore → low, none
  // composite≈10.5 → low
  {
    entity_id: "THE-007", haven_type: "microjuridiction_offshore", region: "APAC",
    secrecy_score: 0.12,
    corporate_tax_rate: 0.25,
    beneficial_ownership_opacity: 0.10,
    treaty_network_abuse: 0.08,
    profit_shifting_intensity: 0.10,
    illicit_flow_volume: 0.08,
    regulatory_compliance: 0.88,
    automatic_info_exchange: 0.85,
    beneficial_ownership_register: 0.90,
    politically_exposed_persons: 0.08,
    real_estate_opacity: 0.10,
    trust_structure_opacity: 0.08,
    shell_company_ease: 0.10,
    enforcement_effectiveness: 0.85,
    civil_society_access: 0.90,
    multilateral_cooperation: 0.88,
    domestic_tax_erosion: 0.10,
  },
  // THE-008 — NOAM, centre_services_financiers → low, none
  // composite≈9.5 → low
  {
    entity_id: "THE-008", haven_type: "centre_services_financiers", region: "NOAM",
    secrecy_score: 0.10,
    corporate_tax_rate: 0.22,
    beneficial_ownership_opacity: 0.08,
    treaty_network_abuse: 0.10,
    profit_shifting_intensity: 0.08,
    illicit_flow_volume: 0.10,
    regulatory_compliance: 0.90,
    automatic_info_exchange: 0.88,
    beneficial_ownership_register: 0.85,
    politically_exposed_persons: 0.10,
    real_estate_opacity: 0.08,
    trust_structure_opacity: 0.10,
    shell_company_ease: 0.08,
    enforcement_effectiveness: 0.88,
    civil_society_access: 0.85,
    multilateral_cooperation: 0.90,
    domestic_tax_erosion: 0.08,
  },
];

// ── Scoring functions (mirrors Python engine exactly) ─────────────────────────

function evasionScore(e: TheInput): number {
  return Math.round((e.secrecy_score * 0.4 + e.beneficial_ownership_opacity * 0.35 + e.treaty_network_abuse * 0.25) * 100 * 100) / 100;
}

function opacityScore(e: TheInput): number {
  return Math.round((e.trust_structure_opacity * 0.4 + e.real_estate_opacity * 0.35 + e.shell_company_ease * 0.25) * 100 * 100) / 100;
}

function harmScore(e: TheInput): number {
  return Math.round((e.illicit_flow_volume * 0.4 + e.profit_shifting_intensity * 0.35 + e.domestic_tax_erosion * 0.25) * 100 * 100) / 100;
}

function enforcementScore(e: TheInput): number {
  return Math.round(((1 - e.enforcement_effectiveness) * 0.4 + (1 - e.automatic_info_exchange) * 0.35 + (1 - e.multilateral_cooperation) * 0.25) * 100 * 100) / 100;
}

function theComposite(ev: number, op: number, ha: number, en: number): number {
  return Math.round((ev * 0.30 + op * 0.25 + ha * 0.25 + en * 0.20) * 100) / 100;
}

function theRisk(comp: number): string {
  if (comp >= 60) return "critical";
  if (comp >= 40) return "high";
  if (comp >= 20) return "moderate";
  return "low";
}

function thePattern(e: TheInput): string {
  if (e.beneficial_ownership_opacity > 0.85 && e.politically_exposed_persons > 0.80) return "sovereign_wealth_capture";
  if (e.profit_shifting_intensity > 0.85 && e.treaty_network_abuse > 0.80) return "corporate_profit_shifting";
  if (e.illicit_flow_volume > 0.85 && e.shell_company_ease > 0.80) return "illicit_financial_flows";
  if (e.secrecy_score > 0.80 && e.regulatory_compliance < 0.25) return "regulatory_arbitrage_network";
  if (e.domestic_tax_erosion > 0.80 && e.civil_society_access < 0.25) return "democratic_fiscal_erosion";
  return "none";
}

function theSeverity(risk: string): string {
  if (risk === "critical") return "crise_paradis_fiscal_systémique";
  if (risk === "high") return "opacité_financière_majeure_détectée";
  if (risk === "moderate") return "érosion_fiscale_structurelle";
  return "surveillance_conformité_fiscale";
}

function theAction(risk: string): string {
  if (risk === "critical") return "intervention_urgente_paradis_fiscal_critique";
  if (risk === "high") return "renforcement_échange_informations_automatique";
  if (risk === "moderate") return "audit_conformité_fiscale_approfondi";
  return "veille_transparence_fiscale_continue";
}

function theSignal(risk: string): string {
  if (risk === "critical") return "🔴 Crise paradis fiscal systémique — évasion fiscale en péril démocratique";
  if (risk === "high") return "🟠 Opacité financière majeure détectée — flux illicites significatifs";
  if (risk === "moderate") return "🟡 Érosion fiscale structurelle active — risque modéré";
  return "🟢 Conformité fiscale sous surveillance";
}

function analyzeEntity(e: TheInput) {
  const ev = evasionScore(e);
  const op = opacityScore(e);
  const ha = harmScore(e);
  const en = enforcementScore(e);
  const comp = theComposite(ev, op, ha, en);
  const risk = theRisk(comp);
  const pattern = thePattern(e);
  const severity = theSeverity(risk);
  const action = theAction(risk);
  const signal = theSignal(risk);

  return {
    entity_id: e.entity_id,
    haven_type: e.haven_type,
    region: e.region,
    evasion_score: ev,
    opacity_score: op,
    harm_score: ha,
    enforcement_score: en,
    composite_score: comp,
    risk_level: risk,
    tax_haven_pattern: pattern,
    severity,
    recommended_action: action,
    signal,
    secrecy_score: e.secrecy_score,
    illicit_flow_volume: e.illicit_flow_volume,
  };
}

// ── GET handler ───────────────────────────────────────────────────────────────

export async function GET() {
  if (!SWARM_API_URL) {
    const entities = MOCK_ENTITIES.map(analyzeEntity);

    const risk_distribution: Record<string, number> = {};
    const pattern_distribution: Record<string, number> = {};
    const severity_distribution: Record<string, number> = {};
    const action_distribution: Record<string, number> = {};
    let tComp = 0;

    for (const ent of entities) {
      risk_distribution[ent.risk_level] = (risk_distribution[ent.risk_level] || 0) + 1;
      pattern_distribution[ent.tax_haven_pattern] = (pattern_distribution[ent.tax_haven_pattern] || 0) + 1;
      severity_distribution[ent.severity] = (severity_distribution[ent.severity] || 0) + 1;
      action_distribution[ent.recommended_action] = (action_distribution[ent.recommended_action] || 0) + 1;
      tComp += ent.composite_score;
    }

    const n = entities.length;
    const avgComp = Math.round((tComp / n) * 10) / 10;

    const summary = {
      module_id: 405,
      module_name: "Paradis Fiscaux & Centres Financiers Offshore Intelligence Engine",
      total: n,
      critical: risk_distribution["critical"] || 0,
      high: risk_distribution["high"] || 0,
      moderate: risk_distribution["moderate"] || 0,
      low: risk_distribution["low"] || 0,
      avg_composite: avgComp,
      pattern_distribution,
      risk_distribution,
      severity_distribution,
      action_distribution,
      avg_estimated_tax_haven_index: Math.round(avgComp / 100 * 10 * 100) / 100,
    };

    return NextResponse.json(sealResponse({ entities, summary } as Record<string, unknown>));
  }

  try {
    const url = new URL(`${SWARM_API_URL}/api/tax-haven-engine`);
    const res = await fetch(url.toString(), { cache: "no-store" });
    if (res.ok) return NextResponse.json(sealResponse(await res.json()));
  } catch {}
  return NextResponse.json(sealResponse({ entities: [], summary: {} } as Record<string, unknown>), { status: 502 });
}
