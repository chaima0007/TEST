import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[sales-skills] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001",
    rep_name: "Sophie Martin",
    manager_id: "mgr_001",
    overall_skill_score: 87.2,
    technical_score: 90.4,
    operational_score: 85.0,
    results_score: 83.1,
    weakest_area: "Technique de closing",
    skill_level: "expert",
    skill_gap: "none",
    coaching_priority: "maintain",
    development_path: "advanced_training",
    strengths: [
      "Découverte client excellente (92/100) — écoute et qualification au top",
      "Démos très efficaces (88/100) — présentation convaincante",
      "Prospection efficace (85/100) — pipeline bien rempli",
      "Gestion du pipeline rigoureuse (88/100) — prévisions fiables",
      "Quota dépassé (128%) — objectifs commerciaux atteints",
      "Taux de victoire élevé (48%) — conversion deals supérieure",
      "Top performer Q précédent — excellence commerciale confirmée",
    ],
    gaps: [],
    recommended_actions: [
      "Conserver le rythme — partager les meilleures pratiques avec l'équipe",
      "Envisager un rôle de mentor pour les commerciaux en développement",
    ],
  },
  {
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    manager_id: "mgr_001",
    overall_skill_score: 74.5,
    technical_score: 76.0,
    operational_score: 78.0,
    results_score: 70.8,
    weakest_area: "Négociation",
    skill_level: "advanced",
    skill_gap: "minor",
    coaching_priority: "low",
    development_path: "self_directed",
    strengths: [
      "Découverte client excellente (82/100) — écoute et qualification au top",
      "Gestion du pipeline rigoureuse (82/100) — prévisions fiables",
      "Discipline CRM exemplaire (83/100) — données à jour",
    ],
    gaps: [],
    recommended_actions: [
      "S'inscrire aux formations en ligne sur les domaines identifiés",
      "Utiliser les ressources de la bibliothèque de formation interne",
    ],
  },
  {
    rep_id: "rep_003",
    rep_name: "Marie Lefevre",
    manager_id: "mgr_001",
    overall_skill_score: 61.3,
    technical_score: 63.0,
    operational_score: 60.0,
    results_score: 59.8,
    weakest_area: "Discipline CRM",
    skill_level: "proficient",
    skill_gap: "moderate",
    coaching_priority: "medium",
    development_path: "peer_mentoring",
    strengths: [
      "Démos très efficaces (80/100) — présentation convaincante",
    ],
    gaps: [
      "Hygiène CRM à améliorer (48/100) — données manquantes ou obsolètes",
    ],
    recommended_actions: [
      "Associer à un top performer pour du mentoring pair-à-pair",
      "Participer à des revues de deals en équipe pour observer les bonnes pratiques",
    ],
  },
  {
    rep_id: "rep_004",
    rep_name: "Thomas Bernard",
    manager_id: "mgr_002",
    overall_skill_score: 47.8,
    technical_score: 50.0,
    operational_score: 46.0,
    results_score: 45.5,
    weakest_area: "Gestion des objections",
    skill_level: "developing",
    skill_gap: "moderate",
    coaching_priority: "medium",
    development_path: "skills_coaching",
    strengths: [],
    gaps: [
      "Objections mal gérées (42/100) — manque de réponses préparées",
      "Pipeline mal géré (44/100) — prévisions peu fiables",
    ],
    recommended_actions: [
      "Planifier un coaching individuel hebdomadaire avec le manager",
      "Travailler les appels d'entraînement et les jeux de rôle sur les points faibles",
    ],
  },
  {
    rep_id: "rep_005",
    rep_name: "Claire Fontaine",
    manager_id: "mgr_002",
    overall_skill_score: 80.1,
    technical_score: 82.0,
    operational_score: 80.0,
    results_score: 77.5,
    weakest_area: "Prospection",
    skill_level: "advanced",
    skill_gap: "minor",
    coaching_priority: "low",
    development_path: "advanced_training",
    strengths: [
      "Découverte client excellente (85/100) — écoute et qualification au top",
      "Gestion des objections solide (82/100) — réponses précises et pertinentes",
      "Discipline CRM exemplaire (81/100) — données à jour",
      "Quota dépassé (108%) — objectifs commerciaux atteints",
    ],
    gaps: [],
    recommended_actions: [
      "S'inscrire aux formations en ligne sur les domaines identifiés",
      "Utiliser les ressources de la bibliothèque de formation interne",
    ],
  },
  {
    rep_id: "rep_006",
    rep_name: "Antoine Moreau",
    manager_id: "mgr_002",
    overall_skill_score: 35.2,
    technical_score: 34.0,
    operational_score: 38.0,
    results_score: 34.5,
    weakest_area: "Technique de closing",
    skill_level: "developing",
    skill_gap: "significant",
    coaching_priority: "high",
    development_path: "skills_coaching",
    strengths: [],
    gaps: [
      "Découverte client insuffisante (35/100) — qualification trop superficielle",
      "Technique de closing faible (28/100) — deals qui s'étirent sans décision",
      "Objections mal gérées (30/100) — manque de réponses préparées",
      "Quota sous-atteint (58%) — objectifs commerciaux non réalisés",
    ],
    recommended_actions: [
      "Planifier un coaching individuel hebdomadaire avec le manager",
      "Travailler les appels d'entraînement et les jeux de rôle sur les points faibles",
      "Plan de développement 30-60-90j à mettre en place avec le manager immédiatement",
    ],
  },
  {
    rep_id: "rep_007",
    rep_name: "Isabelle Petit",
    manager_id: "mgr_001",
    overall_skill_score: 22.8,
    technical_score: 24.0,
    operational_score: 22.0,
    results_score: 21.5,
    weakest_area: "Discipline CRM",
    skill_level: "beginner",
    skill_gap: "critical",
    coaching_priority: "immediate",
    development_path: "skills_coaching",
    strengths: [],
    gaps: [
      "Découverte client insuffisante (25/100) — qualification trop superficielle",
      "Démos peu convaincantes (22/100) — adapter au persona acheteur",
      "Objections mal gérées (20/100) — manque de réponses préparées",
      "Négociation à améliorer (22/100) — risque de concessions excessives",
      "Technique de closing faible (18/100) — deals qui s'étirent sans décision",
      "Prospection insuffisante (24/100) — pipeline sous-alimenté",
      "Pipeline mal géré (22/100) — prévisions peu fiables",
      "Hygiène CRM à améliorer (15/100) — données manquantes ou obsolètes",
      "Quota sous-atteint (35%) — objectifs commerciaux non réalisés",
      "Taux de victoire bas (8%) — qualification ou closing à renforcer",
    ],
    recommended_actions: [
      "Planifier un coaching individuel hebdomadaire avec le manager",
      "Travailler les appels d'entraînement et les jeux de rôle sur les points faibles",
      "Plan de développement 30-60-90j à mettre en place avec le manager immédiatement",
    ],
  },
  {
    rep_id: "rep_008",
    rep_name: "Nicolas Roux",
    manager_id: "mgr_002",
    overall_skill_score: 55.6,
    technical_score: 57.0,
    operational_score: 54.0,
    results_score: 54.8,
    weakest_area: "Prospection",
    skill_level: "proficient",
    skill_gap: "moderate",
    coaching_priority: "medium",
    development_path: "skills_coaching",
    strengths: [
      "Démos très efficaces (80/100) — présentation convaincante",
    ],
    gaps: [
      "Prospection insuffisante (46/100) — pipeline sous-alimenté",
    ],
    recommended_actions: [
      "Planifier un coaching individuel hebdomadaire avec le manager",
      "Travailler les appels d'entraînement et les jeux de rôle sur les points faibles",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const level    = searchParams.get("level");
  const priority = searchParams.get("priority");
  const manager  = searchParams.get("manager");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-skills`);
      if (level)    url.searchParams.set("level", level);
      if (priority) url.searchParams.set("priority", priority);
      if (manager)  url.searchParams.set("manager", manager);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let reps = [...mockReps];
  if (level)    reps = reps.filter((r) => r.skill_level === level);
  if (priority) reps = reps.filter((r) => r.coaching_priority === priority);
  if (manager)  reps = reps.filter((r) => r.manager_id === manager);

  const level_counts:    Record<string, number> = {};
  const gap_counts:      Record<string, number> = {};
  const priority_counts: Record<string, number> = {};
  const path_counts:     Record<string, number> = {};
  let total_o = 0, total_t = 0, total_op = 0, total_r = 0;

  for (const rep of mockReps) {
    level_counts[rep.skill_level]           = (level_counts[rep.skill_level] || 0) + 1;
    gap_counts[rep.skill_gap]               = (gap_counts[rep.skill_gap] || 0) + 1;
    priority_counts[rep.coaching_priority]  = (priority_counts[rep.coaching_priority] || 0) + 1;
    path_counts[rep.development_path]       = (path_counts[rep.development_path] || 0) + 1;
    total_o  += rep.overall_skill_score;
    total_t  += rep.technical_score;
    total_op += rep.operational_score;
    total_r  += rep.results_score;
  }

  const n = mockReps.length;

  return sealResponse(NextResponse.json({
    reps,
    summary: {
      total: n,
      level_counts,
      gap_counts,
      priority_counts,
      path_counts,
      avg_overall_score:     Math.round((total_o / n) * 10) / 10,
      avg_technical_score:   Math.round((total_t / n) * 10) / 10,
      avg_operational_score: Math.round((total_op / n) * 10) / 10,
      avg_results_score:     Math.round((total_r / n) * 10) / 10,
      top_performer_count:   mockReps.filter((r) => r.skill_level === "expert" || r.skill_level === "advanced").length,
      immediate_coaching_count: mockReps.filter((r) => r.coaching_priority === "immediate").length,
      at_risk_count:         mockReps.filter((r) => r.skill_gap === "critical" || r.skill_gap === "significant").length,
    },
  }));
}
