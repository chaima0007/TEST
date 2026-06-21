import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Racial Discrimination Minority Rights Engine Agent",
  domain: "racial_discrimination_minority_rights",
  total_entities: 8,
  avg_composite: 61.91,
  confidence_score: 0.87,
  avg_estimated_racial_discrimination_minority_rights_index: 6.19,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  data_sources: [
    "cerd_committee_reports_2023",
    "minority_rights_group_international_2023",
    "human_rights_watch_racial_discrimination_2022",
    "amnesty_international_systemic_racism_2023",
  ],
  critical_alerts: [
    "USA/Violence Policière Raciale: racial_violence_impunity",
    "Chine/Tibet & Xinjiang: systemic_racial_discrimination",
    "Inde/Discrimination Castes Dalits: systemic_racial_discrimination",
    "Brésil/Racisme Structurel & Féminicide Noir: racial_violence_impunity",
  ],
  entities: [
    {
      id: "RDMR-001",
      name: "USA/Violence Policière Raciale — Killings BLM Persistance, 1 000+ Morts/An, Disparités Raciales Justice Pénale & Sur-Incarcération Noirs 5×",
      country: "USA",
      composite_score: 81.6,
      systemic_racial_discrimination_score: 85.0,
      minority_legal_protection_gap_score: 80.0,
      racial_violence_impunity_score: 82.0,
      institutional_exclusion_score: 78.0,
      risk_level: "critique",
      primary_pattern: "racial_violence_impunity",
      estimated_racial_discrimination_minority_rights_index: 8.16,
      last_updated: "2026-06-21",
    },
    {
      id: "RDMR-002",
      name: "Chine/Tibet & Xinjiang — Discrimination Ethnique Systémique, Suppression Culture Tibétaine, Assimilation Forcée Ouïghours & Persécution Religieuse",
      country: "Chine",
      composite_score: 89.1,
      systemic_racial_discrimination_score: 92.0,
      minority_legal_protection_gap_score: 90.0,
      racial_violence_impunity_score: 88.0,
      institutional_exclusion_score: 85.0,
      risk_level: "critique",
      primary_pattern: "systemic_racial_discrimination",
      estimated_racial_discrimination_minority_rights_index: 8.91,
      last_updated: "2026-06-21",
    },
    {
      id: "RDMR-003",
      name: "Inde/Discrimination Castes Dalits — 200M Dalits Intouchabilité Persistante, Violences Sexuelles Dalites, Exclusion Économique & Impunité Auteurs",
      country: "Inde",
      composite_score: 79.1,
      systemic_racial_discrimination_score: 82.0,
      minority_legal_protection_gap_score: 78.0,
      racial_violence_impunity_score: 80.0,
      institutional_exclusion_score: 75.0,
      risk_level: "critique",
      primary_pattern: "systemic_racial_discrimination",
      estimated_racial_discrimination_minority_rights_index: 7.91,
      last_updated: "2026-06-21",
    },
    {
      id: "RDMR-004",
      name: "Brésil/Racisme Structurel & Féminicide Noir — Noirs 75% Victimes Homicides, Féminicide Noir 2× Plus Élevé, Exclusion Socio-Économique & Impunité Persistante",
      country: "Brésil",
      composite_score: 77.65,
      systemic_racial_discrimination_score: 80.0,
      minority_legal_protection_gap_score: 75.0,
      racial_violence_impunity_score: 82.0,
      institutional_exclusion_score: 72.0,
      risk_level: "critique",
      primary_pattern: "racial_violence_impunity",
      estimated_racial_discrimination_minority_rights_index: 7.77,
      last_updated: "2026-06-21",
    },
    {
      id: "RDMR-005",
      name: "Hongrie/Discrimination Roms UE — 700K Roms Ségrégation Scolaire, Exclusion Emploi, Expulsions Forcées & Discours Haineux Gouvernemental Légitimé",
      country: "Hongrie",
      composite_score: 59.85,
      systemic_racial_discrimination_score: 62.0,
      minority_legal_protection_gap_score: 58.0,
      racial_violence_impunity_score: 55.0,
      institutional_exclusion_score: 65.0,
      risk_level: "élevé",
      primary_pattern: "institutional_exclusion",
      estimated_racial_discrimination_minority_rights_index: 5.99,
      last_updated: "2026-06-21",
    },
    {
      id: "RDMR-006",
      name: "Israël/Palestine — Apartheid Selon HRW & Amnesty, Discrimination Systémique Arabes Israéliens, Déni Droits Palestiniens & Ségrégation Territoriale",
      country: "Israël/Palestine",
      composite_score: 58.65,
      systemic_racial_discrimination_score: 58.0,
      minority_legal_protection_gap_score: 62.0,
      racial_violence_impunity_score: 55.0,
      institutional_exclusion_score: 60.0,
      risk_level: "élevé",
      primary_pattern: "minority_legal_protection_gap",
      estimated_racial_discrimination_minority_rights_index: 5.87,
      last_updated: "2026-06-21",
    },
    {
      id: "RDMR-007",
      name: "France/Discrimination Institutionnelle Voilée — Rapport Défenseur des Droits: Discrimination 20% Minorités Emploi, Contrôles Faciaux, Islamophobie & Inégalités Logement",
      country: "France",
      composite_score: 35.9,
      systemic_racial_discrimination_score: 35.0,
      minority_legal_protection_gap_score: 38.0,
      racial_violence_impunity_score: 30.0,
      institutional_exclusion_score: 42.0,
      risk_level: "modéré",
      primary_pattern: "institutional_exclusion",
      estimated_racial_discrimination_minority_rights_index: 3.59,
      last_updated: "2026-06-21",
    },
    {
      id: "RDMR-008",
      name: "Canada/TRC & Multiculturalisme — Politique Multiculturalisme Avancée, TRC 94 Appels à l'Action, Réconciliation Peuples Autochtones & Cadre Anti-Discrimination Robuste",
      country: "Canada",
      composite_score: 13.45,
      systemic_racial_discrimination_score: 12.0,
      minority_legal_protection_gap_score: 15.0,
      racial_violence_impunity_score: 10.0,
      institutional_exclusion_score: 18.0,
      risk_level: "faible",
      primary_pattern: "minority_legal_protection_gap",
      estimated_racial_discrimination_minority_rights_index: 1.35,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[racial-discrimination-minority-rights-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/racial-discrimination-minority-rights-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
