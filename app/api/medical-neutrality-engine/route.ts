import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[medical-neutrality-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Medical Neutrality Engine Agent",
  domain: "medical_neutrality",
  total_entities: 8,
  avg_composite: 60.31,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { medical_access_denial: 2, healthcare_workers_targeting: 2, accountability_impunity: 2, attacks_medical_facilities: 2 },
  top_risk_entities: [
    "Syrie — 600+ Hôpitaux Bombardés, Barrel Bombs Assad & Double-Tap sur Secouristes",
    "Gaza/Palestine — Hôpitaux Al-Shifa/Al-Ahli Détruits, Pénurie Médicale & Médecins Tués",
    "Yémen — Frappes Hôpitaux Coalition Saoudienne, Choléra & Blocus Médicaments",
  ],
  critical_alerts: [
    "Syrie: medical_access_denial",
    "Gaza/Palestine: medical_access_denial",
    "Yémen: healthcare_workers_targeting",
    "Ukraine: accountability_impunity",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_medical_neutrality_index: 6.03,
  data_sources: [
    "physicians_for_human_rights_attack_on_health_care_global_report",
    "msf_not_a_target_attacks_hospitals_healthcare_conflict_report",
    "who_ssa_surveillance_system_attacks_healthcare_database",
  ],
  entities: [
    { entity_id: "MN-001", name: "Syrie — 600+ Hôpitaux Bombardés, Barrel Bombs Assad & Double-Tap sur Secouristes", country: "Moyen-Orient", composite_score: 91.45, attacks_medical_facilities_score: 92.0, healthcare_workers_targeting_score: 90.0, medical_access_denial_score: 95.0, accountability_impunity_score: 88.0, risk_level: "critique", primary_pattern: "medical_access_denial", estimated_medical_neutrality_index: 9.15, last_updated: "2026-06-20" },
    { entity_id: "MN-002", name: "Gaza/Palestine — Hôpitaux Al-Shifa/Al-Ahli Détruits, Pénurie Médicale & Médecins Tués", country: "Moyen-Orient", composite_score: 88.85, attacks_medical_facilities_score: 90.0, healthcare_workers_targeting_score: 85.0, medical_access_denial_score: 92.0, accountability_impunity_score: 88.0, risk_level: "critique", primary_pattern: "medical_access_denial", estimated_medical_neutrality_index: 8.89, last_updated: "2026-06-20" },
    { entity_id: "MN-003", name: "Yémen — Frappes Hôpitaux Coalition Saoudienne, Choléra & Blocus Médicaments", country: "Moyen-Orient", composite_score: 87.9, attacks_medical_facilities_score: 88.0, healthcare_workers_targeting_score: 90.0, medical_access_denial_score: 88.0, accountability_impunity_score: 85.0, risk_level: "critique", primary_pattern: "healthcare_workers_targeting", estimated_medical_neutrality_index: 8.79, last_updated: "2026-06-20" },
    { entity_id: "MN-004", name: "Ukraine — Hôpitaux Marioupol/Kherson Bombardés, MSF Évacuations & Crimes de Guerre Russes", country: "Europe de l'Est", composite_score: 78.55, attacks_medical_facilities_score: 78.0, healthcare_workers_targeting_score: 80.0, medical_access_denial_score: 75.0, accountability_impunity_score: 82.0, risk_level: "critique", primary_pattern: "accountability_impunity", estimated_medical_neutrality_index: 7.86, last_updated: "2026-06-20" },
    { entity_id: "MN-005", name: "Éthiopie/Tigré — Cliniques Pillées, Viol Personnel Médical & Famine Obstruction Aide", country: "Afrique Sub-Saharienne", composite_score: 53.85, attacks_medical_facilities_score: 52.0, healthcare_workers_targeting_score: 58.0, medical_access_denial_score: 55.0, accountability_impunity_score: 50.0, risk_level: "élevé", primary_pattern: "healthcare_workers_targeting", estimated_medical_neutrality_index: 5.39, last_updated: "2026-06-20" },
    { entity_id: "MN-006", name: "Myanmar — Raids Militaires Cliniques, Médecins Arrêtés & Soins Refusés Minorités", country: "Asie du Sud-Est", composite_score: 51.35, attacks_medical_facilities_score: 50.0, healthcare_workers_targeting_score: 55.0, medical_access_denial_score: 52.0, accountability_impunity_score: 48.0, risk_level: "élevé", primary_pattern: "attacks_medical_facilities", estimated_medical_neutrality_index: 5.14, last_updated: "2026-06-20" },
    { entity_id: "MN-007", name: "MSF/CICR — Reporting Violations, Safe Access Négociations & Plaidoyer Humanitaire", country: "Global", composite_score: 26.1, attacks_medical_facilities_score: 22.0, healthcare_workers_targeting_score: 28.0, medical_access_denial_score: 30.0, accountability_impunity_score: 25.0, risk_level: "modéré", primary_pattern: "attacks_medical_facilities", estimated_medical_neutrality_index: 2.61, last_updated: "2026-06-20" },
    { entity_id: "MN-008", name: "ONU/OMS — Résolution WHA65.20, Monitoring SSA & Mécanisme Rapportage Attaques", country: "Global", composite_score: 4.4, attacks_medical_facilities_score: 4.0, healthcare_workers_targeting_score: 5.0, medical_access_denial_score: 3.0, accountability_impunity_score: 6.0, risk_level: "faible", primary_pattern: "accountability_impunity", estimated_medical_neutrality_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/medical-neutrality-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
