import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[churn-predictor] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "acc_001",
    account_name: "TechCorp Enterprise",
    arr_eur: 240000,
    churn_probability_pct: 84.2,
    churn_risk: "critical",
    retention_action: "emergency",
    churn_drivers: [
      "Usage en déclin (MAU -45%)",
      "Champion perdu — relation à reconstruire",
      "RFP reçu — évaluation formelle ouverte",
      "3 bugs critiques ouverts — impact business",
      "NPS très négatif (-42)",
      "NPS en déclin",
    ],
    retention_signals: [],
    risk_flags: [
      "CRITIQUE — perte imminente (201 840€ à risque)",
      "Double menace — champion perdu ET RFP ouvert simultanément",
      "3 bugs critiques bloquants — escalade requise",
    ],
    recommended_actions: [
      "Identifier et activer un nouveau champion interne en urgence",
      "Déclencher un call exécutif d'urgence et préparer une contre-proposition",
      "Escalader les 3 bug(s) critique(s) à l'équipe engineering",
      "Planifier un Success Call pour comprendre le déclin d'usage",
      "Conduire une interview NPS Detractor pour identifier les irritants",
      "Demander une introduction au sponsor exécutif côté client",
    ],
    arr_at_risk_eur: 201840,
    days_to_act: 3,
    usage_risk_score: 72.0,
    support_risk_score: 70.0,
    financial_risk_score: 0.0,
    relationship_risk_score: 80.0,
    competitive_risk_score: 85.0,
  },
  {
    account_id: "acc_002",
    account_name: "FinancePlus SA",
    arr_eur: 180000,
    churn_probability_pct: 71.5,
    churn_risk: "high",
    retention_action: "emergency",
    churn_drivers: [
      "RFP reçu — évaluation formelle ouverte",
      "Usage en déclin (MAU -28%)",
      "2 retards de paiement",
      "Concurrent mentionné — évaluation en cours",
      "Renouvellement dans 45 jours",
    ],
    retention_signals: [
      "Sponsor exécutif impliqué — relation stratégique solide",
    ],
    risk_flags: [
      "Renouvellement CRITIQUE dans 45 jours",
    ],
    recommended_actions: [
      "Déclencher un call exécutif d'urgence et préparer une contre-proposition",
      "Planifier un Success Call pour comprendre le déclin d'usage",
      "Déclencher le processus de renouvellement anticipé",
      "Aligner Finance et Account Manager sur la situation de paiement",
    ],
    arr_at_risk_eur: 128700,
    days_to_act: 7,
    usage_risk_score: 48.0,
    support_risk_score: 5.0,
    financial_risk_score: 30.0,
    relationship_risk_score: 25.0,
    competitive_risk_score: 85.0,
  },
  {
    account_id: "acc_003",
    account_name: "RetailGroup France",
    arr_eur: 120000,
    churn_probability_pct: 63.8,
    churn_risk: "high",
    retention_action: "rescue",
    churn_drivers: [
      "Connexions rares (tous les 12 jours)",
      "Adoption très faible (18%)",
      "4 tickets en retard — insatisfaction support",
      "1 bug critique ouvert — impact business",
      "NPS négatif (-15)",
      "Dernier QBR > 90 jours",
    ],
    retention_signals: [
      "Historique de paiement parfait",
    ],
    risk_flags: [
      "1 bug critique bloquant — escalade requise",
    ],
    recommended_actions: [
      "Escalader les 1 bug(s) critique(s) à l'équipe engineering",
      "Proposer une session de formation sur les fonctionnalités clés",
      "Conduire une interview NPS Detractor pour identifier les irritants",
      "Planifier un QBR immédiatement — dernier QBR trop ancien",
      "Demander une introduction au sponsor exécutif côté client",
    ],
    arr_at_risk_eur: 76560,
    days_to_act: 7,
    usage_risk_score: 55.0,
    support_risk_score: 65.0,
    financial_risk_score: 0.0,
    relationship_risk_score: 50.0,
    competitive_risk_score: 0.0,
  },
  {
    account_id: "acc_004",
    account_name: "StartupCloud SAS",
    arr_eur: 48000,
    churn_probability_pct: 52.1,
    churn_risk: "medium",
    retention_action: "proactive",
    churn_drivers: [
      "Usage en déclin (MAU -22%)",
      "Champion perdu — relation à reconstruire",
      "NPS en déclin",
    ],
    retention_signals: [
      "Sponsor exécutif impliqué — relation stratégique solide",
      "Aucun ticket ouvert — client satisfait",
      "Historique de paiement parfait",
    ],
    risk_flags: [],
    recommended_actions: [
      "Identifier et activer un nouveau champion interne en urgence",
      "Planifier un Success Call pour comprendre le déclin d'usage",
      "Déclencher le processus de renouvellement anticipé",
    ],
    arr_at_risk_eur: 25008,
    days_to_act: 14,
    usage_risk_score: 38.0,
    support_risk_score: 0.0,
    financial_risk_score: 0.0,
    relationship_risk_score: 60.0,
    competitive_risk_score: 0.0,
  },
  {
    account_id: "acc_005",
    account_name: "ManuFactory Pro",
    arr_eur: 95000,
    churn_probability_pct: 45.6,
    churn_risk: "medium",
    retention_action: "proactive",
    churn_drivers: [
      "Légère baisse d'usage (MAU -8%)",
      "1 retard de paiement",
      "Connexions rares (tous les 9 jours)",
      "Concurrent mentionné — évaluation en cours",
    ],
    retention_signals: [
      "Forte adoption fonctionnelle (72%)",
      "NPS positif (28) — client satisfait",
    ],
    risk_flags: [],
    recommended_actions: [
      "Planifier un Success Call pour comprendre le déclin d'usage",
      "Aligner Finance et Account Manager sur la situation de paiement",
      "Demander une introduction au sponsor exécutif côté client",
    ],
    arr_at_risk_eur: 43320,
    days_to_act: 14,
    usage_risk_score: 20.0,
    support_risk_score: 10.0,
    financial_risk_score: 15.0,
    relationship_risk_score: 20.0,
    competitive_risk_score: 35.0,
  },
  {
    account_id: "acc_006",
    account_name: "ConsultFirst International",
    arr_eur: 72000,
    churn_probability_pct: 31.4,
    churn_risk: "low",
    retention_action: "nurture",
    churn_drivers: [
      "Adoption très faible (25%)",
      "Renouvellement dans 75 jours",
    ],
    retention_signals: [
      "Sponsor exécutif impliqué — relation stratégique solide",
      "Aucun ticket ouvert — client satisfait",
      "Historique de paiement parfait",
    ],
    risk_flags: [],
    recommended_actions: [
      "Proposer une session de formation sur les fonctionnalités clés",
      "Déclencher le processus de renouvellement anticipé",
      "Planifier un QBR immédiatement — dernier QBR trop ancien",
    ],
    arr_at_risk_eur: 22608,
    days_to_act: 30,
    usage_risk_score: 30.0,
    support_risk_score: 0.0,
    financial_risk_score: 0.0,
    relationship_risk_score: 15.0,
    competitive_risk_score: 0.0,
  },
  {
    account_id: "acc_007",
    account_name: "EduTech Learn",
    arr_eur: 36000,
    churn_probability_pct: 21.8,
    churn_risk: "low",
    retention_action: "nurture",
    churn_drivers: [
      "Légère baisse d'usage (MAU -6%)",
    ],
    retention_signals: [
      "Forte adoption fonctionnelle (75%)",
      "Sponsor exécutif impliqué — relation stratégique solide",
      "Aucun ticket ouvert — client satisfait",
      "Historique de paiement parfait",
    ],
    risk_flags: [],
    recommended_actions: [
      "Planifier un Success Call pour comprendre le déclin d'usage",
      "Déclencher le processus de renouvellement anticipé",
    ],
    arr_at_risk_eur: 7848,
    days_to_act: 30,
    usage_risk_score: 10.0,
    support_risk_score: 0.0,
    financial_risk_score: 0.0,
    relationship_risk_score: 5.0,
    competitive_risk_score: 0.0,
  },
  {
    account_id: "acc_008",
    account_name: "HealthTech AG",
    arr_eur: 156000,
    churn_probability_pct: 11.3,
    churn_risk: "safe",
    retention_action: "expand",
    churn_drivers: [],
    retention_signals: [
      "Usage en hausse (+18% MAU)",
      "Forte adoption fonctionnelle (88%)",
      "Sponsor exécutif impliqué — relation stratégique solide",
      "NPS positif (62) — client satisfait",
      "NPS en amélioration",
      "Aucun ticket ouvert — client satisfait",
      "Historique de paiement parfait",
    ],
    risk_flags: [],
    recommended_actions: [],
    arr_at_risk_eur: 17628,
    days_to_act: 90,
    usage_risk_score: 0.0,
    support_risk_score: 0.0,
    financial_risk_score: 0.0,
    relationship_risk_score: 0.0,
    competitive_risk_score: 0.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk = searchParams.get("risk");
  const action = searchParams.get("action");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/churn-predictor`);
      if (risk) url.searchParams.set("risk", risk);
      if (action) url.searchParams.set("action", action);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (risk) accounts = accounts.filter((a) => a.churn_risk === risk);
  if (action) accounts = accounts.filter((a) => a.retention_action === action);

  const risk_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_prob = 0;
  let total_arr_at_risk = 0;

  for (const a of mockAccounts) {
    risk_counts[a.churn_risk] = (risk_counts[a.churn_risk] || 0) + 1;
    action_counts[a.retention_action] = (action_counts[a.retention_action] || 0) + 1;
    total_prob += a.churn_probability_pct;
    total_arr_at_risk += a.arr_at_risk_eur;
  }

  const n = mockAccounts.length;

  return sealResponse(NextResponse.json({
    accounts,
    summary: {
      total: n,
      risk_counts,
      action_counts,
      avg_churn_probability: Math.round((total_prob / n) * 10) / 10,
      total_arr_at_risk_eur: total_arr_at_risk,
      critical_count: risk_counts["critical"] ?? 0,
      emergency_count: action_counts["emergency"] ?? 0,
    },
  }));
}
