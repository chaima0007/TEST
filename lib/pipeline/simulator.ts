// ─── Agent « Simulateur de réussite » (logique pure, testée) ─────────────────
//
// Estime la probabilité de décrocher une mission et simule, par Monte-Carlo,
// la distribution de revenus sur l'ensemble des opportunités d'un run.
// Déterministe (RNG seedé) → entièrement testable.

export type Seniority = "junior" | "mid" | "senior";

export interface WinInput {
  /** Score de compatibilité du match, 0..1 (cf. matcher.ts). */
  confidence: number;
  seniority: Seniority;
  /** Budget de l'offre en euros, ou null si inconnu. */
  budget: number | null;
}

export interface WinEstimate {
  probability: number; // 0..1
  factors: { label: string; effect: number }[]; // contributions (+/-), pour expliquer
}

export type Recommendation = "strong" | "consider" | "skip";

const clamp = (x: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, x));

/**
 * Probabilité de gagner = base + compatibilité + ajustement séniorité − pression
 * concurrentielle (les gros budgets attirent plus de candidats).
 */
export function winProbability(input: WinInput): WinEstimate {
  const factors: { label: string; effect: number }[] = [];

  const base = 0.15;
  const fromConfidence = 0.6 * input.confidence;
  factors.push({ label: "Compatibilité", effect: fromConfidence });

  const seniorityAdj = input.seniority === "senior" ? 0.08 : input.seniority === "junior" ? -0.05 : 0;
  if (seniorityAdj !== 0) factors.push({ label: "Séniorité", effect: seniorityAdj });

  let competition = 0;
  if (input.budget !== null) {
    if (input.budget > 20000) competition = -0.1;
    else if (input.budget > 5000) competition = -0.05;
  }
  if (competition !== 0) factors.push({ label: "Concurrence (budget élevé)", effect: competition });

  const probability = clamp(base + fromConfidence + seniorityAdj + competition, 0.02, 0.95);
  return { probability: Math.round(probability * 100) / 100, factors };
}

/** Valeur attendue d'une opportunité = budget × probabilité. */
export function expectedValue(budget: number | null, probability: number): number {
  if (budget === null) return 0;
  return Math.round(budget * probability);
}

export function recommendation(probability: number): Recommendation {
  if (probability >= 0.6) return "strong";
  if (probability >= 0.35) return "consider";
  return "skip";
}

// RNG déterministe (mulberry32) — pour des simulations reproductibles/testables.
function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export interface PortfolioItem {
  probability: number;
  budget: number | null;
}

export interface PortfolioSimulation {
  trials: number;
  expectedRevenue: number; // moyenne sur tous les scénarios
  expectedWins: number; // nombre moyen de missions décrochées
  p10: number;
  p50: number; // médiane
  p90: number;
}

/**
 * Monte-Carlo : sur `trials` scénarios, chaque opportunité est gagnée selon sa
 * probabilité (Bernoulli) ; on agrège revenu total et missions gagnées.
 * Renvoie l'espérance et les percentiles p10/p50/p90 du revenu total.
 */
export function simulatePortfolio(
  items: PortfolioItem[],
  opts: { trials?: number; seed?: number } = {},
): PortfolioSimulation {
  const trials = opts.trials ?? 1000;
  const rand = mulberry32(opts.seed ?? 42);

  const revenues: number[] = new Array(trials);
  let totalWins = 0;
  let totalRevenue = 0;

  for (let t = 0; t < trials; t++) {
    let revenue = 0;
    let wins = 0;
    for (const item of items) {
      if (rand() < item.probability) {
        wins++;
        revenue += item.budget ?? 0;
      }
    }
    revenues[t] = revenue;
    totalWins += wins;
    totalRevenue += revenue;
  }

  revenues.sort((a, b) => a - b);
  const pct = (p: number) => revenues[Math.min(trials - 1, Math.floor(p * trials))];

  return {
    trials,
    expectedRevenue: Math.round(totalRevenue / trials),
    expectedWins: Math.round((totalWins / trials) * 10) / 10,
    p10: pct(0.1),
    p50: pct(0.5),
    p90: pct(0.9),
  };
}
