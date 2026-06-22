import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[account-health-scorer] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "ah_001",
    account_name: "CloudScale Technologies",
    arr_eur: 240000,
    segment: "enterprise",
    health_score: 91.0,
    health_tier: "champion",
    health_action: "celebrate",
    churn_risk: "low",
    expansion_potential: "strong",
    health_drivers: [
      "Engagement produit fort — DAU/MAU 45%",
      "Adoption features élevée — 72% des features actives",
      "NPS excellent (68) — compte promoteur actif",
      "Sponsor exécutif engagé — décision de renouvellement facilitée",
      "Champion fort (9/10) — défenseur interne actif",
      "Discussions expansion en cours — signal d'upsell positif",
      "5 intégrations actives — fort ancrage technique",
      "Historique de paiement parfait — compte fiable",
    ],
    risk_signals: [],
    recommended_plays: [
      "Programme référence client — case study ou témoignage",
      "Présenter la roadmap produit en avant-première — renforcer la fidélité",
      "Initier une conversation upsell/cross-sell formelle",
    ],
    renewal_probability_pct: 92.4,
  },
  {
    account_id: "ah_002",
    account_name: "DataVault Partners",
    arr_eur: 180000,
    segment: "enterprise",
    health_score: 83.0,
    health_tier: "champion",
    health_action: "celebrate",
    churn_risk: "low",
    expansion_potential: "strong",
    health_drivers: [
      "Engagement produit fort — DAU/MAU 38%",
      "NPS excellent (52) — compte promoteur actif",
      "Sponsor exécutif engagé — décision de renouvellement facilitée",
      "Champion fort (8/10) — défenseur interne actif",
      "Discussions expansion en cours — signal d'upsell positif",
      "Historique de paiement parfait — compte fiable",
    ],
    risk_signals: [],
    recommended_plays: [
      "Programme référence client — case study ou témoignage",
      "Présenter la roadmap produit en avant-première — renforcer la fidélité",
      "Initier une conversation upsell/cross-sell formelle",
    ],
    renewal_probability_pct: 87.6,
  },
  {
    account_id: "ah_003",
    account_name: "NexaRetail Group",
    arr_eur: 144000,
    segment: "enterprise",
    health_score: 72.0,
    health_tier: "healthy",
    health_action: "maintain",
    churn_risk: "medium",
    expansion_potential: "moderate",
    health_drivers: [
      "Adoption features élevée — 55% des features actives",
      "Champion fort (7/10) — défenseur interne actif",
      "Historique de paiement parfait — compte fiable",
    ],
    risk_signals: [
      "Aucun sponsor exécutif — vulnérabilité organisationnelle",
    ],
    recommended_plays: [
      "QBR prochain trimestre — maintenir l'alignement stratégique",
      "Identifier des opportunités d'adoption features non utilisées",
      "Explorer les besoins additionnels — potentiel expansion identifié",
    ],
    renewal_probability_pct: 73.2,
  },
  {
    account_id: "ah_004",
    account_name: "HealthBridge Systems",
    arr_eur: 96000,
    segment: "mid_market",
    health_score: 64.0,
    health_tier: "healthy",
    health_action: "maintain",
    churn_risk: "medium",
    expansion_potential: "limited",
    health_drivers: [
      "Engagement produit fort — DAU/MAU 32%",
      "Historique de paiement parfait — compte fiable",
    ],
    risk_signals: [
      "Dernier QBR il y a 95j — relation négligée",
      "Aucun sponsor exécutif — vulnérabilité organisationnelle",
    ],
    recommended_plays: [
      "QBR prochain trimestre — maintenir l'alignement stratégique",
      "Identifier des opportunités d'adoption features non utilisées",
    ],
    renewal_probability_pct: 64.4,
  },
  {
    account_id: "ah_005",
    account_name: "FinCore Solutions",
    arr_eur: 72000,
    segment: "mid_market",
    health_score: 48.0,
    health_tier: "at_risk",
    health_action: "intervene",
    churn_risk: "high",
    expansion_potential: "limited",
    health_drivers: [],
    risk_signals: [
      "Engagement produit faible — DAU/MAU 12% sous le seuil",
      "Adoption features insuffisante — 22% seulement",
      "Dernier QBR il y a 105j — relation négligée",
      "Aucun sponsor exécutif — vulnérabilité organisationnelle",
      "Champion faible (4/10) — risque si changement de contact",
    ],
    recommended_plays: [
      "Appel de revue urgente — identifier les frictions et blocages",
      "Escalade interne — impliquer le management dans la relation",
      "Session d'activation produit — former les utilisateurs inactifs",
    ],
    renewal_probability_pct: 48.8,
  },
  {
    account_id: "ah_006",
    account_name: "LogiFlux GmbH",
    arr_eur: 60000,
    segment: "mid_market",
    health_score: 41.0,
    health_tier: "at_risk",
    health_action: "intervene",
    churn_risk: "high",
    expansion_potential: "none",
    health_drivers: [],
    risk_signals: [
      "NPS négatif (-15) — risque de churn élevé",
      "2 ticket(s) critique(s) ouvert(s) — blocage produit",
      "Adoption features insuffisante — 18% seulement",
      "Aucun sponsor exécutif — vulnérabilité organisationnelle",
    ],
    recommended_plays: [
      "Appel de revue urgente — identifier les frictions et blocages",
      "Escalade interne — impliquer le management dans la relation",
      "Résoudre les tickets critiques en priorité absolue — unlocker le compte",
    ],
    renewal_probability_pct: 39.9,
  },
  {
    account_id: "ah_007",
    account_name: "EduSpark Ltd",
    arr_eur: 24000,
    segment: "smb",
    health_score: 22.0,
    health_tier: "critical",
    health_action: "escalate",
    churn_risk: "imminent",
    expansion_potential: "none",
    health_drivers: [],
    risk_signals: [
      "Engagement produit faible — DAU/MAU 5% sous le seuil",
      "Adoption features insuffisante — 8% seulement",
      "NPS négatif (-45) — risque de churn élevé",
      "3 ticket(s) critique(s) ouvert(s) — blocage produit",
      "Renouvellement dans 2 mois — fenêtre de risque",
      "Aucun sponsor exécutif — vulnérabilité organisationnelle",
      "2 facture(s) en retard — signal financier préoccupant",
    ],
    recommended_plays: [
      "Escalade C-level immédiate — mobiliser direction pour sauver le compte",
      "Plan de récupération 30j — objectifs mesurables et responsables définis",
      "Executive Business Review d'urgence — valeur démontrée, roadmap personnalisée",
      "Résoudre les impayés en priorité — éviter la suspension de service",
    ],
    renewal_probability_pct: 12.7,
  },
  {
    account_id: "ah_008",
    account_name: "PropLink AG",
    arr_eur: 12000,
    segment: "smb",
    health_score: 15.0,
    health_tier: "critical",
    health_action: "escalate",
    churn_risk: "imminent",
    expansion_potential: "none",
    health_drivers: [],
    risk_signals: [
      "Engagement produit faible — DAU/MAU 3% sous le seuil",
      "Adoption features insuffisante — 5% seulement",
      "NPS négatif (-60) — risque de churn élevé",
      "Renouvellement dans 1 mois — fenêtre de risque",
      "Aucun sponsor exécutif — vulnérabilité organisationnelle",
      "3 facture(s) en retard — signal financier préoccupant",
      "Champion faible (2/10) — risque si changement de contact",
    ],
    recommended_plays: [
      "Escalade C-level immédiate — mobiliser direction pour sauver le compte",
      "Plan de récupération 30j — objectifs mesurables et responsables définis",
      "Executive Business Review d'urgence — valeur démontrée, roadmap personnalisée",
      "Résoudre les impayés en priorité — éviter la suspension de service",
    ],
    renewal_probability_pct: 4.8,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const tier = searchParams.get("tier");
  const action = searchParams.get("action");
  const churn = searchParams.get("churn");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/account-health-scorer`);
      if (tier) url.searchParams.set("tier", tier);
      if (action) url.searchParams.set("action", action);
      if (churn) url.searchParams.set("churn", churn);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (tier) accounts = accounts.filter((a) => a.health_tier === tier);
  if (action) accounts = accounts.filter((a) => a.health_action === action);
  if (churn) accounts = accounts.filter((a) => a.churn_risk === churn);

  const tier_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const churn_counts: Record<string, number> = {};
  let total_score = 0;
  let arr_at_risk = 0;

  for (const a of mockAccounts) {
    tier_counts[a.health_tier] = (tier_counts[a.health_tier] || 0) + 1;
    action_counts[a.health_action] = (action_counts[a.health_action] || 0) + 1;
    churn_counts[a.churn_risk] = (churn_counts[a.churn_risk] || 0) + 1;
    total_score += a.health_score;
    if (a.health_tier === "at_risk" || a.health_tier === "critical") arr_at_risk += a.arr_eur;
  }

  const n = mockAccounts.length;

  return sealResponse(NextResponse.json({
    accounts,
    summary: {
      total: n,
      tier_counts,
      action_counts,
      churn_counts,
      avg_health_score: Math.round((total_score / n) * 10) / 10,
      champion_count: mockAccounts.filter((a) => a.health_tier === "champion").length,
      critical_count: mockAccounts.filter((a) => a.health_tier === "critical").length,
      total_arr_at_risk_eur: arr_at_risk,
    },
  }));
}
