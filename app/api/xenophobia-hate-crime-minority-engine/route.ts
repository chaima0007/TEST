import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[xenophobia-hate-crime-minority-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Xenophobia Hate Crime Minority Engine Agent",
  domain: "xenophobia_hate_crime_minority",
  total_entities: 8,
  avg_composite: 60.09,
  confidence_score: 0.86,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    ethnic_violence_pogrom_targeting_scale: 2,
    hate_speech_incitement_state_complicity: 2,
    discriminatory_policy_minority_exclusion: 2,
    xenophobia_migrant_scapegoating_violence: 2,
  },
  top_risk_entities: [
    "Myanmar/Rohingya — Génocide Reconnu ONU, Villages Brûlés, 700K Réfugiés Bangladesh & Apartheid Ethnic Cleansing",
    "Inde/BJP-RSS — Loi CAA Discriminatoire, Pogroms Musulmans, Démolitions Bulldozer & Discours Haine Officiel",
    "Hongrie/Pologne — Déshumanisation Migrants, Clôtures Frontière, Hate Speech Légalisé & Minorités Roma Exclusion",
  ],
  critical_alerts: [
    "Myanmar/Rohingya: ethnic_violence_pogrom_targeting_scale",
    "Inde/BJP-RSS: hate_speech_incitement_state_complicity",
    "Chine/Ouïghours: discriminatory_policy_minority_exclusion",
    "Éthiopie/Tigré: ethnic_violence_pogrom_targeting_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_xenophobia_hate_crime_minority_index: 6.01,
  data_sources: [
    "osce_odihr_hate_crime_data_2023",
    "human_rights_watch_xenophobia_discrimination_2023",
    "amnesty_international_hate_crimes_minorities_2023",
    "un_committee_elimination_racial_discrimination_2023",
  ],
  entities: [
    {
      id: "XHCM-001",
      name: "Myanmar/Rohingya — Génocide Reconnu ONU, Villages Brûlés, 700K Réfugiés Bangladesh & Apartheid Ethnic Cleansing",
      country: "Myanmar",
      ethnic_violence_pogrom_targeting_scale_score: 98.0,
      hate_speech_incitement_state_complicity_score: 95.0,
      discriminatory_policy_minority_exclusion_score: 97.0,
      xenophobia_migrant_scapegoating_violence_score: 90.0,
      composite_score: 95.55,
      risk_level: "critique",
      primary_pattern: "ethnic_violence_pogrom_targeting_scale",
      estimated_xenophobia_hate_crime_minority_index: 9.56,
      last_updated: "2026-06-21",
    },
    {
      id: "XHCM-002",
      name: "Inde/BJP-RSS — Loi CAA Discriminatoire, Pogroms Musulmans, Démolitions Bulldozer & Discours Haine Officiel",
      country: "Inde",
      ethnic_violence_pogrom_targeting_scale_score: 90.0,
      hate_speech_incitement_state_complicity_score: 92.0,
      discriminatory_policy_minority_exclusion_score: 88.0,
      xenophobia_migrant_scapegoating_violence_score: 85.0,
      composite_score: 89.25,
      risk_level: "critique",
      primary_pattern: "hate_speech_incitement_state_complicity",
      estimated_xenophobia_hate_crime_minority_index: 8.93,
      last_updated: "2026-06-21",
    },
    {
      id: "XHCM-003",
      name: "Chine/Ouïghours-Tibet — Surveillance Ethnique, Internement Culturel, Stérilisations Forcées & Langues Interdites",
      country: "Chine",
      ethnic_violence_pogrom_targeting_scale_score: 87.0,
      hate_speech_incitement_state_complicity_score: 85.0,
      discriminatory_policy_minority_exclusion_score: 92.0,
      xenophobia_migrant_scapegoating_violence_score: 83.0,
      composite_score: 87.3,
      risk_level: "critique",
      primary_pattern: "discriminatory_policy_minority_exclusion",
      estimated_xenophobia_hate_crime_minority_index: 8.73,
      last_updated: "2026-06-21",
    },
    {
      id: "XHCM-004",
      name: "Éthiopie/Tigré — Massacres Ethniques, Villages Amhara Tigré Oromo, Famine Arme Guerre & Dépeuplementt Forcé",
      country: "Éthiopie",
      ethnic_violence_pogrom_targeting_scale_score: 86.0,
      hate_speech_incitement_state_complicity_score: 84.0,
      discriminatory_policy_minority_exclusion_score: 83.0,
      xenophobia_migrant_scapegoating_violence_score: 82.0,
      composite_score: 83.95,
      risk_level: "critique",
      primary_pattern: "ethnic_violence_pogrom_targeting_scale",
      estimated_xenophobia_hate_crime_minority_index: 8.40,
      last_updated: "2026-06-21",
    },
    {
      id: "XHCM-005",
      name: "Hongrie/Pologne — Déshumanisation Migrants, Clôtures Anti-Réfugiés, Minorités Roma Exclusion & Parti Jobbik Influence",
      country: "Hongrie/Pologne",
      ethnic_violence_pogrom_targeting_scale_score: 57.0,
      hate_speech_incitement_state_complicity_score: 59.0,
      discriminatory_policy_minority_exclusion_score: 56.0,
      xenophobia_migrant_scapegoating_violence_score: 55.0,
      composite_score: 56.95,
      risk_level: "élevé",
      primary_pattern: "hate_speech_incitement_state_complicity",
      estimated_xenophobia_hate_crime_minority_index: 5.70,
      last_updated: "2026-06-21",
    },
    {
      id: "XHCM-006",
      name: "USA/Europe — Suprémacisme Blanc Attentats, Islamophobie Post-9/11, Antisémitisme Montant & Afro-descendants Violences",
      country: "USA/Europe",
      ethnic_violence_pogrom_targeting_scale_score: 54.0,
      hate_speech_incitement_state_complicity_score: 52.0,
      discriminatory_policy_minority_exclusion_score: 53.0,
      xenophobia_migrant_scapegoating_violence_score: 57.0,
      composite_score: 54.05,
      risk_level: "élevé",
      primary_pattern: "xenophobia_migrant_scapegoating_violence",
      estimated_xenophobia_hate_crime_minority_index: 5.41,
      last_updated: "2026-06-21",
    },
    {
      id: "XHCM-007",
      name: "OSCE/ODIHR — Hate Crime Data Collection, Tolerance Programmes, Early Warning Systems & CERD Monitoring",
      country: "Global",
      ethnic_violence_pogrom_targeting_scale_score: 26.0,
      hate_speech_incitement_state_complicity_score: 25.0,
      discriminatory_policy_minority_exclusion_score: 27.0,
      xenophobia_migrant_scapegoating_violence_score: 24.0,
      composite_score: 25.7,
      risk_level: "modéré",
      primary_pattern: "discriminatory_policy_minority_exclusion",
      estimated_xenophobia_hate_crime_minority_index: 2.57,
      last_updated: "2026-06-21",
    },
    {
      id: "XHCM-008",
      name: "ONU/ICERD — Convention Discrimination Raciale, Rapporteur Spécial Racisme, Décennie Afrodescendants & DDPA Durban",
      country: "Global",
      ethnic_violence_pogrom_targeting_scale_score: 5.0,
      hate_speech_incitement_state_complicity_score: 4.0,
      discriminatory_policy_minority_exclusion_score: 4.0,
      xenophobia_migrant_scapegoating_violence_score: 5.0,
      composite_score: 4.55,
      risk_level: "faible",
      primary_pattern: "discriminatory_policy_minority_exclusion",
      estimated_xenophobia_hate_crime_minority_index: 0.46,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(
      `${process.env.SWARM_API_URL}/xenophobia-hate-crime-minority-engine`,
      { next: { revalidate: 30 } }
    );
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
