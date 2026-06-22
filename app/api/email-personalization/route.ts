import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[email-personalization] SWARM_API_URL non défini — mode dégradé activé");
}

const SWARM_API_URL = process.env.SWARM_API_URL;

const mockEmails = [
  {
    prospect_id: "p_001",
    campaign_id: "c_saas_q3",
    rep_id: "rep_001",
    name: "Alexandre Bertrand",
    company: "TechVision SA",
    industry: "saas",
    company_size: "enterprise",
    personalization_score: 87.3,
    personalization_level: "hyper_personalized",
    email_tone: "executive",
    send_timing: "morning",
    recommended_action: "send_now",
    predicted_open_rate: 0.48,
    predicted_reply_rate: 0.18,
    send_score: 78.5,
    is_ready_to_send: true,
    personalization_tips: [],
    subject_suggestions: [
      "Félicitations pour votre levée — comment accélérer la croissance SaaS",
      "3 leviers pour améliorer la croissance SaaS en Q3",
    ],
    risk_flags: [],
    optimization_score: 82.9,
  },
  {
    prospect_id: "p_002",
    campaign_id: "c_saas_q3",
    rep_id: "rep_001",
    name: "Nathalie Rousseau",
    company: "DataFlow SARL",
    industry: "finance",
    company_size: "mid_market",
    personalization_score: 72.1,
    personalization_level: "highly_personalized",
    email_tone: "consultative",
    send_timing: "morning",
    recommended_action: "refine_and_send",
    predicted_open_rate: 0.38,
    predicted_reply_rate: 0.12,
    send_score: 58.4,
    is_ready_to_send: true,
    personalization_tips: ["Rechercher un trigger event récent (levée de fonds, recrutement, expansion)"],
    subject_suggestions: [
      "Suite à votre intérêt — prochaine étape concrète",
      "Idée rapide pour la performance financière",
    ],
    risk_flags: [],
    optimization_score: 65.3,
  },
  {
    prospect_id: "p_003",
    campaign_id: "c_retail_q3",
    rep_id: "rep_002",
    name: "Julien Perret",
    company: "RetailMax Nord",
    industry: "retail",
    company_size: "smb",
    personalization_score: 48.5,
    personalization_level: "moderately_personalized",
    email_tone: "educational",
    send_timing: "midday",
    recommended_action: "review_before_send",
    predicted_open_rate: 0.28,
    predicted_reply_rate: 0.05,
    send_score: 38.2,
    is_ready_to_send: false,
    personalization_tips: [
      "Enrichir le profil — ajouter plus de données de personnalisation",
      "Identifier les points de douleur spécifiques au persona",
      "Rechercher un trigger event récent (levée de fonds, recrutement, expansion)",
    ],
    subject_suggestions: ["Idée rapide pour l'expérience client retail"],
    risk_flags: [],
    optimization_score: 43.4,
  },
  {
    prospect_id: "p_004",
    campaign_id: "c_retail_q3",
    rep_id: "rep_002",
    name: "Claire Fontaine",
    company: "ModeXpress SAS",
    industry: "retail",
    company_size: "enterprise",
    personalization_score: 91.0,
    personalization_level: "hyper_personalized",
    email_tone: "urgency",
    send_timing: "immediate",
    recommended_action: "send_now",
    predicted_open_rate: 0.55,
    predicted_reply_rate: 0.22,
    send_score: 82.6,
    is_ready_to_send: true,
    personalization_tips: [],
    subject_suggestions: [
      "Action requise avant la fin du trimestre",
      "Suite à votre intérêt — prochaine étape concrète",
    ],
    risk_flags: [],
    optimization_score: 86.8,
  },
  {
    prospect_id: "p_005",
    campaign_id: "c_saas_q3",
    rep_id: "rep_003",
    name: "Marc Guillot",
    company: "CloudBase Inc",
    industry: "saas",
    company_size: "mid_market",
    personalization_score: 22.0,
    personalization_level: "template",
    email_tone: "educational",
    send_timing: "midday",
    recommended_action: "rewrite_required",
    predicted_open_rate: 0.22,
    predicted_reply_rate: 0.03,
    send_score: 18.5,
    is_ready_to_send: false,
    personalization_tips: [
      "Enrichir le profil — ajouter plus de données de personnalisation",
      "Identifier les points de douleur spécifiques au persona",
      "Rechercher un trigger event récent (levée de fonds, recrutement, expansion)",
      "Améliorer la ligne d'objet — viser un score supérieur à 60",
      "Renforcer la pertinence du corps — aligner sur le secteur et le persona",
      "Personnaliser au minimum 3 éléments avant d'envoyer",
    ],
    subject_suggestions: ["Idée rapide pour la croissance SaaS"],
    risk_flags: [
      "Personnalisation insuffisante — risque d'atterrir en spam",
      "Score d'envoi critique — ne pas envoyer sans optimisation",
    ],
    optimization_score: 20.3,
  },
  {
    prospect_id: "p_006",
    campaign_id: "c_finance_q3",
    rep_id: "rep_003",
    name: "Sophie Marchand",
    company: "CapitolFin SA",
    industry: "finance",
    company_size: "enterprise",
    personalization_score: 65.8,
    personalization_level: "highly_personalized",
    email_tone: "challenger",
    send_timing: "immediate",
    recommended_action: "refine_and_send",
    predicted_open_rate: 0.41,
    predicted_reply_rate: 0.13,
    send_score: 56.2,
    is_ready_to_send: true,
    personalization_tips: ["Renforcer la pertinence du corps — aligner sur le secteur et le persona"],
    subject_suggestions: [
      "Félicitations pour votre levée — comment accélérer la performance financière",
      "3 leviers pour améliorer la performance financière en Q3",
    ],
    risk_flags: [],
    optimization_score: 61.0,
  },
  {
    prospect_id: "p_007",
    campaign_id: "c_finance_q3",
    rep_id: "rep_001",
    name: "Éric Moulin",
    company: "InvestPro SARL",
    industry: "finance",
    company_size: "smb",
    personalization_score: 35.0,
    personalization_level: "generic",
    email_tone: "educational",
    send_timing: "next_business_day",
    recommended_action: "review_before_send",
    predicted_open_rate: 0.25,
    predicted_reply_rate: 0.04,
    send_score: 36.5,
    is_ready_to_send: false,
    personalization_tips: [
      "Identifier les points de douleur spécifiques au persona",
      "Rechercher un trigger event récent (levée de fonds, recrutement, expansion)",
      "Améliorer la ligne d'objet — viser un score supérieur à 60",
    ],
    subject_suggestions: ["Idée rapide pour la performance financière"],
    risk_flags: [],
    optimization_score: 35.8,
  },
  {
    prospect_id: "p_008",
    campaign_id: "c_retail_q3",
    rep_id: "rep_002",
    name: "Valérie Simon",
    company: "MegaDist SAS",
    industry: "retail",
    company_size: "enterprise",
    personalization_score: 0.0,
    personalization_level: "template",
    email_tone: "educational",
    send_timing: "hold",
    recommended_action: "hold",
    predicted_open_rate: 0.0,
    predicted_reply_rate: 0.0,
    send_score: 0.0,
    is_ready_to_send: false,
    personalization_tips: [],
    subject_suggestions: [],
    risk_flags: ["Prospect opt-out — ne pas contacter"],
    optimization_score: 0.0,
  },
];

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const level  = searchParams.get("level");
  const action = searchParams.get("action");
  const tone   = searchParams.get("tone");

  if (SWARM_API_URL) {
    try {
      const url = new URL(`${SWARM_API_URL}/api/email-personalization`);
      if (level)  url.searchParams.set("level", level);
      if (action) url.searchParams.set("action", action);
      if (tone)   url.searchParams.set("tone", tone);
      const res = await fetch(url.toString(), { cache: "no-store" });
      if (res.ok) return sealResponse(NextResponse.json(await res.json()));
    } catch {}
  }

  let emails = [...mockEmails];
  if (level)  emails = emails.filter((e) => e.personalization_level === level);
  if (action) emails = emails.filter((e) => e.recommended_action === action);
  if (tone)   emails = emails.filter((e) => e.email_tone === tone);

  const level_counts:  Record<string, number> = {};
  const tone_counts:   Record<string, number> = {};
  const timing_counts: Record<string, number> = {};
  const action_counts: Record<string, number> = {};
  let total_p = 0, total_s = 0, total_o = 0, total_r = 0;

  for (const e of mockEmails) {
    level_counts[e.personalization_level]  = (level_counts[e.personalization_level] || 0) + 1;
    tone_counts[e.email_tone]              = (tone_counts[e.email_tone] || 0) + 1;
    timing_counts[e.send_timing]           = (timing_counts[e.send_timing] || 0) + 1;
    action_counts[e.recommended_action]    = (action_counts[e.recommended_action] || 0) + 1;
    total_p += e.personalization_score;
    total_s += e.send_score;
    total_o += e.predicted_open_rate;
    total_r += e.predicted_reply_rate;
  }

  const n = mockEmails.length;

  return sealResponse(NextResponse.json({
    emails,
    summary: {
      total:                       n,
      level_counts,
      tone_counts,
      timing_counts,
      action_counts,
      avg_personalization_score:   Math.round((total_p / n) * 10) / 10,
      avg_send_score:              Math.round((total_s / n) * 10) / 10,
      avg_predicted_open_rate:     Math.round((total_o / n) * 1000) / 1000,
      avg_predicted_reply_rate:    Math.round((total_r / n) * 1000) / 1000,
      ready_to_send_count:         mockEmails.filter((e) => e.is_ready_to_send).length,
      needs_review_count:          mockEmails.filter((e) => e.recommended_action === "review_before_send").length,
      held_count:                  mockEmails.filter((e) => e.recommended_action === "hold").length,
      high_personalization_count:  mockEmails.filter((e) =>
        e.personalization_level === "hyper_personalized" ||
        e.personalization_level === "highly_personalized"
      ).length,
    },
  }));
}
