"use client";

import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface Deal {
  deal_id: string;
  deal_name: string;
  rep_id: string;
  primary_objection_type: string;
  objection_severity: string;
  handling_readiness: string;
  objection_action: string;
  handling_effectiveness_score: number;
  objection_density_score: number;
  pattern_risk_score: number;
  rep_preparedness_score: number;
  objection_composite: number;
  handle_rate: number;
  late_stage_risk: boolean;
  is_objection_contained: boolean;
  needs_coaching: boolean;
  region: string;
}

interface Summary {
  total: number;
  objection_type_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  readiness_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_objection_composite: number;
  avg_handle_rate: number;
  contained_count: number;
  coaching_count: number;
  avg_handling_effectiveness_score: number;
  avg_pattern_risk_score: number;
  avg_rep_preparedness_score: number;
  avg_objection_density_score: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const SEVERITY_COLOR: Record<string, string> = {
  minor:        "text-emerald-400",
  moderate:     "text-amber-400",
  serious:      "text-orange-400",
  deal_breaker: "text-rose-400",
};
const SEVERITY_BG: Record<string, string> = {
  minor:        "bg-emerald-500/20 border-emerald-500/40",
  moderate:     "bg-amber-500/20 border-amber-500/40",
  serious:      "bg-orange-500/20 border-orange-500/40",
  deal_breaker: "bg-rose-500/20 border-rose-500/40",
};
const TYPE_ICON: Record<string, string> = {
  price:         "💰",
  timing:        "⏰",
  competitor:    "⚔️",
  status_quo:    "🔒",
  risk:          "🛡️",
  no_objection:  "✅",
};
const READINESS_COLOR: Record<string, string> = {
  prepared:    "text-emerald-400",
  needs_prep:  "text-amber-400",
  reactive:    "text-orange-400",
  unprepared:  "text-rose-400",
};

function ObjectionRing({ score, color }: { score: number; color: string }) {
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

function SeverityDistBar({ counts }: { counts: Record<string, number> }) {
  const order = ["minor", "moderate", "serious", "deal_breaker"];
  const colors = ["bg-emerald-500", "bg-amber-500", "bg-orange-500", "bg-rose-500"];
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
  const [tab, setTab] = useState<"signals" | "scores" | "coaching">("signals");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    deal.objection_composite >= 70 ? "#10b981"
    : deal.objection_composite >= 50 ? "#38bdf8"
    : deal.objection_composite >= 30 ? "#f59e0b"
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
          <ObjectionRing score={deal.objection_composite} color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">{deal.deal_name}</h2>
            <p className="text-slate-400 text-sm">{deal.rep_id} · {deal.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${SEVERITY_BG[deal.objection_severity]}`}>
                {deal.objection_severity.replace(/_/g, " ")}
              </span>
              <span className="text-xs text-slate-400">
                {TYPE_ICON[deal.primary_objection_type]} {deal.primary_objection_type.replace(/_/g, " ")}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["signals", "scores", "coaching"] as const).map((t) => (
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
                  ["Handle Rate",     deal.handle_rate.toFixed(0) + "%"],
                  ["Readiness",       deal.handling_readiness.replace(/_/g, " ")],
                  ["Contained",       deal.is_objection_contained ? "✅ Yes" : "❌ No"],
                  ["Late-Stage Risk", deal.late_stage_risk ? "⚠️ Yes" : "✅ No"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className={`font-semibold mt-0.5 ${label === "Readiness" ? READINESS_COLOR[deal.handling_readiness] : "text-white"}`}>{value}</div>
                  </div>
                ))}
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Handling Effectiveness" value={deal.handling_effectiveness_score} color="bg-indigo-500" />
              <ScoreBar label="Objection Density"      value={deal.objection_density_score}      color="bg-violet-500" />
              <ScoreBar label="Pattern Risk (inverted)" value={deal.pattern_risk_score}          color="bg-sky-500" />
              <ScoreBar label="Rep Preparedness"        value={deal.rep_preparedness_score}      color="bg-amber-500" />
            </div>
          )}

          {tab === "coaching" && (
            <div className="space-y-3">
              <div className="bg-indigo-500/10 border border-indigo-500/30 rounded-xl p-4">
                <div className="text-xs text-indigo-400 uppercase tracking-wide mb-1">Recommended Action</div>
                <div className="text-white font-bold text-lg capitalize">
                  {deal.objection_action.replace(/_/g, " ")}
                </div>
              </div>
              {deal.needs_coaching && (
                <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-3 text-sm text-amber-300">
                  🎓 Rep coaching required — use objection battlecard and ROI calculator
                </div>
              )}
              {deal.objection_severity === "deal_breaker" && (
                <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 text-sm text-rose-300">
                  🚨 Deal-breaker objection — executive call required immediately
                </div>
              )}
              {deal.is_objection_contained && (
                <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-3 text-sm text-emerald-300">
                  ✅ Objections contained — continue current handling approach
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
    deal.objection_composite >= 70 ? "#10b981"
    : deal.objection_composite >= 50 ? "#38bdf8"
    : deal.objection_composite >= 30 ? "#f59e0b"
    : "#f43f5e";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-indigo-500/50 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <ObjectionRing score={deal.objection_composite} color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">{deal.deal_name}</div>
          <div className="text-slate-400 text-xs">{deal.rep_id} · {deal.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${SEVERITY_BG[deal.objection_severity]}`}>
              {deal.objection_severity.replace(/_/g, " ")}
            </span>
            <span className="text-xs text-slate-400">
              {TYPE_ICON[deal.primary_objection_type]}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          <div className="text-sm font-bold text-white">{deal.handle_rate.toFixed(0)}%</div>
          <div className="text-xs text-slate-500">handled</div>
          {deal.needs_coaching && (
            <div className="text-xs text-amber-400 mt-1">🎓 coach</div>
          )}
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400 flex items-center gap-2">
        <span className={READINESS_COLOR[deal.handling_readiness]}>{deal.handling_readiness.replace(/_/g, " ")}</span>
        {deal.late_stage_risk && <span className="text-orange-400">· late-stage ⚠️</span>}
      </div>
    </div>
  );
}

// ── page ─────────────────────────────────────────────────────────────────────
export default function ObjectionPatternAnalyzerPage() {
  const [deals, setDeals]       = useState<Deal[]>([]);
  const [summary, setSummary]   = useState<Summary | null>(null);
  const [loading, setLoading]   = useState(true);
  const [selected, setSelected] = useState<Deal | null>(null);
  const [filterType,   setFilterType]   = useState("all");
  const [filterRegion, setFilterRegion] = useState("all");

  useEffect(() => {
    async function load() {
        setLoading(true);
        const params = new URLSearchParams();
        if (filterType   !== "all") params.set("type",   filterType);
        if (filterRegion !== "all") params.set("region", filterRegion);
        const res = await fetch(`/api/objection-pattern-analyzer?${params}`);
        const data = await res.json();
        setDeals(data.deals);
        setSummary(data.summary);
        setLoading(false);
  }
    load();
  }, [filterType, filterRegion]);

  const dealBreakerDeals = deals.filter((d) => d.objection_severity === "deal_breaker");

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Objection Pattern Analyzer</h1>
          <p className="text-slate-400 text-sm mt-1">
            Classifies objection types, tracks recurrence, and surfaces rep coaching opportunities
          </p>
        </div>

        {/* deal-breaker alert */}
        {dealBreakerDeals.length > 0 && (
          <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-4 flex items-center gap-3">
            <span className="text-2xl">🚨</span>
            <div>
              <div className="text-rose-300 font-semibold">
                {dealBreakerDeals.length} deal-breaker objection{dealBreakerDeals.length > 1 ? "s" : ""} — executive escalation needed
              </div>
              <div className="text-rose-400/70 text-xs mt-0.5">
                {dealBreakerDeals.map((d) => d.deal_name).join(" · ")}
              </div>
            </div>
          </div>
        )}

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {[
              { label: "Total Deals",   value: summary.total },
              { label: "Contained",     value: summary.contained_count,  color: "text-emerald-400" },
              { label: "Need Coaching", value: summary.coaching_count,   color: "text-amber-400" },
              { label: "Avg Handle %",  value: summary.avg_handle_rate.toFixed(1) + "%", color: "text-indigo-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* severity dist bar */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-400 mb-2">Objection Severity Distribution</div>
            <SeverityDistBar counts={summary.severity_counts} />
            <div className="flex gap-4 mt-2 text-xs text-slate-500">
              {["minor","moderate","serious","deal_breaker"].map((k) => (
                <span key={k} className={SEVERITY_COLOR[k]}>{k.replace(/_/g," ")}: {summary.severity_counts[k] || 0}</span>
              ))}
            </div>
          </div>
        )}

        {/* filters */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "All Types",     val: "all" },
            { label: "💰 Price",       val: "price" },
            { label: "⏰ Timing",      val: "timing" },
            { label: "⚔️ Competitor",  val: "competitor" },
            { label: "🔒 Status Quo",  val: "status_quo" },
            { label: "🛡️ Risk",         val: "risk" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterType(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterType === val
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
          <div className="text-slate-400 text-center py-16">Loading objection data…</div>
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
              <ScoreBar label="Handling Effectiveness"  value={summary.avg_handling_effectiveness_score} color="bg-indigo-500" />
              <ScoreBar label="Objection Density"       value={summary.avg_objection_density_score}      color="bg-violet-500" />
              <ScoreBar label="Pattern Risk (inverted)" value={summary.avg_pattern_risk_score}           color="bg-sky-500" />
              <ScoreBar label="Rep Preparedness"        value={summary.avg_rep_preparedness_score}       color="bg-amber-500" />
            </div>
          </div>
        )}
      </div>

      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
