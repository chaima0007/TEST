"use client";

import { useEffect, useState } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────

type Grade = "S" | "A" | "B" | "C" | "D";

interface FeatureContributions {
  pagespeed: number;
  load_time: number;
  icp_fit: number;
  sector: number;
  company_size: number;
  engagement: number;
}

interface ScoredLead {
  company_id: string;
  company_name: string;
  sector: string;
  city: string;
  pagespeed_score: number;
  load_time_ms: number;
  icp_fit: number;
  company_size: string;
  open_rate: number;
  reply_signal: number;
  action_score: number;
  grade: Grade;
  feature_contributions: FeatureContributions;
  recommended_action: string;
}

interface Summary {
  total: number;
  grade_S: number;
  grade_A: number;
  grade_B: number;
  grade_C: number;
  grade_D: number;
  avg_score: number;
  sector_breakdown: Record<string, { count: number; avg_score: number }>;
  weights: Record<string, number>;
}

// ─── Constants ────────────────────────────────────────────────────────────────

const GRADE_META: Record<Grade, { label: string; color: string; bg: string; border: string; desc: string }> = {
  S: { label: "Grade S", color: "text-yellow-300", bg: "bg-yellow-900/30", border: "border-yellow-600", desc: "Appel immédiat" },
  A: { label: "Grade A", color: "text-emerald-400", bg: "bg-emerald-900/30", border: "border-emerald-700", desc: "Email Tier A" },
  B: { label: "Grade B", color: "text-blue-400", bg: "bg-blue-900/30", border: "border-blue-700", desc: "Email masse" },
  C: { label: "Grade C", color: "text-amber-400", bg: "bg-amber-900/30", border: "border-amber-700", desc: "Nurturing" },
  D: { label: "Grade D", color: "text-slate-400", bg: "bg-slate-800", border: "border-slate-700", desc: "Exclure" },
};

const FEATURE_META: { key: keyof FeatureContributions; label: string; max: number; color: string }[] = [
  { key: "pagespeed",    label: "PageSpeed (inv.)", max: 0.30, color: "bg-red-500" },
  { key: "load_time",   label: "Temps chargement", max: 0.15, color: "bg-orange-500" },
  { key: "icp_fit",     label: "ICP Fit",           max: 0.25, color: "bg-indigo-500" },
  { key: "sector",      label: "Demande secteur",   max: 0.15, color: "bg-cyan-500" },
  { key: "company_size",label: "Taille entreprise", max: 0.10, color: "bg-purple-500" },
  { key: "engagement",  label: "Engagement email",  max: 0.05, color: "bg-emerald-500" },
];

const FILTER_TABS = [
  { key: "all", label: "Tous" },
  { key: "S",   label: "Grade S" },
  { key: "A",   label: "Grade A" },
  { key: "B",   label: "Grade B" },
  { key: "C",   label: "Grade C" },
  { key: "D",   label: "Grade D" },
];

// ─── Sub-components ───────────────────────────────────────────────────────────

function GradeBadge({ grade }: { grade: Grade }) {
  const m = GRADE_META[grade];
  return (
    <span className={`inline-flex items-center justify-center w-8 h-8 rounded-lg text-sm font-black border ${m.bg} ${m.color} ${m.border}`}>
      {grade}
    </span>
  );
}

function ScoreBar({ score, grade }: { score: number; grade: Grade }) {
  const m = GRADE_META[grade];
  const barColor = grade === "S" ? "bg-yellow-400" : grade === "A" ? "bg-emerald-500" :
    grade === "B" ? "bg-blue-500" : grade === "C" ? "bg-amber-500" : "bg-slate-600";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-2 rounded-full transition-all ${barColor}`} style={{ width: `${score}%` }} />
      </div>
      <span className={`text-xs font-bold tabular-nums w-10 text-right ${m.color}`}>{score}</span>
    </div>
  );
}

function FeatureBar({ value, max, color, label }: { value: number; max: number; color: string; label: string }) {
  const pct = Math.min(100, Math.round((value / max) * 100));
  return (
    <div className="flex items-center gap-2 text-xs">
      <span className="text-slate-500 w-32 flex-shrink-0 truncate">{label}</span>
      <div className="flex-1 bg-slate-800 rounded-full h-1.5 overflow-hidden">
        <div className={`h-1.5 rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-slate-400 tabular-nums w-12 text-right">
        {(value * 100).toFixed(1)}%
      </span>
    </div>
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

function DetailModal({ lead, onClose }: { lead: ScoredLead; onClose: () => void }) {
  useEffect(() => {
    const h = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const m = GRADE_META[lead.grade];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <div
        className={`bg-slate-900 border-2 ${m.border} rounded-2xl shadow-2xl w-full max-w-lg mx-4 p-6 space-y-5`}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start gap-4">
          <GradeBadge grade={lead.grade} />
          <div className="flex-1">
            <h2 className="text-white font-bold text-lg">{lead.company_name}</h2>
            <p className="text-slate-400 text-sm">{lead.sector} · {lead.city} · {lead.company_size}</p>
            <p className={`text-xs mt-1 font-medium ${m.color}`}>{m.desc}</p>
          </div>
          <div className="text-right">
            <p className={`text-3xl font-black ${m.color}`}>{lead.action_score}</p>
            <p className="text-xs text-slate-500">/100</p>
          </div>
        </div>

        {/* Score bar */}
        <ScoreBar score={lead.action_score} grade={lead.grade} />

        {/* Technical signals */}
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">PageSpeed</p>
            <p className={`font-bold text-base ${lead.pagespeed_score < 40 ? "text-red-400" : lead.pagespeed_score < 60 ? "text-amber-400" : "text-emerald-400"}`}>
              {lead.pagespeed_score}/100
            </p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">Temps chargement</p>
            <p className={`font-bold text-base ${lead.load_time_ms > 5000 ? "text-red-400" : lead.load_time_ms > 3000 ? "text-amber-400" : "text-emerald-400"}`}>
              {(lead.load_time_ms / 1000).toFixed(1)}s
            </p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">ICP Fit</p>
            <p className="text-indigo-400 font-bold text-base">{Math.round(lead.icp_fit * 100)}%</p>
          </div>
          <div className="bg-slate-800/60 rounded-lg p-3">
            <p className="text-slate-500 text-xs mb-1">Engagement</p>
            <p className="text-emerald-400 font-bold text-base">
              {lead.reply_signal > 0 ? "Répondu" : lead.open_rate > 0 ? `Ouvert ${Math.round(lead.open_rate * 100)}%` : "Aucun"}
            </p>
          </div>
        </div>

        {/* Feature contributions */}
        <div className="bg-slate-800 rounded-xl p-4">
          <p className="text-xs text-slate-500 mb-3 uppercase tracking-wider font-semibold">
            Contributions par feature
          </p>
          <div className="space-y-2.5">
            {FEATURE_META.map((f) => (
              <FeatureBar
                key={f.key}
                value={lead.feature_contributions[f.key]}
                max={f.max}
                color={f.color}
                label={f.label}
              />
            ))}
          </div>
        </div>

        {/* Recommended action */}
        <div className="bg-indigo-950/40 border border-indigo-900/50 rounded-lg p-3">
          <p className="text-xs text-indigo-400 font-semibold mb-1">Action recommandée</p>
          <p className="text-slate-300 text-sm">{lead.recommended_action}</p>
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

export default function LeadsPage() {
  const [leads, setLeads] = useState<ScoredLead[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState<ScoredLead | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/leads")
      .then((r) => r.json())
      .then((d) => {
        setLeads(d.leads ?? []);
        setSummary(d.summary ?? null);
      })
      .finally(() => setLoading(false));
  }, []);

  const filtered = filter === "all" ? leads : leads.filter((l) => l.grade === filter);

  return (
    <div className="p-6 space-y-6 text-slate-100">
      <div>
        <h1 className="text-2xl font-bold text-white">Scoring Leads</h1>
        <p className="text-slate-400 text-sm mt-1">
          Score 0–100 pondéré : PageSpeed (30%) + Chargement (15%) + ICP Fit (25%) + Secteur (15%) + Taille (10%) + Engagement (5%)
        </p>
      </div>

      {/* KPI strip */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-3">
          <KpiCard label="Total" value={summary.total} />
          <KpiCard label="Grade S" value={summary.grade_S} sub="Appel immédiat" accent="text-yellow-300" />
          <KpiCard label="Grade A" value={summary.grade_A} sub="Email Tier A" accent="text-emerald-400" />
          <KpiCard label="Grade B" value={summary.grade_B} sub="Email masse" accent="text-blue-400" />
          <KpiCard label="Grade C" value={summary.grade_C} sub="Nurturing" accent="text-amber-400" />
          <KpiCard label="Grade D" value={summary.grade_D} sub="À exclure" accent="text-slate-400" />
          <KpiCard label="Score moy." value={summary.avg_score} sub="/ 100" accent="text-indigo-400" />
        </div>
      )}

      {/* Feature weight legend */}
      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4">
            Poids des features
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {FEATURE_META.map((f) => {
              const pct = Math.round(f.max * 100);
              return (
                <div key={f.key} className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full flex-shrink-0 ${f.color}`} />
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-slate-300 truncate">{f.label}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div className={`h-1.5 rounded-full ${f.color}`} style={{ width: `${pct / 0.30}%` }} />
                      </div>
                      <span className="text-xs text-slate-500 tabular-nums w-8">{pct}%</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Filter tabs */}
      <div className="flex gap-2 flex-wrap">
        {FILTER_TABS.map((tab) => (
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
                {summary[`grade_${tab.key}` as keyof Summary] as number}
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
                <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider font-medium">Grade</th>
                <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider font-medium">Entreprise</th>
                <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider font-medium hidden md:table-cell">Secteur</th>
                <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider font-medium">Score</th>
                <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider font-medium hidden lg:table-cell">PageSpeed</th>
                <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider font-medium hidden lg:table-cell">ICP Fit</th>
                <th className="text-left py-3 px-4 text-xs text-slate-500 uppercase tracking-wider font-medium hidden xl:table-cell">Action recommandée</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((lead) => {
                const m = GRADE_META[lead.grade];
                return (
                  <tr
                    key={lead.company_id}
                    onClick={() => setSelected(lead)}
                    className="border-b border-slate-800/50 hover:bg-slate-800/40 cursor-pointer transition-colors"
                  >
                    <td className="py-3 px-4">
                      <GradeBadge grade={lead.grade} />
                    </td>
                    <td className="py-3 px-4">
                      <p className="text-white font-semibold text-sm">{lead.company_name}</p>
                      <p className="text-slate-500 text-xs">{lead.city} · {lead.company_size}</p>
                    </td>
                    <td className="py-3 px-4 hidden md:table-cell">
                      <span className="text-slate-400 text-sm capitalize">{lead.sector}</span>
                    </td>
                    <td className="py-3 px-4 w-40">
                      <ScoreBar score={lead.action_score} grade={lead.grade} />
                    </td>
                    <td className="py-3 px-4 hidden lg:table-cell">
                      <span className={`text-sm font-mono ${lead.pagespeed_score < 40 ? "text-red-400" : lead.pagespeed_score < 60 ? "text-amber-400" : "text-emerald-400"}`}>
                        {lead.pagespeed_score}/100
                      </span>
                    </td>
                    <td className="py-3 px-4 hidden lg:table-cell">
                      <span className="text-sm text-indigo-400 font-mono">{Math.round(lead.icp_fit * 100)}%</span>
                    </td>
                    <td className="py-3 px-4 hidden xl:table-cell">
                      <p className="text-slate-400 text-xs truncate max-w-xs">{lead.recommended_action}</p>
                    </td>
                  </tr>
                );
              })}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={7} className="text-center text-slate-500 py-10">
                    Aucun lead dans ce grade.
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
              .sort((a, b) => b[1].avg_score - a[1].avg_score)
              .map(([sector, data]) => (
                <div key={sector} className="bg-slate-800 border border-slate-700 rounded-lg px-4 py-3">
                  <p className="text-white font-medium text-sm capitalize">{sector}</p>
                  <p className="text-slate-400 text-xs">
                    {data.count} lead{data.count > 1 ? "s" : ""} · moy. {data.avg_score}
                  </p>
                </div>
              ))}
          </div>
        </div>
      )}

      {selected && <DetailModal lead={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
