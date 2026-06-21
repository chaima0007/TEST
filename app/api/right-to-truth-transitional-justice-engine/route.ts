import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[right-to-truth-transitional-justice-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "right_to_truth_transitional_justice",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "RTT-001", name: "Corée du Nord — Aucun Mécanisme, Crimes Humanité Systématiques & COI ONU Ignoré", composite_score: 95.55, risk_level: "critique", estimated_transitional_justice_index: 9.56 },
    { id: "RTT-002", name: "Syrie — Tribunal International Absent, Crimes Assad & Mécanisme IIIM ONU Limité", composite_score: 91.30, risk_level: "critique", estimated_transitional_justice_index: 9.13 },
    { id: "RTT-003", name: "Chine Tiananmen — Déni Total 35 Ans, Victimes Sans Réparation & Mémoire Censurée", composite_score: 87.30, risk_level: "critique", estimated_transitional_justice_index: 8.73 },
    { id: "RTT-004", name: "Cambodge ECCC — Khmers Rouges, Lenteur Tribunal & Impunité Cadres Intermédiaires", composite_score: 67.30, risk_level: "critique", estimated_transitional_justice_index: 6.73 },
    { id: "RTT-005", name: "Colombie JEP — Justice Spéciale Paix, Résultats Mitigés & Réintégration FARC", composite_score: 53.30, risk_level: "élevé", estimated_transitional_justice_index: 5.33 },
    { id: "RTT-006", name: "Kenya TJRC — Commission Vérité Ignorée, Rapport 2013 Non Appliqué & Impunité Élites", composite_score: 46.70, risk_level: "élevé", estimated_transitional_justice_index: 4.67 },
    { id: "RTT-007", name: "Tunisie IVD — Instance Vérité Dignité, Application Partielle & Transition Fragile", composite_score: 28.70, risk_level: "modéré", estimated_transitional_justice_index: 2.87 },
    { id: "RTT-008", name: "Afrique du Sud CVR — Commission Vérité Réconciliation, Modèle Mandela & Réparations", composite_score: 12.45, risk_level: "faible", estimated_transitional_justice_index: 1.25 },
  ],
  avg_composite: 60.32,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/right-to-truth-transitional-justice-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
