import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "ci_001",
    deal_name: "ERP Total Energies",
    rep_id: "rep_001",
    rep_name: "Sophie Martin",
    account_name: "Total Energies SE",
    competitor_name: "SAP S/4HANA",
    competitor_category: "enterprise",
    competitor_threat: "critical",
    competitive_position: "tied",
    competitive_action: "defend_and_close",
    threat_score: 95.0,
    position_score: 89.0,
    win_probability_pct: 52.5,
    battle_tactics: [
      "Escalade exécutive urgente — impliquer le C-level pour contrer SAP S/4HANA",
      "RFP détecté chez SAP S/4HANA — activer la battlecard de réponse RFP immédiatement",
      "Demo concurrente demandée — organiser une contre-démo centrée sur les cas d'usage critiques",
      "Grille tarifaire concurrente reçue — construire une analyse TCO sur 3 ans favorable",
    ],
    differentiators: [
      "4 fonctionnalités exclusives non disponibles chez SAP S/4HANA",
      "PoC complété — valeur prouvée sur l'environnement client réel",
      "Sponsor exécutif engagé — relation stratégique au niveau C confirmée",
      "Historique favorable vs SAP S/4HANA: 62% de taux de victoire",
    ],
    risk_signals: [
      "RFP envoyé à SAP S/4HANA — deal en danger immédiat",
      "Décideur a rencontré SAP S/4HANA — évaluation active en cours",
    ],
    manager_alerts: [
      "⚠ Menace critique (SAP S/4HANA) sur deal ERP Total Energies (320,000€) — intervention immédiate requise",
      "RFP deal stratégique (320,000€) — mobiliser l'équipe solution pour réponse complète",
    ],
  },
  {
    deal_id: "ci_002",
    deal_name: "CRM Capgemini",
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    account_name: "Capgemini France",
    competitor_name: "Salesforce",
    competitor_category: "enterprise",
    competitor_threat: "high",
    competitive_position: "trailing",
    competitive_action: "escalate",
    threat_score: 65.0,
    position_score: 42.0,
    win_probability_pct: 31.0,
    battle_tactics: [
      "Escalade exécutive urgente — impliquer le C-level pour contrer Salesforce",
      "Planifier une session de solution architect pour démonstration technique approfondie",
      "Demo concurrente demandée — organiser une contre-démo centrée sur les cas d'usage critiques",
    ],
    differentiators: [
      "3 fonctionnalités exclusives non disponibles chez Salesforce",
      "Position tarifaire compétitive — prix aligné ou avantageux vs concurrent",
    ],
    risk_signals: [
      "Champion interne soutient le concurrent — influence décisionnelle compromise",
      "Décideur a rencontré Salesforce — évaluation active en cours",
    ],
    manager_alerts: [
      "⚠ Menace critique (Salesforce) sur deal CRM Capgemini (185,000€) — intervention immédiate requise",
      "Position perdante vs Salesforce — revue stratégique deal urgente avec le manager",
    ],
  },
  {
    deal_id: "ci_003",
    deal_name: "Analytics Sodexo",
    rep_id: "rep_001",
    rep_name: "Sophie Martin",
    account_name: "Sodexo Group",
    competitor_name: "Microsoft Power BI",
    competitor_category: "enterprise",
    competitor_threat: "moderate",
    competitive_position: "leading",
    competitive_action: "differentiate",
    threat_score: 35.0,
    position_score: 72.0,
    win_probability_pct: 68.5,
    battle_tactics: [
      "Grille tarifaire concurrente reçue — construire une analyse TCO sur 3 ans favorable",
      "Aucune référence envoyée — sélectionner 2–3 clients comparables et organiser des calls de référence",
    ],
    differentiators: [
      "2 fonctionnalités exclusives non disponibles chez Microsoft Power BI",
      "Sponsor exécutif engagé — relation stratégique au niveau C confirmée",
      "Relation décideur forte (8/10) — influence sur la décision finale",
      "Historique favorable vs Microsoft Power BI: 70% de taux de victoire",
      "Position tarifaire compétitive — prix aligné ou avantageux vs concurrent",
    ],
    risk_signals: [],
    manager_alerts: [],
  },
  {
    deal_id: "ci_004",
    deal_name: "HCM Veolia",
    rep_id: "rep_003",
    rep_name: "Marie Lefevre",
    account_name: "Veolia Environnement",
    competitor_name: "Workday",
    competitor_category: "enterprise",
    competitor_threat: "high",
    competitive_position: "tied",
    competitive_action: "price_protect",
    threat_score: 58.0,
    position_score: 61.0,
    win_probability_pct: 45.0,
    battle_tactics: [
      "Grille tarifaire concurrente reçue — construire une analyse TCO sur 3 ans favorable",
      "RFP détecté chez Workday — activer la battlecard de réponse RFP immédiatement",
      "Fort fit produit non démontré — proposer un PoC ciblé sur les cas d'usage clés",
    ],
    differentiators: [
      "2 fonctionnalités exclusives non disponibles chez Workday",
      "Position tarifaire compétitive — prix aligné ou avantageux vs concurrent",
    ],
    risk_signals: [
      "RFP envoyé à Workday — deal en danger immédiat",
      "Décideur a rencontré Workday — évaluation active en cours",
      "Grille tarifaire concurrente partagée + notre prix non compétitif — risque de disqualification prix",
    ],
    manager_alerts: [
      "⚠ Menace critique (Workday) sur deal HCM Veolia (72,000€) — intervention immédiate requise",
      "RFP deal stratégique (72,000€) — mobiliser l'équipe solution pour réponse complète",
    ],
  },
  {
    deal_id: "ci_005",
    deal_name: "Plateforme Boulanger",
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    account_name: "Boulanger SA",
    competitor_name: "HubSpot",
    competitor_category: "mid_market",
    competitor_threat: "low",
    competitive_position: "winning",
    competitive_action: "maintain",
    threat_score: 15.0,
    position_score: 78.0,
    win_probability_pct: 80.0,
    battle_tactics: [
      "Surveiller l'activité de HubSpot — maintenir cadence d'engagement prospect",
    ],
    differentiators: [
      "3 fonctionnalités exclusives non disponibles chez HubSpot",
      "PoC complété — valeur prouvée sur l'environnement client réel",
      "Sponsor exécutif engagé — relation stratégique au niveau C confirmée",
      "Relation décideur forte (9/10) — influence sur la décision finale",
      "Historique favorable vs HubSpot: 75% de taux de victoire",
      "Position tarifaire compétitive — prix aligné ou avantageux vs concurrent",
    ],
    risk_signals: [],
    manager_alerts: [],
  },
  {
    deal_id: "ci_006",
    deal_name: "Dev Interne Picard",
    rep_id: "rep_003",
    rep_name: "Marie Lefevre",
    account_name: "Picard Surgelés",
    competitor_name: "Développement interne",
    competitor_category: "in_house",
    competitor_threat: "moderate",
    competitive_position: "tied",
    competitive_action: "defend_and_close",
    threat_score: 40.0,
    position_score: 52.0,
    win_probability_pct: 48.0,
    battle_tactics: [
      "Demo concurrente demandée — organiser une contre-démo centrée sur les cas d'usage critiques",
      "Aucune référence envoyée — sélectionner 2–3 clients comparables et organiser des calls de référence",
      "Fort fit produit non démontré — proposer un PoC ciblé sur les cas d'usage clés",
    ],
    differentiators: [
      "2 fonctionnalités exclusives non disponibles chez Développement interne",
      "Relation décideur forte (7/10) — influence sur la décision finale",
    ],
    risk_signals: [
      "Décideur a rencontré Développement interne — évaluation active en cours",
    ],
    manager_alerts: [],
  },
  {
    deal_id: "ci_007",
    deal_name: "Monitoring Allia",
    rep_id: "rep_004",
    rep_name: "Thomas Bernard",
    account_name: "Allia Habitat",
    competitor_name: "Datadog",
    competitor_category: "startup",
    competitor_threat: "critical",
    competitive_position: "losing",
    competitive_action: "escalate",
    threat_score: 85.0,
    position_score: 28.0,
    win_probability_pct: 18.0,
    battle_tactics: [
      "Escalade exécutive urgente — impliquer le C-level pour contrer Datadog",
      "Planifier une session de solution architect pour démonstration technique approfondie",
      "RFP détecté chez Datadog — activer la battlecard de réponse RFP immédiatement",
      "Champion adverse identifié — identifier et activer un champion alternatif chez le prospect",
    ],
    differentiators: [
      "Identifier les différenciateurs clés lors de la prochaine réunion — préparer le battlecard",
    ],
    risk_signals: [
      "RFP envoyé à Datadog — deal en danger immédiat",
      "Champion interne soutient le concurrent — influence décisionnelle compromise",
      "Décideur a rencontré Datadog — évaluation active en cours",
      "4 pertes historiques vs Datadog — pattern préoccupant",
      "Taux de victoire historique de 22% vs Datadog — taux critique",
    ],
    manager_alerts: [
      "⚠ Menace critique (Datadog) sur deal Monitoring Allia (18,000€) — intervention immédiate requise",
      "Position perdante vs Datadog — revue stratégique deal urgente avec le manager",
      "Probabilité de victoire critique: 18% — évaluer si le deal doit être reclassifié",
    ],
  },
  {
    deal_id: "ci_008",
    deal_name: "BI Sofitel",
    rep_id: "rep_004",
    rep_name: "Thomas Bernard",
    account_name: "Sofitel Luxury Hotels",
    competitor_name: "Tableau",
    competitor_category: "enterprise",
    competitor_threat: "none",
    competitive_position: "winning",
    competitive_action: "monitor",
    threat_score: 5.0,
    position_score: 82.0,
    win_probability_pct: 85.0,
    battle_tactics: [
      "Surveiller l'activité de Tableau — maintenir cadence d'engagement prospect",
    ],
    differentiators: [
      "5 fonctionnalités exclusives non disponibles chez Tableau",
      "PoC complété — valeur prouvée sur l'environnement client réel",
      "Sponsor exécutif engagé — relation stratégique au niveau C confirmée",
      "Relation décideur forte (9/10) — influence sur la décision finale",
      "Position tarifaire compétitive — prix aligné ou avantageux vs concurrent",
    ],
    risk_signals: [],
    manager_alerts: [],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const threat   = searchParams.get("threat");
  const position = searchParams.get("position");
  const action   = searchParams.get("action");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/competitive-intelligence`);
      if (threat)   url.searchParams.set("threat", threat);
      if (position) url.searchParams.set("position", position);
      if (action)   url.searchParams.set("action", action);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (threat)   deals = deals.filter((d) => d.competitor_threat === threat);
  if (position) deals = deals.filter((d) => d.competitive_position === position);
  if (action)   deals = deals.filter((d) => d.competitive_action === action);

  const threat_counts:   Record<string, number> = {};
  const position_counts: Record<string, number> = {};
  const action_counts:   Record<string, number> = {};
  let total_threat = 0;
  let total_position = 0;
  let total_win = 0;

  for (const d of mockDeals) {
    threat_counts[d.competitor_threat]     = (threat_counts[d.competitor_threat] || 0) + 1;
    position_counts[d.competitive_position] = (position_counts[d.competitive_position] || 0) + 1;
    action_counts[d.competitive_action]    = (action_counts[d.competitive_action] || 0) + 1;
    total_threat   += d.threat_score;
    total_position += d.position_score;
    total_win      += d.win_probability_pct;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      threat_counts,
      position_counts,
      action_counts,
      avg_threat_score:    Math.round((total_threat / n) * 10) / 10,
      avg_position_score:  Math.round((total_position / n) * 10) / 10,
      avg_win_probability: Math.round((total_win / n) * 10) / 10,
      critical_count:      mockDeals.filter((d) => d.competitor_threat === "critical").length,
      losing_count:        mockDeals.filter((d) => d.competitive_position === "losing").length,
      escalation_count:    mockDeals.filter((d) => d.competitive_action === "escalate").length,
    },
  });
}
