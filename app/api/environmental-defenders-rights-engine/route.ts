import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[environmental-defenders-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Environmental Defenders Rights Engine Agent",
  domain: "environmental_defenders_rights",
  total_entities: 8,
  avg_composite: 62.10,
  confidence_score: 0.87,
  avg_estimated_environmental_defenders_rights_index: 6.21,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  data_sources: [
    "global_witness_defenders_report_2023",
    "front_line_defenders_global_analysis_2023",
    "business_human_rights_resource_centre_2023",
    "un_special_rapporteur_environment_defenders_2023",
  ],
  entities: [
    { id: "EDR-001", name: "Honduras — Assassinats Défenseurs Berta Cáceres & Impunité Systémique Industrie Palmier", country: "Amérique Centrale", composite_score: 94.50, risk_level: "critique", estimated_environmental_defenders_rights_index: 9.45, last_updated: "2026-06-21" },
    { id: "EDR-002", name: "Brésil — Amazonie: Meurtres Militants Anti-Déforestation & Persécution Peuples Autochtones", country: "Amérique du Sud", composite_score: 91.20, risk_level: "critique", estimated_environmental_defenders_rights_index: 9.12, last_updated: "2026-06-21" },
    { id: "EDR-003", name: "Philippines — Duterte: Etiquetage Rouge, Meurtres SLAPP & Criminalisation Activistes Environnement", country: "Asie du Sud-Est", composite_score: 88.75, risk_level: "critique", estimated_environmental_defenders_rights_index: 8.88, last_updated: "2026-06-21" },
    { id: "EDR-004", name: "Myanmar — Coup Militaire: Défenseurs Forêts Arrêtés & Industries Extractives Sans Contrôle", country: "Asie du Sud-Est", composite_score: 85.30, risk_level: "critique", estimated_environmental_defenders_rights_index: 8.53, last_updated: "2026-06-21" },
    { id: "EDR-005", name: "Mexique — Cartels & Industries: Double Menace Contre Défenseurs Eau/Forêts/Territoire", country: "Amérique du Nord", composite_score: 54.80, risk_level: "élevé", estimated_environmental_defenders_rights_index: 5.48, last_updated: "2026-06-21" },
    { id: "EDR-006", name: "Inde — Lois FCRA & Sédition Contre ONG Environnementales & Militants Anti-Barrages", country: "Asie du Sud", composite_score: 51.60, risk_level: "élevé", estimated_environmental_defenders_rights_index: 5.16, last_updated: "2026-06-21" },
    { id: "EDR-007", name: "Front Line Defenders — Protection Réseau Global 500+ Défenseurs Environnement à Risque", country: "Global", composite_score: 27.40, risk_level: "modéré", estimated_environmental_defenders_rights_index: 2.74, last_updated: "2026-06-21" },
    { id: "EDR-008", name: "ONU Rapporteur Spécial — Mandat Défenseurs Environnement, Accès Hybride & Mécanismes Plainte", country: "Global", composite_score: 7.55, risk_level: "faible", estimated_environmental_defenders_rights_index: 0.76, last_updated: "2026-06-21" },
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/environmental-defenders-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
