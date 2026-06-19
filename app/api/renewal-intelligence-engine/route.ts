import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockRenewals = [
  {
    customer_id: "ri_001",
    customer_name: "CloudScale Technologies",
    arr_eur: 240000,
    segment: "enterprise",
    days_to_renewal: 12,
    renewal_risk: "critical",
    renewal_action: "escalate",
    predicted_outcome: "churn",
    engagement_trend: "dormant",
    renewal_probability_pct: 18.5,
    expected_arr_change_pct: -100.0,
    risk_signals: [
      "Score santé critique (28/100) — risque de non-renouvellement",
      "NPS négatif (-55) — insatisfaction client",
      "Usage produit dormant — signal de désengagement",
      "Concurrent mentionné — risque de displacement",
      "Remise demandée — signal de sensibilité prix",
      "Sponsor exécutif non aligné — renouvellement fragile",
      "Renouvellement dans 12j — urgence critique",
    ],
    positive_signals: [],
    renewal_plays: [
      "Escalade C-level — mobiliser direction et executive sponsor d'urgence",
      "EBR d'urgence — valeur démontrée, roadmap personnalisée, ROI calculé",
      "Préparer un battlecard concurrentiel — arguments de différenciation",
      "Proposer une extension contractuelle temporaire — éviter la rupture",
    ],
    urgency_score: 87.5,
  },
  {
    customer_id: "ri_002",
    customer_name: "DataVault Partners",
    arr_eur: 180000,
    segment: "enterprise",
    days_to_renewal: 45,
    renewal_risk: "high",
    renewal_action: "intervene",
    predicted_outcome: "downgrade",
    engagement_trend: "declining",
    renewal_probability_pct: 52.0,
    expected_arr_change_pct: -20.0,
    risk_signals: [
      "Score santé insuffisant (48/100) — risque de non-renouvellement",
      "NPS négatif (-12) — insatisfaction client",
      "Usage produit declining — signal de désengagement",
      "Remise demandée — signal de sensibilité prix",
      "Champion faible (3/10) — défenseur interne insuffisant",
    ],
    positive_signals: [
      "Sponsor exécutif aligné — renouvellement facilité",
      "3 ans client — relation établie et fidèle",
    ],
    renewal_plays: [
      "Réunion de renouvellement stratégique — CEO/VP Sales + champion client",
      "Présenter un rapport ROI personnalisé — quantifier la valeur délivrée",
      "Structurer une offre de renouvellement attractive — valeur vs. remise",
    ],
    urgency_score: 62.4,
  },
  {
    customer_id: "ri_003",
    customer_name: "NexaRetail Group",
    arr_eur: 144000,
    segment: "enterprise",
    days_to_renewal: 58,
    renewal_risk: "high",
    renewal_action: "intervene",
    predicted_outcome: "renew",
    engagement_trend: "stable",
    renewal_probability_pct: 58.0,
    expected_arr_change_pct: 0.0,
    risk_signals: [
      "Score santé insuffisant (52/100) — risque de non-renouvellement",
      "Concurrent mentionné — risque de displacement",
    ],
    positive_signals: [
      "Sponsor exécutif aligné — renouvellement facilité",
      "Champion fort (7/10) — défenseur interne actif",
      "2 ans client — relation établie et fidèle",
    ],
    renewal_plays: [
      "Réunion de renouvellement stratégique — CEO/VP Sales + champion client",
      "Présenter un rapport ROI personnalisé — quantifier la valeur délivrée",
    ],
    urgency_score: 55.8,
  },
  {
    customer_id: "ri_004",
    customer_name: "HealthBridge Systems",
    arr_eur: 96000,
    segment: "mid_market",
    days_to_renewal: 75,
    renewal_risk: "moderate",
    renewal_action: "nurture",
    predicted_outcome: "renew",
    engagement_trend: "stable",
    renewal_probability_pct: 68.0,
    expected_arr_change_pct: 0.0,
    risk_signals: [
      "NPS modéré (12) — engagement insuffisant",
      "Remise demandée — signal de sensibilité prix",
    ],
    positive_signals: [
      "Score santé correct (62/100)",
      "Sponsor exécutif aligné — renouvellement facilité",
      "Champion fort (7/10) — défenseur interne actif",
      "Renouvellement précédent ponctuel — historique favorable",
    ],
    renewal_plays: [
      "QBR de renouvellement — aligner sur les objectifs de la prochaine période",
      "Identifier et activer les cas d'usage non utilisés — maximiser la valeur",
    ],
    urgency_score: 38.5,
  },
  {
    customer_id: "ri_005",
    customer_name: "FinCore Solutions",
    arr_eur: 72000,
    segment: "mid_market",
    days_to_renewal: 82,
    renewal_risk: "moderate",
    renewal_action: "nurture",
    predicted_outcome: "expand",
    engagement_trend: "growing",
    renewal_probability_pct: 76.0,
    expected_arr_change_pct: 15.0,
    risk_signals: [],
    positive_signals: [
      "Score santé élevé (78/100) — compte en bonne forme",
      "NPS excellent (45) — client promoteur actif",
      "Usage produit en croissance — valeur perçue en hausse",
      "Discussion expansion en cours — signal d'upsell positif",
      "Sponsor exécutif aligné — renouvellement facilité",
      "Champion fort (8/10) — défenseur interne actif",
    ],
    renewal_plays: [
      "QBR de renouvellement — aligner sur les objectifs de la prochaine période",
      "Identifier et activer les cas d'usage non utilisés — maximiser la valeur",
      "Formaliser la discussion expansion — proposition commerciale à préparer",
    ],
    urgency_score: 27.0,
  },
  {
    customer_id: "ri_006",
    customer_name: "LogiFlux GmbH",
    arr_eur: 60000,
    segment: "mid_market",
    days_to_renewal: 105,
    renewal_risk: "low",
    renewal_action: "close",
    predicted_outcome: "expand",
    engagement_trend: "growing",
    renewal_probability_pct: 88.0,
    expected_arr_change_pct: 25.0,
    risk_signals: [],
    positive_signals: [
      "Score santé élevé (88/100) — compte en bonne forme",
      "NPS excellent (62) — client promoteur actif",
      "Usage produit en croissance — valeur perçue en hausse",
      "Discussion expansion en cours — signal d'upsell positif",
      "Sponsor exécutif aligné — renouvellement facilité",
      "Champion fort (9/10) — défenseur interne actif",
      "4 ans client — relation établie et fidèle",
      "Renouvellement précédent ponctuel — historique favorable",
    ],
    renewal_plays: [
      "Engager le processus de renouvellement — dossier commercial à préparer",
      "Valider les conditions contractuelles — anticiper les demandes",
      "Inclure un volet expansion dans la proposition — opportunité upsell",
    ],
    urgency_score: 14.0,
  },
  {
    customer_id: "ri_007",
    customer_name: "EduSpark Ltd",
    arr_eur: 24000,
    segment: "smb",
    days_to_renewal: 120,
    renewal_risk: "low",
    renewal_action: "close",
    predicted_outcome: "renew",
    engagement_trend: "stable",
    renewal_probability_pct: 84.0,
    expected_arr_change_pct: 0.0,
    risk_signals: [],
    positive_signals: [
      "Score santé élevé (82/100) — compte en bonne forme",
      "NPS excellent (38) — client promoteur actif",
      "Sponsor exécutif aligné — renouvellement facilité",
      "Champion fort (8/10) — défenseur interne actif",
      "2 ans client — relation établie et fidèle",
      "Renouvellement précédent ponctuel — historique favorable",
    ],
    renewal_plays: [
      "Engager le processus de renouvellement — dossier commercial à préparer",
      "Valider les conditions contractuelles — anticiper les demandes",
    ],
    urgency_score: 8.4,
  },
  {
    customer_id: "ri_008",
    customer_name: "PropLink AG",
    arr_eur: 12000,
    segment: "smb",
    days_to_renewal: 150,
    renewal_risk: "low",
    renewal_action: "close",
    predicted_outcome: "renew",
    engagement_trend: "growing",
    renewal_probability_pct: 91.0,
    expected_arr_change_pct: 0.0,
    risk_signals: [],
    positive_signals: [
      "Score santé élevé (91/100) — compte en bonne forme",
      "NPS excellent (71) — client promoteur actif",
      "Usage produit en croissance — valeur perçue en hausse",
      "Sponsor exécutif aligné — renouvellement facilité",
      "Champion fort (9/10) — défenseur interne actif",
      "Renouvellement précédent ponctuel — historique favorable",
    ],
    renewal_plays: [
      "Engager le processus de renouvellement — dossier commercial à préparer",
      "Valider les conditions contractuelles — anticiper les demandes",
    ],
    urgency_score: 4.5,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk = searchParams.get("risk");
  const action = searchParams.get("action");
  const outcome = searchParams.get("outcome");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/renewal-intelligence-engine`);
      if (risk) url.searchParams.set("risk", risk);
      if (action) url.searchParams.set("action", action);
      if (outcome) url.searchParams.set("outcome", outcome);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let renewals = [...mockRenewals];
  if (risk) renewals = renewals.filter((r) => r.renewal_risk === risk);
  if (action) renewals = renewals.filter((r) => r.renewal_action === action);
  if (outcome) renewals = renewals.filter((r) => r.predicted_outcome === outcome);

  const risk_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const outcome_counts: Record<string, number> = {};
  let total_prob = 0;
  let arr_at_risk = 0;
  let arr_delta = 0;

  for (const r of mockRenewals) {
    risk_counts[r.renewal_risk] = (risk_counts[r.renewal_risk] || 0) + 1;
    action_counts[r.renewal_action] = (action_counts[r.renewal_action] || 0) + 1;
    outcome_counts[r.predicted_outcome] = (outcome_counts[r.predicted_outcome] || 0) + 1;
    total_prob += r.renewal_probability_pct;
    if (r.renewal_risk === "high" || r.renewal_risk === "critical") arr_at_risk += r.arr_eur;
    arr_delta += r.arr_eur * r.expected_arr_change_pct / 100;
  }

  const n = mockRenewals.length;

  return NextResponse.json(sealResponse({
    renewals,
    summary: {
      total: n,
      risk_counts,
      action_counts,
      outcome_counts,
      avg_renewal_probability_pct: Math.round((total_prob / n) * 10) / 10,
      critical_count: mockRenewals.filter((r) => r.renewal_risk === "critical").length,
      escalation_count: mockRenewals.filter((r) => r.renewal_action === "escalate").length,
      total_arr_at_risk_eur: arr_at_risk,
      expected_arr_delta_eur: Math.round(arr_delta),
    },
  } as Record<string,unknown>));
}
