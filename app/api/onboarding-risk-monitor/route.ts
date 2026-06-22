import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[onboarding-risk-monitor] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockCustomers = [
  {
    customer_id: "ob_001",
    customer_name: "CloudScale Technologies",
    arr_eur: 240000,
    segment: "enterprise",
    phase: "setup",
    risk_score: 72.0,
    risk_level: "critical",
    risk_action: "escalate",
    churn_signal: "strong",
    go_live_delay_days: 21,
    risk_factors: [
      "Go-live en retard de 21j sur la date contractuelle",
      "Sponsor exécutif inactif — manque d'alignement stratégique",
      "Formation insuffisante — 18% seulement complétée",
      "Adoption utilisateurs faible — 10% activés",
      "Aucun cas d'usage validé après 30j — Time-to-Value compromis",
      "3 blocages ouverts — progression bloquée",
      "2 ticket(s) escaladé(s) — problème produit critique",
    ],
    positive_signals: [],
    intervention_plan: [
      "Escalade C-level immédiate — mobiliser direction et executive sponsor",
      "War room onboarding — réunion quotidienne jusqu'à résolution",
      "Résoudre les blocages en priorité absolue — task force technique",
    ],
    time_to_value_score: 8.0,
  },
  {
    customer_id: "ob_002",
    customer_name: "DataVault Partners",
    arr_eur: 180000,
    segment: "enterprise",
    phase: "training",
    risk_score: 58.0,
    risk_level: "high",
    risk_action: "rescue",
    churn_signal: "moderate",
    go_live_delay_days: 14,
    risk_factors: [
      "Go-live en retard de 14j sur la date contractuelle",
      "Champion non engagé — risque de dérive du projet",
      "Formation insuffisante — 25% seulement complétée",
      "Adoption utilisateurs faible — 15% activés",
      "2 blocages ouverts — progression bloquée",
    ],
    positive_signals: [
      "Sponsor exécutif actif — engagement fort du côté client",
      "Kickoff réalisé — projet sur les rails",
    ],
    intervention_plan: [
      "Appel de rescue urgente — identifier les freins et rebloquer le projet",
      "Renforcer le champion interne — contacter nouvelles personas",
      "Définir un quickwin à 14j — démontrer la valeur rapidement",
    ],
    time_to_value_score: 15.0,
  },
  {
    customer_id: "ob_003",
    customer_name: "NexaRetail Group",
    arr_eur: 144000,
    segment: "enterprise",
    phase: "adoption",
    risk_score: 42.0,
    risk_level: "high",
    risk_action: "rescue",
    churn_signal: "moderate",
    go_live_delay_days: 7,
    risk_factors: [
      "Go-live en retard de 7j sur la date contractuelle",
      "Adoption utilisateurs faible — 30% activés",
      "Dernier contact CS il y a 16j — relation négligée",
    ],
    positive_signals: [
      "Sponsor exécutif actif — engagement fort du côté client",
      "Champion engagé — relai interne efficace",
      "Kickoff réalisé — projet sur les rails",
      "Health check effectué — risques identifiés et adressés",
    ],
    intervention_plan: [
      "Appel de rescue urgente — identifier les freins et rebloquer le projet",
      "Renforcer le champion interne — contacter nouvelles personas",
      "Définir un quickwin à 14j — démontrer la valeur rapidement",
    ],
    time_to_value_score: 32.0,
  },
  {
    customer_id: "ob_004",
    customer_name: "HealthBridge Systems",
    arr_eur: 96000,
    segment: "mid_market",
    phase: "training",
    risk_score: 35.0,
    risk_level: "moderate",
    risk_action: "accelerate",
    churn_signal: "early",
    go_live_delay_days: 0,
    risk_factors: [
      "Formation insuffisante — 40% seulement complétée",
      "Adoption utilisateurs faible — 20% activés",
    ],
    positive_signals: [
      "Sponsor exécutif actif — engagement fort du côté client",
      "Champion engagé — relai interne efficace",
      "Kickoff réalisé — projet sur les rails",
      "Aucun blocage ouvert — progression fluide",
    ],
    intervention_plan: [
      "Accélérer le plan de formation — sessions intensives à planifier",
      "Identifier les utilisateurs bloqués et les accompagner",
      "Réviser le planning avec le client — redéfinir les jalons",
    ],
    time_to_value_score: 25.0,
  },
  {
    customer_id: "ob_005",
    customer_name: "FinCore Solutions",
    arr_eur: 72000,
    segment: "mid_market",
    phase: "adoption",
    risk_score: 22.0,
    risk_level: "moderate",
    risk_action: "accelerate",
    churn_signal: "early",
    go_live_delay_days: 0,
    risk_factors: [
      "Formation insuffisante — 55% seulement complétée",
    ],
    positive_signals: [
      "Premier cas d'usage validé — Time-to-Value atteint",
      "Sponsor exécutif actif — engagement fort du côté client",
      "Champion engagé — relai interne efficace",
      "Kickoff réalisé — projet sur les rails",
      "Aucun blocage ouvert — progression fluide",
    ],
    intervention_plan: [
      "Accélérer le plan de formation — sessions intensives à planifier",
      "Identifier les utilisateurs bloqués et les accompagner",
      "Réviser le planning avec le client — redéfinir les jalons",
    ],
    time_to_value_score: 52.0,
  },
  {
    customer_id: "ob_006",
    customer_name: "LogiFlux GmbH",
    arr_eur: 60000,
    segment: "mid_market",
    phase: "value_realization",
    risk_score: 12.0,
    risk_level: "low",
    risk_action: "monitor",
    churn_signal: "none",
    go_live_delay_days: 0,
    risk_factors: [],
    positive_signals: [
      "Premier cas d'usage validé — Time-to-Value atteint",
      "Sponsor exécutif actif — engagement fort du côté client",
      "Champion engagé — relai interne efficace",
      "Formation avancée — 82% complétée",
      "Adoption solide — 65% des utilisateurs actifs",
      "Kickoff réalisé — projet sur les rails",
      "Health check effectué — risques identifiés et adressés",
      "Aucun blocage ouvert — progression fluide",
    ],
    intervention_plan: [
      "Maintenir la cadence de contact hebdomadaire",
      "Suivre les jalons du plan d'implémentation",
      "Préparer l'évaluation de satisfaction à J+90",
    ],
    time_to_value_score: 75.0,
  },
  {
    customer_id: "ob_007",
    customer_name: "EduSpark Ltd",
    arr_eur: 24000,
    segment: "smb",
    phase: "value_realization",
    risk_score: 5.0,
    risk_level: "low",
    risk_action: "monitor",
    churn_signal: "none",
    go_live_delay_days: 0,
    risk_factors: [],
    positive_signals: [
      "Premier cas d'usage validé — Time-to-Value atteint",
      "Sponsor exécutif actif — engagement fort du côté client",
      "Champion engagé — relai interne efficace",
      "Formation avancée — 95% complétée",
      "Adoption solide — 78% des utilisateurs actifs",
      "Kickoff réalisé — projet sur les rails",
      "Health check effectué — risques identifiés et adressés",
      "Aucun blocage ouvert — progression fluide",
      "Toutes les intégrations complétées (3/3)",
    ],
    intervention_plan: [
      "Maintenir la cadence de contact hebdomadaire",
      "Suivre les jalons du plan d'implémentation",
      "Préparer l'évaluation de satisfaction à J+90",
    ],
    time_to_value_score: 90.0,
  },
  {
    customer_id: "ob_008",
    customer_name: "PropLink AG",
    arr_eur: 12000,
    segment: "smb",
    phase: "kickoff",
    risk_score: 8.0,
    risk_level: "low",
    risk_action: "monitor",
    churn_signal: "none",
    go_live_delay_days: 0,
    risk_factors: [],
    positive_signals: [
      "Sponsor exécutif actif — engagement fort du côté client",
      "Champion engagé — relai interne efficace",
      "Kickoff réalisé — projet sur les rails",
      "Aucun blocage ouvert — progression fluide",
    ],
    intervention_plan: [
      "Maintenir la cadence de contact hebdomadaire",
      "Suivre les jalons du plan d'implémentation",
      "Préparer l'évaluation de satisfaction à J+90",
    ],
    time_to_value_score: 20.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk = searchParams.get("risk");
  const action = searchParams.get("action");
  const phase = searchParams.get("phase");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/onboarding-risk-monitor`);
      if (risk) url.searchParams.set("risk", risk);
      if (action) url.searchParams.set("action", action);
      if (phase) url.searchParams.set("phase", phase);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let customers = [...mockCustomers];
  if (risk) customers = customers.filter((c) => c.risk_level === risk);
  if (action) customers = customers.filter((c) => c.risk_action === action);
  if (phase) customers = customers.filter((c) => c.phase === phase);

  const risk_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const phase_counts: Record<string, number> = {};
  let total_score = 0;
  let total_ttv = 0;
  let arr_at_risk = 0;

  for (const c of mockCustomers) {
    risk_counts[c.risk_level] = (risk_counts[c.risk_level] || 0) + 1;
    action_counts[c.risk_action] = (action_counts[c.risk_action] || 0) + 1;
    phase_counts[c.phase] = (phase_counts[c.phase] || 0) + 1;
    total_score += c.risk_score;
    total_ttv += c.time_to_value_score;
    if (c.risk_level === "high" || c.risk_level === "critical") arr_at_risk += c.arr_eur;
  }

  const n = mockCustomers.length;

  return sealResponse(NextResponse.json({
    customers,
    summary: {
      total: n,
      risk_counts,
      action_counts,
      phase_counts,
      avg_risk_score: Math.round((total_score / n) * 10) / 10,
      avg_time_to_value: Math.round((total_ttv / n) * 10) / 10,
      critical_count: mockCustomers.filter((c) => c.risk_level === "critical").length,
      behind_schedule_count: mockCustomers.filter((c) => c.go_live_delay_days > 0).length,
      total_arr_at_risk_eur: arr_at_risk,
    },
  }));
}
