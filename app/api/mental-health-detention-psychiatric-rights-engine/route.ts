import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[mental-health-detention-psychiatric-rights-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "mental-health-detention-psychiatric-rights-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "MHD-001", name: "Russie/Psychiatrie Punitive Héritée — Opposants Internés, Psikhushka Modernisé", composite_score: 91.85, risk_level: "critique", estimated_mental_health_rights_index: 9.19 },
    { id: "MHD-002", name: "Chine/Ankang Centres Détention Psychiatrique — Dissidents Pétitionnaires Internés", composite_score: 87.85, risk_level: "critique", estimated_mental_health_rights_index: 8.79 },
    { id: "MHD-003", name: "Indonésie/Pasung Enchaînement Malades Mentaux — 18 000 Cas Documentés, Pratique Traditionnelle", composite_score: 83.65, risk_level: "critique", estimated_mental_health_rights_index: 8.37 },
    { id: "MHD-004", name: "Nigeria/Prayer Camps Détention Religieuse — 700 000 Sans Soins Psychiatriques", composite_score: 78.65, risk_level: "critique", estimated_mental_health_rights_index: 7.87 },
    { id: "MHD-005", name: "USA/Psychiatrisation Carcérale — 2M Détenus Troubles Mentaux, Soins Insuffisants", composite_score: 53.65, risk_level: "élevé", estimated_mental_health_rights_index: 5.37 },
    { id: "MHD-006", name: "France/Hospitalisation Sans Consentement — 92 000/An, Contrôle Judiciaire Insuffisant", composite_score: 45.65, risk_level: "élevé", estimated_mental_health_rights_index: 4.56 },
    { id: "MHD-007", name: "UK/Mental Health Act Review 2022 — Réforme En Cours, Disparités Raciales", composite_score: 26.65, risk_level: "modéré", estimated_mental_health_rights_index: 2.66 },
    { id: "MHD-008", name: "Finlande/Psychiatrie Ouverte Tornio — Modèle Open Dialogue, Internement Minimal", composite_score: 7.85, risk_level: "faible", estimated_mental_health_rights_index: 0.79 },
  ],
  avg_composite: 59.47,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) return await sealResponse(NextResponse.json({ payload: MOCK }))
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/mental-health-detention-psychiatric-rights-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
