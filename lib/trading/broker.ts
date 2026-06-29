// Connexion au courtier via l'API REST Alpaca (actions + options).
//
// SÉCURITÉ — par défaut :
//   • mode PAPER (compte fictif, aucun argent réel) ;
//   • DRY-RUN si les clés API ne sont pas configurées (ordre simulé, non envoyé).
// Le mode LIVE (argent réel) exige ALPACA_ENV=live ET une confirmation explicite
// passée à `submitOrder`. Voir .env.example et le README.

export type BrokerEnv = "paper" | "live";

export interface BrokerConfig {
  keyId: string;
  secretKey: string;
  env: BrokerEnv;
}

export interface OrderRequest {
  /** Symbole : ticker action ("AAPL") ou symbole OCC d'option ("AAPL240119C00150000"). */
  symbol: string;
  /** Nombre d'actions ou de contrats. */
  qty: number;
  side: "buy" | "sell";
  type?: "market" | "limit";
  limitPrice?: number;
  /** "day" obligatoire pour les options. */
  timeInForce?: "day" | "gtc";
}

export interface OrderResult {
  submitted: boolean;
  dryRun: boolean;
  env: BrokerEnv;
  id?: string;
  status?: string;
  message: string;
  request: OrderRequest;
  raw?: unknown;
}

function baseUrl(env: BrokerEnv): string {
  return env === "live" ? "https://api.alpaca.markets" : "https://paper-api.alpaca.markets";
}

/** Lit la configuration depuis l'environnement (jamais de secret en dur). */
export function loadConfig(): BrokerConfig {
  return {
    keyId: process.env.ALPACA_KEY_ID ?? "",
    secretKey: process.env.ALPACA_SECRET_KEY ?? "",
    env: (process.env.ALPACA_ENV as BrokerEnv) === "live" ? "live" : "paper",
  };
}

export function hasCredentials(cfg: BrokerConfig = loadConfig()): boolean {
  return Boolean(cfg.keyId && cfg.secretKey);
}

function headers(cfg: BrokerConfig): Record<string, string> {
  return {
    "APCA-API-KEY-ID": cfg.keyId,
    "APCA-API-SECRET-KEY": cfg.secretKey,
    "Content-Type": "application/json",
  };
}

/** Récupère l'état du compte (cash, buying power, equity). */
export async function getAccount(cfg: BrokerConfig = loadConfig()) {
  if (!hasCredentials(cfg)) {
    return { connected: false, env: cfg.env, message: "Aucune clé API configurée (mode dry-run)." };
  }
  const res = await fetch(`${baseUrl(cfg.env)}/v2/account`, { headers: headers(cfg) });
  if (!res.ok) throw new Error(`Alpaca /v2/account a renvoyé ${res.status}`);
  const a = (await res.json()) as Record<string, string>;
  return {
    connected: true,
    env: cfg.env,
    accountNumber: a.account_number,
    status: a.status,
    cash: Number(a.cash),
    buyingPower: Number(a.buying_power),
    equity: Number(a.equity),
    optionsTradingLevel: a.options_trading_level,
  };
}

/**
 * Envoie un ordre au courtier.
 *
 * @param confirmLive Doit valoir exactement "LIVE" pour autoriser un ordre réel.
 *                    Ignoré en mode paper. Garde-fou contre les envois accidentels.
 */
export async function submitOrder(
  order: OrderRequest,
  cfg: BrokerConfig = loadConfig(),
  confirmLive?: string,
): Promise<OrderResult> {
  // Garde-fou : pas d'ordre réel sans confirmation explicite.
  if (cfg.env === "live" && confirmLive !== "LIVE") {
    return {
      submitted: false,
      dryRun: true,
      env: cfg.env,
      message:
        "Mode LIVE bloqué : confirmation 'LIVE' requise pour envoyer un ordre avec de l'argent réel.",
      request: order,
    };
  }

  // Dry-run si aucune clé : on simule sans rien envoyer.
  if (!hasCredentials(cfg)) {
    return {
      submitted: false,
      dryRun: true,
      env: cfg.env,
      message: `Dry-run : ordre simulé (${order.side} ${order.qty} ${order.symbol}). Configurez ALPACA_KEY_ID / ALPACA_SECRET_KEY pour exécuter.`,
      request: order,
    };
  }

  const body = {
    symbol: order.symbol,
    qty: String(order.qty),
    side: order.side,
    type: order.type ?? "market",
    time_in_force: order.timeInForce ?? "day",
    ...(order.type === "limit" && order.limitPrice ? { limit_price: String(order.limitPrice) } : {}),
  };

  const res = await fetch(`${baseUrl(cfg.env)}/v2/orders`, {
    method: "POST",
    headers: headers(cfg),
    body: JSON.stringify(body),
  });
  const raw = await res.json();

  if (!res.ok) {
    return {
      submitted: false,
      dryRun: false,
      env: cfg.env,
      message: `Alpaca a rejeté l'ordre (${res.status}) : ${(raw as { message?: string }).message ?? "erreur inconnue"}`,
      request: order,
      raw,
    };
  }

  const r = raw as { id: string; status: string };
  return {
    submitted: true,
    dryRun: false,
    env: cfg.env,
    id: r.id,
    status: r.status,
    message: `Ordre ${cfg.env.toUpperCase()} accepté : ${order.side} ${order.qty} ${order.symbol} (statut ${r.status}).`,
    request: order,
    raw,
  };
}
