import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "qa_001",
    rep_name: "Léa Bertrand",
    region: "France",
    segment: "enterprise",
    quota_eur: 400000,
    current_attainment_pct: 72.5,
    projected_attainment_pct: 118.2,
    projected_closed_eur: 472800,
    gap_to_quota_eur: 0,
    attainment_outcome: "overachieve",
    confidence: "high",
    quota_action: "maintain",
    run_rate_pct: 108.6,
    pipeline_coverage_ratio: 4.2,
    weighted_pipeline_eur: 182800,
    historical_avg_attainment_pct: 112.0,
    prediction_drivers: [
      "Closé YTD: 290,000€ — base solide",
      "Couverture pipeline 4.2x — réservoir suffisant",
      "Run rate 109% — rythme en ligne avec l'objectif",
      "Historique d'atteinte fort — moyenne 112%",
      "Deals closing stage: 120,000€ — à signer",
      "Confiance rep élevée (8/10)",
    ],
    prediction_risks: [],
    action_plan: [
      "Maintenir la cadence — objectif quota sur la bonne trajectoire",
      "Anticiper le pipeline du trimestre suivant",
      "Chercher des opportunités d'expansion sur les comptes actifs",
    ],
  },
  {
    rep_id: "qa_002",
    rep_name: "François Aubert",
    region: "Benelux",
    segment: "enterprise",
    quota_eur: 350000,
    current_attainment_pct: 65.7,
    projected_attainment_pct: 102.4,
    projected_closed_eur: 358400,
    gap_to_quota_eur: 0,
    attainment_outcome: "achieve",
    confidence: "high",
    quota_action: "maintain",
    run_rate_pct: 96.2,
    pipeline_coverage_ratio: 3.5,
    weighted_pipeline_eur: 128400,
    historical_avg_attainment_pct: 98.5,
    prediction_drivers: [
      "Closé YTD: 230,000€ — base solide",
      "Couverture pipeline 3.5x — réservoir suffisant",
      "Run rate 96% — rythme en ligne avec l'objectif",
      "Deals closing stage: 85,000€ — à signer",
    ],
    prediction_risks: [],
    action_plan: [
      "Maintenir la cadence — objectif quota sur la bonne trajectoire",
      "Anticiper le pipeline du trimestre suivant",
      "Chercher des opportunités d'expansion sur les comptes actifs",
    ],
  },
  {
    rep_id: "qa_003",
    rep_name: "Inès Charpentier",
    region: "DACH",
    segment: "mid_market",
    quota_eur: 240000,
    current_attainment_pct: 54.2,
    projected_attainment_pct: 88.6,
    projected_closed_eur: 212640,
    gap_to_quota_eur: 27360,
    attainment_outcome: "slight_miss",
    confidence: "medium",
    quota_action: "accelerate",
    run_rate_pct: 81.3,
    pipeline_coverage_ratio: 2.8,
    weighted_pipeline_eur: 82640,
    historical_avg_attainment_pct: 88.0,
    prediction_drivers: [
      "Closé YTD: 130,000€ — base solide",
      "Couverture pipeline 2.8x — réservoir suffisant",
      "Deals closing stage: 45,000€ — à signer",
    ],
    prediction_risks: [
      "Run rate faible (81%) — rythme de closing en retard",
    ],
    action_plan: [
      "Accélérer le closing — réduire le cycle de vente de 20%",
      "Prioriser les deals à fort potentiel de closing rapide",
      "Maximiser les activités outbound pour alimenter la fin de période",
    ],
  },
  {
    rep_id: "qa_004",
    rep_name: "Pierre-Louis Gallet",
    region: "Nordics",
    segment: "mid_market",
    quota_eur: 200000,
    current_attainment_pct: 45.0,
    projected_attainment_pct: 78.2,
    projected_closed_eur: 156400,
    gap_to_quota_eur: 43600,
    attainment_outcome: "slight_miss",
    confidence: "medium",
    quota_action: "accelerate",
    run_rate_pct: 67.5,
    pipeline_coverage_ratio: 2.4,
    weighted_pipeline_eur: 66400,
    historical_avg_attainment_pct: 82.0,
    prediction_drivers: [
      "Closé YTD: 90,000€ — base solide",
      "Couverture pipeline 2.4x — réservoir suffisant",
    ],
    prediction_risks: [
      "Run rate faible (68%) — rythme de closing en retard",
      "Génération de pipeline faible (2 deals/30j)",
    ],
    action_plan: [
      "Accélérer le closing — réduire le cycle de vente de 20%",
      "Prioriser les deals à fort potentiel de closing rapide",
      "Maximiser les activités outbound pour alimenter la fin de période",
    ],
  },
  {
    rep_id: "qa_005",
    rep_name: "Mathilde Escoffier",
    region: "Southern Europe",
    segment: "mid_market",
    quota_eur: 180000,
    current_attainment_pct: 36.1,
    projected_attainment_pct: 62.4,
    projected_closed_eur: 112320,
    gap_to_quota_eur: 67680,
    attainment_outcome: "miss",
    confidence: "low",
    quota_action: "intervention",
    run_rate_pct: 54.2,
    pipeline_coverage_ratio: 1.6,
    weighted_pipeline_eur: 47320,
    historical_avg_attainment_pct: 74.0,
    prediction_drivers: [
      "Closé YTD: 65,000€ — base solide",
    ],
    prediction_risks: [
      "Couverture pipeline insuffisante (1.6x) — pipeline sous-alimenté",
      "Run rate faible (54%) — rythme de closing en retard",
      "Génération de pipeline faible (1 deals/30j)",
      "Historique d'atteinte fragile — moyenne 74%",
    ],
    action_plan: [
      "Session de coaching hebdomadaire — focus deals closing stage",
      "Combler le gap de 67,680€ — plan d'action deal par deal",
      "Accélérer les deals en stage 2 — propositions et démos urgentes",
      "Revue pipeline bi-mensuelle avec le manager",
    ],
  },
  {
    rep_id: "qa_006",
    rep_name: "Romain Garnier",
    region: "France",
    segment: "enterprise",
    quota_eur: 450000,
    current_attainment_pct: 28.9,
    projected_attainment_pct: 55.8,
    projected_closed_eur: 251100,
    gap_to_quota_eur: 198900,
    attainment_outcome: "miss",
    confidence: "low",
    quota_action: "intervention",
    run_rate_pct: 43.3,
    pipeline_coverage_ratio: 1.8,
    weighted_pipeline_eur: 121100,
    historical_avg_attainment_pct: 71.0,
    prediction_drivers: [
      "Closé YTD: 130,000€ — base solide",
      "Deals closing stage: 80,000€ — à signer",
    ],
    prediction_risks: [
      "Couverture pipeline insuffisante (1.8x) — pipeline sous-alimenté",
      "Run rate faible (43%) — rythme de closing en retard",
      "Génération de pipeline faible (2 deals/30j)",
      "Historique d'atteinte fragile — moyenne 71%",
    ],
    action_plan: [
      "Session de coaching hebdomadaire — focus deals closing stage",
      "Combler le gap de 198,900€ — plan d'action deal par deal",
      "Accélérer les deals en stage 2 — propositions et démos urgentes",
      "Revue pipeline bi-mensuelle avec le manager",
    ],
  },
  {
    rep_id: "qa_007",
    rep_name: "Agathe Renault",
    region: "Iberia",
    segment: "mid_market",
    quota_eur: 160000,
    current_attainment_pct: 18.8,
    projected_attainment_pct: 38.5,
    projected_closed_eur: 61600,
    gap_to_quota_eur: 98400,
    attainment_outcome: "critical_miss",
    confidence: "very_low",
    quota_action: "escalate",
    run_rate_pct: 28.1,
    pipeline_coverage_ratio: 0.9,
    weighted_pipeline_eur: 31600,
    historical_avg_attainment_pct: 52.0,
    prediction_drivers: [],
    prediction_risks: [
      "Couverture pipeline insuffisante (0.9x) — pipeline sous-alimenté",
      "Run rate faible (28%) — rythme de closing en retard",
      "Génération de pipeline faible (0 deals/30j)",
      "Taux de signature faible (12%) — conversion à améliorer",
      "Historique d'atteinte fragile — moyenne 52%",
      "Projection en deçà des 70% — intervention nécessaire",
      "Confiance rep faible (2/10) — signal d'alerte",
    ],
    action_plan: [
      "Escalade manager immédiate — revue pipeline deal by deal",
      "Identifier les deals à impact rapide — closing sprint 30j",
      "Support commercial renforcé — coach deal, exec selling",
      "Revoir les objectifs de fin de période avec le management",
    ],
  },
  {
    rep_id: "qa_008",
    rep_name: "Noé Lombard",
    region: "DACH",
    segment: "enterprise",
    quota_eur: 380000,
    current_attainment_pct: 13.2,
    projected_attainment_pct: 28.1,
    projected_closed_eur: 106780,
    gap_to_quota_eur: 273220,
    attainment_outcome: "critical_miss",
    confidence: "very_low",
    quota_action: "escalate",
    run_rate_pct: 19.7,
    pipeline_coverage_ratio: 0.6,
    weighted_pipeline_eur: 56780,
    historical_avg_attainment_pct: 45.0,
    prediction_drivers: [],
    prediction_risks: [
      "Couverture pipeline insuffisante (0.6x) — pipeline sous-alimenté",
      "Run rate faible (20%) — rythme de closing en retard",
      "Génération de pipeline faible (1 deals/30j)",
      "Taux de signature faible (10%) — conversion à améliorer",
      "Historique d'atteinte fragile — moyenne 45%",
      "Projection en deçà des 70% — intervention nécessaire",
      "Confiance rep faible (3/10) — signal d'alerte",
    ],
    action_plan: [
      "Escalade manager immédiate — revue pipeline deal by deal",
      "Identifier les deals à impact rapide — closing sprint 30j",
      "Support commercial renforcé — coach deal, exec selling",
      "Revoir les objectifs de fin de période avec le management",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const outcome = searchParams.get("outcome");
  const action = searchParams.get("action");
  const confidence = searchParams.get("confidence");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/quota-attainment`);
      if (outcome) url.searchParams.set("outcome", outcome);
      if (action) url.searchParams.set("action", action);
      if (confidence) url.searchParams.set("confidence", confidence);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (outcome) reps = reps.filter((r) => r.attainment_outcome === outcome);
  if (action) reps = reps.filter((r) => r.quota_action === action);
  if (confidence) reps = reps.filter((r) => r.confidence === confidence);

  const outcome_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const confidence_counts: Record<string, number> = {};
  let total_projected = 0;
  let total_gap = 0;

  for (const r of mockReps) {
    outcome_counts[r.attainment_outcome] = (outcome_counts[r.attainment_outcome] || 0) + 1;
    action_counts[r.quota_action] = (action_counts[r.quota_action] || 0) + 1;
    confidence_counts[r.confidence] = (confidence_counts[r.confidence] || 0) + 1;
    total_projected += r.projected_closed_eur;
    total_gap += r.gap_to_quota_eur;
  }

  const n = mockReps.length;
  const avg_projected = mockReps.reduce((s, r) => s + r.projected_attainment_pct, 0) / n;

  return NextResponse.json({
    reps,
    summary: {
      total: n,
      outcome_counts,
      action_counts,
      confidence_counts,
      avg_projected_attainment_pct: Math.round(avg_projected * 10) / 10,
      total_projected_closed_eur: total_projected,
      total_gap_eur: total_gap,
      critical_miss_count: mockReps.filter((r) => r.attainment_outcome === "critical_miss").length,
      escalation_count: mockReps.filter((r) => r.quota_action === "escalate").length,
      overachieve_count: mockReps.filter((r) => r.attainment_outcome === "overachieve").length,
    },
  });
}
