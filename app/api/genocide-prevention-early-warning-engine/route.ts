import { NextResponse } from "next/server"
import { sealResponse } from "@/lib/digital-seal"

if (!process.env.SWARM_API_URL) {
  console.warn("[genocide-prevention-early-warning-engine] SWARM_API_URL not set — using mock data")
}

const MOCK = {
  domain: "genocide-prevention-early-warning-engine",
  generated_at: new Date().toISOString(),
  entities: [
    { id: "GPW-001", name: "Myanmar/Rohingya Génocide — 700 000 Déplacés Bangladesh CIJ Cas Génocide Documenté Armée Tatmadaw Crimes Contre Humanité", composite_score: 94.30, risk_level: "critique", estimated_genocide_risk_index: 9.43 },
    { id: "GPW-002", name: "Soudan/Darfour Récurrence — RSF Retour Violences 2023 El Fasher Assauts Civils ONU Alertes Génocide Imminentes", composite_score: 89.30, risk_level: "critique", estimated_genocide_risk_index: 8.93 },
    { id: "GPW-003", name: "Éthiopie/Tigré — 500 000 Morts Estimés Famine Arme Nettoyage Ethnique Documenté Amnesty HRW Preuves Satellitaires", composite_score: 83.30, risk_level: "critique", estimated_genocide_risk_index: 8.33 },
    { id: "GPW-004", name: "Chine/Ouïghours — Camps Détention 1M+ Stérilisations Forcées Destruction Mosquées ONU Violations Graves Droits", composite_score: 79.30, risk_level: "critique", estimated_genocide_risk_index: 7.93 },
    { id: "GPW-005", name: "RD Congo/Est — Massacres Communautaires Répétés FDLR ADF Groupes Armés Kyvu ONU Alerte Précoce Ignorée", composite_score: 57.90, risk_level: "élevé", estimated_genocide_risk_index: 5.79 },
    { id: "GPW-006", name: "Inde/Manipur — Violence Ethnique Kuki-Meitei 2023 220+ Morts Déplacements Massifs Impunité Accusations Nettoyage", composite_score: 51.90, risk_level: "élevé", estimated_genocide_risk_index: 5.19 },
    { id: "GPW-007", name: "Rwanda/Mémorial Génocide — Gacaca Tribunaux Réconciliation Modèle Prévention ICGLR Mécanisme Alerte Régional", composite_score: 27.90, risk_level: "modéré", estimated_genocide_risk_index: 2.79 },
    { id: "GPW-008", name: "Canada/R2P Doctrine — Responsabilité Protéger ONU 2005 ICISS Rapport Normes Intervention Humanitaire Modèle", composite_score: 11.90, risk_level: "faible", estimated_genocide_risk_index: 1.19 },
  ],
  avg_composite: 61.97,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
}

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return await sealResponse(NextResponse.json({ payload: MOCK }))
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/genocide-prevention-early-warning-engine`, { next: { revalidate: 30 } })
    const data = await res.json()
    return await sealResponse(NextResponse.json({ payload: data }))
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream unavailable" }, { status: 502 }))
  }
}
