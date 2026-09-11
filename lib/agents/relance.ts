// ─── Agent RELANCE — relance de devis / proposition (Caelum) ─────────────────
//
// RELANCE PRÉPARE une séquence de relance APRÈS l'envoi d'un devis (PACTE) resté
// sans réponse. Il n'envoie RIEN : envoi MANUEL par Chaima après relecture (§10).
// Distinct de HERMES (qui relance un premier message froid) : ici la proposition
// est déjà chaude et chiffrée.
//
// Principe : relancer sans harceler. Séquence courte et espacée (J+3 / J+7 /
// clôture), adaptée à l'objection éventuelle, et une CLÔTURE POLIE qui rend la
// main au prospect. Aucune fausse urgence, aucune survente (§13), aucune remise
// inventée (on propose de réduire le périmètre, pas de casser un prix au hasard).
//
// Heuristique déterministe par défaut ; rédaction par Claude si ANTHROPIC_API_KEY
// est présent (repli heuristique en cas d'absence/erreur).

import Anthropic from "@anthropic-ai/sdk";
import { CAELUM_OFFER, type Offer } from "./hermes";

export type Objection = "price" | "timing" | "trust" | "none";

export interface PendingQuote {
  firstName: string;
  company: string;
  service?: string; // défaut : offre Caelum
  objection?: Objection; // ce que le prospect a évoqué, s'il a répondu
  city?: string;
}

export interface FollowUp {
  label: string; // ex : "J+3", "J+7", "J+14 — clôture"
  body: string;
}

export interface FollowUpSequence {
  messages: FollowUp[];
  generatedBy: "heuristic" | "llm";
}

// Survente invérifiable + fausse urgence (PROTOCOLE §13). Déclenche le repli.
const BANNED = [
  /\bgaranti/i,
  /\bcertifi/i,
  /\bmeilleur\b/i,
  /\bn[°o]\s?1\b/i,
  /\b100\s?%/,
  /\bderni[èe]re chance\b/i,
  /\boffre expire\b/i,
];

// Message J+7 adapté à l'objection — honnête, sans casser le prix au hasard.
function objectionBody(p: PendingQuote, service: string): string {
  switch (p.objection) {
    case "price":
      return `Je comprends que le budget compte. On peut réduire le périmètre (par exemple démarrer avec l'essentiel) pour rester dans votre enveloppe — dites-moi ce qui vous conviendrait.`;
    case "timing":
      return `Si le moment n'est pas idéal, aucun souci : je garde la proposition au chaud et je reviens vers vous quand vous le souhaitez.`;
    case "trust":
      return `Je peux vous montrer concrètement ce que donnerait votre ${service} pour ${p.company}, sans engagement, pour que vous puissiez juger sur pièce.`;
    default:
      return `Petite relance : je reste disponible pour un échange de 15 min si c'est utile, ou pour ajuster la proposition à vos besoins.`;
  }
}

function heuristicSequence(p: PendingQuote, o: Offer): FollowUpSequence {
  const service = p.service ?? o.service;
  const messages: FollowUp[] = [
    {
      label: "J+3",
      body: [
        `Bonjour ${p.firstName},`,
        `Je reviens vers vous au sujet de la proposition pour votre ${service}. Avez-vous des questions ?`,
        `Je peux tout à fait l'ajuster si besoin. Belle journée !`,
      ].join("\n\n"),
    },
    {
      label: "J+7",
      body: [`Bonjour ${p.firstName},`, objectionBody(p, service)].join("\n\n"),
    },
    {
      label: "J+14 — clôture",
      body: [
        `Bonjour ${p.firstName},`,
        `Sans nouvelles, je clos le dossier pour ne pas vous encombrer.`,
        `Si le projet redevient d'actualité, un mot suffit et ce sera un plaisir de reprendre. Belle continuation à ${p.company} !`,
      ].join("\n\n"),
    },
  ];
  return { messages, generatedBy: "heuristic" };
}

export interface SequenceWriter {
  draft(p: PendingQuote, o?: Offer): Promise<FollowUpSequence>;
}

export class HeuristicRelance implements SequenceWriter {
  async draft(p: PendingQuote, o: Offer = CAELUM_OFFER): Promise<FollowUpSequence> {
    return heuristicSequence(p, o);
  }
}

const SCHEMA = {
  type: "object",
  additionalProperties: false,
  properties: {
    messages: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        properties: { label: { type: "string" }, body: { type: "string" } },
        required: ["label", "body"],
      },
    },
  },
  required: ["messages"],
} as const;

export class LLMRelance implements SequenceWriter {
  private client: Anthropic;
  private fallback = new HeuristicRelance();

  constructor(opts: { apiKey?: string } = {}) {
    this.client = new Anthropic(opts.apiKey ? { apiKey: opts.apiKey } : {});
  }

  async draft(p: PendingQuote, o: Offer = CAELUM_OFFER): Promise<FollowUpSequence> {
    try {
      const response = await this.client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 900,
        system:
          "Tu es Chaima, fondatrice de Caelum Partners. Rédige en français une séquence COURTE de relance après un devis resté sans réponse : un rappel léger (J+3), un message adapté à l'objection (J+7), puis une clôture polie qui rend la main au prospect (J+14). Relancer sans harceler. Interdits absolus : fausse urgence (« dernière chance », « offre expire »), superlatifs invérifiables (garanti, certifié, meilleur, n°1, 100%), remise chiffrée inventée. Reste chaleureuse, brève, respectueuse.",
        output_config: { format: { type: "json_schema", schema: SCHEMA } },
        messages: [{ role: "user", content: JSON.stringify({ devis: p, offre: o }) }],
      } as never);
      const text = response.content
        .filter((b): b is Anthropic.TextBlock => b.type === "text")
        .map((b) => b.text)
        .join("");
      const parsed = JSON.parse(text) as { messages?: FollowUp[] };
      if (!Array.isArray(parsed.messages) || parsed.messages.length === 0) {
        return this.fallback.draft(p, o);
      }
      const all = parsed.messages.map((m) => `${m.label}\n${m.body}`).join("\n");
      if (BANNED.some((re) => re.test(all))) return this.fallback.draft(p, o);
      return { messages: parsed.messages, generatedBy: "llm" };
    } catch {
      return this.fallback.draft(p, o);
    }
  }
}

export function createRelance(): SequenceWriter {
  return process.env.ANTHROPIC_API_KEY ? new LLMRelance() : new HeuristicRelance();
}
