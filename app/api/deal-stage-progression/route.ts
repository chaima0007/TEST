import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "dsp_001",
    deal_name: "Contrat Plateforme Enterprise — Axa Group",
    rep_id: "rep_001",
    rep_name: "Léa Bertrand",
    account_name: "Axa Group",
    current_stage: "closing",
    previous_stage: "negotiation",
    deal_size_eur: 280000,
    progression_risk: "on_track",
    progression_action: "close_now",
    close_quarter_probability: "high",
    progression_score: 91.5,
    stage_velocity_ratio: 0.85,
    days_over_benchmark: 0,
    estimated_stages_remaining: 0,
    estimated_days_to_close: 4,
    stall_reasons: [],
    next_actions: [
      "Envoyer la proposition finale dans les 24h",
      "Organiser un appel de closing avec le décideur",
      "Aligner sur la date de signature",
    ],
    close_quarter_drivers: [
      "Sponsor exécutif engagé — signal fort de closing",
      "Budget confirmé — décision financière validée",
      "Timeline confirmée — urgence côté client identifiée",
      "Décideur identifié — accès direct au pouvoir de signature",
      "Proposition envoyée — 2 version(s)",
      "5 réunions tenues — relation avancée",
      "Fin de période dans 18j — pression calendaire",
    ],
  },
  {
    deal_id: "dsp_002",
    deal_name: "Expansion Licences SaaS — BNP Paribas",
    rep_id: "rep_002",
    rep_name: "François Aubert",
    account_name: "BNP Paribas",
    current_stage: "negotiation",
    previous_stage: "proposal",
    deal_size_eur: 195000,
    progression_risk: "on_track",
    progression_action: "close_now",
    close_quarter_probability: "high",
    progression_score: 84.2,
    stage_velocity_ratio: 0.9,
    days_over_benchmark: 0,
    estimated_stages_remaining: 1,
    estimated_days_to_close: 11,
    stall_reasons: [],
    next_actions: [
      "Lever les dernières objections contractuelles",
      "Aligner sur la date de signature",
    ],
    close_quarter_drivers: [
      "Budget confirmé — décision financière validée",
      "Décideur identifié — accès direct au pouvoir de signature",
      "4 réunions tenues — relation avancée",
    ],
  },
  {
    deal_id: "dsp_003",
    deal_name: "Migration Cloud — Société Générale",
    rep_id: "rep_003",
    rep_name: "Inès Charpentier",
    account_name: "Société Générale",
    current_stage: "proposal",
    previous_stage: "demo",
    deal_size_eur: 145000,
    progression_risk: "slowing",
    progression_action: "accelerate",
    close_quarter_probability: "medium",
    progression_score: 62.0,
    stage_velocity_ratio: 1.6,
    days_over_benchmark: 8,
    estimated_stages_remaining: 2,
    estimated_days_to_close: 24,
    stall_reasons: [
      "Ralentissement : ratio 1.6× du benchmark — cadence à relever",
    ],
    next_actions: [
      "Relancer le contact dans les 48h — prochaine étape : negotiation",
      "Envoyer un contenu de valeur adapté au stade actuel",
      "Planifier la prochaine réunion avant la fin de semaine",
    ],
    close_quarter_drivers: [
      "Budget confirmé — décision financière validée",
      "3 réunions tenues — relation avancée",
    ],
  },
  {
    deal_id: "dsp_004",
    deal_name: "Intégration API — Carrefour Digital",
    rep_id: "rep_004",
    rep_name: "Pierre-Louis Gallet",
    account_name: "Carrefour Digital",
    current_stage: "demo",
    previous_stage: "qualification",
    deal_size_eur: 78000,
    progression_risk: "slowing",
    progression_action: "accelerate",
    close_quarter_probability: "medium",
    progression_score: 54.5,
    stage_velocity_ratio: 1.55,
    days_over_benchmark: 7,
    estimated_stages_remaining: 3,
    estimated_days_to_close: 38,
    stall_reasons: [
      "Décideur non identifié — champion à sécuriser",
    ],
    next_actions: [
      "Relancer le contact dans les 48h — prochaine étape : proposal",
      "Planifier la prochaine réunion avant la fin de semaine",
    ],
    close_quarter_drivers: [
      "Budget confirmé — décision financière validée",
      "2 réunions tenues — relation avancée",
    ],
  },
  {
    deal_id: "dsp_005",
    deal_name: "Plateforme Analytics — Michelin Group",
    rep_id: "rep_001",
    rep_name: "Léa Bertrand",
    account_name: "Michelin Group",
    current_stage: "qualification",
    previous_stage: "prospecting",
    deal_size_eur: 95000,
    progression_risk: "on_track",
    progression_action: "maintain",
    close_quarter_probability: "low",
    progression_score: 68.0,
    stage_velocity_ratio: 0.9,
    days_over_benchmark: 0,
    estimated_stages_remaining: 4,
    estimated_days_to_close: 47,
    stall_reasons: [],
    next_actions: [
      "Maintenir la cadence d'activité actuelle",
      "Préparer les éléments pour l'étape suivante",
    ],
    close_quarter_drivers: [
      "Budget confirmé — décision financière validée",
      "Timeline confirmée — urgence côté client identifiée",
    ],
  },
  {
    deal_id: "dsp_006",
    deal_name: "Renouvellement Annuel — Orange Business",
    rep_id: "rep_005",
    rep_name: "Mathilde Escoffier",
    account_name: "Orange Business",
    current_stage: "proposal",
    previous_stage: "demo",
    deal_size_eur: 120000,
    progression_risk: "stuck",
    progression_action: "rescue",
    close_quarter_probability: "low",
    progression_score: 38.0,
    stage_velocity_ratio: 2.5,
    days_over_benchmark: 21,
    estimated_stages_remaining: 2,
    estimated_days_to_close: 28,
    stall_reasons: [
      "Bloqué depuis 35j (benchmark 14j) — ratio 2.5×",
      "Aucune activité depuis 9 jours",
      "Budget non confirmé — risque de décrochage",
      "Sponsor exécutif absent — exposition au risque",
    ],
    next_actions: [
      "Session de revue manager — analyse deal by deal",
      "Re-qualifier le champion et vérifier le budget",
      "Proposer une démo personnalisée ou POC pour relancer",
    ],
    close_quarter_drivers: [
      "Décideur identifié — accès direct au pouvoir de signature",
      "Peu de signaux positifs — investissement requis pour débloquer",
    ],
  },
  {
    deal_id: "dsp_007",
    deal_name: "Pilote Automatisation — Renault Trucks",
    rep_id: "rep_006",
    rep_name: "Romain Garnier",
    account_name: "Renault Trucks",
    current_stage: "qualification",
    previous_stage: "demo",
    deal_size_eur: 55000,
    progression_risk: "regressed",
    progression_action: "rescue",
    close_quarter_probability: "low",
    progression_score: 41.0,
    stage_velocity_ratio: 1.2,
    days_over_benchmark: 2,
    estimated_stages_remaining: 4,
    estimated_days_to_close: 52,
    stall_reasons: [
      "Régression de demo → qualification",
      "Décideur non identifié — champion à sécuriser",
    ],
    next_actions: [
      "Session de revue manager — analyse deal by deal",
      "Re-qualifier le champion et vérifier le budget",
      "Demander un exec sponsor côté client",
    ],
    close_quarter_drivers: [
      "Peu de signaux positifs — investissement requis pour débloquer",
    ],
  },
  {
    deal_id: "dsp_008",
    deal_name: "Déploiement Global — Airbus SE",
    rep_id: "rep_007",
    rep_name: "Agathe Renault",
    account_name: "Airbus SE",
    current_stage: "prospecting",
    previous_stage: null,
    deal_size_eur: 420000,
    progression_risk: "stuck",
    progression_action: "reprioritise",
    close_quarter_probability: "very_low",
    progression_score: 18.5,
    stage_velocity_ratio: 3.2,
    days_over_benchmark: 15,
    estimated_stages_remaining: 5,
    estimated_days_to_close: 64,
    stall_reasons: [
      "Bloqué depuis 22j (benchmark 7j) — ratio 3.2×",
      "Aucune activité depuis 12 jours",
      "Budget non confirmé — risque de décrochage",
      "Décideur non identifié — champion à sécuriser",
    ],
    next_actions: [
      "Évaluer si le deal est encore viable",
      "Passer en mode nurture ou fermer le deal",
      "Réallouer le temps commercial sur des deals plus matures",
    ],
    close_quarter_drivers: [
      "Peu de signaux positifs — investissement requis pour débloquer",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk    = searchParams.get("risk");
  const action  = searchParams.get("action");
  const prob    = searchParams.get("probability");
  const stage   = searchParams.get("stage");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/deal-stage-progression`);
      if (risk)   url.searchParams.set("risk", risk);
      if (action) url.searchParams.set("action", action);
      if (prob)   url.searchParams.set("probability", prob);
      if (stage)  url.searchParams.set("stage", stage);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (risk)   deals = deals.filter((d) => d.progression_risk === risk);
  if (action) deals = deals.filter((d) => d.progression_action === action);
  if (prob)   deals = deals.filter((d) => d.close_quarter_probability === prob);
  if (stage)  deals = deals.filter((d) => d.current_stage === stage);

  const risk_counts: Record<string, number>   = {};
  const action_counts: Record<string, number> = {};
  const prob_counts: Record<string, number>   = {};
  let total_pipeline = 0;
  let high_prob_pipeline = 0;
  let stuck_pipeline = 0;

  for (const d of mockDeals) {
    risk_counts[d.progression_risk]          = (risk_counts[d.progression_risk] || 0) + 1;
    action_counts[d.progression_action]      = (action_counts[d.progression_action] || 0) + 1;
    prob_counts[d.close_quarter_probability] = (prob_counts[d.close_quarter_probability] || 0) + 1;
    total_pipeline += d.deal_size_eur;
    if (d.close_quarter_probability === "high") high_prob_pipeline += d.deal_size_eur;
    if (d.progression_risk === "stuck") stuck_pipeline += d.deal_size_eur;
  }

  const n = mockDeals.length;
  const avg_score = mockDeals.reduce((s, d) => s + d.progression_score, 0) / n;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      risk_counts,
      action_counts,
      probability_counts: prob_counts,
      avg_progression_score: Math.round(avg_score * 10) / 10,
      total_pipeline_eur: total_pipeline,
      high_prob_pipeline_eur: high_prob_pipeline,
      stuck_pipeline_eur: stuck_pipeline,
      stuck_count: mockDeals.filter((d) => d.progression_risk === "stuck").length,
      rescue_count: mockDeals.filter(
        (d) => d.progression_action === "rescue" || d.progression_action === "reprioritise"
      ).length,
    },
  });
}
