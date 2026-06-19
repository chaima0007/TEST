import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "fa_001",
    rep_name: "Sophie Moreau",
    region: "EMEA Nord",
    segment: "enterprise",
    accuracy_pct: 94.2,
    accuracy_tier: "excellent",
    bias: "neutral",
    forecast_action: "celebrate",
    rep_tier: "top",
    attainment_pct: 118.0,
    variance_eur: 22000,
    accuracy_drivers: [
      "Précision forecast excellente (94%) — prévisions très fiables",
      "Quota atteint à 118% — performance commerciale solide",
      "Hygiène CRM irréprochable — données à jour (lag 1j)",
      "Couverture pipeline élevée (4.2x) — visibilité long terme",
      "Comportement forecast propre — aucun sandbagging ni pull-in détecté",
      "Deals peu glissants (3j avg) — prévisions temporellement fiables",
      "Évaluée sur 6 trimestres — historique solide",
    ],
    accuracy_gaps: [],
    coaching_recommendations: [
      "Partager les bonnes pratiques de forecast avec l'équipe",
      "Documenter la méthode de qualification pour en faire un standard",
    ],
    reliability_score: 91.5,
  },
  {
    rep_id: "fa_002",
    rep_name: "Thomas Guillot",
    region: "EMEA Sud",
    segment: "enterprise",
    accuracy_pct: 88.5,
    accuracy_tier: "good",
    bias: "pessimistic",
    forecast_action: "calibrate",
    rep_tier: "top",
    attainment_pct: 112.0,
    variance_eur: 35000,
    accuracy_drivers: [
      "Quota atteint à 112% — performance commerciale solide",
      "Couverture pipeline élevée (3.8x) — visibilité long terme",
      "Évaluée sur 5 trimestres — historique solide",
    ],
    accuracy_gaps: [
      "Biais pessimiste — forecast régulièrement < réalisé (sandbagging)",
    ],
    coaching_recommendations: [
      "Corriger le sandbagging — aligner le forecast sur la réalité du pipeline",
      "Session 1:1 de calibration — analyser les deals sous-déclarés",
    ],
    reliability_score: 79.8,
  },
  {
    rep_id: "fa_003",
    rep_name: "Camille Leroux",
    region: "DACH",
    segment: "mid_market",
    accuracy_pct: 81.0,
    accuracy_tier: "good",
    bias: "neutral",
    forecast_action: "calibrate",
    rep_tier: "solid",
    attainment_pct: 94.0,
    variance_eur: -12000,
    accuracy_drivers: [
      "Précision forecast excellente (81%) — prévisions très fiables",
      "Hygiène CRM irréprochable — données à jour (lag 2j)",
    ],
    accuracy_gaps: [],
    coaching_recommendations: [
      "Identifier les catégories de deals les plus difficiles à prévoir",
      "Renforcer la qualification MEDDIC pour améliorer la précision",
    ],
    reliability_score: 72.4,
  },
  {
    rep_id: "fa_004",
    rep_name: "Antoine Bernard",
    region: "Benelux",
    segment: "mid_market",
    accuracy_pct: 76.8,
    accuracy_tier: "good",
    bias: "optimistic",
    forecast_action: "calibrate",
    rep_tier: "solid",
    attainment_pct: 88.0,
    variance_eur: -28000,
    accuracy_drivers: [
      "Couverture pipeline élevée (3.1x) — visibilité long terme",
    ],
    accuracy_gaps: [
      "Biais optimiste — forecast régulièrement > réalisé (sur-déclaration)",
    ],
    coaching_recommendations: [
      "Revoir les critères de commit — n'engager que les deals validés MEDDIC",
      "Instaurer un review hebdomadaire avec le manager avant le commit",
    ],
    reliability_score: 65.2,
  },
  {
    rep_id: "fa_005",
    rep_name: "Julie Fontaine",
    region: "France",
    segment: "mid_market",
    accuracy_pct: 62.0,
    accuracy_tier: "fair",
    bias: "optimistic",
    forecast_action: "improve",
    rep_tier: "developing",
    attainment_pct: 71.0,
    variance_eur: -48000,
    accuracy_drivers: [],
    accuracy_gaps: [
      "Précision insuffisante (62%) — écart forecast/réel trop important",
      "Biais optimiste — forecast régulièrement > réalisé (sur-déclaration)",
      "Pipeline sous-alimenté (2.1x) — visibilité réduite",
      "4 pull-ins last minute — distortion des prévisions",
      "Attainment à 71% — performance commerciale à améliorer",
    ],
    coaching_recommendations: [
      "Revoir les critères de commit — n'engager que les deals validés MEDDIC",
      "Instaurer un review hebdomadaire avec le manager avant le commit",
      "Intensifier la génération de pipeline — viser un coverage ≥ 3x quota",
      "Éliminer les pull-ins late stage — qualifier le close date dès le début",
      "Plan d'amélioration 90j — objectifs hebdomadaires et coaching intensif",
    ],
    reliability_score: 44.8,
  },
  {
    rep_id: "fa_006",
    rep_name: "Maxime Chevalier",
    region: "Iberia",
    segment: "smb",
    accuracy_pct: 58.5,
    accuracy_tier: "fair",
    bias: "neutral",
    forecast_action: "improve",
    rep_tier: "developing",
    attainment_pct: 65.0,
    variance_eur: 8000,
    accuracy_drivers: [],
    accuracy_gaps: [
      "Précision insuffisante (59%) — écart forecast/réel trop important",
      "Hygiène CRM insuffisante — lag moyen de 9j",
      "Deals glissants en moyenne 18j — prévisions de date non fiables",
      "Attainment à 65% — performance commerciale à améliorer",
    ],
    coaching_recommendations: [
      "Améliorer la cadence CRM — viser un lag < 24h (actuel: 9j)",
      "Améliorer la qualification des close dates — utiliser les jalons MEDDIC",
      "Plan d'amélioration 90j — objectifs hebdomadaires et coaching intensif",
    ],
    reliability_score: 36.5,
  },
  {
    rep_id: "fa_007",
    rep_name: "Léa Rousseau",
    region: "UK&I",
    segment: "smb",
    accuracy_pct: 38.0,
    accuracy_tier: "poor",
    bias: "optimistic",
    forecast_action: "overhaul",
    rep_tier: "struggling",
    attainment_pct: 42.0,
    variance_eur: -95000,
    accuracy_drivers: [],
    accuracy_gaps: [
      "Précision insuffisante (38%) — écart forecast/réel trop important",
      "Biais optimiste — forecast régulièrement > réalisé (sur-déclaration)",
      "Hygiène CRM insuffisante — lag moyen de 12j",
      "Pipeline sous-alimenté (1.8x) — visibilité réduite",
      "5 pull-ins last minute — distortion des prévisions",
      "3 événements sandbagging — manque de transparence",
      "Deals glissants en moyenne 22j — prévisions de date non fiables",
      "Attainment à 42% — performance commerciale à améliorer",
    ],
    coaching_recommendations: [
      "Revoir les critères de commit — n'engager que les deals validés MEDDIC",
      "Instaurer un review hebdomadaire avec le manager avant le commit",
      "Améliorer la cadence CRM — viser un lag < 24h (actuel: 12j)",
      "Intensifier la génération de pipeline — viser un coverage ≥ 3x quota",
      "Éliminer les pull-ins late stage — qualifier le close date dès le début",
      "Améliorer la qualification des close dates — utiliser les jalons MEDDIC",
      "Plan d'amélioration 90j — objectifs hebdomadaires et coaching intensif",
      "Révision complète du processus de forecast — atelier avec l'équipe RevOps",
    ],
    reliability_score: 18.2,
  },
  {
    rep_id: "fa_008",
    rep_name: "Nicolas Dupont",
    region: "Nordics",
    segment: "enterprise",
    accuracy_pct: 29.5,
    accuracy_tier: "poor",
    bias: "optimistic",
    forecast_action: "overhaul",
    rep_tier: "struggling",
    attainment_pct: 38.0,
    variance_eur: -135000,
    accuracy_drivers: [],
    accuracy_gaps: [
      "Précision insuffisante (30%) — écart forecast/réel trop important",
      "Biais optimiste — forecast régulièrement > réalisé (sur-déclaration)",
      "Hygiène CRM insuffisante — lag moyen de 15j",
      "Pipeline sous-alimenté (1.5x) — visibilité réduite",
      "6 pull-ins last minute — distortion des prévisions",
      "Deals glissants en moyenne 28j — prévisions de date non fiables",
      "Attainment à 38% — performance commerciale à améliorer",
    ],
    coaching_recommendations: [
      "Revoir les critères de commit — n'engager que les deals validés MEDDIC",
      "Instaurer un review hebdomadaire avec le manager avant le commit",
      "Améliorer la cadence CRM — viser un lag < 24h (actuel: 15j)",
      "Intensifier la génération de pipeline — viser un coverage ≥ 3x quota",
      "Éliminer les pull-ins late stage — qualifier le close date dès le début",
      "Améliorer la qualification des close dates — utiliser les jalons MEDDIC",
      "Plan d'amélioration 90j — objectifs hebdomadaires et coaching intensif",
      "Révision complète du processus de forecast — atelier avec l'équipe RevOps",
    ],
    reliability_score: 11.5,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const accuracy = searchParams.get("accuracy");
  const action = searchParams.get("action");
  const bias = searchParams.get("bias");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/forecast-accuracy-engine`);
      if (accuracy) url.searchParams.set("accuracy", accuracy);
      if (action) url.searchParams.set("action", action);
      if (bias) url.searchParams.set("bias", bias);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (accuracy) reps = reps.filter((r) => r.accuracy_tier === accuracy);
  if (action) reps = reps.filter((r) => r.forecast_action === action);
  if (bias) reps = reps.filter((r) => r.bias === bias);

  const accuracy_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const bias_counts: Record<string, number> = {};
  let total_accuracy = 0;
  let total_attainment = 0;
  let total_variance = 0;

  for (const r of mockReps) {
    accuracy_counts[r.accuracy_tier] = (accuracy_counts[r.accuracy_tier] || 0) + 1;
    action_counts[r.forecast_action] = (action_counts[r.forecast_action] || 0) + 1;
    bias_counts[r.bias] = (bias_counts[r.bias] || 0) + 1;
    total_accuracy += r.accuracy_pct;
    total_attainment += r.attainment_pct;
    total_variance += r.variance_eur;
  }

  const n = mockReps.length;

  return NextResponse.json(sealResponse({
    reps,
    summary: {
      total: n,
      accuracy_counts,
      action_counts,
      bias_counts,
      avg_accuracy_pct: Math.round((total_accuracy / n) * 10) / 10,
      avg_attainment_pct: Math.round((total_attainment / n) * 10) / 10,
      excellent_count: mockReps.filter((r) => r.accuracy_tier === "excellent").length,
      overhaul_count: mockReps.filter((r) => r.forecast_action === "overhaul").length,
      total_variance_eur: total_variance,
    },
  } as Record<string,unknown>));
}
