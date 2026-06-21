import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[femicide-gender-based-killings-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "femicide_gender_based_killings_engine",
  domain: "femicide_gender_based_killings",
  total_entities: 8,
  avg_composite: 60.46,
  confidence_score: 0.91,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    femicide_impunity: 4,
    legal_protection_deficit: 2,
    gender_violence_systemic: 1,
    state_accountability: 1,
  },
  top_risk_entities: [
    { id: "FGK-001", name: "Mexique — 10 Femmes Assassinées/Jour, Impunité 99%", score: 93.1, risk: "critique" },
    { id: "FGK-002", name: "El Salvador/Honduras/Guatemala — Triangle Nord Féminicides Gangs", score: 89.05, risk: "critique" },
    { id: "FGK-003", name: "Turquie — Retrait Convention Istanbul 2021, 300+ Morts/An", score: 85.0, risk: "critique" },
  ],
  critical_alerts: [
    "FGK-001: Mexique — 10 Femmes Assassinées/Jour, Impunité 99% — composite 93.1",
    "FGK-002: El Salvador/Honduras/Guatemala — Triangle Nord Féminicides Gangs — composite 89.05",
    "FGK-003: Turquie — Retrait Convention Istanbul 2021, 300+ Morts/An — composite 85.0",
    "FGK-004: Pakistan — Crimes Honneur Karo-Kari, 1000+ Annuel — composite 81.05",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_femicide_index: 6.05,
  data_sources: [
    "un_women_femicide_watch_2023",
    "who_violence_against_women_2023",
    "amnesty_international_femicide_report_2023",
    "council_europe_istanbul_convention_monitoring",
  ],
  entities: [
    {
      id: "FGK-001",
      name: "Mexique — 10 Femmes Assassinées/Jour, Impunité 99%",
      country: "Mexique",
      femicide_rate_impunity_score: 96.0,
      legal_protection_enforcement_deficit_score: 92.0,
      gender_violence_systemic_failure_score: 93.0,
      state_accountability_prevention_score: 91.0,
      composite_score: 93.1,
      risk_level: "critique",
      primary_pattern: "10 féminicides quotidiens, impunité 99%, absence enquêtes féminicide, loi Alerta sin efecto",
      estimated_femicide_index: 9.31,
      last_updated: "2026-06-21",
    },
    {
      id: "FGK-002",
      name: "El Salvador/Honduras/Guatemala — Triangle Nord Féminicides Gangs",
      country: "Amérique Centrale",
      femicide_rate_impunity_score: 91.0,
      legal_protection_enforcement_deficit_score: 88.0,
      gender_violence_systemic_failure_score: 89.0,
      state_accountability_prevention_score: 87.0,
      composite_score: 89.05,
      risk_level: "critique",
      primary_pattern: "Féminicides MS-13/Barrio 18, lois insuffisantes, femmes déplacées, violence domestique impunie",
      estimated_femicide_index: 8.91,
      last_updated: "2026-06-21",
    },
    {
      id: "FGK-003",
      name: "Turquie — Retrait Convention Istanbul 2021, 300+ Morts/An",
      country: "Turquie",
      femicide_rate_impunity_score: 87.0,
      legal_protection_enforcement_deficit_score: 84.0,
      gender_violence_systemic_failure_score: 85.0,
      state_accountability_prevention_score: 83.0,
      composite_score: 85.0,
      risk_level: "critique",
      primary_pattern: "Retrait Istanbul Convention 2021, 300+ femmes tuées ex-partenaires annuellement, politiques rétrogrades",
      estimated_femicide_index: 8.5,
      last_updated: "2026-06-21",
    },
    {
      id: "FGK-004",
      name: "Pakistan — Crimes Honneur Karo-Kari, 1000+ Annuel",
      country: "Pakistan",
      femicide_rate_impunity_score: 83.0,
      legal_protection_enforcement_deficit_score: 80.0,
      gender_violence_systemic_failure_score: 81.0,
      state_accountability_prevention_score: 79.0,
      composite_score: 81.05,
      risk_level: "critique",
      primary_pattern: "1000+ crimes honneur annuels estimés ONG, acquittements familiaux, karo-kari systémique, loi honor killing 2004 inappliquée",
      estimated_femicide_index: 8.11,
      last_updated: "2026-06-21",
    },
    {
      id: "FGK-005",
      name: "Afrique du Sud — Féminicide 5x Moyenne Mondiale, Viol Correctionnel",
      country: "Afrique du Sud",
      femicide_rate_impunity_score: 58.0,
      legal_protection_enforcement_deficit_score: 54.0,
      gender_violence_systemic_failure_score: 55.0,
      state_accountability_prevention_score: 52.0,
      composite_score: 55.0,
      risk_level: "élevé",
      primary_pattern: "5x moyenne mondiale féminicide, viol correctionnel documenté, xenofeicide, surpopulation prison sans effet dissuasif",
      estimated_femicide_index: 5.5,
      last_updated: "2026-06-21",
    },
    {
      id: "FGK-006",
      name: "France — 118 Féminicides Conjugaux 2023, Bracelet Insuffisant",
      country: "France",
      femicide_rate_impunity_score: 50.0,
      legal_protection_enforcement_deficit_score: 47.0,
      gender_violence_systemic_failure_score: 46.0,
      state_accountability_prevention_score: 48.0,
      composite_score: 47.95,
      risk_level: "élevé",
      primary_pattern: "118 féminicides 2023, bracelet électronique sous-utilisé, 80% victimes avaient signalé, plan gouvernemental insuffisant",
      estimated_femicide_index: 4.8,
      last_updated: "2026-06-21",
    },
    {
      id: "FGK-007",
      name: "Espagne — Loi Violencia de Género 2004, Réduction 25%",
      country: "Espagne",
      femicide_rate_impunity_score: 28.0,
      legal_protection_enforcement_deficit_score: 27.0,
      gender_violence_systemic_failure_score: 28.0,
      state_accountability_prevention_score: 30.0,
      composite_score: 28.15,
      risk_level: "modéré",
      primary_pattern: "Modèle européen loi intégrale 2004, tribunaux spécialisés, réduction 25% féminicides, protocoles police renforcés",
      estimated_femicide_index: 2.82,
      last_updated: "2026-06-21",
    },
    {
      id: "FGK-008",
      name: "Islande — Égalité Genre Championne, Féminicide Quasi-Nul",
      country: "Islande",
      femicide_rate_impunity_score: 5.0,
      legal_protection_enforcement_deficit_score: 4.0,
      gender_violence_systemic_failure_score: 4.0,
      state_accountability_prevention_score: 5.0,
      composite_score: 4.5,
      risk_level: "faible",
      primary_pattern: "Féminicide quasi-nul, égalité salariale légale, parité politique 50%, modèle nordique prévention violence",
      estimated_femicide_index: 0.45,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/femicide-gender-based-killings-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data.payload ?? data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
