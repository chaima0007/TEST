import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[indigenous-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Indigenous Rights Engine Agent",
  domain: "indigenous_rights",
  total_entities: 8,
  avg_composite: 60.21,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { territorial_dispossession: 3, cultural_linguistic_erasure: 1, fpic_violation_scale: 3, undrip_implementation_gap: 1 },
  top_risk_entities: [
    "Brésil/Amazonie — Garimpeiros Invasions, Yanomami Génocide Lent & Démantèlement FUNAI",
    "Canada — Pensionnats Génocide Culturel, 215 Enfants Kamloops & MMIWG Non Résolus",
    "Australie — Uluru Statement Ignoré, Surincarcération Aborigène & Terres Non Restituées",
  ],
  critical_alerts: [
    "Brésil/Amazonie: territorial_dispossession",
    "Canada: cultural_linguistic_erasure",
    "Australie: territorial_dispossession",
    "Philippines: fpic_violation_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_indigenous_rights_index: 6.02,
  data_sources: [
    "iwgia_indigenous_world_annual_report",
    "un_special_rapporteur_indigenous_peoples_country_visits_reports",
    "forest_peoples_programme_fpic_violations_global_tracker",
  ],
  entities: [
    { id: "IR-001", name: "Brésil/Amazonie — Garimpeiros Invasions, Yanomami Génocide Lent & Démantèlement FUNAI", country: "Amérique Latine", composite_score: 91.9, territorial_dispossession_score: 95.0, fpic_violation_scale_score: 92.0, cultural_linguistic_erasure_score: 88.0, undrip_implementation_gap_score: 92.0, risk_level: "critique", primary_pattern: "territorial_dispossession", estimated_indigenous_rights_index: 9.19, last_updated: "2026-06-21" },
    { id: "IR-002", name: "Canada — Pensionnats Génocide Culturel, 215 Enfants Kamloops & MMIWG Non Résolus", country: "Amérique du Nord", composite_score: 88.25, territorial_dispossession_score: 88.0, fpic_violation_scale_score: 85.0, cultural_linguistic_erasure_score: 92.0, undrip_implementation_gap_score: 88.0, risk_level: "critique", primary_pattern: "cultural_linguistic_erasure", estimated_indigenous_rights_index: 8.83, last_updated: "2026-06-21" },
    { id: "IR-003", name: "Australie — Uluru Statement Ignoré, Surincarcération Aborigène & Terres Non Restituées", country: "Océanie", composite_score: 84.25, territorial_dispossession_score: 85.0, fpic_violation_scale_score: 82.0, cultural_linguistic_erasure_score: 85.0, undrip_implementation_gap_score: 85.0, risk_level: "critique", primary_pattern: "territorial_dispossession", estimated_indigenous_rights_index: 8.43, last_updated: "2026-06-21" },
    { id: "IR-004", name: "Philippines — Projets Miniers FPIC Bafoués, Défenseurs Terres Assassinés & Militarisation", country: "Asie du Sud-Est", composite_score: 82.5, territorial_dispossession_score: 82.0, fpic_violation_scale_score: 88.0, cultural_linguistic_erasure_score: 78.0, undrip_implementation_gap_score: 82.0, risk_level: "critique", primary_pattern: "fpic_violation_scale", estimated_indigenous_rights_index: 8.25, last_updated: "2026-06-21" },
    { id: "IR-005", name: "USA — Dakota Access Pipeline, Standing Rock Répression & Réserves Sous-financées", country: "Amérique du Nord", composite_score: 54.0, territorial_dispossession_score: 55.0, fpic_violation_scale_score: 58.0, cultural_linguistic_erasure_score: 52.0, undrip_implementation_gap_score: 50.0, risk_level: "élevé", primary_pattern: "fpic_violation_scale", estimated_indigenous_rights_index: 5.4, last_updated: "2026-06-21" },
    { id: "IR-006", name: "Norvège/Sápmi — Éoliennes Fosen FPIC Non Respecté, Jeûne Sami & Arrêt Cour Non Appliqué", country: "Europe du Nord", composite_score: 50.55, territorial_dispossession_score: 48.0, fpic_violation_scale_score: 55.0, cultural_linguistic_erasure_score: 48.0, undrip_implementation_gap_score: 52.0, risk_level: "élevé", primary_pattern: "fpic_violation_scale", estimated_indigenous_rights_index: 5.06, last_updated: "2026-06-21" },
    { id: "IR-007", name: "IWGIA/Forest Peoples Programme — Réseau Mondial, Documentation & Plaidoyer UNDRIP", country: "Global", composite_score: 25.85, territorial_dispossession_score: 22.0, fpic_violation_scale_score: 25.0, cultural_linguistic_erasure_score: 28.0, undrip_implementation_gap_score: 30.0, risk_level: "modéré", primary_pattern: "territorial_dispossession", estimated_indigenous_rights_index: 2.59, last_updated: "2026-06-21" },
    { id: "IR-008", name: "ONU/UNDRIP — Déclaration Droits Peuples Autochtones 2007, Instance Permanente & Rapporteur", country: "Global", composite_score: 4.4, territorial_dispossession_score: 4.0, fpic_violation_scale_score: 5.0, cultural_linguistic_erasure_score: 3.0, undrip_implementation_gap_score: 6.0, risk_level: "faible", primary_pattern: "undrip_implementation_gap", estimated_indigenous_rights_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/indigenous-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
