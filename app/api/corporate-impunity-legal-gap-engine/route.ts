import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[corporate-impunity-legal-gap-engine] SWARM_API_URL not set — using mock data");
}

const MOCK = {
  domain: "corporate_impunity_legal_gap",
  generated_at: new Date().toISOString(),
  accent: "#7c3aed",
  avg_composite: 61.56,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  entities: [
    { id: "CIL-001", name: "Shell Nigeria — 50 Ans Impunité Pétrole Delta Niger, 0 Condamné", composite_score: 93.15, risk_level: "critique", corporate_liability_evasion_score: 95, victim_access_justice_barrier_score: 94, extraterritorial_jurisdiction_gap_score: 91, enforcement_capacity_deficit_score: 92, estimated_corporate_impunity_legal_gap_index: 9.32 },
    { id: "CIL-002", name: "Chevron Ecuador — Procès 20 Ans, Jugement 9.5Mds$ Non Exécuté", composite_score: 88.15, risk_level: "critique", corporate_liability_evasion_score: 90, victim_access_justice_barrier_score: 88, extraterritorial_jurisdiction_gap_score: 87, enforcement_capacity_deficit_score: 87, estimated_corporate_impunity_legal_gap_index: 8.82 },
    { id: "CIL-003", name: "Glencore DRC — Cobalt Enfants, Procédures Belgique Bloquées", composite_score: 84.95, risk_level: "critique", corporate_liability_evasion_score: 87, victim_access_justice_barrier_score: 85, extraterritorial_jurisdiction_gap_score: 84, enforcement_capacity_deficit_score: 83, estimated_corporate_impunity_legal_gap_index: 8.50 },
    { id: "CIL-004", name: "Facebook Myanmar — Génocide Amplifié, Immunité Section 230 USA", composite_score: 81.05, risk_level: "critique", corporate_liability_evasion_score: 78, victim_access_justice_barrier_score: 80, extraterritorial_jurisdiction_gap_score: 85, enforcement_capacity_deficit_score: 82, estimated_corporate_impunity_legal_gap_index: 8.11 },
    { id: "CIL-005", name: "Nestlé Côte d'Ivoire — Travail Enfants Cacao, Procès SCOTUS Rejeté", composite_score: 57.10, risk_level: "élevé", corporate_liability_evasion_score: 58, victim_access_justice_barrier_score: 56, extraterritorial_jurisdiction_gap_score: 58, enforcement_capacity_deficit_score: 56, estimated_corporate_impunity_legal_gap_index: 5.71 },
    { id: "CIL-006", name: "H&M Bangladesh — Effondrement Rana Plaza, Compensations Partielles", composite_score: 52.10, risk_level: "élevé", corporate_liability_evasion_score: 54, victim_access_justice_barrier_score: 52, extraterritorial_jurisdiction_gap_score: 50, enforcement_capacity_deficit_score: 52, estimated_corporate_impunity_legal_gap_index: 5.21 },
    { id: "CIL-007", name: "Apple-Foxconn — Accord Moniteur Indépendant, Améliorations Partielles", composite_score: 27.05, risk_level: "modéré", corporate_liability_evasion_score: 28, victim_access_justice_barrier_score: 27, extraterritorial_jurisdiction_gap_score: 26, enforcement_capacity_deficit_score: 27, estimated_corporate_impunity_legal_gap_index: 2.71 },
    { id: "CIL-008", name: "Patagonia — Traçabilité Totale, B-Corp, Engagements Légaux Volontaires", composite_score: 8.95, risk_level: "faible", corporate_liability_evasion_score: 8, victim_access_justice_barrier_score: 9, extraterritorial_jurisdiction_gap_score: 10, enforcement_capacity_deficit_score: 9, estimated_corporate_impunity_legal_gap_index: 0.90 },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return sealResponse(NextResponse.json(await sealResponse(MOCK)));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/corporate-impunity-legal-gap-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(await sealResponse(data.payload ?? data)));
  } catch {
    return sealResponse(NextResponse.json(await sealResponse(MOCK), { status: 502 }));
  }
}
