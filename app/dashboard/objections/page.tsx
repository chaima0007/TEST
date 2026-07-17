"use client";

import { useEffect, useState } from "react";

type ObjectionType =
  | "price"
  | "timing"
  | "competitor"
  | "trust"
  | "relevance"
  | "authority"
  | "satisfied"
  | "no_budget"
  | "too_busy"
  | "unknown";

interface RebuttalStats {
  total: number;
  wins: number;
  win_rate_pct: number;
}

interface Rebuttal {
  rebuttal_id: string;
  objection: ObjectionType;
  name: string;
  template_id: string;
  talking_points: string[];
  urgency_angle: boolean;
  social_proof: boolean;
  stats: RebuttalStats;
}

interface Summary {
  total_rebuttals: number;
  objection_types: number;
  avg_win_rate_pct: number;
  best_rebuttal: string;
  total_outcomes: number;
}

interface ApiData {
  rebuttals: Rebuttal[];
  summary: Summary;
  by_objection: Record<string, number>;
}

const OBJECTION_META: Record<ObjectionType, { label: string; color: string }> = {
  price:      { label: "Prix",        color: "bg-red-500/20 text-red-300 border-red-500/30" },
  timing:     { label: "Délai",       color: "bg-amber-500/20 text-amber-300 border-amber-500/30" },
  competitor: { label: "Concurrent",  color: "bg-violet-500/20 text-violet-300 border-violet-500/30" },
  trust:      { label: "Confiance",   color: "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" },
  relevance:  { label: "Pertinence",  color: "bg-blue-500/20 text-blue-300 border-blue-500/30" },
  authority:  { label: "Autorité",    color: "bg-indigo-500/20 text-indigo-300 border-indigo-500/30" },
  satisfied:  { label: "Satisfait",   color: "bg-teal-500/20 text-teal-300 border-teal-500/30" },
  no_budget:  { label: "Budget",      color: "bg-orange-500/20 text-orange-300 border-orange-500/30" },
  too_busy:   { label: "Trop occupé", color: "bg-slate-500/20 text-slate-300 border-slate-500/30" },
  unknown:    { label: "Inconnu",     color: "bg-slate-500/20 text-slate-400 border-slate-500/30" },
};

const FILTER_TABS: Array<{ key: ObjectionType | "all"; label: string }> = [
  { key: "all",       label: "Tous" },
  { key: "price",     label: "Prix" },
  { key: "timing",    label: "Délai" },
  { key: "competitor",label: "Concurrent" },
  { key: "trust",     label: "Confiance" },
  { key: "relevance", label: "Pertinence" },
  { key: "authority", label: "Autorité" },
  { key: "satisfied", label: "Satisfait" },
  { key: "no_budget", label: "Budget" },
  { key: "too_busy",  label: "Trop occupé" },
  { key: "unknown",   label: "Inconnu" },
];

function ObjectionBadge({ objection }: { objection: ObjectionType }) {
  const m = OBJECTION_META[objection];
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full border font-medium ${m.color}`}>
      {m.label}
    </span>
  );
}

function WinRateBar({ pct }: { pct: number }) {
  const color =
    pct >= 60 ? "bg-emerald-500" :
    pct >= 45 ? "bg-blue-500" :
    pct >= 30 ? "bg-amber-500" :
    "bg-slate-500";
  const textColor =
    pct >= 60 ? "text-emerald-400" :
    pct >= 45 ? "text-blue-400" :
    pct >= 30 ? "text-amber-400" :
    "text-slate-400";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-white/[0.05] rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className={`text-xs font-mono w-10 text-right ${textColor}`}>{pct}%</span>
    </div>
  );
}

function FlagChip({ type }: { type: "urgency" | "social" }) {
  if (type === "urgency") {
    return (
      <span className="text-xs font-medium text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded-full">
        Urgence
      </span>
    );
  }
  return (
    <span className="text-xs font-medium text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 px-2 py-0.5 rounded-full">
      Preuve sociale
    </span>
  );
}

function DetailModal({ rebuttal, onClose }: { rebuttal: Rebuttal; onClose: () => void }) {
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className="bg-[#0f1117] border border-white/[0.08] rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-start justify-between p-5 border-b border-white/[0.06] sticky top-0 bg-[#0f1117] z-10">
          <div className="flex items-center gap-2 flex-wrap">
            <h2 className="font-bold text-lg text-white">{rebuttal.name}</h2>
            <ObjectionBadge objection={rebuttal.objection} />
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-white text-xl ml-4 flex-shrink-0">
            ×
          </button>
        </div>

        <div className="p-5 space-y-5">
          <div>
            <p className="text-xs text-gray-500 mb-2">Taux de succès</p>
            <WinRateBar pct={rebuttal.stats.win_rate_pct} />
            <div className="flex gap-4 mt-2">
              <span className="text-xs text-gray-500">{rebuttal.stats.total} utilisations</span>
              <span className="text-xs text-gray-500">{rebuttal.stats.wins} succès</span>
            </div>
          </div>

          {(rebuttal.urgency_angle || rebuttal.social_proof) && (
            <div className="flex gap-2 flex-wrap">
              {rebuttal.urgency_angle && <FlagChip type="urgency" />}
              {rebuttal.social_proof && <FlagChip type="social" />}
            </div>
          )}

          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-3">Points clés</p>
            <ol className="space-y-2">
              {rebuttal.talking_points.map((point, i) => (
                <li key={i} className="flex gap-3">
                  <span className="flex-shrink-0 w-5 h-5 rounded-full bg-indigo-600/30 border border-indigo-500/30 text-indigo-400 text-xs flex items-center justify-center font-bold">
                    {i + 1}
                  </span>
                  <p className="text-sm text-gray-300 leading-relaxed">{point}</p>
                </li>
              ))}
            </ol>
          </div>

          <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-3">
            <p className="text-xs text-gray-500 mb-1">Template associé</p>
            <p className="text-sm font-mono text-indigo-300">{rebuttal.template_id}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function RebuttalCard({ rebuttal, onOpen }: { rebuttal: Rebuttal; onOpen: () => void }) {
  return (
    <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4 flex flex-col gap-3 hover:border-white/[0.12] transition-colors">
      <div className="flex items-start justify-between gap-2">
        <ObjectionBadge objection={rebuttal.objection} />
      </div>
      <p className="font-semibold text-white text-sm leading-snug">{rebuttal.name}</p>
      <div>
        <WinRateBar pct={rebuttal.stats.win_rate_pct} />
      </div>
      {(rebuttal.urgency_angle || rebuttal.social_proof) && (
        <div className="flex gap-1.5 flex-wrap">
          {rebuttal.urgency_angle && <FlagChip type="urgency" />}
          {rebuttal.social_proof && <FlagChip type="social" />}
        </div>
      )}
      <button
        onClick={onOpen}
        className="mt-auto text-xs text-indigo-400 hover:text-indigo-300 text-left transition-colors"
      >
        Voir les points clés →
      </button>
    </div>
  );
}

export default function ObjectionsPage() {
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<ObjectionType | "all">("all");
  const [selected, setSelected] = useState<Rebuttal | null>(null);

  useEffect(() => {
    fetch("/api/objections")
      .then(r => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!data) {
    return <p className="text-gray-500 p-8">Erreur de chargement.</p>;
  }

  const { rebuttals, summary } = data;

  const bestRebuttal = rebuttals.find(r => r.rebuttal_id === summary.best_rebuttal);

  const filtered =
    filter === "all" ? rebuttals : rebuttals.filter(r => r.objection === filter);

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {selected && <DetailModal rebuttal={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-white">Gestion des Objections</h1>
        <p className="text-sm text-gray-500 mt-0.5">
          14 stratégies de réponse · catalogue de rebuttals éprouvés
        </p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Total rebuttals</p>
          <p className="text-2xl font-bold text-white">{summary.total_rebuttals}</p>
        </div>
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">{"Types d'objections"}</p>
          <p className="text-2xl font-bold text-indigo-400">{summary.objection_types}</p>
        </div>
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Taux de succès moyen</p>
          <p className="text-2xl font-bold text-emerald-400">{summary.avg_win_rate_pct}%</p>
        </div>
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">Meilleur rebuttal</p>
          <p className="text-lg font-bold text-amber-400 truncate">{bestRebuttal?.name ?? "—"}</p>
        </div>
      </div>

      <div className="flex gap-2 flex-wrap">
        {FILTER_TABS.map(tab => (
          <button
            key={tab.key}
            onClick={() => setFilter(tab.key)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
              filter === tab.key
                ? "bg-indigo-600 border-indigo-500 text-white"
                : "bg-white/[0.03] border-white/[0.07] text-gray-400 hover:text-white"
            }`}
          >
            {tab.label}
            {tab.key !== "all" && data.by_objection[tab.key]
              ? ` (${data.by_objection[tab.key]})`
              : tab.key === "all"
              ? ` (${rebuttals.length})`
              : ""}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.length === 0 ? (
          <p className="text-gray-600 col-span-full text-center py-10 text-sm">Aucun rebuttal.</p>
        ) : filtered.map(r => (
          <RebuttalCard
            key={r.rebuttal_id}
            rebuttal={r}
            onOpen={() => setSelected(r)}
          />
        ))}
      </div>

      <p className="text-xs text-gray-600 text-center">
        {filtered.length} rebuttal(s) affiché(s) — Cliquer sur une carte pour le détail
      </p>
    </div>
  );
}
