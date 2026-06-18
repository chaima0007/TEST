import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rai_001",
    rep_name: "Léa Bertrand",
    region: "France",
    segment: "enterprise",
    activity_tier: "elite",
    activity_trend: "stable",
    coaching_focus: "on_track",
    activity_action: "celebrate",
    activity_score: 91.0,
    call_index: 1.45,
    email_index: 1.38,
    meeting_index: 1.5,
    proposal_index: 1.6,
    connect_rate_pct: 32.0,
    email_reply_rate_pct: 22.0,
    meeting_show_rate_pct: 88.0,
    deals_created_30d: 6,
    pipeline_generated_eur: 145000,
    coaching_insights: [
      "Performance exemplaire — score 91 : idéal pour le peer coaching",
      "Pipeline/réunion : 9,667€ — bon ROI réunion",
    ],
    action_items: [
      "Planifier une session de peer coaching avec les reps moins performants",
      "Documenter les meilleures pratiques pour la playbook équipe",
      "Identifier des opportunités d'expansion territoriale",
    ],
  },
  {
    rep_id: "rai_002",
    rep_name: "François Aubert",
    region: "Benelux",
    segment: "enterprise",
    activity_tier: "high",
    activity_trend: "accelerating",
    coaching_focus: "on_track",
    activity_action: "maintain",
    activity_score: 72.5,
    call_index: 1.1,
    email_index: 1.2,
    meeting_index: 1.1,
    proposal_index: 1.0,
    connect_rate_pct: 24.0,
    email_reply_rate_pct: 16.0,
    meeting_show_rate_pct: 82.0,
    deals_created_30d: 4,
    pipeline_generated_eur: 98000,
    coaching_insights: [
      "Activité conforme aux benchmarks — maintenir la cadence",
    ],
    action_items: [
      "Maintenir la cadence actuelle et préparer le pipeline du trimestre prochain",
    ],
  },
  {
    rep_id: "rai_003",
    rep_name: "Inès Charpentier",
    region: "DACH",
    segment: "mid_market",
    activity_tier: "average",
    activity_trend: "stable",
    coaching_focus: "meetings",
    activity_action: "nudge",
    activity_score: 55.0,
    call_index: 0.95,
    email_index: 0.88,
    meeting_index: 0.62,
    proposal_index: 0.9,
    connect_rate_pct: 18.0,
    email_reply_rate_pct: 12.0,
    meeting_show_rate_pct: 75.0,
    deals_created_30d: 3,
    pipeline_generated_eur: 52000,
    coaching_insights: [
      "Réunions bookées 9/15 — 62% du benchmark",
      "Pipeline/réunion : 5,778€ — améliorer la qualification avant réunion",
    ],
    action_items: [
      "Augmenter les demandes de démo après chaque appel de qualification",
      "Utiliser des outils de planification (Calendly) pour réduire la friction",
    ],
  },
  {
    rep_id: "rai_004",
    rep_name: "Pierre-Louis Gallet",
    region: "Nordics",
    segment: "mid_market",
    activity_tier: "average",
    activity_trend: "declining",
    coaching_focus: "calls",
    activity_action: "nudge",
    activity_score: 48.0,
    call_index: 0.72,
    email_index: 0.85,
    meeting_index: 0.78,
    proposal_index: 0.8,
    connect_rate_pct: 16.0,
    email_reply_rate_pct: 10.5,
    meeting_show_rate_pct: 70.0,
    deals_created_30d: 2,
    pipeline_generated_eur: 35000,
    coaching_insights: [
      "Volume d'appels 43/60 — seulement 72% du benchmark (déficit 17 appels)",
      "Tendance activité en baisse — risque de ralentissement pipeline sous 30j",
    ],
    action_items: [
      "Augmenter le volume d'appels de 17 — viser 60/mois",
      "Définir des créneaux fixes de cold calling (ex. 8h-10h, 17h-18h)",
    ],
  },
  {
    rep_id: "rai_005",
    rep_name: "Mathilde Escoffier",
    region: "Southern Europe",
    segment: "mid_market",
    activity_tier: "low",
    activity_trend: "declining",
    coaching_focus: "calls",
    activity_action: "coach",
    activity_score: 32.0,
    call_index: 0.45,
    email_index: 0.6,
    meeting_index: 0.5,
    proposal_index: 0.55,
    connect_rate_pct: 11.0,
    email_reply_rate_pct: 7.5,
    meeting_show_rate_pct: 62.0,
    deals_created_30d: 1,
    pipeline_generated_eur: 18000,
    coaching_insights: [
      "Volume d'appels 27/60 — seulement 45% du benchmark (déficit 33 appels)",
      "Volume email 60/100 — 60% du benchmark",
      "Réunions bookées 7/15 — 47% du benchmark",
      "Taux de connexion faible (11.0%) — améliorer les horaires et scripts d'appel",
      "Taux de réponse email faible (7.5%) — personnaliser l'accroche et l'objet",
      "Tendance activité en baisse — risque de ralentissement pipeline sous 30j",
    ],
    action_items: [
      "Augmenter le volume d'appels de 33 — viser 60/mois",
      "Définir des créneaux fixes de cold calling (ex. 8h-10h, 17h-18h)",
    ],
  },
  {
    rep_id: "rai_006",
    rep_name: "Romain Garnier",
    region: "France",
    segment: "enterprise",
    activity_tier: "low",
    activity_trend: "stalled",
    coaching_focus: "emails",
    activity_action: "coach",
    activity_score: 28.5,
    call_index: 0.55,
    email_index: 0.38,
    meeting_index: 0.6,
    proposal_index: 0.5,
    connect_rate_pct: 14.0,
    email_reply_rate_pct: 6.0,
    meeting_show_rate_pct: 68.0,
    deals_created_30d: 1,
    pipeline_generated_eur: 12000,
    coaching_insights: [
      "Volume email 38/100 — 38% du benchmark",
      "Volume d'appels 33/60 — seulement 55% du benchmark (déficit 27 appels)",
      "Taux de connexion faible (14.0%) — améliorer les horaires et scripts d'appel",
      "Taux de réponse email faible (6.0%) — personnaliser l'accroche et l'objet",
      "Activité quasi nulle sur les 7 derniers jours — signal d'alerte critique",
    ],
    action_items: [
      "Activer des séquences email automatisées pour les comptes dormants",
      "Viser +30% de volume email sur les 2 prochaines semaines",
    ],
  },
  {
    rep_id: "rai_007",
    rep_name: "Agathe Renault",
    region: "Iberia",
    segment: "mid_market",
    activity_tier: "inactive",
    activity_trend: "stalled",
    coaching_focus: "calls",
    activity_action: "intervene",
    activity_score: 12.0,
    call_index: 0.18,
    email_index: 0.22,
    meeting_index: 0.15,
    proposal_index: 0.1,
    connect_rate_pct: 8.0,
    email_reply_rate_pct: 3.5,
    meeting_show_rate_pct: 50.0,
    deals_created_30d: 0,
    pipeline_generated_eur: 0,
    coaching_insights: [
      "Volume d'appels 11/60 — seulement 18% du benchmark (déficit 49 appels)",
      "Volume email 22/100 — 22% du benchmark",
      "Réunions bookées 2/15 — 13% du benchmark",
      "Taux de connexion faible (8.0%) — améliorer les horaires et scripts d'appel",
      "Taux de réponse email faible (3.5%) — personnaliser l'accroche et l'objet",
      "Activité quasi nulle sur les 7 derniers jours — signal d'alerte critique",
    ],
    action_items: [
      "Session de revue individuelle avec le manager dans les 24h",
      "Identifier les blocages : motivation, compétences, territoire ?",
      "Plan de remédiation avec jalons hebdomadaires",
      "Réévaluation du quota si territoire ou segment problématique",
    ],
  },
  {
    rep_id: "rai_008",
    rep_name: "Noé Lombard",
    region: "DACH",
    segment: "enterprise",
    activity_tier: "inactive",
    activity_trend: "stalled",
    coaching_focus: "calls",
    activity_action: "intervene",
    activity_score: 8.5,
    call_index: 0.1,
    email_index: 0.15,
    meeting_index: 0.12,
    proposal_index: 0.08,
    connect_rate_pct: 5.0,
    email_reply_rate_pct: 2.0,
    meeting_show_rate_pct: 40.0,
    deals_created_30d: 0,
    pipeline_generated_eur: 0,
    coaching_insights: [
      "Volume d'appels 6/60 — seulement 10% du benchmark (déficit 54 appels)",
      "Volume email 15/100 — 15% du benchmark",
      "Réunions bookées 1/15 — 7% du benchmark",
      "Taux de connexion faible (5.0%) — améliorer les horaires et scripts d'appel",
      "Taux de réponse email faible (2.0%) — personnaliser l'accroche et l'objet",
      "Activité quasi nulle sur les 7 derniers jours — signal d'alerte critique",
    ],
    action_items: [
      "Session de revue individuelle avec le manager dans les 24h",
      "Identifier les blocages : motivation, compétences, territoire ?",
      "Plan de remédiation avec jalons hebdomadaires",
      "Réévaluation du quota si territoire ou segment problématique",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier   = searchParams.get("tier");
  const trend  = searchParams.get("trend");
  const action = searchParams.get("action");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/rep-activity-intelligence`);
      if (tier)   url.searchParams.set("tier", tier);
      if (trend)  url.searchParams.set("trend", trend);
      if (action) url.searchParams.set("action", action);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (tier)   reps = reps.filter((r) => r.activity_tier === tier);
  if (trend)  reps = reps.filter((r) => r.activity_trend === trend);
  if (action) reps = reps.filter((r) => r.activity_action === action);

  const tier_counts: Record<string, number>   = {};
  const trend_counts: Record<string, number>  = {};
  const action_counts: Record<string, number> = {};
  let total_pipeline = 0;

  for (const r of mockReps) {
    tier_counts[r.activity_tier]   = (tier_counts[r.activity_tier] || 0) + 1;
    trend_counts[r.activity_trend] = (trend_counts[r.activity_trend] || 0) + 1;
    action_counts[r.activity_action] = (action_counts[r.activity_action] || 0) + 1;
    total_pipeline += r.pipeline_generated_eur;
  }

  const n = mockReps.length;
  const avg_score = mockReps.reduce((s, r) => s + r.activity_score, 0) / n;

  return NextResponse.json({
    reps,
    summary: {
      total: n,
      tier_counts,
      trend_counts,
      action_counts,
      avg_activity_score: Math.round(avg_score * 10) / 10,
      total_pipeline_generated_eur: total_pipeline,
      elite_count: mockReps.filter((r) => r.activity_tier === "elite").length,
      inactive_count: mockReps.filter((r) => r.activity_tier === "inactive").length,
      intervention_count: mockReps.filter(
        (r) => r.activity_action === "intervene" || r.activity_action === "coach"
      ).length,
      declining_count: mockReps.filter(
        (r) => r.activity_trend === "declining" || r.activity_trend === "stalled"
      ).length,
    },
  });
}
