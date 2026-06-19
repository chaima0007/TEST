"use client";
import { useEffect, useState } from "react";

type Zone = {
  zone_id: string;
  ecosystem_type: string;
  region: string;
  planetary_risk: string;
  ecosystem_pattern: string;
  ecosystem_severity: string;
  recommended_action: string;
  boundary_score: number;
  biodiversity_score: number;
  degradation_score: number;
  exposure_score: number;
  planetary_risk_composite: number;
  is_tipping_point_risk: boolean;
  requires_emergency_intervention: boolean;
  estimated_planetary_risk_index: number;
  ecosystem_signal: string;
};

type Summary = {
  total: number;
  risk_counts: Record<string, number>;
  pattern_counts: Record<string, number>;
  severity_counts: Record<string, number>;
  action_counts: Record<string, number>;
  avg_planetary_risk_composite: number;
  tipping_point_risk_count: number;
  emergency_intervention_count: number;
  avg_boundary_score: number;
  avg_biodiversity_score: number;
  avg_degradation_score: number;
  avg_exposure_score: number;
  avg_estimated_planetary_risk_index: number;
};

const RISK_COLORS: Record<string, string> = {
  low:      "#10b981",
  moderate: "#f59e0b",
  high:     "#f97316",
  critical: "#ef4444",
};
const PAT_COLORS: Record<string, string> = {
  none:                    "#10b981",
  tipping_point_breach:    "#ef4444",
  biodiversity_collapse:   "#dc2626",
  carbon_crisis:           "#a855f7",
  water_system_failure:    "#3b82f6",
  ecosystem_fragmentation: "#f97316",
};
const SEV_COLORS: Record<string, string> = {
  thriving:       "#10b981",
  degrading:      "#f59e0b",
  critical_stress:"#f97316",
  collapsed:      "#ef4444",
};
const ACT_COLORS: Record<string, string> = {
  no_action:                  "#10b981",
  ecosystem_monitoring:       "#06b6d4",
  nature_positive_program:    "#3b82f6",
  carbon_emergency:           "#a855f7",
  tipping_point_intervention: "#f97316",
  ecosystem_emergency:        "#ef4444",
};

const RISK_BADGE: Record<string, string> = {
  low:      "bg-emerald-900 text-emerald-300",
  moderate: "bg-amber-900 text-amber-300",
  high:     "bg-orange-900 text-orange-300",
  critical: "bg-red-900 text-red-300",
};
const SEV_BADGE: Record<string, string> = {
  thriving:       "bg-emerald-900 text-emerald-300",
  degrading:      "bg-amber-900 text-amber-300",
  critical_stress:"bg-orange-900 text-orange-300",
  collapsed:      "bg-red-900 text-red-300",
};

function GaugeRing({ value, label, color }: { value: number; label: string; color: string }) {
  const r = 36;
  const circ = 2 * Math.PI * r;
  const fill = circ * (1 - value / 100);
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="88" height="88" viewBox="0 0 88 88">
        <circle cx="44" cy="44" r={r} fill="none" stroke="#1e293b" strokeWidth="8" />
        <circle cx="44" cy="44" r={r} fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circ} strokeDashoffset={fill}
          strokeLinecap="round" transform="rotate(-90 44 44)" />
        <text x="44" y="49" textAnchor="middle" fill="white" fontSize="13" fontWeight="bold">
          {Math.round(value)}
        </text>
      </svg>
      <span className="text-xs text-slate-400 text-center">{label}</span>
    </div>
  );
}

function DistBar({ title, counts, colors }: { title: string; counts: Record<string, number>; colors: Record<string, string> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1;
  return (
    <div className="flex flex-col gap-1">
      <span className="text-xs text-slate-400 font-medium">{title}</span>
      <div className="flex h-3 rounded overflow-hidden gap-px">
        {Object.entries(counts).map(([k, v]) => (
          <div key={k} style={{ width: `${(v / total) * 100}%`, background: colors[k] || "#475569" }} title={`${k}: ${v}`} />
        ))}
      </div>
      <div className="flex flex-wrap gap-x-3 gap-y-0.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="text-xs text-slate-400">
            <span style={{ color: colors[k] || "#94a3b8" }}>■</span> {k} {v}
          </span>
        ))}
      </div>
    </div>
  );
}

function DetailModal({ zone, onClose }: { zone: Zone; onClose: () => void }) {
  const [tab, setTab] = useState<"scores" | "signal" | "action">("scores");
  useEffect(() => {
    const h = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", h);
    return () => window.removeEventListener("keydown", h);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <div className="bg-slate-900 border border-blue-600/30 rounded-xl w-full max-w-lg p-6 shadow-2xl" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-lg font-bold text-white">{zone.zone_id}</span>
            <span className="ml-2 text-green-400 text-xs">{zone.region}</span>
            <p className="text-xs text-slate-400 mt-0.5 capitalize">{zone.ecosystem_type.replace(/_/g, " ")}</p>
          </div>
          <button onClick={onClose} className="text-slate-500 hover:text-white text-xl leading-none">✕</button>
        </div>

        <div className="flex gap-2 mb-4">
          {(["scores", "signal", "action"] as const).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-3 py-1 rounded text-xs font-medium transition-colors ${tab === t ? "bg-green-700 text-white" : "bg-slate-800 text-slate-400 hover:text-white"}`}>
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </button>
          ))}
        </div>

        {tab === "scores" && (
          <div className="grid grid-cols-2 gap-3 text-sm">
            {([
              ["Boundary",    zone.boundary_score,    "#ef4444"],
              ["Biodiversity",zone.biodiversity_score,"#a855f7"],
              ["Degradation", zone.degradation_score, "#f97316"],
              ["Exposure",    zone.exposure_score,    "#3b82f6"],
            ] as [string, number, string][]).map(([l, v, c]) => (
              <div key={l} className="bg-slate-800 rounded-lg p-3">
                <div className="text-slate-400 text-xs mb-1">{l}</div>
                <div className="text-white font-bold text-lg">{v.toFixed(1)}</div>
                <div className="h-1.5 rounded mt-1 bg-slate-700">
                  <div className="h-1.5 rounded" style={{ width: `${Math.min(v, 100)}%`, background: c }} />
                </div>
              </div>
            ))}
            <div className="col-span-2 bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Planetary Risk Composite</div>
              <div className="text-white font-bold text-2xl">{zone.planetary_risk_composite.toFixed(1)}</div>
            </div>
          </div>
        )}

        {tab === "signal" && (
          <div className="bg-slate-800 rounded-lg p-4 text-sm text-slate-200 leading-relaxed">
            {zone.ecosystem_signal}
            <div className="mt-3 flex gap-2 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[zone.planetary_risk] || "bg-slate-700 text-slate-300"}`}>{zone.planetary_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[zone.ecosystem_severity] || "bg-slate-700 text-slate-300"}`}>{zone.ecosystem_severity}</span>
            </div>
          </div>
        )}

        {tab === "action" && (
          <div className="space-y-3 text-sm">
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Recommended Action</div>
              <div className="text-green-400 font-medium">{zone.recommended_action.replace(/_/g, " ")}</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Planetary Risk Index</div>
              <div className="text-white font-bold">{zone.estimated_planetary_risk_index.toFixed(2)} / 10</div>
            </div>
            <div className="bg-slate-800 rounded-lg p-3">
              <div className="text-slate-400 text-xs mb-1">Ecosystem Pattern</div>
              <div className="text-slate-200 capitalize">{zone.ecosystem_pattern.replace(/_/g, " ")}</div>
            </div>
            <div className="flex gap-2">
              {zone.is_tipping_point_risk            && <span className="px-2 py-1 rounded bg-amber-900 text-amber-300 text-xs font-medium">TIPPING RISK</span>}
              {zone.requires_emergency_intervention  && <span className="px-2 py-1 rounded bg-red-900 text-red-300 text-xs font-medium">EMERGENCY</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function PlanetaryIntelligenceDashboard() {
  const [data, setData]         = useState<{ zones: Zone[]; summary: Summary } | null>(null);
  const [riskFilter, setRisk]   = useState("all");
  const [patFilter, setPat]     = useState("all");
  const [selected, setSelected] = useState<Zone | null>(null);

  useEffect(() => {
    fetch("/api/planetary-intelligence-engine")
      .then(r => r.json()).then(setData).catch(console.error);
  }, []);

  if (!data) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="text-green-400 text-lg animate-pulse">Loading Planetary Intelligence Engine...</div>
    </div>
  );

  const { zones, summary } = data;
  const filtered = zones.filter(z =>
    (riskFilter === "all" || z.planetary_risk === riskFilter) &&
    (patFilter  === "all" || z.ecosystem_pattern === patFilter)
  );

  const kpis = [
    { label: "Zones Monitored",  value: summary.total,                                                  accent: "text-green-400" },
    { label: "Avg Risk Composite",value: summary.avg_planetary_risk_composite.toFixed(1),              accent: "text-teal-400"  },
    { label: "Tipping Risk",      value: summary.tipping_point_risk_count,                             accent: "text-amber-400" },
    { label: "Emergency Zones",   value: summary.emergency_intervention_count,                         accent: "text-red-400"   },
    { label: "Avg Risk Index",    value: `${summary.avg_estimated_planetary_risk_index.toFixed(2)}/10`,accent: "text-green-400" },
    { label: "Avg Boundary",      value: Math.round(summary.avg_boundary_score),                       accent: "text-blue-400"  },
  ];

  const dists: Array<{ title: string; counts: Record<string, number>; colors: Record<string, string> }> = [
    { title: "Risk",     counts: summary.risk_counts,     colors: RISK_COLORS },
    { title: "Pattern",  counts: summary.pattern_counts,  colors: PAT_COLORS  },
    { title: "Severity", counts: summary.severity_counts, colors: SEV_COLORS  },
    { title: "Action",   counts: summary.action_counts,   colors: ACT_COLORS  },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 space-y-6">
      {selected && <DetailModal zone={selected} onClose={() => setSelected(null)} />}

      <div>
        <h1 className="text-2xl font-bold text-white">Planetary Intelligence & Ecosystem Risk Monitoring</h1>
        <p className="text-slate-400 text-sm mt-1">
          Planetary boundaries · Tipping points · Biodiversity intelligence · Climate risk exposure
        </p>
      </div>

      {/* 6 KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {kpis.map(k => (
          <div key={k.label} className="bg-slate-900 border border-blue-600/30 rounded-xl p-3 text-center">
            <div className={`text-xl font-bold ${k.accent}`}>{k.value}</div>
            <div className="text-xs text-slate-500 mt-0.5">{k.label}</div>
          </div>
        ))}
      </div>

      {/* 4 GaugeRings */}
      <div className="bg-slate-900 border border-blue-600/30 rounded-xl p-5">
        <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-4">Average Sub-Scores</h2>
        <div className="grid grid-cols-4 gap-4">
          <GaugeRing value={summary.avg_boundary_score}     label="Boundary"     color="#ef4444" />
          <GaugeRing value={summary.avg_biodiversity_score} label="Biodiversity" color="#a855f7" />
          <GaugeRing value={summary.avg_degradation_score}  label="Degradation"  color="#f97316" />
          <GaugeRing value={summary.avg_exposure_score}     label="Exposure"     color="#3b82f6" />
        </div>
      </div>

      {/* 4 DistBars */}
      <div className="bg-slate-900 border border-blue-600/30 rounded-xl p-5 grid grid-cols-1 md:grid-cols-2 gap-5">
        {dists.map(d => <DistBar key={d.title} {...d} />)}
      </div>

      {/* Filter Pills */}
      <div className="flex flex-wrap gap-2">
        {["all", "low", "moderate", "high", "critical"].map(r => (
          <button key={r} onClick={() => setRisk(r)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${riskFilter === r ? "bg-green-700 border-green-600 text-white" : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {r}
          </button>
        ))}
        <span className="w-px h-5 self-center bg-slate-700" />
        {["all", "none", "tipping_point_breach", "biodiversity_collapse", "carbon_crisis", "water_system_failure", "ecosystem_fragmentation"].map(p => (
          <button key={p} onClick={() => setPat(p)}
            className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${patFilter === p ? "bg-teal-900 border-teal-800 text-white" : "bg-slate-900 border-slate-700 text-slate-400 hover:text-white"}`}>
            {p.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Zone Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filtered.map(z => (
          <div key={z.zone_id} onClick={() => setSelected(z)}
            className="bg-slate-900 border border-blue-600/30 rounded-xl p-4 cursor-pointer hover:border-green-600 transition-colors">
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-white">{z.zone_id}</span>
              <span className="text-xs text-slate-400">{z.region}</span>
            </div>
            <p className="text-xs text-slate-500 mb-2 capitalize">{z.ecosystem_type.replace(/_/g, " ")}</p>
            <div className="flex gap-1 mb-3 flex-wrap">
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${RISK_BADGE[z.planetary_risk] || "bg-slate-700 text-slate-300"}`}>{z.planetary_risk}</span>
              <span className={`px-2 py-0.5 rounded text-xs font-medium ${SEV_BADGE[z.ecosystem_severity] || "bg-slate-700 text-slate-300"}`}>{z.ecosystem_severity}</span>
            </div>
            <div className="text-2xl font-black text-white mb-1">{z.planetary_risk_composite.toFixed(1)}</div>
            <div className="text-xs text-slate-500 mb-2 capitalize">{z.ecosystem_pattern.replace(/_/g, " ")}</div>
            <div className="text-xs text-green-400 font-medium mb-2">Risk Index: {z.estimated_planetary_risk_index.toFixed(2)}/10</div>
            <div className="flex gap-1 flex-wrap">
              {z.is_tipping_point_risk           && <span className="px-1.5 py-0.5 rounded bg-amber-900 text-amber-300 text-xs">TIPPING</span>}
              {z.requires_emergency_intervention && <span className="px-1.5 py-0.5 rounded bg-red-900 text-red-300 text-xs">EMERGENCY</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
