"use client";

import { useEffect, useState } from "react";

type Sentiment = "Positif" | "Curieux" | "Sceptique" | "Méfiant" | "Négatif" | "Pressé" | "Fantôme";

interface SentimentEntry {
  id: string;
  text: string;
  sentiment: Sentiment;
  agent_id: string;
  confidence: number;
  keywords: string[];
  sector: string;
  timestamp: string;
}

interface Summary {
  total: number;
  by_sentiment: Record<string, number>;
  by_agent: Record<string, number>;
  avg_confidence: number;
  positive_rate_pct: number;
}

interface ApiData {
  entries: SentimentEntry[];
  summary: Summary;
}

const SENTIMENT_COLORS: Record<Sentiment, { bg: string; text: string; bar: string }> = {
  Positif:   { bg: "bg-emerald-900/40", text: "text-emerald-300", bar: "bg-emerald-500" },
  Curieux:   { bg: "bg-blue-900/40",    text: "text-blue-300",    bar: "bg-blue-500" },
  Sceptique: { bg: "bg-amber-900/40",   text: "text-amber-300",   bar: "bg-amber-500" },
  Méfiant:   { bg: "bg-red-900/40",     text: "text-red-300",     bar: "bg-red-500" },
  Négatif:   { bg: "bg-slate-800",      text: "text-slate-400",   bar: "bg-slate-500" },
  Pressé:    { bg: "bg-violet-900/40",  text: "text-violet-300",  bar: "bg-violet-500" },
  Fantôme:   { bg: "bg-slate-800",      text: "text-slate-400",   bar: "bg-slate-600" },
};

const AGENT_COLORS: Record<string, { bg: string; text: string }> = {
  "3.5": { bg: "bg-indigo-900/50",  text: "text-indigo-300" },
  "3.1": { bg: "bg-amber-900/50",   text: "text-amber-300" },
  "3.2": { bg: "bg-orange-900/50",  text: "text-orange-300" },
  "3.3": { bg: "bg-red-900/50",     text: "text-red-300" },
  "3.7": { bg: "bg-slate-700",      text: "text-slate-400" },
};

const ALL_SENTIMENTS: Sentiment[] = ["Positif", "Curieux", "Sceptique", "Méfiant", "Négatif", "Pressé", "Fantôme"];

function SentimentBadge({ sentiment }: { sentiment: Sentiment }) {
  const c = SENTIMENT_COLORS[sentiment];
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold ${c.bg} ${c.text}`}>
      {sentiment}
    </span>
  );
}

function ConfidenceBar({ value }: { value: number }) {
  const pct = Math.round(value * 100);
  const color = pct >= 70 ? "bg-emerald-500" : pct >= 50 ? "bg-blue-500" : "bg-amber-500";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-[11px] text-slate-400 w-8 text-right">{pct}%</span>
    </div>
  );
}

function AgentChip({ id }: { id: string }) {
  const c = AGENT_COLORS[id] ?? { bg: "bg-slate-700", text: "text-slate-400" };
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-[11px] font-mono font-semibold ${c.bg} ${c.text}`}>
      Agent {id}
    </span>
  );
}

function KpiCard({ label, value, sub }: { label: string; value: string | number; sub?: string }) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-4 flex flex-col gap-1">
      <p className="text-[11px] text-slate-400 uppercase tracking-wide">{label}</p>
      <p className="text-2xl font-bold text-white">{value}</p>
      {sub && <p className="text-[11px] text-slate-500">{sub}</p>}
    </div>
  );
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleString("fr-FR", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function SentimentPage() {
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [analyzeText, setAnalyzeText] = useState("");
  const [analyzeSector, setAnalyzeSector] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [analyzeResult, setAnalyzeResult] = useState<SentimentEntry | null>(null);
  const [analyzeError, setAnalyzeError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/sentiment")
      .then((r) => r.json())
      .then((d: ApiData) => { setData(d); setLoading(false); })
      .catch(() => { setError("Impossible de charger les données."); setLoading(false); });
  }, []);

  async function handleAnalyze() {
    if (!analyzeText.trim()) return;
    setAnalyzing(true);
    setAnalyzeResult(null);
    setAnalyzeError(null);
    try {
      const res = await fetch("/api/sentiment", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: analyzeText, sector: analyzeSector || undefined }),
      });
      if (!res.ok) throw new Error("Erreur serveur");
      const entry = await res.json() as SentimentEntry;
      setAnalyzeResult(entry);
    } catch {
      setAnalyzeError("Échec de l'analyse. Réessayez.");
    } finally {
      setAnalyzing(false);
    }
  }

  const maxCount = data
    ? Math.max(...ALL_SENTIMENTS.map((s) => data.summary.by_sentiment[s] ?? 0), 1)
    : 1;

  return (
    <div className="min-h-screen bg-slate-900 text-white p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Routage Sentiment IA</h1>
        <p className="text-sm text-slate-400 mt-1">
          Analyse automatique des réponses prospects · routage vers l&apos;agent optimal
        </p>
      </div>

      <div className="bg-slate-800 border border-slate-700 rounded-xl p-5 space-y-4">
        <h2 className="text-sm font-semibold text-slate-200 uppercase tracking-wide">Analyseur en direct</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div className="md:col-span-2">
            <textarea
              className="w-full h-24 bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-sm text-white placeholder:text-slate-500 resize-none focus:outline-none focus:ring-1 focus:ring-indigo-500"
              placeholder="Collez la réponse du prospect ici…"
              value={analyzeText}
              onChange={(e) => setAnalyzeText(e.target.value)}
            />
          </div>
          <div className="flex flex-col gap-3">
            <input
              className="bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-sm text-white placeholder:text-slate-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              placeholder="Secteur (optionnel)"
              value={analyzeSector}
              onChange={(e) => setAnalyzeSector(e.target.value)}
            />
            <button
              onClick={handleAnalyze}
              disabled={analyzing || !analyzeText.trim()}
              className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-sm font-semibold rounded-lg px-4 py-2 transition-colors"
            >
              {analyzing ? "Analyse…" : "Analyser →"}
            </button>
          </div>
        </div>

        {analyzeError && (
          <p className="text-sm text-red-400">{analyzeError}</p>
        )}

        {analyzeResult && (
          <div className="bg-slate-900 border border-slate-700 rounded-lg p-4 space-y-3">
            <div className="flex flex-wrap items-center gap-3">
              <SentimentBadge sentiment={analyzeResult.sentiment} />
              <AgentChip id={analyzeResult.agent_id} />
              <span className="text-sm text-slate-400">
                Confiance : <span className="text-white font-semibold">{Math.round(analyzeResult.confidence * 100)}%</span>
              </span>
            </div>
            {analyzeResult.keywords.length > 0 && (
              <div className="flex flex-wrap gap-2">
                <span className="text-[11px] text-slate-500">Mots-clés :</span>
                {analyzeResult.keywords.map((k) => (
                  <span key={k} className="text-[11px] bg-slate-700 text-slate-300 px-2 py-0.5 rounded">
                    {k}
                  </span>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {loading && (
        <div className="text-center py-16 text-slate-500">Chargement des données…</div>
      )}
      {error && (
        <div className="text-center py-16 text-red-400">{error}</div>
      )}

      {data && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <KpiCard label="Total analyses" value={data.summary.total} />
            <KpiCard
              label="Taux positif"
              value={`${data.summary.positive_rate_pct}%`}
              sub="Positif + Pressé"
            />
            <KpiCard
              label="Confiance moyenne"
              value={`${Math.round(data.summary.avg_confidence * 100)}%`}
            />
            <KpiCard
              label="Réponses routées"
              value={data.summary.total}
              sub="vers 5 agents"
            />
          </div>

          <div className="bg-slate-800 border border-slate-700 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-200 uppercase tracking-wide mb-4">
              Distribution des sentiments
            </h2>
            <div className="space-y-3">
              {ALL_SENTIMENTS.map((s) => {
                const count = data.summary.by_sentiment[s] ?? 0;
                const pct = Math.round((count / maxCount) * 100);
                const c = SENTIMENT_COLORS[s];
                return (
                  <div key={s} className="flex items-center gap-3">
                    <div className="w-24 flex-shrink-0">
                      <SentimentBadge sentiment={s} />
                    </div>
                    <div className="flex-1 h-2 bg-slate-700 rounded-full overflow-hidden">
                      <div className={`h-full ${c.bar} rounded-full transition-all`} style={{ width: `${pct}%` }} />
                    </div>
                    <span className="text-sm text-slate-300 w-6 text-right">{count}</span>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="bg-slate-800 border border-slate-700 rounded-xl overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-700">
              <h2 className="text-sm font-semibold text-slate-200 uppercase tracking-wide">
                Analyses récentes
              </h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left px-4 py-3 text-[11px] text-slate-400 uppercase tracking-wide font-medium">Texte</th>
                    <th className="text-left px-4 py-3 text-[11px] text-slate-400 uppercase tracking-wide font-medium">Sentiment</th>
                    <th className="text-left px-4 py-3 text-[11px] text-slate-400 uppercase tracking-wide font-medium">Agent</th>
                    <th className="text-left px-4 py-3 text-[11px] text-slate-400 uppercase tracking-wide font-medium w-32">Confiance</th>
                    <th className="text-left px-4 py-3 text-[11px] text-slate-400 uppercase tracking-wide font-medium">Secteur</th>
                    <th className="text-left px-4 py-3 text-[11px] text-slate-400 uppercase tracking-wide font-medium">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {data.entries.map((entry) => (
                    <tr key={entry.id} className="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors">
                      <td className="px-4 py-3 text-slate-300 max-w-xs">
                        <span className="truncate block" title={entry.text}>{entry.text}</span>
                      </td>
                      <td className="px-4 py-3">
                        <SentimentBadge sentiment={entry.sentiment} />
                      </td>
                      <td className="px-4 py-3">
                        <AgentChip id={entry.agent_id} />
                      </td>
                      <td className="px-4 py-3 w-32">
                        <ConfidenceBar value={entry.confidence} />
                      </td>
                      <td className="px-4 py-3 text-slate-400 text-[12px]">{entry.sector}</td>
                      <td className="px-4 py-3 text-slate-500 text-[11px] whitespace-nowrap">
                        {formatDate(entry.timestamp)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
