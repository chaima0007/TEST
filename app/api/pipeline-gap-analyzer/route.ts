import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "pg_001",
    rep_name: "Alexia Moreau",
    region: "France",
    segment: "enterprise",
    quota_eur: 400000,
    gap_eur: 180000,
    gap_severity: "critical",
    pipeline_action: "emergency",
    quota_risk: "critical",
    coverage_health: "insufficient",
    coverage_ratio: 0.8,
    expected_close_eur: 52000,
    quota_remaining_eur: 232000,
    attainment_pct: 42.0,
    run_rate_pct: 52.3,
    gap_drivers: [
      "Couverture pipeline insuffisante — 0.8x (seuil: 3x)",
      "Rythme de vente insuffisant — pace à 52% vs. objectif",
      "Génération de pipeline faible — seulement 1 nouvelles opportunités sur 30j",
      "Entonnoir déséquilibré — trop de pipeline en early stage",
      "Taux de signature faible (12%) — qualification à améliorer",
    ],
    gap_closers: [
      "Prospection intensive immédiate — 10 nouveaux comptes ciblés cette semaine",
      "Réactiver les deals dormants — relancer les opportunités stagnantes",
      "Demander des introductions client — activer le réseau et les références",
      "Concentrer 80% du temps sur les deals closing stage — maximiser la signature",
    ],
    pipeline_score: 11.2,
  },
  {
    rep_id: "pg_002",
    rep_name: "Thomas Lehmann",
    region: "DACH",
    segment: "enterprise",
    quota_eur: 350000,
    gap_eur: 124000,
    gap_severity: "severe",
    pipeline_action: "emergency",
    quota_risk: "behind",
    coverage_health: "insufficient",
    coverage_ratio: 1.4,
    expected_close_eur: 68000,
    quota_remaining_eur: 192000,
    attainment_pct: 45.1,
    run_rate_pct: 61.8,
    gap_drivers: [
      "Couverture pipeline insuffisante — 1.4x (seuil: 3x)",
      "Rythme de vente insuffisant — pace à 62% vs. objectif",
      "Génération de pipeline faible — seulement 2 nouvelles opportunités sur 30j",
      "Cycle de vente moyen (95j) > jours restants (60j)",
    ],
    gap_closers: [
      "Prospection intensive immédiate — 10 nouveaux comptes ciblés cette semaine",
      "Réactiver les deals dormants — relancer les opportunités stagnantes",
      "Demander des introductions client — activer le réseau et les références",
    ],
    pipeline_score: 24.5,
  },
  {
    rep_id: "pg_003",
    rep_name: "Camille Dupont",
    region: "France",
    segment: "mid_market",
    quota_eur: 200000,
    gap_eur: 55000,
    gap_severity: "moderate",
    pipeline_action: "build",
    quota_risk: "behind",
    coverage_health: "thin",
    coverage_ratio: 2.1,
    expected_close_eur: 82000,
    quota_remaining_eur: 137000,
    attainment_pct: 31.5,
    run_rate_pct: 63.0,
    gap_drivers: [
      "Pipeline mince — couverture 2.1x seulement",
      "Rythme de vente insuffisant — pace à 63% vs. objectif",
      "Entonnoir déséquilibré — trop de pipeline en early stage",
    ],
    gap_closers: [
      "Intensifier la génération de pipeline — 5 nouveaux comptes par semaine",
      "Maximiser les activités outbound — emails, appels, LinkedIn",
      "Cibler les comptes ICP non prospectés — liste ABM à activer",
    ],
    pipeline_score: 36.8,
  },
  {
    rep_id: "pg_004",
    rep_name: "Marco Ricci",
    region: "Southern Europe",
    segment: "mid_market",
    quota_eur: 180000,
    gap_eur: 38000,
    gap_severity: "moderate",
    pipeline_action: "build",
    quota_risk: "at_risk",
    coverage_health: "thin",
    coverage_ratio: 2.4,
    expected_close_eur: 74000,
    quota_remaining_eur: 112000,
    attainment_pct: 37.8,
    run_rate_pct: 71.2,
    gap_drivers: [
      "Pipeline mince — couverture 2.4x seulement",
      "Génération de pipeline faible — seulement 2 nouvelles opportunités sur 30j",
    ],
    gap_closers: [
      "Intensifier la génération de pipeline — 5 nouveaux comptes par semaine",
      "Maximiser les activités outbound — emails, appels, LinkedIn",
      "Cibler les comptes ICP non prospectés — liste ABM à activer",
    ],
    pipeline_score: 42.3,
  },
  {
    rep_id: "pg_005",
    rep_name: "Sophie Andersen",
    region: "Nordics",
    segment: "mid_market",
    quota_eur: 160000,
    gap_eur: 18000,
    gap_severity: "minor",
    pipeline_action: "accelerate",
    quota_risk: "at_risk",
    coverage_health: "adequate",
    coverage_ratio: 3.2,
    expected_close_eur: 72000,
    quota_remaining_eur: 90000,
    attainment_pct: 43.8,
    run_rate_pct: 82.4,
    gap_drivers: [
      "Suivi insuffisant — 45% de taux de follow-up",
    ],
    gap_closers: [
      "Accélérer les deals en stage 2 et 3 — réduire le cycle de décision",
      "Qualifier et éliminer les deals fantômes — nettoyer le CRM",
      "Préparer les propositions en attente — débloquer les deals stagnants",
    ],
    pipeline_score: 58.6,
  },
  {
    rep_id: "pg_006",
    rep_name: "Lucas Bernard",
    region: "France",
    segment: "enterprise",
    quota_eur: 450000,
    gap_eur: 9000,
    gap_severity: "minor",
    pipeline_action: "accelerate",
    quota_risk: "at_risk",
    coverage_health: "adequate",
    coverage_ratio: 3.5,
    expected_close_eur: 168000,
    quota_remaining_eur: 177000,
    attainment_pct: 60.7,
    run_rate_pct: 85.6,
    gap_drivers: [
      "Rythme de vente insuffisant — pace à 86% vs. objectif",
    ],
    gap_closers: [
      "Accélérer les deals en stage 2 et 3 — réduire le cycle de décision",
      "Qualifier et éliminer les deals fantômes — nettoyer le CRM",
      "Préparer les propositions en attente — débloquer les deals stagnants",
    ],
    pipeline_score: 67.4,
  },
  {
    rep_id: "pg_007",
    rep_name: "Elena Vasquez",
    region: "Iberia",
    segment: "mid_market",
    quota_eur: 220000,
    gap_eur: 0,
    gap_severity: "none",
    pipeline_action: "maintain",
    quota_risk: "on_track",
    coverage_health: "healthy",
    coverage_ratio: 4.8,
    expected_close_eur: 115000,
    quota_remaining_eur: 88000,
    attainment_pct: 60.0,
    run_rate_pct: 96.2,
    gap_drivers: [],
    gap_closers: [
      "Maintenir la cadence d'activité — objectifs de pipeline respectés",
      "Chercher des opportunités d'expansion sur les comptes existants",
      "Anticiper le pipeline du prochain trimestre",
    ],
    pipeline_score: 79.1,
  },
  {
    rep_id: "pg_008",
    rep_name: "David Kim",
    region: "Benelux",
    segment: "enterprise",
    quota_eur: 380000,
    gap_eur: 0,
    gap_severity: "none",
    pipeline_action: "maintain",
    quota_risk: "on_track",
    coverage_health: "healthy",
    coverage_ratio: 5.2,
    expected_close_eur: 182000,
    quota_remaining_eur: 114000,
    attainment_pct: 70.0,
    run_rate_pct: 104.5,
    gap_drivers: [],
    gap_closers: [
      "Maintenir la cadence d'activité — objectifs de pipeline respectés",
      "Chercher des opportunités d'expansion sur les comptes existants",
      "Anticiper le pipeline du prochain trimestre",
    ],
    pipeline_score: 91.3,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const severity = searchParams.get("severity");
  const action = searchParams.get("action");
  const risk = searchParams.get("risk");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/pipeline-gap-analyzer`);
      if (severity) url.searchParams.set("severity", severity);
      if (action) url.searchParams.set("action", action);
      if (risk) url.searchParams.set("risk", risk);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (severity) reps = reps.filter((r) => r.gap_severity === severity);
  if (action) reps = reps.filter((r) => r.pipeline_action === action);
  if (risk) reps = reps.filter((r) => r.quota_risk === risk);

  const severity_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const risk_counts: Record<string, number> = {};
  let total_score = 0;
  let total_gap = 0;
  let total_coverage = 0;
  let coverage_n = 0;

  for (const r of mockReps) {
    severity_counts[r.gap_severity] = (severity_counts[r.gap_severity] || 0) + 1;
    action_counts[r.pipeline_action] = (action_counts[r.pipeline_action] || 0) + 1;
    risk_counts[r.quota_risk] = (risk_counts[r.quota_risk] || 0) + 1;
    total_score += r.pipeline_score;
    total_gap += r.gap_eur;
    if (r.coverage_ratio < 99) {
      total_coverage += r.coverage_ratio;
      coverage_n++;
    }
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total: n,
      severity_counts,
      action_counts,
      risk_counts,
      avg_pipeline_score: Math.round((total_score / n) * 10) / 10,
      avg_coverage_ratio: coverage_n > 0 ? Math.round((total_coverage / coverage_n) * 100) / 100 : 0,
      critical_count: mockReps.filter((r) => r.gap_severity === "critical").length,
      emergency_count: mockReps.filter((r) => r.pipeline_action === "emergency").length,
      total_gap_eur: total_gap,
    },
  });
}
