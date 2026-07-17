"use client";

import { useEffect, useState } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type Reason = "opt_out" | "bounce" | "spam" | "unreachable" | "competitor" | "client";

interface SuppressionEntry {
  key: string;
  key_type: "email" | "domain";
  reason: Reason;
  added_at: string;
  note: string;
}

interface Summary {
  unique_emails_contacted: number;
  unique_domains_contacted: number;
  suppression_list_size: number;
  fingerprints_seen: number;
  total_contact_events: number;
}

interface DedupData {
  source: string;
  summary: Summary;
  entries: SuppressionEntry[];
}

// ─── Constants ────────────────────────────────────────────────────────────────

const REASON_META: Record<Reason, { label: string; color: string; bg: string }> = {
  opt_out:     { label: "Opt-out", color: "text-red-300", bg: "bg-red-900/30 border-red-700" },
  bounce:      { label: "Bounce", color: "text-orange-300", bg: "bg-orange-900/30 border-orange-700" },
  spam:        { label: "Spam", color: "text-yellow-300", bg: "bg-yellow-900/30 border-yellow-700" },
  unreachable: { label: "Injoignable", color: "text-slate-300", bg: "bg-slate-800 border-slate-600" },
  competitor:  { label: "Concurrent", color: "text-purple-300", bg: "bg-purple-900/30 border-purple-700" },
  client:      { label: "Client", color: "text-emerald-300", bg: "bg-emerald-900/30 border-emerald-700" },
};

// ─── Sub-components ───────────────────────────────────────────────────────────

function ReasonBadge({ reason }: { reason: Reason }) {
  const m = REASON_META[reason] ?? { label: reason, color: "text-slate-400", bg: "bg-slate-800 border-slate-600" };
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${m.bg} ${m.color}`}>
      {m.label}
    </span>
  );
}

function TypeBadge({ type }: { type: "email" | "domain" }) {
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-mono border ${
      type === "domain"
        ? "bg-indigo-900/30 border-indigo-700 text-indigo-300"
        : "bg-slate-800 border-slate-600 text-slate-300"
    }`}>
      {type}
    </span>
  );
}

function KpiCard({ label, value, sub, accent }: {
  label: string; value: string | number; sub?: string; accent?: string;
}) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col gap-1">
      <p className="text-xs text-slate-500 font-medium uppercase tracking-wider">{label}</p>
      <p className={`text-2xl font-bold ${accent ?? "text-white"}`}>{value}</p>
      {sub && <p className="text-xs text-slate-500">{sub}</p>}
    </div>
  );
}

function formatDate(iso: string) {
  try {
    return new Date(iso).toLocaleDateString("fr-FR", { day: "2-digit", month: "short", year: "numeric" });
  } catch {
    return iso;
  }
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function DedupPage() {
  const [data, setData] = useState<DedupData | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | Reason>("all");

  useEffect(() => {
    setLoading(true);
    fetch("/api/dedup")
      .then((r) => r.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-slate-500 text-center py-16">Chargement…</div>;
  if (!data) return <p className="text-slate-500 p-8">Erreur de chargement.</p>;

  const { summary, entries } = data;

  // Reason distribution
  const reasonCounts: Record<string, number> = {};
  for (const e of entries) {
    reasonCounts[e.reason] = (reasonCounts[e.reason] ?? 0) + 1;
  }

  const filtered = filter === "all" ? entries : entries.filter((e) => e.reason === filter);
  const reasons = Object.keys(REASON_META) as Reason[];

  return (
    <div className="p-6 space-y-6 text-slate-100">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Déduplication & Suppression</h1>
          <p className="text-slate-400 text-sm mt-1">
            Liste noire RGPD, déduplication des contacts et fingerprints
          </p>
        </div>
        {data.source === "mock" && (
          <span className="text-xs bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-1 rounded-full">
            Données démo
          </span>
        )}
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
        <KpiCard label="Emails contactés" value={summary.unique_emails_contacted.toLocaleString("fr-FR")} accent="text-indigo-400" />
        <KpiCard label="Domaines" value={summary.unique_domains_contacted.toLocaleString("fr-FR")} accent="text-blue-400" />
        <KpiCard label="Supprimés" value={summary.suppression_list_size} sub="liste noire" accent="text-red-400" />
        <KpiCard label="Fingerprints" value={summary.fingerprints_seen.toLocaleString("fr-FR")} sub="vus" accent="text-purple-400" />
        <KpiCard label="Événements" value={summary.total_contact_events.toLocaleString("fr-FR")} sub="total" accent="text-slate-300" />
      </div>

      {/* Reason distribution */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">
          Répartition par raison de suppression
        </h3>
        <div className="flex flex-wrap gap-3">
          {reasons.map((reason) => {
            const count = reasonCounts[reason] ?? 0;
            if (count === 0) return null;
            const m = REASON_META[reason];
            const pct = Math.round((count / entries.length) * 100);
            return (
              <button
                key={reason}
                onClick={() => setFilter(filter === reason ? "all" : reason)}
                className={`flex items-center gap-3 rounded-lg px-4 py-3 border transition-colors ${
                  filter === reason ? "ring-2 ring-indigo-500" : ""
                } ${m.bg} hover:opacity-90`}
              >
                <div>
                  <p className={`text-sm font-semibold ${m.color}`}>{m.label}</p>
                  <p className="text-slate-400 text-xs">{count} entrée{count > 1 ? "s" : ""} · {pct}%</p>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-2 flex-wrap">
        <button
          onClick={() => setFilter("all")}
          className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors border ${
            filter === "all"
              ? "bg-indigo-600 border-indigo-500 text-white"
              : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white"
          }`}
        >
          Tous <span className="ml-1.5 opacity-70">{entries.length}</span>
        </button>
        {reasons.map((reason) => {
          const count = reasonCounts[reason] ?? 0;
          if (count === 0) return null;
          return (
            <button
              key={reason}
              onClick={() => setFilter(filter === reason ? "all" : reason)}
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors border ${
                filter === reason
                  ? "bg-indigo-600 border-indigo-500 text-white"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white"
              }`}
            >
              {REASON_META[reason].label} <span className="ml-1.5 opacity-70">{count}</span>
            </button>
          );
        })}
      </div>

      {/* Suppression table */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-800">
              <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider">Type</th>
              <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider">Clé</th>
              <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider">Raison</th>
              <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider hidden sm:table-cell">Ajouté le</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={4} className="text-center text-slate-500 py-10">
                  Aucune entrée pour ce filtre.
                </td>
              </tr>
            ) : (
              filtered.map((entry, i) => (
                <tr key={i} className="border-b border-slate-800/50 hover:bg-slate-800/30 transition-colors">
                  <td className="py-3 px-4">
                    <TypeBadge type={entry.key_type} />
                  </td>
                  <td className="py-3 px-4">
                    <p className="text-slate-300 text-sm font-mono truncate max-w-xs">{entry.key}</p>
                  </td>
                  <td className="py-3 px-4">
                    <ReasonBadge reason={entry.reason} />
                  </td>
                  <td className="py-3 px-4 hidden sm:table-cell">
                    <span className="text-slate-500 text-xs">{formatDate(entry.added_at)}</span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <p className="text-xs text-slate-600 text-center">
        {filtered.length} entr{filtered.length > 1 ? "ées" : "ée"} — conformité RGPD assurée
      </p>
    </div>
  );
}
