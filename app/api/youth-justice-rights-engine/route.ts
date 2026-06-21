import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[youth-justice-rights-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Youth Justice Rights Engine Agent",
  domain: "youth_justice_rights",
  total_entities: 8,
  avg_composite: 61.74,
  confidence_score: 0.85,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { juvenile_detention_incarceration_severity: 3, fair_trial_youth_procedural_gap: 2, rehabilitation_reintegration_absence: 2, racial_class_bias_youth_justice_scale: 1 },
  top_risk_entities: [
    "USA — 60K Mineurs En Détention, Biais Racial 5x Plus Noirs & Procès Adultes Dès 10 Ans",
    "Brésil — FEBEM/FUNABEM Abus Systémique, 25K Mineurs Privés Liberté & Zéro Réhabilitation",
    "Afrique Sub-Sah. — Détention Préventive 90%, Pas d'Avocat, Mélange Adultes/Enfants & Torture",
  ],
  critical_alerts: [
    "USA: juvenile_detention_incarceration_severity",
    "Brésil: rehabilitation_reintegration_absence",
    "Afrique Sub-Sah.: fair_trial_youth_procedural_gap",
    "Inde: racial_class_bias_youth_justice_scale",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_youth_justice_rights_index: 6.17,
  data_sources: [
    "unicef_justice_children_juvenile_justice_global_assessment",
    "human_rights_watch_youth_justice_incarceration_racial_bias_report",
    "penal_reform_international_global_prison_trends_youth_report",
  ],
  entities: [
    { id: "YJR-001", name: "USA — 60K Mineurs En Détention, Biais Racial 5x Plus Noirs & Procès Adultes Dès 10 Ans", country: "Amérique du Nord", composite_score: 93.55, juvenile_detention_incarceration_severity_score: 95.0, fair_trial_youth_procedural_gap_score: 92.0, rehabilitation_reintegration_absence_score: 92.0, racial_class_bias_youth_justice_scale_score: 95.0, risk_level: "critique", primary_pattern: "juvenile_detention_incarceration_severity", estimated_youth_justice_rights_index: 9.36, last_updated: "2026-06-21" },
    { id: "YJR-002", name: "Brésil — FEBEM/FUNABEM Abus Systémique, 25K Mineurs Privés Liberté & Zéro Réhabilitation", country: "Amérique Latine", composite_score: 90.25, juvenile_detention_incarceration_severity_score: 92.0, fair_trial_youth_procedural_gap_score: 88.0, rehabilitation_reintegration_absence_score: 90.0, racial_class_bias_youth_justice_scale_score: 88.0, risk_level: "critique", primary_pattern: "rehabilitation_reintegration_absence", estimated_youth_justice_rights_index: 9.03, last_updated: "2026-06-21" },
    { id: "YJR-003", name: "Afrique Sub-Sah. — Détention Préventive 90%, Pas d'Avocat, Mélange Adultes/Enfants & Torture", country: "Afrique", composite_score: 88.05, juvenile_detention_incarceration_severity_score: 90.0, fair_trial_youth_procedural_gap_score: 90.0, rehabilitation_reintegration_absence_score: 85.0, racial_class_bias_youth_justice_scale_score: 85.0, risk_level: "critique", primary_pattern: "fair_trial_youth_procedural_gap", estimated_youth_justice_rights_index: 8.81, last_updated: "2026-06-21" },
    { id: "YJR-004", name: "Inde — Age Responsabilité 7 Ans, Centres Détention Surpeuplés & Biais Caste Systémique", country: "Asie du Sud", composite_score: 85.55, juvenile_detention_incarceration_severity_score: 88.0, fair_trial_youth_procedural_gap_score: 85.0, rehabilitation_reintegration_absence_score: 84.0, racial_class_bias_youth_justice_scale_score: 88.0, risk_level: "critique", primary_pattern: "racial_class_bias_youth_justice_scale", estimated_youth_justice_rights_index: 8.56, last_updated: "2026-06-21" },
    { id: "YJR-005", name: "Australie — Surreprésentation Autochtones 5x, Détention Enfants 10 Ans & Centres Don Dale Scandale", country: "Océanie", composite_score: 53.8, juvenile_detention_incarceration_severity_score: 55.0, fair_trial_youth_procedural_gap_score: 52.0, rehabilitation_reintegration_absence_score: 53.0, racial_class_bias_youth_justice_scale_score: 55.0, risk_level: "élevé", primary_pattern: "racial_class_bias_youth_justice_scale", estimated_youth_justice_rights_index: 5.38, last_updated: "2026-06-21" },
    { id: "YJR-006", name: "France/UE — CEF Centres Éducatifs Fermés, Détention Préventive Mineurs & Biais Classe/Race Documenté", country: "Europe", composite_score: 51.95, juvenile_detention_incarceration_severity_score: 52.0, fair_trial_youth_procedural_gap_score: 50.0, rehabilitation_reintegration_absence_score: 52.0, racial_class_bias_youth_justice_scale_score: 55.0, risk_level: "élevé", primary_pattern: "racial_class_bias_youth_justice_scale", estimated_youth_justice_rights_index: 5.2, last_updated: "2026-06-21" },
    { id: "YJR-007", name: "IAYFJM/PRI — Justice Restauratrice Juvénile, Standards Minima ONU Beijing & Plaidoyer Décriminalisation", country: "Global", composite_score: 26.35, juvenile_detention_incarceration_severity_score: 22.0, fair_trial_youth_procedural_gap_score: 28.0, rehabilitation_reintegration_absence_score: 25.0, racial_class_bias_youth_justice_scale_score: 30.0, risk_level: "modéré", primary_pattern: "fair_trial_youth_procedural_gap", estimated_youth_justice_rights_index: 2.64, last_updated: "2026-06-21" },
    { id: "YJR-008", name: "ONU/UNICEF — Règles Beijing CRC Art.37-40, Directives Riyad & SDG 16 Justice Équitable Enfants", country: "Global", composite_score: 4.45, juvenile_detention_incarceration_severity_score: 4.0, fair_trial_youth_procedural_gap_score: 5.0, rehabilitation_reintegration_absence_score: 3.0, racial_class_bias_youth_justice_scale_score: 6.0, risk_level: "faible", primary_pattern: "juvenile_detention_incarceration_severity", estimated_youth_justice_rights_index: 0.45, last_updated: "2026-06-21" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/youth-justice-rights-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
