import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const MOCK = {
  agent: "Inventions Portfolio Engine Agent",
  domain: "inventions_portfolio",
  inventor: "Chaima Mhadbi",
  applicant: "Caelum Partners SPRL",
  total_inventions: 6,
  avg_patentability_score: 9.02,
  confidence_score: 0.95,
  avg_estimated_inventions_portfolio_index: 9.02,
  generation_distribution: { G1: 2, G2: 2, G3: 2 },
  risk_distribution: { critique: 2, "élevé": 3, modéré: 1, faible: 0 },
  data_sources: [
    "epo_patent_database_2026",
    "uspto_prior_art_search_2026",
    "caelum_swarm_intelligence_engines",
    "un_sdg_technology_frameworks",
  ],
  critical_alerts: [],
  entities: [
    {
      entity_id: "CAE-INV-001",
      name: "Scoring IA Droits Humains Automatisé",
      generation: "G1",
      ipc_class: "G06N 20/00",
      composite_score: 87.2,
      risk_level: "élevé",
      patentability_score: 8.72,
      filing_status: "draft",
    },
    {
      entity_id: "CAE-INV-002",
      name: "Détection Précoce Crises par IA",
      generation: "G1",
      ipc_class: "G06N 5/04",
      composite_score: 87.3,
      risk_level: "élevé",
      patentability_score: 8.73,
      filing_status: "draft",
    },
    {
      entity_id: "CAE-INV-003",
      name: "Apprentissage Fédéré Droits Humains",
      generation: "G2",
      ipc_class: "G06N 20/00 · H04L 9/32",
      composite_score: 89.9,
      risk_level: "élevé",
      patentability_score: 8.99,
      filing_status: "draft",
    },
    {
      entity_id: "CAE-INV-004",
      name: "Blockchain Preuves de Violations",
      generation: "G2",
      ipc_class: "H04L 9/32",
      composite_score: 90.1,
      risk_level: "critique",
      patentability_score: 9.01,
      filing_status: "draft",
    },
    {
      entity_id: "CAE-INV-005",
      name: "Plateforme ESG CSDDD Due Diligence",
      generation: "G3",
      ipc_class: "G06Q 10/06",
      composite_score: 92.9,
      risk_level: "critique",
      patentability_score: 9.29,
      filing_status: "draft",
    },
    {
      entity_id: "CAE-INV-006",
      name: "Indice Risque de Conflit Armé Multi-modal",
      generation: "G3",
      ipc_class: "G06N 20/00 · G06F 40/56",
      composite_score: 93.9,
      risk_level: "modéré",
      patentability_score: 9.39,
      filing_status: "draft",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    console.warn("[inventions-portfolio-engine] SWARM_API_URL not set — returning mock");
    return await sealResponse(NextResponse.json({ payload: MOCK }));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/inventions-portfolio-engine`, { next: { revalidate: 30 } });
    const data = await res.json();
    return await sealResponse(NextResponse.json({ payload: data }));
  } catch {
    return await sealResponse(NextResponse.json({ error: "upstream_error" }, { status: 502 }));
  }
}
