// ─── Étape 2 — Extraction (Analyzer) ─────────────────────────────────────────
//
// Extrait des entités structurées (budget, compétences, durée, lieu) à partir
// du texte brut d'une offre. La V1 utilise un extracteur HEURISTIQUE
// déterministe — pas de LLM, donc pas de clé API, testable et reproductible.
// Pour brancher un vrai LLM plus tard, il suffit d'implémenter `Analyzer`.

import type { RawJobInput } from "./connectors";

export interface ExtractedFields {
  skills: string[];
  /** Budget total estimé en euros, ou null si introuvable. */
  budget: number | null;
  durationDays: number | null;
  location: string | null;
}

export interface Analyzer {
  extract(job: RawJobInput): ExtractedFields;
}

// Dictionnaire de compétences reconnues → libellé canonique.
const SKILL_KEYWORDS: Record<string, string> = {
  "next.js": "Next.js",
  nextjs: "Next.js",
  typescript: "TypeScript",
  javascript: "JavaScript",
  react: "React",
  tailwind: "Tailwind",
  prisma: "Prisma",
  node: "Node.js",
  python: "Python",
  sql: "SQL",
  dbt: "dbt",
  figma: "Figma",
  design: "Design",
};

/** Convertit une chaîne "12 000", "12k", "1 200,50" en nombre. */
function parseAmount(raw: string): number {
  const isThousand = /k/i.test(raw);
  const digits = raw.replace(/[^\d.,]/g, "").replace(/\s/g, "");
  // "1 200,50" (fr) → on retire les séparateurs de milliers, virgule = décimale
  const normalized = digits.replace(/\.(?=\d{3}\b)/g, "").replace(",", ".");
  const value = parseFloat(normalized);
  if (Number.isNaN(value)) return NaN;
  return isThousand ? value * 1000 : value;
}

export class HeuristicAnalyzer implements Analyzer {
  extract(job: RawJobInput): ExtractedFields {
    const text = `${job.title} ${job.description} ${job.rawBudget ?? ""}`;
    const lower = text.toLowerCase();

    // Compétences
    const skills = Array.from(
      new Set(
        Object.entries(SKILL_KEYWORDS)
          .filter(([kw]) => lower.includes(kw))
          .map(([, label]) => label),
      ),
    );

    return {
      skills,
      budget: this.extractBudget(text, lower),
      durationDays: this.extractDuration(lower),
      location: this.extractLocation(lower),
    };
  }

  // Gère deux cas : un TJM ("450€/jour") combiné à une durée → budget total estimé,
  // sinon un montant global ("12 000 €", "12k€", "Budget 40 000 €").
  private extractBudget(text: string, lower: string): number | null {
    const dayRate = lower.match(/(\d[\d\s.,]*)\s*€?\s*\/?\s*(?:jour|j\b|jr)/);
    if (dayRate) {
      const rate = parseAmount(dayRate[1]);
      const days = this.extractDuration(lower);
      if (!Number.isNaN(rate)) return days ? Math.round(rate * days) : rate;
    }

    // Montants explicites en euros (avec ou sans "k").
    const amounts = [...text.matchAll(/(\d[\d\s.,]*)\s*(k€|k\b|€|euros?)/gi)]
      .map((m) => parseAmount(m[1] + (/k/i.test(m[2]) ? "k" : "")))
      .filter((n) => !Number.isNaN(n));

    if (amounts.length === 0) return null;
    // Le montant le plus élevé est généralement l'enveloppe globale.
    return Math.max(...amounts);
  }

  private extractDuration(lower: string): number | null {
    const m = lower.match(/(\d+)\s*(jour|jours|semaine|semaines|mois|an|ans)/);
    if (!m) return null;
    const n = parseInt(m[1], 10);
    const unit = m[2];
    if (unit.startsWith("jour")) return n;
    if (unit.startsWith("semaine")) return n * 5; // jours ouvrés
    if (unit.startsWith("mois")) return n * 21;
    return n * 252; // an(s)
  }

  private extractLocation(lower: string): string | null {
    if (/(full\s*remote|t[ée]l[ée]travail|remote)/.test(lower)) return "remote";
    const cities = ["paris", "lyon", "marseille", "bordeaux", "lille", "nantes"];
    const found = cities.find((c) => lower.includes(c));
    return found ? found.charAt(0).toUpperCase() + found.slice(1) : null;
  }
}
