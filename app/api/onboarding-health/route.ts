import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "onb_001",
    account_name: "NexaCloud Enterprise",
    arr_eur: 180000,
    onboarding_status: "on_track",
    onboarding_action: "monitor",
    overall_score: 84.5,
    milestone_score: 88.0,
    engagement_score: 90.0,
    health_score: 80.0,
    completion_pct: 88.0,
    days_remaining: 18,
    schedule_delta_pct: 12.0,
    go_live_done: false,
    blockers: [],
    achievements: [
      "Kickoff effectué — onboarding lancé",
      "Configuration technique quasi-complète (92%)",
      "Migration données quasi-complète (95%)",
      "En avance de 12% sur le planning — bon rythme!",
      "Sponsor exécutif client actif — bon alignement stratégique",
      "CSM dédié assigné — accompagnement personnalisé",
    ],
    recommended_actions: [
      "Intensifier le rythme — go-live dans 18j",
    ],
  },
  {
    account_id: "onb_002",
    account_name: "FinEdge Solutions",
    arr_eur: 96000,
    onboarding_status: "on_track",
    onboarding_action: "celebrate",
    overall_score: 97.0,
    milestone_score: 100.0,
    engagement_score: 95.0,
    health_score: 100.0,
    completion_pct: 100.0,
    days_remaining: 5,
    schedule_delta_pct: 8.0,
    go_live_done: true,
    blockers: [],
    achievements: [
      "Go-live complété — onboarding réussi!",
      "Kickoff effectué — onboarding lancé",
      "Configuration technique quasi-complète (100%)",
      "Migration données quasi-complète (100%)",
      "Formation utilisateurs avancée (100%)",
      "En avance de 8% sur le planning — bon rythme!",
      "NPS onboarding positif (52)",
      "CSM dédié assigné — accompagnement personnalisé",
    ],
    recommended_actions: [
      "Planifier la revue post-onboarding et passation au CSM",
    ],
  },
  {
    account_id: "onb_003",
    account_name: "RetailPro International",
    arr_eur: 144000,
    onboarding_status: "at_risk",
    onboarding_action: "accelerate",
    overall_score: 58.2,
    milestone_score: 56.0,
    engagement_score: 65.0,
    health_score: 70.0,
    completion_pct: 56.0,
    days_remaining: 21,
    schedule_delta_pct: -18.0,
    go_live_done: false,
    blockers: [
      "2 bloqueurs d'intégration actifs",
      "Retard de 18% sur le planning prévu",
    ],
    achievements: [
      "Kickoff effectué — onboarding lancé",
      "CSM dédié assigné — accompagnement personnalisé",
    ],
    recommended_actions: [
      "Résoudre en urgence les 2 bloqueur(s) d'intégration",
      "Reprendre contact — 8j sans interaction",
      "Activer le sponsor exécutif pour débloquer les ressources",
    ],
  },
  {
    account_id: "onb_004",
    account_name: "ManuGroup France",
    arr_eur: 120000,
    onboarding_status: "at_risk",
    onboarding_action: "accelerate",
    overall_score: 52.7,
    milestone_score: 48.0,
    engagement_score: 60.0,
    health_score: 72.0,
    completion_pct: 48.0,
    days_remaining: 35,
    schedule_delta_pct: -22.0,
    go_live_done: false,
    blockers: [
      "Configuration technique à 35% après 28j",
      "Migration données à 42% après 28j",
      "Retard de 22% sur le planning prévu",
    ],
    achievements: [
      "Kickoff effectué — onboarding lancé",
      "Sponsor exécutif client actif — bon alignement stratégique",
    ],
    recommended_actions: [
      "Escalader la configuration technique — appel avec l'équipe d'implémentation",
      "Lancer la migration des données — ressources à débloquer",
      "Demander la désignation d'un PM côté client",
    ],
  },
  {
    account_id: "onb_005",
    account_name: "HealthCo Belgium",
    arr_eur: 72000,
    onboarding_status: "delayed",
    onboarding_action: "accelerate",
    overall_score: 38.4,
    milestone_score: 32.0,
    engagement_score: 55.0,
    health_score: 50.0,
    completion_pct: 32.0,
    days_remaining: 14,
    schedule_delta_pct: -38.0,
    go_live_done: false,
    blockers: [
      "3 bloqueurs d'intégration actifs",
      "Configuration technique à 28% après 42j",
      "Migration données à 35% après 42j",
      "Retard de 38% sur le planning prévu",
      "Aucun contact depuis 16j",
    ],
    achievements: [
      "Kickoff effectué — onboarding lancé",
    ],
    recommended_actions: [
      "Résoudre en urgence les 3 bloqueur(s) d'intégration",
      "Escalader la configuration technique — appel avec l'équipe d'implémentation",
      "Lancer la migration des données — ressources à débloquer",
      "Reprendre contact — 16j sans interaction",
      "Intensifier le rythme — go-live dans 14j",
    ],
  },
  {
    account_id: "onb_006",
    account_name: "EduTech Learn GmbH",
    arr_eur: 48000,
    onboarding_status: "delayed",
    onboarding_action: "accelerate",
    overall_score: 31.8,
    milestone_score: 28.0,
    engagement_score: 40.0,
    health_score: 45.0,
    completion_pct: 28.0,
    days_remaining: -12,
    schedule_delta_pct: -42.0,
    go_live_done: false,
    blockers: [
      "2 bloqueurs d'intégration actifs",
      "Configuration technique à 20% après 67j",
      "Retard de 42% sur le planning prévu",
      "Go-live en retard de 12j sur la date cible",
      "Aucun chef de projet côté client désigné",
    ],
    achievements: [
      "Kickoff effectué — onboarding lancé",
    ],
    recommended_actions: [
      "Résoudre en urgence les 2 bloqueur(s) d'intégration",
      "Escalader la configuration technique — appel avec l'équipe d'implémentation",
      "Demander la désignation d'un PM côté client",
      "Activer le sponsor exécutif pour débloquer les ressources",
    ],
  },
  {
    account_id: "onb_007",
    account_name: "PropTech Venture",
    arr_eur: 36000,
    onboarding_status: "critical",
    onboarding_action: "rescue",
    overall_score: 18.5,
    milestone_score: 10.0,
    engagement_score: 35.0,
    health_score: 32.0,
    completion_pct: 10.0,
    days_remaining: 28,
    schedule_delta_pct: -55.0,
    go_live_done: false,
    blockers: [
      "4 bloqueurs d'intégration actifs",
      "Kickoff non effectué — onboarding non démarré",
      "Configuration technique à 5% après 37j",
      "Migration données à 0% après 37j",
      "Retard de 55% sur le planning prévu",
      "Aucun chef de projet côté client désigné",
      "Aucun contact depuis 22j",
    ],
    achievements: [],
    recommended_actions: [
      "Résoudre en urgence les 4 bloqueur(s) d'intégration",
      "Planifier le kickoff immédiatement",
      "Escalader la configuration technique — appel avec l'équipe d'implémentation",
      "Lancer la migration des données — ressources à débloquer",
      "Demander la désignation d'un PM côté client",
      "Activer le sponsor exécutif pour débloquer les ressources",
      "Reprendre contact — 22j sans interaction",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const status = searchParams.get("status");
  const action = searchParams.get("action");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/onboarding-health`);
      if (status) url.searchParams.set("status", status);
      if (action) url.searchParams.set("action", action);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (status) accounts = accounts.filter((a) => a.onboarding_status === status);
  if (action) accounts = accounts.filter((a) => a.onboarding_action === action);

  const status_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_score = 0;
  let total_completion = 0;
  let critical_count = 0;
  let overdue_count = 0;
  let completed_count = 0;
  let arr_at_risk = 0;

  for (const a of mockAccounts) {
    status_counts[a.onboarding_status] = (status_counts[a.onboarding_status] || 0) + 1;
    action_counts[a.onboarding_action] = (action_counts[a.onboarding_action] || 0) + 1;
    total_score += a.overall_score;
    total_completion += a.completion_pct;
    if (a.onboarding_status === "critical") critical_count++;
    if (a.days_remaining < 0 && !a.go_live_done) overdue_count++;
    if (a.go_live_done) completed_count++;
    if (a.onboarding_status === "critical" || a.onboarding_status === "at_risk") {
      arr_at_risk += a.arr_eur;
    }
  }

  const n = mockAccounts.length;

  return NextResponse.json({
    accounts,
    summary: {
      total: n,
      status_counts,
      action_counts,
      avg_completion_pct: Math.round((total_completion / n) * 10) / 10,
      avg_overall_score: Math.round((total_score / n) * 10) / 10,
      critical_count,
      overdue_count,
      completed_count,
      total_arr_at_risk_eur: arr_at_risk,
    },
  });
}
