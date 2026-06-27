"use client";

import { useEffect, useState } from "react";

// ── Types ──────────────────────────────────────────────────────────────────────

interface Message {
  direction: "outbound" | "inbound";
  content: string;
  timestamp: string;
  agent_id: string;
  sentiment: string;
  objection_type: string;
}

interface SentimentPoint {
  sentiment: string;
  score: number;
  timestamp: string;
}

interface Prospect {
  prospect_id: string;
  company_name: string;
  sector: string;
  email: string;
  created_at: string;
  stage: string;
  touch_count: number;
  reply_count: number;
  latest_sentiment: string | null;
  sentiment_trend: string;
  objections_seen: string[];
  tags: string[];
  assigned_agent: string;
  quote_eur: number;
  notes: string;
  last_contacted_at: string | null;
  message_count: number;
  messages: Message[];
  sentiment_history: SentimentPoint[];
}

interface Summary {
  total_prospects: number;
  by_stage: Record<string, number>;
  active_negotiations: number;
  won_deals: number;
  total_won_revenue_eur: number;
  total_messages: number;
  avg_touches: number;
}

interface MemoryData {
  source: string;
  summary: Summary;
  prospects: Prospect[];
}

// ── Colour maps ────────────────────────────────────────────────────────────────

const STAGE_COLORS: Record<string, string> = {
  detected:     "bg-gray-500/20 text-gray-400",
  contacted:    "bg-blue-500/20 text-blue-400",
  opened:       "bg-sky-500/20 text-sky-400",
  replied:      "bg-indigo-500/20 text-indigo-400",
  negotiating:  "bg-amber-500/20 text-amber-400",
  quoted:       "bg-orange-500/20 text-orange-400",
  won:          "bg-emerald-500/20 text-emerald-400",
  lost:         "bg-red-500/20 text-red-400",
  unsubscribed: "bg-rose-500/20 text-rose-400",
};

const SENTIMENT_COLORS: Record<string, string> = {
  positif:   "text-emerald-400",
  curieux:   "text-sky-400",
  neutre:    "text-gray-400",
  sceptique: "text-amber-400",
  méfiant:   "text-orange-400",
  négatif:   "text-red-400",
};

const TREND_ICONS: Record<string, string> = {
  improving: "↑",
  declining: "↓",
  stable:    "→",
  unknown:   "?",
};

const TREND_COLORS: Record<string, string> = {
  improving: "text-emerald-400",
  declining: "text-red-400",
  stable:    "text-gray-400",
  unknown:   "text-gray-600",
};

// ── Helpers ────────────────────────────────────────────────────────────────────

const STAGE_ORDER = ["detected","contacted","opened","replied","negotiating","quoted","won","lost","unsubscribed"];

function daysAgo(iso: string | null) {
  if (!iso) return "—";
  const d = (Date.now() - new Date(iso).getTime()) / 86400000;
  if (d < 1) return "aujourd'hui";
  return `il y a ${Math.floor(d)}j`;
}

function capitalise(s: string) { return s.charAt(0).toUpperCase() + s.slice(1); }

// ── Sub-components ─────────────────────────────────────────────────────────────

function KpiCard({ label, value, color }: { label: string; value: string | number; color?: string }) {
  return (
    <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
      <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">{label}</p>
      <p className={`text-2xl font-bold ${color ?? "text-white"}`}>{value}</p>
    </div>
  );
}

function StageFunnel({ byStage }: { byStage: Record<string, number> }) {
  const stages = STAGE_ORDER.filter(s => byStage[s]);
  const max = Math.max(...stages.map(s => byStage[s] ?? 0), 1);
  return (
    <div className="space-y-2">
      {stages.map(stage => {
        const count = byStage[stage] ?? 0;
        const pct   = (count / max) * 100;
        return (
          <div key={stage} className="flex items-center gap-3">
            <span className={`text-xs px-2 py-0.5 rounded-full w-24 text-center shrink-0 ${STAGE_COLORS[stage] ?? "bg-gray-500/20 text-gray-400"}`}>
              {capitalise(stage)}
            </span>
            <div className="flex-1 h-2 bg-white/[0.05] rounded-full overflow-hidden">
              <div className="h-full bg-indigo-500 rounded-full transition-all" style={{ width: `${pct}%` }} />
            </div>
            <span className="text-sm font-bold text-right w-6">{count}</span>
          </div>
        );
      })}
    </div>
  );
}

function MessageBubble({ msg }: { msg: Message }) {
  const isOut = msg.direction === "outbound";
  return (
    <div className={`flex ${isOut ? "justify-end" : "justify-start"}`}>
      <div className={`max-w-xs rounded-xl px-3 py-2 text-xs ${isOut ? "bg-indigo-600/30 text-indigo-100" : "bg-white/[0.06] text-gray-300"}`}>
        <p className="leading-relaxed">{msg.content}</p>
        <p className={`mt-1 text-[10px] ${isOut ? "text-indigo-300/60" : "text-gray-500"}`}>
          {isOut ? `Agent ${msg.agent_id}` : msg.objection_type !== "none" ? `Obj: ${msg.objection_type}` : ""}
          {" "}{daysAgo(msg.timestamp)}
        </p>
      </div>
    </div>
  );
}

function ProspectRow({ prospect, onClick }: { prospect: Prospect; onClick: () => void }) {
  return (
    <tr
      className="border-b border-white/[0.04] hover:bg-white/[0.02] cursor-pointer transition-colors"
      onClick={onClick}
    >
      <td className="py-3 px-4">
        <p className="font-medium text-sm">{prospect.company_name}</p>
        <p className="text-xs text-gray-500">{prospect.sector}</p>
      </td>
      <td className="py-3 px-4">
        <span className={`text-xs px-2 py-0.5 rounded-full ${STAGE_COLORS[prospect.stage] ?? "bg-gray-500/20 text-gray-400"}`}>
          {capitalise(prospect.stage)}
        </span>
      </td>
      <td className="py-3 px-4 text-sm font-mono text-indigo-400">{prospect.assigned_agent}</td>
      <td className="py-3 px-4 text-sm">
        <span className={SENTIMENT_COLORS[prospect.latest_sentiment ?? ""] ?? "text-gray-400"}>
          {prospect.latest_sentiment ? capitalise(prospect.latest_sentiment) : "—"}
        </span>
        {" "}
        <span className={`text-xs ${TREND_COLORS[prospect.sentiment_trend]}`}>
          {TREND_ICONS[prospect.sentiment_trend]}
        </span>
      </td>
      <td className="py-3 px-4 text-sm">{prospect.touch_count} / {prospect.reply_count}</td>
      <td className="py-3 px-4 text-xs text-gray-500">{daysAgo(prospect.last_contacted_at)}</td>
      <td className="py-3 px-4 text-sm">
        {prospect.quote_eur > 0
          ? <span className="text-emerald-400 font-semibold">{prospect.quote_eur.toLocaleString()}€</span>
          : <span className="text-gray-600">—</span>}
      </td>
    </tr>
  );
}

function ProspectDetail({ prospect, onClose }: { prospect: Prospect; onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div
        className="bg-[#0f1117] border border-white/[0.08] rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto"
        onClick={e => e.stopPropagation()}
      >
        <div className="flex items-start justify-between p-5 border-b border-white/[0.06]">
          <div>
            <h2 className="text-lg font-bold">{prospect.company_name}</h2>
            <p className="text-sm text-gray-500">{prospect.sector} · {prospect.email}</p>
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-white transition-colors text-xl leading-none">×</button>
        </div>

        <div className="p-5 space-y-5">
          {/* Stage + KPIs */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-white/[0.03] rounded-xl p-3 text-center">
              <p className="text-xs text-gray-500">Stage</p>
              <span className={`text-xs px-2 py-0.5 rounded-full mt-1 inline-block ${STAGE_COLORS[prospect.stage] ?? ""}`}>
                {capitalise(prospect.stage)}
              </span>
            </div>
            <div className="bg-white/[0.03] rounded-xl p-3 text-center">
              <p className="text-xs text-gray-500">Contacts</p>
              <p className="text-lg font-bold">{prospect.touch_count}</p>
            </div>
            <div className="bg-white/[0.03] rounded-xl p-3 text-center">
              <p className="text-xs text-gray-500">Réponses</p>
              <p className="text-lg font-bold">{prospect.reply_count}</p>
            </div>
            <div className="bg-white/[0.03] rounded-xl p-3 text-center">
              <p className="text-xs text-gray-500">Devis</p>
              <p className="text-lg font-bold text-emerald-400">
                {prospect.quote_eur > 0 ? `${prospect.quote_eur.toLocaleString()}€` : "—"}
              </p>
            </div>
          </div>

          {/* Sentiment & Objections */}
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-white/[0.03] rounded-xl p-3">
              <p className="text-xs text-gray-500 mb-2">Sentiment</p>
              <div className="flex items-center gap-2">
                <span className={`font-semibold ${SENTIMENT_COLORS[prospect.latest_sentiment ?? ""] ?? "text-gray-400"}`}>
                  {prospect.latest_sentiment ? capitalise(prospect.latest_sentiment) : "—"}
                </span>
                <span className={`text-sm ${TREND_COLORS[prospect.sentiment_trend]}`}>
                  {TREND_ICONS[prospect.sentiment_trend]} {prospect.sentiment_trend}
                </span>
              </div>
            </div>
            <div className="bg-white/[0.03] rounded-xl p-3">
              <p className="text-xs text-gray-500 mb-2">Objections</p>
              <div className="flex flex-wrap gap-1">
                {prospect.objections_seen.length > 0
                  ? prospect.objections_seen.map(o => (
                      <span key={o} className="text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded-full">{o}</span>
                    ))
                  : <span className="text-xs text-gray-600">Aucune</span>
                }
              </div>
            </div>
          </div>

          {/* Conversation */}
          {prospect.messages.length > 0 && (
            <div>
              <p className="text-xs text-gray-500 uppercase tracking-wider mb-3">Derniers échanges</p>
              <div className="space-y-2">
                {prospect.messages.map((msg, i) => <MessageBubble key={i} msg={msg} />)}
              </div>
            </div>
          )}

          {/* Assigned agent */}
          <div className="flex items-center justify-between text-sm text-gray-500 border-t border-white/[0.05] pt-4">
            <span>Agent assigné : <span className="font-mono text-indigo-400">{prospect.assigned_agent || "—"}</span></span>
            <span>Dernier contact : {daysAgo(prospect.last_contacted_at)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Page ───────────────────────────────────────────────────────────────────────

const STAGE_FILTERS = ["all", "contacted", "replied", "negotiating", "quoted", "won", "lost"] as const;
type StageFilter = typeof STAGE_FILTERS[number];

export default function MemoryPage() {
  const [data, setData]       = useState<MemoryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter]   = useState<StageFilter>("all");
  const [search, setSearch]   = useState("");
  const [selected, setSelected] = useState<Prospect | null>(null);

  useEffect(() => {
    fetch("/api/memory")
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

  if (!data) return <p className="text-gray-500 p-8">Erreur de chargement.</p>;

  const { summary } = data;

  const filtered = data.prospects.filter(p => {
    if (filter !== "all" && p.stage !== filter) return false;
    if (search) {
      const q = search.toLowerCase();
      return p.company_name.toLowerCase().includes(q) || p.sector.toLowerCase().includes(q) || p.email.toLowerCase().includes(q);
    }
    return true;
  });

  return (
    <div className="p-6 space-y-6 max-w-7xl mx-auto">
      {selected && <ProspectDetail prospect={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Mémoire Prospects</h1>
          <p className="text-sm text-gray-500 mt-0.5">Historique complet des interactions par prospect</p>
        </div>
        {data.source === "mock" && (
          <span className="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-1 rounded-full">
            Données démo
          </span>
        )}
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
        <KpiCard label="Prospects" value={summary.total_prospects} />
        <KpiCard label="Négociations" value={summary.active_negotiations} color="text-amber-400" />
        <KpiCard label="Gagnés" value={summary.won_deals} color="text-emerald-400" />
        <KpiCard label="CA gagné" value={`${summary.total_won_revenue_eur.toLocaleString()}€`} color="text-emerald-400" />
        <KpiCard label="Messages" value={summary.total_messages} />
        <KpiCard label="Moy. contacts" value={summary.avg_touches} />
        <KpiCard label="Source" value={data.source === "live" ? "Live" : "Démo"} color={data.source === "live" ? "text-emerald-400" : "text-amber-400"} />
      </div>

      {/* Funnel + filters */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl p-4">
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-3">Entonnoir</p>
          <StageFunnel byStage={summary.by_stage} />
        </div>

        <div className="lg:col-span-2 space-y-3">
          {/* Search */}
          <input
            type="text"
            placeholder="Rechercher une entreprise, secteur…"
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full bg-white/[0.03] border border-white/[0.07] rounded-xl px-4 py-2.5 text-sm text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500/50"
          />

          {/* Stage filter tabs */}
          <div className="flex flex-wrap gap-2">
            {STAGE_FILTERS.map(f => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
                  filter === f
                    ? "bg-indigo-600 border-indigo-500 text-white"
                    : "bg-white/[0.03] border-white/[0.07] text-gray-400 hover:text-white"
                }`}
              >
                {f === "all" ? "Tous" : capitalise(f)}
                {f !== "all" && summary.by_stage[f] ? ` (${summary.by_stage[f]})` : ""}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Prospect table */}
      <div className="bg-white/[0.03] border border-white/[0.07] rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[700px]">
            <thead>
              <tr className="border-b border-white/[0.06]">
                {["Entreprise", "Stage", "Agent", "Sentiment", "Contacts/Rép.", "Dernier contact", "Devis"].map(h => (
                  <th key={h} className="text-left py-3 px-4 text-xs text-gray-500 uppercase tracking-wider font-medium">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan={7} className="text-center py-10 text-gray-600 text-sm">
                    Aucun prospect pour ce filtre.
                  </td>
                </tr>
              ) : (
                filtered.map(p => (
                  <ProspectRow key={p.prospect_id} prospect={p} onClick={() => setSelected(p)} />
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      <p className="text-xs text-gray-600 text-center">
        {filtered.length} prospect{filtered.length > 1 ? "s" : ""} affichés — Cliquer pour voir l'historique complet
      </p>
    </div>
  );
}
