import { NextResponse } from "next/server";
import { sealResponse } from "@/lib/digital-seal";

if (!process.env.SWARM_API_URL) {
  console.warn("[templates] SWARM_API_URL non défini — mode local");
}

interface SubjectVariant {
  variant_key: string;
  subject: string;
}

interface TemplateStats {
  renders: number;
  sends: number;
  opens: number;
  clicks: number;
  replies: number;
  open_rate_pct: number;
  click_rate_pct: number;
  reply_rate_pct: number;
}

interface Template {
  template_id: string;
  name: string;
  channel: "email" | "sms" | "linkedin";
  description: string;
  tags: string[];
  subject_variants: SubjectVariant[];
  required_variables: string[];
  stats: TemplateStats;
}

const TEMPLATES: Template[] = [
  {
    template_id: "intro_value",
    name: "Introduction valeur",
    channel: "email",
    description: "Premier contact cold — met en avant la perte de trafic mesurée sur le site du prospect.",
    tags: ["cold", "intro"],
    subject_variants: [
      { variant_key: "A", subject: "Votre site {company_name} perd du trafic chaque jour" },
      { variant_key: "B", subject: "J'ai analysé le site de {company_name}" },
      { variant_key: "C", subject: "Score PageSpeed : {pagespeed}/100 — on peut faire mieux" },
    ],
    required_variables: ["contact_name", "company_name", "sector", "pagespeed", "revenue_loss", "agent_name"],
    stats: {
      renders: 842,
      sends: 624,
      opens: 312,
      clicks: 87,
      replies: 156,
      open_rate_pct: 50.0,
      click_rate_pct: 13.9,
      reply_rate_pct: 25.0,
    },
  },
  {
    template_id: "follow_up_1",
    name: "Relance 1",
    channel: "email",
    description: "Première relance après intro sans réponse — rappel concis de la valeur proposée.",
    tags: ["cold", "followup"],
    subject_variants: [
      { variant_key: "A", subject: "Suite à mon email sur {company_name}" },
      { variant_key: "B", subject: "Toujours intéressé par {company_name} ?" },
      { variant_key: "C", subject: "Re: Analyse de {company_name}" },
    ],
    required_variables: ["contact_name", "company_name", "agent_name"],
    stats: {
      renders: 612,
      sends: 498,
      opens: 189,
      clicks: 44,
      replies: 89,
      open_rate_pct: 37.9,
      click_rate_pct: 8.8,
      reply_rate_pct: 17.9,
    },
  },
  {
    template_id: "social_proof",
    name: "Preuve sociale",
    channel: "email",
    description: "Cas client similaire pour rassurer — résultats chiffrés dans le même secteur.",
    tags: ["cold", "social_proof"],
    subject_variants: [
      { variant_key: "A", subject: "Ce que {case_company} a réussi en 90 jours" },
      { variant_key: "B", subject: "+{case_traffic} visiteurs/mois — même secteur que vous" },
      { variant_key: "C", subject: "Comment {case_company} a généré {case_leads} leads" },
    ],
    required_variables: ["contact_name", "case_company", "sector", "case_traffic", "case_leads", "company_name", "agent_name"],
    stats: {
      renders: 287,
      sends: 231,
      opens: 124,
      clicks: 39,
      replies: 62,
      open_rate_pct: 53.7,
      click_rate_pct: 16.9,
      reply_rate_pct: 26.8,
    },
  },
  {
    template_id: "urgency_close",
    name: "Clôture urgence",
    channel: "email",
    description: "Clôture avec élément de rareté — crée une urgence douce sans être agressif.",
    tags: ["cold", "urgency"],
    subject_variants: [
      { variant_key: "A", subject: "Dernière disponibilité ce mois-ci" },
      { variant_key: "B", subject: "On ferme notre agenda vendredi" },
      { variant_key: "C", subject: "Une opportunité à ne pas rater pour {company_name}" },
    ],
    required_variables: ["contact_name", "company_name", "agent_name"],
    stats: {
      renders: 198,
      sends: 176,
      opens: 105,
      clicks: 28,
      replies: 44,
      open_rate_pct: 59.7,
      click_rate_pct: 15.9,
      reply_rate_pct: 25.0,
    },
  },
  {
    template_id: "breakup",
    name: "Breakup email",
    channel: "email",
    description: "Dernier email de la séquence cold — laisse la porte ouverte sans pression.",
    tags: ["cold", "breakup"],
    subject_variants: [
      { variant_key: "A", subject: "Je vous laisse tranquille après ça" },
      { variant_key: "B", subject: "C'est mon dernier email" },
      { variant_key: "C", subject: "On se dit au revoir ?" },
    ],
    required_variables: ["contact_name", "agent_name"],
    stats: {
      renders: 145,
      sends: 132,
      opens: 92,
      clicks: 8,
      replies: 18,
      open_rate_pct: 69.7,
      click_rate_pct: 6.1,
      reply_rate_pct: 13.6,
    },
  },
  {
    template_id: "warm_check_in",
    name: "Check-in prospect chaud",
    channel: "email",
    description: "Réactivation d'un prospect ayant montré de l'intérêt — ton conversationnel.",
    tags: ["warm", "reactivation"],
    subject_variants: [
      { variant_key: "A", subject: "Des nouvelles de {company_name} ?" },
      { variant_key: "B", subject: "On reprend là où on s'était arrêtés ?" },
      { variant_key: "C", subject: "Toujours un projet d'optimisation chez {company_name} ?" },
    ],
    required_variables: ["contact_name", "company_name", "agent_name"],
    stats: {
      renders: 203,
      sends: 178,
      opens: 112,
      clicks: 34,
      replies: 71,
      open_rate_pct: 62.9,
      click_rate_pct: 19.1,
      reply_rate_pct: 39.9,
    },
  },
  {
    template_id: "case_study",
    name: "Cas client",
    channel: "email",
    description: "Étude de cas approfondie pour prospect chaud — résultats détaillés avec gains SEO et leads.",
    tags: ["warm", "social_proof"],
    subject_variants: [
      { variant_key: "A", subject: "Étude de cas : {case_company} — {case_pagespeed_gain} points PageSpeed" },
      { variant_key: "B", subject: "Comment {case_company} a explosé ses leads en {sector}" },
      { variant_key: "C", subject: "+{case_traffic} visiteurs — voilà comment on l'a fait" },
    ],
    required_variables: ["contact_name", "case_company", "sector", "case_pagespeed_gain", "case_traffic", "case_leads", "company_name", "agent_name"],
    stats: {
      renders: 167,
      sends: 148,
      opens: 98,
      clicks: 42,
      replies: 67,
      open_rate_pct: 66.2,
      click_rate_pct: 28.4,
      reply_rate_pct: 45.3,
    },
  },
  {
    template_id: "demo_offer",
    name: "Offre de démo",
    channel: "email",
    description: "Proposition de démonstration personnalisée — faible friction, haut impact.",
    tags: ["warm", "demo"],
    subject_variants: [
      { variant_key: "A", subject: "20 min pour vous montrer ce qu'on ferait pour {company_name}" },
      { variant_key: "B", subject: "Démo gratuite — résultats concrets pour {company_name}" },
      { variant_key: "C", subject: "Je réserve un créneau pour {company_name} ?" },
    ],
    required_variables: ["contact_name", "company_name", "agent_name"],
    stats: {
      renders: 134,
      sends: 119,
      opens: 82,
      clicks: 51,
      replies: 58,
      open_rate_pct: 68.9,
      click_rate_pct: 42.9,
      reply_rate_pct: 48.7,
    },
  },
  {
    template_id: "quote_reminder",
    name: "Rappel devis",
    channel: "email",
    description: "Rappel doux après envoi d'un devis — lève les blocages sans pression.",
    tags: ["post_quote"],
    subject_variants: [
      { variant_key: "A", subject: "Votre devis {quote_total}€ — des questions ?" },
      { variant_key: "B", subject: "Suite à votre devis pour {company_name}" },
      { variant_key: "C", subject: "On valide le devis ensemble ?" },
    ],
    required_variables: ["contact_name", "company_name", "quote_total", "agent_name"],
    stats: {
      renders: 89,
      sends: 78,
      opens: 56,
      clicks: 21,
      replies: 38,
      open_rate_pct: 71.8,
      click_rate_pct: 26.9,
      reply_rate_pct: 48.7,
    },
  },
  {
    template_id: "objection_faq",
    name: "FAQ objections",
    channel: "email",
    description: "Réponses aux objections courantes post-devis — rassure et lève les freins.",
    tags: ["post_quote", "objection"],
    subject_variants: [
      { variant_key: "A", subject: "Les 3 questions qu'on nous pose toujours" },
      { variant_key: "B", subject: "Vos doutes — nos réponses" },
      { variant_key: "C", subject: "Ce que nos clients se demandaient avant de signer" },
    ],
    required_variables: ["contact_name", "agent_name"],
    stats: {
      renders: 67,
      sends: 58,
      opens: 42,
      clicks: 16,
      replies: 28,
      open_rate_pct: 72.4,
      click_rate_pct: 27.6,
      reply_rate_pct: 48.3,
    },
  },
  {
    template_id: "final_offer",
    name: "Offre finale",
    channel: "email",
    description: "Dernière proposition avec avantage exceptionnel — crée l'urgence de décision.",
    tags: ["post_quote", "urgency"],
    subject_variants: [
      { variant_key: "A", subject: "Offre spéciale {company_name} — valable 48h" },
      { variant_key: "B", subject: "Dernière chance : {quote_total}€ avec bonus inclus" },
      { variant_key: "C", subject: "On fait un geste pour {company_name} — décision ce vendredi" },
    ],
    required_variables: ["contact_name", "company_name", "quote_total", "agent_name"],
    stats: {
      renders: 112,
      sends: 98,
      opens: 74,
      clicks: 19,
      replies: 29,
      open_rate_pct: 75.5,
      click_rate_pct: 19.4,
      reply_rate_pct: 29.6,
    },
  },
];

export async function GET() {
  try {
    const totalSends = TEMPLATES.reduce((s, t) => s + t.stats.sends, 0);
    const totalOpens = TEMPLATES.reduce((s, t) => s + t.stats.opens, 0);
    const totalClicks = TEMPLATES.reduce((s, t) => s + t.stats.clicks, 0);
    const totalReplies = TEMPLATES.reduce((s, t) => s + t.stats.replies, 0);

    const avgOpenRate =
      Math.round(
        (TEMPLATES.reduce((s, t) => s + t.stats.open_rate_pct, 0) / TEMPLATES.length) * 10
      ) / 10;
    const avgReplyRate =
      Math.round(
        (TEMPLATES.reduce((s, t) => s + t.stats.reply_rate_pct, 0) / TEMPLATES.length) * 10
      ) / 10;

    const topTemplate = TEMPLATES.reduce((best, t) =>
      t.stats.reply_rate_pct > best.stats.reply_rate_pct ? t : best
    ).template_id;

    const byTag: Record<string, number> = {};
    for (const t of TEMPLATES) {
      for (const tag of t.tags) {
        byTag[tag] = (byTag[tag] ?? 0) + 1;
      }
    }

    return NextResponse.json(sealResponse({
      templates: TEMPLATES,
      summary: {
        templates_count: 11,
        total_sends: totalSends,
        total_opens: totalOpens,
        total_clicks: totalClicks,
        total_replies: totalReplies,
        avg_open_rate_pct: avgOpenRate,
        avg_reply_rate_pct: avgReplyRate,
        top_template: topTemplate,
      },
      by_tag: byTag,
    }));
  } catch {
    return NextResponse.json(sealResponse({ error: "upstream error" }), { status: 502 });
  }
}
