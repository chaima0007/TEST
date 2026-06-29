// Récupération et sélection de contrats d'options via l'API publique Yahoo Finance.
// Endpoint "options" : aucune clé requise.

const BASE = "https://query1.finance.yahoo.com/v7/finance/options";

export interface OptionContract {
  contractSymbol: string;
  strike: number;
  lastPrice: number;
  bid: number;
  ask: number;
  volume: number;
  openInterest: number;
  impliedVolatility: number;
  inTheMoney: boolean;
  expiration: number; // ms epoch
}

export interface OptionsChain {
  symbol: string;
  underlyingPrice: number;
  expirationDates: number[]; // ms epoch, triées
  expiration: number; // échéance effectivement renvoyée
  calls: OptionContract[];
  puts: OptionContract[];
}

interface YahooOptionsResponse {
  optionChain: {
    result?: Array<{
      underlyingSymbol: string;
      expirationDates: number[];
      quote: { regularMarketPrice: number };
      options: Array<{
        expirationDate: number;
        calls: RawContract[];
        puts: RawContract[];
      }>;
    }>;
    error?: { description: string } | null;
  };
}

interface RawContract {
  contractSymbol: string;
  strike: number;
  lastPrice: number;
  bid?: number;
  ask?: number;
  volume?: number;
  openInterest?: number;
  impliedVolatility?: number;
  inTheMoney?: boolean;
  expiration: number;
}

const UA =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36";

function map(c: RawContract): OptionContract {
  return {
    contractSymbol: c.contractSymbol,
    strike: c.strike,
    lastPrice: c.lastPrice,
    bid: c.bid ?? 0,
    ask: c.ask ?? 0,
    volume: c.volume ?? 0,
    openInterest: c.openInterest ?? 0,
    impliedVolatility: c.impliedVolatility ?? 0,
    inTheMoney: c.inTheMoney ?? false,
    expiration: c.expiration * 1000,
  };
}

/**
 * Télécharge la chaîne d'options d'un sous-jacent.
 * @param symbol Ticker du sous-jacent (ex: "AAPL").
 * @param expiration Échéance ciblée (ms epoch). Par défaut : la plus proche.
 */
export async function fetchOptionsChain(symbol: string, expiration?: number): Promise<OptionsChain> {
  const url = expiration
    ? `${BASE}/${encodeURIComponent(symbol)}?date=${Math.floor(expiration / 1000)}`
    : `${BASE}/${encodeURIComponent(symbol)}`;

  const res = await fetch(url, {
    headers: { "User-Agent": UA, Accept: "application/json" },
    next: { revalidate: 30 },
  });
  if (!res.ok) throw new Error(`Yahoo Finance options a renvoyé ${res.status} pour ${symbol}`);

  const data = (await res.json()) as YahooOptionsResponse;
  if (data.optionChain.error) throw new Error(`Yahoo Finance: ${data.optionChain.error.description}`);

  const result = data.optionChain.result?.[0];
  const block = result?.options?.[0];
  if (!result || !block) throw new Error(`Aucune chaîne d'options pour "${symbol}"`);

  return {
    symbol: result.underlyingSymbol,
    underlyingPrice: result.quote.regularMarketPrice,
    expirationDates: result.expirationDates.map((d) => d * 1000),
    expiration: block.expirationDate * 1000,
    calls: block.calls.map(map),
    puts: block.puts.map(map),
  };
}

export interface ContractSelection {
  contract: OptionContract;
  type: "call" | "put";
  /** Décalage en nombre de strikes par rapport à l'ATM (0 = ATM). */
  moneyness: "ITM" | "ATM" | "OTM";
  /** Prix indicatif (mid bid/ask, sinon lastPrice). */
  estPrice: number;
}

/**
 * Sélectionne le contrat à trader à partir d'un signal directionnel.
 *  - signal long  -> CALL
 *  - signal short -> PUT
 * Choisit le strike le plus proche du prix (ATM) avec un léger biais directionnel
 * configurable, en privilégiant la liquidité (volume + open interest).
 *
 * @param strikeOffset Nombre de strikes hors de la monnaie à viser (0 = ATM,
 *                     +1 = un cran OTM, etc.). Par défaut 0.
 */
export function selectContract(
  chain: OptionsChain,
  direction: "long" | "short",
  strikeOffset = 0,
): ContractSelection {
  const type: "call" | "put" = direction === "long" ? "call" : "put";
  const list = type === "call" ? chain.calls : chain.puts;
  if (!list.length) throw new Error(`Aucun ${type} disponible dans la chaîne`);

  // Strikes triés et liquides uniquement.
  const liquid = list
    .filter((c) => c.bid > 0 || c.ask > 0 || c.lastPrice > 0)
    .sort((a, b) => a.strike - b.strike);
  const pool = liquid.length ? liquid : list.slice().sort((a, b) => a.strike - b.strike);

  // Index du strike le plus proche du sous-jacent (ATM).
  let atm = 0;
  let best = Infinity;
  for (let i = 0; i < pool.length; i++) {
    const d = Math.abs(pool[i].strike - chain.underlyingPrice);
    if (d < best) {
      best = d;
      atm = i;
    }
  }

  // Pour un call, OTM = strikes plus hauts ; pour un put, OTM = strikes plus bas.
  const idx = type === "call" ? atm + strikeOffset : atm - strikeOffset;
  const contract = pool[Math.max(0, Math.min(pool.length - 1, idx))];

  const mid = contract.bid > 0 && contract.ask > 0 ? (contract.bid + contract.ask) / 2 : contract.lastPrice;
  const moneyness: ContractSelection["moneyness"] =
    contract.strike === pool[atm].strike
      ? "ATM"
      : contract.inTheMoney
        ? "ITM"
        : "OTM";

  return { contract, type, moneyness, estPrice: round2(mid) };
}

function round2(v: number): number {
  return Math.round(v * 100) / 100;
}
