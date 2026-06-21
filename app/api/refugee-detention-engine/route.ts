import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[refugee-detention-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Refugee Detention Engine Agent",
  domain: "refugee_detention",
  total_entities: 8,
  avg_composite: 59.91,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { inhumane_conditions: 1, legal_access_denial: 2, arbitrary_detention_scale: 2, pushback_refoulement: 3 },
  top_risk_entities: [
    "Libye — Centres Détention Milices, Tortures/Viols Documentés & Financement UE Complicité",
    "Australie/Nauru — Offshore Detention, Manus Island Fermé/Remplacé & Limbes Juridiques",
    "USA/Immigration — Centres ICE Privés, Décès en Détention & Séparation Familles Frontière",
  ],
  critical_alerts: [
    "Libye: inhumane_conditions",
    "Australie/Nauru: legal_access_denial",
    "USA/Immigration: arbitrary_detention_scale",
    "Grèce/Turquie: pushback_refoulement",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_refugee_detention_index: 5.99,
  data_sources: [
    "global_detention_project_immigration_detention_global_report",
    "unhcr_global_trends_forced_displacement_annual_report",
    "human_rights_watch_refugee_detention_conditions_global_audit",
  ],
  entities: [
    { id: "RD-001", name: "Libye — Centres Détention Milices, Tortures/Viols Documentés & Financement UE Complicité", country: "Afrique du Nord", composite_score: 93.25, arbitrary_detention_scale_score: 95.0, inhumane_conditions_score: 95.0, legal_access_denial_score: 92.0, pushback_refoulement_score: 90.0, risk_level: "critique", primary_pattern: "inhumane_conditions", estimated_refugee_detention_index: 9.33, last_updated: "2026-06-21" },
    { id: "RD-002", name: "Australie/Nauru — Offshore Detention, Manus Island Fermé/Remplacé & Limbes Juridiques", country: "Océanie", composite_score: 87.75, arbitrary_detention_scale_score: 88.0, inhumane_conditions_score: 85.0, legal_access_denial_score: 90.0, pushback_refoulement_score: 88.0, risk_level: "critique", primary_pattern: "legal_access_denial", estimated_refugee_detention_index: 8.78, last_updated: "2026-06-21" },
    { id: "RD-003", name: "USA/Immigration — Centres ICE Privés, Décès en Détention & Séparation Familles Frontière", country: "Amérique du Nord", composite_score: 83.0, arbitrary_detention_scale_score: 85.0, inhumane_conditions_score: 82.0, legal_access_denial_score: 80.0, pushback_refoulement_score: 85.0, risk_level: "critique", primary_pattern: "arbitrary_detention_scale", estimated_refugee_detention_index: 8.3, last_updated: "2026-06-21" },
    { id: "RD-004", name: "Grèce/Turquie — Pushbacks Illégaux Égée, Camps Surpeuplés & Violations Art.33 Convention", country: "Europe", composite_score: 81.0, arbitrary_detention_scale_score: 80.0, inhumane_conditions_score: 82.0, legal_access_denial_score: 78.0, pushback_refoulement_score: 85.0, risk_level: "critique", primary_pattern: "pushback_refoulement", estimated_refugee_detention_index: 8.1, last_updated: "2026-06-21" },
    { id: "RD-005", name: "Bangladesh/Rohingyas — Cox's Bazar 1M Réfugiés, Restriction Liberté & Retour Forcé Myanmar", country: "Asie du Sud", composite_score: 54.25, arbitrary_detention_scale_score: 52.0, inhumane_conditions_score: 55.0, legal_access_denial_score: 58.0, pushback_refoulement_score: 52.0, risk_level: "élevé", primary_pattern: "pushback_refoulement", estimated_refugee_detention_index: 5.43, last_updated: "2026-06-21" },
    { id: "RD-006", name: "UE/Rwanda Plan — Externalisation Asile, Accord UK-Rwanda & Détention Expéditive", country: "Europe", composite_score: 49.8, arbitrary_detention_scale_score: 48.0, inhumane_conditions_score: 45.0, legal_access_denial_score: 55.0, pushback_refoulement_score: 52.0, risk_level: "élevé", primary_pattern: "legal_access_denial", estimated_refugee_detention_index: 4.98, last_updated: "2026-06-21" },
    { id: "RD-007", name: "UNHCR/ECRE — Plaidoyer Anti-Détention, Alternatives & Standards Minima Protection", country: "Global", composite_score: 25.85, arbitrary_detention_scale_score: 22.0, inhumane_conditions_score: 25.0, legal_access_denial_score: 28.0, pushback_refoulement_score: 30.0, risk_level: "modéré", primary_pattern: "arbitrary_detention_scale", estimated_refugee_detention_index: 2.59, last_updated: "2026-06-21" },
    { id: "RD-008", name: "ONU/Convention 1951 — Statut Réfugiés, Protocole 1967 & Principe Non-Refoulement", country: "Global", composite_score: 4.4, arbitrary_detention_scale_score: 4.0, inhumane_conditions_score: 5.0, legal_access_denial_score: 3.0, pushback_refoulement_score: 6.0, risk_level: "faible", primary_pattern: "pushback_refoulement", estimated_refugee_detention_index: 0.44, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/refugee-detention-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
