"use client";

import { useEffect, useState, useCallback } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface Deal {
  deal_id: string;
  deal_name: string;
  rep_id: string;
  committee_coverage: string;
  committee_risk: string;
  deal_complexity: string;
  committee_action: string;
  role_coverage_score: number;
  engagement_breadth_score: number;
  blocker_management_score: number;
  late_stage_alignment_score: number;
  committee_composite: number;
  coverage_ratio: number;
  missing_role_count: number;
  is_well_covered: boolean;
  needs_expansion: boolean;
  region: string;
}

interface Summary {
  total: number;
  coverage_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  complexity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_committee_composite: number;
  avg_coverage_ratio: number;
  well_covered_count: number;
  expansion_needed_count: number;
  avg_role_coverage_score: number;
  avg_engagement_breadth_score: number;
  avg_blocker_management_score: number;
  avg_late_stage_alignment_score: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const COV_COLOR: Record<string, string> = {
  full_coverage:    "text-emerald-400",
  partial:          "text-sky-400",
  thin:             "text-amber-400",
  single_threaded:  "text-rose-400",
};
const COV_BG: Record<string, string> = {
  full_coverage:    "bg-emerald-500/20 border-emerald-500/40",
  partial:          "bg-sky-500/20 border-sky-500/40",
  thin:             "bg-amber-500/20 border-amber-500/40",
  single_threaded:  "bg-rose-500/20 border-rose-500/40",
};
const RISK_COLOR: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-amber-400",
  high:     "text-orange-400",
  critical: "text-rose-400",
};
const COV_ICON: Record<string, string> = {
  full_coverage:   "🗺️",
  partial:         "🧩",
  thin:            "🔍",
  single_threaded: "⚠️",
};

function CommitteeRing({ score, color }: { score: number; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  return (
    <svg width={88} height={88} viewBox="0 0 88 88">
      <circle cx={44} cy={44} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle
        cx={44} cy={44} r={r} fill="none"
        stroke={color} strokeWidth={8}
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 44 44)"
      />
      <text x={44} y={49} textAnchor="middle" fill="white" fontSize={14} fontWeight="bold">
        {Math.round(score)}
      </text>
    </svg>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs text-slate-400 mb-1">
        <span>{label}</span><span>{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}

function CoverageDistBar({ counts }: { counts: Record<string, number> }) {
  const order = ["full_coverage", "partial", "thin", "single_threaded"];
  const colors = ["bg-emerald-500", "bg-sky-500", "bg-amber-500", "bg-rose-500"];
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex gap-1 h-3 rounded-full overflow-hidden">
      {order.map((k, i) => (
        <div
          key={k}
          className={colors[i]}
          style={{ width: `${((counts[k] || 0) / total) * 100}%` }}
          title={`${k}: ${counts[k] || 0}`}
        />
      ))}
    </div>
  );
}

// ── DealModal ────────────────────────────────────────────────────────────────
function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const [tab, setTab] = useState<"signals" | "scores" | "actions">("signals");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    deal.committee_composite >= 70 ? "#10b981"
    : deal.committee_composite >= 50 ? "#38bdf8"
    : deal.committee_composite >= 30 ? "#f59e0b"
    : "#f43f5e";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* header */}
        <div className="flex items-center gap-4 p-5 border-b border-slate-800">
          <CommitteeRing score={deal.committee_composite} color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">{deal.deal_name}</h2>
            <p className="text-slate-400 text-sm">{deal.rep_id} · {deal.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${COV_BG[deal.committee_coverage]}`}>
                {COV_ICON[deal.committee_coverage]} {deal.committee_coverage.replace(/_/g, " ")}
              </span>
              <span className={`text-xs font-semibold ${RISK_COLOR[deal.committee_risk]}`}>
                {deal.committee_risk.toUpperCase()} RISK
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["signals", "scores", "actions"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "signals" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Coverage Ratio",  (deal.coverage_ratio * 100).toFixed(0) + "%"],
                  ["Missing Roles",   deal.missing_role_count],
                  ["Well Covered",    deal.is_well_covered ? "✅ Yes" : "❌ No"],
                  ["Needs Expansion", deal.needs_expansion ? "⚠️ Yes" : "✅ No"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Deal Complexity</div>
                <div className="text-white font-semibold capitalize">{deal.deal_complexity}</div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Role Coverage"        value={deal.role_coverage_score}        color="bg-indigo-500" />
              <ScoreBar label="Engagement Breadth"   value={deal.engagement_breadth_score}   color="bg-violet-500" />
              <ScoreBar label="Blocker Management"   value={deal.blocker_management_score}   color="bg-sky-500" />
              <ScoreBar label="Late-Stage Alignment" value={deal.late_stage_alignment_score} color="bg-emerald-500" />
            </div>
          )}

          {tab === "actions" && (
            <div className="space-y-3">
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-xl p-4">
                <div className="text-xs text-indigo-400 uppercase tracking-wide mb-1">Recommended Action</div>
                <div className="text-white font-bold text-lg capitalize">
                  {deal.committee_action.replace(/_/g, " ")}
                </div>
              </div>
              {deal.missing_role_count >= 2 && (
                <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 text-sm text-rose-300">
                  ⚠️ {deal.missing_role_count} key roles unidentified — expand stakeholder mapping
                </div>
              )}
              {deal.committee_coverage === "single_threaded" && (
                <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-3 text-sm text-amber-300">
                  🧵 Single-threaded deal — request champion introductions immediately
                </div>
              )}
              {deal.is_well_covered && (
                <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-3 text-sm text-emerald-300">
                  🗺️ Full committee coverage — maintain momentum and protect relationships
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── DealCard ─────────────────────────────────────────────────────────────────
function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  const ringColor =
    deal.committee_composite >= 70 ? "#10b981"
    : deal.committee_composite >= 50 ? "#38bdf8"
    : deal.committee_composite >= 30 ? "#f59e0b"
    : "#f43f5e";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-indigo-500/50 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <CommitteeRing score={deal.committee_composite} color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">{deal.deal_name}</div>
          <div className="text-slate-400 text-xs">{deal.rep_id} · {deal.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${COV_BG[deal.committee_coverage]}`}>
              {COV_ICON[deal.committee_coverage]} {deal.committee_coverage.replace(/_/g, " ")}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          <div className={`text-sm font-bold ${RISK_COLOR[deal.committee_risk]}`}>
            {(deal.coverage_ratio * 100).toFixed(0)}%
          </div>
          <div className="text-xs text-slate-500">covered</div>
          {deal.needs_expansion && (
            <div className="text-xs text-amber-400 mt-1">🧩 expand</div>
          )}
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        Missing: {deal.missing_role_count} role{deal.missing_role_count !== 1 ? "s" : ""} · {deal.deal_complexity}
      </div>
    </div>
  );
}

// ── page ─────────────────────────────────────────────────────────────────────
export default function BuyingCommitteeMapperPage() {
  const [deals, setDeals]       = useState<Deal[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [selected, setSelected] = useState<Deal | null>(null);
  const [filterCoverage, setFilterCoverage] = useState("all");
  const [filterRisk,     setFilterRisk]     = useState("all");
  const [filterRegion,   setFilterRegion]   = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams();
    if (filterCoverage !== "all") params.set("coverage", filterCoverage);
    if (filterRisk     !== "all") params.set("risk",     filterRisk);
    if (filterRegion   !== "all") params.set("region",   filterRegion);
    const res = await fetch(`/api/buying-committee-mapper?${params}`);
    const data = await res.json();
    setDeals(data.deals);
    setSummary(data.summary);
    setLoading(false);
  }, [filterCoverage, filterRisk, filterRegion]);

  useEffect(() => { load(); }, [load]);

  const singleThreaded = deals.filter((d) => d.committee_coverage === "single_threaded");

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Buying Committee Mapper</h1>
          <p className="text-slate-400 text-sm mt-1">
            Maps stakeholder coverage across economic buyer, champion, evaluator, and end-user roles
          </p>
        </div>

        {/* single-threaded alert */}
        {singleThreaded.length > 0 && (
          <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-4 flex items-center gap-3">
            <span className="text-2xl">🧵</span>
            <div>
              <div className="text-rose-300 font-semibold">
                {singleThreaded.length} single-threaded deal{singleThreaded.length > 1 ? "s" : ""} — critical risk
              </div>
              <div className="text-rose-400/70 text-xs mt-0.5">
                {singleThreaded.map((d) => d.deal_name).join(" · ")}
              </div>
            </div>
          </div>
        )}

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Total Deals",     value: summary.total },
              { label: "Well Covered",    value: summary.well_covered_count,    color: "text-emerald-400" },
              { label: "Need Expansion",  value: summary.expansion_needed_count, color: "text-amber-400" },
              { label: "Avg Composite",   value: summary.avg_committee_composite.toFixed(1), color: "text-indigo-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* coverage dist bar */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-400 mb-2">Coverage Distribution</div>
            <CoverageDistBar counts={summary.coverage_counts} />
            <div className="flex gap-4 mt-2 text-xs text-slate-500">
              {["full_coverage","partial","thin","single_threaded"].map((k) => (
                <span key={k} className={COV_COLOR[k]}>{k.replace(/_/g," ")}: {summary.coverage_counts[k] || 0}</span>
              ))}
            </div>
          </div>
        )}

        {/* filters */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "All Coverage",    val: "all" },
            { label: "🗺️ Full",          val: "full_coverage" },
            { label: "🧩 Partial",       val: "partial" },
            { label: "🔍 Thin",          val: "thin" },
            { label: "⚠️ Single Thread", val: "single_threaded" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterCoverage(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterCoverage === val
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {label}
            </button>
          ))}
          <select
            value={filterRegion}
            onChange={(e) => setFilterRegion(e.target.value)}
            className="px-3 py-1.5 rounded-lg text-xs bg-slate-800 text-slate-300 border border-slate-700"
          >
            <option value="all">All Regions</option>
            {["NAMER","EMEA","APAC","LATAM"].map((r) => (
              <option key={r} value={r}>{r}</option>
            ))}
          </select>
        </div>

        {/* deals grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Loading committee data…</div>
        ) : deals.length === 0 ? (
          <div className="text-slate-500 text-center py-16">No deals match your filters.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {deals.map((d) => (
              <DealCard key={d.deal_id} deal={d} onClick={() => setSelected(d)} />
            ))}
          </div>
        )}

        {/* avg score bars */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Average Score Breakdown</div>
            <div className="space-y-3">
              <ScoreBar label="Role Coverage"        value={summary.avg_role_coverage_score}        color="bg-indigo-500" />
              <ScoreBar label="Engagement Breadth"   value={summary.avg_engagement_breadth_score}   color="bg-violet-500" />
              <ScoreBar label="Blocker Management"   value={summary.avg_blocker_management_score}   color="bg-sky-500" />
              <ScoreBar label="Late-Stage Alignment" value={summary.avg_late_stage_alignment_score} color="bg-emerald-500" />
            </div>
          </div>
        )}
      </div>

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
