import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[neuroright-mental-sovereignty-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Neuroright Mental Sovereignty Engine Agent",
  domain: "neuroright_mental_sovereignty",
  total_entities: 8,
  avg_composite: 61.41,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { mental_state_manipulation_risk: 2, neurotechnology_regulation_gap: 2, cognitive_liberty_violation_scale: 2, brain_data_collection_consent_absence: 2 },
  top_risk_entities: [
    "Chine — BCI Militaire, Surveillance Émotions Usines & Neuroimagerie Carcérale Ouïghours",
    "USA/Neuralink — Implants Cérébraux Humains 2024, Données Cerveau Sans Régulation & HIPAA Gap",
    "Corée du Sud — Casques EEG Employés, Brain Score Recrutement & Zéro Cadre Légal Neuro-Data",
  ],
  critical_alerts: [
    "Chine: mental_state_manipulation_risk",
    "USA/Neuralink: neurotechnology_regulation_gap",
    "Corée du Sud: cognitive_liberty_violation_scale",
    "Neuromarketing Global/Amazon-Meta: brain_data_collection_consent_absence",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_neuroright_mental_sovereignty_index: 6.14,
  data_sources: [
    "neurorights_foundation_yuste_five_neurorights_framework",
    "un_ohchr_neurotechnology_human_rights_report_2021",
    "ieee_neuroethics_brain_computer_interface_rights_standards",
  ],
  entities: [
    { id: "NMS-001", name: "Chine — BCI Militaire, Surveillance Émotions Usines & Neuroimagerie Carcérale Ouïghours", country: "Asie de l'Est", composite_score: 93.65, brain_data_collection_consent_absence_score: 95.0, neurotechnology_regulation_gap_score: 92.0, mental_state_manipulation_risk_score: 95.0, cognitive_liberty_violation_scale_score: 92.0, risk_level: "critique", primary_pattern: "mental_state_manipulation_risk", estimated_neuroright_mental_sovereignty_index: 9.37, last_updated: "2026-06-21" },
    { id: "NMS-002", name: "USA/Neuralink — Implants Cérébraux Humains 2024, Données Cerveau Sans Régulation & HIPAA Gap", country: "Amérique du Nord", composite_score: 89.15, brain_data_collection_consent_absence_score: 88.0, neurotechnology_regulation_gap_score: 95.0, mental_state_manipulation_risk_score: 88.0, cognitive_liberty_violation_scale_score: 85.0, risk_level: "critique", primary_pattern: "neurotechnology_regulation_gap", estimated_neuroright_mental_sovereignty_index: 8.92, last_updated: "2026-06-21" },
    { id: "NMS-003", name: "Corée du Sud — Casques EEG Employés, Brain Score Recrutement & Zéro Cadre Légal Neuro-Data", country: "Asie de l'Est", composite_score: 88.4, brain_data_collection_consent_absence_score: 88.0, neurotechnology_regulation_gap_score: 88.0, mental_state_manipulation_risk_score: 88.0, cognitive_liberty_violation_scale_score: 90.0, risk_level: "critique", primary_pattern: "cognitive_liberty_violation_scale", estimated_neuroright_mental_sovereignty_index: 8.84, last_updated: "2026-06-21" },
    { id: "NMS-004", name: "Neuromarketing Global/Amazon-Meta — Scans Cérébraux Consommateurs Sans Consentement Explicite", country: "Global", composite_score: 85.75, brain_data_collection_consent_absence_score: 85.0, neurotechnology_regulation_gap_score: 85.0, mental_state_manipulation_risk_score: 88.0, cognitive_liberty_violation_scale_score: 85.0, risk_level: "critique", primary_pattern: "brain_data_collection_consent_absence", estimated_neuroright_mental_sovereignty_index: 8.58, last_updated: "2026-06-21" },
    { id: "NMS-005", name: "UAE/Russie — Détecteurs Mensonge IA Cerveau Frontières, Interrogatoires & Pas de Recours", country: "Moyen-Orient/Europe de l'Est", composite_score: 53.35, brain_data_collection_consent_absence_score: 52.0, neurotechnology_regulation_gap_score: 55.0, mental_state_manipulation_risk_score: 52.0, cognitive_liberty_violation_scale_score: 55.0, risk_level: "élevé", primary_pattern: "brain_data_collection_consent_absence", estimated_neuroright_mental_sovereignty_index: 5.34, last_updated: "2026-06-21" },
    { id: "NMS-006", name: "UE — AI Act Ne Couvre Pas Neuro-Data, RGPD Insuffisant Données Cérébrales & Gap Régulation", country: "Europe", composite_score: 50.75, brain_data_collection_consent_absence_score: 50.0, neurotechnology_regulation_gap_score: 55.0, mental_state_manipulation_risk_score: 48.0, cognitive_liberty_violation_scale_score: 50.0, risk_level: "élevé", primary_pattern: "neurotechnology_regulation_gap", estimated_neuroright_mental_sovereignty_index: 5.08, last_updated: "2026-06-21" },
    { id: "NMS-007", name: "Neurorights Foundation/Yuste — 5 Neurodroits, Loi Chili 2021 & 30+ Pays Sensibilisés", country: "Global", composite_score: 25.85, brain_data_collection_consent_absence_score: 22.0, neurotechnology_regulation_gap_score: 28.0, mental_state_manipulation_risk_score: 25.0, cognitive_liberty_violation_scale_score: 30.0, risk_level: "modéré", primary_pattern: "cognitive_liberty_violation_scale", estimated_neuroright_mental_sovereignty_index: 2.59, last_updated: "2026-06-21" },
    { id: "NMS-008", name: "ONU/OHCHR — Neurotechnologie & Droits Humains Rapport 2021, ICCPR Art.17 Vie Privée Mentale", country: "Global", composite_score: 4.4, brain_data_collection_consent_absence_score: 4.0, neurotechnology_regulation_gap_score: 5.0, mental_state_manipulation_risk_score: 3.0, cognitive_liberty_violation_scale_score: 6.0, risk_level: "faible", primary_pattern: "mental_state_manipulation_risk", estimated_neuroright_mental_sovereignty_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/neuroright-mental-sovereignty-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
