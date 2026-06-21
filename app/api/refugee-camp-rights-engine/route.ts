import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[refugee-camp-rights-engine] SWARM_API_URL not set — using mock data");
}

const MOCK = {
  domain: "refugee_camp_rights",
  generated_at: new Date().toISOString(),
  accent: "#0891b2",
  avg_composite: 60.99,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  entities: [
    { id: "RCR-001", name: "Cox's Bazar Bangladesh — 900K Rohingyas, Surpopulation Catastrophique", composite_score: 93.75, risk_level: "critique", camp_living_conditions_score: 98, protection_from_violence_score: 92, freedom_of_movement_score: 95, legal_status_access_score: 88, estimated_refugee_camp_rights_index: 9.38 },
    { id: "RCR-002", name: "Dadaab Kenya — 220K Réfugiés 30 Ans, Conditions Dégradées", composite_score: 87.30, risk_level: "critique", camp_living_conditions_score: 90, protection_from_violence_score: 88, freedom_of_movement_score: 86, legal_status_access_score: 84, estimated_refugee_camp_rights_index: 8.73 },
    { id: "RCR-003", name: "Zaatari Jordanie — 80K Syriens, Accès Eau Limité & Violences", composite_score: 84.35, risk_level: "critique", camp_living_conditions_score: 87, protection_from_violence_score: 85, freedom_of_movement_score: 84, legal_status_access_score: 80, estimated_refugee_camp_rights_index: 8.44 },
    { id: "RCR-004", name: "Moria Lesbos Grèce — Surpopulation Extrême, Incendie 2020", composite_score: 81.20, risk_level: "critique", camp_living_conditions_score: 85, protection_from_violence_score: 82, freedom_of_movement_score: 80, legal_status_access_score: 76, estimated_refugee_camp_rights_index: 8.12 },
    { id: "RCR-005", name: "Kakuma Kenya — 190K Réfugiés, Services Insuffisants", composite_score: 55.40, risk_level: "élevé", camp_living_conditions_score: 58, protection_from_violence_score: 55, freedom_of_movement_score: 57, legal_status_access_score: 50, estimated_refugee_camp_rights_index: 5.54 },
    { id: "RCR-006", name: "Nyarugusu Tanzanie — 150K Congolais, Rations Réduites", composite_score: 50.60, risk_level: "élevé", camp_living_conditions_score: 53, protection_from_violence_score: 50, freedom_of_movement_score: 52, legal_status_access_score: 46, estimated_refugee_camp_rights_index: 5.06 },
    { id: "RCR-007", name: "Azraq Jordanie — Meilleure Gestion, Énergie Solaire", composite_score: 26.65, risk_level: "modéré", camp_living_conditions_score: 28, protection_from_violence_score: 26, freedom_of_movement_score: 27, legal_status_access_score: 25, estimated_refugee_camp_rights_index: 2.67 },
    { id: "RCR-008", name: "Za'atari Amélioration — Nouvelles Infrastructures UNHCR", composite_score: 8.65, risk_level: "faible", camp_living_conditions_score: 10, protection_from_violence_score: 9, freedom_of_movement_score: 8, legal_status_access_score: 7, estimated_refugee_camp_rights_index: 0.87 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/refugee-camp-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
