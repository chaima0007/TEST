import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[territory-optimizer] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "to_001",
    rep_name: "Julien Mercier",
    region: "Île-de-France",
    segment: "enterprise",
    quota_eur: 500000,
    territory_health: "poor",
    territory_action: "restructure",
    coverage_gap: "critical",
    workload_balance: "overloaded",
    territory_score: 18.4,
    coverage_pct: 21.0,
    icp_penetration_pct: 18.0,
    whitespace_opportunity_eur: 1250000,
    workload_ratio: 1.7,
    market_penetration_pct: 8.0,
    territory_drivers: [
      "Couverture territoire faible — seulement 21% des comptes actifs",
      "Pénétration ICP insuffisante — 18% des comptes ICP engagés",
      "50 comptes whitespace non contactés — opportunité non exploitée",
      "Territoire surchargé — 170 comptes vs. cible 100",
      "Pénétration marché faible — 8% du marché adressable capturé",
      "Activité outbound insuffisante — 12 actions sur 30j",
    ],
    territory_plays: [
      "Redécouper le territoire — analyse ICP et potentiel marché par zone",
      "Rééquilibrer les comptes avec le management — ajustement du portefeuille",
      "Définir les comptes prioritaires Q1 — focus sur les 20% à plus fort potentiel",
      "Activer le whitespace — plan d'attaque systématique sur les comptes non contactés",
    ],
    optimization_score: 14.2,
  },
  {
    rep_id: "to_002",
    rep_name: "Nadia Kowalski",
    region: "DACH",
    segment: "enterprise",
    quota_eur: 420000,
    territory_health: "poor",
    territory_action: "restructure",
    coverage_gap: "critical",
    workload_balance: "balanced",
    territory_score: 24.7,
    coverage_pct: 28.0,
    icp_penetration_pct: 22.0,
    whitespace_opportunity_eur: 960000,
    workload_ratio: 1.05,
    market_penetration_pct: 11.0,
    territory_drivers: [
      "Couverture territoire faible — seulement 28% des comptes actifs",
      "Pénétration ICP insuffisante — 22% des comptes ICP engagés",
      "40 comptes whitespace non contactés — opportunité non exploitée",
      "Pénétration marché faible — 11% du marché adressable capturé",
      "72 comptes dormants > 40 comptes actifs — déséquilibre",
    ],
    territory_plays: [
      "Redécouper le territoire — analyse ICP et potentiel marché par zone",
      "Rééquilibrer les comptes avec le management — ajustement du portefeuille",
      "Définir les comptes prioritaires Q1 — focus sur les 20% à plus fort potentiel",
      "Activer le whitespace — plan d'attaque systématique sur les comptes non contactés",
    ],
    optimization_score: 22.8,
  },
  {
    rep_id: "to_003",
    rep_name: "Arnaud Petit",
    region: "Rhône-Alpes",
    segment: "mid_market",
    quota_eur: 280000,
    territory_health: "fair",
    territory_action: "rebalance",
    coverage_gap: "significant",
    workload_balance: "overloaded",
    territory_score: 36.2,
    coverage_pct: 42.0,
    icp_penetration_pct: 38.0,
    whitespace_opportunity_eur: 480000,
    workload_ratio: 1.4,
    market_penetration_pct: 18.0,
    territory_drivers: [
      "Territoire surchargé — 140 comptes vs. cible 100",
      "Concentration géographique excessive — 75% du revenu sur une zone",
      "30 comptes whitespace non contactés — opportunité non exploitée",
    ],
    territory_plays: [
      "Rebalancer la charge de travail — identifier les comptes à transférer ou activer",
      "Prioriser les comptes ICP dormants — campagne de réactivation ciblée",
      "Optimiser les routes terrain — réduire les déplacements improductifs",
    ],
    optimization_score: 34.5,
  },
  {
    rep_id: "to_004",
    rep_name: "Isabelle Fontaine",
    region: "Bretagne-Normandie",
    segment: "mid_market",
    quota_eur: 220000,
    territory_health: "fair",
    territory_action: "rebalance",
    coverage_gap: "minor",
    workload_balance: "underloaded",
    territory_score: 42.8,
    coverage_pct: 55.0,
    icp_penetration_pct: 48.0,
    whitespace_opportunity_eur: 320000,
    workload_ratio: 0.62,
    market_penetration_pct: 22.0,
    territory_drivers: [
      "Territoire sous-chargé — 62 comptes vs. cible 100",
      "20 comptes whitespace non contactés — opportunité non exploitée",
    ],
    territory_plays: [
      "Rebalancer la charge de travail — identifier les comptes à transférer ou activer",
      "Prioriser les comptes ICP dormants — campagne de réactivation ciblée",
      "Optimiser les routes terrain — réduire les déplacements improductifs",
    ],
    optimization_score: 42.1,
  },
  {
    rep_id: "to_005",
    rep_name: "Renaud Blanc",
    region: "Sud-Ouest",
    segment: "mid_market",
    quota_eur: 260000,
    territory_health: "good",
    territory_action: "expand",
    coverage_gap: "minor",
    workload_balance: "balanced",
    territory_score: 58.3,
    coverage_pct: 62.0,
    icp_penetration_pct: 57.0,
    whitespace_opportunity_eur: 200000,
    workload_ratio: 0.95,
    market_penetration_pct: 28.0,
    territory_drivers: [
      "15 comptes whitespace non contactés — opportunité non exploitée",
    ],
    territory_plays: [
      "Étendre la couverture — 5 nouveaux comptes ICP par semaine",
      "Intensifier l'outbound sur le whitespace — ABM et séquences personnalisées",
      "Activer les signaux d'intention — prioriser les comptes avec intent data",
      "Capitaliser sur les 8 signaux expansion détectés",
    ],
    optimization_score: 54.7,
  },
  {
    rep_id: "to_006",
    rep_name: "Claire Morin",
    region: "Pays-de-la-Loire",
    segment: "mid_market",
    quota_eur: 240000,
    territory_health: "good",
    territory_action: "optimize",
    coverage_gap: "none",
    workload_balance: "balanced",
    territory_score: 67.4,
    coverage_pct: 74.0,
    icp_penetration_pct: 71.0,
    whitespace_opportunity_eur: 120000,
    workload_ratio: 1.02,
    market_penetration_pct: 34.0,
    territory_drivers: [],
    territory_plays: [
      "Affiner la segmentation — micro-ciblage des comptes à meilleur potentiel",
      "Chercher des opportunités d'expansion sur les comptes actifs",
      "Anticiper la couverture du prochain trimestre",
    ],
    optimization_score: 63.2,
  },
  {
    rep_id: "to_007",
    rep_name: "Vincent Leroux",
    region: "Grand-Est",
    segment: "enterprise",
    quota_eur: 380000,
    territory_health: "excellent",
    territory_action: "optimize",
    coverage_gap: "none",
    workload_balance: "balanced",
    territory_score: 79.6,
    coverage_pct: 82.0,
    icp_penetration_pct: 78.0,
    whitespace_opportunity_eur: 60000,
    workload_ratio: 1.0,
    market_penetration_pct: 42.0,
    territory_drivers: [],
    territory_plays: [
      "Affiner la segmentation — micro-ciblage des comptes à meilleur potentiel",
      "Chercher des opportunités d'expansion sur les comptes actifs",
      "Anticiper la couverture du prochain trimestre",
    ],
    optimization_score: 74.8,
  },
  {
    rep_id: "to_008",
    rep_name: "Amélie Rousseau",
    region: "Nouvelle-Aquitaine",
    segment: "enterprise",
    quota_eur: 440000,
    territory_health: "excellent",
    territory_action: "optimize",
    coverage_gap: "none",
    workload_balance: "balanced",
    territory_score: 88.1,
    coverage_pct: 91.0,
    icp_penetration_pct: 87.0,
    whitespace_opportunity_eur: 25000,
    workload_ratio: 0.98,
    market_penetration_pct: 52.0,
    territory_drivers: [],
    territory_plays: [
      "Affiner la segmentation — micro-ciblage des comptes à meilleur potentiel",
      "Chercher des opportunités d'expansion sur les comptes actifs",
      "Anticiper la couverture du prochain trimestre",
    ],
    optimization_score: 86.3,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const health = searchParams.get("health");
  const action = searchParams.get("action");
  const gap = searchParams.get("gap");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/territory-optimizer`);
      if (health) url.searchParams.set("health", health);
      if (action) url.searchParams.set("action", action);
      if (gap) url.searchParams.set("gap", gap);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (health) reps = reps.filter((r) => r.territory_health === health);
  if (action) reps = reps.filter((r) => r.territory_action === action);
  if (gap) reps = reps.filter((r) => r.coverage_gap === gap);

  const health_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const gap_counts: Record<string, number> = {};
  let total_score = 0;
  let total_coverage = 0;
  let total_opt = 0;
  let total_whitespace = 0;

  for (const r of mockReps) {
    health_counts[r.territory_health] = (health_counts[r.territory_health] || 0) + 1;
    action_counts[r.territory_action] = (action_counts[r.territory_action] || 0) + 1;
    gap_counts[r.coverage_gap] = (gap_counts[r.coverage_gap] || 0) + 1;
    total_score += r.territory_score;
    total_coverage += r.coverage_pct;
    total_opt += r.optimization_score;
    total_whitespace += r.whitespace_opportunity_eur;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total: n,
      health_counts,
      action_counts,
      gap_counts,
      avg_territory_score: Math.round((total_score / n) * 10) / 10,
      avg_coverage_pct: Math.round((total_coverage / n) * 10) / 10,
      avg_optimization_score: Math.round((total_opt / n) * 10) / 10,
      poor_count: mockReps.filter((r) => r.territory_health === "poor").length,
      restructure_count: mockReps.filter((r) => r.territory_action === "restructure").length,
      total_whitespace_eur: total_whitespace,
    },
  }));
}
