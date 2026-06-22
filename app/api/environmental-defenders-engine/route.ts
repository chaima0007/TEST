import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[environmental-defenders-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Environmental Defenders Engine Agent",
  domain: "environmental_defenders",
  total_entities: 8,
  avg_composite: 60.46,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { criminalization_prosecution: 3, corporate_state_collusion: 2, killings_disappearances: 2, impunity_justice_denial: 1 },
  top_risk_entities: [
    "Honduras/Amérique Centrale — Berta Cáceres, 200 Défenseurs Tués/An & Impunité Totale",
    "Philippines — 200 Défenseurs Tués, Proclamation 32 & Criminalisation Activisme",
    "Brésil/Amazonie — Dom Phillips, Bruno Araújo & Déforestation Industrie Agro",
  ],
  critical_alerts: [
    "Honduras/Amérique Centrale: killings_disappearances",
    "Philippines: criminalization_prosecution",
    "Brésil/Amazonie: corporate_state_collusion",
    "RDC/Congo: impunity_justice_denial",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_environmental_defenders_index: 6.05,
  data_sources: [
    "global_witness_defending_tomorrow_annual_report_environmental_defenders",
    "front_line_defenders_global_analysis_human_rights_defenders_at_risk",
    "un_special_rapporteur_environmental_defenders_annual_report_ohchr",
  ],
  entities: [
    { id: "ED-001", name: "Honduras/Amérique Centrale — Berta Cáceres, 200 Défenseurs Tués/An & Impunité Totale", country: "Amérique Latine", composite_score: 91.5, killings_disappearances_score: 95.0, criminalization_prosecution_score: 88.0, corporate_state_collusion_score: 92.0, impunity_justice_denial_score: 90.0, risk_level: "critique", primary_pattern: "killings_disappearances", estimated_environmental_defenders_index: 9.15, last_updated: "2026-06-20" },
    { id: "ED-002", name: "Philippines — 200 Défenseurs Tués, Proclamation 32 & Criminalisation Activisme", country: "Asie du Sud-Est", composite_score: 88.25, killings_disappearances_score: 88.0, criminalization_prosecution_score: 92.0, corporate_state_collusion_score: 85.0, impunity_justice_denial_score: 88.0, risk_level: "critique", primary_pattern: "criminalization_prosecution", estimated_environmental_defenders_index: 8.83, last_updated: "2026-06-20" },
    { id: "ED-003", name: "Brésil/Amazonie — Dom Phillips, Bruno Araújo & Déforestation Industrie Agro", country: "Amérique Latine", composite_score: 85.1, killings_disappearances_score: 85.0, criminalization_prosecution_score: 78.0, corporate_state_collusion_score: 90.0, impunity_justice_denial_score: 88.0, risk_level: "critique", primary_pattern: "corporate_state_collusion", estimated_environmental_defenders_index: 8.51, last_updated: "2026-06-20" },
    { id: "ED-004", name: "RDC/Congo — Défenseurs Forêts, Parc Virunga & Industrie Extractive Violente", country: "Afrique Sub-Saharienne", composite_score: 77.9, killings_disappearances_score: 78.0, criminalization_prosecution_score: 72.0, corporate_state_collusion_score: 82.0, impunity_justice_denial_score: 80.0, risk_level: "critique", primary_pattern: "impunity_justice_denial", estimated_environmental_defenders_index: 7.79, last_updated: "2026-06-20" },
    { id: "ED-005", name: "Inde — Défenseurs Adivasi, UAPA & Criminalisation Protestataires Environnement", country: "Asie du Sud", composite_score: 55.85, killings_disappearances_score: 52.0, criminalization_prosecution_score: 58.0, corporate_state_collusion_score: 55.0, impunity_justice_denial_score: 60.0, risk_level: "élevé", primary_pattern: "criminalization_prosecution", estimated_environmental_defenders_index: 5.59, last_updated: "2026-06-20" },
    { id: "ED-006", name: "Indonésie — Papouasie, Défenseurs Forêts & Loi Minière Extractiviste", country: "Asie du Sud-Est", composite_score: 53.65, killings_disappearances_score: 50.0, criminalization_prosecution_score: 55.0, corporate_state_collusion_score: 58.0, impunity_justice_denial_score: 52.0, risk_level: "élevé", primary_pattern: "corporate_state_collusion", estimated_environmental_defenders_index: 5.37, last_updated: "2026-06-20" },
    { id: "ED-007", name: "Europe/SLAPP — Poursuites-Bâillons Anti-Environnement, Directive Anti-SLAPP UE", country: "Europe", composite_score: 27.0, killings_disappearances_score: 20.0, criminalization_prosecution_score: 32.0, corporate_state_collusion_score: 28.0, impunity_justice_denial_score: 30.0, risk_level: "modéré", primary_pattern: "criminalization_prosecution", estimated_environmental_defenders_index: 2.7, last_updated: "2026-06-20" },
    { id: "ED-008", name: "ONU/Global Witness/OHCHR — Rapporteur Défenseurs & Déclaration ONU Droits", country: "Global", composite_score: 4.4, killings_disappearances_score: 4.0, criminalization_prosecution_score: 5.0, corporate_state_collusion_score: 3.0, impunity_justice_denial_score: 6.0, risk_level: "faible", primary_pattern: "killings_disappearances", estimated_environmental_defenders_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/environmental-defenders-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
