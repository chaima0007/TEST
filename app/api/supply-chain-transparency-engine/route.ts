import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[supply-chain-transparency-engine] SWARM_API_URL non défini — mode mock activé");
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(sealResponse(getMockData(), "Supply Chain Transparency Agent"));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/supply-chain-transparency-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`Upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(sealResponse(data, "Supply Chain Transparency Agent"));
  } catch {
    return NextResponse.json(sealResponse(getMockData(), "Supply Chain Transparency Agent"), { status: 502 });
  }
}

// ── Types ─────────────────────────────────────────────────────────────────────

interface SctEntity {
  id: string;
  name: string;
  country: string;
  sector: string;
  composite_score: number;
  traceability_score: number;
  compliance_score: number;
  disclosure_score: number;
  risk_mitigation_score: number;
  risk_level: string;
  primary_pattern: string;
  key_signals: string[];
  estimated_transparency_index: number;
  last_updated: string;
  recommended_action: string;
}

interface SctSummary {
  total_entities: number;
  avg_composite: number;
  risk_distribution: Record<string, number>;
  pattern_distribution: Record<string, number>;
  top_risk_entities: string[];
  critical_alerts: string[];
  last_analysis: string;
  engine_version: string;
  domain: string;
  confidence_score: number;
  data_sources: string[];
  entities: SctEntity[];
  avg_estimated_transparency_index: number;
}

// ── Mock scoring helpers (mirrors Python engine exactly) ───────────────────────

interface SctInput {
  id: string;
  name: string;
  country: string;
  sector: string;
  supplier_mapping_incompleteness: number;
  origin_verification_gap: number;
  tier_visibility_deficit: number;
  regulatory_audit_failures: number;
  certification_gap_rate: number;
  labor_standards_violations: number;
  esg_reporting_deficit: number;
  public_disclosure_gap: number;
  third_party_audit_absence: number;
  geopolitical_supplier_exposure: number;
  concentration_risk: number;
  crisis_resilience_deficit: number;
}

function traceabilityScore(e: SctInput): number {
  return Math.round((e.supplier_mapping_incompleteness * 0.40 + e.origin_verification_gap * 0.35 + e.tier_visibility_deficit * 0.25) * 100 * 100) / 100;
}

function complianceScore(e: SctInput): number {
  return Math.round((e.regulatory_audit_failures * 0.45 + e.certification_gap_rate * 0.35 + e.labor_standards_violations * 0.20) * 100 * 100) / 100;
}

function disclosureScore(e: SctInput): number {
  return Math.round((e.esg_reporting_deficit * 0.40 + e.public_disclosure_gap * 0.40 + e.third_party_audit_absence * 0.20) * 100 * 100) / 100;
}

function riskMitigationScore(e: SctInput): number {
  return Math.round((e.geopolitical_supplier_exposure * 0.40 + e.concentration_risk * 0.35 + e.crisis_resilience_deficit * 0.25) * 100 * 100) / 100;
}

function sctComposite(tr: number, co: number, di: number, ri: number): number {
  return Math.round((tr * 0.30 + co * 0.25 + di * 0.25 + ri * 0.20) * 100) / 100;
}

function sctRiskLevel(comp: number): string {
  if (comp >= 60) return "critique";
  if (comp >= 40) return "élevé";
  if (comp >= 20) return "modéré";
  return "faible";
}

function sctPattern(e: SctInput): string {
  if (e.supplier_mapping_incompleteness > 0.75 && e.tier_visibility_deficit > 0.70) return "Opacité Fournisseur Critique";
  if (e.regulatory_audit_failures > 0.70 && e.certification_gap_rate > 0.65) return "Non-Conformité Réglementaire";
  if (e.origin_verification_gap > 0.65 && e.esg_reporting_deficit > 0.60) return "Traçabilité Défaillante";
  if (e.public_disclosure_gap > 0.45 && e.third_party_audit_absence > 0.40) return "Divulgation Insuffisante";
  return "Risque Fournisseur Émergent";
}

function sctAction(risk: string): string {
  if (risk === "critique") return "plan_urgence_transparence_chaîne_approvisionnement";
  if (risk === "élevé") return "audit_conformité_fournisseurs_prioritaire";
  if (risk === "modéré") return "programme_amélioration_divulgation_continue";
  return "veille_transparence_fournisseurs_active";
}

function sctKeySignals(e: SctInput): string[] {
  const signals: string[] = [];
  if (e.supplier_mapping_incompleteness > 0.60)
    signals.push(`Cartographie fournisseurs incomplète à ${Math.round(e.supplier_mapping_incompleteness * 100)}%`);
  if (e.regulatory_audit_failures > 0.55)
    signals.push(`Écarts audit réglementaire : ${Math.round(e.regulatory_audit_failures * 100)}% de non-conformités`);
  if (e.geopolitical_supplier_exposure > 0.50)
    signals.push(`Exposition géopolitique fournisseurs élevée (${Math.round(e.geopolitical_supplier_exposure * 100)}%)`);
  if (e.origin_verification_gap > 0.55)
    signals.push(`Taux de vérification origines insuffisant — ${Math.round(e.origin_verification_gap * 100)}% non vérifiés`);
  if (e.concentration_risk > 0.50)
    signals.push(`Risque concentration fournisseurs critique (${Math.round(e.concentration_risk * 100)}%)`);
  if (e.esg_reporting_deficit > 0.55)
    signals.push(`Qualité reporting ESG dégradée — déficit de ${Math.round(e.esg_reporting_deficit * 100)}%`);
  if (signals.length < 3) signals.push("Surveillance continue de la chaîne d'approvisionnement active");
  if (signals.length < 3) signals.push("Veille conformité fournisseurs en cours");
  if (signals.length < 3) signals.push("Aucune anomalie critique détectée — maintien des bonnes pratiques");
  return signals.slice(0, 3);
}

function analyzeEntity(e: SctInput): SctEntity {
  const tr = traceabilityScore(e);
  const co = complianceScore(e);
  const di = disclosureScore(e);
  const ri = riskMitigationScore(e);
  const comp = sctComposite(tr, co, di, ri);
  const risk = sctRiskLevel(comp);
  const pattern = sctPattern(e);
  const action = sctAction(risk);
  const signals = sctKeySignals(e);
  const transparencyIndex = Math.round(comp / 100 * 10 * 100) / 100;

  return {
    id: e.entity_id,
    name: e.name,
    country: e.country,
    sector: e.sector,
    composite_score: comp,
    traceability_score: tr,
    compliance_score: co,
    disclosure_score: di,
    risk_mitigation_score: ri,
    risk_level: risk,
    primary_pattern: pattern,
    key_signals: signals,
    estimated_transparency_index: transparencyIndex,
    last_updated: new Date().toISOString(),
    recommended_action: action,
  };
}

// ── Raw input data ─────────────────────────────────────────────────────────────

const RAW_ENTITIES: SctInput[] = [
  // ENT-001 — GlobalTex Industries (Bangladesh, Textile) → critique
  {
    id: "ENT-001", name: "GlobalTex Industries", country: "Bangladesh", sector: "Textile",
    supplier_mapping_incompleteness: 0.88, origin_verification_gap: 0.82, tier_visibility_deficit: 0.85,
    regulatory_audit_failures: 0.80, certification_gap_rate: 0.75, labor_standards_violations: 0.82,
    esg_reporting_deficit: 0.78, public_disclosure_gap: 0.75, third_party_audit_absence: 0.72,
    geopolitical_supplier_exposure: 0.85, concentration_risk: 0.80, crisis_resilience_deficit: 0.75,
  },
  // ENT-002 — MineralCorp Congo (DRC, Mining) → critique
  {
    id: "ENT-002", name: "MineralCorp Congo", country: "DRC", sector: "Mining",
    supplier_mapping_incompleteness: 0.90, origin_verification_gap: 0.88, tier_visibility_deficit: 0.85,
    regulatory_audit_failures: 0.85, certification_gap_rate: 0.80, labor_standards_violations: 0.88,
    esg_reporting_deficit: 0.82, public_disclosure_gap: 0.80, third_party_audit_absence: 0.75,
    geopolitical_supplier_exposure: 0.92, concentration_risk: 0.85, crisis_resilience_deficit: 0.80,
  },
  // ENT-003 — AgriChain Asia Pacific (Vietnam, Agriculture) → critique
  {
    id: "ENT-003", name: "AgriChain Asia Pacific", country: "Vietnam", sector: "Agriculture",
    supplier_mapping_incompleteness: 0.72, origin_verification_gap: 0.78, tier_visibility_deficit: 0.75,
    regulatory_audit_failures: 0.82, certification_gap_rate: 0.78, labor_standards_violations: 0.75,
    esg_reporting_deficit: 0.72, public_disclosure_gap: 0.70, third_party_audit_absence: 0.68,
    geopolitical_supplier_exposure: 0.80, concentration_risk: 0.75, crisis_resilience_deficit: 0.72,
  },
  // ENT-004 — FastFashion EU GmbH (Germany, Retail) → élevé
  {
    id: "ENT-004", name: "FastFashion EU GmbH", country: "Germany", sector: "Retail",
    supplier_mapping_incompleteness: 0.55, origin_verification_gap: 0.68, tier_visibility_deficit: 0.52,
    regulatory_audit_failures: 0.52, certification_gap_rate: 0.50, labor_standards_violations: 0.55,
    esg_reporting_deficit: 0.62, public_disclosure_gap: 0.58, third_party_audit_absence: 0.52,
    geopolitical_supplier_exposure: 0.58, concentration_risk: 0.55, crisis_resilience_deficit: 0.52,
  },
  // ENT-005 — TechSupply Chain Inc (Taiwan, Electronics) → élevé
  {
    id: "ENT-005", name: "TechSupply Chain Inc", country: "Taiwan", sector: "Electronics",
    supplier_mapping_incompleteness: 0.55, origin_verification_gap: 0.62, tier_visibility_deficit: 0.50,
    regulatory_audit_failures: 0.52, certification_gap_rate: 0.48, labor_standards_violations: 0.52,
    esg_reporting_deficit: 0.58, public_disclosure_gap: 0.55, third_party_audit_absence: 0.48,
    geopolitical_supplier_exposure: 0.58, concentration_risk: 0.55, crisis_resilience_deficit: 0.50,
  },
  // ENT-006 — FoodTrace SARL (France, Food & Beverage) → modéré
  {
    id: "ENT-006", name: "FoodTrace SARL", country: "France", sector: "Food & Beverage",
    supplier_mapping_incompleteness: 0.30, origin_verification_gap: 0.32, tier_visibility_deficit: 0.28,
    regulatory_audit_failures: 0.28, certification_gap_rate: 0.25, labor_standards_violations: 0.30,
    esg_reporting_deficit: 0.32, public_disclosure_gap: 0.48, third_party_audit_absence: 0.45,
    geopolitical_supplier_exposure: 0.35, concentration_risk: 0.30, crisis_resilience_deficit: 0.28,
  },
  // ENT-007 — Nordic Transparency AS (Norway, Financial Services) → faible
  {
    id: "ENT-007", name: "Nordic Transparency AS", country: "Norway", sector: "Financial Services",
    supplier_mapping_incompleteness: 0.10, origin_verification_gap: 0.08, tier_visibility_deficit: 0.10,
    regulatory_audit_failures: 0.08, certification_gap_rate: 0.10, labor_standards_violations: 0.08,
    esg_reporting_deficit: 0.10, public_disclosure_gap: 0.08, third_party_audit_absence: 0.10,
    geopolitical_supplier_exposure: 0.12, concentration_risk: 0.10, crisis_resilience_deficit: 0.08,
  },
  // ENT-008 — GreenChain Certified (Netherlands, Sustainability) → faible
  {
    id: "ENT-008", name: "GreenChain Certified", country: "Netherlands", sector: "Sustainability",
    supplier_mapping_incompleteness: 0.08, origin_verification_gap: 0.10, tier_visibility_deficit: 0.08,
    regulatory_audit_failures: 0.10, certification_gap_rate: 0.08, labor_standards_violations: 0.10,
    esg_reporting_deficit: 0.08, public_disclosure_gap: 0.10, third_party_audit_absence: 0.08,
    geopolitical_supplier_exposure: 0.10, concentration_risk: 0.08, crisis_resilience_deficit: 0.10,
  },
];

// ── getMockData ────────────────────────────────────────────────────────────────

function getMockData(): { entities: SctEntity[]; summary: SctSummary } {
  const entities = RAW_ENTITIES.map(analyzeEntity);

  const risk_distribution: Record<string, number> = {};
  const pattern_distribution: Record<string, number> = {};
  const top_risk_entities: string[] = [];
  const critical_alerts: string[] = [];
  let totalComposite = 0;

  for (const ent of entities) {
    risk_distribution[ent.risk_level] = (risk_distribution[ent.risk_level] || 0) + 1;
    pattern_distribution[ent.primary_pattern] = (pattern_distribution[ent.primary_pattern] || 0) + 1;
    totalComposite += ent.composite_score;
    if (ent.risk_level === "critique") {
      top_risk_entities.push(ent.entity_id);
      critical_alerts.push(`${ent.name} (${ent.country}): ${ent.key_signals[0]}`);
    }
  }

  const n = entities.length;
  const avg_composite = Math.round(totalComposite / n * 100) / 100;
  const avg_estimated_transparency_index = Math.round(avg_composite / 100 * 10 * 100) / 100;

  const summary: SctSummary = {
    total_entities: n,
    avg_composite,
    risk_distribution,
    pattern_distribution,
    top_risk_entities,
    critical_alerts,
    last_analysis: new Date().toISOString(),
    engine_version: "1.0.0",
    domain: "transparency",
    confidence_score: 0.91,
    data_sources: ["supplier_audits", "regulatory_filings", "esg_reports", "third_party_assessments"],
    entities,
    avg_estimated_transparency_index,
  };

  return { entities, summary };
}
