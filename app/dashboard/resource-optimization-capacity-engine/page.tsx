"use client";

import { useEffect, useState } from "react";

// ── types ────────────────────────────────────────────────────────────────────
interface ResourceItem {
  resource_id: string;
  resource_type: string;
  region: string;
  resource_risk: string;
  capacity_pattern: string;
  resource_severity: string;
  recommended_action: string;
  utilization_score: number;
  allocation_score: number;
  efficiency_score: number;
  planning_score: number;
  resource_composite: number;
  has_capacity_alert: boolean;
  requires_strategic_review: boolean;
  estimated_capacity_gap_index: number;
  resource_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_resource_composite: number;
  capacity_alert_count: number;
  strategic_review_count: number;
  avg_utilization_score: number;
  avg_allocation_score: number;
  avg_efficiency_score: number;
  avg_planning_score: number;
  avg_estimated_capacity_gap_index: number;
}

// ── helpers ──────────────────────────────────────────────────────────────────
const RISK_COLOR: Record<string, string> = {
  critical: "text-rose-400",
  high:     "text-amber-400",
  moderate: "text-yellow-400",
  low:      "text-slate-400",
};

const RISK_BG: Record<string, string> = {
  critical: "bg-rose-500/20 border-rose-500/40",
  high:     "bg-amber-500/20 border-amber-500/40",
  moderate: "bg-yellow-500/20 border-yellow-500/40",
  low:      "bg-slate-500/20 border-slate-500/40",
};

const SEVERITY_COLOR: Record<string, string> = {
  critical: "text-rose-400",
  strained: "text-amber-400",
  balanced: "text-yellow-400",
  optimal:  "text-slate-400",
};

const PATTERN_ICON: Record<string, string> = {
  resource_overload:        "🔴",
  capacity_gap:             "📉",
  allocation_imbalance:     "⚖️",
  constraint_bottleneck:    "🚧",
  utilization_inefficiency: "⚡",
  none:                     "—",
};

const TYPE_ICON: Record<string, string> = {
  human:     "👥",
  tech:      "💻",
  financial: "💰",
  physical:  "🏭",
};

function CompositeRing({ score, color }: { score: number; color: string }) {
  const r = 36, circ = 2 * Math.PI * r;
  const fill = (Math.min(score, 100) / 100) * circ;
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

function RiskDistBar({ counts }: { counts: Record<string, number> }) {
  const order  = ["critical", "high", "moderate", "low"];
  const colors = ["bg-rose-500", "bg-amber-500", "bg-yellow-500", "bg-slate-500"];
  const total  = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
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

// ── ResourceModal ─────────────────────────────────────────────────────────────
function ResourceModal({ item, onClose }: { item: ResourceItem; onClose: () => void }) {
  const [tab, setTab] = useState<"overview" | "scores" | "action">("overview");

  useEffect(() => {
    const esc = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", esc);
    return () => window.removeEventListener("keydown", esc);
  }, [onClose]);

  const ringColor =
    item.resource_composite >= 60 ? "#f43f5e"
    : item.resource_composite >= 40 ? "#f59e0b"
    : item.resource_composite >= 20 ? "#eab308"
    : "#64748b";

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
          <CompositeRing score={item.resource_composite} color={ringColor} />
          <div className="flex-1 min-w-0">
            <h2 className="text-white font-bold text-lg truncate">
              {TYPE_ICON[item.resource_type] || "📦"} {item.resource_id}
            </h2>
            <p className="text-slate-400 text-sm">{item.resource_type} · {item.region}</p>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[item.resource_risk]}`}>
                {item.resource_risk} risk
              </span>
              <span className={`text-xs font-medium ${SEVERITY_COLOR[item.resource_severity]}`}>
                {item.resource_severity}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl">✕</button>
        </div>

        {/* tabs */}
        <div className="flex border-b border-slate-800">
          {(["overview", "scores", "action"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium capitalize transition-colors ${
                tab === t ? "text-amber-400 border-b-2 border-amber-400" : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "overview" && (
            <>
              <div className="grid grid-cols-2 gap-3">
                {[
                  ["Pattern",       PATTERN_ICON[item.capacity_pattern] + " " + item.capacity_pattern.replace(/_/g, " ")],
                  ["Gap Index",     item.estimated_capacity_gap_index.toFixed(2) + " / 10"],
                  ["Capacity Alert", item.has_capacity_alert ? "🚨 Yes" : "No"],
                  ["Strategic Review", item.requires_strategic_review ? "⚡ Yes" : "No"],
                ].map(([label, value]) => (
                  <div key={label as string} className="bg-slate-800/60 rounded-lg p-3">
                    <div className="text-xs text-slate-400">{label}</div>
                    <div className="text-white font-semibold mt-0.5 text-sm">{value}</div>
                  </div>
                ))}
              </div>
              <div className="bg-slate-800/60 rounded-lg p-3">
                <div className="text-xs text-slate-400 mb-1">Resource Signal</div>
                <div className="text-amber-300 text-sm leading-relaxed">{item.resource_signal}</div>
              </div>
            </>
          )}

          {tab === "scores" && (
            <div className="space-y-3">
              <ScoreBar label="Utilisation" value={item.utilization_score} color="bg-amber-500" />
              <ScoreBar label="Allocation"  value={item.allocation_score}  color="bg-orange-500" />
              <ScoreBar label="Efficacité"  value={item.efficiency_score}  color="bg-yellow-500" />
              <ScoreBar label="Planification" value={item.planning_score}  color="bg-amber-700" />
            </div>
          )}

          {tab === "action" && (
            <div className="space-y-3">
              <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-4">
                <div className="text-xs text-amber-400 uppercase tracking-wide mb-1">Action Recommandée</div>
                <div className="text-white font-bold text-lg capitalize">
                  {item.recommended_action.replace(/_/g, " ")}
                </div>
              </div>
              {item.requires_strategic_review && (
                <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-3 text-sm text-amber-300">
                  ⚡ Revue stratégique requise — escalader au comité de direction
                </div>
              )}
              {item.has_capacity_alert && (
                <div className="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 text-sm text-rose-300">
                  🚨 Alerte capacité active — intervention immédiate recommandée
                </div>
              )}
              {!item.has_capacity_alert && (
                <div className="bg-slate-800/60 rounded-xl p-3 text-sm text-slate-400">
                  Aucune alerte capacité — surveillance de routine suffisante
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── ResourceCard ──────────────────────────────────────────────────────────────
function ResourceCard({ item, onClick }: { item: ResourceItem; onClick: () => void }) {
  const ringColor =
    item.resource_composite >= 60 ? "#f43f5e"
    : item.resource_composite >= 40 ? "#f59e0b"
    : item.resource_composite >= 20 ? "#eab308"
    : "#64748b";

  return (
    <div
      onClick={onClick}
      className="bg-slate-900 border border-slate-800 rounded-xl p-4 cursor-pointer hover:border-amber-700 hover:bg-slate-800/60 transition-all"
    >
      <div className="flex items-center gap-3">
        <CompositeRing score={item.resource_composite} color={ringColor} />
        <div className="flex-1 min-w-0">
          <div className="text-white font-semibold truncate">
            {TYPE_ICON[item.resource_type] || "📦"} {item.resource_id}
          </div>
          <div className="text-slate-400 text-xs">{item.resource_type} · {item.region}</div>
          <div className="flex gap-2 mt-1 flex-wrap">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${RISK_BG[item.resource_risk]}`}>
              {item.resource_risk}
            </span>
          </div>
        </div>
        <div className="text-right shrink-0">
          {item.requires_strategic_review && <div className="text-xs text-amber-400">⚡ Revue</div>}
          <div className={`text-sm font-bold mt-1 ${SEVERITY_COLOR[item.resource_severity]}`}>
            {item.resource_severity}
          </div>
          {item.has_capacity_alert && (
            <div className="text-xs text-rose-400 mt-1">🚨</div>
          )}
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-400">
        {PATTERN_ICON[item.capacity_pattern]} {item.capacity_pattern.replace(/_/g, " ")} · gap: {item.estimated_capacity_gap_index.toFixed(2)}
      </div>
    </div>
  );
}

// ── page ─────────────────────────────────────────────────────────────────────
export default function ResourceOptimizationCapacityEnginePage() {
  const [resources, setResources] = useState<ResourceItem[]>([]);
  const [summary, setSummary]     = useState<Summary | null>(null);
  const [loading, setLoading]     = useState(true);
  const [selected, setSelected]   = useState<ResourceItem | null>(null);
  const [filterRisk,    setFilterRisk]    = useState("all");
  const [filterPattern, setFilterPattern] = useState("all");

  useEffect(() => {
    async function load() {
        setLoading(true);
        const params = new URLSearchParams();
        if (filterRisk    !== "all") params.set("risk",    filterRisk);
        if (filterPattern !== "all") params.set("pattern", filterPattern);
        const res  = await fetch(`/api/resource-optimization-capacity-engine?${params}`);
        const data = await res.json();
        setResources(data.resources);
        setSummary(data.summary);
        setLoading(false);
  }
    load();
  }, [filterRisk, filterPattern]);

  const distributions = [
    { title: "Utilisation Moy.",  counts: summary?.risk_counts ?? {},    colors: { critical: "bg-rose-500", high: "bg-amber-500", moderate: "bg-yellow-500", low: "bg-slate-500" } },
    { title: "Patterns",          counts: summary?.pattern_counts ?? {},  colors: { resource_overload: "bg-rose-500", capacity_gap: "bg-amber-500", allocation_imbalance: "bg-yellow-500", constraint_bottleneck: "bg-orange-500", utilization_inefficiency: "bg-amber-700", none: "bg-slate-500" } },
  ] as Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }>;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">

        {/* header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Resource Optimization & Capacity Planning Engine</h1>
          <p className="text-slate-400 text-sm mt-1">
            Évalue les ressources humaines, technologiques, financières et physiques pour détecter
            surcharges, écarts de capacité, déséquilibres d&apos;allocation et inefficacités — et recommande
            la réponse opérationnelle ou stratégique adaptée.
          </p>
        </div>

        {/* KPI strip */}
        {summary && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {[
              { label: "Ressources",        value: summary.total },
              { label: "Composite Moy.",    value: summary.avg_resource_composite.toFixed(1),           color: "text-amber-400" },
              { label: "Alertes Capacité",  value: summary.capacity_alert_count,                        color: "text-rose-400" },
              { label: "Revue Stratégique", value: summary.strategic_review_count,                      color: "text-orange-400" },
              { label: "Écart Moy.",        value: summary.avg_estimated_capacity_gap_index.toFixed(2), color: "text-amber-300" },
              { label: "Moy. Util.",        value: summary.avg_utilization_score.toFixed(1),            color: "text-yellow-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                <div className="text-xs text-slate-400">{label}</div>
                <div className={`text-2xl font-bold mt-1 ${color ?? "text-white"}`}>{value}</div>
              </div>
            ))}
          </div>
        )}

        {/* 4 gauge bars */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <div className="text-sm font-semibold text-slate-300 mb-4">Scores Moyens par Dimension</div>
            <div className="space-y-3">
              <ScoreBar label="Utilisation" value={summary.avg_utilization_score} color="bg-amber-500" />
              <ScoreBar label="Allocation"  value={summary.avg_allocation_score}  color="bg-orange-500" />
              <ScoreBar label="Efficacité"  value={summary.avg_efficiency_score}  color="bg-yellow-500" />
              <ScoreBar label="Planification" value={summary.avg_planning_score}  color="bg-amber-700" />
            </div>
          </div>
        )}

        {/* distribution bars */}
        {summary && (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {distributions.map(({ title, counts, colors }) => {
              const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
              return (
                <div key={title} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
                  <div className="text-xs text-slate-400 mb-2">{title}</div>
                  <div className="flex gap-1 h-3 rounded-full overflow-hidden">
                    {Object.entries(counts).map(([k, v]) => (
                      <div
                        key={k}
                        className={colors[k] ?? "bg-slate-600"}
                        style={{ width: `${(v / total) * 100}%` }}
                        title={`${k}: ${v}`}
                      />
                    ))}
                  </div>
                  <div className="flex flex-wrap gap-2 mt-2 text-xs text-slate-500">
                    {Object.entries(counts).map(([k, v]) => (
                      <span key={k}>{k.replace(/_/g, " ")}: {v}</span>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* risk distribution bar */}
        {summary && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <div className="text-xs text-slate-400 mb-2">Distribution du Risque Ressource</div>
            <RiskDistBar counts={summary.risk_counts} />
            <div className="flex gap-4 mt-2 text-xs text-slate-500">
              {["critical", "high", "moderate", "low"].map((k) => (
                <span key={k} className={RISK_COLOR[k]}>{k}: {summary.risk_counts[k] || 0}</span>
              ))}
            </div>
          </div>
        )}

        {/* filters */}
        <div className="flex flex-wrap gap-2">
          {[
            { label: "Tous",           val: "all" },
            { label: "🔴 Critical",    val: "critical" },
            { label: "🟠 High",        val: "high" },
            { label: "🟡 Moderate",    val: "moderate" },
            { label: "⚫ Low",         val: "low" },
          ].map(({ label, val }) => (
            <button
              key={val}
              onClick={() => setFilterRisk(val)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                filterRisk === val
                  ? "bg-amber-700 text-white"
                  : "bg-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {label}
            </button>
          ))}
          <select
            value={filterPattern}
            onChange={(e) => setFilterPattern(e.target.value)}
            className="px-3 py-1.5 rounded-lg text-xs bg-slate-800 text-slate-300 border border-slate-700"
          >
            <option value="all">Tous Patterns</option>
            {["resource_overload", "capacity_gap", "allocation_imbalance", "constraint_bottleneck", "utilization_inefficiency", "none"].map((p) => (
              <option key={p} value={p}>{p.replace(/_/g, " ")}</option>
            ))}
          </select>
        </div>

        {/* resources grid */}
        {loading ? (
          <div className="text-slate-400 text-center py-16">Analyse du portefeuille de ressources…</div>
        ) : resources.length === 0 ? (
          <div className="text-slate-500 text-center py-16">Aucune ressource ne correspond aux filtres.</div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {resources.map((r) => (
              <ResourceCard key={r.resource_id} item={r} onClick={() => setSelected(r)} />
            ))}
          </div>
        )}
      </div>

      {selected && <ResourceModal item={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
