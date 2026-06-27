"use client";

import { useEffect, useState } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type Tier = "A" | "B" | "C";
type UrgencyLabel = "critique" | "mauvais" | "moyen" | "acceptable" | "bon";

interface EnrichedProspect {
  company_id: string;
  name: string;
  sector: string;
  website: string;
  contact_email: string;
  pagespeed_score: number;
  load_time_ms: number;
  icp_fit: number;
  urgency: number;
  company_size: string;
  priority_score: number;
  tier: Tier;
  sector_score: number;
  urgency_label: UrgencyLabel;
  estimated_revenue_impact_eur: number;
  enrichment_notes: string[];
}

interface Summary {
  total: number;
  tier_A: number;
  tier_B: number;
  tier_C: number;
  avg_priority: number;
  total_revenue_impact_eur: number;
  urgency_distribution: Record<string, number>;
  sector_breakdown: Record<string, { count: number; avg_priority: number }>;
}

// ─── Constants ────────────────────────────────────────────────────────────────

const TIER_META: Record<Tier, { label: string; color: string; bg: string; border: string; desc: string }> = {
  A: { label: "Tier A", color: "text-emerald-400", bg: "bg-emerald-900/30", border: "border-emerald-700", desc: "Priorité maximale" },
  B: { label: "Tier B", color: "text-blue-400", bg: "bg-blue-900/30", border: "border-blue-700", desc: "Priorité normale" },
  C: { label: "Tier C", color: "text-slate-400", bg: "bg-slate-800", border: "border-slate-700", desc: "Faible priorité" },
};

const URGENCY_META: Record<UrgencyLabel, { color: string; dot: string }> = {
  critique:   { color: "text-red-400",    dot: "bg-red-500" },
  mauvais:    { color: "text-orange-400", dot: "bg-orange-500" },
  moyen:      { color: "text-amber-400",  dot: "bg-amber-500" },
  acceptable: { color: "text-blue-400",   dot: "bg-blue-500" },
  bon:        { color: "text-emerald-400",dot: "bg-emerald-500" },
};

// ─── Sub-components ───────────────────────────────────────────────────────────

function TierBadge({ tier }: { tier: Tier }) {
  const m = TIER_META[tier];
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold border ${m.bg} ${m.color} ${m.border}`}>
      {m.label}
    </span>
  );
}

function PriorityBar({ score, tier }: { score: number; tier: Tier }) {
  const barColor = tier === "A" ? "bg-emerald-500" : tier === "B" ? "bg-blue-500" : "bg-slate-600";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden min-w-[60px]">
        <div className={`h-2 rounded-full ${barColor} transition-all`} style={{ width: `${score}%` }} />
      </div>
      <span className="text-xs font-bold tabular-nums w-8 text-right text-slate-300">{score}</span>
    </div>
  );
}

function UrgencyPill({ label }: { label: UrgencyLabel }) {
  const m = URGENCY_META[label] ?? { color: "text-slate-400", dot: "bg-slate-500" };
  return (
    <span className={`flex items-center gap-1.5 text-xs font-medium capitalize ${m.color}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${m.dot}`} />
      {label}
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

// ─── Detail Modal ─────────────────────────────────────────────────────────────

function DetailModal({ prospect: p, onClose }: { prospect: EnrichedProspect; onClose: () => void }) {
  useEffect(() => {
    const h = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const tm = TIER_META[p.tier];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <div
        className={`bg-slate-900 border-2 ${tm.border} rounded-2xl shadow-2xl w-full max-w-lg mx-4 p-6 space-y-5`}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start gap-4">
          <div className={`w-12 h-12 rounded-xl flex items-center justify-center text-lg font-black border-2 ${tm.border} ${tm.bg} ${tm.color} flex-shrink-0`}>
            {p.tier}
          </div>
          <div className="flex-1">
            <h2 className="text-white font-bold text-lg">{p.name}</h2>
            <p className="text-slate-400 text-sm">{p.sector} · {p.company_size}</p>
            {p.website && <p className="text-slate-500 text-xs mt-0.5">{p.website}</p>}
          </div>
          <div className="text-right">
            <p className={`text-3xl font-black ${tm.color}`}>{p.priority_score}</p>
            <p className="text-xs text-slate-500">score</p>
          </div>
        </div>

        {/* Priority bar */}
        <PriorityBar score={p.priority_score} tier={p.tier} />

        {/* Signal grid */}
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">ICP Fit</p>
            <p className="text-indigo-400 font-bold">{Math.round(p.icp_fit * 100)}%</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">Urgence</p>
            <UrgencyPill label={p.urgency_label as UrgencyLabel} />
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">PageSpeed</p>
            <p className={`font-bold ${p.pagespeed_score < 30 ? "text-red-400" : p.pagespeed_score < 50 ? "text-orange-400" : p.pagespeed_score < 70 ? "text-amber-400" : "text-emerald-400"}`}>
              {p.pagespeed_score}/100
            </p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">Temps chargement</p>
            <p className={`font-bold ${p.load_time_ms > 5000 ? "text-red-400" : p.load_time_ms > 3000 ? "text-amber-400" : "text-emerald-400"}`}>
              {(p.load_time_ms / 1000).toFixed(1)}s
            </p>
          </div>
        </div>

        {/* Revenue impact */}
        {p.estimated_revenue_impact_eur > 0 && (
          <div className="bg-emerald-950/40 border border-emerald-900/50 rounded-lg p-3 flex items-center gap-3">
            <div>
              <p className="text-xs text-emerald-400 font-semibold">Impact revenu estimé</p>
              <p className="text-white font-bold text-lg">
                {p.estimated_revenue_impact_eur.toLocaleString("fr-FR")} €/an
              </p>
            </div>
          </div>
        )}

        {/* Enrichment notes */}
        {p.enrichment_notes.length > 0 && (
          <div className="bg-indigo-950/40 border border-indigo-900/50 rounded-lg p-3">
            <p className="text-xs text-indigo-400 font-semibold mb-2">Notes d'enrichissement</p>
            <ul className="space-y-1">
              {p.enrichment_notes.map((note, i) => (
                <li key={i} className="text-slate-300 text-sm flex items-start gap-2">
                  <span className="text-indigo-500 mt-0.5">·</span>
                  {note}
                </li>
              ))}
            </ul>
          </div>
        )}

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

export default function EnricherPage() {
  const [prospects, setProspects] = useState<EnrichedProspect[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<EnrichedProspect | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/enricher")
      .then((r) => r.json())
      .then((d) => {
        setProspects(d.prospects ?? []);
        setSummary(d.summary ?? null);
      })
      .finally(() => setLoading(false));
  }, []);

  const filtered = filter === "all" ? prospects : prospects.filter((p) => p.tier === filter);

  const urgencyOrder = ["critique", "mauvais", "moyen", "acceptable", "bon"];

  return (
    <div className="p-6 space-y-6 text-slate-100">
      <div>
        <h1 className="text-2xl font-bold text-white">Enrichissement Prospects</h1>
        <p className="text-slate-400 text-sm mt-1">
          Score priorité 0–100 : ICP Fit (55%) + Urgence PageSpeed (45%) · Tier A ≥ 70 · Tier B ≥ 45
        </p>
      </div>

      {/* KPI strip */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <KpiCard label="Total" value={summary.total} />
          <KpiCard label="Tier A" value={summary.tier_A} sub="Priorité max" accent="text-emerald-400" />
          <KpiCard label="Tier B" value={summary.tier_B} sub="Normal" accent="text-blue-400" />
          <KpiCard label="Tier C" value={summary.tier_C} sub="Faible" accent="text-slate-400" />
          <KpiCard label="Score moy." value={summary.avg_priority} sub="/ 100" accent="text-indigo-400" />
          <KpiCard
            label="Impact CA"
            value={`${(summary.total_revenue_impact_eur / 1000).toFixed(0)}k€`}
            sub="estimé / an"
            accent="text-emerald-400"
          />
        </div>
      )}

      {/* Urgency distribution */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">
            Répartition par urgence PageSpeed
          </h3>
          <div className="flex flex-wrap gap-3">
            {urgencyOrder.map((label) => {
              const count = summary.urgency_distribution[label] ?? 0;
              if (count === 0) return null;
              const m = URGENCY_META[label as UrgencyLabel] ?? { color: "text-slate-400", dot: "bg-slate-500" };
              return (
                <div key={label} className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 flex items-center gap-3">
                  <span className={`w-2.5 h-2.5 rounded-full ${m.dot}`} />
                  <div>
                    <p className={`text-sm font-semibold capitalize ${m.color}`}>{label}</p>
                    <p className="text-slate-500 text-xs">{count} prospect{count > 1 ? "s" : ""}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Filter tabs */}
      <div className="flex gap-2 flex-wrap">
        {[
          { key: "all", label: "Tous" },
          { key: "A", label: "Tier A" },
          { key: "B", label: "Tier B" },
          { key: "C", label: "Tier C" },
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setFilter(tab.key)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors border ${
              filter === tab.key
                ? "bg-indigo-600 border-indigo-500 text-white"
                : "bg-slate-800 border-slate-700 text-slate-400 hover:text-white"
            }`}
          >
            {tab.label}
            {tab.key !== "all" && summary && (
              <span className="ml-1.5 opacity-70">
                {summary[`tier_${tab.key}` as keyof Summary] as number}
              </span>
            )}
            {tab.key === "all" && summary && (
              <span className="ml-1.5 opacity-70">{summary.total}</span>
            )}
          </button>
        ))}
      </div>

      {/* Table */}
      {loading ? (
        <div className="text-slate-500 text-center py-16">Chargement…</div>
      ) : (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-800">
                <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider">Tier</th>
                <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider">Entreprise</th>
                <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider hidden md:table-cell">Secteur</th>
                <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider">Priorité</th>
                <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider hidden lg:table-cell">Urgence</th>
                <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider hidden lg:table-cell">ICP Fit</th>
                <th className="text-right py-3 px-4 text-xs text-slate-500 uppercase tracking-wider hidden xl:table-cell">Impact CA</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((p) => (
                <tr
                  key={p.company_id}
                  onClick={() => setSelected(p)}
                  className="border-b border-slate-800/50 hover:bg-slate-800/40 cursor-pointer transition-colors"
                >
                  <td className="py-3 px-4">
                    <TierBadge tier={p.tier} />
                  </td>
                  <td className="py-3 px-4">
                    <p className="text-white font-semibold text-sm">{p.name}</p>
                    <p className="text-slate-500 text-xs">{p.company_size} · {p.contact_email}</p>
                  </td>
                  <td className="py-3 px-4 hidden md:table-cell">
                    <span className="text-slate-400 text-sm capitalize">{p.sector}</span>
                  </td>
                  <td className="py-3 px-4 w-40">
                    <PriorityBar score={p.priority_score} tier={p.tier} />
                  </td>
                  <td className="py-3 px-4 hidden lg:table-cell">
                    <UrgencyPill label={p.urgency_label as UrgencyLabel} />
                  </td>
                  <td className="py-3 px-4 hidden lg:table-cell">
                    <span className="text-indigo-400 text-sm font-mono">{Math.round(p.icp_fit * 100)}%</span>
                  </td>
                  <td className="py-3 px-4 hidden xl:table-cell text-right">
                    {p.estimated_revenue_impact_eur > 0 ? (
                      <span className="text-emerald-400 text-sm font-mono">
                        {p.estimated_revenue_impact_eur.toLocaleString("fr-FR")} €
                      </span>
                    ) : (
                      <span className="text-slate-600 text-sm">—</span>
                    )}
                  </td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={7} className="text-center text-slate-500 py-10">
                    Aucun prospect dans ce tier.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Sector breakdown */}
      {summary && Object.keys(summary.sector_breakdown).length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">
            Par secteur
          </h3>
          <div className="flex flex-wrap gap-3">
            {Object.entries(summary.sector_breakdown)
              .sort((a, b) => b[1].avg_priority - a[1].avg_priority)
              .map(([sector, data]) => (
                <div key={sector} className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-3">
                  <p className="text-white font-medium text-sm capitalize">{sector}</p>
                  <p className="text-slate-400 text-xs">
                    {data.count} prospect{data.count > 1 ? "s" : ""} · moy. {data.avg_priority}
                  </p>
                </div>
              ))}
          </div>
        </div>
      )}

      {selected && <DetailModal prospect={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
