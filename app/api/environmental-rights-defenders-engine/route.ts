import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Environmental Rights Defenders Engine Agent",
  domain: "environmental_rights_defenders",
  total_entities: 8,
  avg_composite: 62.31,
  confidence_score: 0.88,
  avg_estimated_environmental_rights_defenders_index: 6.23,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "global_witness_defenders_killed_2023",
    "front_line_defenders_2023",
    "business_human_rights_resource_centre_env_2023",
    "unhchr_environmental_defenders_2022",
  ],
  critical_alerts: [],
  entities: [
    {
      id: "ERD-001",
      name: "Honduras — Effet Berta Cáceres, Défenseurs Eau Systématiquement Assassinés, COPINH Persécuté &amp; Impunité Totale Tueurs",
      country: "Honduras",
      composite_score: 92.90,
      risk_level: "critique",
      estimated_environmental_rights_defenders_index: 9.29,
      primary_pattern: "defenders_killed_attacked",
    },
    {
      id: "ERD-002",
      name: "Philippines — Mindanao Défenseurs Miniers Tués, 800+ Activistes Environnement Assassinés &amp; Loi Anti-Terrorisme Instrumentalisée",
      country: "Philippines",
      composite_score: 89.90,
      risk_level: "critique",
      estimated_environmental_rights_defenders_index: 8.99,
      primary_pattern: "state_criminal_criminalisation",
    },
    {
      id: "ERD-003",
      name: "Brésil/Amazonie — Défenseurs Autochtones Tués Héritage Bolsonaro, Dom Phillips Assassiné &amp; Terres Indigènes Déforestées Impunément",
      country: "Brésil",
      composite_score: 89.35,
      risk_level: "critique",
      estimated_environmental_rights_defenders_index: 8.94,
      primary_pattern: "corporate_land_grabbing_impunity",
    },
    {
      id: "ERD-004",
      name: "Cambodge — Défenseurs Forêts Emprisonnés, Mother Nature Cambodia Arrêtée &amp; Concessions Foncières Géantes Complicité État",
      country: "Cambodge",
      composite_score: 85.85,
      risk_level: "critique",
      estimated_environmental_rights_defenders_index: 8.59,
      primary_pattern: "state_criminal_criminalisation",
    },
    {
      id: "ERD-005",
      name: "Mexique — Activistes Eau/Forêts Tués Cartels et État, Impunité 98% Meurtres &amp; Communautés Zapotèques Assiégées",
      country: "Mexique",
      composite_score: 55.30,
      risk_level: "élevé",
      estimated_environmental_rights_defenders_index: 5.53,
      primary_pattern: "defenders_killed_attacked",
    },
    {
      id: "ERD-006",
      name: "Colombie — Post-Accord Leaders Environnementaux Tués, 33% Défenseurs Globaux Assassinés 2022 &amp; PDET Non-Implémenté",
      country: "Colombie",
      composite_score: 52.80,
      risk_level: "élevé",
      estimated_environmental_rights_defenders_index: 5.28,
      primary_pattern: "defenders_killed_attacked",
    },
    {
      id: "ERD-007",
      name: "Kenya — Ogiek Victoire Partielle Cour Africaine, Défenseurs Fonciers Mau Forest &amp; Litiges Environnementaux en Progrès",
      country: "Kenya",
      composite_score: 26.55,
      risk_level: "modéré",
      estimated_environmental_rights_defenders_index: 2.66,
      primary_pattern: "climate_justice_indigenous_rights",
    },
    {
      id: "ERD-008",
      name: "Costa Rica — Modèle Conservation, Droits Verts Constitutionnels, Tribunaux Environnementaux &amp; Défenseurs Protégés par Loi",
      country: "Costa Rica",
      composite_score: 5.80,
      risk_level: "faible",
      estimated_environmental_rights_defenders_index: 0.58,
      primary_pattern: "climate_justice_indigenous_rights",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[environmental-rights-defenders-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/environmental-rights-defenders-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
