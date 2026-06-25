"use client";

import { useState, useEffect, useRef } from "react";

interface DealData {
  deal_id: string;
  deal_name: string;
  rep_id: string;
  contamination_level: string;
  contamination_risk: string;
  primary_contamination_type: string;
  contamination_action: string;
  ethics_score: number;
  compliance_score: number;
  financial_integrity_score: number;
  audit_quality_score: number;
  contamination_composite: number;
  requires_legal_review: boolean;
  requires_escalation: boolean;
  estimated_compliance_exposure_usd: number;
  contamination_signal: string;
  deal_value_usd: number;
}

interface Summary {
  total: number;
  level_counts: Record<string, number>;
  risk_counts: Record<string, number>;
  type_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_contamination_composite: number;
  legal_review_required_count: number;
  escalation_required_count: number;
  avg_ethics_score: number;
  avg_compliance_score: number;
  avg_financial_integrity_score: number;
  avg_audit_quality_score: number;
  total_compliance_exposure_usd: number;
}

const LEVEL_BG: Record<string, string> = {
  clean:           "bg-emerald-500/20 border-emerald-500/30 text-emerald-300",
  advisory:        "bg-amber-500/20 border-amber-500/30 text-amber-300",
  review_required: "bg-orange-500/20 border-orange-500/30 text-orange-300",
  blocked:         "bg-rose-500/20 border-rose-500/30 text-rose-300",
};
const LEVEL_COLOR: Record<string, string> = {
  clean:           "#34d399",
  advisory:        "#fbbf24",
  review_required: "#f97316",
  blocked:         "#f87171",
};
const RISK_BG: Record<string, string> = {
  low:      "bg-emerald-500/15 text-emerald-300",
  moderate: "bg-amber-500/15 text-amber-300",
  high:     "bg-orange-500/15 text-orange-300",
  critical: "bg-rose-500/15 text-rose-300",
};
const TYPE_BG: Record<string, string> = {
  none:                   "bg-slate-700/50 text-slate-400",
  conflict_of_interest:   "bg-rose-500/15 text-rose-300",
  compliance_gap:         "bg-amber-500/15 text-amber-300",
  channel_conflict:       "bg-violet-500/15 text-violet-300",
  financial_irregularity: "bg-orange-500/15 text-orange-300",
};

function fmt(n: number) {
  return n >= 1_000_000
    ? `$${(n / 1_000_000).toFixed(1)}M`
    : n >= 1_000
    ? `$${(n / 1_000).toFixed(0)}K`
    : `$${n}`;
}

function ContaminationMeter({ value, color }: { value: number; color: string }) {
  const size = 72;
  const r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const fill = (value / 100) * circ;
  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth={size * 0.1} />
      <circle
        cx={size / 2} cy={size / 2} r={r} fill="none"
        stroke={color} strokeWidth={size * 0.1}
        strokeDasharray={`${fill} ${circ - fill}`}
        strokeLinecap="round"
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
      />
      <text x={size / 2} y={size / 2 + 5} textAnchor="middle" fill={color} fontSize={size * 0.18} fontWeight="bold">
        {value.toFixed(0)}
      </text>
    </svg>
  );
}

function SmallRing({ value, color, label }: { value: number; color: string; label: string }) {
  const size = 64;
  const r = size * 0.38;
  const circ = 2 * Math.PI * r;
  const fill = (value / 100) * circ;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth={size * 0.1} />
        <circle
          cx={size / 2} cy={size / 2} r={r} fill="none"
          stroke={color} strokeWidth={size * 0.1}
          strokeDasharray={`${fill} ${circ - fill}`}
          strokeLinecap="round"
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
        <text x={size / 2} y={size / 2 + 4} textAnchor="middle" fill={color} fontSize={size * 0.2} fontWeight="bold">
          {value.toFixed(0)}
        </text>
      </svg>
      <span className="text-slate-500 text-xs text-center leading-tight">{label}</span>
    </div>
  );
}

function DetailModal({ deal, onClose }: { deal: DealData; onClose: () => void }) {
  const [tab, setTab] = useState(0);
  const backdrop = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose]);

  const color = LEVEL_COLOR[deal.contamination_level] ?? "#94a3b8";

  return (
    <div
      ref={backdrop}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      onClick={(e) => { if (e.target === backdrop.current) onClose(); }}
    >
      <div className="relative w-full max-w-2xl rounded-2xl border border-slate-700 bg-slate-900 shadow-2xl mx-4">
        <button onClick={onClose} className="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors text-xl font-bold">✕</button>

        <div className="p-6 border-b border-slate-800">
          <div className="flex items-center gap-4">
            <ContaminationMeter value={deal.contamination_composite} color={color} />
            <div>
              <h2 className="text-xl font-bold text-slate-100">{deal.deal_name}</h2>
              <p className="text-slate-400 text-sm mt-0.5">{fmt(deal.deal_value_usd)} · Rep {deal.rep_id}</p>
              <div className="flex gap-2 mt-2 flex-wrap">
                <span className={`px-2 py-0.5 rounded-full border text-xs font-semibold uppercase tracking-wide ${LEVEL_BG[deal.contamination_level]}`}>
                  {deal.contamination_level.replace("_", " ")}
                </span>
                <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${TYPE_BG[deal.primary_contamination_type]}`}>
                  {deal.primary_contamination_type.replace(/_/g, " ")}
                </span>
              </div>
              {(deal.requires_legal_review || deal.requires_escalation) && (
                <div className="flex gap-2 mt-2">
                  {deal.requires_legal_review && (
                    <span className="px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 text-xs font-semibold">LEGAL REVIEW</span>
                  )}
                  {deal.requires_escalation && (
                    <span className="px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 text-xs font-semibold">ESCALATE</span>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="flex border-b border-slate-800">
          {["Risk Scores", "Exposure Analysis", "Action"].map((t, i) => (
            <button
              key={t} onClick={() => setTab(i)}
              className={`flex-1 px-4 py-3 text-sm font-medium transition-colors ${tab === i ? "text-indigo-400 border-b-2 border-indigo-400" : "text-slate-500 hover:text-slate-300"}`}
            >{t}</button>
          ))}
        </div>

        <div className="p-6">
          {tab === 0 && (
            <div className="space-y-4">
              <div className="grid grid-cols-4 gap-3">
                <SmallRing value={deal.ethics_score} color="#f87171" label="Ethics Risk" />
                <SmallRing value={deal.compliance_score} color="#fbbf24" label="Compliance Risk" />
                <SmallRing value={deal.financial_integrity_score} color="#f97316" label="Financial Risk" />
                <SmallRing value={deal.audit_quality_score} color="#c084fc" label="Audit Risk" />
              </div>
              <div className="bg-slate-800/30 rounded-xl p-4">
                <p className="text-slate-400 text-xs mb-1">Contamination Signal</p>
                <p className="text-slate-200 text-sm">{deal.contamination_signal}</p>
              </div>
            </div>
          )}
          {tab === 1 && (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-slate-800/50 rounded-xl p-4">
                  <p className="text-slate-400 text-xs mb-1">Deal Value</p>
                  <p className="text-slate-100 text-lg font-bold">{fmt(deal.deal_value_usd)}</p>
                </div>
                <div className="bg-slate-800/50 rounded-xl p-4">
                  <p className="text-slate-400 text-xs mb-1">Compliance Exposure</p>
                  <p className="text-rose-400 text-lg font-bold">{fmt(deal.estimated_compliance_exposure_usd)}</p>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className={`rounded-xl p-3 text-center ${RISK_BG[deal.contamination_risk]}`}>
                  <p className="text-xs opacity-70 mb-1">Risk Level</p>
                  <p className="text-sm font-bold uppercase">{deal.contamination_risk}</p>
                </div>
                <div className="rounded-xl p-3 text-center bg-slate-800/50">
                  <p className="text-xs text-slate-400 mb-1">Composite Score</p>
                  <p className="text-sm font-bold" style={{ color }}>{deal.contamination_composite.toFixed(1)}</p>
                </div>
              </div>
            </div>
          )}
          {tab === 2 && (
            <div className="space-y-4">
              <div className="bg-indigo-500/10 border border-indigo-500/20 rounded-xl p-4">
                <p className="text-indigo-400 text-xs font-semibold uppercase tracking-wide mb-2">Required Action</p>
                <p className="text-slate-200 font-semibold text-base">
                  {deal.contamination_action.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}
                </p>
              </div>
              <div className="bg-slate-800/30 rounded-xl p-4 space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Legal Review Required</span>
                  <span className={deal.requires_legal_review ? "text-rose-400 font-semibold" : "text-slate-500"}>
                    {deal.requires_legal_review ? "YES" : "No"}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Escalation Required</span>
                  <span className={deal.requires_escalation ? "text-amber-400 font-semibold" : "text-slate-500"}>
                    {deal.requires_escalation ? "YES" : "No"}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-slate-400">Contamination Type</span>
                  <span className="text-slate-200 font-semibold">{deal.primary_contamination_type.replace(/_/g, " ")}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function DealContaminationPage() {
  const [data, setData] = useState<{ deals: DealData[]; summary: Summary } | null>(null);
  const [loading, setLoading] = useState(true);
  const [levelFilter, setLevelFilter] = useState<string>("all");
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const [selected, setSelected] = useState<DealData | null>(null);

  async function load() {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (levelFilter !== "all") params.set("level", levelFilter);
        if (riskFilter !== "all")  params.set("risk", riskFilter);
        const res = await fetch(`/api/deal-contamination-risk-engine?${params}`);
        setData(await res.json());
      } finally {
        setLoading(false);
      }
  }

  useEffect(() => {
    load();
  }, [levelFilter, riskFilter]);

  const s = data?.summary;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">

        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-slate-100">Deal Contamination Risk Engine</h1>
            <p className="text-slate-400 mt-1">Detect conflict of interest, compliance gaps, and financial irregularities</p>
          </div>
          <button onClick={load} className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium transition-colors">
            Refresh
          </button>
        </div>

        {s && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { label: "Avg Contamination Score", value: s.avg_contamination_composite.toFixed(1), sub: "composite", color: "text-rose-400" },
              { label: "Legal Review Required", value: s.legal_review_required_count, sub: `of ${s.total} deals`, color: "text-rose-400" },
              { label: "Escalation Required", value: s.escalation_required_count, sub: `of ${s.total} deals`, color: "text-amber-400" },
              { label: "Compliance Exposure", value: s.total_compliance_exposure_usd >= 1_000_000 ? `$${(s.total_compliance_exposure_usd / 1_000_000).toFixed(1)}M` : `$${(s.total_compliance_exposure_usd / 1000).toFixed(0)}K`, sub: "total risk", color: "text-orange-400" },
            ].map(({ label, value, sub, color }) => (
              <div key={label} className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
                <p className="text-slate-400 text-xs mb-1">{label}</p>
                <p className={`text-2xl font-bold ${color}`}>{value}</p>
                <p className="text-slate-500 text-xs mt-1">{sub}</p>
              </div>
            ))}
          </div>
        )}

        {s && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-4">Average Risk Scores (higher = more risk)</h2>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              {[
                { label: "Ethics Risk", value: s.avg_ethics_score, color: "#f87171" },
                { label: "Compliance Risk", value: s.avg_compliance_score, color: "#fbbf24" },
                { label: "Financial Risk", value: s.avg_financial_integrity_score, color: "#f97316" },
                { label: "Audit Risk", value: s.avg_audit_quality_score, color: "#c084fc" },
              ].map(({ label, value, color }) => (
                <div key={label} className="flex flex-col items-center gap-2">
                  <SmallRing value={value} color={color} label={label} />
                </div>
              ))}
            </div>
          </div>
        )}

        {s && (
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
            <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wide mb-3">Contamination Level Distribution</h2>
            <div className="flex h-5 rounded-full overflow-hidden gap-0.5">
              {(["clean", "advisory", "review_required", "blocked"] as const).map((lv) => {
                const pct = ((s.level_counts[lv] || 0) / s.total) * 100;
                const cols: Record<string, string> = { clean: "bg-emerald-500", advisory: "bg-amber-500", review_required: "bg-orange-500", blocked: "bg-rose-500" };
                return pct > 0 ? (
                  <div key={lv} style={{ width: `${pct}%` }} className={`${cols[lv]} relative group`}>
                    <div className="absolute bottom-full mb-1 left-1/2 -translate-x-1/2 bg-slate-800 text-xs rounded px-2 py-1 whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity z-10">
                      {lv.replace("_", " ")}: {s.level_counts[lv]}
                    </div>
                  </div>
                ) : null;
              })}
            </div>
            <div className="flex flex-wrap gap-3 mt-3">
              {(["clean", "advisory", "review_required", "blocked"] as const).map((lv) => {
                const dot: Record<string, string> = { clean: "bg-emerald-500", advisory: "bg-amber-500", review_required: "bg-orange-500", blocked: "bg-rose-500" };
                return (
                  <div key={lv} className="flex items-center gap-1.5">
                    <div className={`w-2.5 h-2.5 rounded-full ${dot[lv]}`} />
                    <span className="text-slate-400 text-xs">{lv.replace("_", " ")} ({s.level_counts[lv] || 0})</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        <div className="flex flex-wrap gap-3">
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1">
            {["all", "clean", "advisory", "review_required", "blocked"].map((lv) => (
              <button
                key={lv} onClick={() => setLevelFilter(lv)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${levelFilter === lv ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"}`}
              >
                {lv === "all" ? "All Levels" : lv.replace("_", " ")}
              </button>
            ))}
          </div>
          <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1">
            {["all", "low", "moderate", "high", "critical"].map((r) => (
              <button
                key={r} onClick={() => setRiskFilter(r)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${riskFilter === r ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-slate-200"}`}
              >
                {r === "all" ? "All Risk" : r}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="bg-slate-900 border border-slate-800 rounded-2xl p-5 animate-pulse h-52" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {(data?.deals ?? []).map((deal) => {
              const color = LEVEL_COLOR[deal.contamination_level] ?? "#94a3b8";
              const size = 52;
              const r = size * 0.38;
              const circ = 2 * Math.PI * r;
              const fill = (deal.contamination_composite / 100) * circ;
              return (
                <button
                  key={deal.deal_id}
                  onClick={() => setSelected(deal)}
                  className="bg-slate-900 border border-slate-800 rounded-2xl p-5 text-left hover:border-indigo-500/50 transition-all hover:bg-slate-800/50 group"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex-1 min-w-0 mr-3">
                      <p className="text-slate-100 font-semibold text-sm truncate">{deal.deal_name}</p>
                      <p className="text-slate-400 text-xs">{fmt(deal.deal_value_usd)}</p>
                    </div>
                    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="flex-shrink-0">
                      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="#1e293b" strokeWidth={size * 0.1} />
                      <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke={color} strokeWidth={size * 0.1}
                        strokeDasharray={`${fill} ${circ - fill}`} strokeLinecap="round"
                        transform={`rotate(-90 ${size / 2} ${size / 2})`} />
                      <text x={size / 2} y={size / 2 + 4} textAnchor="middle" fill={color} fontSize={size * 0.2} fontWeight="bold">
                        {deal.contamination_composite.toFixed(0)}
                      </text>
                    </svg>
                  </div>
                  <div className="flex flex-wrap gap-1.5 mb-3">
                    <span className={`px-2 py-0.5 rounded-full border text-xs font-semibold ${LEVEL_BG[deal.contamination_level]}`}>
                      {deal.contamination_level.replace("_", " ")}
                    </span>
                    <span className={`px-2 py-0.5 rounded-full text-xs font-semibold ${RISK_BG[deal.contamination_risk]}`}>
                      {deal.contamination_risk}
                    </span>
                  </div>
                  {(deal.requires_legal_review || deal.requires_escalation) && (
                    <div className="flex gap-1 mb-2 flex-wrap">
                      {deal.requires_legal_review && <span className="px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 text-xs">Legal</span>}
                      {deal.requires_escalation && <span className="px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 text-xs">Escalate</span>}
                    </div>
                  )}
                  {deal.estimated_compliance_exposure_usd > 0 && (
                    <p className="text-rose-400 text-xs font-semibold mb-1">Exposure: {fmt(deal.estimated_compliance_exposure_usd)}</p>
                  )}
                  <p className="text-slate-500 text-xs line-clamp-2 group-hover:text-slate-400 transition-colors">
                    {deal.contamination_signal}
                  </p>
                </button>
              );
            })}
          </div>
        )}
      </div>

      {selected && <DetailModal deal={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
