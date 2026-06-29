// Orchestrateur du bot de day trading sur options.
//
// Pipeline complet :
//   1. Récupère les bougies intraday du sous-jacent (Yahoo Finance).
//   2. Calcule le signal de la stratégie Momentum VWAP/EMA.
//   3. Si le signal est directionnel, sélectionne le contrat d'option adapté
//      (call si haussier, put si baissier) dans la chaîne Yahoo.
//   4. Dimensionne la position selon le budget de risque.
//   5. Envoie l'ordre au courtier (paper par défaut, dry-run sans clés).

import type { Interval, Range, Signal } from "./types";
import { getMarketData } from "./datasource";
import { fetchOptionsChain, selectContract, type ContractSelection } from "./options";
import { generateSignal, DEFAULT_PARAMS } from "./strategy";
import { submitOrder, loadConfig, type OrderResult, type BrokerConfig } from "./broker";

export interface BotOptions {
  symbol: string;
  interval?: Interval;
  range?: Range;
  /** Capital de référence pour le dimensionnement (€/$). */
  capital?: number;
  /** Risque maximum par trade en % du capital. */
  riskPerTradePct?: number;
  /** Confiance minimale du signal pour déclencher un ordre (0..1). */
  minConfidence?: number;
  /** Décalage de strike pour le choix du contrat (0 = ATM). */
  strikeOffset?: number;
  /** Échéance ciblée (ms epoch). Par défaut : la plus proche. */
  expiration?: number;
  /** Si vrai, calcule le signal et le contrat sans envoyer d'ordre. */
  analyzeOnly?: boolean;
  /** Confirmation "LIVE" requise pour un ordre en argent réel. */
  confirmLive?: string;
}

export interface BotRun {
  signal: Signal;
  contract: ContractSelection | null;
  contracts: number;
  order: OrderResult | null;
  notes: string[];
}

export async function runBot(opts: BotOptions, cfg: BrokerConfig = loadConfig()): Promise<BotRun> {
  const {
    symbol,
    interval = "5m",
    range = "5d",
    capital = 10_000,
    riskPerTradePct = 1,
    minConfidence = 0.6,
    strikeOffset = 0,
    expiration,
    analyzeOnly = false,
    confirmLive,
  } = opts;

  const notes: string[] = [];

  // 1 + 2 — données et signal sur le sous-jacent.
  const market = await getMarketData(symbol, interval, range);
  if (market.candles.length < DEFAULT_PARAMS.emaSlow + 2) {
    throw new Error(`Pas assez de bougies pour ${symbol} (${market.candles.length}).`);
  }
  const signal = generateSignal(symbol, market.candles);

  // Pas de trade si signal neutre ou confiance trop faible.
  if (signal.side === "flat") {
    notes.push("Signal neutre : aucune position prise.");
    return { signal, contract: null, contracts: 0, order: null, notes };
  }
  if (signal.confidence < minConfidence) {
    notes.push(
      `Confiance ${(signal.confidence * 100).toFixed(0)}% < seuil ${(minConfidence * 100).toFixed(0)}% : trade ignoré.`,
    );
    return { signal, contract: null, contracts: 0, order: null, notes };
  }

  // 3 — sélection du contrat d'option.
  const chain = await fetchOptionsChain(symbol, expiration);
  const selection = selectContract(chain, signal.side === "long" ? "long" : "short", strikeOffset);
  notes.push(
    `Contrat retenu : ${selection.type.toUpperCase()} ${selection.contract.strike} (${selection.moneyness}), échéance ${new Date(chain.expiration).toISOString().slice(0, 10)}, prime ≈ ${selection.estPrice}.`,
  );

  // 4 — dimensionnement. Le risque max par trade = % du capital ; la perte
  // maximale d'une option longue = la prime payée (× 100 par contrat).
  const premiumPerContract = selection.estPrice * 100;
  const riskBudget = capital * (riskPerTradePct / 100);
  let contracts = premiumPerContract > 0 ? Math.floor(riskBudget / premiumPerContract) : 0;
  if (contracts < 1) {
    contracts = 0;
    notes.push(
      `Budget de risque (${riskBudget.toFixed(0)}) insuffisant pour 1 contrat (prime ${premiumPerContract.toFixed(0)}).`,
    );
    return { signal, contract: selection, contracts, order: null, notes };
  }
  notes.push(`Taille : ${contracts} contrat(s) ≈ ${(contracts * premiumPerContract).toFixed(0)} de prime.`);

  if (analyzeOnly) {
    notes.push("Mode analyse : aucun ordre envoyé.");
    return { signal, contract: selection, contracts, order: null, notes };
  }

  // 5 — envoi de l'ordre. On achète toujours l'option (acheteur de call/put) :
  // côté = "buy", risque limité à la prime.
  const order = await submitOrder(
    {
      symbol: selection.contract.contractSymbol,
      qty: contracts,
      side: "buy",
      type: "limit",
      // Limite défensive : on ne paie pas plus que ~5 % au-dessus du mid.
      limitPrice: Math.round(selection.estPrice * 1.05 * 100) / 100,
      timeInForce: "day",
    },
    cfg,
    confirmLive,
  );
  notes.push(order.message);

  return { signal, contract: selection, contracts, order, notes };
}
