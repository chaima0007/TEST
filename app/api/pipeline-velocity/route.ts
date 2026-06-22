import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[pipeline-velocity] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "vel_001",
    deal_name: "NexaCloud Platform — Expansion",
    account_name: "NexaCloud Enterprise",
    segment: "enterprise",
    arr_eur: 240000,
    stage: "closing",
    velocity_status: "fast",
    velocity_action: "close_now",
    velocity_score: 91.5,
    stage_pace_score: 100.0,
    activity_score: 100.0,
    probability_score: 85.0,
    velocity_eur_per_day: 5100.0,
    schedule_delta_pct: 28.0,
    days_in_current_stage: 3,
    stage_benchmark_days: 7,
    stage_overdue: false,
    win_probability_pct: 85,
    last_activity_days: 1,
    has_next_step_scheduled: true,
    champion_present: true,
    decision_maker_engaged: true,
    risk_flags: [],
    momentum_signals: [
      "Probabilité de gain élevée (85%)",
      "Champion actif côté client — bonne adhésion interne",
      "Décideur engagé — raccourcit le cycle de décision",
      "Prochaine étape planifiée — momentum maintenu",
      "Activité récente — deal vivant et engagé",
      "Progression linéaire — aucune régression",
      "En avance de 28% sur le cycle de vente prévu",
      "Deal en phase de closing — proche de la signature",
    ],
    recommended_actions: [
      "Finaliser les termes contractuels et accélérer la signature",
    ],
  },
  {
    deal_id: "vel_002",
    deal_name: "FinEdge — Suite Enterprise",
    account_name: "FinEdge Solutions",
    segment: "enterprise",
    arr_eur: 180000,
    stage: "negotiation",
    velocity_status: "fast",
    velocity_action: "monitor",
    velocity_score: 78.0,
    stage_pace_score: 85.0,
    activity_score: 90.0,
    probability_score: 70.0,
    velocity_eur_per_day: 2916.67,
    schedule_delta_pct: 15.0,
    days_in_current_stage: 8,
    stage_benchmark_days: 14,
    stage_overdue: false,
    win_probability_pct: 70,
    last_activity_days: 2,
    has_next_step_scheduled: true,
    champion_present: true,
    decision_maker_engaged: true,
    risk_flags: [],
    momentum_signals: [
      "Probabilité de gain élevée (70%)",
      "Champion actif côté client — bonne adhésion interne",
      "Décideur engagé — raccourcit le cycle de décision",
      "Prochaine étape planifiée — momentum maintenu",
      "Activité récente — deal vivant et engagé",
      "Progression linéaire — aucune régression",
      "En avance de 15% sur le cycle de vente prévu",
    ],
    recommended_actions: [],
  },
  {
    deal_id: "vel_003",
    deal_name: "RetailPro — Analytics Module",
    account_name: "RetailPro International",
    segment: "mid_market",
    arr_eur: 96000,
    stage: "proposal",
    velocity_status: "on_pace",
    velocity_action: "monitor",
    velocity_score: 62.5,
    stage_pace_score: 75.0,
    activity_score: 65.0,
    probability_score: 55.0,
    velocity_eur_per_day: 1466.67,
    schedule_delta_pct: 5.0,
    days_in_current_stage: 12,
    stage_benchmark_days: 21,
    stage_overdue: false,
    win_probability_pct: 55,
    last_activity_days: 4,
    has_next_step_scheduled: true,
    champion_present: true,
    decision_maker_engaged: false,
    risk_flags: [],
    momentum_signals: [
      "Champion actif côté client — bonne adhésion interne",
      "Prochaine étape planifiée — momentum maintenu",
      "Progression linéaire — aucune régression",
    ],
    recommended_actions: [
      "Engager le décideur — critique en phase avancée",
    ],
  },
  {
    deal_id: "vel_004",
    deal_name: "ManuGroup — Opérations Suite",
    account_name: "ManuGroup France",
    segment: "mid_market",
    arr_eur: 72000,
    stage: "demo",
    velocity_status: "on_pace",
    velocity_action: "accelerate",
    velocity_score: 51.0,
    stage_pace_score: 70.0,
    activity_score: 50.0,
    probability_score: 40.0,
    velocity_eur_per_day: 720.0,
    schedule_delta_pct: -8.0,
    days_in_current_stage: 10,
    stage_benchmark_days: 14,
    stage_overdue: false,
    win_probability_pct: 40,
    last_activity_days: 5,
    has_next_step_scheduled: false,
    champion_present: true,
    decision_maker_engaged: false,
    risk_flags: [
      "Pas de prochaine étape planifiée",
    ],
    momentum_signals: [
      "Champion actif côté client — bonne adhésion interne",
      "Progression linéaire — aucune régression",
    ],
    recommended_actions: [
      "Planifier la prochaine étape immédiatement",
    ],
  },
  {
    deal_id: "vel_005",
    deal_name: "HealthCo — Compliance Platform",
    account_name: "HealthCo Belgium",
    segment: "smb",
    arr_eur: 48000,
    stage: "qualification",
    velocity_status: "slow",
    velocity_action: "accelerate",
    velocity_score: 38.0,
    stage_pace_score: 35.0,
    activity_score: 35.0,
    probability_score: 30.0,
    velocity_eur_per_day: 214.29,
    schedule_delta_pct: -18.0,
    days_in_current_stage: 22,
    stage_benchmark_days: 14,
    stage_overdue: true,
    win_probability_pct: 30,
    last_activity_days: 9,
    has_next_step_scheduled: true,
    champion_present: false,
    decision_maker_engaged: false,
    risk_flags: [
      "En stage 'qualification' depuis 22j (benchmark: 14j)",
      "Faible activité — 9j sans contact",
      "Pas de champion identifié côté client",
    ],
    momentum_signals: [
      "Prochaine étape planifiée — momentum maintenu",
    ],
    recommended_actions: [
      "Reprendre contact — 9j sans interaction",
      "Identifier et activer un champion interne",
      "Accélérer la sortie du stage 'qualification' (dépassé de 8j)",
    ],
  },
  {
    deal_id: "vel_006",
    deal_name: "EduTech — Learning Management",
    account_name: "EduTech Learn GmbH",
    segment: "smb",
    arr_eur: 36000,
    stage: "proposal",
    velocity_status: "slow",
    velocity_action: "rescue",
    velocity_score: 28.5,
    stage_pace_score: 20.0,
    activity_score: 40.0,
    probability_score: 35.0,
    velocity_eur_per_day: 291.67,
    schedule_delta_pct: -22.0,
    days_in_current_stage: 32,
    stage_benchmark_days: 21,
    stage_overdue: true,
    win_probability_pct: 35,
    last_activity_days: 6,
    has_next_step_scheduled: true,
    champion_present: false,
    decision_maker_engaged: false,
    risk_flags: [
      "En stage 'proposal' depuis 32j (benchmark: 21j)",
      "2 bloqueur(s) actif(s) dans le deal",
      "Pas de champion identifié côté client",
      "En retard de 22% sur le cycle prévu",
    ],
    momentum_signals: [
      "Prochaine étape planifiée — momentum maintenu",
    ],
    recommended_actions: [
      "Résoudre les 2 bloqueur(s) avant d'avancer",
      "Identifier et activer un champion interne",
      "Engager le décideur — critique en phase avancée",
      "Accélérer la sortie du stage 'proposal' (dépassé de 11j)",
    ],
  },
  {
    deal_id: "vel_007",
    deal_name: "PropTech — Portfolio Tool",
    account_name: "PropTech Venture",
    segment: "smb",
    arr_eur: 24000,
    stage: "demo",
    velocity_status: "stalled",
    velocity_action: "rescue",
    velocity_score: 12.0,
    stage_pace_score: 0.0,
    activity_score: 10.0,
    probability_score: 20.0,
    velocity_eur_per_day: 96.0,
    schedule_delta_pct: -35.0,
    days_in_current_stage: 38,
    stage_benchmark_days: 14,
    stage_overdue: true,
    win_probability_pct: 20,
    last_activity_days: 18,
    has_next_step_scheduled: false,
    champion_present: false,
    decision_maker_engaged: false,
    risk_flags: [
      "En stage 'demo' depuis 38j (benchmark: 14j)",
      "Deal revenu en arrière 2x — instabilité du cycle",
      "1 bloqueur(s) actif(s) dans le deal",
      "Aucune activité depuis 18j — deal en danger",
      "Pas de prochaine étape planifiée",
      "Pas de champion identifié côté client",
      "En retard de 35% sur le cycle prévu",
    ],
    momentum_signals: [],
    recommended_actions: [
      "Résoudre les 1 bloqueur(s) avant d'avancer",
      "Planifier la prochaine étape immédiatement",
      "Reprendre contact — 18j sans interaction",
      "Analyser les causes de régression et requalifier",
      "Identifier et activer un champion interne",
      "Évaluer si le deal doit être mis en pause ou abandonné",
      "Accélérer la sortie du stage 'demo' (dépassé de 24j)",
    ],
  },
  {
    deal_id: "vel_008",
    deal_name: "LogiChain — Supply Analytics",
    account_name: "LogiChain Systems",
    segment: "enterprise",
    arr_eur: 0,
    stage: "prospecting",
    velocity_status: "stalled",
    velocity_action: "rescue",
    velocity_score: 5.0,
    stage_pace_score: 0.0,
    activity_score: 0.0,
    probability_score: 10.0,
    velocity_eur_per_day: 0.0,
    schedule_delta_pct: -40.0,
    days_in_current_stage: 28,
    stage_benchmark_days: 7,
    stage_overdue: true,
    win_probability_pct: 10,
    last_activity_days: 21,
    has_next_step_scheduled: false,
    champion_present: false,
    decision_maker_engaged: false,
    risk_flags: [
      "En stage 'prospecting' depuis 28j (benchmark: 7j)",
      "Deal revenu en arrière 3x — instabilité du cycle",
      "2 bloqueur(s) actif(s) dans le deal",
      "Aucune activité depuis 21j — deal en danger",
      "Pas de prochaine étape planifiée",
      "Pas de champion identifié côté client",
      "Probabilité de gain faible (10%)",
      "En retard de 40% sur le cycle prévu",
    ],
    momentum_signals: [],
    recommended_actions: [
      "Résoudre les 2 bloqueur(s) avant d'avancer",
      "Planifier la prochaine étape immédiatement",
      "Reprendre contact — 21j sans interaction",
      "Analyser les causes de régression et requalifier",
      "Identifier et activer un champion interne",
      "Évaluer si le deal doit être mis en pause ou abandonné",
      "Accélérer la sortie du stage 'prospecting' (dépassé de 21j)",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const status = searchParams.get("status");
  const action = searchParams.get("action");
  const segment = searchParams.get("segment");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/pipeline-velocity`);
      if (status) url.searchParams.set("status", status);
      if (action) url.searchParams.set("action", action);
      if (segment) url.searchParams.set("segment", segment);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let deals = [...mockDeals];
  if (status) deals = deals.filter((d) => d.velocity_status === status);
  if (action) deals = deals.filter((d) => d.velocity_action === action);
  if (segment) deals = deals.filter((d) => d.segment === segment);

  const status_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_velocity = 0;
  let total_pipeline = 0;
  let total_weighted = 0;
  let total_score = 0;
  let stalled_count = 0;
  let rescue_count = 0;
  let close_now_count = 0;

  for (const d of mockDeals) {
    status_counts[d.velocity_status] = (status_counts[d.velocity_status] || 0) + 1;
    action_counts[d.velocity_action] = (action_counts[d.velocity_action] || 0) + 1;
    total_velocity += d.velocity_eur_per_day;
    total_pipeline += d.arr_eur;
    total_weighted += d.arr_eur * d.win_probability_pct / 100;
    total_score += d.velocity_score;
    if (d.velocity_status === "stalled") stalled_count++;
    if (d.velocity_action === "rescue") rescue_count++;
    if (d.velocity_action === "close_now") close_now_count++;
  }

  const n = mockDeals.length;

  return sealResponse(NextResponse.json({
    deals,
    summary: {
      total: n,
      status_counts,
      action_counts,
      avg_velocity_score: Math.round((total_score / n) * 10) / 10,
      total_velocity_eur_per_day: Math.round(total_velocity * 100) / 100,
      total_pipeline_eur: total_pipeline,
      total_weighted_pipeline_eur: Math.round(total_weighted * 100) / 100,
      stalled_count,
      rescue_count,
      close_now_count,
    },
  }));
}
