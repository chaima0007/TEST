import { NextResponse } from "next/server";

const SWARM_API_URL = process.env.SWARM_API_URL;

interface SubjectVariant { variant_key: string; subject: string }
interface Template {
  template_id: string;
  name: string;
  channel: string;
  description: string;
  tags: string[];
  subject_variants: SubjectVariant[];
  required_variables: string[];
  body_text: string;
  body_html: string;
}

const TEMPLATES: Template[] = [
  {
    template_id: "intro_value",
    name: "Introduction valeur",
    channel: "email",
    description: "Premier contact — présentation de la valeur",
    tags: ["cold", "intro"],
    subject_variants: [
      { variant_key: "A", subject: "Votre site {company_name} perd du trafic chaque jour" },
      { variant_key: "B", subject: "J'ai analysé le site de {company_name}" },
      { variant_key: "C", subject: "Score PageSpeed : {pagespeed}/100 — on peut faire mieux" },
    ],
    required_variables: ["contact_name", "company_name", "sector", "pagespeed", "revenue_loss", "agent_name"],
    body_text:
      "Bonjour {contact_name},\n\nEn analysant les sites dans le secteur {sector}, j'ai remarqué que {company_name} obtient un score PageSpeed de {pagespeed}/100 — ce qui représente une perte estimée de {revenue_loss}€/mois en trafic organique non capté.\n\nEn 5 jours ouvrés, nous pouvons corriger les points critiques et améliorer votre positionnement Google.\n\nAvez-vous 15 minutes cette semaine pour en discuter ?\n\nCordialement,\n{agent_name}",
    body_html:
      "<p>Bonjour <strong>{contact_name}</strong>,</p><p>En analysant les sites dans le secteur <em>{sector}</em>, j'ai remarqué que <strong>{company_name}</strong> obtient un score PageSpeed de <strong>{pagespeed}/100</strong> — ce qui représente une perte estimée de <strong>{revenue_loss}€/mois</strong> en trafic organique non capté.</p><p>En 5 jours ouvrés, nous pouvons corriger les points critiques et améliorer votre positionnement Google.</p><p>Avez-vous 15 minutes cette semaine pour en discuter ?</p><p>Cordialement,<br><strong>{agent_name}</strong></p>",
  },
  {
    template_id: "follow_up_1",
    name: "Relance 1",
    channel: "email",
    description: "Première relance après intro sans réponse",
    tags: ["cold", "followup"],
    subject_variants: [
      { variant_key: "A", subject: "Re: {company_name} — avez-vous vu mon message ?" },
      { variant_key: "B", subject: "Une question rapide sur votre site" },
      { variant_key: "C", subject: "Votre concurrent a déjà agi — et vous ?" },
    ],
    required_variables: ["contact_name", "company_name", "agent_name"],
    body_text:
      "Bonjour {contact_name},\n\nJe me permets de revenir vers vous concernant {company_name}.\n\nUn concurrent dans votre secteur vient d'améliorer son score de 18 points et capte désormais les recherches que vous manquez.\n\nVoulez-vous que je vous envoie l'analyse comparative gratuitement ?\n\nBonne journée,\n{agent_name}",
    body_html:
      "<p>Bonjour <strong>{contact_name}</strong>,</p><p>Je me permets de revenir vers vous concernant <strong>{company_name}</strong>.</p><p>Un concurrent dans votre secteur vient d'améliorer son score de 18 points et capte désormais les recherches que vous manquez.</p><p>Voulez-vous que je vous envoie l'analyse comparative gratuitement ?</p><p>Bonne journée,<br><strong>{agent_name}</strong></p>",
  },
  {
    template_id: "social_proof",
    name: "Preuve sociale",
    channel: "email",
    description: "Troisième touch — cas client similaire",
    tags: ["cold", "social_proof"],
    subject_variants: [
      { variant_key: "A", subject: "Comment {case_company} a gagné +{case_traffic}% de trafic en 30 jours" },
    ],
    required_variables: ["contact_name", "case_company", "sector", "case_traffic", "case_leads", "company_name", "agent_name"],
    body_text:
      "Bonjour {contact_name},\n\n{case_company}, actif dans le secteur {sector} comme vous, a vu son trafic organique augmenter de {case_traffic}% en 30 jours après optimisation PageSpeed et mobile.\n\nRésultat : +{case_leads} leads supplémentaires par mois.\n\nJe serais ravi de vous préparer une projection similaire pour {company_name}.\n\nCordialement,\n{agent_name}",
    body_html:
      "<p>Bonjour <strong>{contact_name}</strong>,</p><p><strong>{case_company}</strong>, actif dans le secteur <em>{sector}</em> comme vous, a vu son trafic organique augmenter de <strong>{case_traffic}%</strong> en 30 jours après optimisation PageSpeed et mobile.</p><p>Résultat : <strong>+{case_leads} leads supplémentaires</strong> par mois.</p><p>Je serais ravi de vous préparer une projection similaire pour <strong>{company_name}</strong>.</p><p>Cordialement,<br><strong>{agent_name}</strong></p>",
  },
  {
    template_id: "urgency_close",
    name: "Clôture urgence",
    channel: "email",
    description: "Avant-dernière relance avec angle urgence",
    tags: ["cold", "urgency"],
    subject_variants: [
      { variant_key: "A", subject: "Dernière chance : offre limitée pour {company_name}" },
      { variant_key: "C", subject: "Je ferme votre dossier vendredi — un mot avant ?" },
    ],
    required_variables: ["contact_name", "company_name", "agent_name"],
    body_text:
      "Bonjour {contact_name},\n\nJe m'apprête à clore le dossier {company_name} cette semaine.\n\nAvant cela, je voulais vous signaler que l'offre tarifaire que je vous avais préparée expire vendredi. Après cette date, les délais de livraison seront allongés à 3 semaines.\n\nUn simple 'oui' ou 'non' me suffit.\n\n{agent_name}",
    body_html:
      "<p>Bonjour <strong>{contact_name}</strong>,</p><p>Je m'apprête à clore le dossier <strong>{company_name}</strong> cette semaine.</p><p>Avant cela, je voulais vous signaler que l'offre tarifaire que je vous avais préparée expire <strong>vendredi</strong>. Après cette date, les délais de livraison seront allongés à 3 semaines.</p><p>Un simple 'oui' ou 'non' me suffit.</p><p><strong>{agent_name}</strong></p>",
  },
  {
    template_id: "breakup",
    name: "Breakup email",
    channel: "email",
    description: "Dernier message — fermeture du dossier",
    tags: ["cold", "breakup"],
    subject_variants: [{ variant_key: "A", subject: "Je ferme votre dossier" }],
    required_variables: ["contact_name", "agent_name"],
    body_text:
      "Bonjour {contact_name},\n\nN'ayant pas eu de retour de votre part, je ferme votre dossier.\n\nSi votre situation évolue et que vous souhaitez optimiser votre présence en ligne, n'hésitez pas à me contacter.\n\nBonne continuation,\n{agent_name}",
    body_html:
      "<p>Bonjour <strong>{contact_name}</strong>,</p><p>N'ayant pas eu de retour de votre part, je ferme votre dossier.</p><p>Si votre situation évolue et que vous souhaitez optimiser votre présence en ligne, n'hésitez pas à me contacter.</p><p>Bonne continuation,<br><strong>{agent_name}</strong></p>",
  },
  {
    template_id: "demo_offer",
    name: "Offre de démo",
    channel: "email",
    description: "Proposition de démo personnalisée",
    tags: ["warm", "demo"],
    subject_variants: [{ variant_key: "A", subject: "Démo personnalisée pour {company_name} — 20 minutes" }],
    required_variables: ["contact_name", "company_name", "agent_name"],
    body_text:
      "Bonjour {contact_name},\n\nJe vous propose une démo personnalisée de 20 minutes pour {company_name}.\n\nAu programme :\n• Audit live de votre site\n• Comparaison avec 3 concurrents\n• Plan d'action chiffré\n\nQuel créneau vous conviendrait cette semaine ou la suivante ?\n\n{agent_name}",
    body_html:
      "<p>Bonjour <strong>{contact_name}</strong>,</p><p>Je vous propose une démo personnalisée de 20 minutes pour <strong>{company_name}</strong>.</p><ul><li>Audit live de votre site</li><li>Comparaison avec 3 concurrents</li><li>Plan d'action chiffré</li></ul><p>Quel créneau vous conviendrait cette semaine ou la suivante ?</p><p><strong>{agent_name}</strong></p>",
  },
  {
    template_id: "quote_reminder",
    name: "Rappel devis",
    channel: "email",
    description: "Relance après envoi du devis",
    tags: ["post_quote"],
    subject_variants: [{ variant_key: "A", subject: "Votre devis {company_name} — avez-vous des questions ?" }],
    required_variables: ["contact_name", "company_name", "quote_total", "agent_name"],
    body_text:
      "Bonjour {contact_name},\n\nJe reviens vers vous au sujet du devis envoyé pour {company_name} ({quote_total}€ TTC).\n\nAvez-vous eu le temps d'en prendre connaissance ? Je suis disponible pour répondre à toute question.\n\n{agent_name}",
    body_html:
      "<p>Bonjour <strong>{contact_name}</strong>,</p><p>Je reviens vers vous au sujet du devis envoyé pour <strong>{company_name}</strong> (<strong>{quote_total}€ TTC</strong>).</p><p>Avez-vous eu le temps d'en prendre connaissance ? Je suis disponible pour répondre à toute question.</p><p><strong>{agent_name}</strong></p>",
  },
];

function substitute(text: string, vars: Record<string, string>): string {
  return text.replace(/\{(\w+)\}/g, (match, key) => vars[key] ?? match);
}

function getTemplate(id: string) {
  return TEMPLATES.find((t) => t.template_id === id) ?? null;
}

export async function GET() {
  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/templates`, { cache: "no-store" });
      if (res.ok) return NextResponse.json(await res.json());
    } catch { /* fall through */ }
  }
  return NextResponse.json({ templates: TEMPLATES });
}

export async function POST(request: Request) {
  const body = await request.json();
  const { template_id, variables = {}, variant_key = "A" } = body;

  if (SWARM_API_URL) {
    try {
      const res = await fetch(`${SWARM_API_URL}/templates/render`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ template_id, variables, variant_key }),
        cache: "no-store",
      });
      if (res.ok) return NextResponse.json(await res.json());
    } catch { /* fall through */ }
  }

  const tmpl = getTemplate(template_id);
  if (!tmpl) {
    return NextResponse.json({ error: `Template '${template_id}' not found` }, { status: 404 });
  }

  const subjectVariant = tmpl.subject_variants.find((v) => v.variant_key === variant_key)
    ?? tmpl.subject_variants[0];

  const subject   = substitute(subjectVariant?.subject ?? "", variables);
  const body_text = substitute(tmpl.body_text, variables);
  const body_html = substitute(tmpl.body_html, variables);

  const missing = tmpl.required_variables.filter((v) => !(v in variables));

  return NextResponse.json({
    template_id,
    variant_key,
    subject,
    body_text,
    body_html,
    channel: tmpl.channel,
    is_complete: missing.length === 0,
    missing_vars: missing,
  });
}
