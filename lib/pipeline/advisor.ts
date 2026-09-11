// ─── Agent « Conseiller » ────────────────────────────────────────────────────
//
// Classe les opportunités d'un run par valeur attendue, désigne le meilleur coup
// et rédige une recommandation. Les CHIFFRES sont calculés de façon déterministe
// (simulator.ts) — le LLM ne sert qu'à rédiger le texte du conseil, et seulement
// si ANTHROPIC_API_KEY est présent (repli heuristique sinon).

import Anthropic from "@anthropic-ai/sdk";
import {
  winProbability,
  expectedValue,
  recommendation,
  simulatePortfolio,
  type Seniority,
  type Recommendation,
  type PortfolioSimulation,
} from "./simulator";

export interface AdviceInput {
  id: string;
  title: string;
  profileName: string;
  confidence: number;
  seniority: Seniority;
  budget: number | null;
}

export interface RankedOpportunity {
  id: string;
  title: string;
  profileName: string;
  budget: number | null;
  probability: number;
  expectedValue: number;
  recommendation: Recommendation;
}

export interface Advice {
  ranked: RankedOpportunity[];
  top: RankedOpportunity | null;
  portfolio: PortfolioSimulation;
  summary: string;
  generatedBy: "heuristic" | "llm";
}

const eur = (n: number) => `${n.toLocaleString("fr-FR")} €`;

/** Calcul déterministe : probabilités, valeurs attendues, classement, simulation. */
export function computeRanking(items: AdviceInput[]): {
  ranked: RankedOpportunity[];
  top: RankedOpportunity | null;
  portfolio: PortfolioSimulation;
} {
  const ranked = items
    .map((it) => {
      const { probability } = winProbability({
        confidence: it.confidence,
        seniority: it.seniority,
        budget: it.budget,
      });
      return {
        id: it.id,
        title: it.title,
        profileName: it.profileName,
        budget: it.budget,
        probability,
        expectedValue: expectedValue(it.budget, probability),
        recommendation: recommendation(probability),
      };
    })
    .sort((a, b) => b.expectedValue - a.expectedValue);

  const portfolio = simulatePortfolio(
    ranked.map((r) => ({ probability: r.probability, budget: r.budget })),
  );

  return { ranked, top: ranked[0] ?? null, portfolio };
}

function heuristicSummary(
  ranked: RankedOpportunity[],
  portfolio: PortfolioSimulation,
): string {
  if (ranked.length === 0) return "Aucune opportunité à analyser pour ce run.";
  const top = ranked[0];
  const strong = ranked.filter((r) => r.recommendation === "strong");
  const lines = [
    `Priorité : « ${top.title} » (${top.profileName}) — ${Math.round(top.probability * 100)} % de chances, valeur attendue ${eur(top.expectedValue)}.`,
    `Simulation sur ${portfolio.trials} scénarios : en médiane ${eur(portfolio.p50)} de revenu (${portfolio.expectedWins} mission(s) en moyenne), entre ${eur(portfolio.p10)} et ${eur(portfolio.p90)}.`,
  ];
  if (strong.length > 1) {
    lines.push(`${strong.length} opportunités à fort potentiel — traite-les en premier.`);
  }
  return lines.join(" ");
}

export interface Advisor {
  advise(items: AdviceInput[]): Promise<Advice>;
}

/** Conseiller heuristique : recommandation 100 % calculée, sans appel réseau. */
export class HeuristicAdvisor implements Advisor {
  async advise(items: AdviceInput[]): Promise<Advice> {
    const { ranked, top, portfolio } = computeRanking(items);
    return { ranked, top, portfolio, summary: heuristicSummary(ranked, portfolio), generatedBy: "heuristic" };
  }
}

/** Conseiller LLM : mêmes chiffres déterministes, rédaction par Claude. */
export class LLMAdvisor implements Advisor {
  private client: Anthropic;

  constructor(opts: { apiKey?: string } = {}) {
    this.client = new Anthropic(opts.apiKey ? { apiKey: opts.apiKey } : {});
  }

  async advise(items: AdviceInput[]): Promise<Advice> {
    const { ranked, top, portfolio } = computeRanking(items);
    if (ranked.length === 0) {
      return { ranked, top, portfolio, summary: heuristicSummary(ranked, portfolio), generatedBy: "heuristic" };
    }

    try {
      // On donne au modèle les FAITS calculés ; il ne fait que rédiger le conseil.
      const facts = {
        portfolio,
        opportunites: ranked.slice(0, 5).map((r) => ({
          mission: r.title,
          freelance: r.profileName,
          probabilite: r.probability,
          valeurAttendue: r.expectedValue,
          reco: r.recommendation,
        })),
      };
      const response = await this.client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 400,
        system:
          "Tu es un conseiller en missions freelance. À partir des chiffres FOURNIS (ne les recalcule pas, ne les invente pas), rédige un conseil bref et actionnable en français : quelle mission viser en priorité et pourquoi. 3 phrases max.",
        messages: [{ role: "user", content: JSON.stringify(facts) }],
      });
      const summary = response.content
        .filter((b): b is Anthropic.TextBlock => b.type === "text")
        .map((b) => b.text)
        .join("")
        .trim();
      return {
        ranked,
        top,
        portfolio,
        summary: summary || heuristicSummary(ranked, portfolio),
        generatedBy: summary ? "llm" : "heuristic",
      };
    } catch {
      return { ranked, top, portfolio, summary: heuristicSummary(ranked, portfolio), generatedBy: "heuristic" };
    }
  }
}

export function createAdvisor(): Advisor {
  return process.env.ANTHROPIC_API_KEY ? new LLMAdvisor() : new HeuristicAdvisor();
}
