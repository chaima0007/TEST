import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[drug-policy-human-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Drug Policy Human Rights Engine Agent",
  domain: "drug_policy_human_rights",
  total_entities: 8,
  avg_composite: 58.36,
  confidence_score: 0.83,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { extrajudicial_killings: 2, criminalization_scale: 2, racial_marginalization_bias: 2, treatment_access_denial: 2 },
  top_risk_entities: [
    "Philippines/Duterte — 30 000 Tués Guerre Drogues, Exécutions Extrajudiciaires Policières",
    "Indonésie/Thaïlande — Peine de Mort Drogues, Zéro Tolérance & Milliers Emprisonnés",
    "USA — Mass Incarceration, War on Drugs, Biais Racial & Prison Industrial Complex",
  ],
  critical_alerts: [
    "Philippines/Duterte: extrajudicial_killings",
    "Indonésie/Thaïlande: criminalization_scale",
    "USA: racial_marginalization_bias",
    "Russie: treatment_access_denial",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_drug_policy_human_rights_index: 5.84,
  data_sources: [
    "human_rights_watch_killing_the_future_drug_war_report",
    "unodc_world_drug_report_annual_statistics_trends",
    "idpc_international_drug_policy_consortium_shadow_report_ungass",
  ],
  entities: [
    { id: "DP-001", name: "Philippines/Duterte — 30 000 Tués Guerre Drogues, Exécutions Extrajudiciaires Policières", country: "Asie du Sud-Est", composite_score: 90.95, criminalization_scale_score: 92.0, extrajudicial_killings_score: 98.0, treatment_access_denial_score: 85.0, racial_marginalization_bias_score: 88.0, risk_level: "critique", primary_pattern: "extrajudicial_killings", estimated_drug_policy_human_rights_index: 9.1, last_updated: "2026-06-20" },
    { id: "DP-002", name: "Indonésie/Thaïlande — Peine de Mort Drogues, Zéro Tolérance & Milliers Emprisonnés", country: "Asie du Sud-Est", composite_score: 84.0, criminalization_scale_score: 85.0, extrajudicial_killings_score: 88.0, treatment_access_denial_score: 82.0, racial_marginalization_bias_score: 80.0, risk_level: "critique", primary_pattern: "criminalization_scale", estimated_drug_policy_human_rights_index: 8.4, last_updated: "2026-06-20" },
    { id: "DP-003", name: "USA — Mass Incarceration, War on Drugs, Biais Racial & Prison Industrial Complex", country: "Amérique du Nord", composite_score: 79.8, criminalization_scale_score: 78.0, extrajudicial_killings_score: 72.0, treatment_access_denial_score: 80.0, racial_marginalization_bias_score: 92.0, risk_level: "critique", primary_pattern: "racial_marginalization_bias", estimated_drug_policy_human_rights_index: 7.98, last_updated: "2026-06-20" },
    { id: "DP-004", name: "Russie — Peine Sévère Héroïne, Refus Substitution Méthadone & Prohibition Harm Reduction", country: "Europe de l'Est", composite_score: 78.75, criminalization_scale_score: 80.0, extrajudicial_killings_score: 75.0, treatment_access_denial_score: 88.0, racial_marginalization_bias_score: 70.0, risk_level: "critique", primary_pattern: "treatment_access_denial", estimated_drug_policy_human_rights_index: 7.88, last_updated: "2026-06-20" },
    { id: "DP-005", name: "Amérique Latine/Mexique — Cartels, Militarisation & Victimes Civils Guerre Drogues", country: "Amérique Latine", composite_score: 54.0, criminalization_scale_score: 55.0, extrajudicial_killings_score: 58.0, treatment_access_denial_score: 52.0, racial_marginalization_bias_score: 50.0, risk_level: "élevé", primary_pattern: "extrajudicial_killings", estimated_drug_policy_human_rights_index: 5.4, last_updated: "2026-06-20" },
    { id: "DP-006", name: "Afrique/Ghana — Criminalisation Usage Personnel, Absence Harm Reduction & Emprisonnement", country: "Afrique Sub-Saharienne", composite_score: 50.4, criminalization_scale_score: 50.0, extrajudicial_killings_score: 45.0, treatment_access_denial_score: 55.0, racial_marginalization_bias_score: 52.0, risk_level: "élevé", primary_pattern: "criminalization_scale", estimated_drug_policy_human_rights_index: 5.04, last_updated: "2026-06-20" },
    { id: "DP-007", name: "Portugal/UE — Modèle Décriminalisation, Harm Reduction & Résistance Politique Mondiale", country: "Europe", composite_score: 24.6, criminalization_scale_score: 22.0, extrajudicial_killings_score: 20.0, treatment_access_denial_score: 28.0, racial_marginalization_bias_score: 30.0, risk_level: "modéré", primary_pattern: "treatment_access_denial", estimated_drug_policy_human_rights_index: 2.46, last_updated: "2026-06-20" },
    { id: "DP-008", name: "ONU/ONUDC/OMS — Conventions Drogues 1961-1988, Harm Reduction Recommandée & Réforme", country: "Global", composite_score: 4.4, criminalization_scale_score: 4.0, extrajudicial_killings_score: 5.0, treatment_access_denial_score: 3.0, racial_marginalization_bias_score: 6.0, risk_level: "faible", primary_pattern: "racial_marginalization_bias", estimated_drug_policy_human_rights_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/drug-policy-human-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
