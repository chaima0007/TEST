"use client";

import { useState } from "react";

interface SignalResp {
  symbol: string;
  currency: string;
  exchange: string;
  lastPrice: number;
  candleCount: number;
  signal: {
    side: "long" | "short" | "flat";
    action: string;
    price: number;
    confidence: number;
    score: { passed: number; total: number };
    reason: string;
    stopLoss: number | null;
    takeProfit1: number | null;
    takeProfit: number | null;
    indicators: {
      emaFast: number;
      emaSlow: number;
      emaTrend: number;
      vwap: number;
      rsi: number;
      atr: number;
      macdHist: number;
      adx: number;
      plusDI: number;
      minusDI: number;
      stochK: number;
      relVolume: number;
    };
  };
}

interface BotResp {
  signal: SignalResp["signal"] & { symbol: string };
  contract: {
    type: "call" | "put";
    moneyness: string;
    estPrice: number;
    contract: { contractSymbol: string; strike: number; expiration: number };
  } | null;
  contracts: number;
  order: { message: string; dryRun: boolean; env: string; submitted: boolean } | null;
  notes: string[];
}

interface BacktestResp {
  metrics: {
    trades: number;
    winRate: number;
    totalReturnPct: number;
    avgReturnPct: number;
    maxDrawdownPct: number;
    profitFactor: number;
  };
}

const fmt = (n: number | null | undefined, d = 2) =>
  n == null || Number.isNaN(n) ? "—" : n.toLocaleString("fr-FR", { maximumFractionDigits: d });

export default function TradingPage() {
  const [symbol, setSymbol] = useState("AAPL");
  const [interval, setInterval] = useState("5m");
  const [range, setRange] = useState("5d");
  const [loading, setLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const [signal, setSignal] = useState<SignalResp | null>(null);
  const [bot, setBot] = useState<BotResp | null>(null);
  const [bt, setBt] = useState<BacktestResp | null>(null);

  const run = async (key: string, fn: () => Promise<void>) => {
    setLoading(key);
    setError(null);
    try {
      await fn();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(null);
    }
  };

  const getSignal = () =>
    run("signal", async () => {
      setBot(null);
      const r = await fetch(`/api/trading/signal?symbol=${symbol}&interval=${interval}&range=${range}`);
      const d = await r.json();
      if (!r.ok) throw new Error(d.error || "Erreur");
      setSignal(d);
    });

  const runBacktest = () =>
    run("backtest", async () => {
      const r = await fetch(`/api/trading/backtest?symbol=${symbol}&interval=${interval}&range=1mo`);
      const d = await r.json();
      if (!r.ok) throw new Error(d.error || "Erreur");
      setBt(d);
    });

  const placeOrder = (analyzeOnly: boolean) =>
    run(analyzeOnly ? "analyze" : "order", async () => {
      const r = await fetch("/api/trading/order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbol, interval, range, analyzeOnly, minConfidence: 0.6 }),
      });
      const d = await r.json();
      if (!r.ok) throw new Error(d.error || "Erreur");
      setBot(d);
    });

  const sideColor = (s?: string) =>
    s === "long" ? "text-emerald-600 bg-emerald-50" : s === "short" ? "text-red-600 bg-red-50" : "text-slate-500 bg-slate-100";

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="max-w-5xl mx-auto px-6 py-10">
        <header className="mb-8">
          <h1 className="text-3xl font-black tracking-tight">Day Trading — Options</h1>
          <p className="text-slate-500 mt-1">
            Stratégie Momentum VWAP/EMA · données Yahoo Finance · exécution courtier (paper par défaut).
          </p>
        </header>

        {/* Avertissement risque */}
        <div className="mb-8 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
          ⚠️ Outil éducatif. Le trading d&apos;options comporte un risque de perte total et rapide
          du capital. Mode <strong>paper / dry-run</strong> par défaut — aucun ordre réel n&apos;est
          envoyé tant que vous n&apos;avez pas configuré de clés API et confirmé explicitement.
        </div>

        {/* Contrôles */}
        <div className="grid sm:grid-cols-4 gap-3 mb-6">
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-slate-500 font-medium">Symbole</span>
            <input
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              className="rounded-lg border border-slate-300 px-3 py-2 font-mono"
              placeholder="AAPL"
            />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-slate-500 font-medium">Intervalle</span>
            <select value={interval} onChange={(e) => setInterval(e.target.value)} className="rounded-lg border border-slate-300 px-3 py-2">
              {["1m", "2m", "5m", "15m", "30m", "60m"].map((i) => (
                <option key={i}>{i}</option>
              ))}
            </select>
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="text-slate-500 font-medium">Historique</span>
            <select value={range} onChange={(e) => setRange(e.target.value)} className="rounded-lg border border-slate-300 px-3 py-2">
              {["1d", "5d", "1mo"].map((r) => (
                <option key={r}>{r}</option>
              ))}
            </select>
          </label>
          <div className="flex items-end">
            <button
              onClick={getSignal}
              disabled={loading !== null}
              className="w-full bg-slate-900 hover:bg-slate-700 disabled:opacity-50 text-white font-semibold rounded-lg px-4 py-2 transition-colors"
            >
              {loading === "signal" ? "..." : "Analyser le signal"}
            </button>
          </div>
        </div>

        {error && <div className="mb-6 rounded-lg bg-red-50 border border-red-200 text-red-700 px-4 py-3 text-sm">{error}</div>}

        {/* Signal */}
        {signal && (
          <section className="mb-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-xl font-bold">
                  {signal.symbol} <span className="text-slate-400 text-sm font-normal">{signal.exchange}</span>
                </h2>
                <p className="text-slate-500 text-sm">
                  Dernier : {fmt(signal.lastPrice)} {signal.currency} · {signal.candleCount} bougies
                </p>
              </div>
              <span className={`px-3 py-1.5 rounded-full text-sm font-bold uppercase ${sideColor(signal.signal.side)}`}>
                {signal.signal.side} · {(signal.signal.confidence * 100).toFixed(0)}% · {signal.signal.score.passed}/{signal.signal.score.total}
              </span>
            </div>
            <p className="text-sm text-slate-600 mb-4">{signal.signal.reason}</p>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-sm">
              <Stat label="EMA 9 / 21" value={`${fmt(signal.signal.indicators.emaFast)} / ${fmt(signal.signal.indicators.emaSlow)}`} />
              <Stat label="EMA 50 (tendance)" value={fmt(signal.signal.indicators.emaTrend)} />
              <Stat label="VWAP" value={fmt(signal.signal.indicators.vwap)} />
              <Stat label="RSI" value={fmt(signal.signal.indicators.rsi, 0)} />
              <Stat label="ADX (force)" value={fmt(signal.signal.indicators.adx, 0)} />
              <Stat label="+DI / -DI" value={`${fmt(signal.signal.indicators.plusDI, 0)} / ${fmt(signal.signal.indicators.minusDI, 0)}`} />
              <Stat label="MACD hist" value={fmt(signal.signal.indicators.macdHist, 3)} />
              <Stat label="Stoch %K" value={fmt(signal.signal.indicators.stochK, 0)} />
              <Stat label="Vol. relatif" value={`${fmt(signal.signal.indicators.relVolume, 2)}×`} />
              <Stat label="ATR" value={fmt(signal.signal.indicators.atr)} />
              <Stat label="Stop-loss" value={fmt(signal.signal.stopLoss)} />
              <Stat label="TP1 / TP2" value={`${fmt(signal.signal.takeProfit1)} / ${fmt(signal.signal.takeProfit)}`} />
            </div>

            <div className="flex flex-wrap gap-3 mt-6">
              <button
                onClick={() => placeOrder(true)}
                disabled={loading !== null}
                className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-semibold rounded-lg px-4 py-2 text-sm transition-colors"
              >
                {loading === "analyze" ? "..." : "Choisir le contrat d'option"}
              </button>
              <button
                onClick={() => placeOrder(false)}
                disabled={loading !== null}
                className="bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-semibold rounded-lg px-4 py-2 text-sm transition-colors"
              >
                {loading === "order" ? "..." : "Passer l'ordre (paper / dry-run)"}
              </button>
              <button
                onClick={runBacktest}
                disabled={loading !== null}
                className="border border-slate-300 hover:border-slate-900 font-semibold rounded-lg px-4 py-2 text-sm transition-colors"
              >
                {loading === "backtest" ? "..." : "Backtester (1 mois)"}
              </button>
            </div>
          </section>
        )}

        {/* Résultat bot / options */}
        {bot && (
          <section className="mb-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-bold mb-3">Exécution options</h2>
            {bot.contract ? (
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-sm mb-4">
                <Stat label="Type" value={bot.contract.type.toUpperCase()} />
                <Stat label="Strike" value={fmt(bot.contract.contract.strike)} />
                <Stat label="Moneyness" value={bot.contract.moneyness} />
                <Stat label="Prime ≈" value={fmt(bot.contract.estPrice)} />
                <Stat label="Contrats" value={String(bot.contracts)} />
                <Stat label="Échéance" value={new Date(bot.contract.contract.expiration).toISOString().slice(0, 10)} />
                <div className="col-span-2 sm:col-span-4">
                  <Stat label="Symbole OCC" value={bot.contract.contract.contractSymbol} mono />
                </div>
              </div>
            ) : (
              <p className="text-sm text-slate-500 mb-3">Aucun contrat sélectionné.</p>
            )}
            <ul className="space-y-1 text-sm text-slate-600">
              {bot.notes.map((n, i) => (
                <li key={i} className="flex gap-2">
                  <span className="text-slate-400">→</span> {n}
                </li>
              ))}
            </ul>
            {bot.order && (
              <div className={`mt-4 rounded-lg px-4 py-3 text-sm ${bot.order.submitted ? "bg-emerald-50 text-emerald-800" : "bg-slate-100 text-slate-700"}`}>
                <strong>{bot.order.env.toUpperCase()}{bot.order.dryRun ? " · DRY-RUN" : ""}</strong> — {bot.order.message}
              </div>
            )}
          </section>
        )}

        {/* Backtest */}
        {bt && (
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-bold mb-4">Backtest (1 mois, 5m)</h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-sm">
              <Stat label="Trades" value={String(bt.metrics.trades)} />
              <Stat label="Taux de réussite" value={`${fmt(bt.metrics.winRate, 1)} %`} />
              <Stat label="Rendement total" value={`${fmt(bt.metrics.totalReturnPct)} %`} />
              <Stat label="Rendement moyen / trade" value={`${fmt(bt.metrics.avgReturnPct)} %`} />
              <Stat label="Drawdown max" value={`${fmt(bt.metrics.maxDrawdownPct)} %`} />
              <Stat label="Profit factor" value={fmt(bt.metrics.profitFactor)} />
            </div>
            <p className="text-xs text-slate-400 mt-4">
              Backtest sur le sous-jacent (signal). Le rendement réel des options dépend du delta, de
              la volatilité implicite et du theta — non modélisés ici.
            </p>
          </section>
        )}
      </div>
    </div>
  );
}

function Stat({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <div className="rounded-lg bg-slate-50 border border-slate-100 px-3 py-2">
      <p className="text-slate-400 text-xs">{label}</p>
      <p className={`font-semibold ${mono ? "font-mono text-xs break-all" : ""}`}>{value}</p>
    </div>
  );
}
