import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockAccounts = [
  {
    account_id: "cs_001",
    account_name: "NexaCloud Enterprise",
    segment: "enterprise",
    arr_eur: 240000,
    lifecycle_stage: "mature",
    risk_level: "low",
    playbook_motion: "expand",
    overall_health_score: 88.5,
    renewal_urgency: "medium",
    expansion_readiness: "ready",
    key_risks: [],
    immediate_actions: [
      "Préparer une proposition d'expansion — licences, modules ou tier supérieur",
      "Qualifier l'opportunité d'expansion avec le champion et le décideur budget",
      "Impliquer le sponsor exécutif dans la conversation d'expansion",
      "Planifier un QBR axé croissance — présenter les ROI atteints et les next steps",
    ],
    playbook_steps: [
      "S1 : QBR de valeur — quantifier le ROI réalisé, ouvrir la discussion croissance",
      "S2 : Qualification expansion — identifier les nouveaux cas d'usage ou équipes",
      "S3 : Proposition commerciale — licences / modules / tier supérieur",
      "S4 : Présentation exécutive — ROI + business case expansion",
      "S5 : Négociation et signature — co-construire le plan de déploiement",
      "S6 : Kick-off expansion — reproduire le succès sur le nouveau périmètre",
    ],
    success_metrics: [
      "Proposition d'expansion envoyée sous 14 jours",
      "Expansion signée ≥ 15% de l'ARR actuel",
      "NPS ≥ 40 maintenu post-expansion",
      "Nouveau périmètre en production sous 60 jours",
    ],
  },
  {
    account_id: "cs_002",
    account_name: "FinEdge Solutions",
    segment: "enterprise",
    arr_eur: 180000,
    lifecycle_stage: "growth",
    risk_level: "low",
    playbook_motion: "expand",
    overall_health_score: 79.0,
    renewal_urgency: "low",
    expansion_readiness: "ready",
    key_risks: [],
    immediate_actions: [
      "Préparer une proposition d'expansion — licences, modules ou tier supérieur",
      "Qualifier l'opportunité d'expansion avec le champion et le décideur budget",
      "Planifier un QBR axé croissance — présenter les ROI atteints et les next steps",
    ],
    playbook_steps: [
      "S1 : QBR de valeur — quantifier le ROI réalisé, ouvrir la discussion croissance",
      "S2 : Qualification expansion — identifier les nouveaux cas d'usage ou équipes",
      "S3 : Proposition commerciale — licences / modules / tier supérieur",
      "S4 : Présentation exécutive — ROI + business case expansion",
      "S5 : Négociation et signature — co-construire le plan de déploiement",
      "S6 : Kick-off expansion — reproduire le succès sur le nouveau périmètre",
    ],
    success_metrics: [
      "Proposition d'expansion envoyée sous 14 jours",
      "Expansion signée ≥ 15% de l'ARR actuel",
      "NPS ≥ 40 maintenu post-expansion",
      "Nouveau périmètre en production sous 60 jours",
    ],
  },
  {
    account_id: "cs_003",
    account_name: "RetailPro International",
    segment: "mid_market",
    arr_eur: 144000,
    lifecycle_stage: "mature",
    risk_level: "medium",
    playbook_motion: "accelerate",
    overall_health_score: 63.5,
    renewal_urgency: "high",
    expansion_readiness: "building",
    key_risks: [
      "DAU/MAU à 18% — usage irrégulier, valeur non perçue",
    ],
    immediate_actions: [
      "Session d'activation fonctionnelle — couvrir les 55% de features non utilisées",
      "Organiser un atelier 'best practices' avec les utilisateurs clés",
      "Partager des cas d'usage clients similaires pour inspirer l'adoption",
      "Séquence de renouvellement urgente — 85j avant expiration",
    ],
    playbook_steps: [
      "S1 : Audit d'adoption — cartographier les features non utilisées",
      "S2 : Atelier d'activation — session pratique avec utilisateurs finaux",
      "S3 : Partage de best practices — cas d'usage sectoriels similaires",
      "S4 : Suivi hebdomadaire des métriques d'usage pendant 30j",
      "S5 : QBR d'adoption — présenter la progression et fixer les objectifs",
    ],
    success_metrics: [
      "Features adoptées ≥ 70% sous 60 jours",
      "DAU/MAU ratio ≥ 0.25 sous 45 jours",
      "Score d'adoption ≥ 70 au prochain QBR",
      "Création de 2+ cas d'usage additionnels documentés",
    ],
  },
  {
    account_id: "cs_004",
    account_name: "ManuGroup France",
    segment: "enterprise",
    arr_eur: 120000,
    lifecycle_stage: "growth",
    risk_level: "medium",
    playbook_motion: "retain",
    overall_health_score: 55.0,
    renewal_urgency: "high",
    expansion_readiness: "not_ready",
    key_risks: [
      "Sponsor exécutif inactif sur un compte stratégique",
      "1 QBRs manqués — relation à risque",
    ],
    immediate_actions: [
      "Séquence de renouvellement urgente — 75j avant expiration",
      "QBR de santé — présenter les succès et aligner sur les objectifs année suivante",
      "Reprendre cadence QBR — proposer format flexible si besoin",
      "Enquête NPS détaillée — identifier les axes d'amélioration prioritaires",
    ],
    playbook_steps: [
      "S1 : QBR de santé — bilan valeur, objectifs année suivante",
      "S2 : Revue des risques identifiés — plan d'action correctif si nécessaire",
      "S3 : Engagement renouvellement — préparer et envoyer la proposition",
      "S4 : Traitement des objections — prix, fonctionnalités, concurrence",
      "S5 : Signature du renouvellement — confirmer les termes et lancer N+1",
    ],
    success_metrics: [
      "Renouvellement signé ≥ 60 jours avant échéance",
      "Score de santé ≥ 65 maintenu",
      "NPS stable ou en hausse",
      "Zéro escalade non résolue à la date de renouvellement",
    ],
  },
  {
    account_id: "cs_005",
    account_name: "HealthCo Belgium",
    segment: "mid_market",
    arr_eur: 72000,
    lifecycle_stage: "at_risk",
    risk_level: "high",
    playbook_motion: "rescue",
    overall_health_score: 38.0,
    renewal_urgency: "immediate",
    expansion_readiness: "not_ready",
    key_risks: [
      "Adoption produit faible (32/100) — risque de churn",
      "Pression concurrentielle active — protéger la relation en priorité",
      "Renouvellement dans 25j — santé insuffisante pour sécuriser",
      "NPS négatif (-18) — promoteur → détracteur, churn probable",
      "Champion faible ou absent — pas de relais interne",
    ],
    immediate_actions: [
      "Appel de récupération urgent avec le champion — comprendre les blocages",
      "Engager le sponsor exécutif côté client et côté fournisseur",
      "Construire un plan de remédiation 30j avec jalons mesurables",
      "Préparer un briefing concurrentiel — renforcer la valeur différenciante",
      "Campagne de réengagement utilisateur — dernière session il y a 18j",
      "Enquête NPS détaillée — identifier les axes d'amélioration prioritaires",
    ],
    playbook_steps: [
      "S1 : Appel d'urgence — diagnostic 360° des problèmes ouverts",
      "S2 : Plan de remédiation formalisé — responsables + dates + KPIs",
      "S3 : Résolution des escalades techniques en moins de 48h",
      "S4 : Check-in hebdomadaire de suivi pendant 4 semaines",
      "S5 : QBR de récupération — valider le retour à la santé",
      "S6 : Revue post-crise — leçons apprises, plan de prévention",
    ],
    success_metrics: [
      "Résolution de 100% des escalades ouvertes sous 48h",
      "Score de santé ≥ 50 dans les 30 jours",
      "NPS ≥ 0 en fin de programme de récupération",
      "Renouvellement sécurisé sans décote",
    ],
  },
  {
    account_id: "cs_006",
    account_name: "EduTech Learn GmbH",
    segment: "smb",
    arr_eur: 48000,
    lifecycle_stage: "adoption",
    risk_level: "medium",
    playbook_motion: "accelerate",
    overall_health_score: 58.0,
    renewal_urgency: "low",
    expansion_readiness: "not_ready",
    key_risks: [
      "Adoption produit faible (45/100) — risque de churn",
      "Dernière connexion il y a 12j — désengagement utilisateur",
    ],
    immediate_actions: [
      "Session d'activation fonctionnelle — couvrir les 62% de features non utilisées",
      "Organiser un atelier 'best practices' avec les utilisateurs clés",
      "Investiguer les freins à l'usage quotidien — UX, formation, intégration",
      "Partager des cas d'usage clients similaires pour inspirer l'adoption",
      "Campagne de réengagement utilisateur — dernière session il y a 12j",
    ],
    playbook_steps: [
      "S1 : Audit d'adoption — cartographier les features non utilisées",
      "S2 : Atelier d'activation — session pratique avec utilisateurs finaux",
      "S3 : Partage de best practices — cas d'usage sectoriels similaires",
      "S4 : Suivi hebdomadaire des métriques d'usage pendant 30j",
      "S5 : QBR d'adoption — présenter la progression et fixer les objectifs",
    ],
    success_metrics: [
      "Features adoptées ≥ 70% sous 60 jours",
      "DAU/MAU ratio ≥ 0.25 sous 45 jours",
      "Score d'adoption ≥ 70 au prochain QBR",
      "Création de 2+ cas d'usage additionnels documentés",
    ],
  },
  {
    account_id: "cs_007",
    account_name: "PropTech Ventures",
    segment: "mid_market",
    arr_eur: 36000,
    lifecycle_stage: "at_risk",
    risk_level: "critical",
    playbook_motion: "rescue",
    overall_health_score: 20.0,
    renewal_urgency: "high",
    expansion_readiness: "not_ready",
    key_risks: [
      "2 escalades ouvertes — satisfaction critique",
      "Adoption produit faible (18/100) — risque de churn",
      "Dernière connexion il y a 22j — désengagement utilisateur",
      "NPS négatif (-35) — promoteur → détracteur, churn probable",
      "2 QBRs manqués — relation à risque",
      "Champion faible ou absent — pas de relais interne",
      "DAU/MAU à 8% — usage irrégulier, valeur non perçue",
    ],
    immediate_actions: [
      "Appel de récupération urgent avec le champion — comprendre les blocages",
      "Escalader les 2 ticket(s) en attente — résoudre sous 48h",
      "Engager le sponsor exécutif côté client et côté fournisseur",
      "Construire un plan de remédiation 30j avec jalons mesurables",
      "Campagne de réengagement utilisateur — dernière session il y a 22j",
      "Enquête NPS détaillée — identifier les axes d'amélioration prioritaires",
    ],
    playbook_steps: [
      "S1 : Appel d'urgence — diagnostic 360° des problèmes ouverts",
      "S2 : Plan de remédiation formalisé — responsables + dates + KPIs",
      "S3 : Résolution des escalades techniques en moins de 48h",
      "S4 : Check-in hebdomadaire de suivi pendant 4 semaines",
      "S5 : QBR de récupération — valider le retour à la santé",
      "S6 : Revue post-crise — leçons apprises, plan de prévention",
    ],
    success_metrics: [
      "Résolution de 100% des escalades ouvertes sous 48h",
      "Score de santé ≥ 50 dans les 30 jours",
      "NPS ≥ 0 en fin de programme de récupération",
      "Renouvellement sécurisé sans décote",
    ],
  },
  {
    account_id: "cs_008",
    account_name: "StartupCo SaaS",
    segment: "smb",
    arr_eur: 24000,
    lifecycle_stage: "onboarding",
    risk_level: "medium",
    playbook_motion: "onboard",
    overall_health_score: 52.0,
    renewal_urgency: "low",
    expansion_readiness: "not_ready",
    key_risks: [],
    immediate_actions: [
      "Lancer la séquence d'onboarding — kick-off et plan de succès J0-90",
      "Identifier et activer le champion interne dès la première semaine",
      "Valider les jalons d'onboarding — objectifs, cas d'usage, KPIs",
      "Planifier un check-in bi-hebdomadaire jusqu'à l'adoption stable",
    ],
    playbook_steps: [
      "S1 : Kick-off officiel — plan de succès 90j, parties prenantes identifiées",
      "S2 : Activation technique — intégrations, SSO, migration données",
      "S3 : Formation utilisateurs clés — scénarios métier prioritaires",
      "S4 : Check-in J30 — adoption initiale, blocages levés",
      "S5 : Check-in J60 — extension à d'autres équipes, cas d'usage avancés",
      "S6 : Revue J90 — validation objectifs, passage à la phase adoption",
    ],
    success_metrics: [
      "100% des utilisateurs clés actifs à J30",
      "≥ 3 cas d'usage métier validés à J60",
      "Score d'adoption ≥ 60 à J90",
      "Champion identifié et engagé avant J15",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const motion = searchParams.get("motion");
  const stage = searchParams.get("stage");
  const risk = searchParams.get("risk");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/customer-success-playbook`);
      if (motion) url.searchParams.set("motion", motion);
      if (stage) url.searchParams.set("stage", stage);
      if (risk) url.searchParams.set("risk", risk);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let accounts = [...mockAccounts];
  if (motion) accounts = accounts.filter((a) => a.playbook_motion === motion);
  if (stage) accounts = accounts.filter((a) => a.lifecycle_stage === stage);
  if (risk) accounts = accounts.filter((a) => a.risk_level === risk);

  const motion_counts: Record<string, number> = {};
  const stage_counts: Record<string, number> = {};
  const risk_counts: Record<string, number> = {};
  let total_health = 0;
  let arr_at_risk = 0;
  let arr_expand = 0;

  for (const a of mockAccounts) {
    motion_counts[a.playbook_motion] = (motion_counts[a.playbook_motion] || 0) + 1;
    stage_counts[a.lifecycle_stage] = (stage_counts[a.lifecycle_stage] || 0) + 1;
    risk_counts[a.risk_level] = (risk_counts[a.risk_level] || 0) + 1;
    total_health += a.overall_health_score;
    if (a.risk_level === "high" || a.risk_level === "critical") arr_at_risk += a.arr_eur;
    if (a.expansion_readiness === "ready") arr_expand += a.arr_eur;
  }

  const n = mockAccounts.length;

  return NextResponse.json({
    accounts,
    summary: {
      total: n,
      motion_counts,
      stage_counts,
      risk_counts,
      avg_health_score: Math.round((total_health / n) * 10) / 10,
      total_arr_at_risk_eur: arr_at_risk,
      total_arr_expansion_ready_eur: arr_expand,
      rescue_count: mockAccounts.filter((a) => a.playbook_motion === "rescue").length,
      expand_ready_count: mockAccounts.filter((a) => a.expansion_readiness === "ready").length,
      renewal_urgent_count: mockAccounts.filter((a) =>
        a.renewal_urgency === "immediate" || a.renewal_urgency === "high"
      ).length,
    },
  });
}
