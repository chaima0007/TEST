"use client";

import { useEffect, useState } from "react";

interface Territory {
  territory_id: string;
  territory_name: string;
  rep_id: string;
  whitespace_priority: string;
  whitespace_type: string;
  territory_health: string;
  whitespace_action: string;
  opportunity_density_score: number;
  market_timing_score: number;
  territory_coverage_score: number;
  icp_alignment_score: number;
  whitespace_composite: number;
  estimated_whitespace_arr: number;
  territory_penetration_pct: number;
  is_high_potential_territory: boolean;
  needs_immediate_prospecting: boolean;
  region: string;
}

interface Summary {
  total: number;
  priority_counts: Record<string, number>;
  type_counts: Record<string, number>;
  health_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_whitespace_composite: number;
  total_estimated_whitespace_arr: number;
  high_potential_count: number;
  immediate_prospecting_count: number;
  avg_opportunity_density_score: number;
  avg_market_timing_score: number;
  avg_territory_coverage_score: number;
  avg_icp_alignment_score: number;
}

const PRIORITY_COLORS: Record<string, string> = {
  urgent: "text-red-400",
  high: "text-orange-400",
  medium: "text-yellow-400",
  low: "text-slate-400",
};

const PRIORITY_BG: Record<string, string> = {
  urgent: "bg-red-500/20 border-red-500/40",
  high: "bg-orange-500/20 border-orange-500/40",
  medium: "bg-yellow-500/20 border-yellow-500/40",
  low: "bg-slate-700/40 border-slate-600/40",
};

const HEALTH_COLOR: Record<string, string> = {
  underpenetrated: "#22d3ee",
  developing: "#a78bfa",
  optimized: "#34d399",
  saturated: "#f87171",
};

const TYPE_LABELS: Record<string, string> = {
  new_logo: "New Logo",
  product_expand: "Product Expand",
  geo_expand: "Geo Expand",
  segment_expand: "Segment Expand",
  dormant_reactivate: "Dormant Reactivate",
};

const ACTION_LABELS: Record<string, string> = {
  nurture: "Nurture",
  prospect: "Prospect",
  prioritize: "Prioritize",
  immediate_focus: "Immediate Focus",
};

function WhitespaceRing({ score, priority }: { score: number; priority: string }) {
  const r = 52;
  const circ = 2 * Math.PI * r;
  const fill = (score / 100) * circ;
  const color =
    priority === "urgent" ? "#f87171" :
    priority === "high"   ? "#fb923c" :
    priority === "medium" ? "#facc15" : "#64748b";
  return (
    <svg width="128" height="128" viewBox="0 0 128 128">
      <circle cx="64" cy="64" r={r} fill="none" stroke="#1e293b" strokeWidth="12" />
      <circle
        cx="64" cy="64" r={r} fill="none"
        stroke={color} strokeWidth="12"
        strokeDasharray={`${fill} ${circ}`}
        strokeLinecap="round"
        transform="rotate(-90 64 64)"
      />
      <text x="64" y="60" textAnchor="middle" fill={color} fontSize="22" fontWeight="bold">{score}</text>
      <text x="64" y="78" textAnchor="middle" fill="#94a3b8" fontSize="10">Composite</text>
    </svg>
  );
}

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1">
        <span className="text-slate-400">{label}</span>
        <span className="text-slate-200 font-medium">{value}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className="h-full rounded-full transition-all duration-700" style={{ width: `${value}%`, backgroundColor: color }} />
      </div>
    </div>
  );
}

function PriorityBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  const order = ["urgent", "high", "medium", "low"];
  const colors = ["#f87171", "#fb923c", "#facc15", "#64748b"];
  return (
    <div className="flex h-3 rounded-full overflow-hidden gap-0.5">
      {order.map((k, i) =>
        (counts[k] || 0) > 0 ? (
          <div
            key={k}
            title={`${k}: ${counts[k]}`}
            style={{ width: `${((counts[k] || 0) / total) * 100}%`, backgroundColor: colors[i] }}
          />
        ) : null
      )}
    </div>
  );
}

function TerritoryModal({ territory, onClose }: { territory: Territory; onClose: () => void }) {
  const [tab, setTab] = useState<"signals" | "scores" | "actions">("signals");

  useEffect(() => {
    const handler = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const priorityColor = PRIORITY_COLORS[territory.whitespace_priority] || "text-slate-400";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div>
              <h2 className="text-slate-100 font-semibold text-lg leading-tight">{territory.territory_name}</h2>
              <p className="text-slate-400 text-sm mt-0.5">{territory.rep_id} · {territory.region}</p>
            </div>
            <span className={`text-xs font-bold uppercase px-2 py-1 rounded-full border ${PRIORITY_BG[territory.whitespace_priority]} ${priorityColor}`}>
              {territory.whitespace_priority}
            </span>
          </div>
          <div className="flex gap-2 mt-4">
            {(["signals", "scores", "actions"] as const).map((t) => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-colors ${
                  tab === t ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {t.charAt(0).toUpperCase() + t.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Body */}
        <div className="p-5 space-y-4">
          {tab === "signals" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Type", TYPE_LABELS[territory.whitespace_type] || territory.whitespace_type],
                  ["Health", territory.territory_health.replace(/_/g, " ")],
                  ["Penetration", `${territory.territory_penetration_pct}%`],
                  ["Est. ARR", `$${(territory.estimated_whitespace_arr / 1e6).toFixed(1)}M`],
                ].map(([label, value]) => (
                  <div key={label} className="bg-slate-800/60 rounded-xl p-3">
                    <p className="text-xs text-slate-500">{label}</p>
                    <p className="text-sm font-semibold text-slate-100 capitalize mt-0.5">{value}</p>
                  </div>
                ))}
              </div>
              <div className="grid grid-cols-2 gap-2">
                {territory.is_high_potential_territory && (
                  <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-lg p-2 text-xs text-emerald-400 flex items-center gap-1.5">
                    <span>★</span> High Potential
                  </div>
                )}
                {territory.needs_immediate_prospecting && (
                  <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-2 text-xs text-red-400 flex items-center gap-1.5">
                    <span>⚡</span> Immediate Focus
                  </div>
                )}
              </div>
            </>
          )}
          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Opportunity Density" value={territory.opportunity_density_score} color="#818cf8" />
              <ScoreBar label="Market Timing" value={territory.market_timing_score} color="#34d399" />
              <ScoreBar label="Coverage Score" value={territory.territory_coverage_score} color="#fb923c" />
              <ScoreBar label="ICP Alignment" value={territory.icp_alignment_score} color="#a78bfa" />
              <div className="pt-2 border-t border-slate-800">
                <ScoreBar label="Whitespace Composite" value={territory.whitespace_composite} color="#f472b6" />
              </div>
            </div>
          )}
          {tab === "actions" && (
            <div className="space-y-3">
              <div className="bg-slate-800/60 rounded-xl p-4">
                <p className="text-xs text-slate-500 mb-1">Recommended Action</p>
                <p className="text-indigo-300 font-semibold capitalize">{ACTION_LABELS[territory.whitespace_action] || territory.whitespace_action}</p>
              </div>
              <div className="space-y-2 text-sm text-slate-300">
                {territory.whitespace_action === "immediate_focus" && (
                  <p className="bg-red-500/10 border border-red-500/20 rounded-lg p-3 text-red-300 text-xs">
                    This territory has high-density whitespace with active buying signals. Prioritize outreach this week.
                  </p>
                )}
                {territory.whitespace_action === "prioritize" && (
                  <p className="bg-orange-500/10 border border-orange-500/20 rounded-lg p-3 text-orange-300 text-xs">
                    Strong whitespace opportunity — schedule 10+ prospecting touches in the next 2 weeks.
                  </p>
                )}
                {territory.whitespace_action === "prospect" && (
                  <p className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-3 text-yellow-300 text-xs">
                    Medium-priority whitespace. Add to weekly prospecting cadence.
                  </p>
                )}
                {territory.whitespace_action === "nurture" && (
                  <p className="bg-slate-700/60 rounded-lg p-3 text-slate-400 text-xs">
                    Low whitespace opportunity. Maintain through marketing nurture sequences.
                  </p>
                )}
              </div>
            </div>
          )}
        </div>

        <div className="p-4 border-t border-slate-800">
          <button onClick={onClose} className="w-full py-2 text-sm text-slate-400 hover:text-slate-200 transition-colors">
            Close
          </button>
        </div>
      </div>
    </div>
  );
}

function TerritoryCard({ territory, onClick }: { territory: Territory; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className={`bg-slate-900 border rounded-2xl p-4 cursor-pointer hover:border-indigo-500/50 transition-all ${PRIORITY_BG[territory.whitespace_priority]}`}
    >
      <div className="flex items-start justify-between gap-2 mb-3">
        <div className="min-w-0">
          <p className="text-slate-100 font-semibold text-sm truncate">{territory.territory_name}</p>
          <p className="text-slate-500 text-xs mt-0.5">{territory.region} · {territory.rep_id}</p>
        </div>
        <span className={`text-xs font-bold uppercase shrink-0 ${PRIORITY_COLORS[territory.whitespace_priority]}`}>
          {territory.whitespace_priority}
        </span>
      </div>

      <div className="flex items-center gap-3 mb-3">
        <WhitespaceRing score={territory.whitespace_composite} priority={territory.whitespace_priority} />
        <div className="flex-1 space-y-2 min-w-0">
          <ScoreBar label="Opportunity" value={territory.opportunity_density_score} color="#818cf8" />
          <ScoreBar label="Timing" value={territory.market_timing_score} color="#34d399" />
          <ScoreBar label="Coverage" value={territory.territory_coverage_score} color="#fb923c" />
          <ScoreBar label="ICP Fit" value={territory.icp_alignment_score} color="#a78bfa" />
        </div>
      </div>

      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-400">
          <span
            className="inline-block w-2 h-2 rounded-full mr-1"
            style={{ backgroundColor: HEALTH_COLOR[territory.territory_health] || "#64748b" }}
          />
          {territory.territory_health.replace(/_/g, " ")} · {territory.territory_penetration_pct}% penetrated
        </span>
        <span className="text-emerald-400 font-medium">${(territory.estimated_whitespace_arr / 1e6).toFixed(1)}M ARR</span>
      </div>
      <div className="flex gap-1 mt-2">
        {territory.is_high_potential_territory && (
          <span className="text-xs bg-emerald-500/15 text-emerald-400 rounded px-1.5 py-0.5">★ High Potential</span>
        )}
        {territory.needs_immediate_prospecting && (
          <span className="text-xs bg-red-500/15 text-red-400 rounded px-1.5 py-0.5">⚡ Immediate Focus</span>
        )}
      </div>
    </div>
  );
}

export default function TerritoryWhitespacePage() {
  const [data, setData] = useState<{ territories: Territory[]; summary: Summary } | null>(null);
  const [selected, setSelected] = useState<Territory | null>(null);
  const [filterPriority, setFilterPriority] = useState("all");
  const [filterType, setFilterType] = useState("all");

  useEffect(() => {
    async function load() {
        const params = new URLSearchParams();
        if (filterPriority !== "all") params.set("priority", filterPriority);
        if (filterType !== "all")     params.set("type", filterType);
        const res = await fetch(`/api/territory-whitespace?${params}`);
        setData(await res.json());
  }
    load();
  }, [filterPriority, filterType]);

  const s = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        {/* Header */}
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Territory Whitespace Analyzer</h1>
          <p className="text-slate-400 text-sm mt-1">Identify untapped accounts matching ICP with high-intent buying signals</p>
        </div>

        {/* Urgent alert */}
        {s && s.immediate_prospecting_count > 0 && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 flex items-center gap-3">
            <span className="text-2xl">🎯</span>
            <div>
              <p className="text-red-300 font-semibold">
                {s.immediate_prospecting_count} {s.immediate_prospecting_count === 1 ? "territory" : "territories"} need immediate prospecting focus
              </p>
              <p className="text-red-400/80 text-xs mt-0.5">
                Total whitespace ARR at stake: ${s ? (s.total_estimated_whitespace_arr / 1e6).toFixed(1) : "—"}M
              </p>
            </div>
          </div>
        )}

        {/* KPI strip */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {[
            { label: "Total Territories", value: s?.total ?? "—", sub: "in analysis" },
            { label: "Avg Composite", value: s ? `${s.avg_whitespace_composite}` : "—", sub: "whitespace score" },
            { label: "High Potential", value: s?.high_potential_count ?? "—", sub: "territories" },
            { label: "Total Whitespace ARR", value: s ? `$${(s.total_estimated_whitespace_arr / 1e6).toFixed(1)}M` : "—", sub: "uncaptured potential" },
          ].map(({ label, value, sub }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <p className="text-xs text-slate-500">{label}</p>
              <p className="text-2xl font-bold text-slate-100 mt-1">{value}</p>
              <p className="text-xs text-slate-500 mt-0.5">{sub}</p>
            </div>
          ))}
        </div>

        {/* Priority distribution + score averages */}
        {s && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Priority Distribution</h3>
              <PriorityBar counts={s.priority_counts} />
              <div className="flex flex-wrap gap-x-4 gap-y-1 mt-3">
                {Object.entries(s.priority_counts).map(([k, v]) => (
                  <span key={k} className={`text-xs ${PRIORITY_COLORS[k] || "text-slate-400"}`}>
                    {k}: {v}
                  </span>
                ))}
              </div>
            </div>
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <h3 className="text-sm font-semibold text-slate-300 mb-3">Avg Score Breakdown</h3>
              <div className="space-y-2">
                <ScoreBar label="Opportunity Density" value={s.avg_opportunity_density_score} color="#818cf8" />
                <ScoreBar label="Market Timing" value={s.avg_market_timing_score} color="#34d399" />
                <ScoreBar label="Coverage Score" value={s.avg_territory_coverage_score} color="#fb923c" />
                <ScoreBar label="ICP Alignment" value={s.avg_icp_alignment_score} color="#a78bfa" />
              </div>
            </div>
          </div>
        )}

        {/* Filters */}
        <div className="flex flex-wrap gap-2">
          <div className="flex gap-1 flex-wrap">
            {["all", "urgent", "high", "medium", "low"].map((p) => (
              <button
                key={p}
                onClick={() => setFilterPriority(p)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  filterPriority === p ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {p === "all" ? "All Priorities" : p.charAt(0).toUpperCase() + p.slice(1)}
              </button>
            ))}
          </div>
          <div className="flex gap-1 flex-wrap">
            {["all", "new_logo", "product_expand", "geo_expand", "segment_expand", "dormant_reactivate"].map((t) => (
              <button
                key={t}
                onClick={() => setFilterType(t)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  filterType === t ? "bg-violet-600 text-white" : "bg-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {t === "all" ? "All Types" : TYPE_LABELS[t] || t}
              </button>
            ))}
          </div>
        </div>

        {/* Territory cards grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {data?.territories.map((t) => (
            <TerritoryCard key={t.territory_id} territory={t} onClick={() => setSelected(t)} />
          ))}
        </div>

        {data?.territories.length === 0 && (
          <div className="text-center py-16 text-slate-500">No territories match the selected filters.</div>
        )}
      </div>

      {selected && <TerritoryModal territory={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
