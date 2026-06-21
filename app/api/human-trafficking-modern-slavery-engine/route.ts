import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "human_trafficking_modern_slavery_engine",
  domain: "human_trafficking_modern_slavery",
  total_entities: 8,
  avg_composite: 62.02,
  confidence_score: 0.89,
  avg_estimated_human_trafficking_modern_slavery_index: 6.20,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  data_sources: [
    "ilo_global_estimates_modern_slavery_2022",
    "unodc_global_trafficking_report_2023",
    "walk_free_global_slavery_index_2023",
    "polaris_project_national_human_trafficking_hotline",
  ],
  critical_alerts: [
    "Corée du Nord/Travail Forcé État: trafic_echelle_recrutement_victimes",
    "Érythrée/Service National Indéfini: trafic_echelle_recrutement_victimes",
    "Thaïlande/Pêche Esclavage En Mer: travail_force_exploitation_sexuelle_severite",
    "Mauritanie/Esclavage Héréditaire: trafic_echelle_recrutement_victimes",
  ],
  entities: [
    {
      entity_id: "HTMS-001",
      name: "Corée du Nord/Travail Forcé État",
      country: "Asie du Nord-Est",
      composite_score: 91.6,
      risk_level: "critique",
      primary_pattern: "trafic_echelle_recrutement_victimes",
      estimated_human_trafficking_modern_slavery_index: 9.16,
    },
    {
      entity_id: "HTMS-002",
      name: "Érythrée/Service National Indéfini",
      country: "Afrique de l'Est",
      composite_score: 86.65,
      risk_level: "critique",
      primary_pattern: "trafic_echelle_recrutement_victimes",
      estimated_human_trafficking_modern_slavery_index: 8.67,
    },
    {
      entity_id: "HTMS-003",
      name: "Thaïlande/Pêche Esclavage En Mer",
      country: "Asie du Sud-Est",
      composite_score: 82.1,
      risk_level: "critique",
      primary_pattern: "travail_force_exploitation_sexuelle_severite",
      estimated_human_trafficking_modern_slavery_index: 8.21,
    },
    {
      entity_id: "HTMS-004",
      name: "Mauritanie/Esclavage Héréditaire",
      country: "Afrique de l'Ouest",
      composite_score: 80.5,
      risk_level: "critique",
      primary_pattern: "trafic_echelle_recrutement_victimes",
      estimated_human_trafficking_modern_slavery_index: 8.05,
    },
    {
      entity_id: "HTMS-005",
      name: "Inde/Travail Bonded 8M Walk Free",
      country: "Asie du Sud",
      composite_score: 59.6,
      risk_level: "élevé",
      primary_pattern: "travail_force_exploitation_sexuelle_severite",
      estimated_human_trafficking_modern_slavery_index: 5.96,
    },
    {
      entity_id: "HTMS-006",
      name: "Cambodge/Trafic Forcé Centres Arnaques",
      country: "Asie du Sud-Est",
      composite_score: 56.9,
      risk_level: "élevé",
      primary_pattern: "travail_force_exploitation_sexuelle_severite",
      estimated_human_trafficking_modern_slavery_index: 5.69,
    },
    {
      entity_id: "HTMS-007",
      name: "Mexique/Traite Routiers Migratoires",
      country: "Amérique Centrale",
      composite_score: 34.4,
      risk_level: "modéré",
      primary_pattern: "travail_force_exploitation_sexuelle_severite",
      estimated_human_trafficking_modern_slavery_index: 3.44,
    },
    {
      entity_id: "HTMS-008",
      name: "Pays-Bas/Mécanisme National Référence",
      country: "Europe Occidentale",
      composite_score: 4.4,
      risk_level: "faible",
      primary_pattern: "absence_systeme_protection_soutien_victimes",
      estimated_human_trafficking_modern_slavery_index: 0.44,
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[human_trafficking_modern_slavery-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/human-trafficking-modern-slavery-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
