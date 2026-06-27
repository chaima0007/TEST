"use client";

import { useEffect, useRef, useState } from "react";

// ─── Types ───────────────────────────────────────────────────────────────────

type ObjectionType = "price" | "trust" | "timing" | "competitor" | "technical" | "none";
type Timeline = "immédiat" | "sous_48h" | "cette_semaine" | "dans_un_mois" | "indéfini";
type Priority = "urgent" | "high" | "normal" | "low";

interface ClassificationResult {
  objection_type: ObjectionType;
  timeline: Timeline;
  buying_signal: number;
  competitor_mentioned: boolean;
  objection_keywords: string[];
  buying_keywords: string[];
  next_action: string;
  priority: Priority;
}

interface ReplyRecord {
  reply_id: string;
  prospect_id: string;
  company_name: string;
  sector: string;
  email_subject: string;
  email_snippet: string;
  received_at: string;
  classification: ClassificationResult;
}

interface Summary {
  total: number;
  urgent: number;
  high: number;
  normal: number;
  low: number;
  avg_buying_signal: number;
  objection_distribution: Record<string, number>;
  competitor_mentions: number;
  timeline_distribution: Record<string, number>;
}

// ─── Constants ───────────────────────────────────────────────────────────────

const OBJECTION_LABELS: Record<ObjectionType, string> = {
  price: "Prix",
  trust: "Confiance",
  timing: "Timing",
  competitor: "Concurrent",
  technical: "Technique",
  none: "Aucune",
};

const OBJECTION_COLORS: Record<ObjectionType, string> = {
  price: "bg-red-900/50 text-red-300 border-red-700",
  trust: "bg-amber-900/50 text-amber-300 border-amber-700",
  timing: "bg-blue-900/50 text-blue-300 border-blue-700",
  competitor: "bg-purple-900/50 text-purple-300 border-purple-700",
  technical: "bg-cyan-900/50 text-cyan-300 border-cyan-700",
  none: "bg-emerald-900/50 text-emerald-300 border-emerald-700",
};

const PRIORITY_COLORS: Record<Priority, string> = {
  urgent: "text-red-400",
  high: "text-orange-400",
  normal: "text-yellow-400",
  low: "text-slate-400",
};

const PRIORITY_BADGE: Record<Priority, string> = {
  urgent: "bg-red-500 text-white",
  high: "bg-orange-500 text-white",
  normal: "bg-yellow-500 text-white",
  low: "bg-slate-600 text-white",
};

const TIMELINE_LABELS: Record<Timeline, string> = {
  "immédiat": "Immédiat",
  "sous_48h": "< 48h",
  "cette_semaine": "Cette semaine",
  "dans_un_mois": "Dans 1 mois",
  "indéfini": "Indéfini",
};

const OBJECTION_FILTERS = [
  { key: "all", label: "Toutes" },
  { key: "price", label: "Prix" },
  { key: "trust", label: "Confiance" },
  { key: "timing", label: "Timing" },
  { key: "competitor", label: "Concurrent" },
  { key: "technical", label: "Technique" },
  { key: "none", label: "Positif" },
];

// ─── Sub-components ───────────────────────────────────────────────────────────

function ObjectionBadge({ type }: { type: ObjectionType }) {
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium border ${OBJECTION_COLORS[type]}`}
    >
      {OBJECTION_LABELS[type]}
    </span>
  );
}

function BuyingBar({ score }: { score: number }) {
  const pct = Math.round(score * 100);
  const color =
    pct >= 75 ? "bg-emerald-500" : pct >= 50 ? "bg-yellow-500" : pct >= 25 ? "bg-orange-500" : "bg-slate-600";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 bg-slate-800 rounded-full h-1.5 overflow-hidden">
        <div className={`h-1.5 rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-xs tabular-nums text-slate-400 w-8 text-right">{pct}%</span>
    </div>
  );
}

function KpiCard({ label, value, sub, accent }: { label: string; value: string | number; sub?: string; accent?: string }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col gap-1">
      <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-slate-500">{sub}</p>}
    </div>
  );
}

function timeAgo(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 60) return `${mins}min`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h`;
  return `${Math.floor(hrs / 24)}j`;
}

// ─── Live Classifier Panel ───────────────────────────────────────────────────

function ClassifierPanel() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<ClassificationResult | null>(null);
  const [loading, setLoading] = useState(false);

  const classify = async () => {
    if (!text.trim()) return;
    setLoading(true);
    try {
      const res = await fetch("/api/replies", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      setResult(data.classification);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
      <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider">
        Analyser une réponse
      </h3>
      <textarea
        className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-indigo-500 resize-none"
        rows={4}
        placeholder="Collez ici le texte de la réponse email du prospect…"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button
        onClick={classify}
        disabled={loading || !text.trim()}
        className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white text-sm font-medium rounded-lg transition-colors"
      >
        {loading ? "Analyse…" : "Classifier"}
      </button>

      {result && (
        <div className="border-t border-slate-800 pt-4 space-y-3">
          <div className="flex flex-wrap gap-2 items-center">
            <ObjectionBadge type={result.objection_type} />
            <span className={`text-sm font-semibold ${PRIORITY_COLORS[result.priority]}`}>
              {result.priority.toUpperCase()}
            </span>
            <span className="text-xs text-slate-500 bg-slate-800 px-2 py-0.5 rounded">
              {TIMELINE_LABELS[result.timeline]}
            </span>
            {result.competitor_mentioned && (
              <span className="text-xs bg-purple-900/50 text-purple-300 border border-purple-700 px-2 py-0.5 rounded-full">
                Concurrent mentionné
              </span>
            )}
          </div>
          <div>
            <p className="text-xs text-slate-500 mb-1">Signal d'achat</p>
            <BuyingBar score={result.buying_signal} />
          </div>
          {result.buying_keywords.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {result.buying_keywords.map((k) => (
                <span key={k} className="text-[10px] bg-emerald-900/40 text-emerald-400 px-1.5 py-0.5 rounded">
                  {k}
                </span>
              ))}
            </div>
          )}
          {result.objection_keywords.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {result.objection_keywords.map((k) => (
                <span key={k} className="text-[10px] bg-red-900/40 text-red-400 px-1.5 py-0.5 rounded">
                  {k}
                </span>
              ))}
            </div>
          )}
          <div className="bg-indigo-950/40 border border-indigo-900/50 rounded-lg p-3">
            <p className="text-xs text-indigo-400 font-semibold mb-1">Action recommandée</p>
            <p className="text-slate-300 text-sm">{result.next_action}</p>
          </div>
        </div>
      )}
    </div>
  );
}

// ─── Detail Modal ─────────────────────────────────────────────────────────────

function DetailModal({ reply, onClose }: { reply: ReplyRecord; onClose: () => void }) {
  useEffect(() => {
    const h = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const c = reply.classification;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl w-full max-w-lg mx-4 p-6 space-y-5"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-3">
          <div>
            <h2 className="text-white font-bold text-lg">{reply.company_name}</h2>
            <p className="text-slate-400 text-sm">{reply.email_subject}</p>
          </div>
          <span className={`flex-shrink-0 text-xs font-bold px-2 py-0.5 rounded ${PRIORITY_BADGE[c.priority]}`}>
            {c.priority.toUpperCase()}
          </span>
        </div>

        <div className="bg-slate-800/60 rounded-lg p-3 text-slate-300 text-sm italic border-l-2 border-slate-600">
          "{reply.email_snippet}"
        </div>

        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">Objection</p>
            <ObjectionBadge type={c.objection_type} />
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">Délai</p>
            <p className="text-white font-medium">{TIMELINE_LABELS[c.timeline]}</p>
          </div>
        </div>

        <div>
          <p className="text-xs text-slate-500 mb-2">Signal d'achat</p>
          <BuyingBar score={c.buying_signal} />
        </div>

        {c.buying_keywords.length > 0 && (
          <div>
            <p className="text-xs text-slate-500 mb-1">Signaux positifs</p>
            <div className="flex flex-wrap gap-1">
              {c.buying_keywords.map((k) => (
                <span key={k} className="text-[10px] bg-emerald-900/40 text-emerald-400 px-2 py-0.5 rounded border border-emerald-800">
                  {k}
                </span>
              ))}
            </div>
          </div>
        )}

        {c.objection_keywords.length > 0 && (
          <div>
            <p className="text-xs text-slate-500 mb-1">Mots-clés objection</p>
            <div className="flex flex-wrap gap-1">
              {c.objection_keywords.map((k) => (
                <span key={k} className="text-[10px] bg-red-900/40 text-red-400 px-2 py-0.5 rounded border border-red-800">
                  {k}
                </span>
              ))}
            </div>
          </div>
        )}

        {c.competitor_mentioned && (
          <p className="text-xs text-purple-400 bg-purple-900/20 border border-purple-900 rounded-lg px-3 py-2">
            Concurrent mentionné — activer Agent 3.1 (différenciation)
          </p>
        )}

        <div className="bg-indigo-950/40 border border-indigo-900/50 rounded-lg p-3">
          <p className="text-xs text-indigo-400 font-semibold mb-1">Action recommandée</p>
          <p className="text-slate-300 text-sm">{c.next_action}</p>
        </div>

        <button
          onClick={onClose}
          className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium transition-colors"
        >
          Fermer
        </button>
      </div>
    </div>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function RepliesPage() {
  const [replies, setReplies] = useState<ReplyRecord[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<ReplyRecord | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/replies")
      .then((r) => r.json())
      .then((d) => {
        setReplies(d.replies ?? []);
        setSummary(d.summary ?? null);
      })
      .finally(() => setLoading(false));
  }, []);

  const filtered =
    filter === "all" ? replies : replies.filter((r) => r.classification.objection_type === filter);

  return (
    <div className="p-6 space-y-6 text-slate-100">
      <div>
        <h1 className="text-2xl font-bold text-white">Analyse des Réponses</h1>
        <p className="text-slate-400 text-sm mt-1">
          Classificateur d'intentions — objections, signaux d'achat, actions recommandées
        </p>
      </div>

      {/* KPI Strip */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <KpiCard label="Total" value={summary.total} />
          <KpiCard label="Urgents" value={summary.urgent} accent="text-red-400" />
          <KpiCard label="Haute prio." value={summary.high} accent="text-orange-400" />
          <KpiCard
            label="Signal moy."
            value={`${Math.round(summary.avg_buying_signal * 100)}%`}
            sub="d'achat"
            accent="text-emerald-400"
          />
          <KpiCard
            label="Concurrents"
            value={summary.competitor_mentions}
            accent={summary.competitor_mentions > 0 ? "text-purple-400" : "text-slate-400"}
          />
          <KpiCard label="Pas d'objection" value={summary.objection_distribution["none"] ?? 0} accent="text-emerald-400" />
        </div>
      )}

      {/* Objection distribution */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">
            Distribution des objections
          </h3>
          <div className="flex flex-wrap gap-3">
            {Object.entries(summary.objection_distribution)
              .sort(([, a], [, b]) => b - a)
              .map(([type, count]) => (
                <div
                  key={type}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg border text-sm cursor-pointer transition-opacity ${
                    OBJECTION_COLORS[type as ObjectionType] ?? "bg-slate-800 text-slate-300 border-slate-700"
                  } ${filter === type ? "opacity-100 ring-2 ring-white/30" : "opacity-80 hover:opacity-100"}`}
                  onClick={() => setFilter(filter === type ? "all" : type)}
                >
                  <span className="font-medium">{OBJECTION_LABELS[type as ObjectionType] ?? type}</span>
                  <span className="font-bold tabular-nums">{count}</span>
                </div>
              ))}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Replies table */}
        <div className="xl:col-span-2 space-y-4">
          {/* Filter tabs */}
          <div className="flex gap-2 flex-wrap">
            {OBJECTION_FILTERS.map((tab) => (
              <button
                key={tab.key}
                onClick={() => setFilter(tab.key)}
                className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors border ${
                  filter === tab.key
                    ? "bg-indigo-600 border-indigo-500 text-white"
                    : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white hover:border-slate-600"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {loading ? (
            <div className="text-slate-500 py-16 text-center">Chargement…</div>
          ) : (
            <div className="space-y-2">
              {filtered.map((reply) => (
                <div
                  key={reply.reply_id}
                  onClick={() => setSelected(reply)}
                  className="bg-slate-900 border border-slate-800 hover:border-slate-600 rounded-xl p-4 cursor-pointer transition-all"
                >
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div className="min-w-0">
                      <p className="text-white font-medium truncate">{reply.company_name}</p>
                      <p className="text-slate-500 text-xs truncate">{reply.email_subject}</p>
                    </div>
                    <div className="flex flex-col items-end gap-1 flex-shrink-0">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${PRIORITY_BADGE[reply.classification.priority]}`}>
                        {reply.classification.priority.toUpperCase()}
                      </span>
                      <span className="text-xs text-slate-500">{timeAgo(reply.received_at)}</span>
                    </div>
                  </div>

                  <p className="text-slate-400 text-xs line-clamp-2 italic mb-3">
                    "{reply.email_snippet}"
                  </p>

                  <div className="flex flex-wrap items-center gap-2">
                    <ObjectionBadge type={reply.classification.objection_type} />
                    <span className="text-xs text-slate-500 bg-slate-800 px-2 py-0.5 rounded">
                      {TIMELINE_LABELS[reply.classification.timeline]}
                    </span>
                    {reply.classification.competitor_mentioned && (
                      <span className="text-[10px] text-purple-400">Concurrent</span>
                    )}
                    <div className="flex-1 min-w-[80px]">
                      <BuyingBar score={reply.classification.buying_signal} />
                    </div>
                  </div>
                </div>
              ))}
              {filtered.length === 0 && (
                <div className="text-slate-500 text-center py-10">Aucune réponse dans cette catégorie.</div>
              )}
            </div>
          )}
        </div>

        {/* Live Classifier */}
        <div>
          <ClassifierPanel />
        </div>
      </div>

      {selected && <DetailModal reply={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
