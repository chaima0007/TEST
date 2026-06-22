import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[forecast-commit] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "fc_001",
    rep_id: "rep_001",
    rep_name: "Sophie Martin",
    account_name: "Total Energies SE",
    commit_score: 95.0,
    sandbag_score: 8.0,
    risk_score: 0.0,
    calibrated_probability: 0.845,
    commit_category: "commit",
    forecast_confidence: "high",
    bias_type: "accurate",
    commit_action: "confirm",
    confidence_factors: [
      "Bon de commande reçu — engagement financier formel",
      "Budget confirmé — financement sécurisé",
      "Décideur identifié et engagé — alignement décisionnel",
      "Champion fort — support interne solide",
      "Alignement C-level — soutien stratégique acquis",
      "Concurrents éliminés — position de leader confirmée",
      "Toutes les objections résolues — voie libre pour la signature",
    ],
    risk_factors: [],
    recommended_actions: [
      "Valider le commit — deal solide, maintenir le rythme de clôture",
      "Planifier la revue contractuelle finale avec les parties",
    ],
  },
  {
    deal_id: "fc_002",
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    account_name: "Capgemini France",
    commit_score: 72.0,
    sandbag_score: 42.0,
    risk_score: 12.0,
    calibrated_probability: 0.712,
    commit_category: "commit",
    forecast_confidence: "medium",
    bias_type: "sandbagging_risk",
    commit_action: "pull_in",
    confidence_factors: [
      "Contrat envoyé — phase contractuelle engagée",
      "Accord verbal obtenu — intention d'achat confirmée",
      "Budget confirmé — financement sécurisé",
      "Champion fort — support interne solide",
    ],
    risk_factors: [
      "Concurrents toujours actifs — deal non sécurisé",
    ],
    recommended_actions: [
      "Challenger le rep — les signaux suggèrent une clôture plus rapide",
      "Proposer une incitation de fin de mois pour accélérer la signature",
    ],
  },
  {
    deal_id: "fc_003",
    rep_id: "rep_001",
    rep_name: "Sophie Martin",
    account_name: "Sodexo Group",
    commit_score: 52.0,
    sandbag_score: 5.0,
    risk_score: 24.0,
    calibrated_probability: 0.548,
    commit_category: "upside",
    forecast_confidence: "medium",
    bias_type: "accurate",
    commit_action: "monitor",
    confidence_factors: [
      "Accord verbal obtenu — intention d'achat confirmée",
      "Budget confirmé — financement sécurisé",
      "Champion fort — support interne solide",
      "Prochaine étape définie dans 8j",
    ],
    risk_factors: [
      "Décideur non confirmé à J-30 — risque de décision sans validation",
      "Objections non résolues — résistance acheteur persistante",
    ],
    recommended_actions: [
      "Surveiller l'évolution des signaux — deal en phase de maturation",
      "Fixer un point de revue dans 7 jours pour évaluer la progression",
    ],
  },
  {
    deal_id: "fc_004",
    rep_id: "rep_003",
    rep_name: "Marie Lefevre",
    account_name: "Veolia Environnement",
    commit_score: 38.0,
    sandbag_score: 15.0,
    risk_score: 47.0,
    calibrated_probability: 0.388,
    commit_category: "pipeline",
    forecast_confidence: "low",
    bias_type: "accurate",
    commit_action: "monitor",
    confidence_factors: [
      "Champion fort — support interne solide",
    ],
    risk_factors: [
      "Décideur non confirmé à J-30 — risque de décision sans validation",
      "Budget non confirmé à J-30 — risque de blocage financier",
      "Deal en retard dans le stade actuel — progression bloquée",
      "Objections non résolues — résistance acheteur persistante",
      "Concurrents toujours actifs — deal non sécurisé",
    ],
    recommended_actions: [
      "Surveiller l'évolution des signaux — deal en phase de maturation",
      "Fixer un point de revue dans 7 jours pour évaluer la progression",
    ],
  },
  {
    deal_id: "fc_005",
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    account_name: "Boulanger SA",
    commit_score: 62.0,
    sandbag_score: 5.0,
    risk_score: 38.0,
    calibrated_probability: 0.492,
    commit_category: "commit",
    forecast_confidence: "medium",
    bias_type: "accurate",
    commit_action: "challenge",
    confidence_factors: [
      "Équipe légale en review — validation finale en cours",
      "Budget confirmé — financement sécurisé",
      "Décideur identifié et engagé — alignement décisionnel",
    ],
    risk_factors: [
      "Pas de contrat envoyé à J-14 — risque de glissement de closing",
      "Objections non résolues — résistance acheteur persistante",
      "Concurrents toujours actifs — deal non sécurisé",
    ],
    recommended_actions: [
      "Valider les hypothèses du rep avec des preuves concrètes",
      "Demander un plan de clôture détaillé avec jalons et responsables",
    ],
  },
  {
    deal_id: "fc_006",
    rep_id: "rep_003",
    rep_name: "Marie Lefevre",
    account_name: "Picard Surgelés",
    commit_score: 18.0,
    sandbag_score: 5.0,
    risk_score: 72.0,
    calibrated_probability: 0.215,
    commit_category: "at_risk",
    forecast_confidence: "very_low",
    bias_type: "overforecasting_risk",
    commit_action: "escalate",
    confidence_factors: [],
    risk_factors: [
      "Décideur non confirmé à J-30 — risque de décision sans validation",
      "Budget non confirmé à J-30 — risque de blocage financier",
      "Pas de contrat envoyé à J-14 — risque de glissement de closing",
      "Probabilité rep supérieure à l'IA — risque de surconfiance commerciale",
      "Pas d'activité depuis 18j — deal en dérive",
      "Objections non résolues — résistance acheteur persistante",
      "Concurrents toujours actifs — deal non sécurisé",
    ],
    recommended_actions: [
      "Escalader au manager — deal à risque nécessitant une intervention",
      "Réunion d'urgence avec le rep pour plan de récupération",
    ],
  },
  {
    deal_id: "fc_007",
    rep_id: "rep_004",
    rep_name: "Thomas Bernard",
    account_name: "Allia Habitat",
    commit_score: 8.0,
    sandbag_score: 3.0,
    risk_score: 55.0,
    calibrated_probability: 0.148,
    commit_category: "omitted",
    forecast_confidence: "very_low",
    bias_type: "accurate",
    commit_action: "push_out",
    confidence_factors: [],
    risk_factors: [
      "Pas d'activité depuis 22j — deal en dérive",
      "Décideur non confirmé à J-30 — risque de décision sans validation",
      "Budget non confirmé à J-30 — risque de blocage financier",
      "Objections non résolues — résistance acheteur persistante",
    ],
    recommended_actions: [
      "Réaligner la date de clôture sur les signaux réels du deal",
      "Identifier les blocages spécifiques empêchant la signature",
    ],
  },
  {
    deal_id: "fc_008",
    rep_id: "rep_004",
    rep_name: "Thomas Bernard",
    account_name: "Sofitel Luxury Hotels",
    commit_score: 85.0,
    sandbag_score: 62.0,
    risk_score: 5.0,
    calibrated_probability: 0.778,
    commit_category: "upside",
    forecast_confidence: "medium",
    bias_type: "sandbagger",
    commit_action: "pull_in",
    confidence_factors: [
      "Contrat envoyé — phase contractuelle engagée",
      "Accord verbal obtenu — intention d'achat confirmée",
      "Budget confirmé — financement sécurisé",
      "Décideur identifié et engagé — alignement décisionnel",
      "Champion fort — support interne solide",
      "Alignement C-level — soutien stratégique acquis",
      "Concurrents éliminés — position de leader confirmée",
      "Toutes les objections résolues — voie libre pour la signature",
    ],
    risk_factors: [],
    recommended_actions: [
      "Challenger le rep — les signaux suggèrent une clôture plus rapide",
      "Proposer une incitation de fin de mois pour accélérer la signature",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const category   = searchParams.get("category");
  const confidence = searchParams.get("confidence");
  const action     = searchParams.get("action");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/forecast-commit`);
      if (category)   url.searchParams.set("category", category);
      if (confidence) url.searchParams.set("confidence", confidence);
      if (action)     url.searchParams.set("action", action);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let deals = [...mockDeals];
  if (category)   deals = deals.filter((d) => d.commit_category === category);
  if (confidence) deals = deals.filter((d) => d.forecast_confidence === confidence);
  if (action)     deals = deals.filter((d) => d.commit_action === action);

  const cat_counts:  Record<string, number> = {};
  const conf_counts: Record<string, number> = {};
  const bias_counts: Record<string, number> = {};
  const act_counts:  Record<string, number> = {};
  let total_commit = 0, total_sandbag = 0, total_risk = 0, total_prob = 0;

  for (const d of mockDeals) {
    cat_counts[d.commit_category]     = (cat_counts[d.commit_category] || 0) + 1;
    conf_counts[d.forecast_confidence] = (conf_counts[d.forecast_confidence] || 0) + 1;
    bias_counts[d.bias_type]          = (bias_counts[d.bias_type] || 0) + 1;
    act_counts[d.commit_action]       = (act_counts[d.commit_action] || 0) + 1;
    total_commit  += d.commit_score;
    total_sandbag += d.sandbag_score;
    total_risk    += d.risk_score;
    total_prob    += d.calibrated_probability;
  }

  const n = mockDeals.length;

  return sealResponse(NextResponse.json({
    deals,
    summary: {
      total: n,
      cat_counts,
      conf_counts,
      bias_counts,
      act_counts,
      avg_commit_score:          Math.round((total_commit / n) * 10) / 10,
      avg_sandbag_score:         Math.round((total_sandbag / n) * 10) / 10,
      avg_risk_score:            Math.round((total_risk / n) * 10) / 10,
      avg_calibrated_probability: Math.round((total_prob / n) * 1000) / 1000,
      solid_commit_count:  mockDeals.filter((d) => d.commit_category === "commit").length,
      at_risk_count:       mockDeals.filter((d) => d.commit_category === "at_risk").length,
      escalation_count:    mockDeals.filter((d) => d.commit_action === "escalate").length,
      sandbag_count:       mockDeals.filter((d) =>
        d.bias_type === "sandbagger" || d.bias_type === "sandbagging_risk"
      ).length,
    },
  }));
}
