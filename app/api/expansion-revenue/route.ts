import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[expansion-revenue] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "exp_001",
    account_name: "NexaCloud Enterprise",
    current_arr_eur: 240000,
    product_tier: "professional",
    expansion_tier: "hot",
    expansion_action: "close",
    expansion_score: 88.5,
    utilization_score: 100.0,
    relationship_score: 95.0,
    growth_score: 100.0,
    timing_score: 100.0,
    opportunity_types: ["SEAT_EXPANSION", "UPSELL", "RENEWAL_UPLIFT"],
    estimated_expansion_eur: 138000.0,
    seat_utilization_pct: 94.0,
    modules_utilization_pct: 72.0,
    positive_signals: [
      "Capacité quasi-atteinte — 94% des licences utilisées",
      "Adoption fonctionnelle excellente (82%)",
      "Engagement exécutif confirmé — deal décisionnel facilité",
      "Champion très actif — défense interne forte",
      "NPS excellent (72) — client promoteur",
      "3 signal(s) de croissance détecté(s) — intent expansion confirmé",
      "Historique d'expansion — client récurrent dans les achats",
      "QBR récent — relation maintenue et opportunités discutées",
      "Renouvellement dans 6 mois — fenêtre d'expansion idéale",
    ],
    risk_factors: [],
    recommended_actions: [
      "Proposer une extension de licences — utilisation actuelle à 94%",
      "Préparer une démonstration du tier supérieur (passage de professional)",
      "Négocier une revalorisation tarifaire à la prochaine fenêtre de renouvellement (6m)",
    ],
  },
  {
    account_id: "exp_002",
    account_name: "FinEdge Solutions",
    current_arr_eur: 180000,
    product_tier: "professional",
    expansion_tier: "hot",
    expansion_action: "close",
    expansion_score: 75.25,
    utilization_score: 95.0,
    relationship_score: 80.0,
    growth_score: 85.0,
    timing_score: 100.0,
    opportunity_types: ["SEAT_EXPANSION", "UPSELL", "RENEWAL_UPLIFT"],
    estimated_expansion_eur: 102000.0,
    seat_utilization_pct: 88.0,
    modules_utilization_pct: 65.0,
    positive_signals: [
      "Forte utilisation — 88% des licences actives",
      "Bonne adoption des fonctionnalités (68%)",
      "Engagement exécutif confirmé — deal décisionnel facilité",
      "Champion engagé — bonne adhésion interne",
      "NPS positif (38) — satisfaction bonne",
      "2 signal(s) de croissance détecté(s) — intent expansion confirmé",
      "Historique d'expansion — client récurrent dans les achats",
      "Renouvellement dans 7 mois — fenêtre d'expansion idéale",
    ],
    risk_factors: [],
    recommended_actions: [
      "Proposer une extension de licences — utilisation actuelle à 88%",
      "Préparer une démonstration du tier supérieur (passage de professional)",
      "Négocier une revalorisation tarifaire à la prochaine fenêtre de renouvellement (7m)",
    ],
  },
  {
    account_id: "exp_003",
    account_name: "RetailPro International",
    current_arr_eur: 144000,
    product_tier: "starter",
    expansion_tier: "warm",
    expansion_action: "nurture",
    expansion_score: 59.5,
    utilization_score: 80.0,
    relationship_score: 55.0,
    growth_score: 60.0,
    timing_score: 60.0,
    opportunity_types: ["UPSELL", "CROSS_SELL", "NEW_MODULE"],
    estimated_expansion_eur: 93600.0,
    seat_utilization_pct: 75.0,
    modules_utilization_pct: 45.0,
    positive_signals: [
      "Champion engagé — bonne adhésion interne",
      "NPS positif (28) — satisfaction bonne",
      "1 signal(s) de croissance détecté(s) — intent expansion confirmé",
    ],
    risk_factors: [],
    recommended_actions: [
      "Préparer une démonstration du tier supérieur (passage de starter)",
      "Présenter les 4 module(s) non adoptés lors du prochain QBR",
      "Améliorer l'adoption (42%) via une session d'activation fonctionnelle",
    ],
  },
  {
    account_id: "exp_004",
    account_name: "ManuGroup France",
    current_arr_eur: 120000,
    product_tier: "professional",
    expansion_tier: "warm",
    expansion_action: "nurture",
    expansion_score: 47.75,
    utilization_score: 60.0,
    relationship_score: 53.0,
    growth_score: 50.0,
    timing_score: 100.0,
    opportunity_types: ["UPSELL", "CROSS_SELL", "RENEWAL_UPLIFT"],
    estimated_expansion_eur: 57000.0,
    seat_utilization_pct: 72.0,
    modules_utilization_pct: 50.0,
    positive_signals: [
      "Bonne adoption des fonctionnalités (65%)",
      "Engagement exécutif confirmé — deal décisionnel facilité",
      "1 signal(s) de croissance détecté(s) — intent expansion confirmé",
      "Renouvellement dans 4 mois — fenêtre d'expansion idéale",
    ],
    risk_factors: [],
    recommended_actions: [
      "Préparer une démonstration du tier supérieur (passage de professional)",
      "Présenter les 3 module(s) non adoptés lors du prochain QBR",
      "Négocier une revalorisation tarifaire à la prochaine fenêtre de renouvellement (4m)",
      "Planifier un QBR — dernière revue > 90j",
    ],
  },
  {
    account_id: "exp_005",
    account_name: "HealthCo Belgium",
    current_arr_eur: 72000,
    product_tier: "starter",
    expansion_tier: "cool",
    expansion_action: "qualify",
    expansion_score: 35.5,
    utilization_score: 40.0,
    relationship_score: 30.0,
    growth_score: 40.0,
    timing_score: 60.0,
    opportunity_types: ["UPSELL", "CROSS_SELL", "NEW_MODULE"],
    estimated_expansion_eur: 45360.0,
    seat_utilization_pct: 58.0,
    modules_utilization_pct: 40.0,
    positive_signals: [
      "NPS positif (22) — satisfaction bonne",
    ],
    risk_factors: [
      "Champion faible ou absent — support interne insuffisant",
    ],
    recommended_actions: [
      "Préparer une démonstration du tier supérieur (passage de starter)",
      "Présenter les 3 module(s) non adoptés lors du prochain QBR",
      "Améliorer l'adoption (35%) via une session d'activation fonctionnelle",
    ],
  },
  {
    account_id: "exp_006",
    account_name: "EduTech Learn GmbH",
    current_arr_eur: 48000,
    product_tier: "starter",
    expansion_tier: "cool",
    expansion_action: "qualify",
    expansion_score: 28.0,
    utilization_score: 20.0,
    relationship_score: 28.0,
    growth_score: 40.0,
    timing_score: 60.0,
    opportunity_types: ["UPSELL", "NEW_MODULE"],
    estimated_expansion_eur: 29760.0,
    seat_utilization_pct: 45.0,
    modules_utilization_pct: 62.0,
    positive_signals: [
      "Champion engagé — bonne adhésion interne",
    ],
    risk_factors: [
      "Dernier QBR il y a 200j — relation à ré-activer",
    ],
    recommended_actions: [
      "Préparer une démonstration du tier supérieur (passage de starter)",
      "Améliorer l'adoption (28%) via une session d'activation fonctionnelle",
      "Planifier un QBR — dernière revue > 90j",
    ],
  },
  {
    account_id: "exp_007",
    account_name: "PropTech Venture",
    current_arr_eur: 36000,
    product_tier: "professional",
    expansion_tier: "cold",
    expansion_action: "watch",
    expansion_score: 18.0,
    utilization_score: 20.0,
    relationship_score: 10.0,
    growth_score: 15.0,
    timing_score: 30.0,
    opportunity_types: ["NEW_MODULE"],
    estimated_expansion_eur: 4320.0,
    seat_utilization_pct: 40.0,
    modules_utilization_pct: 70.0,
    positive_signals: [],
    risk_factors: [
      "Pression concurrentielle active — rétention prioritaire avant expansion",
      "NPS négatif (-15) — insatisfaction à résoudre en priorité",
      "Champion faible ou absent — support interne insuffisant",
      "Dernier QBR il y a 250j — relation à ré-activer",
      "Adoption faible (22%) — risque de churn avant expansion",
    ],
    recommended_actions: [
      "Améliorer l'adoption (22%) via une session d'activation fonctionnelle",
      "Renforcer la valeur perçue avant toute conversation d'expansion",
      "Planifier un QBR — dernière revue > 90j",
    ],
  },
  {
    account_id: "exp_008",
    account_name: "LogiChain Systems",
    current_arr_eur: 24000,
    product_tier: "starter",
    expansion_tier: "cold",
    expansion_action: "watch",
    expansion_score: 8.5,
    utilization_score: 20.0,
    relationship_score: 0.0,
    growth_score: 15.0,
    timing_score: 30.0,
    opportunity_types: ["NEW_MODULE"],
    estimated_expansion_eur: 2880.0,
    seat_utilization_pct: 35.0,
    modules_utilization_pct: 75.0,
    positive_signals: [],
    risk_factors: [
      "Pression concurrentielle active — rétention prioritaire avant expansion",
      "Santé compte faible (35) — résoudre les problèmes avant d'upseller",
      "NPS négatif (-30) — insatisfaction à résoudre en priorité",
      "Champion faible ou absent — support interne insuffisant",
      "Contrat expiré ou mois-à-mois — priorité renouvellement avant expansion",
      "Adoption faible (18%) — risque de churn avant expansion",
    ],
    recommended_actions: [
      "Améliorer l'adoption (18%) via une session d'activation fonctionnelle",
      "Renforcer la valeur perçue avant toute conversation d'expansion",
      "Priorité : résoudre les problèmes de santé compte avant expansion",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier = searchParams.get("tier");
  const action = searchParams.get("action");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/expansion-revenue`);
      if (tier) url.searchParams.set("tier", tier);
      if (action) url.searchParams.set("action", action);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (tier) accounts = accounts.filter((a) => a.expansion_tier === tier);
  if (action) accounts = accounts.filter((a) => a.expansion_action === action);

  const tier_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_score = 0;
  let total_expansion = 0;
  let total_arr = 0;
  let hot_count = 0;
  let close_count = 0;

  for (const a of mockAccounts) {
    tier_counts[a.expansion_tier] = (tier_counts[a.expansion_tier] || 0) + 1;
    action_counts[a.expansion_action] = (action_counts[a.expansion_action] || 0) + 1;
    total_score += a.expansion_score;
    total_expansion += a.estimated_expansion_eur;
    total_arr += a.current_arr_eur;
    if (a.expansion_tier === "hot") hot_count++;
    if (a.expansion_action === "close") close_count++;
  }

  const n = mockAccounts.length;

  return sealResponse(NextResponse.json({
    accounts,
    summary: {
      total: n,
      tier_counts,
      action_counts,
      avg_expansion_score: Math.round((total_score / n) * 10) / 10,
      total_estimated_expansion_eur: Math.round(total_expansion * 100) / 100,
      total_current_arr_eur: total_arr,
      hot_count,
      close_ready_count: close_count,
    },
  }));
}
