import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[patent-revenue-prioritization-engine] SWARM_API_URL is not set — falling back to mock data");
}

const MOCK = {
  agent: "Patent Revenue Prioritization Engine Agent",
  domain: "patent_revenue_prioritization",
  total_entities: 8,
  avg_composite: 62.54,
  confidence_score: 0.94,
  risk_distribution: { critique: 4, "élevé": 2, modéré: 1, faible: 1 },
  pattern_distribution: {
    filing_urgency: 1,
    competitive_moat: 4,
    market_size_potential: 2,
    licensing_revenue_potential: 1,
  },
  top_risk_entities: [
    "CAE-INV-005 — ESG CSDDD Compliance Engine (50 000 entreprises EU obligées 2026)",
    "CAE-INV-006 — Risque Conflit Armé & Analyse Géopolitique IA (Défense/Gouvernements)",
    "CAE-INV-004 — Blockchain Preuves Droits Humains (Legal Tech & Justice Internationale)",
  ],
  critical_alerts: [
    "CAE-INV-005: filing_urgency — EPO FILING URGENT",
    "CAE-INV-006: competitive_moat — EPO FILING URGENT",
    "CAE-INV-004: competitive_moat — EPO FILING URGENT",
    "CAE-INV-007: competitive_moat — EPO FILING URGENT",
  ],
  last_analysis: "2026-06-21",
  engine_version: "1.0.0",
  avg_estimated_patent_revenue_prioritization_index: 6.25,
  data_sources: [
    "epo_patent_analytics_2026",
    "caelum_market_analysis_2026",
    "eu_csddd_implementation_tracker_2026",
    "un_sdg_technology_licensing_2025",
  ],
  revenue_forecast: {
    "CAE-INV-005": {
      market: "EU CSDDD compliance",
      target_companies: 50000,
      license_fee_eur: 15000,
      annual_potential: "750M EUR",
    },
    "CAE-INV-006": {
      market: "Defense/Government",
      target_contracts: 50,
      license_fee_eur: 500000,
      annual_potential: "25M EUR",
    },
    "CAE-INV-004": {
      market: "Legal Tech",
      target_companies: 5000,
      license_fee_eur: 20000,
      annual_potential: "100M EUR",
    },
    "CAE-INV-007": {
      market: "AI Platform SaaS",
      target_companies: 10000,
      license_fee_eur: 8000,
      annual_potential: "80M EUR",
    },
    "CAE-INV-003": {
      market: "FinTech / HealthTech Privacy",
      target_companies: 3000,
      license_fee_eur: 25000,
      annual_potential: "75M EUR",
    },
    "CAE-INV-008": {
      market: "ESG SaaS",
      target_companies: 20000,
      license_fee_eur: 5000,
      annual_potential: "100M EUR",
    },
  },
  entities: [
    {
      id: "PAT-001",
      name: "CAE-INV-005 — ESG CSDDD Compliance Engine (50 000 entreprises EU obligées 2026)",
      invention_code: "CAE-INV-005",
      market_size_potential: 98.0,
      competitive_moat: 92.0,
      filing_urgency: 95.0,
      licensing_revenue_potential: 95.0,
      composite_score: 95.15,
      risk_level: "critique",
      primary_pattern: "filing_urgency",
      estimated_patent_revenue_prioritization_index: 9.52,
      last_updated: "2026-06-21",
    },
    {
      id: "PAT-002",
      name: "CAE-INV-006 — Risque Conflit Armé & Analyse Géopolitique IA (Défense/Gouvernements)",
      invention_code: "CAE-INV-006",
      market_size_potential: 88.0,
      competitive_moat: 95.0,
      filing_urgency: 90.0,
      licensing_revenue_potential: 92.0,
      composite_score: 91.05,
      risk_level: "critique",
      primary_pattern: "competitive_moat",
      estimated_patent_revenue_prioritization_index: 9.11,
      last_updated: "2026-06-21",
    },
    {
      id: "PAT-003",
      name: "CAE-INV-004 — Blockchain Preuves Droits Humains (Legal Tech & Justice Internationale)",
      invention_code: "CAE-INV-004",
      market_size_potential: 85.0,
      competitive_moat: 90.0,
      filing_urgency: 88.0,
      licensing_revenue_potential: 88.0,
      composite_score: 87.6,
      risk_level: "critique",
      primary_pattern: "competitive_moat",
      estimated_patent_revenue_prioritization_index: 8.76,
      last_updated: "2026-06-21",
    },
    {
      id: "PAT-004",
      name: "CAE-INV-007 — AI Scoring V2 Droits Humains Gen4 (Prochaine Génération Moteurs)",
      invention_code: "CAE-INV-007",
      market_size_potential: 82.0,
      competitive_moat: 88.0,
      filing_urgency: 85.0,
      licensing_revenue_potential: 80.0,
      composite_score: 83.85,
      risk_level: "critique",
      primary_pattern: "competitive_moat",
      estimated_patent_revenue_prioritization_index: 8.38,
      last_updated: "2026-06-21",
    },
    {
      id: "PAT-005",
      name: "CAE-INV-003 — Federated Learning Données Sensibles (Privacy-Preserving AI Analytics)",
      invention_code: "CAE-INV-003",
      market_size_potential: 52.0,
      competitive_moat: 55.0,
      filing_urgency: 48.0,
      licensing_revenue_potential: 50.0,
      composite_score: 51.6,
      risk_level: "élevé",
      primary_pattern: "competitive_moat",
      estimated_patent_revenue_prioritization_index: 5.16,
      last_updated: "2026-06-21",
    },
    {
      id: "PAT-006",
      name: "CAE-INV-008 — ESG Reporting Automatisé Gen4 (CSRD/GRI/SASB Multi-Framework)",
      invention_code: "CAE-INV-008",
      market_size_potential: 58.0,
      competitive_moat: 45.0,
      filing_urgency: 52.0,
      licensing_revenue_potential: 48.0,
      composite_score: 51.35,
      risk_level: "élevé",
      primary_pattern: "market_size_potential",
      estimated_patent_revenue_prioritization_index: 5.14,
      last_updated: "2026-06-21",
    },
    {
      id: "PAT-007",
      name: "CAE-INV-002 — Détection Crises Humanitaires Précoce (Early Warning System)",
      invention_code: "CAE-INV-002",
      market_size_potential: 35.0,
      competitive_moat: 28.0,
      filing_urgency: 22.0,
      licensing_revenue_potential: 30.0,
      composite_score: 29.0,
      risk_level: "modéré",
      primary_pattern: "market_size_potential",
      estimated_patent_revenue_prioritization_index: 2.9,
      last_updated: "2026-06-21",
    },
    {
      id: "PAT-008",
      name: "CAE-INV-001 — Scoring IA Droits Humains V1 (Protection En Cours — Dépôt Initial)",
      invention_code: "CAE-INV-001",
      market_size_potential: 12.0,
      competitive_moat: 10.0,
      filing_urgency: 8.0,
      licensing_revenue_potential: 15.0,
      composite_score: 11.1,
      risk_level: "faible",
      primary_pattern: "licensing_revenue_potential",
      estimated_patent_revenue_prioritization_index: 1.11,
      last_updated: "2026-06-21",
    },
  ],
};

export async function GET() {
  if (!process.env.SWARM_API_URL) {
    return NextResponse.json(await sealResponse(MOCK));
  }
  try {
    const res = await fetch(`${process.env.SWARM_API_URL}/patent-revenue-prioritization-engine`, {
      next: { revalidate: 30 },
    });
    if (!res.ok) throw new Error(`upstream ${res.status}`);
    const data = await res.json();
    return NextResponse.json(await sealResponse(data));
  } catch {
    return NextResponse.json(await sealResponse(MOCK), { status: 502 });
  }
}
