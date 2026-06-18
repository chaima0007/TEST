// ─── Agent COMMANDANT (premium) — chef d'orchestre ───────────────────────────
//
// Reçoit un objectif business et des plans candidats. Pour chaque plan :
//   1. RESPECT   — porte de conformité (compliance.ts) ; un plan non conforme
//                  est éliminé, quel que soit son rendement.
//   2. SUCCÈS    — simulation Monte-Carlo du tunnel de prospection.
//   3. ROI       — profit attendu = revenu simulé − investissement financier.
// Puis il classe les plans conformes par profit attendu et recommande le meilleur.

import { checkPlan, type PlanAction, type ComplianceResult } from "./compliance";

export interface Funnel {
  messagesTotal: number; // volume total de messages sur la période
  replyRate: number; // 0..1
  callRate: number; // réponses → appels
  closeRate: number; // appels → signatures
}

export interface Plan {
  id: string;
  label: string;
  price: number; // prix du service vendu (€)
  cost: number; // investissement financier du plan (€)
  funnel: Funnel;
  actions: PlanAction[];
}

export interface PlanSimulation {
  planId: string;
  label: string;
  compliance: ComplianceResult;
  trials: number;
  probAtLeastOne: number; // P(≥1 client)
  expectedClients: number;
  expectedRevenue: number;
  cost: number;
  expectedProfit: number; // revenu attendu − coût
  roi: number; // profit / coût (0 si coût nul)
}

// RNG déterministe (mulberry32) — simulations reproductibles/testables.
function mulberry32(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Probabilité qu'un message aboutisse à une signature (tunnel multiplicatif). */
function perMessageWin(f: Funnel): number {
  return f.replyRate * f.callRate * f.closeRate;
}

export function simulatePlan(plan: Plan, opts: { trials?: number; seed?: number } = {}): PlanSimulation {
  const trials = opts.trials ?? 50;
  const compliance = checkPlan(plan.actions);
  const p = perMessageWin(plan.funnel);
  const rand = mulberry32(opts.seed ?? 1);

  let totalClients = 0;
  let weeksWithClient = 0;
  for (let t = 0; t < trials; t++) {
    let clients = 0;
    for (let m = 0; m < plan.funnel.messagesTotal; m++) {
      if (rand() < p) clients++;
    }
    totalClients += clients;
    if (clients >= 1) weeksWithClient++;
  }

  const expectedClients = Math.round((totalClients / trials) * 100) / 100;
  const expectedRevenue = Math.round(expectedClients * plan.price);
  const expectedProfit = expectedRevenue - plan.cost;
  return {
    planId: plan.id,
    label: plan.label,
    compliance,
    trials,
    probAtLeastOne: Math.round((weeksWithClient / trials) * 100) / 100,
    expectedClients,
    expectedRevenue,
    cost: plan.cost,
    expectedProfit,
    roi: plan.cost > 0 ? Math.round((expectedProfit / plan.cost) * 100) / 100 : 0,
  };
}

export interface CommandantDecision {
  objective: string;
  trials: number;
  simulations: PlanSimulation[]; // tous les plans (conformes + rejetés)
  eligible: PlanSimulation[]; // conformes uniquement, triés par profit attendu
  recommended: PlanSimulation | null;
  rationale: string;
}

const eur = (n: number) => `${n.toLocaleString("fr-FR")} €`;

/** Décide du meilleur plan : conforme d'abord, puis profit attendu maximal. */
export function decide(
  objective: string,
  plans: Plan[],
  opts: { trials?: number; seed?: number } = {},
): CommandantDecision {
  const trials = opts.trials ?? 50;
  const simulations = plans.map((p) => simulatePlan(p, { trials, seed: opts.seed }));
  const eligible = simulations
    .filter((s) => s.compliance.compliant)
    .sort((a, b) => b.expectedProfit - a.expectedProfit);
  const recommended = eligible[0] ?? null;
  const rejected = simulations.filter((s) => !s.compliance.compliant);

  const rationale = recommended
    ? `Plan retenu : « ${recommended.label} » — ${Math.round(recommended.probAtLeastOne * 100)} % de chances de signer, ` +
      `profit attendu ${eur(recommended.expectedProfit)} (revenu ${eur(recommended.expectedRevenue)} − coût ${eur(recommended.cost)}).` +
      (rejected.length ? ` ${rejected.length} plan(s) écarté(s) pour non-respect des règles.` : "")
    : "Aucun plan conforme : revoir les actions pour respecter les règles.";

  return { objective, trials, simulations, eligible, recommended, rationale };
}
