"use client";

import { useEffect, useState, useCallback } from "react";

/* ── types ──────────────────────────────────────────────────────────────── */
interface Rep {
  rep_id: string;
  region: string;
  engagement_risk: string;
  engagement_pattern: string;
  engagement_severity: string;
  recommended_action: string;
  velocity_score: number;
  breadth_score: number;
  responsiveness_score: number;
  momentum_score: number;
  engagement_composite: number;
  has_engagement_gap: boolean;
  requires_engagement_coaching: boolean;
  estimated_pipeline_at_risk_usd: number;
  engagement_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_engagement_composite: number;
  engagement_gap_count: number;
  coaching_count: number;
  avg_velocity_score: number;
  avg_breadth_score: number;
  avg_responsiveness_score: number;
  avg_momentum_score: number;
  total_estimated_pipeline_at_risk_usd: number;
}

/* ── helpers ─────────────────────────────────────────────────────────────── */
const fmtUSD = (v: number) =>
  v >= 1_000_000
    ? `$${(v / 1_000_000).toFixed(1)}M`
    : v >= 1_000
    ? `$${(v / 1_000).toFixed(0)}K`
    : `$${v.toFixed(0)}`;

const riskColor: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-sky-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};

const riskBorder: Record<string, string> = {
  low:      "border-emerald-500/40",
  moderate: "border-sky-500/40",
  high:     "border-orange-500/40",
  critical: "border-red-500/40",
};

const severityBadge: Record<string, string> = {
  accelerating: "bg-emerald-900/50 text-emerald-300",
  engaged:      "bg-sky-900/50 text-sky-300",
  slowing:      "bg-orange-900/50 text-orange-300",
  stalled:      "bg-red-900/50 text-red-300",
};

const patternLabel: Record<string, string> = {
  none:                      "None",
  buyer_ghosting_cycle:      "Ghosting Cycle",
  single_contact_dependency: "Single Contact",
  response_lag_accumulation: "Response Lag",
  momentum_reversal:         "Momentum Reversal",
  executive_access_deficit:  "Exec Access Deficit",
};

const patternColor: Record<string, string> = {
  none:                      "bg-slate-700 text-slate-300",
  buyer_ghosting_cycle:      "bg-red-900/60 text-red-300",
  single_contact_dependency: "bg-orange-900/60 text-orange-300",
  response_lag_accumulation: "bg-amber-900/60 text-amber-300",
  momentum_reversal:         "bg-purple-900/60 text-purple-300",
  executive_access_deficit:  "bg-rose-900/60 text-rose-300",
};

/* ── Gauge ───────────────────────────────────────────────────────────────── */
function Gauge({ label, value, color }: { label: string; value: number; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const dash = (value / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="96" height="96" viewBox="0 0 96 96">
        <circle cx="48" cy="48" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle
          cx="48" cy="48" r={r} fill="none"
          stroke={color} strokeWidth="8"
          strokeDasharray={`${dash} ${circ}`}
          strokeLinecap="round"
          transform="rotate(-90 48 48)"
          style={{ transition: "stroke-dasharray 0.6s ease" }}
        />
        <text x="48" y="53" textAnchor="middle" fontSize="15" fontWeight="700" fill="white">
          {value.toFixed(0)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center leading-tight">{label}</span>
    </div>
  );
}

/* ── DistBar ─────────────────────────────────────────────────────────────── */
function DistBar({
  title, counts, colors, total,
}: {
  title: string;
  counts: Record<string, number>;
  colors: Record<string, string>;
  total: number;
}) {
  return (
    <div className="space-y-1">
      <p className="text-xs text-slate-400 font-medium">{title}</p>
      {Object.entries(counts).map(([k, v]) => (
        <div key={k} className="flex items-center gap-2">
          <span className="text-xs text-slate-400 w-32 truncate capitalize">{k.replace(/_/g, " ")}</span>
          <div className="flex-1 bg-slate-800 rounded-full h-2">
            <div
              className="h-2 rounded-full transition-all duration-500"
              style={{ width: `${total ? (v / total) * 100 : 0}%`, background: colors[k] || "#64748b" }}
            />
          </div>
          <span className="text-xs text-slate-300 w-4 text-right">{v}</span>
        </div>
      ))}
    </div>
  );
}

/* ── DetailModal ─────────────────────────────────────────────────────────── */
function DetailModal({ rep, onClose }: { rep: Rep; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");

  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", fn);
    return () => window.removeEventListener("keydown", fn);
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl mx-4 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div>
            <p className="font-bold text-white">{rep.rep_id}</p>
            <p className="text-xs text-slate-400">{rep.region}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex border-b border-slate-800">
          {(["scores", "signal", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2 text-xs font-medium capitalize transition-colors ${
                tab === t ? "text-sky-400 border-b-2 border-sky-400" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5">
          {tab === "scores" && (
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-slate-800/60 rounded-xl p-3">
                <p className="text-xs text-slate-400">Velocity Score</p>
                <p className="text-2xl font-bold text-sky-400">{rep.velocity_score.toFixed(1)}</p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-3">
                <p className="text-xs text-slate-400">Breadth Score</p>
                <p className="text-2xl font-bold text-blue-400">{rep.breadth_score.toFixed(1)}</p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-3">
                <p className="text-xs text-slate-400">Responsiveness Score</p>
                <p className="text-2xl font-bold text-indigo-400">{rep.responsiveness_score.toFixed(1)}</p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-3">
                <p className="text-xs text-slate-400">Momentum Score</p>
                <p className="text-2xl font-bold text-violet-400">{rep.momentum_score.toFixed(1)}</p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-3 col-span-2">
                <p className="text-xs text-slate-400">Engagement Composite</p>
                <p className="text-3xl font-bold text-white">{rep.engagement_composite.toFixed(1)}</p>
              </div>
            </div>
          )}
          {tab === "signal" && (
            <div className="space-y-3">
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">Engagement Signal</p>
                <p className="text-sm text-slate-200 leading-relaxed">{rep.engagement_signal}</p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">Pipeline at Risk</p>
                <p className="text-2xl font-bold text-red-400">{fmtUSD(rep.estimated_pipeline_at_risk_usd)}</p>
              </div>
              <div className="flex gap-2">
                {rep.has_engagement_gap && (
                  <span className="px-2 py-1 rounded-lg text-xs bg-red-900/50 text-red-300">🔗 ENGAGEMENT GAP</span>
                )}
                {rep.requires_engagement_coaching && (
                  <span className="px-2 py-1 rounded-lg text-xs bg-sky-900/50 text-sky-300">🔗 COACH</span>
                )}
              </div>
            </div>
          )}
          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">Recommended Action</p>
                <p className="text-sm font-semibold text-sky-300 capitalize">
                  {rep.recommended_action.replace(/_/g, " ")}
                </p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">Pattern</p>
                <p className="text-sm font-semibold text-white">{patternLabel[rep.engagement_pattern] ?? rep.engagement_pattern}</p>
              </div>
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-400 mb-1">Severity</p>
                <span className={`px-2 py-1 rounded-lg text-xs font-medium ${severityBadge[rep.engagement_severity] ?? "bg-slate-700 text-slate-300"}`}>
                  {rep.engagement_severity}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

/* ── Main page ───────────────────────────────────────────────────────────── */
export default function SalesBuyerEngagementVelocityPage() {
  const [data, setData]           = useState<{ reps: Rep[]; summary: Summary } | null>(null);
  const [loading, setLoading]     = useState(true);
  const [riskFilter, setRiskFilter]       = useState("all");
  const [patternFilter, setPatternFilter] = useState("all");
  const [selected, setSelected]   = useState<Rep | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (riskFilter    !== "all") params.set("risk",    riskFilter);
      if (patternFilter !== "all") params.set("pattern", patternFilter);
      const res  = await fetch(`/api/sales-buyer-engagement-velocity-intelligence-engine?${params}`);
      const json = await res.json();
      setData(json);
    } finally {
      setLoading(false);
    }
  }, [riskFilter, patternFilter]);

  useEffect(() => { load(); }, [load]);

  const s = data?.summary;

  const distributions = [
    {
      title: "Risk Distribution",
      counts: s?.risk_counts ?? {},
      colors: { low: "#34d399", moderate: "#38bdf8", high: "#f97316", critical: "#f87171" },
    },
    {
      title: "Pattern Distribution",
      counts: s?.pattern_counts ?? {},
      colors: {
        none:                      "#475569",
        buyer_ghosting_cycle:      "#ef4444",
        single_contact_dependency: "#f97316",
        response_lag_accumulation: "#fbbf24",
        momentum_reversal:         "#a78bfa",
        executive_access_deficit:  "#f43f5e",
      },
    },
    {
      title: "Severity Distribution",
      counts: s?.severity_counts ?? {},
      colors: { accelerating: "#34d399", engaged: "#38bdf8", slowing: "#f97316", stalled: "#f87171" },
    },
    {
      title: "Action Distribution",
      counts: s?.action_counts ?? {},
      colors: {
        no_action:                       "#475569",
        re_engagement_sequence_coaching: "#38bdf8",
        multithreading_coaching:         "#f97316",
        executive_outreach_coaching:     "#f43f5e",
        deal_velocity_coaching:          "#fbbf24",
        deal_rescue_intervention:        "#ef4444",
      },
    },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}

      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="p-2 rounded-xl bg-sky-500/10 border border-sky-500/20">
          <svg className="w-6 h-6 text-sky-400" fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <div>
          <h1 className="text-xl font-bold text-white">Sales Buyer Engagement Velocity Intelligence</h1>
          <p className="text-xs text-slate-400">Per-rep buyer engagement patterns — response velocity, stakeholder breadth &amp; deal momentum signals</p>
        </div>
        <button
          onClick={load}
          className="ml-auto px-3 py-1.5 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 transition-colors"
        >
          {loading ? "Loading…" : "Refresh"}
        </button>
      </div>

      {/* KPI strip */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {[
          { label: "Total Reps",        value: s?.total ?? "—" },
          { label: "Avg Composite",     value: s ? s.avg_engagement_composite.toFixed(1) : "—" },
          { label: "Engagement Gaps",   value: s?.engagement_gap_count ?? "—" },
          { label: "Need Coaching",     value: s?.coaching_count ?? "—" },
          { label: "Pipeline at Risk",  value: s ? fmtUSD(s.total_estimated_pipeline_at_risk_usd) : "—" },
          { label: "Critical Risk",     value: s ? (s.risk_counts["critical"] ?? 0) : "—" },
        ].map(({ label, value }) => (
          <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-400">{label}</p>
            <p className="text-xl font-bold text-white mt-1">{value}</p>
          </div>
        ))}
      </div>

      {/* Gauges */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
        <p className="text-sm font-semibold text-slate-300 mb-4">Average Sub-Scores</p>
        <div className="flex flex-wrap justify-around gap-4">
          <Gauge label="Velocity"        value={s?.avg_velocity_score        ?? 0} color="#38bdf8" />
          <Gauge label="Breadth"         value={s?.avg_breadth_score         ?? 0} color="#60a5fa" />
          <Gauge label="Responsiveness"  value={s?.avg_responsiveness_score  ?? 0} color="#818cf8" />
          <Gauge label="Momentum"        value={s?.avg_momentum_score        ?? 0} color="#a78bfa" />
        </div>
      </div>

      {/* Distributions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {distributions.map((d) => (
          <div key={d.title} className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <DistBar title={d.title} counts={d.counts} colors={d.colors} total={s?.total ?? 0} />
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <div className="flex gap-1 flex-wrap">
          {["all", "low", "moderate", "high", "critical"].map((r) => (
            <button
              key={r}
              onClick={() => setRiskFilter(r)}
              className={`px-3 py-1 text-xs rounded-full border transition-colors capitalize ${
                riskFilter === r
                  ? "bg-sky-500 text-slate-900 border-sky-500 font-semibold"
                  : "bg-slate-800 text-slate-300 border-slate-700 hover:border-slate-500"
              }`}
            >
              {r}
            </button>
          ))}
        </div>
        <div className="flex gap-1 flex-wrap">
          {["all", "buyer_ghosting_cycle", "single_contact_dependency", "response_lag_accumulation", "momentum_reversal", "executive_access_deficit"].map((p) => (
            <button
              key={p}
              onClick={() => setPatternFilter(p)}
              className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                patternFilter === p
                  ? "bg-sky-500 text-slate-900 border-sky-500 font-semibold"
                  : "bg-slate-800 text-slate-300 border-slate-700 hover:border-slate-500"
              }`}
            >
              {patternLabel[p] ?? p}
            </button>
          ))}
        </div>
      </div>

      {/* Rep cards */}
      {loading ? (
        <div className="text-center py-16 text-slate-500">Loading…</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {(data?.reps ?? []).map((rep) => (
            <button
              key={rep.rep_id}
              onClick={() => setSelected(rep)}
              className={`text-left bg-slate-900 border rounded-2xl p-5 hover:border-sky-500/60 transition-colors space-y-3 ${riskBorder[rep.engagement_risk] ?? "border-slate-800"}`}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-semibold text-white">{rep.rep_id}</p>
                  <p className="text-xs text-slate-400">{rep.region}</p>
                </div>
                <span className={`text-xs font-bold uppercase ${riskColor[rep.engagement_risk] ?? "text-slate-400"}`}>
                  {rep.engagement_risk}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className={`px-2 py-0.5 rounded-md text-xs font-medium ${patternColor[rep.engagement_pattern] ?? "bg-slate-700 text-slate-300"}`}>
                  {patternLabel[rep.engagement_pattern] ?? rep.engagement_pattern}
                </span>
                <span className={`px-2 py-0.5 rounded-md text-xs font-medium ${severityBadge[rep.engagement_severity] ?? "bg-slate-700 text-slate-300"}`}>
                  {rep.engagement_severity}
                </span>
              </div>

              <div className="flex justify-between text-xs text-slate-400">
                <span>Composite <span className="text-white font-semibold">{rep.engagement_composite.toFixed(1)}</span></span>
                <span>At Risk <span className="text-red-400 font-semibold">{fmtUSD(rep.estimated_pipeline_at_risk_usd)}</span></span>
              </div>

              <div className="flex gap-1.5">
                {rep.has_engagement_gap && (
                  <span className="px-1.5 py-0.5 rounded text-[10px] bg-red-900/50 text-red-300">🔗 GAP</span>
                )}
                {rep.requires_engagement_coaching && (
                  <span className="px-1.5 py-0.5 rounded text-[10px] bg-sky-900/50 text-sky-300">🔗 COACH</span>
                )}
              </div>

              <p className="text-xs text-slate-500 line-clamp-2">{rep.engagement_signal}</p>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
