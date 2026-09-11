// ─── Agent HERMES — brouillons de prospection LinkedIn (Caelum) ──────────────
//
// HERMES PRÉPARE des messages de prospection sur-mesure ; il n'envoie RIEN.
// Envoi MANUEL uniquement par Chaima après relecture (§10). Aucune automatisation,
// aucun scraping LinkedIn (contraire aux CGU + RGPD, cf. PROTOCOLE CODEX §3).
//
// Sert la PRIORITÉ ACTUELLE : décrocher le 1er client pour l'offre « site web
// premium » à 500€. Heuristique déterministe par défaut ; rédaction par Claude
// si ANTHROPIC_API_KEY est présent (repli heuristique en cas d'absence/erreur).

import Anthropic from "@anthropic-ai/sdk";

export interface Prospect {
  firstName: string;
  company: string;
  sector?: string; // ex : "cabinet d'avocats", "restaurant", "kiné"
  signal?: string; // ex : "pas de site", "site lent et daté", "aucune prise de RDV en ligne"
  city?: string;
}

export interface Offer {
  service: string;
  price: number;
  currency: string;
  edge: string;
}

export const CAELUM_OFFER: Offer = {
  service: "site web premium",
  price: 500,
  currency: "€",
  edge: "design sur-mesure, mise en ligne rapide, hébergement sécurisé inclus",
};

export interface OutreachDraft {
  connectionNote: string; // note de demande de connexion (bornée, cf. NOTE_CAP)
  altConnectionNote: string; // variante A/B
  firstMessage: string; // 1er message après acceptation
  followUp: string; // relance si pas de réponse
  generatedBy: "heuristic" | "llm";
}

// Borne conservatrice pour la note de connexion. NON VÉRIFIÉ : la limite exacte
// imposée par LinkedIn varie ; on reste volontairement en dessous.
export const NOTE_CAP = 280;

// Termes bannis : affirmations « sur nous » non sourçables / survente (PROTOCOLE §13).
const BANNED = [/\bgaranti/i, /\bcertifi/i, /\bmeilleur\b/i, /\bn[°o]\s?1\b/i, /\b100\s?%/];

function trimTo(s: string, cap: number): string {
  if (s.length <= cap) return s;
  return s.slice(0, cap - 1).trimEnd() + "…";
}

function eur(o: Offer): string {
  return `${o.price.toLocaleString("fr-FR")} ${o.currency}`;
}

function heuristicDraft(p: Prospect, o: Offer): OutreachDraft {
  const secteur = p.sector ? ` dans ${p.sector}` : "";
  const constat = p.signal
    ? `J'ai remarqué un point concret côté web (${p.signal}).`
    : `Je vois un vrai potentiel côté présence web.`;

  const connectionNote = trimTo(
    `Bonjour ${p.firstName}, je découvre ${p.company}${secteur}. J'accompagne des indépendants et TPE sur leur ${o.service}. Ravie d'échanger si le sujet vous parle.`,
    NOTE_CAP,
  );
  const altConnectionNote = trimTo(
    `Bonjour ${p.firstName}, ${constat} J'aide des structures comme ${p.company} à avoir un ${o.service} clair et efficace. Au plaisir de connecter.`,
    NOTE_CAP,
  );
  const firstMessage = [
    `Merci d'avoir accepté, ${p.firstName} !`,
    `${constat} Chez Caelum Partners, je conçois votre ${o.service} (${o.edge}) à partir de ${eur(o)}, pensé pour convertir.`,
    `Est-ce que 15 minutes cette semaine vous conviendraient pour voir si ça a du sens pour ${p.company} ? Sans engagement.`,
  ].join("\n\n");
  const followUp = [
    `Bonjour ${p.firstName}, je me permets un petit rappel — sans vouloir insister.`,
    `Si un ${o.service} à ${eur(o)} n'est pas d'actualité, aucun souci ; dites-le-moi et je n'en reparle plus.`,
    `Sinon, je vous montre en 15 min ce que ça donnerait pour ${p.company}. Belle journée !`,
  ].join("\n\n");

  return { connectionNote, altConnectionNote, firstMessage, followUp, generatedBy: "heuristic" };
}

export interface Writer {
  draft(p: Prospect, o?: Offer): Promise<OutreachDraft>;
}

export class HeuristicHermes implements Writer {
  async draft(p: Prospect, o: Offer = CAELUM_OFFER): Promise<OutreachDraft> {
    return heuristicDraft(p, o);
  }
}

const SCHEMA = {
  type: "object",
  additionalProperties: false,
  properties: {
    connectionNote: { type: "string" },
    altConnectionNote: { type: "string" },
    firstMessage: { type: "string" },
    followUp: { type: "string" },
  },
  required: ["connectionNote", "altConnectionNote", "firstMessage", "followUp"],
} as const;

export class LLMHermes implements Writer {
  private client: Anthropic;
  private fallback = new HeuristicHermes();

  constructor(opts: { apiKey?: string } = {}) {
    this.client = new Anthropic(opts.apiKey ? { apiKey: opts.apiKey } : {});
  }

  async draft(p: Prospect, o: Offer = CAELUM_OFFER): Promise<OutreachDraft> {
    try {
      const response = await this.client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 900,
        system:
          "Tu es Chaima, fondatrice de Caelum Partners. Rédige en français une séquence de prospection LinkedIn HONNÊTE et non-spammy : note de connexion (courte), une variante A/B, un premier message après acceptation, une relance polie. Personnalise avec les infos du prospect. Interdits : superlatifs invérifiables (garanti, certifié, meilleur, n°1, 100%), fausse urgence, flatterie creuse. Propose un échange de 15 min sans engagement.",
        output_config: { format: { type: "json_schema", schema: SCHEMA } },
        messages: [{ role: "user", content: JSON.stringify({ prospect: p, offre: o, note_cap: NOTE_CAP }) }],
      } as never);
      const text = response.content
        .filter((b): b is Anthropic.TextBlock => b.type === "text")
        .map((b) => b.text)
        .join("");
      const parsed = JSON.parse(text) as Omit<OutreachDraft, "generatedBy">;
      if (!parsed.connectionNote || !parsed.firstMessage) return this.fallback.draft(p, o);
      // Garde-fous : borne la note, rejette la survente → repli si non conforme.
      const note = trimTo(parsed.connectionNote, NOTE_CAP);
      const all = [note, parsed.altConnectionNote, parsed.firstMessage, parsed.followUp].join("\n");
      if (BANNED.some((re) => re.test(all))) return this.fallback.draft(p, o);
      return {
        connectionNote: note,
        altConnectionNote: trimTo(parsed.altConnectionNote ?? "", NOTE_CAP),
        firstMessage: parsed.firstMessage,
        followUp: parsed.followUp ?? "",
        generatedBy: "llm",
      };
    } catch {
      return this.fallback.draft(p, o);
    }
  }
}

export function createHermes(): Writer {
  return process.env.ANTHROPIC_API_KEY ? new LLMHermes() : new HeuristicHermes();
}
