import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockMeetings = [
  {
    meeting_id: "mtg_001",
    deal_id: "deal_001",
    rep_id: "rep_001",
    rep_name: "Sophie Martin",
    account_name: "Total Energies SE",
    meeting_type: "executive_review",
    meeting_outcome: "advanced",
    meeting_quality: "excellent",
    buying_signal_strength: "strong",
    follow_up_urgency: "same_week",
    quality_score: 88.0,
    engagement_score: 85.0,
    buying_signals_count: 5,
    objections_count: 1,
    next_step_agreed: true,
    next_step_days_out: 5,
    positive_signals: [
      "Décideur présent — validation stratégique possible",
      "Sponsor exécutif engagé — soutien haut niveau confirmé",
      "Questions actives du prospect — fort intérêt détecté",
      "Demande de tarification — signal d'achat fort",
      "Timeline mentionnée — urgence côté client",
    ],
    concerns: ["1 objection soulevée — à adresser en suivi"],
    follow_up_actions: [
      "Envoyer la proposition sous 48h",
      "Planifier la réunion de validation avec le C-level",
      "Préparer la réponse aux objections identifiées",
    ],
    manager_alerts: [],
  },
  {
    meeting_id: "mtg_002",
    deal_id: "deal_002",
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    account_name: "Capgemini France",
    meeting_type: "demo",
    meeting_outcome: "advanced",
    meeting_quality: "good",
    buying_signal_strength: "strong",
    follow_up_urgency: "same_week",
    quality_score: 72.0,
    engagement_score: 70.0,
    buying_signals_count: 4,
    objections_count: 1,
    next_step_agreed: true,
    next_step_days_out: 7,
    positive_signals: [
      "Questions actives du prospect — fort intérêt détecté",
      "Demande de tarification — signal d'achat fort",
      "Timeline mentionnée — urgence côté client",
      "Budget confirmé — capacité financière validée",
    ],
    concerns: ["1 objection soulevée — à adresser en suivi"],
    follow_up_actions: [
      "Envoyer la proposition commerciale complète",
      "Planifier une démo technique approfondie",
    ],
    manager_alerts: [],
  },
  {
    meeting_id: "mtg_003",
    deal_id: "deal_003",
    rep_id: "rep_001",
    rep_name: "Sophie Martin",
    account_name: "Sodexo Group",
    meeting_type: "discovery",
    meeting_outcome: "maintained",
    meeting_quality: "good",
    buying_signal_strength: "moderate",
    follow_up_urgency: "standard",
    quality_score: 58.0,
    engagement_score: 50.0,
    buying_signals_count: 2,
    objections_count: 2,
    next_step_agreed: true,
    next_step_days_out: 10,
    positive_signals: [
      "Questions actives du prospect — fort intérêt détecté",
      "Décideur présent — validation stratégique possible",
    ],
    concerns: [
      "2 objections soulevées — friction significative",
      "Pas de discussion tarif/timeline — avancement limité",
    ],
    follow_up_actions: [
      "Préparer un dossier de réponse aux objections",
      "Identifier d'autres interlocuteurs clés",
    ],
    manager_alerts: [],
  },
  {
    meeting_id: "mtg_004",
    deal_id: "deal_004",
    rep_id: "rep_003",
    rep_name: "Marie Lefevre",
    account_name: "Veolia Environnement",
    meeting_type: "follow_up",
    meeting_outcome: "maintained",
    meeting_quality: "average",
    buying_signal_strength: "weak",
    follow_up_urgency: "same_week",
    quality_score: 42.0,
    engagement_score: 35.0,
    buying_signals_count: 1,
    objections_count: 2,
    next_step_agreed: true,
    next_step_days_out: 14,
    positive_signals: ["Timeline mentionnée — urgence côté client"],
    concerns: [
      "2 objections soulevées — friction significative",
      "Faible engagement — risque de stagnation",
      "Pas de décideur présent — blocage possible",
    ],
    follow_up_actions: [
      "Planifier une réunion avec le décideur",
      "Retravailler la proposition de valeur",
    ],
    manager_alerts: [],
  },
  {
    meeting_id: "mtg_005",
    deal_id: "deal_005",
    rep_id: "rep_002",
    rep_name: "Lucas Dubois",
    account_name: "Boulanger SA",
    meeting_type: "proposal_review",
    meeting_outcome: "no_decision",
    meeting_quality: "average",
    buying_signal_strength: "weak",
    follow_up_urgency: "same_week",
    quality_score: 38.0,
    engagement_score: 30.0,
    buying_signals_count: 1,
    objections_count: 1,
    next_step_agreed: false,
    next_step_days_out: null,
    positive_signals: ["Demande de tarification — signal d'achat fort"],
    concerns: [
      "Pas de prochaine étape définie — deal en suspens",
      "Faible engagement — risque de stagnation",
    ],
    follow_up_actions: [
      "Relance sous 48h pour définir la prochaine étape",
      "Qualifier le niveau d'intérêt réel",
    ],
    manager_alerts: [
      "Pas de next step — intervention manager recommandée",
    ],
  },
  {
    meeting_id: "mtg_006",
    deal_id: "deal_006",
    rep_id: "rep_003",
    rep_name: "Marie Lefevre",
    account_name: "Picard Surgelés",
    meeting_type: "negotiation",
    meeting_outcome: "regressed",
    meeting_quality: "poor",
    buying_signal_strength: "negative",
    follow_up_urgency: "immediate",
    quality_score: 22.0,
    engagement_score: 15.0,
    buying_signals_count: 0,
    objections_count: 4,
    next_step_agreed: false,
    next_step_days_out: null,
    positive_signals: [],
    concerns: [
      "Pas de prochaine étape définie — deal en suspens",
      "4 objections majeures — friction critique",
      "Aucun signal d'achat positif",
      "Talk ratio déséquilibré — prospect peu engagé",
    ],
    follow_up_actions: [
      "Escalade immédiate au manager",
      "Revoir fondamentalement l'approche commerciale",
      "Évaluer si le deal est récupérable",
    ],
    manager_alerts: [
      "Réunion régressée — deal en danger critique",
      "Escalade senior recommandée sous 24h",
    ],
  },
  {
    meeting_id: "mtg_007",
    deal_id: "deal_007",
    rep_id: "rep_004",
    rep_name: "Thomas Bernard",
    account_name: "Allia Habitat",
    meeting_type: "qbr",
    meeting_outcome: "regressed",
    meeting_quality: "poor",
    buying_signal_strength: "negative",
    follow_up_urgency: "immediate",
    quality_score: 18.0,
    engagement_score: 10.0,
    buying_signals_count: 0,
    objections_count: 3,
    next_step_agreed: false,
    next_step_days_out: null,
    positive_signals: [],
    concerns: [
      "Pas de prochaine étape définie — deal en suspens",
      "3 objections majeures — friction critique",
      "Aucun signal d'achat positif",
      "Évaluation concurrente suspectée",
    ],
    follow_up_actions: [
      "Appel exécutif dans les 24h",
      "Construire un plan de récupération d'urgence",
      "Identifier et neutraliser les objections bloquantes",
    ],
    manager_alerts: [
      "Réunion régressée — deal en danger critique",
      "Escalade C-level recommandée immédiatement",
    ],
  },
  {
    meeting_id: "mtg_008",
    deal_id: "deal_008",
    rep_id: "rep_004",
    rep_name: "Thomas Bernard",
    account_name: "Sofitel Luxury Hotels",
    meeting_type: "intro",
    meeting_outcome: "maintained",
    meeting_quality: "average",
    buying_signal_strength: "moderate",
    follow_up_urgency: "standard",
    quality_score: 40.0,
    engagement_score: 45.0,
    buying_signals_count: 2,
    objections_count: 1,
    next_step_agreed: true,
    next_step_days_out: 10,
    positive_signals: [
      "Questions actives du prospect — fort intérêt détecté",
      "Timeline mentionnée — urgence côté client",
    ],
    concerns: ["1 objection soulevée — à adresser en suivi"],
    follow_up_actions: [
      "Envoyer le résumé de la réunion et les ressources promises",
      "Planifier la prochaine démo produit",
    ],
    manager_alerts: [],
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const outcome  = searchParams.get("outcome");
  const quality  = searchParams.get("quality");
  const urgency  = searchParams.get("urgency");
  const strength = searchParams.get("strength");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/meeting-intelligence`);
      if (outcome)  url.searchParams.set("outcome", outcome);
      if (quality)  url.searchParams.set("quality", quality);
      if (urgency)  url.searchParams.set("urgency", urgency);
      if (strength) url.searchParams.set("strength", strength);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch {}
  }

  let meetings = [...mockMeetings];
  if (outcome)  meetings = meetings.filter((m) => m.meeting_outcome === outcome);
  if (quality)  meetings = meetings.filter((m) => m.meeting_quality === quality);
  if (urgency)  meetings = meetings.filter((m) => m.follow_up_urgency === urgency);
  if (strength) meetings = meetings.filter((m) => m.buying_signal_strength === strength);

  const outcome_counts:  Record<string, number> = {};
  const quality_counts:  Record<string, number> = {};
  const urgency_counts:  Record<string, number> = {};
  const signal_counts:   Record<string, number> = {};
  let total_quality = 0;
  let total_engagement = 0;
  let next_step_count = 0;
  let advanced_count = 0;

  for (const m of mockMeetings) {
    outcome_counts[m.meeting_outcome]         = (outcome_counts[m.meeting_outcome] || 0) + 1;
    quality_counts[m.meeting_quality]         = (quality_counts[m.meeting_quality] || 0) + 1;
    urgency_counts[m.follow_up_urgency]       = (urgency_counts[m.follow_up_urgency] || 0) + 1;
    signal_counts[m.buying_signal_strength]   = (signal_counts[m.buying_signal_strength] || 0) + 1;
    total_quality    += m.quality_score;
    total_engagement += m.engagement_score;
    if (m.next_step_agreed) next_step_count++;
    if (m.meeting_outcome === "advanced") advanced_count++;
  }

  const n = mockMeetings.length;

  return NextResponse.json(sealResponse({
    meetings,
    summary: {
      total: n,
      outcome_counts,
      quality_counts,
      urgency_counts,
      signal_counts,
      avg_quality_score:    Math.round((total_quality / n) * 10) / 10,
      avg_engagement_score: Math.round((total_engagement / n) * 10) / 10,
      next_step_rate:       Math.round((next_step_count / n) * 1000) / 10,
      advancement_rate:     Math.round((advanced_count / n) * 1000) / 10,
      immediate_follow_up_count: mockMeetings.filter((m) => m.follow_up_urgency === "immediate").length,
    },
  } as Record<string,unknown>));
}
