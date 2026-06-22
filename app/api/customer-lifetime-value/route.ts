import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[customer-lifetime-value] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "clv_001",
    account_name: "Total Energies SE",
    region: "France",
    segment: "enterprise",
    arr_eur: 320000,
    clv_3yr_eur: 987450,
    clv_tier: "platinum",
    expansion_potential: "high",
    churn_risk: "low",
    clv_action: "invest",
    health_score: 84.5,
    churn_probability_pct: 8.2,
    expansion_opportunity_eur: 96000,
    predicted_arr_yr2_eur: 361600,
    predicted_arr_yr3_eur: 305850,
    value_drivers: [
      "ARR élevé (320,000€) — compte stratégique",
      "3 renouvellements réussis — fidélité prouvée",
      "Croissance ARR moyenne 15% — expansion historique forte",
      "Utilisation licences 88% — engagement utilisateurs élevé",
      "4 modules adoptés — stickiness multi-produit",
      "NPS 62 — promoteur actif",
      "Sponsor exécutif engagé — relation stratégique sécurisée",
    ],
    risk_signals: [],
    recommended_plays: [
      "QBR stratégique avec le C-level — présentation roadmap",
      "Executive Sponsor Program — renforcer les liens exécutifs",
      "Session de découverte expansion — présenter les 2 modules non adoptés",
      "Proposer une montée en gamme de licences — 80%+ d'utilisation",
    ],
  },
  {
    account_id: "clv_002",
    account_name: "Capgemini France",
    region: "France",
    segment: "enterprise",
    arr_eur: 185000,
    clv_3yr_eur: 582300,
    clv_tier: "platinum",
    expansion_potential: "medium",
    churn_risk: "low",
    clv_action: "invest",
    health_score: 72.0,
    churn_probability_pct: 12.5,
    expansion_opportunity_eur: 55500,
    predicted_arr_yr2_eur: 205350,
    predicted_arr_yr3_eur: 191950,
    value_drivers: [
      "ARR élevé (185,000€) — compte stratégique",
      "2 renouvellements réussis — fidélité prouvée",
      "Croissance ARR moyenne 12% — expansion historique forte",
      "NPS 48 — promoteur actif",
      "Sponsor exécutif engagé — relation stratégique sécurisée",
    ],
    risk_signals: [],
    recommended_plays: [
      "QBR stratégique avec le C-level — présentation roadmap",
      "Session de découverte expansion — présenter les 2 modules non adoptés",
      "Planifier un QBR — dernière réunion stratégique trop ancienne",
    ],
  },
  {
    account_id: "clv_003",
    account_name: "Sodexo Group",
    region: "France",
    segment: "enterprise",
    arr_eur: 95000,
    clv_3yr_eur: 268500,
    clv_tier: "gold",
    expansion_potential: "high",
    churn_risk: "low",
    clv_action: "invest",
    health_score: 65.5,
    churn_probability_pct: 18.0,
    expansion_opportunity_eur: 47500,
    predicted_arr_yr2_eur: 104025,
    predicted_arr_yr3_eur: 69475,
    value_drivers: [
      "ARR élevé (95,000€) — compte stratégique",
      "1 renouvellement réussi — fidélité prouvée",
    ],
    risk_signals: [],
    recommended_plays: [
      "Session de découverte expansion — présenter les 3 modules non adoptés",
      "Construire le business case d'expansion basé sur l'utilisation actuelle",
    ],
  },
  {
    account_id: "clv_004",
    account_name: "Veolia Environnement",
    region: "France",
    segment: "mid_market",
    arr_eur: 72000,
    clv_3yr_eur: 198720,
    clv_tier: "gold",
    expansion_potential: "medium",
    churn_risk: "medium",
    clv_action: "invest",
    health_score: 52.0,
    churn_probability_pct: 28.5,
    expansion_opportunity_eur: 28800,
    predicted_arr_yr2_eur: 75600,
    predicted_arr_yr3_eur: 51120,
    value_drivers: [
      "ARR élevé (72,000€) — compte stratégique",
    ],
    risk_signals: [
      "NPS négatif (-5) — insatisfaction client",
      "4 tickets support en 90j — friction produit",
    ],
    recommended_plays: [
      "Session de découverte expansion — présenter les 2 modules non adoptés",
      "Construire le business case d'expansion basé sur l'utilisation actuelle",
    ],
  },
  {
    account_id: "clv_005",
    account_name: "Boulanger SA",
    region: "France",
    segment: "mid_market",
    arr_eur: 42000,
    clv_3yr_eur: 112560,
    clv_tier: "silver",
    expansion_potential: "high",
    churn_risk: "low",
    clv_action: "grow",
    health_score: 68.0,
    churn_probability_pct: 14.5,
    expansion_opportunity_eur: 25200,
    predicted_arr_yr2_eur: 47040,
    predicted_arr_yr3_eur: 23520,
    value_drivers: [
      "Utilisation licences 85% — engagement utilisateurs élevé",
      "NPS 52 — promoteur actif",
    ],
    risk_signals: [],
    recommended_plays: [
      "Session de découverte expansion — présenter les 2 modules non adoptés",
      "Proposer une montée en gamme de licences — 80%+ d'utilisation",
    ],
  },
  {
    account_id: "clv_006",
    account_name: "Picard Surgelés",
    region: "France",
    segment: "mid_market",
    arr_eur: 28000,
    clv_3yr_eur: 65240,
    clv_tier: "silver",
    expansion_potential: "low",
    churn_risk: "medium",
    clv_action: "grow",
    health_score: 44.5,
    churn_probability_pct: 33.0,
    expansion_opportunity_eur: 8400,
    predicted_arr_yr2_eur: 28560,
    predicted_arr_yr3_eur: 8680,
    value_drivers: [],
    risk_signals: [
      "NPS négatif (-12) — insatisfaction client",
      "3 tickets support en 90j — friction produit",
      "Dernier QBR il y a 8 mois — relation négligée",
    ],
    recommended_plays: [
      "Planifier un QBR — dernière réunion stratégique trop ancienne",
      "Maintenir le contact régulier — newsletter produit + invitations événements",
    ],
  },
  {
    account_id: "clv_007",
    account_name: "Allia Habitat",
    region: "DACH",
    segment: "mid_market",
    arr_eur: 18000,
    clv_3yr_eur: 29340,
    clv_tier: "bronze",
    expansion_potential: "low",
    churn_risk: "high",
    clv_action: "rescue",
    health_score: 32.0,
    churn_probability_pct: 48.5,
    expansion_opportunity_eur: 7200,
    predicted_arr_yr2_eur: 9540,
    predicted_arr_yr3_eur: 1800,
    value_drivers: [],
    risk_signals: [
      "Évaluation concurrente active — risque de départ imminent",
      "Champion clé parti — relation à reconstruire urgemment",
      "NPS négatif (-28) — insatisfaction client",
      "Dernier QBR il y a 9 mois — relation négligée",
    ],
    recommended_plays: [
      "Appel exécutif dans les 48h — escalade senior",
      "Identifier et neutraliser le concurrent en évaluation",
      "Proposer un plan de valeur personnalisé (ROI review)",
    ],
  },
  {
    account_id: "clv_008",
    account_name: "Sofitel Luxury Hotels",
    region: "Iberia",
    segment: "mid_market",
    arr_eur: 9500,
    clv_3yr_eur: 6650,
    clv_tier: "minimal",
    expansion_potential: "none",
    churn_risk: "critical",
    clv_action: "rescue",
    health_score: 18.5,
    churn_probability_pct: 72.0,
    expansion_opportunity_eur: 0,
    predicted_arr_yr2_eur: 2375,
    predicted_arr_yr3_eur: 0,
    value_drivers: [],
    risk_signals: [
      "Évaluation concurrente active — risque de départ imminent",
      "Champion clé parti — relation à reconstruire urgemment",
      "2 retards de paiement — tension financière côté client",
      "Score churn rep 8/10 — signal d'alerte critique",
      "NPS négatif (-55) — insatisfaction client",
      "7 tickets support en 90j — friction produit",
    ],
    recommended_plays: [
      "Appel exécutif dans les 48h — escalade senior",
      "Identifier et neutraliser le concurrent en évaluation",
      "Proposer un plan de valeur personnalisé (ROI review)",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier   = searchParams.get("tier");
  const risk   = searchParams.get("risk");
  const action = searchParams.get("action");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/customer-lifetime-value`);
      if (tier)   url.searchParams.set("tier", tier);
      if (risk)   url.searchParams.set("risk", risk);
      if (action) url.searchParams.set("action", action);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (tier)   accounts = accounts.filter((a) => a.clv_tier === tier);
  if (risk)   accounts = accounts.filter((a) => a.churn_risk === risk);
  if (action) accounts = accounts.filter((a) => a.clv_action === action);

  const tier_counts: Record<string, number>   = {};
  const risk_counts: Record<string, number>   = {};
  const action_counts: Record<string, number> = {};
  let total_clv = 0;
  let total_arr = 0;
  let total_exp = 0;
  let at_risk_arr = 0;

  for (const a of mockAccounts) {
    tier_counts[a.clv_tier]   = (tier_counts[a.clv_tier] || 0) + 1;
    risk_counts[a.churn_risk] = (risk_counts[a.churn_risk] || 0) + 1;
    action_counts[a.clv_action] = (action_counts[a.clv_action] || 0) + 1;
    total_clv += a.clv_3yr_eur;
    total_arr += a.arr_eur;
    total_exp += a.expansion_opportunity_eur;
    if (a.churn_risk === "critical" || a.churn_risk === "high") at_risk_arr += a.arr_eur;
  }

  const n = mockAccounts.length;
  const avg_health = mockAccounts.reduce((s, a) => s + a.health_score, 0) / n;

  return sealResponse(NextResponse.json({
    accounts,
    summary: {
      total: n,
      tier_counts,
      churn_risk_counts: risk_counts,
      action_counts,
      avg_health_score: Math.round(avg_health * 10) / 10,
      total_clv_eur: total_clv,
      total_arr_eur: total_arr,
      total_expansion_opportunity_eur: total_exp,
      at_risk_arr_eur: at_risk_arr,
      rescue_count: mockAccounts.filter((a) => a.clv_action === "rescue").length,
    },
  }));
}
