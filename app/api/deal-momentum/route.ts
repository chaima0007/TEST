import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "dm_001",
    rep_id: "rep_001",
    rep_name: "Sophie Martin",
    account_name: "Total Energies SE",
    momentum_score: 82.4,
    velocity_score: 78.0,
    engagement_score: 95.0,
    risk_score: 18.0,
    momentum_level: "accelerating",
    stall_reason: "no_stall",
    momentum_trend: "improving",
    momentum_action: "accelerate",
    momentum_indicators: [
      "3 avancement(s) de stade — progression active",
      "4 réunion(s) ce mois — engagement élevé",
      "Décideur engagé récemment — alignement validé",
      "Champion actif — support interne confirmé",
      "Proposition envoyée — étape commerciale franchie",
      "Tarification discutée — évaluation budgétaire active",
      "Budget confirmé — engagement financier sécurisé",
      "Prochaine étape définie dans 4j — plan d'action en place",
    ],
    risk_signals: [
      "Concurrent mentionné — risque concurrentiel identifié",
    ],
    recommended_actions: [
      "Accélérer vers la prochaine étape — créer un sentiment d'urgence",
      "Présenter une offre à durée limitée ou incentive de signature",
    ],
  },
  {
    deal_id: "dm_002",
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    account_name: "Capgemini France",
    momentum_score: 67.1,
    velocity_score: 65.0,
    engagement_score: 72.0,
    risk_score: 20.0,
    momentum_level: "positive",
    stall_reason: "no_stall",
    momentum_trend: "stable",
    momentum_action: "maintain",
    momentum_indicators: [
      "2 avancement(s) de stade — progression active",
      "Décideur engagé récemment — alignement validé",
      "Champion actif — support interne confirmé",
      "POC démarré — validation technique en cours",
      "Prochaine étape définie dans 7j — plan d'action en place",
    ],
    risk_signals: [
      "1 objection(s) non résolue(s) — blocage potentiel",
    ],
    recommended_actions: [
      "Maintenir le rythme d'engagement — ne pas perdre la dynamique",
      "Confirmer les prochaines étapes avec un calendrier précis",
    ],
  },
  {
    deal_id: "dm_003",
    rep_id: "rep_001",
    rep_name: "Sophie Martin",
    account_name: "Sodexo Group",
    momentum_score: 51.3,
    velocity_score: 48.0,
    engagement_score: 55.0,
    risk_score: 25.0,
    momentum_level: "neutral",
    stall_reason: "no_stall",
    momentum_trend: "stable",
    momentum_action: "maintain",
    momentum_indicators: [
      "Champion actif — support interne confirmé",
      "Tarification discutée — évaluation budgétaire active",
      "Prochaine étape définie dans 10j — plan d'action en place",
    ],
    risk_signals: [
      "1 objection(s) non résolue(s) — blocage potentiel",
      "Budget non confirmé à J-30 — risque de fermeture sans décision",
    ],
    recommended_actions: [
      "Maintenir le rythme d'engagement — ne pas perdre la dynamique",
      "Confirmer les prochaines étapes avec un calendrier précis",
    ],
  },
  {
    deal_id: "dm_004",
    rep_id: "rep_003",
    rep_name: "Marie Lefevre",
    account_name: "Veolia Environnement",
    momentum_score: 36.8,
    velocity_score: 30.0,
    engagement_score: 42.0,
    risk_score: 35.0,
    momentum_level: "stalling",
    stall_reason: "decision_delayed",
    momentum_trend: "deteriorating",
    momentum_action: "re_engage",
    momentum_indicators: [
      "Proposition envoyée — étape commerciale franchie",
    ],
    risk_signals: [
      "Deal en retard de 12j sur le plan prévu",
      "2 objection(s) non résolue(s) — blocage potentiel",
      "Budget non confirmé à J-30 — risque de fermeture sans décision",
    ],
    recommended_actions: [
      "Relancer avec un contenu à haute valeur ajoutée personnalisé",
      "Proposer une nouvelle date de réunion dans les 5 jours",
    ],
  },
  {
    deal_id: "dm_005",
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    account_name: "Boulanger SA",
    momentum_score: 22.5,
    velocity_score: 15.0,
    engagement_score: 28.0,
    risk_score: 55.0,
    momentum_level: "declining",
    stall_reason: "competitive_threat",
    momentum_trend: "critical",
    momentum_action: "competitive_defense",
    momentum_indicators: [],
    risk_signals: [
      "Démo concurrent demandée — évaluation comparative active",
      "2 objection(s) non résolue(s) — blocage potentiel",
      "Deal en retard de 22j sur le plan prévu",
      "Pas d'activité depuis 16j — deal en dérive",
    ],
    recommended_actions: [
      "Déployer la battlecard concurrente — différenciation ciblée",
      "Accélérer la démonstration de valeur unique avant décision",
    ],
  },
  {
    deal_id: "dm_006",
    rep_id: "rep_003",
    rep_name: "Marie Lefevre",
    account_name: "Picard Surgelés",
    momentum_score: 18.2,
    velocity_score: 12.0,
    engagement_score: 20.0,
    risk_score: 60.0,
    momentum_level: "declining",
    stall_reason: "internal_misalignment",
    momentum_trend: "deteriorating",
    momentum_action: "re_engage",
    momentum_indicators: [],
    risk_signals: [
      "2 régression(s) de stade — dynamique négative",
      "3 objection(s) non résolue(s) — blocage potentiel",
      "1 blocage(s) technique(s) — frein à la progression",
      "Pas d'activité depuis 18j — deal en dérive",
    ],
    recommended_actions: [
      "Relancer avec un contenu à haute valeur ajoutée personnalisé",
      "Proposer une nouvelle date de réunion dans les 5 jours",
    ],
  },
  {
    deal_id: "dm_007",
    rep_id: "rep_004",
    rep_name: "Thomas Bernard",
    account_name: "Allia Habitat",
    momentum_score: 8.4,
    velocity_score: 5.0,
    engagement_score: 8.0,
    risk_score: 85.0,
    momentum_level: "stalled",
    stall_reason: "champion_left",
    momentum_trend: "critical",
    momentum_action: "champion_recovery",
    momentum_indicators: [],
    risk_signals: [
      "Champion quitté l'entreprise — risque critique sur le deal",
      "Démo concurrent demandée — évaluation comparative active",
      "3 objection(s) non résolue(s) — blocage potentiel",
      "2 blocage(s) technique(s) — frein à la progression",
      "Deal en retard de 45j sur le plan prévu",
    ],
    recommended_actions: [
      "Identifier et qualifier un nouveau champion interne en urgence",
      "Solliciter une introduction via le sponsor exec ou réseau",
    ],
  },
  {
    deal_id: "dm_008",
    rep_id: "rep_004",
    rep_name: "Thomas Bernard",
    account_name: "Sofitel Luxury Hotels",
    momentum_score: 58.7,
    velocity_score: 55.0,
    engagement_score: 65.0,
    risk_score: 30.0,
    momentum_level: "positive",
    stall_reason: "no_stall",
    momentum_trend: "improving",
    momentum_action: "accelerate",
    momentum_indicators: [
      "Champion actif — support interne confirmé",
      "Sponsor exec impliqué — engagement stratégique",
      "Tarification discutée — évaluation budgétaire active",
      "Prochaine étape définie dans 6j — plan d'action en place",
    ],
    risk_signals: [
      "1 objection(s) non résolue(s) — blocage potentiel",
      "Budget non confirmé à J-30 — risque de fermeture sans décision",
    ],
    recommended_actions: [
      "Accélérer vers la prochaine étape — créer un sentiment d'urgence",
      "Présenter une offre à durée limitée ou incentive de signature",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const level  = searchParams.get("level");
  const action = searchParams.get("action");
  const trend  = searchParams.get("trend");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/deal-momentum`);
      if (level)  url.searchParams.set("level", level);
      if (action) url.searchParams.set("action", action);
      if (trend)  url.searchParams.set("trend", trend);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (level)  deals = deals.filter((d) => d.momentum_level === level);
  if (action) deals = deals.filter((d) => d.momentum_action === action);
  if (trend)  deals = deals.filter((d) => d.momentum_trend === trend);

  const level_counts:  Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const trend_counts:  Record<string, number> = {};
  let total_m = 0, total_v = 0, total_e = 0, total_r = 0;

  for (const d of mockDeals) {
    level_counts[d.momentum_level]   = (level_counts[d.momentum_level] || 0) + 1;
    action_counts[d.momentum_action] = (action_counts[d.momentum_action] || 0) + 1;
    trend_counts[d.momentum_trend]   = (trend_counts[d.momentum_trend] || 0) + 1;
    total_m += d.momentum_score;
    total_v += d.velocity_score;
    total_e += d.engagement_score;
    total_r += d.risk_score;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      level_counts,
      action_counts,
      trend_counts,
      avg_momentum_score:    Math.round((total_m / n) * 10) / 10,
      avg_velocity_score:    Math.round((total_v / n) * 10) / 10,
      avg_engagement_score:  Math.round((total_e / n) * 10) / 10,
      avg_risk_score:        Math.round((total_r / n) * 10) / 10,
      at_risk_count:         mockDeals.filter((d) =>
        d.momentum_level === "declining" || d.momentum_level === "stalled"
      ).length,
      stalled_count:         mockDeals.filter((d) => d.momentum_level === "stalled").length,
    },
  });
}
