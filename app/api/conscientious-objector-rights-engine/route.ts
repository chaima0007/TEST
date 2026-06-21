import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[conscientious-objector-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Conscientious Objector Rights Engine Agent",
  domain: "conscientious_objector_rights",
  total_entities: 8,
  avg_composite: 61.41,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { legal_recognition_gap: 3, criminalization_prosecution_scale: 1, alternative_service_availability: 2, persecution_harassment_pattern: 2 },
  top_risk_entities: [
    "Russie — Objecteurs Ukraine Emprisonnés, Mobilisation Forcée 300K & Torture Rapportée",
    "Corée du Sud — 600+ Emprisonnements/An Témoins Jéhovah & CDH ONU Condamné 18 Fois",
    "Érythrée — Conscription à Vie, Objecteurs Camp Sawa Torturés & Fuite Massive vers Europe",
  ],
  critical_alerts: [
    "Russie: legal_recognition_gap",
    "Corée du Sud: criminalization_prosecution_scale",
    "Érythrée: alternative_service_availability",
    "Turquie: legal_recognition_gap",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_conscientious_objector_rights_index: 6.14,
  data_sources: [
    "war_resisters_international_conscientious_objection_country_report",
    "amnesty_international_prisoners_of_conscience_conscription_report",
    "un_commission_human_rights_resolution_conscientious_objection",
  ],
  entities: [
    { entity_id: "CO-001", name: "Russie — Objecteurs Ukraine Emprisonnés, Mobilisation Forcée 300K & Torture Rapportée", country: "Europe de l'Est", composite_score: 93.65, criminalization_prosecution_scale_score: 95.0, alternative_service_availability_score: 92.0, legal_recognition_gap_score: 95.0, persecution_harassment_pattern_score: 92.0, risk_level: "critique", primary_pattern: "legal_recognition_gap", estimated_conscientious_objector_rights_index: 9.37, last_updated: "2026-06-21" },
    { entity_id: "CO-002", name: "Corée du Sud — 600+ Emprisonnements/An Témoins Jéhovah & CDH ONU Condamné 18 Fois", country: "Asie de l'Est", composite_score: 90.0, criminalization_prosecution_scale_score: 90.0, alternative_service_availability_score: 88.0, legal_recognition_gap_score: 92.0, persecution_harassment_pattern_score: 90.0, risk_level: "critique", primary_pattern: "criminalization_prosecution_scale", estimated_conscientious_objector_rights_index: 9.0, last_updated: "2026-06-21" },
    { entity_id: "CO-003", name: "Érythrée — Conscription à Vie, Objecteurs Camp Sawa Torturés & Fuite Massive vers Europe", country: "Afrique de l'Est", composite_score: 88.5, criminalization_prosecution_scale_score: 88.0, alternative_service_availability_score: 90.0, legal_recognition_gap_score: 88.0, persecution_harassment_pattern_score: 88.0, risk_level: "critique", primary_pattern: "alternative_service_availability", estimated_conscientious_objector_rights_index: 8.85, last_updated: "2026-06-21" },
    { entity_id: "CO-004", name: "Turquie — Aucune Loi OC Reconnue, Poursuites Répétées Büyükanıt & CEDH Condamné 15x", country: "Moyen-Orient", composite_score: 85.75, criminalization_prosecution_scale_score: 85.0, alternative_service_availability_score: 85.0, legal_recognition_gap_score: 88.0, persecution_harassment_pattern_score: 85.0, risk_level: "critique", primary_pattern: "legal_recognition_gap", estimated_conscientious_objector_rights_index: 8.58, last_updated: "2026-06-21" },
    { entity_id: "CO-005", name: "Israël — OC Partiel, Prisonniers Conscience Femmes Bédouines & Traitement Discriminatoire", country: "Moyen-Orient", composite_score: 53.65, criminalization_prosecution_scale_score: 55.0, alternative_service_availability_score: 52.0, legal_recognition_gap_score: 55.0, persecution_harassment_pattern_score: 52.0, risk_level: "élevé", primary_pattern: "persecution_harassment_pattern", estimated_conscientious_objector_rights_index: 5.37, last_updated: "2026-06-21" },
    { entity_id: "CO-006", name: "Grèce — Service Civil Punitif 2x Militaire, Réforme 2019 Incomplète & Discrimination Persist.", country: "Europe", composite_score: 49.5, criminalization_prosecution_scale_score: 50.0, alternative_service_availability_score: 48.0, legal_recognition_gap_score: 50.0, persecution_harassment_pattern_score: 50.0, risk_level: "élevé", primary_pattern: "alternative_service_availability", estimated_conscientious_objector_rights_index: 4.95, last_updated: "2026-06-21" },
    { entity_id: "CO-007", name: "War Resisters International/Amnesty — Monitoring OC Global, Prisonniers Conscience & Plaidoyer", country: "Global", composite_score: 25.85, criminalization_prosecution_scale_score: 22.0, alternative_service_availability_score: 28.0, legal_recognition_gap_score: 25.0, persecution_harassment_pattern_score: 30.0, risk_level: "modéré", primary_pattern: "persecution_harassment_pattern", estimated_conscientious_objector_rights_index: 2.59, last_updated: "2026-06-21" },
    { entity_id: "CO-008", name: "ONU/CDH — Résolution 1998/77 Objection Conscience, CCPR Art.18 & Comité Droits Humains", country: "Global", composite_score: 4.4, criminalization_prosecution_scale_score: 4.0, alternative_service_availability_score: 5.0, legal_recognition_gap_score: 3.0, persecution_harassment_pattern_score: 6.0, risk_level: "faible", primary_pattern: "legal_recognition_gap", estimated_conscientious_objector_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/conscientious-objector-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
