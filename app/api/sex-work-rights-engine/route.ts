import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sex-work-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Sex Work Rights Engine Agent",
  domain: "sex_work_rights",
  total_entities: 8,
  avg_composite: 58.32,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { criminalization_rate: 3, violence_impunity: 2, legal_protection_absence: 2, stigma_discrimination: 1 },
  top_risk_entities: [
    "Asie du Sud-Est/Cambodge — Raflades, Centres Détention & Criminalisation SESTA/FOSTA",
    "Afrique Sub-Saharienne — Kenya/Nigeria Sex Workers, Police Brutalité & VIH Non-Traité",
    "USA — SESTA/FOSTA, Criminalisation Numérique & Travailleuses du Sexe Déplacées",
  ],
  critical_alerts: [
    "Asie du Sud-Est/Cambodge: criminalization_rate",
    "Afrique Sub-Saharienne: violence_impunity",
    "USA: legal_protection_absence",
    "Russie/Europe Est: stigma_discrimination",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_sex_work_rights_index: 5.83,
  data_sources: [
    "who_unaids_sex_work_criminalization_health_impact_report",
    "global_network_sex_work_projects_gnswp_annual_advocacy_report",
    "human_rights_watch_swept_away_criminalization_sex_workers_report",
  ],
  entities: [
    { entity_id: "SWR-001", name: "Asie du Sud-Est/Cambodge — Raflades, Centres Détention & Criminalisation SESTA/FOSTA", country: "Asie du Sud-Est", composite_score: 89.0, criminalization_rate_score: 90.0, violence_impunity_score: 88.0, legal_protection_absence_score: 92.0, stigma_discrimination_score: 85.0, risk_level: "critique", primary_pattern: "criminalization_rate", estimated_sex_work_rights_index: 8.9, last_updated: "2026-06-20" },
    { entity_id: "SWR-002", name: "Afrique Sub-Saharienne — Kenya/Nigeria Sex Workers, Police Brutalité & VIH Non-Traité", country: "Afrique Sub-Saharienne", composite_score: 86.4, criminalization_rate_score: 85.0, violence_impunity_score: 90.0, legal_protection_absence_score: 88.0, stigma_discrimination_score: 82.0, risk_level: "critique", primary_pattern: "violence_impunity", estimated_sex_work_rights_index: 8.64, last_updated: "2026-06-20" },
    { entity_id: "SWR-003", name: "USA — SESTA/FOSTA, Criminalisation Numérique & Travailleuses du Sexe Déplacées", country: "Amérique du Nord", composite_score: 75.95, criminalization_rate_score: 72.0, violence_impunity_score: 75.0, legal_protection_absence_score: 80.0, stigma_discrimination_score: 78.0, risk_level: "critique", primary_pattern: "legal_protection_absence", estimated_sex_work_rights_index: 7.6, last_updated: "2026-06-20" },
    { entity_id: "SWR-004", name: "Russie/Europe Est — Persécution LGBT & Travailleuses Sexuelles, Extorsion Policière", country: "Europe de l'Est", composite_score: 73.55, criminalization_rate_score: 68.0, violence_impunity_score: 72.0, legal_protection_absence_score: 75.0, stigma_discrimination_score: 82.0, risk_level: "critique", primary_pattern: "stigma_discrimination", estimated_sex_work_rights_index: 7.36, last_updated: "2026-06-20" },
    { entity_id: "SWR-005", name: "Inde — Devadasi, Section 370 & Traite Sous Couvert Travail Sexuel", country: "Asie du Sud", composite_score: 55.85, criminalization_rate_score: 52.0, violence_impunity_score: 58.0, legal_protection_absence_score: 55.0, stigma_discrimination_score: 60.0, risk_level: "élevé", primary_pattern: "criminalization_rate", estimated_sex_work_rights_index: 5.59, last_updated: "2026-06-20" },
    { entity_id: "SWR-006", name: "Chine — Rééducation Par le Travail, Raflades Régulières & Absence Droits Travail", country: "Asie du Nord-Est", composite_score: 53.9, criminalization_rate_score: 55.0, violence_impunity_score: 50.0, legal_protection_absence_score: 58.0, stigma_discrimination_score: 52.0, risk_level: "élevé", primary_pattern: "criminalization_rate", estimated_sex_work_rights_index: 5.39, last_updated: "2026-06-20" },
    { entity_id: "SWR-007", name: "Nouvelle-Zélande/NZ — Modèle Décriminalisation, Lacunes & Limites Réplication Mondiale", country: "Océanie", composite_score: 27.5, criminalization_rate_score: 22.0, violence_impunity_score: 28.0, legal_protection_absence_score: 30.0, stigma_discrimination_score: 32.0, risk_level: "modéré", primary_pattern: "legal_protection_absence", estimated_sex_work_rights_index: 2.75, last_updated: "2026-06-20" },
    { entity_id: "SWR-008", name: "ONU/OMS/ONUSIDA — Recommandations Décriminalisation & Résistance États Membres", country: "Global", composite_score: 4.4, criminalization_rate_score: 4.0, violence_impunity_score: 5.0, legal_protection_absence_score: 3.0, stigma_discrimination_score: 6.0, risk_level: "faible", primary_pattern: "violence_impunity", estimated_sex_work_rights_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/sex-work-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
