"use client";

import { useEffect, useState } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface ChannelCredits {
  [channel: string]: number;
}

interface RoiByChannel {
  [channel: string]: number;
}

interface Deal {
  deal_id: string;
  account_id: string;
  rep_id: string;
  attributed_revenue: number;
  attribution_model: string;
  channel_credits: ChannelCredits;
  roi_by_channel: RoiByChannel;
  revenue_risk: string;
  optimization_action: string;
  top_channel: string;
  attribution_efficiency: number;
  pipeline_to_revenue_ratio: number;
  cost_per_acquisition: number;
  cycle_efficiency: number;
  is_high_value: boolean;
  deal_name: string;
  account_name: string;
  segment: string;
  industry: string;
  total_touchpoints: number;
  pipeline_created: number;
  closed_won_value: number;
  closed_lost_value: number;
}

interface Summary {
  total: number;
  model_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  action_counts: Record<string, number>;
  top_channel_counts: Record<string, number>;
  total_attributed_revenue: number;
  avg_attribution_efficiency: number;
  avg_pipeline_to_revenue_ratio: number;
  avg_cycle_efficiency: number;
  high_value_count: number;
  high_risk_count: number;
  scale_up_count: number;
  avg_cost_per_acquisition: number;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function riskColor(risk: string) {
  return (
    {
      low:      "text-emerald-400",
      medium:   "text-amber-400",
      high:     "text-orange-400",
      critical: "text-red-400",
    }[risk] ?? "text-slate-400"
  );
}

function riskBg(risk: string) {
  return (
    {
      low:      "bg-emerald-900/30 border-emerald-700/50",
      medium:   "bg-amber-900/30 border-amber-700/50",
      high:     "bg-orange-900/30 border-orange-700/50",
      critical: "bg-red-900/30 border-red-700/50",
    }[risk] ?? "bg-slate-800 border-slate-700"
  );
}

function actionBadge(action: string) {
  const map: Record<string, string> = {
    scale_up:   "bg-emerald-900/50 text-emerald-300 border border-emerald-700/50",
    maintain:   "bg-blue-900/50 text-blue-300 border border-blue-700/50",
    optimize:   "bg-violet-900/50 text-violet-300 border border-violet-700/50",
    reduce:     "bg-orange-900/50 text-orange-300 border border-orange-700/50",
    reallocate: "bg-red-900/50 text-red-300 border border-red-700/50",
  };
  return map[action] ?? "bg-slate-700 text-slate-300";
}

function modelBadge(model: string) {
  const map: Record<string, string> = {
    first_touch:    "bg-indigo-900/50 text-indigo-300 border border-indigo-700/50",
    last_touch:     "bg-purple-900/50 text-purple-300 border border-purple-700/50",
    linear:         "bg-cyan-900/50 text-cyan-300 border border-cyan-700/50",
    time_decay:     "bg-teal-900/50 text-teal-300 border border-teal-700/50",
    position_based: "bg-fuchsia-900/50 text-fuchsia-300 border border-fuchsia-700/50",
  };
  return map[model] ?? "bg-slate-700 text-slate-300";
}

function fmtLabel(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function fmtMoney(n: number) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M€`;
  if (n >= 1_000)     return `${(n / 1_000).toFixed(0)}k€`;
  return `${n.toFixed(0)}€`;
}

// ── Attribution Ring ─────────────────────────────────────────────────────────

function AttributionRing({ efficiency, size = 52 }: { efficiency: number; size?: number }) {
  const cx = size / 2;
  const cy = size / 2;
  const r  = size * 0.38;
  const circ = 2 * Math.PI * r;
  const arc  = (efficiency / 100) * circ;
  const color =
    efficiency >= 70 ? "#34d399" :
    efficiency >= 50 ? "#a78bfa" :
    efficiency >= 30 ? "#fbbf24" : "#f87171";

  return (
    <svg width={size} height={size} className="flex-shrink-0">
      <circle cx={cx} cy={cy} r={r} stroke="#1e293b" strokeWidth={size * 0.12} fill="none" />
      <circle
        cx={cx} cy={cy} r={r}
        stroke={color} strokeWidth={size * 0.12} fill="none"
        strokeDasharray={`${arc} ${circ - arc}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${cx} ${cy})`}
      />
      <text x={cx} y={cy + 1} textAnchor="middle" dominantBaseline="middle"
        fill={color} fontSize={size * 0.22} fontWeight="700">
        {Math.round(efficiency)}
      </text>
    </svg>
  );
}

// ── Model Distribution Bar ────────────────────────────────────────────────────

function ModelDistBar({ counts }: { counts: Record<string, number> }) {
  const total = Object.values(counts).reduce((s, n) => s + n, 0);
  if (total === 0) return null;
  const colors: Record<string, string> = {
    first_touch:    "bg-indigo-500",
    last_touch:     "bg-purple-500",
    linear:         "bg-cyan-500",
    time_decay:     "bg-teal-500",
    position_based: "bg-fuchsia-500",
  };
  const entries = Object.entries(counts).sort((a, b) => b[1] - a[1]);

  return (
    <div className="space-y-1.5">
      <div className="flex h-2.5 rounded-full overflow-hidden gap-px">
        {entries.map(([k, v]) => (
          <div
            key={k}
            className={`${colors[k] ?? "bg-slate-500"} transition-all`}
            style={{ width: `${(v / total) * 100}%` }}
          />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-1">
        {entries.map(([k, v]) => (
          <span key={k} className="flex items-center gap-1 text-xs text-slate-400">
            <span className={`w-2 h-2 rounded-full ${colors[k] ?? "bg-slate-500"}`} />
            {fmtLabel(k)} <span className="text-slate-300 font-medium">{v}</span>
          </span>
        ))}
      </div>
    </div>
  );
}

// ── Deal Modal ────────────────────────────────────────────────────────────────

function DealModal({ deal, onClose }: { deal: Deal; onClose: () => void }) {
  const [tab, setTab] = useState<"channels" | "roi" | "metrics">("channels");

  useEffect(() => {
    const fn = (e: KeyboardEvent) => e.key === "Escape" && onClose();
    document.addEventListener("keydown", fn);
    return () => document.removeEventListener("keydown", fn);
  }, [onClose]);

  const channels = Object.entries(deal.channel_credits).sort((a, b) => b[1] - a[1]);
  const maxCredit = channels[0]?.[1] ?? 1;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <div
        className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-xl max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-start justify-between gap-3">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 flex-wrap">
                <h2 className="text-slate-100 font-bold text-lg truncate">{deal.deal_name}</h2>
                {deal.is_high_value && (
                  <span className="px-1.5 py-0.5 bg-amber-900/50 text-amber-300 border border-amber-700/50 rounded text-xs font-medium">
                    High Value
                  </span>
                )}
              </div>
              <p className="text-slate-400 text-sm mt-0.5">{deal.account_name} · {fmtLabel(deal.segment)}</p>
            </div>
            <button onClick={onClose} className="text-slate-500 hover:text-slate-300 text-xl leading-none flex-shrink-0">✕</button>
          </div>
          <div className="flex items-center gap-3 mt-3 flex-wrap">
            <span className={`px-2 py-0.5 rounded text-xs font-medium ${modelBadge(deal.attribution_model)}`}>
              {fmtLabel(deal.attribution_model)}
            </span>
            <span className={`px-2 py-0.5 rounded text-xs font-medium ${actionBadge(deal.optimization_action)}`}>
              {fmtLabel(deal.optimization_action)}
            </span>
            <span className={`text-xs font-medium ${riskColor(deal.revenue_risk)}`}>
              Risk: {fmtLabel(deal.revenue_risk)}
            </span>
          </div>
        </div>

        {/* KPIs */}
        <div className="grid grid-cols-3 gap-px bg-slate-800 border-b border-slate-800">
          {[
            ["Revenue", fmtMoney(deal.attributed_revenue)],
            ["Efficiency", `${deal.attribution_efficiency}%`],
            ["CPA", fmtMoney(deal.cost_per_acquisition)],
          ].map(([label, val]) => (
            <div key={label} className="bg-slate-900 px-4 py-3 text-center">
              <div className="text-slate-400 text-xs">{label}</div>
              <div className="text-slate-100 font-bold text-base">{val}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-800">
          {(["channels", "roi", "metrics"] as const).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className={`flex-1 py-2.5 text-sm font-medium transition-colors ${
                tab === t
                  ? "text-indigo-400 border-b-2 border-indigo-500"
                  : "text-slate-500 hover:text-slate-300"
              }`}
            >
              {t === "channels" ? "Channel Credits" : t === "roi" ? "ROI by Channel" : "Metrics"}
            </button>
          ))}
        </div>

        <div className="p-5 space-y-3">
          {tab === "channels" && (
            <>
              <p className="text-slate-400 text-xs mb-3">
                Attribution model: <span className="text-slate-200 font-medium">{fmtLabel(deal.attribution_model)}</span>
                {" · "}{deal.total_touchpoints} touchpoints
              </p>
              {channels.map(([ch, credit]) => (
                <div key={ch} className="space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-300 font-medium">{fmtLabel(ch)}</span>
                    <span className="text-indigo-300 font-bold">{fmtMoney(credit)}</span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-indigo-500 rounded-full transition-all"
                      style={{ width: `${(credit / maxCredit) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </>
          )}

          {tab === "roi" && (
            <>
              <p className="text-slate-400 text-xs mb-3">Return on investment per channel</p>
              {Object.entries(deal.roi_by_channel)
                .sort((a, b) => b[1] - a[1])
                .map(([ch, roi]) => (
                  <div key={ch} className="flex items-center justify-between py-2 border-b border-slate-800/60 last:border-0">
                    <span className="text-slate-300 text-sm">{fmtLabel(ch)}</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${roi >= 5 ? "bg-emerald-500" : roi >= 2 ? "bg-amber-500" : "bg-red-500"}`}
                          style={{ width: `${Math.min(100, (roi / 20) * 100)}%` }}
                        />
                      </div>
                      <span className={`text-sm font-bold w-12 text-right ${roi >= 5 ? "text-emerald-400" : roi >= 2 ? "text-amber-400" : "text-red-400"}`}>
                        {roi}x
                      </span>
                    </div>
                  </div>
                ))}
            </>
          )}

          {tab === "metrics" && (
            <div className="grid grid-cols-2 gap-3">
              {[
                ["Pipeline Created", fmtMoney(deal.pipeline_created)],
                ["Won Value", fmtMoney(deal.closed_won_value)],
                ["Lost Value", fmtMoney(deal.closed_lost_value)],
                ["P→R Ratio", deal.pipeline_to_revenue_ratio.toFixed(3)],
                ["Cycle Efficiency", `${deal.cycle_efficiency}%`],
                ["Segment", fmtLabel(deal.segment)],
                ["Industry", fmtLabel(deal.industry)],
                ["Top Channel", fmtLabel(deal.top_channel)],
              ].map(([label, val]) => (
                <div key={label} className="bg-slate-800/50 rounded-lg p-3">
                  <div className="text-slate-500 text-xs mb-1">{label}</div>
                  <div className="text-slate-100 font-semibold text-sm">{val}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ── Deal Card ─────────────────────────────────────────────────────────────────

function DealCard({ deal, onClick }: { deal: Deal; onClick: () => void }) {
  const channels = Object.entries(deal.channel_credits).sort((a, b) => b[1] - a[1]);

  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-xl border transition-all hover:border-indigo-500/50 hover:bg-slate-800/80 ${riskBg(deal.revenue_risk)}`}
    >
      <div className="flex items-start gap-3">
        <AttributionRing efficiency={deal.attribution_efficiency} size={52} />
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-0.5">
            <span className="text-slate-100 font-semibold text-sm truncate">{deal.deal_name}</span>
            {deal.is_high_value && (
              <span className="px-1.5 py-0.5 bg-amber-900/50 text-amber-300 border border-amber-700/50 rounded text-[10px] font-medium">
                HV
              </span>
            )}
          </div>
          <p className="text-slate-400 text-xs truncate">{deal.account_name}</p>
          <div className="flex items-center gap-2 mt-1.5 flex-wrap">
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${modelBadge(deal.attribution_model)}`}>
              {fmtLabel(deal.attribution_model)}
            </span>
            <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${actionBadge(deal.optimization_action)}`}>
              {fmtLabel(deal.optimization_action)}
            </span>
          </div>
        </div>
        <div className="text-right flex-shrink-0">
          <div className="text-indigo-300 font-bold text-sm">{fmtMoney(deal.attributed_revenue)}</div>
          <div className={`text-xs mt-0.5 ${riskColor(deal.revenue_risk)}`}>{fmtLabel(deal.revenue_risk)} risk</div>
        </div>
      </div>

      {channels.length > 0 && (
        <div className="mt-3">
          <div className="flex h-1.5 rounded-full overflow-hidden gap-px">
            {channels.map(([ch, credit]) => (
              <div
                key={ch}
                className="bg-indigo-500 opacity-60 hover:opacity-100 transition-opacity"
                style={{ width: `${(credit / deal.attributed_revenue) * 100}%` }}
                title={`${fmtLabel(ch)}: ${fmtMoney(credit)}`}
              />
            ))}
          </div>
          <p className="text-slate-500 text-[10px] mt-1">Top: {fmtLabel(deal.top_channel)} · ROI {deal.roi_by_channel[deal.top_channel] ?? "—"}x</p>
        </div>
      )}
    </button>
  );
}

// ── Page ──────────────────────────────────────────────────────────────────────

export default function RevenueAttributionPage() {
  const [data, setData]         = useState<{ deals: Deal[]; summary: Summary } | null>(null);
  const [loading, setLoading]   = useState(true);
  const [modelFilter, setModelFilter] = useState("");
  const [riskFilter, setRiskFilter]   = useState("");
  const [actionFilter, setActionFilter] = useState("");
  const [selected, setSelected] = useState<Deal | null>(null);

  async function load() {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (modelFilter)  params.set("model", modelFilter);
        if (riskFilter)   params.set("risk", riskFilter);
        if (actionFilter) params.set("action", actionFilter);
        const res = await fetch(`/api/revenue-attribution?${params}`);
        if (res.ok) setData(await res.json());
      } finally {
        setLoading(false);
      }
  }

  useEffect(() => {
    load();
  }, [modelFilter, riskFilter, actionFilter]);

  const s = data?.summary;
  const deals = data?.deals ?? [];

  const models   = ["first_touch", "last_touch", "linear", "time_decay", "position_based"];
  const risks    = ["low", "medium", "high", "critical"];
  const actions  = ["scale_up", "maintain", "optimize", "reduce", "reallocate"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Revenue Attribution</h1>
          <p className="text-slate-400 text-sm mt-1">Multi-touch attribution engine — channel ROI & optimization</p>
        </div>
        <button
          onClick={load}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-sm font-medium transition-colors"
        >
          Refresh
        </button>
      </div>

      {/* KPI Strip */}
      {s && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: "Total Revenue",   value: fmtMoney(s.total_attributed_revenue), sub: `${s.total} deals` },
            { label: "Avg Efficiency",  value: `${s.avg_attribution_efficiency}%`,   sub: `${s.scale_up_count} scale-up` },
            { label: "High Value",      value: String(s.high_value_count),            sub: "deals" },
            { label: "High Risk",       value: String(s.high_risk_count),             sub: "needs action" },
          ].map(({ label, value, sub }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="text-slate-400 text-xs">{label}</div>
              <div className="text-slate-100 font-bold text-xl mt-1">{value}</div>
              <div className="text-slate-500 text-xs mt-0.5">{sub}</div>
            </div>
          ))}
        </div>
      )}

      {/* Model Distribution */}
      {s && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h2 className="text-slate-300 text-sm font-semibold mb-3">Attribution Model Distribution</h2>
          <ModelDistBar counts={s.model_counts} />
        </div>
      )}

      {/* Filters */}
      <div className="flex gap-2 flex-wrap">
        {/* Model filter */}
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1">
          <span className="text-slate-500 text-xs">Model:</span>
          <div className="flex gap-1">
            {["", ...models].map((m) => (
              <button
                key={m}
                onClick={() => setModelFilter(m)}
                className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${
                  modelFilter === m
                    ? "bg-indigo-600 text-white"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {m ? fmtLabel(m) : "All"}
              </button>
            ))}
          </div>
        </div>

        {/* Risk filter */}
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1">
          <span className="text-slate-500 text-xs">Risk:</span>
          <div className="flex gap-1">
            {["", ...risks].map((r) => (
              <button
                key={r}
                onClick={() => setRiskFilter(r)}
                className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${
                  riskFilter === r
                    ? "bg-indigo-600 text-white"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {r ? fmtLabel(r) : "All"}
              </button>
            ))}
          </div>
        </div>

        {/* Action filter */}
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-lg px-2 py-1">
          <span className="text-slate-500 text-xs">Action:</span>
          <div className="flex gap-1">
            {["", ...actions].map((a) => (
              <button
                key={a}
                onClick={() => setActionFilter(a)}
                className={`px-2 py-0.5 rounded text-xs font-medium transition-colors ${
                  actionFilter === a
                    ? "bg-indigo-600 text-white"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {a ? fmtLabel(a) : "All"}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Deal Cards */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <div className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {deals.map((deal) => (
            <DealCard key={deal.deal_id} deal={deal} onClick={() => setSelected(deal)} />
          ))}
          {deals.length === 0 && (
            <div className="col-span-full text-center py-12 text-slate-500">
              No deals match the selected filters.
            </div>
          )}
        </div>
      )}

      {/* Channel Summary */}
      {s && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
          <h2 className="text-slate-300 text-sm font-semibold mb-3">Top Channel Distribution</h2>
          <div className="flex flex-wrap gap-2">
            {Object.entries(s.top_channel_counts)
              .sort((a, b) => b[1] - a[1])
              .map(([ch, count]) => (
                <div key={ch} className="bg-slate-800 rounded-lg px-3 py-2 flex items-center gap-2">
                  <span className="text-slate-300 text-sm font-medium">{fmtLabel(ch)}</span>
                  <span className="bg-indigo-900/50 text-indigo-300 text-xs font-bold px-1.5 py-0.5 rounded">{count}</span>
                </div>
              ))}
          </div>
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-slate-800/50 rounded-lg p-3">
              <div className="text-slate-500 text-xs">Avg P→R Ratio</div>
              <div className="text-slate-100 font-bold text-sm mt-1">{s.avg_pipeline_to_revenue_ratio.toFixed(3)}</div>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3">
              <div className="text-slate-500 text-xs">Avg Cycle Efficiency</div>
              <div className="text-slate-100 font-bold text-sm mt-1">{s.avg_cycle_efficiency}%</div>
            </div>
            <div className="bg-slate-800/50 rounded-lg p-3">
              <div className="text-slate-500 text-xs">Avg CPA</div>
              <div className="text-slate-100 font-bold text-sm mt-1">{fmtMoney(s.avg_cost_per_acquisition)}</div>
            </div>
          </div>
        </div>
      )}

      {/* Modal */}
      {selected && <DealModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
