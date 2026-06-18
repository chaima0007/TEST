import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockReps = [
  {
    rep_id: "rep_001",
    rep_name: "Sophie Müller",
    segment: "enterprise",
    tenure_months: 30,
    coaching_intensity: "light",
    primary_focus: "strategy",
    coaching_score: 88.0,
    top_skill_gaps: [],
    strengths: [
      "Atteinte quota à 118% — performer solide",
      "Discipline prochaines étapes excellente — 85% des meetings conclus avec une NS",
      "Multi-threading fort — 3.8 contacts en moyenne par deal",
      "Bonne tenue sur les prix — seulement 8% de remise moyenne",
      "Couverture pipeline excellente — 3.5x le quota",
      "CRM à jour en moins de 24h — hygiène commerciale exemplaire",
    ],
    development_areas: [],
    coaching_actions: [
      "Focus stratégie compte — identifier les opportunités d'expansion sur les 5 meilleurs comptes",
    ],
    session_plan: [
      "S1 : Revue performance — identifier les leviers de surperformance à capitaliser",
      "S2 : Stratégie comptes — expansion et renouvellements priorisés",
      "S3 : Best practice sharing — pitcher 1 technique gagnante à l'équipe",
    ],
    kpis_to_track: [
      "Atteinte quota — objectif ≥ 100% (actuellement 118%)",
      "Couverture pipeline — objectif ≥ 3x (actuellement 3.5x)",
      "Prochaines étapes définies — objectif ≥ 80% (actuellement 85%)",
      "Remise moyenne — objectif ≤ 10% (actuellement 8%)",
    ],
  },
  {
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    segment: "enterprise",
    tenure_months: 18,
    coaching_intensity: "light",
    primary_focus: "strategy",
    coaching_score: 80.0,
    top_skill_gaps: [],
    strengths: [
      "Atteinte quota à 105% — performer solide",
      "Couverture pipeline excellente — 3.2x le quota",
      "Multi-threading fort — 3.2 contacts en moyenne par deal",
      "Bonne tenue sur les prix — seulement 7% de remise moyenne",
    ],
    development_areas: [],
    coaching_actions: [
      "Focus stratégie compte — identifier les opportunités d'expansion sur les 5 meilleurs comptes",
    ],
    session_plan: [
      "S1 : Revue performance — identifier les leviers de surperformance à capitaliser",
      "S2 : Stratégie comptes — expansion et renouvellements priorisés",
      "S3 : Best practice sharing — pitcher 1 technique gagnante à l'équipe",
    ],
    kpis_to_track: [
      "Atteinte quota — objectif ≥ 100% (actuellement 105%)",
      "Couverture pipeline — objectif ≥ 3x (actuellement 3.2x)",
      "Prochaines étapes définies — objectif ≥ 80% (actuellement 82%)",
      "Remise moyenne — objectif ≤ 10% (actuellement 7%)",
    ],
  },
  {
    rep_id: "rep_003",
    rep_name: "Marie Fontaine",
    segment: "mid_market",
    tenure_months: 14,
    coaching_intensity: "moderate",
    primary_focus: "skills",
    coaching_score: 65.0,
    top_skill_gaps: ["discovery", "multi_threading"],
    strengths: [
      "Progression quota solide — 88% d'atteinte",
      "Bonne tenue sur les prix — seulement 10% de remise moyenne",
    ],
    development_areas: [
      "Découverte insuffisante — 4 questions/appel (objectif ≥ 8)",
      "Multi-threading trop faible — 1.8 contacts/deal (objectif ≥ 3)",
    ],
    coaching_actions: [
      "Session de coaching bi-hebdomadaire — suivi structuré pendant 60 jours",
      "Exercice de roleplay discovery — préparer un bank de 15 questions impactantes",
      "Écouter et annoter 3 recordings de top performers en discovery",
      "Cartographier les parties prenantes manquantes sur chaque deal actif",
      "Identifier 2 nouveaux contacts sur les 3 deals les plus importants cette semaine",
    ],
    session_plan: [
      "S1 : Diagnostic — identifier les 2 axes de progression prioritaires",
      "S2 : Skill drill — exercice pratique sur l'axe #1",
      "S3 : Pipeline review — couvrir les deals à risque et les prochaines étapes",
      "S4 : Skill drill — exercice pratique sur l'axe #2",
      "S5 : Bilan 30j — mesurer les progrès et ajuster le plan",
    ],
    kpis_to_track: [
      "Atteinte quota — objectif ≥ 100% (actuellement 88%)",
      "Couverture pipeline — objectif ≥ 3x (actuellement 2.4x)",
      "Prochaines étapes définies — objectif ≥ 80% (actuellement 72%)",
      "Questions discovery/appel — objectif ≥ 8 (actuellement 4)",
      "Contacts/deal — objectif ≥ 3 (actuellement 1.8)",
      "Remise moyenne — objectif ≤ 10% (actuellement 10%)",
    ],
  },
  {
    rep_id: "rep_004",
    rep_name: "James O'Brien",
    segment: "mid_market",
    tenure_months: 22,
    coaching_intensity: "moderate",
    primary_focus: "pipeline",
    coaching_score: 62.0,
    top_skill_gaps: ["pipeline_hygiene", "forecasting"],
    strengths: [
      "Multi-threading fort — 3.0 contacts en moyenne par deal",
    ],
    development_areas: [
      "Hygiène CRM insuffisante — 5j de délai moyen de mise à jour (objectif ≤ 1j)",
      "Prévisions peu fiables — 32% d'écart forecast vs actuals (objectif ≤ 10%)",
    ],
    coaching_actions: [
      "Nettoyage pipeline immédiat — archiver les deals non mis à jour depuis 5j+",
      "Rappel processus CRM — mise à jour obligatoire dans les 24h post-réunion",
      "Revue du processus de forecast — alignement sur les critères de stade CRM",
      "Rétro mensuelle forecast vs actuals — analyser les écarts",
    ],
    session_plan: [
      "S1 : Diagnostic — identifier les 2 axes de progression prioritaires",
      "S2 : Skill drill — exercice pratique sur l'axe #1",
      "S3 : Pipeline review — couvrir les deals à risque et les prochaines étapes",
      "S4 : Skill drill — exercice pratique sur l'axe #2",
      "S5 : Bilan 30j — mesurer les progrès et ajuster le plan",
    ],
    kpis_to_track: [
      "Atteinte quota — objectif ≥ 100% (actuellement 82%)",
      "Couverture pipeline — objectif ≥ 3x (actuellement 2.8x)",
      "Prochaines étapes définies — objectif ≥ 80% (actuellement 75%)",
      "Délai mise à jour CRM — objectif ≤ 1j (actuellement 5j)",
      "Précision forecast — objectif ≤ 10% d'écart (actuellement 32%)",
      "Remise moyenne — objectif ≤ 10% (actuellement 12%)",
    ],
  },
  {
    rep_id: "rep_005",
    rep_name: "David Chen",
    segment: "enterprise",
    tenure_months: 8,
    coaching_intensity: "intensive",
    primary_focus: "skills",
    coaching_score: 42.0,
    top_skill_gaps: ["discovery", "qualification", "multi_threading", "closing"],
    strengths: [],
    development_areas: [
      "Découverte insuffisante — 3 questions/appel (objectif ≥ 8)",
      "Qualification incomplète — 28% des pertes sans décision",
      "Multi-threading trop faible — 1.5 contacts/deal (objectif ≥ 3)",
      "Compétences de closing à développer — pipeline présent mais conversion insuffisante",
    ],
    coaching_actions: [
      "Session de coaching bi-hebdomadaire — suivi structuré pendant 60 jours",
      "Shadow calls : écouter 2 appels/semaine et débriefing post-appel",
      "Revue pipeline hebdomadaire — deal review approfondi chaque lundi",
      "Exercice de roleplay discovery — préparer un bank de 15 questions impactantes",
      "Écouter et annoter 3 recordings de top performers en discovery",
      "Formation MEDDIC/BANT — revoir les critères de qualification par segment",
      "Template de qualification obligatoire avant démo/proposition",
      "Cartographier les parties prenantes manquantes sur chaque deal actif",
      "Identifier et travailler les deals bloqués en stade avancé",
    ],
    session_plan: [
      "S1 : Diagnostic 360° — évaluation complète des compétences et de la pipeline",
      "S2 : Plan d'action 60j — objectifs, jalons, indicateurs de succès",
      "S3 : Shadow call discovery — débriefing et feedback immédiat",
      "S4 : Deal review #1 — plan par deal pour les 5 priorités pipeline",
      "S5 : Skill training discovery & qualification",
      "S6 : Shadow call proposal — débriefing et amélioration",
      "S7 : Pipeline review + forecast calibration",
      "S8 : Bilan 30j — ajustement du plan et nouveaux objectifs",
    ],
    kpis_to_track: [
      "Atteinte quota — objectif ≥ 100% (actuellement 58%)",
      "Couverture pipeline — objectif ≥ 3x (actuellement 2.2x)",
      "Prochaines étapes définies — objectif ≥ 80% (actuellement 55%)",
      "Questions discovery/appel — objectif ≥ 8 (actuellement 3)",
      "Contacts/deal — objectif ≥ 3 (actuellement 1.5)",
      "Remise moyenne — objectif ≤ 10% (actuellement 18%)",
    ],
  },
  {
    rep_id: "rep_006",
    rep_name: "Aisha Tan",
    segment: "mid_market",
    tenure_months: 5,
    coaching_intensity: "intensive",
    primary_focus: "pipeline",
    coaching_score: 36.0,
    top_skill_gaps: ["pipeline_hygiene", "multi_threading", "discovery"],
    strengths: [],
    development_areas: [
      "Découverte insuffisante — 4 questions/appel (objectif ≥ 8)",
      "Hygiène CRM insuffisante — 8j de délai moyen de mise à jour (objectif ≤ 1j)",
      "Multi-threading trop faible — 1.2 contacts/deal (objectif ≥ 3)",
    ],
    coaching_actions: [
      "Session de coaching bi-hebdomadaire — suivi structuré pendant 60 jours",
      "Shadow calls : écouter 2 appels/semaine et débriefing post-appel",
      "Revue pipeline hebdomadaire — deal review approfondi chaque lundi",
      "Exercice de roleplay discovery — préparer un bank de 15 questions impactantes",
      "Nettoyage pipeline immédiat — archiver les deals non mis à jour depuis 8j+",
      "Rappel processus CRM — mise à jour obligatoire dans les 24h post-réunion",
      "Cartographier les parties prenantes manquantes sur chaque deal actif",
    ],
    session_plan: [
      "S1 : Diagnostic 360° — évaluation complète des compétences et de la pipeline",
      "S2 : Plan d'action 60j — objectifs, jalons, indicateurs de succès",
      "S3 : Shadow call discovery — débriefing et feedback immédiat",
      "S4 : Deal review #1 — plan par deal pour les 5 priorités pipeline",
      "S5 : Skill training discovery & qualification",
      "S6 : Shadow call proposal — débriefing et amélioration",
      "S7 : Pipeline review + forecast calibration",
      "S8 : Bilan 30j — ajustement du plan et nouveaux objectifs",
    ],
    kpis_to_track: [
      "Atteinte quota — objectif ≥ 100% (actuellement 55%)",
      "Couverture pipeline — objectif ≥ 3x (actuellement 1.2x)",
      "Prochaines étapes définies — objectif ≥ 80% (actuellement 48%)",
      "Questions discovery/appel — objectif ≥ 8 (actuellement 4)",
      "Contacts/deal — objectif ≥ 3 (actuellement 1.2)",
      "Délai mise à jour CRM — objectif ≤ 1j (actuellement 8j)",
      "Remise moyenne — objectif ≤ 10% (actuellement 14%)",
    ],
  },
  {
    rep_id: "rep_007",
    rep_name: "Carlos Rivera",
    segment: "smb",
    tenure_months: 3,
    coaching_intensity: "critical",
    primary_focus: "mindset",
    coaching_score: 18.0,
    top_skill_gaps: ["discovery", "qualification", "pipeline_hygiene", "multi_threading"],
    strengths: [],
    development_areas: [
      "Découverte insuffisante — 2 questions/appel (objectif ≥ 8)",
      "Qualification incomplète — 35% des pertes sans décision",
      "Hygiène CRM insuffisante — 12j de délai moyen de mise à jour (objectif ≤ 1j)",
      "Multi-threading trop faible — 1.1 contacts/deal (objectif ≥ 3)",
    ],
    coaching_actions: [
      "Session de coaching bi-hebdomadaire — suivi structuré pendant 60 jours",
      "Shadow calls : écouter 2 appels/semaine et débriefing post-appel",
      "Revue pipeline hebdomadaire — deal review approfondi chaque lundi",
      "Exercice de roleplay discovery — préparer un bank de 15 questions impactantes",
      "Écouter et annoter 3 recordings de top performers en discovery",
      "Formation MEDDIC/BANT — revoir les critères de qualification par segment",
      "Nettoyage pipeline immédiat — archiver les deals non mis à jour depuis 12j+",
      "Rappel processus CRM — mise à jour obligatoire dans les 24h post-réunion",
      "Cartographier les parties prenantes manquantes sur chaque deal actif",
    ],
    session_plan: [
      "S1 : PIP kick-off — plan d'amélioration formalisé, objectifs 30/60/90j",
      "S2 : Audit activités — analyser les appels, emails, réunions de la semaine passée",
      "S3 : Shadow call x2 — feedback en temps réel et plan de correction",
      "S4 : Pipeline clean-up — archiver les deals fantômes, qualifier les actifs",
      "S5 : Formation intensive discovery & qualification",
      "S6 : Roleplay closing — 3 scénarios différents avec feedback",
      "S7 : Review pipeline + forecast — calibration et discipline",
      "S8 : Bilan 30j — décision : poursuivre PIP ou escalader",
    ],
    kpis_to_track: [
      "Atteinte quota — objectif ≥ 100% (actuellement 28%)",
      "Couverture pipeline — objectif ≥ 3x (actuellement 0.8x)",
      "Prochaines étapes définies — objectif ≥ 80% (actuellement 35%)",
      "Questions discovery/appel — objectif ≥ 8 (actuellement 2)",
      "Contacts/deal — objectif ≥ 3 (actuellement 1.1)",
      "Délai mise à jour CRM — objectif ≤ 1j (actuellement 12j)",
      "Remise moyenne — objectif ≤ 10% (actuellement 22%)",
    ],
  },
  {
    rep_id: "rep_008",
    rep_name: "Erik Lindström",
    segment: "smb",
    tenure_months: 2,
    coaching_intensity: "critical",
    primary_focus: "mindset",
    coaching_score: 8.0,
    top_skill_gaps: ["discovery", "qualification", "multi_threading", "forecasting"],
    strengths: [],
    development_areas: [
      "Découverte insuffisante — 1 questions/appel (objectif ≥ 8)",
      "Qualification incomplète — 42% des pertes sans décision",
      "Multi-threading trop faible — 1.0 contacts/deal (objectif ≥ 3)",
      "Prévisions peu fiables — 48% d'écart forecast vs actuals (objectif ≤ 10%)",
    ],
    coaching_actions: [
      "Session de coaching bi-hebdomadaire — suivi structuré pendant 60 jours",
      "Shadow calls : écouter 2 appels/semaine et débriefing post-appel",
      "Revue pipeline hebdomadaire — deal review approfondi chaque lundi",
      "Exercice de roleplay discovery — préparer un bank de 15 questions impactantes",
      "Formation MEDDIC/BANT — revoir les critères de qualification par segment",
      "Cartographier les parties prenantes manquantes sur chaque deal actif",
      "Revue du processus de forecast — alignement sur les critères de stade CRM",
      "Rétro mensuelle forecast vs actuals — analyser les écarts",
    ],
    session_plan: [
      "S1 : PIP kick-off — plan d'amélioration formalisé, objectifs 30/60/90j",
      "S2 : Audit activités — analyser les appels, emails, réunions de la semaine passée",
      "S3 : Shadow call x2 — feedback en temps réel et plan de correction",
      "S4 : Pipeline clean-up — archiver les deals fantômes, qualifier les actifs",
      "S5 : Formation intensive discovery & qualification",
      "S6 : Roleplay closing — 3 scénarios différents avec feedback",
      "S7 : Review pipeline + forecast — calibration et discipline",
      "S8 : Bilan 30j — décision : poursuivre PIP ou escalader",
    ],
    kpis_to_track: [
      "Atteinte quota — objectif ≥ 100% (actuellement 18%)",
      "Couverture pipeline — objectif ≥ 3x (actuellement 0.5x)",
      "Prochaines étapes définies — objectif ≥ 80% (actuellement 28%)",
      "Questions discovery/appel — objectif ≥ 8 (actuellement 1)",
      "Contacts/deal — objectif ≥ 3 (actuellement 1.0)",
      "Précision forecast — objectif ≤ 10% d'écart (actuellement 48%)",
      "Remise moyenne — objectif ≤ 10% (actuellement 30%)",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const intensity = searchParams.get("intensity");
  const focus = searchParams.get("focus");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/sales-coaching`);
      if (intensity) url.searchParams.set("intensity", intensity);
      if (focus) url.searchParams.set("focus", focus);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let reps = [...mockReps];
  if (intensity) reps = reps.filter((r) => r.coaching_intensity === intensity);
  if (focus) reps = reps.filter((r) => r.primary_focus === focus);

  const intensity_counts: Record<string, number> = {};
  const focus_counts: Record<string, number> = {};
  const gap_counts: Record<string, number> = {};
  let total_score = 0;

  for (const r of mockReps) {
    intensity_counts[r.coaching_intensity] = (intensity_counts[r.coaching_intensity] || 0) + 1;
    focus_counts[r.primary_focus] = (focus_counts[r.primary_focus] || 0) + 1;
    total_score += r.coaching_score;
    for (const g of r.top_skill_gaps) {
      gap_counts[g] = (gap_counts[g] || 0) + 1;
    }
  }

  const n = mockReps.length;

  return NextResponse.json({
    reps,
    summary: {
      total: n,
      intensity_counts,
      focus_counts,
      gap_counts,
      avg_coaching_score: Math.round((total_score / n) * 10) / 10,
      critical_count: mockReps.filter((r) => r.coaching_intensity === "critical").length,
      star_count: mockReps.filter((r) => r.coaching_intensity === "light").length,
    },
  });
}
