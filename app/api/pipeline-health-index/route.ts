import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockPipelines = [
  {
    pipeline_id: "ph_001",
    rep_id: "rep_001",
    rep_name: "Sophie Martin",
    region: "France",
    health_grade: "excellent",
    pipeline_risk: "low",
    health_action: "maintain",
    phi_score: 82.8,
    velocity_score: 88.0,
    quality_score: 79.2,
    coverage_score: 85.0,
    activity_score: 92.5,
    coverage_ratio: 3.2,
    stale_deal_pct: 8.3,
    remediation_plays: [
      "1 deal sans activité en 30j — revue immédiate pour relancer ou disqualifier",
      "2 deal(s) en contact unique — plan de multi-threading à lancer sous 7j",
    ],
    risk_signals: [],
    manager_alerts: [],
  },
  {
    pipeline_id: "ph_002",
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    region: "France",
    health_grade: "good",
    pipeline_risk: "moderate",
    health_action: "accelerate",
    phi_score: 62.3,
    velocity_score: 42.0,
    quality_score: 72.5,
    coverage_score: 70.0,
    activity_score: 78.0,
    coverage_ratio: 2.1,
    stale_deal_pct: 20.0,
    remediation_plays: [
      "Vélocité faible (âge moyen 68j vs benchmark 45j) — définir next steps impératifs sur tous les deals",
      "2 deal(s) sans activité en 30j — revue immédiate pour relancer ou disqualifier",
    ],
    risk_signals: [
      "3 deals sans sponsor exécutif — risque de blocage décisionnel",
    ],
    manager_alerts: [],
  },
  {
    pipeline_id: "ph_003",
    rep_id: "rep_003",
    rep_name: "Marie Lefevre",
    region: "DACH",
    health_grade: "good",
    pipeline_risk: "moderate",
    health_action: "improve_qual",
    phi_score: 60.1,
    velocity_score: 72.0,
    quality_score: 38.5,
    coverage_score: 85.0,
    activity_score: 68.0,
    coverage_ratio: 3.4,
    stale_deal_pct: 10.0,
    remediation_plays: [
      "Qualification insuffisante (45% BANT qualifiés) — session de coaching qualification avec manager",
      "1 deal(s) sans activité en 30j — revue immédiate pour relancer ou disqualifier",
    ],
    risk_signals: [
      "Précision du forecast faible (52%) — réviser les critères de qualification",
    ],
    manager_alerts: [],
  },
  {
    pipeline_id: "ph_004",
    rep_id: "rep_004",
    rep_name: "Thomas Bernard",
    region: "Iberia",
    health_grade: "fair",
    pipeline_risk: "high",
    health_action: "add_pipeline",
    phi_score: 44.5,
    velocity_score: 55.0,
    quality_score: 52.0,
    coverage_score: 28.0,
    activity_score: 58.0,
    coverage_ratio: 0.95,
    stale_deal_pct: 12.5,
    remediation_plays: [
      "Pipeline insuffisant (95,000€ vs quota 100,000€) — campagne de prospection intensive requise",
      "Activer les referrals clients et les campagnes inbound pour régénérer la pipeline",
      "1 deal(s) sans activité en 30j — revue immédiate pour relancer ou disqualifier",
    ],
    risk_signals: [
      "Pipeline sous le quota: 95,000€ vs 100,000€ — manque de 5,000€",
      "Précision du forecast faible (55%) — réviser les critères de qualification",
    ],
    manager_alerts: [
      "Pipeline sous-couvert: déficit de 5,000€ — assistance génération pipeline requise",
    ],
  },
  {
    pipeline_id: "ph_005",
    rep_id: "rep_005",
    rep_name: "Emma Rousseau",
    region: "France",
    health_grade: "fair",
    pipeline_risk: "high",
    health_action: "boost_activity",
    phi_score: 41.2,
    velocity_score: 58.0,
    quality_score: 55.0,
    coverage_score: 55.0,
    activity_score: 18.0,
    coverage_ratio: 1.6,
    stale_deal_pct: 25.0,
    remediation_plays: [
      "Activité faible (12 appels, 3 RDV) — fixer des objectifs journaliers avec le rep",
      "3 deal(s) sans activité en 30j — revue immédiate pour relancer ou disqualifier",
    ],
    risk_signals: [
      "3 deals sans activité récente — stagnation pipeline détectée",
    ],
    manager_alerts: [
      "Pipeline dégradé pour Emma Rousseau — planifier une revue pipeline complète cette semaine",
    ],
  },
  {
    pipeline_id: "ph_006",
    rep_id: "rep_006",
    rep_name: "Antoine Moreau",
    region: "Benelux",
    health_grade: "poor",
    pipeline_risk: "severe",
    health_action: "add_pipeline",
    phi_score: 28.5,
    velocity_score: 20.0,
    quality_score: 32.0,
    coverage_score: 18.0,
    activity_score: 48.0,
    coverage_ratio: 0.55,
    stale_deal_pct: 40.0,
    remediation_plays: [
      "Pipeline insuffisant (55,000€ vs quota 100,000€) — campagne de prospection intensive requise",
      "Activer les referrals clients et les campagnes inbound pour régénérer la pipeline",
      "4 deal(s) sans activité en 30j — revue immédiate pour relancer ou disqualifier",
      "3 deal(s) en contact unique — plan de multi-threading à lancer sous 7j",
    ],
    risk_signals: [
      "Pipeline sous le quota: 55,000€ vs 100,000€ — manque de 45,000€",
      "40% des deals dépassent la date de clôture prévue — forecast peu fiable",
      "4 deals sans activité récente — stagnation pipeline détectée",
      "Taux de victoire faible (18%) — efficacité de closing en baisse",
      "Précision du forecast faible (42%) — réviser les critères de qualification",
    ],
    manager_alerts: [
      "Pipeline dégradé pour Antoine Moreau — planifier une revue pipeline complète cette semaine",
      "Risque SÉVÈRE détecté — Antoine Moreau risque de manquer le quota de façon significative",
      "Pipeline sous-couvert: déficit de 45,000€ — assistance génération pipeline requise",
    ],
  },
  {
    pipeline_id: "ph_007",
    rep_id: "rep_007",
    rep_name: "Clara Petit",
    region: "DACH",
    health_grade: "critical",
    pipeline_risk: "severe",
    health_action: "add_pipeline",
    phi_score: 15.2,
    velocity_score: 8.0,
    quality_score: 18.0,
    coverage_score: 12.0,
    activity_score: 25.0,
    coverage_ratio: 0.3,
    stale_deal_pct: 66.7,
    remediation_plays: [
      "Pipeline insuffisant (30,000€ vs quota 100,000€) — campagne de prospection intensive requise",
      "Activer les referrals clients et les campagnes inbound pour régénérer la pipeline",
      "4 deal(s) sans activité en 30j — revue immédiate pour relancer ou disqualifier",
      "2 deal(s) en contact unique — plan de multi-threading à lancer sous 7j",
      "2 deal(s) dépassant la date de clôture prévue — revue du forecast obligatoire",
    ],
    risk_signals: [
      "Pipeline sous le quota: 30,000€ vs 100,000€ — manque de 70,000€",
      "67% des deals dépassent la date de clôture prévue — forecast peu fiable",
      "4 deals sans activité récente — stagnation pipeline détectée",
      "Taux de victoire faible (15%) — efficacité de closing en baisse",
      "Précision du forecast faible (35%) — réviser les critères de qualification",
    ],
    manager_alerts: [
      "⚠ Pipeline CRITIQUE pour Clara Petit (DACH) — intervention manager immédiate requise",
      "Risque SÉVÈRE détecté — Clara Petit risque de manquer le quota de façon significative",
      "Pipeline sous-couvert: déficit de 70,000€ — assistance génération pipeline requise",
    ],
  },
  {
    pipeline_id: "ph_008",
    rep_id: "rep_008",
    rep_name: "Julien Lambert",
    region: "Iberia",
    health_grade: "good",
    pipeline_risk: "low",
    health_action: "maintain",
    phi_score: 68.8,
    velocity_score: 75.0,
    quality_score: 68.0,
    coverage_score: 70.0,
    activity_score: 62.5,
    coverage_ratio: 2.2,
    stale_deal_pct: 0.0,
    remediation_plays: [
      "Maintenir les bonnes pratiques en place",
    ],
    risk_signals: [],
    manager_alerts: [],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const grade  = searchParams.get("grade");
  const risk   = searchParams.get("risk");
  const action = searchParams.get("action");
  const region = searchParams.get("region");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/pipeline-health-index`);
      if (grade)  url.searchParams.set("grade", grade);
      if (risk)   url.searchParams.set("risk", risk);
      if (action) url.searchParams.set("action", action);
      if (region) url.searchParams.set("region", region);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let pipelines = [...mockPipelines];
  if (grade)  pipelines = pipelines.filter((p) => p.health_grade === grade);
  if (risk)   pipelines = pipelines.filter((p) => p.pipeline_risk === risk);
  if (action) pipelines = pipelines.filter((p) => p.health_action === action);
  if (region) pipelines = pipelines.filter((p) => p.region === region);

  const grade_counts:  Record<string, number> = {};
  const risk_counts:   Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_phi = 0, total_vel = 0, total_qual = 0, total_cov = 0, total_act = 0;

  for (const p of mockPipelines) {
    grade_counts[p.health_grade]   = (grade_counts[p.health_grade] || 0) + 1;
    risk_counts[p.pipeline_risk]   = (risk_counts[p.pipeline_risk] || 0) + 1;
    action_counts[p.health_action] = (action_counts[p.health_action] || 0) + 1;
    total_phi  += p.phi_score;
    total_vel  += p.velocity_score;
    total_qual += p.quality_score;
    total_cov  += p.coverage_score;
    total_act  += p.activity_score;
  }

  const n = mockPipelines.length;

  return NextResponse.json({
    pipelines,
    summary: {
      total: n,
      grade_counts,
      risk_counts,
      action_counts,
      avg_phi_score:      Math.round((total_phi / n) * 10) / 10,
      avg_velocity_score: Math.round((total_vel / n) * 10) / 10,
      avg_quality_score:  Math.round((total_qual / n) * 10) / 10,
      avg_coverage_score: Math.round((total_cov / n) * 10) / 10,
      avg_activity_score: Math.round((total_act / n) * 10) / 10,
      critical_count:     mockPipelines.filter((p) => p.health_grade === "critical").length,
      severe_risk_count:  mockPipelines.filter((p) => p.pipeline_risk === "severe").length,
    },
  });
}
