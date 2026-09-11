// ─── Agent PACTE — rédacteur de proposition commerciale / devis (Caelum) ─────
//
// PACTE PRÉPARE un devis structuré à partir d'un lead qualifié ; il n'envoie et
// ne signe RIEN. Envoi + signature = strictement humains (§10/§11). Le document
// est RÉDIGÉ en entier (contrat/devis complet), seul l'envoi réel est bloqué.
//
// Sert la PRIORITÉ ACTUELLE : convertir un prospect intéressé en 1er client pour
// l'offre « site web premium » à 500 €. Heuristique déterministe par défaut ;
// rédaction par Claude si ANTHROPIC_API_KEY est présent (repli heuristique).
//
// HONNÊTETÉ DURE (§10/§13) : Caelum n'a PAS encore d'inscription légale ni de
// Stripe. PACTE ne promet jamais de paiement en ligne, ne prétend pas pouvoir
// facturer, et laisse les modalités de facturation « À CONFIRMER » — c'est à
// Chaima de compléter selon son statut réel.

import Anthropic from "@anthropic-ai/sdk";
import { CAELUM_OFFER, type Offer } from "./hermes";

export interface LeadBrief {
  firstName: string;
  company: string;
  sector?: string; // ex : "cabinet d'avocats"
  need?: string; // ce que le prospect a exprimé, ex : "site vitrine + prise de RDV"
  city?: string;
}

export interface Proposal {
  subject: string; // objet du devis
  greeting: string;
  understanding: string; // reformulation du besoin (montre qu'on a écouté)
  scope: string[]; // livrables INCLUS
  outOfScope: string[]; // hors périmètre (honnêteté : ce qui n'est pas compris)
  timeline: string; // délai indicatif
  priceLine: string; // prix formaté
  terms: string[]; // modalités (dont facturation À CONFIRMER)
  nextStep: string; // prochaine étape concrète
  generatedBy: "heuristic" | "llm";
}

// Survente invérifiable + promesses de paiement qu'on ne peut pas tenir
// (Stripe non actif, inscription légale en attente). Déclenche le repli.
const BANNED = [/\bgaranti/i, /\bcertifi/i, /\bmeilleur\b/i, /\bn[°o]\s?1\b/i, /\b100\s?%/];
const BANNED_PAYMENT = [/\bpaiement en ligne\b/i, /\bcarte bancaire\b/i, /\bstripe\b/i, /\bpayez? en ligne\b/i];

function eur(o: Offer): string {
  return `${o.price.toLocaleString("fr-FR")} ${o.currency}`;
}

// Modalités toujours honnêtes : facturation à confirmer selon le statut réel,
// jamais de paiement en ligne tant que Stripe/inscription ne sont pas en place.
function safeTerms(o: Offer): string[] {
  return [
    `Prix forfaitaire : ${eur(o)} (offre « ${o.service} »).`,
    `Modalités de facturation : À CONFIRMER — précisées avant tout engagement (règlement par virement uniquement à ce stade).`,
    `Devis indicatif valable 30 jours à compter de son envoi.`,
    `Un aller-retour de révisions inclus ; au-delà, sur devis complémentaire.`,
  ];
}

function heuristicProposal(l: LeadBrief, o: Offer): Proposal {
  const secteur = l.sector ? ` (${l.sector})` : "";
  const besoin = l.need
    ? `Vous cherchez à ${l.need}.`
    : `Vous souhaitez une présence web claire et efficace pour ${l.company}.`;

  return {
    subject: `Proposition — ${o.service} pour ${l.company}`,
    greeting: `Bonjour ${l.firstName},`,
    understanding: `Merci pour votre temps. ${besoin} Voici une proposition concrète pour ${l.company}${secteur}, pensée pour convertir vos visiteurs en contacts.`,
    scope: [
      `Design sur-mesure (vitrine 3 à 5 sections), adapté à votre image`,
      `Entièrement responsive (mobile, tablette, ordinateur)`,
      `Formulaire de contact relié à votre e-mail`,
      `Mise en ligne + hébergement sécurisé inclus`,
      `Un aller-retour de révisions`,
    ],
    outOfScope: [
      `Rédaction longue de contenu (textes fournis par vos soins, ou en option)`,
      `Boutique en ligne / paiement (non compris dans cette offre)`,
      `Référencement avancé et campagnes publicitaires (en option)`,
      `Maintenance mensuelle (proposée séparément)`,
    ],
    timeline: `Délai indicatif : 1 à 2 semaines après validation et réception de vos contenus.`,
    priceLine: `${eur(o)} — forfait tout compris pour le périmètre ci-dessus.`,
    terms: safeTerms(o),
    nextStep: `Prochaine étape : si cette proposition vous convient, dites-le-moi et nous calons 15 min pour démarrer. Sans engagement d'ici là.`,
    generatedBy: "heuristic",
  };
}

export interface ProposalWriter {
  draft(l: LeadBrief, o?: Offer): Promise<Proposal>;
}

export class HeuristicPacte implements ProposalWriter {
  async draft(l: LeadBrief, o: Offer = CAELUM_OFFER): Promise<Proposal> {
    return heuristicProposal(l, o);
  }
}

const SCHEMA = {
  type: "object",
  additionalProperties: false,
  properties: {
    subject: { type: "string" },
    greeting: { type: "string" },
    understanding: { type: "string" },
    scope: { type: "array", items: { type: "string" } },
    outOfScope: { type: "array", items: { type: "string" } },
    timeline: { type: "string" },
    priceLine: { type: "string" },
    nextStep: { type: "string" },
  },
  required: ["subject", "understanding", "scope", "timeline", "priceLine", "nextStep"],
} as const;

export class LLMPacte implements ProposalWriter {
  private client: Anthropic;
  private fallback = new HeuristicPacte();

  constructor(opts: { apiKey?: string } = {}) {
    this.client = new Anthropic(opts.apiKey ? { apiKey: opts.apiKey } : {});
  }

  async draft(l: LeadBrief, o: Offer = CAELUM_OFFER): Promise<Proposal> {
    try {
      const response = await this.client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 1100,
        system:
          "Tu es Chaima, fondatrice de Caelum Partners. Rédige en français une proposition commerciale (devis) HONNÊTE et concrète pour une offre de site web premium. Montre que tu as compris le besoin, liste des livrables réalistes ET ce qui est hors périmètre. Interdits absolus : superlatifs invérifiables (garanti, certifié, meilleur, n°1, 100%), toute promesse de paiement en ligne / carte / Stripe (non disponibles). Ne prétends pas être une société enregistrée. Reste sobre et factuel.",
        output_config: { format: { type: "json_schema", schema: SCHEMA } },
        messages: [{ role: "user", content: JSON.stringify({ lead: l, offre: o }) }],
      } as never);
      const text = response.content
        .filter((b): b is Anthropic.TextBlock => b.type === "text")
        .map((b) => b.text)
        .join("");
      const parsed = JSON.parse(text) as Partial<Proposal>;
      if (!parsed.subject || !parsed.priceLine || !Array.isArray(parsed.scope)) {
        return this.fallback.draft(l, o);
      }
      // Garde-fous : survente OU promesse de paiement non tenable → repli.
      const all = [
        parsed.subject, parsed.understanding, parsed.timeline, parsed.priceLine, parsed.nextStep,
        ...(parsed.scope ?? []), ...(parsed.outOfScope ?? []),
      ].join("\n");
      if (BANNED.some((re) => re.test(all)) || BANNED_PAYMENT.some((re) => re.test(all))) {
        return this.fallback.draft(l, o);
      }
      return {
        subject: parsed.subject,
        greeting: parsed.greeting ?? `Bonjour ${l.firstName},`,
        understanding: parsed.understanding ?? "",
        scope: parsed.scope ?? [],
        outOfScope: parsed.outOfScope ?? [],
        timeline: parsed.timeline ?? "",
        priceLine: parsed.priceLine,
        // Les modalités (dont facturation À CONFIRMER) restent TOUJOURS les nôtres,
        // jamais générées par le LLM : c'est notre garde-fou légal.
        terms: safeTerms(o),
        nextStep: parsed.nextStep ?? "",
        generatedBy: "llm",
      };
    } catch {
      return this.fallback.draft(l, o);
    }
  }
}

export function createPacte(): ProposalWriter {
  return process.env.ANTHROPIC_API_KEY ? new LLMPacte() : new HeuristicPacte();
}
