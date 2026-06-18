import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "ap_001",
    account_name: "Total Energies SE",
    rep_id: "rep_001",
    rep_name: "Sophie Martin",
    penetration_level: "deep",
    stakeholder_risk: "secure",
    committee_gap: "none",
    penetration_action: "maintain",
    penetration_score: 89.0,
    coverage_score: 97.0,
    relationship_score: 81.0,
    multithread_ratio: 0.8,
    expansion_plays: [
      "Maintenir le rythme d'engagement — 10 contacts mappés, 8 actifs",
    ],
    risk_signals: [],
    manager_alerts: [],
  },
  {
    account_id: "ap_002",
    account_name: "Capgemini France",
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    penetration_level: "solid",
    stakeholder_risk: "stable",
    committee_gap: "missing_finance",
    penetration_action: "expand_finance",
    penetration_score: 65.0,
    coverage_score: 72.0,
    relationship_score: 58.0,
    multithread_ratio: 0.67,
    expansion_plays: [
      "Aucun contact Finance/Achats engagé — impératif avant la phase contractuelle",
      "Seulement 4/6 contacts actifs en 30j — relancer les contacts dormants",
    ],
    risk_signals: [
      "Pas de contact Finance/Achats en phase de proposition/négociation — approbation budgétaire en risque",
    ],
    manager_alerts: [],
  },
  {
    account_id: "ap_003",
    account_name: "Sodexo Group",
    rep_id: "rep_001",
    rep_name: "Sophie Martin",
    penetration_level: "solid",
    stakeholder_risk: "stable",
    committee_gap: "missing_exec",
    penetration_action: "expand_exec",
    penetration_score: 58.0,
    coverage_score: 60.0,
    relationship_score: 56.0,
    multithread_ratio: 0.75,
    expansion_plays: [
      "Aucun contact C-level — demander une introduction via le champion existant pour un EBR",
    ],
    risk_signals: [
      "Aucun contact exécutif sur un deal de 95,000€ — risque de blocage décisionnel",
    ],
    manager_alerts: [],
  },
  {
    account_id: "ap_004",
    account_name: "Veolia Environnement",
    rep_id: "rep_003",
    rep_name: "Marie Lefevre",
    penetration_level: "partial",
    stakeholder_risk: "vulnerable",
    committee_gap: "multiple_gaps",
    penetration_action: "multithread_now",
    penetration_score: 38.0,
    coverage_score: 42.0,
    relationship_score: 34.0,
    multithread_ratio: 0.5,
    expansion_plays: [
      "Urgence multi-threading — identifier 3+ nouveaux contacts dans le comité d'achat sous 7 jours",
      "Demander au contact actuel de faire des introductions internes auprès des décideurs",
      "Aucun contact Finance/Achats engagé — impératif avant la phase contractuelle",
    ],
    risk_signals: [
      "1 détracteur(s) identifié(s) — risque de blocage interne",
      "Aucun contact exécutif sur un deal de 72,000€ — risque de blocage décisionnel",
    ],
    manager_alerts: [
      "Pénétration critique (partial) sur deal stratégique 72,000€ — escalade senior recommandée",
    ],
  },
  {
    account_id: "ap_005",
    account_name: "Boulanger SA",
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    penetration_level: "partial",
    stakeholder_risk: "stable",
    committee_gap: "missing_tech",
    penetration_action: "expand_tech",
    penetration_score: 45.0,
    coverage_score: 47.0,
    relationship_score: 43.0,
    multithread_ratio: 0.6,
    expansion_plays: [
      "Évaluateur technique non engagé — planifier une session technique avec l'IT",
    ],
    risk_signals: [],
    manager_alerts: [],
  },
  {
    account_id: "ap_006",
    account_name: "Picard Surgelés",
    rep_id: "rep_003",
    rep_name: "Marie Lefevre",
    penetration_level: "thin",
    stakeholder_risk: "critical",
    committee_gap: "multiple_gaps",
    penetration_action: "rebuild_champion",
    penetration_score: 28.0,
    coverage_score: 30.0,
    relationship_score: 26.0,
    multithread_ratio: 0.33,
    expansion_plays: [
      "Champion perdu — cartographier les promoteurs internes restants et en activer un nouveau",
      "Organiser un executive briefing pour rebâtir la relation au niveau stratégique",
      "Aucun contact C-level — demander une introduction via le champion existant pour un EBR",
    ],
    risk_signals: [
      "Champion principal a quitté ou changé de rôle — relation à reconstruire d'urgence",
      "2 détracteur(s) identifié(s) — risque de blocage interne",
    ],
    manager_alerts: [
      "Champion perdu chez Picard Surgelés — revue manager pour plan de récupération urgent",
      "2 détracteurs chez Picard Surgelés — risque de blocage interne, revue stratégique requise",
    ],
  },
  {
    account_id: "ap_007",
    account_name: "Allia Habitat",
    rep_id: "rep_004",
    rep_name: "Thomas Bernard",
    penetration_level: "single",
    stakeholder_risk: "vulnerable",
    committee_gap: "multiple_gaps",
    penetration_action: "multithread_now",
    penetration_score: 22.0,
    coverage_score: 14.0,
    relationship_score: 30.0,
    multithread_ratio: 1.0,
    expansion_plays: [
      "Urgence multi-threading — identifier 3+ nouveaux contacts dans le comité d'achat sous 7 jours",
      "Demander au contact actuel de faire des introductions internes auprès des décideurs",
    ],
    risk_signals: [
      "Contact unique — risque critique de single-point-of-failure",
    ],
    manager_alerts: [
      "⚠ Contact unique sur Allia Habitat (18,000€) — action multi-threading immédiate requise",
    ],
  },
  {
    account_id: "ap_008",
    account_name: "Sofitel Luxury Hotels",
    rep_id: "rep_004",
    rep_name: "Thomas Bernard",
    penetration_level: "deep",
    stakeholder_risk: "secure",
    committee_gap: "none",
    penetration_action: "maintain",
    penetration_score: 82.0,
    coverage_score: 85.0,
    relationship_score: 79.0,
    multithread_ratio: 0.9,
    expansion_plays: [
      "Maintenir le rythme d'engagement — 8 contacts mappés, 7 actifs",
    ],
    risk_signals: [],
    manager_alerts: [],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const level  = searchParams.get("level");
  const risk   = searchParams.get("risk");
  const action = searchParams.get("action");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/account-penetration`);
      if (level)  url.searchParams.set("level", level);
      if (risk)   url.searchParams.set("risk", risk);
      if (action) url.searchParams.set("action", action);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (level)  accounts = accounts.filter((a) => a.penetration_level === level);
  if (risk)   accounts = accounts.filter((a) => a.stakeholder_risk === risk);
  if (action) accounts = accounts.filter((a) => a.penetration_action === action);

  const level_counts:  Record<string, number> = {};
  const risk_counts:   Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_pen = 0, total_cov = 0, total_rel = 0;

  for (const a of mockAccounts) {
    level_counts[a.penetration_level]   = (level_counts[a.penetration_level] || 0) + 1;
    risk_counts[a.stakeholder_risk]     = (risk_counts[a.stakeholder_risk] || 0) + 1;
    action_counts[a.penetration_action] = (action_counts[a.penetration_action] || 0) + 1;
    total_pen += a.penetration_score;
    total_cov += a.coverage_score;
    total_rel += a.relationship_score;
  }

  const n = mockAccounts.length;

  return NextResponse.json({
    accounts,
    summary: {
      total: n,
      level_counts,
      risk_counts,
      action_counts,
      avg_penetration_score:  Math.round((total_pen / n) * 10) / 10,
      avg_coverage_score:     Math.round((total_cov / n) * 10) / 10,
      avg_relationship_score: Math.round((total_rel / n) * 10) / 10,
      single_threaded_count:  mockAccounts.filter((a) => a.penetration_level === "single").length,
      critical_risk_count:    mockAccounts.filter((a) => a.stakeholder_risk === "critical").length,
    },
  });
}
