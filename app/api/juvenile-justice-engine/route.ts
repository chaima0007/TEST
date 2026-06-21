import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[juvenile-justice-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Juvenile Justice Engine Agent",
  domain: "juvenile_justice",
  total_entities: 8,
  avg_composite: 59.21,
  confidence_score: 0.84,
  risk_distribution: { critique: 4, élevé: 2, modéré: 1, faible: 1 },
  pattern_distribution: { child_detention_scale: 3, age_criminal_responsibility: 2, torture_juvenile_detention: 1, rehabilitation_failure: 2 },
  top_risk_entities: [
    "Chine — Centres Rééducation Mineurs, Travail Forcé & Aucune Garantie Procédurale",
    "USA — Jugement Mineurs comme Adultes, Prison à Vie Sans Liberté Conditionnelle & Solitary Confinement",
    "Iran — Exécution Mineurs, Peine de Mort Crimes Commis avant 18 Ans & Tribunaux Spéciaux",
  ],
  critical_alerts: [
    "Chine: child_detention_scale",
    "USA: age_criminal_responsibility",
    "Iran: age_criminal_responsibility",
    "Arabie Saoudite: torture_juvenile_detention",
  ],
  last_analysis: "2026-06-20",
  engine_version: "1.0.0",
  avg_estimated_juvenile_justice_index: 5.92,
  data_sources: [
    "unicef_justice_children_global_report_annual",
    "child_rights_international_network_juvenile_justice_database",
    "un_committee_rights_child_general_comment_10_juvenile_justice",
  ],
  entities: [
    { id: "JJ-001", name: "Chine — Centres Rééducation Mineurs, Travail Forcé & Aucune Garantie Procédurale", country: "Asie du Nord-Est", composite_score: 87.1, child_detention_scale_score: 90.0, rehabilitation_failure_score: 85.0, age_criminal_responsibility_score: 85.0, torture_juvenile_detention_score: 88.0, risk_level: "critique", primary_pattern: "child_detention_scale", estimated_juvenile_justice_index: 8.71, last_updated: "2026-06-20" },
    { id: "JJ-002", name: "USA — Jugement Mineurs comme Adultes, Prison à Vie Sans Liberté Conditionnelle & Solitary Confinement", country: "Amérique du Nord", composite_score: 86.55, child_detention_scale_score: 88.0, rehabilitation_failure_score: 85.0, age_criminal_responsibility_score: 90.0, torture_juvenile_detention_score: 82.0, risk_level: "critique", primary_pattern: "age_criminal_responsibility", estimated_juvenile_justice_index: 8.66, last_updated: "2026-06-20" },
    { id: "JJ-003", name: "Iran — Exécution Mineurs, Peine de Mort Crimes Commis avant 18 Ans & Tribunaux Spéciaux", country: "Moyen-Orient", composite_score: 83.6, child_detention_scale_score: 82.0, rehabilitation_failure_score: 80.0, age_criminal_responsibility_score: 88.0, torture_juvenile_detention_score: 85.0, risk_level: "critique", primary_pattern: "age_criminal_responsibility", estimated_juvenile_justice_index: 8.36, last_updated: "2026-06-20" },
    { id: "JJ-004", name: "Arabie Saoudite — Exécutions Mineurs, Flagellation & Conditions Détention Inhumaines", country: "Moyen-Orient", composite_score: 80.9, child_detention_scale_score: 78.0, rehabilitation_failure_score: 82.0, age_criminal_responsibility_score: 80.0, torture_juvenile_detention_score: 85.0, risk_level: "critique", primary_pattern: "torture_juvenile_detention", estimated_juvenile_justice_index: 8.09, last_updated: "2026-06-20" },
    { id: "JJ-005", name: "Inde — POCSO, Tribunaux Juvéniles Surchargés & Conditions Maisons de Correction Déplorables", country: "Asie du Sud", composite_score: 53.85, child_detention_scale_score: 52.0, rehabilitation_failure_score: 55.0, age_criminal_responsibility_score: 58.0, torture_juvenile_detention_score: 50.0, risk_level: "élevé", primary_pattern: "rehabilitation_failure", estimated_juvenile_justice_index: 5.39, last_updated: "2026-06-20" },
    { id: "JJ-006", name: "Brésil — FEBEM/FUNDAC, Massacres en Centres Jeunes & Surpopulation Systémique", country: "Amérique Latine", composite_score: 51.15, child_detention_scale_score: 50.0, rehabilitation_failure_score: 48.0, age_criminal_responsibility_score: 55.0, torture_juvenile_detention_score: 52.0, risk_level: "élevé", primary_pattern: "rehabilitation_failure", estimated_juvenile_justice_index: 5.12, last_updated: "2026-06-20" },
    { id: "JJ-007", name: "UE/Norvège — Justice Restaurative, Modèle Nordique & Déjudiciarisation Mineurs", country: "Europe", composite_score: 26.1, child_detention_scale_score: 22.0, rehabilitation_failure_score: 30.0, age_criminal_responsibility_score: 28.0, torture_juvenile_detention_score: 25.0, risk_level: "modéré", primary_pattern: "child_detention_scale", estimated_juvenile_justice_index: 2.61, last_updated: "2026-06-20" },
    { id: "JJ-008", name: "ONU/UNICEF — Convention Droits Enfant, Règles Beijing & Directives Riyad", country: "Global", composite_score: 4.4, child_detention_scale_score: 4.0, rehabilitation_failure_score: 5.0, age_criminal_responsibility_score: 3.0, torture_juvenile_detention_score: 6.0, risk_level: "faible", primary_pattern: "child_detention_scale", estimated_juvenile_justice_index: 0.44, last_updated: "2026-06-20" },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/juvenile-justice-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
