import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[informal-economy-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Informal Economy Rights Engine Agent",
  domain: "informal_economy_rights",
  total_entities: 8,
  avg_composite: 61.68,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { social_protection_exclusion_scale: 2, workplace_safety_absence_pattern: 2, income_instability_poverty_trap: 2, legal_status_vulnerability_severity: 2 },
  top_risk_entities: [
    "Inde — 90% Économie Informelle, 500M Travailleurs Sans Protection Sociale & Caste Emploi",
    "Bangladesh — 80% Emplois Informels, Usines Sans Contrat, Rana Plaza 2013 & Syndicats Interdits",
    "Nigeria/Afrique Sub-Sah. — 85% Informel, Vendeurs Rue Expulsés, Zéro Assurance Chômage",
  ],
  critical_alerts: [
    "Inde: social_protection_exclusion_scale",
    "Bangladesh: workplace_safety_absence_pattern",
    "Nigeria/Afrique Sub-Sah.: social_protection_exclusion_scale",
    "Pérou/Amérique Latine: income_instability_poverty_trap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_informal_economy_rights_index: 6.17,
  data_sources: [
    "wiego_women_informal_employment_global_local_rights_report",
    "ilo_world_employment_social_outlook_informal_economy_2023",
    "streetnet_international_street_vendor_rights_monitoring",
  ],
  entities: [
    { id: "IER-001", name: "Inde — 90% Économie Informelle, 500M Travailleurs Sans Protection Sociale & Caste Emploi", country: "Asie du Sud", composite_score: 92.9, social_protection_exclusion_scale_score: 95.0, legal_status_vulnerability_severity_score: 92.0, workplace_safety_absence_pattern_score: 92.0, income_instability_poverty_trap_score: 92.0, risk_level: "critique", primary_pattern: "social_protection_exclusion_scale", estimated_informal_economy_rights_index: 9.29, last_updated: "2026-06-21" },
    { id: "IER-002", name: "Bangladesh — 80% Emplois Informels, Usines Sans Contrat, Rana Plaza 2013 & Syndicats Interdits", country: "Asie du Sud", composite_score: 90.25, social_protection_exclusion_scale_score: 88.0, legal_status_vulnerability_severity_score: 90.0, workplace_safety_absence_pattern_score: 95.0, income_instability_poverty_trap_score: 88.0, risk_level: "critique", primary_pattern: "workplace_safety_absence_pattern", estimated_informal_economy_rights_index: 9.03, last_updated: "2026-06-21" },
    { id: "IER-003", name: "Nigeria/Afrique Sub-Sah. — 85% Informel, Vendeurs Rue Expulsés, Zéro Assurance Chômage", country: "Afrique de l'Ouest", composite_score: 88.6, social_protection_exclusion_scale_score: 90.0, legal_status_vulnerability_severity_score: 88.0, workplace_safety_absence_pattern_score: 88.0, income_instability_poverty_trap_score: 88.0, risk_level: "critique", primary_pattern: "social_protection_exclusion_scale", estimated_informal_economy_rights_index: 8.86, last_updated: "2026-06-21" },
    { id: "IER-004", name: "Pérou/Amérique Latine — 70% Informel, Micro-Commerce Femmes, Harcèlement Police & Précarité", country: "Amérique Latine", composite_score: 86.35, social_protection_exclusion_scale_score: 85.0, legal_status_vulnerability_severity_score: 88.0, workplace_safety_absence_pattern_score: 85.0, income_instability_poverty_trap_score: 88.0, risk_level: "critique", primary_pattern: "income_instability_poverty_trap", estimated_informal_economy_rights_index: 8.64, last_updated: "2026-06-21" },
    { id: "IER-005", name: "Égypte/MENA — 40%+ Informel, Charbonniers/Pêcheurs Sans Contrat, Risques Chimiques & Chaleur", country: "Moyen-Orient/Afrique du Nord", composite_score: 53.1, social_protection_exclusion_scale_score: 52.0, legal_status_vulnerability_severity_score: 55.0, workplace_safety_absence_pattern_score: 55.0, income_instability_poverty_trap_score: 50.0, risk_level: "élevé", primary_pattern: "legal_status_vulnerability_severity", estimated_informal_economy_rights_index: 5.31, last_updated: "2026-06-21" },
    { id: "IER-006", name: "Mexique — 57% Informel, Travailleurs Domestiques Sans IMSS, Enfants Champs Agricoles & Précarité", country: "Amérique Latine", composite_score: 52.0, social_protection_exclusion_scale_score: 50.0, legal_status_vulnerability_severity_score: 52.0, workplace_safety_absence_pattern_score: 52.0, income_instability_poverty_trap_score: 55.0, risk_level: "élevé", primary_pattern: "income_instability_poverty_trap", estimated_informal_economy_rights_index: 5.2, last_updated: "2026-06-21" },
    { id: "IER-007", name: "WIEGO/StreetNet — Droits Travailleurs Informels, Collecte Données & Plaidoyer OIT Convention", country: "Global", composite_score: 25.85, social_protection_exclusion_scale_score: 22.0, legal_status_vulnerability_severity_score: 28.0, workplace_safety_absence_pattern_score: 25.0, income_instability_poverty_trap_score: 30.0, risk_level: "modéré", primary_pattern: "legal_status_vulnerability_severity", estimated_informal_economy_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "IER-008", name: "OIT/Convention C189 — Travailleurs Domestiques, SDG 8.3 Emploi Décent & Protection Sociale", country: "Global", composite_score: 4.4, social_protection_exclusion_scale_score: 4.0, legal_status_vulnerability_severity_score: 5.0, workplace_safety_absence_pattern_score: 3.0, income_instability_poverty_trap_score: 6.0, risk_level: "faible", primary_pattern: "workplace_safety_absence_pattern", estimated_informal_economy_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/informal-economy-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
