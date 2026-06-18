import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "sv_001",
    rep_name: "Chloé Deschamps",
    region: "France",
    segment: "enterprise",
    velocity_eur_per_day: 4166.67,
    velocity_tier: "elite",
    velocity_action: "celebrate",
    primary_driver: "balanced",
    velocity_score: 91.2,
    opportunity_index: 1.6,
    win_rate_index: 1.5,
    deal_size_index: 1.4,
    cycle_time_index: 1.3,
    quota_attainment_pct: 125.0,
    projected_arr_eur: 1520833,
    velocity_gaps: [],
    velocity_levers: [
      "Documenter le playbook — partager les best practices avec l'équipe",
      "Mentorer les reps en dessous de la moyenne — partage de compétences",
      "Chercher à battre les benchmarks sur le levier le plus faible",
    ],
    benchmark_velocity_eur_per_day: 2777.78,
  },
  {
    rep_id: "sv_002",
    rep_name: "Antoine Girard",
    region: "Benelux",
    segment: "enterprise",
    velocity_eur_per_day: 3333.33,
    velocity_tier: "elite",
    velocity_action: "celebrate",
    primary_driver: "win_rate",
    velocity_score: 86.4,
    opportunity_index: 1.3,
    win_rate_index: 1.7,
    deal_size_index: 1.2,
    cycle_time_index: 1.1,
    quota_attainment_pct: 100.0,
    projected_arr_eur: 1216667,
    velocity_gaps: [],
    velocity_levers: [
      "Documenter le playbook — partager les best practices avec l'équipe",
      "Mentorer les reps en dessous de la moyenne — partage de compétences",
      "Chercher à battre les benchmarks sur le levier le plus faible",
    ],
    benchmark_velocity_eur_per_day: 2777.78,
  },
  {
    rep_id: "sv_003",
    rep_name: "Laure Favre",
    region: "DACH",
    segment: "mid_market",
    velocity_eur_per_day: 2500.0,
    velocity_tier: "high",
    velocity_action: "accelerate",
    primary_driver: "deal_size",
    velocity_score: 72.1,
    opportunity_index: 1.1,
    win_rate_index: 1.0,
    deal_size_index: 0.85,
    cycle_time_index: 1.2,
    quota_attainment_pct: 92.5,
    projected_arr_eur: 912500,
    velocity_gaps: [],
    velocity_levers: [
      "Capitaliser sur le momentum — augmenter le volume d'activité de 20%",
      "Chercher des opportunités de multi-threading — élargir les contacts clés",
      "Accélérer les deals closing stage — revue pipeline hebdomadaire",
    ],
    benchmark_velocity_eur_per_day: 2777.78,
  },
  {
    rep_id: "sv_004",
    rep_name: "Mathieu Renard",
    region: "Nordics",
    segment: "mid_market",
    velocity_eur_per_day: 2083.33,
    velocity_tier: "high",
    velocity_action: "accelerate",
    primary_driver: "cycle_time",
    velocity_score: 66.8,
    opportunity_index: 1.2,
    win_rate_index: 0.95,
    deal_size_index: 1.0,
    cycle_time_index: 0.72,
    quota_attainment_pct: 78.1,
    projected_arr_eur: 760417,
    velocity_gaps: [
      "Cycle de vente trop long — 125j vs. benchmark 90j (CT index: 0.7x)",
    ],
    velocity_levers: [
      "Capitaliser sur le momentum — augmenter le volume d'activité de 20%",
      "Chercher des opportunités de multi-threading — élargir les contacts clés",
      "Accélérer les deals closing stage — revue pipeline hebdomadaire",
    ],
    benchmark_velocity_eur_per_day: 2777.78,
  },
  {
    rep_id: "sv_005",
    rep_name: "Estelle Vidal",
    region: "Southern Europe",
    segment: "mid_market",
    velocity_eur_per_day: 1388.89,
    velocity_tier: "average",
    velocity_action: "optimize",
    primary_driver: "opportunities",
    velocity_score: 52.3,
    opportunity_index: 0.75,
    win_rate_index: 0.9,
    deal_size_index: 1.1,
    cycle_time_index: 1.0,
    quota_attainment_pct: 52.0,
    projected_arr_eur: 506944,
    velocity_gaps: [
      "Volume d'opportunités faible — 6 vs. benchmark 8 (0.8x)",
    ],
    velocity_levers: [
      "Augmenter le volume d'opportunités — 3 nouveaux comptes par semaine",
      "Analyser les deals gagnés récents — répliquer les patterns de succès",
    ],
    benchmark_velocity_eur_per_day: 2777.78,
  },
  {
    rep_id: "sv_006",
    rep_name: "Bertrand Collet",
    region: "France",
    segment: "enterprise",
    velocity_eur_per_day: 1111.11,
    velocity_tier: "average",
    velocity_action: "optimize",
    primary_driver: "win_rate",
    velocity_score: 47.6,
    opportunity_index: 0.85,
    win_rate_index: 0.65,
    deal_size_index: 0.95,
    cycle_time_index: 1.1,
    quota_attainment_pct: 41.7,
    projected_arr_eur: 405556,
    velocity_gaps: [
      "Taux de signature sous benchmark — 13% vs. 20% (0.7x)",
    ],
    velocity_levers: [
      "Améliorer le taux de conversion — revoir le process de qualification",
      "Analyser les deals gagnés récents — répliquer les patterns de succès",
    ],
    benchmark_velocity_eur_per_day: 2777.78,
  },
  {
    rep_id: "sv_007",
    rep_name: "Pascaline Morel",
    region: "Iberia",
    segment: "mid_market",
    velocity_eur_per_day: 555.56,
    velocity_tier: "low",
    velocity_action: "rescue",
    primary_driver: "opportunities",
    velocity_score: 31.4,
    opportunity_index: 0.5,
    win_rate_index: 0.7,
    deal_size_index: 0.8,
    cycle_time_index: 0.6,
    quota_attainment_pct: 20.8,
    projected_arr_eur: 202778,
    velocity_gaps: [
      "Volume d'opportunités faible — 4 vs. benchmark 8 (0.5x)",
      "Taux de signature sous benchmark — 14% vs. 20% (0.7x)",
      "Cycle de vente trop long — 150j vs. benchmark 90j (CT index: 0.6x)",
      "Pipeline stagnant — seulement 28% des deals avancent par mois",
    ],
    velocity_levers: [
      "Intensifier la prospection — doubler le volume d'outreach cette semaine",
      "Hebdo velocity check avec le manager — suivi des 4 leviers",
    ],
    benchmark_velocity_eur_per_day: 2777.78,
  },
  {
    rep_id: "sv_008",
    rep_name: "Théodore Lamy",
    region: "DACH",
    segment: "enterprise",
    velocity_eur_per_day: 138.89,
    velocity_tier: "stalled",
    velocity_action: "reset",
    primary_driver: "cycle_time",
    velocity_score: 12.8,
    opportunity_index: 0.375,
    win_rate_index: 0.4,
    deal_size_index: 0.5,
    cycle_time_index: 0.33,
    quota_attainment_pct: 5.2,
    projected_arr_eur: 50694,
    velocity_gaps: [
      "Volume d'opportunités faible — 3 vs. benchmark 8 (0.4x)",
      "Taux de signature sous benchmark — 8% vs. 20% (0.4x)",
      "Taille moyenne des deals faible — 25,000€ vs. 50,000€ (0.5x)",
      "Cycle de vente trop long — 270j vs. benchmark 90j (CT index: 0.3x)",
      "Pipeline stagnant — seulement 15% des deals avancent par mois",
      "Taux de connexion outreach faible — 12% de réponse",
    ],
    velocity_levers: [
      "Audit complet du pipeline — identifier et éliminer les deals fantômes",
      "Reboot outbound — nouvelles séquences, nouvelles cibles ICP",
      "Session de coaching intensif — refonte du pitch et des objections",
      "Définir un plan 30j avec des jalons clairs et mesurables",
    ],
    benchmark_velocity_eur_per_day: 2777.78,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier = searchParams.get("tier");
  const action = searchParams.get("action");
  const driver = searchParams.get("driver");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-velocity`);
      if (tier) url.searchParams.set("tier", tier);
      if (action) url.searchParams.set("action", action);
      if (driver) url.searchParams.set("driver", driver);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (tier) reps = reps.filter((r) => r.velocity_tier === tier);
  if (action) reps = reps.filter((r) => r.velocity_action === action);
  if (driver) reps = reps.filter((r) => r.primary_driver === driver);

  const tier_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const driver_counts: Record<string, number> = {};
  let total_velocity = 0;
  let total_score = 0;
  let total_projected = 0;

  for (const r of mockReps) {
    tier_counts[r.velocity_tier] = (tier_counts[r.velocity_tier] || 0) + 1;
    action_counts[r.velocity_action] = (action_counts[r.velocity_action] || 0) + 1;
    driver_counts[r.primary_driver] = (driver_counts[r.primary_driver] || 0) + 1;
    total_velocity += r.velocity_eur_per_day;
    total_score += r.velocity_score;
    total_projected += r.projected_arr_eur;
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total: n,
      tier_counts,
      action_counts,
      driver_counts,
      avg_velocity_eur_per_day: Math.round((total_velocity / n) * 100) / 100,
      avg_velocity_score: Math.round((total_score / n) * 10) / 10,
      elite_count: mockReps.filter((r) => r.velocity_tier === "elite").length,
      stalled_count: mockReps.filter((r) => r.velocity_tier === "stalled").length,
      total_projected_arr_eur: total_projected,
    },
  });
}
