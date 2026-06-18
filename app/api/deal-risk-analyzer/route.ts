import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockDeals = [
  {
    deal_id: "dr_001",
    account_name: "CloudScale Technologies",
    segment: "enterprise",
    arr_eur: 240000,
    stage: "negotiation",
    risk_score: 78.0,
    risk_level: "critical",
    deal_action: "escalate",
    stall_reasons: ["no_champion", "single_threaded", "budget_freeze", "competitor_threat"],
    risk_factors: [
      "Deal bloqué en negotiation depuis 25j — seuil critique dépassé",
      "Aucun champion interne identifié — deal vulnérable à tout changement d'interlocuteur",
      "Deal mono-thread — un seul interlocuteur actif, risque de blocage",
      "Budget non confirmé à moins de 60j de la close date — risque de report",
      "Concurrent actif sur le deal — risque de displacement",
    ],
    positive_signals: ["Prochaine étape définie — momentum maintenu"],
    intervention_plan: [
      "Escalade C-level — mobiliser le management pour débloquer le deal",
      "Identifier un champion interne en urgence — contacter 3 nouvelles personas",
      "QBR de récupération — ROI, roadmap, valeur démontrée en réunion urgente",
      "Proposer un POC rapide ou une période de test pour relancer l'engagement",
    ],
    forecast_adjustment_pct: -55.0,
  },
  {
    deal_id: "dr_002",
    account_name: "DataVault Partners",
    segment: "enterprise",
    arr_eur: 180000,
    stage: "closing",
    risk_score: 65.0,
    risk_level: "critical",
    deal_action: "escalate",
    stall_reasons: ["technical_blocker", "procurement_delay", "executive_misalignment"],
    risk_factors: [
      "Deal bloqué en closing depuis 18j — seuil critique dépassé",
      "Validation technique non complète — bloqueur produit non résolu",
      "Procurement engagé sans légal — risque de rallongement contractuel",
      "Sponsor exécutif non engagé sur deal > 50k€",
    ],
    positive_signals: [
      "Budget confirmé — deal qualifié côté financement",
      "Plan d'action mutuel en place — deal bien structuré",
      "Critères de décision alignés — processus d'évaluation transparent",
    ],
    intervention_plan: [
      "Escalade C-level — mobiliser le management pour débloquer le deal",
      "QBR de récupération — ROI, roadmap, valeur démontrée en réunion urgente",
      "Proposer un POC rapide ou une période de test pour relancer l'engagement",
    ],
    forecast_adjustment_pct: -40.0,
  },
  {
    deal_id: "dr_003",
    account_name: "NexaRetail Group",
    segment: "enterprise",
    arr_eur: 144000,
    stage: "proposal",
    risk_score: 52.0,
    risk_level: "high",
    deal_action: "intervene",
    stall_reasons: ["single_threaded", "competitor_threat", "scope_creep"],
    risk_factors: [
      "Progression lente en proposal (18j) — risque de stagnation",
      "Deal mono-thread — un seul interlocuteur actif",
      "Concurrent actif sur le deal — risque de displacement",
      "Scope du deal modifié — risque de re-qualification et de retard",
      "Pas de plan d'action mutuel — deal non structuré côté client",
    ],
    positive_signals: [
      "Sponsor exécutif engagé — décision facilitée",
      "Budget confirmé — deal qualifié côté financement",
      "Taux de réponse email élevé (78%) — engagement actif",
    ],
    intervention_plan: [
      "Élargir le mapping relationnel — identifier et engager 2 nouveaux stakeholders",
      "Établir un plan d'action mutuel — cadrer les prochaines étapes avec le client",
      "Préparer un battlecard concurrentiel — différenciation et arguments ROI",
      "Fixer une deadline de décision avec le client — créer l'urgence",
    ],
    forecast_adjustment_pct: -30.0,
  },
  {
    deal_id: "dr_004",
    account_name: "HealthBridge Systems",
    segment: "mid_market",
    arr_eur: 96000,
    stage: "qualification",
    risk_score: 48.0,
    risk_level: "high",
    deal_action: "intervene",
    stall_reasons: ["no_champion", "budget_freeze"],
    risk_factors: [
      "Progression lente en qualification (28j) — risque de stagnation",
      "Aucun champion interne identifié — deal vulnérable",
      "Budget non confirmé à moins de 60j de la close date",
      "Pas de contact depuis 10j — deal potentiellement dormant",
    ],
    positive_signals: [
      "Critères de décision alignés — processus d'évaluation transparent",
    ],
    intervention_plan: [
      "Élargir le mapping relationnel — identifier et engager 2 nouveaux stakeholders",
      "Qualifier le budget en priorité — appel finance ou sponsor pour confirmation",
      "Fixer une deadline de décision avec le client — créer l'urgence",
    ],
    forecast_adjustment_pct: -35.0,
  },
  {
    deal_id: "dr_005",
    account_name: "FinCore Solutions",
    segment: "mid_market",
    arr_eur: 72000,
    stage: "proposal",
    risk_score: 32.0,
    risk_level: "moderate",
    deal_action: "accelerate",
    stall_reasons: ["competitor_threat"],
    risk_factors: [
      "Concurrent actif sur le deal — risque de displacement",
      "Dernière réunion sans prochaine étape définie — momentum perdu",
    ],
    positive_signals: [
      "Champion fort (8/10) — défenseur interne actif",
      "3 parties prenantes actives — alignment multi-thread",
      "Budget confirmé — deal qualifié côté financement",
      "Critères de décision alignés — processus d'évaluation transparent",
    ],
    intervention_plan: [
      "Accélérer la prochaine étape — réduire le cycle de décision",
      "Renforcer les preuves de valeur — étude de cas, démonstration ciblée",
      "Préparer la proposition commerciale finale",
      "Engager le sponsor exécutif pour validation finale",
    ],
    forecast_adjustment_pct: -20.0,
  },
  {
    deal_id: "dr_006",
    account_name: "LogiFlux GmbH",
    segment: "mid_market",
    arr_eur: 60000,
    stage: "negotiation",
    risk_score: 28.0,
    risk_level: "moderate",
    deal_action: "accelerate",
    stall_reasons: [],
    risk_factors: [
      "Pas de plan d'action mutuel — deal non structuré côté client",
    ],
    positive_signals: [
      "Champion fort (9/10) — défenseur interne actif",
      "4 parties prenantes engagées — base de support large",
      "Sponsor exécutif engagé — décision facilitée",
      "Budget confirmé — deal qualifié côté financement",
      "Validation technique complète — risque produit éliminé",
      "Taux de réponse email élevé (85%) — engagement actif",
    ],
    intervention_plan: [
      "Accélérer la prochaine étape — réduire le cycle de décision",
      "Renforcer les preuves de valeur — étude de cas, démonstration ciblée",
      "Préparer la proposition commerciale finale",
      "Engager le sponsor exécutif pour validation finale",
    ],
    forecast_adjustment_pct: -5.0,
  },
  {
    deal_id: "dr_007",
    account_name: "EduSpark Ltd",
    segment: "smb",
    arr_eur: 24000,
    stage: "discovery",
    risk_score: 15.0,
    risk_level: "low",
    deal_action: "monitor",
    stall_reasons: [],
    risk_factors: [],
    positive_signals: [
      "Champion fort (7/10) — défenseur interne actif",
      "Plan d'action mutuel en place — deal bien structuré",
      "Prochaine étape définie — momentum maintenu",
      "Taux de réponse email élevé (80%) — engagement actif",
    ],
    intervention_plan: [
      "Maintenir le cadence de contact hebdomadaire",
      "Tracker les jalons du plan d'action mutuel",
      "Mettre à jour le CRM après chaque interaction",
    ],
    forecast_adjustment_pct: 0.0,
  },
  {
    deal_id: "dr_008",
    account_name: "PropLink AG",
    segment: "smb",
    arr_eur: 12000,
    stage: "closing",
    risk_score: 10.0,
    risk_level: "low",
    deal_action: "monitor",
    stall_reasons: [],
    risk_factors: [],
    positive_signals: [
      "Champion fort (8/10) — défenseur interne actif",
      "4 parties prenantes engagées — base de support large",
      "Sponsor exécutif engagé — décision facilitée",
      "Plan d'action mutuel en place — deal bien structuré",
      "Équipe légale engagée — progression vers la signature",
      "Validation technique complète — risque produit éliminé",
      "Budget confirmé — deal qualifié côté financement",
      "Critères de décision alignés — processus d'évaluation transparent",
      "Prochaine étape définie — momentum maintenu",
    ],
    intervention_plan: [
      "Maintenir le cadence de contact hebdomadaire",
      "Tracker les jalons du plan d'action mutuel",
      "Mettre à jour le CRM après chaque interaction",
    ],
    forecast_adjustment_pct: 0.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const risk = searchParams.get("risk");
  const action = searchParams.get("action");
  const stage = searchParams.get("stage");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/deal-risk-analyzer`);
      if (risk) url.searchParams.set("risk", risk);
      if (action) url.searchParams.set("action", action);
      if (stage) url.searchParams.set("stage", stage);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let deals = [...mockDeals];
  if (risk) deals = deals.filter((d) => d.risk_level === risk);
  if (action) deals = deals.filter((d) => d.deal_action === action);
  if (stage) deals = deals.filter((d) => d.stage === stage);

  const risk_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  const stage_counts: Record<string, number> = {};
  const stall_counts: Record<string, number> = {};
  let total_score = 0;
  let arr_at_risk = 0;

  for (const d of mockDeals) {
    risk_counts[d.risk_level] = (risk_counts[d.risk_level] || 0) + 1;
    action_counts[d.deal_action] = (action_counts[d.deal_action] || 0) + 1;
    stage_counts[d.stage] = (stage_counts[d.stage] || 0) + 1;
    for (const s of d.stall_reasons) {
      stall_counts[s] = (stall_counts[s] || 0) + 1;
    }
    total_score += d.risk_score;
    if (d.risk_level === "high" || d.risk_level === "critical") arr_at_risk += d.arr_eur;
  }

  const n = mockDeals.length;

  return NextResponse.json({
    deals,
    summary: {
      total: n,
      risk_counts,
      action_counts,
      stage_counts,
      top_stall_reasons: stall_counts,
      avg_risk_score: Math.round((total_score / n) * 10) / 10,
      critical_count: mockDeals.filter((d) => d.risk_level === "critical").length,
      escalation_count: mockDeals.filter((d) => d.deal_action === "escalate").length,
      total_arr_at_risk_eur: arr_at_risk,
    },
  });
}
