import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[cultural-heritage-destruction-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Cultural Heritage Destruction Engine Agent",
  domain: "cultural_heritage_destruction",
  total_entities: 8,
  avg_composite: 60.24,
  confidence_score: 0.82,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { deliberate_destruction_scale: 3, cultural_identity_erasure: 2, looting_trafficking: 2, impunity_accountability_gap: 1 },
  top_risk_entities: [
    "Irak/Syrie/Daech — Palmyre, Nimroud, Bibliothèque Mossoul & Destruction Systématique",
    "Mali/Tombouctou — Mausolées UNESCO, Manuscrits Brûlés & Destruction Ansar Dine",
    "Chine/Tibet/Ouïghours — Mosquées Rasées, Monastères Détruits & Sinisation Culturelle",
  ],
  critical_alerts: [
    "Irak/Syrie/Daech: deliberate_destruction_scale",
    "Mali/Tombouctou: impunity_accountability_gap",
    "Chine/Tibet/Ouïghours: cultural_identity_erasure",
    "Yémen: looting_trafficking",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_cultural_heritage_destruction_index: 6.02,
  data_sources: [
    "unesco_report_on_illicit_trafficking_cultural_property_annual",
    "interpol_works_of_art_unit_stolen_cultural_property_global_report",
    "aliph_international_alliance_protection_heritage_conflict_areas_annual",
  ],
  entities: [
    { entity_id: "CHD-001", name: "Irak/Syrie/Daech — Palmyre, Nimroud, Bibliothèque Mossoul & Destruction Systématique", country: "Moyen-Orient", composite_score: 91.6, deliberate_destruction_scale_score: 95.0, looting_trafficking_score: 90.0, cultural_identity_erasure_score: 92.0, impunity_accountability_gap_score: 88.0, risk_level: "critique", primary_pattern: "deliberate_destruction_scale", estimated_cultural_heritage_destruction_index: 9.16, last_updated: "2026-06-20" },
    { entity_id: "CHD-002", name: "Chine/Tibet/Ouïghours — Mosquées Rasées, Monastères Détruits & Sinisation Culturelle", country: "Asie du Nord-Est", composite_score: 82.5, deliberate_destruction_scale_score: 85.0, looting_trafficking_score: 72.0, cultural_identity_erasure_score: 92.0, impunity_accountability_gap_score: 80.0, risk_level: "critique", primary_pattern: "cultural_identity_erasure", estimated_cultural_heritage_destruction_index: 8.25, last_updated: "2026-06-20" },
    { entity_id: "CHD-003", name: "Mali/Tombouctou — Mausolées UNESCO, Manuscrits Brûlés & Destruction Ansar Dine", country: "Afrique Sub-Saharienne", composite_score: 85.85, deliberate_destruction_scale_score: 82.0, looting_trafficking_score: 85.0, cultural_identity_erasure_score: 88.0, impunity_accountability_gap_score: 90.0, risk_level: "critique", primary_pattern: "impunity_accountability_gap", estimated_cultural_heritage_destruction_index: 8.59, last_updated: "2026-06-20" },
    { entity_id: "CHD-004", name: "Yémen — Patrimoine Millénaire, Bombardements Sana'a, Marib Pillés & Guerre Coalition", country: "Moyen-Orient", composite_score: 81.0, deliberate_destruction_scale_score: 80.0, looting_trafficking_score: 78.0, cultural_identity_erasure_score: 82.0, impunity_accountability_gap_score: 85.0, risk_level: "critique", primary_pattern: "looting_trafficking", estimated_cultural_heritage_destruction_index: 8.1, last_updated: "2026-06-20" },
    { entity_id: "CHD-005", name: "Ukraine — Patrimoine Détruit par Russie, Monuments Volés & Effacement Identité Culturelle", country: "Europe de l'Est", composite_score: 54.0, deliberate_destruction_scale_score: 55.0, looting_trafficking_score: 58.0, cultural_identity_erasure_score: 52.0, impunity_accountability_gap_score: 50.0, risk_level: "élevé", primary_pattern: "deliberate_destruction_scale", estimated_cultural_heritage_destruction_index: 5.4, last_updated: "2026-06-20" },
    { entity_id: "CHD-006", name: "Afghanistan/Bamiyan — Bouddhas Détruits Taliban, Trafic Antiquités & Insécurité Totale", country: "Asie Centrale", composite_score: 54.1, deliberate_destruction_scale_score: 52.0, looting_trafficking_score: 60.0, cultural_identity_erasure_score: 50.0, impunity_accountability_gap_score: 55.0, risk_level: "élevé", primary_pattern: "looting_trafficking", estimated_cultural_heritage_destruction_index: 5.41, last_updated: "2026-06-20" },
    { entity_id: "CHD-007", name: "Musées Occident — Restitution Coloniale, Bronzes Bénin, Elgin Marbles & Blocage Légal", country: "Europe/Amérique du Nord", composite_score: 28.45, deliberate_destruction_scale_score: 22.0, looting_trafficking_score: 35.0, cultural_identity_erasure_score: 30.0, impunity_accountability_gap_score: 28.0, risk_level: "modéré", primary_pattern: "cultural_identity_erasure", estimated_cultural_heritage_destruction_index: 2.85, last_updated: "2026-06-20" },
    { entity_id: "CHD-008", name: "UNESCO/INTERPOL/CPI — Convention 1954, Résolution Al-Mahdi, ALIPH & Bouclier Bleu", country: "Global", composite_score: 4.4, deliberate_destruction_scale_score: 4.0, looting_trafficking_score: 5.0, cultural_identity_erasure_score: 3.0, impunity_accountability_gap_score: 6.0, risk_level: "faible", primary_pattern: "deliberate_destruction_scale", estimated_cultural_heritage_destruction_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/cultural-heritage-destruction-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
