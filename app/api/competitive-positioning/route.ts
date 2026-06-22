import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[competitive-positioning] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "d_001",
    account_id: "acc_001",
    account_name: "TechCorp SA",
    deal_name: "ERP Migration Q3",
    deal_value: 180000,
    competitor_name: "Salesforce",
    positioning_score: 82.4,
    positioning_strength: "dominant",
    competitor_threat: "medium",
    win_probability: "very_high",
    recommended_action: "accelerate",
    battlecard_points: [
      "Supériorité produit claire (+16pts) — démontrer les cas d'usage clés",
      "Avantage POC — résultats concrets à présenter au comité",
      "Champion interne actif — le mobiliser pour défendre la décision",
      "Plus de références clients (3 de plus) — organiser des appels de référence",
      "4 différenciateurs uniques démontrés — les ancrer dans la proposition de valeur",
    ],
    risk_factors: [],
    win_rate_vs_competitor: 0.667,
    competitive_gap: 18.4,
    is_winnable: true,
    urgency_score: 48.0,
    key_differentiators: [
      "Adéquation produit supérieure (88/100 vs 72/100)",
      "Preuve de concept réalisée avec succès",
      "4 fonctionnalité(s) unique(s) non disponibles chez Salesforce",
      "5 références clients vérifiables dans le secteur",
    ],
  },
  {
    deal_id: "d_002",
    account_id: "acc_002",
    account_name: "GlobalFinance SARL",
    deal_name: "CRM Unification",
    deal_value: 95000,
    competitor_name: "Microsoft Dynamics",
    positioning_score: 14.0,
    positioning_strength: "critical",
    competitor_threat: "high",
    win_probability: "very_low",
    recommended_action: "executive_escalation",
    battlecard_points: [],
    risk_factors: [
      "Microsoft Dynamics est le fournisseur actuel — coûts de migration importants",
      "Microsoft Dynamics a une preuve de concept — risque de verrouillage technique",
      "Écart de prix défavorable (22% moins cher) — préparer la justification du ROI",
      "Relation concurrente plus forte — risque de décision basée sur la relation",
      "Absence de champion interne — décision moins prévisible",
      "Décideur budget non engagé — deal en risque de stagnation",
    ],
    win_rate_vs_competitor: 0.2,
    competitive_gap: -40.2,
    is_winnable: false,
    urgency_score: 70.0,
    key_differentiators: [],
  },
  {
    deal_id: "d_003",
    account_id: "acc_003",
    account_name: "MediaGroup SAS",
    deal_name: "Analytics Platform",
    deal_value: 60000,
    competitor_name: "HubSpot",
    positioning_score: 64.8,
    positioning_strength: "strong",
    competitor_threat: "medium",
    win_probability: "high",
    recommended_action: "differentiate",
    battlecard_points: [
      "Supériorité produit claire (+15pts) — démontrer les cas d'usage clés",
      "Champion interne actif — le mobiliser pour défendre la décision",
      "3 différenciateurs uniques démontrés — les ancrer dans la proposition de valeur",
      "Relation commerciale supérieure — capitaliser sur la confiance établie",
    ],
    risk_factors: [
      "Absence de champion interne — décision moins prévisible",
    ],
    win_rate_vs_competitor: 0.6,
    competitive_gap: 22.0,
    is_winnable: true,
    urgency_score: 35.0,
    key_differentiators: [
      "Adéquation produit supérieure (82/100 vs 67/100)",
      "3 fonctionnalité(s) unique(s) non disponibles chez HubSpot",
      "4 références clients vérifiables dans le secteur",
    ],
  },
  {
    deal_id: "d_004",
    account_id: "acc_004",
    account_name: "RetailChain Nord",
    deal_name: "Customer 360",
    deal_value: 75000,
    competitor_name: "SAP",
    positioning_score: 38.5,
    positioning_strength: "weak",
    competitor_threat: "high",
    win_probability: "low",
    recommended_action: "executive_escalation",
    battlecard_points: [
      "Positionnement prix compétitif — mettre en avant le ROI total (TCO)",
    ],
    risk_factors: [
      "SAP est le fournisseur actuel — coûts de migration importants",
      "SAP a une preuve de concept — risque de verrouillage technique",
      "Relation concurrente plus forte — risque de décision basée sur la relation",
      "Absence de champion interne — décision moins prévisible",
      "Bilan négatif face à SAP (1V/4D) — analyser les pertes passées",
    ],
    win_rate_vs_competitor: 0.2,
    competitive_gap: -18.0,
    is_winnable: true,
    urgency_score: 83.0,
    key_differentiators: [
      "Preuve de concept réalisée avec succès",
    ],
  },
  {
    deal_id: "d_005",
    account_id: "acc_005",
    account_name: "HealthTech Pro",
    deal_name: "Patient Data Platform",
    deal_value: 220000,
    competitor_name: "Oracle",
    positioning_score: 70.2,
    positioning_strength: "strong",
    competitor_threat: "medium",
    win_probability: "high",
    recommended_action: "differentiate",
    battlecard_points: [
      "Champion interne actif — le mobiliser pour défendre la décision",
      "Avantage POC — résultats concrets à présenter au comité",
      "5 différenciateurs uniques démontrés — les ancrer dans la proposition de valeur",
      "Bilan favorable face à Oracle (3V/2D) — utiliser comme preuve sociale",
    ],
    risk_factors: [
      "Décideur budget non engagé — deal en risque de stagnation",
    ],
    win_rate_vs_competitor: 0.6,
    competitive_gap: 12.0,
    is_winnable: true,
    urgency_score: 43.0,
    key_differentiators: [
      "Adéquation produit supérieure (78/100 vs 66/100)",
      "Preuve de concept réalisée avec succès",
      "5 fonctionnalité(s) unique(s) non disponibles chez Oracle",
      "4 références clients vérifiables dans le secteur",
    ],
  },
  {
    deal_id: "d_006",
    account_id: "acc_006",
    account_name: "LogisticsPlus SA",
    deal_name: "Supply Chain Intelligence",
    deal_value: 140000,
    competitor_name: "Zendesk",
    positioning_score: 55.3,
    positioning_strength: "competitive",
    competitor_threat: "low",
    win_probability: "medium",
    recommended_action: "differentiate",
    battlecard_points: [
      "Supériorité produit claire (+10pts) — démontrer les cas d'usage clés",
      "2 différenciateurs uniques démontrés — les ancrer dans la proposition de valeur",
    ],
    risk_factors: [
      "Absence de champion interne — décision moins prévisible",
    ],
    win_rate_vs_competitor: 0.5,
    competitive_gap: 8.0,
    is_winnable: true,
    urgency_score: 25.0,
    key_differentiators: [
      "Adéquation produit supérieure (75/100 vs 65/100)",
      "2 fonctionnalité(s) unique(s) non disponibles chez Zendesk",
    ],
  },
  {
    deal_id: "d_007",
    account_id: "acc_007",
    account_name: "EduSmart Group",
    deal_name: "LMS Platform",
    deal_value: 45000,
    competitor_name: "Pipedrive",
    positioning_score: 88.1,
    positioning_strength: "dominant",
    competitor_threat: "low",
    win_probability: "very_high",
    recommended_action: "accelerate",
    battlecard_points: [
      "Supériorité produit claire (+20pts) — démontrer les cas d'usage clés",
      "Positionnement prix compétitif — mettre en avant le ROI total (TCO)",
      "Avantage POC — résultats concrets à présenter au comité",
      "Champion interne actif — le mobiliser pour défendre la décision",
      "Plus de références clients (4 de plus) — organiser des appels de référence",
      "5 différenciateurs uniques démontrés — les ancrer dans la proposition de valeur",
      "Bilan favorable face à Pipedrive (5V/1D) — utiliser comme preuve sociale",
    ],
    risk_factors: [],
    win_rate_vs_competitor: 0.833,
    competitive_gap: 24.0,
    is_winnable: true,
    urgency_score: 25.0,
    key_differentiators: [
      "Adéquation produit supérieure (90/100 vs 70/100)",
      "Prix compétitif — 15% plus économique sur le TCO",
      "Preuve de concept réalisée avec succès",
      "5 fonctionnalité(s) unique(s) non disponibles chez Pipedrive",
      "5 références clients vérifiables dans le secteur",
    ],
  },
  {
    deal_id: "d_008",
    account_id: "acc_008",
    account_name: "FinServ Capital",
    deal_name: "Risk Analytics",
    deal_value: 310000,
    competitor_name: "Workday",
    positioning_score: 47.0,
    positioning_strength: "competitive",
    competitor_threat: "medium",
    win_probability: "medium",
    recommended_action: "competitive_response",
    battlecard_points: [
      "Champion interne actif — le mobiliser pour défendre la décision",
    ],
    risk_factors: [
      "Workday a une preuve de concept — risque de verrouillage technique",
      "Absence de champion interne — décision moins prévisible",
    ],
    win_rate_vs_competitor: 0.5,
    competitive_gap: 5.0,
    is_winnable: true,
    urgency_score: 60.0,
    key_differentiators: [
      "3 fonctionnalité(s) unique(s) non disponibles chez Workday",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const strength    = searchParams.get("strength");
  const threat      = searchParams.get("threat");
  const probability = searchParams.get("probability");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/competitive-positioning`);
      if (strength)    url.searchParams.set("strength", strength);
      if (threat)      url.searchParams.set("threat", threat);
      if (probability) url.searchParams.set("probability", probability);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let deals = [...mockDeals];
  if (strength)    deals = deals.filter((d) => d.positioning_strength === strength);
  if (threat)      deals = deals.filter((d) => d.competitor_threat === threat);
  if (probability) deals = deals.filter((d) => d.win_probability === probability);

  const strength_counts:    Record<string, number> = {};
  const threat_counts:      Record<string, number> = {};
  const probability_counts: Record<string, number> = {};
  const action_counts:      Record<string, number> = {};
  let total_pos = 0, total_wr = 0, total_urg = 0, total_gap = 0;

  for (const d of mockDeals) {
    strength_counts[d.positioning_strength]  = (strength_counts[d.positioning_strength] || 0) + 1;
    threat_counts[d.competitor_threat]       = (threat_counts[d.competitor_threat] || 0) + 1;
    probability_counts[d.win_probability]    = (probability_counts[d.win_probability] || 0) + 1;
    action_counts[d.recommended_action]      = (action_counts[d.recommended_action] || 0) + 1;
    total_pos += d.positioning_score;
    total_wr  += d.win_rate_vs_competitor;
    total_urg += d.urgency_score;
    total_gap += d.competitive_gap;
  }

  const n = mockDeals.length;

  return sealResponse(NextResponse.json({
    deals,
    summary: {
      total:                  n,
      strength_counts,
      threat_counts,
      probability_counts,
      action_counts,
      avg_positioning_score:  Math.round((total_pos / n) * 10) / 10,
      avg_win_rate:           Math.round((total_wr / n) * 1000) / 1000,
      avg_urgency_score:      Math.round((total_urg / n) * 10) / 10,
      high_threat_count:      mockDeals.filter((d) => d.competitor_threat === "high").length,
      winnable_count:         mockDeals.filter((d) => d.is_winnable).length,
      dominant_count:         mockDeals.filter((d) => d.positioning_strength === "dominant").length,
      escalation_count:       mockDeals.filter((d) => d.recommended_action === "executive_escalation").length,
      avg_competitive_gap:    Math.round((total_gap / n) * 10) / 10,
    },
  }));
}
