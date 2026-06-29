// Bot de day trading sur options exécutable en ligne de commande.
//
// Usage :
//   npx tsx scripts/trade-bot.ts AAPL --analyze
//   npx tsx scripts/trade-bot.ts AAPL --capital 20000 --risk 1 --min-conf 0.65
//   ALPACA_KEY_ID=... ALPACA_SECRET_KEY=... npx tsx scripts/trade-bot.ts AAPL   # paper
//
// Idéal pour un cron en séance (ex: toutes les 5 min pendant les heures de marché).
// Par défaut : mode paper / dry-run, aucun ordre réel sans configuration + confirmation.

import { runBot } from "../lib/trading/bot";

function arg(name: string): string | undefined {
  const i = process.argv.indexOf(`--${name}`);
  return i >= 0 ? process.argv[i + 1] : undefined;
}
function flag(name: string): boolean {
  return process.argv.includes(`--${name}`);
}

async function main() {
  const symbol = process.argv[2];
  if (!symbol || symbol.startsWith("--")) {
    console.error("Usage : npx tsx scripts/trade-bot.ts <SYMBOLE> [--analyze] [--capital N] [--risk N] [--min-conf N] [--offset N] [--live]");
    process.exit(1);
  }

  const run = await runBot({
    symbol: symbol.toUpperCase(),
    interval: (arg("interval") as never) || "5m",
    range: (arg("range") as never) || "5d",
    capital: arg("capital") ? Number(arg("capital")) : 10_000,
    riskPerTradePct: arg("risk") ? Number(arg("risk")) : 1,
    minConfidence: arg("min-conf") ? Number(arg("min-conf")) : 0.6,
    strikeOffset: arg("offset") ? Number(arg("offset")) : 0,
    analyzeOnly: flag("analyze"),
    confirmLive: flag("live") ? "LIVE" : undefined,
  });

  const s = run.signal;
  console.log(`\n=== ${s.symbol} @ ${new Date(s.time).toISOString()} ===`);
  console.log(`Signal   : ${s.side.toUpperCase()} (confiance ${(s.confidence * 100).toFixed(0)}%)`);
  console.log(`Prix     : ${s.price}  | RSI ${s.indicators.rsi}  VWAP ${s.indicators.vwap}  ATR ${s.indicators.atr}`);
  console.log(`Raison   : ${s.reason}`);
  if (run.contract) {
    console.log(`Contrat  : ${run.contract.type.toUpperCase()} ${run.contract.contract.strike} (${run.contract.moneyness}) prime≈${run.contract.estPrice}`);
    console.log(`OCC      : ${run.contract.contract.contractSymbol}  ×${run.contracts}`);
  }
  console.log("\nNotes :");
  run.notes.forEach((n) => console.log("  - " + n));
  if (run.order) console.log(`\nOrdre : [${run.order.env}${run.order.dryRun ? "/dry-run" : ""}] ${run.order.message}`);
}

main().catch((e) => {
  console.error("Erreur :", (e as Error).message);
  process.exit(1);
});
