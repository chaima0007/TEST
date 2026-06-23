"use client";

import { useEffect, useState } from "react";

interface RepConcentration {
  rep_id: string;
  region: string;
  concentration_risk: string;
  concentration_pattern: string;
  concentration_severity: string;
  recommended_action: string;
  deal_concentration_score: number;
  account_concentration_score: number;
  product_concentration_score: number;
  stage_concentration_score: number;
  concentration_composite: number;
  is_fragile_pipeline: boolean;
  requires_rebalancing: boolean;
  estimated_at_risk_revenue_usd: number;
  concentration_signal: string;
}

interface Summary {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_concentration_composite: number;
  fragile_pipeline_count: number;
  rebalancing_count: number;
  avg_deal_concentration_score: number;
  avg_account_concentration_score: number;
  avg_product_concentration_score: number;
  avg_stage_concentration_score: number;
  total_estimated_at_risk_revenue_usd: number;
}

const RISK_COLORS: Record<string, string> = {
  low:      "text-emerald-400",
  moderate: "text-yellow-400",
  high:     "text-orange-400",
  critical: "text-red-400",
};

const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-400/10 border-emerald-400/30",
  moderate: "bg-yellow-400/10 border-yellow-400/30",
  high:     "bg-orange-400/10 border-orange-400/30",
  critical: "bg-red-400/10 border-red-400/30",
};

const SEV_COLORS: Record<string, string> = {
  diversified:  "text-emerald-400",
  watch:        "text-yellow-400",
  concentrated: "text-orange-400",
  critical:     "text-red-400",
};

const ACTION_COLORS: Record<string, string> = {
  no_action:                "text-slate-400",
  pipeline_diversification: "text-sky-400",
  rep_rebalancing:          "text-yellow-400",
  forecast_risk_flag:       "text-orange-400",
  executive_review:         "text-red-400",
};

function fmt(s: string) {
  return s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function fmtUSD(v: number) {
  if (v >= 1_000_000) return `$${(v / 1_000_000).toFixed(1)}M`;
  if (v >= 1_000)     return `$${(v / 1_000).toFixed(0)}K`;
  return `$${v.toFixed(0)}`;
}

function RingGauge({ value, color }: { value: number; color: string }) {
  const r = 28, cx = 36, cy = 36;
  const circ = 2 * Math.PI * r;
  const dash = Math.min(value / 100, 1) * circ;
  return (
    <svg width={72} height={72} className="rotate-[-90deg]">
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#1e293b" strokeWidth={8} />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={color} strokeWidth={8}
        strokeDasharray={`${dash} ${circ}`} strokeLinecap="round" />
    </svg>
  );
}

function ScoreBar({ label, value }: { label: string; value: number }) {
  const pct = Math.min(value, 100);
  const color = value >= 60 ? "bg-red-500" : value >= 40 ? "bg-orange-500" : value >= 20 ? "bg-yellow-500" : "bg-emerald-500";
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs text-slate-400">
        <span>{label}</span><span className="text-slate-300">{value.toFixed(1)}</span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full transition-all ${color}`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

function DetailModal({ rep, onClose }: { rep: RepConcentration; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  const riskColor = RISK_COLORS[rep.concentration_risk] || "text-slate-400";
  const composite = rep.concentration_composite;
  const gaugeColor = composite >= 60 ? "#f87171" : composite >= 40 ? "#fb923c" : composite >= 20 ? "#facc15" : "#34d399";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={onClose}>
      <div className="relative w-full max-w-2xl mx-4 bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl"
        onClick={(e) => e.stopPropagation()}>
        <div className="flex items-start justify-between p-6 border-b border-slate-800">
          <div>
            <h2 className="text-lg font-bold text-slate-100">{rep.rep_id}</h2>
            <p className="text-sm text-slate-400 mt-0.5">{rep.region} · {fmt(rep.concentration_pattern)}</p>
          </div>
          <div className="text-right">
            <span className={`text-sm font-semibold ${riskColor}`}>{fmt(rep.concentration_risk)} Risk</span>
            <p className={`text-xs mt-0.5 ${SEV_COLORS[rep.concentration_severity] || "text-slate-400"}`}>{fmt(rep.concentration_severity)}</p>
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {["Overview", "Scores", "Action"].map((t, i) => (
            <button key={t} onClick={() => setTab(i)}
              className={`flex-1 py-2.5 text-sm font-medium transition-colors ${tab === i ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"}`}>
              {t}
            </button>
          ))}
        </div>

        <div className="p-6 space-y-4 max-h-[60vh] overflow-y-auto">
          {tab === 0 && (
            <>
              <div className="flex items-center gap-6">
                <div className="relative flex-shrink-0">
                  <RingGauge value={composite} color={gaugeColor} />
                  <span className="absolute inset-0 flex items-center justify-center text-xs font-bold text-slate-200">
                    {composite.toFixed(1)}
                  </span>
                </div>
                <div className="flex-1 space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Revenue at Risk</span>
                    <span className="text-slate-200 font-medium">{fmtUSD(rep.estimated_at_risk_revenue_usd)}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Fragile Pipeline</span>
                    <span className={rep.is_fragile_pipeline ? "text-red-400" : "text-emerald-400"}>{rep.is_fragile_pipeline ? "Yes" : "No"}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-slate-400">Needs Rebalancing</span>
                    <span className={rep.requires_rebalancing ? "text-orange-400" : "text-emerald-400"}>{rep.requires_rebalancing ? "Yes" : "No"}</span>
                  </div>
                </div>
              </div>
              <div className={`rounded-lg border p-3 ${RISK_BG[rep.concentration_risk] || "bg-slate-800/50 border-slate-700"}`}>
                <p className="text-xs text-slate-300">{rep.concentration_signal}</p>
              </div>
            </>
          )}
          {tab === 1 && (
            <div className="space-y-3">
              <ScoreBar label="Deal Concentration"    value={rep.deal_concentration_score} />
              <ScoreBar label="Account Concentration" value={rep.account_concentration_score} />
              <ScoreBar label="Product Concentration" value={rep.product_concentration_score} />
              <ScoreBar label="Stage Concentration"   value={rep.stage_concentration_score} />
              <div className="pt-2 border-t border-slate-800">
                <ScoreBar label="Concentration Composite" value={rep.concentration_composite} />
              </div>
            </div>
          )}
          {tab === 2 && (
            <div className="space-y-4">
              <div>
                <p className="text-xs text-slate-500 mb-1">Recommended Action</p>
                <span className={`text-sm font-semibold ${ACTION_COLORS[rep.recommended_action] || "text-slate-400"}`}>{fmt(rep.recommended_action)}</span>
              </div>
              <div>
                <p className="text-xs text-slate-500 mb-1">Concentration Pattern</p>
                <span className="text-sm text-slate-200">{fmt(rep.concentration_pattern)}</span>
              </div>
              <div>
                <p className="text-xs text-slate-500 mb-1">Severity</p>
                <span className={`text-sm font-medium ${SEV_COLORS[rep.concentration_severity] || "text-slate-400"}`}>{fmt(rep.concentration_severity)}</span>
              </div>
            </div>
          )}
        </div>

        <div className="flex justify-end p-4 border-t border-slate-800">
          <button onClick={onClose}
            className="px-4 py-2 text-sm text-slate-400 hover:text-slate-200 transition-colors">Close</button>
        </div>
      </div>
    </div>
  );
}

export default function PipelineConcentrationPage() {
  const [data, setData] = useState<{ reps: RepConcentration[]; summary: Summary } | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");
  const [selected, setSelected] = useState<RepConcentration | null>(null);

  useEffect(() => {
    async function load() {
        const params = new URLSearchParams();
        if (riskFilter !== "all") params.set("risk", riskFilter);
        const res = await fetch(`/api/sales-pipeline-concentration-risk-engine?${params}`);
        if (res.ok) setData(await res.json());
  }
    load();
  }, [riskFilter]);

  const summary = data?.summary;
  const reps = data?.reps ?? [];

  const kpis = summary ? [
    { label: "Total Reps",        value: summary.total,                                   sub: "evaluated" },
    { label: "Fragile Pipelines", value: summary.fragile_pipeline_count,                  sub: "single-point risk" },
    { label: "Need Rebalancing",  value: summary.rebalancing_count,                       sub: "diversify now" },
    { label: "Avg Composite",     value: summary.avg_concentration_composite.toFixed(1),  sub: "concentration score" },
    { label: "Revenue at Risk",   value: fmtUSD(summary.total_estimated_at_risk_revenue_usd), sub: "forecast exposure" },
  ] : [];

  const RISKS = ["all", "low", "moderate", "high", "critical"];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Pipeline Concentration Risk Engine</h1>
        <p className="text-slate-400 mt-1 text-sm">Detect over-concentrated pipelines — whale deals, single-account exposure, product silos — before fragile forecasts collapse.</p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {kpis.map((k) => (
          <div key={k.label} className="bg-slate-900 border border-slate-800 rounded-xl p-4">
            <p className="text-xs text-slate-500">{k.label}</p>
            <p className="text-2xl font-bold text-slate-100 mt-1">{k.value}</p>
            <p className="text-xs text-slate-500 mt-0.5">{k.sub}</p>
          </div>
        ))}
      </div>

      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { title: "Risk Level",   counts: summary.risk_counts,     colors: { low: "bg-emerald-500", moderate: "bg-yellow-500", high: "bg-orange-500", critical: "bg-red-500" } },
            { title: "Pattern",      counts: summary.pattern_counts,  colors: {} },
            { title: "Severity",     counts: summary.severity_counts, colors: { diversified: "bg-emerald-500", watch: "bg-yellow-500", concentrated: "bg-orange-500", critical: "bg-red-500" } },
            { title: "Action",       counts: summary.action_counts,   colors: {} },
          ].map(({ title, counts, colors }) => (
            <div key={title} className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-3">
              <h3 className="text-sm font-semibold text-slate-300">{title}</h3>
              {Object.entries(counts).map(([k, v]) => {
                const pct = summary.total > 0 ? (v / summary.total) * 100 : 0;
                const col = (colors as Record<string, string>)[k] ?? "bg-violet-500";
                return (
                  <div key={k} className="space-y-1">
                    <div className="flex justify-between text-xs text-slate-400">
                      <span>{fmt(k)}</span><span>{v}</span>
                    </div>
                    <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                      <div className={`h-full rounded-full ${col}`} style={{ width: `${pct}%` }} />
                    </div>
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      )}

      {summary && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-3">
          <h3 className="text-sm font-semibold text-slate-300">Average Sub-Scores</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <ScoreBar label="Deal Concentration"    value={summary.avg_deal_concentration_score} />
            <ScoreBar label="Account Concentration" value={summary.avg_account_concentration_score} />
            <ScoreBar label="Product Concentration" value={summary.avg_product_concentration_score} />
            <ScoreBar label="Stage Concentration"   value={summary.avg_stage_concentration_score} />
          </div>
        </div>
      )}

      <div className="flex flex-wrap gap-2">
        {RISKS.map((r) => (
          <button key={r} onClick={() => setRiskFilter(r)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border transition-colors ${
              riskFilter === r
                ? "bg-indigo-600 border-indigo-500 text-white"
                : "bg-slate-900 border-slate-700 text-slate-400 hover:border-slate-500"
            }`}>
            {fmt(r)}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {reps.map((rep) => {
          const col = RISK_COLORS[rep.concentration_risk] || "text-slate-400";
          const bg  = RISK_BG[rep.concentration_risk]     || "bg-slate-800/50 border-slate-700";
          const gaugeColor = rep.concentration_composite >= 60 ? "#f87171" : rep.concentration_composite >= 40 ? "#fb923c" : rep.concentration_composite >= 20 ? "#facc15" : "#34d399";
          return (
            <button key={rep.rep_id} onClick={() => setSelected(rep)} className="text-left w-full">
              <div className={`rounded-xl border p-4 space-y-3 hover:border-indigo-500/50 transition-colors ${bg}`}>
                <div className="flex items-start justify-between">
                  <div>
                    <p className="font-semibold text-slate-100 text-sm">{rep.rep_id}</p>
                    <p className="text-xs text-slate-400">{rep.region}</p>
                  </div>
                  <div className="text-right">
                    <span className={`text-xs font-bold ${col}`}>{fmt(rep.concentration_risk).toUpperCase()}</span>
                    <p className="text-xs text-slate-500 mt-0.5">{fmt(rep.concentration_severity)}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="relative flex-shrink-0">
                    <RingGauge value={rep.concentration_composite} color={gaugeColor} />
                    <span className="absolute inset-0 flex items-center justify-center text-xs font-bold text-slate-200">
                      {rep.concentration_composite.toFixed(0)}
                    </span>
                  </div>
                  <div className="flex-1 space-y-1.5 min-w-0">
                    <div className="flex justify-between text-xs text-slate-400">
                      <span>Rev at Risk</span>
                      <span className="text-slate-200">{fmtUSD(rep.estimated_at_risk_revenue_usd)}</span>
                    </div>
                    <div className="flex justify-between text-xs text-slate-400">
                      <span>Pattern</span>
                      <span className="text-slate-300 truncate ml-2">{fmt(rep.concentration_pattern)}</span>
                    </div>
                    <div className="flex justify-between text-xs text-slate-400">
                      <span>Action</span>
                      <span className={`${ACTION_COLORS[rep.recommended_action] || "text-slate-400"}`}>{fmt(rep.recommended_action)}</span>
                    </div>
                  </div>
                </div>

                <div className="flex gap-2 flex-wrap">
                  {rep.is_fragile_pipeline && (
                    <span className="px-2 py-0.5 text-xs rounded-full bg-red-500/20 text-red-400 border border-red-500/30">Fragile</span>
                  )}
                  {rep.requires_rebalancing && (
                    <span className="px-2 py-0.5 text-xs rounded-full bg-yellow-500/20 text-yellow-400 border border-yellow-500/30">Rebalance</span>
                  )}
                </div>

                <p className="text-xs text-slate-500 truncate">{rep.concentration_signal}</p>
              </div>
            </button>
          );
        })}
      </div>

      {selected && <DetailModal rep={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
