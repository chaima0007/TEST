import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[child-soldiers-armed-recruitment-contemporain-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "child-soldiers-armed-recruitment-contemporain-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "CSR-001", name: "RD Congo/M23 Recrutement — 3 000+ Enfants Soldats M23 CNDP Kyvu 2023 ONU Rapport Enrôlement Forcé Dès 8 Ans", composite_score: 93.30, risk_level: "critique", estimated_child_soldier_index: 9.33 },
    { id: "CSR-002", name: "Somalie/Al-Shabaab — 5 000+ Enfants Recrutés Annuellement Suicide Bombing Enfants ONU Cas Documentés UNICEF", composite_score: 88.30, risk_level: "critique", estimated_child_soldier_index: 8.83 },
    { id: "CSR-003", name: "Soudan/RSF Enfants — Forces Appui Rapide Recrutent Enfants Darfour 2023 12-17 Ans Formation Paramilitaire", composite_score: 82.30, risk_level: "critique", estimated_child_soldier_index: 8.23 },
    { id: "CSR-004", name: "Yémen/Houthis — 3 500+ Enfants Soldats Houthis ONU Vérifiés Coalition Saoudienne Aussi Documentée UNICEF", composite_score: 77.30, risk_level: "critique", estimated_child_soldier_index: 7.73 },
    { id: "CSR-005", name: "Myanmar/Tatmadaw — Armée Birmane Recrutement Enfants Persistant Malgré Interdiction CPI Enquêtes 2023", composite_score: 57.50, risk_level: "élevé", estimated_child_soldier_index: 5.75 },
    { id: "CSR-006", name: "Mali/Groupes Armés — JNIM Katiba Macina Recrutement Enfants Sahel 1 200 Cas ONU 2023 Filles Esclavage Sexuel", composite_score: 51.50, risk_level: "élevé", estimated_child_soldier_index: 5.15 },
    { id: "CSR-007", name: "Philippines/Lumad — Enfants Autochtones Lumad Recrutement Contesté NPA Armée Droits Humains Alert", composite_score: 29.50, risk_level: "modéré", estimated_child_soldier_index: 2.95 },
    { id: "CSR-008", name: "Allemagne/Loi Interdiction — Modèle Législatif Stricte Prohibition Recrutement Mineurs Coopération ICC Coalition Stop", composite_score: 11.90, risk_level: "faible", estimated_child_soldier_index: 1.19 },
  ],
  avg_composite: 61.45,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/child-soldiers-armed-recruitment-contemporain-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
