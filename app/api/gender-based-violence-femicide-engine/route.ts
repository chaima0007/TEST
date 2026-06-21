import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[gender-based-violence-femicide-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "gender_based_violence_femicide_engine",
  domain: "gender_based_violence_femicide",
  total_entities: 8,
  avg_composite: 61.64,
  confidence_score: 0.92,
  risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
  pattern_distribution: {
    femicide_impunity: 3,
    sexual_violence: 2,
    honor_killing_forced_marriage: 2,
    legal_deficit: 1,
  },
  top_risk_entities: [
    { id: "GBV-001", name: "Mexique/Amérique Centrale — 10 Féminicides/Jour", score: 93.5, risk: "critique" },
    { id: "GBV-002", name: "Afghanistan/Taliban — Mariage Enfants & Violence Conjugale", score: 91.45, risk: "critique" },
    { id: "GBV-003", name: "Pakistan/Inde — Honor Killings 1000+/An", score: 88.45, risk: "critique" },
  ],
  critical_alerts: [
    "GBV-001: Mexique/Amérique Centrale — 10 Féminicides/Jour — composite 93.5",
    "GBV-002: Afghanistan/Taliban — Mariage Enfants & Violence Conjugale — composite 91.45",
    "GBV-003: Pakistan/Inde — Honor Killings 1000+/An — composite 88.45",
    "GBV-004: RDC/Afrique Conflits — Viol Arme de Guerre — composite 84.2",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_gender_based_violence_femicide_index: 6.16,
  data_sources: [
    "un_women_gbv_prevalence_global_database",
    "who_femicide_global_status_report",
    "amnesty_honor_killing_sexual_violence_documentation",
  ],
  entities: [
    {
      id: "GBV-001",
      name: "Mexique/Amérique Centrale — 10 Féminicides/Jour",
      country: "Mexique",
      femicide_domestic_violence_impunity_severity_score: 95.0,
      rape_sexual_violence_prosecution_gap_scale_score: 92.0,
      honor_killing_forced_marriage_prevalence_score: 92.0,
      gbv_legal_protection_enforcement_deficit_gap_score: 93.0,
      composite_score: 93.5,
      risk_level: "critique",
      primary_pattern: "Alerte Genre 22 États, Impunité 95% & Cartels Femmes",
      estimated_gender_based_violence_femicide_index: 9.35,
      last_updated: "2026-06-21",
    },
    {
      id: "GBV-002",
      name: "Afghanistan/Taliban — Mariage Enfants & Violence Conjugale",
      country: "Afghanistan",
      femicide_domestic_violence_impunity_severity_score: 93.0,
      rape_sexual_violence_prosecution_gap_scale_score: 90.0,
      honor_killing_forced_marriage_prevalence_score: 91.0,
      gbv_legal_protection_enforcement_deficit_gap_score: 89.0,
      composite_score: 91.45,
      risk_level: "critique",
      primary_pattern: "Mariage Enfants Légalisé, Violence Non Criminalisée & Stoning",
      estimated_gender_based_violence_femicide_index: 9.15,
      last_updated: "2026-06-21",
    },
    {
      id: "GBV-003",
      name: "Pakistan/Inde — Honor Killings 1000+/An",
      country: "Pakistan",
      femicide_domestic_violence_impunity_severity_score: 90.0,
      rape_sexual_violence_prosecution_gap_scale_score: 87.0,
      honor_killing_forced_marriage_prevalence_score: 88.0,
      gbv_legal_protection_enforcement_deficit_gap_score: 86.0,
      composite_score: 88.45,
      risk_level: "critique",
      primary_pattern: "Honor Killings, Viol Conjugal Légal, Acid Attacks & Jirga",
      estimated_gender_based_violence_femicide_index: 8.85,
      last_updated: "2026-06-21",
    },
    {
      id: "GBV-004",
      name: "RDC/Afrique Conflits — Viol Arme de Guerre",
      country: "RDC",
      femicide_domestic_violence_impunity_severity_score: 86.0,
      rape_sexual_violence_prosecution_gap_scale_score: 83.0,
      honor_killing_forced_marriage_prevalence_score: 83.0,
      gbv_legal_protection_enforcement_deficit_gap_score: 84.0,
      composite_score: 84.2,
      risk_level: "critique",
      primary_pattern: "200 000 Survivantes, Impunité Militaires & Fistules Non Traitées",
      estimated_gender_based_violence_femicide_index: 8.42,
      last_updated: "2026-06-21",
    },
    {
      id: "GBV-005",
      name: "Brésil/Turquie — Feminicide Post-COVID & Istanbul",
      country: "Brésil",
      femicide_domestic_violence_impunity_severity_score: 57.0,
      rape_sexual_violence_prosecution_gap_scale_score: 54.0,
      honor_killing_forced_marriage_prevalence_score: 54.0,
      gbv_legal_protection_enforcement_deficit_gap_score: 55.0,
      composite_score: 55.1,
      risk_level: "élevé",
      primary_pattern: "Hausse Post-COVID, Maria da Penha Non Appliquée & Retrait Convention Istanbul",
      estimated_gender_based_violence_femicide_index: 5.51,
      last_updated: "2026-06-21",
    },
    {
      id: "GBV-006",
      name: "Europe/USA — Cyberviolence Genre & Underreporting",
      country: "Europe/USA",
      femicide_domestic_violence_impunity_severity_score: 53.0,
      rape_sexual_violence_prosecution_gap_scale_score: 52.0,
      honor_killing_forced_marriage_prevalence_score: 51.0,
      gbv_legal_protection_enforcement_deficit_gap_score: 52.0,
      composite_score: 52.15,
      risk_level: "élevé",
      primary_pattern: "Cyberviolence Montante, Underreporting 80% & VAWA Insuffisant",
      estimated_gender_based_violence_femicide_index: 5.22,
      last_updated: "2026-06-21",
    },
    {
      id: "GBV-007",
      name: "ONU Femmes/CEDAW — Mécanismes Élimination Discrimination",
      country: "International",
      femicide_domestic_violence_impunity_severity_score: 27.0,
      rape_sexual_violence_prosecution_gap_scale_score: 25.0,
      honor_killing_forced_marriage_prevalence_score: 26.0,
      gbv_legal_protection_enforcement_deficit_gap_score: 25.0,
      composite_score: 25.9,
      risk_level: "modéré",
      primary_pattern: "Standards Protection & Comité CEDAW Rapports",
      estimated_gender_based_violence_femicide_index: 2.59,
      last_updated: "2026-06-21",
    },
    {
      id: "GBV-008",
      name: "ONU/DEVAW — Convention Istanbul & SDG 5.2",
      country: "International",
      femicide_domestic_violence_impunity_severity_score: 4.0,
      rape_sexual_violence_prosecution_gap_scale_score: 4.0,
      honor_killing_forced_marriage_prevalence_score: 4.0,
      gbv_legal_protection_enforcement_deficit_gap_score: 4.0,
      composite_score: 4.0,
      risk_level: "faible",
      primary_pattern: "Déclaration Élimination Violence Femmes 1993 & SDG 5.2",
      estimated_gender_based_violence_femicide_index: 0.4,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[gender-based-violence-femicide-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/gender-based-violence-femicide-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
