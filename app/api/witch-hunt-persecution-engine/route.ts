import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[witch-hunt-persecution-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Witch Hunt Persecution Engine Agent",
  domain: "witch_hunt_persecution",
  total_entities: 8,
  avg_composite: 61.34,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { accused_killings_violence_scale: 2, legal_protection_absence: 2, children_women_targeting_pattern: 2, stigma_social_exclusion_severity: 2 },
  top_risk_entities: [
    "Tanzanie — 10,000+ Meurtres Sorcellerie/Albinisme, Membres Prélevés Vivants & Commerce Rituels",
    "Papouasie-Nouvelle-Guinée — Femmes Brûlées Vives Accusations Sorcellerie & Loi Abrogée 1971",
    "Inde — 2,500+ Meurtres Sorcellerie 2000-2016, Femmes Adivasi Jharkhand & Bihar Ciblées",
  ],
  critical_alerts: [
    "Tanzanie: accused_killings_violence_scale",
    "Papouasie-Nouvelle-Guinée: legal_protection_absence",
    "Inde: children_women_targeting_pattern",
    "RDC: children_women_targeting_pattern",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_witch_hunt_persecution_index: 6.13,
  data_sources: [
    "un_independent_expert_report_harmful_traditional_practices_witchcraft",
    "actionaid_stepping_stones_witch_camp_monitoring_report",
    "hrw_accused_killed_witch_hunt_persecution_africa_pacific",
  ],
  entities: [
    { entity_id: "WH-001", name: "Tanzanie — 10,000+ Meurtres Sorcellerie/Albinisme, Membres Prélevés Vivants & Commerce Rituels", country: "Afrique de l'Est", composite_score: 92.9, accused_killings_violence_scale_score: 95.0, legal_protection_absence_score: 92.0, stigma_social_exclusion_severity_score: 92.0, children_women_targeting_pattern_score: 92.0, risk_level: "critique", primary_pattern: "accused_killings_violence_scale", estimated_witch_hunt_persecution_index: 9.29, last_updated: "2026-06-21" },
    { entity_id: "WH-002", name: "Papouasie-Nouvelle-Guinée — Femmes Brûlées Vives Accusations Sorcellerie & Loi Abrogée 1971", country: "Pacifique", composite_score: 90.0, accused_killings_violence_scale_score: 90.0, legal_protection_absence_score: 92.0, stigma_social_exclusion_severity_score: 88.0, children_women_targeting_pattern_score: 90.0, risk_level: "critique", primary_pattern: "legal_protection_absence", estimated_witch_hunt_persecution_index: 9.0, last_updated: "2026-06-21" },
    { entity_id: "WH-003", name: "Inde — 2,500+ Meurtres Sorcellerie 2000-2016, Femmes Adivasi Jharkhand & Bihar Ciblées", country: "Asie du Sud", composite_score: 88.4, accused_killings_violence_scale_score: 88.0, legal_protection_absence_score: 88.0, stigma_social_exclusion_severity_score: 88.0, children_women_targeting_pattern_score: 90.0, risk_level: "critique", primary_pattern: "children_women_targeting_pattern", estimated_witch_hunt_persecution_index: 8.84, last_updated: "2026-06-21" },
    { entity_id: "WH-004", name: "RDC — 30,000 Enfants Accusés Sorcellerie Rue Kinshasa, Abandonnés & Violences Exorcisme", country: "Afrique Centrale", composite_score: 85.75, accused_killings_violence_scale_score: 85.0, legal_protection_absence_score: 85.0, stigma_social_exclusion_severity_score: 88.0, children_women_targeting_pattern_score: 85.0, risk_level: "critique", primary_pattern: "children_women_targeting_pattern", estimated_witch_hunt_persecution_index: 8.58, last_updated: "2026-06-21" },
    { entity_id: "WH-005", name: "Ghana — Witch Camps Gnani/Gambaga, 1,000+ Femmes Exilées à Vie Sans Procès & Retour Impossible", country: "Afrique de l'Ouest", composite_score: 53.5, accused_killings_violence_scale_score: 52.0, legal_protection_absence_score: 55.0, stigma_social_exclusion_severity_score: 55.0, children_women_targeting_pattern_score: 52.0, risk_level: "élevé", primary_pattern: "stigma_social_exclusion_severity", estimated_witch_hunt_persecution_index: 5.35, last_updated: "2026-06-21" },
    { entity_id: "WH-006", name: "Éthiopie — Femmes Âgées Accusées Sorcellerie Villages Ruraux, Lynchages & Expulsions Communautaires", country: "Afrique de l'Est", composite_score: 49.9, accused_killings_violence_scale_score: 48.0, legal_protection_absence_score: 52.0, stigma_social_exclusion_severity_score: 50.0, children_women_targeting_pattern_score: 50.0, risk_level: "élevé", primary_pattern: "accused_killings_violence_scale", estimated_witch_hunt_persecution_index: 4.99, last_updated: "2026-06-21" },
    { entity_id: "WH-007", name: "Stepping Stones Nigeria/ActionAid — Monitoring Sorcellerie Global, Plaidoyer Witch Camps & Données", country: "Global", composite_score: 25.85, accused_killings_violence_scale_score: 22.0, legal_protection_absence_score: 28.0, stigma_social_exclusion_severity_score: 25.0, children_women_targeting_pattern_score: 30.0, risk_level: "modéré", primary_pattern: "stigma_social_exclusion_severity", estimated_witch_hunt_persecution_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "WH-008", name: "ONU/Expert Indépendant — Rapport 2009 Pratiques Traditionnelles Néfastes & CEDAW Art.5", country: "Global", composite_score: 4.4, accused_killings_violence_scale_score: 4.0, legal_protection_absence_score: 5.0, stigma_social_exclusion_severity_score: 3.0, children_women_targeting_pattern_score: 6.0, risk_level: "faible", primary_pattern: "legal_protection_absence", estimated_witch_hunt_persecution_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/witch-hunt-persecution-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
