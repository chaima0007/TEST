// ─── Étape 2 (variante LLM) — extraction par Claude ──────────────────────────
//
// Implémentation alternative de `Analyzer` qui délègue l'extraction à Claude
// via le SDK officiel. ACTIVÉE UNIQUEMENT si ANTHROPIC_API_KEY est présent ;
// sinon on retombe sur l'extracteur heuristique (zéro casse, zéro dépendance
// réseau au runtime). Toute erreur (réseau, parsing, quota) → repli heuristique.
//
// Modèle par défaut : claude-opus-4-8. Sortie contrainte par un JSON Schema
// (structured outputs) — pas de prefill, pas de post-traitement fragile.

import Anthropic from "@anthropic-ai/sdk";
import { HeuristicAnalyzer, type Analyzer, type ExtractedFields } from "./analyzer";
import type { RawJobInput } from "./connectors";

const MODEL = "claude-opus-4-8";

// Schéma de sortie : mêmes champs que ExtractedFields.
const OUTPUT_SCHEMA = {
  type: "object",
  additionalProperties: false,
  properties: {
    skills: { type: "array", items: { type: "string" } },
    budget: { type: ["number", "null"] },
    durationDays: { type: ["number", "null"] },
    location: { type: ["string", "null"] },
  },
  required: ["skills", "budget", "durationDays", "location"],
} as const;

const SYSTEM = [
  "Tu extrais des données structurées d'offres de mission freelance.",
  "budget : enveloppe totale estimée en euros (convertis un TJM × durée si besoin), sinon null.",
  "durationDays : durée en jours ouvrés, sinon null.",
  "skills : compétences techniques demandées (libellés canoniques, ex: Next.js, TypeScript, Python, SQL).",
  "location : 'remote' si télétravail, sinon la ville, sinon null.",
].join(" ");

export class LLMAnalyzer implements Analyzer {
  private client: Anthropic;
  private fallback: Analyzer;

  constructor(opts: { apiKey?: string; fallback?: Analyzer } = {}) {
    this.client = new Anthropic(opts.apiKey ? { apiKey: opts.apiKey } : {});
    this.fallback = opts.fallback ?? new HeuristicAnalyzer();
  }

  async extract(job: RawJobInput): Promise<ExtractedFields> {
    try {
      const response = await this.client.messages.create({
        model: MODEL,
        max_tokens: 1024,
        system: SYSTEM,
        output_config: { format: { type: "json_schema", schema: OUTPUT_SCHEMA } },
        messages: [
          {
            role: "user",
            content: `Titre: ${job.title}\nDescription: ${job.description}\nBudget affiché: ${job.rawBudget ?? "(non précisé)"}`,
          },
        ],
      } as never); // `output_config` peut précéder les types du SDK selon la version

      const text = response.content
        .filter((b): b is Anthropic.TextBlock => b.type === "text")
        .map((b) => b.text)
        .join("");
      const parsed = JSON.parse(text) as ExtractedFields;

      // Garde-fou : si la forme est inattendue, on retombe sur l'heuristique.
      if (!Array.isArray(parsed.skills)) return this.fallback.extract(job);
      return {
        skills: parsed.skills,
        budget: typeof parsed.budget === "number" ? parsed.budget : null,
        durationDays: typeof parsed.durationDays === "number" ? parsed.durationDays : null,
        location: typeof parsed.location === "string" ? parsed.location : null,
      };
    } catch {
      return this.fallback.extract(job);
    }
  }
}

/**
 * Choisit l'extracteur selon l'environnement : Claude si ANTHROPIC_API_KEY est
 * présent, sinon l'heuristique déterministe. Point d'entrée unique pour le pipeline.
 */
export function createAnalyzer(): Analyzer {
  if (process.env.ANTHROPIC_API_KEY) {
    return new LLMAnalyzer({ fallback: new HeuristicAnalyzer() });
  }
  return new HeuristicAnalyzer();
}
