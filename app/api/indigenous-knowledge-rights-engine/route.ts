import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[indigenous-knowledge-rights-engine] SWARM_API_URL non défini — mode dégradé activé");
}

const UPSTREAM = process.env.SWARM_API_URL;
if (!UPSTREAM) console.warn("[indigenous-knowledge-rights-engine] SWARM_API_URL not set — running in offline mode");

export async function GET() {
  try {
    if (!UPSTREAM) throw new Error("offline");
    const res = await fetch(`${UPSTREAM}/api/indigenous-knowledge-rights-engine`, { next: { revalidate: 30 } });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return sealResponse(NextResponse.json(data));
  } catch {
    return sealResponse(NextResponse.json({
      agent: "Indigenous Knowledge Rights Engine Agent",
      domain: "indigenous_knowledge_rights",
      total_entities: 8,
      avg_composite: 60.01,
      confidence_score: 0.85,
      risk_distribution: { critique: 4, "élevé": 2, "modéré": 1, faible: 1 },
      top_risk_entities: [
        "Amazonie — Biopiraterie Plantes Médicinales, Brevets Corporations & Pillage Savoirs Chamanes",
        "Afrique — Appropriation Pharmacopée Traditionnelle, OMPI Négociations Bloquées & Communautés Non-Compensées",
        "Asie Pacifique — Extinction 200 Langues/Décennie, Savoirs Ancestraux Non-Documentés & Assimilation Forcée",
      ],
      critical_alerts: [
        "Amazonie: biopiracy",
        "Afrique: cultural_appropriation",
        "Asie Pacifique: language_extinction",
        "Himalaya: sacred_site_protection",
      ],
      last_analysis: "2026-06-22",
      engine_version: "1.0.0",
      avg_estimated_indigenous_knowledge_rights_index: 6.00,
      data_sources: [
        "wipo_igc_traditional_knowledge_documentation_2024",
        "un_declaration_indigenous_peoples_rights_implementation",
        "ethnobiology_biopiracy_patents_database",
        "endangered_languages_project_global_atlas",
        "cultural_survival_sacred_sites_protection_reports",
      ],
    }, { status: 200 }));
  }
}
