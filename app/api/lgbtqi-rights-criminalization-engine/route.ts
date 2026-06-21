import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[lgbtqi-rights-criminalization-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "lgbtqi-rights-criminalization-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "LRC-001", name: "Iran — Peine de Mort Légale Homosexualité, Exécutions Documentées, Castration Forcée Autorisée & Islamisation Totale Code Pénal", composite_score: 91.00, risk_level: "critique", estimated_lgbtqi_persecution_index: 9.10 },
    { id: "LRC-002", name: "Arabie Saoudite — Flagellation-Emprisonnement-Mort LGBTQI+, Charia Appliquée, Aucune Protection Légale & Censure Totale", composite_score: 88.00, risk_level: "critique", estimated_lgbtqi_persecution_index: 8.80 },
    { id: "LRC-003", name: "Nigeria — Loi 14 Ans Prison Fédérale + Charia États Nord, Same-Sex Marriage Prohibition Act, Violence Communautaire & Police", composite_score: 82.65, risk_level: "critique", estimated_lgbtqi_persecution_index: 8.27 },
    { id: "LRC-004", name: "Ouganda — Anti-Homosexuality Act 2023, Réclusion Criminelle à Vie, ONG LGBTQI+ Fermées & Soutien Gouvernemental Persécution", composite_score: 81.25, risk_level: "critique", estimated_lgbtqi_persecution_index: 8.12 },
    { id: "LRC-005", name: "Russie — Loi Propagande LGBTQI+ 2023, ONG Agents Étrangers, Arrêts Prisonniers Politiques & Retrait Européen Droits Humains", composite_score: 56.60, risk_level: "élevé", estimated_lgbtqi_persecution_index: 5.66 },
    { id: "LRC-006", name: "Égypte — Article 278 Code Pénal, Arrestations Massives Apps Rencontre, Procès Militaires Civils & Campagnes Morales Policières", composite_score: 54.65, risk_level: "élevé", estimated_lgbtqi_persecution_index: 5.46 },
    { id: "LRC-007", name: "Jamaïque — Buggery Act Colonial Maintenu, Violence Communautaire, Expulsions Militants LGBTQI+ & Progrès Judiciaires Timides", composite_score: 33.55, risk_level: "modéré", estimated_lgbtqi_persecution_index: 3.35 },
    { id: "LRC-008", name: "Canada — Mariage Égal 2005, Loi C-4 Thérapies Conversion Interdites, Refugees LGBTQI+ Acceptés & Modèle International", composite_score: 2.40, risk_level: "faible", estimated_lgbtqi_persecution_index: 0.24 },
  ],
  avg_composite: 61.26,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 }
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/lgbtqi-rights-criminalization-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
