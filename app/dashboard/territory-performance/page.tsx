"use client";

import { useEffect, useState, useCallback } from "react";

interface TerritoryData {
  territory_id: string;
  territory_name: string;
  rep_id: string;
  region: string;
  territory_status: string;
  territory_risk: string;
  market_penetration: string;
  territory_action: string;
  attainment_pct: number;
  projected_attainment: number;
  coverage_ratio: number;
  penetration_pct: number;
  account_health_score: number;
  activity_score: number;
  growth_score: number;
  is_at_risk: boolean;
  needs_rebalancing: boolean;
  actual_revenue: number;
  target_revenue: number;
}

interface Summary {
  total: number;
  status_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  penetration_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_attainment_pct: number;
  avg_projected_attainment: number;
  total_revenue_gap: number;
  at_risk_count: number;
  rebalancing_count: number;
  avg_account_health: number;
  avg_growth_score: number;
  high_performing_count: number;
}

const STATUS_COLOR: Record<string, string> = {
  overperforming:  "text-emerald-400 bg-emerald-400/10 border-emerald-400/20",
  on_target:       "text-sky-400 bg-sky-400/10 border-sky-400/20",
  underperforming: "text-yellow-400 bg-yellow-400/10 border-yellow-400/20",
  critical:        "text-red-400 bg-red-400/10 border-red-400/20",
};

const RISK_COLOR: Record<string, string> = {
  low:      "text-emerald-400",
  medium:   "text-yellow-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};

const STATUS_ARC_COLOR: Record<string, string> = {
  overperforming:  "#10b981",
  on_target:       "#38bdf8",
  underperforming: "#fbbf24",
  critical:        "#f87171",
};

function fmt(n: number) {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000)     return `$${(n / 1_000).toFixed(0)}K`;
  return `$${n}`;
}

function TerritoryGauge({ pct, status }: { pct: number; status: string }) {
  const r = 38, cx = 48, cy = 48;
  const circ = 2 * Math.PI * r;
  const arc = Math.min(pct / 130, 1) * circ;
  const color = STATUS_ARC_COLOR[status] || "#94a3b8";
  return (
    <svg viewBox="0 0 96 96" className="w-24 h-24">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth="8"
        strokeDasharray={`${arc} ${circ - arc}`} strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`} />
      <text x={cx} y={cy - 4} textAnchor="middle" fill="white" fontSize="11" fontWeight="bold">
        {pct.toFixed(0)}%
      </text>
      <text x={cx} y={cy + 10} textAnchor="middle" fill="#94a3b8" fontSize="7">projected</text>
    </svg>
  );
}

function StatusDistBar({ counts }: { counts: Record<string, number> }) {
  const order = ["overperforming", "on_target", "underperforming", "critical"];
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  const colors = ["#10b981", "#38bdf8", "#fbbf24", "#f87171"];
  const labels = ["Overperf.", "On Target", "Underperf.", "Critical"];
  return (
    <div className="space-y-1.5">
      {order.map((k, i) => {
        const v = counts[k] || 0;
        const w = (v / total) * 100;
        return (
          <div key={k} className="flex items-center gap-2 text-xs">
            <span className="w-16 text-slate-400 text-right">{labels[i]}</span>
            <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
              <div className="h-full rounded-full" style={{ width: `${w}%`, backgroundColor: colors[i] }} />
            </div>
            <span className="w-4 text-slate-300">{v}</span>
          </div>
        );
      })}
    </div>
  );
}

function MiniBar({ value, color }: { value: number; color: string }) {
  return (
    <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
      <div className="h-full rounded-full" style={{ width: `${Math.min(100, value)}%`, backgroundColor: color }} />
    </div>
  );
}

function TerritoryCard({ t, onClick }: { t: TerritoryData; onClick: () => void }) {
  const sc = STATUS_COLOR[t.territory_status] || "text-slate-400 bg-slate-400/10 border-slate-400/20";
  const rc = RISK_COLOR[t.territory_risk] || "text-slate-400";
  return (
    <button onClick={onClick}
      className="bg-slate-800/60 border border-slate-700 rounded-xl p-4 text-left hover:border-indigo-500/50 hover:bg-slate-800 transition-all w-full">
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="font-semibold text-slate-100 text-sm">{t.territory_name}</div>
          <div className="text-xs text-slate-500 mt-0.5">{t.region} · {t.rep_id}</div>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span className={`text-xs font-medium px-2 py-0.5 rounded-full border ${sc}`}>
            {t.territory_status.replace("_", " ")}
          </span>
          {t.needs_rebalancing && (
            <span className="text-xs text-violet-400 bg-violet-400/10 px-1.5 py-0.5 rounded border border-violet-400/20">rebalance</span>
          )}
        </div>
      </div>
      <div className="flex items-center gap-4 mb-3">
        <TerritoryGauge pct={t.projected_attainment} status={t.territory_status} />
        <div className="flex-1 space-y-1.5">
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Attainment</span>
            <span className="text-slate-200">{t.attainment_pct.toFixed(1)}%</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Coverage</span>
            <span className="text-slate-200">{t.coverage_ratio.toFixed(2)}×</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Penetration</span>
            <span className="text-slate-200">{t.penetration_pct.toFixed(0)}% — {t.market_penetration}</span>
          </div>
          <div className="flex justify-between text-xs">
            <span className="text-slate-400">Risk</span>
            <span className={rc}>{t.territory_risk}</span>
          </div>
        </div>
      </div>
      <div className="space-y-1">
        <div className="flex justify-between text-xs mb-0.5">
          <span className="text-slate-400">Account Health</span>
          <span className="text-slate-300">{t.account_health_score.toFixed(0)}</span>
        </div>
        <MiniBar value={t.account_health_score} color="#10b981" />
        <div className="flex justify-between text-xs mb-0.5 mt-1">
          <span className="text-slate-400">Growth Score</span>
          <span className="text-slate-300">{t.growth_score.toFixed(0)}</span>
        </div>
        <MiniBar value={t.growth_score} color="#818cf8" />
      </div>
    </button>
  );
}

function TerritoryModal({ t, onClose }: { t: TerritoryData; onClose: () => void }) {
  const [tab, setTab] = useState<"performance" | "market" | "actions">("performance");
  useEffect(() => {
    const fn = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", fn);
    return () => document.removeEventListener("keydown", fn);
  }, [onClose]);

  const sc = STATUS_COLOR[t.territory_status] || "text-slate-400 bg-slate-400/10 border-slate-400/20";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />
      <div className="relative bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl">
        <div className="flex items-start justify-between p-5 border-b border-slate-800">
          <div>
            <h2 className="text-lg font-bold text-white">{t.territory_name}</h2>
            <div className="flex items-center gap-2 mt-1 flex-wrap">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${sc}`}>
                {t.territory_status.replace("_", " ")}
              </span>
              <span className={`text-xs ${RISK_COLOR[t.territory_risk]}`}>{t.territory_risk} risk</span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-xl p-1">×</button>
        </div>
        <div className="flex border-b border-slate-800">
          {(["performance", "market", "actions"] as const).map((tab_name) => (
            <button key={tab_name} onClick={() => setTab(tab_name)}
              className={`flex-1 py-2.5 text-xs font-medium capitalize transition-colors ${tab === tab_name ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-400 hover:text-slate-200"}`}>
              {tab_name}
            </button>
          ))}
        </div>
        <div className="p-5 max-h-96 overflow-y-auto">
          {tab === "performance" && (
            <div className="space-y-3">
              <div className="flex justify-center mb-4">
                <TerritoryGauge pct={t.projected_attainment} status={t.territory_status} />
              </div>
              {[
                ["Actual Revenue", fmt(t.actual_revenue)],
                ["Target Revenue", fmt(t.target_revenue)],
                ["Attainment %", `${t.attainment_pct.toFixed(1)}%`],
                ["Projected %", `${t.projected_attainment.toFixed(1)}%`],
                ["Coverage Ratio", `${t.coverage_ratio.toFixed(2)}×`],
              ].map(([label, value]) => (
                <div key={label} className="flex justify-between text-sm border-b border-slate-800 pb-2">
                  <span className="text-slate-400">{label}</span>
                  <span className="text-slate-100 font-medium">{value}</span>
                </div>
              ))}
            </div>
          )}
          {tab === "market" && (
            <div className="space-y-3">
              {[
                ["Market Penetration", `${t.penetration_pct.toFixed(0)}% — ${t.market_penetration}`],
                ["Account Health", `${t.account_health_score.toFixed(0)}/100`],
                ["Activity Score", `${t.activity_score.toFixed(0)}/100`],
                ["Growth Score", `${t.growth_score.toFixed(0)}/100`],
              ].map(([label, value]) => (
                <div key={label} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">{label}</span>
                    <span className="text-slate-100 font-medium">{value}</span>
                  </div>
                  {label !== "Market Penetration" && (
                    <MiniBar
                      value={parseFloat(String(value).split("/")[0])}
                      color={label === "Account Health" ? "#10b981" : label === "Activity Score" ? "#22d3ee" : "#818cf8"}
                    />
                  )}
                </div>
              ))}
            </div>
          )}
          {tab === "actions" && (
            <div className="space-y-3">
              <div className="flex justify-between text-sm border-b border-slate-800 pb-2">
                <span className="text-slate-400">Recommended Action</span>
                <span className="text-indigo-400 font-medium capitalize">{t.territory_action.replace(/_/g, " ")}</span>
              </div>
              <div className="flex justify-between text-sm border-b border-slate-800 pb-2">
                <span className="text-slate-400">At Risk</span>
                <span className={t.is_at_risk ? "text-red-400" : "text-emerald-400"}>
                  {t.is_at_risk ? "Yes" : "No"}
                </span>
              </div>
              <div className="flex justify-between text-sm border-b border-slate-800 pb-2">
                <span className="text-slate-400">Needs Rebalancing</span>
                <span className={t.needs_rebalancing ? "text-violet-400" : "text-emerald-400"}>
                  {t.needs_rebalancing ? "Yes" : "No"}
                </span>
              </div>
              <div className="flex justify-between text-sm border-b border-slate-800 pb-2">
                <span className="text-slate-400">Rep</span>
                <span className="text-slate-200">{t.rep_id}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-400">Region</span>
                <span className="text-slate-200">{t.region}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function TerritoryPerformancePage() {
  const [territories, setTerritories] = useState<TerritoryData[]>([]);
  const [summary, setSummary]         = useState<Summary | null>(null);
  const [loading, setLoading]         = useState(true);
  const [selected, setSelected]       = useState<TerritoryData | null>(null);
  const [filterStatus, setFilterStatus] = useState("all");
  const [filterRisk, setFilterRisk]     = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (filterStatus !== "all") params.set("status", filterStatus);
      if (filterRisk   !== "all") params.set("risk", filterRisk);
      const res = await fetch(`/api/territory-performance?${params}`);
      const data = await res.json();
      setTerritories(data.territories || []);
      setSummary(data.summary || null);
    } catch {}
    setLoading(false);
  }, [filterStatus, filterRisk]);

  useEffect(() => { load(); }, [load]);

  const statuses = ["all", "overperforming", "on_target", "underperforming", "critical"];
  const risks    = ["all", "low", "medium", "high", "critical"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-white">Territory Performance</h1>
          <p className="text-slate-400 text-sm mt-1">Territory-level attainment, market penetration, and recommended actions</p>
        </div>

        {summary && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Avg Attainment", value: `${summary.avg_attainment_pct.toFixed(1)}%`, sub: "current period", color: "text-sky-400" },
              { label: "Avg Projected", value: `${summary.avg_projected_attainment.toFixed(1)}%`, sub: "end-of-period", color: "text-emerald-400" },
              { label: "Revenue Gap", value: fmt(summary.total_revenue_gap), sub: `${summary.at_risk_count} at risk`, color: "text-red-400" },
              { label: "High Performing", value: `${summary.high_performing_count}/${summary.total}`, sub: `${summary.rebalancing_count} rebalance needed`, color: "text-violet-400" },
            ].map((k) => (
              <div key={k.label} className="bg-slate-800/60 border border-slate-700 rounded-xl p-4">
                <div className="text-xs text-slate-400 mb-1">{k.label}</div>
                <div className={`text-2xl font-bold ${k.color}`}>{k.value}</div>
                <div className="text-xs text-slate-500 mt-1">{k.sub}</div>
              </div>
            ))}
          </div>
        )}

        {summary && (
          <div className="bg-slate-800/60 border border-slate-700 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-slate-300 mb-4">Territory Status Distribution</h2>
            <StatusDistBar counts={summary.status_counts} />
          </div>
        )}

        <div className="flex flex-wrap gap-3">
          <div className="flex gap-1 bg-slate-800/60 border border-slate-700 rounded-lg p-1">
            {statuses.map((s) => (
              <button key={s} onClick={() => setFilterStatus(s)}
                className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${filterStatus === s ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"}`}>
                {s === "all" ? "All" : s.replace("_", " ")}
              </button>
            ))}
          </div>
          <div className="flex gap-1 bg-slate-800/60 border border-slate-700 rounded-lg p-1">
            {risks.map((r) => (
              <button key={r} onClick={() => setFilterRisk(r)}
                className={`px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${filterRisk === r ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"}`}>
                {r === "all" ? "All Risk" : r}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="text-center text-slate-400 py-12">Loading...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {territories.map((t) => (
              <TerritoryCard key={t.territory_id} t={t} onClick={() => setSelected(t)} />
            ))}
          </div>
        )}
      </div>
      {selected && <TerritoryModal t={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
