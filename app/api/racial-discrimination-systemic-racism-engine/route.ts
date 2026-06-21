import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[racial-discrimination-systemic-racism-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Racial Discrimination Systemic Racism Engine Agent",
  domain: "racial_discrimination_systemic_racism",
  total_entities: 8,
  avg_composite: 61.26,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { racial_profiling_police_brutality_severity: 4, systemic_economic_housing_discrimination_scale: 2, anti_racism_policy_reparation_deficit_gap: 2 },
  top_risk_entities: ["USA/Apartheid Héritage — George Floyd 1 000 Noirs Tués Police/An, Mass Incarceration 40% Noir, Redlining Persistant & Reparations Bloquées", "Brésil/Dalit Noirs — 75% Victimes Homicides Noirs, Police Favela Opération Morro João Pedro, Quilombolas Expulsés & Quota Contourné", "Inde/Caste-Race — Dalits 165M, Violences Caste 50 000/An, Endogamie Forcée & Discrimination Emploi Systémique"],
  critical_alerts: ["USA/Apartheid Héritage: racial_profiling_police_brutality_severity", "Brésil/Dalit Noirs: racial_profiling_police_brutality_severity", "Inde/Caste-Race: systemic_economic_housing_discrimination_scale", "Europe/Roms: systemic_economic_housing_discrimination_scale"],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_racial_discrimination_systemic_racism_index: 6.13,
  data_sources: ["un_cerd_racial_discrimination_report", "human_rights_watch_racial_profiling_report", "amnesty_international_systemic_racism_report"],
  entities: [
    { entity_id: "RDS-001", name: "USA/Apartheid Héritage — George Floyd 1 000 Noirs Tués Police/An, Mass Incarceration 40% Noir, Redlining Persistant & Reparations Bloquées", country: "USA", composite_score: 92.65, racial_profiling_police_brutality_severity_score: 94.0, systemic_economic_housing_discrimination_scale_score: 92.0, hate_crime_racial_violence_impunity_score: 93.0, anti_racism_policy_reparation_deficit_gap_score: 91.0, risk_level: "critique", primary_pattern: "racial_profiling_police_brutality_severity", estimated_racial_discrimination_systemic_racism_index: 9.27, last_updated: "2026-06-21" },
    { entity_id: "RDS-002", name: "Brésil/Dalit Noirs — 75% Victimes Homicides Noirs, Police Favela Opération Morro João Pedro, Quilombolas Expulsés & Quota Contourné", country: "Brésil", composite_score: 89.85, racial_profiling_police_brutality_severity_score: 90.0, systemic_economic_housing_discrimination_scale_score: 89.0, hate_crime_racial_violence_impunity_score: 92.0, anti_racism_policy_reparation_deficit_gap_score: 88.0, risk_level: "critique", primary_pattern: "racial_profiling_police_brutality_severity", estimated_racial_discrimination_systemic_racism_index: 8.98, last_updated: "2026-06-21" },
    { entity_id: "RDS-003", name: "Inde/Caste-Race — Dalits 165M, Violences Caste 50 000/An, Endogamie Forcée & Discrimination Emploi Systémique", country: "Inde", composite_score: 86.55, racial_profiling_police_brutality_severity_score: 87.0, systemic_economic_housing_discrimination_scale_score: 88.0, hate_crime_racial_violence_impunity_score: 85.0, anti_racism_policy_reparation_deficit_gap_score: 86.0, risk_level: "critique", primary_pattern: "systemic_economic_housing_discrimination_scale", estimated_racial_discrimination_systemic_racism_index: 8.65, last_updated: "2026-06-21" },
    { entity_id: "RDS-004", name: "Europe/Roms — Roms Expulsions France/Italie, Stérilisation Forcée Slovaquie, Écoles Séparées & Discrimination Logement Légal", country: "Europe", composite_score: 82.55, racial_profiling_police_brutality_severity_score: 83.0, systemic_economic_housing_discrimination_scale_score: 84.0, hate_crime_racial_violence_impunity_score: 81.0, anti_racism_policy_reparation_deficit_gap_score: 82.0, risk_level: "critique", primary_pattern: "systemic_economic_housing_discrimination_scale", estimated_racial_discrimination_systemic_racism_index: 8.26, last_updated: "2026-06-21" },
    { entity_id: "RDS-005", name: "Israël/Arabes — Loi Nation-État 2018, Planification Discriminatoire, Arabes-Israéliens 20% Citoyens Inégaux & Bédouins Villages Non-Reconnus", country: "Israël", composite_score: 55.45, racial_profiling_police_brutality_severity_score: 56.0, systemic_economic_housing_discrimination_scale_score: 54.0, hate_crime_racial_violence_impunity_score: 55.0, anti_racism_policy_reparation_deficit_gap_score: 57.0, risk_level: "élevé", primary_pattern: "anti_racism_policy_reparation_deficit_gap", estimated_racial_discrimination_systemic_racism_index: 5.54, last_updated: "2026-06-21" },
    { entity_id: "RDS-006", name: "Australie/Aborigènes — Incarcération 15× Moyenne, Décès Garde Policière, Enfants Retirés 20 000 & Pas Traité Constitutionnel", country: "Australie", composite_score: 52.45, racial_profiling_police_brutality_severity_score: 52.0, systemic_economic_housing_discrimination_scale_score: 51.0, hate_crime_racial_violence_impunity_score: 54.0, anti_racism_policy_reparation_deficit_gap_score: 53.0, risk_level: "élevé", primary_pattern: "racial_profiling_police_brutality_severity", estimated_racial_discrimination_systemic_racism_index: 5.25, last_updated: "2026-06-21" },
    { entity_id: "RDS-007", name: "ECRI/CERD — Commission Européenne Contre Racisme, Comité ONU Élimination Discrimination Raciale & Réseau Europeen Anti-Racisme", country: "Global", composite_score: 26.55, racial_profiling_police_brutality_severity_score: 27.0, systemic_economic_housing_discrimination_scale_score: 25.0, hate_crime_racial_violence_impunity_score: 28.0, anti_racism_policy_reparation_deficit_gap_score: 26.0, risk_level: "modéré", primary_pattern: "anti_racism_policy_reparation_deficit_gap", estimated_racial_discrimination_systemic_racism_index: 2.66, last_updated: "2026-06-21" },
    { entity_id: "RDS-008", name: "ONU/CERD 1965 — Convention Élimination Discrimination Raciale 1965, DDPA Durban 2001 & SDG 10.3 Inégalités", country: "Global", composite_score: 4.0, racial_profiling_police_brutality_severity_score: 4.0, systemic_economic_housing_discrimination_scale_score: 4.0, hate_crime_racial_violence_impunity_score: 4.0, anti_racism_policy_reparation_deficit_gap_score: 4.0, risk_level: "faible", primary_pattern: "racial_profiling_police_brutality_severity", estimated_racial_discrimination_systemic_racism_index: 0.4, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/racial-discrimination-systemic-racism-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
