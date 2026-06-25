"use client";

import { useEffect, useState } from "react";

type OptimizationTier = "weak" | "fair" | "good" | "excellent";

interface DimensionScores {
  length: number;
  personalization: number;
  urgency: number;
  clarity: number;
  question: number;
  emoji_balance: number;
}

interface SubjectLine {
  subject_id: string;
  text: string;
  template_id?: string;
  variant_key: string;
  send_hour: number;
}

interface OptimizedSubject {
  subject: SubjectLine;
  predicted_open_rate: number;
  optimization_tier: OptimizationTier;
  dimension_scores: DimensionScores;
  suggestions: string[];
  emoji_count: number;
  word_count: number;
  char_count: number;
  has_personalization: boolean;
  has_urgency: boolean;
  has_question: boolean;
}

interface Summary {
  total: number;
  tier_counts: Record<OptimizationTier, number>;
  avg_open_rate: number;
  best_open_rate: number;
  pct_with_personalization: number;
}

const TIER_STYLES: Record<OptimizationTier, { bg: string; text: string; border: string; bar: string; label: string }> = {
  excellent: { bg: "bg-emerald-900/40",  text: "text-emerald-300", border: "border-emerald-700/60", bar: "bg-emerald-500", label: "EXCELLENT" },
  good:      { bg: "bg-indigo-900/40",   text: "text-indigo-300",  border: "border-indigo-700/60",  bar: "bg-indigo-400",  label: "BON" },
  fair:      { bg: "bg-amber-900/30",    text: "text-amber-300",   border: "border-amber-700/40",   bar: "bg-amber-400",   label: "MOYEN" },
  weak:      { bg: "bg-slate-800",       text: "text-slate-400",   border: "border-slate-700",      bar: "bg-slate-500",   label: "FAIBLE" },
};

const DIM_LABELS: Record<keyof DimensionScores, string> = {
  length: "Longueur",
  personalization: "Personnalisation",
  urgency: "Urgence",
  clarity: "Clarté",
  question: "Question",
  emoji_balance: "Emojis",
};

function TierBadge({ tier }: { tier: OptimizationTier }) {
  const s = TIER_STYLES[tier];
  return (
    <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${s.bg} ${s.text} ${s.border}`}>
      {s.label}
    </span>
  );
}

function DimBar({ label, value }: { label: string; value: number }) {
  const color = value >= 80 ? "bg-emerald-500" : value >= 60 ? "bg-indigo-400" : value >= 40 ? "bg-amber-400" : "bg-red-500";
  return (
    <div>
      <div className="flex justify-between text-[10px] text-slate-400 mb-0.5">
        <span>{label}</span>
        <span className="font-mono">{Math.round(value)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full ${color} rounded-full`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function KpiCard({ label, value, sub, accent }: { label: string; value: string | number; sub?: string; accent?: string }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
      <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold mb-1">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-slate-500 mt-0.5">{sub}</p>}
    </div>
  );
}

function LiveAnalyzer({ onResult }: { onResult: (r: OptimizedSubject) => void }) {
  const [text, setText] = useState("");
  const [hour, setHour] = useState(9);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("/api/subject-optimizer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, send_hour: hour }),
      });
      const data = await res.json();
      onResult(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
      <p className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Analyser un sujet</p>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Votre sujet d'email ici… ex: Bonjour {contact_name} — offre exclusive aujourd'hui ⚡"
        rows={2}
        className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 resize-none"
      />
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2">
          <label className="text-xs text-slate-500">Heure d'envoi</label>
          <input
            type="number"
            min={0} max={23}
            value={hour}
            onChange={(e) => setHour(Number(e.target.value))}
            className="w-16 bg-slate-800 border border-slate-700 rounded px-2 py-1 text-sm text-white text-center focus:outline-none focus:border-indigo-500"
          />
          <span className="text-xs text-slate-500">h</span>
        </div>
        <button
          onClick={analyze}
          disabled={loading || !text.trim()}
          className="ml-auto px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-sm font-medium rounded-lg transition-colors"
        >
          {loading ? "Analyse…" : "Analyser →"}
        </button>
      </div>
    </div>
  );
}

function ResultPanel({ result }: { result: OptimizedSubject }) {
  const s = TIER_STYLES[result.optimization_tier];
  return (
    <div className={`bg-slate-900 border ${result.optimization_tier === "excellent" ? "border-emerald-700/40" : "border-slate-800"} rounded-xl p-5 space-y-4`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1">
          <p className="text-sm text-slate-300 font-medium">"{result.subject.text}"</p>
          <div className="flex items-center gap-2 mt-1 flex-wrap">
            <span className="text-xs text-slate-500">{result.char_count} car. · {result.word_count} mots</span>
            {result.has_personalization && <span className="text-[10px] text-indigo-400">✓ Personnalisé</span>}
            {result.has_urgency && <span className="text-[10px] text-amber-400">✓ Urgence</span>}
            {result.has_question && <span className="text-[10px] text-emerald-400">✓ Question</span>}
          </div>
        </div>
        <div className="flex-shrink-0 text-center">
          <p className={`text-3xl font-bold ${s.text}`}>{Math.round(result.predicted_open_rate * 100)}%</p>
          <TierBadge tier={result.optimization_tier} />
        </div>
      </div>

      <div className="space-y-1.5">
        {(Object.entries(result.dimension_scores) as [keyof DimensionScores, number][]).map(([k, v]) => (
          <DimBar key={k} label={DIM_LABELS[k]} value={v} />
        ))}
      </div>

      {result.suggestions.length > 0 && (
        <div>
          <p className="text-xs text-slate-500 font-semibold mb-1.5">Suggestions</p>
          <ul className="space-y-1">
            {result.suggestions.map((s, i) => (
              <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                <span className="text-amber-400 flex-shrink-0">→</span>
                {s}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default function SubjectOptimizerPage() {
  const [data, setData] = useState<{ subjects: OptimizedSubject[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [tierFilter, setTierFilter] = useState<OptimizationTier | "all">("all");
  const [liveResult, setLiveResult] = useState<OptimizedSubject | null>(null);

  useEffect(() => {
    fetch("/api/subject-optimizer")
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-6 text-slate-500 text-center py-16">Chargement…</div>;
  if (!data) return null;

  const { subjects, summary } = data;
  const filtered = tierFilter === "all" ? subjects : subjects.filter((s) => s.optimization_tier === tierFilter);

  const tierTabs: { key: OptimizationTier | "all"; label: string }[] = [
    { key: "all",       label: `Tous (${summary.total})` },
    { key: "excellent", label: `Excellent (${summary.tier_counts.excellent})` },
    { key: "good",      label: `Bon (${summary.tier_counts.good})` },
    { key: "fair",      label: `Moyen (${summary.tier_counts.fair})` },
    { key: "weak",      label: `Faible (${summary.tier_counts.weak})` },
  ];

  return (
    <div className="p-6 space-y-6 text-slate-100">
      <div>
        <h1 className="text-2xl font-bold text-white">Optimiseur de Sujets Email</h1>
        <p className="text-slate-400 text-sm mt-1">
          Prédiction du taux d'ouverture — longueur, personnalisation, urgence, clarté, question, emojis
        </p>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard label="Sujets analysés" value={summary.total} />
        <KpiCard
          label="Taux d'ouverture moyen"
          value={`${Math.round(summary.avg_open_rate * 100)}%`}
          accent={summary.avg_open_rate >= 0.28 ? "text-emerald-400" : "text-amber-400"}
        />
        <KpiCard
          label="Meilleur taux"
          value={`${Math.round(summary.best_open_rate * 100)}%`}
          accent="text-emerald-400"
        />
        <KpiCard
          label="Avec personnalisation"
          value={`${Math.round(summary.pct_with_personalization * 100)}%`}
          accent="text-indigo-400"
        />
      </div>

      {/* Live analyzer */}
      <LiveAnalyzer onResult={setLiveResult} />
      {liveResult && <ResultPanel result={liveResult} />}

      {/* Filter tabs */}
      <div className="flex flex-wrap gap-2">
        {tierTabs.map((t) => (
          <button
            key={t.key}
            onClick={() => setTierFilter(t.key)}
            className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${
              tierFilter === t.key ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-white"
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* Subject list */}
      <div className="space-y-3">
        {filtered.map((opt, idx) => {
          const s = TIER_STYLES[opt.optimization_tier];
          return (
            <div
              key={opt.subject.subject_id}
              className={`bg-slate-900 border rounded-xl p-4 ${opt.optimization_tier === "excellent" ? "border-emerald-800/50" : "border-slate-800"}`}
            >
              <div className="flex items-start gap-3">
                <span className="text-xs text-slate-600 font-mono pt-0.5 flex-shrink-0 w-6">#{idx + 1}</span>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap mb-1">
                    <TierBadge tier={opt.optimization_tier} />
                    {opt.subject.template_id && (
                      <span className="text-[10px] text-slate-500 font-mono">{opt.subject.template_id}</span>
                    )}
                    <span className="text-[10px] text-slate-600">v{opt.subject.variant_key} · {opt.subject.send_hour}h</span>
                  </div>
                  <p className="text-sm text-slate-200 mb-2">"{opt.subject.text}"</p>
                  <div className="grid grid-cols-3 md:grid-cols-6 gap-x-4 gap-y-1.5">
                    {(Object.entries(opt.dimension_scores) as [keyof DimensionScores, number][]).map(([k, v]) => (
                      <div key={k}>
                        <div className="text-[9px] text-slate-600 mb-0.5 truncate">{DIM_LABELS[k]}</div>
                        <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${v >= 80 ? "bg-emerald-500" : v >= 60 ? "bg-indigo-400" : v >= 40 ? "bg-amber-400" : "bg-red-500"}`}
                            style={{ width: `${v}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                  {opt.suggestions.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1">
                      {opt.suggestions.slice(0, 2).map((sg, i) => (
                        <span key={i} className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded">
                          {sg.slice(0, 50)}{sg.length > 50 ? "…" : ""}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                <div className="flex-shrink-0 text-right">
                  <p className={`text-2xl font-bold ${s.text}`}>{Math.round(opt.predicted_open_rate * 100)}%</p>
                  <p className="text-[10px] text-slate-600">ouverture</p>
                </div>
              </div>
            </div>
          );
        })}
        {filtered.length === 0 && (
          <div className="text-center py-12 text-slate-500">Aucun sujet pour ce filtre</div>
        )}
      </div>
    </div>
  );
}
