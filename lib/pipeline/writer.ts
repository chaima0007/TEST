// ─── Agents « Rédacteur » + « Négociateur » (actions) ────────────────────────
//
// Donnent aux agents des ACTIONS au-delà de l'analyse : rédiger une proposition
// sur-mesure et préparer les réponses aux questions de suivi du recruteur.
// La validation reste humaine (l'agent prépare, l'utilisateur envoie).
// Héritage Claude si ANTHROPIC_API_KEY, repli heuristique sinon.

import Anthropic from "@anthropic-ai/sdk";

export interface WriterInput {
  jobTitle: string;
  jobDescription: string;
  budget: number | null;
  freelanceName: string;
  freelanceBio: string;
  commonSkills: string[];
}

export interface Followup {
  question: string;
  answer: string;
}

export interface Dossier {
  proposal: string;
  followups: Followup[];
  generatedBy: "heuristic" | "llm";
}

function heuristicProposal(i: WriterInput): string {
  const skills = i.commonSkills.length ? i.commonSkills.join(", ") : "les compétences requises";
  const budget = i.budget !== null ? ` Le budget annoncé (${i.budget.toLocaleString("fr-FR")} €) correspond à mon positionnement.` : "";
  return [
    `Bonjour,`,
    `Votre mission « ${i.jobTitle} » correspond précisément à mon profil. Je maîtrise ${skills} et j'ai déjà mené des projets similaires.`,
    `${i.freelanceBio} Je peux démarrer rapidement et vous proposer un premier point dès cette semaine.${budget}`,
    `Seriez-vous disponible pour un échange de 15 minutes afin d'en discuter ?`,
    `Bien à vous,\n${i.freelanceName}`,
  ].join("\n\n");
}

function heuristicFollowups(i: WriterInput): Followup[] {
  const skills = i.commonSkills[0] ?? "ce type de mission";
  return [
    { question: "Quelle est votre disponibilité ?", answer: "Je peux démarrer sous quelques jours et réserver le temps nécessaire à la mission." },
    { question: `Avez-vous de l'expérience sur ${skills} ?`, answer: `Oui, c'est au cœur de mon activité ; je peux partager des références sur demande.` },
    { question: "Quel est votre tarif ?", answer: i.budget !== null ? `Mon positionnement est cohérent avec l'enveloppe de ${i.budget.toLocaleString("fr-FR")} € annoncée.` : "Je m'aligne sur le budget de la mission, à préciser ensemble." },
  ];
}

export interface Writer {
  prepare(input: WriterInput): Promise<Dossier>;
}

export class HeuristicWriter implements Writer {
  async prepare(input: WriterInput): Promise<Dossier> {
    return { proposal: heuristicProposal(input), followups: heuristicFollowups(input), generatedBy: "heuristic" };
  }
}

const SCHEMA = {
  type: "object",
  additionalProperties: false,
  properties: {
    proposal: { type: "string" },
    followups: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        properties: { question: { type: "string" }, answer: { type: "string" } },
        required: ["question", "answer"],
      },
    },
  },
  required: ["proposal", "followups"],
} as const;

export class LLMWriter implements Writer {
  private client: Anthropic;
  private fallback = new HeuristicWriter();

  constructor(opts: { apiKey?: string } = {}) {
    this.client = new Anthropic(opts.apiKey ? { apiKey: opts.apiKey } : {});
  }

  async prepare(input: WriterInput): Promise<Dossier> {
    try {
      const response = await this.client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 800,
        system:
          "Tu es un freelance qui répond à une mission. Rédige en français : (1) une proposition courte, professionnelle et personnalisée (pas de blabla générique), (2) 3 questions de suivi probables du recruteur avec une réponse suggérée. Utilise le ton à la première personne.",
        output_config: { format: { type: "json_schema", schema: SCHEMA } },
        messages: [{ role: "user", content: JSON.stringify(input) }],
      } as never);
      const text = response.content
        .filter((b): b is Anthropic.TextBlock => b.type === "text")
        .map((b) => b.text)
        .join("");
      const parsed = JSON.parse(text) as { proposal: string; followups: Followup[] };
      if (!parsed.proposal || !Array.isArray(parsed.followups)) return this.fallback.prepare(input);
      return { proposal: parsed.proposal, followups: parsed.followups, generatedBy: "llm" };
    } catch {
      return this.fallback.prepare(input);
    }
  }
}

export function createWriter(): Writer {
  return process.env.ANTHROPIC_API_KEY ? new LLMWriter() : new HeuristicWriter();
}
