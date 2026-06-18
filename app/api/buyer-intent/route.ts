import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockProspects = [
  {
    prospect_id: "bi_001",
    company_name: "Total Energies SE",
    rep_id: "rep_001",
    rep_name: "Sophie Martin",
    intent_level: "hot",
    intent_category: "product_interest",
    intent_trend: "spiked",
    outreach_strategy: "executive_outreach",
    intent_score: 88.5,
    digital_score: 82.0,
    engagement_score: 90.0,
    trigger_score: 30.0,
    hot_signals: [
      "Démo demandée — signal d'achat très fort",
      "Trial gratuit démarré — évaluation active du produit",
      "3 visites page tarification — comparaison de prix active",
      "2 cas client(s) téléchargé(s) — validation par les pairs",
      "Webinaire suivi — engagement éducatif actif",
      "Réponse à l'outreach — ouverture au dialogue commercial",
      "Levée de fonds annoncée — budget disponible, fenêtre d'opportunité ouverte",
    ],
    cold_signals: [],
    recommended_actions: [
      "Contact C-level direct — valeur stratégique à mettre en avant",
      "Préparer un executive brief personnalisé avec ROI chiffré",
    ],
  },
  {
    prospect_id: "bi_002",
    company_name: "Capgemini France",
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    intent_level: "hot",
    intent_category: "competitive_eval",
    intent_trend: "accelerating",
    outreach_strategy: "immediate_outreach",
    intent_score: 72.3,
    digital_score: 75.0,
    engagement_score: 68.0,
    trigger_score: 0.0,
    hot_signals: [
      "Démo demandée — signal d'achat très fort",
      "4 visites page tarification — comparaison de prix active",
      "3 cas client(s) téléchargé(s) — validation par les pairs",
      "2 visites page démo — intérêt produit confirmé",
      "Réponse à l'outreach — ouverture au dialogue commercial",
    ],
    cold_signals: [],
    recommended_actions: [
      "Appel de découverte aujourd'hui — fenêtre d'engagement optimale",
      "Personnaliser l'outreach autour de : Démo demandée — signal d'achat très fort, 4 visites page tarification — comparaison de prix active",
    ],
  },
  {
    prospect_id: "bi_003",
    company_name: "Sodexo Group",
    rep_id: "rep_001",
    rep_name: "Sophie Martin",
    intent_level: "warm",
    intent_category: "relationship",
    intent_trend: "stable",
    outreach_strategy: "value_content",
    intent_score: 55.8,
    digital_score: 42.0,
    engagement_score: 62.0,
    trigger_score: 0.0,
    hot_signals: [
      "Webinaire suivi — engagement éducatif actif",
      "Réponse à l'outreach — ouverture au dialogue commercial",
      "1 cas client(s) téléchargé(s) — validation par les pairs",
    ],
    cold_signals: [],
    recommended_actions: [
      "Envoyer 1–2 cas clients ciblés sur le secteur/douleur identifiée",
      "Inviter à un prochain webinaire produit lié aux signaux détectés",
    ],
  },
  {
    prospect_id: "bi_004",
    company_name: "Veolia Environnement",
    rep_id: "rep_003",
    rep_name: "Marie Lefevre",
    intent_level: "warm",
    intent_category: "event_triggered",
    intent_trend: "spiked",
    outreach_strategy: "immediate_outreach",
    intent_score: 48.5,
    digital_score: 18.0,
    engagement_score: 42.0,
    trigger_score: 45.0,
    hot_signals: [
      "Contrat concurrent expiré — prospect en recherche de solution",
      "Changement de leadership — opportunité de repositionnement",
      "Offre d'emploi pertinente publiée — besoin business identifié",
    ],
    cold_signals: [],
    recommended_actions: [
      "Appel de découverte aujourd'hui — fenêtre d'engagement optimale",
      "Personnaliser l'outreach autour de : Contrat concurrent expiré — prospect en recherche de solution, Changement de leadership — opportunité de repositionnement",
    ],
  },
  {
    prospect_id: "bi_005",
    company_name: "Boulanger SA",
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    intent_level: "lukewarm",
    intent_category: "product_interest",
    intent_trend: "stable",
    outreach_strategy: "event_invite",
    intent_score: 32.1,
    digital_score: 28.0,
    engagement_score: 38.0,
    trigger_score: 0.0,
    hot_signals: [
      "Webinaire suivi — engagement éducatif actif",
      "1 cas client(s) téléchargé(s) — validation par les pairs",
    ],
    cold_signals: [],
    recommended_actions: [
      "Inviter au prochain événement / webinaire en lien avec les besoins",
      "Personnaliser l'invitation avec les signaux d'engagement passés",
    ],
  },
  {
    prospect_id: "bi_006",
    company_name: "Picard Surgelés",
    rep_id: "rep_003",
    rep_name: "Marie Lefevre",
    intent_level: "lukewarm",
    intent_category: "relationship",
    intent_trend: "declining",
    outreach_strategy: "nurture_sequence",
    intent_score: 22.4,
    digital_score: 20.0,
    engagement_score: 25.0,
    trigger_score: 0.0,
    hot_signals: [],
    cold_signals: [
      "Pas d'engagement depuis 25 jours — intérêt en déclin",
    ],
    recommended_actions: [
      "Enrôler dans la séquence de nurture — cadence bimensuelle",
      "Partager du contenu éducatif aligné sur les besoins sectoriels",
    ],
  },
  {
    prospect_id: "bi_007",
    company_name: "Allia Habitat",
    rep_id: "rep_004",
    rep_name: "Thomas Bernard",
    intent_level: "cold",
    intent_category: "relationship",
    intent_trend: "dormant",
    outreach_strategy: "wait_and_monitor",
    intent_score: 8.2,
    digital_score: 5.0,
    engagement_score: 12.0,
    trigger_score: 0.0,
    hot_signals: [],
    cold_signals: [
      "Pas d'engagement depuis 65 jours — intérêt en déclin",
      "Emails non ouverts malgré plusieurs envois — désengagement email",
      "Score ICP faible (35/100) — adéquation produit-marché limitée",
    ],
    recommended_actions: [
      "Surveiller les signaux — relancer si activité détectée",
      "Configurer une alerte sur les triggers externes (levée de fonds, recrutement)",
    ],
  },
  {
    prospect_id: "bi_008",
    company_name: "Sofitel Luxury Hotels",
    rep_id: "rep_004",
    rep_name: "Thomas Bernard",
    intent_level: "warm",
    intent_category: "pain_driven",
    intent_trend: "accelerating",
    outreach_strategy: "value_content",
    intent_score: 51.0,
    digital_score: 38.0,
    engagement_score: 55.0,
    trigger_score: 20.0,
    hot_signals: [
      "Changement de leadership — opportunité de repositionnement",
      "Offre d'emploi pertinente publiée — besoin business identifié",
      "Réponse à l'outreach — ouverture au dialogue commercial",
    ],
    cold_signals: [],
    recommended_actions: [
      "Envoyer 1–2 cas clients ciblés sur le secteur/douleur identifiée",
      "Inviter à un prochain webinaire produit lié aux signaux détectés",
    ],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const level    = searchParams.get("level");
  const strategy = searchParams.get("strategy");
  const trend    = searchParams.get("trend");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/buyer-intent`);
      if (level)    url.searchParams.set("level", level);
      if (strategy) url.searchParams.set("strategy", strategy);
      if (trend)    url.searchParams.set("trend", trend);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let prospects = [...mockProspects];
  if (level)    prospects = prospects.filter((p) => p.intent_level === level);
  if (strategy) prospects = prospects.filter((p) => p.outreach_strategy === strategy);
  if (trend)    prospects = prospects.filter((p) => p.intent_trend === trend);

  const level_counts:    Record<string, number> = {};
  const category_counts: Record<string, number> = {};
  const trend_counts:    Record<string, number> = {};
  const strategy_counts: Record<string, number> = {};
  let total_intent = 0, total_digital = 0, total_engagement = 0;

  for (const p of mockProspects) {
    level_counts[p.intent_level]         = (level_counts[p.intent_level] || 0) + 1;
    category_counts[p.intent_category]   = (category_counts[p.intent_category] || 0) + 1;
    trend_counts[p.intent_trend]         = (trend_counts[p.intent_trend] || 0) + 1;
    strategy_counts[p.outreach_strategy] = (strategy_counts[p.outreach_strategy] || 0) + 1;
    total_intent     += p.intent_score;
    total_digital    += p.digital_score;
    total_engagement += p.engagement_score;
  }

  const n = mockProspects.length;

  return NextResponse.json({
    prospects,
    summary: {
      total: n,
      level_counts,
      category_counts,
      trend_counts,
      strategy_counts,
      avg_intent_score:     Math.round((total_intent / n) * 10) / 10,
      avg_digital_score:    Math.round((total_digital / n) * 10) / 10,
      avg_engagement_score: Math.round((total_engagement / n) * 10) / 10,
      hot_count:            mockProspects.filter((p) => p.intent_level === "hot").length,
      immediate_outreach_count: mockProspects.filter((p) =>
        p.outreach_strategy === "immediate_outreach" || p.outreach_strategy === "executive_outreach"
      ).length,
    },
  });
}
